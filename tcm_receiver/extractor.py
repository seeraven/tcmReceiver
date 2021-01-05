# -*- coding: utf-8 -*-
"""
Module handling the extraction of datasets from the raw data input.

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
import re

from .dataset import Dataset


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------
# pylint: disable=too-few-public-methods
class Extractor:
    """Extractor for datasets from byte stream."""

    def __init__(self):
        """Construct a new extractor object."""
        self.buffer = b''
        self.pattern = re.compile(r'Channel=([0-9]*) Battery=([0-9]) ID=([0-9]*) Temp=([0-9.-]*)')

    def add_bytes(self, new_bytes):
        """Add the given bytes to the internal buffer and check for complete messages.

        Args:
            new_bytes (bytes): The bytes to add.

        Return:
            Returns a list of extracted Dataset records. The list might be empty.
        """
        self.buffer += new_bytes
        datasets = []

        while b'\n' in self.buffer:
            end_index = self.buffer.find(b'\n')
            line = self.buffer[:end_index].strip()
            match = self.pattern.match(line.decode())
            if match:
                try:
                    datasets.append(Dataset(match.group(1),
                                            match.group(2),
                                            match.group(3),
                                            match.group(4)))
                # pylint: disable=bare-except
                except:                              # noqa
                    print("ERROR: Can't create dataset from line %s." % match.group(0))
            self.buffer = self.buffer[end_index+1:]

        return datasets


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
