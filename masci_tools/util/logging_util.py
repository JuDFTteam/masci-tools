# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), 2018 Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.    #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools    #
# For further information on the license, see the LICENSE.txt file            #
#                                                                             #
###############################################################################
"""
This module defines useful utility for logging related functionality
"""
from logging import Handler


class DictHandler(Handler):
    """
    Custom Handler for the logging module inserting logging messages
    into a given dictionary.

    Messages are grouped into list under the names of the error categories.
    Keyword arguments can be used to modify the keys for the different levels
    """

    def __init__(self, log_dict, **kwargs):
        from logging import _levelToName
        import copy

        self.log_dict = log_dict

        levels = copy.copy(list(_levelToName.values()))
        levels.remove('NOTSET')

        self.level_names = {name: name if name not in kwargs else kwargs[name] for name in levels}

        for name in self.level_names.values():
            self.log_dict[name] = []

        super().__init__()

    def emit(self, record):
        """
        Emit a record.
        """
        try:
            msg = self.format(record)
            entry_name = self.level_names.get(record.levelname, 'NOTSET')
            if entry_name not in self.log_dict:
                self.log_dict[entry_name] = []

            self.log_dict[entry_name].append(msg)
        except Exception:  #pylint: disable=broad-except
            self.handleError(record)

    def __repr__(self):
        from logging import getLevelName
        level = getLevelName(self.level)
        return '<%s (%s)>' % (self.__class__.__name__, level)
