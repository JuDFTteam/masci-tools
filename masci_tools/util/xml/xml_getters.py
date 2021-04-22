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
from lxml import etree


def get_fleur_modes(xmltree, schema_dict, logger=None):
    """
    Determine the calculation modes of fleur for the given xml file. Calculation modes
    are things that change the produced files or output in the out.xml files

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param logger: logger object for logging warnings, errors

    :returns: dictionary with all the extracted calculation modes

    The following modes are inspected:

        - `jspin`: How many spins are considered in the calculation
        - `noco`: Is the calculation non-collinear?
        - `soc`: Is spin-orbit coupling included?
        - `relax`: Is the calculation a structure relaxation?
        - `gw`: Special mode for GW/Spex calculations
        - `force_theorem`: Is a Force theorem calculation performed?
        - `film`: Is the structure a film system
        - `ldau`: Is LDA+U included?
        - `dos`: Is it a density of states calculation?
        - `band`: Is it a bandstructure calculation?
        - `bz_integration`: How is the integration over the Brillouin-Zone performed?

    """
    from masci_tools.util.schema_dict_util import read_constants
    from masci_tools.util.schema_dict_util import evaluate_attribute, tag_exists
    from masci_tools.util.xml.common_functions import clear_xml

    if isinstance(xmltree, etree._ElementTree):
        xmltree = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree
    constants = read_constants(root, schema_dict)

    fleur_modes = {}
    fleur_modes['jspin'] = evaluate_attribute(root, schema_dict, 'jspins', logger=logger, constants=constants)

    noco = evaluate_attribute(root, schema_dict, 'l_noco', constants=constants, logger=logger, optional=True)
    if noco is None:
        noco = False
    fleur_modes['noco'] = noco

    soc = evaluate_attribute(root, schema_dict, 'l_soc', constants=constants, logger=logger, optional=True)
    if soc is None:
        soc = False
    fleur_modes['soc'] = soc

    relax = evaluate_attribute(root, schema_dict, 'l_f', constants=constants, logger=logger, optional=True)
    if relax is None:
        relax = False
    fleur_modes['relax'] = relax

    gw = evaluate_attribute(root, schema_dict, 'gw', constants=constants, logger=logger, optional=True)
    if gw is None:
        gw = False
    else:
        gw = gw != 0
    fleur_modes['gw'] = gw

    if schema_dict.inp_version > (0, 27):
        fleur_modes['force_theorem'] = tag_exists(root, schema_dict, 'forceTheorem', logger=logger)
    else:
        fleur_modes['force_theorem'] = False

    fleur_modes['film'] = tag_exists(root, schema_dict, 'filmPos', logger=logger)
    fleur_modes['ldau'] = tag_exists(root, schema_dict, 'ldaU', contains='species', logger=logger)
    fleur_modes['dos'] = evaluate_attribute(root, schema_dict, 'dos', constants=constants, logger=logger)
    fleur_modes['band'] = evaluate_attribute(root, schema_dict, 'band', constants=constants, logger=logger)
    fleur_modes['bz_integration'] = evaluate_attribute(root,
                                                       schema_dict,
                                                       'mode',
                                                       constants=constants,
                                                       tag_name='bzIntegration',
                                                       logger=logger)

    return fleur_modes


@schema_dict_version_dispatch(output_schema=False)
def get_nkpts(xmltree, schema_dict, logger=None):
    """
    Get the number of kpoints that will be used in the calculation specified in the given
    fleur XMl file.

    .. warning::
        For file versions before Max5 only kPointList or kPointCount tags will work. However,
        for kPointCount there is no real guarantee that for every occasion it will correspond
        to the number of kpoints. So a warning is written out

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param logger: logger object for logging warnings, errors

    :returns: int with the number of kpoints
    """
    from masci_tools.util.schema_dict_util import eval_simple_xpath
    from masci_tools.util.schema_dict_util import evaluate_attribute
    from masci_tools.util.xml.common_functions import clear_xml

    if isinstance(xmltree, etree._ElementTree):
        xmltree = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree

    #Get the name of the current selected kPointSet
    list_name = evaluate_attribute(root, schema_dict, 'listName', logger=logger)

    kpointlists = eval_simple_xpath(root, schema_dict, 'kPointList', list_return=True, logger=logger)

    if len(kpointlists) == 0:
        raise ValueError('No Kpoint lists found in the given inp.xml')

    labels = [kpoint_set.attrib.get('name') for kpoint_set in kpointlists]
    if list_name not in labels:
        raise ValueError(f'Selected Kpoint list with the name: {list_name} does not exist'
                         f'Available list names: {labels}')

    kpoint_index = labels.index(list_name)

    kpoint_set = kpointlists[kpoint_index]

    nkpts = evaluate_attribute(kpoint_set, schema_dict, 'count', logger=logger)

    return nkpts


@get_nkpts.register(max_version='0.31')
def get_nkpts_max4(xmltree, schema_dict, logger=None):
    """
    Get the number of kpoints that will be used in the calculation specified in the given
    fleur XMl file. Version specific for Max4 versions or older

    .. warning::
        For file versions before Max5 only kPointList or kPointCount tags will work. However,
        for kPointCount there is no real guarantee that for every occasion it will correspond
        to the number of kpoints. So a warning is written out

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param logger: logger object for logging warnings, errors

    :returns: int with the number of kpoints
    """
    from masci_tools.util.schema_dict_util import evaluate_attribute, eval_simple_xpath
    from masci_tools.util.xml.common_functions import clear_xml
    import warnings

    if isinstance(xmltree, etree._ElementTree):
        xmltree = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree

    modes = get_fleur_modes(root, schema_dict, logger=logger)

    alt_kpt_set = None
    if modes['band'] or modes['gw']:
        expected_mode = 'bands' if modes['band'] else 'gw'
        alt_kpts = eval_simple_xpath(root, schema_dict, 'altKPointSet', list_return=True, logger=logger)
        for kpt_set in alt_kpts:
            if evaluate_attribute(kpt_set, schema_dict, 'purpose', logger=logger) == expected_mode:
                alt_kpt_set = kpt_set
                break

    kpt_tag = None
    if alt_kpt_set is not None:
        kpt_tag = eval_simple_xpath(alt_kpt_set, schema_dict, 'kPointList', list_return=True, logger=logger)
        if len(kpt_tag) == 0:
            kpt_tag = eval_simple_xpath(alt_kpt_set, schema_dict, 'kPointCount', list_return=True, logger=logger)
            if len(kpt_tag) == 0:
                kpt_tag = None
            else:
                warnings.warn('kPointCount is not guaranteed to result in the given number of kpoints')

    if kpt_tag is None:
        kpt_tag = eval_simple_xpath(root,
                                    schema_dict,
                                    'kPointList',
                                    not_contains='altKPointSet',
                                    list_return=True,
                                    logger=logger)
        if len(kpt_tag) == 0:
            kpt_tag = eval_simple_xpath(root,
                                        schema_dict,
                                        'kPointCount',
                                        not_contains='altKPointSet',
                                        list_return=True,
                                        logger=logger)
            if len(kpt_tag) == 0:
                raise ValueError('No kPointList or kPointCount found')
            else:
                warnings.warn('kPointCount is not guaranteed to result in the given number of kpoints')

    kpt_tag = kpt_tag[0]

    nkpts = evaluate_attribute(kpt_tag, schema_dict, 'count', logger=logger)

    return nkpts


def get_cell(xmltree, schema_dict, logger=None):
    """
    Get the Bravais matrix from the given fleur xml file. In addition a list
    determining in, which directions there are periodic boundary conditions
    in the system.

    .. warning::
        Only the explicit definition of the Bravais matrix is supported.
        Old inputs containing the `latnam` definitions are not supported

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param logger: logger object for logging warnings, errors

    :returns: numpy array of the bravais matrix and list of boolean values for
              periodic boundary conditions
    """
    from masci_tools.util.schema_dict_util import read_constants, eval_simple_xpath
    from masci_tools.util.schema_dict_util import evaluate_text, tag_exists
    from masci_tools.util.xml.common_functions import clear_xml
    from masci_tools.util.xml.converters import convert_xml_attribute
    from masci_tools.util.constants import BOHR_A
    import numpy as np

    if isinstance(xmltree, etree._ElementTree):
        xmltree = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree
    constants = read_constants(root, schema_dict, logger=logger)

    cell = None
    lattice_tag = None
    if tag_exists(root, schema_dict, 'bulkLattice', logger=logger):
        lattice_tag = eval_simple_xpath(root, schema_dict, 'bulkLattice', logger=logger)
        pbc = [True, True, True]
    elif tag_exists(root, schema_dict, 'filmLattice', logger=logger):
        lattice_tag = eval_simple_xpath(root, schema_dict, 'filmLattice', logger=logger)
        pbc = [True, True, False]

    if lattice_tag is not None:
        row1 = evaluate_text(lattice_tag,
                             schema_dict,
                             'row-1',
                             constants=constants,
                             contains='bravaisMatrix',
                             logger=logger,
                             optional=True)
        row2 = evaluate_text(lattice_tag,
                             schema_dict,
                             'row-2',
                             constants=constants,
                             contains='bravaisMatrix',
                             logger=logger,
                             optional=True)
        row3 = evaluate_text(lattice_tag,
                             schema_dict,
                             'row-3',
                             constants=constants,
                             contains='bravaisMatrix',
                             logger=logger,
                             optional=True)

        if all(x is not None and x != [] for x in [row1, row2, row3]):
            #Explicit Conversion to float for versions Max4 and before
            if schema_dict.inp_version < (0, 33):
                row1, suc = convert_xml_attribute(row1, ['float_expression'], constants=constants, logger=logger)
                row2, suc = convert_xml_attribute(row2, ['float_expression'], constants=constants, logger=logger)
                row3, suc = convert_xml_attribute(row3, ['float_expression'], constants=constants, logger=logger)

            cell = np.array([row1, row2, row3]) * BOHR_A

    if cell is None:
        raise ValueError('Could not extract Bravais matrix out of inp.xml. Is the '
                         'Bravais matrix explicitly given? i.e Latnam definition '
                         'not supported.')

    return cell, pbc


def get_parameter_data(xmltree, schema_dict, inpgen_ready=True, write_ids=True, logger=None):
    """
    This routine returns an python dictionary produced from the inp.xml
    file, which contains all the parameters needed to setup a new inp.xml from a inpgen
    input file to produce the same input (for parameters that the inpgen can control)

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param inpgen_ready: Bool, return a dict which can be inputed into inpgen while setting atoms
    :param write_ids: Bool, if True the atom ids are added to the atom namelists
    :param logger: logger object for logging warnings, errors

    :returns: dict, which will lead to the same inp.xml (in case if other defaults,
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
    if isinstance(xmltree, etree._ElementTree):
        xmltree = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree
    constants = read_constants(root, schema_dict, logger=logger)

    # Create the cards

    # &input # most things are not needed for AiiDA here. or we ignor them for now.
    # film is set by the plugin depended on the structure
    # symor per default = False? to avoid input which fleur can't take

    # &comp
    comp_dict = {}
    comp_dict['jspins'] = evaluate_attribute(root, schema_dict, 'jspins', constants=constants, logger=logger)
    comp_dict['frcor'] = evaluate_attribute(root,
                                            schema_dict,
                                            'frcor',
                                            constants=constants,
                                            logger=logger,
                                            optional=True)
    comp_dict['ctail'] = evaluate_attribute(root, schema_dict, 'ctail', constants=constants, logger=logger)
    comp_dict['kcrel'] = evaluate_attribute(root,
                                            schema_dict,
                                            'kcrel',
                                            constants=constants,
                                            logger=logger,
                                            optional=True)
    comp_dict['gmax'] = evaluate_attribute(root, schema_dict, 'gmax', constants=constants, logger=logger)
    comp_dict['gmaxxc'] = evaluate_attribute(root, schema_dict, 'gmaxxc', constants=constants, logger=logger)
    comp_dict['kmax'] = evaluate_attribute(root, schema_dict, 'kmax', constants=constants, logger=logger)

    if schema_dict.inp_version <= (0, 31):
        comp_dict['gmax'], _ = convert_xml_attribute(comp_dict['gmax'], ['float', 'float_expression'],
                                                     constants=constants,
                                                     logger=logger)
        comp_dict['gmaxxc'], _ = convert_xml_attribute(comp_dict['gmaxxc'], ['float', 'float_expression'],
                                                       constants=constants,
                                                       logger=logger)
        comp_dict['kmax'], _ = convert_xml_attribute(comp_dict['kmax'], ['float', 'float_expression'],
                                                     constants=constants,
                                                     logger=logger)

    parameters['comp'] = filter_out_empty_dict_entries(comp_dict)

    # &atoms
    species_list = eval_simple_xpath(root, schema_dict, 'species', list_return=True, logger=logger)
    species_several = {}
    # first we see if there are several species with the same atomic number
    for species in species_list:
        atom_z = evaluate_attribute(species, schema_dict, 'atomicNumber', constants, logger=logger)
        species_several[atom_z] = species_several.get(atom_z, 0) + 1

    species_count = {}
    for indx, species in enumerate(species_list):
        atom_dict = {}
        atoms_name = 'atom{}'.format(indx)
        atom_z = evaluate_attribute(species, schema_dict, 'atomicNumber', constants=constants, logger=logger)
        if not inpgen_ready:
            atom_dict['z'] = atom_z
        species_count[atom_z] = species_count.get(atom_z, 0) + 1
        atom_id = f'{atom_z}.{species_count[atom_z]}'
        if write_ids:
            if species_several[atom_z] > 1:
                atom_dict['id'] = atom_id

        if schema_dict.inp_version <= (0, 31):
            atom_dict['ncst'] = evaluate_attribute(species, schema_dict, 'coreStates', constants, logger=logger)
        atom_dict['rmt'] = evaluate_attribute(species, schema_dict, 'radius', constants=constants, logger=logger)
        atom_dict['dx'] = evaluate_attribute(species, schema_dict, 'logIncrement', constants=constants, logger=logger)
        atom_dict['jri'] = evaluate_attribute(species, schema_dict, 'gridPoints', constants=constants, logger=logger)
        atom_dict['lmax'] = evaluate_attribute(species, schema_dict, 'lmax', constants=constants, logger=logger)
        atom_dict['lnonsph'] = evaluate_attribute(species, schema_dict, 'lnonsphr', constants=constants, logger=logger)
        atom_dict['bmu'] = evaluate_attribute(species, schema_dict, 'magMom', constants, logger=logger, optional=True)

        atom_dict['element'] = evaluate_attribute(species, schema_dict, 'element', constants=constants, logger=logger)

        #atom_econfig = eval_simple_xpath(species, schema_dict, 'electronConfig')
        atom_lo = eval_simple_xpath(species, schema_dict, 'lo', list_return=True, logger=logger)
        #atom_econfig = eval_simple_xpath(species, schema_dict, 'electronConfig')

        if len(atom_lo) != 0:
            atom_dict['lo'] = convert_fleur_lo(atom_lo)

        if schema_dict.inp_version <= (0, 31):
            atom_dict['bmu'], _ = convert_xml_attribute(atom_dict['bmu'], ['float', 'float_expression'],
                                                        constants=constants,
                                                        logger=logger)
            atom_dict['dx'], _ = convert_xml_attribute(atom_dict['dx'], ['float', 'float_expression'],
                                                       constants=constants,
                                                       logger=logger)
            atom_dict['rmt'], _ = convert_xml_attribute(atom_dict['rmt'], ['float', 'float_expression'],
                                                        constants=constants,
                                                        logger=logger)

        parameters[atoms_name] = filter_out_empty_dict_entries(atom_dict)

    # &soc
    soc = evaluate_attribute(root, schema_dict, 'l_soc', constants=constants, logger=logger, optional=True)
    theta = evaluate_attribute(root,
                               schema_dict,
                               'theta',
                               constants=constants,
                               contains='soc',
                               logger=logger,
                               optional=True)
    phi = evaluate_attribute(root,
                             schema_dict,
                             'phi',
                             constants=constants,
                             contains='soc',
                             logger=logger,
                             optional=True)
    if soc is not None and soc:
        if schema_dict.inp_version <= (0, 31):
            theta, _ = convert_xml_attribute(theta, ['float', 'float_expression'], constants=constants, logger=logger)
            phi, _ = convert_xml_attribute(phi, ['float', 'float_expression'], constants=constants, logger=logger)

        parameters['soc'] = {'theta': theta, 'phi': phi}

    # &kpt
    #attrib = convert_from_fortran_bool(eval_xpath(root, l_soc_xpath))
    #theta = eval_xpath(root, theta_xpath)
    #phi = eval_xpath(root, phi_xpath)
    # if kpt:
    #    new_parameters['kpt'] = {'theta' : theta, 'phi' : phi}
    #    # ['nkpt', 'kpts', 'div1', 'div2', 'div3',                         'tkb', 'tria'],

    # title
    title = evaluate_text(root, schema_dict, 'comment', constants=constants, logger=logger, optional=True)
    if title:
        parameters['title'] = title.replace('\n', '').strip()

    # &exco
    #TODO, easy
    exco_dict = {}
    exco_dict['xctyp'] = evaluate_attribute(root,
                                            schema_dict,
                                            'name',
                                            constants,
                                            contains='xcFunctional',
                                            logger=logger)
    # 'exco' : ['xctyp', 'relxc'],
    parameters['exco'] = filter_out_empty_dict_entries(exco_dict)
    # &film
    # TODO

    # &qss
    # TODO

    # lattice, not supported?

    return parameters


def get_structure_data(xmltree, schema_dict, logger=None):
    """
    Get the structure defined in the given fleur xml file.

    .. warning::
        Only the explicit definition of the Bravais matrix is supported.
        Old inputs containing the `latnam` definitions are not supported

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param logger: logger object for logging warnings, errors

    :returns: tuple containing the structure information

    The tuple contains the following entries:

        1. :atom_data: list of tuples containing the absolute positions and symbols of the atoms
        2. :cell: numpy array, bravais matrix of the given system
        3. :pbc: list of booleans, determines in which directions periodic boundary conditions are applicable

    """
    from masci_tools.util.schema_dict_util import read_constants, eval_simple_xpath
    from masci_tools.util.schema_dict_util import evaluate_text, evaluate_attribute
    from masci_tools.util.xml.common_functions import clear_xml
    from masci_tools.util.xml.converters import convert_xml_attribute
    from masci_tools.io.common_functions import rel_to_abs, rel_to_abs_f

    if isinstance(xmltree, etree._ElementTree):
        xmltree = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree
    constants = read_constants(root, schema_dict, logger=logger)
    cell, pbc = get_cell(root, schema_dict, logger=logger)

    species_names = evaluate_attribute(root,
                                       schema_dict,
                                       'name',
                                       constants=constants,
                                       contains='species',
                                       logger=logger)
    species_elements = evaluate_attribute(root,
                                          schema_dict,
                                          'element',
                                          constants=constants,
                                          contains='species',
                                          logger=logger)

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
    atom_groups = eval_simple_xpath(root, schema_dict, 'atomGroup', list_return=True, logger=logger)
    for group in atom_groups:

        group_species = evaluate_attribute(group, schema_dict, 'species', constants=constants, logger=logger)

        atom_positions = []

        absolute_positions = evaluate_text(group,
                                           schema_dict,
                                           'absPos',
                                           constants=constants,
                                           list_return=True,
                                           logger=logger,
                                           optional=True)
        relative_positions = evaluate_text(group,
                                           schema_dict,
                                           'relPos',
                                           constants=constants,
                                           list_return=True,
                                           logger=logger,
                                           optional=True)
        film_positions = evaluate_text(group,
                                       schema_dict,
                                       'filmPos',
                                       constants=constants,
                                       list_return=True,
                                       logger=logger,
                                       optional=True)

        if schema_dict.inp_version < (0, 33):
            for indx, pos in enumerate(absolute_positions):
                absolute_positions[indx], suc = convert_xml_attribute(pos, ['float', 'float_expression'],
                                                                      constants=constants,
                                                                      logger=logger)
            for indx, pos in enumerate(relative_positions):
                relative_positions[indx], suc = convert_xml_attribute(pos, ['float', 'float_expression'],
                                                                      constants=constants,
                                                                      logger=logger)
            for indx, pos in enumerate(film_positions):
                film_positions[indx], suc = convert_xml_attribute(pos, ['float', 'float_expression'],
                                                                  constants=constants,
                                                                  logger=logger)

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
def get_kpoints_data(xmltree, schema_dict, name=None, logger=None):
    """
    Get the kpoint sets defined in the given fleur xml file.

    .. warning::
        For file versions before Max5 the name argument is not valid

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param name: str, optional, if given only the kpoint set with the given name
                 is returned
    :param logger: logger object for logging warnings, errors

    :returns: tuple containing the kpoint information

    The tuple contains the following entries:

        1. :kpoints: dict or list (list if there is only one kpoint set),
                     containing the coordinates of the kpoints
        2. :weights: dict or list (list if there is only one kpoint set),
                     containing the weights of the kpoints
        3. :cell: numpy array, bravais matrix of the given system
        4. :pbc: list of booleans, determines in which directions periodic boundary conditions are applicable

    """
    from masci_tools.util.schema_dict_util import read_constants, eval_simple_xpath
    from masci_tools.util.schema_dict_util import evaluate_text, evaluate_attribute
    from masci_tools.util.xml.common_functions import clear_xml
    from masci_tools.util.xml.converters import convert_xml_attribute

    if isinstance(xmltree, etree._ElementTree):
        xmltree = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree

    constants = read_constants(root, schema_dict, logger=logger)

    cell, pbc = get_cell(root, schema_dict, logger=logger)

    kpointlists = eval_simple_xpath(root, schema_dict, 'kPointList', list_return=True, logger=logger)

    if len(kpointlists) == 0:
        raise ValueError('No Kpoint lists found in the given inp.xml')

    labels = [kpoint_set.attrib.get('name') for kpoint_set in kpointlists]
    if name is not None and name not in labels:
        raise ValueError(f'Found no Kpoint list with the name: {name}' f'Available list names: {labels}')

    kpoints_data = {}
    weights_data = {}
    for kpointlist in kpointlists:

        label = evaluate_attribute(kpointlist, schema_dict, 'name', logger=logger)

        if name is not None and name != label:
            continue

        kpoints = evaluate_text(kpointlist, schema_dict, 'kPoint', constants=constants, list_return=True, logger=logger)
        weights = evaluate_attribute(kpointlist,
                                     schema_dict,
                                     'weight',
                                     constants=constants,
                                     list_return=True,
                                     logger=logger)

        if schema_dict.inp_version == (0, 32):
            for indx, kpoint in enumerate(kpoints):
                kpoints[indx], suc = convert_xml_attribute(kpoint, ['float', 'float_expression'],
                                                           constants=constants,
                                                           logger=logger)
            weights, suc = convert_xml_attribute(weights, ['float', 'float_expression'],
                                                 constants=constants,
                                                 list_return=True,
                                                 logger=logger)

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
def get_kpoints_data_max4(xmltree, schema_dict, logger=None):
    """
    Get the kpoint sets defined in the given fleur xml file.

    .. note::
        This function is specific to file version before and including the
        Max4 release of fleur

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param logger: logger object for logging warnings, errors

    :returns: tuple containing the kpoint information

    The tuple contains the following entries:

        1. :kpoints: list containing the coordinates of the kpoints
        2. :weights: list containing the weights of the kpoints
        3. :cell: numpy array, bravais matrix of the given system
        4. :pbc: list of booleans, determines in which directions periodic boundary conditions are applicable

    """
    from masci_tools.util.schema_dict_util import read_constants, eval_simple_xpath
    from masci_tools.util.schema_dict_util import evaluate_text, evaluate_attribute
    from masci_tools.util.xml.common_functions import clear_xml
    from masci_tools.util.xml.converters import convert_xml_attribute

    if isinstance(xmltree, etree._ElementTree):
        xmltree = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree

    constants = read_constants(root, schema_dict, logger=logger)

    cell, pbc = get_cell(root, schema_dict, logger=logger)

    kpointlist = eval_simple_xpath(root,
                                   schema_dict,
                                   'kPointList',
                                   list_return=True,
                                   not_contains='altKPoint',
                                   logger=logger)

    if len(kpointlist) == 0:
        raise ValueError('No Kpoint lists found in the given inp.xml')

    kpointlist = kpointlist[0]

    kpoints = evaluate_text(kpointlist,
                            schema_dict,
                            'kPoint',
                            constants=constants,
                            not_contains='altKPoint',
                            list_return=True,
                            logger=logger)
    weights = evaluate_attribute(kpointlist,
                                 schema_dict,
                                 'weight',
                                 constants=constants,
                                 not_contains='altKPoint',
                                 list_return=True,
                                 logger=logger)

    for indx, kpoint in enumerate(kpoints):
        kpoints[indx], suc = convert_xml_attribute(kpoint, ['float', 'float_expression'],
                                                   constants=constants,
                                                   logger=logger)
    weights, suc = convert_xml_attribute(weights, ['float', 'float_expression'],
                                         constants=constants,
                                         list_return=True,
                                         logger=logger)

    return kpoints, weights, cell, pbc


@schema_dict_version_dispatch(output_schema=False)
def get_relaxation_information(xmltree, schema_dict, logger=None):
    """
    Get the relaxation information from the given fleur XML file. This includes the current
    displacements, energy and posforce evolution

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param logger: logger object for logging warnings, errors

    :returns: dict with the relaxation information

    :raises ValueError: If no relaxation section is included in the xml tree
    """
    from masci_tools.util.schema_dict_util import tag_exists, read_constants, evaluate_text, eval_simple_xpath
    from masci_tools.util.schema_dict_util import evaluate_attribute
    from masci_tools.util.xml.converters import convert_xml_attribute, convert_xml_text
    from masci_tools.util.xml.common_functions import clear_xml

    if isinstance(xmltree, etree._ElementTree):
        xmltree = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree
    constants = read_constants(root, schema_dict, logger=logger)

    if not tag_exists(root, schema_dict, 'relaxation', logger=logger):
        raise ValueError('No relaxation information included in the given XML file')

    relax_tag = eval_simple_xpath(root, schema_dict, 'relaxation', logger=logger)

    out_dict = {}
    out_dict['displacements'] = evaluate_text(relax_tag,
                                              schema_dict,
                                              'displace',
                                              list_return=True,
                                              constants=constants,
                                              logger=logger)

    energies = evaluate_attribute(relax_tag,
                                  schema_dict,
                                  'energy',
                                  list_return=True,
                                  constants=constants,
                                  logger=logger)
    out_dict['energies'], _ = convert_xml_attribute(energies, ['float', 'float_expression'],
                                                    list_return=True,
                                                    logger=logger)

    out_dict['posforces'] = []
    relax_iters = eval_simple_xpath(relax_tag, schema_dict, 'step', list_return=True, logger=logger)
    for step in relax_iters:
        posforces = evaluate_text(step, schema_dict, 'posforce', list_return=True, constants=constants, logger=logger)
        posforces, _ = convert_xml_text(posforces, [{
            'length': 6,
            'type': ['float', 'float_expression']
        }],
                                        list_return=True,
                                        logger=logger)
        out_dict['posforces'].append(posforces)

    return out_dict


@get_relaxation_information.register(max_version='0.28')
def get_relaxation_information_pre029(xmltree, schema_dict, logger=None):
    """
    Get the relaxation information from the given fleur XML file. This includes the current
    displacements, energy and posforce evolution

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param logger: logger object for logging warnings, errors

    :returns: dict with the relaxation information

    :raises ValueError: If no relaxation section is included in the xml tree
    """
    raise NotImplementedError(
        f"'get_relaxation_information' is not implemented for inputs of version '{schema_dict['inp_version']}'")
