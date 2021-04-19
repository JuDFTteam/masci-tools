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
Here commonly used functions that do not need aiida-stuff (i.e. can be tested
without a database) are collected.
"""
import io
import numpy as np
import warnings
####################################################################################

#helper functions used in calculation, parser etc.


def open_general(filename_or_handle, iomode=None):
    """
    Open a file directly from a path or use a file handle if that is given.
    Also take care of closed files by reopenning them.
    This is intended to be used like this::

        f = open_general(outfile)
        with f: # make sure the file is properly closed
            txt = f.readlines()
    """
    reopen_file = False
    # this is needed in order to make python2 and 3 work (in py3 file does not exist anymore)

    if not isinstance(filename_or_handle, io.IOBase):
        reopen_file = True

    if reopen_file:
        if iomode is None:
            iomode = u'r'
        f = open(filename_or_handle, iomode)
    else:
        f = filename_or_handle
        if f.closed:  # reopen file if it was closed before
            if iomode is None:
                f = open(f.name, f.mode)
            else:
                f = open(f.name, iomode)
        else:  # make sure reading the file now starts at the beginning again
            f.seek(0)
    return f


def skipHeader(seq, n):
    """Iterate over a sequence skipping the first n elements

    Args:
        seq (iterable): Iterable sequence
        n (int): Number of Elements to skip in the beginning of the sequence

    Yields:
        item: Elements in seq after the first n elements
    """
    for i, item in enumerate(seq):
        if i >= n:
            yield item


def filter_out_empty_dict_entries(dict_to_filter):
    """
    Filter out entries in a given dict that correspond to empty values.
    At the moment this is empty lists, dicts and None

    :param dict_to_filter: dict to filter

    :returns: dict without empty entries
    """

    EMPTY_VALUES = (None, [], {})

    return {key: val for key, val in dict_to_filter.items() if val not in EMPTY_VALUES}


def get_alat_from_bravais(bravais, is3D=True):
    bravais_tmp = bravais
    if not is3D:
        #take only in-plane lattice to find maximum as alat
        bravais_tmp = bravais[:2, :2]
    return np.sqrt(np.sum(bravais_tmp**2, axis=1)).max()


def search_string(searchkey, txt):
    iline = 0
    for line in txt:
        if searchkey in line:
            return iline
        iline += 1
    return -1


def angles_to_vec(magnitude, theta, phi):
    """
    convert (magnitude, theta, phi) to (x,y,z)

    theta/phi need to be in radians!

    Input can be single number, list of numpy.ndarray data
    Returns x,y,z vector
    """

    # correct data type if necessary
    if isinstance(magnitude, list):
        magnitude = np.array(magnitude)
    if isinstance(theta, list):
        theta = np.array(theta)
    if isinstance(phi, list):
        phi = np.array(phi)
    single_value_input = False
    if not isinstance(magnitude, np.ndarray):
        magnitude = np.array([magnitude])
        single_value_input = True
    if not isinstance(theta, np.ndarray):
        theta = np.array([theta])
        single_value_input = True
    if not isinstance(phi, np.ndarray):
        phi = np.array([phi])
        single_value_input = True

    vec = []
    for mag_i, phi_i, theta_i in zip(magnitude, phi, theta):
        r_inplane = mag_i * np.sin(theta_i)
        x = r_inplane * np.cos(phi_i)
        y = r_inplane * np.sin(phi_i)
        z = np.cos(theta_i) * mag_i
        vec.append([x, y, z])
    vec = np.array(vec)

    if single_value_input:
        vec = vec[0]

    return vec


def get_Ang2aBohr():
    from masci_tools.util.constants import BOHR_A
    warnings.warn(
        'get_Ang2aBohr is deprecated. Use 1/BOHR_A with the BOHR_A constant from the module masci_tools.util.constants instead',
        DeprecationWarning)
    return 1.0 / BOHR_A


def get_aBohr2Ang():
    from masci_tools.util.constants import BOHR_A
    warnings.warn(
        'get_aBohr2Ang is deprecated. Use the BOHR_A constant from the module masci_tools.util.constants instead',
        DeprecationWarning)
    return BOHR_A


def get_Ry2eV():
    from masci_tools.util.constants import RY_TO_EV
    warnings.warn(
        'get_Ry2eV is deprecated. Use the RY_TO_EV constant from the module masci_tools.util.constants instead',
        DeprecationWarning)
    return RY_TO_EV


def vec_to_angles(vec):
    """
    converts vector (x,y,z) to (magnitude, theta, phi)
    """
    magnitude, theta, phi = [], [], []
    if len(vec) == 3 and len(np.shape(vec)) < 2:
        vec = np.array([vec])
        multiple_entries = False
    else:
        multiple_entries = True

    for vec_i in vec:
        phi.append(np.arctan2(vec_i[1], vec_i[0]))
        r_inplane = np.sqrt(vec_i[0]**2 + vec_i[1]**2)
        theta.append(np.arctan2(r_inplane, vec_i[2]))
        magnitude.append(np.sqrt(r_inplane**2 + vec_i[2]**2))
    if multiple_entries:
        magnitude, theta, phi = np.array(magnitude), np.array(theta), np.array(phi)
    else:
        magnitude, theta, phi = magnitude[0], theta[0], phi[0]
    return magnitude, theta, phi


def get_version_info(outfile):
    f = open_general(outfile)
    with f:
        tmptxt = f.readlines()
    itmp = search_string('Code version:', tmptxt)
    if itmp == -1:  # try to find serial number from header of file
        itmp = search_string('# serial:', tmptxt)
        code_version = tmptxt[itmp].split(':')[1].split('_')[1].strip()
        compile_options = tmptxt[itmp].split(':')[1].split('_')[2].strip()
        serial_number = tmptxt[itmp].split(':')[1].split('_')[3].strip()
    else:
        code_version = tmptxt.pop(itmp).split(':')[1].strip()
        itmp = search_string('Compile options:', tmptxt)
        compile_options = tmptxt.pop(itmp).split(':')[1].strip()
        itmp = search_string('serial number for files:', tmptxt)
        serial_number = tmptxt.pop(itmp).split(':')[1].strip()
    return code_version, compile_options, serial_number


def get_corestates_from_potential(potfile='potential'):
    """Read core states from potential file"""
    f = open_general(potfile)
    with f:
        txt = f.readlines()

    #get start of each potential part
    istarts = [iline for iline in range(len(txt)) if 'POTENTIAL' in txt[iline]]
    print(istarts)

    n_core_states = []  #number of core states per potential
    e_core_states = []  #energies of core states
    l_core_states = []  #angular momentum index, i.e. 0=s, 1=p etc...
    for pot_index, start_index in enumerate(istarts):
        line = txt[start_index + 6]
        n = int(line.split()[0])
        print(pot_index, n)
        n_core_states.append(n)
        elevels = np.zeros(n)  #temp array for energies
        langmom = np.zeros(n, dtype=int)  #temp array for angular momentum index
        for icore in range(n):
            line = txt[start_index + 7 + icore].split()
            langmom[icore] = int(line[0])
            elevels[icore] = float(line[1].replace('D', 'E'))
        e_core_states.append(elevels)
        l_core_states.append(langmom)

    return n_core_states, e_core_states, l_core_states


def get_highest_core_state(nstates, energies, lmoments):
    """Find highest lying core state from list of core states, needed to find and check energy contour"""
    idx = energies.argmax()
    lval = lmoments[idx]
    nquant = sum(lmoments == lval) + lval
    level_descr = '%i%s' % (nquant, 'spdfgh'[lval])

    return lval, energies[idx], level_descr


def interpolate_dos(
    dosfile,
    return_original=False,
):
    r"""
    interpolation function copied from complexdos3 fortran code

    Principle of DOS here: Two-point contour integration
    for DOS in the middle of the two points. The input DOS
    and energy must be complex. Parameter deltae should be
    of the order of magnitude of eim::

              <-2*deltae->   _
                   /\        |     DOS=(n(1)+n(2))/2 + (n(1)-n(2))*eim/deltae
                  /  \       |
                (1)  (2)   2*i*eim=2*i*pi*Kb*Tk
                /      \     |
               /        \    |
        ------------------------ (Real E axis)

    :param input: either absolute path of 'complex.dos' file or file handle to it

    :returns: E_Fermi, numpy array of interpolated dos

    :note: output units are in Ry!
    """

    f = open_general(dosfile)
    with f:
        text = f.readline()  # dummy readin of header, may be replaced later
        npot = int(f.readline().split()[0])
        iemax = int(f.readline().split()[0])
        lmax = int(f.readline().split()[0])

        dosnew_all_atoms = []
        dos_all_atoms = []

        for i1 in range(npot):
            #print('Reading potential',i1)
            # Read header (not used)
            for iheader in range(3):
                text = f.readline()

            # extract EF
            ef = float(f.readline().split()[7])

            # some more dummy lines
            for iheader in range(5, 9 + 1):
                text = f.readline()

            # now header is done. start reading DOS
            # Read dos: (total dos stored at DOS(LMAX+1,IE))
            dos_l_cmplx = []
            for ie in range(iemax):
                tmpline = f.readline().replace('(', '').replace(')', '').replace(',', '').split()
                ez = float(tmpline[0]) + 1j * float(tmpline[1])
                dostmp_complex = [[tmpline[len(tmpline) - 2], tmpline[len(tmpline) - 1]]]
                dostmp_complex += [[tmpline[iline], tmpline[iline + 1]] for iline in range(2, len(tmpline) - 2, 2)]
                dostmp = [ez] + [float(ds[0]) + 1j * float(ds[1]) for ds in dostmp_complex]
                dos_l_cmplx.append(dostmp)
            dos_l_cmplx = np.array(dos_l_cmplx)
            dos_l = np.imag(dos_l_cmplx.copy())
            dos_l[:, 0] = np.real(dos_l_cmplx.copy()[:, 0])
            dos_all_atoms.append(dos_l)

            # Compute and write out corrected dos at new (middle) energy points:
            dosnew = []
            ez = dos_l_cmplx[:, 0]
            for ie in range(1, iemax - 1):
                deltae = np.real(ez[ie + 1] - ez[ie])
                eim = np.imag(ez[ie])
                enew = np.real(ez[ie])  # Real quantity

                tmpdos = [enew]
                for ll in range(1, lmax + 3):
                    t = (dos_l_cmplx[ie - 1, ll] - dos_l_cmplx[ie + 1, ll]) * 0.5 * (0.0 + eim * 1j) / deltae
                    #print ie+1, ll,  dos_l_cmplx[ie, ll], deltae, eim, t, shape(dos_l_cmplx[ie]), lmax
                    #tmpdos.append(dos_l_cmplx[ie, ll] + 0.5*(dos_l_cmplx[ie-1, ll]-dos_l_cmplx[ie+1, ll])*(0.+1j*eim)/deltae)
                    tmpdos.append(dos_l_cmplx[ie, ll] + t)
                tmpdos = np.array(tmpdos)
                # build imaginary part (factor -1/2pi is already included)
                tmpdos = np.array([np.real(tmpdos[0])] + [np.imag(ds) for ds in tmpdos[1:]])
                dosnew.append(tmpdos)

            # save to big array with all atoms
            dosnew_all_atoms.append(dosnew)

            if i1 != npot:
                text = f.readline()  # dummy line

        dosnew_all_atoms = np.array(dosnew_all_atoms)
        dos_all_atoms = np.array(dos_all_atoms)

    if return_original:
        return ef, dos_all_atoms, dosnew_all_atoms
    else:
        return ef, dosnew_all_atoms


def get_ef_from_potfile(potfile):
    """
    extract fermi energy from potfile
    """
    f = open_general(potfile)
    with f:
        txt = f.readlines()
    ef = float(txt[3].split()[1])
    return ef


def convert_to_pystd(value):
    """Recursively convert numpy datatypes to standard python, needed by aiida-core.

    Usage:
        converted = convert_to_pystd(to_convert)

    where `to_convert` can be a dict, array, list, or single valued variable
    """
    if isinstance(value, np.ndarray):
        value = list(value)
        value = convert_to_pystd(value)
    elif isinstance(value, list):
        for index, val in enumerate(value):
            value[index] = convert_to_pystd(val)
    elif isinstance(value, tuple):
        value = tuple(convert_to_pystd(val) for val in value)
    elif isinstance(value, np.integer):
        value = int(value)
    elif isinstance(value, np.floating):
        value = float(value)
    elif isinstance(value, np.str):
        value = str(value)
    elif isinstance(value, dict):
        for key, val in value.items():
            value[key] = convert_to_pystd(val)
    return value


def camel_to_snake(name):
    """
    Converts camelCase to snake_case variable names
    Used in the Fleur parser to convert attribute names from the xml files
    """
    name = name.replace('-', '')
    return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')


def convert_to_fortran(val, quote_strings=True):
    """
    :param val: the value to be read and converted to a Fortran-friendly string.
    """
    # Note that bool should come before integer, because a boolean matches also
    # isinstance(...,int)
    import numbers

    if isinstance(val, (bool, np.bool_)):
        if val:
            val_str = '.true.'
        else:
            val_str = '.false.'
    elif isinstance(val, numbers.Integral):
        val_str = '{:d}'.format(val)
    elif isinstance(val, numbers.Real):
        val_str = ('{:18.10e}'.format(val)).replace('e', 'd')
    elif isinstance(val, str):
        if quote_strings:
            val_str = "'{!s}'".format(val)
        else:
            val_str = '{!s}'.format(val)
    else:
        raise ValueError(f"Invalid value '{val}' of type '{type(val)}' passed, accepts only booleans, ints, "
                         'floats and strings')

    return val_str


def convert_to_fortran_string(string):
    """
    converts some parameter strings to the format for the inpgen
    :param string: some string
    :returns: string in right format (extra "")
    """
    return f'"{string}"'


def is_sequence(arg):
    """
    Checks if arg is a sequence
    """
    if isinstance(arg, str):
        return False
    elif hasattr(arg, '__iter__'):
        return True
    elif not hasattr(arg, 'strip') and hasattr(arg, '__getitem__'):
        return True
    else:
        return False


def abs_to_rel(vector, cell):
    """
    Converts a position vector in absolute coordinates to relative coordinates.

    :param vector: list or np.array of length 3, vector to be converted
    :param cell: Bravais matrix of a crystal 3x3 Array, List of list or np.array
    :return: list of length 3 of scaled vector, or False if vector was not length 3
    """

    if len(vector) == 3:
        cell_np = np.array(cell)
        inv_cell_np = np.linalg.inv(cell_np)
        postionR = np.array(vector)
        # np.matmul(inv_cell_np, postionR)#
        new_rel_post = np.matmul(postionR, inv_cell_np)
        new_rel_pos = list(new_rel_post)
        return new_rel_pos
    else:
        return False


def abs_to_rel_f(vector, cell, pbc):
    """
    Converts a position vector in absolute coordinates to relative coordinates
    for a film system.

    :param vector: list or np.array of length 3, vector to be converted
    :param cell: Bravais matrix of a crystal 3x3 Array, List of list or np.array
    :param pbc: Boundary conditions, List or Tuple of 3 Boolean
    :return: list of length 3 of scaled vector, or False if vector was not length 3
    """
    # TODO this currently only works if the z-coordinate is the one with no pbc
    # Therefore if a structure with x non pbc is given this should also work.
    # maybe write a 'tranform film to fleur_film routine'?
    if len(vector) == 3:
        if not pbc[2]:
            # leave z coordinate absolute
            # convert only x and y.
            postionR = np.array(vector)
            postionR_f = np.array(postionR[:2])
            cell_np = np.array(cell)
            cell_np = np.array(cell_np[0:2, 0:2])
            inv_cell_np = np.linalg.inv(cell_np)
            # np.matmul(inv_cell_np, postionR_f)]
            new_xy = np.matmul(postionR_f, inv_cell_np)
            new_rel_pos_f = [new_xy[0], new_xy[1], postionR[2]]
            return new_rel_pos_f
        else:
            print('FLEUR can not handle this type of film coordinate')
    else:
        return False


def rel_to_abs(vector, cell):
    """
    Converts a position vector in internal coordinates to absolute coordinates
    in Angstrom.

    :param vector: list or np.array of length 3, vector to be converted
    :param cell: Bravais matrix of a crystal 3x3 Array, List of list or np.array
    :return: list of legth 3 of scaled vector, or False if vector was not lenth 3
    """
    if len(vector) == 3:
        cell_np = np.array(cell)
        postionR = np.array(vector)
        new_abs_post = np.matmul(postionR, cell_np)
        new_abs_pos = list(new_abs_post)
        return new_abs_pos
    else:
        return False


def rel_to_abs_f(vector, cell):
    """
    Converts a position vector in internal coordinates to absolute coordinates
    in Angstrom for a film structure (2D).
    """
    # TODO this currently only works if the z-coordinate is the one with no pbc
    # Therefore if a structure with x non pbc is given this should also work.
    # maybe write a 'tranform film to fleur_film routine'?
    if len(vector) == 3:
        postionR = np.array(vector)
        postionR_f = np.array(postionR[:2])
        cell_np = np.array(cell)
        cell_np = np.array(cell_np[0:2, 0:2])
        new_xy = np.matmul(postionR_f, cell_np)
        new_abs_pos_f = [new_xy[0], new_xy[1], postionR[2]]
        return new_abs_pos_f
    else:
        return False


def get_wigner_matrix(l, phi, theta):
    """Produces the wigner rotation matrix for the density matrix

    :param l: int, orbital quantum number
    :param phi: float, angle (radian) corresponds to euler angle alpha
    :param theta: float, angle (radian) corresponds to euler angle beta
    """
    d_wigner = np.zeros((7, 7), dtype=complex)
    for m in range(-l, l + 1):
        for mp in range(-l, l + 1):
            base = np.sqrt(fac(l + m) * fac(l - m) * fac(l + mp) * fac(l - mp))
            base *= np.exp(-1j * phi * mp)

            for x in range(max(0, m - mp), min(l - mp, l + m) + 1):
                denom = fac(l - mp - x) * fac(l + m - x) * fac(x) * fac(x + mp - m)

                d_wigner[m + 3, mp + 3] += base/denom * (-1)**x * np.cos(theta/2.0)**(2*l+m-mp-2*x) \
                                          * np.sin(theta/2.0)**(2*x+mp-m)

    return d_wigner


def fac(n):
    """Returns the factorial of n"""
    if n < 2:
        return 1
    else:
        return n * fac(n - 1)
