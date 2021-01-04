# -*- coding: utf-8 -*-
"""
Module handling the command line interface of the tcmReceiver application.

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
import argparse

from .capture_cmd import add_capture_parser
from .print_cmd import add_print_parser
from .publish_cmd import add_publish_parser


# -----------------------------------------------------------------------------
# Module Variables
# -----------------------------------------------------------------------------
DESCRIPTION = """
TcmReceiver
===========

Python based application to analyze the data of a 433 MHz thermometer received
using an Arduino. The extracted data is sent via MQTT.

This command provides the following subcommands:
  - "capture" to capture raw data from the serial port and save it in a file.
    This helps development and debugging this application.
  - "print" to parse the data from the serial port or a previously recorded
    file and print the results on stdout.
  - "publish" to parse the data from the serial port or a previously recorded
    file and publish the mqtt messages.

See the help of the individual subcommands for more information and the
command line options.
"""


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------
def get_parser():
    """Get the argument parser for the :code:`tcmReceiver` command."""
    parser = argparse.ArgumentParser(description=DESCRIPTION,
                                     formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers()

    # Options for all commands
    parser.add_argument("-d", "--device",
                        help="The serial port device to open. Default: %(default)s.",
                        action="store",
                        default="/dev/ttyUSB0")
    parser.add_argument("-i", "--input-file",
                        metavar="DATAFILE",
                        help="Instead of using a serial port, read the data from "
                        "the specified data file (previously captured using the -c option).",
                        action="store",
                        default=None)

    # Add commands
    add_capture_parser(subparsers)
    add_print_parser(subparsers)
    add_publish_parser(subparsers)

    return parser


def tcm_receiver():
    """Execute the main function if called as :code:`tcmReceiver`.

    Return:
        Returns True on success, otherwise False.
    """
    parser = get_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        return args.func(args)

    parser.error("Please specify a subcommand!")
    return False


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
