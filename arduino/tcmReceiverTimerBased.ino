/*
 * TCM Temperature Receiver
 *
 * (c) 2020 by Clemens Rabe
 */

/// Receiver connected to Arduino PIN 2.
#define DATA_PIN 2

/// Duration of a single pulse in microseconds.
#define TCM_PULSE_MUS 2000

/// Number of samples per pulse.
#define SAMPLES_PER_PULSE 8

/// Desired timer frequency in Hz (Number of samples / Pulse Length)
#define TIMER_FREQUENCY (SAMPLES_PER_PULSE * 1000000 / TCM_PULSE_MUS)

/*
 * Prescaler values:
 *  Prescaler | Timer Speed | CMR 
 *  ----------+-------------+---------
 *       1    |     16 MHz  | 3999
 *       8    |      2 MHz  |  499
 *       64   |    250 KHz  |   61.5
 *       256  |   62.5 KHz  |   14.63
 *       1024 | 15.625 KHz  |    2.91
 */

/// Prescaler value to reduce 16 MHz to 2 MHz
#define TIMER_PRESCALER_VALUE 8

/// Compare match register to achieve TIMER_FREQUENCY ((16 MHz / (TIMER_PRESCALER_VALUE * TIMER_FREQUENCY)) - 1)
#define TIMER_COMPARE_MATCH_REGISTER_VALUE 499

/// Phase-Locked-Loop (PLL) length.
#define PLL_RAMP_LEN         160

/// Phase-Locked-Loop (PLL) default increment.
#define PLL_RAMP_INC         (PLL_RAMP_LEN / SAMPLES_PER_PULSE)

/// Phase-Locked-Loop (PLL) adjustment threshold.
#define PLL_RAMP_TRANSITION  (PLL_RAMP_LEN / 2)

/// Phase-Locked-Loop (PLL) adjustment on signal change.
#define PLL_RAMP_ADJUST      9

/// Phase-Locked-Loop (PLL) increment on signal change in first half.
#define PLL_RAMP_INC_RETARD  (PLL_RAMP_INC - PLL_RAMP_ADJUST)

/// Phase-Locked-Loop (PLL) increment on signal change in second half.
#define PLL_RAMP_INC_ADVANCE (PLL_RAMP_INC + PLL_RAMP_ADJUST)


/// Number of high states per pulse sampling.
volatile uint8_t g_pulseNumHighStates_ui = 0;

/// Last pin state during pulse sampling.
volatile bool    g_lastPinState_b = false;

/// Flag indicating the start of a bit
volatile uint8_t g_pllPulseStart_i = 1;

/// PLL ramp value.
volatile uint8_t g_pllRamp_ui = 0;

/// Pulse bits ring buffer.
volatile uint8_t g_pulseBits_ui[256];

/// Write index in g_pulseBits_ui ring buffer.
volatile uint8_t g_writeIdx_ui = 0;

/// Read index in g_pulseBits_ui ring buffer.
volatile uint8_t g_readIdx_ui = 0;


/**
 * Timer Interrupt Handler.
 */
ISR(TIMER1_COMPA_vect){
  const bool pinIsHigh_b = ((PIND & (1 << DATA_PIN)) == (1 << DATA_PIN));

  if (pinIsHigh_b) {
    ++g_pulseNumHighStates_ui;
  }

  if (pinIsHigh_b != g_lastPinState_b) {
    if (g_pllPulseStart_i) {
      g_pllRamp_ui += PLL_RAMP_INC;
    } else {
      g_pllRamp_ui += ((g_pllRamp_ui < PLL_RAMP_TRANSITION)?PLL_RAMP_INC_RETARD:PLL_RAMP_INC_ADVANCE);
    }
    g_lastPinState_b = pinIsHigh_b;
  } else {
    g_pllRamp_ui += PLL_RAMP_INC;
  }
  g_pllPulseStart_i = 0;

  // If we have enough samples of the pulse
  if (g_pllRamp_ui >= PLL_RAMP_LEN) {    
    // Count the pulse as high if at least 5 of 8 samples vote for high
    if (g_pulseNumHighStates_ui >= 5) {
      g_pulseBits_ui[g_writeIdx_ui++] = 1;
    } else {
      g_pulseBits_ui[g_writeIdx_ui++] = 0;
    }

    g_pllRamp_ui -= PLL_RAMP_LEN;
    g_pulseNumHighStates_ui = 0;
    g_pllPulseStart_i = 1;
  }
}


void setup() {
  Serial.begin(9600);
  Serial.println("TCM Temperature Sensor Receiver");
  pinMode(DATA_PIN, INPUT);

  // Setup timer interrupt
  cli();

  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1  = 0;                          //initialize counter value to 0
  OCR1A  = TIMER_COMPARE_MATCH_REGISTER_VALUE;
  TCCR1B |= (1 << WGM12);              // turn on CTC mode
  TCCR1B |= (1 << CS11);               // set CS11 bit for 8 prescaler
  TIMSK1 |= (1 << OCIE1A);             // enable timer compare interrupt

  sei();                               // enable interrupts
}

uint8_t pulsesToBit(uint8_t f_firstIdx_ui) {
  const uint8_t first_ui  = g_pulseBits_ui[f_firstIdx_ui++];
  const uint8_t second_ui = g_pulseBits_ui[f_firstIdx_ui++];
  const uint8_t third_ui  = g_pulseBits_ui[f_firstIdx_ui];

  if ((first_ui == 0) && (second_ui == 1) && (third_ui == 0)) {
    return 0;
  } else if ((first_ui == 1) && (second_ui == 1) && (third_ui == 0)) {
    return 1;
  }

  return 2;
}

int decodePllBitSequence() {
  // First element must be a low pulse
  if (g_pulseBits_ui[g_readIdx_ui] != 0) {
    return 0;
  }

  // Decode first 24 bits, then the next 24 bits
  uint32_t firstBits_ui = 0;
  uint32_t secondBits_ui = 0;

  for (uint8_t bitNr_ui = 0; bitNr_ui < 24; ++bitNr_ui) {
    const uint8_t bit_ui = pulsesToBit(g_readIdx_ui + 1 + (3*bitNr_ui));
    if (bit_ui == 2) {
      return 0;
    }
    firstBits_ui = (firstBits_ui << 1) | bit_ui;
  }
  
  for (uint8_t bitNr_ui = 0; bitNr_ui < 24; ++bitNr_ui) {
    const uint8_t bit_ui = pulsesToBit(g_readIdx_ui + 1 + (3*24) + (3*bitNr_ui));
    if (bit_ui == 2) {
      return 0;
    }
    secondBits_ui = (secondBits_ui << 1) | bit_ui;
  }

  // Second bits must be inverse of first bits
  if (((firstBits_ui ^ secondBits_ui) & 0xffffff) != 0xffffff) {
    return 0;
  }

  // First two bits must be zero, 5th and 6th bit must be 1
  if ((firstBits_ui & 0xcc0000) != 0x0c0000) {
    return 0;
  }

  // Decode it according to
  //       16   12   8    4   0
  // 00CC11SB IIIITTTT OOOODDDD
  const uint8_t channel_ui = (firstBits_ui & 0x300000) >> 20;
  const uint8_t sign_ui    = (firstBits_ui & 0x020000) >> 17;
  const uint8_t battery_ui = (firstBits_ui & 0x010000) >> 16;
  const uint8_t ident_ui   = (firstBits_ui & 0x00f000) >> 12;
  const uint8_t tens_ui    = (firstBits_ui & 0x000f00) >> 8;
  const uint8_t ones_ui    = (firstBits_ui & 0x0000f0) >> 4;
  const uint8_t decis_ui   = (firstBits_ui & 0x00000f);

  float temp_f = float(tens_ui) * 10.0f + float(ones_ui) * 1.0f + float(decis_ui) * 0.1f;
  if (sign_ui) {
    temp_f *= -1.0f;
  }

  Serial.print("Channel=");
  Serial.print(int(channel_ui));
  Serial.print(" Battery=");
  Serial.print(int(battery_ui));
  Serial.print(" ID=");
  Serial.print(int(ident_ui));
  Serial.print(" Temp=");
  Serial.println(temp_f);
  
  return 1;
}

void loop() {
  const uint8_t bufferSize_ui = g_writeIdx_ui - g_readIdx_ui;

  if (bufferSize_ui >= 145) {
    if (decodePllBitSequence()) {
      g_readIdx_ui += 145;
    } else {
      ++g_readIdx_ui;
    }
  }
}
