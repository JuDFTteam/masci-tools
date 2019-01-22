"""Holds composable output data types (plug-in functions) for the HDF file Reader module."""
import inspect
import copy
from collections import Counter, namedtuple

import matplotlib.pyplot as plt
import numpy as np
from h5py._hl.dataset import Dataset as h5py_Dataset

EXCEPTIONS = [inspect, copy, Counter, namedtuple, plt, np, h5py_Dataset]
"""Mandatory: include all imported types here to avoid malfunction.
Reason: this package uses introspection on all types found in this module.
The ones mentioned here will be passed over."""




class FleurData(object):
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

        # for get_data(), buffer llc_normalized, unfold_weight, unfold_w_exponent, call_count. info see there.
        self.buffer_llc_normalized = None
        self.buffer_unfold_weight = None
        self.buffer_unfolding_weight_exponent = []
        self.buffer_call_count = 0

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


class FleurBandData(FleurData):
    def __init__(self, **kwds):
        FleurData.__init__(self, **kwds)
        self.HARTREE_EV = 27.2114

        # this has to be in a try-except block cause don't know
        # if attributes have already been assigned
        try:
            self.atoms_per_group_dict = Counter(self.atoms_group)
            self.atoms_group_keys = self.atoms_per_group_dict.keys()

            # wrong:
            # self.atoms_per_group = np.zeros(self.num_groups)
            # for i in range(self.num_groups):
            #     self.atoms_per_group[i] = np.count_nonzero(np.array(self.atoms_group) == i)
            # correct, but wrong type (list):
            # self.atoms_per_group = list(self.atoms_per_group_dict.values())
            # correct:
            self.atoms_per_group = np.fromiter(self.atoms_per_group_dict.values(), dtype=float)

            # JW: CP 181124 code
            # self.atoms_per_group = np.zeros(max(self.atom_group_keys))
            # for i in range(max(self.atom_group_keys)):
            #     self.atoms_per_group[i] = self.atoms_per_group_dict[i]

            # JW: CP 181212 code
            (self.num_spin, self.num_k, self.num_e,
             self.num_groups, self.num_char) = self.llikecharge.shape

        except AttributeError:
            pass

    def _get_data(self, mask_bands, mask_characters, mask_groups, mask_spin, unfolding_weight_exponent=1,
                  ignore_atoms_per_group=False):

        # DEVNOTE:
        # this is a wrapper function for get_data_and_weight. If only the exponent changes,
        # don't recumpute but just rescale buffered data.
        # Why is the exponent buffered in a growing list?
        # Turns out that this function is called twice on every user selection change, not once.
        # So buffering a single value, or comparing old and new value (via widget observe) does not work.
        # Instead, have to compare against the second last exponent, cause the last exp. is alwazs the same as
        # the current one.
        # TODO: find out why this function is called twice on any user selection change and correct that.

        # print(f"call_count: {self.buffer_call_count}")
        # print(f"unfolding_weigh_exp: {unfolding_weight_exponent}")
        # print(f"buffered unfolding_weigh_exp: {self.buffer_unfolding_weight_exponent}")

        if (len(self.buffer_unfolding_weight_exponent) > 50):
            self.buffer_unfolding_weight_exponent = []

        if (self.buffer_llc_normalized is None) or \
                ((len(self.buffer_unfolding_weight_exponent) > 1) and (unfolding_weight_exponent == self.buffer_unfolding_weight_exponent[-2])):
            llc_normalized, unfold_weight = self._get_data_and_weight(mask_bands, mask_characters, mask_groups, mask_spin, unfolding_weight_exponent,
                  ignore_atoms_per_group)
            self.buffer_llc_normalized = llc_normalized
            self.buffer_unfold_weight = unfold_weight
            # print("recomputing llc_normalized data")
        else:
            pass
            # print("using buffered llc_normalized data")

        self.buffer_unfolding_weight_exponent.append(unfolding_weight_exponent)
        self.buffer_call_count += 1
        return self.buffer_llc_normalized * (self.buffer_unfold_weight ** unfolding_weight_exponent)

    def _get_data_and_weight(self, mask_bands, mask_characters, mask_groups, mask_spin,
                             unfolding_weight_exponent=1, ignore_atoms_per_group=False):
        """
        processes the data to obtain the weights: this is the function with most significant runtime!
        Each argument is a bool list reflecting the user selection.

        :param ignore_atoms_per_group:
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
        atoms_per_group_copy = copy.deepcopy(self.atoms_per_group)

        # ignores that there are not necessarily equally many atoms in each atom group
        if ignore_atoms_per_group:
            atoms_per_group_red[:] = 1
            atoms_per_group_copy[:] = 1

        # compute normalized weights with tensor product
        llc_redG = np.tensordot(llc_red, atoms_per_group_red, axes=([3], [0]))
        llc_redGC = np.sum(llc_redG, axis=3)
        llc_norm_temp = np.tensordot(llc, atoms_per_group_copy, axes=([3], [0]))
        llc_norm = np.sum(llc_norm_temp, axis=3)
        llc_normalized = llc_redGC / llc_norm

        # consider unfolding weight
        unfold_weight = np.ones_like(llc_normalized)
        if self.bandUnfolding:
            unfold_weight = self.bandUnfolding_weights
            unfold_weight = unfold_weight[mask_spin, :, :]
            unfold_weight = unfold_weight[:, :, mask_bands]
            # unfold_weight = unfold_weight ** unfolding_weight_exponent
            # llc_normalized = llc_normalized * unfold_weight

        return llc_normalized, unfold_weight

    def reshape_data(self, mask_bands, mask_characters, mask_groups, spin, unfolding_weight_exponent,
                     ignore_atoms_per_group=False):
        """
        Reshapes the 2-dimensional field of weights into a 1d array to speed up plotting
        --> avoids to call the scatter plot for every band

        christian's code version 181214

        :param ignore_atoms_per_group:
        :param mask_bands:
        :param mask_characters:
        :param mask_groups:
        :param spin:
        :return:
        """
        mask_spin = self._mask_spin(spin)
        total_weight = self._get_data(mask_bands, mask_characters, mask_groups, mask_spin,
                                      unfolding_weight_exponent, ignore_atoms_per_group)

        # only select the requested spin and bands
        evs = self.eigenvalues[spin, :, mask_bands]

        # to speed up scatter plot, unfold data in one dimension
        (Nk, Ne) = evs.T.shape

        evs_resh = np.reshape(evs, Nk * Ne)

        # weight_resh = np.reshape(total_weight[0].T, Nk * Ne)
        weight_resh = total_weight[0].T.flatten()
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

    def simulate_gui_selection(self, which_spin=[], which_bands=[], which_characters=[], which_groups=[]):
        """
        For testing plotting without gui.
        :return:
        """
        spin=0
        mask_spin = self._mask_spin(which_spin=which_spin)
        mask_bands = self._mask_bands(which_bands=which_bands)
        mask_characters = self._mask_characters(which_characters=which_characters)
        mask_groups = self._mask_groups(which_groups=which_groups)

        Selection = namedtuple('Selection', ['spin',
                                             'mask_spin', 'mask_bands',
                                             'mask_characters', 'mask_groups'])
        return Selection(spin,
                         mask_spin, mask_bands,
                         mask_characters, mask_groups)



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
