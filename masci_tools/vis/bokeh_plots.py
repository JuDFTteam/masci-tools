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
Here are general and special bokeh plots to use

"""
import math
import numpy as np
import pandas as pd
import json

from bokeh.models import (ColumnDataSource, LinearColorMapper, LogColorMapper, ColorBar, BasicTicker, Title, Legend)
from bokeh.layouts import gridplot
from bokeh.core.properties import FontSize
from bokeh.io import show as bshow
from bokeh.plotting import figure as bokeh_fig
from matplotlib.colors import Normalize, LogNorm, to_hex
from matplotlib.cm import plasma, inferno, magma, viridis  #pylint: disable=no-name-in-module
from matplotlib.cm import ScalarMappable

################## Helpers     ################


def get_colormap(colormap, N_cols):
    """
    Returns a colormap with <N_cols> colors. <colormap> can be either None,
    a string with the name of a Bokeh color palette or a list/tuple of colors.

    copied from https://github.com/PatrikHlobil/Pandas-Bokeh/blob/master/pandas_bokeh/plot.py
    credits to PatrikHlobil
    """
    from bokeh.palettes import all_palettes

    if colormap is None:
        if N_cols <= 10:
            colormap = all_palettes['Category10'][10][:N_cols]
        elif N_cols <= 20:
            colormap = all_palettes['Category20'][N_cols]
        else:
            colormap = all_palettes['Category20'][20] * int(N_cols / 20 + 1)
            colormap = colormap[:N_cols]
    elif isinstance(colormap, str):
        if colormap in all_palettes:
            colormap = all_palettes[colormap]
            max_key = max(colormap.keys())
            if N_cols <= max_key:
                colormap = colormap[N_cols]
            else:
                colormap = colormap[max_key]
                colormap = colormap * int(N_cols / len(colormap) + 1)
                colormap = colormap[:N_cols]
        else:
            raise ValueError(
                'Could not find <colormap> with name %s. The following predefined colormaps are '
                'supported (see also https://bokeh.pydata.org/en/latest/docs/reference/palettes.html ): %s' %
                (colormap, list(all_palettes.keys())))
    elif isinstance(colormap, (list, tuple)):
        colormap = colormap * int(N_cols / len(colormap) + 1)
        colormap = colormap[:N_cols]
    else:
        raise ValueError('<colormap> can only be None, a name of a colorpalette as string( see '
                         'https://bokeh.pydata.org/en/latest/docs/reference/palettes.html ) or a list/tuple of colors.')

    return colormap


def prepare_plot(data, figure_options):
    """
    used to set some default options.
    """

    # get updated default figure option, data from columns
    figure_options_defaults = {
        'title': '',
        'toolbar_location': 'below',
        'active_scroll': 'wheel_zoom',
        'plot_width': 600,
        'plot_height': 400,
        'output_backend': 'webgl',
        'sizing_mode': 'fixed',
        'x_axis_location': 'below'
    }

    figure_opt = figure_options_defaults.update(figure_options)
    # this output is what every routine should use.
    return data, figure_opt


##################################### general plots ##########################

tooltips_def_scatter = [('X value', '@x'), ('Y value', '@y')]


def bokeh_scatter(source,
                  xdata='x',
                  ydata='y',
                  figure=None,
                  scale=['linear', 'linear'],
                  xlabel='x',
                  ylabel='y',
                  legend_labels=None,
                  title='',
                  outfilename='scatter.html',
                  tools='hover',
                  tooltips=tooltips_def_scatter,
                  toolbar_location=None,
                  background_fill_color='#ffffff',
                  figure_kwargs={},
                  show=True,
                  bounds=None,
                  **kwargs):
    """
    create an interactive scatter plot with bokeh


    """
    # create figure if needed

    if figure is None:
        fig_kwargs = {
            'title': title,
            'tools': tools,
            'y_axis_type': scale[1],
            'x_axis_type': scale[0],
            'tooltips': tooltips,
            'toolbar_location': toolbar_location
        }
        fig_kwargs.update(figure_kwargs)
        p = bokeh_fig(**fig_kwargs)
    else:
        p = figure
        if background_fill_color is not None:
            p.background_fill_color = background_fill_color
        if title is not None:
            p.title = Title(text=title)
    if xlabel is not None:
        p.xaxis.axis_label = xlabel
    if ylabel is not None:
        p.yaxis.axis_label = ylabel

    p.yaxis.axis_line_width = 2
    p.xaxis.axis_line_width = 2
    p.xaxis.axis_label_text_font_size = '18pt'
    p.yaxis.axis_label_text_font_size = '18pt'
    p.yaxis.major_label_text_font_size = '16pt'
    p.xaxis.major_label_text_font_size = '16pt'

    # choose color map
    # draw scatter plot
    p.scatter(x=xdata, y=ydata, source=source, **kwargs)

    # source.plot_bokeh.scatter(x='pt_number', y='mean', category='mean', colormap='Plasma', show_figure=False
    if show:
        bshow(p)

    return p


# line plot
tooltips_def_line = [('X value', '@x'), ('Y value', '@y')]


def bokeh_line(source,
               xdata=['x'],
               ydata=['y'],
               figure=None,
               scale=['linear', 'linear'],
               xlabel='x',
               ylabel='y',
               legend_labels=None,
               title='',
               outfilename='scatter.html',
               tools='hover',
               tooltips=tooltips_def_line,
               toolbar_location=None,
               background_fill_color='#ffffff',
               colormap=None,
               color=None,
               marker='circle',
               marker_size=6,
               figure_kwargs={},
               show=True,
               plot_points=False,
               bounds=None,
               name='line plot',
               legend_layout_location='center',
               **kwargs):
    """
    Create an interactive multi line plot with bokeh, while also showing points

    Per default all ydata use the same x, if xdata is list it has to have the same length as ydata
    """
    # create figure if needed
    if figure is None:
        fig_kwargs = {
            'title': title,
            'tools': tools,
            'y_axis_type': scale[1],
            'x_axis_type': scale[0],
            'tooltips': tooltips,
            'toolbar_location': 'above'
        }
        fig_kwargs.update(figure_kwargs)
        p = bokeh_fig(**fig_kwargs)
    else:
        p = figure
        if background_fill_color is not None:
            p.background_fill_color = background_fill_color
        if title is not None:
            p.title = Title(text=title)

    if xlabel is not None:
        p.xaxis.axis_label = xlabel
    if ylabel is not None:
        p.yaxis.axis_label = ylabel

    p.yaxis.axis_line_width = 2
    p.xaxis.axis_line_width = 2
    p.xaxis.axis_label_text_font_size = '18pt'
    p.yaxis.axis_label_text_font_size = '18pt'
    p.yaxis.major_label_text_font_size = '16pt'
    p.xaxis.major_label_text_font_size = '16pt'

    if isinstance(xdata, list):
        if len(xdata) != len(ydata):
            xdata = xdata[0]

    N_col = len(ydata)

    # choose color map
    colormap = get_colormap(colormap, N_col)
    if color is not None:
        colormap = get_colormap([color], N_col)

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
    legitems = []

    for i, yname, in enumerate(ydatad):
        color = colormap[i]
        if isinstance(xdatad, list):
            xdat = xdatad[i]
        else:
            xdat = xdatad

        if isinstance(name, list):
            namet = name[i]
        else:
            namet = name

        if isinstance(source, list):
            sourcet = source[i]
        else:
            sourcet = source

        if legend_labels is None:
            leg_label = yname
        else:
            leg_label = legend_labels[i]

        l1 = p.line(
            x=xdat,
            y=yname,
            source=sourcet,  #legend_label=" " + leg_label,
            color=color,
            name=namet,
            **kwargs)
        s1 = None
        if plot_points:
            s1 = p.scatter(
                x=xdat,
                y=yname,
                source=sourcet,
                #legend_label=" " + leg_label,
                color=color,
                marker=marker,
                size=marker_size)
        if s1:
            legitems.append((leg_label, [l1, s1]))
        else:
            legitems.append((leg_label, [l1]))

    # TODO do not hardcode.
    legend = Legend(items=legitems,
                    location='top_right',
                    background_fill_color=background_fill_color,
                    click_policy='hide',
                    orientation='vertical',
                    label_text_font_size='14pt')

    p.add_layout(legend, legend_layout_location)
    #p.legend.location = "top_right"
    #p.legend.background_fill_color = background_fill_color
    #p.legend.click_policy = "hide"  # "mute"#"hide"
    #p.legend.orientation = "vertical"
    #p.legend.label_text_font_size = "14pt"
    if show:
        bshow(p)

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
                        color_map=plasma,
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

    source.
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


def plot_convergence_results(distance,
                             total_energy,
                             iteration,
                             link=False,
                             nodes=[],
                             saveas1='t_energy_convergence',
                             saveas2='distance_convergence',
                             figure_kwargs={
                                 'plot_width': 800,
                                 'plot_height': 450
                             },
                             show=True,
                             **kwargs):
    """
    Plot the total energy versus the scf iteration
    and plot the distance of the density versus iterations. Uses bokeh_line and bokeh_scatter

    :param distance: list of floats
    :total_energy: list of floats
    :param iteration: list of Int
    :param link: bool, optional default=False:
    :param nodes: list of node uuids or pks important for links
    :param saveas1: str, optional default='t_energy_convergence', save first figure as
    :param saveas2: str, optional default='distance_convergence', save second figure as
    :param figure_kwargs: dict, optional default={'plot_width': 800, 'plot_height': 450}, gets parsed
    to bokeh_line
    :param **kwargs: further key-word arguments for bokeh_line

    :returns grid: bokeh grid with figures
    """

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

    tools = 'hover,tap,box_zoom,zoom_out,crosshair,reset,save'
    active_tools = 'hover'
    tooltips_def_scatter1 = [('Iteration', '@x'), ('Total energy distance', '@y')]
    tooltips_def_scatter2 = [('Iteration', '@x'), ('Charge distance', '@y')]
    figure_kwargs.update({'active_inspect': 'hover'})

    # plot
    p1 = bokeh_line(source=source1,
                    ydata=['total_energy_delta'],
                    xdata=['iterations'],
                    xlabel=xlabel,
                    ylabel=ylabel1,
                    title=title1,
                    name='delta total energy',
                    scale=['linear', 'log'],
                    plot_points=True,
                    tools=tools,
                    tooltips=tooltips_def_scatter1,
                    figure_kwargs=figure_kwargs,
                    **kwargs)

    p2 = bokeh_line(source=source2,
                    ydata=['distance'],
                    xdata=['iterations'],
                    xlabel=xlabel,
                    ylabel=ylabel2,
                    title=title2,
                    name='distance',
                    scale=['linear', 'log'],
                    plot_points=True,
                    tools=tools,
                    tooltips=tooltips_def_scatter2,
                    figure_kwargs=figure_kwargs,
                    **kwargs)
    grid = gridplot([p1, p2], ncols=2)

    if show:
        bshow(grid)

    return grid


def plot_convergence_results_m(distances,
                               total_energies,
                               iterations,
                               link=False,
                               nodes=[],
                               plot_labels=[],
                               saveas1='t_energy_convergence',
                               saveas2='distance_convergence',
                               show=True,
                               figure_kwargs={
                                   'plot_width': 600,
                                   'plot_height': 450
                               },
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
    :param **kwargs: further key-word arguments for bokeh_line

    :returns grid: bokeh grid with figures
    """

    xlabel = r'Iteration'
    ylabel1 = r'Total energy difference [Htr]'
    ylabel2 = r'Distance [me/bohr^3]'
    title1 = r'Total energy difference over scf-Iterations'
    title2 = r'Convergence (log)'

    iterations1 = []
    plot_labels1 = []
    plot_labels2 = []

    data_dict1 = {}
    data_dict2 = {}

    xdatal_all = []
    ydata1l_all = []
    ydata2l_all = []
    data_sources = []
    data_sources2 = []

    tools = 'hover,tap,box_zoom,zoom_out,crosshair,reset,save,pan'
    tooltips_def_scatter1 = [('Calculation id', '@id'), ('Iteration', '@x'), ('Total energy difference', '@y')]

    tooltips_def_scatter2 = [('Calculation id', '@id'), ('Iteration', '@x'), ('Charge distance', '@y')]
    figure_kwargs.update({'active_inspect': 'hover'})

    # since we make a log plot of the total_energy make sure to plot the absolute total energy
    for i, total_energy in enumerate(total_energies):
        if nodes:
            id = nodes[i]
        else:
            id = i

        xdatal = 'iterations_{}'.format(id)
        xdatal_all.append('x')
        total_energy_abs_diff = []
        for en0, en1 in zip(total_energy[:-1], total_energy[1:]):
            total_energy_abs_diff.append(abs(en1 - en0))
        ydata1l = '{}'.format(id)
        ydata2l = '{}'.format(id)
        ydata1l_all.append('y')
        ydata2l_all.append('y')

        plot_labels1.append('{}'.format(id))
        plot_labels2.append('{}'.format(id))
        #print('lengths1 : y {} x {}'.format(len(total_energy_abs_diff), len(iterations[i][1:])))

        data = {
            'y': total_energy_abs_diff,
            'x': iterations[i][1:],
            'id': [id for j in range(len(total_energy_abs_diff))]
        }
        if nodes:
            data.update({'nodes_pk': [str(nodes[i]) for j in range(len(total_energy_abs_diff))]})
        if plot_labels:
            data.update({'process_label': [plot_labels[i] for j in range(len(total_energy_abs_diff))]})

        datasrc = ColumnDataSource(data)
        data_sources.append(datasrc)
        #print('lengths2 : y {} x {}'.format(len(distances[i]), len(iterations[i])))
        data = {'y': distances[i], 'x': iterations[i], 'id': [id for j in range(len(distances[i]))]}
        if nodes:
            data.update({'nodes_pk': [str(nodes[i]) for j in range(len(distances[i]))]})
        if plot_labels:
            data.update({'process_label': [plot_labels[i] for j in range(len(distances[i]))]})

        datasrc = ColumnDataSource(data)
        data_sources2.append(datasrc)

    if plot_labels:
        if not nodes:
            plot_labels1 = plot_labels
            plot_labels2 = plot_labels
        tooltips_def_scatter2.append(('process label', '@process_label'))
        tooltips_def_scatter1.append(('process label', '@process_label'))

    if nodes:
        tooltips_def_scatter2.append(('outpara pk', '@nodes_pk'))
        tooltips_def_scatter1.append(('outpara pk', '@nodes_pk'))

    # plot
    p1 = bokeh_line(source=data_sources,
                    ydata=ydata1l_all,
                    xdata=xdatal_all,
                    xlabel=xlabel,
                    ylabel=ylabel1,
                    title=title1,
                    name=plot_labels1,
                    legend_labels=plot_labels1,
                    scale=['linear', 'log'],
                    plot_points=True,
                    tools=tools,
                    tooltips=tooltips_def_scatter1,
                    figure_kwargs=figure_kwargs,
                    show=False,
                    legend_layout_location='right')

    p2 = bokeh_line(source=data_sources2,
                    ydata=ydata2l_all,
                    xdata=xdatal_all,
                    xlabel=xlabel,
                    ylabel=ylabel2,
                    name=plot_labels2,
                    scale=['linear', 'log'],
                    legend_labels=plot_labels2,
                    plot_points=True,
                    tools=tools,
                    title=title2,
                    tooltips=tooltips_def_scatter2,
                    figure_kwargs=figure_kwargs,
                    show=False,
                    legend_layout_location='right')
    grid = gridplot([p1, p2], ncols=2)

    if show:
        bshow(grid)

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
