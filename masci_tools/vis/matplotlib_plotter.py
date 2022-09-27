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
This module contains a subclass of :py:class:`~masci_tools.vis.parameters.Plotter` for the matplotlib library
"""
from .parameters import Plotter, _generate_plot_parameters_table
import matplotlib.pyplot as plt
from matplotlib import cm
import copy


class MatplotlibPlotter(Plotter):
    """
    Class for plotting parameters and standard code snippets for plotting with the
    matplotlib backend.

    Kwargs in the __init__ method are forwarded to setting default values for the instance

    For specific documentation about the parameter/defaults handling refer to
    :py:class:`~masci_tools.vis.parameters.Plotter`.

    Below the current defined default values are shown:

    """
    _MATPLOTLIB_DEFAULTS = {
        # figure properties
        'title_fontsize': 16,
        'figure_kwargs': {
            'figsize': (8, 6),
            'dpi': 100,
            'facecolor': 'w',
            'edgecolor': 'k',
            'constrained_layout': True,
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
        'invert_xaxis': False,
        'invert_yaxis': False,
        'color_cycle': None,
        'color_cycle_always_advance': False,
        'sub_colormap': None,

        # plot properties
        'linewidth': 2.0,
        'linestyle': '-',
        'marker': 'o',
        'markersize': 4.0,
        'color': None,
        'zorder': None,
        'repeat_parameters': None,
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
        'colorbar_options': {
            'pad': 0.05
        },
        # legend properties
        'legend': False,
        'legend_show_data_labels': False,
        'legend_remove_duplicates': False,
        'legend_options': {
            'fontsize': 'large',
            'linewidth': 3.0,
            'loc': 'best',
            'fancybox': True
        },

        # save all plots?
        'save_plots': False,  # True
        'save_format': 'png',  #'pdf'
        'save_options': {
            'transparent': True
        },
        'tightlayout': False,
        'show': True,
        # write data to file
        'save_raw_plot_data': False,
        'raw_plot_data_format': 'txt'
    }

    _MATPLOTLIB_DESCRIPTIONS = {
        # figure properties
        'title_fontsize':
        'Fontsize for the title of the figure',
        'figure_kwargs':
        'Arguments passed to `plt.figure` when creating the figure. '
        'Includes things like figsize, dpi, background color, ...',

        # axis properties
        'alpha':
        'Float specifying the transparency of the title',
        'axis_linewidth':
        'Linewidth of the lines for the axis',
        'use_axis_formatter':
        'If True the labels will always not be formatted '
        'with an additive constant at the top',
        'set_powerlimits':
        'If True the threshold for switching to scientific notation is adjusted to 0,3',
        'xticks':
        'Positions of the ticks on the x axis',
        'xticklabels':
        'Labels for the ticks on the x-axis',
        'yticks':
        'Positions for the ticks on the y-axis',
        'yticklabels':
        'Labels for the ticks on the y-axis',
        'invert_xaxis':
        'If True the direction of the x-axis is inverted',
        'invert_yaxis':
        'If True the direction of the y-axis is inverted',
        'color_cycle':
        'If set this will override the default color cycle of matplotlib. '
        'Can be given as name of a colormap cycle or list of colors',
        'color_cycle_always_advance':
        'Always advance the color cycle even if the color was specified',
        'sub_colormap':
        'If a colormap is used this can be used to cut out a part of the colormap. '
        'For example (0.5,1.0) will only use the upper half of the colormap',

        # plot properties
        'linewidth':
        'Linewidth for the plot(s)',
        'linestyle':
        'Linestyle for the plot(s)',
        'marker':
        'Shape of the marker to use for the plot(s)',
        'markersize':
        'Size of the markers to use in the plot(s)',
        'color':
        'Color to use in the plot(s)',
        'zorder':
        'z-position to use for the plot(s) (Is used to define fore- and background)',
        'repeat_parameters':
        'If set as integer the parameters for single plots (except labels) will be repeated after the given number of plots. '
        'Only implemented for multiple_scatterplots',
        'edgecolor':
        'Edgecolor to use in the plot(s)',
        'facecolor':
        'Facecolor to use in the plot(s)',
        'plot_label':
        'Label to use in the plot(s) for the legend',
        'area_plot':
        'If True fill_between(x) will be used to produce the plot(s)',
        'area_vertical':
        'Determines, whether to use fill_between or fill_betweenx for area plots',
        'area_enclosing_line':
        'If True a enclosing line will be drawn around the area',
        'area_alpha':
        'Transparency to use for the area in the area plot(s)',
        'area_linecolor':
        'Color for the enclosing line in the area plot(s)',
        'plot_alpha':
        'Transparency to use for the plot(s)',
        'cmap':
        'Colormap to use for scatter/pcolormesh or 3D plots',
        'norm':
        'If set this norm will be used to normalize data for the colormapping',
        'shading':
        'Shading to use for pcolormesh plots',
        'rasterized':
        'Rasterize the pcolormesh when drawing vector graphics.',

        #scale and limits placeholder
        'scale':
        "Dict specifying the scales of the axis, e.g {'y': 'log'}"
        'will create a logarithmic scale on the y-axis',
        'limits':
        "Dict specifying the limits of the axis, e.g {'x': (-5,5)}",

        # x, y label
        'labelfontsize':
        'Fontsize for the labels on the axis',
        'lines':
        'Dict specifying straight help-lines to draw. '
        "For example {'vertical': 0, 'horizontal': [-1,1]} will draw a vertical line at 0 "
        'and two horizontal at -1 and 1',
        'line_options':
        'Color, width, and more options for the help-lines',
        'font_options':
        'Default font options that can be used for text annotations',

        # ticks
        'tick_paramsx':
        'Parameters for major ticks on the x-axis (Size, fontsize, ...)',
        'tick_paramsy':
        'Parameters for major ticks on the y-axis (Size, fontsize, ...)',
        'tick_paramsx_minor':
        'Parameters for minor ticks on the x-axis (Size, fontsize, ...)',
        'tick_paramsy_minor':
        'Parameters for minor ticks on the y-axis (Size, fontsize, ...)',
        'colorbar':
        'If True and the function implements color mapping, a colorbar is shown',
        'colorbar_options':
        'Parameters for displaying the colorbar (Fontsize, ...)',
        # legend properties
        'legend':
        'If True a legend for the plot is shown',
        'legend_show_data_labels':
        'If True the column names from the data argument are shown if not overwritten',
        'legend_remove_duplicates':
        'If True duplicate legend labels are removed',
        'legend_options':
        'Parameters for displaying the legend (Fontsize, location, ...)',

        # save all plots?
        'save_plots':
        'if True the plots will be saved to file',
        'save_format':
        'Formats to save the plots to, can be single or list of formats',
        'save_options':
        'Additional options for saving the plots to file',
        'tightlayout':
        'If True the tight layout will be used (NOT IMPLEMENTED)',
        'show':
        'If True plt.show will be called at the end of the routine',
        # write data to file
        'save_raw_plot_data':
        'If True the data for the plot is saved to file (NOT IMPLEMENTED)',
        'raw_plot_data_format':
        'Format in which to save the data for the plot (NOT IMPLEMENTED)'
    }

    _MATPLOTLIB_GENERAL_ARGS = {
        'save_plots', 'save_format', 'tightlayout', 'save_raw_plot_data', 'raw_plot_data_format', 'show', 'legend',
        'legend_options', 'colorbar', 'colorbar_options', 'tick_paramsy', 'tick_paramsx', 'tick_paramsy_minor',
        'tick_paramsx_minor', 'font_options', 'line_options', 'labelfontsize', 'lines', 'scale', 'limits', 'xticks',
        'xticklabels', 'yticks', 'yticklabels', 'figure_kwargs', 'title_font_size', 'repeat_colors_after',
        'color_cycle', 'color_cycle_always_advance'
        'sub_colormap', 'save_options'
    }

    _TYPE_TO_KWARGS = {
        'default': {'linewidth', 'linestyle', 'marker', 'markersize', 'color', 'plot_label', 'plot_alpha', 'zorder'},
        'colormap_scatter': {
            'linewidth', 'linestyle', 'marker', 'markersize', 'color', 'plot_label', 'plot_alpha', 'zorder', 'cmap',
            'norm'
        },
        'area': {'area_linecolor', 'area_alpha', 'zorder'},
        'colormesh': {
            'linewidth', 'linestyle', 'shading', 'rasterized', 'cmap', 'norm', 'edgecolor', 'facecolor', 'plot_label',
            'plot_alpha', 'zorder'
        },
        'histogram':
        {'linewidth', 'linestyle', 'color', 'plot_label', 'plot_alpha', 'edgecolor', 'facecolor', 'zorder'},
    }

    _POSTPROCESS_RENAMES = {'plot_label': 'label', 'plot_alpha': 'alpha'}

    __doc__ = __doc__ + _generate_plot_parameters_table(_MATPLOTLIB_DEFAULTS, _MATPLOTLIB_DESCRIPTIONS)

    def __init__(self, **kwargs):
        super().__init__(self._MATPLOTLIB_DEFAULTS,
                         general_keys=self._MATPLOTLIB_GENERAL_ARGS,
                         key_descriptions=self._MATPLOTLIB_DESCRIPTIONS,
                         type_kwargs_mapping=self._TYPE_TO_KWARGS,
                         kwargs_postprocess_rename=self._POSTPROCESS_RENAMES,
                         **kwargs)

    def plot_kwargs(self,
                    plot_type='default',
                    ignore=None,
                    extra_keys=None,
                    post_process=True,
                    list_of_dicts=True,
                    **kwargs):
        """
        Creates a dict or list of dicts (for multiple plots) with the defined parameters
        for the plotting calls of matplotlib

        :param ignore: str or list of str (optional), defines keys to ignore in the creation of the dict
        :param extra_keys: optional set for additional keys to retrieve
        :param post_process: bool, if True the parameters are cleaned up for inserting them directly into matplotlib plitting functions

        Kwargs are used to replace values by custom parameters:

        Example for using a custom markersize::

            p = MatplotlibPlotter()
            p.add_parameter('marker_custom', default_from='marker')
            p.plot_kwargs(marker='marker_custom')

        This code snippet will return the standard parameters for a plot, but the value
        for the marker will be taken from the key `marker_custom`
        """
        if self.single_plot:
            any_area = self['area_plot']
        else:
            any_area = any(self[('area_plot', indx)] for indx in range(self.num_plots))

        if any_area:
            area_kwargs = self._type_kwargs_mapping['area']
            extra_keys = extra_keys | area_kwargs if extra_keys is not None else area_kwargs

        #list of dicts is done later
        plot_kwargs = super().plot_kwargs(plot_type=plot_type,
                                          ignore=ignore,
                                          extra_keys=extra_keys,
                                          post_process=post_process,
                                          list_of_dicts=False,
                                          **kwargs)

        if not post_process:
            return plot_kwargs

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

        if self['limits'] is not None and 'color' in self['limits'] and 'cmap' in plot_kwargs:
            if 'norm' not in plot_kwargs:
                plot_kwargs['vmin'], plot_kwargs['vmax'] = self['limits']['color']

        if list_of_dicts:
            plot_kwargs = self.dict_of_lists_to_list_of_dicts(plot_kwargs,
                                                              self.single_plot,
                                                              self.num_plots,
                                                              repeat_after=self['repeat_parameters'],
                                                              ignore_repeat={'plot_label'})

        if not list_of_dicts and 'label' in plot_kwargs:
            label = plot_kwargs.pop('label')
            if isinstance(label, list):
                plot_kwargs['label'] = [value if value is not None else '' for value in label]
            else:
                plot_kwargs['label'] = label if label is not None else ''

        if not self.single_plot and list_of_dicts:
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

        if self['legend_show_data_labels']:
            if not self.single_plot and list_of_dicts:
                for index, value in enumerate(plot_kwargs):
                    if value.get('label') is None:
                        value.pop('label', None)
            elif plot_kwargs.get('label') is None:
                plot_kwargs.pop('label', None)
        else:
            if not self.single_plot and list_of_dicts:
                for index, value in enumerate(plot_kwargs):
                    if 'label' not in value:
                        value['label'] = None
            elif 'label' not in plot_kwargs:
                plot_kwargs['label'] = None

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

        if self['invert_xaxis']:
            ax.invert_xaxis()

        if self['invert_yaxis']:
            ax.invert_yaxis()

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
                if self['invert_xaxis']:
                    ax.set_xlim(xmax, xmin)
                else:
                    ax.set_xlim(xmin, xmax)
            if 'y' in self['limits']:
                ymin = self['limits']['y'][0]
                ymax = self['limits']['y'][1]
                if self['invert_yaxis']:
                    ax.set_ylim(ymax, ymin)
                else:
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
            if self['legend_remove_duplicates']:
                leg_elems = ax.get_legend_handles_labels()
                by_label = dict(zip(*reversed(leg_elems)))
                leg_elems = (by_label.values(), by_label.keys())
            else:
                leg_elems = ()

        if self['legend']:
            loptions = copy.deepcopy(self['legend_options'])
            linewidth = loptions.pop('linewidth', 1.5)
            title_font_size = loptions.get('fontsize', 15)
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
                cmaps = self['cmap']
            else:
                cmaps = [self['cmap']]
            bar_ax = None
            cmin = cmax = None
            if self['limits'] is not None and 'color' in self['limits']:
                cmin, cmax = self['limits']['color']

            coptions = copy.deepcopy(self['colorbar_options'])
            labelsize = coptions.pop('labelsize', None)
            label = coptions.pop('label', '')
            pad = coptions.pop('padding', 0.05)

            for indx, cmap in enumerate(cmaps):
                mappable = cm.ScalarMappable(cmap=cmap, norm=self['norm'])
                if cmin is not None:
                    mappable.set_clim(cmin, cmax)

                cax = ax.inset_axes([1.0 + (pad + 0.01) * (indx + 1), 0, pad, 1], transform=ax.transAxes)
                cbar = plt.colorbar(mappable, cax=cax, **coptions)

                if indx < len(cmaps) - 1:
                    cbar.ax.tick_params(labelsize=0)
                elif labelsize is not None:
                    cbar.ax.tick_params(labelsize=labelsize)

            cbar.set_label(label)

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
        from matplotlib import colors
        import numpy as np

        new_cmap = colors.LinearSegmentedColormap.from_list(f'trunc({cmap.name},{minval:.2f},{maxval:.2f})',
                                                            cmap(np.linspace(minval, maxval, n)))

        return new_cmap

    def save_plot(self, saveas):
        """
        Save the current figure or show the current figure

        :param saveas: str, filename for the resulting file
        """
        if self['save_plots']:
            if isinstance(self['save_format'], list):
                formats = self['save_format']
            else:
                formats = [self['save_format']]

            for save_format in formats:
                savefilename = f'{saveas}.{save_format}'
                print(f'Save plot to: {savefilename}')
                plt.savefig(savefilename, format=save_format, **self['save_options'])
        if self['show']:
            plt.show()
