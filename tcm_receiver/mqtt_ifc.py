# -*- coding: utf-8 -*-
"""
Module providing the mqtt interface of the tcmReceiver application.

Copyright:
    2021 by Clemens Rabe <clemens.rabe@clemensrabe.de>

    All rights reserved.

    This file is part of tcmReceiver (https://github.com/seeraven/tcmReceiver)
    and is released under the "BSD 3-Clause License". Please see the ``LICENSE`` file
    that is included as part of this package.
"""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import time

import paho.mqtt.client as mqtt


# -----------------------------------------------------------------------------
# Class Definitions
# -----------------------------------------------------------------------------
class MqttInterface:
    """This class represents the MQTT interface to send the current values."""

    def __init__(self, args):
        """Construct a new MqttInterface object.

        Args:
            args (obj): The arguments object.
        """
        self.topics = {}
        for item in args.mqtt_topics.split(','):
            if item.count('=') == 1:
                channel, topic = item.split('=')
                self.topics[channel] = topic
            else:
                print("ERROR: Ignoring MQTT item %s. "
                      "Please use <Channel>=<MQTT Topic> items!" % item)

        self.client = mqtt.Client("tcmReceiver")
        self.client.username_pw_set(args.mqtt_username, args.mqtt_password)
        self.client.connect_async(args.mqtt_host, args.mqtt_port)
        self.client.loop_start()

        # To allow the client to connect to the broker
        time.sleep(1)

    def close(self):
        """Close the connection."""
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, dataset):
        """Publish a new value.

        Args:
            dataset (obj): The dataset to publish.
        """
        if str(dataset.channel) in self.topics:
            ret = self.client.publish(self.topics[str(dataset.channel)] + '/temperature',
                                      dataset.temperature)
            if ret.rc == mqtt.MQTT_ERR_NO_CONN:
                print("ERROR: MQTT Client is not connected!")
            elif ret.rc == mqtt.MQTT_ERR_QUEUE_SIZE:
                print("ERROR: MQTT Client queue size exceeded!")

            ret = self.client.publish(self.topics[str(dataset.channel)] + '/battery_low',
                                      1 if dataset.battery_low else 0)
            if ret.rc == mqtt.MQTT_ERR_NO_CONN:
                print("ERROR: MQTT Client is not connected!")
            elif ret.rc == mqtt.MQTT_ERR_QUEUE_SIZE:
                print("ERROR: MQTT Client queue size exceeded!")

        else:
            print("WARNING: Ignoring %s" % dataset)


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
