###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools.   #
# For further information on the license, see the LICENSE.txt file.           #
# For further information please visit http://judft.de/.                      #
#                                                                             #
###############################################################################
"""This file contains a class to compute the crystalfield
   coefficients from convoluting the charge density with the potential
   which produces the crystalfield. This is both compatible with
   the Yttrium-Analogue approximation and self-consitent calculation of
   the potential

"""
#TODO: Replace double underscore methods for reading
#TODO: Refactor plotting methods to use general plot_methods

from __future__ import annotations

import h5py
import os
import csv
import logging
import tabulate
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path
from scipy.interpolate import interp1d
from scipy.special import sph_harm  #pylint: disable=no-name-in-module
from masci_tools.util.constants import HTR_TO_KELVIN
from masci_tools.io.common_functions import skipHeader
from masci_tools.util.typing import FileLike

from masci_tools.vis.plot_methods import plot_params as mpl_plotter
from masci_tools.vis.parameters import ensure_plotter_consistency, NestedPlotParameters

from typing import NamedTuple, Any
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  #type: ignore[misc]
import warnings

logger = logging.getLogger(__name__)


#This namedtuple is used as the return value for the crystal field calculation to have easy access
#to all the necessary information
class CFCoefficient(NamedTuple):
    """
    Namedtuple representing an individual crystal field coefficient
    """
    l: int
    m: int
    spin_up: float | complex
    spin_down: float | complex
    unit: str
    convention: str


class CFCalculation:
    r"""Class for calculating Crystal Field coefficients using the procedure
    described in C.E. Patrick, J.B. Staunton: J. Phys.: Condens. Matter 31, 305901 (2019)

    Using the formula:
        .. math::
            B_{lm} = \sqrt{\frac{2l+1}{4\pi}} \int^{R_{MT}}\! dr r^2 V_{lm}(r)n_{4f}(r)

        The read in quantities are interpolated from logarithmic meshes to equidistant meshes

        The function constructs an equidistant mesh between 0 and the muffin tin radius
        defined in `self.reference_radius` and with `self.radial_points` points

    :param radial_points: int, number of radial points in the interpolated mesh
    :param reference_radius: stror float; Either 'pot' or 'cdn' or explicit number. Defines which muffin-tin radius
                                is used for the equidistant mesh.
                                IMPORTANT! If txt files are used the muffin-tin radius has to be provided explicitly
    :param coefficient_cutoff: float Defines minimum value that cf coefficients have to have to be considered non-zero

    """

    __version__ = '0.2.0'

    #prefactor for converting Blm to Alm<r^l>
    _alphalm = {
        (0, 0): 1.0,
        (2, 0): 0.5,
        (2, 2): np.sqrt(6.0) / 2.0,
        (4, 0): 1.0 / 8.0,
        (4, 2): np.sqrt(10.0) / 4.0,
        (4, 3): -np.sqrt(35.0) / 2.0,
        (4, 4): np.sqrt(70.0) / 8.0,
        (6, 0): 1.0 / 16.0,
        (6, 2): np.sqrt(105.0) / 16.0,
        (6, 3): -np.sqrt(105.0) / 8.0,
        (6, 4): 3.0 * np.sqrt(14.0) / 16.0,
        (6, 6): np.sqrt(231.0) / 16.0,
    }

    def __init__(self,
                 *,
                 radial_points: int = 4000,
                 reference_radius: float | Literal['pot', 'cdn'] = 'pot',
                 coefficient_cutoff: float | None = 1e-3,
                 **kwargs: Any) -> None:

        self.vlm = {}
        self.cdn = {}

        self.density_normalization: float | None = None
        self.phi: float | None = None
        self.theta: float | None = None

        self.interpolated: bool = False
        self.int = {}
        self.bravaisMat = {}
        self.atom_type: int | None = None

        self.radial_points = radial_points
        self.reference_radius = reference_radius
        self.coefficient_cutoff: float | None = coefficient_cutoff
        self.pot_cutoff = None
        if 'pot_cutoff' in kwargs:
            warnings.warn('The argument pot_cutoff is deprecated. Use cf_cutoff instead', DeprecationWarning)
            self.pot_cutoff = kwargs['pot_cutoff']
        self.only_m0 = False
        if 'only_m0' in kwargs:
            warnings.warn('The argument only_m0 is deprecated.', DeprecationWarning)
            self.only_m0 = kwargs['only_m0']
        if 'quiet' in kwargs:
            warnings.warn('The argument quiet is deprecated.', DeprecationWarning)

    @property
    def denNorm(self):
        """Returns the density normalization

        DEPRECATED: Use density_normalization instead
        """
        return self.density_normalization

    def stevens_prefactor(self, l: int, m: int) -> float:
        """Gives the lm dependent prefactor for conversion between
        Blm and Alm coefficients

        Args:
            :param l: int; orbital quantum number
            :param m: int; magnetic quantum number

        :returns: float prefactor for conversion to Steven's Coefficients
        """
        return self._alphalm.get((l, abs(m)), 0.0)

    def readPot(self, *args, **kwargs):
        """DEPRECATED: Use read_pot"""
        warnings.warn('readPot is deprecated. Use read_potential instead', DeprecationWarning)
        if 'atomType' in kwargs:
            warnings.warn('The argument atomType is deprecated. Use atom_type instead', DeprecationWarning)
            kwargs['atom_type'] = kwargs.pop('atomType')
        if 'complexData' in kwargs:
            warnings.warn('The argument complexData is deprecated. Use complex_data instead', DeprecationWarning)
            kwargs['complex_data'] = kwargs.pop('complexData')
        if 'lm' in kwargs:
            warnings.warn('The argument lm is deprecated. Use lm_indices instead', DeprecationWarning)
            kwargs['lm_indices'] = kwargs.pop('lm')

        self.read_potential(*args, **kwargs)

    def read_potential(self,
                       *files: FileLike | h5py.File,
                       lm_indices: list[tuple[int, int]] | None = None,
                       atom_type: int | None = None,
                       header: int = 0,
                       complex_data: bool = True) -> None:
        """Reads in the potentials for the CF coefficient calculation
        If hdf files are given also the muffin tin radius is read in

        :param args: Expects string filenames for the potentials to read in
                     The function expects either HDF files or txt files with the
                     format (rmesh,vlmup,vlmdn)
        :param lm_indices: list of tuples, Defines the l and m indices for the given txt files
        :param atom_type: int, Defines the atomType to read in (only for HDF files)
        :param header: int, Define how many lines to skip in the beginning of txt file
        :param complex_data: bool, Define if the data in the text file is complex

        Raises:
            ValueError: lm indices list length has to match number of files read in

        """

        if lm_indices is None:
            lm_indices = []

        #Reads in the filenames given in args as potentials
        for index, file in enumerate(files):
            if isinstance(file, (str, Path)):
                _, extension = os.path.splitext(file)
                if extension == '.hdf':
                    with h5py.File(file, 'r') as hdffile:
                        self.__readpotHDF(hdffile, atom_type=atom_type)
                else:
                    if index >= len(lm_indices):
                        raise ValueError('Not enough lm indices for the given files')
                    self.__readpottxt(file, lm_indices[index], header=header, complexData=complex_data)
            else:
                self.__readpotHDF(file, atom_type)

    @classmethod
    def from_arrays(cls, charge_density: np.ndarray, potentials: dict[tuple[int, int], np.ndarray],
                    radial_mesh: dict[str, np.ndarray], **kwargs: Any) -> CFCalculation:
        """
        Create a CFCalculation instance from arrays

        .. warning::
            Using this classmethod will not check that the charge density and potential have the same bravais
            matrix

        :param charge_density: Array for the normed charge density
        :param potentials: Data for the potentials (dict mapping (l,m) tuples to the corresponding data)
        :param radial_mesh: dict for the data for the used radial meshs (keys 'cdn' and 'pot')

        Other Kwargs are passed on to the constructor
        """

        cfcalc = cls(**kwargs)

        cfcalc.cdn['data'] = charge_density
        cfcalc.cdn['rmesh'] = radial_mesh['cdn']
        cfcalc.cdn['RMT'] = np.max(radial_mesh['cdn'])

        cfcalc.vlm = potentials
        cfcalc.vlm['rmesh'] = radial_mesh['pot']
        cfcalc.vlm['RMT'] = np.max(radial_mesh['pot'])

        return cfcalc

    def readCDN(self, *args, **kwargs):
        """DEPRECATED: Use read_charge_density instead"""
        warnings.warn('readCDN is deprecated. Use read_charge_density instead', DeprecationWarning)
        if 'atomType' in kwargs:
            warnings.warn('The argument atomType is deprecated. Use atom_type instead', DeprecationWarning)
            kwargs['atom_type'] = kwargs.pop('atomType')
        self.read_charge_density(*args, **kwargs)

    def read_charge_density(self,
                            file: FileLike | h5py.File,
                            atom_type: int | None = None,
                            header: int = 0,
                            atomic_cdn: bool = True) -> None:
        """Reads in the normed charge density for the CF coefficient calculation
        If hdf files are given also the muffin tin radius is read in

        Parameters:
            :param file: Expects string filename for the charge density to read in
                         The function expects either HDF files or txt files with the
                         format (rmesh,cdn).
                         The charge density should be given as r^2n(r) and normed to 1
        kwargs:
            :param atom_type: int, Defines the atom_type to read in (only for HDF files)
            :param header: int, Define how many lines to skip in the beginning of txt file

        """
        if isinstance(file, (str, Path)):
            _, extension = os.path.splitext(file)
            if extension == '.hdf':
                with h5py.File(file, 'r') as hdffile:
                    self.__readcdnHDF(hdffile, atom_type=atom_type, atomic_cdn=atomic_cdn)
            else:
                if not atomic_cdn:
                    raise ValueError('The complete spherical charge density is not available for txt files')
                self.__readcdntxt(file, header=header)
        else:
            self.__readcdnHDF(file, atom_type=atom_type, atomic_cdn=atomic_cdn)

    def __readpotHDF(self, hdffile, atom_type=None):
        """Read in the potential from a HDF file

        """

        info = hdffile.get('general')
        numPOT = info.attrs['numPOT'][0]
        if 'bravaisMatrix' in info:
            self.bravaisMat['pot'] = np.array(info.get('bravaisMatrix'))

        if numPOT == 0:
            raise ValueError(f'No potentials found in {hdffile}')

        potential_groups = {key for key in hdffile if 'pot-' in key}

        if len(potential_groups) != 1 and atom_type is None:
            raise ValueError('Multiple possibilities for calculated potentials. '
                             f'Select the desired atomType: {potential_groups}')

        if atom_type is not None:
            pot_group = f'pot-{atom_type}'
        else:
            pot_group = potential_groups.pop()
            _, _, atom_type = pot_group.partition('-')

        if self.atom_type is not None and self.atom_type != atom_type:
            logger.warning('atom_type %s for potential does not correspond to previously read in data (%s)', atom_type,
                           self.atom_type)

        if self.atom_type is None:
            self.atom_type = atom_type

        if pot_group in hdffile:
            _pot = hdffile.get(pot_group)

            self.vlm['RMT'] = _pot.attrs['RMT'][0]
            for key in _pot.keys():

                if key == 'rmesh':
                    _rmesh = _pot.get(key)
                    self.vlm['rmesh'] = np.array(_rmesh)
                else:
                    _vlm = _pot.get(key)
                    l = _vlm.attrs['l'][0]
                    m = _vlm.attrs['m'][0]

                    _data = _vlm.get('vlm')
                    _data = np.array(_data[:, :, 0] + 1j * _data[:, :, 1])
                    if self.pot_cutoff is None or abs(_data).max() >= self.pot_cutoff:
                        self.vlm[(l, m)] = _data

        else:
            raise ValueError(f'No potential for atomType {atom_type} found in {hdffile}')

        logger.info('read_potential (HDF): Generated the following information: %s', self.vlm.keys())

    def __readpottxt(self, file, index, header=0, complexData=True):
        """Read in the potential for the (l,m) tuple 'index' from a txt file
        The muffin-tin radius is inferred from the biggest argument in the rmesh
        """

        with open(file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

            if index not in self.vlm:
                self.vlm[index] = []
                self.vlm[index].append([])
                self.vlm[index].append([])
            else:
                raise KeyError(f'Multiple definitions for potential {index}')

            self.vlm['rmesh'] = []

            for line in skipHeader(reader, header):
                while '' in line:
                    line.remove('')
                self.vlm['rmesh'].append(float(line[0]))
                if complexData:
                    self.vlm[index][0].append(float(line[1]) + 1j * float(line[2]))
                    self.vlm[index][1].append(float(line[3]) + 1j * float(line[4]))
                else:
                    self.vlm[index][0].append(float(line[1]))
                    self.vlm[index][1].append(float(line[2]))

            self.vlm[index] = np.array(self.vlm[index])
            self.vlm['rmesh'] = np.array(self.vlm['rmesh'])
            self.vlm['RMT'] = max(self.vlm['rmesh'])

    def __readcdnHDF(self, hdffile, atom_type=None, atomic_cdn=True):
        """Read in the charge density from a HDF file

        """

        info = hdffile.get('general')
        numCDN = info.attrs['numCDN'][0]
        if 'bravaisMatrix' in info:
            self.bravaisMat['cdn'] = np.array(info.get('bravaisMatrix'))

        if numCDN == 0:
            raise ValueError(f'No charge densities found in {hdffile}')

        cdn_groups = {key for key in hdffile if 'cdn-' in key}

        if len(cdn_groups) != 1 and atom_type is None:
            raise ValueError('Multiple possibilities for calculated charge densities. '
                             f'Select the desired atom_type: {cdn_groups}')

        if atom_type is not None:
            cdn_group = f'cdn-{atom_type}'
        else:
            cdn_group = cdn_groups.pop()
            _, _, atom_type = cdn_group.partition('-')

        if self.atom_type is not None and self.atom_type != atom_type:
            logger.warning('atom_type %s for density does not correspond to previously read in data (%s)', atom_type,
                           self.atom_type)

        if self.atom_type is None:
            self.atom_type = atom_type

        if cdn_group in hdffile:
            _cdn = hdffile.get(cdn_group)
            self.cdn['RMT'] = _cdn.attrs['RMT'][0]
            _rmesh = _cdn.get('rmesh')
            self.cdn['rmesh'] = np.array(_rmesh)
            if atomic_cdn:
                _data = _cdn.get('cdn')
                self.cdn['data'] = np.array(_data)
            else:
                _data = _cdn.get('cdn_spherical')
                if _data is None:
                    raise ValueError(f'Complete spherical charge density is not available in {cdn_group}')
                self.cdn['data'] = np.array(_data)
        else:
            raise ValueError(f'No charge density for atom_type {atom_type} found in {hdffile}')

        logger.info('read_charge_density (HDF): Generated the following information: %s', self.cdn.keys())

    def __readcdntxt(self, file, header=0):
        """Read in the charge density from a txt file
        The muffin-tin radius is inferred from the biggest argument in the rmesh
        """

        with open(file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

            if 'data' not in self.cdn:
                self.cdn['data'] = []
            else:
                raise KeyError('Charge density already read in')

            self.cdn['rmesh'] = []

            for line in skipHeader(reader, header):
                while '' in line:
                    line.remove('')

                self.cdn['rmesh'].append(float(line[0]))
                self.cdn['data'].append(float(line[1]))

            self.cdn['data'] = np.array(self.cdn['data'])
            self.cdn['rmesh'] = np.array(self.cdn['rmesh'])
            self.cdn['RMT'] = max(self.cdn['rmesh'])

    def validate(self) -> None:
        """Validate that the object can be used to execute the calculation
        Checks that the given bravais matrices are equal if given
        """

        if 'data' not in self.cdn or 'rmesh' not in self.cdn:
            raise ValueError('Charge density input incomplete')

        if 'rmesh' not in self.vlm or len(self.vlm.items()) <= 2:
            raise ValueError('Potential input incomplete')

        if 'cdn' in self.bravaisMat and 'pot' in self.bravaisMat:
            diffBravais = self.bravaisMat['cdn'] - self.bravaisMat['pot']
            max_diff = np.max(np.abs(diffBravais))
            if max_diff > 1e-8:
                logger.warning('Differing definitions of potentials and charge density bravais matrix. Max. Diff: %f',
                               max_diff)

    def interpolate(self) -> None:
        """Interpolate all quantities to a common equidistant radial mesh

        """

        if self.reference_radius == 'pot':
            refRMT = self.vlm['RMT']
        elif self.reference_radius == 'cdn':
            refRMT = self.cdn['RMT']
        else:
            refRMT = self.reference_radius

        self.int = defaultdict(dict)

        self.int['rmesh'] = np.arange(0.0, refRMT, refRMT / self.radial_points)
        self.int['cdn'] = interp1d(self.cdn['rmesh'], self.cdn['data'], fill_value='extrapolate')

        for key, value in self.vlm.items():
            if key not in ('RMT', 'rmesh'):
                self.int[key]['spin-up'] = interp1d(self.vlm['rmesh'], value[0, :], fill_value='extrapolate')
                if value.shape[0] == 2:
                    self.int[key]['spin-down'] = interp1d(self.vlm['rmesh'], value[1, :], fill_value='extrapolate')
        self.interpolated = True

    def get_coefficients(self,
                         convention: Literal['Stevens', 'Wybourne'] = 'Stevens',
                         table_fmt: str | None = None) -> list[CFCoefficient]:
        """Performs the integration to obtain the crystal field coefficients
        If the data was not already interpolated, the interpolation will
        be performed beforehand

        Parameters:
            :param convention: str of the convention to use (Stevens or Wybourne)
            :param table_fmt: str if not None a table with the given format will be printed using tabulate

        :returns: list of CFCoefficient objects (namedtuple), with all the necessary information
        """

        if convention not in ('Stevens', 'Wybourne'):
            raise ValueError(f'Unknown Crystal field convention: {convention}')

        self.validate()

        if 'cdn' in self.bravaisMat and 'pot' in self.bravaisMat:
            a_vector = self.bravaisMat['pot'][0, :]
            c_vector = self.bravaisMat['pot'][2, :]

            self.theta = np.arccos(c_vector[2] / (np.linalg.norm(c_vector)))
            self.phi = np.arccos(a_vector[0] / (np.linalg.norm(a_vector)))

            logger.info(r'Angle between lattice vector c and z-axis: %f $\pi$', self.theta / np.pi)
            logger.info(r'Angle between lattice vector a and x-axis:  %f $\pi$', self.phi / np.pi)

        if not self.interpolated:
            self.interpolate()

        self.density_normalization = np.trapz(self.int['cdn'](self.int['rmesh']), self.int['rmesh'])
        logger.info('Density normalization = %f', self.density_normalization)

        results = []
        for lmkey, vlm in [(key, val) for key, val in self.int.items() if isinstance(key, tuple)]:
            l, m = lmkey
            if not self.only_m0 or m == 0:
                integral = {}
                for key, pot in vlm.items():
                    integral[key] = np.trapz(
                        pot(self.int['rmesh']) * self.int['cdn'](self.int['rmesh']), self.int['rmesh'])
                    integral[key] *= np.sqrt((2.0 * l + 1.0) / (4.0 * np.pi)) * HTR_TO_KELVIN

                if 'spin-down' not in integral:
                    integral['spin-down'] = integral['spin-up']

                if convention == 'Stevens':
                    integral = {key: val.real * self.stevens_prefactor(l, m) for key, val in integral.items()}

                if self.coefficient_cutoff is not None:
                    if all(np.abs(value) < self.coefficient_cutoff for value in integral.values()):
                        logger.info('Dismissing coefficient for (%i,%i): %s', l, m, integral)
                        continue

                results.append(
                    CFCoefficient(l=l,
                                  m=m,
                                  spin_up=integral['spin-up'],
                                  spin_down=integral['spin-down'],
                                  unit='K',
                                  convention=convention))

        results.sort(key=lambda item: (item.l, abs(item.m)))

        if table_fmt is not None:

            print(f'\nThe following results were obtained with the {convention} convention:')

            results_table = [
                [val for key, val in entry._asdict().items() if key not in ('unit', 'convention')] for entry in results
            ]

            headers = ('l', 'm', 'Spin-Up [K]', 'Spin-Down [K]')
            if table_fmt in ('latex', 'latex_raw'):
                table_fmt = 'latex_raw'
                if convention == 'Stevens':
                    headers = ('l', 'm', r'$A^{\uparrow}_{lm}\langle r^l \rangle$ [K]',
                               r'$A^{\downarrow}_{lm}\langle r^l \rangle$ [K]')
                else:
                    headers = ('l', 'm', r'$B^{\uparrow}_{lm}$ [K]', r'$B^{\downarrow}_{lm}$ [K]')

            print(tabulate.tabulate(results_table, tablefmt=table_fmt, headers=headers))

        return results

    def performIntegration(self, convert=True):
        """DEPRECATED: Use get_coefficients instead

        Performs the integration to obtain the crystal field coefficients
        If the data was not already interpolated, the interpolation will
        be performed beforehand

        Parameters:
            :param convert: bool, converts to Steven's coefficients (if True)

        :returns: list of CFCoefficient objects (namedtuple), with all the necessary information

        """
        warnings.warn('performIntegration is deprecated. Use get_coefficients instead', DeprecationWarning)
        return self.get_coefficients(convention='Stevens' if convert else 'Wybourne')

    @property
    def nonzero_coefficients_lm(self) -> list[tuple[int, int]]:
        """
        Return the lm indices of coefficients that are bigger than the set cutoff
        """
        if self.coefficient_cutoff is None:
            warnings.warn('Coefficient cutoff not set. All coefficients are returned', UserWarning)
        return [(coeff.l, coeff.m) for coeff in self.get_coefficients()]

    @property
    def spin_polarized(self) -> bool:
        """
        Return whether the potentials have a spin-down component
        """
        return any(entry.shape[0] == 2 for key, entry in self.vlm.items() if key not in ('RMT', 'rmesh'))

    def get_potentials(self,
                       spin: Literal['up', 'down'],
                       interpolated: bool = True,
                       only_nonzero: bool = True,
                       complex_data: bool = True) -> tuple[np.ndarray, dict[tuple[int, int], np.ndarray]]:
        """
        Return the potentials and the corresponding radial mesh

        :param spin: which spin to return
        :param interpolated: bool, if True the interpolated mesh and potentials are returned
        :param only_nonzero: bool, if True only the potentials corresponding to a non-zero coefficient are returned
        :param complex_data: bool, if False only the real part of the potentials is returned
        """
        if only_nonzero:
            indices = self.nonzero_coefficients_lm
        else:
            indices = [key for key in self.vlm.keys() if key not in ('RMT', 'rmesh')]

        if interpolated:
            rmesh = self.int['rmesh']
            potentials = {key: self.int[key][f'spin-{spin}'](rmesh) for key in indices}
        else:
            rmesh = self.vlm['rmesh']
            spin_index = 0 if spin == 'up' else 1
            potentials = {key: self.vlm[key][spin_index] for key in indices}

        if not complex_data:
            potentials = {key: pot.real for key, pot in potentials.items()}

        return rmesh, potentials

    def get_charge_density(self, interpolated=True) -> tuple[np.ndarray, np.ndarray]:
        """
        Return the charge density and the corresponding radial mesh

        :param spin: which spin to return
        :param interpolated: bool, if True the interpolated mesh and density are returned
        """

        if interpolated:
            rmesh = self.int['rmesh']
            density = self.int['cdn'](rmesh)
        else:
            rmesh = self.vlm['rmesh']
            density = self.cdn['data']

        return rmesh, density


@ensure_plotter_consistency(mpl_plotter)
def plot_crystal_field_calculation(cfcalc,
                                   *,
                                   saveas='crystal_field_calc',
                                   potential_title='Potential',
                                   density_title='Density',
                                   xlabel='$R$ (Bohr)',
                                   potential_ylabel='$Vpot$ (Hartree)',
                                   density_ylabel='Density',
                                   density_kwargs=None,
                                   potential=True,
                                   density=True,
                                   axis_potential=None,
                                   axis_density=None,
                                   **kwargs):
    """
    Plot the given potentials and charge densities used in the given
    :py:class:`CFCalculation`

    :param cfcalc: CFcalculation containing the data to plot
    :param saveas: str, Define the filename to save the figure
    :param potential_title: Title for the potential subplot
    :param density_title: Title for the charge density subplot
    :param xlabel: label for the x axis of both subplots
    :param potential_ylabel: label for the y axis of the potential subplot
    :param density_ylabel: label for the y axis f the charge density subplot
    :param density_kwargs: dict with keyword argument passed to the plotting of the
                           density
    :param figure: Use this preexisting matplotlib figure to produce the plots

    All other Kwargs are passed on to the :py:func:`~masci_tools.vis.plot_methods.multiple_scatterplots()`
    calls for plotting the potentials
    """
    from masci_tools.vis.plot_methods import multiple_scatterplots

    if density_kwargs is None:
        density_kwargs = {}

    if 'filename' in kwargs:
        warnings.warn('filename is deprecated. Use saveas instead', DeprecationWarning)
        saveas = kwargs.pop('filename')

    if 'pot_ylabel' in kwargs:
        warnings.warn('pot_ylabel is deprecated. Use potential_ylabel instead', DeprecationWarning)
        potential_ylabel = kwargs.pop('pot_ylabel')

    if 'cdn_ylabel' in kwargs:
        warnings.warn('cdn_ylabel is deprecated. Use density_ylabel instead', DeprecationWarning)
        density_ylabel = kwargs.pop('cdn_ylabel')

    if 'pot_title' in kwargs:
        warnings.warn('pot_title is deprecated. Use potential_title instead', DeprecationWarning)
        potential_title = kwargs.pop('pot_title')

    if 'cdn_title' in kwargs:
        warnings.warn('cdn_title is deprecated. Use density_title instead', DeprecationWarning)
        density_title = kwargs.pop('cdn_title')

    if 'save' in kwargs:
        warnings.warn('save is deprecated. Use save_plots instead', DeprecationWarning)
        kwargs['save_plots'] = kwargs.pop('save')

    rmesh, potentials = cfcalc.get_potentials('up', complex_data=False)

    indices, ydata = zip(*sorted(potentials.items(), key=lambda x: x[0]))
    labels = [rf'$V_{{{l}{m}}}$' for l, m in indices]

    figure = None
    if potential and density and axis_potential is None and axis_density is None:
        figure = plt.figure()
        gs = figure.add_gridspec(1, 2)
        axis_potential = figure.add_subplot(gs[0])
        axis_density = figure.add_subplot(gs[1])

    mpl_plotter.single_plot = False
    mpl_plotter.num_plots = len(indices)

    mpl_plotter.set_defaults(
        default_type='function',
        plot_label=labels,
        legend=True,
        legend_options={
            'loc': 'upper left',
            'ncol': 1,
            'borderaxespad': 0.0,
            'linewidth': None,
        },
        marker=None,
        color_cycle=['black', 'red', 'blue', 'orange', 'green', 'purple'],
    )

    save_keys = {'show', 'save_plots', 'save_format', 'save_options'}
    save_options = {key: val for key, val in kwargs.items() if key in save_keys}
    kwargs = {key: val for key, val in kwargs.items() if key not in save_keys}

    mpl_plotter.set_parameters(**save_options)

    if potential:
        with NestedPlotParameters(mpl_plotter):
            axis_potential = multiple_scatterplots(rmesh,
                                                   ydata,
                                                   xlabel=xlabel,
                                                   ylabel=potential_ylabel,
                                                   title=potential_title,
                                                   show=False,
                                                   save_plots=False,
                                                   axis=axis_potential,
                                                   **kwargs)

        mpl_plotter.set_defaults(default_type='function', plot_label=None, linestyle='--', legend=False)

        if cfcalc.spin_polarized:
            rmesh, potentials = cfcalc.get_potentials('down', complex_data=False)

            _, ydata = zip(*sorted(potentials.items(), key=lambda x: x[0]))
            with NestedPlotParameters(mpl_plotter):
                axis_potential = multiple_scatterplots(rmesh,
                                                       ydata,
                                                       xlabel=xlabel,
                                                       ylabel=potential_ylabel,
                                                       title=potential_title,
                                                       show=False,
                                                       save_plots=False,
                                                       axis=axis_potential,
                                                       **kwargs)

    rmesh_int, density_int = cfcalc.get_charge_density()
    rmesh, charge_density = cfcalc.get_charge_density(interpolated=False)

    xdata = [rmesh, rmesh_int]
    ydata = [charge_density, density_int]

    if density:
        mpl_plotter.single_plot = False
        mpl_plotter.num_plots = 2

        mpl_plotter.set_defaults(default_type='function',
                                 plot_label=[r'$n(r)$', None],
                                 linestyle=['-', '--'],
                                 color=['black', 'blue'],
                                 legend=True)

        with NestedPlotParameters(mpl_plotter):
            axis_density = multiple_scatterplots(xdata,
                                                 ydata,
                                                 xlabel=xlabel,
                                                 ylabel=density_ylabel,
                                                 title=density_title,
                                                 show=False,
                                                 save_plots=False,
                                                 axis=axis_density,
                                                 **density_kwargs)

    if figure is not None:
        figure.set_size_inches(14.0, 10.0)
        figure.subplots_adjust(left=0.10, bottom=0.2, right=0.90, wspace=0.4, hspace=0.4)

    mpl_plotter.save_plot(saveas)

    return [axis_potential, axis_density]


@ensure_plotter_consistency(mpl_plotter)
def plot_crystal_field_potential(cfcoeffs,
                                 *,
                                 saveas='crystal_field_potential_areaplot',
                                 spin='avg',
                                 phi=0.0,
                                 figure=None,
                                 **kwargs):
    """
    Plots the angular dependence of the calculated CF potential as well
    as a plane defined by phi.

    :param cfcoeffs: list of CFCoefficients to construct the potential
    :param saveas: str, defines the filename to save the figure
    :param spin: str; Either 'up', 'dn' or 'avg'. Which spin direction to plot
                    ('avg'-> ('up'+'dn')/2.0)
    :param phi: float, defines the phi angle of the plane

    :raises AssertionError: When coefficients are provided as wrong types or in the wrong convention
    :raises ValueError: When coefficients are provided in the wrong convention

    """
    from masci_tools.vis.plot_methods import colormesh_plot

    assert all(isinstance(coeff, CFCoefficient) for coeff in cfcoeffs), \
           'Only provide a list of CFCoefficients to plot_crystal_field_potential'

    if 'filename' in kwargs:
        warnings.warn('filename is deprecated. Use saveas instead', DeprecationWarning)
        saveas = kwargs.pop('filename')

    if 'save' in kwargs:
        warnings.warn('save is deprecated. Use save_plots instead', DeprecationWarning)
        kwargs['save_plots'] = kwargs.pop('save')

    if spin not in ('up', 'down', 'avg'):
        raise ValueError(f"Invalid Argument for spin: '{spin}'")

    if not all(coeff.convention == 'Wybourne' for coeff in cfcoeffs):
        raise ValueError('Wrong convention for plotting in spherical harmonics basis')

    #generate the theta/phi meshgrid
    theta_grid = np.linspace(0, np.pi, 181)
    phi_grid = np.linspace(0.0, 2.0 * np.pi, 361)
    xv, yv = np.meshgrid(phi_grid, theta_grid)
    cf_grid = np.zeros((181, 361), dtype='complex')

    for coeff in cfcoeffs:
        if spin == 'avg':
            value = 0.5 * (coeff.spin_up + coeff.spin_down)
        elif spin == 'up':
            value = coeff.spin_up
        elif spin == 'down':
            value = coeff.spin_down
        if coeff.m >= 0:
            cf_grid += value * sph_harm(coeff.m, coeff.l, xv, yv)

    #Plot the angular dependence
    maxv = max(cf_grid.real.max(), abs(cf_grid.real.min()))

    if figure is None:
        figure = plt.figure(figsize=(15, 5))

    gs = mpl.gridspec.GridSpec(1, 2, width_ratios=[2.0, 1.5])
    ax = plt.subplot(gs[0])

    mpl_plotter.set_defaults(default_type='function',
                             cmap='coolwarm',
                             limits={'color': (-maxv, maxv)},
                             xticks=[0.0, np.pi / 2.0, np.pi, 3 * np.pi / 2.0, 2 * np.pi],
                             xticklabels=[r'0', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$'],
                             yticks=[0.0, np.pi / 4.0, np.pi / 2.0, 3 * np.pi / 4.0, np.pi],
                             yticklabels=[r'$\pi/2$', r'$\pi/4$', r'$0.0$', r'$-\pi/4$', r'$-\pi/2$'])

    outer_keys = {'show', 'save_plots', 'save_format', 'save_options', 'colorbar'}
    outer_options = {key: val for key, val in kwargs.items() if key in outer_keys}
    kwargs = {key: val for key, val in kwargs.items() if key not in outer_keys}

    mpl_plotter.set_parameters(**outer_options)

    #Angular dependence plot

    gs = mpl.gridspec.GridSpec(1, 2, width_ratios=[2.0, 1.5])
    ax = plt.subplot(gs[0])
    with NestedPlotParameters(mpl_plotter):
        ax = colormesh_plot(xv,
                            yv,
                            cf_grid.real,
                            xlabel=r'$\phi$',
                            ylabel=r'$\theta$',
                            title='Angular Dependence',
                            axis=ax,
                            show=False,
                            save_plots=False,
                            colorbar=False,
                            **kwargs)

    if np.abs(phi_grid - phi).min() > 1e-5:
        raise ValueError(f'Angle {phi} not found in grid')
    phi_ind = np.abs(phi_grid - phi).argmin()

    theta_grid_pm = list(-1.0 * theta_grid)
    theta_cf = list(cf_grid[:, phi_ind])
    for index, theta in enumerate(theta_grid):
        theta_grid_pm.append(theta)
        theta_cf.append(theta_cf[index])

    theta_grid = np.array(theta_grid)
    theta_cf = np.array(theta_cf)

    #interpolate
    theta_cf = interp1d(theta_grid_pm, theta_cf.real, fill_value='extrapolate')

    nx = 200
    ny = 200
    #Define the cartesian grid between -1 and 1
    x = np.linspace(-1, 1, nx)
    y = np.linspace(-1, 1, ny)
    xv, yv = np.meshgrid(x, y)
    z = theta_cf(np.arctan(xv / yv))

    phi_fract = phi / np.pi

    ax = plt.subplot(gs[1])
    mpl_plotter.set_defaults(default_type='function',
                             cmap='coolwarm',
                             limits={'color': (-maxv, maxv)},
                             xticks=[-1.0, -0.5, 0.0, 0.5, 1.0],
                             yticks=[-1.0, -0.5, 0.0, 0.5, 1.0],
                             colorbar_options={
                                 'shrink': 0.8,
                                 'label': r'$V_{{CF}}$ [K]',
                                 'labelsize': 14
                             })

    with NestedPlotParameters(mpl_plotter):
        ax = colormesh_plot(xv,
                            yv,
                            z,
                            xlabel=r'x [Bohr]',
                            ylabel=r'y [Bohr]',
                            title=rf'Crystal Field potential for $\phi={{{phi_fract:.2f}}}\pi$',
                            axis=ax,
                            show=False,
                            save_plots=False,
                            colorbar=False,
                            **kwargs)

    mpl_plotter.show_colorbar(ax)
    figure.set_constrained_layout_pads(w_pad=0., h_pad=0.0, hspace=0., wspace=0.)

    mpl_plotter.save_plot(saveas)

    return figure
