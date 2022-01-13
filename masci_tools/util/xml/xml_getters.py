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
from __future__ import annotations

from masci_tools.io.parsers.fleur_schema import schema_dict_version_dispatch
from masci_tools.io.common_functions import AtomSiteProperties
from masci_tools.util.typing import XMLLike
from masci_tools.io.parsers import fleur_schema

from lxml import etree
import warnings
import numpy as np
from logging import Logger
from typing import Any


def get_fleur_modes(xmltree: XMLLike,
                    schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
                    logger: Logger | None = None) -> dict[str, Any]:
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
        xmltree, _ = clear_xml(xmltree)
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

    gw = None
    if tag_exists(root, schema_dict, 'expertModes', logger=logger):
        gw = evaluate_attribute(root, schema_dict, 'gw', constants=constants, logger=logger, optional=True)
        if gw is None and schema_dict.inp_version >= (0, 34):
            gw = evaluate_attribute(root, schema_dict, 'spex', constants=constants, logger=logger, optional=True)

    if gw is None:
        gw = False
    else:
        gw = gw != 0
    fleur_modes['gw'] = gw

    if schema_dict.inp_version > (0, 27):
        fleur_modes['force_theorem'] = tag_exists(root, schema_dict, 'forceTheorem', logger=logger)
    else:
        fleur_modes['force_theorem'] = False

    if schema_dict.inp_version >= (0, 33):
        if tag_exists(root, schema_dict, 'cFCoeffs', logger=logger):
            cf_coeff = any(
                evaluate_attribute(root,
                                   schema_dict,
                                   'potential',
                                   contains='cFCoeffs',
                                   logger=logger,
                                   list_return=True,
                                   optional=True))
            cf_coeff = cf_coeff or any(
                evaluate_attribute(root,
                                   schema_dict,
                                   'chargeDensity',
                                   contains='cFCoeffs',
                                   logger=logger,
                                   list_return=True,
                                   optional=True))
        else:
            cf_coeff = False
        fleur_modes['cf_coeff'] = cf_coeff
    else:
        fleur_modes['cf_coeff'] = False

    plot = None
    if tag_exists(root, schema_dict, 'plotting', logger=logger):
        plot = evaluate_attribute(root, schema_dict, 'iplot', logger=logger, optional=True)

    if schema_dict.inp_version >= (0, 29) and plot is not None:
        plot = isinstance(plot, int) and plot != 0

    if plot is None:
        plot = False
    fleur_modes['plot'] = plot

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

    greensf = False
    if schema_dict.inp_version >= (0, 32):
        #We make the assumption that the existence of a greensfCalculation
        #tag implies the existence of a greens function calculation
        greensf = tag_exists(root, schema_dict, 'greensfCalculation', contains='species', logger=logger)
        if schema_dict.inp_version >= (0, 35):
            greensf = greensf or tag_exists(root, schema_dict, 'torqueCalculation', contains='species', logger=logger)
        else:
            greensf = greensf or tag_exists(root, schema_dict, 'torgueCalculation', contains='species', logger=logger)
    fleur_modes['greensf'] = greensf

    ldahia = False
    if schema_dict.inp_version >= (0, 32):
        ldahia = tag_exists(root, schema_dict, 'ldaHIA', contains='species', logger=logger)
    fleur_modes['ldahia'] = ldahia

    return fleur_modes


@schema_dict_version_dispatch(output_schema=False)
def get_nkpts(xmltree: XMLLike,
              schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
              logger: Logger | None = None) -> int:
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
        xmltree, _ = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree

    #Get the name of the current selected kPointSet
    list_name = evaluate_attribute(root, schema_dict, 'listName', logger=logger)

    kpointlists = eval_simple_xpath(root,
                                    schema_dict,
                                    'kPointList',
                                    contains='kPointLists',
                                    list_return=True,
                                    logger=logger)

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
def get_nkpts_max4(xmltree: XMLLike,
                   schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
                   logger: Logger | None = None) -> int:
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

    if isinstance(xmltree, etree._ElementTree):
        xmltree, _ = clear_xml(xmltree)
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

    kpt_tag: list[etree._Element] = []
    if alt_kpt_set is not None:
        kpt_tag = eval_simple_xpath(alt_kpt_set, schema_dict, 'kPointList', list_return=True, logger=logger)
        if len(kpt_tag) == 0:
            kpt_tag = eval_simple_xpath(alt_kpt_set, schema_dict, 'kPointCount', list_return=True, logger=logger)
            if len(kpt_tag) != 0:
                warnings.warn('kPointCount is not guaranteed to result in the given number of kpoints')

    if not kpt_tag and getattr(schema_dict, 'out_version', None) is None:
        kpt_tag = eval_simple_xpath(root,
                                    schema_dict,
                                    'kPointList',
                                    not_contains=['altKPointSet', 'numericalParameters'],
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
            warnings.warn('kPointCount is not guaranteed to result in the given number of kpoints')
    elif not kpt_tag and getattr(schema_dict, 'out_version', None) is not None:
        kpt_tag = eval_simple_xpath(root,
                                    schema_dict,
                                    'kPointList',
                                    contains='numericalParameters',
                                    list_return=True,
                                    logger=logger)

    nkpts = evaluate_attribute(kpt_tag[0], schema_dict, 'count', logger=logger)

    return nkpts


def get_cell(xmltree: XMLLike,
             schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
             logger: Logger | None = None,
             convert_to_angstroem: bool = True) -> tuple[np.ndarray, tuple[bool, bool, bool]]:
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
    :param convert_to_angstroem: bool if True the bravais matrix is converted to angstroem

    :returns: numpy array of the bravais matrix and list of boolean values for
              periodic boundary conditions
    """
    from masci_tools.util.schema_dict_util import read_constants, eval_simple_xpath
    from masci_tools.util.schema_dict_util import evaluate_text, tag_exists, evaluate_attribute
    from masci_tools.util.xml.common_functions import clear_xml
    from masci_tools.util.constants import BOHR_A

    if isinstance(xmltree, etree._ElementTree):
        xmltree, _ = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree
    constants = read_constants(root, schema_dict, logger=logger)

    cell: np.ndarray | None = None
    lattice_tag: etree._Element | None = None
    if tag_exists(root, schema_dict, 'bulkLattice', logger=logger):
        lattice_tag = eval_simple_xpath(root, schema_dict, 'bulkLattice', logger=logger)  #type: ignore
        pbc = (True, True, True)
    elif tag_exists(root, schema_dict, 'filmLattice', logger=logger):
        lattice_tag = eval_simple_xpath(root, schema_dict, 'filmLattice', logger=logger)  #type: ignore
        pbc = (True, True, False)

    if lattice_tag is not None:
        lattice_scale = evaluate_attribute(lattice_tag,
                                           schema_dict,
                                           'scale',
                                           constants=constants,
                                           logger=logger,
                                           not_contains={'/a', 'c/'})

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
            cell = np.array([row1, row2, row3]) * lattice_scale
            if convert_to_angstroem and cell is not None:
                cell *= BOHR_A

    if cell is None:
        raise ValueError('Could not extract Bravais matrix out of inp.xml. Is the '
                         'Bravais matrix explicitly given? i.e Latnam definition '
                         'not supported.')

    return cell, pbc


def _get_species_info(xmltree: XMLLike,
                      schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
                      logger: Logger | None = None) -> dict[str, dict[str, str]]:
    """
    Gets the species identifiers and information.
    Used to keep species information consistent between
    :py:func:`get_parameter_data` and :py:func:`get_structure_data`

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param logger: logger object for logging warnings, errors

    :returns: Tuple of dicts, containing the normalized species ids
              and the elements for each species
    """
    from masci_tools.util.xml.common_functions import clear_xml
    from masci_tools.util.schema_dict_util import read_constants, evaluate_attribute
    import re

    if isinstance(xmltree, etree._ElementTree):
        xmltree, _ = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree
    constants = read_constants(root, schema_dict, logger=logger)

    names = evaluate_attribute(root,
                               schema_dict,
                               'name',
                               constants=constants,
                               contains='species',
                               logger=logger,
                               list_return=True)
    elements = evaluate_attribute(root,
                                  schema_dict,
                                  'element',
                                  constants=constants,
                                  contains='species',
                                  logger=logger,
                                  list_return=True)

    if len(names) != len(elements):
        raise ValueError(
            f'Failed to read in species names and elements. Got {len(names)} names and {len(elements)} elements')

    species_info: dict[str, dict[str, str]] = {}
    for name, element in zip(names, elements):
        #Check if the species name has a numerical id at the end (separated by - or .)
        #And add all of them first
        species_info[name] = {}
        species_info[name]['element'] = element
        species_info[name]['normed_name'] = name
        match = re.fullmatch(r'(.+[\-\.])([1-9]+)', name)
        if match:
            species_info[name]['id'] = match.group(2)

    for name, info in species_info.items():
        if 'id' not in info:
            element = info['element']
            #Find the smallest id which is free
            used_ids = {
                int(val['id']) for name, val in species_info.items() if 'id' in val and val['element'] == element
            }
            possible_ids = range(1, max(used_ids, default=0) + 2)
            info['id'] = str(min(set(possible_ids) - set(used_ids)))
            #Just append the id to the normed name
            info['normed_name'] += f"-{info['id']}"

    return species_info


def get_parameter_data(xmltree: XMLLike,
                       schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
                       inpgen_ready: bool = True,
                       write_ids: bool = True,
                       extract_econfig: bool = False,
                       logger: Logger | None = None) -> dict[str, Any]:
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
    from masci_tools.util.schema_dict_util import read_constants, eval_simple_xpath, attrib_exists
    from masci_tools.util.schema_dict_util import evaluate_attribute, evaluate_text, evaluate_tag
    from masci_tools.util.xml.common_functions import clear_xml
    from masci_tools.util.xml.converters import convert_fleur_lo, convert_fleur_electronconfig
    from masci_tools.io.common_functions import filter_out_empty_dict_entries

    # TODO: convert econfig
    # TODO: parse kpoints, somehow count is bad (if symmetry changes), mesh is not known, path cannot be specified

    ########
    parameters = {}
    if isinstance(xmltree, etree._ElementTree):
        xmltree, _ = clear_xml(xmltree)
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
    parameters['comp'] = filter_out_empty_dict_entries(comp_dict)

    # &atoms
    species_list = eval_simple_xpath(root, schema_dict, 'species', list_return=True, logger=logger)

    species_info = _get_species_info(xmltree, schema_dict, logger=logger)

    for indx, species in enumerate(species_list):
        atom_dict = {}
        atoms_name = f'atom{indx}'
        atom_z = evaluate_attribute(species, schema_dict, 'atomicNumber', constants=constants, logger=logger)
        atom_name = evaluate_attribute(species, schema_dict, 'name', constants=constants, logger=logger)
        if not inpgen_ready:
            atom_dict['z'] = atom_z
        atom_id = f"{atom_z}.{species_info[atom_name]['id']}"
        if write_ids:
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

        if extract_econfig:
            if inpgen_ready:
                atom_econfig = eval_simple_xpath(species,
                                                 schema_dict,
                                                 'electronConfig',
                                                 list_return=True,
                                                 logger=logger)
                if len(atom_econfig) != 0:
                    atom_dict['econfig'] = convert_fleur_electronconfig(atom_econfig[0])
            else:
                atom_dict['econfig'] = evaluate_tag(species,
                                                    schema_dict,
                                                    'electronConfig',
                                                    constants=constants,
                                                    logger=logger,
                                                    subtags=True,
                                                    ignore={'flipSpins'})

        atom_lo = eval_simple_xpath(species, schema_dict, 'lo', list_return=True, logger=logger)

        if len(atom_lo) != 0:
            atom_dict['lo'] = convert_fleur_lo(atom_lo)

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
        parameters['soc'] = {'theta': theta, 'phi': phi}

    # kpt
    if schema_dict.inp_version > (0, 31):
        list_name = evaluate_attribute(root, schema_dict, 'listName', logger=logger)
        kpointlists = eval_simple_xpath(root,
                                        schema_dict,
                                        'kPointList',
                                        contains='kPointLists',
                                        list_return=True,
                                        logger=logger)

        if len(kpointlists) == 0:
            raise ValueError('No Kpoint lists found in the given inp.xml')
        labels = [kpoint_set.attrib.get('name') for kpoint_set in kpointlists]
        if list_name not in labels:
            raise ValueError(f'Selected Kpoint list with the name: {list_name} does not exist'
                             f'Available list names: {labels}')

        kpoint_index = labels.index(list_name)
        kpoint_set = kpointlists[kpoint_index]

        if attrib_exists(kpoint_set, schema_dict, 'type', logger=logger):
            kpoint_type = evaluate_attribute(kpoint_set, schema_dict, 'type', logger=logger)

            if kpoint_type == 'mesh':
                nx = evaluate_attribute(kpoint_set, schema_dict, 'nx', logger=logger, optional=True)
                ny = evaluate_attribute(kpoint_set, schema_dict, 'ny', logger=logger, optional=True)
                nz = evaluate_attribute(kpoint_set, schema_dict, 'nz', logger=logger, optional=True)
                if all(n is not None for n in (nx, ny, nz)):
                    parameters['kpt'] = {'div1': nx, 'div2': ny, 'div3': nz}

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


def get_structure_data(
        xmltree: XMLLike,
        schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
        include_relaxations: bool = True,
        site_namedtuple: bool = True,
        convert_to_angstroem: bool = True,
        normalize_kind_name: bool = True,
        logger: Logger | None = None) -> tuple[list[AtomSiteProperties], np.ndarray, tuple[bool, bool, bool]]:
    """
    Get the structure defined in the given fleur xml file.

    .. warning::
        Only the explicit definition of the Bravais matrix is supported.
        Old inputs containing the `latnam` definitions are not supported

    .. warning::
        In versions ``0.5.0`` or later the output of the atom sites was restructured
        to be more interoperable with other IO functions (e.g. :py:func:`~masci_tools.io.fleur_inpgen.write_inpgen_file()`)
        The new format returns a list of :py:class:`~masci_tools.io.common_functions.AtomSiteProperties`
        instead of the list of tuples (position, symbol)

        For better compatibility this output is not default in ``0.5.0`` but instead
        is enabled by ``site_namedtuple=True`` and a DeprecationWarning is given when
        this argument is ``False``.

    .. note::
        In versions ``0.5.0`` or later the returned atom positions correspond to the relaxed
        structure if a ``relaxation`` section is present in the xmltree


    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param include_relaxations: bool if True and a relaxation section is included
                                the resulting positions correspond to the relaxed structure
    :param logger: logger object for logging warnings, errors
    :param convert_to_angstroem: bool if True the bravais matrix is converted to angstroem

    :returns: tuple containing the structure information

    The tuple contains the following entries:

        1. :atom_data: list of (named)tuples containing the absolute positions and symbols of the atoms
        2. :cell: numpy array, bravais matrix of the given system
        3. :pbc: list of booleans, determines in which directions periodic boundary conditions are applicable

    """
    from masci_tools.util.schema_dict_util import read_constants, eval_simple_xpath, tag_exists
    from masci_tools.util.schema_dict_util import evaluate_text, evaluate_attribute
    from masci_tools.util.xml.common_functions import clear_xml
    from masci_tools.io.common_functions import rel_to_abs, rel_to_abs_f, abs_to_rel, abs_to_rel_f
    from masci_tools.io.common_functions import find_symmetry_relation
    from masci_tools.util.constants import BOHR_A

    if not site_namedtuple:
        warnings.warn(
            'Output of atom positions in pure tuples of the form (position, symbol) is deprecated.'
            'Please adjust your code to use the namedtuple AtomSiteProperties (see masci_tools.io.common_functions)'
            ' with the fields (position, symbol, kind)', DeprecationWarning)

    if isinstance(xmltree, etree._ElementTree):
        xmltree, _ = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree
    constants = read_constants(root, schema_dict, logger=logger)
    cell, pbc = get_cell(root, schema_dict, logger=logger, convert_to_angstroem=convert_to_angstroem)

    species_info = _get_species_info(xmltree, schema_dict, logger=None)

    atom_data: list[AtomSiteProperties] = []
    atom_groups = eval_simple_xpath(root, schema_dict, 'atomGroup', list_return=True, logger=logger)

    #Read relaxation information if available
    displacements = None
    rotations, shifts = None, None
    if include_relaxations and schema_dict.inp_version >= (0, 29):
        if tag_exists(root, schema_dict, 'relaxation', logger=logger):
            relax_info = get_relaxation_information(root, schema_dict, logger=logger)
            #We still read in the normal atom positions since the displacements are provided
            #per atomtype
            displacements = relax_info['displacements']
            if convert_to_angstroem:
                displacements = [np.array(displace) * BOHR_A for displace in displacements]
            rotations, shifts = get_symmetry_information(root, schema_dict, logger=logger)

            if len(displacements) != len(atom_groups):
                raise ValueError(
                    f'Did not get the right number of relaxed positions. Expected {len(atom_groups)} got {len(displacements)}'
                )

    for indx, group in enumerate(atom_groups):

        atom_positions: list[list[float]] = []

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

        if convert_to_angstroem:
            atom_positions = [list(np.array(pos) * BOHR_A) for pos in absolute_positions]
        else:
            atom_positions = absolute_positions

        for rel_pos in relative_positions:
            atom_positions.append(rel_to_abs(rel_pos, cell))

        for film_pos in film_positions:
            film_pos = rel_to_abs_f(film_pos, cell)
            if convert_to_angstroem:
                film_pos[2] *= BOHR_A
            atom_positions.append(film_pos)

        if len(atom_positions) == 0:
            raise ValueError('Failed to read atom positions for group')

        if displacements:
            representative_pos = np.array(atom_positions[0])

            if rotations is None or shifts is None:
                raise ValueError('Symmetry information is required but not available')

            if len(film_positions) != 0:
                rel_displace = abs_to_rel_f(displacements[indx], cell, pbc)
                rel_representative_pos = abs_to_rel_f(representative_pos, cell, pbc)
                rel_displace[2] = rel_displace[2] / cell[2, 2]
                rel_representative_pos[2] = rel_representative_pos[2] / cell[2, 2]
            else:
                rel_displace = abs_to_rel(displacements[indx], cell)
                rel_representative_pos = abs_to_rel(representative_pos, cell)

            for pos_indx, pos in enumerate(atom_positions):
                rot, shift = find_symmetry_relation(representative_pos,
                                                    pos,
                                                    rotations,
                                                    shifts,
                                                    cell,
                                                    relative_pos=False,
                                                    film=len(film_positions) != 0)

                #More explicit than it needs to be
                #but analogous to fleur
                rot_pos = np.matmul(rot, rel_representative_pos) + shift
                site_displace = np.matmul(rot, rel_representative_pos + rel_displace) + shift
                site_displace = site_displace - rot_pos

                if len(film_positions) != 0:
                    site_displace = rel_to_abs_f(site_displace, cell)
                    site_displace[2] *= cell[2, 2]
                else:
                    site_displace = rel_to_abs(site_displace, cell)

                atom_positions[pos_indx] = list(np.array(atom_positions[pos_indx]) + np.array(site_displace))

        group_species = evaluate_attribute(group, schema_dict, 'species', constants=constants, logger=logger)
        element = species_info[group_species]['element']
        if normalize_kind_name and site_namedtuple:
            normed_name = species_info[group_species]['normed_name']
            if normed_name != group_species:
                if logger is None:
                    warnings.warn(
                        f'Normalized species name {group_species} to {normed_name}. '
                        "Use the option 'normed_kind_name=False' to preserve the original species name", UserWarning)
                else:
                    logger.warning(f'Normalized species name {group_species} to {normed_name}. '
                                   "Use the option 'normed_kind_name=False' to preserve the original species name")
                group_species = normed_name

        if site_namedtuple:
            atom_data.extend(
                AtomSiteProperties(position=pos, symbol=element, kind=group_species) for pos in atom_positions)
        else:
            atom_data.extend((pos, element) for pos in atom_positions)  #type:ignore

    return atom_data, cell, pbc


@schema_dict_version_dispatch(output_schema=False)
def get_kpoints_data(
    xmltree: XMLLike,
    schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
    name: str | None = None,
    index: int | None = None,
    only_used: bool = False,
    logger: Logger | None = None,
    convert_to_angstroem: bool = True
) -> tuple[list[list[float]] | dict[str, list[list[float]]], list[float] | dict[str, list[float]], np.ndarray, tuple[
        bool, bool, bool]]:
    """
    Get the kpoint sets defined in the given fleur xml file.

    .. warning::
        For file versions before Max5 the name argument is not valid

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param name: str, optional, if given only the kpoint set with the given name
                 is returned
    :param index: int, optional, if given only the kpoint set with the given index
                  is returned
    :param only_used: bool if True only the kpoint list used in the calculation is returned
    :param logger: logger object for logging warnings, errors
    :param convert_to_angstroem: bool if True the bravais matrix is converted to angstroem

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

    if name is not None and index is not None:
        raise ValueError('Only provide one of index or name to select kpoint lists')

    if only_used and (name is not None or index is not None):
        raise ValueError('Either use only_used=False and provide the name/index or use only_used=True. Not both')

    if isinstance(xmltree, etree._ElementTree):
        xmltree, _ = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree

    constants = read_constants(root, schema_dict, logger=logger)

    if only_used:
        name = evaluate_attribute(root, schema_dict, 'listName', logger=logger)

    cell, pbc = get_cell(root, schema_dict, logger=logger, convert_to_angstroem=convert_to_angstroem)

    kpointlists = eval_simple_xpath(root,
                                    schema_dict,
                                    'kPointList',
                                    contains='kPointLists',
                                    list_return=True,
                                    logger=logger)

    if len(kpointlists) == 0:
        raise ValueError('No Kpoint lists found in the given inp.xml')

    labels = [kpoint_set.attrib.get('name') for kpoint_set in kpointlists]
    if name is not None and name not in labels:
        if only_used:
            raise ValueError(f'Found no Kpoint list with the name: {name}'
                             f'Available list names: {labels}'
                             'The listName attribute is not consistent with the rest of the input')
        raise ValueError(f'Found no Kpoint list with the name: {name}'
                         f'Available list names: {labels}')

    if index is not None:
        try:
            kpointlists = [kpointlists[index]]
        except IndexError as exc:
            raise ValueError(f'No kPointList with index {index} found. Only {len(kpointlists)} available') from exc

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
def get_kpoints_data_max4(
        xmltree: XMLLike,
        schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
        logger: Logger | None = None,
        convert_to_angstroem: bool = True,
        only_used: bool = False) -> tuple[list[list[float]], list[float], np.ndarray, tuple[bool, bool, bool]]:
    """
    Get the kpoint sets defined in the given fleur xml file.

    .. note::
        This function is specific to file version before and including the
        Max4 release of fleur

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param logger: logger object for logging warnings, errors
    :param convert_to_angstroem: bool if True the bravais matrix is converted to angstroem
    :param only_used: (Has no effect for Max4) bool if True only the kpoint list used in the calculation is returned

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

    if isinstance(xmltree, etree._ElementTree):
        xmltree, _ = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree

    constants = read_constants(root, schema_dict, logger=logger)

    cell, pbc = get_cell(root, schema_dict, logger=logger, convert_to_angstroem=convert_to_angstroem)

    kpointlist = eval_simple_xpath(root,
                                   schema_dict,
                                   'kPointList',
                                   list_return=True,
                                   not_contains=['altKPoint', 'numericalParameters'],
                                   logger=logger)

    if len(kpointlist) == 0:
        if getattr(schema_dict, 'out_version', None) is not None:
            kpointlist = eval_simple_xpath(root,
                                           schema_dict,
                                           'kPointList',
                                           list_return=True,
                                           contains='numericalParameters',
                                           logger=logger)
        else:
            raise ValueError('No Kpoint lists found in the given inp.xml')

    kpoints = evaluate_text(kpointlist[0],
                            schema_dict,
                            'kPoint',
                            constants=constants,
                            not_contains='altKPoint',
                            list_return=True,
                            logger=logger)
    weights = evaluate_attribute(kpointlist[0],
                                 schema_dict,
                                 'weight',
                                 constants=constants,
                                 not_contains='altKPoint',
                                 list_return=True,
                                 logger=logger)

    return kpoints, weights, cell, pbc


@schema_dict_version_dispatch(output_schema=False)
def get_relaxation_information(xmltree: XMLLike,
                               schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
                               logger: Logger | None = None) -> dict[str, Any]:
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
    from masci_tools.util.xml.common_functions import clear_xml

    if isinstance(xmltree, etree._ElementTree):
        xmltree, _ = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree
    constants = read_constants(root, schema_dict, logger=logger)

    if not tag_exists(root, schema_dict, 'relaxation', logger=logger):
        raise ValueError('No relaxation information included in the given XML file')

    relax_tag: etree._Element = eval_simple_xpath(root, schema_dict, 'relaxation', logger=logger)  #type:ignore

    out_dict = {}
    out_dict['displacements'] = evaluate_text(relax_tag,
                                              schema_dict,
                                              'displace',
                                              list_return=True,
                                              constants=constants,
                                              logger=logger)

    out_dict['energies'] = evaluate_attribute(relax_tag,
                                              schema_dict,
                                              'energy',
                                              list_return=True,
                                              constants=constants,
                                              logger=logger)

    out_dict['posforces'] = []
    relax_iters = eval_simple_xpath(relax_tag, schema_dict, 'step', list_return=True, logger=logger)
    for step in relax_iters:
        posforces = evaluate_text(step, schema_dict, 'posforce', list_return=True, constants=constants, logger=logger)
        out_dict['posforces'].append(posforces)

    return out_dict


@get_relaxation_information.register(max_version='0.28')
def get_relaxation_information_pre029(xmltree: XMLLike,
                                      schema_dict: (fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict),
                                      logger: Logger | None = None) -> None:
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


def get_symmetry_information(xmltree: XMLLike,
                             schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
                             logger: Logger | None = None) -> tuple[list[np.ndarray], list[np.ndarray]]:
    """
    Get the symmetry information from the given fleur XML file. This includes the
    rotation matrices and shifts defined in the ``symmetryOperations`` tag.

    .. note::
        Only the explicit definition of the used symmetry operations in the xml file
        is supported.

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param logger: logger object for logging warnings, errors

    :returns: tuple of the rotations and their respective shifts

    :raises ValueError: If no symmetryOperations section is included in the xml tree
    """
    from masci_tools.util.schema_dict_util import tag_exists, read_constants, evaluate_text, eval_simple_xpath
    from masci_tools.util.xml.common_functions import clear_xml

    if isinstance(xmltree, etree._ElementTree):
        xmltree, _ = clear_xml(xmltree)
        root = xmltree.getroot()
    else:
        root = xmltree
    constants = read_constants(root, schema_dict, logger=logger)

    if not tag_exists(root, schema_dict, 'symmetryOperations', logger=logger):
        raise ValueError('No explicit symmetry information included in the given XML file')

    ops = eval_simple_xpath(root, schema_dict, 'symOp', logger=logger, list_return=True)

    rotations = []
    shifts = []
    for op in ops:
        row1 = evaluate_text(op, schema_dict, 'row-1', constants=constants, logger=logger)
        row2 = evaluate_text(op, schema_dict, 'row-2', constants=constants, logger=logger)
        row3 = evaluate_text(op, schema_dict, 'row-3', constants=constants, logger=logger)

        rot = np.array([row1[:3], row2[:3], row3[:3]]).astype(int)
        shift = np.array([row1[3], row2[3], row3[3]])

        rotations.append(rot)
        shifts.append(shift)

    return rotations, shifts
