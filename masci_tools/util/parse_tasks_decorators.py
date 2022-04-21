###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools.   #
# For further information on the license, see the LICENSE.txt file.           #
# For further information please visit http://judft.de/.                      #
#                                                                             #
###############################################################################
"""
This module defines decorators for the _TaskParser class to make extending/modifying the parser
more convenient

Up till now 3 decorators are defined:
    - ```register_migration``` marks a function of making backwards incompatible changes
      to the parsing tasks
    - ```register_parsing_function``` gives a mappimg between available parsing functions
      and the keywords in the parsing tasks
    - ```conversion_function``` makes the decorated function available to be called easily
      after a certain parsing task has occurred
"""
from masci_tools.io.parsers.fleur import conversion_function, register_migration
import warnings

warnings.warn('The decorators for the outxml_parser were moved to masci_tools.io.parsers.fleur', DeprecationWarning)
