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

import matplotlib.pyplot as plt

class MatplotlibPlotter(Plotter):

    _PLOT_DEFAULTS = {
        # figure properties
        'title_fontsize' : 16,
        'figsize' : (8, 6),
        'dpi' : 80,
        'facecolor' : 'w',
        'edgecolor': 'k',

        # axis properties
        'alpha' : 1,
        'axis_linewidth' : 1.5,
        'use_axis_formatter' : False,
        'set_powerlimits': True,
        'xticks': None,
        'xticklabels': None,

        # plot properties
        'linewidth' : 2.0,
        'linestyle' : '-',
        'marker': 'o',
        'markersize' : 4.0,
        'color': None,
        'plot_label': '',

        # x, y label
        'labelfontsize' : 15,

        # ticks
        'ticklabelsizex' : 14,
        'ticklabelsizey' : 14,
        'tick_paramsx' : {'size': 4.0, 'width': 1.0, 'labelsize': 14, 'length': 5, 'labelrotation': 0},
        'tick_paramsy' : {'size': 4.0, 'width': 1.0, 'labelsize': 14, 'length': 5, 'labelrotation': 0},
        'ticklabelsizex_minor' : 0,
        'ticklabelsizey_minor' : 0,
        'tick_paramsx_minor_g' : {'size': 2.0, 'width': 1.0, 'labelsize': 0, 'length': 2.5},
        'tick_paramsy_minor_g' : {'size': 2.0, 'width': 1.0, 'labelsize': 0, 'length': 2.5},
        # legend properties
        'legend' : False,
        'legend_options': {
            'bbox_to_anchor': (0.65, 0.97),
            'fontsize': 16,
            'linewidth': 3.0,
            'borderaxespad': 0,
            'loc': 2,
            'fancybox': True
        },

        # save all plots?
        'save_plots' : False,  # True
        'save_format' : 'png',  #'pdf'
        'tightlayout' : False,

        'show' : True,
        # write data to file
        'save_raw_plot_data' : False,
        'raw_plot_data_format' : 'txt'}

    def __init__(self, **kwargs):
        super().__init__(self._PLOT_DEFAULTS, **kwargs)

    def figure_kwargs(self):

        FIGURE_KEYS = {'figsize', 'dpi', 'facecolor', 'edgecolor'}

        fig_kwargs = {}
        for key in FIGURE_KEYS:
            if self[key] is not None:
                fig_kwargs[key] = self[key]

        return fig_kwargs

    def plot_kwargs(self, indx=None):

        FIGURE_KEYS = {'linewidth','linestyle','marker','markersize','color','plot_label'}

        plot_kwargs = {}
        for key in FIGURE_KEYS:
            if key == 'plot_label':
                set_key = 'label'
            else:
                set_key = key

            if self[(key,indx)] is not None:
                plot_kwargs[set_key] = self[(key,indx)]

        return plot_kwargs

    def prepare_figure(self, title=None, xlabel=None, ylabel=None, axis=None, minor=False, projection=None):

        if axis is not None:
            ax = axis
        else:
            fig = plt.figure(num=None, **self.figure_kwargs())
            ax = fig.add_subplot(111, projection=projection)

        for axis in ['top', 'bottom', 'left', 'right']:
            ax.spines[axis].set_linewidth(self['axis_linewidth'])
        ax.set_title(title, fontsize=self['title_fontsize'], alpha=self['alpha'], ha='center')
        ax.set_xlabel(xlabel, fontsize=self['labelfontsize'])
        ax.set_ylabel(ylabel, fontsize=self['labelfontsize'])
        ax.yaxis.set_tick_params(**self['tick_paramsy'])
        ax.xaxis.set_tick_params(**self['tick_paramsx'])

        if minor:
            ax.yaxis.set_tick_params(which='minor', **self['tick_paramsy_minor'])
            ax.xaxis.set_tick_params(which='minor', **self['tick_paramsx_minor'])

        if self['xticks'] is not None:
                ax.xaxis.set_ticks(self['xticks'])
        if self['xticklabels'] is not None:
                ax.xaxis.set_ticklabels(self['xticklabels'])

        if self['use_axis_formatter']:
            if self['set_powerlimits']:
                ax.yaxis.get_major_formatter().set_powerlimits((0, 3))
                ax.xaxis.get_major_formatter().set_powerlimits((0, 3))
            ax.yaxis.get_major_formatter().set_useOffset(False)
            ax.xaxis.get_major_formatter().set_useOffset(False)

        return ax

    def show_legend(self, ax):
        #TODO legend
        if self['legend']:
            loptions = copy.deepcopy(self['legend_options'])
            linewidth = loptions.pop('linewidth', 1.5)
            title_font_size = loptions.pop('title_fontsize', 15)
            leg = ax.legend(**loptions)
            leg.get_frame().set_linewidth(linewidth)
            leg.get_title().set_fontsize(title_font_size)  #legend 'Title' fontsize

    def save_figure(self, saveas):
        if self['save_plots']:
            savefilename = f"{saveas}.{self['save_format']}"
            print(f'Save plot to: {savefilename}')
            plt.savefig(savefilename, format=self['save_format'], transparent=True)
        elif self['show']:
            plt.show()
