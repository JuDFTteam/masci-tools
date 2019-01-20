# -*- coding: utf-8 -*-
"""Holds classes for plots using matplotlib.
"""

import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

from studenproject18ws.plot.base import *
from studenproject18ws.dos.reader import get_dos
from masci_tools.vis.plot_methods import single_scatterplot, multiple_scatterplots



class Bandplot(Plot):
    """
    Class for rendering interactive matplotlib plots of the band data in a GUI frontend.
    Examples: Jupyter Notebook or Lab, Tkinter, PyQt, ...

    Examples
    --------

    >>> import matplotlib.pyplot as plt
    >>> from studenproject18ws.hdf.reader import Reader
    >>> from studenproject18ws.hdf.recipes import Recipes
    >>> from studenproject18ws.plot.matplot import Bandplot as Bandplot
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

    def setup_band_labels(self, plt):
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
            self._plot_bands_compare_two_characters(mask_bands, mask_characters, mask_groups, spins[0],
                                                    unfolding_weight_exponent,
                                                    ax, alpha, ignore_atoms_per_group, marker_size)
        else:
            (alphas, colors) = self.get_alphas_colors_for_spin_overlay(spins)
            for spin in spins:
                self._plot_bands_normal(mask_bands, mask_characters, mask_groups, spin,
                                        unfolding_weight_exponent,
                                        ax, colors[spin], alphas[spin], ignore_atoms_per_group, marker_size)

    def _plot_bands_normal(self, mask_bands, mask_characters, mask_groups, spin,
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

    def _plot_bands_compare_two_characters(self, mask_bands, mask_characters, mask_groups, spin, unfolding_weight_exponent, ax,
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

    def plot_groupVelocity(self, select_band, spin, ax):
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


class DOSPlot(Plot):
    def __init__(self, data: DataBands, filepaths_dos : list):
        Plot.__init__(self, data)
        self.filepaths_dos = filepaths_dos

    def plot_dos(self, spins,
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
        (alphas, colors) = self.get_alphas_colors_for_spin_overlay(spins, PlotDataType.DOS)
        dos_lims = [None, None]
        for spin in spins:
            (E, dos, dos_lims[spin]) = get_dos(self.filepaths_dos[spin], self.data,
                                        mask_groups, mask_characters,
                                        select_groups, interstitial, all_characters)

            ax.plot(dos, E, color=colors[spin], alpha=alphas[spin])


        if fix_xlim:
            # spins is either [0], [1], or [0,1]
            # if [0,1], get the lowest and largest xlim of both tuples
            dos_lim = dos_lims[0] #
            if (len(spin) == 2):
                dos_lim[0] = min(dos_lims[0][0], dos_lims[1][0])
                dos_lim[1] = max(dos_lims[0][1], dos_lims[1][1])
            ax.set_xlim(dos_lim)


    def plot_dos_masci(self, spins, only_total=False, saveas=r'dos_plot', title=r'Density of states', linestyle='-',
                 marker=None, legend=False, limits=[None, None], ax=None):
        """
        Plot the total density of states from a FLEUR DOS.1 file

        Notes
        -----
        Adapated from masci_tools.vis.plot_methods.
        TODO: adapt colors so that both DOS plots for different spins can be distinguised if more than one spin
        is supplied.

        params:
        """
        for spin in spins:
            doses = []
            energies = []
            # dosmt_total = np.zeros(nData, "d")
            # totaldos = np.zeros(nData, "d")

            # read data from file
            datafile = self.filepaths_dos[spin]  # 'DOS.1'
            data = np.loadtxt(datafile, skiprows=0)

            energy = data[..., 0]
            totaldos = data[:, 1]
            interstitialdos = data[:, 2]
            dosmt_total = totaldos - interstitialdos

            doses = [totaldos, interstitialdos, dosmt_total]
            energies = [energy, energy, energy]
            # xlabel = r'E - E$_F$ [eV]'
            ylabel = r'Energy [eV]'
            xlabel = r'DOS [eV$^{-1}$]'

            if only_total:
                single_scatterplot(energy, totaldos, xlabel, ylabel, title, plotlabel='total dos', linestyle=linestyle,
                                   marker=marker, limits=limits, saveas=saveas, axis=ax)
            else:
                multiple_scatterplots(energies, doses, xlabel, ylabel, title,
                                      plot_labels=['Total', 'Interstitial', 'Muffin-Tin'], linestyle=linestyle,
                                      marker=marker, legend=legend, limits=limits, saveas=saveas, axis=ax)



class BandDOSPlot(Bandplot, DOSPlot):
    def __init__(self, data: DataBands, filepaths_dos : list):
        Bandplot.__init__(self, data)
        DOSPlot.__init__(self, data, filepaths_dos)

    def setup_banddos(self, plt):
        fig_scale = 0.65
        fig_ratio = [12, 6]
        figsize = [fig_scale * el for el in fig_ratio]

        fig = plt.figure(figsize=figsize)
        # order: first add dos plot, then band plot.
        # otherwise labels (.setup() below) will be set on dos instead band plot.
        gs_dos = gridspec.GridSpec(1, 2)
        ax_dos = fig.add_subplot(gs_dos[0, 1])
        gs = gridspec.GridSpec(1, 2)
        ax_bands = fig.add_subplot(gs[0, 0], sharey=ax_dos)
        gs.update(wspace=0, left=0.1, right=1.4)
        gs_dos.update(left=0.6, right=0.9, wspace=0)
        plt.setp(ax_dos.get_yticklabels(), visible=False)
        # gs.tight_layout(fig, rect=[0, 0, 1, 0.97])

        return (fig, ax_bands, ax_dos)

    def plot_bandDOS(self, mask_bands, mask_characters, mask_groups, spins,
                   unfolding_weight_exponent, compare_characters,
                   ax_bands, ignore_atoms_per_group, marker_size,
                     dos_select_groups, dos_interstitial, dos_all_characters,
                     ax_dos, dos_fix_xlim=True):
        self.plot_bands(mask_bands, mask_characters, mask_groups, spins,
                        unfolding_weight_exponent, compare_characters, ax_bands,
                        ignore_atoms_per_group, marker_size)
        self.plot_dos(spins, mask_groups, mask_characters,
                      dos_select_groups, dos_interstitial, dos_all_characters,
                      ax_dos, dos_fix_xlim)



