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
This module provides functions to extract distinct parts of the fleur xml files
for easy versioning and reuse
"""
from masci_tools.io.parsers.fleur.fleur_schema import schema_dict_version_dispatch


def get_fleur_modes(xmltree, schema_dict):

    from masci_tools.util.schema_dict_util import read_constants
    from masci_tools.util.schema_dict_util import evaluate_attribute, tag_exists
    from masci_tools.util.xml.common_functions import clear_xml

    xmltree = clear_xml(xmltree)
    root = xmltree.getroot()
    constants = read_constants(root, schema_dict)

    fleur_modes = {}
    fleur_modes['jspin'] = evaluate_attribute(root, schema_dict, 'jspins', constants=constants)

    noco = evaluate_attribute(root, schema_dict, 'l_noco', constants=constants, optional=True)
    if noco is None:
        noco = False
    fleur_modes['noco'] = noco

    soc = evaluate_attribute(root, schema_dict, 'l_soc', constants=constants, optional=True)
    if soc is None:
        soc = False
    fleur_modes['soc'] = soc

    forces = evaluate_attribute(root, schema_dict, 'l_f', constants=constants, optional=True)
    if forces is None:
        forces = False
    fleur_modes['forces'] = forces

    gw = evaluate_attribute(root, schema_dict, 'gw', constants=constants, optional=True)
    if gw is None:
        gw = False
    else:
        gw = gw != 0
    fleur_modes['gw'] = gw

    if schema_dict.inp_version > (0, 27):
        fleur_modes['force_theorem'] = tag_exists(root, schema_dict, 'forceTheorem')
    else:
        fleur_modes['force_theorem'] = False

    fleur_modes['film'] = tag_exists(root, schema_dict, 'filmPos')
    fleur_modes['ldau'] = tag_exists(root, schema_dict, 'ldaU', contains='species')
    fleur_modes['dos'] = evaluate_attribute(root, schema_dict, 'dos', constants=constants)
    fleur_modes['band'] = evaluate_attribute(root, schema_dict, 'band', constants=constants)
    fleur_modes['bz_integration'] = evaluate_attribute(root,
                                                       schema_dict,
                                                       'mode',
                                                       constants=constants,
                                                       tag_name='bzIntegration')

    return fleur_modes


def get_cell(xmltree, schema_dict):

    from masci_tools.util.schema_dict_util import read_constants, eval_simple_xpath
    from masci_tools.util.schema_dict_util import evaluate_text, tag_exists
    from masci_tools.util.xml.common_functions import clear_xml
    from masci_tools.util.xml.converters import convert_xml_attribute
    from masci_tools.util.constants import BOHR_A
    import numpy as np

    xmltree = clear_xml(xmltree)

    root = xmltree.getroot()

    constants = read_constants(root, schema_dict)

    cell = None
    lattice_tag = None
    if tag_exists(root, schema_dict, 'bulkLattice'):
        lattice_tag = eval_simple_xpath(root, schema_dict, 'bulkLattice')
        pbc = [True, True, True]
    elif tag_exists(root, schema_dict, 'filmLattice'):
        lattice_tag = eval_simple_xpath(root, schema_dict, 'filmLattice')
        pbc = [True, True, False]

    if lattice_tag is not None:
        row1 = evaluate_text(lattice_tag,
                             schema_dict,
                             'row-1',
                             constants=constants,
                             contains='bravaisMatrix',
                             optional=True)
        row2 = evaluate_text(lattice_tag,
                             schema_dict,
                             'row-2',
                             constants=constants,
                             contains='bravaisMatrix',
                             optional=True)
        row3 = evaluate_text(lattice_tag,
                             schema_dict,
                             'row-3',
                             constants=constants,
                             contains='bravaisMatrix',
                             optional=True)

        if all(x is not None and x != [] for x in [row1, row2, row3]):
            #Explicit Conversion to float for versions Max4 and before
            if schema_dict.inp_version < (0, 33):
                row1, suc = convert_xml_attribute(row1, ['float_expression'], constants=constants)
                row2, suc = convert_xml_attribute(row2, ['float_expression'], constants=constants)
                row3, suc = convert_xml_attribute(row3, ['float_expression'], constants=constants)

            cell = np.array([row1, row2, row3]) * BOHR_A

    if cell is None:
        raise ValueError('Could not extract Bravais matrix out of inp.xml. Is the '
                         'Bravais matrix explicitly given? i.e Latnam definition '
                         'not supported.')

    return cell, pbc


def get_parameter_data(xmltree, schema_dict, inpgen_ready=True, write_ids=True):
    """
    This routine returns an python dictionary produced from the inp.xml
    file, which can be used as a calc_parameters node by inpgen.
    Be aware that inpgen does not take all information that is contained in an inp.xml file

    :param inpxmlfile: and xml etree of a inp.xml file
    :param inpgen_ready: Bool, return a dict which can be inputed into inpgen while setting atoms
    :return new_parameters: A Dict, which will lead to the same inp.xml (in case if other defaults,
                            which can not be controlled by input for inpgen, were changed)

    """
    from masci_tools.util.schema_dict_util import read_constants, eval_simple_xpath
    from masci_tools.util.schema_dict_util import evaluate_attribute, evaluate_text
    from masci_tools.util.xml.common_functions import clear_xml
    from masci_tools.util.xml.converters import convert_fleur_lo, convert_xml_attribute
    from masci_tools.io.common_functions import filter_out_empty_dict_entries

    # TODO: convert econfig
    # TODO: parse kpoints, somehow count is bad (if symmetry changes), mesh is not known, path cannot be specified

    ########
    parameters = {}

    xmltree = clear_xml(xmltree)
    root = xmltree.getroot()
    constants = read_constants(root, schema_dict)

    # Create the cards

    # &input # most things are not needed for AiiDA here. or we ignor them for now.
    # film is set by the plugin depended on the structure
    # symor per default = False? to avoid input which fleur can't take

    # &comp
    comp_dict = {}
    comp_dict['jspins'] = evaluate_attribute(root, schema_dict, 'jspins', constants=constants)
    comp_dict['frcor'] = evaluate_attribute(root, schema_dict, 'frcor', constants=constants, optional=True)
    comp_dict['ctail'] = evaluate_attribute(root, schema_dict, 'ctail', constants=constants)
    comp_dict['kcrel'] = evaluate_attribute(root, schema_dict, 'kcrel', constants=constants, optional=True)
    comp_dict['gmax'] = evaluate_attribute(root, schema_dict, 'gmax', constants=constants)
    comp_dict['gmaxxc'] = evaluate_attribute(root, schema_dict, 'gmaxxc', constants=constants)
    comp_dict['kmax'] = evaluate_attribute(root, schema_dict, 'kmax', constants=constants)

    if schema_dict.inp_version <= (0, 31):
        comp_dict['gmax'], _ = convert_xml_attribute(comp_dict['gmax'], ['float', 'float_expression'],
                                                     constants=constants)
        comp_dict['gmaxxc'], _ = convert_xml_attribute(comp_dict['gmaxxc'], ['float', 'float_expression'],
                                                       constants=constants)
        comp_dict['kmax'], _ = convert_xml_attribute(comp_dict['kmax'], ['float', 'float_expression'],
                                                     constants=constants)

    parameters['comp'] = filter_out_empty_dict_entries(comp_dict)

    # &atoms
    species_list = eval_simple_xpath(root, schema_dict, 'species', list_return=True)
    species_several = {}
    # first we see if there are several species with the same atomic number
    for species in species_list:
        atom_z = evaluate_attribute(species, schema_dict, 'atomicNumber', constants)
        species_several[atom_z] = species_several.get(atom_z, 0) + 1

    species_count = {}
    for indx, species in enumerate(species_list):
        atom_dict = {}
        atoms_name = 'atom{}'.format(indx)
        atom_z = evaluate_attribute(species, schema_dict, 'atomicNumber', constants)
        if not inpgen_ready:
            atom_dict['z'] = atom_z
        species_count[atom_z] = species_count.get(atom_z, 0) + 1
        atom_id = f'{atom_z}.{species_count[atom_z]}'
        if write_ids:
            if species_several[atom_z] > 1:
                atom_dict['id'] = atom_id

        if schema_dict.inp_version <= (0, 31):
            atom_dict['ncst'] = evaluate_attribute(species, schema_dict, 'coreStates', constants)
        atom_dict['rmt'] = evaluate_attribute(species, schema_dict, 'radius', constants=constants)
        atom_dict['dx'] = evaluate_attribute(species, schema_dict, 'logIncrement', constants=constants)
        atom_dict['jri'] = evaluate_attribute(species, schema_dict, 'gridPoints', constants=constants)
        atom_dict['lmax'] = evaluate_attribute(species, schema_dict, 'lmax', constants=constants)
        atom_dict['lnonsph'] = evaluate_attribute(species, schema_dict, 'lnonsphr', constants=constants)
        atom_dict['bmu'] = evaluate_attribute(species, schema_dict, 'magMom', constants, optional=True)

        atom_dict['element'] = evaluate_attribute(species, schema_dict, 'element', constants=constants)

        #atom_econfig = eval_simple_xpath(species, schema_dict, 'electronConfig')
        atom_lo = eval_simple_xpath(species, schema_dict, 'lo', list_return=True)
        #atom_econfig = eval_simple_xpath(species, schema_dict, 'electronConfig')

        if len(atom_lo) != 0:
            atom_dict['lo'] = convert_fleur_lo(atom_lo)

        if schema_dict.inp_version <= (0, 31):
            atom_dict['bmu'], _ = convert_xml_attribute(atom_dict['bmu'], ['float', 'float_expression'],
                                                        constants=constants)
            atom_dict['dx'], _ = convert_xml_attribute(atom_dict['dx'], ['float', 'float_expression'],
                                                       constants=constants)
            atom_dict['rmt'], _ = convert_xml_attribute(atom_dict['rmt'], ['float', 'float_expression'],
                                                        constants=constants)

        parameters[atoms_name] = filter_out_empty_dict_entries(atom_dict)

    # &soc
    soc = evaluate_attribute(root, schema_dict, 'l_soc', constants=constants, optional=True)
    theta = evaluate_attribute(root, schema_dict, 'theta', constants=constants, contains='soc', optional=True)
    phi = evaluate_attribute(root, schema_dict, 'phi', constants=constants, contains='soc', optional=True)
    if soc is not None and soc:
        if schema_dict.inp_version <= (0, 31):
            theta, _ = convert_xml_attribute(theta, ['float', 'float_expression'], constants=constants)
            phi, _ = convert_xml_attribute(phi, ['float', 'float_expression'], constants=constants)

        parameters['soc'] = {'theta': theta, 'phi': phi}

    # &kpt
    #attrib = convert_from_fortran_bool(eval_xpath(root, l_soc_xpath))
    #theta = eval_xpath(root, theta_xpath)
    #phi = eval_xpath(root, phi_xpath)
    # if kpt:
    #    new_parameters['kpt'] = {'theta' : theta, 'phi' : phi}
    #    # ['nkpt', 'kpts', 'div1', 'div2', 'div3',                         'tkb', 'tria'],

    # title
    title = evaluate_text(root, schema_dict, 'comment', constants=constants, optional=True)
    if title:
        parameters['title'] = title.replace('\n', '').strip()

    # &exco
    #TODO, easy
    exco_dict = {}
    exco_dict['xctyp'] = evaluate_attribute(root, schema_dict, 'name', constants, contains='xcFunctional')
    # 'exco' : ['xctyp', 'relxc'],
    parameters['exco'] = filter_out_empty_dict_entries(exco_dict)
    # &film
    # TODO

    # &qss
    # TODO

    # lattice, not supported?

    return parameters


def get_structure_data(xmltree, schema_dict):

    from masci_tools.util.schema_dict_util import read_constants, eval_simple_xpath
    from masci_tools.util.schema_dict_util import evaluate_text, evaluate_attribute
    from masci_tools.util.xml.common_functions import clear_xml
    from masci_tools.util.xml.converters import convert_xml_attribute
    from masci_tools.io.common_functions import rel_to_abs, rel_to_abs_f

    xmltree = clear_xml(xmltree)

    root = xmltree.getroot()

    constants = read_constants(root, schema_dict)

    cell, pbc = get_cell(xmltree, schema_dict)

    species_names = evaluate_attribute(root, schema_dict, 'name', constants=constants, contains='species')
    species_elements = evaluate_attribute(root, schema_dict, 'element', constants=constants, contains='species')

    if not isinstance(species_names, list):
        species_names = [species_names]
    if not isinstance(species_elements, list):
        species_elements = [species_elements]

    if len(species_names) != len(species_elements):
        raise ValueError(
            f'Failed to read in species names and elements. Got {len(species_names)} names and {len(species_elements)} elements'
        )

    species_dict = dict(zip(species_names, species_elements))

    atom_data = []
    atom_groups = eval_simple_xpath(root, schema_dict, 'atomGroup', list_return=True)
    for group in atom_groups:

        group_species = evaluate_attribute(group, schema_dict, 'species', constants=constants)

        atom_positions = []

        absolute_positions = evaluate_text(group,
                                           schema_dict,
                                           'absPos',
                                           constants=constants,
                                           list_return=True,
                                           optional=True)
        relative_positions = evaluate_text(group,
                                           schema_dict,
                                           'relPos',
                                           constants=constants,
                                           list_return=True,
                                           optional=True)
        film_positions = evaluate_text(group,
                                       schema_dict,
                                       'filmPos',
                                       constants=constants,
                                       list_return=True,
                                       optional=True)

        if schema_dict.inp_version < (0, 33):
            for indx, pos in enumerate(absolute_positions):
                absolute_positions[indx], suc = convert_xml_attribute(pos, ['float', 'float_expression'],
                                                                      constants=constants)
            for indx, pos in enumerate(relative_positions):
                relative_positions[indx], suc = convert_xml_attribute(pos, ['float', 'float_expression'],
                                                                      constants=constants)
            for indx, pos in enumerate(film_positions):
                film_positions[indx], suc = convert_xml_attribute(pos, ['float', 'float_expression'],
                                                                  constants=constants)

        atom_positions = absolute_positions

        for rel_pos in relative_positions:
            atom_positions.append(rel_to_abs(rel_pos, cell))

        for film_pos in film_positions:
            atom_positions.append(rel_to_abs_f(film_pos, cell))

        if len(atom_positions) == 0:
            raise ValueError('Failed to read atom positions for group')

        atom_data.extend((pos, species_dict[group_species]) for pos in atom_positions)

    return atom_data, cell, pbc


@schema_dict_version_dispatch(output_schema=False)
def get_kpoints_data(xmltree, schema_dict, name=None):

    from masci_tools.util.schema_dict_util import read_constants, eval_simple_xpath
    from masci_tools.util.schema_dict_util import evaluate_text, evaluate_attribute
    from masci_tools.util.xml.common_functions import clear_xml
    from masci_tools.util.xml.converters import convert_xml_attribute

    xmltree = clear_xml(xmltree)

    root = xmltree.getroot()

    constants = read_constants(root, schema_dict)

    cell, pbc = get_cell(xmltree, schema_dict)

    kpointlists = eval_simple_xpath(root, schema_dict, 'kPointList', list_return=True)

    if len(kpointlists) == 0:
        raise ValueError('No Kpoint lists found in the given inp.xml')

    labels = [kpoint_set.attrib.get('name') for kpoint_set in kpointlists]
    if name is not None and name not in labels:
        raise ValueError(f'Found no Kpoint list with the name: {name}' f'Available list names: {labels}')

    kpoints_data = {}
    weights_data = {}
    for kpointlist in kpointlists:

        label = evaluate_attribute(kpointlist, schema_dict, 'name')

        if name is not None and name != label:
            continue

        kpoints = evaluate_text(kpointlist, schema_dict, 'kPoint', constants=constants, list_return=True)
        weights = evaluate_attribute(kpointlist, schema_dict, 'weight', constants=constants, list_return=True)

        if schema_dict.inp_version == (0, 32):
            for indx, kpoint in enumerate(kpoints):
                kpoints[indx], suc = convert_xml_attribute(kpoint, ['float', 'float_expression'], constants=constants)
            weights, suc = convert_xml_attribute(weights, ['float', 'float_expression'],
                                                 constants=constants,
                                                 list_return=True)

        if not isinstance(kpoints[0], list):
            kpoints = [kpoints]
            weights = [weights]

        kpoints_data[label] = kpoints
        weights_data[label] = weights

    if len(kpoints_data) == 1:
        _, kpoints_data = kpoints_data.popitem()
        _, weights_data = weights_data.popitem()

    return kpoints_data, weights_data, cell, pbc


@get_kpoints_data.register(max_version='0.31')
def get_kpoints_data_max4(xmltree, schema_dict):

    from masci_tools.util.schema_dict_util import read_constants, eval_simple_xpath
    from masci_tools.util.schema_dict_util import evaluate_text, evaluate_attribute
    from masci_tools.util.xml.common_functions import clear_xml
    from masci_tools.util.xml.converters import convert_xml_attribute

    xmltree = clear_xml(xmltree)

    root = xmltree.getroot()

    constants = read_constants(root, schema_dict)

    cell, pbc = get_cell(xmltree, schema_dict)

    kpointlist = eval_simple_xpath(root, schema_dict, 'kPointList', list_return=True, not_contains='altKPoint')

    if len(kpointlist) == 0:
        raise ValueError('No Kpoint lists found in the given inp.xml')

    kpointlist = kpointlist[0]

    kpoints = evaluate_text(kpointlist,
                            schema_dict,
                            'kPoint',
                            constants=constants,
                            not_contains='altKPoint',
                            list_return=True)
    weights = evaluate_attribute(kpointlist,
                                 schema_dict,
                                 'weight',
                                 constants=constants,
                                 not_contains='altKPoint',
                                 list_return=True)

    for indx, kpoint in enumerate(kpoints):
        kpoints[indx], suc = convert_xml_attribute(kpoint, ['float', 'float_expression'], constants=constants)
    weights, suc = convert_xml_attribute(weights, ['float', 'float_expression'], constants=constants, list_return=True)

    return kpoints, weights, cell, pbc
