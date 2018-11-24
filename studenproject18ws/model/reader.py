import ntpath
import os

import h5py
import numpy as np

from studenproject18ws.model.exceptions import *


class Reader(object):
    """HDF5 file reader for script hdf2mic.py

     Parameters
     ----------
     filepath : str
         The HDF5 file path (relative or absolute) with, file extension.

     Attributes
     ----------

     Notes
     -----
     Use with a context manager (see example).

     Examples
     --------
     Open a file.

     >>> inputfile = "/foo/bar.h5"
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
         .. [1] xy
            URL: www.foo.bar
     """

    def __init__(self, filepath):
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

        # E_n sampled at discrete k values stored in "kpts"
        self.eigenvalues = self._dataset("/eigenvalues/eigenvalues")

        # something related to the projection on s,p,d,f,... orbitals...
        self.llikecharge = self._dataset("/eigenvalues/lLikeCharge")

        # 3d coordinates of the path along which E_n(kx, ky, kz) is sampled
        self.kpts = self._dataset("/kpts/coordinates")

        # index of the high symmetry points
        self.special_points = self._dataset("/kpts/specialPointIndices")

        # what is this weight good for? <----------------------------------------------
        self.weights1 = self._dataset("/kpts/weights")
        self.weights2 = None

        self.band_unfolding = self._dataset("/general").attrs['bandUnfolding'][0]

        # weight for each E_n(k)
        if (self.band_unfolding):
            self.weights2 = self._dataset("/bandUnfolding/weights")

        # fermi_energy of the system
        self.fermi_energy = self._dataset("/general").attrs['lastFermiEnergy'][0]

        # shape: number of bands per k_pt
        self.numFoundEigenvals = self._dataset("/eigenvalues/numFoundEigenvals")

        self.rec_cell = self._dataset("/cell/reciprocalCell")[:]
        self.bravais = self._dataset("/cell/bravaisMatrix")[:]

        # %%
        # =============================================================================
        # Visualization of the realspace lattice:
        #   - without distinction between atom groups
        #   - with distinction between atom groups
        # =============================================================================

        self.atoms_coords = self._dataset("/atoms/positions")
        self.atom_group = self._dataset("/atoms/equivAtomsGroup")

        self.number_atom_groups = max(self.atom_group[:])
        self.k_dist = self._create_k_spacing()

    def _create_k_spacing(self):
        kx = self.kpts[:].T[0]
        ky = self.kpts[:].T[1]
        kz = self.kpts[:].T[2]
        k_dist = np.zeros(len(kx))
        # trivial...
        k_dist[0] = 0

        for i in range(1, len(kx)):
            k_dist[i] = k_dist[i - 1] + np.sqrt(
                (kx[i] - kx[i - 1]) ** 2 + (ky[i] - ky[i - 1]) ** 2 + (kz[i] - kz[i - 1]) ** 2)

        return k_dist

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

    def is_number(self, s):
        try:
            return float(s)
        except ValueError:
            return None
