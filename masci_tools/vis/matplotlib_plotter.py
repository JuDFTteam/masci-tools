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
       :lines: 40-148
       :linenos:

    """
    _MATPLOTLIB_DEFAULTS = {
        # figure properties
        'title_fontsize': 16,
        'figure_kwargs': {
            'figsize': (8, 6),
            'dpi': 600,
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
        'color_cycle': None,
        'sub_colormap': None,

        # plot properties
        'linewidth': 2.0,
        'linestyle': '-',
        'marker': 'o',
        'markersize': 4.0,
        'color': None,
        'zorder': None,
        'repeat_colors_after': None,
        'edgecolor': None,
        'facecolor': None,
        'plot_label': None,
        'area_plot': False,
        'area_vertical': False,
        'area_enclosing_line': True,
        'area_alpha': 1.0,
        'area_linecolor': None,
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
        'font_options': {
            'family': 'serif',
            'color': 'black',
            'weight': 'normal',
            'size': 16,
        },

        # ticks
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
        'colorbar_padding': 0.1,
        # legend properties
        'legend': False,
        'legend_options': {
            'fontsize': 16,
            'linewidth': 3.0,
            'loc': 'best',
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

    _MATPLOTLIB_GENERAL_ARGS = {
        'save_plots', 'save_format', 'tightlayout', 'save_raw_plot_data', 'raw_plot_data_format', 'show', 'legend',
        'legend_options', 'colorbar', 'colorbar_padding', 'tick_paramsy', 'tick_paramsx', 'tick_paramsy_minor',
        'tick_paramsx_minor', 'font_options', 'line_options', 'labelfontsize', 'lines', 'scale', 'limits', 'xticks',
        'xticklabels', 'yticks', 'yticklabels', 'figure_kwargs', 'title_font_size', 'repeat_colors_after',
        'color_cycle', 'sub_colormap'
    }

    #Sets of keys with special purposes

    _PLOT_KWARGS = {'linewidth', 'linestyle', 'marker', 'markersize', 'color', 'plot_label', 'plot_alpha', 'zorder'}
    _PLOT_KWARGS_AREA = {'area_linecolor', 'area_alpha', 'zorder'}
    _PLOT_KWARGS_COLORMESH = {
        'linewidth', 'linestyle', 'shading', 'rasterized', 'cmap', 'norm', 'edgecolor', 'facecolor', 'plot_label',
        'plot_alpha', 'zorder'
    }
    _PLOT_KWARGS_HIST = {
        'linewidth', 'linestyle', 'color', 'plot_label', 'plot_alpha', 'edgecolor', 'facecolor', 'zorder'
    }

    def __init__(self, **kwargs):
        super().__init__(self._MATPLOTLIB_DEFAULTS, general_keys=self._MATPLOTLIB_GENERAL_ARGS, **kwargs)

    def plot_kwargs(self, ignore=None, extra_keys=None, plot_type='default', post_process=True, **kwargs):
        """
        Creates a dict or list of dicts (for multiple plots) with the defined parameters
        for the plotting calls fo matplotlib

        :param ignore: str or list of str (optional), defines keys to ignore in the creation of the dict
        :param extra_keys: optional set for addtional keys to retrieve
        :param post_process: bool, if True the parameters are cleaned up for inserting them directly into matplotlib plitting functions

        Kwargs are used to replace values by custom parameters:

        Example for using a custom markersize::

            p = MatplotlibPlotter()
            p.add_parameter('marker_custom', default_from='marker')
            p.plot_kwargs(marker='marker_custom')

        This code snippet will return the standard parameters for a plot, but the value
        for the marker will be taken from the key `marker_custom`
        """
        if plot_type == 'default':
            kwargs_keys = self._PLOT_KWARGS
        elif plot_type == 'colormesh':
            kwargs_keys = self._PLOT_KWARGS_COLORMESH
        elif plot_type == 'histogram':
            kwargs_keys = self._PLOT_KWARGS_HIST

        if self.single_plot:
            any_area = self['area_plot']
        else:
            any_area = any(self[('area_plot', indx)] for indx in range(self.num_plots))

        if any_area:
            kwargs_keys = kwargs_keys | self._PLOT_KWARGS_AREA

        if extra_keys is not None:
            kwargs_keys = kwargs_keys | extra_keys

        #Insert custom keys to retrieve
        kwargs_keys = kwargs_keys.copy()
        for key, replace_key in kwargs.items():
            kwargs_keys.remove(key)
            kwargs_keys.add(replace_key)

        plot_kwargs = self.get_multiple_kwargs(kwargs_keys, ignore=ignore)

        #Rename replaced keys back to standard names
        for key, replace_key in kwargs.items():
            custom_val = plot_kwargs.pop(replace_key)
            plot_kwargs[key] = custom_val

        if not post_process:
            return plot_kwargs

        if 'plot_label' in plot_kwargs:
            plot_kwargs['label'] = plot_kwargs.pop('plot_label')

        if 'plot_alpha' in plot_kwargs:
            plot_kwargs['alpha'] = plot_kwargs.pop('plot_alpha')

        if 'cmap' in plot_kwargs and self['sub_colormap'] is not None:
            if not isinstance(self['sub_colormap'], (tuple, list)):
                raise ValueError('sub_colormap has to be a tuple of two numbers')

            if isinstance(plot_kwargs['cmap'], list):
                for indx, cmap in enumerate(plot_kwargs['cmap']):
                    if isinstance(cmap, str):
                        cmap = plt.get_cmap(cmap)

                    if isinstance(self['sub_colormap'], list):
                        limits = self['sub_colormap'][indx]
                    else:
                        limits = self['sub_colormap']

                    plot_kwargs['cmap'][indx] = self.truncate_colormap(cmap, *limits)
            else:
                if isinstance(plot_kwargs['cmap'], str):
                    plot_kwargs['cmap'] = plt.get_cmap(plot_kwargs['cmap'])

                plot_kwargs['cmap'] = self.truncate_colormap(plot_kwargs['cmap'], *self['sub_colormap'])

        plot_kwargs = self.dict_of_lists_to_list_of_dicts(plot_kwargs, self.single_plot, self.num_plots)

        if not self.single_plot:
            for index, value in enumerate(plot_kwargs):
                if self[('area_plot', index)]:
                    value.pop('marker', None)
                    value.pop('markersize', None)
                    value['alpha'] = value.pop('area_alpha')
                else:
                    value.pop('area_alpha', None)
                    value.pop('area_linecolor', None)
        else:
            if self['area_plot']:
                plot_kwargs.pop('marker', None)
                plot_kwargs.pop('markersize', None)
                plot_kwargs['alpha'] = plot_kwargs.pop('area_alpha')
            else:
                plot_kwargs.pop('area_alpha', None)
                plot_kwargs.pop('area_linecolor', None)

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

        :returns: the created or modified axis object
        """
        from cycler import cycler, Cycler

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

        if self['color_cycle'] is not None:
            if isinstance(self['color_cycle'], str):
                ax.set_prop_cycle(cycler(color=plt.get_cmap(self['color_cycle']).colors))
            elif isinstance(self['color_cycle'], Cycler):
                ax.set_prop_cycle(self['color_cycle'])
            else:
                ax.set_prop_cycle(cycler(color=self['color_cycle']))

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

    def show_legend(self, ax, leg_elems=None):
        """
        Print a legend for the plot

        :param ax: Axes object on which to perform the operation
        """
        if leg_elems is None:
            leg_elems = ()

        if self['legend']:
            loptions = copy.deepcopy(self['legend_options'])
            linewidth = loptions.pop('linewidth', 1.5)
            title_font_size = loptions.pop('fontsize', 15)
            leg = ax.legend(*leg_elems, **loptions)
            leg.get_frame().set_linewidth(linewidth)
            leg.get_title().set_fontsize(title_font_size)  #legend 'Title' fontsize

    def show_colorbar(self, ax):
        """
        Print a colorbar for the plot

        :param ax: Axes object on which to perform the operation
        """

        if self['colorbar']:
            if isinstance(self['cmap'], list):
                raise ValueError('show_colorbar only available for single colormaps')
            mappable = cm.ScalarMappable(cmap=self['cmap'], norm=self['norm'])
            if self['limits'] is not None:
                if 'color' in self['limits']:
                    cmin = self['limits']['color'][0]
                    cmax = self['limits']['color'][1]
                    mappable.set_clim(cmin, cmax)

            plt.colorbar(mappable, ax=ax, pad=self['colorbar_padding'])

    @staticmethod
    def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=256):
        """
        Cut off parts of colormap

        :param cmap: cmap to truncate
        :param minval: minimum value of new colormap
        :param maxval: maximum value of new colormap
        :param n: number of colors in new colormap

        :returns: colormap truncated to only hold colors between minval and maxval from old colormap
        """
        import matplotlib.colors as colors
        import numpy as np

        new_cmap = colors.LinearSegmentedColormap.from_list(
            'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval), cmap(np.linspace(minval, maxval, n)))

        return new_cmap

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
