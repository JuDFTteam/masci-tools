# -*- coding: utf-8 -*-
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
from collections import namedtuple
from itertools import groupby
import numpy as np
import h5py

from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.reader import Transformation, AttribTransformation
from masci_tools.util.constants import HTR_TO_EV

GreensfElement = namedtuple('GreensfElement',
                            ['l', 'lp', 'atomType', 'atomTypep', 'sphavg', 'onsite', 'contour', 'nLO', 'atomDiff'])


def _get_sphavg_recipe(group_name, index, contour):
    """
    Get the HDF5Reader recipe for reading in a spherically averaged Green's function element

    :param group_name: str of the group containing the Green's function elements
    :param index: integer index of the element to read in (indexing starts at 1)
    :param contour: integer index of the energy contour to read in (indexing starts at 1)

    :returns: dict with the recipe reading all the necessary information from the ``greensf.hdf`` file
    """
    return {
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


def _get_radial_recipe(group_name, index, contour):
    """
    Get the HDF5Reader recipe for reading in a radial Green's function element

    :param group_name: str of the group containing the Green's function elements
    :param index: integer index of the element to read in (indexing starts at 1)
    :param contour: integer index of the energy contour to read in (indexing starts at 1)

    :returns: dict with the recipe reading all the necessary information from the ``greensf.hdf`` file
    """
    recipe = _get_sphavg_recipe(group_name, index, contour)

    recipe['datasets'].pop('sphavg')

    recipe['datasets']['coefficients'] = {
        'h5path':
        f'/{group_name}/element-{index}',
        'transforms': [
            Transformation(name='get_all_child_datasets',
                           args=(),
                           kwargs={'ignore': ['scalarProducts', 'LOContribution']}),
            Transformation(name='convert_to_complex_array', args=(), kwargs={}),
            Transformation(name='multiply_scalar', args=(1.0 / HTR_TO_EV,), kwargs={})
        ],
        'unpack_dict':
        True
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


def _get_greensf_group_name(hdffile):
    """
    Return the name of the group containing the Green's function elements

    :param hdffile: h5py.File of the greensf.hdf file

    :returns: str of the group name containing the Green's Function elements
    """
    if '/GreensFunctionElements' in hdffile:
        return 'GreensFunctionElements'
    elif '/Hubbard1Elements' in hdffile:
        return 'Hubbard1Elements'


def _read_element_header(hdffile, index):
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
    atomDiff = np.array(element.attrs['atomDiff'])
    nLO = element.attrs['numLOs'][0]

    return GreensfElement(l, lp, atomType, atomTypep, sphavg, onsite, contour, nLO, atomDiff)


def _read_gf_element(file, index):
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
        gf_element = _read_element_header(h5reader._h5_file, index)
        group_name = _get_greensf_group_name(h5reader._h5_file)

        if gf_element.sphavg:
            recipe = _get_sphavg_recipe(group_name, index, gf_element.contour)
        else:
            recipe = _get_radial_recipe(group_name, index, gf_element.contour, nlo=gf_element.nLO)

        data, attributes = h5reader.read(recipe=recipe)

    return gf_element, data, attributes


class GreensFunction:
    """
    Class for working with Green's functions calculated by the fleur code

    :param element: :py:class:`GreensfElement` namedtuple containing the information about the element
    :param data: datasets dict produced by one of the hdf recipes for reading Green's functions
    :param attributes: attributes dict produced by one of the hdf recipes for reading Green's functions
    """

    def __init__(self, element, data, attributes):
        self.element = element

        self.points = data.pop('energy_points')
        self.weights = data.pop('energy_weights')

        self.data = data

        if not self.sphavg:
            self.scalar_products = attributes['scalarProducts']
            self.radial_functions = attributes['radialFunctions']
            raise NotImplementedError("Radial Green's functions not yet implemented")

        self.spins = attributes['spins']
        self.mperp = attributes['mperp']
        self.lmax = attributes['lmax']

    @classmethod
    def fromFile(cls, file, index):
        """
        Classmethod for creating a :py:class:`GreensFunction` instance directly from a hdf file

        :param file: path or opened file handle to a greensf.hdf file
        :param index: int index of the element to read in
        """
        element, data, attributes = _read_gf_element(file, index)
        return cls(element, data, attributes)

    def __getattr__(self, attr):
        """
        This __getattr__ method redirects lookups of field names of the stored :py:class:`GreensfElement`
        to return the value from the namedtuple

        :param attr: attribute to look up

        :returns: value of the attribute if it is a field name of :py:class:`GreensfElement`
        """
        if attr in GreensfElement._fields:
            return self.element._asdict()[attr]
        raise AttributeError(f'{self.__class__.__name__!r} object has no attribute {attr!r}')

    @staticmethod
    def to_m_index(m):
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
    def to_spin_indices(spin):
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
    def nspins(self):
        """
        Return the number of spins of the current element.
        If mperp is True for the element it is 4 otherwise it
        is determined by the spins attribute
        """
        if self.mperp:
            return 4
        else:
            return self.spins

    def get_scalar_product_by_key(self, key, spin):
        spin1, spin2 = self.to_spin_indices(spin)
        return self.scalar_products[f'{key}n'][spin1, spin2]

    def __str__(self):
        """
        String representation of the :py:class:`GreensFunction`. Chosen to be the
        str representation of the stored :py:class:`GreensfElement` instance.
        """
        return str(self.element)

    def energy_dependence(self, *, m=None, mp=None, spin, imag=True, both_contours=False):
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
        if spin is not None:
            spin -= 1
            spin_index = min(spin, 2 if self.mperp else self.nspins - 1)
        else:
            spin_index = slice(0, min(3, self.nspins))

        if m is not None:
            m_index = self.to_m_index(m)
        else:
            m_index = slice(self.lmax - self.l, self.lmax + self.l + 1, 1)

        if mp is not None:
            mp_index = self.to_m_index(mp)
        else:
            mp_index = slice(self.lmax - self.l, self.lmax + self.lp + 1, 1)

        gf = self.data['sphavg'][:, spin_index, mp_index, m_index, :].T

        if both_contours:
            return gf
        else:
            if imag:
                data = -1 / (2 * np.pi * 1j) * (gf[..., 0] - gf[..., 1])
            else:
                data = -1 / (2 * np.pi) * (gf[..., 0] + gf[..., 1])

        return data.real

    def trace_energy_dependence(self, spin, imag=True):
        """
        Select trace of data with energy dependence

        :param spin: integer spin between 1 and nspins
        :param imag: bool if True the imaginary part 1/2i(G(z)-G(z^*)) is returned
                     otherwise the real part 1/2(G(z)+G(z^*))

        :returns: numpy array with the selected and traced over data
        """
        if self.l != self.lp:
            raise ValueError('Trace only supported for l==lp')

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


def printElements(elements, index=None, mark=None):
    """
    Print the given list of :py:class:`GreensfElement` in a nice table

    :param elements: list of :py:class:`GreensfElement` to be printed
    :param index: optional list of indices to show instead of the default index in the list
    :param mark: optional list of int with elements to emphasize with an arrow and color
    """
    print('Index  | l     | lp    | atom  | atomp | sphavg | onsite | iContour |     atomDiff      |')
    print('-----------------------------------------------------------------------------------------')
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
                                       suppress_small=False,
                                       sign=' ',
                                       floatmode='fixed')
        print(
            color +
            f'{elem_index+1:<7d}|{element.l:7d}|{element.lp:7d}|{element.atomType:7d}|{element.atomTypep:7d}|{str(element.sphavg):>8s}|{str(element.onsite):>8s}|{element.contour:10d}|{atomdiff_str}|{markStr}'
            + colors.endc)


def listElements(hdffile, show=False):
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
        print(f'These Elements are found in {hdffile}:')
        printElements(elements)

    return elements


def selectOnsite(hdffile, l, atomType, lp=None, show=True):
    """
    Find the specified onsite element in the ``greensf.hdf`` file

    :param hdffile: filepath or file handle to a greensf.hdf file
    :param l: integer of the orbital quantum number
    :param atomType: integer of the atom type
    :param lp: optional integer of the second orbital quantum number (default equal to l)
    :param show: bool if True the found elements are printed in a table and the selected ones are marked

    :returns: list of indexes in the ``greensf.hdf`` file corresponding to the selected criteria
    """
    if lp is None:
        lp = l

    elements = listElements(hdffile)

    foundIndices = []
    for index, elem in enumerate(elements):
        if elem.l != l:
            continue
        if elem.lp != lp:
            continue
        if elem.atomType != atomType:
            continue
        if elem.atomTypep != atomType:
            continue
        if np.linalg.norm(elem.atomDiff) > 1e-12:
            continue
        foundIndices.append(index + 1)

    if show:
        printElements(elements, mark=foundIndices)
    return foundIndices


def intersite_shells(hdffile, refAtom, return_greensf=True, show=False):
    """
    Construct the green's function pairs to calculate the Jij exchange constants
    for a given reference atom from a given ``greensf.hdf`` file

    :param hdffile: filepath or file handle to a greensf.hdf file
    :param refAtom: integer of the atom to calculate the Jij's for (correspinds to the i)
    :param return_greensf: bool, if True instead of the indices aiterator yielding the
                           green's functions directly for calculations
    :param show: if True the elements belonging to a shell are printed in a shell

    :returns: either list of tuples with distance and all indices of pairs in the shell
              or flat iterator with distance and the two corresponding :py:class:`GreensFunction`
              instances
    """
    elements = listElements(hdffile)

    distances = [np.linalg.norm(elem.atomDiff) for elem in elements]

    #sort the elements according to shells
    index_sorted = sorted(range(len(elements)), key=lambda k: distances[k])
    elements_sorted = [elements[index] for index in index_sorted]
    jijPairs = []
    for dist, shell in groupby(zip(index_sorted, elements_sorted), key=lambda k: distances[k[0]]):
        if dist > 1e-12:
            if show:
                print(f'\nFound shell at distance: {dist}')
                print('The following elements are present:')
            shell_list = list(shell)
            jijPairsShell = []

            #Try to find gij gji pairs for Jij calculations
            for indexij, elemij in shell_list:
                for indexji, elemji in shell_list:
                    if elemij.contour != elemji.contour:
                        continue
                    if elemij.atomType != refAtom:
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
                    #Plus 1 because the indexing starts at 1 in the hdf file
                    if (indexji + 1, indexij + 1) not in jijPairsShell or \
                       elemij.atomType == elemij.atomTypep:
                        jijPairsShell.append((indexij + 1, indexji + 1))
            if len(jijPairsShell) > 0:
                jijPairs.append((dist, jijPairsShell))

            if show:
                #print the elements in the shell
                elem = [x[1] for x in shell_list]
                index = [x[0] for x in shell_list]
                printElements(elem, index=index)

    def shell_iterator(shells):
        for distance, pairs in shells:
            for g1, g2 in pairs:
                yield (distance,
                       GreensFunction.fromFile(hdffile, g1),\
                       GreensFunction.fromFile(hdffile, g2))

    if return_greensf:
        return shell_iterator(jijPairs)
    else:
        return jijPairs
