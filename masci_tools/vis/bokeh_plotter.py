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
Here are all plot varaiables/constants,

"""
from masci_tools.vis import Plotter
import copy


class BokehPlotter(Plotter):

    _BOKEH_DEFAULTS = {
        'figure_kwargs': {
            'tools': 'hover',
            'y_axis_type': 'linear',
            'x_axis_type': 'linear',
            'toolbar_location': None,
            'tooltips': [('X value', '@x'), ('Y value', '@y')]
        },
        'axis_linewidth': 2,
        'label_fontsize': '18pt',
        'tick_label_fontsize': '16pt',
        'background_fill_color': '#ffffff',

        #legend options
        'legend_location': 'top_right',
        'legend_click_policy': 'hide',  # "mute"#"hide"
        'legend_orientation': 'vertical',
        'legend_font_size': '14pt',

        #plot parameters
        'color_palette': None,
        'color': None,
        'legend_label': None,
        'alpha': 1.0,
        'name': None,
        'line_color': None,
        'line_alpha': 1.0,
        'line_dash': None,
        'line_width': 2.0,
        'marker': 'circle',
        'marker_size': 6,
        'area_plot': False,
        'area_vertical': False,
        'fill_alpha': 1.0,
        'fill_color': None,
        'straight_lines': None,
        'straight_line_options': {
            'line_color': 'black',
            'line_width': 1.0,
            'line_dash': 'dashed'
        },

        #output control
        'show': True,
    }

    _BOKEH_GENERAL_ARGS = {
        'show',
        'colormap',
        'legend_location',
        'legend_click_policy',
        'legend_font_size',
        'legend_orientation',
        'background_fill_color',
        'tick_label_fontsize',
        'label_fontsize',
        'axis_linewidth',
        'figure_kwargs',
        'straight_lines',
    }

    _PLOT_KWARGS = {'color', 'alpha', 'legend_label', 'name'}
    _PLOT_KWARGS_LINE = {'line_color', 'line_alpha', 'line_dash', 'line_width'}
    _PLOT_KWARGS_SCATTER = {'marker', 'marker_size'}
    _PLOT_KWARGS_AREA = {'fill_alpha', 'fill_color'}

    def __init__(self, **kwargs):

        super().__init__(self._BOKEH_DEFAULTS, general_keys=self._BOKEH_GENERAL_ARGS, **kwargs)

    def plot_kwargs(self, ignore=None, extra_keys=None, **kwargs):
        """
        Creates a dict or list of dicts (for multiple plots) with the defined parameters
        for the plotting calls fo matplotlib

        :param ignore: str or list of str (optional), defines keys to ignore in the creation of the dict
        :param extra_keys: optional set for addtional keys to retrieve

        Kwargs are used to replace values by custom parameters:

        Example for using a custom markersize::

            p = MatplotlibPlotter()
            p.add_parameter('marker_custom', default_from='marker')
            p.plot_kwargs(marker='marker_custom')

        This code snippet will return the standard parameters for a plot, but the value
        for the marker will be taken from the key `marker_custom`
        """
        if self.plot_type == 'default':
            kwargs_keys = self._PLOT_KWARGS
        elif self.plot_type == 'line':
            kwargs_keys = self._PLOT_KWARGS | self._PLOT_KWARGS_LINE
        elif self.plot_type == 'scatter':
            kwargs_keys = self._PLOT_KWARGS | self._PLOT_KWARGS_SCATTER
        elif self.plot_type == 'area':
            kwargs_keys = self._PLOT_KWARGS | self._PLOT_KWARGS_AREA

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

        if 'marker_size' in plot_kwargs:
            plot_kwargs['size'] = plot_kwargs.pop('marker_size')

        plot_kwargs = self.dict_of_lists_to_list_of_dicts(plot_kwargs, self.single_plot, self.num_plots)

        return plot_kwargs

    def prepare_figure(self, title, xlabel, ylabel, figure=None):
        from bokeh.plotting import figure as bokeh_fig
        from bokeh.models import Title

        if figure is None:
            p = bokeh_fig(**self['figure_kwargs'])
        else:
            p = figure
            if self['background_fill_color'] is not None:
                p.background_fill_color = self['background_fill_color']

        if title is not None:
            p.title = Title(text=title)
        if xlabel is not None:
            p.xaxis.axis_label = xlabel
        if ylabel is not None:
            p.yaxis.axis_label = ylabel

        p.yaxis.axis_line_width = self['axis_linewidth']
        p.xaxis.axis_line_width = self['axis_linewidth']
        p.xaxis.axis_label_text_font_size = self['label_fontsize']
        p.yaxis.axis_label_text_font_size = self['label_fontsize']
        p.yaxis.major_label_text_font_size = self['tick_label_fontsize']
        p.xaxis.major_label_text_font_size = self['tick_label_fontsize']

        return p

    def set_color_palette_by_num_plots(self):
        """
        Set the colormap for the configured number of plots according to the set colormap or color

        copied from https://github.com/PatrikHlobil/Pandas-Bokeh/blob/master/pandas_bokeh/plot.py
        credits to PatrikHlobil
        modified for use in this Plotter class
        """
        from bokeh.palettes import all_palettes

        if self['color'] is not None:
            color = self['color']
            if not isinstance(self['color'], (list, tuple)):
                color = [color]

            color = color * int(self.num_plots / len(color) + 1)
            color = color[:self.num_plots]
        elif self['color_palette'] is not None:
            if self['color_palette'] in all_palettes:
                color = all_palettes[self['color_palette']]
                max_key = max(color.keys())
                if self.num_plots <= max_key:
                    color = color[self.num_plots]
                else:
                    color = color[max_key]
                    color = color * int(self.num_plots / len(color) + 1)
                    color = color[:self.num_plots]
            else:
                raise ValueError(
                    'Could not find <colormap> with name %s. The following predefined colormaps are '
                    'supported (see also https://bokeh.pydata.org/en/latest/docs/reference/palettes.html ): %s' %
                    (self['colormap'], list(all_palettes.keys())))
        else:
            if self.num_plots <= 10:
                color = all_palettes['Category10'][10][:self.num_plots]
            elif self.num_plots <= 20:
                color = all_palettes['Category20'][self.num_plots]
            else:
                color = all_palettes['Category20'][20] * int(self.num_plots / 20 + 1)
                color = color[:self.num_plots]

        self['color'] = color

    def draw_straight_lines(self, fig):
        """
        Draw horizontal and vertical lines specified in the lines argument

        :param ax: Axes object on which to perform the operation
        """
        from bokeh.models import Span

        if self['straight_lines'] is not None:
            added_lines = []
            if 'horizontal' in self['straight_lines']:
                lines = copy.deepcopy(self['straight_lines']['horizontal'])
                if not isinstance(lines, list):
                    lines = [lines]

                for line_def in lines:
                    options = copy.deepcopy(self['straight_line_options'])
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
                        added_lines.append(Span(location=pos, dimension='width', **options))
            if 'vertical' in self['straight_lines']:
                lines = copy.deepcopy(self['straight_lines']['vertical'])
                if not isinstance(lines, list):
                    lines = [lines]

                for line_def in lines:
                    options = copy.deepcopy(self['straight_line_options'])
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
                        added_lines.append(Span(location=pos, dimension='height', **options))
            fig.renderers.extend(added_lines)

    def set_legend(self, fig):

        fig.legend.location = self['legend_location']
        fig.legend.background_fill_color = self['background_fill_color']
        fig.legend.click_policy = self['legend_click_policy']
        fig.legend.orientation = self['legend_orientation']
        fig.legend.label_text_font_size = self['legend_font_size']

    def save_plot(self, figure):
        from bokeh.io import show as bokeh_show
        if self['show']:
            bokeh_show(figure)
