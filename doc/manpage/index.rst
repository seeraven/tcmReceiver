tcmReceiver
===========

Synopsis
--------

tcmReceiver [-h|--help] [-d DEVICE] [-c DATAFILE] [-i DATAFILE] capture OUTPUT_FILE

tcmReceiver [-h|--help] [-d DEVICE] [-c DATAFILE] [-i DATAFILE] print

tcmReceiver [-h|--help] [-d DEVICE] [-c DATAFILE] [-i DATAFILE] publish [--mqtt-host MQTT_HOST] [--mqtt-port MQTT_PORT] [--mqtt-username MQTT_USERNAME] [--mqtt-password MQTT_PASSWORD] [--mqtt-topics MQTT_TOPICS]


Description
-----------

Arduino program and python readout script to receive temperature information of
a 433 MHz temperature sensor and publish it via MQTT.


Options of tcmReceiver
----------------------

-h, --help                          Show the general help.
-d DEVICE, --device DEVICE          The serial port device to open. Default: :code:`/dev/ttyUSB0`.
-c DATAFILE, --capture DATAFILE     Capture raw data from the serial port and store it in the given file.
-i DATAFILE, --input-file DATAFILE  Instead of using a serial port, read the data from the specified data
                                    file (previously captured using the :code:`-c` option).
--mqtt-host MQTT_HOST               MQTT host. [Default: :code:`192.168.1.70`]
--mqtt-port MQTT_PORT               MQTT port. [Default: :code:`1883`]
--mqtt-username MQTT_USERNAME       MQTT username. [Default: :code:`mqtt`]
--mqtt-password MQTT_PASSWORD       MQTT password. [Default: :code:`mqtt`]
--mqtt-topics MQTT_TOPICS           Comma separated list of channel number and the corresponding MQTT topic. The suffix '/temperature' resp. '/battery_low' is added automatically. [Default: :code:`1=tcm/channel1`]


Examples
--------

- Capture from the serial line for further investigation::

      $ tcmReceiver -d /dev/ttyUSB0 capture testdata.dat

- Replay the data from the test data and print it on stdout::

      $ tcmReceiver -i testdata.dat print

- Read from the serial port and publish the data received on channels 1 and 2::

      $ tcmReceiver -d /dev/ttyUSB1 publish --mqtt-topics '1=tcm/garden,2=tcm/garage'


License
-------

tcmReceiver (https://github.com/seeraven/tcmReceiver) is released under the
"BSD 3-Clause License". Please see the LICENSE file that is included as part of this package.
