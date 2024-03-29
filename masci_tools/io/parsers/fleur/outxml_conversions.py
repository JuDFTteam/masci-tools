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
This module contains custom conversion functions for the outxml_parser, which
cannot be handled by the standard parsing framework
"""
from __future__ import annotations

from datetime import date
import numpy as np
from masci_tools.util.constants import HTR_TO_EV
from masci_tools.io.common_functions import convert_to_pystd, abs_to_rel, abs_to_rel_f
from typing import Any
from logging import Logger

from . import conversion_function


@conversion_function
def convert_htr_to_ev(out_dict: dict[str, Any],
                      name: str,
                      converted_name: str | None = None,
                      pop: bool = False,
                      add_unit: bool = True,
                      logger: Logger | None = None) -> dict[str, Any]:
    """
    Convert value from htr to eV
    """

    if pop:
        old = out_dict.pop(name, None)
    else:
        old = out_dict.get(name)

    if converted_name is None:
        converted_name = f'{old}_ev'

    if add_unit:
        out_dict[f'{converted_name}_units'] = 'eV'

    if old is None:
        if name in out_dict:
            if logger is not None:
                logger.warning(f'convert_htr_to_ev cannot convert None to eV (Name: {name})')
            out_dict[converted_name] = None
        return out_dict

    old = old[-1]
    if old is not None:
        out_dict.setdefault(converted_name, []).append(old * HTR_TO_EV)
    else:
        if logger is not None:
            logger.warning(f'convert_htr_to_ev cannot convert None to eV (Name: {name})')
        out_dict.setdefault(converted_name, []).append(None)

    return out_dict


@conversion_function
def calculate_total_magnetic_moment(out_dict: dict[str, Any], logger: Logger) -> dict[str, Any]:
    """
    Calculate the the total magnetic moment per cell

    :param out_dict: dict with the already parsed information
    """
    total_charge = out_dict.get('spin_dependent_charge_total', None)

    if total_charge is None:
        if logger is not None:
            logger.warning('calculate_total_magnetic_moment got None')
        return out_dict

    total_charge = total_charge[-1]
    if isinstance(total_charge, list):
        if 'total_magnetic_moment_cell' not in out_dict:
            out_dict['total_magnetic_moment_cell'] = []

        out_dict['total_magnetic_moment_cell'].append(convert_to_pystd(np.abs(total_charge[0] - total_charge[1])))

    return out_dict


@conversion_function
def calculate_walltime(out_dict: dict[str, Any], logger: Logger) -> dict[str, Any]:
    """
    Calculate the walltime from start and end time

    :param out_dict: dict with the already parsed information
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised
    """

    if out_dict['start_date']['time'] is not None:
        starttimes = out_dict['start_date']['time'].split(':')
    else:
        starttimes = [0, 0, 0]
        msg = 'Starttime was unparsed, inp.xml prob not complete, do not believe the walltime!'
        if logger is not None:
            logger.warning(msg)

    if out_dict['end_date']['time'] is not None:
        endtimes = out_dict['end_date']['time'].split(':')
    else:
        endtimes = [0, 0, 0]
        msg = 'Endtime was unparsed, inp.xml prob not complete, do not believe the walltime!'
        if logger is not None:
            logger.warning(msg)

    if out_dict['start_date']['date'] is not None:
        start_date = out_dict['start_date']['date']
    else:
        start_date = None
        msg = 'Startdate was unparsed, inp.xml prob not complete, do not believe the walltime!'
        if logger is not None:
            logger.warning(msg)

    if out_dict['end_date']['date'] is not None:
        end_date = out_dict['end_date']['date']
    else:
        end_date = None
        msg = 'Enddate was unparsed, inp.xml prob not complete, do not believe the walltime!'
        if logger is not None:
            logger.warning(msg)

    offset = 0
    if start_date is not None and end_date is not None:
        if start_date != end_date:
            date_sl = [int(ent) for ent in start_date.split('/')]
            date_el = [int(ent) for ent in end_date.split('/')]
            date_s = date(*date_sl)
            date_e = date(*date_el)
            diff = date_e - date_s
            offset = diff.days * 86400

    time = offset + (int(endtimes[0]) - int(starttimes[0])) * 60 * 60 + (
        int(endtimes[1]) - int(starttimes[1])) * 60 + int(endtimes[2]) - int(starttimes[2])
    out_dict['walltime'] = time
    out_dict['walltime_units'] = 'seconds'

    return out_dict


@conversion_function
def convert_ldau_definitions(out_dict: dict[str, Any], logger: Logger) -> dict[str, Any]:
    """
    Convert the parsed information from LDA+U into a more readable dict

    ldau_info has keys for each species with LDA+U ({species_name}/{atom_number})
    and this in turn contains a dict with the LDA+U definition for the given orbital (spdf)

    :param out_dict: dict with the already parsed information
    """
    parsed_ldau = out_dict['ldau_info'].pop('parsed_ldau')
    ldau_species = out_dict['ldau_info'].pop('ldau_species')

    if isinstance(ldau_species['name'], str):
        ldau_species = {key: [val] for key, val in ldau_species.items()}

    if isinstance(parsed_ldau['l'], int):
        parsed_ldau = {key: [val] for key, val in parsed_ldau.items()}

    ldau_definitions = zip(ldau_species['name'], ldau_species['atomic_number'], parsed_ldau['l'])
    for index, ldau_def in enumerate(ldau_definitions):

        species_name, atom_number, orbital = ldau_def

        species_key = f'{species_name}/{atom_number}'
        orbital_key = 'spdf'[orbital]

        ldau_dict = out_dict['ldau_info'].setdefault(species_key, {})
        ldau_dict[orbital_key] = {
            'u': parsed_ldau['u'][index],
            'j': parsed_ldau['j'][index],
            'unit': 'eV',
            'double_counting': 'AMF' if parsed_ldau['l_amf'][index] else 'FLL'
        }

    return out_dict


@conversion_function
def convert_ldahia_definitions(out_dict: dict[str, Any], logger: Logger) -> dict[str, Any]:
    """
    Convert the parsed information from LDA+U into a more readable dict

    ldau_info has keys for each species with LDA+U ({species_name}/{atom_number})
    and this in turn contains a dict with the LDA+U definition for the given orbital (spdf)

    :param out_dict: dict with the already parsed information
    """
    parsed_ldahia = out_dict['ldahia_info'].pop('parsed_ldahia')
    ldahia_species = out_dict['ldahia_info'].pop('ldahia_species')

    if isinstance(ldahia_species['name'], str):
        ldahia_species = {key: [val] for key, val in ldahia_species.items()}

    if isinstance(parsed_ldahia['l'], int):
        parsed_ldahia = {key: [val] for key, val in parsed_ldahia.items()}

    ldau_definitions = zip(ldahia_species['name'], ldahia_species['atomic_number'], parsed_ldahia['l'])
    for index, ldahia_def in enumerate(ldau_definitions):

        species_name, atom_number, orbital = ldahia_def

        species_key = f'{species_name}/{atom_number}'
        orbital_key = 'spdf'[orbital]

        ldahia_dict = out_dict['ldahia_info'].setdefault(species_key, {})

        ldahia_dict[orbital_key] = {
            'u': parsed_ldahia['u'][index],
            'j': parsed_ldahia['j'][index],
            'unit': 'eV',
            'double_counting': 'AMF' if parsed_ldahia['l_amf'][index] else 'FLL',
            'initial_occupation': parsed_ldahia['init_occ'][index]
        }

    return out_dict


@conversion_function
def convert_relax_info(out_dict: dict[str, Any], logger: Logger) -> dict[str, Any]:
    """
    Convert the general relaxation information

    :param out_dict: dict with the already parsed information
    """

    atoms, cell, pbc = out_dict.pop('parsed_relax_info')
    film = not all(pbc)

    positions = [convert_to_pystd(site.position) for site in atoms]
    if film:
        positions = [abs_to_rel_f(position, cell, pbc) for position in positions]
    else:
        positions = [abs_to_rel(position, cell) for position in positions]

    out_dict['relax_brav_vectors'] = cell.tolist()
    out_dict['relax_atom_positions'] = [[round(x, 16) for x in pos] for pos in positions]
    out_dict['relax_atomtype_info'] = [(site.kind, site.symbol) for site in atoms]

    return out_dict


@conversion_function
def convert_forces(out_dict: dict[str, Any], logger: Logger) -> dict[str, Any]:
    """
    Convert the parsed forces from a iteration

    :param out_dict: dict with the already parsed information
    """
    parsed_forces = out_dict.pop('parsed_forces')

    if 'force_largest_component' not in out_dict:
        out_dict['force_largest_component'] = []
        out_dict['force_atoms'] = []
        out_dict['abspos_atoms'] = []

    if isinstance(parsed_forces['atom_type'], int):
        parsed_forces = {key: [val] for key, val in parsed_forces.items()}

    largest_force = 0.0
    forces = []
    abspos = []
    for index, atomType in enumerate(parsed_forces['atom_type']):

        force_x = parsed_forces['f_x'][index]
        force_y = parsed_forces['f_y'][index]
        force_z = parsed_forces['f_z'][index]

        x = parsed_forces['x'][index]
        y = parsed_forces['y'][index]
        z = parsed_forces['z'][index]

        forces.append((atomType, [force_x, force_y, force_z]))
        abspos.append((atomType, [x, y, z]))

        if abs(force_x) > largest_force:
            largest_force = abs(force_x)
        if abs(force_y) > largest_force:
            largest_force = abs(force_y)
        if abs(force_z) > largest_force:
            largest_force = abs(force_z)

    out_dict['force_largest_component'].append(largest_force)
    out_dict['force_atoms'].append(forces)
    out_dict['abspos_atoms'].append(abspos)

    return out_dict
