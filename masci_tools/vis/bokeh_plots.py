# -*- coding: utf-8 -*-
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
from masci_tools.vis.bokeh_plotter import BokehPlotter
from masci_tools.vis import ensure_plotter_consistency, NestedPlotParameters

import pandas as pd
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


##################################### general plots ##########################


@ensure_plotter_consistency(plot_params)
def bokeh_scatter(source,
                  *,
                  xdata='x',
                  ydata='y',
                  xlabel='x',
                  ylabel='y',
                  title='',
                  figure=None,
                  outfilename='scatter.html',
                  **kwargs):
    """
    Create an interactive scatter plot with bokeh

    :param source: source for the data of the plot (pandas Dataframe for example)
    :param xdata: key from which to pull the data for the x-axis
    :param ydata: key from which to pull the data for the y-axis
    :param xlabel: label for the x-axis
    :param ylabel: label for the y-axis
    :param title: title of the figure
    :param figure: bokeh figure (optional), if provided the plot will be added to this figure
    :param outfilename: filename of the output file

    Kwargs will be passed on to :py:class:`masci_tools.vis.bokeh_plotter.BokehPlotter`.
    If the arguments are not recognized they are passed on to the bokeh function `scatter`
    """

    kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)

    p = plot_params.prepare_figure(title, xlabel, ylabel, figure=figure)

    res = p.scatter(x=xdata, y=ydata, source=source, **kwargs)

    if plot_params['level'] is not None:
        res.level = plot_params['level']

    plot_params.draw_straight_lines(p)
    plot_params.set_limits(p)
    plot_params.save_plot(p)

    return p


@ensure_plotter_consistency(plot_params)
def bokeh_multi_scatter(source,
                        *,
                        xdata='x',
                        ydata='y',
                        figure=None,
                        xlabel='x',
                        ylabel='y',
                        title='',
                        outfilename='scatter.html',
                        **kwargs):
    """
    Create an interactive scatter (muliple data sets possible) plot with bokeh

    :param source: source for the data of the plot (pandas Dataframe for example)
    :param xdata: key from which to pull the data for the x-axis (or if source is None list with data for x-axis)
    :param ydata: key from which to pull the data for the y-axis (or if source is None list with data for y-axis)
    :param xlabel: label for the x-axis
    :param ylabel: label for the y-axis
    :param title: title of the figure
    :param figure: bokeh figure (optional), if provided the plot will be added to this figure
    :param outfilename: filename of the output file

    Kwargs will be passed on to :py:class:`masci_tools.vis.bokeh_plotter.BokehPlotter`.
    If the arguments are not recognized they are passed on to the bokeh function `scatter`
    """
    from bokeh.models import ColumnDataSource

    plot_params.set_defaults(default_type='function', name='scatter plot')

    default_legend_label = ydata
    if source is not None:
        if not isinstance(ydata, list):
            if not isinstance(xdata, list):
                xdata = [xdata]
            ydata = [ydata] * len(xdata)
            default_legend_label = xdata

    if isinstance(xdata, list):
        if len(xdata) != len(ydata):
            xdata = xdata[0]

    plot_params.single_plot = False
    plot_params.num_plots = len(ydata)

    kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)
    p = plot_params.prepare_figure(title, xlabel, ylabel, figure=figure)

    #Process the given color arguments
    plot_params.set_color_palette_by_num_plots()

    # prepare ColumnDataSource for plot
    if source is None:  # create columndatasources from data given
        # Columns need to have same length
        source = []
        if isinstance(ydata[0], list):
            ydatad = []
            xdatad = []
            for i, ydat in enumerate(ydata):
                label = 'y{}'.format(i)
                ydatad.append(label)
                xdatad.append('x{}'.format(i))
                if isinstance(xdata[0], list):
                    xdat = xdata[i]
                else:
                    xdat = xdata[0]
                source.append(ColumnDataSource({'x': xdat, 'y': ydata}))
        else:
            raise ValueError('If no source dataframe or ColumnData is given, ydata has to be a list'
                             ' of lists, not of type: {}'.format(type(ydata[0])))
    else:
        xdatad = xdata
        ydatad = ydata

    # draw line plot
    # dataframe and column data source expect all entries to be same length...
    # therefore we parse data to plot routines directly... might make other things harder

    plot_kwargs = plot_params.plot_kwargs(plot_type='scatter')

    for indx, data in enumerate(zip(ydatad, plot_kwargs)):

        yname, plot_kw = data

        if isinstance(xdatad, list):
            xdat = xdatad[indx]
        else:
            xdat = xdatad

        if isinstance(source, list):
            sourcet = source[indx]
        else:
            sourcet = source

        if isinstance(default_legend_label, list):
            leg_label = default_legend_label[indx]
        else:
            leg_label = default_legend_label

        if 'legend_label' not in plot_kw:
            plot_kw['legend_label'] = leg_label

        res = p.scatter(x=xdat, y=yname, source=sourcet, **plot_kw)

        if plot_params[('level', indx)] is not None:
            res.level = plot_params[('level', indx)]

    plot_params.draw_straight_lines(p)
    plot_params.set_limits(p)
    plot_params.set_legend(p)
    plot_params.save_plot(p)

    return p


@ensure_plotter_consistency(plot_params)
def bokeh_line(source,
               *,
               xdata='x',
               ydata='y',
               figure=None,
               xlabel='x',
               ylabel='y',
               title='',
               outfilename='scatter.html',
               plot_points=False,
               **kwargs):
    """
    Create an interactive multi-line plot with bokeh

    :param source: source for the data of the plot (pandas Dataframe for example)
    :param xdata: key from which to pull the data for the x-axis (or if source is None list with data for x-axis)
    :param ydata: key from which to pull the data for the y-axis (or if source is None list with data for y-axis)
    :param xlabel: label for the x-axis
    :param ylabel: label for the y-axis
    :param title: title of the figure
    :param figure: bokeh figure (optional), if provided the plot will be added to this figure
    :param outfilename: filename of the output file
    :param plot_points: bool, if True also plot the points with a scatterplot on top

    Kwargs will be passed on to :py:class:`masci_tools.vis.bokeh_plotter.BokehPlotter`.
    If the arguments are not recognized they are passed on to the bokeh function `line`
    """
    from bokeh.models import ColumnDataSource

    plot_params.set_defaults(default_type='function', name='line plot')

    default_legend_label = ydata
    if source is not None:
        if not isinstance(ydata, list):
            if not isinstance(xdata, list):
                xdata = [xdata]
            ydata = [ydata] * len(xdata)
            default_legend_label = xdata

    if isinstance(xdata, list):
        if len(xdata) != len(ydata):
            xdata = xdata[0]

    plot_params.single_plot = False
    plot_params.num_plots = len(ydata)

    kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)
    p = plot_params.prepare_figure(title, xlabel, ylabel, figure=figure)

    #Process the given color arguments
    plot_params.set_color_palette_by_num_plots()

    # prepare ColumnDataSource for plot
    if source is None:  # create columndatasources from data given
        # Columns need to have same length
        source = []
        if isinstance(ydata[0], list):
            ydatad = []
            xdatad = []
            for i, ydat in enumerate(ydata):
                label = 'y{}'.format(i)
                ydatad.append(label)
                xdatad.append('x{}'.format(i))
                if isinstance(xdata[0], list):
                    xdat = xdata[i]
                else:
                    xdat = xdata[0]
                source.append(ColumnDataSource({'x': xdat, 'y': ydata}))
        else:
            raise ValueError('If no source dataframe or ColumnData is given, ydata has to be a list'
                             ' of lists, not of type: {}'.format(type(ydata[0])))
    else:
        xdatad = xdata
        ydatad = ydata

    # draw line plot
    # dataframe and column data source expect all entries to be same length...
    # therefore we parse data to plot routines directly... might make other things harder

    plot_kw_line = plot_params.plot_kwargs(plot_type='line')
    plot_kw_scatter = plot_params.plot_kwargs(plot_type='scatter')
    plot_kw_area = plot_params.plot_kwargs(plot_type='area')

    area_curve = kwargs.pop('area_curve', None)

    for indx, data in enumerate(zip(ydatad, plot_kw_line, plot_kw_scatter, plot_kw_area)):

        yname, kw_line, kw_scatter, kw_area = data

        if isinstance(xdatad, list):
            xdat = xdatad[indx]
        else:
            xdat = xdatad

        if isinstance(source, list):
            sourcet = source[indx]
        else:
            sourcet = source

        if isinstance(default_legend_label, list):
            leg_label = default_legend_label[indx]
        else:
            leg_label = default_legend_label

        if 'legend_label' not in kw_line:
            kw_line['legend_label'] = leg_label
            kw_scatter['legend_label'] = leg_label
            kw_area['legend_label'] = leg_label

        if area_curve is not None:
            if isinstance(area_curve, list):
                try:
                    shift = area_curve[indx]
                except IndexError:
                    shift = area_curve[0]
            else:
                shift = area_curve
        else:
            shift = 0

        if plot_params[('area_plot', indx)]:
            if plot_params[('area_vertical', indx)]:
                p.harea(y=yname, x1=xdat, x2=shift, **kw_area, source=sourcet)
            else:
                p.varea(x=xdat, y1=yname, y2=shift, **kw_area, source=sourcet)

        res = p.line(x=xdat, y=yname, source=sourcet, **kw_line, **kwargs)
        res2 = None
        if plot_points:
            res2 = p.scatter(x=xdat, y=yname, source=sourcet, **kw_scatter)

        if plot_params[('level', indx)] is not None:
            res.level = plot_params[('level', indx)]
            if res2 is not None:
                res2.level = plot_params[('level', indx)]

    plot_params.draw_straight_lines(p)
    plot_params.set_limits(p)
    plot_params.set_legend(p)
    plot_params.save_plot(p)

    return p


@ensure_plotter_consistency(plot_params)
def bokeh_dos(dosdata,
              *,
              energy='energy_grid',
              ynames=None,
              energy_label=r'E-E_F [eV]',
              dos_label=r'DOS [1/eV]',
              title=r'Density of states',
              xyswitch=False,
              e_fermi=0,
              outfilename='dos_plot.html',
              **kwargs):
    """
    Create an interactive dos plot (non-spinpolarized) with bokeh
    Both horizontal or vertical orientation are possible

    :param dosdata: source for the dosdata of the plot (pandas Dataframe for example)
    :param energy: key from which to pull the data for the energy grid
    :param ynames: keys from which to pull the data for dos components
    :param energy_label: label for the energy-axis
    :param dos_label: label for the dos-axis
    :param title: title of the figure
    :param xyswitch: bool if True, the energy will be plotted along the y-direction
    :param e_fermi: float, determines, where to put the line for the fermi energy
    :param outfilename: filename of the output file

    Kwargs will be passed on to :py:func:`bokeh_line()`
    """

    if 'limits' in kwargs:
        limits = kwargs.pop('limits')
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
                             figure_kwargs={
                                 'tooltips': [('Name', '$name'), ('Energy', '@energy_grid{0.0[00]}'),
                                              ('DOS value', '@$name{0.00}')],
                                 'width':
                                 1000,
                             })

    if ynames is None:
        ynames = set(dosdata.keys()) - set([energy] if isinstance(energy, str) else energy)
        ynames = sorted(ynames)

    if xyswitch:
        x, y = ynames, energy
        xlabel, ylabel = dos_label, energy_label
        plot_params.set_defaults(default_type='function', area_vertical=True)
    else:
        xlabel, ylabel = energy_label, dos_label
        x, y = energy, ynames

    p = bokeh_line(dosdata, xdata=x, ydata=y, xlabel=xlabel, ylabel=ylabel, title=title, name=ynames, **kwargs)

    return p


@ensure_plotter_consistency(plot_params)
def bokeh_spinpol_dos(dosdata,
                      *,
                      spin_dn_negative=True,
                      energy='energy_grid',
                      ynames=None,
                      energy_label=r'E-E_F [eV]',
                      dos_label=r'DOS [1/eV]',
                      title=r'Density of states',
                      xyswitch=False,
                      e_fermi=0,
                      spin_arrows=True,
                      outfilename='dos_plot.html',
                      **kwargs):
    """
    Create an interactive dos plot (spinpolarized) with bokeh
    Both horizontal or vertical orientation are possible

    :param dosdata: source for the dosdata of the plot (pandas Dataframe for example)
    :param energy: key from which to pull the data for the energy grid
    :param ynames: keys from which to pull the data for dos components
    :param spin_dn_negative: bool, if True (default), the spin down components are plotted downwards
    :param energy_label: label for the energy-axis
    :param dos_label: label for the dos-axis
    :param title: title of the figure
    :param xyswitch: bool if True, the energy will be plotted along the y-direction
    :param e_fermi: float, determines, where to put the line for the fermi energy
    :param spin_arrows: bool, if True (default) small arrows will be plotted on the left side of the plot indicating
                        the spin directions (if spin_dn_negative is True)
    :param outfilename: filename of the output file

    Kwargs will be passed on to :py:func:`bokeh_line()`
    """
    from bokeh.models import NumeralTickFormatter, Arrow, NormalHead

    if 'limits' in kwargs:
        limits = kwargs.pop('limits')
        if xyswitch:
            limits['x'], limits['y'] = limits.pop('dos', None), limits.pop('energy', None)
        else:
            limits['x'], limits['y'] = limits.pop('energy', None), limits.pop('dos', None)
        kwargs['limits'] = {k: v for k, v in limits.items() if v is not None}

    lines = {'horizontal': 0}
    lines['vertical'] = e_fermi

    if ynames is None:
        ynames = set(dosdata.keys()) - set([energy] if isinstance(energy, str) else energy)
        ynames = sorted(ynames)
        ynames.extend([f'{key} Spin-Down' for key in ynames])

    if spin_dn_negative:
        dosdata[[key for key in ynames if '_down' in key]] = -dosdata[[key for key in ynames if '_down' in key]]

    if xyswitch:
        lines['vertical'], lines['horizontal'] = lines['horizontal'], lines['vertical']

    plot_params.set_defaults(default_type='function',
                             straight_lines=lines,
                             figure_kwargs={
                                 'tooltips': [('DOS Name', '$name'), ('Energy', '@energy_grid{0.0[00]}'),
                                              ('Value', '@$name{(0,0.00)}')],
                                 'width':
                                 1000
                             })

    if xyswitch:
        x, y = ynames, energy
        xlabel, ylabel = dos_label, energy_label
        plot_params.set_defaults(default_type='function',
                                 area_vertical=True,
                                 x_axis_formatter=NumeralTickFormatter(format='(0,0)'))
    else:
        xlabel, ylabel = energy_label, dos_label
        x, y = energy, ynames
        plot_params.set_defaults(default_type='function',
                                 area_vertical=True,
                                 y_axis_formatter=NumeralTickFormatter(format='(0,0)'))

    plot_params.single_plot = False
    plot_params.num_plots = len(ynames) // 2  #We want the same colors for opposite spin-directions
    plot_params.set_parameters(color=kwargs.pop('color', None), color_palette=kwargs.pop('color_palette', None))
    plot_params.set_color_palette_by_num_plots()

    #Double the colors for spin up and down
    kwargs['color'] = list(plot_params['color'].copy())
    kwargs['color'].extend(kwargs['color'])

    if 'legend_label' not in kwargs:
        kwargs['legend_label'] = list(ynames.copy())
    else:
        if isinstance(kwargs['legend_label'], list):
            if len(kwargs['legend_label']) == len(ynames) // 2:
                kwargs['legend_label'].extend(kwargs['legend_label'])

    if 'show' in kwargs:
        plot_params.set_parameters(show=kwargs['show'])

    with NestedPlotParameters(plot_params):
        p = bokeh_line(dosdata,
                       xdata=x,
                       ydata=y,
                       xlabel=xlabel,
                       ylabel=ylabel,
                       title=title,
                       name=ynames,
                       show=False,
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

    plot_params.save_plot(p)

    return p


@ensure_plotter_consistency(plot_params)
def bokeh_bands(bandsdata,
                *,
                k_label='kpath',
                eigenvalues='eigenvalues_up',
                weight=None,
                xlabel='',
                ylabel=r'E-E_F [eV]',
                title='',
                special_kpoints=None,
                size_min=3.0,
                size_scaling=10.0,
                outfilename='bands_plot.html',
                **kwargs):
    """
    Create an interactive bandstructure plot (non-spinpolarized) with bokeh
    Can make a simple plot or weight the size and color of the points against a given weight

    :param bandsdata: source for the bandsdata of the plot (pandas Dataframe for example)
    :param k_label: key from which to pull the data for the kpoints
    :param eigenvalues: key from which to pull the data for eigenvalues
    :param weight: optional key from the bandsdata. If given the size and color of each point
                   are adjusted to show the weights
    :param xlabel: label for the x-axis (default no label)
    :param ylabel: label for the y-axis
    :param title: title of the figure
    :param special_kpoints: list of tuples (str, float), place vertical lines at the given values
                            and mark them on the x-axis with the given label
    :param e_fermi: float, determines, where to put the line for the fermi energy
    :param size_min: minimum value used in scaling points for weight
    :param size_scaling: factor used in scaling points for weight
    :param outfilename: filename of the output file

    Kwargs will be passed on to :py:func:`bokeh_multi_scatter()`
    """
    from bokeh.transform import linear_cmap

    if weight is not None:

        ylimits = (-15, 15)
        if 'limits' in kwargs:
            if 'y' in kwargs['limits']:
                ylimits = kwargs['limits']['y']

        weight_max = bandsdata[weight].loc[(bandsdata[eigenvalues] > ylimits[0]) &
                                           (bandsdata[eigenvalues] < ylimits[1])].max()

        bandsdata['weight_size'] = size_min + size_scaling * bandsdata[weight] / weight_max
        plot_params.set_defaults(default_type='function',
                                 color=linear_cmap(weight, 'Blues256', weight_max, -0.05),
                                 marker_size='weight_size')
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
                             limits=limits)

    return bokeh_multi_scatter(bandsdata,
                               xdata=k_label,
                               ydata=eigenvalues,
                               xlabel='',
                               ylabel=ylabel,
                               title=title,
                               **kwargs)


@ensure_plotter_consistency(plot_params)
def bokeh_spinpol_bands(bandsdata,
                        *,
                        k_label='kpath',
                        eigenvalues=None,
                        weight=None,
                        xlabel='',
                        ylabel=r'E-E_F [eV]',
                        title='',
                        special_kpoints=None,
                        size_min=3.0,
                        size_scaling=10.0,
                        outfilename='bands_plot.html',
                        **kwargs):
    """
    Create an interactive bandstructure plot (spinpolarized) with bokeh
    Can make a simple plot or weight the size and color of the points against a given weight

    :param bandsdata: source for the bandsdata of the plot (pandas Dataframe for example)
    :param k_label: key from which to pull the data for the kpoints
    :param eigenvalues: keys from which to pull the data for eigenvalues (default ['eigenvalues_up','eigenvalues_down'])
    :param weight: optional key from the bandsdata. If given the size and color of each point
                   are adjusted to show the weights
    :param xlabel: label for the x-axis (default no label)
    :param ylabel: label for the y-axis
    :param title: title of the figure
    :param special_kpoints: list of tuples (str, float), place vertical lines at the given values
                            and mark them on the x-axis with the given label
    :param e_fermi: float, determines, where to put the line for the fermi energy
    :param size_min: minimum value used in scaling points for weight
    :param size_scaling: factor used in scaling points for weight
    :param outfilename: filename of the output file

    Kwargs will be passed on to :py:func:`bokeh_multi_scatter()`
    """
    from bokeh.transform import linear_cmap

    if eigenvalues is None:
        eigenvalues = ['eigenvalues_up', 'eigenvalues_down']

    plot_params.single_plot = False
    plot_params.num_plots = 2

    if weight is not None:
        cmaps = ['Blues256', 'Reds256']
        color = []

        ylimits = (-15, 15)
        if 'limits' in kwargs:
            if 'y' in kwargs['limits']:
                ylimits = kwargs['limits']['y']

        weight_max = bandsdata[weight[0]].loc[(bandsdata[eigenvalues[0]] > ylimits[0]) &
                                              (bandsdata[eigenvalues[0]] < ylimits[1])].max()
        weight_max = max(
            weight_max, bandsdata[weight[1]].loc[(bandsdata[eigenvalues[1]] > ylimits[0]) &
                                                 (bandsdata[eigenvalues[1]] < ylimits[1])].max())

        for indx, (w, cmap) in enumerate(zip(weight, cmaps)):
            color.append(linear_cmap(w, cmap, weight_max, -0.05))
            bandsdata[f'weight_size_{indx}'] = size_min + size_scaling * bandsdata[w] / weight_max
        plot_params.set_defaults(default_type='function', color=color, marker_size=['weight_size_0', 'weight_size_1'])
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
                             level=[None, 'underlay'])

    return bokeh_multi_scatter(bandsdata,
                               xdata=k_label,
                               ydata=eigenvalues,
                               xlabel='',
                               ylabel=ylabel,
                               title=title,
                               **kwargs)


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
                raise ValueError('Entry for element ' + datum + ' is negative but' ' log-scale is selected')
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


######## a 2d matrix plot ##########

######### plot convergence results plot ########


@ensure_plotter_consistency(plot_params)
def plot_convergence_results(iteration, distance, total_energy, *, show=True, **kwargs):
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

    xlabel = r'Iteration'
    ylabel1 = r'Total energy difference [Htr]'
    ylabel2 = r'Distance [me/bohr^3]'
    title1 = r'Total energy difference over scf-Iterations'
    title2 = r'Convergence (log)'

    # since we make a log plot of the total_energy make sure to plot the absolute total energy
    total_energy_abs_diff = []
    for en0, en1 in zip(total_energy[:-1], total_energy[1:]):
        total_energy_abs_diff.append(abs(en1 - en0))

    source1 = pd.DataFrame({'total_energy_delta': total_energy_abs_diff, 'iterations': iteration[1:]})
    source2 = pd.DataFrame({'distance': distance, 'iterations': iteration})

    plot_params.set_defaults(default_type='function',
                             figure_kwargs={
                                 'tools': 'hover,tap,box_zoom,zoom_out,crosshair,reset,save',
                                 'tooltips': [('Iteration', '@x'), ('Total energy distance', '@y')],
                                 'active_inspect': 'hover',
                                 'plot_width': 800,
                                 'plot_height': 450,
                                 'y_axis_type': 'log',
                                 'x_axis_type': 'linear',
                             })

    plot_params.set_parameters(show=show)

    with NestedPlotParameters(plot_params):
        p1 = bokeh_line(source=source1,
                        ydata='total_energy_delta',
                        xdata='iterations',
                        xlabel=xlabel,
                        ylabel=ylabel1,
                        title=title1,
                        name='delta total energy',
                        plot_points=True,
                        show=False,
                        **kwargs)

    plot_params.set_defaults(default_type='function',
                             figure_kwargs={'tooltips': [('Iteration', '@x'), ('Charge distance', '@y')]})

    with NestedPlotParameters(plot_params):
        p2 = bokeh_line(source=source2,
                        ydata='distance',
                        xdata='iterations',
                        xlabel=xlabel,
                        ylabel=ylabel2,
                        title=title2,
                        name='distance',
                        plot_points=True,
                        show=False,
                        **kwargs)

    grid = gridplot([p1, p2], ncols=2)

    plot_params.save_plot(grid)

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
                               saveas1='t_energy_convergence',
                               saveas2='distance_convergence',
                               show=True,
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
    from bokeh.models import ColumnDataSource
    from bokeh.layouts import gridplot

    xlabel = r'Iteration'
    ylabel1 = r'Total energy difference [Htr]'
    ylabel2 = r'Distance [me/bohr^3]'
    title1 = r'Total energy difference over scf-Iterations'
    title2 = r'Convergence (log)'

    if nodes is not None:
        if not isinstance(nodes, list):
            nodes = [nodes]

    if plot_label is not None:
        if not isinstance(plot_label, list):
            plot_label = [plot_label]

    plot_labels1 = []
    plot_labels2 = []

    data_sources = []
    data_sources2 = []

    tooltips_scatter1 = [('Calculation id', '@id'), ('Iteration', '@x'), ('Total energy difference', '@y')]
    tooltips_scatter2 = [('Calculation id', '@id'), ('Iteration', '@x'), ('Charge distance', '@y')]

    xdata = ['x'] * len(total_energies)
    ydata = ['y'] * len(total_energies)

    # since we make a log plot of the total_energy make sure to plot the absolute total energy
    for i, (iters, total_energy, distance) in enumerate(zip(iterations, total_energies, distances)):
        if nodes is not None:
            node_id = nodes[i]
        else:
            node_id = i

        total_energy_abs_diff = []
        for en0, en1 in zip(total_energy[:-1], total_energy[1:]):
            total_energy_abs_diff.append(abs(en1 - en0))

        plot_labels1.append(f'{node_id}')
        plot_labels2.append(f'{node_id}')
        data = {'y': total_energy_abs_diff, 'x': iters[1:], 'id': [node_id] * len(total_energy_abs_diff)}
        if nodes is not None:
            data['nodes_pk'] = [str(nodes[i])] * len(total_energy_abs_diff)
        if plot_label is not None:
            data['process_label'] = [plot_label[i]] * len(total_energy_abs_diff)

        datasrc = ColumnDataSource(data)
        data_sources.append(datasrc)
        data = {'y': distance, 'x': iters, 'id': [node_id] * len(distance)}
        if nodes is not None:
            data['nodes_pk'] = [str(nodes[i])] * len(distance)
        if plot_label is not None:
            data['process_label'] = [plot_label[i]] * len(distance)

        datasrc = ColumnDataSource(data)
        data_sources2.append(datasrc)

    if plot_label is not None:
        if nodes is None:
            plot_labels1 = plot_label
            plot_labels2 = plot_label
        tooltips_scatter1.append(('process label', '@process_label'))
        tooltips_scatter2.append(('process label', '@process_label'))

    if nodes is not None:
        tooltips_scatter1.append(('outpara pk', '@nodes_pk'))
        tooltips_scatter2.append(('outpara pk', '@nodes_pk'))

    plot_params.set_defaults(default_type='function',
                             figure_kwargs={
                                 'tools': 'hover,tap,box_zoom,zoom_out,crosshair,reset,save,pan',
                                 'tooltips': tooltips_scatter1,
                                 'active_inspect': 'hover',
                                 'plot_width': 800,
                                 'plot_height': 450,
                                 'y_axis_type': 'log',
                                 'x_axis_type': 'linear',
                             },
                             legend_outside_plot_area=True)
    plot_params.set_parameters(show=show)

    # plot
    with NestedPlotParameters(plot_params):
        p1 = bokeh_line(source=data_sources,
                        ydata=ydata,
                        xdata=xdata,
                        xlabel=xlabel,
                        ylabel=ylabel1,
                        title=title1,
                        name=plot_labels1,
                        legend_label=plot_labels1,
                        plot_points=True,
                        show=False,
                        **kwargs)

    plot_params.set_defaults(default_type='function', figure_kwargs={
        'tooltips': tooltips_scatter2,
    })

    with NestedPlotParameters(plot_params):
        p2 = bokeh_line(source=data_sources2,
                        ydata=ydata,
                        xdata=xdata,
                        xlabel=xlabel,
                        ylabel=ylabel2,
                        title=title2,
                        name=plot_labels2,
                        legend_label=plot_labels2,
                        plot_points=True,
                        show=False,
                        **kwargs)

    grid = gridplot([p1, p2], ncols=2)

    plot_params.save_plot(grid)

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
