"""
This module is only here for backwards compatibility
"""
import warnings

warnings.warn('The fleur_schema module was moved from masci_tools.io.parsers.fleur'
              'to masci_tools.io.parsers', DeprecationWarning)

from masci_tools.io.parsers.fleur_schema import *
