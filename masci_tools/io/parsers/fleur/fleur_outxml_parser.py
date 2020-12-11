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
from masci_tools.util.xml.common_xml_util import eval_xpath, get_xml_attribute, clear_xml, convert_xml_attribute, read_constants
import masci_tools.util.schema_dict_util as schema_util
from masci_tools.io.parsers.fleur.fleur_schema import load_inpschema, load_outschema
from masci_tools.io.common_functions import camel_to_snake
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

    out_dict, fleurmode, constants = parse_general_information(root,
                                                               outschema_dict,
                                                               inpschema_dict,
                                                               parser_info_out=parser_info_out)

    if iteration_to_parse is None:
        iteration_to_parse = 'last'  #This is the default from the aiida_fleur parser

    iteration_base_xpath = schema_util.get_tag_xpath(outschema_dict, 'iteration')

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
        if out_dict['energy_hartree'] is not None:
            out_dict['energy'] = [e * htr for e in out_dict['energy_hartree']]
        else:
            out_dict['energy'] = None
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
        'jspin': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'jspins'
            }
        },
        'relax': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'l_f'
            }
        },
        'ldau': {
            'parse_type': 'exists',
            'path_spec': {
                'name': 'ldaU',
                'contains': 'species'
            }
        },
        'soc': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'l_soc'
            }
        },
        'noco': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'l_noco'
            }
        },
        'film': {
            'parse_type': 'exists',
            'path_spec': {
                'name': 'filmPos'
            }
        }
    }

    general_out_info = {
        'creator_name': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'version',
                'not_contains': 'git'
            }
        },
        'creator_target_architecture': {
            'parse_type': 'text',
            'path_spec': {
                'name': 'targetComputerArchitectures'
            }
        },
        'creator_target_structure': {
            'parse_type': 'text',
            'path_spec': {
                'name': 'targetStructureClass'
            }
        },
        'output_file_version': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'fleurOutputVersion'
            }
        },
        'number_of_iterations': {
            'parse_type': 'numberNodes',
            'path_spec': {
                'name': 'iteration'
            }
        },
        'number_of_atoms': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'nat'
            }
        },
        'number_of_atom_types': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'ntype'
            }
        },
        'start_date': {
            'parse_type': 'allAttribs',
            'path_spec': {
                'name': 'startDateAndTime'
            },
            'ignore': ['zone'],
            'flat': False,
        },
        'end_date': {
            'parse_type': 'allAttribs',
            'path_spec': {
                'name': 'endDateAndTime'
            },
            'ignore': ['zone'],
            'flat': False,
        }
    }

    general_inp_info = {
        'title': {
            'parse_type': 'text',
            'path_spec': {
                'name': 'comment'
            }
        },
        'kmax': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'Kmax'
            }
        },
        'gmax': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'Gmax'
            }
        },
        'number_of_spin_components': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'jspins'
            }
        },
        'number_of_symmetries': {
            'parse_type': 'numberNodes',
            'path_spec': {
                'name': 'symOp'
            }
        },
        'number_of_species': {
            'parse_type': 'numberNodes',
            'path_spec': {
                'name': 'species'
            }
        }
    }

    ldau_info = {
        'parsed_ldau': {
            'parse_type': 'allAttribs',
            'path_spec': {
                'name': 'ldaU',
                'contains': 'species'
            },
            'subdict': 'ldau_info',
        }
    }

    root_tag = '/fleurOutput'
    constants = read_constants(root, inpschema_dict, abspath=root_tag)

    fleurmode = {'jspin': 1, 'relax': False, 'ldau': False, 'soc': False, 'noco': False, 'film': False}
    fleurmode = parse_task(fleurmode_info,
                           root,
                           fleurmode,
                           inpschema_dict,
                           constants,
                           parser_info_out,
                           root_tag=root_tag,
                           use_lists=False)
    parser_info_out['fleur_modes'] = fleurmode

    out_dict = {}
    out_dict = parse_task(general_inp_info,
                          root,
                          out_dict,
                          inpschema_dict,
                          constants,
                          parser_info_out,
                          root_tag=root_tag,
                          use_lists=False)

    out_dict = parse_task(general_out_info, root, out_dict, outschema_dict, constants, parser_info_out, use_lists=False)

    #Convert the read in times/dates to a walltime
    out_dict = calculate_walltime(out_dict, parser_info_out)

    if fleurmode['ldau']:
        out_dict['ldau_info'] = {}

        ldau_tag_path = schema_util.get_tag_xpath(inpschema_dict, 'ldaU', contains='species')
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

    tasks_definition = {}

    tasks_definition['iteration_number'] = {
        'number_of_iterations_total': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'overallNumber'
            },
            'overwrite_last': True,
        }
    }

    tasks_definition['total_energy'] = {
        'energy_hartree': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'totalEnergy'
            }
        },
    }

    tasks_definition['total_energy_contributions'] = {
        'sum_of_eigenvalues': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'sumOfEigenvalues'
            }
        },
        'energy_core_electrons': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'coreElectrons'
            }
        },
        'energy_valence_electrons': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'valenceElectrons'
            }
        },
        'charge_den_xc_den_integral': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'chargeDenXCDenIntegral'
            }
        },
    }

    tasks_definition['ldau_energy_correction'] = {
        'ldau_energy_correction': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'dftUCorrection'
            },
            'subdict': 'ldau_info'
        },
    }

    tasks_definition['nmmp_distances'] = {
        'density_matrix_distance': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'distance',
                'contains': 'ldaUDensityMatrixConvergence'
            },
            'subdict': 'ldau_info'
        },
    }

    tasks_definition['fermi_energy'] = {
        'fermi_energy': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'FermiEnergy'
            },
        }
    }
    tasks_definition['bandgap'] = {
        'bandgap': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'bandgap'
            },
        }
    }

    tasks_definition['magnetic_moments'] = {
        'magnetic_moments': {
            'parse_type': 'allAttribs',
            'path_spec': {
                'name': 'magneticMoment'
            },
            'base_value': 'moment',
            'ignore': ['atomType']
        }
    }

    tasks_definition['orbital_magnetic_moments'] = {
        'orbital_magnetic_moments': {
            'parse_type': 'allAttribs',
            'path_spec': {
                'name': 'orbMagMoment'
            },
            'base_value': 'moment',
            'ignore': ['atomType']
        }
    }

    tasks_definition['forcetheorem_dmi'] = {
        'force_dmi': {
            'parse_type': 'allAttribs',
            'path_spec': {
                'name': 'Entry',
                'contains': 'DMI'
            }
        },
        'force_dmi_qs': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'qpoints',
                'contains': 'Forcetheorem_DMI'
            }
        },
        'force_dmi_angles': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'Angles',
                'contains': 'Forcetheorem_DMI'
            }
        }
    }

    if fleurmode['jspin'] == 1:
        tasks_definition['distances'] = {}
    else:
        tasks_definition['distances'] = {}

    #These are the default things to be parsed for all iterations
    iteration_tasks = [
        'iteration_number', 'total_energy', 'distances', 'total_energy_contributions', 'fermi_energy', 'bandgap'
    ]

    iteration_tasks_forcetheorem = []

    #Mode specific tasks
    if fleurmode['jspin'] == 2:
        iteration_tasks.append('magnetic_moments')

    if fleurmode['soc']:
        iteration_tasks.append('orbital_magnetic_moments')

    if fleurmode['ldau']:
        iteration_tasks.append('ldau_energy_correction')
        iteration_tasks.append('nmmp_distances')

    #TODO: Check if this is a Forcetheorem iteration

    forcetheorem_tags = ['Forcetheorem_DMI', 'Forcetheorem_SSDISP', 'Forcetheorem_JIJ', 'Forcetheorem_MAE']
    for tag in forcetheorem_tags:
        exists = schema_util.tag_exists(iteration, outschema_dict, tag)
        if exists:
            iteration_tasks = [tag.lower()]
            break

    for task in iteration_tasks:
        try:
            definition = tasks_definition[task]
            out_dict = parse_task(definition, iteration, out_dict, outschema_dict, constants, parser_info_out)
        except KeyError:
            parser_info_out['parser_warnings'].append(f"Unknown task: '{task}'. Skipping this one")

    if fleurmode['relax']:  #This is too complex to put it into the standard tasks for now
        pass

    return out_dict


def parse_task(tasks_definition,
               node,
               out_dict,
               schema_dict,
               constants,
               parser_info_out,
               root_tag=None,
               use_lists=True):
    """
    Evaluates the task given in the tasks_definition dict

    :param task_definition: dict, specifies what should be parsed (explanation below)
    :param node: etree.Element, the xpath expressions are evaluated from this node
    :param out_dict: dict, output will be put in this dictionary
    :param schema_dict: dict, here all paths and attributes are stored according to the
                        outputschema
    :param constants: dict with all the defined mathematical constants
    :param parser_info_out: dict, with warnings, info, errors, ...
    :param root_tag: str, this string will be appended in front of any xpath before it is evaluated
    :param use_lists: bool, if True lists are created for each key if not otherwise specified


    Each entry in the task_definition dict will be parsed and inserted into the same key in
    the output dict

    The following keys are expected in each entry of the task_definition dictionary:
        :param parse_type: str, defines which methods to use when extracting the information
        :param path_spec: dict with all the arguments that should be passed to get_tag_xpath
                          or get_attrib_xpath to get the correct path
        :param subdict: str, if present the parsed values are put into this key in the output dictionary
        :param overwrite_last: bool, if True no list is inserted and each entry overwrites the last

    For the allAttribs parse_type there are more keys that can appear:
        :param base_value: str, optional. If given the attribute
                           with this name will be inserted into the key from the task_definition
                           all other keys are formatted as {task_key}_{attribute_name}
        :param ignore: list of str, these attributes will be ignored
        :param overwrite: list of str, these attributes will not create a list and overwrite any value
                          that might be there
        :param flat: bool, if False the dict parsed from the tag is inserted as a dict into the correspondin key
                           if True the values will be extracted and put into the output dictionary with the
                           format {task_key}_{attribute_name}

    """

    _FUNCTION_DICT = {
        'attrib': schema_util.evaluate_attribute,
        'text': schema_util.evaluate_text,
        'exists': schema_util.tag_exists,
        'numberNodes': schema_util.get_number_of_nodes,
        'singleValue': schema_util.evaluate_single_value_tag,
        'allAttribs': schema_util.evaluate_tag,
    }

    for task_key, spec in tasks_definition.items():

        action = _FUNCTION_DICT[spec['parse_type']]
        args = spec['path_spec'].copy()

        if spec['parse_type'] in ['attrib', 'text', 'singleValue', 'allAttribs']:
            args['constants'] = constants

        if root_tag is not None:
            args['abspath'] = root_tag

        parsed_dict = out_dict
        if 'subdict' in spec:
            parsed_dict = out_dict.get(spec['subdict'], {})

        parsed_value = action(node, schema_dict, parser_info_out=parser_info_out, **args)

        if 'process_function' in spec:
            parsed_value = spec['process_function'](parsed_value, parser_info_out=parser_info_out)

        if isinstance(parsed_value, dict):

            if spec['parse_type'] == 'singleValue':
                base_value = 'value'
                no_list = ['units']
                ignore = ['comment']
                flat = True
            elif spec['parse_type'] == 'allAttribs':
                base_value = spec.get('base_value', '')
                ignore = spec.get('ignore', [])
                no_list = spec.get('overwrite', [])
                flat = spec.get('flat', True)

            if flat:
                for key, val in parsed_value.items():
                    if key in ignore:
                        continue

                    if val is None:
                        continue

                    if key == base_value:
                        current_key = task_key
                    else:
                        current_key = f'{task_key}_{camel_to_snake(key)}'

                    if current_key not in parsed_dict and use_lists:
                        parsed_dict[current_key] = []

                    if key in no_list:
                        parsed_dict[current_key] = val
                    else:
                        if use_lists:
                            parsed_dict[current_key].append(val)
                        else:
                            parsed_dict[current_key] = val
            else:
                for key, val in list(parsed_value.items()):
                    if key in ignore:
                        parsed_value.pop(key)
                    else:
                        parsed_value.pop(key)
                        parsed_value[camel_to_snake(key)] = val

                parsed_dict[task_key] = parsed_value

        else:
            if task_key not in parsed_dict and use_lists:
                parsed_dict[task_key] = []
            overwrite = spec.get('overwrite_last', False)
            if parsed_value is not None:
                if use_lists and not overwrite:
                    parsed_dict[task_key].append(parsed_value)
                else:
                    parsed_dict[task_key] = parsed_value

        if 'subdict' in spec:
            out_dict[spec['subdict']] = parsed_dict
        else:
            out_dict = parsed_dict

    return out_dict


def calculate_walltime(out_dict, parser_info_out=None):
    """
    Convert the times
    """
    print(out_dict)
    if parser_info_out is None:
        parser_info_out = {'parser_warnings': []}

    if out_dict['start_date']['time'] is not None:
        starttimes = out_dict['start_date']['time'].split(':')
    else:
        starttimes = [0, 0, 0]
        msg = 'Starttime was unparsed, inp.xml prob not complete, do not believe the walltime!'
        parser_info_out['parser_warnings'].append(msg)

    if out_dict['end_date']['time'] is not None:
        endtimes = out_dict['end_date']['time'].split(':')
    else:
        endtimes = [0, 0, 0]
        msg = 'Endtime was unparsed, inp.xml prob not complete, do not believe the walltime!'
        parser_info_out['parser_warnings'].append(msg)

    if out_dict['start_date']['date'] is not None:
        start_date = out_dict['start_date']['date']
    else:
        starttimes = [0, 0, 0]
        msg = 'Startdate was unparsed, inp.xml prob not complete, do not believe the walltime!'
        parser_info_out['parser_warnings'].append(msg)

    if out_dict['end_date']['date'] is not None:
        end_date = out_dict['end_date']['date']
    else:
        starttimes = [0, 0, 0]
        msg = 'Enddate was unparsed, inp.xml prob not complete, do not believe the walltime!'
        parser_info_out['parser_warnings'].append(msg)

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

    return out_dict
