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
Here are general and special bokeh plots to use

"""
from .bokeh_plotter import BokehPlotter
from .parameters import ensure_plotter_consistency, NestedPlotParameters
from .data import process_data_arguments

import pandas as pd
import numpy as np
import warnings
from pprint import pprint

################## Helpers     ################

plot_params = BokehPlotter()


def set_bokeh_plot_defaults(**kwargs):
    """
    Set defaults for bokeh backend
    according to the given keyword arguments

    Available defaults can be seen in :py:class:`~masci_tools.vis.bokeh_plotter.BokehPlotter`
    """
    plot_params.set_defaults(**kwargs)


def reset_bokeh_plot_defaults():
    """
    Reset the defaults for bokeh backend
    to the hardcoded defaults

    Available defaults can be seen in :py:class:`~masci_tools.vis.bokeh_plotter.BokehPlotter`
    """
    plot_params.reset_defaults()


def show_bokeh_plot_defaults():
    """
    Show the currently set defaults for bokeh backend

    Available defaults can be seen in :py:class:`~masci_tools.vis.bokeh_plotter.BokehPlotter`
    """
    pprint(plot_params.get_dict())


def get_bokeh_help(key):
    """
    Print the decription of the given key in the bokeh backend

    Available defaults can be seen in :py:class:`~masci_tools.vis.bokeh_plotter.BokehPlotter`
    """
    plot_params.get_description(key)


def load_bokeh_defaults(filename='plot_bokeh_defaults.json'):
    """
    Load defaults for the bokeh backend from a json file.

    :param filename: filename,from  where the defaults should be taken
    """
    plot_params.load_defaults(filename)


def save_bokeh_defaults(filename='plot_bokeh_defaults.json', save_complete=False):
    """
    Save the current defaults for the matplotlib backend to a json file.

    :param filename: filename, where the defaults should be stored
    :param save_complete: bool if True not only the overwritten user defaults
                          but also the unmodified harcoded defaults are stored
    """
    plot_params.save_defaults(filename, save_complete=save_complete)


##################################### general plots ##########################


@ensure_plotter_consistency(plot_params)
def bokeh_scatter(x,
                  y=None,
                  *,
                  xlabel='x',
                  ylabel='y',
                  title='',
                  figure=None,
                  data=None,
                  saveas='scatter',
                  copy_data=False,
                  **kwargs):
    """
    Create an interactive scatter plot with bokeh

    :param x: arraylike or key for data for the x-axis
    :param y: arraylike or key for data for the y-axis
    :param data: source for the data of the plot (pandas Dataframe for example)
    :param xlabel: label for the x-axis
    :param ylabel: label for the y-axis
    :param title: title of the figure
    :param figure: bokeh figure (optional), if provided the plot will be added to this figure
    :param outfilename: filename of the output file
    :param copy_data: bool, if True the data argument will be copied

    Kwargs will be passed on to :py:class:`masci_tools.vis.bokeh_plotter.BokehPlotter`.
    If the arguments are not recognized they are passed on to the bokeh function `scatter`
    """
    from bokeh.models import ColumnDataSource

    if isinstance(x, (dict, pd.DataFrame, ColumnDataSource)) or x is None:
        warnings.warn(
            'Passing the source as first argument is deprecated. Please pass in source by the keyword data'
            'and xdata and ydata as the first arguments', DeprecationWarning)
        data = x
        x = kwargs.pop('xdata', 'x')
        y = kwargs.pop('ydata', 'y')

    plot_data = process_data_arguments(data=data,
                                       x=x,
                                       y=y,
                                       copy_data=copy_data,
                                       single_plot=True,
                                       same_length=True,
                                       use_column_source=True)
    entry, source = plot_data.items(first=True)

    plot_params.set_defaults(default_type='function', name=entry.y)
    kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)

    p = plot_params.prepare_figure(title, xlabel, ylabel, figure=figure)

    plot_kwargs = plot_params.plot_kwargs(plot_type='scatter')
    res = p.scatter(x=entry.x, y=entry.y, source=source, **plot_kwargs, **kwargs)
    plot_params.add_tooltips(p, res, entry)

    if plot_params['level'] is not None:
        res.level = plot_params['level']

    plot_params.draw_straight_lines(p)
    plot_params.set_limits(p)
    plot_params.save_plot(p, saveas)

    return p


@ensure_plotter_consistency(plot_params)
def bokeh_multi_scatter(x,
                        y=None,
                        *,
                        data=None,
                        figure=None,
                        xlabel='x',
                        ylabel='y',
                        title='',
                        saveas='scatter',
                        copy_data=False,
                        set_default_legend=True,
                        **kwargs):
    """
    Create an interactive scatter (muliple data sets possible) plot with bokeh

    :param x: arraylike or key for data for the x-axis
    :param y: arraylike or key for data for the y-axis
    :param data: source for the data of the plot (pandas Dataframe for example)
    :param xlabel: label for the x-axis
    :param ylabel: label for the y-axis
    :param title: title of the figure
    :param figure: bokeh figure (optional), if provided the plot will be added to this figure
    :param outfilename: filename of the output file
    :param copy_data: bool, if True the data argument will be copied
    :param set_default_legend: bool if True the data names are used to generate default legend labels

    Kwargs will be passed on to :py:class:`masci_tools.vis.bokeh_plotter.BokehPlotter`.
    If the arguments are not recognized they are passed on to the bokeh function `scatter`
    """
    from bokeh.models import ColumnDataSource

    if isinstance(x, (dict, pd.DataFrame, ColumnDataSource)) or x is None:
        warnings.warn(
            'Passing the source as first argument is deprecated. Please pass in source by the keyword data'
            'and xdata and ydata as the first arguments', DeprecationWarning)
        data = x
        x = kwargs.pop('xdata', 'x')
        y = kwargs.pop('ydata', 'y')

    plot_data = process_data_arguments(data=data,
                                       x=x,
                                       y=y,
                                       same_length=True,
                                       copy_data=copy_data,
                                       use_column_source=True)

    plot_params.single_plot = False
    plot_params.num_plots = len(plot_data)

    if plot_data.distinct_datasets('x') == 1:
        default_legend_label = plot_data.get_keys('y')
    else:
        default_legend_label = plot_data.get_keys('x')
    if set_default_legend:
        plot_params.set_defaults(default_type='function', legend_label=default_legend_label)

    plot_params.set_defaults(default_type='function', name=default_legend_label)
    kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)
    p = plot_params.prepare_figure(title, xlabel, ylabel, figure=figure)

    #Process the given color arguments
    plot_params.set_color_palette_by_num_plots()

    plot_kwargs = plot_params.plot_kwargs(plot_type='scatter')

    for indx, ((entry, source), plot_kw) in enumerate(zip(plot_data.items(), plot_kwargs)):

        res = p.scatter(x=entry.x, y=entry.y, source=source, **plot_kw, **kwargs)
        plot_params.add_tooltips(p, res, entry)

        if plot_params[('level', indx)] is not None:
            res.level = plot_params[('level', indx)]

    plot_params.draw_straight_lines(p)
    plot_params.set_limits(p)
    plot_params.set_legend(p)
    plot_params.save_plot(p, saveas)

    return p


@ensure_plotter_consistency(plot_params)
def bokeh_line(x,
               y=None,
               *,
               data=None,
               figure=None,
               xlabel='x',
               ylabel='y',
               title='',
               saveas='line',
               plot_points=False,
               area_curve=0,
               copy_data=False,
               set_default_legend=True,
               **kwargs):
    """
    Create an interactive multi-line plot with bokeh

    :param x: arraylike or key for data for the x-axis
    :param y: arraylike or key for data for the y-axis
    :param data: source for the data of the plot (optional) (pandas Dataframe for example)
    :param xlabel: label for the x-axis
    :param ylabel: label for the y-axis
    :param title: title of the figure
    :param figure: bokeh figure (optional), if provided the plot will be added to this figure
    :param outfilename: filename of the output file
    :param plot_points: bool, if True also plot the points with a scatterplot on top
    :param copy_data: bool, if True the data argument will be copied
    :param set_default_legend: bool if True the data names are used to generate default legend labels

    Kwargs will be passed on to :py:class:`masci_tools.vis.bokeh_plotter.BokehPlotter`.
    If the arguments are not recognized they are passed on to the bokeh function `line`
    """
    from bokeh.models import ColumnDataSource

    if isinstance(x, (dict, pd.DataFrame, ColumnDataSource)) or x is None:
        warnings.warn(
            'Passing the source as first argument is deprecated. Please pass in source by the keyword data'
            'and xdata and ydata as the first arguments', DeprecationWarning)
        data = x
        x = kwargs.pop('xdata', 'x')
        y = kwargs.pop('ydata', 'y')

    plot_data = process_data_arguments(data=data,
                                       x=x,
                                       y=y,
                                       shift=area_curve,
                                       same_length=True,
                                       copy_data=copy_data,
                                       use_column_source=True)

    plot_params.single_plot = False
    plot_params.num_plots = len(plot_data)

    if plot_data.distinct_datasets('x') == 1:
        default_legend_label = plot_data.get_keys('y')
    else:
        default_legend_label = plot_data.get_keys('x')
    if set_default_legend:
        plot_params.set_defaults(default_type='function', legend_label=default_legend_label)

    plot_params.set_defaults(default_type='function', name=default_legend_label)

    kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)
    p = plot_params.prepare_figure(title, xlabel, ylabel, figure=figure)

    #Process the given color arguments
    plot_params.set_color_palette_by_num_plots()

    plot_kw_line = plot_params.plot_kwargs(plot_type='line')
    plot_kw_scatter = plot_params.plot_kwargs(plot_type='scatter')
    plot_kw_area = plot_params.plot_kwargs(plot_type='area')

    area_curve = kwargs.pop('area_curve', None)

    for indx, ((entry, source), kw_line, kw_scatter,
               kw_area) in enumerate(zip(plot_data.items(), plot_kw_line, plot_kw_scatter, plot_kw_area)):

        if plot_params[('area_plot', indx)]:
            if plot_params[('area_vertical', indx)]:
                p.harea(y=entry.y, x1=entry.x, x2=entry.shift, **kw_area, source=source)
            else:
                p.varea(x=entry.x, y1=entry.y, y2=entry.shift, **kw_area, source=source)

        res = p.line(x=entry.x, y=entry.y, source=source, **kw_line, **kwargs)
        plot_params.add_tooltips(p, res, entry)
        res2 = None
        if plot_points:
            res2 = p.scatter(x=entry.x, y=entry.y, source=source, **kw_scatter)

        if plot_params[('level', indx)] is not None:
            res.level = plot_params[('level', indx)]
            if res2 is not None:
                res2.level = plot_params[('level', indx)]

    plot_params.draw_straight_lines(p)
    plot_params.set_limits(p)
    plot_params.set_legend(p)
    plot_params.save_plot(p, saveas)

    return p


@ensure_plotter_consistency(plot_params)
def bokeh_dos(energy_grid,
              dos_data=None,
              *,
              data=None,
              energy_label=r'E-E_F [eV]',
              dos_label=r'DOS [1/eV]',
              title=r'Density of states',
              xyswitch=False,
              e_fermi=0,
              saveas='dos_plot',
              copy_data=False,
              **kwargs):
    """
    Create an interactive dos plot (non-spinpolarized) with bokeh
    Both horizontal or vertical orientation are possible

    :param energy_grid: arraylike or key data for the energy grid
    :param spin_up_data: arraylike or key data for the DOS
    :param data: source for the DOS data (optional) of the plot (pandas Dataframe for example)
    :param energy_label: label for the energy-axis
    :param dos_label: label for the dos-axis
    :param title: title of the figure
    :param xyswitch: bool if True, the energy will be plotted along the y-direction
    :param e_fermi: float, determines, where to put the line for the fermi energy
    :param outfilename: filename of the output file
    :param copy_data: bool, if True the data argument will be copied

    Kwargs will be passed on to :py:func:`bokeh_line()`
    """
    from bokeh.models import ColumnDataSource

    if isinstance(energy_grid, (dict, pd.DataFrame, ColumnDataSource)) or energy_grid is None:
        warnings.warn(
            'Passing the dataframe as first argument is deprecated. Please pass in source by the keyword data'
            'and energy_grid and dos_data as the first arguments', DeprecationWarning)
        data = energy_grid
        energy_grid = kwargs.pop('energy', 'energy_grid')
        dos_data = kwargs.pop('ynames', None)

    if dos_data is None and data is not None:
        dos_data = set(data.keys()) - set([energy_grid] if isinstance(energy_grid, str) else energy_grid)
        dos_data = sorted(dos_data)

    plot_data = process_data_arguments(data=data,
                                       energy=energy_grid,
                                       dos=dos_data,
                                       same_length=True,
                                       copy_data=copy_data,
                                       use_column_source=True)

    plot_params.single_plot = False
    plot_params.num_plots = len(plot_data)

    if 'limits' in kwargs:
        limits = kwargs.pop('limits')
        if 'x' not in limits and 'y' not in limits:
            if xyswitch:
                limits['x'], limits['y'] = limits.pop('dos', None), limits.pop('energy', None)
            else:
                limits['x'], limits['y'] = limits.pop('energy', None), limits.pop('dos', None)
        kwargs['limits'] = {k: v for k, v in limits.items() if v is not None}

    lines = {'horizontal': 0}
    lines['vertical'] = e_fermi

    if xyswitch:
        lines['vertical'], lines['horizontal'] = lines['horizontal'], lines['vertical']

    plot_params.set_defaults(default_type='function',
                             straight_lines=lines,
                             tooltips=[('Name', '$name'), ('Energy', '@{x}{{0.0[00]}}'),
                                       ('DOS value', '@$name{{0.00}}')],
                             figure_kwargs={
                                 'width': 1000,
                             })

    if xyswitch:
        x, y = plot_data.get_keys('dos'), plot_data.get_keys('energy')
        xlabel, ylabel = dos_label, energy_label
        plot_params.set_defaults(default_type='function', area_vertical=True)
    else:
        xlabel, ylabel = energy_label, dos_label
        x, y = plot_data.get_keys('energy'), plot_data.get_keys('dos')

    p = bokeh_line(x,
                   y,
                   data=plot_data.data,
                   xlabel=xlabel,
                   ylabel=ylabel,
                   title=title,
                   name=y,
                   saveas=saveas,
                   **kwargs)

    return p


@ensure_plotter_consistency(plot_params)
def bokeh_spinpol_dos(energy_grid,
                      spin_up_data=None,
                      spin_dn_data=None,
                      *,
                      data=None,
                      spin_dn_negative=True,
                      energy_label=r'E-E_F [eV]',
                      dos_label=r'DOS [1/eV]',
                      title=r'Density of states',
                      xyswitch=False,
                      e_fermi=0,
                      spin_arrows=True,
                      saveas='dos_plot',
                      copy_data=False,
                      **kwargs):
    """
    Create an interactive dos plot (spinpolarized) with bokeh
    Both horizontal or vertical orientation are possible

    :param energy_grid: arraylike or key data for the energy grid
    :param spin_up_data: arraylike or key data for the DOS spin-up
    :param spin_dn_data: arraylike or key data for the DOS spin-dn
    :param data: source for the DOS data (optional) of the plot (pandas Dataframe for example)
    :param spin_dn_negative: bool, if True (default), the spin down components are plotted downwards
    :param energy_label: label for the energy-axis
    :param dos_label: label for the dos-axis
    :param title: title of the figure
    :param xyswitch: bool if True, the energy will be plotted along the y-direction
    :param e_fermi: float, determines, where to put the line for the fermi energy
    :param spin_arrows: bool, if True (default) small arrows will be plotted on the left side of the plot indicating
                        the spin directions (if spin_dn_negative is True)
    :param outfilename: filename of the output file
    :param copy_data: bool, if True the data argument will be copied

    Kwargs will be passed on to :py:func:`bokeh_line()`
    """
    from bokeh.models import NumeralTickFormatter, Arrow, NormalHead
    from bokeh.models import ColumnDataSource

    if isinstance(energy_grid, (dict, pd.DataFrame, ColumnDataSource)) or energy_grid is None:
        warnings.warn(
            'Passing the dataframe as first argument is deprecated. Please pass in source by the keyword data'
            'and energy_grid and dos_data as the first arguments', DeprecationWarning)
        data = energy_grid
        energy_grid = kwargs.pop('energy', 'energy_grid')
        spin_up_data = kwargs.pop('ynames', None)
        spin_up_data, spin_dn_data = spin_up_data[:len(spin_up_data) // 2], spin_up_data[len(spin_up_data) // 2:]

    if spin_up_data is None and data is not None:
        spin_up_data = {key for key in data.keys() if '_up' in key}
        spin_up_data = sorted(spin_up_data)
        spin_dn_data = {key for key in data.keys() if '_dn' in key}
        spin_dn_data = sorted(spin_dn_data)

    plot_data = process_data_arguments(data=data,
                                       energy=energy_grid,
                                       spin_up=spin_up_data,
                                       spin_dn=spin_dn_data,
                                       same_length=True,
                                       copy_data=copy_data,
                                       use_column_source=True)

    plot_params.single_plot = False
    plot_params.num_plots = len(plot_data)

    if 'limits' in kwargs:
        limits = kwargs.pop('limits')
        if 'x' not in limits and 'y' not in limits:
            if xyswitch:
                limits['x'], limits['y'] = limits.pop('dos', None), limits.pop('energy', None)
            else:
                limits['x'], limits['y'] = limits.pop('energy', None), limits.pop('dos', None)
        kwargs['limits'] = {k: v for k, v in limits.items() if v is not None}

    lines = {'horizontal': 0}
    lines['vertical'] = e_fermi

    if spin_dn_negative:
        plot_data.apply('spin_dn', lambda x: -x)

    if xyswitch:
        lines['vertical'], lines['horizontal'] = lines['horizontal'], lines['vertical']

    plot_params.set_defaults(default_type='function',
                             straight_lines=lines,
                             tooltips=[('DOS Name', '$name'), ('Energy', '@{x}{{0.0[00]}}'),
                                       ('Value', '@$name{{(0,0.00)}}')],
                             figure_kwargs={'width': 1000})

    #Create the full data for the scatterplot
    energy_entries = plot_data.get_keys('energy') * 2
    dos_entries = plot_data.get_keys('spin_up') + plot_data.get_keys('spin_dn')
    sources = plot_data.data
    if isinstance(sources, list):
        sources = sources * 2

    if xyswitch:
        x, y = dos_entries, energy_entries
        xlabel, ylabel = dos_label, energy_label
        plot_params.set_defaults(default_type='function',
                                 area_vertical=True,
                                 x_axis_formatter=NumeralTickFormatter(format='(0,0)'))
    else:
        xlabel, ylabel = energy_label, dos_label
        x, y = energy_entries, dos_entries
        plot_params.set_defaults(default_type='function',
                                 area_vertical=True,
                                 y_axis_formatter=NumeralTickFormatter(format='(0,0)'))

    plot_params.set_parameters(color=kwargs.pop('color', None), color_palette=kwargs.pop('color_palette', None))
    plot_params.set_color_palette_by_num_plots()

    #Double the colors for spin up and down
    kwargs['color'] = list(plot_params['color'].copy())
    kwargs['color'].extend(kwargs['color'])

    if 'legend_label' not in kwargs:
        kwargs['legend_label'] = dos_entries
    else:
        if isinstance(kwargs['legend_label'], list):
            if len(kwargs['legend_label']) == len(plot_data):
                kwargs['legend_label'].extend(kwargs['legend_label'])

    if 'show' in kwargs:
        plot_params.set_parameters(show=kwargs.pop('show'))
    if 'save_plots' in kwargs:
        plot_params.set_parameters(show=kwargs.pop('save_plots'))

    with NestedPlotParameters(plot_params):
        p = bokeh_line(x,
                       y,
                       xlabel=xlabel,
                       ylabel=ylabel,
                       title=title,
                       data=sources,
                       name=dos_entries,
                       show=False,
                       save_plots=False,
                       **kwargs)

    if spin_arrows and spin_dn_negative:

        #These are hardcoded because the parameters are not
        #reused anywhere (for now)
        x_pos = 50
        length = 70
        pad = 30
        height = p.plot_height - 100
        alpha = 0.5

        p.add_layout(
            Arrow(x_start=x_pos,
                  x_end=x_pos,
                  y_start=height - pad - length,
                  y_end=height - pad,
                  start_units='screen',
                  end_units='screen',
                  line_width=2,
                  line_alpha=alpha,
                  end=NormalHead(line_width=2, size=10, fill_alpha=alpha, line_alpha=alpha)))
        p.add_layout(
            Arrow(x_start=x_pos,
                  x_end=x_pos,
                  y_start=pad + length,
                  y_end=pad,
                  start_units='screen',
                  end_units='screen',
                  line_width=2,
                  line_alpha=alpha,
                  end=NormalHead(line_width=2, size=10, fill_alpha=alpha, line_alpha=alpha)))

    plot_params.save_plot(p, saveas)

    return p


@ensure_plotter_consistency(plot_params)
def bokeh_bands(kpath,
                bands=None,
                *,
                data=None,
                size_data=None,
                color_data=None,
                xlabel='',
                ylabel=r'E-E_F [eV]',
                title='',
                special_kpoints=None,
                markersize_min=3.0,
                markersize_scaling=10.0,
                saveas='bands_plot',
                scale_color=True,
                separate_bands=False,
                line_plot=False,
                band_index=None,
                copy_data=False,
                **kwargs):
    """
    Create an interactive bandstructure plot (non-spinpolarized) with bokeh
    Can make a simple plot or weight the size and color of the points against a given weight

    :param kpath: arraylike or key data for the kpoint data
    :param bands: arraylike or key data for the eigenvalues
    :param size_data: arraylike or key data the weights to emphasize (optional)
    :param color_data: str or arraylike, data for the color values with a colormap (optional)
    :param data: source for the bands data (optional) of the plot (pandas Dataframe for example)
    :param xlabel: label for the x-axis (default no label)
    :param ylabel: label for the y-axis
    :param title: title of the figure
    :param special_kpoints: list of tuples (str, float), place vertical lines at the given values
                            and mark them on the x-axis with the given label
    :param e_fermi: float, determines, where to put the line for the fermi energy
    :param markersize_min: minimum value used in scaling points for weight
    :param markersize_scaling: factor used in scaling points for weight
    :param outfilename: filename of the output file
    :param scale_color: bool, if True (default) the weight will be additionally shown via a colormapping
    :param line_plot: bool, if True the bandstructure will be plotted with lines
                      Here no weights are supported
    :param separate_bands: bool, if True the bandstructure will be separately plotted for each band
                           allows more specific parametrization
    :param band_index: data for which eigenvalue belongs to which band (needed for line_plot and separate_bands)
    :param copy_data: bool, if True the data argument will be copied

    Kwargs will be passed on to :py:func:`bokeh_multi_scatter()` or :py:func:`bokeh_line()`
    """
    from bokeh.transform import linear_cmap
    from bokeh.models import ColumnDataSource

    if 'size_scaling' in kwargs:
        warnings.warn('size_scaling is deprecated. Use markersize_scaling instead', DeprecationWarning)
        markersize_scaling = kwargs.pop('size_scaling')

    if 'size_min' in kwargs:
        warnings.warn('size_min is deprecated. Use markersize_min instead', DeprecationWarning)
        markersize_min = kwargs.pop('size_min')

    if isinstance(kpath, (dict, pd.DataFrame, ColumnDataSource)) or kpath is None:
        warnings.warn(
            'Passing the dataframe as first argument is deprecated. Please pass in source by the keyword data'
            'and kpath and bands as the first arguments', DeprecationWarning)
        data = kpath
        kpath = kwargs.pop('k_label', 'kpath')
        bands = kwargs.pop('eigenvalues', 'eigenvalues_up')

    if 'weight' in kwargs:
        warnings.warn('The weight argument is deprecated. Use size_data and color_data instead', DeprecationWarning)
        size_data = kwargs.pop('weight')

    plot_data = process_data_arguments(single_plot=True,
                                       data=data,
                                       kpath=kpath,
                                       bands=bands,
                                       size=size_data,
                                       color=color_data,
                                       band_index=band_index,
                                       copy_data=copy_data,
                                       use_column_source=True)

    if line_plot and size_data is not None:
        raise ValueError('Bandstructure with lines and size scaling not supported')

    if line_plot and color_data is not None:
        raise ValueError('Bandstructure with lines and color mapping not supported')

    if line_plot or separate_bands:
        if band_index is None:
            raise ValueError('The data for band indices are needed for separate_bands and line_plot')
        plot_data.group_data('band_index')
        plot_data.sort_data('kpath')

    if scale_color and size_data is not None:
        if color_data is not None:
            raise ValueError('color_data should not be provided when scale_color is True')
        plot_data.copy_data('size', 'color', rename_original=True)

    if color_data is not None:
        kwargs['color'] = plot_data.get_keys('color')

    entries = plot_data.keys(first=True)
    if entries.size is not None:
        ylimits = (-15, 15)
        if 'limits' in kwargs:
            if 'y' in kwargs['limits']:
                ylimits = kwargs['limits']['y']

        data = plot_data.values(first=True)
        mask = np.logical_and(data.bands > ylimits[0], data.bands < ylimits[1])

        weight_max = plot_data.max('size', mask=mask)

        plot_params.set_defaults(default_type='function', marker_size=entries.size)
        if scale_color:
            plot_params.set_defaults(default_type='function',
                                     color=linear_cmap(entries.color, 'Blues256', weight_max, -0.05))

        transform = lambda size: markersize_min + markersize_scaling * size / weight_max
        plot_data.apply('size', transform)
    else:
        plot_params.set_defaults(default_type='function', color='black')

    if special_kpoints is None:
        special_kpoints = []

    xticks = []
    xticklabels = {}
    for label, pos in special_kpoints:
        #if label in ('Gamma', 'g'): Latex label missing for bokeh
        #    label = r'$\Gamma$'
        if pos.is_integer():
            xticklabels[int(pos)] = label
        xticklabels[pos] = label
        xticks.append(pos)

    lines = {'horizontal': 0}
    lines['vertical'] = xticks

    limits = {'y': (-15, 15)}
    plot_params.set_defaults(default_type='function',
                             straight_lines=lines,
                             x_ticks=xticks,
                             x_ticklabels_overwrite=xticklabels,
                             figure_kwargs={
                                 'width': 1280,
                                 'height': 720
                             },
                             x_range_padding=0.0,
                             y_range_padding=0.0,
                             legend_label='Eigenvalues',
                             limits=limits)

    if line_plot:
        return bokeh_line(plot_data.get_keys('kpath'),
                          plot_data.get_keys('bands'),
                          data=plot_data.data,
                          xlabel='',
                          ylabel=ylabel,
                          title=title,
                          set_default_legend=False,
                          saveas=saveas,
                          **kwargs)
    return bokeh_multi_scatter(plot_data.get_keys('kpath'),
                               plot_data.get_keys('bands'),
                               data=plot_data.data,
                               xlabel='',
                               ylabel=ylabel,
                               title=title,
                               set_default_legend=False,
                               saveas=saveas,
                               **kwargs)


@ensure_plotter_consistency(plot_params)
def bokeh_spinpol_bands(kpath,
                        bands_up=None,
                        bands_dn=None,
                        *,
                        size_data=None,
                        color_data=None,
                        data=None,
                        xlabel='',
                        ylabel=r'E-E_F [eV]',
                        title='',
                        special_kpoints=None,
                        markersize_min=3.0,
                        markersize_scaling=10.0,
                        saveas='bands_plot',
                        scale_color=True,
                        line_plot=False,
                        separate_bands=False,
                        band_index=None,
                        copy_data=False,
                        **kwargs):
    """
    Create an interactive bandstructure plot (spinpolarized) with bokeh
    Can make a simple plot or weight the size and color of the points against a given weight

    :param kpath: arraylike or key data for the kpoint data
    :param bands_up: arraylike or key data for the eigenvalues spin-up
    :param bands_dn: arraylike or key data for the eigenvalues spin-dn
    :param size_data: arraylike or key data the weights to emphasize (optional)
    :param color_data: str or arraylike, data for the color values with a colormap (optional)
    :param data: source for the bands data (optional) of the plot (pandas Dataframe for example)
    :param xlabel: label for the x-axis (default no label)
    :param ylabel: label for the y-axis
    :param title: title of the figure
    :param special_kpoints: list of tuples (str, float), place vertical lines at the given values
                            and mark them on the x-axis with the given label
    :param e_fermi: float, determines, where to put the line for the fermi energy
    :param markersize_min: minimum value used in scaling points for weight
    :param markersize_scaling: factor used in scaling points for weight
    :param outfilename: filename of the output file
    :param scale_color: bool, if True (default) the weight will be additionally shown via a colormapping
    :param line_plot: bool, if True the bandstructure will be plotted with lines
                      Here no weights are supported
    :param separate_bands: bool, if True the bandstructure will be separately plotted for each band
                           allows more specific parametrization
    :param band_index: data for which eigenvalue belongs to which band (needed for line_plot and separate_bands)
    :param copy_data: bool, if True the data argument will be copied

    Kwargs will be passed on to :py:func:`bokeh_multi_scatter()` or :py:func:`bokeh_line()`
    """
    from bokeh.transform import linear_cmap
    from bokeh.models import ColumnDataSource

    if 'size_scaling' in kwargs:
        warnings.warn('size_scaling is deprecated. Use markersize_scaling instead', DeprecationWarning)
        markersize_scaling = kwargs.pop('size_scaling')

    if 'size_min' in kwargs:
        warnings.warn('size_min is deprecated. Use markersize_min instead', DeprecationWarning)
        markersize_min = kwargs.pop('size_min')

    if isinstance(kpath, (dict, pd.DataFrame, ColumnDataSource)) or kpath is None:
        warnings.warn(
            'Passing the dataframe as first argument is deprecated. Please pass in source by the keyword data'
            'and kpath and bands_up and bands_dn as the first arguments', DeprecationWarning)
        data = kpath
        kpath = kwargs.pop('k_label', 'kpath')
        bands_up = kwargs.pop('eigenvalues', ['eigenvalues_up', 'eigenvalues_down'])
        bands_up, bands_dn = bands_up[0], bands_up[1]

    if 'weight' in kwargs:
        warnings.warn('The weight argument is deprecated. Use size_data and color_data instead', DeprecationWarning)
        size_data = kwargs.pop('weight')

    plot_data = process_data_arguments(data=data,
                                       kpath=kpath,
                                       bands=[bands_up, bands_dn],
                                       size=size_data,
                                       color=color_data,
                                       band_index=band_index,
                                       copy_data=copy_data,
                                       use_column_source=True)

    plot_params.single_plot = False
    plot_params.num_plots = len(plot_data)

    if len(plot_data) != 2:
        raise ValueError('Wrong number of plots specified (Only 2 permitted)')

    if line_plot and size_data is not None:
        raise ValueError('Bandstructure with lines and size scaling not supported')

    if line_plot and color_data is not None:
        raise ValueError('Bandstructure with lines and color mapping not supported')

    if line_plot or separate_bands:
        if band_index is None:
            raise ValueError('The data for band indices are needed for separate_bands and line_plot')

        plot_data.group_data('band_index')
        plot_data.sort_data('kpath')

    if scale_color and size_data is not None:
        if color_data is not None:
            raise ValueError('color_data should not be provided when scale_color is True')
        plot_data.copy_data('size', 'color', rename_original=True)

    if color_data is not None:
        kwargs['color'] = plot_data.get_keys('color')

    if any(entry.size is not None for entry in plot_data.keys()):

        ylimits = (-15, 15)
        if 'limits' in kwargs:
            if 'y' in kwargs['limits']:
                ylimits = kwargs['limits']['y']

        data = plot_data.values()
        mask = [np.logical_and(col.bands > ylimits[0], col.bands < ylimits[1]) for col in data]
        weight_max = plot_data.max('size', mask=mask)

        transform = lambda size: markersize_min + markersize_scaling * size / weight_max
        plot_data.apply('size', transform)

        plot_params.set_defaults(default_type='function', marker_size=plot_data.get_keys('size'))
        if scale_color:
            plot_params.set_defaults(default_type='function',
                                     color=[
                                         linear_cmap(name, palette, weight_max, -0.05)
                                         for name, palette in zip(plot_data.get_keys('color'), ['Blues256', 'Reds256'])
                                     ])
    else:
        color = ['blue', 'red']
        plot_params.set_defaults(default_type='function', color=color)

    if special_kpoints is None:
        special_kpoints = []

    xticks = []
    xticklabels = {}
    for label, pos in special_kpoints:
        #if label in ('Gamma', 'g'): Latex label missing for bokeh
        #    label = r'$\Gamma$'
        if pos.is_integer():
            xticklabels[int(pos)] = label
        xticklabels[pos] = label
        xticks.append(pos)

    lines = {'horizontal': 0}
    lines['vertical'] = xticks

    limits = {'y': (-15, 15)}
    plot_params.set_defaults(default_type='function',
                             straight_lines=lines,
                             x_ticks=xticks,
                             x_ticklabels_overwrite=xticklabels,
                             figure_kwargs={
                                 'width': 1280,
                                 'height': 720
                             },
                             x_range_padding=0.0,
                             y_range_padding=0.0,
                             limits=limits,
                             legend_label=['Spin Up', 'Spin Down'],
                             level=[None, 'underlay'])

    if line_plot or separate_bands:
        plot_params.num_plots = len(plot_data)
        kwargs = plot_params.expand_parameters(original_length=2, **kwargs)

    if line_plot:
        return bokeh_line(plot_data.get_keys('kpath'),
                          plot_data.get_keys('bands'),
                          data=plot_data.data,
                          xlabel='',
                          ylabel=ylabel,
                          title=title,
                          set_default_legend=False,
                          saveas=saveas,
                          **kwargs)
    return bokeh_multi_scatter(plot_data.get_keys('kpath'),
                               plot_data.get_keys('bands'),
                               data=plot_data.data,
                               xlabel='',
                               ylabel=ylabel,
                               title=title,
                               set_default_legend=False,
                               saveas=saveas,
                               **kwargs)


@ensure_plotter_consistency(plot_params)
def bokeh_spectral_function(kpath,
                            energy_grid,
                            spectral_function,
                            *,
                            data=None,
                            special_kpoints=None,
                            e_fermi=0,
                            xlabel='',
                            ylabel=r'$E-E_F$ [eV]',
                            title='',
                            saveas='spectral_function',
                            copy_data=False,
                            figure=None,
                            **kwargs):
    """
    Create a colormesh plot of a spectral function

    :param kpath: data for the kpoint coordinates
    :param energy_grid: data for the energy grid
    :param spectral_function: 2D data for the spectral function
    :param data: source for the data of the plot (optional) (pandas Dataframe for example)
    :param title: str, Title of the plot
    :param xlabel: str, label for the x-axis
    :param ylabel: str, label for the y-axis
    :param saveas: str, filename for the saved plot
    :param e_fermi: float (default 0), place the line for the fermi energy at this value
    :param special_kpoints: list of tuples (str, float), place vertical lines at the given values
                            and mark them on the x-axis with the given label
    :param copy_data: bool, if True the data argument will be copied

    All other Kwargs are passed on to the image call of bokeh
    """

    plot_data = process_data_arguments(single_plot=True,
                                       data=data,
                                       kpath=kpath,
                                       energy=energy_grid,
                                       spectral_function=spectral_function,
                                       forbid_split_up={
                                           'spectral_function',
                                       },
                                       copy_data=copy_data)

    if special_kpoints is None:
        special_kpoints = []

    xticks = []
    xticklabels = {}
    for label, pos in special_kpoints:
        #if label in ('Gamma', 'g'): Latex label missing for bokeh
        #    label = r'$\Gamma$'
        if pos.is_integer():
            xticklabels[int(pos)] = label
        xticklabels[pos] = label
        xticks.append(pos)

    lines = {'horizontal': 0}
    lines['vertical'] = xticks

    limits = {'y': (plot_data.min('energy'), plot_data.max('energy'))}
    plot_params.set_defaults(default_type='function',
                             straight_lines=lines,
                             x_ticks=xticks,
                             x_ticklabels_overwrite=xticklabels,
                             figure_kwargs={
                                 'width': 1280,
                                 'height': 720
                             },
                             x_range_padding=0.0,
                             y_range_padding=0.0,
                             limits=limits,
                             color_palette='Plasma256',
                             legend_label='Spectral function',
                             straight_line_options={'line_color': 'white'})

    kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)
    p = plot_params.prepare_figure(title, xlabel, ylabel, figure=figure)

    entry = plot_data.values(first=True)

    plot_kw = plot_params.plot_kwargs(plot_type='image')

    min_energy = plot_data.min('energy')
    dh = plot_data.max('energy') - min_energy
    p.image([entry.spectral_function],
            x=0,
            y=plot_data.min('energy'),
            dh=dh,
            dw=plot_data.max('kpath'),
            **plot_kw,
            **kwargs)

    plot_params.draw_straight_lines(p)
    plot_params.set_limits(p)
    plot_params.set_legend(p)
    plot_params.save_plot(p, saveas)

    return p


####################################################################################################
##################################### special plots ################################################
####################################################################################################

# periodic table

# tools="pan, xpan, ypan, poly_select, tap, wheel_zoom, xwheel_zoom, ywheel_zoom, xwheel_pan, ywheel_pan,
#         box_zoom, redo, undo, reset, save, crosshair, zoom_out, xzoom_out, yzoom_out, hover"
tooltips_def_period = [('Name', '@name'), ('Atomic number', '@{atomic number}'), ('Atomic mass', '@{atomic mass}'),
                       ('CPK color', '$color[hex, swatch]:CPK'),
                       ('Electronic configuration', '@{electronic configuration}')]


def periodic_table_plot(source,
                        display_values=[],
                        display_positions=[],
                        color_value=None,
                        tooltips=tooltips_def_period,
                        title='',
                        outfilename='periodictable.html',
                        value_color_range=[None, None],
                        log_scale=0,
                        color_map=None,
                        bokeh_palette='Plasma256',
                        toolbar_location=None,
                        tools='hover',
                        blank_color='#c4c4c4',
                        blank_outsiders=[True, True],
                        include_legend=True,
                        copy_source=True,
                        legend_labels=None,
                        color_bar_title=None,
                        show=True):
    """
    Plot function for an interactive periodic table plot. Heat map and hover tool.
    source must be a panda dataframe containing, period, group,

    param source: pandas dataframe containing everything
    param tooltips: what is shown with hover tool. values have to be in source
    example:

    .. code-block:: python

        Keys of panda DF. group, period symbol and atomic number or required...
        Index([u'atomic number', u'symbol', u'name', u'atomic mass', u'CPK',
           u'electronic configuration', u'electronegativity', u'atomic radius',
           u'ion radius', u'van der Waals radius', u'IE-1', u'EA',
           u'standard state', u'bonding type', u'melting point', u'boiling point',
           u'density', u'metal', u'year discovered', u'group', u'period',
           u'rmt_mean', u'rmt_std', u'number_of_occ', u'type_color', u'c_value'],
          dtype='object')

        tooltips_def = [("Name", "@name"),
                    ("Atomic number", "@{atomic number}"),
                    ("Atomic mass", "@{atomic mass}"),
                    ("CPK color", "$color[hex, swatch]:CPK"),
                    ("Electronic configuration", "@{electronic configuration}")]

    param display_values: list of strings, have to match source. Values to be displayed on the element rectangles
    example:["rmt_mean", "rmt_std", "number_of_occ"]
    param display_positions: list of floats, length has to match display_values, At which y offset the display values should be displayed.
    """
    # TODO: solve the use of two different color bars, we just one to use a bokeh color bar and not matplotlib...
    from bokeh.io import export_png
    from bokeh.io import output_notebook, output_file
    from bokeh.sampledata.periodic_table import elements
    from bokeh.transform import dodge, factor_cmap
    from bokeh.models import Arrow, OpenHead, NormalHead, VeeHead
    from bokeh.models import Range1d, LabelSet, Label
    from bokeh.models import LinearColorMapper, LogColorMapper, ColorBar
    from bokeh.models import BasicTicker

    from bokeh.io import show as bshow
    from bokeh.plotting import figure as bokeh_fig
    from matplotlib.colors import Normalize, LogNorm, to_hex
    from matplotlib.cm import plasma  #pylint: disable=no-name-in-module
    from matplotlib.cm import ScalarMappable

    if color_map is None:
        color_map = plasma

    if len(display_values) != len(display_positions):
        raise ValueError(
            'The input lists "display_values" and "display_positions" of "periodic_table_plot" need to have same length.'
        )

    if copy_source:
        source1 = source.copy()
    else:  # inline we change the data here!
        source1 = source

    TOOLTIPS = tooltips

    # defaults
    plot_width = 1470
    plot_height = 1040
    cbar_height = 40
    cbar_width = 500
    cbar_fontsize = 12  # size of cbar labels
    cbar_standoff = 8

    # preprocessing data
    # if colors are not given in source, color
    # if source has "type_color"]

    # colors are tricky, since for the periodic table we use matplotlib, for the legend we have to use bokeh

    # Define color map called 'color_scale'
    data = source1[color_value]
    if value_color_range[0] is not None:
        mind = value_color_range[0]
    else:
        mind = min(data)  # 0.65 #
    if value_color_range[1] is not None:
        maxd = value_color_range[1]
    else:
        maxd = max(data)  # 2.81 #

    if log_scale == 0:
        color_mapper = LinearColorMapper(palette=bokeh_palette, low=mind, high=maxd)
        norm = Normalize(vmin=mind, vmax=maxd)
    elif log_scale == 1:
        for datum in data:
            if datum < 0:
                raise ValueError(f'Entry for element {datum} is negative but log-scale is selected')
        color_mapper = LogColorMapper(palette=bokeh_palette, low=mind, high=maxd)
        norm = LogNorm(vmin=mind, vmax=maxd)
    color_scale = ScalarMappable(norm=norm, cmap=color_map).to_rgba(data, alpha=None)

    # Define color for blank entries
    default_value = None
    color_list = []
    color_values = []
    for i in range(len(source1)):
        color_list.append(blank_color)
        color_values.append(default_value)

    for i, data_element in enumerate(source1[color_value]):
        if blank_outsiders[0] and data_element < mind:
            continue
        if blank_outsiders[1] and data_element > maxd:
            continue
        color_list[i] = to_hex(color_scale[i])
        # color_values[i] = data_element

    source1['type_color'] = color_list
    # source["c_value"] = color_values

    if include_legend:
        # we copy the Be entry and display it with some text again at another spot
        be = source1[3:4].copy()
        be['group'] = '7'
        # print(be)
        source1.loc[-1] = be.values[0]
        source1.index = source1.index + 1
        source1 = source1.sort_index()
        # df.head()
    groups = [str(x) for x in range(1, 19)]
    periods = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
    # Plot
    p = bokeh_fig(
        title=title,
        plot_width=plot_width,
        plot_height=plot_height,  # 450,
        x_range=groups,
        y_range=list(reversed(periods)),
        tools=tools,
        toolbar_location=toolbar_location,
        tooltips=TOOLTIPS)
    r = p.rect(
        'group',
        'period',
        0.95,
        0.95,
        source=source1,
        fill_alpha=0.6,  # legend="metal",
        color='type_color')

    text_props = {'source': source1, 'text_align': 'left', 'text_baseline': 'middle'}
    x = dodge('group', -0.4, range=p.x_range)

    # The element names
    p.text(x=x,
           y=dodge('period', 0.25, range=p.y_range),
           text='symbol',
           text_font_style='bold',
           text_font_size='14pt',
           **text_props)
    p.text(x=dodge('group', 0.1, range=p.x_range),
           y=dodge('period', 0.25, range=p.y_range),
           text='atomic number',
           text_font_size='12pt',
           **text_props)

    # The values displayed on the element boxes
    for i, label in enumerate(display_values):
        p.text(x=x,
               y=dodge('period', display_positions[i], range=p.y_range),
               text=label,
               text_font_size='10pt',
               **text_props)

        # legend
        # not a real legend, but selfmade text
        # print(be.values[0])
        # print(source.loc(-1))
        # print(be['group'])
        # p.text(x=be['group'], y=dodge("period", 0.25, range=p.y_range), text="test", text_font_style="bold", text_font_size="14pt")
        if legend_labels is not None:
            label1 = legend_labels[i]
        else:
            label1 = label

        # I do not like the hardcoded positions of the legend
        legendlabel = Label(
            x=7.1,
            y=8.4 + display_positions[i],  # x_units='screen', y_units='screen',
            text=label1,
            render_mode='canvas',  # 'css',
            border_line_color='black',
            border_line_alpha=0.0,
            background_fill_color=None,
            background_fill_alpha=1.0)
        p.add_layout(legendlabel)

        legendlabelarrow = Arrow(
            x_start=7.05,
            x_end=6.7,
            y_start=8.5 + display_positions[i],
            y_end=8.5 + display_positions[i],  # x_units='screen', y_units='screen',
            line_width=2,
            end=OpenHead(line_width=2, size=4))  # 'css',
        # border_line_color='black', border_line_alpha=0.0,
        # background_fill_color=None, background_fill_alpha=1.0))
        p.add_layout(legendlabelarrow)

    # labels = LabelSet(x=70, y=80, text=display_values, level='glyph',
    #          x_offset=0, y_offset=5, render_mode='canvas')
    # p.add_layout(labels)

    p.yaxis.major_label_text_font_size = '22pt'
    p.xaxis.visible = False
    p.outline_line_color = None
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_standoff = 0
    # p.legend.orientation = "horizontal"
    p.hover.renderers = [r]
    alpha = 1.0
    # add color bar
    if color_bar_title is None:
        color_bar_title = color_value
    color_bar = ColorBar(
        color_mapper=color_mapper,
        title=color_bar_title,
        title_text_font_size='12pt',
        ticker=BasicTicker(desired_num_ticks=10),
        border_line_color=None,
        background_fill_color=None,
        # 'vertical',
        label_standoff=cbar_standoff,
        location=(plot_width * 0.2, plot_height * 0.69),
        orientation='horizontal',
        scale_alpha=alpha,
        major_label_text_font_size=str(cbar_fontsize) + 'pt',
        height=cbar_height,
        width=cbar_width)

    p.add_layout(color_bar, 'center')

    # deactivate grid

    p.grid.grid_line_color = None

    # export_png(p, filename="plot.png")
    output_file(outfilename)

    if show:
        bshow(p)

    return p


@ensure_plotter_consistency(plot_params)
def plot_lattice_constant(scaling,
                          total_energy,
                          *,
                          fit_data=None,
                          data=None,
                          figure=None,
                          relative=True,
                          ref_const=None,
                          title='Equation of states',
                          saveas='lattice_constant',
                          copy_data=False,
                          **kwargs):
    """
    Plot a lattice constant versus Total energy
    Plot also the fit.
    On the x axis is the scaling, it

    :param scaling: arraylike, data for the scaling factor
    :param total_energy: arraylike, data for the total energy
    :param fit_data: arraylike, optional data of fitted data
    :param relative: bool, scaling factor given (True), or lattice constants given?
    :param ref_const: float (optional), or list of floats, lattice constant for scaling 1.0
    :param data: source for the data of the plot (optional) (pandas Dataframe for example)
    :param copy_data: bool if True the data argument will be copied
    :param figure: bokeh figure (optional), if provided the plot will be added to this figure

    Function specific parameters:
        :param marker_fit: defaults to `marker`, marker type for the fit data
        :param marker_size_fit: defaults to `marker_size`, markersize for the fit data
        :param line_width_fit: defaults to `line_width`, linewidth for the fit data
        :param legend_label_fit: str label for the fit data

    Other Kwargs will be passed on to :py:func:`bokeh_line()`
    """
    # TODO: make box which shows fit results. (fit resuls have to be past)

    plot_data = process_data_arguments(data=data,
                                       scaling=scaling,
                                       energy=total_energy,
                                       fit=fit_data,
                                       copy_data=copy_data,
                                       use_column_source=True)

    plot_params.single_plot = False
    plot_params.num_plots = len(plot_data)

    if relative:
        if ref_const:
            xlabel = rf'Relative Volume [a/{ref_const}$\AA$]'
        else:
            xlabel = r'Relative Volume'
    else:
        xlabel = r'Volume [$\AA$]'

    if len(plot_data) > 1:
        ylabel = r'Total energy norm[0] [eV]'
    else:
        ylabel = r'Total energy [eV]'

    #Add custom parameters for fit
    plot_params.add_parameter('marker_fit', default_from='marker')
    plot_params.add_parameter('marker_size_fit', default_from='marker_size')
    plot_params.add_parameter('line_width_fit', default_from='line_width')
    plot_params.add_parameter('legend_label_fit')

    plot_params.set_defaults(default_type='function',
                             marker_fit='square',
                             legend_label='simulation data',
                             legend_label_fit='fit results',
                             color='black' if len(plot_data) == 1 else None)

    kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)
    p = plot_params.prepare_figure(title=title, xlabel=xlabel, ylabel=ylabel, figure=figure)

    plot_kw = plot_params.plot_kwargs(post_process=False)
    plot_fit_kw_line = plot_params.plot_kwargs(post_process=False,
                                               plot_type='line',
                                               line_width='line_width_fit',
                                               legend_label='legend_label_fit')
    plot_fit_kw_scatter = plot_params.plot_kwargs(post_process=False,
                                                  plot_type='scatter',
                                                  marker='marker_fit',
                                                  marker_size='marker_size_fit',
                                                  legend_label='legend_label_fit')
    plot_fit_kw = {**plot_fit_kw_line, **plot_fit_kw_scatter}

    with NestedPlotParameters(plot_params):
        p = bokeh_line(plot_data.get_keys('scaling'),
                       plot_data.get_keys('energy'),
                       data=plot_data.data,
                       xlabel=xlabel,
                       ylabel=ylabel,
                       title=title,
                       figure=p,
                       show=False,
                       save_plots=False,
                       plot_points=True,
                       **plot_kw,
                       **kwargs)
    if any(entry.fit is not None for entry in plot_data.keys()):
        with NestedPlotParameters(plot_params):
            p = bokeh_line(plot_data.get_keys('scaling'),
                           plot_data.get_keys('fit'),
                           data=plot_data.data,
                           xlabel=xlabel,
                           ylabel=ylabel,
                           title=title,
                           figure=p,
                           show=False,
                           save_plots=False,
                           plot_points=True,
                           **plot_fit_kw,
                           **kwargs)

    plot_params.draw_straight_lines(p)
    plot_params.save_plot(p, saveas)

    return p


######## a 2d matrix plot ##########

######### plot convergence results plot ########


@ensure_plotter_consistency(plot_params)
def plot_convergence(iteration,
                     distance,
                     total_energy,
                     *,
                     data=None,
                     saveas_energy='energy_convergence',
                     saveas_distance='distance_convergence',
                     figure_energy=None,
                     figure_distance=None,
                     xlabel='Iteration',
                     ylabel_energy='Total energy difference [Htr]',
                     ylabel_distance='Distance [me/bohr^3]',
                     title_energy='Total energy difference over scf-Iterations',
                     title_distance='Convergence (log)',
                     copy_data=False,
                     drop_last_iteration=False,
                     **kwargs):
    """
    Plot the total energy differences versus the scf iteration
    and plot the distance of the density versus iterations.

    :param iteration: data for the number of iterations
    :param distance: data of distances
    :param total_energy: data of total energies
    :param data: source for the data of the plot (optional) (pandas Dataframe for example)
    :param xlabel: str, label for the x-axis of both plots
    :param saveas_energy: str, filename for the energy convergence plot
    :param figure_energy: Axes object for the energy convergence plot
    :param title_energy: str, title for the energy convergence plot
    :param ylabel_energy: str, label for the y-axis for the energy convergence plot
    :param saveas_distance: str, filename for the distance plot
    :param figure_distance: Axes object for the distance plot
    :param title_distance: str, title for the distance plot
    :param ylabel_distance: str, label for the y-axis for the distance plot
    :param copy_data: bool if  True the data argument is copied
    :param drop_last_iteration: bool if True the last iteration is dropped for the distance plot

    Other Kwargs will be passed on to all :py:func:`bokeh_line()` calls
    """

    plot_data = process_data_arguments(data=data,
                                       iteration=iteration,
                                       distance=distance,
                                       energy=total_energy,
                                       copy_data=copy_data,
                                       use_column_source=True)

    plot_params.single_plot = False
    plot_params.num_plots = len(plot_data)

    #Calculate energy differences and corresponding
    plot_data.copy_data('energy', 'energy_diff')
    plot_data.copy_data('iteration', 'iteration_energy')
    plot_data.apply('energy_diff', np.diff)
    plot_data.apply('energy_diff', np.abs)
    plot_data.apply('iteration_energy', np.delete, obj=0)
    plot_data.apply('iteration_energy', np.append, values=np.nan)
    plot_data.apply('energy_diff', np.append, values=np.nan)

    if drop_last_iteration:
        plot_data.apply('iteration', np.delete, obj=-1)

    if len(plot_data) == 1:
        default_energy_label = 'delta total energy'
        default_distance_label = 'distance'
    else:
        default_energy_label = [f'delta total energy {i}' for i in range(len(plot_data))]
        default_distance_label = [f'distance {i}' for i in range(len(plot_data))]

    plot_params.set_defaults(default_type='function',
                             legend_label=default_energy_label,
                             color='black' if len(plot_data) == 1 else None,
                             tooltips=[('Calculation id', '$name'), ('Iteration', '@{x}'),
                                       ('Total energy difference', '@{y}')],
                             figure_kwargs={
                                 'plot_width': 800,
                                 'plot_height': 450,
                                 'y_axis_type': 'log',
                                 'x_axis_type': 'linear',
                             },
                             legend_outside_plot_area=True)

    with NestedPlotParameters(plot_params):
        p1 = bokeh_line(plot_data.get_keys('iteration_energy'),
                        plot_data.get_keys('energy_diff'),
                        data=plot_data.data,
                        xlabel=xlabel,
                        ylabel=ylabel_energy,
                        title=title_energy,
                        saveas=saveas_energy,
                        figure=figure_energy,
                        plot_points=True,
                        set_default_legend=False,
                        **kwargs)

    plot_params.set_defaults(default_type='function',
                             legend_label=default_distance_label,
                             tooltips=[('Calculation id', '$name'), ('Iteration', '@{x}'), ('Charge distance', '@{y}')])

    with NestedPlotParameters(plot_params):
        p2 = bokeh_line(plot_data.get_keys('iteration'),
                        plot_data.get_keys('distance'),
                        data=plot_data.data,
                        xlabel=xlabel,
                        ylabel=ylabel_distance,
                        title=title_distance,
                        saveas=saveas_distance,
                        figure=figure_distance,
                        plot_points=True,
                        set_default_legend=False,
                        **kwargs)

    return p1, p2


@ensure_plotter_consistency(plot_params)
def plot_convergence_results(iteration, distance, total_energy, *, saveas='convergence', **kwargs):
    """
    Plot the total energy versus the scf iteration
    and plot the distance of the density versus iterations. Uses bokeh_line and bokeh_scatter

    :param iteration: list of Int
    :param distance: list of floats
    :total_energy: list of floats
    :param show: bool, if True call show

    Kwargs will be passed on to :py:func:`bokeh_line()`

    :returns grid: bokeh grid with figures
    """
    from bokeh.layouts import gridplot

    warnings.warn(
        'plot_convergence_results is deprecated. Use the more general plot_convergence instead.'
        'It can do both single and multiple calculations natively', DeprecationWarning)

    if 'show' in kwargs:
        plot_params.set_parameters(show=kwargs.pop('show'))
    if 'save_plots' in kwargs:
        plot_params.set_parameters(show=kwargs.pop('save_plots'))

    with NestedPlotParameters(plot_params):
        p1, p2 = plot_convergence(iteration, distance, total_energy, save_plots=False, show=False, **kwargs)

    grid = gridplot([p1, p2], ncols=1)

    plot_params.save_plot(grid, saveas)

    return grid


@ensure_plotter_consistency(plot_params)
def plot_convergence_results_m(iterations,
                               distances,
                               total_energies,
                               *,
                               link=False,
                               nodes=None,
                               modes=None,
                               plot_label=None,
                               saveas='convergence',
                               **kwargs):
    """
    Plot the total energy versus the scf iteration
    and plot the distance of the density versus iterations in a bokeh grid for several SCF results.

    :param distances: list of lists of floats
    :total_energies: list of lists of floats
    :param iterations: list of lists of Int
    :param link: bool, optional default=False:
    :param nodes: list of node uuids or pks important for links
    :param saveas1: str, optional default='t_energy_convergence', save first figure as
    :param saveas2: str, optional default='distance_convergence', save second figure as
    :param figure_kwargs: dict, optional default={'plot_width': 600, 'plot_height': 450}, gets parsed
                          to bokeh_line
    :param kwargs: further key-word arguments for bokeh_line

    :returns grid: bokeh grid with figures
    """
    from bokeh.layouts import gridplot

    warnings.warn(
        'plot_convergence_results_m is deprecated. Use the more general plot_convergence instead.'
        'It can do both single and multiple calculations natively', DeprecationWarning)

    if 'show' in kwargs:
        plot_params.set_parameters(show=kwargs.pop('show'))
    if 'save_plots' in kwargs:
        plot_params.set_parameters(show=kwargs.pop('save_plots'))
    if plot_label is not None:
        kwargs['legend_label'] = plot_label

    if modes is None:
        modes = []

    with NestedPlotParameters(plot_params):
        p1, p2 = plot_convergence(iterations,
                                  distances,
                                  total_energies,
                                  save_plots=False,
                                  show=False,
                                  drop_last_iteration=any(mode == 'force' for mode in modes),
                                  **kwargs)

    grid = gridplot([p1, p2], ncols=1)

    plot_params.save_plot(grid, saveas)

    return grid


######### plot_convex_hull plot ########


def plot_convex_hull2d(hull,
                       title='Convex Hull',
                       xlabel='Atomic Procentage',
                       ylabel='Formation energy / atom [eV]',
                       linestyle='-',
                       marker='o',
                       legend=True,
                       legend_option={},
                       saveas='convex_hull',
                       limits=[None, None],
                       scale=[None, None],
                       axis=None,
                       color='k',
                       color_line='k',
                       linewidth=2,
                       markersize=8,
                       marker_hull='o',
                       markersize_hull=8,
                       **kwargs):
    """
    Plot method for a 2d convex hull diagram

    :param hull: scipy.spatial.ConvexHull
    """
    pass
