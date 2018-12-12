"""Holds composable output data types (plug-in functions) for the HDF file Reader module."""
import inspect
from collections import Counter
import deprecated

import matplotlib.pyplot as plt
import numpy as np
from h5py._hl.dataset import Dataset as h5py_Dataset

EXCEPTIONS = [inspect, Counter, plt, np, h5py_Dataset]
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
                self.atoms_per_group[i] = np.count_nonzero(np.array(self.atoms_group)==i)

        except AttributeError:
            pass

    def count_atom_groups(self):
        return max(self.atoms_group[:])

    def E_i(self, i, spin=0):
        return self.eigenvalues[spin].T[i]

    @deprecated
    def weights(self, characters, groups, spin):
        """
        deprecated: christian's code version 181124
        :param characters:
        :param groups:
        :param spin:
        :return:
        """
        weights_reduced = np.zeros((self.eigenvalues.shape[2], len(self.k_points)))
        weights_norm = np.zeros((self.eigenvalues.shape[2], len(self.k_points)))

        # this can surely be improved with matrix product method and sum
        # second loop for normalization is even partially redundant...
        for group in groups:
            for character in characters:
                weights_reduced += self.atoms_per_group_dict[group] * self.llikecharge[spin][:].T[character][group][:]

        for group in range(max(self.atom_group_keys)):
            for character in range(4):
                weights_norm += self.atoms_per_group[group] * self.llikecharge[spin][:].T[character][group][:]

        return weights_reduced / weights_norm

    @deprecated
    def combined_weight(self, characters, groups, spin):
        """
        deprecated: christian's code version 181124
        :param characters:
        :param groups:
        :param spin:
        :return:
        """
        if (self.bandUnfolding == True):
            return self.weights(characters, groups, spin) * self.bandUnfolding_weights[spin].T[:]
        else:
            return self.weights(characters, groups, spin)

    def get_data(self, mask_bands, mask_characters, mask_groups, mask_spin):
        """
        current: christian's code version 181212

        :param mask_bands:
        :param mask_characters:
        :param mask_groups:
        :param mask_spin:
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
            llc_normalized = llc_normalized * unfold_weight

        return llc_normalized

    def create_mask_spin(self, which_spin):
        mask_spin = np.zeros(self.num_spin).astype(bool)
        mask_spin[which_spin] = True
        return mask_spin

    def create_mask_characters(self,which_characters=[0,1,2,3]):
        CHARACTER_FILTER = np.zeros(4).astype(bool)
        CHARACTER_FILTER[which_characters] = True
        return CHARACTER_FILTER

    def create_group_filter(self,which_groups=[]):
        if not which_groups:
            which_groups=range(self.num_groups)
        GROUP_FILTER = np.zeros(self.num_groups).astype(bool)
        GROUP_FILTER[which_groups] = True
        return GROUP_FILTER

    def create_band_filter(self,which_bands=[]):
        if not which_bands:
            which_bands = range(self.num_e)
        BAND_FILTER = np.zeros(self.num_e).astype(bool)
        BAND_FILTER[which_bands] = True
        return BAND_FILTER

    def reshape_data(self, mask_bands, mask_characters, mask_groups, spin):
        """
        current: christian's code version 181212

        :param mask_bands:
        :param mask_characters:
        :param mask_groups:
        :param spin:
        :return:
        """
        mask_spin = self.create_mask_spin(spin)
        total_weight = self.get_data(mask_bands, mask_characters, mask_groups, mask_spin)

        # only select the requested spin and bands
        evs = self.eigenvalues[spin, :, mask_bands]

        # to speed up scatter plot, unfold data in one dimension
        (Nk, Ne) = evs.T.shape

        evs_resh = np.reshape(evs, Nk * Ne)
        weight_resh = np.reshape(total_weight[0].T, Nk * Ne)
        k_resh = np.tile(self.k_distances, Ne)
        return (k_resh, evs_resh, weight_resh)


    def new_plotfunction_weights(self, bands, characters, groups, spin):
        """

        :param bands:
        :param characters:
        :param groups:
        :param spin:
        :return:
        """

        weight_k_n = self.combined_weight(characters, groups, spin)

        fig = plt.figure()
        ax1 = fig.add_subplot(111)

        for n in bands:
            weight_k_n[n]
            ax1.scatter(self.k_distances, self.E_i(n, spin), marker='o', c='b', s=2 * weight_k_n[n], lw=0)

        plt.xticks(self.k_special_points, self.k_special_point_labels)

        """
        for i in range(len(special_points)):
            index = special_points[i]
            plt.vlines(k_dist[index-1], -0.2, 0.4)
        """
        plt.xlim(0, max(self.k_distances))
        return plt

# # For demonstraction purposes:
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
