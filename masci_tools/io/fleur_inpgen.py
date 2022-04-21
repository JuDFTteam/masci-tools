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
This module contains functionality for writing input files for the input generator of fleur
"""
from __future__ import annotations

import io
import numpy as np
import os
import copy
import warnings
from typing import Iterable, Sequence, Any, cast
try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

from masci_tools.util.constants import PERIODIC_TABLE_ELEMENTS, BOHR_A
from masci_tools.util.typing import FileLike
from masci_tools.util.xml.converters import convert_to_fortran_bool, convert_from_fortran_bool
from masci_tools.io.common_functions import abs_to_rel_f, abs_to_rel, convert_to_fortran_string
from masci_tools.io.common_functions import rel_to_abs, rel_to_abs_f, AtomSiteProperties
from masci_tools.io.common_functions import convert_to_fortran

__all__ = ('write_inpgen_file', 'read_inpgen_file', 'AtomDictProperties', 'Kinds')

# Inpgen file structure, order is important
POSSIBLE_NAMELISTS = [
    'title', 'input', 'lattice', 'gen', 'shift', 'factor', 'qss', 'soc', 'atom', 'comp', 'exco', 'expert', 'film',
    'kpt', 'end'
]
POSSIBLE_PARAMS: dict[str, list[str]] = {
    'input': ['film', 'cartesian', 'cal_symm', 'checkinp', 'symor', 'oldfleur'],
    'lattice': ['latsys', 'a0', 'a', 'b', 'c', 'alpha', 'beta', 'gamma'],
    'atom': ['id', 'z', 'rmt', 'dx', 'jri', 'lmax', 'lnonsph', 'ncst', 'econfig', 'bmu', 'lo', 'element', 'name'],
    'comp': ['jspins', 'frcor', 'ctail', 'kcrel', 'gmax', 'gmaxxc', 'kmax'],
    'exco': ['xctyp', 'relxc'],
    'expert': ['spex', 'primCellZ'],
    'film': ['dvac', 'dtild'],
    'soc': ['theta', 'phi'],
    'qss': ['x', 'y', 'z'],
    'kpt': ['nkpt', 'kpts', 'div1', 'div2', 'div3', 'tkb', 'tria', 'gamma'],
    'title': []
}

VALUE_ONLY_NAMELISTS = ['soc', 'qss']

# convert these 'booleans' to the inpgen format.
REPLACER_VALUES_BOOL = [True, False, 'True', 'False', 't', 'T', 'F', 'f']


class AtomDictProperties(TypedDict, total=False):
    """
    TypedDict for the atom properties
    """
    position: list[float] | tuple[float, float, float] | np.ndarray
    kind_name: str


class Kinds(TypedDict, total=False):
    """
    TypedDict for the kinds
    """
    symbols: Sequence[str]
    name: str
    weights: Sequence[float]


def write_inpgen_file(cell: np.ndarray | list[list[float]],
                      atom_sites: (Sequence[AtomSiteProperties] | Sequence[tuple[list[float], str, str]] |
                                   Sequence[AtomDictProperties]),
                      kinds: Iterable[Kinds] | None = None,
                      return_contents: bool = False,
                      file: FileLike = 'inpgen.in',
                      pbc: tuple[bool, bool, bool] = (True, True, True),
                      input_params: dict[str, Any] | None = None,
                      significant_figures_cell: int = 9,
                      significant_figures_positions: int = 10,
                      convert_from_angstroem: bool = True) -> str | None:
    """Write an input file for the fleur inputgenerator 'inpgen' from given inputs

    :param cell: 3x3 arraylike. The bravais matrix of the structure, in Angstrom by default
    :param atom_sites: either list of a dict containing the keys absolute 'position' in Angstrom (default) and 'kind_name', i.e

                       .. code-block::

                          [{'position': (0.0, 0.0, -1.0545708047819), 'kind_name': 'Fe123'},
                           {'position': (1.4026317387183, 1.9836207751336, 0.0), 'kind_name': 'Pt'},
                           {'position': (0.0, 0.0, 1.4026318234924), 'kind_name': 'Pt'}]

                       In this case the argument ``kinds`` is required. The other possibility is a list of tuples
                       of the form of :py:class:`~masci_tools.io.common_functions.AtomSiteProperties`

    :param kinds: a list of kind information containing the keys symbols, weights, mass, name i.e.

                      .. code-block::

                        [{'symbols': ('Fe',), 'weights': (1.0,), 'mass': 55.845, 'name': 'Fe123'},
                         {'symbols': ('Pt',), 'weights': (1.0,), 'mass': 195.084, 'name': 'Pt'}]

                  Required when atom_sites is a list of dicts

    :param file: Path or filehandle where the file should be written to. Defaults to 'inpgen.in' in the current folder.
    :param pbc: tuple of boolean length 3, optional, Periodic boundary conditions of the structure. Defaults to (True, True, True).
    :param input_params: Optional dict containing further namelist which should be written to the file. Defaults to None.
    :param significant_figures_cell: int, how many decimal places should be written for the bravais matrix (default: 9)
    :param significant_figures_positions: int, how many decimal places should be written for the atom positions (default: 10)
    :param convert_from_angstroem: optional boolean, if True the positions and elements of the bravais matrix are converted to bohr
                                   from Angstroem

    :raises ValueError: If some input is wrong or inconsistent.

    Comments: This was extracted out of aiida-fleur for more general use,
    the datastructures stayed very close to what aiida provides (to_raw()), it may not
    yet be convenient for all usecases. I.e data so far has to be given in Angstrom and will be converted to fleur units.
    # This could be made optional
    """

    # Get the connection between coordination number and element symbol
    _atomic_numbers = {data['symbol']: num for num, data in PERIODIC_TABLE_ELEMENTS.items()}

    # If two lattices are given, via the input &lattice
    # and a structure of some form
    # currently is not allow the use of &lattice
    _use_aiida_structure = True

    # Default title
    _inp_title = 'A Fleur input generator calculation with aiida'
    bulk = True
    film = False

    # some keywords require a string " around them in the input file.
    string_replace = ['econfig', 'lo', 'element', 'name', 'xctyp']

    # of some keys only the values are written to the file, specify them here.

    # Scaling comes from the Structure
    # but we have to convert from Angstrom to a.u (bohr radii)
    scaling_factors = [1.0, 1.0, 1.0]
    scaling_lat = 1.  # /bohr_to_ang = 0.52917720859
    if convert_from_angstroem:
        scaling_pos = 1. / BOHR_A  # Angstrom to atomic
    else:
        scaling_pos = 1.0
    own_lattice = False  # not _use_aiida_structure

    if all(isinstance(site, dict) for site in atom_sites):
        atom_sites = cast(Sequence[AtomDictProperties], atom_sites)
        if kinds is None:
            raise ValueError('The argument kinds is required, when atom_sites is provided as dicts')

        symbols = [[kind['symbols'][0]] for site in atom_sites for kind in kinds if kind['name'] == site['kind_name']]
        if any(len(symbol) == 0 for symbol in symbols):
            raise ValueError('Failed getting symbols for all kinds. Check that all needed kinds are given')
        atom_sites = [
            AtomSiteProperties(position=list(site['position']), symbol=kind[0], kind=site['kind_name'])
            for site, kind in zip(atom_sites, symbols)
        ]

    elif any(not isinstance(site, AtomSiteProperties) for site in atom_sites):
        if kinds is not None:
            raise ValueError('The argument kinds is not required, when atom_sites is provided as tuples')
        atom_sites = [AtomSiteProperties(*site) for site in atom_sites]

    #Workaround: cast(Sequence[AtomsiteProperties], atom_sites) does not work for some reason
    atom_sites = [cast(AtomSiteProperties, site) for site in atom_sites]

    ##########################################
    ############# INPUT CHECK ################
    ##########################################
    # first check existence of structure and if 1D, 2D, 3D

    if False in pbc:
        bulk = False
        film = True

    # check existence of parameters (optional)
    if input_params is None:
        input_params = {}

    # we write always out rel coordinates, because that's the way FLEUR uses
    # them best. we have to convert them from abs, because that's how they
    # are stored in a Structure node. cartesian=F is default
    if 'input' not in input_params:
        input_params['input'] = {}

    input_params['input']['cartesian'] = False
    if film:
        input_params['input']['film'] = True

    namelists_toprint = POSSIBLE_NAMELISTS

    if 'title' in list(input_params.keys()):
        _inp_title = input_params.pop('title')
    input_params = cast('dict[str, dict[str, Any]]', input_params)

    input_params = copy.deepcopy(input_params)
    # TODO validate type of values of the input parameter keys ?
    # check input_parameters
    for name, parameters in input_params.items():
        if 'atom' in name:  # this namelist can be specified more often
            # special atom namelist needs to be set for writing,
            #  but insert it in the right spot!
            index = namelists_toprint.index('atom') + 1
            namelists_toprint.insert(index, name)
            name = 'atom'
        if name not in POSSIBLE_NAMELISTS:
            raise ValueError(f"The namelist '{name}' is not supported by the fleur"
                             f" inputgenerator. Check on the fleur website or add '{name}'"
                             'to _possible_namelists.')
        for para in parameters:
            if para not in POSSIBLE_PARAMS[name]:
                raise ValueError(f"The property '{para}' is not supported by the "
                                 f"namelist '{name}'. "
                                 'Check the fleur website, or if it really is,'
                                 ' update _possible_params. ')
            if para in string_replace:
                # TODO check if its in the parameter dict
                parameters[para] = convert_to_fortran_string(parameters[para])
            # things that are in string replace can never be a bool
            # Otherwise input where someone given the title 'F' would fail...
            elif parameters[para] in REPLACER_VALUES_BOOL:
                # because 1/1.0 == True, and 0/0.0 == False
                # maybe change in convert_to_fortran that no error occurs
                if isinstance(parameters[para], (bool, str)):
                    parameters[para] = convert_to_fortran_bool(parameters[para])
    # in fleur it is possible to give a lattice namelist
    if 'lattice' in input_params:
        own_lattice = True
        if cell is not None:  # two structures given?
            # which one should be prepared? TODO: log warning or even error
            if _use_aiida_structure:
                input_params.pop('lattice', {})
                own_lattice = False

    ##############################
    # END OF INITIAL INPUT CHECK #
    ##############################

    #######################################################
    ######### PREPARE PARAMETERS FOR INPUT FILE ###########
    #######################################################

    #### STRUCTURE_PARAMETERS ####
    scaling_factor_card = ''
    cell_parameters_card = ''
    # We allow to set the significant figures format, because sometimes
    # inpgen has numerical problems which are not there with less precise formatting
    if not own_lattice:
        for vector in cell:
            scaled = [a * scaling_pos for a in vector]  # scaling_pos=1./bohr_to_ang
            cell_parameters_card += ' '.join([f'{value:18.{significant_figures_cell}f}' for value in scaled]) + '\n'
        scaling_factor_card += ' '.join([f'{value:18.{significant_figures_cell}f}' for value in scaling_factors]) + '\n'

    #### ATOMIC_POSITIONS ####
    if own_lattice:
        # TODO with own lattice atomic positions have to come from somewhere
        # else.... User input?
        raise ValueError('fleur lattice needs also the atom position as input,'
                         ' not implemented yet, sorry!')

    atom_positions_text = []
    natoms = len(atom_sites)
    # for FLEUR true, general not, because you could put several
    # atoms on a site
    # TODO this feature might change in Fleur, do different. that in inpgen kind gets a name, which will also be the name in fleur inp.xml.
    # now user has to make kind_name = atom id.
    for site in atom_sites:

        if kinds is not None:
            for kin in kinds:
                if kin['name'] == site.kind:
                    kind = kin
            # then we do not at atoms with weights smaller one
            if kind.get('weights', [1])[0] < 1.0:
                natoms = natoms - 1
                # Log message?
                continue

        atomic_number = _atomic_numbers[site.symbol]
        atomic_number_name = str(atomic_number)
        if atomic_number == 0:  # 'X' element for vacancies
            natoms = natoms - 1
            continue
        # per default we use relative coordinates in Fleur
        # we have to scale back to atomic units from angstrom
        pos = list(site.position)
        if bulk:
            vector_rel = abs_to_rel(pos, cell)
        elif film:
            vector_rel = abs_to_rel_f(pos, cell, pbc)
            vector_rel[2] = vector_rel[2] * scaling_pos
        position_str = ' '.join([f'{value:18.{significant_figures_positions}f}' for value in vector_rel])

        if site.symbol != site.kind:  # This is an important fact, if user renames it becomes a new atomtype or species!
            label = ''
            try:
                # Kind names can be more then numbers now, this might need to be reworked
                head = site.kind.rstrip('0123456789')
                kind_namet = int(site.kind[len(head):])
                #if int(kind_name[len(head)]) > 4:
                #    raise InputValidationError('New specie name/label should start with a digit smaller than 4')
            except ValueError:
                warnings.warn(f'Warning: Kind name {site.kind} will be ignored and not used to set a charge number.')
            else:
                atomic_number_name = f'{atomic_number}.{kind_namet}'
                label = str(kind_namet)
            atom_positions_text.append(f'    {atomic_number_name:>7} {position_str} {label}\n')
        else:
            atom_positions_text.append(f'    {atomic_number_name:>7} {position_str}\n')
    # TODO check format
    # we write it later, since we do not know what natoms is before the loop...
    atom_positions_str = f'    {natoms:3}\n' + ''.join(atom_positions_text)

    #### Kpts ####
    # TODO: kpts
    # kpoints_card = ""#.join(kpoints_card_list)
    #del kpoints_card_list

    #######################################
    #### WRITE ALL CARDS IN INPUT FILE ####

    inpgen_file_content = []

    # first write title
    inpgen_file_content.append(f'{_inp_title}\n')
    # then write &input namelist
    inpgen_file_content.append('&input')
    # namelist content; set to {} if not present, so that we leave an
    # empty namelist
    namelist = input_params.pop('input', {})
    for k, val in sorted(namelist.items()):
        inpgen_file_content.append(get_input_data_text(k, val, value_only=False))
    inpgen_file_content.append('/\n')

    # Write lattice information now
    inpgen_file_content.append(cell_parameters_card)
    inpgen_file_content.append(f'{scaling_lat:18.10f}\n')
    inpgen_file_content.append(scaling_factor_card)
    inpgen_file_content.append('\n')

    # Write Atomic positions
    inpgen_file_content.append(atom_positions_str)

    # Write namelists after atomic positions
    for namels_name in namelists_toprint:
        namelist = input_params.pop(namels_name, {})
        if namelist:
            if 'atom' in namels_name:
                namels_name = 'atom'
            inpgen_file_content.append(f'&{namels_name}\n')
            for k, val in sorted(namelist.items(), reverse=namels_name == 'soc'):
                inpgen_file_content.append(get_input_data_text(k, val, value_only=namels_name in VALUE_ONLY_NAMELISTS))
            inpgen_file_content.append('/\n')
    # inpgen_file_content.append(kpoints_card)

    if input_params:
        raise ValueError('input_params leftover: The following namelists are specified'
                         ' in input_params, but are '
                         'not valid namelists for the current type of calculation: '
                         f"{','.join(list(input_params.keys()))}")

    inpgen_file_content_str = ''.join(inpgen_file_content)

    if not return_contents:
        if isinstance(file, io.IOBase):
            file.write(inpgen_file_content_str)
        else:
            with open(file, 'w', encoding='utf-8') as inpfile:  #type:ignore[arg-type]
                inpfile.write(inpgen_file_content_str)

    return inpgen_file_content_str


def get_input_data_text(key: str, val: Any, value_only: bool, mapping: dict[str, Any] | None = None) -> str:
    """
    Given a key and a value, return a string (possibly multiline for arrays)
    with the text to be added to the input file.

    :param key: the flag name
    :param val: the flag value. If it is an array, a line for each element
                is produced, with variable indexing starting from 1.
                Each value is formatted using the convert_to_fortran function.
    :param mapping: Optional parameter, must be provided if val is a dictionary.
                    It maps each key of the 'val' dictionary to the corresponding
                    list index. For instance, if ``key='magn'``,
                    ``val = {'Fe': 0.1, 'O': 0.2}`` and ``mapping = {'Fe': 2, 'O': 1}``,
                    this function will return the two lines ``magn(1) = 0.2`` and
                    ``magn(2) = 0.1``. This parameter is ignored if 'val'
                    is not a dictionary.
    """
    # I don't try to do iterator=iter(val) and catch TypeError because
    # it would also match strings
    # I check first the dictionary, because it would also match
    # hasattr(__iter__)
    if isinstance(val, dict):
        if mapping is None:
            raise ValueError("If 'val' is a dictionary, you must provide also "
                             "the 'mapping' parameter")

        # At difference with the case of a list, at the beginning
        # list_of_strings
        # is a list of 2-tuples where the first element is the idx, and the
        # second is the actual line. This is used at the end to
        # resort everything.
        list_of_strings = []
        for elemk, itemval in val.items():
            try:
                idx = mapping[elemk]
            except KeyError as exc:
                raise ValueError(f"Unable to find the key '{elemk}' in the mapping dictionary") from exc

            list_of_strings.append(f'  {key}({idx})={convert_to_fortran(itemval)} ')
            #changed {0}({2}) = {1}\n".format

        #Sort according to the mapping then rejoin the string
        list_of_strings = sorted(list_of_strings, key=lambda key: mapping[key])  #type:ignore
        return ''.join(list_of_strings)
    if not isinstance(val, str) and hasattr(val, '__iter__'):
        if value_only:
            list_of_strings = [f'  ({idx + 1}){convert_to_fortran(itemval)} ' for idx, itemval in enumerate(val)]
        else:
            # a list/array/tuple of values
            list_of_strings = [f'  {key}({idx + 1})={convert_to_fortran(itemval)} ' for idx, itemval in enumerate(val)]
        return ''.join(list_of_strings)

    # single value
    #return "  {0}={1} ".format(key, convert_to_fortran(val))
    if value_only:
        return f' {val} '
    return f'  {key}={val} '


def read_inpgen_file(
    file: FileLike,
    convert_to_angstroem: bool = True
) -> tuple[np.ndarray | None, list[AtomSiteProperties], tuple[bool, bool, bool], dict[str, Any]]:
    """
    Method which reads in an inpgen input file and parses the structure and name lists information.

    :param file: path to the file to read or opened file handle
    :param convert_to_angstroem: bool if True the bravais matrix (and atom positions) are converted to angstroem

    :returns: tuple of bravais matrix, atom sites, periodic boundary conditions and parameters
    """
    pbc = (True, True, True)
    input_params = {}
    namelists_raw = {}
    atom_sites = []
    cell: np.ndarray | None = np.zeros((3, 3))
    lattice_information = []

    if isinstance(file, io.IOBase):
        contents = file.read()
    else:
        if os.path.exists(file):  #type:ignore[arg-type]
            with open(file, encoding='utf-8') as f:  #type:ignore[arg-type]
                contents = f.read()
        else:
            contents = file

    content_lines = contents.split('\n')
    # Strip out comments from the inpgen file
    content_lines = [line.partition('!')[0].strip() for line in content_lines if line.partition('!')[0].strip() != '']
    # The first line is the title
    if not content_lines[0].startswith('&'):
        input_params['title'] = content_lines[0]

    content_lines = content_lines[1:]
    if '&lattice' in contents:
        cell = None

    # each line starting with a & is a name list, we can not assume the line will end with a \
    # since this is not fully required
    name_list_start = False
    for line in content_lines:
        if line.startswith('&'):
            if not name_list_start:
                name_list_start = True
                namelist_name = line.split('&')[1].split()[0]
                namelist_raw = line.split(f'&{namelist_name}')[1]
            else:
                name_list_start = False
        else:
            if name_list_start:
                namelist_raw += line
            else:
                lattice_information.append(line)
        if line.endswith('/'):
            name_list_start = False
            j = 0
            while namelist_name in namelists_raw:
                namelist_name = namelist_name + f'{j}'
            namelists_raw[namelist_name] = namelist_raw

    for key, val in namelists_raw.items():
        parsed_name_dict = {}
        #dict(val)
        indx = 0

        split_string = val.rstrip('/').split()

        if 'atom' in key:
            keyt = 'atom'
        else:
            keyt = key

        if keyt not in VALUE_ONLY_NAMELISTS:
            for param in split_string.copy():
                if '=' not in param:
                    split_string[split_string.index(param) - 1] += f' {param}'
                    split_string.remove(param)

        for param in split_string:
            if param in ('/', ''):
                continue
            pval = param.rstrip('/')
            pval = pval.strip()
            pval = pval.split('=')
            if keyt not in VALUE_ONLY_NAMELISTS:
                pval[1] = pval[1].strip('"')
            # works for all namelist except gen and sym
            if 'atom' in key:
                keyt = 'atom'
            else:
                keyt = key
            if pval[0] not in POSSIBLE_PARAMS[keyt] and keyt not in VALUE_ONLY_NAMELISTS:
                raise ValueError(f'Value {pval[0]} is not allowed as inpgen input of namelist {keyt}.')
            if keyt in VALUE_ONLY_NAMELISTS:
                att_name = POSSIBLE_PARAMS[keyt][indx]
                value = pval[0]
                indx += 1
            else:
                att_name = pval[0]
                value = pval[1]

            if value.replace('.', '').isnumeric():
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            elif value in REPLACER_VALUES_BOOL:
                value = convert_from_fortran_bool(value)

            parsed_name_dict[att_name] = value
        input_params[key] = parsed_name_dict

    film = input_params.get('input', {}).get('film', False)
    if film:
        pbc = (True, True, False)

    if cell is not None:
        if len(lattice_information) <= 6:
            raise ValueError('Too few lines found for lattice+atom information')
        cell_information, atom_information = lattice_information[:5], lattice_information[5:]
        cell = np.array([[float(val) for val in value.split()] for value in cell_information[:3]])

        global_scaling = float(cell_information[3])
        column_scaling = np.array([float(val) for val in cell_information[4].split()])

        cell *= global_scaling
        cell = cell * column_scaling
        if convert_to_angstroem:
            cell *= BOHR_A  #type:ignore
    else:
        atom_information = lattice_information
        warnings.warn('Lattice was specified via the &lattice namelist'
                      'Atom positions will be returned as relative positions')

    if len(atom_information) <= 1:
        raise ValueError('Too few lines found for atom information')

    for atom_string in atom_information[1:]:

        atom_info = atom_string.split()

        nz, _, add_id = atom_info[0].partition('.')
        element: str = PERIODIC_TABLE_ELEMENTS[int(nz)]['symbol']  #type:ignore
        pos = np.array([float(val) for val in atom_info[1:4]])

        if cell is not None:
            if film:
                pos = rel_to_abs_f(pos, cell)
                if convert_to_angstroem:
                    pos[2] *= BOHR_A
            else:
                pos = rel_to_abs(pos, cell)

        kind_name: str = None  #type:ignore
        if add_id:
            kind_name = f'{element}-{add_id}'
        else:
            kind_name = element

        if len(atom_info) == 5:
            kind_name = atom_info[4]

        atom_sites.append(AtomSiteProperties(position=list(pos), symbol=element, kind=kind_name))

    return cell, atom_sites, pbc, input_params
