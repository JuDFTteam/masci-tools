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
from masci_tools.io.common_functions import get_wigner_matrix
import numpy as np

def set_nmmpmat(xmltree, nmmplines, schema_dict, species_name, orbital, spin,\
                occStates=None, denmat=None, phi=None, theta=None):
    """Routine sets the block in the n_mmp_mat file specified by species_name, orbital and spin
    to the desired density matrix

    :param fleurinp_tree_copy: an xmltree that represents inp.xml
    :param nmmp_lines_copy: list of lines in the n_mmp_mat file
    :param species_name: string, name of the species you want to change
    :param orbital: integer, orbital quantum number of the LDA+U procedure to be modified
    :param spin: integer, specifies which spin block should be modified
    :param occStates: list, sets the diagonal elements of the density matrix and everything
                      else to zero
    :param denmat: matrix, specify the density matrix explicitely
    :param phi: float, optional angle (radian), by which to rotate the density matrix before writing it
    :param theta: float, optional angle (radian), by which to rotate the density matrix before writing it

    :raises ValueError: If something in the input is wrong
    :raises KeyError: If no LDA+U procedure is found on a species
    """
    from masci_tools.util.xml.common_xml_util import eval_xpath, get_xml_attribute
    from masci_tools.util.schema_dict_util import evaluate_attribute, eval_simple_xpath

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
        if evaluate_attribute(xmltree, schema_dict, 'l_mtnocoPot'):
            nspins = 3

    if spin > nspins:
        raise ValueError(f'Invalid input: spin {spin} requested, but input has only {nspins} spins')

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

    if phi is not None or theta is not None:
        if phi is None:
            phi = 0.0
        if theta is None:
            theta = 0.0
        d_wigner = get_wigner_matrix(orbital, phi, theta)

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

        if occStates is not None:
            #diagonal density matrix
            denmatpad = np.zeros((7, 7), dtype=complex)

            #Fill out the outer states with zero
            occStatespad = np.zeros(7, dtype=complex)
            occStatespad[3 - orbital:4 + orbital] = occStates[:]

            for i, occ in enumerate(occStatespad):
                denmatpad[i, i] = occ
        elif denmat is not None:
            #density matrix is completely specified
            denmatpad = np.zeros((7, 7), dtype=complex)
            denmatpad[3 - orbital:4 + orbital, 3 - orbital:4 + orbital] = denmat
        else:
            raise ValueError('Invalid definition of density matrix. Provide either occStates or denmat')

        if phi is not None and theta is not None:
            #Rotate the density matrix
            denmatpad = d_wigner.T.conj().dot(denmatpad.dot(d_wigner))

        #check if fleurinp has a specified n_mmp_mat file if not initialize it with 0
        if nmmplines is None:
            nmmplines = []
            for index in range(numRows):
                nmmplines.append(''.join(map(str, [f'{0.0:20.13f}' for x in range(7)])))

        #Select the right block from n_mmp_mat and overwrite it with denmatpad
        startRow = ((spin - 1) * len(all_ldau) + ldau_index) * 14
        for index in range(startRow, startRow + 14):
            currentLine = index - startRow
            currentRow = currentLine // 2
            if currentLine % 2 == 0:
                #Line ends with a real part
                nmmplines[index] = ''.join(map(str, [f'{x.real:20.13f}{x.imag:20.13f}'\
                                                           for x in denmatpad[currentRow, :3]])) +\
                                         f'{denmatpad[currentRow, 3].real:20.13f}'
            else:
                #Line begins with a imaginary part
                nmmplines[index] = f'{denmatpad[currentRow, 3].imag:20.13f}' +\
                                         ''.join(map(str, [f'{x.real:20.13f}{x.imag:20.13f}'\
                                                           for x in denmatpad[currentRow, 4:]]))

    return nmmplines


def rotate_nmmpmat(xmltree, nmmplines, schema_dict, species_name, orbital, phi, theta):
    """
    Rotate the density matrix with the given angles phi and theta

    :param fleurinp_tree_copy: an xmltree that represents inp.xml
    :param nmmp_lines_copy: list of lines in the n_mmp_mat file
    :param species_name: string, name of the species you want to change
    :param orbital: integer, orbital quantum number of the LDA+U procedure to be modified
    :param phi: float, angle (radian), by which to rotate the density matrix
    :param theta: float, angle (radian), by which to rotate the density matrix

    :raises ValueError: If something in the input is wrong
    :raises KeyError: If no LDA+U procedure is found on a species
    """
    from masci_tools.util.xml.common_xml_util import eval_xpath, get_xml_attribute
    from masci_tools.util.schema_dict_util import evaluate_attribute, eval_simple_xpath

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
        if evaluate_attribute(xmltree, schema_dict, 'l_mtnocoPot'):
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

    d_wigner = get_wigner_matrix(orbital, phi, theta)

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

        denmat = [np.zeros((7, 7), dtype=complex) for spin in range(nspins)]

        for spin in range(nspins):
            startRow = (spin * len(all_ldau) + ldau_index) * 14
            for index, line in enumerate(nmmplines[startRow:startRow + 14]):
                currentLine = index - startRow
                currentRow = currentLine // 2
                if currentLine % 2 == 0:
                    rowData = [float(x) for x in line.split()]
                else:
                    rowData.extend([float(x) for x in line.split()])
                    rowData = [x + 1j * y for x, y in zip(rowData[:-1], rowData[1:])]
                    denmat[spin][currentRow, :] += np.array(rowData)

        #Rotate the density matrix
        denmat = [d_wigner.T.conj().dot(denmat_spin.dot(d_wigner)) for denmat_spin in denmat]

        #Select the right block from n_mmp_mat and overwrite it with denmatpad
        for spin, denmatrot in enumerate(denmat):
            startRow = (spin * len(all_ldau) + ldau_index) * 14
            for index in range(startRow, startRow + 14):
                currentLine = index - startRow
                currentRow = currentLine // 2
                if currentLine % 2 == 0:
                    #Line ends with a real part
                    nmmplines[index] = ''.join(map(str, [f'{x.real:20.13f}{x.imag:20.13f}'\
                                                               for x in denmatrot[currentRow, :3]])) +\
                                             f'{denmatrot[currentRow, 3].real:20.13f}'
                else:
                    #Line begins with a imaginary part
                    nmmplines[index] = f'{denmatrot[currentRow, 3].imag:20.13f}' +\
                                             ''.join(map(str, [f'{x.real:20.13f}{x.imag:20.13f}'\
                                                               for x in denmatrot[currentRow, 4:]]))

    return nmmplines


def validate_nmmpmat(xmltree, nmmplines, schema_dict):
    """
    Checks that the given nmmp_lines is valid with the given fleurinp_tree

    Checks that the number of blocks is as expected from the inp.xml and each
    block does not contain non-zero elements outside their size given by the
    orbital quantum number in the inp.xml. Additionally the occupations, i.e.
    diagonal elements are checked that they are in between 0 and the maximum
    possible occupation

    :param fleurinp_tree_copy: an xmltree that represents inp.xml
    :param nmmp_lines_copy: list of lines in the n_mmp_mat file

    :raises ValueError: if any of the above checks are violated.
    """
    from masci_tools.util.xml.common_xml_util import get_xml_attribute
    from masci_tools.util.schema_dict_util import evaluate_attribute, eval_simple_xpath

    nspins = evaluate_attribute(xmltree, schema_dict, 'jspins')
    if 'l_mtnocoPot' in schema_dict['attrib_types']:
        if evaluate_attribute(xmltree, schema_dict, 'l_mtnocoPot'):
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
