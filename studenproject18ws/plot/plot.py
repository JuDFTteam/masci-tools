# -*- coding: utf-8 -*-
"""Holds classes for plots of the self.data.

Each class is for a different type of plot utility. For instance, matploblib plots
are gathered in the class Matplot.

"""

import logging
import numpy as np
import matplotlib.pyplot as plt

from studenproject18ws.hdf.output_types import *
from studenproject18ws.dos.reader import get_dos


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


class Bandplot_matplotlib(Plot):
    """
    Class for rendering interactive matplotlib plots of the band data in a GUI frontend.
    Examples: Jupyter Notebook or Lab, Tkinter, PyQt, ...

    Examples
    --------

    >>> import matplotlib.pyplot as plt
    >>> from studenproject18ws.hdf.reader import Reader
    >>> from studenproject18ws.hdf.recipes import Recipes
    >>> from studenproject18ws.plot.plot import Bandplot_matplotlib as Bandplot
    >>>
    >>> filepath = "path/to/my.hdf"
    >>> data = None
    >>> reader = Reader(filepath)
    >>> with reader as h5file:
    ...    data = reader.read(recipe=Recipes.Bands)
    ...    data.move_datasets_to_memory()
    >>>
    >>> bandplotter = Bandplot(data)
    >>>
    >>> # Hre. define plot(selection) function that calls bandplotter plot functions with data selections
    >>> def plot(ax, selection):
    ...    # call bandplotter plot methods. the actual plt plot methods are then called on ax
    ...    return
    >>>
    >>> # separate plt into fig and ax for easier handling
    >>> fig, ax = plt.subplots(1, figsize=(10,6))
    >>>
    >>> # A dummy example function that is called very time the plot is to be updated
    >>> def update_plot():
    ...
    ...    # this has to be here: update plot figure labels
    ...    ax.clear()
    ...    bandplotter.setup(plt)
    ...
    ...    selection = None
    ...    # accumulate user selection and call bandplotter
    ...    plot(ax, selection)

    """

    def __init__(self, data: DataBands):
        Plot.__init__(self, data)

        # self.setup(plt)
        # # Not sure if this has any effect:
        # # The idea was to put this in the init method so teh setup step
        # # doesn't have to be repeated on any update. But at least in Jupyter
        # # this does not work. So unless this is indeed helpful in other frontends,
        # # it can be removed. Commenting it out for the time being.

    def get_band_data_ylim(self):
        sel = self.data.simulate_gui_selection()

        (k_r, E_r, W_r) = self.data.reshape_data(sel.mask_bands, sel.mask_characters, sel.mask_groups, sel.spin,
                                                 unfolding_weight_exponent=1, ignore_atoms_per_group=False)

        ymin = np.min(((E_r - self.data.fermi_energy) * self.data.HARTREE_EV))
        ymax = np.max(((E_r - self.data.fermi_energy) * self.data.HARTREE_EV))

        return (ymin, ymax)

    def setup(self, plt):
        """
        Call this function every time the interactive plot is about to be updated in the GUI.

        It repaints the labels on the figure.


        :param plt:
        :return:
        """
        labels = []
        for label in self.data.k_special_point_labels:
            label = label.decode("utf-8")
            if (label == "g"):
                labels += ["$\Gamma$"]
            else:
                labels += str(label)

        plt.xticks(self.data.k_special_points, labels)
        plt.ylabel("E(k) [eV]")
        plt.xlim(0, max(self.data.k_distances))
        plt.hlines(0, 0, max(self.data.k_distances), lw=0.1)

    def plot_bands(self, mask_bands, mask_characters, mask_groups, spins,
                   unfolding_weight_exponent, compare_characters,
                   ax, ignore_atoms_per_group, marker_size=1):
        """
        Top-level method for the bandDOS plot. Calls appropriate subplot methods based on user selection.

        :param mask_bands: list of bool
        :param mask_characters: list of bool
        :param mask_groups: list of bool
        :param spins: list of int. either [0] or [0,1]
        :param unfolding_weight_exponent: dloat
        :param compare_characters: bool
        :param ax: pyplot ax
        :param ignore_atoms_per_group: bool
        :param marker_size: float
        :return:
        """
        alpha = 1
        if compare_characters:
            self.plot_bands_compare_two_characters(mask_bands, mask_characters, mask_groups, spins[0],
                                                   unfolding_weight_exponent,
                                                   ax, alpha, ignore_atoms_per_group, marker_size)
        else:
            alphas = {0: 1, 1: 1} if (len(spins) ==1) else {0: 1, 1: 0.5}
            colors = {0: 'blue', 1: 'red'}
            for spin in spins:
                self.plot_bands_normal(mask_bands, mask_characters, mask_groups, spin,
                                       unfolding_weight_exponent,
                                       ax, colors[spin], alphas[spin], ignore_atoms_per_group, marker_size)

    def plot_bands_normal(self, mask_bands, mask_characters, mask_groups, spin,
                          unfolding_weight_exponent, ax, color, alpha=1,
                          ignore_atoms_per_group=False, marker_size=1):
        """Plot regular.

        Static plot method as template for interactive plot function in GUI.

        christian's code version 181214

        :param marker_size:
        :param ignore_atoms_per_group:
        :param mask_bands:
        :param mask_characters:
        :param mask_groups:
        :param spin:
        :param unfolding_weight_exponent:
        :param ax:
        :param color:
        :param alpha:
        :return:
        """
        (k_r, E_r, W_r) = self.data.reshape_data(mask_bands, mask_characters, mask_groups, spin,
                                                 unfolding_weight_exponent, ignore_atoms_per_group)

        # just plot points with minimal size of t
        speed_up = True
        if speed_up:
            t = 1e-4
            k_r = k_r[W_r > t]
            E_r = E_r[W_r > t]
            W_r = W_r[W_r > t]
        W_r *= marker_size
        ax.scatter(k_r, (E_r - self.data.fermi_energy) * self.data.HARTREE_EV,
                   marker='o', c=color, s=5 * W_r, lw=0, alpha=alpha)

    def plot_bands_compare_two_characters(self, mask_bands, mask_characters, mask_groups, spin, unfolding_weight_exponent, ax,
                                          alpha=1, ignore_atoms_per_group=False, marker_size=1):
        """Plot with exactly 2 selected band characters mapped to colormap.

        Static plot method as template for interactive plot function in GUI.
        Note: right now, selection (s,p) = [True,True,False,False] is hardcoded!

        christian's code version 190108

        Notes
        =====
        The conversion mask_characters -> characters -> self.mask_characters() looks a bit strange.
        Probably could be done simpler with a list comprehension.

        :param marker_size:
        :param ignore_atoms_per_group:
        :param mask_bands:
        :param mask_characters:
        :param mask_groups:
        :param spin:
        :param ax:
        :param alpha:
        :return:
        """

        characters = np.array(range(4))[mask_characters]
        if (len(characters) != 2):
            print("plot_two_characters: tried to plot with other than 2 characters selected. not allowed!")
            ax.scatter([0], [0])
            return

        (k_resh, evs_resh, weight_resh) = self.data \
            .reshape_data(mask_bands, self.data._mask_characters([characters[0]]),
                          mask_groups, spin, unfolding_weight_exponent, ignore_atoms_per_group)


        (k_resh2, evs_resh2, weight_resh2) = self.data \
            .reshape_data(mask_bands, self.data._mask_characters([characters[1]]),
                          mask_groups, spin, unfolding_weight_exponent, ignore_atoms_per_group)

        # print(f"non-zero elements in divisor array: {np.count_nonzero(weight_resh+weight_resh2)} of {weight_resh.size} elements.")
        rel = weight_resh / (weight_resh + weight_resh2) * 20
        tot_weight = weight_resh + weight_resh2
        # ax1.scatter(k_resh, (evs_resh-fermi_energy)*hartree_in_ev, marker='o', c="g", s = 5 * weight_resh, lw=0, alpha = alpha)
        # ax1.scatter(k_resh2, (evs_resh-fermi_energy)*hartree_in_ev, marker='o', c="r", s = 5 * weight_resh2, lw=0, alpha = alpha)
        # print(len(tot_weight))
        # print(len(k_resh2))
        # print(len(rel))
        # print(len(evs_resh))

        # dont change order inside if statement...
        speed_up = True
        if speed_up:
            t = 1e-4
            k_resh2 = k_resh2[tot_weight > t]
            evs_resh = evs_resh[tot_weight > t]
            rel = rel[tot_weight > t]
            tot_weight = tot_weight[tot_weight > t]
        tot_weight *= marker_size

        # print(len(tot_weight))
        # print(len(k_resh2))
        # print(len(rel))
        # print(len(evs_resh))

        # cm = plt.cm.get_cmap('RdYlBu')
        # cm = plt.cm.winter
        cm = plt.cm.plasma
        ax.scatter(k_resh2, (evs_resh - self.data.fermi_energy) * self.data.HARTREE_EV,
                   marker='o', c=rel, s=5 * tot_weight, lw=0, alpha=alpha, cmap=cm)

    def plot_dos(self, filepath_dos,
                 mask_groups, mask_characters,
                 select_groups, interstitial, all_characters,
                 ax, fix_xlim=True):
        """Placeholder function.

        Notes:
        =====
        This is placeholder function.
        Though CP has added code 180109 for plotting the DOS,
        this is for txt DOS example file.
        The plot function here though will expect the DOS info
        to lie in the same hdf file the bandstructure has been
        read from.
        Until that is implemented, the GUI will not have a DOS plot.

        TODO This is a different matplot than the bandstructure matplot! How to handle that?
        :return:
        """

        (E, dos, dos_lim) = get_dos(filepath_dos, self.data,
                mask_groups, mask_characters,
                select_groups, interstitial, all_characters)
        if fix_xlim:
            ylim = (np.min(dos_lim), np.max(dos_lim))
            ax.set_xlim(ylim)
        ax.plot(dos, E)




    def groupVelocity(self, select_band, spin, ax):
        """Plot group velocity of single band, no checking.

        Notes
        =====
        TODO This is a different matplot than the bandstructure matplot! How to handle that?

        :param select_band: index of user-selected band
        :param spin: 0 or 1
        :param ax: of plot
        :return:
        """
        k = self.data.k_distances
        E_iso = self.data.eigenvalues[spin].T[select_band]
        ax.plot(k, E_iso, label="E_iso")

        dE = np.zeros(len(E_iso) - 2)
        # E_iso = np.sin(k) ** 2
        dE = (E_iso[2:] - E_iso[0:-2]) / (k[2:] - k[:-2])
        ax.plot(k[1:-1], dE, label="dE/dk")


class AtomsGroupPlot_Ipyvolume(Plot):
    def __init__(self, data: Data):
        raise NotImplementedError
