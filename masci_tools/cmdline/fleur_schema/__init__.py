# -*- coding: utf-8 -*-

import click

from .fleur_schema import add_fleur_schema
from .fleur_schema import validate_inpxmlfile
from .fleur_schema import validate_outxmlfile


@click.group('fleur-schema')
def cmd_fleur_schema():
    """Commands related to the Fleur XML Schemas"""


cmd_fleur_schema.add_command(add_fleur_schema)
cmd_fleur_schema.add_command(validate_inpxmlfile)
cmd_fleur_schema.add_command(validate_outxmlfile)
