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
In this module are plot routines collected to create default plots out of certain
ouput nodes from certain workflows with matplot lib.

Comment: Do not use any aiida methods, otherwise the methods in here can become
tricky to use inside a virtual environment. Make the user extract thing out of
aiida objects before hand or write something on top. Since usually parameter nodes,
or files are plotted, parse a dict or filepath.

Each of the plot_methods can take keyword arguments to modify parameters of the plots
There are keywords that are handled by a special class for defaults. All other arguments
will be passed on to the matplotlib plotting calls

For the definition of the defaults refer to :py:class:`~masci_tools.vis.matplotlib_plotter.MatplotlibPlotter`

"""
# TODO but allow to optional parse information for saving and title,
#  (that user can put pks or structure formulas in there)
# Write/export data to file for all methods

from .matplotlib_plotter import MatplotlibPlotter
from masci_tools.vis import ensure_plotter_consistency, NestedPlotParameters
import warnings
import copy
import typing

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from pprint import pprint
import pandas as pd

plot_params = MatplotlibPlotter()


def set_mpl_plot_defaults(**kwargs):
    """
    Set defaults for matplotib backend
    according to the given keyword arguments

    Available defaults can be seen in :py:class:`~masci_tools.vis.matplotlib_plotter.MatplotlibPlotter`
    """
    plot_params.set_defaults(**kwargs)


def reset_mpl_plot_defaults():
    """
    Reset the defaults for matplotib backend
    to the hardcoded defaults

    Available defaults can be seen in :py:class:`~masci_tools.vis.matplotlib_plotter.MatplotlibPlotter`
    """
    plot_params.reset_defaults()


def show_mpl_plot_defaults():
    """
    Show the currently set defaults for matplotib backend
    to the hardcoded defaults

    Available defaults can be seen in :py:class:`~masci_tools.vis.matplotlib_plotter.MatplotlibPlotter`
    """
    pprint(plot_params.get_dict())


def get_mpl_help(key):
    """
    Print the decription of the given key in the matplotlib backend

    Available defaults can be seen in :py:class:`~masci_tools.vis.matplotlib_plotter.MatplotlibPlotter`
    """
    plot_params.get_description(key)


###############################################################################
########################## general plot routines ##############################
###############################################################################


@ensure_plotter_consistency(plot_params)
def single_scatterplot(xdata,
                       ydata,
                       *,
                       xlabel='',
                       ylabel='',
                       title='',
                       saveas='scatterplot',
                       axis=None,
                       xerr=None,
                       yerr=None,
                       area_curve=None,
                       **kwargs):
    """
    Create a standard scatter plot (this should be flexible enough) to do all the
    basic plots.

    :param xdata: arraylike, data for the x coordinate
    :param ydata: arraylike, data for the y coordinate
    :param xlabel: str, label written on the x axis
    :param ylabel: str, label written on the y axis
    :param title: str, title of the figure
    :param saveas: str specifying the filename (without file format)
    :param axis: Axes object, if given the plot will be applied to this object
    :param xerr: optional data for errorbar in x-direction
    :param yerr: optional data for errorbar in y-direction
    :param area_curve: if an area plot is made this arguments defines the other enclosing line
                       defaults to 0

    Kwargs will be passed on to :py:class:`masci_tools.vis.matplotlib_plotter.MatplotlibPlotter`.
    If the arguments are not recognized they are passed on to the matplotlib functions
    (`errorbar` or `fill_between`)
    """
    #DEPRECATION WARNINGS
    if 'plotlabel' in kwargs:
        warnings.warn('Please use plot_label instead of plotlabel', DeprecationWarning)
        kwargs['plot_label'] = kwargs.pop('plotlabel')

    if 'scale' in kwargs:
        scale = kwargs.get('scale')
        if isinstance(scale, list):
            warnings.warn("Please provide scale as dict in the form {'x': value, 'y': value2}", DeprecationWarning)
            scale_new = {}
            if scale[0] is not None:
                scale_new['x'] = scale[0]
            if scale[1] is not None:
                scale_new['y'] = scale[1]
            kwargs['scale'] = scale_new

    if 'limits' in kwargs:
        limits = kwargs.get('limits')
        if isinstance(limits, list):
            warnings.warn("Please provide limits as dict in the form {'x': value, 'y': value2}", DeprecationWarning)
            limits_new = {}
            if limits[0] is not None:
                limits_new['x'] = limits[0]
            if limits[1] is not None:
                limits_new['y'] = limits[1]
            kwargs['limits'] = limits_new

    plot_params.set_defaults(default_type='function', color='k', plot_label='scatterplot')
    kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)
    ax = plot_params.prepare_plot(title=title, xlabel=xlabel, ylabel=ylabel, axis=axis)

    #ax.xaxis.set_major_formatter(DateFormatter("%b %y"))
    #if yerr or xerr:
    #    p1 = ax.errorbar(xdata, ydata, linetyp, label=plotlabel, color=color,
    #                 linewidth=linewidth_g, markersize=markersize_g, yerr=yerr, xerr=xerr)
    #else:
    #    p1 = ax.plot(xdata, ydata, linetyp, label=plotlabel, color=color,
    #                 linewidth=linewidth_g, markersize=markersize_g)
    # TODO customizable error bars fmt='o', ecolor='g', capthick=2, ...
    # there the if is prob better...
    plot_kwargs = plot_params.plot_kwargs()
    if area_curve is None:
        shift = 0
    else:
        shift = area_curve

    if plot_params['area_plot']:
        linecolor = plot_kwargs.pop('area_linecolor', None)
        if plot_params['area_vertical']:
            result = ax.fill_betweenx(ydata, xdata, x2=shift, **plot_kwargs, **kwargs)
        else:
            result = ax.fill_between(xdata, ydata, y2=shift, **plot_kwargs, **kwargs)
        plot_kwargs.pop('alpha', None)
        plot_kwargs.pop('label', None)
        plot_kwargs.pop('color', None)
        if plot_params['area_enclosing_line']:
            if linecolor is None:
                linecolor = result.get_facecolor()[0]
            ax.errorbar(xdata,
                        ydata,
                        yerr=yerr,
                        xerr=xerr,
                        alpha=plot_params['plot_alpha'],
                        color=linecolor,
                        **plot_kwargs,
                        **kwargs)
    else:
        ax.errorbar(xdata, ydata, yerr=yerr, xerr=xerr, **plot_kwargs, **kwargs)

    plot_params.set_scale(ax)
    plot_params.set_limits(ax)
    plot_params.draw_lines(ax)
    plot_params.save_plot(saveas)

    return ax


@ensure_plotter_consistency(plot_params)
def multiple_scatterplots(xdata,
                          ydata,
                          *,
                          xlabel='',
                          ylabel='',
                          title='',
                          saveas='mscatterplot',
                          axis=None,
                          xerr=None,
                          yerr=None,
                          area_curve=None,
                          **kwargs):
    """
    Create a standard scatter plot with multiple sets of data (this should be flexible enough)
    to do all the basic plots.

    :param xdata: arraylike, data for the x coordinate
    :param ydata: arraylike, data for the y coordinate
    :param xlabel: str, label written on the x axis
    :param ylabel: str, label written on the y axis
    :param title: str, title of the figure
    :param saveas: str specifying the filename (without file format)
    :param axis: Axes object, if given the plot will be applied to this object
    :param xerr: optional data for errorbar in x-direction
    :param yerr: optional data for errorbar in y-direction
    :param area_curve: if an area plot is made this arguments defines the other enclosing line
                       defaults to 0

    Kwargs will be passed on to :py:class:`masci_tools.vis.matplotlib_plotter.MatplotlibPlotter`.
    If the arguments are not recognized they are passed on to the matplotlib functions
    (`errorbar` or `fill_between`)
    """

    nplots = len(ydata)
    if nplots != len(xdata):  # todo check dimention not len, without moving to special datatype.
        print('ydata and xdata must have the same dimension')
        return

    if not isinstance(ydata[0], (list, np.ndarray, pd.Series)):
        xdata, ydata = [xdata], [ydata]

    plot_params.single_plot = False
    plot_params.num_plots = len(ydata)

    #DEPRECATION WARNINGS
    if 'plot_labels' in kwargs:
        warnings.warn('Please use plot_label instead of plot_labels', DeprecationWarning)
        kwargs['plot_label'] = kwargs.pop('plot_labels')

    if 'colors' in kwargs:
        warnings.warn('Please use color instead of colors', DeprecationWarning)
        kwargs['color'] = kwargs.pop('colors')

    if 'legend_option' in kwargs:
        warnings.warn('Please use legend_options instead of legend_option', DeprecationWarning)
        kwargs['legend_options'] = kwargs.pop('legend_option')

    if 'scale' in kwargs:
        scale = kwargs.get('scale')
        if isinstance(scale, list):
            warnings.warn("Please provide scale as dict in the form {'x': value, 'y': value2}", DeprecationWarning)
            scale_new = {}
            if scale[0] is not None:
                scale_new['x'] = scale[0]
            if scale[1] is not None:
                scale_new['y'] = scale[1]
            kwargs['scale'] = scale_new

    if 'limits' in kwargs:
        limits = kwargs.get('limits')
        if isinstance(limits, list):
            warnings.warn("Please provide limits as dict in the form {'x': value, 'y': value2}", DeprecationWarning)
            limits_new = {}
            if limits[0] is not None:
                limits_new['x'] = limits[0]
            if limits[1] is not None:
                limits_new['y'] = limits[1]
            kwargs['limits'] = limits_new

    if 'xticks' in kwargs:
        xticks = kwargs.get('xticks')
        if isinstance(xticks[0], list):
            warnings.warn('Please provide xticks and xticklabels seperately as two lists', DeprecationWarning)
            kwargs['xticklabels'] = xticks[0]
            kwargs['xticks'] = xticks[1]

    kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)
    ax = plot_params.prepare_plot(title=title, xlabel=xlabel, ylabel=ylabel, axis=axis)

    # TODO good checks for input and setting of internals before plotting
    # allow all arguments as value then use for all or as lists with the righ length.

    plot_kwargs = plot_params.plot_kwargs()
    colors = []

    for indx, data in enumerate(zip(xdata, ydata, plot_kwargs)):

        x, y, plot_kw = data

        if plot_params['repeat_colors_after'] is not None:
            if indx >= plot_params['repeat_colors_after']:
                plot_kw['color'] = colors[indx % plot_params['repeat_colors_after']]

        if isinstance(yerr, list):
            try:
                yerrt = yerr[indx]
            except IndexError:
                yerrt = yerr[0]
        else:
            yerrt = yerr

        if isinstance(xerr, list):
            try:
                xerrt = xerr[indx]
            except IndexError:
                xerrt = xerr[0]
        else:
            xerrt = xerr

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
            linecolor = plot_kw.pop('area_linecolor', None)
            if plot_params[('area_vertical', indx)]:
                result = ax.fill_betweenx(y, x, x2=shift, **plot_kw, **kwargs)
            else:
                result = ax.fill_between(x, y, y2=shift, **plot_kw, **kwargs)
            colors.append(result.get_facecolor()[0])
            plot_kw.pop('alpha', None)
            plot_kw.pop('label', None)
            plot_kw.pop('color', None)
            if plot_params[('area_enclosing_line', indx)]:
                if linecolor is None:
                    linecolor = result.get_facecolor()[0]
                ax.errorbar(x,
                            y,
                            yerr=yerrt,
                            xerr=xerrt,
                            alpha=plot_params[('plot_alpha', indx)],
                            color=linecolor,
                            **plot_kw,
                            **kwargs)
        else:
            result = ax.errorbar(x, y, yerr=yerrt, xerr=xerrt, **plot_kw, **kwargs)
            colors.append(result.lines[0].get_color())

    plot_params.set_scale(ax)
    plot_params.set_limits(ax)
    plot_params.draw_lines(ax)
    plot_params.show_legend(ax)
    plot_params.save_plot(saveas)

    return ax


@ensure_plotter_consistency(plot_params)
def multi_scatter_plot(xdata,
                       ydata,
                       *,
                       size_data=None,
                       color_data=None,
                       xlabel='',
                       ylabel='',
                       title='',
                       saveas='mscatterplot',
                       axis=None,
                       **kwargs):
    """
    Create a scatter plot with varying marker size
    Info: x, y, size and color data must have the same dimensions.

    :param xdata: arraylike, data for the x coordinate
    :param ydata: arraylike, data for the y coordinate
    :param size_data: arraylike, data for the markersizes (optional)
    :param color_data: arraylike, data for the color values with a colormap (optional)
    :param xlabel: str, label written on the x axis
    :param ylabel: str, label written on the y axis
    :param title: str, title of the figure
    :param saveas: str specifying the filename (without file format)
    :param axis: Axes object, if given the plot will be applied to this object
    :param xerr: optional data for errorbar in x-direction
    :param yerr: optional data for errorbar in y-direction

    Kwargs will be passed on to :py:class:`masci_tools.vis.matplotlib_plotter.MatplotlibPlotter`.
    If the arguments are not recognized they are passed on to the matplotlib function `scatter`
    """

    nplots = len(ydata)
    if nplots != len(xdata):  # todo check dimention not len, without moving to special datatype.
        print('ydata and xdata must have the same dimension')
        return

    if not isinstance(ydata[0], (list, np.ndarray, pd.Series)):
        xdata, ydata, size_data, color_data = [xdata], [ydata], [size_data], [color_data]

    plot_params.single_plot = False
    plot_params.num_plots = len(ydata)

    #DEPRECATION WARNINGS: label/plot_labels, alpha, limits, scale, legend_option, xticks

    if 'label' in kwargs:
        warnings.warn('Please use plot_label instead of label', DeprecationWarning)
        kwargs['plot_label'] = kwargs.pop('label')

    if 'alpha' in kwargs:
        warnings.warn('Please use plot_alpha instead of alpha', DeprecationWarning)
        kwargs['plot_alpha'] = kwargs.pop('alpha')

    if 'legend_option' in kwargs:
        warnings.warn('Please use legend_options instead of legend_option', DeprecationWarning)
        kwargs['legend_options'] = kwargs.pop('legend_option')

    if 'scale' in kwargs:
        scale = kwargs.get('scale')
        if isinstance(scale, list):
            warnings.warn("Please provide scale as dict in the form {'x': value, 'y': value2}", DeprecationWarning)
            scale_new = {}
            if scale[0] is not None:
                scale_new['x'] = scale[0]
            if scale[1] is not None:
                scale_new['y'] = scale[1]
            kwargs['scale'] = scale_new

    if 'limits' in kwargs:
        limits = kwargs.get('limits')
        if isinstance(limits, list):
            warnings.warn("Please provide limits as dict in the form {'x': value, 'y': value2}", DeprecationWarning)
            limits_new = {}
            if limits[0] is not None:
                limits_new['x'] = limits[0]
            if limits[1] is not None:
                limits_new['y'] = limits[1]
            kwargs['limits'] = limits_new

    if 'xticks' in kwargs:
        xticks = kwargs.get('xticks')
        if isinstance(xticks[0], list):
            warnings.warn('Please provide xticks and xticklabels seperately as two lists', DeprecationWarning)
            kwargs['xticklabels'] = xticks[0]
            kwargs['xticks'] = xticks[1]

    plot_params.set_defaults(default_type='function', linestyle=None, area_plot=False, colorbar=False)
    kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)
    ax = plot_params.prepare_plot(title=title, xlabel=xlabel, ylabel=ylabel, axis=axis)

    plot_kwargs = plot_params.plot_kwargs(ignore='markersize', extra_keys={'cmap'})

    legend_elements = []
    legend_labels = []

    if size_data is None:
        size_data = [None] * plot_params.num_plots

    if color_data is None:
        color_data = [None] * plot_params.num_plots

    for indx, data in enumerate(zip(xdata, ydata, size_data, color_data, plot_kwargs)):

        x, y, size, color, plot_kw = data

        if size is None:
            size = plot_params['markersize']

        if color is not None:
            plot_kw.pop('color')

        res = ax.scatter(x, y=y, s=size, c=color, **plot_kw, **kwargs)
        if plot_kw.get('label', None) is not None and color is not None:
            legend_elements.append(res.legend_elements(num=1)[0][0])
            legend_labels.append(plot_kw['label'])

    if any(c is not None for c in color_data):
        legend_elements = (legend_elements, legend_labels)
    else:
        legend_elements = None

    plot_params.set_scale(ax)
    plot_params.set_limits(ax)
    plot_params.draw_lines(ax)
    plot_params.show_legend(ax, leg_elems=legend_elements)
    plot_params.show_colorbar(ax)
    plot_params.save_plot(saveas)

    return ax


@ensure_plotter_consistency(plot_params)
def colormesh_plot(xdata, ydata, cdata, *, xlabel='', ylabel='', title='', saveas='colormesh', axis=None, **kwargs):
    """
    Create plot with pcolormesh

    :param xdata: arraylike, data for the x coordinate
    :param ydata: arraylike, data for the y coordinate
    :param cdata: arraylike, data for the color values with a colormap
    :param xlabel: str, label written on the x axis
    :param ylabel: str, label written on the y axis
    :param title: str, title of the figure
    :param saveas: str specifying the filename (without file format)
    :param axis: Axes object, if given the plot will be applied to this object

    Kwargs will be passed on to :py:class:`masci_tools.vis.matplotlib_plotter.MatplotlibPlotter`.
    If the arguments are not recognized they are passed on to the matplotlib function `pcolormesh`
    """

    #Set default limits (not setting them leaves empty border)
    limits = kwargs.pop('limits', {})
    if 'x' not in limits:
        limits['x'] = (xdata.min(), xdata.max())
    if 'y' not in limits:
        limits['y'] = (ydata.min(), ydata.max())
    kwargs['limits'] = limits

    plot_params.set_defaults(default_type='function', edgecolor='face')
    kwargs = plot_params.set_parameters(continue_on_error=True, area_plot=False, **kwargs)
    ax = plot_params.prepare_plot(title=title, xlabel=xlabel, ylabel=ylabel, axis=axis)

    plot_kwargs = plot_params.plot_kwargs(plot_type='colormesh')

    ax.pcolormesh(xdata, ydata, cdata, **plot_kwargs, **kwargs)

    plot_params.set_scale(ax)
    plot_params.set_limits(ax)
    plot_params.show_legend(ax)
    plot_params.show_colorbar(ax)
    plot_params.draw_lines(ax)
    plot_params.save_plot(saveas)

    return ax


@ensure_plotter_consistency(plot_params)
def waterfall_plot(xdata,
                   ydata,
                   zdata,
                   *,
                   xlabel='',
                   ylabel='',
                   zlabel='',
                   title='',
                   saveas='waterfallplot',
                   axis=None,
                   **kwargs):
    """
    Create a standard waterfall plot

    :param xdata: arraylike, data for the x coordinate
    :param ydata: arraylike, data for the y coordinate
    :param zdata: arraylike, data for the z coordinate
    :param xlabel: str, label written on the x axis
    :param ylabel: str, label written on the y axis
    :param zlabel: str, label written on the z axis
    :param title: str, title of the figure
    :param axis: Axes object, if given the plot will be applied to this object
    :param saveas: str specifying the filename (without file format)

    Kwargs will be passed on to :py:class:`masci_tools.vis.matplotlib_plotter.MatplotlibPlotter`.
    If the arguments are not recognized they are passed on to the matplotlib function `scatter3D`
    """

    nplots = len(ydata)
    if nplots != len(xdata):  # todo check dimention not len, without moving to special datatype.
        print('ydata and xdata must have the same dimension')
        return
    if nplots != len(zdata):  # todo check dimention not len, without moving to special datatype.
        print('ydata and zdata must have the same dimension')
        return

    if isinstance(zdata, np.ndarray):
        zmin = zdata.min()
        zmax = zdata.max()
    else:
        zmin = min(zdata)
        zmax = max(zdata)

    clim = None
    if 'limits' in kwargs:
        clim = kwargs['limits'].get('color', None)
    else:
        kwargs['limits'] = {}
    if clim is None:
        clim = (kwargs.get('vmin', zmin), kwargs.get('vmax', zmax))
    kwargs['limits']['color'] = clim

    if not isinstance(ydata[0], (list, np.ndarray, pd.Series)):
        xdata, ydata, zdata = [xdata], [ydata], [zdata]

    plot_params.single_plot = False
    plot_params.num_plots = len(ydata)

    plot_params.set_defaults(default_type='function', markersize=30, linewidth=0, area_plot=False)
    kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)
    ax = plot_params.prepare_plot(title=title, xlabel=xlabel, ylabel=ylabel, zlabel=zlabel, axis=axis, projection='3d')

    plot_kwargs = plot_params.plot_kwargs(ignore=['markersize'], extra_keys={'cmap'})

    for indx, data in enumerate(zip(xdata, ydata, zdata, plot_kwargs)):

        x, y, z, plot_kw = data
        ax.scatter3D(x, y, z, c=z, s=plot_params[('markersize', indx)], **plot_kw, **kwargs)

    plot_params.set_scale(ax)
    plot_params.set_limits(ax)
    plot_params.show_legend(ax)
    plot_params.show_colorbar(ax)
    plot_params.save_plot(saveas)

    return ax


@ensure_plotter_consistency(plot_params)
def surface_plot(xdata,
                 ydata,
                 zdata,
                 *,
                 xlabel='',
                 ylabel='',
                 zlabel='',
                 title='',
                 saveas='surface_plot',
                 axis=None,
                 **kwargs):
    """
    Create a standard surface plot

    :param xdata: arraylike, data for the x coordinate
    :param ydata: arraylike, data for the y coordinate
    :param zdata: arraylike, data for the z coordinate
    :param xlabel: str, label written on the x axis
    :param ylabel: str, label written on the y axis
    :param zlabel: str, label written on the z axis
    :param title: str, title of the figure
    :param axis: Axes object, if given the plot will be applied to this object
    :param saveas: str specifying the filename (without file format)

    Kwargs will be passed on to :py:class:`masci_tools.vis.matplotlib_plotter.MatplotlibPlotter`.
    If the arguments are not recognized they are passed on to the matplotlib function `plot_surface`
    """

    nplots = len(ydata)
    if nplots != len(xdata):  # todo check dimention not len, without moving to special datatype.
        print('ydata and xdata must have the same dimension')
        return
    if nplots != len(zdata):  # todo check dimention not len, without moving to special datatype.
        print('ydata and zdata must have the same dimension')
        return

    if isinstance(zdata, np.ndarray):
        zmin = zdata.min()
        zmax = zdata.max()
    else:
        zmin = min(zdata)
        zmax = max(zdata)

    clim = None
    if 'limits' in kwargs:
        clim = kwargs['limits'].get('color', None)
    else:
        kwargs['limits'] = {}
    if clim is None:
        clim = (kwargs.get('vmin', zmin), kwargs.get('vmax', zmax))
    kwargs['limits']['color'] = clim

    plot_params.set_defaults(default_type='function', linewidth=0, area_plot=False)
    kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)
    ax = plot_params.prepare_plot(title=title, xlabel=xlabel, ylabel=ylabel, zlabel=zlabel, axis=axis, projection='3d')

    plot_kwargs = plot_params.plot_kwargs(ignore=['markersize', 'marker'], extra_keys={'cmap'})
    ax.plot_surface(xdata, ydata, zdata, **plot_kwargs, **kwargs)

    plot_params.set_scale(ax)
    plot_params.set_limits(ax)
    plot_params.show_legend(ax)
    plot_params.show_colorbar(ax)
    plot_params.save_plot(saveas)

    return ax


@ensure_plotter_consistency(plot_params)
def multiplot_moved(xdata,
                    ydata,
                    *,
                    xlabel='',
                    ylabel='',
                    title='',
                    scale_move=1.0,
                    min_add=0,
                    saveas='mscatterplot',
                    **kwargs):
    """
    Plots all the scatter plots above each other. It adds an arbitrary offset to the ydata to do this and
    calls `multiple_scatterplots`. Therefore you might not want to show the yaxis ticks

    :param xdata: arraylike, data for the x coordinate
    :param ydata: arraylike, data for the y coordinate
    :param xlabel: str, label written on the x axis
    :param ylabel: str, label written on the y axis
    :param title: str, title of the figure
    :param scale_move: float, max*scale_move determines size of the shift
    :param min_add: float, minimum shift
    :param saveas: str specifying the filename (without file format)

    Kwargs are passed on to the :py:func:`multiple_scatterplots()` call
    """

    if 'yticks' not in kwargs:
        kwargs['yticks'] = []
    if 'yticklabels' not in kwargs:
        kwargs['yticklabels'] = []

    ydatanew = []
    shifts = []

    ymax = 0
    for data in ydata:
        ydatanew.append(np.array(data) + ymax)
        shifts.append(ymax)
        ymax = ymax + max(data) * scale_move + min_add

    ax = multiple_scatterplots(xdata,
                               ydatanew,
                               xlabel=xlabel,
                               ylabel=ylabel,
                               title=title,
                               saveas=saveas,
                               area_curve=shifts,
                               **kwargs)

    return ax


@ensure_plotter_consistency(plot_params)
def histogram(xdata,
              density=False,
              histtype='bar',
              align='mid',
              orientation='vertical',
              log=False,
              axis=None,
              title='hist',
              xlabel='bins',
              ylabel='counts',
              saveas='histogram',
              return_hist_output=False,
              **kwargs):
    """
    Create a standard looking histogram

    :param xdata: arraylike, Data for the histogram
    :param density: bool, if True the histogram is normed and a normal distribution is plotted with
                    the same mu and sigma as the data
    :param histtype: str, type of the histogram
    :param align: str, defines where the bars for the bins are aligned
    :param orientation: str, is the histogram vertical or horizontal
    :param log: bool, if True a logarithmic scale is used for the counts
    :param axis: Axes object where to add the plot
    :param title: str, Title of the plot
    :param xlabel: str, label for the x-axis
    :param ylabel: str, label for the y-axis
    :param saveas: str, filename for the saved plot
    :param return_hist_output: bool, if True the data output from hist will be returned

    Kwargs will be passed on to :py:class:`masci_tools.vis.matplotlib_plotter.MatplotlibPlotter`.
    If the arguments are not recognized they are passed on to the matplotlib function `hist`
    """

    if 'label' in kwargs:
        warnings.warn('Please use plot_label instead of label', DeprecationWarning)
        kwargs['plot_label'] = kwargs.pop('label')

    if 'legend_option' in kwargs:
        warnings.warn('Please use legend_options instead of legend_option', DeprecationWarning)
        kwargs['legend_options'] = kwargs.pop('legend_option')

    if 'limits' in kwargs:
        limits = kwargs.get('limits')
        if isinstance(limits, list):
            warnings.warn("Please provide limits as dict in the form {'x': value, 'y': value2}", DeprecationWarning)
            limits_new = {}
            if limits[0] is not None:
                limits_new['x'] = limits[0]
            if limits[1] is not None:
                limits_new['y'] = limits[1]
            kwargs['limits'] = limits_new

    kwargs = plot_params.set_parameters(continue_on_error=True, set_powerlimits=not log, area_plot=False, **kwargs)

    if orientation == 'horizontal':
        if xlabel == 'bins' and ylabel == 'counts':
            xlabel, ylabel = ylabel, xlabel

    ax = plot_params.prepare_plot(title=title, xlabel=xlabel, ylabel=ylabel, axis=axis, minor=True)

    plot_kwargs = plot_params.plot_kwargs(plot_type='histogram')
    n, bins, patches = ax.hist(xdata,
                               density=density,
                               histtype=histtype,
                               align=align,
                               orientation=orientation,
                               log=log,
                               **plot_kwargs,
                               **kwargs)

    if density:
        mu = np.mean(xdata)
        sigma = np.std(xdata)
        y = norm.pdf(bins, mu, sigma)
        if orientation == 'horizontal':
            ax.plot(y, bins, '--')
        else:
            ax.plot(bins, y, '--')

    plot_params.set_limits(ax)
    plot_params.draw_lines(ax)
    plot_params.show_legend(ax)
    plot_params.save_plot(saveas)

    if return_hist_output:
        return ax, n, bins, patches
    else:
        return ax


# todo remove default histogramm, replace it in all code by histogramm
def default_histogram(*args, **kwargs):
    """
    Create a standard looking histogram (DEPRECATED)
    """

    warnings.warn('Use histogram instead of default_histogram', DeprecationWarning)

    res = histogram(*args, **kwargs)

    return res


@ensure_plotter_consistency(plot_params)
def barchart(xdata,
             ydata,
             *,
             width=0.35,
             xlabel='x',
             ylabel='y',
             title='',
             bottom=None,
             saveas='barchart',
             axis=None,
             xerr=None,
             yerr=None,
             **kwargs):
    """
    Create a standard bar chart plot (this should be flexible enough) to do all the
    basic bar chart plots.

    :param xdata: arraylike data for the x coordinates of the bars
    :param ydata: arraylike data for the heights of the bars
    :param width: float determines the width of the bars
    :param axis: Axes object where to add the plot
    :param title: str, Title of the plot
    :param xlabel: str, label for the x-axis
    :param ylabel: str, label for the y-axis
    :param saveas: str, filename for the saved plot
    :param xerr: optional data for errorbar in x-direction
    :param yerr: optional data for errorbar in y-direction
    :param bottom: bottom values for the lowest end of the bars

    Kwargs will be passed on to :py:class:`masci_tools.vis.matplotlib_plotter.MatplotlibPlotter`.
    If the arguments are not recognized they are passed on to the matplotlib function `bar`

    TODO: grouped barchart (meaing not stacked)
    """

    nplots = len(ydata)
    if nplots != len(xdata):  # todo check dimention not len, without moving to special datatype.
        print('ydata and xdata must have the same dimension')
        return

    if not isinstance(ydata[0], (list, np.ndarray, pd.Series)):
        xdata, ydata = [xdata], [ydata]

    plot_params.single_plot = False
    plot_params.num_plots = len(ydata)

    #DEPRECATION WARNINGS
    if 'plot_labels' in kwargs:
        warnings.warn('Please use plot_label instead of plot_labels', DeprecationWarning)
        kwargs['plot_label'] = kwargs.pop('plot_labels')

    if 'colors' in kwargs:
        warnings.warn('Please use color instead of colors', DeprecationWarning)
        kwargs['color'] = kwargs.pop('colors')

    if 'legend_option' in kwargs:
        warnings.warn('Please use legend_options instead of legend_option', DeprecationWarning)
        kwargs['legend_options'] = kwargs.pop('legend_option')

    if 'scale' in kwargs:
        scale = kwargs.get('scale')
        if isinstance(scale, list):
            warnings.warn("Please provide scale as dict in the form {'x': value, 'y': value2}", DeprecationWarning)
            scale_new = {}
            if scale[0] is not None:
                scale_new['x'] = scale[0]
            if scale[1] is not None:
                scale_new['y'] = scale[1]
            kwargs['scale'] = scale_new

    if 'limits' in kwargs:
        limits = kwargs.get('limits')
        if isinstance(limits, list):
            warnings.warn("Please provide limits as dict in the form {'x': value, 'y': value2}", DeprecationWarning)
            limits_new = {}
            if limits[0] is not None:
                limits_new['x'] = limits[0]
            if limits[1] is not None:
                limits_new['y'] = limits[1]
            kwargs['limits'] = limits_new

    if 'xticks' in kwargs:
        xticks = kwargs.get('xticks')
        if isinstance(xticks[0], list):
            warnings.warn('Please provide xticks and xticklabels seperately as two lists', DeprecationWarning)
            kwargs['xticklabels'] = xticks[0]
            kwargs['xticks'] = xticks[1]

    plot_params.set_defaults(default_type='function', linewidth=None)
    kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)
    ax = plot_params.prepare_plot(title=title, xlabel=xlabel, ylabel=ylabel, axis=axis)

    # TODO good checks for input and setting of internals before plotting
    # allow all arguments as value then use for all or as lists with the righ length.
    if bottom:
        datab = bottom
    else:
        datab = np.zeros(len(ydata[0]))

    plot_kwargs = plot_params.plot_kwargs(plot_type='histogram')

    for indx, data in enumerate(zip(xdata, ydata, plot_kwargs)):

        x, y, plot_kw = data

        if isinstance(yerr, list):
            try:
                yerrt = yerr[indx]
            except KeyError:
                yerrt = yerr[0]
        else:
            yerrt = yerr

        if isinstance(xerr, list):
            try:
                xerrt = xerr[indx]
            except KeyError:
                xerrt = xerr[0]
        else:
            xerrt = xerr

        ax.bar(x, y, width, bottom=datab, **plot_kw, **kwargs)

        datab = datab + np.array(y)

    plot_params.set_scale(ax)
    plot_params.set_limits(ax)
    plot_params.draw_lines(ax)
    plot_params.show_legend(ax)
    plot_params.save_plot(saveas)

    return ax


@ensure_plotter_consistency(plot_params)
def multiaxis_scatterplot(xdata,
                          ydata,
                          *,
                          axes_loc,
                          xlabel,
                          ylabel,
                          title,
                          num_cols=1,
                          num_rows=1,
                          saveas='mscatterplot',
                          **kwargs):
    """
    Create a scatter plot with multiple axes.

    :param xdata: list of arraylikes, passed on to the plotting functions for each axis (x-axis)
    :param ydata: list of arraylikes, passed on to the plotting functions for each axis (y-axis)
    :param axes_loc: list of tuples of two integers, location of each axis
    :param xlabel: str or list of str, labels for the x axis
    :param ylabel: str or list of str, labels for the y-axis
    :param title: str or list of str, titles for the subplots
    :param num_rows: int, how many rows of axis are created
    :param num_cols: int, how many columns of axis are created
    :param saveas: str filename of the saved file

    Special Kwargs:
        :param subplot_params: dict with integer keys, can contain all valid kwargs for :py:func:`multiple_scatterplots()`
                               with the integer key denoting to which subplot the changes are applied
        :param axes_kwargs: dict with integer keys, additional arguments to pass on to `subplot2grid` for the creation
                            of each axis (e.g colspan, rowspan)

    Other Kwargs will be passed on to all :py:func:`multiple_scatterplots()` calls
    (If they are not overwritten by parameters in `subplot_params`).
    """

    #convert parameters to list of parameters for subplots
    subplot_params = kwargs.pop('subplot_params', {})
    axes_kwargs = kwargs.pop('axes_kwargs', {})

    param_list = [None] * len(axes_loc)
    for indx, val in enumerate(param_list):
        if indx in subplot_params:
            param_list[indx] = subplot_params[indx]
        else:
            param_list[indx] = {}

        if indx in axes_kwargs:
            param_list[indx]['axes_kwargs'] = axes_kwargs[indx]

        if not isinstance(xlabel, list):
            param_list[indx]['xlabel'] = xlabel
        else:
            param_list[indx]['xlabel'] = xlabel[indx]

        if not isinstance(ylabel, list):
            param_list[indx]['ylabel'] = ylabel
        else:
            param_list[indx]['ylabel'] = ylabel[indx]

        if not isinstance(title, list):
            param_list[indx]['title'] = title
        else:
            param_list[indx]['title'] = title[indx]

    general_keys = set(plot_params['figure_kwargs']) | {'show', 'save_plots'}
    general_info = {key: val for key, val in kwargs.items() if key in general_keys}
    kwargs = {key: val for key, val in kwargs.items() if key not in general_keys}

    plot_params.set_parameters(**general_info)

    #figsize is automatically scaled with the shape of the plot
    plot_shape = (num_rows, num_cols)
    plot_params['figure_kwargs'] = {
        'figsize': ([plot_shape[indx] * size for indx, size in enumerate(plot_params['figure_kwargs']['figsize'])])
    }

    plt.figure(**plot_params['figure_kwargs'])

    axis = []
    for indx, subplot_data in enumerate(zip(axes_loc, xdata, ydata, param_list)):

        location, x, y, params = subplot_data

        subplot_kwargs = copy.deepcopy(kwargs)
        subplot_kwargs.update(params)

        ax = plt.subplot2grid(plot_shape, location, **subplot_kwargs.pop('axes_kwargs', {}))
        with NestedPlotParameters(plot_params):
            ax = multiple_scatterplots(x, y, axis=ax, **subplot_kwargs, save_plots=False, show=False)

        axis.append(ax)

    plot_params.save_plot(saveas)

    return axis


###############################################################################
########################## special plot routines ##############################
###############################################################################


@ensure_plotter_consistency(plot_params)
def plot_convex_hull2d(hull,
                       *,
                       title='Convex Hull',
                       xlabel='Atomic Procentage',
                       ylabel='Formation energy / atom [eV]',
                       saveas='convex_hull',
                       axis=None,
                       **kwargs):
    """
    Plot method for a 2d convex hull diagramm

    :param hull: pyhull.Convexhull #scipy.spatial.ConvexHull
    :param axis: Axes object where to add the plot
    :param title: str, Title of the plot
    :param xlabel: str, label for the x-axis
    :param ylabel: str, label for the y-axis
    :param saveas: str, filename for the saved plot

    Function specific parameters:
        :param marker_hull: defaults to `marker`, marker type for the hull plot
        :param markersize_hull: defaults to `markersize`, markersize for the hull plot
        :param color_hull: defaults to `color`, color for the hull plot

    Kwargs will be passed on to :py:class:`masci_tools.vis.matplotlib_plotter.MatplotlibPlotter`.
    If the arguments are not recognized they are passed on to the matplotlib functions `plot`
    """

    #DEPRECATE: color_line
    if 'color_line' in kwargs:
        warnings.warn('Please use color instead of color_line', DeprecationWarning)
        kwargs['color'] = kwargs.pop('colors')

    #Define function wide custom parameters
    plot_params.add_parameter('marker_hull', default_from='marker')
    plot_params.add_parameter('markersize_hull', default_from='markersize')
    plot_params.add_parameter('color_hull', default_from='color')

    kwargs = plot_params.set_parameters(continue_on_error=True, set_powerlimits=False, **kwargs)
    ax = plot_params.prepare_plot(title=title, xlabel=xlabel, ylabel=ylabel, axis=axis)

    points = hull.points

    plot_kw = plot_params.plot_kwargs()
    plot_hull_kw = plot_params.plot_kwargs(marker='marker_hull', markersize='markersize_hull', color='color_hull')
    plot_hull_kw['linestyle'] = ''
    linestyle = plot_kw['linestyle']
    plot_kw['linestyle'] = ''

    ax.plot(points[:, 0], points[:, 1], **plot_kw, **kwargs)
    for simplex in hull.simplices:
        # TODO leave out some lines, the ones about [0,0 -1,0]
        data = simplex.coords
        ax.plot(data[:, 0], data[:, 1], linestyle=linestyle, **plot_kw, **kwargs)
        ax.plot(data[:, 0], data[:, 1], **plot_hull_kw, **kwargs)
        # this section is from scipy.spatial.Convexhull interface
        #ax.plot(points[simplex, 0], points[simplex, 1], linestyle=linestyle,
        #        color=color_line, linewidth=linewidth, markersize=markersize, **kwargs)
        #ax.plot(points[simplex, 0], points[simplex, 1], linestyle='',
        #        color=color, markersize=markersize_hull, marker=marker_hull, **kwargs)

    plot_params.set_scale(ax)
    plot_params.set_limits(ax)
    plot_params.draw_lines(ax)
    plot_params.show_legend(ax)
    plot_params.save_plot(saveas)

    return ax


@ensure_plotter_consistency(plot_params)
def plot_residuen(xdata,
                  fitdata,
                  realdata,
                  *,
                  errors=None,
                  xlabel=r'Energy [eV]',
                  ylabel=r'cts/s [arb]',
                  title=r'Residuen',
                  saveas='residuen',
                  hist=True,
                  return_residuen_data=True,
                  **kwargs):
    """
    Calculates and plots the residuen for given xdata fit results and the real data.

    If hist=True also the normed residual distribution is ploted with a normal distribution.

    :param xdata: arraylike data for the x-coordinate
    :param fitdata: arraylike fitted data for the y-coordinate
    :param realdata: arraylike data to plot residuen against the fit
    :param errors: dict, can be used to provide errordata for the x and y direction
    :param xlabel: str, label for the x-axis
    :param ylabel: str, label for the y-axis
    :param title: str, title for the plot
    :param saveas: str, filename for the saved plot
    :param hist: bool, if True a normed residual distribution is ploted with a normal distribution.
    :param return_residuen_data: bool, if True in addition to the produced axis object also
                                 the residuen data is returned

    Special Kwargs:
        :param hist_kwargs: dict, these arguments will be passed on to the
                            :py:func:`histogram()` call (if hist=True)

    Other Kwargs will be passed on to all :py:func:`single_scatterplot()` call
    """

    if errors is None:
        errors = {}

    ydata = realdata - fitdata
    hist_kwargs = kwargs.pop('hist_kwargs', {})

    general_keys = set(plot_params['figure_kwargs']) | {'show', 'save_plots'}
    general_info = {key: val for key, val in kwargs.items() if key in general_keys}
    kwargs = {key: val for key, val in kwargs.items() if key not in general_keys}
    plot_params.set_parameters(**general_info)

    if hist:
        figsize = plot_params['figure_kwargs']['figsize']
        #figsize is automatically scaled with the shape of the plot
        plot_params['figure_kwargs'] = {'figsize': (figsize[0] * 2, figsize[1])}

    plt.figure(**plot_params['figure_kwargs'])

    if hist:
        ax1 = plt.subplot2grid((1, 2), (0, 0))
        ax2 = plt.subplot2grid((1, 2), (0, 1), sharey=ax1)
        axes = [ax1, ax2]
    else:
        ax1 = plt.subplot2grid((1, 1), (0, 0))
        axes = ax1

    with NestedPlotParameters(plot_params):
        ax1 = single_scatterplot(xdata,
                                 ydata,
                                 xlabel=xlabel,
                                 ylabel=ylabel,
                                 title=title,
                                 axis=ax1,
                                 show=False,
                                 save_plots=False,
                                 xerr=errors.get('x', None),
                                 yerr=errors.get('y', None),
                                 **kwargs)

    if hist:
        with NestedPlotParameters(plot_params):
            ax2 = histogram(ydata,
                            bins=20,
                            axis=ax2,
                            orientation='horizontal',
                            title='Residuen distribution',
                            density=True,
                            show=False,
                            save_plots=False,
                            **hist_kwargs)

    plot_params.save_plot(saveas)

    if return_residuen_data:
        return axes, ydata
    else:
        return axes


@ensure_plotter_consistency(plot_params)
def plot_convergence_results(iteration,
                             distance,
                             total_energy,
                             *,
                             saveas1='t_energy_convergence',
                             axis1=None,
                             saveas2='distance_convergence',
                             axis2=None,
                             **kwargs):
    """
    Plot the total energy versus the scf iteration
    and plot the distance of the density versus iterations.

    :param iteration: array for the number of iterations
    :param distance: array of distances
    :param total_energy: array of total energies
    :param saveas1: str, filename for the energy convergence plot
    :param axis1: Axes object for the energy convergence plot
    :param saveas2: str, filename for the distance plot
    :param axis2: Axes object for the distance plot

    Other Kwargs will be passed on to all :py:func:`single_scatterplot()` calls
    """
    xlabel = r'Iteration'
    ylabel1 = r'Total energy difference [Htr]'
    ylabel2 = r'Distance [me/bohr^3]'
    title1 = r'Total energy difference over scf-Iterations'
    #title2 = r'Distance over scf-Iterations'
    title2 = r'Convergence (log)'
    # since we make a log plot of the total_energy make sure to plot the absolute total energy
    total_energy_abs_diff = []
    for en0, en1 in zip(total_energy[:-1], total_energy[1:]):
        total_energy_abs_diff.append(abs(en1 - en0))
    #saveas3 ='t_energy_convergence2'

    p1 = single_scatterplot(iteration[1:],
                            total_energy_abs_diff,
                            xlabel=xlabel,
                            ylabel=ylabel1,
                            title=title1,
                            plot_label='delta total energy',
                            saveas=saveas1,
                            scale={'y': 'log'},
                            axis=axis1,
                            **kwargs)
    #single_scatterplot(total_energy, iteration, xlabel, ylabel1, title1, plotlabel='total energy', saveas=saveas3)
    p2 = single_scatterplot(iteration,
                            distance,
                            xlabel=xlabel,
                            ylabel=ylabel2,
                            title=title2,
                            plot_label='distance',
                            saveas=saveas2,
                            scale={'y': 'log'},
                            axis=axis2,
                            **kwargs)

    return p1, p2


@ensure_plotter_consistency(plot_params)
def plot_convergence_results_m(iterations,
                               distances,
                               total_energies,
                               *,
                               modes,
                               nodes=None,
                               saveas1='t_energy_convergence',
                               saveas2='distance_convergence',
                               axis1=None,
                               axis2=None,
                               **kwargs):
    """
    Plot the total energy versus the scf iteration
    and plot the distance of the density versus iterations.

    :param iterations: array for the number of iterations
    :param distances: array of distances
    :param total_energies: array of total energies
    :param modes: list of convergence modes (if 'force' is in the list the last distance is removed)
    :param saveas1: str, filename for the energy convergence plot
    :param axis1: Axes object for the energy convergence plot
    :param saveas2: str, filename for the distance plot
    :param axis2: Axes object for the distance plot

    Other Kwargs will be passed on to all :py:func:`multiple_scatterplots()` calls
    """
    xlabel = r'Iteration'
    ylabel1 = r'Total energy difference [Htr]'
    ylabel2 = r'Distance [me/bohr^3]'
    title1 = r'Total energy difference over scf-Iterations'
    #title2 = r'Distance over scf-Iterations'
    title2 = r'Convergence (log)'

    if 'plot_labels' in kwargs:
        warnings.warn('Please use plot_label instead of plot_labels', DeprecationWarning)
        kwargs['plot_label'] = kwargs.pop('plot_labels')

    iterations1 = []
    plot_labels1 = []
    plot_labels2 = []

    # since we make a log plot of the total_energy make sure to plot the absolute total energy
    total_energy_abs_diffs = []
    for i, total_energy in enumerate(total_energies):
        iterations1.append(iterations[i][1:])
        total_energy_abs_diff = []
        for en0, en1 in zip(total_energy[:-1], total_energy[1:]):
            total_energy_abs_diff.append(abs(en1 - en0))
        total_energy_abs_diffs.append(total_energy_abs_diff)
        plot_labels1.append('delta total energy {}'.format(i))
        plot_labels2.append('distance {}'.format(i))
    #saveas3 ='t_energy_convergence2'
    if 'plot_label' in kwargs:
        plot_label = plot_params.convert_to_complete_list(kwargs.pop('plot_label'),
                                                          single_plot=False,
                                                          num_plots=len(plot_labels1),
                                                          key='plot_label')
        plot_labels1 = [label if label is not None else plot_labels1[indx] for indx, label in enumerate(plot_label)]
        plot_labels2 = [label if label is not None else plot_labels2[indx] for indx, label in enumerate(plot_label)]

    p1 = multiple_scatterplots(iterations1,
                               total_energy_abs_diffs,
                               xlabel=xlabel,
                               ylabel=ylabel1,
                               title=title1,
                               plot_label=plot_labels1,
                               saveas=saveas1,
                               scale={'y': 'log'},
                               axis=axis1,
                               **kwargs)
    for i, mode in enumerate(modes):
        if mode == 'force':
            iterations[i].pop()
            print('Drop the last iteration because there was no charge distance, mode=force')

    p2 = multiple_scatterplots(iterations,
                               distances,
                               xlabel=xlabel,
                               ylabel=ylabel2,
                               title=title2,
                               plot_label=plot_labels2,
                               saveas=saveas2,
                               scale={'y': 'log'},
                               axis=axis2,
                               **kwargs)

    return p1, p2


@ensure_plotter_consistency(plot_params)
def plot_lattice_constant(scaling,
                          total_energy,
                          *,
                          fit_y=None,
                          relative=True,
                          ref_const=None,
                          multi=False,
                          title=r'Equation of states',
                          saveas='lattice_constant',
                          axis=None,
                          **kwargs):
    """
    Plot a lattice constant versus Total energy
    Plot also the fit.
    On the x axis is the scaling, it

    :param scaling: arraylike, data for the scaling factor
    :param total_energy: arraylike, data for the total energy
    :param fit_y: arraylike, optional data of fitted data
    :param relative: bool, scaling factor given (True), or lattice constants given?
    :param ref_const: float (optional), or list of floats, lattice constant for scaling 1.0
    :param multi: bool default False are they multiple plots?

    Function specific parameters:
        :param marker_fit: defaults to `marker`, marker type for the fit data
        :param markersize_fit: defaults to `markersize`, markersize for the fit data
        :param linewidth_fit: defaults to `linewidth`, linewidth for the fit data
        :param plotlabel_fit: str label for the fit data

    Other Kwargs will be passed on to all :py:func:`single_scatterplot()` or :py:func:`multiple_scatterplots()` calls
    """
    # TODO: make box which shows fit results. (fit resuls have to be past)
    # TODO: multiple plots in one use multi_scatter_plot for this...

    if 'plotlables' in kwargs:
        warnings.warn('plotlables is deprecated. Use plot_label and plot_label_fit instead', DeprecationWarning)
        if multi:
            plot_label = []
            plot_label_fit = []
            for indx in range(len(scaling)):
                plot_label.append(kwargs['plotlables'][2 * indx])
                plot_label_fit.append(kwargs['plotlables'][2 * indx + 1])
            kwargs['plot_label'] = plot_label
            kwargs['plot_label_fit'] = plot_label_fit
        else:
            kwargs['plot_label'] = kwargs['plotlables'][0]
            kwargs['plot_label_fit'] = kwargs['plotlables'][1]

    #print markersize_g
    if relative:
        if ref_const:
            xlabel = rf'Relative Volume [a/{ref_const}$\AA$]'
        else:
            xlabel = r'Relative Volume'
    else:
        xlabel = r'Volume [$\AA$]'

    if multi:
        ylabel = r'Total energy norm[0] [eV]'
    else:
        ylabel = r'Total energy [eV]'

    #Add custom parameters for fit
    plot_params.add_parameter('marker_fit', default_from='marker')
    plot_params.add_parameter('markersize_fit', default_from='markersize')
    plot_params.add_parameter('linewidth_fit', default_from='linewidth')
    plot_params.add_parameter('plot_label_fit')

    plot_params.set_defaults(default_type='function',
                             marker_fit='s',
                             plot_label='simulation data',
                             plot_label_fit='fit results')

    general_keys = set(plot_params['figure_kwargs']) | {'show', 'save_plots'}
    general_info = {key: val for key, val in kwargs.items() if key in general_keys}
    kwargs = {key: val for key, val in kwargs.items() if key not in general_keys}

    plot_params.set_parameters(**general_info)
    kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)
    ax = plot_params.prepare_plot(title=title, xlabel=xlabel, ylabel=ylabel, axis=axis)

    if multi:
        plot_params.single_plot = False
        plot_params.num_plots = len(scaling)

    plot_kw = plot_params.plot_kwargs(post_process=False)
    plot_fit_kw = plot_params.plot_kwargs(post_process=False,
                                          marker='marker_fit',
                                          markersize='markersize_fit',
                                          linewidth='linewidth_fit',
                                          plot_label='plot_label_fit')

    if multi:
        # TODO test if dim of total_e = dim of scaling, dim plot lables...
        # or parse on scaling?

        with NestedPlotParameters(plot_params):
            ax = multiple_scatterplots(scaling,
                                       total_energy,
                                       xlabel=xlabel,
                                       ylabel=ylabel,
                                       title=title,
                                       axis=ax,
                                       show=False,
                                       save_plots=False,
                                       **plot_kw,
                                       **kwargs)
        if fit_y:
            with NestedPlotParameters(plot_params):
                ax = multiple_scatterplots(scaling,
                                           fit_y,
                                           xlabel=xlabel,
                                           ylabel=ylabel,
                                           title=title,
                                           axis=ax,
                                           show=False,
                                           save_plots=False,
                                           **plot_fit_kw,
                                           **kwargs)

    else:
        with NestedPlotParameters(plot_params):
            ax = single_scatterplot(scaling,
                                    total_energy,
                                    xlabel=xlabel,
                                    ylabel=ylabel,
                                    title=title,
                                    axis=ax,
                                    show=False,
                                    save_plots=False,
                                    **plot_kw,
                                    **kwargs)
        if fit_y:
            with NestedPlotParameters(plot_params):
                ax = single_scatterplot(scaling,
                                        fit_y,
                                        xlabel,
                                        ylabel,
                                        title,
                                        axis=ax,
                                        show=False,
                                        save_plots=False,
                                        **plot_fit_kw,
                                        **kwargs)

    plot_params.draw_lines(ax)
    plot_params.save_plot(saveas)

    return ax


def plot_relaxation_results():
    """
    Plot from the result node of a relaxation workflow,
    All forces of every atom type versus relaxation cycle.
    Average force of all atom types versus relaxation cycle.
    Absolut relaxation in Angstroem of every atom type.
    Relative realxation of every atom type to a reference structure.
    (if none given use the structure from first relaxation cycle as reference)
    """
    pass


@ensure_plotter_consistency(plot_params)
def plot_dos(energy_grid,
             dos_data,
             *,
             saveas='dos_plot',
             energy_label=r'$E-E_F$ [eV]',
             dos_label=r'DOS [1/eV]',
             title=r'Density of states',
             xyswitch=False,
             e_fermi=0,
             **kwargs):
    """
    Plot the provided data for a density of states (not spin-polarized). Can be done
    horizontally or vertical via the switch `xyswitch`

    :param energy_grid: arraylike data for the energy grid of the DOS
    :param dos_data: arraylike data for all the DOS components to plot
    :param title: str, Title of the plot
    :param energy_label: str, label for the energy-axis
    :param dos_label: str, label for the DOS-axis
    :param saveas: str, filename for the saved plot
    :param e_fermi: float (default 0), place the line for the fermi energy at this value
    :param xyswitch: bool if True, the enrgy axis will be plotted vertically

    All other Kwargs are passed on to the :py:func:`multiple_scatterplots()` call
    """
    import seaborn as sns

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

    color_cycle = ('black',) + tuple(sns.color_palette('muted'))
    plot_params.set_defaults(default_type='function', marker=None, legend=True, lines=lines, color_cycle=color_cycle)

    if xyswitch:
        figsize = plot_params['figure_kwargs']['figsize']
        plot_params.set_defaults(default_type='function', figure_kwargs={'figsize': figsize[::-1]})

    if isinstance(dos_data[0], (list, np.ndarray)) and \
       not isinstance(energy_grid[0], (list, np.ndarray)):
        energy_grid = [energy_grid] * len(dos_data)

    if xyswitch:
        x, y = dos_data, energy_grid
        xlabel, ylabel = dos_label, energy_label
        plot_params.set_defaults(default_type='function', area_vertical=True)
    else:
        xlabel, ylabel = energy_label, dos_label
        x, y = energy_grid, dos_data

    ax = multiple_scatterplots(x, y, xlabel=xlabel, ylabel=ylabel, title=title, saveas=saveas, **kwargs)

    return ax


@ensure_plotter_consistency(plot_params)
def plot_spinpol_dos(energy_grid,
                     spin_up_data,
                     spin_dn_data,
                     *,
                     saveas='spinpol_dos_plot',
                     energy_label=r'$E-E_F$ [eV]',
                     dos_label=r'DOS [1/eV]',
                     title=r'Density of states',
                     xyswitch=False,
                     energy_grid_dn=None,
                     e_fermi=0,
                     spin_dn_negative=True,
                     **kwargs):
    """
    Plot the provided data for a density of states (spin-polarized). Can be done
    horizontally or vertical via the switch `xyswitch`

    :param energy_grid: arraylike data for the energy grid of the DOS
    :param spin_up_data: arraylike data for all the DOS spin-up components to plot
    :param spin_dn_data: arraylike data for all the DOS spin-down components to plot
    :param title: str, Title of the plot
    :param energy_label: str, label for the energy-axis
    :param dos_label: str, label for the DOS-axis
    :param saveas: str, filename for the saved plot
    :param e_fermi: float (default 0), place the line for the fermi energy at this value
    :param xyswitch: bool if True, the enrgy axis will be plotted vertically
    :param energy_grid_dn: arraylike data for the energy grid of the DOS of the spin-down component
                           (optional)
    :param spin_dn_negative: bool, if True (default) the spin-down components are plotted downwards

    All other Kwargs are passed on to the :py:func:`multiple_scatterplots()` call
    """
    import seaborn as sns

    if 'limits' in kwargs:
        limits = kwargs.pop('limits')
        if xyswitch:
            limits['x'], limits['y'] = limits.pop('dos', None), limits.pop('energy', None)
        else:
            limits['x'], limits['y'] = limits.pop('energy', None), limits.pop('dos', None)
        kwargs['limits'] = {k: v for k, v in limits.items() if v is not None}

    if isinstance(spin_up_data[0], (list, np.ndarray)):
        if len(spin_up_data) != len(spin_dn_data):
            raise ValueError(f'Dimensions do not match: Spin-up: {len(spin_up_data)} Spin-dn: {len(spin_dn_data)}')

    max_dos = max(data.max() for data in spin_up_data)
    max_dos = max(max_dos, max(data.max() for data in spin_dn_data))
    max_dos *= 1.1

    if spin_dn_negative:
        if isinstance(spin_dn_data, np.ndarray):
            spin_dn_data *= -1
        elif isinstance(spin_up_data[0], list):
            spin_dn_data = [-value for data in spin_dn_data for value in data]
        else:
            spin_dn_data = [-value for value in spin_dn_data]
    lines = {'horizontal': 0}
    lines['vertical'] = e_fermi

    if xyswitch:
        lines['vertical'], lines['horizontal'] = lines['horizontal'], lines['vertical']

    if xyswitch:
        limits = {'x': (-max_dos, max_dos)}
    else:
        limits = {'y': (-max_dos, max_dos)}

    if isinstance(spin_up_data[0], (list, np.ndarray)):
        num_plots = len(spin_up_data)
    else:
        num_plots = 1

    color_cycle = ('black',) + tuple(sns.color_palette('muted'))
    plot_params.set_defaults(default_type='function',
                             marker=None,
                             legend=True,
                             lines=lines,
                             limits=limits,
                             repeat_colors_after=num_plots,
                             color_cycle=color_cycle)

    if xyswitch:
        figsize = plot_params['figure_kwargs']['figsize']
        plot_params.set_defaults(default_type='function', figure_kwargs={'figsize': figsize[::-1]})

    save_keys = {'show', 'save_plots', 'save_format', 'save_options'}
    save_options = {key: val for key, val in kwargs.items() if key in save_keys}
    kwargs = {key: val for key, val in kwargs.items() if key not in save_keys}

    plot_params.set_parameters(**save_options)

    if xyswitch:
        plot_params.set_defaults(default_type='function', invert_xaxis=True)

    dos_data = spin_up_data
    if not isinstance(spin_up_data[0], (list, np.ndarray)):
        dos_data = [dos_data, spin_dn_data]
    else:
        dos_data = np.concatenate((dos_data, spin_dn_data), axis=0)

    if isinstance(dos_data[0], (list, np.ndarray)) and \
       not isinstance(energy_grid[0], (list, np.ndarray)):
        energy_grid = [energy_grid] * len(dos_data)

    if xyswitch:
        x, y = dos_data, energy_grid
        xlabel, ylabel = dos_label, energy_label
        plot_params.set_defaults(default_type='function', area_vertical=True)
    else:
        xlabel, ylabel = energy_label, dos_label
        x, y = energy_grid, dos_data

    with NestedPlotParameters(plot_params):
        ax = multiple_scatterplots(x,
                                   y,
                                   xlabel=xlabel,
                                   ylabel=ylabel,
                                   title=title,
                                   save_plots=False,
                                   show=False,
                                   **kwargs)

    if xyswitch:
        ax.annotate(r'$\uparrow$', xy=(0.125, 0.9), xycoords='axes fraction', ha='center', va='center', size=40)
        ax.annotate(r'$\downarrow$', xy=(0.875, 0.9), xycoords='axes fraction', ha='center', va='center', size=40)
    else:
        ax.annotate(r'$\uparrow$', xy=(0.05, 0.875), xycoords='axes fraction', ha='center', va='center', size=40)
        ax.annotate(r'$\downarrow$', xy=(0.05, 0.125), xycoords='axes fraction', ha='center', va='center', size=40)

    plot_params.save_plot(saveas)

    return ax


@ensure_plotter_consistency(plot_params)
def plot_bands(kpath,
               bands,
               *,
               size_data=None,
               special_kpoints=None,
               e_fermi=0,
               xlabel='',
               ylabel=r'$E-E_F$ [eV]',
               title='',
               saveas='bandstructure',
               markersize_min=0.5,
               markersize_scaling=5.0,
               **kwargs):
    """
    Plot the provided data for a bandstrucuture (non spin-polarized). Can be used
    to illustrate weights on bands via `size_data`

    :param kpath: arraylike data for the kpoint data
    :param bands: arraylike data for the eigenvalues
    :param size_data: arraylike data the weights to emphasize (optional)
    :param title: str, Title of the plot
    :param xlabel: str, label for the x-axis
    :param ylabel: str, label for the y-axis
    :param saveas: str, filename for the saved plot
    :param e_fermi: float (default 0), place the line for the fermi energy at this value
    :param special_kpoints: list of tuples (str, float), place vertical lines at the given values
                            and mark them on the x-axis with the given label
    :param markersize_min: minimum value used in scaling points for weight
    :param markersize_scaling: factor used in scaling points for weight

    All other Kwargs are passed on to the :py:func:`multi_scatter_plot()` call
    """

    if special_kpoints is None:
        special_kpoints = []

    xticks = []
    xticklabels = []
    for label, pos in special_kpoints:
        if label in ('Gamma', 'g'):
            label = r'$\Gamma$'
        xticklabels.append(label)
        xticks.append(pos)

    color_data = None
    if size_data is not None:
        ylimits = (-15, 15)
        if 'limits' in kwargs:
            if 'y' in kwargs['limits']:
                ylimits = kwargs['limits']['y']

        weight_max = max(size_data[np.logical_and(bands > ylimits[0], bands < ylimits[1])])
        if 'vmax' not in kwargs:
            kwargs['vmax'] = weight_max

        color_data = copy.copy(size_data)
        size_data = (markersize_min + markersize_scaling * size_data / weight_max)**2
        plot_params.set_defaults(default_type='function', cmap='Blues')
        if 'cmap' not in kwargs:
            #Cut off the white end of the Blues/Reds colormap
            plot_params.set_defaults(default_type='function', sub_colormap=(0.15, 1.0))

    lines = {'vertical': xticks, 'horizontal': e_fermi}

    limits = {'x': (min(kpath), max(kpath)), 'y': (-15, 15)}
    plot_params.set_defaults(default_type='function',
                             lines=lines,
                             limits=limits,
                             xticks=xticks,
                             xticklabels=xticklabels,
                             color='k',
                             line_options={'zorder': -1},
                             colorbar=False)

    ax = multi_scatter_plot(kpath,
                            bands,
                            size_data=size_data,
                            color_data=color_data,
                            xlabel=xlabel,
                            ylabel=ylabel,
                            title=title,
                            saveas=saveas,
                            **kwargs)

    return ax


@ensure_plotter_consistency(plot_params)
def plot_spinpol_bands(kpath,
                       bands_up,
                       bands_dn,
                       *,
                       size_data=None,
                       show_spin_pol=True,
                       special_kpoints=None,
                       e_fermi=0,
                       xlabel='',
                       ylabel=r'$E-E_F$ [eV]',
                       title='',
                       saveas='bandstructure',
                       markersize_min=0.5,
                       markersize_scaling=5.0,
                       **kwargs):
    """
    Plot the provided data for a bandstrucuture (spin-polarized). Can be used
    to illustrate weights on bands via `size_data`

    :param kpath: arraylike data for the kpoint data
    :param bands_up: arraylike data for the eigenvalues (spin-up)
    :param bands_dn: arraylike data for the eigenvalues (spin-dn)
    :param size_data: arraylike data the weights to emphasize BOTH SPINS (optional)
    :param title: str, Title of the plot
    :param xlabel: str, label for the x-axis
    :param ylabel: str, label for the y-axis
    :param saveas: str, filename for the saved plot
    :param e_fermi: float (default 0), place the line for the fermi energy at this value
    :param special_kpoints: list of tuples (str, float), place vertical lines at the given values
                            and mark them on the x-axis with the given label
    :param markersize_min: minimum value used in scaling points for weight
    :param markersize_scaling: factor used in scaling points for weight
    :param show_spin_pol: bool, if True (default) the two different spin channles will be shown in blue
                          and red by default

    All other Kwargs are passed on to the :py:func:`multi_scatter_plot()` call
    """

    if special_kpoints is None:
        special_kpoints = {}

    if size_data is None:
        size_data = [None, None]
        color_data = [None, None]
    else:
        ylimits = (-15, 15)
        if 'limits' in kwargs:
            if 'y' in kwargs['limits']:
                ylimits = kwargs['limits']['y']

        weight_max = max(size_data[0][np.logical_and(bands_up > ylimits[0], bands_up < ylimits[1])])
        weight_max = max(weight_max, max(size_data[1][np.logical_and(bands_dn > ylimits[0], bands_dn < ylimits[1])]))

        if 'vmax' not in kwargs:
            kwargs['vmax'] = weight_max

        color_data = []
        for indx, data in enumerate(size_data):
            color_data.append(copy.copy(data))
            size_data[indx] = (markersize_min + markersize_scaling * data / weight_max)**2

    xticks = []
    xticklabels = []
    for label, pos in special_kpoints:
        if label in ('Gamma', 'g'):
            label = r'$\Gamma$'
        xticklabels.append(label)
        xticks.append(pos)

    lines = {'vertical': xticks, 'horizontal': e_fermi}

    if show_spin_pol:
        color = ['blue', 'red']
        cmaps = ['Blues', 'Reds']
    else:
        color = 'k'
        cmaps = 'Blues'

    limits = {'x': (min(kpath), max(kpath)), 'y': (-15, 15)}
    plot_params.set_defaults(default_type='function',
                             lines=lines,
                             limits=limits,
                             xticks=xticks,
                             xticklabels=xticklabels,
                             color=color,
                             cmap=cmaps,
                             legend=True,
                             line_options={'zorder': -1},
                             colorbar=False)

    if 'cmap' not in kwargs:
        #Cut off the white end of the Blues/Reds colormap
        plot_params.set_defaults(default_type='function', sub_colormap=(0.15, 1.0))

    ax = multi_scatter_plot([kpath, kpath], [bands_dn, bands_up],
                            size_data=size_data,
                            color_data=color_data,
                            xlabel=xlabel,
                            ylabel=ylabel,
                            title=title,
                            saveas=saveas,
                            **kwargs)

    return ax


def plot_certain_bands():
    """
    Plot only certain bands from a bands.1 file from FLEUR
    """
    pass


def plot_bands_and_dos():
    """
    PLot a Bandstructure with a density of states on the right side.
    """
    pass


def plot_corelevels(coreleveldict, compound='', axis=None, saveas='scatterplot', **kwargs):
    """
    Ploting function to visualize corelevels and corelevel shifts
    """

    for elem, corelevel_dict in coreleveldict.items():
        # one plot for each element
        axis = plot_one_element_corelv(corelevel_dict, elem, compound=compound, axis=axis, saveas=saveas, **kwargs)

    return axis


@ensure_plotter_consistency(plot_params)
def plot_one_element_corelv(corelevel_dict, element, compound='', axis=None, saveas='scatterplot', **kwargs):
    """
    This routine creates a plot which visualizes all the binding energies of one
    element (and currenlty one corelevel) for different atomtypes.

    example:
        corelevels = {'W' : {'4f7/2' : [123, 123.3, 123.4 ,123.1], '4f5/2' : [103, 103.3, 103.4, 103.1]}, 'Be' : {'1s': [118, 118.2, 118.4, 118.1, 118.3]}}

    """
    corelevels_names = []
    xdata_all = []
    ydata_all = []

    for corelevel, corelevel_list in corelevel_dict.items():
        #print corelevel
        n_atom = len(corelevel_list)
        x_axis = list(range(0, n_atom, 1))
        y_axis = corelevel_list
        xdata_all.append(x_axis)
        ydata_all.append(y_axis)
        corelevels_names.append(corelevel)

    elem = element
    xdata = xdata_all[0]
    ydata = ydata_all[0]
    xlabel = '{} atomtype'.format(elem)
    ylabel = 'energy in eV'
    title = 'Element: {} from {} cl {}'.format(elem, compound, corelevels_names)
    #plotlabel ='corelevel shifts'
    #linetyp='o-'
    xmin = xdata[0] - 0.5
    xmax = xdata[-1] + 0.5
    ymin = min(ydata) - 1
    ymax = max(ydata) + 1

    plot_params.set_defaults(default_type='function',
                             font_options={'color': 'darkred'},
                             color='k',
                             linewidth=2,
                             limits={
                                 'x': (xmin, xmax),
                                 'y': (ymin, ymax)
                             })

    kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)
    ax = plot_params.prepare_plot(title=title, xlabel=xlabel, ylabel=ylabel, axis=axis)

    for ydata in ydata_all:
        for x, y in zip(xdata, ydata):
            lenx = xmax - xmin
            length = 0.5 / lenx
            offset = 0.5 / lenx
            xminline = x / lenx + offset - length / 2
            xmaxline = x / lenx + offset + length / 2
            ax.axhline(y=y,
                       xmin=xminline,
                       xmax=xmaxline,
                       linewidth=plot_params['linewidth'],
                       color=plot_params['color'])
            text = r'{}'.format(y)
            ax.text(x - 0.25, y + 0.3, text, fontdict=plot_params['font_options'])

    plot_params.set_scale(ax)
    plot_params.set_limits(ax)
    plot_params.draw_lines(ax)
    plot_params.show_legend(ax)
    plot_params.save_plot(saveas)

    return ax


def construct_corelevel_spectrum(coreleveldict,
                                 natom_typesdict,
                                 exp_references={},
                                 scale_to=-1,
                                 fwhm_g=0.6,
                                 fwhm_l=0.1,
                                 energy_range=[None, None],
                                 xspec=None,
                                 energy_grid=0.2,
                                 peakfunction='voigt',
                                 alpha_l=1.0,
                                 beta_l=1.5):
    """
    Constructrs a corelevel spectrum from a given corelevel dict

    :params:

    :returns: list: [xdata_spec, ydata_spec, ydata_single_all, xdata_all, ydata_all, xdatalabel]
    """
    xdata_all = []
    ydata_all = []
    ydata_spec = []
    xdata_spec = []
    xdatalabel = []
    energy_grid = round(energy_grid, 5)  # eV
    #count = 0
    #compound_info_new = compound_info

    for elem, corelevel_dict in coreleveldict.items():
        natom = natom_typesdict.get(elem, 0)
        #elem_count = 0
        for corelevel_name, corelevel_list in corelevel_dict.items():
            # get number of electron if fully occ:
            nelectrons = 1
            if 's' in corelevel_name:
                nelectrons = 2
            else:
                max_state_occ_spin = {'1/2': 2, '3/2': 4, '5/2': 6, '7/2': 8}
                # check if spin in name
                for key, val in max_state_occ_spin.items():
                    if key in corelevel_name:
                        nelectrons = val
            for i, corelevel in enumerate(corelevel_list):
                xdatalabel.append(elem + ' ' + corelevel_name)
                xdata_all.append(corelevel)
                ydata_all.append(natom[i] * nelectrons)
                #count = count + 1
                #elem_count = elem_count + 1
            '''
            not working yet bad design
            if compound_info:
                for compound, element_dict in compound_info.iteritems():
                    for elemt, number in element_dict.iteritems():
                        print number
                        if elemt == elem:
                            # we need to set the index that we find it later, group it
                            if isinstance(number, list):
                                continue
                            compound_info_new[compound][elemt] = [count-elem_count, count-elem_count+number]
             '''
    xmin = min(xdata_all) - 2  #0.5
    xmax = max(xdata_all) + 2  #0.5
    if energy_range[0]:
        xmin = energy_range[0]
    if energy_range[1]:
        xmax = energy_range[1]
    # xdata_spec = np.array(np.arange(xmax,xmin, -energy_grid))
    if xspec is not None:
        xdata_spec = xspec
    else:
        xdata_spec = np.array(np.arange(xmin, xmax + energy_grid, energy_grid))
    ydata_spec = np.zeros(len(xdata_spec), dtype=float)
    ydata_single_all = []
    for i, xpoint in enumerate(xdata_all):
        if peakfunction == 'gaus':
            data_f = np.array(gaussian(xdata_spec, fwhm_g, xpoint))  #, 1.0))
        elif peakfunction == 'voigt':
            data_f = np.array(voigt_profile(xdata_spec, fwhm_g, fwhm_l, xpoint))  # different fwhn for g und l
        elif peakfunction == 'pseudo-voigt':
            data_f = np.array(pseudo_voigt_profile(xdata_spec, fwhm_g, fwhm_l, xpoint))
        elif peakfunction == 'lorentz':
            data_f = np.array(lorentzian(xdata_spec, fwhm_l, xpoint))
        elif peakfunction == 'doniach-sunjic':
            data_f = np.array(doniach_sunjic(xdata_spec, scale=1.0, E_0=xpoint, gamma=fwhm_l, alpha=fwhm_g))
        elif peakfunction == 'asymmetric_lorentz_gauss_conv':
            #print(xpoint, xdata_spec)
            data_f = np.array(
                asymmetric_lorentz_gauss_conv(xdata_spec,
                                              xpoint,
                                              fwhm_g=fwhm_g,
                                              fwhm_l=fwhm_l,
                                              alpha=alpha_l,
                                              beta=beta_l))
        else:
            print('given peakfunction type not known')
            data_f = []
            return

        # sometimes we get a point to much if constructed from new mesh..
        if len(ydata_spec) < len(data_f):
            # TODO: further adjustements? we assume only one point difference
            data_f = data_f[:-1]
        #print('length', len(ydata_spec), len(data_f))
        #gaus_f = lorentzian(xdata_spec, xpoint, 0.6, 100.0)
        if peakfunction == 'doniach-sunjic':
            ydata_spec = ydata_spec + ydata_all[i] * data_f
            ydata_single_all.append(ydata_all[i] * data_f)
        else:
            ydata_spec = ydata_spec + ydata_all[i] * data_f
            ydata_single_all.append(ydata_all[i] * data_f)

    # we scale after and not before, because the max intensity is not neccesary
    # the number of electrons.
    if scale_to > 0.0:
        y_valmax = max(ydata_spec)
        scalingfactor = scale_to / y_valmax
        ydata_spec = ydata_spec * scalingfactor
        ydata_single_all_new = []
        for ydata_single in ydata_single_all:
            ydata_single_all_new.append(ydata_single * scalingfactor)
        ydata_single_all = ydata_single_all_new

    return [xdata_spec, ydata_spec, ydata_single_all, xdata_all, ydata_all, xdatalabel]


@ensure_plotter_consistency(plot_params)
def plot_corelevel_spectra(coreleveldict,
                           natom_typesdict,
                           exp_references={},
                           scale_to=-1,
                           show_single=True,
                           show_ref=True,
                           energy_range=(None, None),
                           title='',
                           fwhm_g=0.6,
                           fwhm_l=0.1,
                           energy_grid=0.2,
                           peakfunction='voigt',
                           linestyle_spec='-',
                           marker_spec='o',
                           color_spec='k',
                           color_single='g',
                           xlabel='Binding energy [eV]',
                           ylabel='Intensity [arb] (natoms*nelectrons)',
                           saveas=None,
                           xspec=None,
                           alpha_l=1.0,
                           beta_l=1.0,
                           **kwargs):
    """
    Plotting function of corelevel in the form of a spectrum.

    Convention: Binding energies are positiv!

    Args:
        coreleveldict: dict of corelevels with a list of corelevel energy of atomstypes
        # (The given corelevel accounts for a weight (number of electrons for full occupied corelevel) in the plot.)
        natom_typesdict: dict with number of atom types for each entry
    Kwargs:
        exp_references: dict with experimental refereces, will be ploted as vertical lines
        show_single (bool): plot all single peaks.
        scale_to float: the maximum 'intensity' will be scaled to this value (useful for experimental comparisons)
        title (string): something for labeling
        fwhm (float): full width half maximum of peaks (gaus, lorentz or voigt_profile)
        energy_grid (float): energy resolution
        linetyp_spec : linetype for spectrum
        peakfunction (string): what the peakfunction should be {'voigt', 'pseudo-voigt', 'lorentz', 'gaus'}

    example:
        coreleveldict = {u'Be': {'1s1/2' : [-1.0220669053033051, -0.3185614920138805,-0.7924091040092139]}}
        n_atom_types_Be12Ti = {'Be' : [4,4,4]}
    """
    #show_compound=True, , compound_info={} compound_info dict: dict that can be used to specify what component should be shown together     compound_info = {'Be12Ti' : {'Be' : 4, 'Ti' : 1}, 'BeTi' : {'Be' : 1, 'Ti' : 1}}
    # TODO feature to make singles of different compounds a different color
    [xdata_spec, ydata_spec, ydata_single_all, xdata_all, ydata_all,
     xdatalabel] = construct_corelevel_spectrum(coreleveldict,
                                                natom_typesdict,
                                                exp_references=exp_references,
                                                scale_to=scale_to,
                                                fwhm_g=fwhm_g,
                                                fwhm_l=fwhm_l,
                                                energy_range=energy_range,
                                                xspec=xspec,
                                                energy_grid=energy_grid,
                                                peakfunction=peakfunction,
                                                alpha_l=alpha_l,
                                                beta_l=beta_l)

    xmin = min(xdata_all) - 2  #0.5
    xmax = max(xdata_all) + 2  #0.5
    if energy_range[0]:
        xmin = energy_range[0]
    if energy_range[1]:
        xmax = energy_range[1]

    xdata = xdata_all
    ydata = ydata_all
    ymax2 = max(ydata_spec) + 1
    ymin = -0.3
    ymax = max(ydata) + 1
    limits = {'x': (xmin, xmax), 'y': (ymin, ymax)}
    limits_spec = {'x': (xmin, xmax), 'y': (ymin, ymax2)}
    #title = title  #'Spectrum of {}'.format(compound)
    """
    # ToDo redesign to use multiple_scatterplot
    axis = multiple_scatterplots(ydata, xdata, xlabel, ylabel, title, plot_labels,
                          linestyle='', marker='o', markersize=markersize_g, legend=legend_g,
                          legend_option={}, saveas='mscatterplot',
                          limits=limits, scale=[None, None],
                          axis=None, xerr=None, yerr=None, colors=[], linewidth=[], xticks=[], title=title, xlabel=xlabel, ylabel=ylabel, **kwargs)
    """

    #print len(xdata), len(ydata)

    if 'plot_label' not in kwargs:
        kwargs['plot_label'] = 'corelevel shifts'

    if 'linestyle' not in kwargs:
        kwargs['linestyle'] = ''

    if saveas is None:
        saveas = 'XPS_theo_{}_{}'.format(fwhm_g, title)
        saveas1 = 'XPS_theo_2_{}_{}'.format(fwhm_g, title)
    else:
        saveas1 = saveas[1]
        saveas = saveas[0]

    ####################################
    ##### PLOT 1, plot raw datapoints

    if not plot_params['show']:
        return [xdata_spec, ydata_spec, ydata_single_all, xdata_all, ydata_all, xdatalabel]

    states = []
    if show_ref and exp_references:
        for elm, ref_list_dict in exp_references.items():
            for state, ref_list in ref_list_dict.items():
                states.extend(ref_list)

    ax = single_scatterplot(xdata_all,
                            ydata_all,
                            xlabel=xlabel,
                            ylabel=ylabel,
                            title=title,
                            line_options={
                                'color': 'k',
                                'linestyle': '-',
                                'linewidth': 2
                            },
                            lines={'vertical': {
                                'pos': states,
                                'ymin': 0,
                                'ymax': 0.1
                            }},
                            limits=limits,
                            saveas=saveas,
                            **kwargs)
    ''' TODO
    for j,y in enumerate(ydata_all):
        for i,x in enumerate(xdata):
            lenx = xmax-xmin
            length = 0.5/lenx
            offset = 0.5/lenx
            xminline = x/lenx + offset - length/2
            xmaxline = x/lenx + offset + length/2
            plt.axhline(y=y[i], xmin=xminline, xmax=xmaxline, linewidth=2, color='k')
            text = r'{}'.format(y[i])
            plt.text(x-0.25, y[i]+0.3, text, fontdict=font)
    '''

    ##############################################################
    ##### PLOT 2, plot spectra, voigts around datapoints #########

    kwargs.pop('linestyle', None)
    kwargs.pop('marker', None)
    kwargs.pop('color', None)
    kwargs.pop('save', None)
    kwargs.pop('save_plots', None)

    ax2 = single_scatterplot(xdata_spec,
                             ydata_spec,
                             xlabel=xlabel,
                             ylabel=ylabel,
                             title=title,
                             marker=marker_spec,
                             linestyle=linestyle_spec,
                             color=color_spec,
                             line_options={
                                 'color': 'k',
                                 'linestyle': '-',
                                 'linewidth': 2
                             },
                             lines={'vertical': {
                                 'pos': states,
                                 'ymin': 0,
                                 'ymax': 0.1
                             }},
                             show=False,
                             save_plots=False,
                             limits=limits_spec,
                             **kwargs)

    if show_single:
        ax2 = multiple_scatterplots([xdata_spec] * len(ydata_single_all),
                                    ydata_single_all,
                                    xlabel=xlabel,
                                    ylabel=ylabel,
                                    title=title,
                                    show=False,
                                    save_plots=False,
                                    axis=ax2,
                                    linestyle='-',
                                    color=color_single,
                                    limits=limits_spec,
                                    **kwargs)
    '''TODO
    if show_compound and compound_info:
        for i,compound_data in enumerate(ydata_compound):
            plotlabel = compound_plot_label[i]
            plt.plot(xdata_spec, compound_data, '-', label=plotlabel, color = color,
                 linewidth=linewidth_g1, markersize = markersize_g)
    '''
    plot_params.save_plot(saveas1)

    # for plotting or file writting
    return [xdata_spec, ydata_spec, ydata_single_all, xdata_all, ydata_all, xdatalabel, ax, ax2]


def asymmetric_lorentz(x, fwhm, mu, alpha=1.0, beta=1.5):
    """
    asymetric lorentz function

    L^alpha for x<=mu
    L^beta for x>mu
    See
    casexps LA
    """

    index = 0
    for i, entry in enumerate(x):
        if entry <= mu:
            index = i
        else:
            break

    ydata1 = lorentzian_one(x[:index], fwhm, mu)**alpha
    ydata2 = lorentzian_one(x[index:], fwhm, mu)**beta

    return np.array(list(ydata1) + list(ydata2))


def lorentzian_one(x, fwhm, mu):
    """
    Returns a Lorentzian line shape at x with FWHM fwhm and mean mu
    """
    return 1.0 / (1 + 4 * ((x - mu) / fwhm)**2)


def gauss_one(x, fwhm, mu):
    """
    Returns a Lorentzian line shape at x with FWHM fwhm and mean mu
    """
    x = np.array(x)
    return np.exp(-4 * np.log(2) * ((x - mu) / fwhm)**2)


def asymmetric_lorentz_gauss_sum(x, mu, fwhm_l, fwhm_g, alpha=1.0, beta=1.5):
    """
    asymmetric Lorentzian with Gauss convoluted

    """

    ygaus = np.array(gauss_one(x, fwhm_g, mu))
    ylorentz = np.array(asymmetric_lorentz(x, fwhm_l, mu, alpha=alpha, beta=beta))
    ydata = ylorentz + ygaus

    return ydata


def asymmetric_lorentz_gauss_conv(x, mu, fwhm_l, fwhm_g, alpha=1.0, beta=1.5):
    """
    asymmetric Lorentzian with Gauss convoluted

    """
    from scipy.signal import fftconvolve
    #from scipy import signal
    # only one function has to be translated
    # gaus has to be symmetric arround 0 for convolution
    # and on the same equidistant grid
    xstep = abs(round(x[-1] - x[-2], 6))
    rangex = abs(x[-1] - x[0])
    #print(xstep, rangex)
    xgaus = np.arange(-rangex / 2.0, rangex / 2.0 + xstep, xstep)
    #print(xgaus[:10], xgaus[-1])
    ygaus = np.array(gauss_one(xgaus, fwhm_g, mu=0.0), dtype=np.float64)
    ylorentz = np.array(asymmetric_lorentz(x, fwhm_l, mu=mu, alpha=alpha, beta=beta), dtype=np.float64)
    ydata = np.convolve(ylorentz, ygaus, mode='same')

    return ydata


'''
def asymmetric_lorentz_gauss_conv_interp(x, mu, fwhm_l,fwhm_g,alpha=1.0, beta=1.5, grid_factor=10):
    """
    asymmetric Lorentzian with Gauss convoluted.

    Real convolution. For the convolution to work we construct a finer mesh,
    with mu shifted to 0.0 on which we convolute.
    Then we linear interpolate on the original mesh points.

    """
    import numpy as np
    from scipy.interpolate import interp1d
    # convolution has to be symmetric arround 0
    # check if xmu is right or left,
    # double longest side, shift xmu to 0.0
    # then interpolate at original mesh points

    x = np.array(x, dtype=np.float64)
    xstep = round(x[-1]-x[-2],6)
    xstepmesh = xstep/grid_factor

    xmesh = np.arange(x[0], x[-1]+xstepmesh/2.0, xstepmesh)

    xmu = np.float64(0.0)
    muindex = 0
    for i, en in enumerate(xmesh):
        if en <=mu:
            xmu = mu
            muindex = i
        else:
            break

    if muindex <= len(xmesh)/2.0:
        xtrans = np.arange(-x[-1] + xmu - xstep, x[-1] - xmu + xstep, xstepmesh)
    else:
        xtrans = np.arange(x[0] - xmu - xstep, -x[0] + xmu + xstep, xstepmesh)

    ygaus = np.array(gauss_one(xtrans, fwhm_g, mu=0.0), dtype=np.float64)
    ylorentz = np.array(asymmetric_lorentz(xtrans,fwhm_l, mu=0.0, alpha=alpha, beta=beta), dtype=np.float64)
    ydata = np.convolve(ylorentz,ygaus,mode='same')

    # iterpolate function and evalutate at original xdata
    f = interp1d(xtrans+xmu, ydata, assume_sorted=True)
    ydata_return = f(x)

    return ydata_return



def asymmetric_lorentz_gauss_conv1(x, mu, fwhm_l,fwhm_g,alpha=1.0, beta=1.5):
    """
    asymmetric Lorentzian with Gauss convoluted

    """
    import numpy as np
    from scipy import signal

    ygaus = np.array(gauss_one(x, fwhm_g, mu))
    ylorentz = np.array(asymmetric_lorentz(x,fwhm_l, mu, alpha=alpha, beta=beta))
    #ydata = np.convolve(ylorentz,np.flip(ygaus, axis=0),mode='same')
    ydata = np.convolve(ylorentz,ygaus,mode='same')
    #ydata = ylorentz+ygaus
    #ydata = direct_convolution(ylorentz,ygaus)
    #ydata = signal.convolve(ylorentz,ygaus)

    return ydata


def asymmetric_lorentz_gauss_conv_linear(x, mu, fwhm_l,fwhm_g,alpha=1.0, beta=1.5):
    """
    asymmetric Lorentzian with Gauss convoluted

    """
    import numpy as np
    #from scipy import signal

    # convolution has to be symmetric arround 0
    # check if xmu is right or left,
    # double longest side, shift xmu to 0.0
    # then shift back and cut off the rest

    # we asume equidistant mesh
    x = np.array(x, dtype=np.float64)


    xstep = round(x[-1]-x[-2],6)

    xmu = np.float64(0.0)
    muindex = 0
    for i, en in enumerate(x):
        if en <=mu:
            xmu = en
            muindex = i
        else:
            break

    #print(x[0]-xmu, -x[0]+xmu,xstep)
    if muindex <= len(x)/2.0:
        xtrans = np.arange(-x[-1]+xmu, x[-1]-xmu,xstep)
    else:
        xtrans = np.arange(x[0]-xmu, -x[0]+xmu,xstep)

    # To keep mu continous we parse the exact mu to the lorentz and gauss...
    # the convolution will not be totally correct...
    # todo maybe combine with gridfactor...
    ygaus = np.array(gauss_one(xtrans, fwhm_g, mu=(xmu-mu)/2.0), dtype=np.float64)
    ylorentz = np.array(asymmetric_lorentz(xtrans,fwhm_l, mu=(xmu-mu)/2.0, alpha=alpha, beta=beta), dtype=np.float64)
    ydata = np.convolve(ylorentz,ygaus,mode='same')

    # shift data back... through cutting it
    if muindex <= len(x)/2.0:
        ydata_new = np.array(ydata[len(ydata)-len(x):], dtype=np.float64)
    else:
        ydata_new = np.array(ydata[:len(x)], dtype=np.float64)

    return ydata_new

def asymmetric_lorentz_gauss_conv(x, mu, fwhm_l,fwhm_g,alpha=1.0, beta=1.5, grid_factor=10):
    """
    asymmetric Lorentzian with Gauss convoluted

    """
    import numpy as np
    #from scipy import signal

    # convolution has to be symmetric arround 0
    # check if xmu is right or left,
    # double longest side, shift xmu to 0.0
    # then shift back and cut off the rest


    # TODO: overall a bit slow, can we speed this up?
    # cone idea for speed up would be only increase the mesh fineness between the x where mu lives...
    # this way npoints is len(x)+gridfactor and not len(x)*gridfoctor
    # logic becomes harder...
    # convolution is n^2
    # we asume equidistant mesh
    # we increase the mesh by a factor of grid_factor
    # because mu can only vary by the meshstep...
    x = np.array(x, dtype=np.float64)


    xstep = round(x[-1]-x[-2],6)
    xstepmesh = xstep/grid_factor

    xmesh1 = np.arange(x[0], x[-1]+xstepmesh/2.0, xstepmesh)
    xmesh = np.round(xmesh1, 6)

    xmu = np.float64(0.0)
    muindex = 0
    for i, en in enumerate(xmesh):
        if en <=mu:
            xmu = en#mu
            muindex = i
        else:
            break

    if muindex <= len(xmesh)/2.0:
        xtrans = np.arange(-x[-1]+xmu, x[-1]-xmu,xstepmesh)
    else:
        xtrans = np.arange(x[0]-xmu, -x[0]+xmu,xstepmesh)

    ygaus = np.array(gauss_one(xtrans, fwhm_g, mu=0.0), dtype=np.float64)
    ylorentz = np.array(asymmetric_lorentz(xtrans,fwhm_l, mu=0.0, alpha=alpha, beta=beta), dtype=np.float64)
    ydata = np.convolve(ylorentz,ygaus,mode='same')

    # shift data back... through cutting it
    if muindex <= len(xmesh)/2.0:
        ydata_new = np.array(ydata[len(ydata)-len(xmesh):], dtype=np.float64)
    else:
        ydata_new = np.array(ydata[:len(xmesh)], dtype=np.float64)

    # back to original mesh
    ydata_return = ydata_new[0::grid_factor]

    return ydata_return


def direct_convolution(a,b):
    """
    convolution, a, b same length, arrays
    """
    import numpy as np

    ydata = np.zeros(len(a))
    for i, entry in enumerate(a):
        for j, entry2 in enumerate(a):
             ydata[i] = ydata[i] + (entry2*b[i-j])

    return ydata
'''


def doniach_sunjic(x, scale=1.0, E_0=0, gamma=1.0, alpha=0.0):
    """
    Doniach Sunjic asymmetric peak function. tail to higher binding energies.

    param x: list values to evaluate this function
    param scale: multiply the function with this factor
    param E_0: position of the peak
    param gamma, 'lifetime' broadening
    param alpha: 'asymmetry' parametera

    See
    Doniach S. and Sunjic M., J. Phys. 4C31, 285 (1970)
    or http://www.casaxps.com/help_manual/line_shapes.htm
    """

    arg = (E_0 - x) / gamma
    alpha2 = (1.0 - alpha)
    #scale = scale/(gamma**alpha2)
    don_su = np.cos(np.pi * alpha + alpha2 * np.arctan(arg)) / (1 + arg**2)**(alpha2 / 2)
    return np.array(scale * don_su)


def gaussian(x, fwhm, mu):
    """
    Returns Gaussian line shape at x with FWHM fwhm and mean mu

    """

    #hwhm = fwhm/2.0
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    #return np.sqrt(np.log(2) / np.pi) / hwhm\
    #                         * np.exp(-((x-mu) / hwhm)**2 * np.log(2))
    return np.exp(-(x - mu)**2 / (2 * (sigma**2))) / (np.sqrt(2 * np.pi) * sigma)


def lorentzian(x, fwhm, mu):
    """
    Returns a Lorentzian line shape at x with FWHM fwhm and mean mu
    """
    hwhm = fwhm / 2.0
    return hwhm / np.pi / ((x - mu)**2 + hwhm**2)


def voigt_profile(x, fwhm_g, fwhm_l, mu):
    """
    Return the Voigt line shape at x with Lorentzian component FWHM fwhm_l
    and Gaussian component FWHM fwhm_g and mean mu.
    There is no closed form for the Voigt profile,
    but it is related to the real part of the Faddeeva function (wofz),
    which is used here.

    """
    from scipy.special import wofz  #pylint: disable=no-name-in-module

    hwhm_l = fwhm_l / 2.0
    sigma = fwhm_g / (2 * np.sqrt(2 * np.log(2)))
    # complex 1j
    return np.real(wofz(((x - mu) + 1j * hwhm_l) / sigma / np.sqrt(2))) / sigma / np.sqrt(2 * np.pi)


def CDF_voigt_profile(x, fwhm_g, fwhm_l, mu):
    """
    Cumulative distribution function of a voigt profile
    implementation of formula found here: https://en.wikipedia.org/wiki/Voigt_profile
    # TODO: is there an other way then to calc 2F2?
    # or is there an other way to calc the integral of wofz directly, or use
    different error functions.
    """
    from scipy.special import erf  #pylint: disable=no-name-in-module
    pass


def hyp2f2(a, b, z):
    """
    Calculation of the 2F2() hypergeometric function,
    since it is not part of scipy
    with the identity 2. from here:
    https://en.wikipedia.org/wiki/Generalized_hypergeometric_function
    a, b,z array like inputs
    TODO: not clear to me how to do this... the identity is only useful
    if we mange the adjust the arguments in a way that we can use them...
    also maybe go for the special case we need first: 1,1,3/2;2;-z2
    """
    from scipy.special import hyp0f1

    pass


def pseudo_voigt_profile(x, fwhm_g, fwhm_l, mu, mix=0.5):
    """
    Linear combination of gaussian and loretzian instead of convolution

    Args:
        x: array of floats
        fwhm_g: FWHM of gaussian
        fwhm_l: FWHM of Lorentzian
        mu: Mean
        mix: ratio of gaus to lorentz, mix* gaus, (1-mix)*Lorentz

    """
    #pseudo_voigt = []
    if mix > 1:
        print('mix has to be smaller than 1.')
        return []
    gaus = gaussian(x, fwhm_g, mu)
    lorentz = lorentzian(x, fwhm_l, mu)
    return mix * gaus + (1 - mix) * lorentz


class PDF(object):

    def __init__(self, pdf, size=(200, 200)):
        """Display a PDF file inside a Jupyter notebook.

        Note: alternative to using aiida.tools.visualization.Graph class.
        Example: https://aiida-tutorials.readthedocs.io/en/latest/pages/2020_Intro_Week/notebooks/querybuilder-tutorial.html#generating-a-provenance-graph

        Reference: https://stackoverflow.com/a/19470377/8116031

        :example:

        >>> # !verdi node graph generate 23
        >>> PDF('23.dot.pdf',size=(800,600))

        :param pdf:
        :param size:
        """
        self.pdf = pdf
        self.size = size

    def _repr_html_(self):
        return '<iframe src={0} width={1[0]} height={1[1]}></iframe>'.format(self.pdf, self.size)

    def _repr_latex_(self):
        return r'\includegraphics[width=1.0\textwidth]{{{0}}}'.format(self.pdf)


def plot_colortable(colors: typing.Dict, title: str, sort_colors: bool = True, emptycols: int = 0):
    """Plot a legend of named colors.

    Reference: https://matplotlib.org/3.1.0/gallery/color/named_colors.html

    :param colors: a dict color_name : color_value (hex str, rgb tuple, ...)
    :param title: plot title
    :param sort_colors: sort
    :param emptycols:
    :return: figure
    """
    import matplotlib.colors as mcolors

    cell_width = 212
    cell_height = 22
    swatch_width = 48
    margin = 12
    topmargin = 40

    # Sort colors by hue, saturation, value and name.
    if sort_colors is True:
        by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))), name) for name, color in colors.items())
        names = [name for hsv, name in by_hsv]
    else:
        names = list(colors)

    n = len(names)
    ncols = 4 - emptycols
    nrows = n // ncols + int(n % ncols > 0)

    width = cell_width * 4 + 2 * margin
    height = cell_height * nrows + margin + topmargin
    dpi = 72

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(margin / width, margin / height, (width - margin) / width, (height - topmargin) / height)
    ax.set_xlim(0, cell_width * 4)
    ax.set_ylim(cell_height * (nrows - 0.5), -cell_height / 2.)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()
    ax.set_title(title, fontsize=24, loc='left', pad=10)

    for i, name in enumerate(names):
        row = i % nrows
        col = i // nrows
        y = row * cell_height

        swatch_start_x = cell_width * col
        swatch_end_x = cell_width * col + swatch_width
        text_pos_x = cell_width * col + swatch_width + 7

        ax.text(text_pos_x, y, name, fontsize=14, horizontalalignment='left', verticalalignment='center')

        ax.hlines(y, swatch_start_x, swatch_end_x, color=colors[name], linewidth=18)

    return fig
