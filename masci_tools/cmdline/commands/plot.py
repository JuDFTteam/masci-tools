"""
Commands for plotting
"""
from .root import cli
import click

from masci_tools.cmdline.utils import echo


@cli.group('plot')
def plot():
    """Commands for visualizing data"""


@plot.command('fleur-bands')
@click.argument('banddos-file', type=click.Path(exists=True))
@click.option('--weight', '-w', type=str, default=None)
@click.option('--backend', type=click.Choice(['matplotlib', 'mpl', 'bokeh']), default='matplotlib')
@click.option('--save', is_flag=True)
@click.option('--show', is_flag=True)
@click.option('--recipe',
              '-r',
              type=click.Choice(
                  ['FleurBands', 'FleurOrbcompBands', 'FleurjDOSBands', 'FleurSimpleBands', 'FleurMCDBands']),
              default='FleurBands')
def plot_fleur_banddos_bands(banddos_file, weight, recipe, backend, save, show):
    """
    Plot bandstructures from the banddos.hdf file from Fleur
    """
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5 import recipes

    from masci_tools.vis.fleur import plot_fleur_bands

    try:
        recipe = getattr(recipes, recipe)
    except AttributeError:
        echo.echo_critical(f'The recipe {recipe} does not exist')

    if not show and not save:
        show = True

    with HDF5Reader(banddos_file) as h5reader:
        data, attributes = h5reader.read(recipe=recipe)

    plot_fleur_bands(data, attributes, weight=weight, backend=backend, show=show, save_plots=save)


@plot.command('fleur-dos')
@click.argument('banddos-file', type=click.Path(exists=True))
@click.option('--total', type=bool, default=True)
@click.option('--interstitial', type=bool, default=True)
@click.option('--atoms', default='all')
@click.option('--l_resolved', default=None)
@click.option('--backend', type=click.Choice(['matplotlib', 'mpl', 'bokeh']), default='matplotlib')
@click.option('--save', is_flag=True)
@click.option('--show', is_flag=True)
@click.option('--recipe',
              '-r',
              type=click.Choice(['FleurDOS', 'FleurORBCOMP', 'FleurJDOS', 'FleurMCD']),
              default='FleurDOS')
def plot_fleur_banddos_dos(banddos_file, total, interstitial, atoms, l_resolved, recipe, backend, save, show):
    """
    Plot density of states from the banddos.hdf file from Fleur
    """
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5 import recipes

    from masci_tools.vis.fleur import plot_fleur_dos

    try:
        recipe = getattr(recipes, recipe)
    except AttributeError:
        echo.echo_critical(f'The recipe {recipe} does not exist')
    if not show and not save:
        show = True

    with HDF5Reader(banddos_file) as h5reader:
        data, attributes = h5reader.read(recipe=recipe)

    plot_fleur_dos(data,
                   attributes,
                   show_total=total,
                   show_interstitial=interstitial,
                   show_atoms=atoms,
                   show_lresolved=l_resolved,
                   backend=backend,
                   show=show,
                   save_plots=save)
