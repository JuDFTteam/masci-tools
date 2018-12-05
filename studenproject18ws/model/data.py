# -*- coding: utf-8 -*-
"""

Notes
=====
Benefit of all this:
- together, the Reader, Transform and Data classes become a utility that can  be reused
  for any kind of hdf5 file readout (extraction, transform, load). all that has to be changed
  is the h5extract dict / JSON.
- benefit of the namedtupple as data output over directly using the dict: autompletion, refactoring
  works (in an IDE), no input clutter.
"""
import os
import ntpath

import numpy as np
import h5py
from h5py._hl.dataset import Dataset
from numpy import ndarray
from collections import namedtuple
from enum import Enum

import studenproject18ws.model.util as util
from studenproject18ws.model.exceptions import Hdf5_DatasetNotFoundError


class ExtractType(Enum):
    """
    TODO
    =====
    See Transform TODO.
    """
    FromDict = 1
    FromFile = 2


class CoordinateSystemType(Enum):
    Internal = 1
    Physical = 2


class LatticeType(Enum):
    Bravais = 1  # real space
    Reciprocal = 2


class Transform(object):
    """Functions to transform raw h5py Datasets.

    TODO
    ====
    - Perhaps could be made nicer, more expressive with Python decorators.
    - Right now, the dict received expects that all objects in the dict
      (Transform functions, etc.) are referred by name (str). So can be
      deserialized from a file (JSON), OR be a dict defined in program.
      For the latter, function.__name__, an_enum.name and so on have to be used.
      Would be nicer, if could use object directly, so function, an_enum.
      For that have to implement a switchher, could perhaps also be done
      with a decorator.
    """
    DEPENDENCIES = {  # function dependent on : datasets (dependeees)
        'coordinates': ['bravaisMatrix', 'reciprocalCell'],
        'k_distance': ['reciprocalCell'],
        'k_special_points': ['k_distances']
    }

    def __init__(self, extract_type=ExtractType.FromDict):
        """


        """
        self.extract_type = extract_type
        # dependee datasets
        self.reciprocalCell = None
        self.bravaisMatrix = None
        self.k_points = None
        self.k_distances = None

    def _update_dependees(self, name, dataset):
        for dependee_names in self.DEPENDENCIES.values():
            if name in dependee_names:
                setattr(self, name, dataset)

    def id(self, name, dataset):
        self._update_dependees(name, dataset)
        return dataset

    def move_to_memory(self, name, dataset):
        """Copies the in-file dataset to an in-memory numpy ndarray.

        In general some sources say it's better and faster to copy HDF5 datasets
        (ie every access is a file access) into an in-memory numpy ndarray.
        Unless the dataset is too large for memory of course.
        It is imperative if the file is opened inside a context manager (a 'with' statement),
        and the dataset will be used outside of that context ('with' statement).

        Note
        ====
        This is equivalent to calling slice function with arg '[:]'.

        :param name:
        :type dataset: Dataset
        :return: ndarray
        """
        transformed = dataset[:]
        self._update_dependees(name, transformed)
        return transformed

    def first_element(self, name, dataset):
        transformed = dataset[0]
        # self._update_dependees(name, transformed)
        return transformed

    def slicer(self, name, dataset, slice_arg):
        """Slice dataset .

        Note: h5py Dataset supports only a subset of numpy ndarray slicing.

        :param name:
        :type dataset: Dataset or ndarray
        :param slice_arg: examples: "[0]", "[2::2]", and so on
        :return:
        """
        transformed = eval("dataset" + slice_arg)
        self._update_dependees(name, transformed)
        return transformed

    def attribute(self, name, dataset, attribute):
        """

        :param name:
        :type dataset: Dataset
        :param attribute:
        :return:
        """
        pass
        transformed = dataset.attrs[attribute]
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

    def coordinates(self, name, dataset, lattice, from_coordsys=CoordinateSystemType.Internal.name):
        """Coordinate transforation

        :param name: name of the dataset
        :param dataset:
        :type dataset: Dataset or ndarray
        :param lattice: from -> to
        :type lattice: LatticeType name, so a str
        :param from_coordsys: from ->to
        :type from_coordsys: CoordinateSystemType name, so a str
        :return:
        """
        transformed = None

        self._update_dependees(name, dataset)
        from_cs = getattr(CoordinateSystemType, from_coordsys)
        lt = getattr(LatticeType, lattice)
        if from_cs == CoordinateSystemType.Internal:  # to Physical
            if lt == LatticeType.Bravais:
                transformed = np.dot(dataset, self.bravaisMatrix)
            else:
                transformed = np.dot(dataset, self.reciprocalCell)
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
        transformed = np.zeros(len(dataset[:]))
        for i in range(len(dataset[:])):
            transformed[i] = self.k_distances[dataset[i] - 1]

        self._update_dependees(name, transformed)
        return transformed


class ReaderGeneric(object):
    """
    Idea: reader receives:
    - a h5 file
    - a dict with h5py groups as keys and values:
      - a Transform function to apply
      - a list or tuple of Transform functions to apply sequentially
      - a dict with values Transform functions as keys and values:
        - arguments for the respective transform functions
    """

    def __init__(self, filepath):
        """

        :param filepath: relative or absolute filepath
        :type filepath: str
        """
        self._f_path = filepath
        self.filename = ntpath.basename(filepath)
        self.filename = os.path.splitext(self.filename)[0]
        self.transformer = Transform()

    def __enter__(self):
        # trysetattr etc goes here
        self._f = h5py.File(self._f_path, 'r')
        return self._f

    def __exit__(self, type, value, traceback):
        # exception handling goes here
        self._f.close()

    def _dataset(self, h5path, safe=False):
        """

        Parameters
        ----------
        h5path : str
            HDF5 group path in file.

        Returns
        -------
        Dataset
            h5py.Dataset

        Raises
        ------
        Hdf2Mic_HDF5DatasetNotFoundError
            if file has no such Dataset
        """
        if h5path == '/' or h5path == '':
            if safe:
                return None
            else:
                pass

        dset = self._f.get(h5path)
        if dset is not None:
            return dset
        elif not safe:
            raise Hdf5_DatasetNotFoundError('ERROR: HDF5 input file {} has no Dataset at {}. Aborting.'
                                            .format(self._f.filename, h5path))
        return None

    def read(self, h5extract: dict):

        # TODO: check dict format

        # remove entries whose key is an empty string
        h5extract = {key: val for key, val in h5extract.items() if key}

        dataset_names = list(h5extract.keys())  # not equal to HDF5 Dataset names (last part of h5path)!

        # get h5 datasets
        h5paths = [item['h5path'] for item in list(h5extract.values())]
        datasets = list(map(lambda h5path: self._dataset(h5path), h5paths))
        print("Loaded datasets.")

        # get Transform function names and/or arguments
        transforms = [item['transforms'] for item in list(h5extract.values())]

        # TODO: pre-check: is there is a transform dependency that cannot be satisfied?
        # this is the case if there is a dependee dataset that's not in the list of read-in datasets.
        # But the check must not include all dependencies listed in Transform, but only those that
        # are going to be used. That means those, whose respective Transform functions are actually
        # going to be called.
        transform_names_set = set(
            [item for sublist in  # flattens list of lists
             [[tf[0] if isinstance(tf, list) else tf for tf in tfsub]  # get tf name, discard tf arg names
              for tfsub in transforms]  # for each dataset's list of transforms
             for item in sublist]  # flattens list of list
        )
        dataset_names_set = set(dataset_names)
        differences = {}
        for transform_name, dependees in Transform.DEPENDENCIES.items():
            if transform_name in transform_names_set:
                difference = set(dependees) - dataset_names_set
                if difference:
                    differences[transform_name] = difference
        if differences:
            raise ValueError(f"Cannot extract & transform data: the input dictionary specifies transforms "
                             f"with unmet dependencies (needed datasets not specified in the extract): \n"
                             f"{differences}")

        # now loop over the datasets until all are transformed. First do those
        # with no Transform dependencies, skip those with dependencies. Then
        # do the latter ones until all dependencies are satisifed.
        transformed = set()
        i = 0
        i_noncyclic = 0
        print("Transforming datasets:")
        while (len(transformed) < len(datasets) and (i_noncyclic < 20)):
            print(f"i = {i}, dataset = '{dataset_names[i]}', h5path = '{h5paths[i]}',"
                  f" transform = '{transforms[i]}':")
            if (dataset_names[i] in transformed):
                print(f"\tdataset '{dataset_names[i]}'' is already transformed, continue.")
            else:
                difference = []  # list of dependee datasets for transformations
                print("\tcheck dependencies:")
                for transform in transforms[i]:
                    # extract transform function names list (in case one of them has args and this is list)
                    transform_name = transform[0] if isinstance(transform, list) else transform
                    print(f"\t\tfor transform_function: '{transform_name}'")
                    if (transform_name in Transform.DEPENDENCIES.keys()):
                        # now have to check: is the dependency resolved?
                        # I.e. are all dependee-datasets already transformed.
                        dependees = Transform.DEPENDENCIES[transform_name]  # list
                        if set(dependees).issubset(transformed):
                            pass
                        else:
                            difference.extend(set(dependees) - transformed)
                            print(f"\tis dependent on untransformed datasets {difference}, try next dataset first")
                            break
                if (not difference):
                    print("\tnot dependent or all dependencies satisfied, transform:")
                    for transform in transforms[i]:
                        transform_name = transform
                        transform_args = [dataset_names[i], datasets[i]]
                        if isinstance(transform, list):
                            transform_name = transform[0]
                            transform_args.extend(transform[1:])
                        transform_function = getattr(self.transformer, transform_name)
                        print(f"\t\ttransform_function: '{transform_name}', transform_args: '{transform_args}'")
                        datasets[i] = transform_function(*transform_args)
                        transformed.add(dataset_names[i])
                    print(f"\ttransformed dataset '{dataset_names[i]}'.")
            i = (i + 1) % len(datasets)
            i_noncyclic += 1

        # creaet namedtyple type, values will be the transformed datasets
        Data = namedtuple('Data', dataset_names)
        print(f"dsets: len = {len(datasets)}, attr_names = {dataset_names}")
        data = Data(*datasets)
        return data


# %% definitions

h5extract = {
    "eigenvalues": {
        "h5path": "/eigenvalues/eigenvalues",
        "description": f"'E_n sampled at discrete k values stored in 'kpts'",
        "transforms": [Transform.id.__name__]
    },
    "llikecharge": {
        "h5path": "/eigenvalues/lLikeCharge",
        "description": f"Something related to the projection on s,p,d,f,... orbitals...",
        "transforms": [Transform.id.__name__]
    },
    "atoms_position": {  # template entry
        "h5path": "/atoms/positions",
        "description": f"Atom coordinates",
        "transforms": [[Transform.coordinates.__name__, LatticeType.Bravais.name]]
    },
    "k_distances": {
        "h5path": "/kpts/coordinates",
        "description": f"k spacing along the path in the Brillouin zone. "
                       f"(Note: k_points are currently not stored, but available after"
                       f"transform via transformer.k_points. k_points are 3d coordinates "
                       f"of the path along which E_n(kx, ky, kz) is sampled. See k_distance"
                       f"function if this should be changed.)"
                       f"",
        "transforms": [Transform.k_distance.__name__]
    },
    "k_special_points": {
        "h5path": "/kpts/specialPointIndices",
        "description": f"high symmetry points k-values",
        "transforms": [Transform.k_special_points.__name__]
    },
    "k_special_point_labels": {  # template entry
        "h5path": "/kpts/specialPointLabels",
        "description": f"high symmetry points labels",
        "transforms": [Transform.id.__name__]
    },
    "fermi_energy": {  # template entry
        "h5path": "/general",
        "description": f"fermi_energy of the system",
        "transforms": [[Transform.attribute.__name__, 'lastFermiEnergy'],
                       [Transform.slicer.__name__, '[0]']]
    },
    "bravaisMatrix": {
        "h5path": "/cell/bravaisMatrix",
        "description": f"Coordinate transformation internal to physical for atoms",
        "transforms": [Transform.move_to_memory.__name__,
                       [Transform.scale_with_constant.__name__, "bohr radius", "angstrom"]
                       ]
    },
    "reciprocalCell": {
        "h5path": "/cell/reciprocalCell",
        "description": f"Coordinate transformation internal to physical for k_points",
        "transforms": [Transform.move_to_memory.__name__]
    },
    "": {  # template entry
        "h5path": "",
        "description": f"",
        "": [Transform.id.__name__]
    },
}

# filename = 'banddos_4x4.hdf'
filename = 'banddos.hdf'
# filename = 'banddos_Co.hdf'

filepath = ['..', 'data', 'input', filename]
filepath = os.path.join(*filepath)
reader = ReaderGeneric(filepath)

data = None
with reader as h5file:
    data = reader.read(h5extract)
    print("success")
    #
    # Note:
    # Inside the with statement (context manager),
    # all HDF5 datasets are available. When the statement is left,
    # the HDF5 file gets closed and the datasets are closed.
    # Should they be left available, apply Transform.to_memory to them.
    #
    print(len(data.k_distances))
    print(len(reader.transformer.k_points))
# Left HDF5 file with statement: file and all open datasets are now closed.

# here
# %% example code
