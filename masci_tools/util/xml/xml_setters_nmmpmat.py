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
This module contains useful methods for initializing or modifying a n_mmp_mat file
for LDA+U
"""

from masci_tools.util.schema_dict_util import get_tag_xpath
import numpy as np

def set_nmmpmat(xmltree, nmmplines, schema_dict, species_name, orbital, spin,\
                state_occupations=None, orbital_occupations=None, denmat=None, phi=None, theta=None):
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
    :param denmat: matrix, specify the density matrix explicitely
    :param phi: float, optional angle (radian), by which to rotate the density matrix before writing it
    :param theta: float, optional angle (radian), by which to rotate the density matrix before writing it

    :raises ValueError: If something in the input is wrong
    :raises KeyError: If no LDA+U procedure is found on a species

    :returns: list with modified nmmplines
    """
    from masci_tools.util.xml.common_functions import eval_xpath, get_xml_attribute
    from masci_tools.util.schema_dict_util import evaluate_attribute, eval_simple_xpath, attrib_exists
    from masci_tools.io.io_nmmpmat import write_nmmpmat, write_nmmpmat_from_states, write_nmmpmat_from_orbitals

    #All lda+U procedures have to be considered since we need to keep the order
    species_base_path = get_tag_xpath(schema_dict, 'species')

    if species_name == 'all':
        species_xpath = species_base_path
    elif species_name[:4] == 'all-':  #format all-<string>
        species_xpath = f'{species_base_path}[contains(@name,"{species_name[4:]}")]'
    else:
        species_xpath = f'{species_base_path}[@name = "{species_name}"]'

    all_species = eval_xpath(xmltree, species_xpath, list_return=True)

    nspins = evaluate_attribute(xmltree, schema_dict, 'jspins')
    if 'l_mtnocoPot' in schema_dict['attrib_types']:
        if attrib_exists(xmltree, schema_dict, 'l_mtnocoPot', contains='Setup'):
            if evaluate_attribute(xmltree, schema_dict, 'l_mtnocoPot', contains='Setup'):
                nspins = 3

    if spin > nspins:
        raise ValueError(f'Invalid input: spin {spin} requested, but input has only {nspins} spins')

    all_ldau = eval_simple_xpath(xmltree, schema_dict, 'ldaU', contains='species', list_return=True)
    numRows = nspins * 14 * len(all_ldau)

    if state_occupations is not None:
        new_nmmpmat_entry = write_nmmpmat_from_states(orbital, state_occupations, phi=phi, theta=theta)
    elif orbital_occupations is not None:
        new_nmmpmat_entry = write_nmmpmat_from_orbitals(orbital, orbital_occupations, phi=phi, theta=theta)
    elif denmat is not None:
        new_nmmpmat_entry = write_nmmpmat(orbital, denmat, phi=phi, theta=theta)
    else:
        raise ValueError('Invalid definition of density matrix. Provide either state_occupations, '
                         'orbital_occupations or denmat')

    #Check that numRows matches the number of lines in nmmp_lines_copy
    #If not either there was an n_mmp_mat file present in Fleurinp before and a lda+u calculation
    #was added or removed or the n_mmp_mat file was initialized and after the fact lda+u procedures were added
    #or removed. In both cases the resolution of this modification is very involved so we throw an error
    if nmmplines is not None:
        #Remove blank lines
        while '' in nmmplines:
            nmmplines.remove('')
        if numRows != len(nmmplines):
            raise ValueError('The number of lines in n_mmp_mat does not match the number expected from '+\
                             'the inp.xml file. Either remove the existing file before making modifications '+\
                             'and only use set_nmmpmat after all modifications to the inp.xml')

    for species in all_species:
        current_name = get_xml_attribute(species, 'name')

        #Determine the place at which the given U procedure occurs
        ldau_index = None
        for index, ldau in enumerate(all_ldau):
            ldau_species = get_xml_attribute(ldau.getparent(), 'name')
            ldau_orbital = evaluate_attribute(ldau, schema_dict, 'l', contains='species')
            if current_name == ldau_species and ldau_orbital == orbital:
                ldau_index = index

        if ldau_index is None:
            raise KeyError(f'No LDA+U procedure found on species {current_name} with l={orbital}')

        #check if fleurinp has a specified n_mmp_mat file if not initialize it with 0
        if nmmplines is None:
            nmmplines = []
            for index in range(numRows):
                nmmplines.append(''.join(map(str, [f'{0.0:20.13f}' for x in range(7)])))

        #Select the right block from n_mmp_mat and overwrite it with denmatpad
        startRow = ((spin - 1) * len(all_ldau) + ldau_index) * 14

        nmmplines[startRow:startRow + 14] = new_nmmpmat_entry

    return nmmplines


def rotate_nmmpmat(xmltree, nmmplines, schema_dict, species_name, orbital, phi, theta):
    """
    Rotate the density matrix with the given angles phi and theta

    :param xmltree: an xmltree that represents inp.xml
    :param nmmplines: list of lines in the n_mmp_mat file
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param species_name: string, name of the species you want to change
    :param orbital: integer, orbital quantum number of the LDA+U procedure to be modified
    :param phi: float, angle (radian), by which to rotate the density matrix
    :param theta: float, angle (radian), by which to rotate the density matrix

    :raises ValueError: If something in the input is wrong
    :raises KeyError: If no LDA+U procedure is found on a species

    :returns: list with modified nmmplines
    """
    from masci_tools.util.xml.common_functions import eval_xpath, get_xml_attribute
    from masci_tools.util.schema_dict_util import evaluate_attribute, eval_simple_xpath, attrib_exists
    from masci_tools.io.io_nmmpmat import read_nmmpmat_block, rotate_nmmpmat_block, format_nmmpmat

    species_base_path = get_tag_xpath(schema_dict, 'species')

    if species_name == 'all':
        species_xpath = species_base_path
    elif species_name[:4] == 'all-':  #format all-<string>
        species_xpath = f'{species_base_path}[contains(@name,"{species_name[4:]}")]'
    else:
        species_xpath = f'{species_base_path}[@name = "{species_name}"]'

    all_species = eval_xpath(xmltree, species_xpath, list_return=True)

    nspins = evaluate_attribute(xmltree, schema_dict, 'jspins')
    if 'l_mtnocoPot' in schema_dict['attrib_types']:
        if attrib_exists(xmltree, schema_dict, 'l_mtnocoPot', contains='Setup'):
            if evaluate_attribute(xmltree, schema_dict, 'l_mtnocoPot', contains='Setup'):
                nspins = 3

    all_ldau = eval_simple_xpath(xmltree, schema_dict, 'ldaU', contains='species', list_return=True)
    numRows = nspins * 14 * len(all_ldau)

    #Check that numRows matches the number of lines in nmmp_lines_copy
    #If not either there was an n_mmp_mat file present in Fleurinp before and a lda+u calculation
    #was added or removed or the n_mmp_mat file was initialized and after the fact lda+u procedures were added
    #or removed. In both cases the resolution of this modification is very involved so we throw an error
    if nmmplines is not None:
        #Remove blank lines
        while '' in nmmplines:
            nmmplines.remove('')
        if numRows != len(nmmplines):
            raise ValueError('The number of lines in n_mmp_mat does not match the number expected from '+\
                             'the inp.xml file. Either remove the existing file before making modifications '+\
                             'and only use set_nmmpmat after all modifications to the inp.xml')
    else:
        raise ValueError('rotate_nmmpmat has to be called with a initialized density matrix')

    for species in all_species:
        current_name = get_xml_attribute(species, 'name')

        #Determine the place at which the given U procedure occurs
        ldau_index = None
        for index, ldau in enumerate(all_ldau):
            ldau_species = get_xml_attribute(ldau.getparent(), 'name')
            ldau_orbital = evaluate_attribute(ldau, schema_dict, 'l', contains='species')
            if current_name == ldau_species and ldau_orbital == orbital:
                ldau_index = index

        if ldau_index is None:
            raise KeyError(f'No LDA+U procedure found on species {current_name} with l={orbital}')

        denmat = []

        for spin in range(nspins):

            startRow = (spin * len(all_ldau) + ldau_index) * 14
            denmat = read_nmmpmat_block(nmmplines, spin * len(all_ldau) + ldau_index)

            denmat = rotate_nmmpmat_block(denmat, orbital, phi=phi, theta=theta)

            nmmplines[startRow:startRow + 14] = format_nmmpmat(denmat)

    return nmmplines


def validate_nmmpmat(xmltree, nmmplines, schema_dict):
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
    from masci_tools.util.xml.common_functions import get_xml_attribute
    from masci_tools.util.schema_dict_util import evaluate_attribute, eval_simple_xpath, attrib_exists

    nspins = evaluate_attribute(xmltree, schema_dict, 'jspins')
    if 'l_mtnocoPot' in schema_dict['attrib_types']:
        if attrib_exists(xmltree, schema_dict, 'l_mtnocoPot', contains='Setup'):
            if evaluate_attribute(xmltree, schema_dict, 'l_mtnocoPot', contains='Setup'):
                nspins = 3

    all_ldau = eval_simple_xpath(xmltree, schema_dict, 'ldaU', contains='species', list_return=True)
    numRows = nspins * 14 * len(all_ldau)

    tol = 0.01
    if nspins > 1:
        maxOcc = 1.0
    else:
        maxOcc = 2.0

    #Check that numRows matches the number of lines in nmmp_lines
    if nmmplines is not None:
        #Remove blank lines
        while '' in nmmplines:
            nmmplines.remove('')
        if numRows != len(nmmplines):
            raise ValueError('The number of lines in n_mmp_mat does not match the number expected from '+\
                             'the inp.xml file.')
    else:
        return

    #Now check for each block if the numbers make sense
    #(no numbers outside the valid area and no nonsensical occupations)
    for ldau_index, ldau in enumerate(all_ldau):

        orbital = evaluate_attribute(ldau, schema_dict, 'l', contains='species')
        species_name = get_xml_attribute(ldau.getparent(), 'name')

        for spin in range(nspins):
            startRow = (spin * len(all_ldau) + ldau_index) * 14

            for index in range(startRow, startRow + 14):
                currentLine = index - startRow
                currentRow = currentLine // 2

                line = nmmplines[index].split('    ')
                while '' in line:
                    line.remove('')
                nmmp = np.array([float(x) for x in line])

                outside_val = False
                if abs(currentRow - 3) > orbital:
                    if any(np.abs(nmmp) > 1e-12):
                        outside_val = True

                if currentLine % 2 == 0:
                    #m=-3 to m=0 real part
                    if any(np.abs(nmmp[:(3 - orbital) * 2]) > 1e-12):
                        outside_val = True

                else:
                    #m=0 imag part to m=3
                    if any(np.abs(nmmp[orbital * 2 + 1:]) > 1e-12):
                        outside_val = True

                if outside_val:
                    raise ValueError(f'Found value outside of valid range in for species {species_name}, spin {spin+1}'
                                     f' and l={orbital}')

                invalid_diag = False
                if spin < 2:
                    if currentRow - 3 <= 0 and currentLine % 2 == 0:
                        if nmmp[currentRow * 2] < -tol or nmmp[currentRow * 2] > maxOcc + tol:
                            invalid_diag = True
                    else:
                        if nmmp[(currentRow - 3) * 2 - 1] < -tol or nmmp[(currentRow - 3) * 2 - 1] > maxOcc + tol:
                            invalid_diag = True

                if invalid_diag:
                    raise ValueError(f'Found invalid diagonal element for species {species_name}, spin {spin+1}'
                                     f' and l={orbital}')
