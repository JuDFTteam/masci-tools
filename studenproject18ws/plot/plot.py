# -*- coding: utf-8 -*-
"""Holds classes for plots of the self.data.

Each class is for a different type of plot utility. For instance, matploblib plots
are gathered in the class Matplot.

"""

import logging
import numpy as np
import matplotlib.pyplot as plt

from studenproject18ws.hdf.output_types import *


class Matplot(object):
    def __init__(self, data: Data):
        """
        Sets up plot axis according to data.

        :param data:
        """
        self.data = data

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

    def bands(self, mask_bands, mask_characters, mask_groups, spin, unfolding_weight_exponent, ax, alpha=1,
              ignore_atoms_per_group=False):
        """Plot regular.

        Static plot method as template for interactive plot function in GUI.

        christian's code version 181214

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
        color = "blue"
        (k_r, E_r, W_r) = self.data.reshape_data(mask_bands, mask_characters, mask_groups, spin,
                                                 unfolding_weight_exponent, ignore_atoms_per_group)
        # just plot points with minimal size of t
        speed_up = True
        if (speed_up == True):
            t = 1e-4
            k_r = k_r[W_r > t]
            E_r = E_r[W_r > t]
            W_r = W_r[W_r > t]
        ax.scatter(k_r, (E_r - self.data.fermi_energy) * self.data.HARTREE_EV,
                   marker='o', c=color, s=5 * W_r, lw=0, alpha=alpha)

    def bands_two_characters(self, mask_bands, mask_characters, mask_groups, spin, unfolding_weight_exponent, ax,
                             alpha=1, ignore_atoms_per_group=False):
        """Plot with exactly 2 selected band characters mapped to colormap.

        Static plot method as template for interactive plot function in GUI.
        Note: right now, selection (s,p) = [True,True,False,False] is hardcoded!

        christian's code version 190108

        Notes
        =====
        The conversion mask_characters -> characters -> self.mask_characters() looks a bit strange.
        Probably could be done simpler with a list comprehension.

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
        if (speed_up == True):
            t = 1e-4
            k_resh2 = k_resh2[tot_weight > t]
            evs_resh = evs_resh[tot_weight > t]
            rel = rel[tot_weight > t]
            tot_weight = tot_weight[tot_weight > t]

        # print(len(tot_weight))
        # print(len(k_resh2))
        # print(len(rel))
        # print(len(evs_resh))

        # cm = plt.cm.get_cmap('RdYlBu')
        # cm = plt.cm.winter
        cm = plt.cm.plasma
        ax.scatter(k_resh2, (evs_resh - self.data.fermi_energy) * self.data.HARTREE_EV, marker='o', c=rel,
                   s=5 * tot_weight,
                   lw=0,
                   alpha=alpha, cmap=cm)

    def dos(self):
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
        pass

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
