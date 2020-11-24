# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools    #
# For further information on the license, see the LICENSE.txt file            #
# For further information please visit http://www.flapw.de or                 #
#                                                                             #
###############################################################################
"""
This module contains functions to load an fleur out.xml file, parse it with a schema
and convert its content to a dict, based on the tasks given
"""
from masci_tools.util.xml.common_xml_util import eval_xpath, get_xml_attribute, clear_xml, convert_xml_attribute
from masci_tools.util.schema_dict_util import *
from masci_tools.io.parsers.fleur.fleur_schema import load_inpschema, load_outschema
from datetime import date
from lxml import etree


def outxml_parser(outxmlfile,
                  version=None,
                  parser_info_out=None,
                  iteration_to_parse=None,
                  overwrite_tasks=None,
                  additional_tasks=None):

    if parser_info_out is None:
        parser_info_out = {'parser_warnings': [], 'fleur_modes': {}}

    parser_version = '0.0.1'
    parser_info_out['parser_info'] = f'Masci-Tools Fleur out.xml Parser v{parser_version}'

    outfile_broken = False
    parse_xml = True
    if isinstance(outxmlfile, str):
        parser = etree.XMLParser(attribute_defaults=True, recover=False, encoding='utf-8')

        try:
            xmltree = etree.parse(outxmlfile, parser)
        except etree.XMLSyntaxError:
            outfile_broken = True
            parser_info_out['parser_warnings'].append('The out.xml file is broken I try to repair it.')

        if outfile_broken:
            # repair xmlfile and try to parse what is possible.
            parser = etree.XMLParser(attribute_defaults=True, recover=True, encoding='utf-8')
            try:
                xmltree = etree.parse(outxmlfile, parser)
            except etree.XMLSyntaxError:
                parse_xml = False
                parser_info_out['parser_warnings'].append('Skipping the parsing of the xml file. '
                                                          'Repairing was not possible.')
    else:
        xmltree = outxmlfile

    if not parse_xml:
        return {}


    if version is None:
        try:
            root = xmltree.getroot()
            version = root.attrib['fleurOutputVersion']
        except KeyError:
            raise ValueError('Failed to extract outputVersion')

    #Load schema_dict (inp and out)
    inpschema_dict = load_inpschema(version)
    outschema_dict, outxmlschema = load_outschema(version, schema_return=True)

    xmltree = clear_xml(xmltree, schema_dict=inpschema_dict)
    root = xmltree.getroot()

    if not outxmlschema.validate(xmltree):
        # get more information on what does not validate
        parser_on_fly = etree.XMLParser(attribute_defaults=True, schema=outxmlschema, encoding='utf-8')
        outxmlfile = etree.tostring(xmltree)
        message = 'Reason is unknown'
        try:
            tree_x = etree.fromstring(outxmlfile, parser_on_fly)
        except etree.XMLSyntaxError as msg:
            message = msg
        raise ValueError(f'Output file does not validate against the schema: {message}')

    if iteration_to_parse is None:
        iteration_to_parse = 'last'  #This is the default from the aiida_fleur parser

    iteration_base_xpath = get_tag_xpath(outschema_dict, 'iteration')

    if iteration_to_parse == 'last':
        iteration_xpath = f'{iteration_base_xpath}[last()]'
    elif iteration_to_parse == 'first':
        iteration_xpath = f'{iteration_base_xpath}[1]'
    elif iteration_to_parse == 'all':
        iteration_xpath = iteration_base_xpath
    elif isinstance(iteration_to_parse, int):
        if iteration_to_parse < 0:
            raise ValueError('Invalid value for iteration_to_parse: Has to be positive or 0')
        iteration_xpath = f'{iteration_base_xpath}[{iteration_to_parse}]'
    else:
        raise ValueError(f"Invalid value for iteration_to_parse: Got '{iteration_to_parse}' "
                          "Valid values are: 'first', 'last', 'all', or int")

    out_dict, fleurmode, constants = parse_general_information(root,
                                                               outschema_dict,
                                                               inpschema_dict,
                                                               parser_info_out=parser_info_out)

    parser_info_out['fleur_modes'] = fleurmode

    for iteration in eval_xpath(root, iteration_xpath, parser_info_out=parser_info_out, list_return=True):
        out_dict = parse_iteration(iteration,
                                   fleurmode,
                                   outschema_dict,
                                   out_dict,
                                   constants,
                                   overwrite_tasks=overwrite_tasks,
                                   additional_tasks=additional_tasks,
                                   parser_info_out=parser_info_out)

    #Convert energy to eV
    htr = 27.21138602
    if 'energy_hartree' in out_dict:
        out_dict['energy'] = [e*htr for e in out_dict['energy_hartree']]
        out_dict['energy_units'] = 'eV'

    for key, value in out_dict.items():
        if isinstance(value, list):
            if len(value) == 1:
                out_dict[key] = value[0]
        elif isinstance(value, dict):
            for subkey, subvalue in value.items():
                if isinstance(subvalue, list):
                    if len(subvalue) == 1:
                        out_dict[key][subkey] = subvalue[0]

    return out_dict


def parse_general_information(root, outschema_dict, inpschema_dict, parser_info_out=None):

    #General switches determining how to parse the output
    fleurmode_info = {
        'jspin': ('attrib', {
            'name': 'jspins'
        }),
        'relax': ('attrib', {
            'name': 'l_f'
        }),
        'ldau': ('exists', {
            'name': 'ldaU',
            'contains': 'species'
        }),
        'soc': ('attrib', {
            'name': 'l_soc'
        }),
        'noco': ('attrib', {
            'name': 'l_noco'
        }),
        'film': ('exists', {
            'name': 'filmPos'
            })
    }

    general_out_info = {
        'creator_name': ('attrib', {
            'name': 'version',
            'not_contains': 'git'
        }),
        'creator_target_architecture': ('text', {
            'name': 'targetComputerArchitectures'
        }),
        'creator_target_structure': ('text', {
            'name': 'targetStructureClass'
        }),
        'output_file_version': ('attrib', {
            'name': 'fleurOutputVersion'
        }),
        'number_of_iterations': ('numberNodes', {
            'name': 'iteration'
        }),
        'number_of_atoms': ('attrib', {
            'name': 'nat'
        }),
        'number_of_atom_types': ('attrib', {
            'name': 'ntype'
        })
    }

    general_inp_info = {
        'title': ('text', {
            'name': 'comment'
        }),
        'kmax': ('attrib', {
            'name': 'Kmax'
        }),
        'gmax': ('attrib', {
            'name': 'Gmax'
        }),
        'number_of_spin_components': ('attrib', {
            'name': 'jspins'
        }),
        'number_of_symmetries': ('numberNodes', {
            'name': 'symOp'
        }),
        'number_of_species': ('numberNodes', {
            'name': 'species'
        })
    }

    function_dict = {
        'attrib': evaluate_attribute,
        'text': evaluate_text,
        'exists': tag_exists,
        'numberNodes': get_number_of_nodes,
        'singleValue': evaluate_single_value_tag,
    }

    root_tag = '/fleurOutput'

    constants = read_constants(root, inpschema_dict, abspath=root_tag)

    fleurmode = {'jspin': 1, 'relax': False, 'ldau': False, 'soc': False, 'noco': False, 'film': False}

    for key, spec in fleurmode_info.items():
        action = function_dict[spec[0]]
        spec[1]['abspath'] = root_tag
        if spec[0] in ['attrib', 'text']:
            spec[1]['constants'] = constants
        value = action(root, inpschema_dict, parser_info_out=parser_info_out, **spec[1])
        if value is not None:  #Don't overwrite defaults if there was no value
            fleurmode[key] = value

    out_dict = {}
    for key, spec in general_inp_info.items():
        action = function_dict[spec[0]]
        spec[1]['abspath'] = root_tag
        if spec[0] in ['attrib', 'text']:
            spec[1]['constants'] = constants
        out_dict[key] = action(root, inpschema_dict, parser_info_out=parser_info_out, **spec[1])

    for key, spec in general_out_info.items():
        action = function_dict[spec[0]]
        if spec[0] in ['attrib', 'text']:
            spec[1]['constants'] = constants
        out_dict[key] = action(root, outschema_dict, parser_info_out=parser_info_out, **spec[1])

    # time
    # Maybe change the behavior if things could not be parsed...
    # Especially if file was broken, ie endtime it not there.
    starttime = evaluate_attribute(root,
                                   outschema_dict,
                                   'time',
                                   constants,
                                   contains='start',
                                   parser_info_out=parser_info_out)
    if starttime is not None:
        starttimes = starttime.split(':')
    else:
        starttimes = [0, 0, 0]
        msg = 'Startime was unparsed, inp.xml prob not complete, do not believe the walltime!'
        parser_info_out['parser_warnings'].append(msg)

    endtime = evaluate_attribute(root,
                                 outschema_dict,
                                 'time',
                                 constants,
                                 contains='end',
                                 parser_info_out=parser_info_out)
    if endtime is not None:
        endtimes = endtime.split(':')
    else:
        endtimes = [0, 0, 0]
        msg = 'Endtime was unparsed, inp.xml prob not complete, do not believe the walltime!'
        parser_info_out['parser_warnings'].append(msg)
    start_date = evaluate_attribute(root,
                                    outschema_dict,
                                    'date',
                                    constants,
                                    contains='start',
                                    parser_info_out=parser_info_out)
    end_date = evaluate_attribute(root,
                                  outschema_dict,
                                  'date',
                                  constants,
                                  contains='end',
                                  parser_info_out=parser_info_out)

    offset = 0
    if start_date != end_date:
        # date="2018/01/15", Can this fail? what happens if not there
        if start_date and end_date:
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
    out_dict['start_date'] = {'date': start_date, 'time': starttime}
    out_dict['end_date'] = {'date': end_date, 'time': endtime}

    if fleurmode['ldau']:
        out_dict['ldau_info'] = {}

        ldau_tag_path = get_tag_xpath(inpschema_dict, 'ldaU', contains='species')
        ldau_tag_info = inpschema_dict['tag_info'][ldau_tag_path]
        ldau_tag_path = f'{root_tag}{ldau_tag_path}'
        ldaU_definitions = eval_xpath(root, ldau_tag_path)

        for ldaU in ldaU_definitions:
            parent = ldaU.getparent()
            element_z = get_xml_attribute(parent, 'atomicNumber')
            species_name = get_xml_attribute(parent, 'name')
            ldauKey = f'{species_name}/{element_z}'

            if ldauKey not in out_dict['ldau_info']:
                out_dict['ldau_info'][ldauKey] = {}

            new_ldau = {}
            for attrib in ldau_tag_info['attribs']:
                possible_types = inpschema_dict['attrib_types'][attrib]
                if attrib not in ldaU.attrib:
                    continue

                warnings = []
                new_ldau[attrib.lower()], suc = convert_xml_attribute(ldaU.attrib[attrib],
                                                                      possible_types,
                                                                      constants,
                                                                      conversion_warnings=warnings)

                if not suc:
                    parser_info_out['parser_warnings'].append(f'Failed to evaluate attribute {attrib}: '
                                                              'Below are the warnings from convert_xml_attribute')
                    for warning in warnings:
                        parser_info_out['parser_warnings'].append(warning)

            #Convert orbital number and double counting to more readable values
            orbital = 'spdf'[new_ldau['l']]
            if new_ldau['l_amf']:
                new_ldau['double_counting'] = 'AMF'
            else:
                new_ldau['double_counting'] = 'FLL'
            new_ldau.pop('l_amf')
            new_ldau.pop('l')
            out_dict['ldau_info'][ldauKey][orbital] = new_ldau

    return out_dict, fleurmode, constants


def parse_iteration(iteration,
                    fleurmode,
                    outschema_dict,
                    out_dict,
                    constants,
                    overwrite_tasks=None,
                    additional_tasks=None,
                    parser_info_out=None):

    #The task definition dictionary maps all the keys in the out_dict to the right function call
    #to obtain them from the out.xml

    function_dict = {
        'attrib': evaluate_attribute,
        'text': evaluate_text,
        'exists': tag_exists,
        'numberNodes': get_number_of_nodes,
        'singleValue': evaluate_single_value_tag,
    }

    tasks_definition = {}
    tasks_definition['total_energy'] = {'energy_hartree': ('singleValue', {'name': 'totalEnergy'})}

    tasks_definition['total_energy_contributions'] = {
        'sum_of_eigenvalues': ('singleValue', {
            'name': 'sumOfEigenvalues'
        }),
        'energy_core_electrons': ('singleValue', {
            'name': 'coreElectrons'
        }),
        'energy_valence_electrons': ('singleValue', {
            'name': 'valenceElectrons'
        }),
        'charge_den_xc_den_integral': ('singleValue', {
            'name': 'chargeDenXCDenIntegral'
        }),
    }

    tasks_definition['ldau_energy_correction'] = {
            'ldau_energy_correction': ('singleValue', {
                'name': 'dftUCorrection'
            }, 'ldau_info')
    }

    tasks_definition['nmmp_distances'] = {
            'density_matrix_distance': ('attrib', {
                'name': 'distance',
                'contains': 'ldaUDensityMatrixConvergence'
            }, 'ldau_info')
    }

    tasks_definition['fermi_energy'] = {'fermi_energy': ('singleValue', {'name': 'FermiEnergy'})}
    tasks_definition['bandgap'] = {'bandgap': ('singleValue', {'name': 'bandgap'})}

    if fleurmode['jspin'] == 1:
        tasks_definition['distances'] = {}
    else:
        tasks_definition['distances'] = {}

    #These are the default things to be parsed for all iterations
    iteration_tasks_all = ['total_energy' , 'distances']

    #These are the default things to be parsed for the last iteration (atm they just overwrite the value)
    iteration_tasks_last = [
        'total_energy_contributions',
        'fermi_energy',
        'bandgap',
    ]

    iteration_tasks_forcetheorem = []

    #Mode specific tasks
    if fleurmode['jspin'] == 2:
        pass
        #iteration_tasks_last.append('magnetic_moments')

    if fleurmode['soc']:
        pass
        #iteration_tasks_last.append('orbital_magnetic_moments')

    if fleurmode['ldau']:
        iteration_tasks_last.append('ldau_energy_correction')
        iteration_tasks_all.append('nmmp_distances')

    #Check if this is a Forcetheorem iteration

    if 'overallNumber' in iteration.attrib:
        out_dict['number_of_iterations_total'] = int(iteration.attrib['overallNumber'])

    for task in iteration_tasks_all:
        for key, spec in tasks_definition[task].items():

            action = function_dict[spec[0]]

            if spec[0] in ['attrib', 'text', 'singleValue']:
                spec[1]['constants'] = constants

            subkey = None
            if len(spec) == 3:
                subkey = spec[2]

            if subkey is not None:
                if subkey not in out_dict:
                    out_dict[subkey] = {}
            else:
                if key not in out_dict:
                    out_dict[key] = []

            value = None
            unit = None
            if spec[0] == 'singleValue':
                value, unit = action(iteration, outschema_dict, parser_info_out=parser_info_out, **spec[1])
            else:
                value = action(iteration, outschema_dict, parser_info_out=parser_info_out, **spec[1])

            if subkey is not None:
                if key not in out_dict[subkey]:
                    out_dict[subkey][key] = []
                if value is not None:
                    out_dict[subkey][key].append(value)
                if unit is not None:
                    out_dict[subkey][f'{key}_units'] = unit
            else:
                if value is not None:
                    out_dict[key].append(value)
                if unit is not None:
                    out_dict[f'{key}_units'] = unit




    for task in iteration_tasks_last:
        for key, spec in tasks_definition[task].items():

            action = function_dict[spec[0]]

            if spec[0] in ['attrib', 'text', 'singleValue']:
                spec[1]['constants'] = constants

            subkey = None
            if len(spec) == 3:
                subkey = spec[2]

            if subkey is not None:
                if subkey not in out_dict:
                    out_dict[subkey] = {}

            value = None
            unit = None
            if spec[0] == 'singleValue':
                value, unit = action(iteration, outschema_dict, parser_info_out=parser_info_out, **spec[1])
            else:
                value = action(iteration, outschema_dict, parser_info_out=parser_info_out, **spec[1])

            if subkey is not None:
                if value is not None:
                    out_dict[subkey][key] = value
                if unit is not None:
                    out_dict[subkey][f'{key}_units'] = unit
            else:
                if value is not None:
                    out_dict[key] = value
                if unit is not None:
                    out_dict[f'{key}_units'] = unit

    if fleurmode['relax']:  #This is too complex to put it into the standard tasks for now
        pass

    return out_dict
