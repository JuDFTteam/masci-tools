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
Simple IO routines for creating text for nmmp_mat files
"""
import numpy as np


def format_nmmpmat(denmat, orbital=None, phi=None, theta=None):
    """
    Format a given 7x7 complex numpy array into the format for the n_mmp_mat file

    Results in list of 14 strings. Every 2 lines correspond to one row in array
    Real and imaginary parts are formatted with 20.13f in alternating order

    :param denmat: numpy array (7x7) and complex for formatting

    :raises ValueError: If denmat has wrong shape or datatype

    :returns: list of str formatted in lines for the n_mmp_mat file
    """

    if denmat.shape != (7, 7):
        raise ValueError(f'Matrix has wrong shape for formatting: {denmat.shape}')

    if denmat.dtype != complex:
        raise ValueError(f'Matrix has wrong dtype for formatting: {denmat.dtype}')

    #Now we generate the text in the format expected in the n_mmp_mat file
    nmmp_lines = []
    for row in denmat:

        nmmp_lines.append(''.join([f'{x.real:20.13f}{x.imag:20.13f}' for x in row[:3]]) + f'{row[3].real:20.13f}')
        nmmp_lines.append(f'{row[3].imag:20.13f}' + ''.join([f'{x.real:20.13f}{x.imag:20.13f}' for x in row[4:]]))

    return nmmp_lines


def rotate_nmmpmat_block(denmat, orbital, phi=None, theta=None):
    """
    Rotate the given 7x7 complex numpy array with the d-wigner matrix
    corresponding to the given orbital and angles

    :param denmat: complex numpy array of shape 7x7
    :param orbital: int of the orbital for the current block
    :param phi: float, angle (radian), by which to rotate the density matrix
    :param theta: float, angle (radian), by which to rotate the density matrix

    :returns: denmat rotated by the d-wigner matrix
    """
    from masci_tools.io.common_functions import get_wigner_matrix

    if theta is None and phi is None:
        return denmat

    if phi is None:
        phi = 0.0
    if theta is None:
        theta = 0.0

    d_wigner = get_wigner_matrix(orbital, phi, theta)
    #Rotate the density matrix
    denmat = d_wigner.T.conj().dot(denmat.dot(d_wigner))

    return denmat


def write_nmmpmat(orbital, denmat, phi=None, theta=None):
    """
    Generate list of str for n_mmp_mat file from given numpy array

    :param orbital: int of the orbital for the current block
    :param denmat: complex numpy array of shape (2*orbital+1 x 2*orbital+1) with the wanted occupations
    :param phi: float, angle (radian), by which to rotate the density matrix
    :param theta: float, angle (radian), by which to rotate the density matrix

    :returns: list of str formatted in lines for the n_mmp_mat file
    """

    denmat_padded = np.zeros((7, 7), dtype=complex)
    denmat_padded[3 - orbital:4 + orbital, 3 - orbital:4 + orbital] = denmat

    if theta is not None or phi is not None:
        denmat_padded = rotate_nmmpmat_block(denmat_padded, orbital, phi=phi, theta=theta)

    return format_nmmpmat(denmat_padded, orbital=orbital, phi=phi, theta=theta)


def write_nmmpmat_from_states(orbital, state_occupations, phi=None, theta=None):
    """
    Generate list of str for n_mmp_mat file from diagonal occupations

    :param orbital: int of the orbital for the current block
    :param state_occupations: list like with length 2*orbital+1 with the occupations of the diagonals
    :param phi: float, angle (radian), by which to rotate the density matrix
    :param theta: float, angle (radian), by which to rotate the density matrix

    :returns: list of str formatted in lines for the n_mmp_mat file
    """

    #diagonal density matrix
    denmat = np.zeros((2 * orbital + 1, 2 * orbital + 1), dtype=complex)

    for i, occ in enumerate(state_occupations):
        denmat[i, i] = occ

    return write_nmmpmat(orbital, denmat, phi=phi, theta=theta)


def write_nmmpmat_from_orbitals(orbital, orbital_occupations, phi=None, theta=None):
    """
    Generate list of str for n_mmp_mat file from orbital occupations

    orbital occupations are provided in the following order
    (expressed as the spherical harmonics since it can be used for all orbitals):

        - Y_l^0
        - 1/sqrt(2) (Y_l^-1 + Y_l^1)
        - i/sqrt(2) (Y_l^-1 - Y_l^1)
        - 1/sqrt(2) (Y_l^-2 + Y_l^2)
        - i/sqrt(2) (Y_l^-2 - Y_l^2)
        - and so on ...

    :param orbital: int of the orbital for the current block
    :param orbital_occupations: list like with length 2*orbital+1 with the occupations of the orbitals
    :param phi: float, angle (radian), by which to rotate the density matrix
    :param theta: float, angle (radian), by which to rotate the density matrix

    :returns: list of str formatted in lines for the n_mmp_mat file
    """

    denmat = np.zeros((2 * orbital + 1, 2 * orbital + 1), dtype=complex)

    for index, occ in enumerate(orbital_occupations):

        if index == 0:
            denmat[orbital, orbital] = occ
        else:
            m = (index + 1) // 2
            if index % 2 == 1:
                denmat[orbital - m, orbital - m] += 1 / 2 * occ
                denmat[orbital + m, orbital + m] += 1 / 2 * occ
                denmat[orbital + m, orbital - m] += 1 / 2 * occ
                denmat[orbital - m, orbital + m] += 1 / 2 * occ
            else:
                denmat[orbital - m, orbital - m] += 1 / 2 * occ
                denmat[orbital + m, orbital + m] += 1 / 2 * occ
                denmat[orbital + m, orbital - m] -= 1 / 2 * occ
                denmat[orbital - m, orbital + m] -= 1 / 2 * occ

    return write_nmmpmat(orbital, denmat, phi=phi, theta=theta)


def read_nmmpmat_block(nmmp_lines, block_index):
    """
    Convert 14 line block of given nmmp_lines into 7x7 complex numpy array

    :param nmmplines: list of lines in the n_mmp_mat file
    :param block_index: int specifying which 14 line block to convert

    :returns: 7x7 complex numpy array of the numbers in the given block
    """
    denmat = np.zeros((7, 7), dtype=complex)

    start_row = block_index * 14

    for index, line in enumerate(nmmp_lines[start_row:start_row + 14]):
        currentRow = index // 2
        if index % 2 == 0:
            rowData = [float(x) for x in line.split()]
        else:
            rowData.extend([float(x) for x in line.split()])
            rowData = [num[0] + 1j * num[1] for indx, num in enumerate(zip(rowData[:-1], rowData[1:])) if indx % 2 == 0]
            denmat[currentRow, :] += np.array(rowData)

    return denmat
