# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of tcmReceiver (https://github.com/seeraven/tcmReceiver)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
#
"""Unit tests of the tcm_receiver.serial_ifc module."""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
from unittest import TestCase

from tcm_receiver.serial_ifc import get_serial


# -----------------------------------------------------------------------------
# Test Class
# -----------------------------------------------------------------------------
class SerialIfcTest(TestCase):
    """Test the :function:`tcm_receiver.serial_ifc.get_serial` function."""

    def test_dev_null(self):
        """tcm_receiver.serial_ifc.get_serial: Use /dev/null."""
        # pylint: disable=missing-class-docstring,too-few-public-methods
        class TestArgs:
            pass
        args = TestArgs()
        # pylint: disable=attribute-defined-outside-init
        args.device = '/dev/null'
        serial_dev = get_serial(args)
        self.assertEqual(serial_dev, None)


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
