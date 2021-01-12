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
This module contains a subclass of :py:class:`~masci_tools.vis.Plotter` for the matplotlib library
"""
from masci_tools.vis import Plotter
import matplotlib.pyplot as plt
from matplotlib import cm
import copy


class MatplotlibPlotter(Plotter):
    """
    Class for plotting parameters and standard code snippets for plotting with the
    matplotlib backend.

    Kwargs in the __init__ method are forwarded to setting default values for the instance

    For specific documentation about the parameter/defaults handling refer to
    :py:class:`~masci_tools.vis.Plotter`.

    Below the current defined default values are shown

    .. literalinclude:: ../../../masci_tools/vis/matplotlib_plotter.py
       :language: python
       :lines: 39-124
       :linenos:

    """
    _MATPLOTLIB_DEFAULTS = {
        # figure properties
        'title_fontsize': 16,
        'figure_kwargs': {
            'figsize': (8, 6),
            'dpi': 80,
            'facecolor': 'w',
            'edgecolor': 'k',
            'constrained_layout': False,
        },

        # axis properties
        'alpha': 1,
        'axis_linewidth': 1.5,
        'use_axis_formatter': False,
        'set_powerlimits': True,
        'xticks': None,
        'xticklabels': None,
        'yticks': None,
        'yticklabels': None,

        # plot properties
        'linewidth': 2.0,
        'linestyle': '-',
        'marker': 'o',
        'markersize': 4.0,
        'color': None,
        'edgecolor': None,
        'facecolor': None,
        'plot_label': None,
        'area_plot': False,
        'plot_alpha': 1.0,
        'cmap': 'viridis',
        'norm': None,
        'shading': 'gouraud',
        'rasterized': True,

        #scale and limits placeholder
        'scale': None,
        'limits': None,

        # x, y label
        'labelfontsize': 15,
        'lines': None,
        'line_options': {
            'linestyle': '--',
            'color': 'k',
            'linewidth': 1.0
        },

        # ticks
        'ticklabelsizex': 14,
        'ticklabelsizey': 14,
        'tick_paramsx': {
            'size': 4.0,
            'width': 1.0,
            'labelsize': 14,
            'length': 5,
            'labelrotation': 0
        },
        'tick_paramsy': {
            'size': 4.0,
            'width': 1.0,
            'labelsize': 14,
            'length': 5,
            'labelrotation': 0
        },
        'ticklabelsizex_minor': 0,
        'ticklabelsizey_minor': 0,
        'tick_paramsx_minor': {
            'size': 2.0,
            'width': 1.0,
            'labelsize': 0,
            'length': 2.5
        },
        'tick_paramsy_minor': {
            'size': 2.0,
            'width': 1.0,
            'labelsize': 0,
            'length': 2.5
        },
        'colorbar': True,
        # legend properties
        'legend': False,
        'legend_options': {
            'bbox_to_anchor': (0.65, 0.97),
            'fontsize': 16,
            'linewidth': 3.0,
            'borderaxespad': 0,
            'loc': 2,
            'fancybox': True
        },

        # save all plots?
        'save_plots': False,  # True
        'save_format': 'png',  #'pdf'
        'tightlayout': False,
        'show': True,
        # write data to file
        'save_raw_plot_data': False,
        'raw_plot_data_format': 'txt'
    }

    _MATPLOTLIB_LIST_ARGS = {'xticks', 'xticklabels', 'yticks', 'yticklabels'}

    #Sets of keys with special purposes

    _PLOT_KWARGS = {'linewidth', 'linestyle', 'marker', 'markersize', 'color', 'plot_label', 'plot_alpha'}
    _PLOT_KWARGS_COLORMESH = {
        'linewidth', 'linestyle', 'shading', 'rasterized', 'cmap', 'norm', 'edgecolor', 'facecolor', 'plot_label', 'plot_alpha'
    }
    _PLOT_KWARGS_HIST = {'linewidth', 'linestyle', 'color', 'plot_label', 'plot_alpha', 'edgecolor', 'facecolor'}

    def __init__(self, **kwargs):
        super().__init__(self._MATPLOTLIB_DEFAULTS, list_arguments=self._MATPLOTLIB_LIST_ARGS, **kwargs)

    def plot_kwargs(self, ignore=None):
        """
        Creates a dict or list of dicts (for multiple plots) with the defined parameters
        for the plotting calls fo matplotlib

        :param ignore: str or list of str (optional), defines keys to ignore in the creation of the dict
        """
        if self.plot_type == 'default':
            kwargs_keys = self._PLOT_KWARGS
        elif self.plot_type == 'colormesh':
            kwargs_keys = self._PLOT_KWARGS_COLORMESH
        elif self.plot_type == 'histogram':
            kwargs_keys = self._PLOT_KWARGS_HIST

        plot_kwargs = self.get_multiple_kwargs(kwargs_keys, ignore=ignore)

        any_list = any([isinstance(val, list) for val in plot_kwargs.values()])

        if any_list:
            for key, val in plot_kwargs.items():
                if not isinstance(val, list):
                    plot_kwargs[key] = [val] * self.num_plots
        elif not self.single_plot:
            plot_kwargs = {key: [value] for key, value in plot_kwargs.items()}

        if 'plot_label' in plot_kwargs:
            plot_kwargs['label'] = plot_kwargs['plot_label']
            plot_kwargs.pop('plot_label')

        if 'plot_alpha' in plot_kwargs:
            plot_kwargs['alpha'] = plot_kwargs['plot_alpha']
            plot_kwargs.pop('plot_alpha')

        if not self.single_plot:
            plot_kwargs = [{key: value[index]
                            for key, value in plot_kwargs.items()}
                           for index in range(max(map(len, plot_kwargs.values())))]
            if len(plot_kwargs) != self.num_plots:
                if len(plot_kwargs) == 1:
                    plot_kwargs = [copy.deepcopy(plot_kwargs[0]) for i in range(self.num_plots)]
                else:
                    raise ValueError('Length does not match number of plots')
            for index, value in enumerate(plot_kwargs):
                if self[('area_plot', index)]:
                    value.pop('marker', None)
                    value.pop('markersize', None)
                    plot_kwargs[index] = value
        else:
            if self['area_plot']:
                plot_kwargs.pop('marker', None)
                plot_kwargs.pop('markersize', None)

        return plot_kwargs

    def prepare_plot(self, title=None, xlabel=None, ylabel=None, zlabel=None, axis=None, minor=False, projection=None):
        """
        Prepares the figure of a matplotlib plot, setting the labels/titles, ticks, ...

        :param title: str for the title of the figure
        :param xlabel: str for the label on the x-axis
        :param ylabel: str for the label on the y-axis
        :param zlabel: str for the label on the z-axis
        :param axis: matplotlib axes object, optional, if given the operations are performed on the object
                     otherwise a new figure and subplot are created
        :param minor: bool, if True minor tick parameters are set
        :param projection: str, passed on to the add_subplot call

        """
        if axis is not None:
            ax = axis
        else:
            fig = plt.figure(num=None, **self['figure_kwargs'])
            ax = fig.add_subplot(111, projection=projection)

        for axes in ['top', 'bottom', 'left', 'right']:
            ax.spines[axes].set_linewidth(self['axis_linewidth'])
        ax.set_title(title, fontsize=self['title_fontsize'], alpha=self['alpha'], ha='center')
        ax.set_xlabel(xlabel, fontsize=self['labelfontsize'])
        ax.set_ylabel(ylabel, fontsize=self['labelfontsize'])
        if zlabel is not None:
            ax.set_zlabel(zlabel, fontsize=self['labelfontsize'])
        ax.yaxis.set_tick_params(**self['tick_paramsy'])
        ax.xaxis.set_tick_params(**self['tick_paramsx'])

        if minor:
            ax.yaxis.set_tick_params(which='minor', **self['tick_paramsy_minor'])
            ax.xaxis.set_tick_params(which='minor', **self['tick_paramsx_minor'])

        if self['xticks'] is not None:
            ax.xaxis.set_ticks(self['xticks'])
        if self['xticklabels'] is not None:
            ax.xaxis.set_ticklabels(self['xticklabels'])

        if self['yticks'] is not None:
            ax.yaxis.set_ticks(self['yticks'])
        if self['yticklabels'] is not None:
            ax.yaxis.set_ticklabels(self['yticklabels'])

        if self['use_axis_formatter']:
            if self['set_powerlimits']:
                ax.yaxis.get_major_formatter().set_powerlimits((0, 3))
                ax.xaxis.get_major_formatter().set_powerlimits((0, 3))
            ax.yaxis.get_major_formatter().set_useOffset(False)
            ax.xaxis.get_major_formatter().set_useOffset(False)

        return ax

    def set_scale(self, ax):
        """
        Set scale of the axis (for example 'log')

        :param ax: Axes object on which to perform the operation
        """

        if self['scale'] is not None:
            if 'x' in self['scale']:
                ax.set_xscale(self['scale']['x'])
            if 'y' in self['scale']:
                ax.set_yscale(self['scale']['y'])
            if 'z' in self['scale']:
                ax.set_zscale(self['scale']['z'])

    def set_limits(self, ax):
        """
        Set limits of the axis

        :param ax: Axes object on which to perform the operation
        """

        if self['limits'] is not None:
            if 'x' in self['limits']:
                xmin = self['limits']['x'][0]
                xmax = self['limits']['x'][1]
                ax.set_xlim(xmin, xmax)
            if 'y' in self['limits']:
                ymin = self['limits']['y'][0]
                ymax = self['limits']['y'][1]
                ax.set_ylim(ymin, ymax)
            if 'z' in self['limits']:
                zmin = self['limits']['z'][0]
                zmax = self['limits']['z'][1]
                ax.set_zlim(zmin, zmax)
            if 'color' in self['limits']:
                cmin = self['limits'][0]
                cmax = self['limits'][1]
                ax.set_clim(cmin, cmax)

    def draw_lines(self, ax):
        """
        Draw horizontal and vertical lines specified in the lines argument

        :param ax: Axes object on which to perform the operation
        """
        if self['lines'] is not None:
            if 'horizontal' in self['lines']:
                lines = copy.deepcopy(self['lines']['horizontal'])
                if not isinstance(lines, list):
                    lines = [lines]

                for line_def in lines:
                    options = copy.deepcopy(self['line_options'])
                    if isinstance(line_def, dict):
                        positions = line_def.pop('pos')
                        if not isinstance(positions, list):
                            positions = [positions]
                        options.update(line_def)
                    elif isinstance(line_def, list):
                        positions = line_def
                    else:
                        positions = [line_def]

                    for pos in positions:
                        ax.axhline(pos, **options)
            if 'vertical' in self['lines']:
                lines = copy.deepcopy(self['lines']['vertical'])
                if not isinstance(lines, list):
                    lines = [lines]

                for line_def in lines:
                    options = copy.deepcopy(self['line_options'])
                    if isinstance(line_def, dict):
                        positions = line_def.pop('pos')
                        if not isinstance(positions, list):
                            positions = [positions]
                        options.update(line_def)
                    elif isinstance(line_def, list):
                        positions = line_def
                    else:
                        positions = [line_def]

                    for pos in positions:
                        ax.axvline(pos, **options)

    def show_legend(self, ax):
        """
        Print a legend for the plot

        :param ax: Axes object on which to perform the operation
        """

        if self['legend']:
            loptions = copy.deepcopy(self['legend_options'])
            linewidth = loptions.pop('linewidth', 1.5)
            title_font_size = loptions.pop('fontsize', 15)
            leg = ax.legend(**loptions)
            leg.get_frame().set_linewidth(linewidth)
            leg.get_title().set_fontsize(title_font_size)  #legend 'Title' fontsize

    def show_colorbar(self, ax):
        """
        Print a colorbar for the plot

        :param ax: Axes object on which to perform the operation
        """

        if self['colorbar']:
            plt.colorbar(cm.ScalarMappable(cmap=self['cmap'], norm=self['norm']), ax=ax)

    def save_plot(self, saveas):
        """
        Save the current figure or show the current figure

        :param saveas: str, filename for the resulting file
        """
        if self['save_plots']:
            savefilename = f"{saveas}.{self['save_format']}"
            print(f'Save plot to: {savefilename}')
            plt.savefig(savefilename, format=self['save_format'], transparent=True)
        if self['show']:
            plt.show()
