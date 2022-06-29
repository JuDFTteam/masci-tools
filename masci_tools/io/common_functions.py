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
from __future__ import annotations

import io
from typing import IO, Any, Generator, Iterable, NamedTuple, TypeVar, Union, Tuple, List
import sys
if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  #type:ignore[misc]
import numpy as np
from collections.abc import Sequence
from masci_tools.util.typing import FileLike
####################################################################################

#helper functions used in calculation, parser etc.


def open_general(filename_or_handle: FileLike, iomode: str | None = None) -> IO[Any]:
    """
    Open a file directly from a path or use a file handle if that is given.
    Also take care of closed files by reopenning them.
    This is intended to be used like this::

        with open_general(outfile) as f:
            txt = f.readlines()
    """
    reopen_file = False
    # this is needed in order to make python2 and 3 work (in py3 file does not exist anymore)

    if not isinstance(filename_or_handle, io.IOBase):
        reopen_file = True

    if reopen_file:
        if iomode is None:
            iomode = 'r'
        f = open(filename_or_handle, iomode, encoding='utf8')  #type:ignore[arg-type]
    else:
        f = filename_or_handle  #type:ignore[assignment]
        if f.closed:  # reopen file if it was closed before
            if iomode is None:
                f = open(f.name, f.mode, encoding='utf8')
            else:
                f = open(f.name, iomode, encoding='utf8')  #pylint: disable=consider-using-with
        else:  # make sure reading the file now starts at the beginning again
            f.seek(0)

    return f


def get_outfile_txt(outfile):
    """Get the content of a file
    In case the outfile is a file handle, we just roll it back and read everything in again.
    For an ordinary file path we open the file in a context manager and then read it.
    """
    if getattr(outfile, 'readlines', None) is not None:
        outfile.seek(0)
        tmptxt = outfile.readlines()
    else:
        with open_general(outfile) as f:
            tmptxt = f.readlines()
    return tmptxt


def skipHeader(seq: Iterable[Any], n: int) -> Generator[Any, None, None]:
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


def filter_out_empty_dict_entries(dict_to_filter: dict) -> dict:
    """
    Filter out entries in a given dict that correspond to empty values.
    At the moment this is empty lists, dicts and None

    :param dict_to_filter: dict to filter

    :returns: dict without empty entries
    """

    EMPTY_VALUES: tuple[None, list, dict] = (None, [], {})

    return {key: val for key, val in dict_to_filter.items() if val not in EMPTY_VALUES}


def get_alat_from_bravais(bravais: np.ndarray, is3D: bool = True) -> float:
    bravais_tmp = bravais
    if not is3D:
        #take only in-plane lattice to find maximum as alat
        bravais_tmp = bravais[:2, :2]
    return np.sqrt(np.sum(bravais_tmp**2, axis=1)).max()


def search_string(searchkey: str, txt: Iterable[str]) -> int:
    iline = 0
    for line in txt:
        if searchkey in line:
            return iline
        iline += 1
    return -1


def angles_to_vec(magnitude: list | np.ndarray | float, theta: list | np.ndarray | float,
                  phi: list | np.ndarray | float) -> np.ndarray:
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
    vec_array = np.array(vec)

    if single_value_input:
        vec_array = vec_array[0]

    return vec_array


def get_Ang2aBohr() -> float:
    from masci_tools.util.constants import ANG_BOHR_KKR
    #warnings.warn(
    #    'get_Ang2aBohr is deprecated. Use 1/BOHR_A with the BOHR_A constant from the module masci_tools.util.constants instead',
    #    DeprecationWarning)
    return ANG_BOHR_KKR


def get_aBohr2Ang() -> float:
    from masci_tools.util.constants import ANG_BOHR_KKR
    #warnings.warn(
    #    'get_aBohr2Ang is deprecated. Use the BOHR_A constant from the module masci_tools.util.constants instead',
    #    DeprecationWarning)
    return 1.0 / ANG_BOHR_KKR


def get_Ry2eV() -> float:
    from masci_tools.util.constants import RY_TO_EV_KKR
    #warnings.warn(
    #    'get_Ry2eV is deprecated. Use the RY_TO_EV constant from the module masci_tools.util.constants instead',
    #    DeprecationWarning)
    return RY_TO_EV_KKR


def vec_to_angles(vec: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray] | tuple[float, float, float]:
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
        magnitude, theta, phi = np.array(magnitude), np.array(theta), np.array(phi)  #type:ignore
    else:
        magnitude, theta, phi = magnitude[0], theta[0], phi[0]
    return magnitude, theta, phi  #type:ignore


def get_version_info(outfile: FileLike) -> tuple[str, str, str]:
    tmptxt = get_outfile_txt(outfile)
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


def get_corestates_from_potential(potfile: FileLike = 'potential') -> tuple[list, list, list]:
    """Read core states from potential file"""
    txt = get_outfile_txt(potfile)

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


def get_highest_core_state(nstates: int, energies: np.ndarray, lmoments: np.ndarray) -> tuple[int, float, str]:
    """Find highest lying core state from list of core states, needed to find and check energy contour"""
    idx = energies.argmax()
    lval = lmoments[idx]
    nquant = sum(lmoments == lval) + lval
    level_descr = f"{nquant}{'spdfgh'[lval]}"

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

    with open_general(dosfile) as f:
        f.readline()  # dummy readin of header, may be replaced later
        npot = int(f.readline().split()[0])
        iemax = int(f.readline().split()[0])
        lmax = int(f.readline().split()[0])

        dosnew_all_atoms = []
        dos_all_atoms = []

        for i1 in range(npot):
            #print('Reading potential',i1)
            # Read header (not used)
            for _ in range(3):
                f.readline()

            # extract EF
            ef = float(f.readline().split()[7])

            # some more dummy lines
            for _ in range(5, 9 + 1):
                f.readline()

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
                f.readline()  # dummy line

        dosnew_all_atoms = np.array(dosnew_all_atoms)
        dos_all_atoms = np.array(dos_all_atoms)

    if return_original:
        return ef, dos_all_atoms, dosnew_all_atoms
    return ef, dosnew_all_atoms


def get_ef_from_potfile(potfile: FileLike) -> float:
    """
    extract fermi energy from potfile
    """
    tmptxt = get_outfile_txt(potfile)
    ef = float(tmptxt[3].split()[1])
    return ef


def convert_to_pystd(value: Any) -> Any:
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
    elif isinstance(value, np.str_):
        value = str(value)
    elif isinstance(value, dict):
        for key, val in value.items():
            value[key] = convert_to_pystd(val)
    return value


def camel_to_snake(name: str) -> str:
    """
    Converts camelCase to snake_case variable names
    Used in the Fleur parser to convert attribute names from the xml files
    """
    name = name.replace('-', '')
    return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')


def convert_to_fortran(val: Any, quote_strings: bool = True) -> str:
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
        val_str = f'{val:d}'
    elif isinstance(val, numbers.Real):
        val_str = f'{val:18.10e}'.replace('e', 'd')
    elif isinstance(val, str):
        if quote_strings:
            val_str = f"'{val!s}'"
        else:
            val_str = f'{val!s}'
    else:
        raise ValueError(f"Invalid value '{val}' of type '{type(val)}' passed, accepts only booleans, ints, "
                         'floats and strings')

    return val_str


def convert_to_fortran_string(string: str) -> str:
    """
    converts some parameter strings to the format for the inpgen
    :param string: some string
    :returns: string in right format (extra "" if not already present)
    """
    if not string.strip().startswith("\"") or \
       not string.strip().endswith("\""):
        return f'"{string}"'
    return string


def is_sequence(arg: Any) -> bool:
    """
    Checks if arg is a sequence
    """
    return isinstance(arg, Sequence) and not isinstance(arg, str)


VectorType: TypeAlias = Union[Tuple[float, float, float], List[float], np.ndarray]
_TVectorType = TypeVar('_TVectorType', bound=VectorType)
"""Generic type variable for atom position types"""


def abs_to_rel(vector: _TVectorType, cell: list[list[float]] | np.ndarray) -> _TVectorType:
    """
    Converts a position vector in absolute coordinates to relative coordinates.

    :param vector: list or np.array of length 3, vector to be converted
    :param cell: Bravais matrix of a crystal 3x3 Array, List of list or np.array
    :return: list of length 3 of scaled vector, or False if vector was not length 3
    """
    if not isinstance(vector, np.ndarray):
        vector_np = np.array(vector)
    else:
        vector_np = vector

    if not isinstance(cell, np.ndarray):
        cell = np.array(cell)

    if len(vector_np) != 3:
        raise ValueError('Vector must be of length 3')

    relative_vector = vector_np @ np.linalg.inv(cell)

    if isinstance(vector, list):
        return relative_vector.tolist()
    if isinstance(vector, tuple):
        return tuple(relative_vector)  #type:ignore
    return relative_vector  #type:ignore[return-value]


def abs_to_rel_f(vector: _TVectorType, cell: list[list[float]] | np.ndarray, pbc: tuple[bool, bool,
                                                                                        bool]) -> _TVectorType:
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
    if not isinstance(vector, np.ndarray):
        vector_np = np.array(vector)
    else:
        vector_np = vector

    if not isinstance(cell, np.ndarray):
        cell = np.array(cell)

    if len(vector_np) != 3:
        raise ValueError('Vector must be of length 3')

    if pbc[2]:
        raise ValueError('FLEUR can not handle this type of film coordinate')

    relative_vector_f = vector_np[:2] @ np.linalg.inv(cell[0:2, 0:2])
    relative_vector = np.append(relative_vector_f, vector_np[2])

    if isinstance(vector, list):
        return relative_vector.tolist()
    if isinstance(vector, tuple):
        return tuple(relative_vector)  #type:ignore
    return relative_vector  #type:ignore[return-value]


def rel_to_abs(vector: _TVectorType, cell: list[list[float]] | np.ndarray) -> _TVectorType:
    """
    Converts a position vector in internal coordinates to absolute coordinates
    in Angstrom.

    :param vector: list or np.array of length 3, vector to be converted
    :param cell: Bravais matrix of a crystal 3x3 Array, List of list or np.array
    :return: list of length 3 of scaled vector, or False if vector was not length 3
    """
    if not isinstance(vector, np.ndarray):
        vector_np = np.array(vector)
    else:
        vector_np = vector

    if not isinstance(cell, np.ndarray):
        cell = np.array(cell)

    if len(vector_np) != 3:
        raise ValueError('Vector must be of length 3')

    absolute_vector = vector_np @ cell

    if isinstance(vector, list):
        return absolute_vector.tolist()
    if isinstance(vector, tuple):
        return tuple(absolute_vector)  #type:ignore
    return absolute_vector


def rel_to_abs_f(vector: _TVectorType, cell: list[list[float]] | np.ndarray) -> _TVectorType:
    """
    Converts a position vector in internal coordinates to absolute coordinates
    in Angstrom for a film structure (2D).
    """
    # TODO this currently only works if the z-coordinate is the one with no pbc
    # Therefore if a structure with x non pbc is given this should also work.
    # maybe write a 'tranform film to fleur_film routine'?
    if not isinstance(vector, np.ndarray):
        vector_np = np.array(vector)
    else:
        vector_np = vector

    if not isinstance(cell, np.ndarray):
        cell = np.array(cell)

    if len(vector_np) != 3:
        raise ValueError('Vector must be of length 3')

    absolute_vector_f = vector_np[:2] @ cell[0:2, 0:2]
    absolute_vector: np.ndarray = np.append(absolute_vector_f, vector_np[2])

    if isinstance(vector, list):
        return absolute_vector.tolist()
    if isinstance(vector, tuple):
        return tuple(absolute_vector)  #type:ignore
    return absolute_vector  #type:ignore[return-value]


def find_symmetry_relation(from_pos: VectorType,
                           to_pos: VectorType,
                           rotations: list[np.ndarray],
                           shifts: list[np.ndarray],
                           cell: list[list[float]] | np.ndarray,
                           relative_pos: bool = False,
                           film: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """
    Find symmetry relation between the given vectors. This functions assumes
    that a symmetry relation exists otherwise an error is raised

    :param from_pos: vector to rotate
    :param to_pos: vector to rotate to
    :param rotations: list of np.arrays with the given symmetry rotations
    :param shifts: list of np.arrays with the given shifts for the symmetry operations
    :param cell: Bravais matrix of a crystal 3x3 Array, List of list or np.array
    :param relative_pos: bool if True the given vectors are assuemd to be in internal coordinates
    :param film: bool if True the vectors are assumed to be film coordinates

    :returns: tuple of rotation and shift mapping ``from_pos`` to ``to_pos``

    :raises ValueError: If no symmetry relation is found
    """

    def lattice_shifts() -> Generator[np.ndarray, None, None]:
        for i in range(-2, 3):
            for j in range(-2, 3):
                for k in range(-2, 3):
                    yield np.array([i, j, k], dtype=int)

    if not relative_pos:
        if film:
            from_pos = abs_to_rel_f(from_pos, cell, (True, True, False))
            to_pos = abs_to_rel_f(to_pos, cell, (True, True, False))
        else:
            from_pos = abs_to_rel(from_pos, cell)
            to_pos = abs_to_rel(to_pos, cell)

    cell = np.array(cell)
    cell_square = np.matmul(cell.T, cell)

    for rot, shift in zip(rotations, shifts):
        rot_pos = np.matmul(rot, np.array(from_pos)) + shift
        diff = rot_pos - np.array(to_pos)
        for lat_shift in lattice_shifts():
            length = np.sqrt(np.dot(np.matmul(diff + lat_shift, cell_square), diff + lat_shift))
            if length < 1e-4:
                return rot, shift

    raise ValueError(f'No symmetry relation found between {from_pos} and {to_pos}')


class AtomSiteProperties(NamedTuple):
    """
    namedtuple used for input output of atom sites
    """
    position: list[float]  #TODO could be made generic with VectorType
    symbol: str
    kind: str


def get_wigner_matrix(l: int, alpha: float, beta: float, gamma: float = 0.0, inverse: bool = False) -> np.ndarray:
    """Produces the wigner rotation matrix for the density matrix

    :param l: int, orbital quantum number
    :param alpha: float, angle (radian) corresponds to euler angle alpha
    :param beta: float, angle (radian) corresponds to euler angle beta
    :param gamma: float, angle (radian) corresponds to euler angle gamma
    """
    if inverse:
        alpha, beta, gamma = -gamma, -beta, -alpha

    d_wigner = np.zeros((7, 7), dtype=complex)
    for m in range(-l, l + 1):
        for mp in range(-l, l + 1):
            base = np.sqrt(fac(l + m) * fac(l - m) * fac(l + mp) * fac(l - mp))
            base *= np.exp(-1j * alpha * mp) * np.exp(-1j * gamma * m)

            for x in range(max(0, m - mp), min(l - mp, l + m) + 1):
                denom = fac(l - mp - x) * fac(l + m - x) * fac(x) * fac(x + mp - m)

                d_wigner[mp + 3, m + 3] += base/denom * (-1)**x * np.cos(beta/2.0)**(2*l+m-mp-2*x) \
                                          * np.sin(beta/2.0)**(2*x+mp-m)
            d_wigner[mp + 3, m + 3] *= (-1)**(m - mp)

    return d_wigner


def fac(n: int) -> int:
    """Returns the factorial of n"""
    if n < 2:
        return 1
    return n * fac(n - 1)


def get_spin_rotation(alpha: float, beta: float) -> np.ndarray:
    """
    Get matrix to rotate the spin frame by the given angles alpha/beta

    :param alpha: angle in radians
    :param beta: angle in radians
    """
    return np.array([[np.exp(-1j * alpha / 2.0) * np.cos(beta / 2),
                      np.exp(-1j * alpha / 2.0) * np.sin(beta / 2)],
                     [-np.exp(1j * alpha / 2.0) * np.sin(beta / 2),
                      np.exp(1j * alpha / 2.0) * np.cos(beta / 2)]])


def get_pauli_matrix(direction: Literal['x', 'y', 'z'], alpha: float = 0.0, beta: float = 0.0) -> np.ndarray:
    """
    Get the pauli matrix with additional rotation applied

    :param direction: str (x,y or z) for which pauli matrix to return
    :param alpha: angle in radians
    :param beta: angle in radians
    """
    if direction == 'x':
        sigma = np.array([[0, 1], [1, 0]], dtype=complex)
    elif direction == 'y':
        sigma = np.array([[0, -1j], [1j, 0]], dtype=complex)
    elif direction == 'z':
        sigma = np.array([[1, 0], [0, -1]], dtype=complex)
    else:
        raise ValueError(f'Invalid value {direction} for direction argument')

    if abs(alpha) > 1e-12 or abs(beta) > 1e-12:
        rot = get_spin_rotation(alpha, beta)
        sigma = rot.T.conj() @ sigma @ rot

    return sigma
