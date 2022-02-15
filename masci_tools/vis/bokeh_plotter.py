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
Here the :py:class:`masci_tools.vis.parameters.Plotter` subclass for the bokeh plotting backend
is defined with default values and many helper methods
"""
from .parameters import Plotter, _generate_plot_parameters_table
import copy


class BokehPlotter(Plotter):
    """
    Class for plotting parameters and standard code snippets for plotting with the
    bokeh backend.

    Kwargs in the __init__ method are forwarded to setting default values for the instance

    For specific documentation about the parameter/defaults handling refer to
    :py:class:`~masci_tools.vis.parameters.Plotter`.

    Below the current defined default values are shown:

    """
    _BOKEH_DEFAULTS = {
        'figure_kwargs': {
            'tools': 'pan,poly_select,tap,wheel_zoom,'
            'box_zoom,redo,undo,reset,save,crosshair,zoom_out,zoom_in',
            'y_axis_type': 'linear',
            'x_axis_type': 'linear',
            'active_inspect': None,
            'toolbar_location': 'right',
        },
        'additional_tools': None,
        'show_tooltips': True,
        'global_tooltips': False,
        'format_tooltips': True,
        'tooltips': [('X', '@{x}'), ('Y', '@{y}')],
        'additional_tooltips': None,
        'axis_linewidth': 2,
        'label_fontsize': '18pt',
        'tick_label_fontsize': '16pt',
        'background_fill_color': '#ffffff',
        'x_axis_formatter': None,
        'y_axis_formatter': None,
        'x_ticks': None,
        'x_ticklabels_overwrite': None,
        'y_ticks': None,
        'y_ticklabels_overwrite': None,
        'x_range_padding': None,
        'y_range_padding': None,
        'limits': None,

        #legend options
        'legend_location': 'top_right',
        'legend_click_policy': 'hide',  # "mute"#"hide"
        'legend_orientation': 'vertical',
        'legend_font_size': '14pt',
        'legend_outside_plot_area': False,

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
        'level': None,
        'straight_lines': None,
        'straight_line_options': {
            'line_color': 'black',
            'line_width': 1.0,
            'line_dash': 'dashed'
        },

        #output control
        'save_plots': False,
        'save_format': 'html',
        'show': True,
    }

    _BOKEH_DESCRIPTIONS = {
        'figure_kwargs':
        'Parameters for creating the bokeh figure. '
        'Includes things like axis type (x and y), tools '
        'plot width/height',
        'additional_tools':
        'tools to add to the tools already '
        'specified in ``figure_kwargs`` (Has to be in the same format)',
        'show_tooltips':
        'Switch whether to add hover tooltips',
        'global_tooltips':
        'Switch whether to add individual (for each renderer) or global hover tooltips. ',
        'format_tooltips':
        'Switch whether to enable the processing of formatted strings in tooltips. ',
        'tooltips':
        'List of tuples specifying the tooltips. '
        'For more information refer to the bokeh documentation. '
        "Strings can contain format specifiers with the data keys of the function e.g. ``'@{x}'``. "
        'Here the ``{x}`` will be replaced by the entry for x. If there are formatting specifications '
        'for bokeh they need to be escaped with double curly braces or ``format_tooltips=False``.',
        'additional_tooltips':
        'Tooltips to add to the already defined ``tooltips`` (See above)',
        'axis_linewidth':
        'Linewidth for the lines of the axis',
        'label_fontsize':
        'Fontsize for the labels of the axis',
        'tick_label_fontsize':
        'fontsize for the ticks on the axis',
        'background_fill_color':
        'Color of the background of the plot',
        'x_axis_formatter':
        'If set this formatter will be used for the ticks on the x-axis',
        'y_axis_formatter':
        'If set this formatter will be used for the ticks on the y-axis',
        'x_ticks':
        'Tick specification for the x-axis',
        'x_ticklabels_overwrite':
        'Overrides the labels for the ticks on the x-axis',
        'y_ticks':
        'Tick specification for the y-axis',
        'y_ticklabels_overwrite':
        'Overrides the labels for the ticks on the y-axis',
        'x_range_padding':
        'Specifies the amount of padding on the edges of the x-axis',
        'y_range_padding':
        'Specifies the amount of padding on the edges of the y-axis',
        'limits':
        "Dict specifying the limits of the axis, e.g {'x': (-5,5)}",

        #legend options
        'legend_location':
        'Location of the legend inside the plot area',
        'legend_click_policy':
        'Policy for what happens when labels are clicked in the legend',
        'legend_orientation':
        'Orientation of the legend',
        'legend_font_size':
        'Fontsize for the labels inside the legend',
        'legend_outside_plot_area':
        'If True the legend will be placed outside of the plot area',

        #plot parameters
        'color_palette':
        'Color palette to use for the plot(s)',
        'color':
        'Specific colors to use for the plot(s)',
        'legend_label':
        'Labels to use for the legend of the plot(s)',
        'alpha':
        'Transparency to use for the plot(s)',
        'name':
        'Name used for identifying elements in the plot (not shown only internally)',
        'line_color':
        'Color to use for line plot(s)',
        'line_alpha':
        'Transparency to use for line plot(s)',
        'line_dash':
        'Dash styles to use for line plot(s)',
        'line_width':
        'Line width to use for line plot(s)',
        'marker':
        'Type of marker to use for scatter plot(s)',
        'marker_size':
        'Marker size to use for scatter plot(s)',
        'area_plot':
        'If True h(v)area will be used to produce the plot(s)',
        'area_vertical':
        'Determines, whether to use harea (False) or varea (True) for area plots',
        'fill_alpha':
        'Transparency to use for the area in area plot(s)',
        'fill_color':
        'Color to use for the area in area plot(s)',
        'level':
        'Can be used to specified, which elements are fore- or background',
        'straight_lines':
        'Dict specifying straight help-lines to draw. '
        "For example {'vertical': 0, 'horizontal': [-1,1]} will draw a vertical line at 0 "
        'and two horizontal at -1 and 1',
        'straight_line_options':
        'Color, width, and more options for the help-lines',

        #output control
        'save_plots':
        'If True plots will be saved to file (Configuration beforehand is needed)',
        'save_format':
        'Formats to save the plots to, can be single or list of formats (html, png or svg)',
        'show':
        'If True bokeh.io.show will be called after the plotting routine',
    }

    _BOKEH_GENERAL_ARGS = {
        'show',
        'save_plots',
        'save_format',
        'color_palette',
        'legend_location',
        'legend_click_policy',
        'legend_font_size',
        'legend_orientation',
        'legend_outside_plot_area',
        'background_fill_color',
        'tick_label_fontsize',
        'label_fontsize',
        'axis_linewidth',
        'figure_kwargs',
        'additional_tools',
        'show_tooltips',
        'global_tooltips',
        'format_tooltips',
        'tooltips',
        'additional_tooltips',
        'straight_lines',
        'x_axis_formatter',
        'y_axis_formatter',
        'x_ticks',
        'y_ticks',
        'y_ticklabels_overwrite',
        'x_ticklabels_overwrite',
        'x_range_padding',
        'y_range_padding',
    }

    _PLOT_KWARGS = {'color', 'alpha', 'legend_label', 'name'}
    _PLOT_KWARGS_LINE = {'line_color', 'line_alpha', 'line_dash', 'line_width'}
    _PLOT_KWARGS_SCATTER = {'marker', 'marker_size', 'fill_alpha', 'fill_color'}
    _PLOT_KWARGS_AREA = {'fill_alpha', 'fill_color'}
    _PLOT_KWARGS_IMAGE = {'color', 'alpha', 'color_palette'}

    __doc__ = __doc__ + _generate_plot_parameters_table(_BOKEH_DEFAULTS, _BOKEH_DESCRIPTIONS)

    def __init__(self, **kwargs):

        super().__init__(self._BOKEH_DEFAULTS,
                         general_keys=self._BOKEH_GENERAL_ARGS,
                         key_descriptions=self._BOKEH_DESCRIPTIONS,
                         **kwargs)

    def plot_kwargs(self,
                    ignore=None,
                    extra_keys=None,
                    plot_type='default',
                    post_process=True,
                    list_of_dicts=True,
                    **kwargs):
        """
        Creates a dict or list of dicts (for multiple plots) with the defined parameters
        for the plotting calls of matplotlib

        :param ignore: str or list of str (optional), defines keys to ignore in the creation of the dict
        :param extra_keys: optional set for additional keys to retrieve
        :param post_process: bool, if True the parameters are cleaned up for inserting them directly into bokeh plotting functions

        Kwargs are used to replace values by custom parameters:

        Example for using a custom markersize::

            p = BokehPlotter()
            p.add_parameter('marker_custom', default_from='marker')
            p.plot_kwargs(marker='marker_custom')

        This code snippet will return the standard parameters for a plot, but the value
        for the marker will be taken from the key `marker_custom`
        """
        if plot_type == 'default':
            kwargs_keys = self._PLOT_KWARGS
        elif plot_type == 'line':
            kwargs_keys = self._PLOT_KWARGS | self._PLOT_KWARGS_LINE
        elif plot_type == 'scatter':
            kwargs_keys = self._PLOT_KWARGS | self._PLOT_KWARGS_SCATTER
        elif plot_type == 'area':
            kwargs_keys = self._PLOT_KWARGS | self._PLOT_KWARGS_AREA
        elif plot_type == 'image':
            kwargs_keys = self._PLOT_KWARGS | self._PLOT_KWARGS_IMAGE

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
            custom_val = plot_kwargs.pop(replace_key, None)
            if custom_val is not None:
                plot_kwargs[key] = custom_val

        if not post_process:
            return plot_kwargs

        if 'marker_size' in plot_kwargs:
            plot_kwargs['size'] = plot_kwargs.pop('marker_size')

        if 'color_palette' in plot_kwargs:
            plot_kwargs['palette'] = plot_kwargs.pop('color_palette')

        if list_of_dicts:
            plot_kwargs = self.dict_of_lists_to_list_of_dicts(plot_kwargs, self.single_plot, self.num_plots)

        return plot_kwargs

    def prepare_figure(self, title, xlabel, ylabel, figure=None):
        """
        Create a bokeh figure according to the set parameters or modify an existing one

        :param title: title of the figure
        :param xlabel: label on the x-axis
        :param ylabel: label on the y-axis
        :param figure: bokeh figure, optional, if given the operations are performed on the object
                       otherwise a new figure is created

        :returns: the created or modified bokeh figure
        """
        from bokeh.plotting import figure as bokeh_fig
        from bokeh.models import Title

        if self['additional_tools'] is not None:
            if isinstance(self['additional_tools'], str):
                default = ''
            else:
                default = []
            tools = self['figure_kwargs'].get('tools', default)
            if isinstance(tools, list):
                if not isinstance(self['additional_tools'], list):
                    raise ValueError('Got tools and additional_tools in different formats.'
                                     'Expected list for additional_tools')
                tools = tools + self['additional_tools']
            else:
                if not isinstance(self['additional_tools'], str):
                    raise ValueError('Got tools and additional_tools in different formats.'
                                     'Expected string for additional_tools')
                tools = f"{tools},{self['additional_tools']}"

            figure_kwargs = {**self['figure_kwargs'], **{'tools': tools}}
        else:
            figure_kwargs = self['figure_kwargs']

        if figure is None:
            p = bokeh_fig(**figure_kwargs)
        else:
            p = figure
            if self['background_fill_color'] is not None:
                p.background_fill_color = self['background_fill_color']

        if self['global_tooltips']:
            self.add_tooltips(p, 'auto', toggleable=True)

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

        if self['y_axis_formatter'] is not None:
            p.yaxis.formatter = self['y_axis_formatter']
        if self['x_axis_formatter'] is not None:
            p.xaxis.formatter = self['x_axis_formatter']

        if self['x_ticks'] is not None:
            p.xaxis.ticker = self['x_ticks']
        if self['y_ticks'] is not None:
            p.xaxis.ticker = self['y_ticks']

        if self['x_ticklabels_overwrite'] is not None:
            p.xaxis.major_label_overrides = self['x_ticklabels_overwrite']

        if self['y_ticklabels_overwrite'] is not None:
            p.yaxis.major_label_overrides = self['y_ticklabels_overwrite']

        if self['x_range_padding'] is not None:
            p.x_range.range_padding = self['x_range_padding']

        if self['y_range_padding'] is not None:
            p.y_range.range_padding = self['y_range_padding']

        return p

    def set_color_palette_by_num_plots(self):
        """
        Set the colormap for the configured number of plots according to the set colormap or color

        copied from https://github.com/PatrikHlobil/Pandas-Bokeh/blob/master/pandas_bokeh/plot.py
        credits to PatrikHlobil
        modified for use in this Plotter class
        """
        from bokeh.palettes import all_palettes  #pylint: disable=no-name-in-module

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
                    f"Could not find <colormap> with name {self['color_palette']}. The following predefined colormaps are "
                    f'supported (see also https://bokeh.pydata.org/en/latest/docs/reference/palettes.html ): {list(all_palettes.keys())}'
                )
        else:
            if self.num_plots <= 10:
                color = all_palettes['Category10'][10][:self.num_plots]
            elif self.num_plots <= 20:
                color = all_palettes['Category20'][self.num_plots]
            else:
                color = all_palettes['Category20'][20] * int(self.num_plots / 20 + 1)
                color = color[:self.num_plots]

        self['color'] = color

    @staticmethod
    def _format_tooltips(tooltips, **kwargs):
        """
        Format the strings in tooltips with the given kwargs.

        :param tooltips: The tooltips list to be formatted
        :param kwargs: The keywords arguments used to format the strings

        :returns: list of tuples with the tooltips ready to be used for tooltips
        """
        import string

        for indx, (label, value) in enumerate(tooltips):
            if len([val[0] for val in string.Formatter().parse(label)]) != 0:
                label = label.format(**kwargs)
            if len([val[0] for val in string.Formatter().parse(value)]) != 0:
                value = value.format(**kwargs)
            tooltips[indx] = (label, value)

        return tooltips

    def add_tooltips(self, fig, renderers, columns=None, toggleable=False):
        """
        Add Hover tooltips to the given renderers and figure

        :param fig: bokeh figure to apply changes to
        :param renderers: bokeh renderers to activate the tooltips for
        :param columns: namedtuple containing the data keys used for evtl. formatting
        :param toggleable: bool, if True these tooltips will be toggleable in the toolbar
        """
        from bokeh.models import HoverTool

        if self['show_tooltips']:

            if self['global_tooltips'] and renderers != 'auto':
                return

            if columns is not None:
                kwargs = columns._asdict()
            else:
                kwargs = {}

            if not isinstance(renderers, list) and renderers != 'auto':
                renderers = [renderers]

            tooltips = self['tooltips']
            if tooltips is None:
                tooltips = []

            additional_tooltips = self['additional_tooltips']
            if additional_tooltips is None:
                additional_tooltips = []

            tooltips = tooltips.copy() + additional_tooltips.copy()

            if self['format_tooltips']:
                final_tooltips = self._format_tooltips(tooltips, **kwargs)
            else:
                final_tooltips = tooltips

            #We make them not toggleable for now since it would lead to multiple
            #hover icons in the toolbar, which is kind of annoying
            hover = HoverTool(tooltips=final_tooltips, toggleable=toggleable, renderers=renderers)
            fig.add_tools(hover)

            active_inspect = fig.toolbar.active_inspect
            if active_inspect is None:
                active_inspect = []
            active_inspect.append(hover)
            fig.toolbar.active_inspect = active_inspect

    def draw_straight_lines(self, fig):
        """
        Draw horizontal and vertical lines specified in the lines argument

        :param fig: bokeh figure on which to perform the operation
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

    def set_limits(self, fig):
        """
        Set limits of the figure

        :param fig: bokeh figure on which to perform the operation
        """
        from bokeh.models import Range1d

        if self['limits'] is not None:
            if 'x' in self['limits']:
                xmin = self['limits']['x'][0]
                xmax = self['limits']['x'][1]
                fig.x_range = Range1d(xmin, xmax)
            if 'y' in self['limits']:
                ymin = self['limits']['y'][0]
                ymax = self['limits']['y'][1]
                fig.y_range = Range1d(ymin, ymax)

    def set_legend(self, fig):
        """
        Set legend options for the figure

        :param fig: bokeh figure on which to perform the operation
        """

        fig.legend.location = self['legend_location']
        fig.legend.background_fill_color = self['background_fill_color']
        fig.legend.click_policy = self['legend_click_policy']
        fig.legend.orientation = self['legend_orientation']
        fig.legend.label_text_font_size = self['legend_font_size']

        if self['legend_outside_plot_area']:
            fig.add_layout(fig.legend[0], 'right')

    def save_plot(self, figure, saveas):
        """
        Show/save the bokeh figure

        :param figure: bokeh figure on which to perform the operation
        """
        from bokeh.io import show, save, export_png, export_svgs
        if self['show']:
            show(figure)
        if self['save_plots']:
            if isinstance(self['save_format'], list):
                formats = self['save_format']
            else:
                formats = [self['save_format']]

            for fmt in formats:
                savefilename = f'{saveas}.{fmt}'
                print(f'Save plot to: {savefilename}')
                if fmt == 'html':
                    save(figure, filename=savefilename)
                elif fmt == 'png':
                    export_png(figure, filename=savefilename)
                elif fmt == 'svg':
                    export_svgs(figure, filename=savefilename)
