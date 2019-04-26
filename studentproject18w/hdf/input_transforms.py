"""Holds the Transform classes for different applications for the HDF file Reader module.

"""
from enum import Enum
import numpy as np
import periodictable

from studentproject18w.hdf import util as util


class CoordinateSystemType(Enum):
    Internal = 1
    Physical = 2


class LatticeType(Enum):
    Bravais = 1  # real space
    Reciprocal = 2


class Transform(object):
    """Base class for Transform functions for HDF file Reader Extract-Transform-Load pipeline.

    This base class holds transform functions useful for all HDF file data extraction application cases.
    For application-specifid transforms, only classes derived from this base should be used or declared.

    Note: if new classes or methods are added, adopt funtion body from existing cases: arguments name, dataset
    are obligatory. Before return transformed dataset, call the base method for updating dependees.

    Note: if a new method introduces new interdependencies between datasets, the DEPENDENCIES dictionary in the
    base class has to be adjusted.

    TODO
    ====
    - Perhaps could be made nicer, more expressive with Python decorators.
    - code could be smart enought to construct DEPENDENCIES list by itself before transformation. Would be safer.
    """
    DEPENDENCIES = {
        'TransformBands.coordinates': ['bravaisMatrix', 'reciprocalCell'],
        'TransformBands.k_distance': ['reciprocalCell', 'k_points'],
        'TransformBands.k_special_points': ['k_distances']
    }
    """Syntax: key = function (depends on) : value = list of datasets (dependees).
       Transform base clas has no functions that are dependend on extracted datasets.   
    """

    def __init__(self):
        """
        """
        # dependee datasets
        # dependee datasets for Band Transforms
        self.reciprocalCell = None
        self.bravaisMatrix = None
        self.k_points = None
        self.k_distances = None

    def _update_dependees(self, name, dataset):
        for dependee_names in self.DEPENDENCIES.values():
            if name in dependee_names:
                setattr(self, name, dataset)

    def id(self, name, dataset):
        """Identity transformation, default.

        :param name: of the dataset
        :type dataset: Dataset or ndarray
        :return: dataset
        """
        transformed = None

        transformed = dataset

        self._update_dependees(name, transformed)
        return dataset

    def attribute(self, name, dataset, attribute):
        """Extracts a specified attribute's value.

        :param name:
        :type dataset: Dataset
        :param attribute: attribute name
        :return:
        """
        transformed = None

        transformed = dataset.attrs[attribute]

        self._update_dependees(name, transformed)
        return transformed

    def attributes(self, name, dataset):
        """Extracts attributes of a dataset as a dict.

        :param name:
        :type dataset: Dataset
        :return: attributes dict
        """
        transformed = None

        transformed = {}
        for key, value in dataset.attrs.items():
            transformed[key] = value

        self._update_dependees(name, transformed)
        return transformed

    def move_to_memory(self, name, dataset):
        """Copies the in-file dataset to an in-memory numpy ndarray.

        In general some sources say it's better and faster to copy HDF5 datasets
        (ie every access is a file access) into an in-memory numpy ndarray.
        Unless the dataset is too large for memory of course.
        It is imperative if the file is opened inside a context manager (a 'with' statement),
        and the dataset will be used outside of that context ('with' statement).

        Note
        ====
        This is equivalent to calling slicer function with arg '[:]'.

        :param name:
        :type dataset: Dataset
        :return: ndarray
        """
        transformed = None

        transformed = dataset[:]

        self._update_dependees(name, transformed)
        return transformed

    def first_element(self, name, dataset):
        transformed = None

        transformed = dataset[0]

        self._update_dependees(name, transformed)
        return transformed

    def slicer(self, name, dataset, slice_arg):
        """Slice dataset.

        Note: h5py Dataset supports only a subset of numpy ndarray slicing.

        :param name:
        :type dataset: Dataset or ndarray
        :param slice_arg: examples: "[0]", "[2::2]", and so on
        :return:
        """
        transformed = None

        transformed = eval("dataset" + slice_arg)

        self._update_dependees(name, transformed)
        return transformed

    def scale_with_constant(self, name, dataset, constant_keywords, constant_unit=1):
        """Scales dataset with scalar=(constant/unit)

        :param name: of dataset
        :type dataset: Dataset or ndarray
        :param constant_keywords: e.g. 'bohr atom radius', selects scipy 'Bohr radius'
        :param constant_unit: e.g. 'angstrom', selects scipy.constants.angstrom
        :return:  scaled dataset
        """
        transformed = None

        scalar = util.constant(constant_keywords).value
        if (isinstance(constant_unit, str)):
            scalar /= util.constant(constant_unit).value
        transformed = dataset * scalar

        self._update_dependees(name, transformed)
        return transformed

    def periodic_elements(self, name, dataset):
        transformed = dataset

        transformed = [periodictable.elements[atomic_number] for atomic_number in dataset]

        self._update_dependees(name, transformed)
        return transformed

class TransformBands(Transform):
    """
    """

    def __init__(self):
        Transform.__init__(self)

    def coordinates(self, name, dataset, lattice, from_coordsys=CoordinateSystemType.Internal.name):
        """Coordinate transforation

        :param name: name of the dataset
        :param dataset:
        :type dataset: Dataset or ndarray
        :param lattice: Bravais or Reciprocal
        :type lattice: LatticeType name, a str
        :param from_coordsys: the 'from' in 'from -> to'
        :type from_coordsys: CoordinateSystemType name, a str
        :return:
        """
        transformed = None

        self._update_dependees(name, dataset)

        # pre-format the Enum name arguments in case not in camel case
        # simple: use function title()
        from_cs = getattr(CoordinateSystemType, from_coordsys.title())
        lt = getattr(LatticeType, lattice.title())
        if from_cs == CoordinateSystemType.Internal:  # to Physical
            if lt == LatticeType.Bravais:
                transformed = np.dot(dataset, self.bravaisMatrix)
            else:
                transformed = np.dot(dataset, self.reciprocalCell.T)
        elif from_cs == CoordinateSystemType.Physical:  # to Internal
            raise NotImplementedError  # TODO

        self._update_dependees(name, transformed)
        return transformed

    def k_distance(self, name, dataset):
        """Get k spacing along the path in the Brillouin Zone.

        Notes
        =====
        Currently, k_points (coordinates)) are not stored in data object,
        but indirectly available via transformer.k_points.

        TODO
        ====
        Change h5extract dict format such that an entry for one h5path can produce
        multiple data attributes, in this case data.k_distances and data.k_points.

        :param name:
        :param dataset:
        :return:
        """
        transformed = None

        self.k_points = self.coordinates(name, dataset, LatticeType.Reciprocal.name)

        kx = self.k_points[:].T[0]
        ky = self.k_points[:].T[1]
        kz = self.k_points[:].T[2]
        transformed = np.zeros(len(kx))  # len(kx) == len(k_points)
        transformed[0] = 0
        for i in range(1, len(kx)):
            transformed[i] = transformed[i - 1] + np.sqrt(
                (kx[i] - kx[i - 1]) ** 2 + (ky[i] - ky[i - 1]) ** 2 + (kz[i] - kz[i - 1]) ** 2)

        self._update_dependees(name, transformed)
        return transformed

    def k_special_points(self, name, dataset):
        transformed = None

        transformed = np.zeros(len(dataset[:]))
        for i in range(len(dataset[:])):
            transformed[i] = self.k_distances[dataset[i] - 1]

        self._update_dependees(name, transformed)
        return transformed
