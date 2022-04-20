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
This module contains useful methods for initializing or modifying a n_mmp_mat file
for LDA+U
"""
from __future__ import annotations
from collections import defaultdict
from typing import NamedTuple

import numpy as np

from masci_tools.io.parsers import fleur_schema
from masci_tools.util.xml.xpathbuilder import XPathBuilder, FilterType
from masci_tools.util.xml.common_functions import get_xml_attribute
from masci_tools.util.xml.common_functions import eval_xpath
from masci_tools.util.typing import XMLLike

from masci_tools.util.schema_dict_util import eval_simple_xpath, evaluate_attribute
from masci_tools.util.schema_dict_util import attrib_exists

from masci_tools.io.io_nmmpmat import write_nmmpmat, write_nmmpmat_from_states, write_nmmpmat_from_orbitals
from masci_tools.io.io_nmmpmat import read_nmmpmat_block, rotate_nmmpmat_block, format_nmmpmat

LINES_PER_BLOCK = 14


def set_nmmpmat(xmltree: XMLLike,
                nmmplines: list[str] | None,
                schema_dict: fleur_schema.SchemaDict,
                species_name: str,
                orbital: int,
                spin: int,
                state_occupations: list[float] | None = None,
                orbital_occupations: list[float] | None = None,
                denmat: np.ndarray | None = None,
                phi: float | None = None,
                theta: float | None = None,
                inverse: bool = False,
                align_to_sqa: bool = False,
                filters: FilterType | None = None) -> list[str]:
    """Routine sets the block in the n_mmp_mat file specified by species_name, orbital and spin
    to the desired density matrix

    :param xmltree: an xmltree that represents inp.xml
    :param nmmplines: list of lines in the n_mmp_mat file
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param species_name: string, name of the species you want to change
    :param orbital: integer, orbital quantum number of the LDA+U procedure to be modified
    :param spin: integer, specifies which spin block should be modified
    :param state_occupations: list, sets the diagonal elements of the density matrix and everything
                              else to zero
    :param denmat: matrix, specify the density matrix explicitly
    :param phi: float, optional angle (radian), by which to rotate the density matrix before writing it
    :param theta: float, optional angle (radian), by which to rotate the density matrix before writing it
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

    :raises ValueError: If something in the input is wrong
    :raises KeyError: If no LDA+U procedure is found on a species

    :returns: list with modified nmmplines
    """

    #All lda+U procedures have to be considered since we need to keep the order
    species_name_base_path = schema_dict.attrib_xpath('name', tag_name='species')
    species_name_xpath = XPathBuilder(species_name_base_path, filters=filters, strict=True)

    if species_name[:4] == 'all-':  #format all-<string>
        species_name_xpath.add_filter('species', {'name': {'contains': species_name[4:]}})
    elif species_name != 'all':
        species_name_xpath.add_filter('species', {'name': species_name})

    possible_species: set[str] = set(eval_xpath(xmltree, species_name_xpath, list_return=True))  #type:ignore

    nspins = _get_number_of_spin_blocks(xmltree, schema_dict)
    if spin > nspins:
        raise ValueError(f'Invalid input: spin {spin} requested, but input has only {nspins} spins')

    if align_to_sqa and (theta is not None or phi is not None):
        raise ValueError(
            'Invalid input: Provide either rotation angles theta or phi or the align_to_sqa switch. Not both')

    ldau_order = _get_ldau_order(xmltree, schema_dict)
    _check_nmmpmat_num_rows(nmmplines, len(ldau_order), nspins, 'set_nmmpmat')

    if state_occupations is not None:
        new_nmmpmat_entry = write_nmmpmat_from_states(orbital, state_occupations, phi=phi, theta=theta, inverse=inverse)
    elif orbital_occupations is not None:
        new_nmmpmat_entry = write_nmmpmat_from_orbitals(orbital,
                                                        orbital_occupations,
                                                        phi=phi,
                                                        theta=theta,
                                                        inverse=inverse)
    elif denmat is not None:
        new_nmmpmat_entry = write_nmmpmat(orbital, denmat, phi=phi, theta=theta, inverse=inverse)
    else:
        raise ValueError('Invalid definition of density matrix. Provide either state_occupations, '
                         'orbital_occupations or denmat')

    for ldau_index, entry in enumerate(ldau_order):
        if entry.species not in possible_species or entry.orbital != orbital:
            continue

        #check if fleurinp has a specified n_mmp_mat file if not initialize it with 0
        if nmmplines is None:
            nmmplines = []
            for _ in range(nspins * LINES_PER_BLOCK * len(ldau_order)):
                nmmplines.append(''.join(map(str, [f'{0.0:20.13f}' for _ in range(7)])))

        #Select the right block from n_mmp_mat and overwrite it with denmatpad
        startRow = ((spin - 1) * len(ldau_order) + ldau_index) * LINES_PER_BLOCK

        nmmplines[startRow:startRow + LINES_PER_BLOCK] = new_nmmpmat_entry

    if nmmplines is None:
        raise ValueError('No denmat blocks set. Probably the species and orbital combination does not exist')

    if align_to_sqa:
        nmmplines = align_nmmpmat_to_sqa(xmltree, nmmplines, schema_dict, species_name, orbital)

    return nmmplines


def align_nmmpmat_to_sqa(xmltree: XMLLike,
                         nmmplines: list[str],
                         schema_dict: fleur_schema.SchemaDict,
                         species_name: str = 'all',
                         orbital: int | str = 'all',
                         phi_before: float | list[float] = 0.0,
                         theta_before: float | list[float] = 0.0,
                         filters: FilterType | None = None) -> list[str]:
    """
    Align the density matrix with the given SQA of the associated species

    :param xmltree: an xmltree that represents inp.xml
    :param nmmplines: list of lines in the n_mmp_mat file
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param species_name: string, name of the species you want to change
    :param orbital: integer or string ('all'), orbital quantum number of the LDA+U procedure to be modified
    :param phi_before: float or list of floats, angle (radian),
                       values for phi for the previous alignment of the density matrix
    :param theta_before: float or list of floats, angle (radian),
                         values for theta for the previous alignment of the density matrix
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

    :raises ValueError: If something in the input is wrong
    :raises KeyError: If no LDA+U procedure is found on a species

    :returns: list with modified nmmplines
    """
    if nmmplines is None:
        raise ValueError('align_nmmpmat_to_sqa has to be called with a initialized density matrix')

    #All lda+U procedures have to be considered since we need to keep the order
    species_name_base_path = schema_dict.attrib_xpath('name', tag_name='species')
    species_name_xpath = XPathBuilder(species_name_base_path, filters=filters, strict=True)

    if species_name[:4] == 'all-':  #format all-<string>
        species_name_xpath.add_filter('species', {'name': {'contains': species_name[4:]}})
    elif species_name != 'all':
        species_name_xpath.add_filter('species', {'name': species_name})

    possible_species: set[str] = set(eval_xpath(xmltree, species_name_xpath, list_return=True))  #type:ignore

    #Extract the SQA for all atom groups
    # (if we have scond variationn SOC it will just set to the same value)
    all_groups = eval_simple_xpath(xmltree, schema_dict, 'atomgroup', list_return=True)
    sqa_per_group: list[tuple[float, float]] = []
    noco = evaluate_attribute(xmltree, schema_dict, 'l_noco')
    if noco is None:
        noco = False
    soc = evaluate_attribute(xmltree, schema_dict, 'l_soc')
    if soc is None:
        soc = False

    if not isinstance(theta_before, list):
        theta_before = [theta_before] * len(all_groups)
    if not isinstance(phi_before, list):
        phi_before = [phi_before] * len(all_groups)

    if len(theta_before) != len(all_groups) or len(phi_before) != len(all_groups):
        raise ValueError('Not the right number of previous SQA given')
    sqa_before = list(zip(theta_before, phi_before))

    if not noco and not soc:
        raise ValueError('No Spin Quantization axis to align to')

    if not noco and soc:
        theta = evaluate_attribute(xmltree, schema_dict, 'theta', contains='soc')
        phi = evaluate_attribute(xmltree, schema_dict, 'phi', contains='soc')
        sqa_per_group = [(theta, phi)] * len(all_groups)
    else:
        for group in all_groups:
            beta = evaluate_attribute(group, schema_dict, 'beta', contains='noco')
            alpha = evaluate_attribute(group, schema_dict, 'alpha', contains='noco')
            sqa_per_group.append((beta, alpha))

    nspins = _get_number_of_spin_blocks(xmltree, schema_dict)
    ldau_order = _get_ldau_order(xmltree, schema_dict)
    _check_nmmpmat_num_rows(nmmplines, len(ldau_order), nspins, 'align_nmmpmat_to_sqa')

    for ldau_index, entry in enumerate(ldau_order):
        if entry.species not in possible_species or orbital not in (entry.orbital, 'all'):
            continue

        theta, phi = sqa_per_group[entry.group_index]
        theta_before, phi_before = sqa_before[entry.group_index]

        theta -= theta_before
        phi -= phi_before

        for spin in range(nspins):

            startRow = (spin * len(ldau_order) + ldau_index) * LINES_PER_BLOCK
            denmat = read_nmmpmat_block(nmmplines, spin * len(ldau_order) + ldau_index)
            denmat = rotate_nmmpmat_block(denmat, entry.orbital, phi=phi, theta=theta, inverse=True)

            nmmplines[startRow:startRow + LINES_PER_BLOCK] = format_nmmpmat(denmat)

    return nmmplines


def rotate_nmmpmat(xmltree: XMLLike,
                   nmmplines: list[str],
                   schema_dict: fleur_schema.SchemaDict,
                   species_name: str,
                   orbital: int | str,
                   phi: float,
                   theta: float,
                   inverse: bool = False,
                   filters: FilterType | None = None) -> list[str]:
    """
    Rotate the density matrix with the given angles phi and theta

    :param xmltree: an xmltree that represents inp.xml
    :param nmmplines: list of lines in the n_mmp_mat file
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param species_name: string, name of the species you want to change
    :param orbital: integer or string ('all'), orbital quantum number of the LDA+U procedure to be modified
    :param phi: float, angle (radian), by which to rotate the density matrix
    :param theta: float, angle (radian), by which to rotate the density matrix
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

    :raises ValueError: If something in the input is wrong
    :raises KeyError: If no LDA+U procedure is found on a species

    :returns: list with modified nmmplines
    """
    if nmmplines is None:
        raise ValueError('rotate_nmmpmat has to be called with a initialized density matrix')

    #All lda+U procedures have to be considered since we need to keep the order
    species_name_base_path = schema_dict.attrib_xpath('name', tag_name='species')
    species_name_xpath = XPathBuilder(species_name_base_path, filters=filters, strict=True)

    if species_name[:4] == 'all-':  #format all-<string>
        species_name_xpath.add_filter('species', {'name': {'contains': species_name[4:]}})
    elif species_name != 'all':
        species_name_xpath.add_filter('species', {'name': species_name})

    possible_species: set[str] = set(eval_xpath(xmltree, species_name_xpath, list_return=True))  #type:ignore

    nspins = _get_number_of_spin_blocks(xmltree, schema_dict)
    ldau_order = _get_ldau_order(xmltree, schema_dict)
    _check_nmmpmat_num_rows(nmmplines, len(ldau_order), nspins, 'rotate_nmmpmat')

    for ldau_index, entry in enumerate(ldau_order):
        if entry.species not in possible_species or orbital not in (entry.orbital, 'all'):
            continue

        for spin in range(nspins):

            startRow = (spin * len(ldau_order) + ldau_index) * LINES_PER_BLOCK
            denmat = read_nmmpmat_block(nmmplines, spin * len(ldau_order) + ldau_index)
            denmat = rotate_nmmpmat_block(denmat, entry.orbital, phi=phi, theta=theta, inverse=inverse)

            nmmplines[startRow:startRow + LINES_PER_BLOCK] = format_nmmpmat(denmat)

    return nmmplines


def validate_nmmpmat(xmltree: XMLLike, nmmplines: list[str] | None, schema_dict: fleur_schema.SchemaDict) -> None:
    """
    Checks that the given nmmp_lines is valid with the given xmltree

    Checks that the number of blocks is as expected from the inp.xml and each
    block does not contain non-zero elements outside their size given by the
    orbital quantum number in the inp.xml. Additionally the occupations, i.e.
    diagonal elements are checked that they are in between 0 and the maximum
    possible occupation

    :param xmltree: an xmltree that represents inp.xml
    :param nmmplines: list of lines in the n_mmp_mat file

    :raises ValueError: if any of the above checks are violated.
    """
    if nmmplines is None:
        return  #Nothing to validate

    nspins = _get_number_of_spin_blocks(xmltree, schema_dict)
    ldau_order = _get_ldau_order(xmltree, schema_dict)
    _check_nmmpmat_num_rows(nmmplines, len(ldau_order), nspins)

    tol = 0.01
    maximum_occupation = 1.0 if nspins > 1 else 2.0

    #Now check for each block if the numbers make sense
    #(no numbers outside the valid area and no nonsensical occupations)
    for ldau_index, entry in enumerate(ldau_order):

        for spin in range(nspins):
            nmmpmat = read_nmmpmat_block(nmmplines, spin * len(ldau_order) + ldau_index)

            #Check for values outside the range -l to l
            outside_val = False
            for index, row in enumerate(nmmpmat):
                if abs(index - 3) > entry.orbital:
                    outside_val = outside_val or any(np.abs(row) > 1e-12)
                else:
                    inside_mask = np.abs(np.array(range(-3, 4))) <= entry.orbital
                    outside_val = outside_val or any(np.abs(row[~inside_mask]) > 1e-12)

            if outside_val:
                raise ValueError(f'Found value outside of valid range in for species {entry.species}, spin {spin+1}'
                                 f' and l={entry.orbital}')

            #check the diagonal for spin-diagonal blocks
            if spin < 2:
                diagonal = nmmpmat.diagonal().real
                invalid_diag = np.logical_or(diagonal < -tol, diagonal > maximum_occupation + tol)

                if invalid_diag.any():
                    raise ValueError(f'Found invalid diagonal element for species {entry.species}, spin {spin+1}'
                                     f' and l={entry.orbital}')


class LDAUElement(NamedTuple):
    """
    Contains the important information needed to locate
    the associated density matrix blocks
    """
    species: str
    orbital: int
    group_index: int


def _get_ldau_order(xmltree: XMLLike, schema_dict: fleur_schema.SchemaDict) -> list[LDAUElement]:
    """
    Get the order of appearance for all LDA+U elements

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    """
    all_ldau = eval_simple_xpath(xmltree, schema_dict, 'ldaU', contains='species', list_return=True)

    species_to_ldauorbital = defaultdict(list)
    for ldau in all_ldau:
        parent = ldau.getparent()
        if parent is None:
            raise ValueError('Could not find parent of tag')
        species_name = get_xml_attribute(parent, 'name')
        orbital = evaluate_attribute(ldau, schema_dict, 'l')
        species_to_ldauorbital[species_name].append(orbital)

    ldau_order: list[LDAUElement] = []
    all_group_species = evaluate_attribute(xmltree, schema_dict, 'species', contains='atomGroup', list_return=True)
    for group_index, species in enumerate(all_group_species):
        if species in species_to_ldauorbital:
            ldau_order.extend(
                LDAUElement(species=species, orbital=orbital, group_index=group_index)
                for orbital in species_to_ldauorbital[species])

    return ldau_order


def _get_number_of_spin_blocks(xmltree: XMLLike, schema_dict: fleur_schema.SchemaDict) -> int:
    """
    Return how many spin blocks should be in the DFT+U density matrix file

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    """

    nspins = evaluate_attribute(xmltree, schema_dict, 'jspins')
    if 'l_mtnocoPot' in schema_dict['attrib_types']:
        if attrib_exists(xmltree, schema_dict, 'l_mtnocoPot', contains='Setup'):
            if evaluate_attribute(xmltree, schema_dict, 'l_mtnocoPot', contains='Setup'):
                nspins = 3
    #yapf: disable
    if schema_dict.inp_version > (0, 32) and attrib_exists(xmltree, schema_dict, 'l_mperp', contains='magnetism'): #type: ignore[attr-defined]
        if evaluate_attribute(xmltree, schema_dict, 'l_mperp', contains='magnetism'):
            nspins = 3
    #yapf: enable

    return nspins


def _check_nmmpmat_num_rows(nmmplines: list[str] | None,
                            num_ldau: int,
                            num_spins: int,
                            name: str | None = None) -> None:
    """Check that number of rows matches the number of lines in nmmp_lines_copy
    If not either there was an n_mmp_mat file present in Fleurinp before and a lda+u calculation
    was added or removed or the n_mmp_mat file was initialized and after the fact lda+u procedures were added
    or removed. In both cases the resolution of this modification is very involved so we throw an error
    """
    if nmmplines is None:
        return

    expected_rows = num_ldau * num_spins * LINES_PER_BLOCK

    #Remove blank lines
    while '' in nmmplines:
        nmmplines.remove('')
    if expected_rows != len(nmmplines):
        hint = ''
        if name is not None:
            hint =  'Either remove the existing file before making modifications ' \
                    f'and only use {name} after all other relevant modifications to the inp.xml'
        raise ValueError(f'The number of lines in n_mmp_mat ({len(nmmplines)}) does not match the number expected from '+\
                         f'the inp.xml file ({expected_rows}). '+hint)
