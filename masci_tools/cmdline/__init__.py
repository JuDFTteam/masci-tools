# -*- coding: utf-8 -*-

import click
import click_completion

#from .parse import cmd_parse
#from .fleur_schema import cmd_fleur_schema
from .plot import cmd_plot

# Activate the completion of parameter types provided by the click_completion package
# for bash: eval "$(_MASCI_TOOLS_COMPLETE=source masci-tools)"
click_completion.init()


def print_version(ctx, param, value):
    from masci_tools import __version__
    if not value or ctx.resilient_parsing:
        return
    click.echo(f'Version {__version__}')
    ctx.exit()


@click.group('masci-tools', context_settings={'help_option_names': ['-h', '--help']})
@click.option('--version',
              '-v',
              is_flag=True,
              callback=print_version,
              expose_value=False,
              is_eager=True,
              help='Print the current version of the `masci-tools` library and exit')
def cmd_root():
    """CLI for the `masci-tools` library."""


#cmd_root.add_command(cmd_parse)
#cmd_root.add_command(cmd_fleur_schema)
cmd_root.add_command(cmd_plot)
