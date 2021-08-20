# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools    #
# For further information on the license, see the LICENSE.txt file            #
# For further information please visit http://www.flapw.de or                 #
#                                                                             #
###############################################################################
"""
This modules provides common plotting functions dispatching to
different plotting backends. At the moment the following backends are used:

* ``matplotlib`` ('mpl', 'matplotlib')
* ``bokeh`` ('bokeh')

The underlying plotting routines collected here should have the same
signature for the data arguments; keyword arguments can be different.
"""
from enum import Enum

__all__ = (
    'set_default_backend',
    'PlotBackend',
    'set_defaults',
    'reset_defaults',
    'show_defaults',
    'save_defaults',
    'load_defaults',
    'get_help',
    'get_plotter',
    'dos',
    'spinpol_dos',
    'bands',
    'spinpol_bands',
    'scatter',
    'line',
)

_DEFAULT_BACKEND = 'mpl'


def set_default_backend(backend):
    """
    Sets the default backend used when no explicit backend is specified.

    :param backend: Name of the backend to use
    """
    global _DEFAULT_BACKEND  #pylint: disable=global-statement
    backend = PlotBackend.from_str(backend)
    _DEFAULT_BACKEND = backend.value


class PlotBackend(Enum):
    """
    Enumeration containing the possible names for each plotting backend
    Initialize using the :py:meth:`from_str()` method

    At the moment the following are supported (case-insensitive)

    * ``matplotlib``: either `'mpl'` or `'matplotlib'`
    * ``bokeh``: `'bokeh'`
    """
    mpl = 'matplotlib'
    bokeh = 'bokeh'

    @staticmethod
    def from_str(label):
        """
        Initialize the :py:class:`PlotBackend` from a given string

        :param label: str to use to initialize the backend
                      if it is `None` the default is returned

        :returns: :py:class:`PlotBackend` instance corresponding to the label
        """
        if label is None:
            #Default backend
            return PlotBackend.default()
        elif isinstance(label, PlotBackend):
            return label
        elif label.lower() in ('mpl', 'matplotlib'):
            return PlotBackend.mpl
        elif label.lower() in ('bokeh',):
            return PlotBackend.bokeh
        else:
            raise NotImplementedError

    @staticmethod
    def default():
        """
        Return a :py:class:`PlotBackend` instance corresponding to
        the current default backend
        """
        return PlotBackend.from_str(_DEFAULT_BACKEND)


def set_defaults(backend=None, **kwargs):
    """
    Sets defaults for the plot parameters.

    :param backend: For which backend to set the parameters

    The Kwargs are used to set the parameters of the specified backend
    """
    from .plot_methods import set_mpl_plot_defaults
    from .bokeh_plots import set_bokeh_plot_defaults

    backend = PlotBackend.from_str(backend)

    if backend == PlotBackend.mpl:
        set_mpl_plot_defaults(**kwargs)
    elif backend == PlotBackend.bokeh:
        set_bokeh_plot_defaults(**kwargs)
    else:
        raise NotImplementedError


def reset_defaults(backend=None):
    """
    Reset the defaults for theplot parameters to the original state.

    :param backend: For which backend to reset the parameters
    """
    from .plot_methods import reset_mpl_plot_defaults
    from .bokeh_plots import reset_bokeh_plot_defaults

    backend = PlotBackend.from_str(backend)

    if backend == PlotBackend.mpl:
        reset_mpl_plot_defaults()
    elif backend == PlotBackend.bokeh:
        reset_bokeh_plot_defaults()
    else:
        raise NotImplementedError


def show_defaults(backend=None):
    """
    Show the current set defaults for the plot parameters.

    :param backend: For which backend to show the parameters
    """
    from .plot_methods import show_mpl_plot_defaults
    from .bokeh_plots import show_bokeh_plot_defaults

    backend = PlotBackend.from_str(backend)

    if backend == PlotBackend.mpl:
        show_mpl_plot_defaults()
    elif backend == PlotBackend.bokeh:
        show_bokeh_plot_defaults()
    else:
        raise NotImplementedError


def save_defaults(backend=None, filename='plot_defaults.json', save_complete=False):
    """
    Save the defaults for the plot parameters.

    :param backend: For which backend to save the parameters
    :param filename: str of the filename to save the defaults to
    :param save_complete: bool, if True also the hardcoded defaults are included
    """
    from .plot_methods import save_mpl_defaults
    from .bokeh_plots import save_bokeh_defaults

    backend = PlotBackend.from_str(backend)

    if backend == PlotBackend.mpl:
        save_mpl_defaults(filename=filename, save_complete=save_complete)
    elif backend == PlotBackend.bokeh:
        save_bokeh_defaults(filename=filename, save_complete=save_complete)
    else:
        raise NotImplementedError


def load_defaults(backend=None, filename='plot_defaults.json'):
    """
    Load defaults for the plot parameters from a file and set the contained defaults.

    :param backend: For which backend to save the parameters
    :param filename: str of the filename to load the defaults from
    """
    from .plot_methods import load_mpl_defaults
    from .bokeh_plots import load_bokeh_defaults

    backend = PlotBackend.from_str(backend)

    if backend == PlotBackend.mpl:
        load_mpl_defaults(filename=filename)
    elif backend == PlotBackend.bokeh:
        load_bokeh_defaults(filename=filename)
    else:
        raise NotImplementedError


def get_help(key, backend=None):
    """
    Get a help string for a given parameter.

    :param key: name of the parameter to get the parameter for
    :param backend: For which backend to get the  description of the parameter
    """
    from .plot_methods import get_mpl_help
    from .bokeh_plots import get_bokeh_help

    backend = PlotBackend.from_str(backend)

    if backend == PlotBackend.mpl:
        get_mpl_help(key)
    elif backend == PlotBackend.bokeh:
        get_bokeh_help(key)
    else:
        raise NotImplementedError


def get_plotter(backend=None):
    """
    Get the instance of the :py:class:`~masci_tools.vis.parameters.Plotter` subclass
    used for the given plotting backend

    :param backend: For which backend to get the Plotter instace
    """
    import masci_tools.vis.plot_methods as mpl
    import masci_tools.vis.bokeh_plots as bok

    backend = PlotBackend.from_str(backend)

    if backend == PlotBackend.mpl:
        return mpl.plot_params
    elif backend == PlotBackend.bokeh:
        return bok.plot_params
    else:
        raise NotImplementedError


def dos(energy_grid, dos_data, backend=None, data=None, **kwargs):
    """
    Plot the provided data as a density of states (not spin-polarized). Can be done
    horizontally or vertical via the switch `xyswitch`

    :param energy_grid: data for the energy grid of the DOS
    :param dos_data: data for all the DOS components to plot
    :param data: source for the data of the plot (optional) (pandas Dataframe for example)
    :param backend: name of the backend to use (uses a default if None is given)

    Kwargs are passed on to the backend plotting functions:

        - ``matplotlib``: :py:func:`~masci_tools.vis.plot_methods.plot_dos()`
        - ``bokeh``: :py:func:`~masci_tools.vis.bokeh_plots.bokeh_dos()`

    :returns: Figure object for the used plotting backend
    """
    from .plot_methods import plot_dos
    from .bokeh_plots import bokeh_dos

    plot_funcs = {PlotBackend.mpl: plot_dos, PlotBackend.bokeh: bokeh_dos}

    backend = PlotBackend.from_str(backend)

    return plot_funcs[backend](energy_grid, dos_data, data=data, **kwargs)


def spinpol_dos(energy_grid, dos_data_up, dos_data_dn, backend=None, data=None, **kwargs):
    """
    Plot the provided data as a density of states (spin-polarized). Can be done
    horizontally or vertical via the switch `xyswitch`

    :param energy_grid: data for the energy grid of the DOS
    :param dos_data_up: data for all the DOS components to plot for spin-up
    :param dos_data_dn: data for all the DOS components to plot for spin-down
    :param data: source for the data of the plot (optional) (pandas Dataframe for example)
    :param backend: name of the backend to use (uses a default if None is given)

    Kwargs are passed on to the backend plotting functions:

        - ``matplotlib``: :py:func:`~masci_tools.vis.plot_methods.plot_spinpol_dos()`
        - ``bokeh``: :py:func:`~masci_tools.vis.bokeh_plots.bokeh_spinpol_dos()`

    :returns: Figure object for the used plotting backend
    """
    from .plot_methods import plot_spinpol_dos
    from .bokeh_plots import bokeh_spinpol_dos

    plot_funcs = {PlotBackend.mpl: plot_spinpol_dos, PlotBackend.bokeh: bokeh_spinpol_dos}

    backend = PlotBackend.from_str(backend)

    return plot_funcs[backend](energy_grid, dos_data_up, dos_data_dn, data=data, **kwargs)


def bands(kpath, eigenvalues, backend=None, data=None, **kwargs):
    """
    Plot the provided data for a bandstructure (non spin-polarized)
    Non-weighted, weighted, as a line plot or scatter plot,
    color-mapped or fixed colors are all possible options

    :param kpath: data for the kpoints path (flattened to 1D)
    :param eigenvalues: data for the eigenvalues
    :param data: source for the data of the plot (optional) (pandas Dataframe for example)
    :param backend: name of the backend to use (uses a default if None is given)

    Kwargs are passed on to the backend plotting functions:

        - ``matplotlib``: :py:func:`~masci_tools.vis.plot_methods.plot_bands()`
        - ``bokeh``: :py:func:`~masci_tools.vis.bokeh_plots.bokeh_bands()`

    :returns: Figure object for the used plotting backend
    """
    from .plot_methods import plot_bands
    from .bokeh_plots import bokeh_bands

    plot_funcs = {PlotBackend.mpl: plot_bands, PlotBackend.bokeh: bokeh_bands}

    backend = PlotBackend.from_str(backend)

    return plot_funcs[backend](kpath, eigenvalues, data=data, **kwargs)


def spinpol_bands(kpath, eigenvalues_up, eigenvalues_dn, backend=None, data=None, **kwargs):
    """
    Plot the provided data for a bandstructure (spin-polarized)
    Non-weighted, weighted, as a line plot or scatter plot,
    color-mapped or fixed colors are all possible options

    :param kpath: data for the kpoints path (flattened to 1D)
    :param eigenvalues_up: data for the eigenvalues for spin-up
    :param eigenvalues_dn: data for the eigenvalues for spin-down
    :param data: source for the data of the plot (optional) (pandas Dataframe for example)
    :param backend: name of the backend to use (uses a default if None is given)

    Kwargs are passed on to the backend plotting functions:

        - ``matplotlib``: :py:func:`~masci_tools.vis.plot_methods.plot_spinpol_bands()`
        - ``bokeh``: :py:func:`~masci_tools.vis.bokeh_plots.bokeh_spinpol_bands()`

    :returns: Figure object for the used plotting backend
    """
    from .plot_methods import plot_spinpol_bands
    from .bokeh_plots import bokeh_spinpol_bands

    plot_funcs = {PlotBackend.mpl: plot_spinpol_bands, PlotBackend.bokeh: bokeh_spinpol_bands}

    backend = PlotBackend.from_str(backend)

    return plot_funcs[backend](kpath, eigenvalues_up, eigenvalues_dn, data=data, **kwargs)


def scatter(xdata, ydata, backend=None, data=None, **kwargs):
    """
    Plot the provided data as a scatter plot. Varying size and color
    are possible. Multiple data sets are possible

    :param xdata: data for the x-axis
    :param xdata: data for the y-axis
    :param data: source for the data of the plot (optional) (pandas Dataframe for example)
    :param backend: name of the backend to use (uses a default if None is given)

    Kwargs are passed on to the backend plotting functions:

        - ``matplotlib``: :py:func:`~masci_tools.vis.plot_methods.multi_scatter_plot()`
        - ``bokeh``: :py:func:`~masci_tools.vis.bokeh_plots.bokeh_multi_scatter()`

    :returns: Figure object for the used plotting backend
    """
    from .plot_methods import multi_scatter_plot
    from .bokeh_plots import bokeh_multi_scatter

    plot_funcs = {PlotBackend.mpl: multi_scatter_plot, PlotBackend.bokeh: bokeh_multi_scatter}

    backend = PlotBackend.from_str(backend)

    return plot_funcs[backend](xdata, ydata, data=data, **kwargs)


def line(xdata, ydata, backend=None, data=None, **kwargs):
    """
    Plot the provided data as a line plot. Multiple data sets are possible

    :param xdata: data for the x-axis
    :param xdata: data for the y-axis
    :param data: source for the data of the plot (optional) (pandas Dataframe for example)
    :param backend: name of the backend to use (uses a default if None is given)

    Kwargs are passed on to the backend plotting functions:

        - ``matplotlib``: :py:func:`~masci_tools.vis.plot_methods.multiple_scatterplots()`
        - ``bokeh``: :py:func:`~masci_tools.vis.bokeh_plots.bokeh_line()`

    :returns: Figure object for the used plotting backend
    """
    from .plot_methods import multiple_scatterplots
    from .bokeh_plots import bokeh_line

    plot_funcs = {PlotBackend.mpl: multiple_scatterplots, PlotBackend.bokeh: bokeh_line}

    backend = PlotBackend.from_str(backend)

    return plot_funcs[backend](xdata, ydata, data=data, **kwargs)
