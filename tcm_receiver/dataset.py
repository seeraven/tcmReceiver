# -*- coding: utf-8 -*-
"""
Module defining the dataset.

Copyright:
    2021 by Clemens Rabe <clemens.rabe@clemensrabe.de>

    All rights reserved.

    This file is part of tcmReceiver (https://github.com/seeraven/tcmReceiver)
    and is released under the "BSD 3-Clause License". Please see the ``LICENSE`` file
    that is included as part of this package.
"""


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------
# pylint: disable=too-few-public-methods
class Dataset:
    """Dataset encapsulating the data record of the TCM temperature sensor."""

    def __init__(self, channel, battery_low, id_nr, temperature):
        """Construct a new dataset."""
        self.channel = int(channel)
        self.id = int(id_nr)
        self.battery_low = bool(battery_low)
        self.temperature = float(temperature)

    def __str__(self):
        """Return the string representation of the object."""
        ret = "Dataset: "
        ret += "Channel=%s, " % self.channel
        ret += "ID=%s, " % self.id
        ret += "BatteryLow=%s, " % self.battery_low
        ret += "Temperature=%f" % self.temperature
        return ret


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
