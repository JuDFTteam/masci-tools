# -*- coding: utf-8 -*-
"""Common base classes and methods for all plotting classes. Actual plotting classes are
divided into inheriting submodules, one per plotting tool (matplotlib, and so on).
"""
from enum import Enum

from studenproject18ws.hdf.output_types import *

class PlotDataType(Enum):
    Bands = 1
    DOS = 2

class Plot(object):
    """
    Base class for all Plot classes.
    """

    def __init__(self, data: Data):
        """
        :param data:
        """
        self.data = data

    def get_data_ylim(self):
        """
        Useful for getting info on the maximum ylim before plotting, e.g. to set ylim to a GUI control.
        :return:
        """
        raise NotImplementedError

    def get_alphas_colors_for_spin_overlay(self, spins, plot_type=PlotDataType.Bands):
        alphas = {0: 1, 1: 1} if (len(spins) == 1) else {0: 1, 1: 0.5}
        if (plot_type == PlotDataType.DOS):
            # DOS: only two lines. loooks odd if spin1 DOS is half-transparent
            alphas[1] = 1
        colors = {0: 'blue', 1: 'red'}
        return (alphas, colors)