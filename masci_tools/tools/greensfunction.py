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
"""
This module contains utility and functions to work with Green's functions calculated
and written to ``greensf.hdf`` files by fleur
"""
from __future__ import annotations

from itertools import groupby, chain
import numpy as np
import h5py
from typing import Iterator, Any, NamedTuple, Generator
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  #type:ignore

from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.reader import Transformation, AttribTransformation, HDF5Recipe
from masci_tools.util.constants import HTR_TO_EV
from masci_tools.util.typing import FileLike


class GreensfElement(NamedTuple):
    """
    Namedtuple representing the high-level information about the Green's functions,
    i.e. what kind, which atoms, which orbitals
    """
    l: int
    lp: int
    atomType: int
    atomTypep: int
    sphavg: bool
    onsite: bool
    kresolved: bool
    contour: int
    nLO: int
    atomDiff: np.ndarray


CoefficientName = Literal['sphavg', 'uu', 'ud', 'du', 'dd', 'ulou', 'uulo', 'ulod', 'dulo', 'uloulo']


def _get_sphavg_recipe(group_name: str, index: int, contour: int, version: int | None = None) -> HDF5Recipe:
    """
    Get the HDF5Reader recipe for reading in a spherically averaged Green's function element

    :param group_name: str of the group containing the Green's function elements
    :param index: integer index of the element to read in (indexing starts at 1)
    :param contour: integer index of the energy contour to read in (indexing starts at 1)

    :returns: dict with the recipe reading all the necessary information from the ``greensf.hdf`` file
    """
    recipe: HDF5Recipe = {
        'datasets': {
            'sphavg': {
                'h5path':
                f'/{group_name}/element-{index}/sphavg',
                'transforms': [
                    Transformation(name='convert_to_complex_array', args=(), kwargs={}),
                    Transformation(name='multiply_scalar', args=(1.0 / HTR_TO_EV,), kwargs={})
                ]
            },
            'energy_points': {
                'h5path':
                f'/EnergyContours/contour-{contour}/ContourPoints',
                'transforms': [
                    Transformation(name='convert_to_complex_array', args=(), kwargs={}),
                    AttribTransformation(name='shift_by_attribute',
                                         attrib_name='fermi_energy',
                                         args=(),
                                         kwargs={
                                             'negative': True,
                                         }),
                    Transformation(name='multiply_scalar', args=(HTR_TO_EV,), kwargs={})
                ]
            },
            'energy_weights': {
                'h5path':
                f'/EnergyContours/contour-{contour}/IntegrationWeights',
                'transforms': [
                    Transformation(name='convert_to_complex_array', args=(), kwargs={}),
                    Transformation(name='multiply_scalar', args=(HTR_TO_EV,), kwargs={})
                ]
            }
        },
        'attributes': {
            'fermi_energy': {
                'h5path':
                '/general',
                'description':
                'fermi_energy of the system',
                'transforms': [
                    Transformation(name='get_attribute', args=('FermiEnergy',), kwargs={}),
                    Transformation(name='get_first_element', args=(), kwargs={})
                ]
            },
            'spins': {
                'h5path':
                '/general',
                'description':
                'number of spins',
                'transforms': [
                    Transformation(name='get_attribute', args=('spins',), kwargs={}),
                    Transformation(name='get_first_element', args=(), kwargs={})
                ]
            },
            'mperp': {
                'h5path':
                '/general',
                'description':
                'Switch whether spin offdiagonal elements are included',
                'transforms': [
                    Transformation(name='get_attribute', args=('mperp',), kwargs={}),
                    Transformation(name='get_first_element', args=(), kwargs={}),
                    Transformation(name='apply_lambda', args=(lambda x: x == 1,), kwargs={})
                ]
            },
            'lmax': {
                'h5path':
                f'/{group_name}',
                'description':
                'Maximum l considered (Determines size of the matrix)',
                'transforms': [
                    Transformation(name='get_attribute', args=('maxl',), kwargs={}),
                    Transformation(name='get_first_element', args=(), kwargs={})
                ]
            },
        }
    }

    if version is not None and version >= 7:
        recipe['attributes']['local_spin_frame'] = {
            'h5path':
            f'/{group_name}/element-{index}/',
            'description':
            'Switch whether the element is in the global spin frame',
            'transforms': [
                Transformation(name='get_attribute', args=('local_spin_frame',), kwargs={}),
                Transformation(name='get_first_element', args=(), kwargs={}),
                Transformation(name='apply_lambda', args=(lambda x: x == 1,), kwargs={})
            ]
        }

        recipe['attributes']['local_real_frame'] = {
            'h5path':
            f'/{group_name}/element-{index}/',
            'description':
            'Switch whether the element is in the global real space frame',
            'transforms': [
                Transformation(name='get_attribute', args=('local_real_frame',), kwargs={}),
                Transformation(name='get_first_element', args=(), kwargs={}),
                Transformation(name='apply_lambda', args=(lambda x: x == 1,), kwargs={})
            ]
        }

        recipe['attributes']['alpha'] = {
            'h5path':
            f'/{group_name}/element-{index}/',
            'description':
            'Noco angle alpha for the first atom',
            'transforms': [
                Transformation(name='get_attribute', args=('alpha',), kwargs={}),
                Transformation(name='get_first_element', args=(), kwargs={})
            ]
        }

        recipe['attributes']['alphap'] = {
            'h5path':
            f'/{group_name}/element-{index}/',
            'description':
            'Noco angle alpha for the second atom',
            'transforms': [
                Transformation(name='get_attribute', args=('alphap',), kwargs={}),
                Transformation(name='get_first_element', args=(), kwargs={})
            ]
        }

        recipe['attributes']['beta'] = {
            'h5path':
            f'/{group_name}/element-{index}/',
            'description':
            'Noco angle beta for the first atom',
            'transforms': [
                Transformation(name='get_attribute', args=('beta',), kwargs={}),
                Transformation(name='get_first_element', args=(), kwargs={})
            ]
        }

        recipe['attributes']['betap'] = {
            'h5path':
            f'/{group_name}/element-{index}/',
            'description':
            'Noco angle beta for the second atom',
            'transforms': [
                Transformation(name='get_attribute', args=('betap',), kwargs={}),
                Transformation(name='get_first_element', args=(), kwargs={})
            ]
        }
    return recipe


def _get_radial_recipe(group_name: str,
                       index: int,
                       contour: int,
                       nLO: int = 0,
                       version: int | None = None) -> HDF5Recipe:
    """
    Get the HDF5Reader recipe for reading in a radial Green's function element

    :param group_name: str of the group containing the Green's function elements
    :param index: integer index of the element to read in (indexing starts at 1)
    :param contour: integer index of the energy contour to read in (indexing starts at 1)

    :returns: dict with the recipe reading all the necessary information from the ``greensf.hdf`` file
    """
    recipe = _get_sphavg_recipe(group_name, index, contour, version=version)

    recipe['datasets'].pop('sphavg')

    recipe['datasets']['coefficients'] = {
        'h5path':
        f'/{group_name}/element-{index}',
        'transforms': [
            Transformation(name='get_all_child_datasets',
                           args=(),
                           kwargs={'ignore': ['scalarProducts', 'LOcontribution', 'mmpmat']}),
            Transformation(name='convert_to_complex_array', args=(), kwargs={}),
            Transformation(name='multiply_scalar', args=(1.0 / HTR_TO_EV,), kwargs={})
        ],
        'unpack_dict':
        True
    }

    if nLO > 0:
        recipe['datasets']['lo_coefficients'] = {
            'h5path':
            f'/{group_name}/element-{index}/LOcontribution',
            'transforms': [
                Transformation(name='merge_subgroup_datasets',
                               args=(),
                               kwargs={
                                   'ignore': 'uloulop-',
                                   'sort_key': lambda x: int(x.split('-', maxsplit=1)[1])
                               }),
                Transformation(name='convert_to_complex_array', args=(), kwargs={}),
                Transformation(name='multiply_scalar', args=(1.0 / HTR_TO_EV,), kwargs={})
            ],
            'unpack_dict':
            True
        }
        recipe['datasets']['uloulo'] = {
            'h5path':
            f'/{group_name}/element-{index}/LOcontribution',
            'transforms': [
                Transformation(name='merge_subgroup_datasets',
                               args=(),
                               kwargs={
                                   'contains': 'uloulop-',
                                   'sort_key': lambda x: int(x.split('-', maxsplit=1)[1])
                               }),
                Transformation(name='convert_to_complex_array', args=(), kwargs={}),
                Transformation(name='stack_datasets', args=(), kwargs={'axis': 1}),
                Transformation(name='multiply_scalar', args=(1.0 / HTR_TO_EV,), kwargs={})
            ],
        }

    recipe['attributes']['scalarProducts'] = {
        'h5path': f'/{group_name}/element-{index}/scalarProducts',
        'transforms': [Transformation(name='get_all_child_datasets', args=(), kwargs={})]
    }

    recipe['attributes']['radialFunctions'] = {
        'h5path': '/RadialFunctions',
        'transforms': [Transformation(name='get_all_child_datasets', args=(), kwargs={})]
    }

    return recipe


def _get_kresolved_recipe(group_name: str, index: int, contour: int, version: int | None = None) -> HDF5Recipe:
    """
    Get the HDF5Reader recipe for reading in a k-resolved Green's function element

    :param group_name: str of the group containing the Green's function elements
    :param index: integer index of the element to read in (indexing starts at 1)
    :param contour: integer index of the energy contour to read in (indexing starts at 1)

    :returns: dict with the recipe reading all the necessary information from the ``greensf.hdf`` file
    """
    recipe = _get_sphavg_recipe(group_name, index, contour, version=version)

    recipe['datasets'].pop('sphavg')

    recipe['datasets']['sphavg'] = {
        'h5path':
        f'/{group_name}/element-{index}',
        'transforms': [
            Transformation(name='get_all_child_datasets', args=(), kwargs={'contains': ['kresolved-']}),
            Transformation(name='convert_to_complex_array', args=(), kwargs={}),
            Transformation(name='stack_datasets',
                           args=(),
                           kwargs={
                               'axis': 0,
                               'sort_key': lambda x: int(x.split('-', maxsplit=1)[1])
                           }),
            Transformation(name='multiply_scalar', args=(1.0 / HTR_TO_EV,), kwargs={})
        ],
    }

    recipe['attributes']['nkpts'] = {
        'h5path':
        '/general/kpts',
        'transforms': [
            Transformation(name='get_attribute', args=('nkpt',), kwargs={}),
            Transformation(name='get_first_element', args=(), kwargs={}),
        ],
    }

    recipe['attributes']['kpoints_kind'] = {
        'h5path':
        '/general/kpts',
        'transforms': [
            Transformation(name='get_attribute', args=('kind',), kwargs={}),
            Transformation(name='convert_to_str', args=(), kwargs={'join': True}),
        ],
    }

    recipe['attributes']['kpoints'] = {
        'h5path': '/general/kpts/coordinates',
    }

    recipe['attributes']['reciprocal_cell'] = {'h5path': '/general/reciprocalCell'}

    recipe['attributes']['special_kpoint_indices'] = {
        'h5path': '/general/kpts/specialPointIndices',
        'transforms': [Transformation(name='shift_dataset', args=(-1,), kwargs={})]
    }

    recipe['attributes']['special_kpoint_labels'] = {
        'h5path': '/general/kpts/specialPointLabels',
        'transforms': [Transformation(name='convert_to_str', args=(), kwargs={})]
    }

    return recipe


def _get_greensf_group_name(hdffile: h5py.File) -> str:
    """
    Return the name of the group containing the Green's function elements

    :param hdffile: h5py.File of the greensf.hdf file

    :returns: str of the group name containing the Green's Function elements
    """
    if '/GreensFunctionElements' in hdffile:
        return 'GreensFunctionElements'
    if '/Hubbard1Elements' in hdffile:
        return 'Hubbard1Elements'
    raise ValueError("No Green's function group found")


def _read_element_header(hdffile: h5py.File, index: int) -> GreensfElement:
    """
    Read the attributes of the given green's function elements

    :param hdffile: h5py.File of the greensf.hdf file
    :param index: integer index of the element to read in (indexing starts at 1)

    :returns: :py:class:`GreensfElement` corresponding to the read in attributes
    """
    group_name = _get_greensf_group_name(hdffile)

    element = hdffile.get(f'/{group_name}/element-{index}')

    l = element.attrs['l'][0]
    lp = element.attrs['lp'][0]
    atomType = element.attrs['atomType'][0]
    atomTypep = element.attrs['atomTypep'][0]
    sphavg = element.attrs['l_sphavg'][0] == 1
    onsite = element.attrs['l_onsite'][0] == 1
    contour = element.attrs['iContour'][0]
    kresolved = element.attrs.get('l_kresolved', [0])[0] == 1
    atomDiff = np.array(element.attrs['atomDiff'])
    atomDiff[abs(atomDiff) < 1e-12] = 0.0
    nLO = element.attrs['numLOs'][0]

    return GreensfElement(l, lp, atomType, atomTypep, sphavg, onsite, kresolved, contour, nLO, atomDiff)


def _get_version(hdffile: h5py.File) -> int | None:
    """
    Get the file version of the given greensf.hdf file

    :param hdffile: h5py.File of the greensf.hdf file
    """
    meta = hdffile.get('/meta')
    version = None
    if meta is not None:
        version = int(meta.attrs['version'][0])

    if version is None:
        raise ValueError('Failed to extract file version of greensf.hdf file')

    return version


def _read_gf_element(file: Any, index: int) -> tuple[GreensfElement, dict[str, Any], dict[str, Any]]:
    """
    Read the information needed for a given Green's function element form a ``greensf.hdf``
    file

    :param file: filepath or handle to be read
    :param index: integer index of the element to read in (indexing starts at 1)

    :returns: tuple of the information containing the :py:class:`GreensfElement` for the element
              and the datasets and attributes dict produced by the corresponding
              :py:class:`~masci_tools.io.parsers.hdf5.HDF5Reader`
    """
    with HDF5Reader(file) as h5reader:
        version = _get_version(h5reader.file)
        gf_element = _read_element_header(h5reader.file, index)
        group_name = _get_greensf_group_name(h5reader.file)

        if gf_element.kresolved:
            recipe = _get_kresolved_recipe(group_name, index, gf_element.contour, version=version)
        elif gf_element.sphavg:
            recipe = _get_sphavg_recipe(group_name, index, gf_element.contour, version=version)
        else:
            recipe = _get_radial_recipe(group_name, index, gf_element.contour, nLO=gf_element.nLO, version=version)

        data, attributes = h5reader.read(recipe=recipe)

    return gf_element, data, attributes


class GreensFunction:
    """
    Class for working with Green's functions calculated by the fleur code

    :param element: :py:class:`GreensfElement` namedtuple containing the information about the element
    :param data: datasets dict produced by one of the hdf recipes for reading Green's functions
    :param attributes: attributes dict produced by one of the hdf recipes for reading Green's functions
    """

    def __init__(self, element: GreensfElement, data: dict[str, Any], attributes: dict[str, Any]) -> None:
        self.element = element

        self.points = data.pop('energy_points')
        self.weights = data.pop('energy_weights')

        self.data = data
        self.extras = attributes

        self.kpoints = None
        self.kpath = None
        if self.kresolved:
            self.kpoints = attributes['kpoints']
            if attributes['kpoints_kind'] == 'path':
                #Project kpoints onto 1D path
                self.kpath = self.kpoints @ attributes['reciprocal_cell'].T
                self.kpath = np.array([np.linalg.norm(ki - kj) for ki, kj in zip(self.kpath[1:], self.kpath[:-1])])
                self.kpath = np.insert(self.kpath, 0, 0.0)
                self.kpath = np.cumsum(self.kpath)

        elif not self.sphavg:
            #Remove trailing n or p
            self.scalar_products = {key.strip('pn'): val for key, val in attributes['scalarProducts'].items()}
            self.radial_functions = attributes['radialFunctions']
            if self.nLO > 0:
                all_local_orbitals = self.radial_functions['llo']

                #Important: Indices have to be shifted to start with 0
                lo_list_atomtype = [
                    indx - 1 for indx, l in enumerate(all_local_orbitals[self.atomType - 1]) if l == self.l
                ]
                lo_list_atomtypep = [
                    indx - 1 for indx, l in enumerate(all_local_orbitals[self.atomTypep - 1]) if l == self.lp
                ]

                for key, val in self.scalar_products.items():
                    if key == 'uloulo':
                        self.scalar_products[key] = np.array(
                            [val.T[indx, lo_list_atomtypep, ...] for indx in lo_list_atomtype])
                    elif key.startswith('ulo'):
                        self.scalar_products[key] = val.T[lo_list_atomtype, ...]
                    elif key.endswith('ulo'):
                        self.scalar_products[key] = val.T[lo_list_atomtypep, ...]
                #TODO: Same selections for radial_functions

        self.spins: int = attributes['spins']
        self.mperp: bool = attributes['mperp']
        self.lmax: int = attributes['lmax']

    @classmethod
    def fromFile(cls, file: Any, index: int | None = None, **selection_params: Any) -> GreensFunction:
        """
        Classmethod for creating a :py:class:`GreensFunction` instance directly from a hdf file

        :param file: path or opened file handle to a greensf.hdf file
        :param index: optional int index of the element to read in

        If index is not given Keyword arguments with the keys being the names of the fields of
        :py:class:`GreensfElement` can be given to select the right Green's function. The specification
        has to match only one element in the file
        """

        if index is None:
            if not selection_params:
                raise ValueError('If index is not given, parameters for selection need to be provided')
            elements = listElements(file)
            indices = select_element_indices(elements, **selection_params)
            if len(indices) == 1:
                index = indices[0] + 1
            else:
                raise ValueError(
                    f'Found multiple possible matches for the given criteria. Indices {indices} are possible')
        else:
            if selection_params:
                raise ValueError('If index is given no further selection parameters are allowed')

        element, data, attributes = _read_gf_element(file, index)
        return cls(element, data, attributes)

    def __getattr__(self, attr: str) -> Any:
        """
        This __getattr__ method redirects lookups of field names of the stored :py:class:`GreensfElement`
        to return the value from the namedtuple

        :param attr: attribute to look up

        :returns: value of the attribute if it is a field name of :py:class:`GreensfElement`
        """
        if attr in GreensfElement._fields:
            return self.element._asdict()[attr]
        raise AttributeError(f'{self.__class__.__name__!r} object has no attribute {attr!r}')

    def get_coefficient(self, name: CoefficientName, spin: int | None = None, radial: bool = False) -> np.ndarray:
        """
        Get the coefficient with the given name from the data attribute

        :param name: name of the coefficient
        :param radial: if the Green's function is stored by coefficient and radial is True
                       it is multiplied by the corresponding radial function
                       otherwise the scalar product is multiplied
        :param spin: integer index of the spin to retrieve

        :returns: numpy.ndarray for the given coefficient and spin
        """
        if spin is not None:
            spin -= 1
            spin_index = min(spin, 2 if self.mperp else self.nspins - 1)

        if radial and self.sphavg:
            raise ValueError("No radial dependence possible. Green's function is spherically averaged")

        coeff: Any = 1 if spin is not None else np.ones((2, 2))
        if name != 'sphavg':
            if radial:
                raise NotImplementedError()
            else:
                if spin is not None:
                    spin1, spin2 = self.to_spin_indices(spin)
                    coeff = self.scalar_products[name][..., spin1, spin2].T
                else:
                    coeff = self.scalar_products[name].T
        elif not self.sphavg:
            raise ValueError("No entry sphavg available. Green's function is stored radially resolved")

        data = self.data[name].T  #Converting from fortran index order
        if spin is not None:
            data = data[:, :, :, spin_index, ...]
        else:
            if self.mperp:
                #Build up the full 2x2 spin matrix for the coefficient
                axes = list(range(len(data.shape)))
                axes[2] = 1
                axes[1] = 2
                spin_offd = np.transpose(data[:, :, :, [2], ...].conj(), axes=axes)
                data = np.concatenate((data, spin_offd), axis=3)
            else:
                data = np.concatenate((data, np.empty_like(data[:, :, :, [0, 1], ...])), axis=3)
            #Reorder spin entries so that the spin-diagonal contributions also
            #end up on the diagonal of the 2x2 matrix
            spin_order = [0, 2, 3, 1]
            data = data[:, :, :, spin_order, ...]
            shape = tuple(chain(data.shape[:3], (2, 2), data.shape[4:]))
            data = np.reshape(data, shape)

        if self.kresolved:
            #Move upper/lower contour index to last one
            return np.swapaxes(data, -2, -1)

        if spin is not None:
            if name == 'uloulo':
                return np.einsum('...ij,...ij->...ij', data, coeff)
            if 'lo' in name:
                return np.einsum('...i,...i->...i', data, coeff)
            return data * coeff

        if name == 'uloulo':
            return np.einsum('...ijkl,...ijkl->...ijkl', data, coeff)
        if 'lo' in name:
            return np.einsum('...ijk,...ijk->...ijk', data, coeff)
        return np.einsum('...ij,...ij->...ij', data, coeff)

    @staticmethod
    def to_m_index(m: int) -> int:
        """
        Convert between magnetic quantum numbers between -l and l
        to 0 and 2l+1 for easier indexing

        :param m: int magnetic quantum number to convert

        :returns: converted magnetic quantum number
        """
        if abs(m) > 3:
            raise ValueError('Invalid magnetic quantum number (>3)')
        return m + 3

    @staticmethod
    def to_spin_indices(spin: int) -> tuple[int, int]:
        """
        Convert between spin index (0 to 3) to the corresponding
        two spin indices (0 or 1)

        :param spin: int spin index to convert

        :returns: tuple of spin indices
        """
        if spin < 0 or spin > 3:
            raise ValueError('Invalid spin index')
        if spin < 2:
            spin1 = spin
            spin2 = spin
        elif spin == 2:
            spin1 = 1
            spin2 = 0
        else:
            spin1 = 0
            spin2 = 1
        return spin1, spin2

    @property
    def nspins(self) -> int:
        """
        Return the number of spins of the current element.
        If mperp is True for the element it is 4 otherwise it
        is determined by the spins attribute
        """
        if self.mperp:
            return 4
        return self.spins

    def __str__(self) -> str:
        """
        String representation of the :py:class:`GreensFunction`. Chosen to be the
        str representation of the stored :py:class:`GreensfElement` instance.
        """
        return str(self.element)

    def energy_dependence(self,
                          *,
                          m: int | None = None,
                          mp: int | None = None,
                          spin: int | None = None,
                          imag: bool = True,
                          both_contours: bool = False) -> np.ndarray:
        """
        Select data with energy dependence

        :param m: optional integer magnetic quantum number between -l and l
        :param mp: optional integer magnetic quantum number between -lp and lp
        :param spin: optional integer spin between 1 and nspins
        :param both_contours: bool id True the data is not added for both energy contours
        :param imag: bool if True and both_contours is False the imaginary part 1/2i(G(z)-G(z^*)) is returned
                     otherwise the real part 1/2(G(z)+G(z^*))

        :returns: numpy array with the selected data
        """
        m_index: int | slice
        mp_index: int | slice

        if m is not None:
            m_index = self.to_m_index(m)
        else:
            m_index = slice(self.lmax - self.l, self.lmax + self.l + 1, 1)

        if mp is not None:
            mp_index = self.to_m_index(mp)
        else:
            mp_index = slice(self.lmax - self.l, self.lmax + self.lp + 1, 1)

        if self.sphavg:
            gf = self.get_coefficient('sphavg', spin=spin)[:, m_index, mp_index, ...]
        else:
            gf =  self.get_coefficient('uu', spin=spin)[:,m_index,mp_index,...] \
                + self.get_coefficient('ud', spin=spin)[:,m_index,mp_index,...] \
                + self.get_coefficient('du', spin=spin)[:,m_index,mp_index,...] \
                + self.get_coefficient('dd', spin=spin)[:,m_index,mp_index,...] \
                + np.sum(self.get_coefficient('uulo', spin=spin)[:,m_index,mp_index,...], axis=-1) \
                + np.sum(self.get_coefficient('ulou', spin=spin)[:,m_index,mp_index,...], axis=-1) \
                + np.sum(self.get_coefficient('dulo', spin=spin)[:,m_index,mp_index,...], axis=-1) \
                + np.sum(self.get_coefficient('uloulo', spin=spin)[:,m_index,mp_index,...], axis=(-1,-2))

        if both_contours:
            return gf
        if imag:
            data = -1 / (2 * np.pi * 1j) * (gf[..., 0] - gf[..., 1])
        else:
            data = -1 / (2 * np.pi) * (gf[..., 0] + gf[..., 1])

        return data.real

    def trace_energy_dependence(self, spin: int, imag: bool = True) -> np.ndarray:
        """
        Select trace of data with energy dependence

        :param spin: integer spin between 1 and nspins
        :param imag: bool if True the imaginary part 1/2i(G(z)-G(z^*)) is returned
                     otherwise the real part 1/2(G(z)+G(z^*))

        :returns: numpy array with the selected and traced over data
        """
        if self.l != self.lp:
            raise ValueError('Trace only supported for l==lp')

        if self.kresolved:
            data = np.zeros((*self.points.shape, self.extras['nkpts']))
        else:
            data = np.zeros(self.points.shape)
        for m in range(-self.l, self.l + 1):
            data += self.energy_dependence(m=m, mp=m, spin=spin, imag=imag)

        return data


class colors:
    """
    Color strings for coloring terminal output

    You may need to change color settings in iPython
    """
    red = '\033[31m'
    endc = '\033[m'
    green = '\033[32m'


def printElements(elements: list[GreensfElement],
                  index: list[int] | None = None,
                  mark: list[int] | None = None) -> None:
    """
    Print the given list of :py:class:`GreensfElement` in a nice table

    :param elements: list of :py:class:`GreensfElement` to be printed
    :param index: optional list of indices to show instead of the default index in the list
    :param mark: optional list of int with elements to emphasize with an arrow and color
    """
    print('Index  | l     | lp    | atom  | atomp | sphavg | onsite | iContour |     atomDiff      |')
    print('-----------------------------------------------------------------------------------------')

    elem_iter: Iterator[tuple[int, GreensfElement]]
    if index is None:
        elem_iter = enumerate(elements)
    else:
        elem_iter = zip(index, elements)

    for elem_index, element in elem_iter:
        if mark is not None and elem_index + 1 in mark:
            markStr = '<---'
            color = colors.green
        else:
            markStr = ''
            color = ''

        atomdiff_str = np.array2string(element.atomDiff,
                                       precision=2,
                                       separator=',',
                                       suppress_small=True,
                                       sign=' ',
                                       floatmode='fixed')
        print(
            color +
            f'{elem_index+1:<7d}|{element.l:7d}|{element.lp:7d}|{element.atomType:7d}|{element.atomTypep:7d}|{str(element.sphavg):>8s}|{str(element.onsite):>8s}|{element.contour:10d}|{atomdiff_str}|{markStr}'
            + colors.endc)


def listElements(hdffile: FileLike, show: bool = False) -> list[GreensfElement]:
    """
    Find the green's function elements contained in the given ``greens.hdf`` file

    :param hdffile: filepath or file handle to a greensf.hdf file
    :param show: bool if True the found elements are printed in a table

    :returns: list of :py:class:`GreensfElement`
    """
    with h5py.File(hdffile, 'r') as h5_file:

        group_name = _get_greensf_group_name(h5_file)

        num_elements = h5_file.get(group_name).attrs['NumElements'][0]

        elements = []
        for index in range(1, num_elements + 1):
            elements.append(_read_element_header(h5_file, index))

    if show:
        print(f'These Elements are found in {hdffile!r}:')
        printElements(elements)

    return elements


def select_elements_from_file(hdffile: FileLike,
                              show: bool = False,
                              **selection_params: Any) -> Generator[GreensFunction, None, None]:
    """
    Construct the green's function matching specified criteria from a given ``greensf.hdf`` file

    :param hdffile: file or file path to the ``greensf.hdf`` file
    :param show: bool if True the found elements will be printed

    The Keyword arguments correspond to the names of the fields and their desired value

    :returns: iterator over the matching :py:class:`GreensFunction`
    """

    elements = listElements(hdffile, show=show)
    found_elements = select_element_indices(elements, show=show, **selection_params)

    def gf_iterator(found_elements: list[int]) -> Generator[GreensFunction, None, None]:
        for index in found_elements:
            yield GreensFunction.fromFile(hdffile, index=index + 1)

    return gf_iterator(found_elements)


def select_elements(greensfunctions: list[GreensFunction],
                    show: bool = False,
                    **selection_params: Any) -> Generator[GreensFunction, None, None]:
    """
    Select :py:class:`GreensFunction` objects from a list based on constraints on the
    values of their underlying :py:class:`GreensfElement`

    :param greensfunctions: list of :py:class:`GreensFunction` to choose from
    :param show: bool if True the found elements will be printed

    The Keyword arguments correspond to the names of the fields and their desired value

    :returns: iterator over the matching :py:class:`GreensFunction`
    """
    elements = [gf.element for gf in greensfunctions]
    found_elements = select_element_indices(elements, show=show, **selection_params)

    def gf_iterator(found_elements: list[int]) -> Generator[GreensFunction, None, None]:
        for index in found_elements:
            yield greensfunctions[index]

    return gf_iterator(found_elements)


def select_element_indices(elements: list[GreensfElement], show: bool = False, **selection_params: Any) -> list[int]:
    """
    Select :py:class:`GreensfElement` objects from a list based on constraints on their
    values

    :param elements: list of :py:class:`GreensfElement` to choose from
    :param show: bool if True the found elements will be printed

    The Keyword arguments correspond to the names of the fields and their desired value

    :returns: list of the indices matching the criteria
    """

    for key in selection_params:
        if key not in GreensfElement._fields:
            raise KeyError(f"Key {key} is not allowed for selecting Green's function elements")

    found_elements = []
    for index, elem in enumerate(elements):
        if all(elem._asdict()[key] ==
               val if not isinstance(elem._asdict()[key], np.ndarray) else np.allclose(elem._asdict()[key], val)
               for key, val in selection_params.items()):
            found_elements.append(index)

    if show:
        printElements(elements, index=found_elements)
    return found_elements


def intersite_shells_from_file(
        hdffile: FileLike,
        reference_atom: int,
        show: bool = False) -> Generator[tuple[np.floating[Any], GreensFunction, GreensFunction], None, None]:
    """
    Construct the green's function pairs to calculate the Jij exchange constants
    for a given reference atom from a given ``greensf.hdf`` file

    :param hdffile: filepath or file handle to a greensf.hdf file
    :param reference_atom: integer of the atom to calculate the Jij's for (correspinds to the i)
    :param show: if True the elements belonging to a shell are printed in a shell

    :returns: flat iterator with distance and the two corresponding :py:class:`GreensFunction`
              instances for each Jij calculation
    """

    elements = listElements(hdffile)
    jij_pairs = intersite_shell_indices(elements, reference_atom, show=show)

    def shell_iterator(
        shells: list[tuple[np.floating[Any], list[tuple[int, int]]]]
    ) -> Generator[tuple[np.floating[Any], GreensFunction, GreensFunction], None, None]:
        for distance, pairs in shells:
            for g1, g2 in pairs:
                #Plus 1 because the indexing starts at 1 in the hdf file
                yield (distance,
                       GreensFunction.fromFile(hdffile, g1+1),\
                       GreensFunction.fromFile(hdffile, g2+1))

    return shell_iterator(jij_pairs)


def intersite_shells(
        greensfunctions: list[GreensFunction],
        reference_atom: int,
        show: bool = False) -> Generator[tuple[np.floating[Any], GreensFunction, GreensFunction], None, None]:
    """
    Construct the green's function pairs to calculate the Jij exchange constants
    for a given reference atom from a list of given :py:class:`GreensFunction`

    :param greensfunctions: List of Greens Function to use
    :param reference_atom: integer of the atom to calculate the Jij's for (correspinds to the i)
    :param show: if True the elements belonging to a shell are printed in a shell

    :returns: flat iterator with distance and the two corresponding :py:class:`GreensFunction`
              instances for each Jij calculation
    """

    elements = [gf.element for gf in greensfunctions]
    jij_pairs = intersite_shell_indices(elements, reference_atom, show=show)

    def shell_iterator(
        shells: list[tuple[np.floating[Any], list[tuple[int, int]]]]
    ) -> Generator[tuple[np.floating[Any], GreensFunction, GreensFunction], None, None]:
        for distance, pairs in shells:
            for g1, g2 in pairs:
                yield (distance, greensfunctions[g1], greensfunctions[g2])

    return shell_iterator(jij_pairs)


def intersite_shell_indices(elements: list[GreensfElement],
                            reference_atom: int,
                            show: bool = False) -> list[tuple[np.floating[Any], list[tuple[int, int]]]]:
    """
    Construct the green's function pairs to calculate the Jij exchange constants
    for a given reference atom from a list of :py:class:`GreensfElement`

    :param elements: list of GreenfElements to use
    :param reference_atom: integer of the atom to calculate the Jij's for (correspinds to the i)
    :param show: if True the elements belonging to a shell are printed in a shell

    :returns: list of tuples with distance and all indices of pairs in the shell
    """

    distances = [round(np.linalg.norm(elem.atomDiff), 12) for elem in elements]

    #sort the elements according to shells
    index_sorted = sorted(range(len(elements)), key=lambda k: distances[k])
    elements_sorted = [elements[index] for index in index_sorted]
    jij_pairs = []
    for dist, shell in groupby(zip(index_sorted, elements_sorted), key=lambda k: distances[k[0]]):
        if dist > 1e-12:
            if show:
                print(f'\nFound shell at distance: {dist}')
                print('The following elements are present:')
            shell_list = list(shell)
            jij_pairs_shell = []

            #Try to find gij gji pairs for Jij calculations
            for indexij, elemij in shell_list:
                for indexji, elemji in shell_list:
                    if elemij.contour != elemji.contour:
                        continue
                    if elemij.atomType != reference_atom:
                        continue
                    if elemij.atomType != elemji.atomTypep:
                        continue
                    if elemij.atomTypep != elemji.atomType:
                        continue
                    if elemij.l != elemji.l:
                        continue
                    if elemij.lp != elemji.lp:
                        continue
                    if np.linalg.norm(elemij.atomDiff + elemji.atomDiff) > 1e-12:
                        continue
                    #here we have found a pair
                    if (indexji, indexij) not in jij_pairs_shell or \
                       elemij.atomType == elemij.atomTypep:
                        jij_pairs_shell.append((indexij, indexji))
            if len(jij_pairs_shell) > 0:
                jij_pairs.append((dist, jij_pairs_shell))

            if show:
                #print the elements in the shell
                elem = [x[1] for x in shell_list]
                index = [x[0] for x in shell_list]
                printElements(elem, index=index)

    return jij_pairs
