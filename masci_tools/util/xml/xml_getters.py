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
from masci_tools.io.fleur_xml import FleurXMLContext

from lxml import etree
import warnings
import numpy as np
from logging import Logger
from typing import Any

from .xpathbuilder import FilterType


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

    fleur_modes = {}
    with FleurXMLContext(xmltree, schema_dict, logger=logger) as root:
        fleur_modes['jspin'] = root.attribute('jspins')
        fleur_modes['noco'] = root.attribute('l_noco', default=False)
        fleur_modes['soc'] = root.attribute('l_soc', default=False)
        fleur_modes['relax'] = root.attribute('l_f', default=False)
        fleur_modes['gw'] = False
        if root.tag_exists('expertModes'):
            gw = root.attribute('gw', optional=True)
            if gw is None and schema_dict.inp_version >= (0, 34):
                gw = root.attribute('spex', default=0)
            fleur_modes['gw'] = gw != 0

        if schema_dict.inp_version > (0, 27):
            fleur_modes['force_theorem'] = root.tag_exists('forceTheorem')
        else:
            fleur_modes['force_theorem'] = False

        fleur_modes['cf_coeff'] = False
        if schema_dict.inp_version >= (0, 33) and root.tag_exists('cFCoeffs'):
            cf_coeff = any(root.attribute('potential', tag_name='cFCoeffs', list_return=True, optional=True))
            cf_coeff = cf_coeff or any(
                root.attribute('chargeDensity', tag_name='cFCoeffs', list_return=True, optional=True))
            fleur_modes['cf_coeff'] = cf_coeff

        fleur_modes['plot'] = False
        if root.tag_exists('plotting'):
            plot = root.attribute('iplot', default=False)
            if schema_dict.inp_version >= (0, 29):
                plot = isinstance(plot, int) and plot != 0
            fleur_modes['plot'] = plot

        fleur_modes['film'] = root.tag_exists('filmPos')
        fleur_modes['ldau'] = root.tag_exists('ldaU', contains='species')
        fleur_modes['dos'] = root.attribute('dos')
        fleur_modes['band'] = root.attribute('band')
        fleur_modes['bz_integration'] = root.attribute('mode', tag_name='bzIntegration')

        greensf = False
        if schema_dict.inp_version >= (0, 32):
            #We make the assumption that the existence of a greensfCalculation
            #tag implies the existence of a greens function calculation
            greensf = root.tag_exists('greensfCalculation', contains='species')
            if schema_dict.inp_version >= (0, 35):
                greensf = greensf or root.tag_exists('torqueCalculation', contains='species')
            else:
                greensf = greensf or root.tag_exists('torgueCalculation', contains='species')
        fleur_modes['greensf'] = greensf

        ldahia = False
        if schema_dict.inp_version >= (0, 32):
            ldahia = root.tag_exists('ldaHIA', contains='species')
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
    with FleurXMLContext(xmltree, schema_dict, logger=logger) as root:
        #Get the name of the current selected kPointSet
        list_name = root.attribute('listName')
        all_names = set(
            root.attribute('name', tag_name='kPointList', contains='kPointLists', list_return=True, optional=True))
        if list_name not in all_names:
            raise ValueError(f'Selected Kpoint list with the name: {list_name} does not exist\n'
                             f'Available list names: {all_names}')

        with root.find('kPointList', contains='kPointLists', filters={'kPointList': {'name': list_name}}) as kpoints:
            nkpts = kpoints.attribute('count')

    if not isinstance(nkpts, int):
        raise ValueError('Failed to evaluate nkpts')

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
    modes = get_fleur_modes(xmltree, schema_dict, logger=logger)
    with FleurXMLContext(xmltree, schema_dict, logger=logger) as root:

        nkpts = None
        if modes['band'] or modes['gw']:
            filters = {'altKPointSet': {'purpose': 'bands' if modes['band'] else 'gw'}}
            if root.tag_exists('altKPointSet', filters=filters):
                with root.find('altKPointSet', filters=filters) as kpoints:
                    nkpts = kpoints.attribute('count', tag_name='kPointList', optional=True)
                    if nkpts is None:
                        nkpts = kpoints.attribute('count', tag_name='kPointCount', optional=True)
                        if nkpts is not None:
                            warnings.warn('kPointCount is not guaranteed to result in the given number of kpoints')
                    if nkpts is None:
                        raise ValueError('No kPointList or kPointCount found')

        output_schema = getattr(schema_dict, 'out_version', None) is not None
        if nkpts is None and output_schema:
            nkpts = root.attribute('count', tag_name='kPointList', contains='numericalParameters')
        elif nkpts is None and not output_schema:
            nkpts = root.attribute('count',
                                   tag_name='kPointList',
                                   not_contains=['altKPointSet', 'numericalParameters'],
                                   optional=True)
            if nkpts is None:
                nkpts = root.attribute('count', tag_name='kPointCount', not_contains='altKPointSet', optional=True)
                if nkpts is not None:
                    warnings.warn('kPointCount is not guaranteed to result in the given number of kpoints')
            if nkpts is None:
                raise ValueError('No kPointList or kPointCount found')

    if not isinstance(nkpts, int):
        raise ValueError('Failed to evaluate nkpts')

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
    from masci_tools.util.constants import BOHR_A

    NO_CELL_ERROR = 'Could not extract Bravais matrix out of inp.xml. Is the ' \
                    'Bravais matrix explicitly given? i.e Latnam definition ' \
                    'not supported.'

    cell: np.ndarray | None = None
    with FleurXMLContext(xmltree, schema_dict, logger=logger) as root:

        lattice_tag: etree._Element | None = None
        if root.tag_exists('bulkLattice'):
            lattice_tag = root.simple_xpath('bulkLattice')  #type:ignore[assignment]
            pbc = (True, True, True)
        elif root.tag_exists('filmLattice'):
            lattice_tag = root.simple_xpath('filmLattice')  #type:ignore[assignment]
            pbc = (True, True, False)

        if lattice_tag is None:
            raise ValueError(NO_CELL_ERROR)

        with root.nested(lattice_tag) as lattice:
            scale = lattice.attribute('scale', not_contains={'/a', 'c/'})

            bravais_tag: etree._Element
            if lattice.tag_exists('bravaisMatrix'):
                bravais_tag = lattice.simple_xpath('bravaisMatrix')  #type:ignore[assignment]
            elif not all(pbc) and schema_dict.inp_version >= (0, 35):
                bravais_tag = lattice.simple_xpath('bravaisMatrixFilm')  #type:ignore[assignment]
            else:
                raise ValueError(NO_CELL_ERROR)

            film_matrix = bravais_tag.tag == 'bravaisMatrixFilm'
            with lattice.nested(bravais_tag) as bravais:

                row1 = bravais.text('row-1', optional=True)
                row2 = bravais.text('row-2', optional=True)
                if film_matrix:
                    dtilda = lattice.attribute('dtilda')
                    row1 += [0.0]
                    row2 += [0.0]
                    row3 = [0.0, 0.0, dtilda]
                else:
                    row3 = bravais.text('row-3', optional=True)

            if all(x is not None and x != [] for x in [row1, row2, row3]):
                cell = np.array([row1, row2, row3]) * scale
                if convert_to_angstroem and cell is not None:
                    cell *= BOHR_A

    if cell is None:
        raise ValueError(NO_CELL_ERROR)

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
    import re

    with FleurXMLContext(xmltree, schema_dict, logger=logger) as root:

        names = root.attribute('name', contains='species', list_return=True)
        elements = root.attribute('element', contains='species', list_return=True)

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
                       allow_special_los: bool = True,
                       logger: Logger | None = None) -> dict[str, Any]:
    """
    This routine returns an python dictionary produced from the inp.xml
    file, which contains all the parameters needed to setup a new inp.xml from a inpgen
    input file to produce the same input (for parameters that the inpgen can control)

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param inpgen_ready: Bool, return a dict which can be inputted into inpgen while setting atoms
    :param write_ids: Bool, if True the atom ids are added to the atom namelists
    :param logger: logger object for logging warnings, errors

    :returns: dict, which will lead to the same inp.xml (in case if other defaults,
              which can not be controlled by input for inpgen, were changed)

    """
    from masci_tools.util.xml.converters import convert_fleur_lo, convert_fleur_electronconfig
    from masci_tools.io.common_functions import filter_out_empty_dict_entries

    # TODO: convert econfig
    # TODO: parse kpoints, somehow count is bad (if symmetry changes), mesh is not known, path cannot be specified

    ########
    parameters = {}

    # Create the cards

    # &input # most things are not needed for AiiDA here. or we ignor them for now.
    # film is set by the plugin depended on the structure
    # symor per default = False? to avoid input which fleur can't take

    with FleurXMLContext(xmltree, schema_dict, logger=logger) as root:

        # &comp namelist
        comp_dict = {}
        comp_dict['jspins'] = root.attribute('jspins')
        comp_dict['frcor'] = root.attribute('frcor', optional=True)
        comp_dict['ctail'] = root.attribute('ctail')
        comp_dict['kcrel'] = root.attribute('kcrel', optional=True)
        comp_dict['gmax'] = root.attribute('gmax')
        comp_dict['gmaxxc'] = root.attribute('gmaxxc')
        comp_dict['kmax'] = root.attribute('kmax')
        parameters['comp'] = filter_out_empty_dict_entries(comp_dict)

        species_info = _get_species_info(xmltree, schema_dict, logger=logger)
        for index, species in enumerate(root.iter('species')):

            atom_dict = {}
            atomlist_name = f'atom{index}'

            atom_z = species.attribute('atomicNumber')
            atom_name = species.attribute('name')
            if not inpgen_ready:
                atom_dict['z'] = atom_z
            atom_id = f"{atom_z}.{species_info[atom_name]['id']}"
            if write_ids:
                atom_dict['id'] = atom_id

            if schema_dict.inp_version <= (0, 31):
                atom_dict['ncst'] = species.attribute('coreStates')
            atom_dict['rmt'] = species.attribute('radius')
            atom_dict['dx'] = species.attribute('logIncrement')
            atom_dict['jri'] = species.attribute('gridPoints')
            atom_dict['lmax'] = species.attribute('lmax')
            atom_dict['lnonsph'] = species.attribute('lnonsphr')
            atom_dict['bmu'] = species.attribute('magMom', optional=True)

            atom_dict['element'] = species.attribute('element')

            if extract_econfig:
                if inpgen_ready:
                    atom_econfig = species.simple_xpath('electronConfig', list_return=True)
                    if len(atom_econfig) != 0:
                        atom_dict['econfig'] = convert_fleur_electronconfig(atom_econfig[0])
                else:
                    atom_dict['econfig'] = species.all_attributes('electronConfig', subtags=True, ignore={'flipSpins'})

            atom_lo = species.simple_xpath('lo', list_return=True)
            if len(atom_lo) != 0:
                atom_dict['lo'] = convert_fleur_lo(atom_lo, allow_special_los=allow_special_los)  #type:ignore[arg-type]

            parameters[atomlist_name] = filter_out_empty_dict_entries(atom_dict)

        # &soc namelist
        soc = root.attribute('l_soc', default=False)
        theta = root.attribute('theta', contains='soc', default=0.0)
        phi = root.attribute('phi', contains='soc', default=0.0)
        if soc:
            parameters['soc'] = {'theta': theta, 'phi': phi}

        # &kpt namelist
        if schema_dict.inp_version > (0, 31):
            list_name = root.attribute('listName')
            all_names = set(
                root.attribute('name', tag_name='kPointList', contains='kPointLists', list_return=True, optional=True))
            if list_name not in all_names:
                raise ValueError(f'Selected Kpoint list with the name: {list_name} does not exist\n'
                                 f'Available list names: {all_names}')

            with root.find('kPointList', contains='kPointLists', filters={'kPointList': {
                    'name': list_name
            }}) as kpoints:

                kpoint_type = kpoints.attribute('type', optional=True)
                if kpoint_type == 'mesh':
                    nx = kpoints.attribute('nx', optional=True)
                    ny = kpoints.attribute('ny', optional=True)
                    nz = kpoints.attribute('nz', optional=True)
                    if all(n is not None for n in (nx, ny, nz)):
                        parameters['kpt'] = {'div1': nx, 'div2': ny, 'div3': nz}

        # title
        title = root.text('comment', optional=True)
        if title:
            parameters['title'] = title.replace('\n', '').strip()

        # &exco
        exco_dict = {}
        exco_dict['xctyp'] = root.attribute(
            'name',
            tag_name='xcFunctional',
        )
        parameters['exco'] = filter_out_empty_dict_entries(exco_dict)
    # &film
    # TODO

    # &qss
    # TODO

    # lattice, not supported?

    return parameters


def get_structure_data(xmltree: XMLLike,
                       schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
                       include_relaxations: bool = True,
                       convert_to_angstroem: bool = True,
                       normalize_kind_name: bool = True,
                       logger: Logger | None = None,
                       **kwargs: Any) -> tuple[list[AtomSiteProperties], np.ndarray, tuple[bool, bool, bool]]:
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

    .. versionchanged:: 0.7.0
        The default for `site_namedtuple` is set to `True`

    .. versionchanged:: 0.10.0
        The argument `site_namedtuple` was deprecated. The old output is no longer supported. If the
        argument `site_namedtuple` is passed a deprecation warning is shown

    """
    from masci_tools.io.common_functions import rel_to_abs, rel_to_abs_f, abs_to_rel, abs_to_rel_f
    from masci_tools.io.common_functions import find_symmetry_relation
    from masci_tools.util.constants import BOHR_A

    if 'site_namedtuple' in kwargs:
        warnings.warn(
            'The argument site_namedtuple is deprecated and has no effect.'
            'The output is always given in AtomSiteProperties', DeprecationWarning)

    cell, pbc = get_cell(xmltree, schema_dict, logger=logger, convert_to_angstroem=convert_to_angstroem)
    species_info = _get_species_info(xmltree, schema_dict, logger=None)

    atom_data: list[AtomSiteProperties] = []
    with FleurXMLContext(xmltree, schema_dict, logger=logger) as root:

        #Read relaxation information if available
        displacements = None
        rotations, shifts = None, None
        if include_relaxations and schema_dict.inp_version >= (0, 29):
            if root.tag_exists('relaxation'):
                relax_info = get_relaxation_information(xmltree, schema_dict, logger=logger)
                #We still read in the normal atom positions since the displacements are provided
                #per atomtype
                displacements = relax_info['displacements']
                if convert_to_angstroem:
                    displacements = [np.array(displace) * BOHR_A for displace in displacements]
                rotations, shifts = get_symmetry_information(xmltree, schema_dict, logger=logger)

                if len(displacements) != root.number_nodes('atomGroup'):
                    raise ValueError(
                        f"Did not get the right number of relaxed positions. Expected {root.number_nodes('atomGroup')} got {len(displacements)}"
                    )

        for index, group in enumerate(root.iter('atomGroup')):

            atom_positions: list[list[float]] = []

            absolute_positions = group.text('absPos', list_return=True, optional=True)
            relative_positions = group.text('relPos', list_return=True, optional=True)
            film_positions = group.text('filmPos', list_return=True, optional=True)

            if convert_to_angstroem:
                atom_positions = [list(np.array(pos) * BOHR_A) for pos in absolute_positions]
            else:
                atom_positions = absolute_positions

            atom_positions.extend(rel_to_abs(pos, cell) for pos in relative_positions)

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
                    rel_displace = abs_to_rel_f(displacements[index], cell, pbc)
                    rel_representative_pos = abs_to_rel_f(representative_pos, cell, pbc)
                    rel_displace[2] = rel_displace[2] / cell[2, 2]
                    rel_representative_pos[2] = rel_representative_pos[2] / cell[2, 2]
                else:
                    rel_displace = abs_to_rel(displacements[index], cell)
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

            group_species = group.attribute('species')
            element = species_info[group_species]['element']
            if normalize_kind_name:
                normed_name = species_info[group_species]['normed_name']
                if normed_name != group_species:
                    if logger is None:
                        warnings.warn(
                            f'Normalized species name {group_species} to {normed_name}. '
                            "Use the option 'normed_kind_name=False' to preserve the original species name",
                            UserWarning)
                    else:
                        logger.warning(f'Normalized species name {group_species} to {normed_name}. '
                                       "Use the option 'normed_kind_name=False' to preserve the original species name")
                    group_species = normed_name

            atom_data.extend(
                AtomSiteProperties(position=pos, symbol=element, kind=group_species) for pos in atom_positions)

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
        For file versions before Max5 arguments `name`, `index` and `only_used`
        have no effect

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

    if name is not None and index is not None:
        raise ValueError('Only provide one of index or name to select kpoint lists')

    if only_used and (name is not None or index is not None):
        raise ValueError('Either use only_used=False and provide the name/index or use only_used=True. Not both')

    cell, pbc = get_cell(xmltree, schema_dict, logger=logger, convert_to_angstroem=convert_to_angstroem)

    with FleurXMLContext(xmltree, schema_dict, logger=logger) as root:

        if only_used:
            name = root.attribute('listName')

        filters: FilterType = {}
        if name is not None:
            filters['kPointList'] = {'name': name}
        if index is not None:
            filters['kPointList'] = {'index': index + 1 if index >= 0 else index}

        if root.number_nodes('kPointList', contains='kPointLists', filters=filters) == 0:
            labels = root.attribute('name', tag_name='kPointList', contains='kPointLists', list_return=True)
            if only_used:
                raise ValueError(f'Found no Kpoint list with the name: {name}'
                                 f'Available list names: {labels}'
                                 'The listName attribute is not consistent with the rest of the input')
            if name is not None:
                raise ValueError(f'Found no Kpoint list with the name: {name}'
                                 f'Available list names: {labels}')
            raise ValueError('No Kpoint lists found in the given inp.xml, matching the criteria could be found'
                             f'Available list names: {labels}')

        kpoints_data = {}
        weights_data = {}
        for kpointlist in root.iter('kPointList', contains='kPointLists', filters=filters):

            label = kpointlist.attribute('name')
            kpoints = kpointlist.text('kPoint', list_return=True)
            weights = kpointlist.attribute('weight', list_return=True)

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
        name: str | None = None,
        index: int | None = None,
        only_used: bool = False,
        logger: Logger | None = None,
        convert_to_angstroem: bool = True
) -> tuple[list[list[float]], list[float], np.ndarray, tuple[bool, bool, bool]]:
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
    :param name: (Has no effect for Max4)
    :param index: (Has no effect for Max4)

    :returns: tuple containing the kpoint information

    The tuple contains the following entries:

        1. :kpoints: list containing the coordinates of the kpoints
        2. :weights: list containing the weights of the kpoints
        3. :cell: numpy array, bravais matrix of the given system
        4. :pbc: list of booleans, determines in which directions periodic boundary conditions are applicable

    """
    cell, pbc = get_cell(xmltree, schema_dict, logger=logger, convert_to_angstroem=convert_to_angstroem)

    with FleurXMLContext(xmltree, schema_dict, logger=logger) as root:

        kpointlist_tag = root.simple_xpath('kPointList',
                                           list_return=True,
                                           not_contains=['altKPoint', 'numericalParameters'])

        if len(kpointlist_tag) == 0:
            if getattr(schema_dict, 'out_version', None) is not None:
                kpointlist_tag = root.simple_xpath('kPointList', list_return=True, contains='numericalParameters')
            else:
                raise ValueError('No Kpoint lists found in the given inp.xml')

        with root.nested(kpointlist_tag[0]) as kpointlist:
            kpoints = kpointlist.text('kPoint', list_return=True)
            weights = kpointlist.attribute('weight', list_return=True)

    return kpoints, weights, cell, pbc


@schema_dict_version_dispatch(output_schema=False)
def get_special_kpoints(
    xmltree: XMLLike,
    schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
    name: str | None = None,
    index: int | None = None,
    only_used: bool = False,
    logger: Logger | None = None,
) -> list[tuple[int, str]] | dict[str, list[tuple[int, str]]]:
    """
    Extract the labeled special kpoints from the given kpointlist

    .. warning::
        Only implemented for versions starting with Max5

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param name: str, optional, if given only the kpoint set with the given name
                 is returned
    :param index: int, optional, if given only the kpoint set with the given index
                  is returned
    :param only_used: bool if True only the kpoint list used in the calculation is returned
    :param logger: logger object for logging warnings, errors

    :returns: list of tuples (index, label) for multiple kpoint sets a dict with the names containing
              the list of tuples is returned
    """

    if name is not None and index is not None:
        raise ValueError('Only provide one of index or name to select kpoint lists')

    if only_used and (name is not None or index is not None):
        raise ValueError('Either use only_used=False and provide the name/index or use only_used=True. Not both')

    with FleurXMLContext(xmltree, schema_dict, logger=logger) as root:

        if only_used:
            name = root.attribute('listName')

        filters: FilterType = {}
        if name is not None:
            filters['kPointList'] = {'name': name}
        if index is not None:
            filters['kPointList'] = {'index': index + 1 if index >= 0 else index}

        if root.number_nodes('kPointList', contains='kPointLists', filters=filters) == 0:
            labels = root.attribute('name', tag_name='kPointList', contains='kPointLists', list_return=True)
            if only_used:
                raise ValueError(f'Found no Kpoint list with the name: {name}'
                                 f'Available list names: {labels}'
                                 'The listName attribute is not consistent with the rest of the input')
            if name is not None:
                raise ValueError(f'Found no Kpoint list with the name: {name}'
                                 f'Available list names: {labels}')
            raise ValueError('No Kpoint lists found in the given inp.xml, matching the criteria could be found'
                             f'Available list names: {labels}')

        special_kpoints = {}
        for kpointlist in root.iter('kPointList', contains='kPointLists', filters=filters):

            label = kpointlist.attribute('name')

            labelled_points = kpointlist.simple_xpath('kPoint',
                                                      filters={'kPoint': {
                                                          'label': {
                                                              '!=': ''
                                                          }
                                                      }},
                                                      list_return=True)

            #yapf: disable
            special_kpoints[label] = [
                (kpointlist.node.index(kpoint), str(kpoint.attrib['label'])) for kpoint in labelled_points  #type:ignore[union-attr]
            ]
            #yapf: enable

    if len(special_kpoints) == 1:
        _, special_kpoints = special_kpoints.popitem()  #type:ignore[assignment]

    return special_kpoints


@get_special_kpoints.register(max_version='0.31')
def get_special_kpoints_max4(
    xmltree: XMLLike,
    schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
    name: str | None = None,
    index: int | None = None,
    only_used: bool = False,
    logger: Logger | None = None,
) -> list[tuple[int, str]] | dict[str, list[tuple[int, str]]]:
    """
    Extract the labeled special kpoints from the given kpointlist

    .. warning::
        Only implemented for versions starting with Max5

    :param xmltree: etree representing the fleur xml file
    :param schema_dict: schema dictionary corresponding to the file version
                        of the xmltree
    :param name: str, optional, if given only the kpoint set with the given name
                 is returned
    :param index: int, optional, if given only the kpoint set with the given index
                  is returned
    :param only_used: bool if True only the kpoint list used in the calculation is returned
    :param logger: logger object for logging warnings, errors

    :returns: list of tuples (index, label) for multiple kpoint sets a dict with the names containing
              the list of tuples is returned
    """

    raise NotImplementedError(
        f"'get_special_kpoints' is not implemented for inputs of version '{schema_dict['inp_version']}'")


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

    with FleurXMLContext(xmltree, schema_dict, logger=logger) as root:

        if not root.tag_exists('relaxation'):
            raise ValueError('No relaxation information included in the given XML file')

        out_dict = {}
        with root.find('relaxation') as relax_tag:

            out_dict['displacements'] = relax_tag.text('displace', list_return=True)
            out_dict['energies'] = relax_tag.attribute('energy', list_return=True)
            out_dict['posforces'] = [step.text('posforce', list_return=True) for step in relax_tag.iter('step')]

    return out_dict


@get_relaxation_information.register(max_version='0.28')
def get_relaxation_information_pre029(xmltree: XMLLike,
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

    with FleurXMLContext(xmltree, schema_dict, logger=logger) as root:

        if not root.tag_exists('symmetryOperations'):
            raise ValueError('No explicit symmetry information included in the given XML file')

        rotations = []
        shifts = []
        for symop in root.iter('symOp'):
            row1 = symop.text('row-1')
            row2 = symop.text('row-2')
            row3 = symop.text('row-3')

            rot = np.array([row1[:3], row2[:3], row3[:3]]).astype(int)
            shift = np.array([row1[3], row2[3], row3[3]])

            rotations.append(rot)
            shifts.append(shift)

    return rotations, shifts
