"""
What I want to be able to do:

input: a dict / JSON:
key = Data attribute name,
value =
2) list of transform function names; those with arguments are lists: (fct_name, args...).
Example:
h5extract = {
   'reciprocalCell' : ['values'],
  'eigenvalues' : ['id'],
  'atomPositions' : ['internal2Physical'],
  'fermiEnergy' :  [['attribute', 'lastFermiEnergy'], 'first'],
  ...
}
Need a multi-dict to store 2 values:
- (list of) Transform functions for each key
- h5 group path for each key
Or, do it like this with a fixed format:
h5extract = {
  DataAttrName1 : {
      'h5path' : h5path,
      'transforms': listOfTransformFunctions
  },
  DataAttrName2
  ...
}

Reader takes in h5stuff dictionary.
r = Reader(h5file, h5extract)
Internally, does this:

- rInit) init a data 'Data' object as a namedtuple (google it) with the list of keys from h5extract
- rExtract) init a a list of h5py Datasets from 'h5path', and read-in each Dataset from file
- rTransform) for each Dataset, apply the corresponding list of 'transforms' sequentially on the Dataset,
  store the result in the namedtuple data object under the attribute name of the respective key.
  Eg transformX(Dataset), and transformX(*[Dataset, transformXArgs]), where * is the splat operator.

Benefit of all this:
- together, the Reader, Transform and Data classes become a utility that can  be reused
  for any kind of hdf5 file readout (extraction, transform, load). all that has to be changed
  is the h5extract dict / JSON.

Difficulties:
- dependencies. Here, rec_cell and bravais must be already read in and passed to Transform
  (best in constructor) so the coord transform functions are callable. That means, the order
  of the processing of h5extract kv pairs is important. independent ones must be *transformed* before
  dependent ones are transformed.
  Can think of two solutions right now:
  a) OrderedDict (insertion order; can be made py2 compatible. Question: what if dict deserialized
     from JSON?).
  b) Transform has a dict like this: dependencies = { fctName : h5ExtractKey }. With that,
     the iteration in Reader step rTransform), goes like this: i have key, now i go through it's trasnform fcts.
     For fct 'fctName', I do a lookup in depencies. If there's a hit, I will transform 'h5ExtractKey'
     first, and then 'x'. This sounds like a recursive call.

Drawbacks:
- autcompletion might not work on data object. The only advantage to just using a dict is that
  refactoring still works.
- this scheme sounds very complicated. could be easier to just go with 'explicit is better than implicit'
  and write a specific Reader for each application case, with more flexibility (Transform puts a limit
  on transforming functions, probably must be extended often) and less interdependency.
  Probably there will not be so much different application cases (requiring different hdf5 data subsets)
  in any case.
"""
import os
import ntpath

import numpy as np
import h5py
from h5py._hl.dataset import Dataset
from collections import namedtuple
from enum import Enum

import studenproject18ws.model.util as util
from studenproject18ws.model.exceptions import Hdf5_DatasetNotFoundError


class ExtractType(Enum):
    FromDict = 1
    FromFile = 2

class CoordinateSystemType(Enum):
    Internal = 1
    Physical = 2

class LatticeType(Enum):
    Bravais = 1 # real space
    Reciprocal = 2


class Transform(object):
    """
    Idea:
    Functions to transform raw h5py Datasets. 
    """
    DEPENDENCIES = {
        'coordinates': ['bravaisMatrix', 'reciprocalCell'],
    }

    def __init__(self, extract_type=ExtractType.FromDict):
        """

        :type bravais: Dataset
        """
        self.extract_type = extract_type
        self.reciprocal_cell = None
        self.bravais_matrix = None
        self.k_dist = None

    def _check_dependency(self, name, dataset):
        for dependent_names in self.DEPENDENCIES.values():
            if name in dependent_names:
                setattr(self, name, dataset)

    def id(self, name, dataset):
        self._check_dependency(name, dataset)
        return dataset

    def to_ndarray(self, name, dataset):
        self._check_dependency(name, dataset)
        return dataset[:]

    def first(self, name, dataset):
        self._check_dependency(name, dataset)
        return dataset[0]

    def to_physical_x(self, name, dataset):
        self._check_dependency(name, dataset)
        return np.dot(dataset, self.bravais_matrix)

    def to_physical_k(self, name, dataset):
        self._check_dependency(name, dataset)
        return np.dot(dataset, self.reciprocal_cell)

    def scale_with_constant(self, name, dataset, constant_name):
        self._check_dependency(name, dataset)
        # return dataset * getattr(constants, constant_name)
        return dataset * util.constant(constant_name)[1]

    # def coordinates(self, name, dataset, orig_lattice_type_name, orig_coordsys_type_name=CoordinateSystemType.Internal.name):
    #     self._check_dependency(name, dataset)
    #     if orig_coordsys_type == CoordinateSystemType.Internal: # to Physical
    #         if orig_lattice_type == LatticeType.Bravais:
    #             return np.dot(dataset, self.bravais_matrix)
    #         else:
    #             return np.dot(dataset, self.reciprocal_cell)
    #     elif orig_coordsys_type == CoordinateSystemType.Physical: # to Internal
    #         return dataset #TODO: transform physical to internal coordinates

    def k_special_points(self, name, dataset):
        k_special_pt = np.zeros(len(dataset[:]))
        for i in range(len(dataset[:])):
            k_special_pt[i] = self.k_dist[dataset[i] - 1]
        return k_special_pt


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

        data_attr_names = list(h5extract.keys())

        # get h5 datasets
        h5paths = [item['h5path'] for item in list(h5extract.values())]
        dsets = list(map(lambda h5path: self._dataset(h5path), h5paths))

        # get Transform function names and/or arguments
        transforms = [item['transforms'] for item in list(h5extract.values())]

        # now loop over the datasets until all are transformed. First do those
        # with no Transform dependencies, skip those with dependencies. Then
        # do the latter ones until all dependencies are satisifed.
        transformer = Transform()
        transformed = []
        i = 0
        while (len(transformed) < len(dsets)):
            print(f"i = {i}, data_attr_name = '{data_attr_names[i]}', h5path = '{h5paths[i]}',"
                  f" transform = {transforms[i]}")
            dependent = False
            print("check dependencies:")
            for transform in transforms[i]:
                # extract transform function names list (in case one of them has args and this is list)
                transforms_method_name = transform[0] if isinstance(transform, list) else transform
                print(f"\tfor transform_method_name: {transforms_method_name}")
                if (transforms_method_name in Transform.DEPENDENCIES.keys()):
                    print("... is dependent, continue")
                    dependent = True
                    break
            if (not dependent):
                print("... is not dependent, transform:")
                for transform in transforms[i]:
                    transforms_method_name = transform
                    trans_method_args = [data_attr_names[i], dsets[i]]
                    if isinstance(transform, list):
                        transforms_method_name = transform[0]
                        trans_method_args.extend(transform[1:])
                    trans_method = getattr(transformer, transforms_method_name)
                    print(f"\ttrans_method_name: {transforms_method_name}, trans_method_args: {trans_method_args}")
                    dsets[i] = trans_method(*trans_method_args)
                    print(f"\ttransformed dset {data_attr_names[i]}")
                    transformed += [i]
            i = (i + 1) % len(dsets)

        # creaet namedtyple type, values will be the transformed datasets
        Data = namedtuple('Data', data_attr_names)
        print(f"dsets: len = {len(dsets)}, attr_names = {data_attr_names}")
        data = Data(*dsets)
        return data


# %% definitions

h5extract = {
    "bravaisMatrix": {
        "h5path": "/cell/bravaisMatrix",
        "description": f"Coordinate transformation internal to physical for atoms",
        "transforms": [Transform.to_ndarray.__name__,
                       [Transform.scale_with_constant.__name__, "bohr_radius"]
                       ]
    },
    "reciprocalCell": {
        "h5path": "/cell/reciprocalCell",
        "description": f"Coordinate transformation internal to physical for k_points",
        "transforms": [Transform.to_ndarray.__name__]
    },
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
    # "k_points": {
    #     "h5path": "/kpts/coordinates",
    #     "description": f"3d coordinates of the path along which E_n(kx, ky, kz) is sampled",
    #     "": [Transform.id.__name__]
    # },
    # "k_special_points": {
    #     "h5path": "/kpts/specialPointIndices",
    #     "description": f"k-values of the high symmetry points",
    #     "": [Transform.k_special_points.__name__]
    # },
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

# %% example code
