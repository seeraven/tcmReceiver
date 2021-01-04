tcmReceiver
===========

Arduino program and python readout script to receive temperature information of
a 433 MHz temperature sensor and publish it via MQTT.


Hardware Interface
------------------

The hardware interface consists of a 433 MHz receiver connected to the D2 input
of the Arduino.


Arduino Setup
-------------

Flash the sketch `arduino/tcmReceiverTimerBased.ino` to the Arduino. Then open
a minicom session at 9600 Baud 8N1 and check the output. It should look like

```
```


Software Installation
---------------------

tcmReceiver is distributed as a single executable packaged using [pyInstaller].
So all you have to do is to download the latest executable and copy it to a
location of your choice, for example `/usr/local/bin`:

    wget https://github.com/seeraven/tcmReceiver/releases/download/v1.0.0/tcmReceiver_Ubuntu18.04_amd64
    chmod +x tcmReceiver_Ubuntu18.04_amd64
    sudo mv tcmReceiver_Ubuntu18.04_amd64 /usr/local/bin/tcmReceiver


Debugging the Protocol
----------------------

For debugging the raw protocol sent over the serial line, you can first capture
a data file by calling:

    tcmReceiver -c raw_data.dat

And then analyse it by using it as an input file:

    tcmReceiver -i raw_data.dat


[pyInstaller]: https://www.pyinstaller.org/
