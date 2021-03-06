#!/bin/bash -e
# ----------------------------------------------------------------------------
# Check the capture subcommand with an invalid capture device argument.
#
# Copyright (c) 2021 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of tcmReceiver (https://github.com/seeraven/tcmReceiver)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
# ----------------------------------------------------------------------------


EXPECTED_OUTPUT_PREFIX=$(basename $0 .sh)
source $TEST_BASE_DIR/helpers/output_helpers.sh


# -----------------------------------------------------------------------------
# Tests:
#   - Test the call without an invalid serial device that has a return code of 1.
# -----------------------------------------------------------------------------
capture_output_failure call -d /dev/do_not_exists capture /tmp/tcmReceiver.raw


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
