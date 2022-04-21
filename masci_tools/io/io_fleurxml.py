"""
This module is only here for backwards compatibility
"""
import warnings

warnings.warn('The io_fleurxml module was renamed to fleur_xml.\n'
              'Import is now masci_tools.io.fleur_xml', DeprecationWarning)

from .fleur_xml import *  #pylint: disable=unused-wildcard-import
