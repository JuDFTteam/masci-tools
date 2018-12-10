# -*- coding: utf-8 -*-
"""

To be removed. See reader.py instead.

"""

import ntpath
import os

import h5py
import numpy as np

import deprecated # pip install deprecated

import studenproject18ws.hdf.util as util
from studenproject18ws.hdf.exceptions import *

@deprecated
class Reader(object):
    """HDF5 input file reader for band structure plot

     Attributes
     ----------
     filename : str
         The HDF5 file path (relative or absolute) with, file extension.

     Notes
     -----
     Use with a context manager (see example).

     Examples
     --------
     Open a file.

     >>> inputfile = "../data/input/banddos.hdf"
     >>> reader = Reader(inputfile)
     >>> with reader as h5file:
     ...     #read in the
     ...     reader.read()

     TODO
     ----
     If the HDF5 Datasets become large, it might be more efficient to save the HDF5 Dataset (in file) to the data
     attribute rather than copy it into a Numpy array (in memory) and save that. In that case, all subsequent operations
     have to be done within the reader's context manager.

     References
     ----------
         .. [1] xy, 2017.
            URL: https://www.foo.bar
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

    def read(self):

        self.eigenvalues = self._dataset("/eigenvalues/eigenvalues")
        "E_n sampled at discrete k values stored in 'kpts'"

        self.llikecharge = self._dataset("/eigenvalues/lLikeCharge")
        "something related to the projection on s,p,d,f,... orbitals..."

        special_points = self._dataset("/kpts/specialPointIndices")
        "index of the high symmetry points"
        self.k_special_points = self.get_k_special_pt(special_points)
        "k values of the high symmetry points"
        self.special_points_label = self._dataset("/kpts/specialPointLabels")

        self.band_unfolding = self._dataset("/general").attrs['bandUnfolding'][0]
        "unfolding True/False"

        self.weights2 = None
        if (self.band_unfolding):
            self.weights2 = self._dataset("/bandUnfolding/weights")
            "weight for each E_n(k)"

        self.fermi_energy = self._dataset("/general").attrs['lastFermiEnergy'][0]
        "fermi_energy of the system"

        self.weights1 = self._dataset("/kpts/weights")
        "useless quantity"
        self.numFoundEigenvals = self._dataset("/eigenvalues/numFoundEigenvals")
        "useless quantity"
        self.jsym = self._dataset("/eigenvalues/jsym")[0]
        "useless quantity"
        self.ksym = self._dataset("/eigenvalues/ksym")[0]
        "useless quantity"

        self.rec_cell = self._dataset("/cell/reciprocalCell")[:]
        "TODO DOCSTRING"
        self.bravais = self._dataset("/cell/bravaisMatrix")[:] * \
                       (util.constant("bohr radius").value / util.constant("angstrom").value)
        "TODO DOCSTRING"

        atoms_coords_int = self._dataset("/atoms/positions")
        self.atoms_coords = self._internal_to_physical_x(atoms_coords_int)
        "atoms coordinates converted to physical dimensions"
        self.atom_group = self._dataset("/atoms/equivAtomsGroup")
        self.number_atom_groups = max(self.atom_group[:])

        kpts_int = self._dataset("/kpts/coordinates")
        self.kpts = self._internal_to_physical_k(kpts_int)
        "3d coordinates of the path along which E_n(kx, ky, kz) is sampled"
        self.k_dist = self._create_k_spacing()

    def _internal_to_physical_x(self, x_int):
        """bla

        Notes
        ----
        x_ext_ik = A_ij * x_int_jk --> should be correct maybe up to transposition

        :param bravais:
        :return:

        """
        return np.dot(x_int, self.bravais)

    def _internal_to_physical_k(self, k_int):
        return np.dot(k_int, self.rec_cell)

    def _create_k_spacing(self):
        kx = self.kpts_int[:].T[0]
        ky = self.kpts_int[:].T[1]
        kz = self.kpts_int[:].T[2]
        k_dist = np.zeros(len(kx))
        # trivial...
        k_dist[0] = 0

        for i in range(1, len(kx)):
            k_dist[i] = k_dist[i - 1] + np.sqrt(
                (kx[i] - kx[i - 1]) ** 2 + (ky[i] - ky[i - 1]) ** 2 + (kz[i] - kz[i - 1]) ** 2)

        return k_dist

    def get_k_special_pt(self, special_points):
        """Get the k values of the high symmetry points.

        :return:
        """
        k_special_pt = np.zeros(len(special_points[:]))
        for i in range(len(special_points[:])):
            k_special_pt[i] = self.k_dist[special_points[i] - 1]
        return k_special_pt

    def _dataset(self, h5path, safe=False):
        """

        Parameters
        ----------<
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

    def is_number(self, s):
        try:
            return float(s)
        except ValueError:
            return None
