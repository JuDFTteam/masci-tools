# -*- coding: utf-8 -*-
"""Common base classes and methods for all plotting classes. Actual plotting classes are
divided into inheriting submodules, one per plotting tool (matplotlib, and so on).
"""
from abc import ABC, abstractmethod
from collections import namedtuple
from enum import Enum
import periodictable
import logging

from studentproject18w.hdf.output_types import *
from studentproject18w.dos.reader import get_dos_num_groups_characters


##########################################################################
#####################Section 1: Abstract Plot base classes ###############
#####################for different applications ##########################
##########################################################################


class PlotDataType(Enum):
    Bands = 1
    DOS_CSV = 2
    DOS_HDF = 3


class AbstractPlot(ABC):
    """
    Base class for all Plot classes.
    """

    def __init__(self, data: FleurData):
        """
        :param data:

        Attributes
        ----------
            icdv    interactive control display values (namedtuple)

        """
        if not hasattr(self, 'types'):
            self.types = set()
        self.data = data
        self.icdv = None

    @abstractmethod
    def get_data_ylim(self):
        """
        Useful for getting info on the maximum ylim before plotting, e.g. to set ylim to a GUI control.
        :return:
        """
        pass

    def get_alphas_colors_for_spin_overlay(self, spins, plotDataTypes=[]):
        alphas = {0: 1, 1: 1} if (len(spins) == 1) else {0: 0.7, 1: 0.4}
        if any(typ in self.types for typ in plotDataTypes):
            # DOS: only two lines. loooks odd if spin1 DOS is half-transparent
            alphas = {0: 1, 1: 1}
        colors = {0: 'blue', 1: 'red'}
        return (alphas, colors)


class AbstractBandPlot(AbstractPlot):
    def __init__(self, data: FleurBandData):
        AbstractPlot.__init__(self, data)
        self.types.update([PlotDataType.Bands])

        self.icdv = BandDataDisplayValues(self)

    @abstractmethod
    def setup_band_labels(self):
        pass

    @abstractmethod
    def plot_bands(self):
        pass

    @abstractmethod
    def _plot_bands_normal(self):
        pass

    @abstractmethod
    def _plot_bands_compare_two_characters(self):
        pass

    @abstractmethod
    def plot_groupVelocity(self):
        pass


class AbstractDOSPlot(AbstractPlot):
    def __init__(self, data: FleurData, filepaths_dos: list):
        AbstractPlot.__init__(self, data)
        self.filepaths_dos = filepaths_dos
        if filepaths_dos:
            self.types.update([PlotDataType.DOS_CSV])
        else:
            self.types.update([PlotDataType.DOS_HDF])

        self.icdv = DOSDataDisplayValues(self)

    @abstractmethod
    def plot_dos(self):
        pass


class AbstractBandDOSPlot(AbstractBandPlot, AbstractDOSPlot):
    def __init__(self, data: FleurBandData, filepaths_dos: list):
        AbstractBandPlot.__init__(self, data)
        AbstractDOSPlot.__init__(self, data, filepaths_dos)

        self.icdv = BandDOSDataDisplayValues(self)

    def plot_bandDOS(self):
        pass


##########################################################################
#####################Section 2: abstract base classes ####################
#####################that define values for interactive###################
#####################controls for plots###################################
##########################################################################


class InteractiveControlDisplayValues(ABC):
    def __init__(self, plotter: AbstractPlot):
        pass

    @abstractmethod
    def convert_selections(self):
        pass


class DOSDataDisplayValues(InteractiveControlDisplayValues):
    def __init__(self, plotter: AbstractDOSPlot):
        InteractiveControlDisplayValues.__init__(self, plotter)

        if (not hasattr(self, 'groups') and (not hasattr(self, 'characters'))):
            self.characters = ['s', 'p', 'd', 'f']
            self.groups = None
            if (PlotDataType.Bands in plotter.types
                    or PlotDataType.DOS_HDF in plotter.types):
                self.groups = plotter.data.atoms_group_keys
                if (not hasattr(self, 'group_labels')):
                    #old: wrong
                    # self.group_labels = [f"{g:<3} {e.symbol:<3}: {int(n):<3}" for g, e, n
                    #                      in zip(plotter.data.atoms_group_keys,
                    #                             plotter.data.atoms_elements,
                    #                             plotter.data.atoms_per_group)]

                    #new: corect
                    group_labels = []
                    for g in plotter.data.atoms_group_keys:
                        index = plotter.data.atoms_group.tolist().index(g)
                        e = plotter.data.atoms_elements[index]
                        n = plotter.data.atoms_per_group[g - 1]
                        label = f"{g:<3} {e.symbol:<3}: {int(n):<3}"
                        group_labels.append(label)
                    self.group_labels = group_labels
            elif (PlotDataType.DOS_CSV in plotter.types):
                (num_groups, num_chars) = get_dos_num_groups_characters(plotter.filepaths_dos[0])
                if (num_groups, num_chars) == (None, None):
                    logging.warn(f"Could not discern num_atom_groups, num_characters "
                                 f"from DOS CSV file {plotter.filepaths_dos[0]}.")
                self.characters = self.characters[:num_chars]
                self.groups = dict.fromkeys(range(1, num_groups + 1)).keys()
                if (not hasattr(self, 'group_labels')):
                    self.group_labels = [f"{int(g)}" for g in
                                         self.groups]  # TODO could likewise use periodictable here!

    def convert_selections(self, characters=[], groups=[]):
        # convert arguments to the expected format for code 181124
        groups_conved = [el - 1 for el in groups] if groups else []
        characters_conved = [self.characters.index(el) for el in characters] if characters else []

        # convert arguments to the expected format for code 181212
        mask_characters = [el in characters for el in self.characters] if characters else []
        mask_groups = [el in [el for el in groups] for el in self.groups] if groups else []

        return (mask_characters, mask_groups)


class BandDataDisplayValues(InteractiveControlDisplayValues):
    """
    Definitions for user-based data selection controls for interactive band plotting interfaces.
    """

    def __init__(self, plotter: AbstractBandPlot):
        """
        :param plotter: e.g. BandPlot or DOSPlot
        """
        InteractiveControlDisplayValues.__init__(self, plotter)

        if not hasattr(self, 'characters'):
            self.characters = ['s', 'p', 'd', 'f']
        if not hasattr(self, 'groups'):
            self.groups = plotter.data.atoms_group_keys
        if not hasattr(self, 'group_labels'):
            self.group_labels = [f"{g:<3} {e.symbol:<3}: {int(n):<3}" for g, e, n
                                 in zip(plotter.data.atoms_group_keys,
                                        plotter.data.atoms_elements,
                                        plotter.data.atoms_per_group)]
        SliderSelection = namedtuple('SliderSelection', ['label', 'min', 'max', 'step', 'initial'])
        if not hasattr(self, 'bands'):
            bands = [band for band in range(plotter.data.eigenvalues.shape[2])]
            self.bands = bands
            self.bands_slider = SliderSelection(label="Bands",
                                                min=bands[0] + 1,
                                                max=bands[-1] + 1,
                                                step=1,
                                                initial=[bands[0] + 1, bands[-1] + 1])

        if not hasattr(self, 'spins'):
            self.spins = [spin for spin in range(plotter.data.num_spin)]
        if not hasattr(self, 'ylim'):
            ylim = plotter.get_data_ylim()
            self.ylim = SliderSelection(label="$E$ Range",
                                        min=ylim[0],
                                        max=ylim[1],
                                        step=(ylim[1] - ylim[0]) / 100,
                                        initial=ylim)
        if not hasattr(self, 'exponent'):
            self.exponent = SliderSelection("Unfolding", 0.0, 4.0, 0.01, 1.0)
        if not hasattr(self, 'marker_size'):
            self.marker_size = SliderSelection("Dot Size", 0.0, 10.0, 0.01, 1.0)

    def convert_selections(self, bands=[], characters=[], groups=[]):
        # convert arguments to the expected format for code 181124
        bands_conved = range(bands[0] - 1, bands[1]) if bands else []
        groups_conved = [el - 1 for el in groups] if groups else []
        characters_conved = [self.characters.index(el) for el in characters] if characters else []

        # convert arguments to the expected format for code 181212
        mask_characters = [el in characters for el in self.characters] if characters else []
        mask_bands = [el in bands_conved for el in self.bands] if bands else []
        mask_groups = [el in [el for el in groups] for el in self.groups] if groups else []

        return (mask_bands, mask_characters, mask_groups)


class BandDOSDataDisplayValues(BandDataDisplayValues, DOSDataDisplayValues):
    """
    Notes
    ----
    Since inherits first from BandData the DOSData, will use inherited
    methods from BandData first if present in both. Example: will use conver_selections()
    of BandDataDisplayValues.
    """

    def __init__(self, plotter: AbstractBandDOSPlot):
        DOSDataDisplayValues.__init__(self, plotter)
        BandDataDisplayValues.__init__(self, plotter)
