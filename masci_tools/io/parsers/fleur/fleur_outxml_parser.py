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
from __future__ import absolute_import
from .parse_tasks import ParseTasks
from masci_tools.util.xml.common_xml_util import eval_xpath, get_xml_attribute, clear_xml, convert_xml_attribute
import masci_tools.util.schema_dict_util as schema_util
from masci_tools.io.parsers.fleur.fleur_schema import load_inpschema, load_outschema
from masci_tools.io.common_functions import camel_to_snake
from masci_tools.util.fleur_outxml_conversions import calculate_walltime, convert_ldau_definitions
from masci_tools.util.fleur_outxml_conversions import convert_relax_info, convert_forces
from masci_tools.util.fleur_outxml_conversions import calculate_total_magnetic_moment
from lxml import etree


def outxml_parser(outxmlfile, version=None, parser_info_out=None, iteration_to_parse=None, **kwargs):
    """
    Parses the out.xml file to a dictionary based on the version and the given tasks

    :param outxmlfile: either path to the out.xml file or a xml etree to be parsed
    :param version: version string to enforce that a given schema is used
    :param parser_info_out: dict, with warnings, info, errors, ...
    :param iteration_to_parse: either str or int, (optional, default 'last')
                               determines which iteration should be parsed.
                               Accepted are 'all', 'first', 'last' or an index for the iteration

    Kwargs:
        :param strict: bool, if True an error will be raised if an unknown task is encountered
                       otherwise a warning is written to parser_info_out
        :param minimal_mode: bool, if True only total Energy, iteration number and distances are parsed
        :param additional_tasks: dict to define custom parsing tasks. For detailed explanation
                                 See :py:mod:`~masci_tools.io.parsers.fleur.default_parse_tasks`.
        :param overwrite: bool, if True and keys in additional_tasks collide with defaults
                          The defaults will be overwritten
        :param append: bool, if True and keys in additional_tasks collide with defaults
                       The inner tasks will be written into the dict. If inner keys collide
                       they are overwritten

    :return: python dictionary with the information parsed from the out.xml

    """

    if parser_info_out is None:
        parser_info_out = {'parser_warnings': [], 'fleur_modes': {}, 'debug_info': {}}

    parser_version = '0.1.0'
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

    xmltree = clear_xml(xmltree)
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

    parse_tasks = ParseTasks(version)
    additional_tasks = kwargs.pop('additional_tasks', {})
    for task_name, task_definition in additional_tasks.items():
        parse_tasks.add_task(task_name, task_definition, **kwargs)

    out_dict, fleurmode, constants = parse_general_information(root,
                                                               parse_tasks,
                                                               outschema_dict,
                                                               inpschema_dict,
                                                               parser_info_out=parser_info_out)

    # get all iterations in out.xml file
    iteration_xpath = schema_util.get_tag_xpath(outschema_dict, 'iteration')
    iteration_nodes = eval_xpath(root, iteration_xpath, parser_info_out=parser_info_out, list_return=True)
    n_iters = len(iteration_nodes)

    # parse only last stable interation
    # (if modes (dos and co) maybe parse anyway if broken?)
    if outfile_broken and (n_iters >= 2):
        iteration_nodes = iteration_nodes[:-2]
        parser_info_out['last_iteration_parsed'] = n_iters - 2
    elif outfile_broken and (n_iters == 1):
        iteration_nodes = iteration_nodes[0]
        parser_info_out['last_iteration_parsed'] = n_iters
    elif not outfile_broken and (n_iters >= 1):
        iteration_nodes = iteration_nodes
    else:  # there was no iteration found.
        # only the starting charge density could be generated
        parser_info_out['parser_warnings'].append('There was no iteration found in the outfile, either just a '
                                                  'starting density was generated or something went wrong.')
        iteration_nodes = None

    if iteration_to_parse is None:
        iteration_to_parse = 'last'  #This is the default from the aiida_fleur parser

    if iteration_to_parse == 'last':
        iteration_nodes = iteration_nodes[-1]
    elif iteration_to_parse == 'first':
        iteration_nodes = iteration_nodes[0]
    elif iteration_to_parse == 'all':
        iteration_nodes = iteration_nodes
    elif isinstance(iteration_to_parse, int):
        iteration_nodes = iteration_nodes[iteration_to_parse]
    else:
        raise ValueError(f"Invalid value for iteration_to_parse: Got '{iteration_to_parse}' "
                         "Valid values are: 'first', 'last', 'all', or int")

    if not isinstance(iteration_nodes, list):
        iteration_nodes = [iteration_nodes]

    for node in iteration_nodes:
        print(node)
        out_dict = parse_iteration(node,
                                   parse_tasks,
                                   fleurmode,
                                   outschema_dict,
                                   out_dict,
                                   constants,
                                   parser_info_out=parser_info_out,
                                   **kwargs)

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


def parse_general_information(root, parse_tasks, outschema_dict, inpschema_dict, parser_info_out=None):
    """
    Parses the information from teh out.xml outside scf iterations

    Also defined constants and fleur calculation modes are read in

    Args:
        :param root: etree Element for the root of the out.xml
        :param parse_tasks: ParseTasks object with all defined tasks
        :param outschema_dict: dict with the information parsed from the OutputSchema
        :param inpschema_dict: dict with the information parsed from the InputSchema
        :param parser_info_out: dict, with warnings, info, errors, ...

    """

    root_tag = '/fleurOutput'
    constants = schema_util.read_constants(root, inpschema_dict, abspath=root_tag)

    fleurmode = {
        'jspin': 1,
        'relax': False,
        'ldau': False,
        'soc': False,
        'noco': False,
        'film': False,
        'dos': False,
        'band': False
    }
    fleurmode = parse_task(parse_tasks['fleur_modes'],
                           root,
                           fleurmode,
                           inpschema_dict,
                           constants,
                           parser_info_out,
                           root_tag=root_tag,
                           use_lists=False)
    parser_info_out['fleur_modes'] = fleurmode

    out_dict = {}
    out_dict = parse_task(parse_tasks['general_inp_info'],
                          root,
                          out_dict,
                          inpschema_dict,
                          constants,
                          parser_info_out,
                          root_tag=root_tag,
                          use_lists=False)

    out_dict = parse_task(parse_tasks['general_out_info'],
                          root,
                          out_dict,
                          outschema_dict,
                          constants,
                          parser_info_out,
                          use_lists=False)

    #Convert the read in times/dates to a walltime
    out_dict = calculate_walltime(out_dict, parser_info_out)

    if fleurmode['ldau']:
        out_dict = parse_task(parse_tasks['ldau_info'],
                              root,
                              out_dict,
                              inpschema_dict,
                              constants,
                              parser_info_out,
                              root_tag=root_tag)
        out_dict = convert_ldau_definitions(out_dict)

    if fleurmode['relax']:

        out_dict['film'] = fleurmode['film']

        if fleurmode['film']:
            out_dict = parse_task(parse_tasks['film_relax_info'],
                                  root,
                                  out_dict,
                                  inpschema_dict,
                                  constants,
                                  parser_info_out,
                                  root_tag=root_tag,
                                  use_lists=False)
        else:
            out_dict = parse_task(parse_tasks['bulk_relax_info'],
                                  root,
                                  out_dict,
                                  inpschema_dict,
                                  constants,
                                  parser_info_out,
                                  root_tag=root_tag,
                                  use_lists=False)

        out_dict = convert_relax_info(out_dict)

    return out_dict, fleurmode, constants


def parse_iteration(iteration_node,
                    parse_tasks,
                    fleurmode,
                    outschema_dict,
                    out_dict,
                    constants,
                    parser_info_out=None,
                    **kwargs):
    """
    Parses an scf iteration node.

    First the necessary tasks are determined according to the fleurmodes.
    The each task is performed

    Args:
        :param iteration_node: etree Element for a scf iteration
        :param parse_tasks: ParseTasks object with all defined tasks
        :param fleurmode: dict with the fleur claculation modes (DOS, magnetic, ...)
        :param outschema_dict: dict with the information parsed form the OutputSchema
        :param out_dict: dict with the parsed results
        :param constants: dict with all the defined mathematical constants
        :param parser_info_out: dict, with warnings, info, errors, ...

    Kwargs:
        :param strict: bool, if True an error will be raised if an unknown task is encountered
                       otherwise a warning is written to parser_info_out
        :param minimal_mode: bool, if True only total Energy, iteration number and distances are parsed
    """

    strict = kwargs.get('strict', False)
    minimal_mode = kwargs.get('minimal_mode', False)
    debug = kwargs.get('debug', False)

    #These are the default things to be parsed for all iterations
    iteration_tasks = [
        'iteration_number', 'total_energy', 'distances', 'total_energy_contributions', 'fermi_energy', 'bandgap',
        'charges'
    ]

    iteration_tasks_forcetheorem = []

    #Mode specific tasks
    if fleurmode['jspin'] == 2:
        iteration_tasks.append('magnetic_moments')

    if fleurmode['soc'] and fleurmode['jspin'] == 2:
        iteration_tasks.append('orbital_magnetic_moments')

    if fleurmode['ldau']:
        iteration_tasks.append('ldau_energy_correction')
        iteration_tasks.append('nmmp_distances')

    if fleurmode['relax']:
        iteration_tasks.append('forces')

    if minimal_mode:
        iteration_tasks = ['iteration_number', 'total_energy', 'distances']

    if fleurmode['jspin'] == 2:
        iteration_tasks.append('magnetic_distances')

    if fleurmode['dos'] or fleurmode['band']:
        iteration_tasks = ['iteration_number', 'fermi_energy', 'bandgap']

    #If the iteration is a forcetheorem calculation
    #Replace all tasks with the given tasks for the calculation
    forcetheorem_tags = ['Forcetheorem_DMI', 'Forcetheorem_SSDISP', 'Forcetheorem_JIJ', 'Forcetheorem_MAE']
    for tag in forcetheorem_tags:
        exists = schema_util.tag_exists(iteration_node, outschema_dict, tag)
        if exists:
            if minimal_mode:
                iteration_tasks = []
            else:
                iteration_tasks = [tag.lower()]
            break

    if debug:
        parser_info_out['debug_info']['iteration_tasks'] = iteration_tasks

    for task in iteration_tasks:
        try:
            out_dict = parse_task(parse_tasks[task], iteration_node, out_dict, outschema_dict, constants,
                                  parser_info_out)
        except KeyError:
            parser_info_out['parser_warnings'].append(f"Unknown task: '{task}'. Skipping this one")
            if strict:
                raise

    if fleurmode['relax']:  #This is too complex to put it into the standard tasks for now
        out_dict = convert_forces(out_dict)

    if 'charges' in iteration_tasks:
        out_dict = calculate_total_magnetic_moment(out_dict)

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
        'parentAttribs': schema_util.evaluate_parent_tag,
    }

    for task_key, spec in tasks_definition.items():

        action = _FUNCTION_DICT[spec['parse_type']]
        args = spec['path_spec'].copy()

        if spec['parse_type'] in ['attrib', 'text', 'singleValue', 'allAttribs', 'parentAttribs']:
            args['constants'] = constants

        if root_tag is not None:
            args['abspath'] = root_tag

        if 'only' in spec and spec['parse_type'] == 'parentAttribs':
            args['only'] = spec['only']

        parsed_dict = out_dict
        if 'subdict' in spec:
            parsed_dict = out_dict.get(spec['subdict'], {})

        parsed_value = action(node, schema_dict, parser_info_out=parser_info_out, **args)

        if isinstance(parsed_value, dict):

            if spec['parse_type'] == 'singleValue':
                base_value = 'value'
                no_list = ['units']
                ignore = ['comment']
                flat = True
            elif spec['parse_type'] in ['allAttribs', 'parentAttribs']:
                base_value = spec.get('base_value', '')
                ignore = spec.get('ignore', [])
                no_list = spec.get('overwrite', [])
                flat = spec.get('flat', True)

            if flat:
                for key, val in parsed_value.items():

                    if key in ignore or val is None:
                        continue

                    if key == base_value:
                        current_key = task_key
                    else:
                        current_key = f'{task_key}_{camel_to_snake(key)}'

                    if current_key not in parsed_dict and use_lists:
                        parsed_dict[current_key] = []

                    if key in no_list or not use_lists:
                        parsed_dict[current_key] = val
                    else:
                        parsed_dict[current_key].append(val)

            else:
                for key, val in list(parsed_value.items()):
                    parsed_value.pop(key)
                    if not key in ignore:
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
