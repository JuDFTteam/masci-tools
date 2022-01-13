"""
This module provides a place for registering click commands from the tools subpackage
into the main cli
"""
from .root import cli
from masci_tools.tools.fleur_inpxml_converter import inpxml

cli.add_command(inpxml)
