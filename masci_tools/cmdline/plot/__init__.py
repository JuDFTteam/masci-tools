# -*- coding: utf-8 -*-

import click

from .plot import plot_fleur_banddos_bands
from .plot import plot_fleur_banddos_dos


@click.group('plot')
def cmd_plot():
    """ Commands for visulaizing data """


cmd_plot.add_command(plot_fleur_banddos_bands)
cmd_plot.add_command(plot_fleur_banddos_dos)
