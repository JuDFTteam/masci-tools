"""Holds composable output data types (plug-in functions) for the HDF file Reader module."""
import inspect
from collections import Counter, namedtuple

import matplotlib.pyplot as plt
import numpy as np
from h5py._hl.dataset import Dataset as h5py_Dataset

EXCEPTIONS = [inspect, Counter, namedtuple, plt, np, h5py_Dataset]
"""Mandatory: include all imported types here to avoid malfunction.
Reason: this package uses introspection on all types found in this module.
The ones mentioned here are passed over."""


class Data(object):
    """Base class for dynamically composable output types for HDF file Reader Extract-Transform-Load pipeline.

    This base class serves as common base for all application-specific data output classes. It this base class
    is used as data output type in a recipe, the resulting object will only have dataset attributes and no
    methods.

    For application-specifid transforms, only classes derived from this base should be used or declared.

    Note: As mentioned in the recipes module, a recipe can compose a new data output type dynamically from
    any combination of classes and functions found in this module, for example, for mixing application cases.

    Note: When defining the __init__ method in a new derived data output class, attributes may be declared,
    and even transformed dataset attributes coming may be accessed. But the latter must take place inside
    a try-except AttributeError region, otherwise the readout will crash. Reason: for checking stuff, the
    reader teomporarily instantiates the data output classes without arguments at one time, so the
    transformed dataset  attributes are missing in that instant. When the reader instantiates again at the end,
    they will be present and the access will work.
    """

    def __init__(self, **kwds):
        """
        :param kwds: entry point for all transformed dataset attributes and additional data output methods
                     specified in recipe and created in reader.
        """
        self.__dict__.update(kwds)

    def move_datasets_to_memory(self):
        """Converts all attributes of type h5py Dataset (in-file) to numpy ndarray (in-memory).

        The Data instance is usually created inside a context manager (with statement)
        with an open HDF file. All attributes of h5py Dataset are accessed from file.
        When the context is closed (the with statement left), the file is closed, and
        these datasets are no longer accessible. If the Data instance should be used
        outside of the file context, call this method before leaving the file context.
        Then all attributes of that type get copied into memory as numpy ndarrays and
        are still accessible later on.

        :return:
        """
        for attr_name, attr in inspect.getmembers(self, predicate=(not inspect.ismethod)):
            if (type(attr) == h5py_Dataset):
                setattr(self, attr_name, attr[:])


class DataBands(Data):
    def __init__(self, **kwds):
        Data.__init__(self, **kwds)
        self.HARTREE_EV = 27.2114
        try:
            self.atoms_per_group_dict = Counter(self.atoms_group)
            self.atom_group_keys = self.atoms_per_group_dict.keys()

            # JW: CP 181124 code
            # self.atoms_per_group = np.zeros(max(self.atom_group_keys))
            # for i in range(max(self.atom_group_keys)):
            #     self.atoms_per_group[i] = self.atoms_per_group_dict[i]

            # JW: CP 181212 code
            (self.num_spin, self.num_k, self.num_e,
             self.num_groups, self.num_char) = self.llikecharge.shape
            self.atoms_per_group = np.zeros(self.num_groups)
            for i in range(self.num_groups):
                self.atoms_per_group[i] = np.count_nonzero(np.array(self.atoms_group) == i)

        except AttributeError:
            pass

    def _get_data(self, mask_bands, mask_characters, mask_groups, mask_spin, unfolding_weight_exponent=1):
        """
        processes the data to obtain the weights: this is the function with most significant runtime!
        Each argument is a bool list reflecting the user selection.

        :param mask_bands: bool list for selected bands
        :param mask_characters: bool list for [s,p,d,f]
        :param mask_groups: bool list for selected atom groups
        :param mask_spin: bool list for selected spins [-1/2,1/2]
        :return:
        """
        # filter arrays in bands and spin:
        llc = self.llikecharge[mask_spin, :, :, :, :]
        llc = llc[:, :, mask_bands, :, :]
        # reduce the arrays in Character, Spin, Group
        # llc_red = llc[SPIN_FILTER, :, :, :, :]
        llc_red = llc[:, :, :, mask_groups, :]
        llc_red = llc_red[:, :, :, :, mask_characters]
        # llc_red = llc_red[:, :, BAND_FILTER, :, :]
        atoms_per_group_red = self.atoms_per_group[mask_groups]

        # compute normalized weights with tensor product
        llc_redG = np.tensordot(llc_red, atoms_per_group_red, axes=([3], [0]))
        llc_redGC = np.sum(llc_redG, axis=3)
        llc_norm_temp = np.tensordot(llc, self.atoms_per_group, axes=([3], [0]))
        llc_norm = np.sum(llc_norm_temp, axis=3)
        llc_normalized = llc_redGC / llc_norm

        # consider unfolding weight
        if self.bandUnfolding:
            unfold_weight = self.bandUnfolding_weights
            unfold_weight = unfold_weight[mask_spin, :, :]
            unfold_weight = unfold_weight[:, :, mask_bands]
            unfold_weight = unfold_weight ** unfolding_weight_exponent
            llc_normalized = llc_normalized * unfold_weight

        return llc_normalized

    def reshape_data(self, mask_bands, mask_characters, mask_groups, spin, unfolding_weight_exponent):
        """
        Reshapes the 2-dimensional field of weights into a 1d array to speed up plotting
        --> avoids to call the scatter plot for every band

        christian's code version 181214

        :param mask_bands:
        :param mask_characters:
        :param mask_groups:
        :param spin:
        :return:
        """
        mask_spin = self._mask_spin(spin)
        total_weight = self._get_data(mask_bands, mask_characters, mask_groups, mask_spin, unfolding_weight_exponent)

        # only select the requested spin and bands
        evs = self.eigenvalues[spin, :, mask_bands]

        # to speed up scatter plot, unfold data in one dimension
        (Nk, Ne) = evs.T.shape

        evs_resh = np.reshape(evs, Nk * Ne)
        weight_resh = np.reshape(total_weight[0].T, Nk * Ne)
        k_resh = np.tile(self.k_distances, Ne)
        return (k_resh, evs_resh, weight_resh)

    def _mask_spin(self, which_spin):
        """
        In original code, helper to simulate gui selection.  (called 'filter' there)
        :param which_spin:
        :return:
        """
        mask_spin = np.zeros(self.num_spin).astype(bool)
        mask_spin[which_spin] = True
        return mask_spin

    def _mask_characters(self, which_characters=[0, 1, 2, 3]):
        """
        In original code, helper to simulate gui selection.  (called 'filter' there)
        :param which_characters:
        :return:
        """
        CHARACTER_FILTER = np.zeros(4).astype(bool)
        CHARACTER_FILTER[which_characters] = True
        return CHARACTER_FILTER

    def _mask_groups(self, which_groups=[]):
        """
        In original code, helper to simulate gui selection.  (called 'filter' there)
        :param which_groups:
        :return:
        """
        if not which_groups:
            which_groups = range(self.num_groups)
        GROUP_FILTER = np.zeros(self.num_groups).astype(bool)
        GROUP_FILTER[which_groups] = True
        return GROUP_FILTER

    def _mask_bands(self, which_bands=[]):
        """
        In original code, helper to simulate gui selection. (called 'filter' there)
        :param which_bands:
        :return:
        """
        if not which_bands:
            which_bands = range(self.num_e)
        BAND_FILTER = np.zeros(self.num_e).astype(bool)
        BAND_FILTER[which_bands] = True
        return BAND_FILTER

    def simulate_gui_selection(self):
        """
        For testing plotting without gui.
        :return:
        """
        spin = 0
        mask_spin = self._mask_spin(spin)
        mask_bands = self._mask_bands()
        mask_characters = self._mask_characters()
        mask_groups = self._mask_groups()

        Selection = namedtuple('Selection', ['spin',
                                             'mask_spin', 'mask_bands',
                                             'mask_characters', 'mask_groups'])
        return Selection(spin,
                         mask_spin, mask_bands,
                         mask_characters, mask_groups)

    def simulate_plot_setup(self):
        """

        christian's code version 190108

        In original code, called  'configure' and called every time after plot method has been switched. See there.

        Note
        ====
        For interactive plotting, this config may have to be packaged differently.

        :return:
        """
        labels = []
        for label in self.k_special_point_labels:
            label = label.decode("utf-8")
            if (label == "g"):
                labels += ["$\Gamma$"]
            else:
                labels += str(label)

        plt.xticks(self.k_special_points, labels)
        plt.ylabel("E(k) [eV]")
        plt.xlim(0, max(self.k_distances))
        plt.hlines(0, 0, max(self.k_distances), lw=0.1)

    def simulate_plot(self, mask_bands, mask_characters, mask_groups, spin, unfolding_weight_exponent, ax, color,
                      alpha=1):
        """Plot regular.

        Static plot method as template for interactive plot function in GUI.

        christian's code version 181214

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
        (k_r, E_r, W_r) = self.reshape_data(mask_bands, mask_characters, mask_groups, spin, unfolding_weight_exponent)
        # just plot points with minimal size of t
        speed_up = True
        if (speed_up == True):
            t = 1e-4
            k_r = k_r[W_r > t]
            E_r = E_r[W_r > t]
            W_r = W_r[W_r > t]
        ax.scatter(k_r, (E_r - self.fermi_energy) * self.HARTREE_EV,
                   marker='o', c=color, s=5 * W_r, lw=0, alpha=alpha)

    def simulate_plot_two_characters(self, mask_bands, mask_characters, mask_groups, spin, unfolding_weight_exponent,
                                     ax, alpha=1):
        """Plot with exactly 2 selected band characters mapped to colormap.

        Static plot method as template for interactive plot function in GUI.
        Note: right now, selection (s,p) = [True,True,False,False] is hardcoded!

        christian's code version 190108

        Notes
        =====
        The conversion mask_characters -> characters -> self.mask_characters() looks a bit stringe.
        Probably could be done simpler with a list comprehension.

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

        (k_resh, evs_resh, weight_resh) = self \
            .reshape_data(mask_bands, mask_characters=self._mask_characters([characters[0]]),
                          mask_groups=mask_groups, spin=spin, unfolding_weight_exponent=1)

        (k_resh2, evs_resh2, weight_resh2) = self \
            .reshape_data(mask_bands, mask_characters=self._mask_characters([characters[1]]),
                          mask_groups=mask_groups, spin=spin, unfolding_weight_exponent=1)

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
        ax.scatter(k_resh2, (evs_resh - self.fermi_energy) * self.HARTREE_EV, marker='o', c=rel, s=5 * tot_weight,
                   lw=0,
                   alpha=alpha, cmap=cm)

    def simulate_plot_dos(self):
        """
        This is placeholder function.
        Though CP has added code 180109 for plotting the DOS,
        this is for txt DOS example file.
        The plot function here though will expect the DOS info
        to lie in the same hdf file the bandstructure has been
        read from.
        Until that is implemented, the GUI will not have a DOS plot.
        :return:
        """
        pass

    def simulate_plot_groupVelocity(self, select_band, spin, ax):
        """

        :param select_band: index of user-selected band
        :param spin: 0 or 1
        :param ax: of plot
        :return:
        """
        k = self.k_distances
        E_iso = self.eigenvalues[spin].T[select_band]
        ax.plot(k, E_iso, label="E_iso")

        dE = np.zeros(len(E_iso)-2)
        E_iso = np.sin(k)**2
        dE = (E_iso[2:] - E_iso[0:-2]) / (k[2:] - k[:-2])
        ax.plot(k[1:-1], dE, label="dE/dk")

# #
# # For demonstraction purposes of how Recipes work:
# #
# # Add Rhubarb.rhubarb, Machiavelli.rhubarb to recipe BandStructure data_classes_functions and see what happens
# class Rhubarb(object):
#     def rhubarb(self):
#         print("rhubarb! rhubarb!")
#
#     def count_atom_groups(self):
#         print("more rhubarb.")
#
#
# class Macchiavelli(object):
#     def rhubarb(self):
#         print("rabarbaro! rabarbaro!")
