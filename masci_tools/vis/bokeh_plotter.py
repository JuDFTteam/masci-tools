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

from bokeh.plotting import figure as bokeh_fig
from bokeh.io import show as bokeh_show
from bokeh.models import Title

class BokehPlotter(Plotter):

    _PLOT_DEFAULTS = {
      'figure_kwargs': {'tools': 'hover',
                        'y_axis_type': 'linear',
                        'x_axis_type': 'linear',
                        'toolbar_location': None,
                        'tooltips': [('X value', '@x'), ('Y value', '@y')]},
      'axis_linewidth': 2,
      'label_fontsize': '18pt',
      'tick_label_fontsize': '16pt',
      'background_fill_color': '#ffffff',
      'show': True,
    }

    def __init__(self, **kwargs):

        super().__init__(self._PLOT_DEFAULTS, **kwargs)

    def prepare_figure(self, title, xlabel, ylabel, figure=None):
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

    def save_plot(self, figure):
        if self['show']:
            bokeh_show(figure)
