"""
Main module defining the CLI for parts of the masci-tools repository
"""
import click
import click_completion
from masci_tools import __version__

click_completion.init()

# Activate the completion of parameter types provided by the click_completion package
# for bash: eval "$(_MASCI_TOOLS_COMPLETE=source masci-tools)"


@click.group('masci-tools', context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(__version__, '-v', '--version', message='masci-tools version %(version)s')
def cli():
    """CLI for the `masci-tools` library."""
