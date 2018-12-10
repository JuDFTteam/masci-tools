import inspect
import numpy as np
from collections import Counter
from h5py._hl.dataset import Dataset as h5py_Dataset

EXCEPTIONS = [inspect, np, Counter, h5py_Dataset]
"""Mandatory: include all imported types here to avoid malfunction.
Reason: this package uses introspection on all types found in this module.
The ones mentioned here are passed over."""


class Data(object):
    def __init__(self, **kwds):
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
            self.atoms_per_group = np.zeros(max(self.atom_group_keys))
            for i in range(max(self.atom_group_keys)):
                self.atoms_per_group[i] = self.atoms_per_group_dict[i]

        except AttributeError:
            pass

    def count_atom_groups(self):
        return max(self.atoms_group[:])

    def E_i(self, i, spin=0):
        return self.eigenvalues[spin].T[i]

    def weights(self, characters, groups, spin):
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

    def combined_weight(self, characters, groups, spin):
        if (self.bandUnfolding == True):
            return self.weights(characters, groups, spin) * self.bandUnfolding_weights[spin].T[:]
        else:
            return self.weights(characters, groups, spin)



# # For demonstraction purposes:
# # Add Rhubarb.rhubarb, Machiavelli.rhubarb to config BandStructure data_classes_functions and see what happens
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
