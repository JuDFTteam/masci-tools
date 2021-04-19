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
This module contains functions to load an fleur out.xml file, parse it with a schema
and convert its content to a dict, based on the tasks given
"""
from masci_tools.util.parse_tasks import ParseTasks
from masci_tools.util.schema_dict_util import tag_exists, read_constants, eval_simple_xpath, evaluate_attribute
from masci_tools.util.xml.common_functions import eval_xpath, clear_xml, validate_xml
from masci_tools.io.parsers.fleur.fleur_schema.schema_dict import OutputSchemaDict
from masci_tools.util.logging_util import DictHandler, OutParserLogAdapter
from lxml import etree
import copy
import warnings
import logging


def outxml_parser(outxmlfile,
                  version=None,
                  parser_info_out=None,
                  iteration_to_parse=None,
                  strict=False,
                  debug=False,
                  **kwargs):
    """
    Parses the out.xml file to a dictionary based on the version and the given tasks

    :param outxmlfile: either path to the out.xml file, opened file handle or a xml etree to be parsed
    :param version: version string to enforce that a given schema is used
    :param parser_info_out: dict, with warnings, info, errors, ...
    :param iteration_to_parse: either str or int, (optional, default 'last')
                               determines which iteration should be parsed.
                               Accepted are 'all', 'first', 'last' or an index for the iteration
    :param strict: bool if True  and no parser_info_out is provided any encountered error will immediately be raised
    :param debug: bool if True additional information is printed out in the logs

    Kwargs:
        :param ignore_validation: bool, if True schema validation errors are only logged
        :param minimal_mode: bool, if True only total Energy, iteration number and distances are parsed
        :param list_return: bool, if True one-item lists in the output dict are not converted to simple values
        :param additional_tasks: dict to define custom parsing tasks. For detailed explanation
                                 See :py:mod:`~masci_tools.io.parsers.fleur.default_parse_tasks`.
        :param overwrite: bool, if True and keys in additional_tasks collide with defaults
                          The defaults will be overwritten
        :param append: bool, if True and keys in additional_tasks collide with defaults
                       The inner tasks will be written into the dict. If inner keys collide
                       they are overwritten

    :return: python dictionary with the information parsed from the out.xml

    :raises ValueError: If the validation against the schema failed, or an irrecoverable error
                        occured during parsing
    :raises FileNotFoundError: If no Schema file for the given version was found
    :raises KeyError: If an unknown task is encountered

    """

    __parser_version__ = '0.5.0'

    logger = logging.getLogger(__name__)

    parser_log_handler = None
    if parser_info_out is not None or not strict:
        if parser_info_out is None:
            parser_info_out = {}

        logging_level = logging.INFO
        if debug:
            logging_level = logging.DEBUG
        logger.setLevel(logging_level)

        parser_log_handler = DictHandler(parser_info_out,
                                         WARNING='parser_warnings',
                                         ERROR='parser_errors',
                                         INFO='parser_info',
                                         DEBUG='parser_debug',
                                         CRITICAL='parser_critical',
                                         ignore_unknown_levels=True,
                                         level=logging_level)

        logger.addHandler(parser_log_handler)

    if strict:
        logger = None

    if logger is not None:
        logger.info('Masci-Tools Fleur out.xml Parser v%s', __parser_version__)

    outfile_broken = False

    if isinstance(outxmlfile, etree._ElementTree):
        xmltree = outxmlfile
    else:
        parser = etree.XMLParser(attribute_defaults=True, recover=False, encoding='utf-8')

        try:
            xmltree = etree.parse(outxmlfile, parser)
        except etree.XMLSyntaxError:
            outfile_broken = True
            if logger is None:
                warnings.warn('The out.xml file is broken I try to repair it.')
            else:
                logger.warning('The out.xml file is broken I try to repair it.')

        if outfile_broken:
            # repair xmlfile and try to parse what is possible.
            parser = etree.XMLParser(attribute_defaults=True, recover=True, encoding='utf-8')
            try:
                xmltree = etree.parse(outxmlfile, parser)
            except etree.XMLSyntaxError:
                if logger is None:
                    raise
                else:
                    logger.exception('Skipping the parsing of the xml file. ' 'Repairing was not possible.')
                    return {}

    if version is None:
        out_version = eval_xpath(xmltree, '//@fleurOutputVersion', logger=logger)
        out_version = str(out_version)
        if out_version is None:
            logger.error('Failed to extract outputVersion')
            raise ValueError('Failed to extract outputVersion')
    else:
        out_version = version

    if out_version == '0.27':
        program_version = eval_xpath(xmltree, '//programVersion/@version', logger=logger)
        if program_version == 'fleur 32':
            #Max5 release (before bugfix)
            out_version = '0.33'
            inp_version = '0.33'
            ignore_validation = True
            if logger is not None:
                logger.warning("Ignoring '0.27' outputVersion for MaX5.0 release")
            else:
                warnings.warn("Ignoring '0.27' outputVersion for MaX5.0 release")
        elif program_version == 'fleur 31':
            #Max4 release
            out_version = '0.31'
            inp_version = '0.31'
            ignore_validation = True
            if logger is not None:
                logger.warning("Ignoring '0.27' outputVersion for MaX4.0 release")
            else:
                warnings.warn("Ignoring '0.27' outputVersion for MaX4.0 release")
        elif program_version == 'fleur 30':
            #Max3.1 release
            out_version = '0.30'
            inp_version = '0.30'
            ignore_validation = True
            if logger is not None:
                logger.warning("Ignoring '0.27' outputVersion for MaX3.1 release")
            else:
                warnings.warn("Ignoring '0.27' outputVersion for MaX3.1 release")
        elif program_version == 'fleur 27':
            #Max3.1 release
            out_version = '0.29'
            inp_version = '0.29'
            ignore_validation = True
            if logger is not None:
                logger.warning("Found version before MaX3.1 release falling back to file version '0.29'")
            warnings.warn(
                'out.xml files before the MaX3.1 release are not explicitely supported.'
                ' No guarantee is given that the parser will work without error', UserWarning)
        else:
            if logger is not None:
                logger.error("Unknown fleur version: File-version '%s' Program-version '%s'", out_version,
                             program_version)
            raise ValueError(f"Unknown fleur version: File-version '{out_version}' Program-version '{program_version}'")
    else:
        ignore_validation = False
        inp_version = eval_xpath(xmltree, '//@fleurInputVersion', logger=logger)
        inp_version = str(inp_version)
        if inp_version is None:
            if logger is not None:
                logger.error('Failed to extract inputVersion')
            raise ValueError('Failed to extract inputVersion')

    ignore_validation = kwargs.get('ignore_validation', ignore_validation)

    #Load schema_dict (inp and out)
    outschema_dict = OutputSchemaDict.fromVersion(out_version, inp_version=inp_version, logger=logger)

    if outschema_dict['out_version'] != out_version or \
       outschema_dict['inp_version'] != inp_version:
        ignore_validation = True
        out_version = outschema_dict['out_version']
        inp_version = outschema_dict['inp_version']

    if logger is not None:
        logger.info('Found fleur out file with the versions out: %s; inp: %s', out_version, inp_version)

    xmltree = clear_xml(xmltree)
    root = xmltree.getroot()

    errmsg = ''
    try:
        validate_xml(xmltree, outschema_dict.xmlschema, error_header='Output file does not validate against the schema')
    except etree.DocumentInvalid as err:
        errmsg = str(err)
        if logger is not None:
            logger.warning(errmsg)
        if not ignore_validation:
            if logger is not None:
                logger.exception(errmsg)
            raise ValueError(errmsg) from err

    if not outschema_dict.xmlschema.validate(xmltree) and errmsg == '':
        msg = 'Output file does not validate against the schema: Reason is unknown'
        if logger is not None:
            logger.warning(msg)
        if not ignore_validation:
            if logger is not None:
                logger.exception(msg)
            raise ValueError(msg)

    parser = ParseTasks(out_version)
    additional_tasks = kwargs.pop('additional_tasks', {})
    for task_name, task_definition in additional_tasks.items():
        parser.add_task(task_name, task_definition, **kwargs)

    out_dict, constants = parse_general_information(root,
                                                    parser,
                                                    outschema_dict,
                                                    logger=logger,
                                                    iteration_to_parse=iteration_to_parse,
                                                    **kwargs)

    # get all iterations in out.xml file
    iteration_nodes = eval_simple_xpath(root, outschema_dict, 'iteration', logger=logger, list_return=True)
    n_iters = len(iteration_nodes)

    # parse only last stable interation
    # (if modes (dos and co) maybe parse anyway if broken?)
    if outfile_broken and (n_iters >= 2):
        iteration_nodes = iteration_nodes[:-2]
        if logger is not None:
            logger.info('The last parsed iteration is %s', n_iters - 2)
    elif outfile_broken and (n_iters == 1):
        iteration_nodes = [iteration_nodes[0]]
        if logger is not None:
            logger.info('The last parsed iteration is %s', n_iters)
    elif not outfile_broken and (n_iters >= 1):
        pass
    else:  # there was no iteration found.
        # only the starting charge density could be generated
        msg = 'There was no iteration found in the outfile, either just a ' \
              'starting density was generated or something went wrong.'
        if logger is None:
            raise ValueError(msg)
        else:
            logger.error(msg)

    if iteration_to_parse is None:
        iteration_to_parse = 'last'  #This is the default from the aiida_fleur parser

    if iteration_to_parse == 'last':
        iteration_nodes = iteration_nodes[-1]
    elif iteration_to_parse == 'first':
        iteration_nodes = iteration_nodes[0]
    elif iteration_to_parse == 'all':
        pass
    elif isinstance(iteration_to_parse, int):
        try:
            iteration_nodes = iteration_nodes[iteration_to_parse]
        except IndexError as exc:
            if logger is not None:
                logger.exception(exc)
            raise ValueError(f"Invalid value for iteration_to_parse: Got '{iteration_to_parse}'"
                             f"; but only '{len(iteration_nodes)}' iterations are available") from exc
    else:
        if logger is not None:
            logger.error(
                "Invalid value for iteration_to_parse: Got '%s' "
                "Valid values are: 'first', 'last', 'all', or int", iteration_to_parse)
        raise ValueError(f"Invalid value for iteration_to_parse: Got '{iteration_to_parse}' "
                         "Valid values are: 'first', 'last', 'all', or int")

    if not isinstance(iteration_nodes, list):
        iteration_nodes = [iteration_nodes]

    logger_info = {'iteration': 'unknown'}
    iteration_logger = OutParserLogAdapter(logger, logger_info)

    for node in iteration_nodes:
        iteration_number = evaluate_attribute(node, outschema_dict, 'numberForCurrentRun', optional=True)

        if iteration_number is not None:
            logger_info['iteration'] = iteration_number

        out_dict = parse_iteration(node, parser, outschema_dict, out_dict, constants, logger=iteration_logger, **kwargs)

        logger_info['iteration'] = 'unknown'

    if not kwargs.get('list_return', False):
        #Convert one item lists to simple values
        for key, value in out_dict.items():
            if isinstance(value, list):
                if len(value) == 1:
                    out_dict[key] = value[0]
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, list):
                        if len(subvalue) == 1:
                            out_dict[key][subkey] = subvalue[0]

    if parser_log_handler is not None:
        if logger is not None:
            logger.removeHandler(parser_log_handler)

    return out_dict


def parse_general_information(root, parser, outschema_dict, logger, iteration_to_parse=None, **kwargs):
    """
    Parses the information from the out.xml outside scf iterations

    Also defined constants and fleur calculation modes are read in

    Args:
        :param root: etree Element for the root of the out.xml
        :param parser: ParseTasks object with all defined tasks
        :param outschema_dict: dict with the information parsed from the OutputSchema
        :param parser_info_out: dict, with warnings, info, errors, ...

    Kwargs:
        :param minimal_mode: bool, if True only total Energy, iteration number and distances are parsed

    """

    minimal_mode = kwargs.get('minimal_mode', False)
    if iteration_to_parse is None:
        iteration_to_parse = 'last'

    constants = read_constants(root, outschema_dict, logger=logger)

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
    fleurmode = parser.perform_task('fleur_modes',
                                    root,
                                    fleurmode,
                                    outschema_dict,
                                    constants,
                                    logger=logger,
                                    use_lists=False)

    if logger is not None:
        logger.info('The following Fleur modes were found: %s', fleurmode)

    parser.determine_tasks(fleurmode, minimal=minimal_mode)

    #For certain fleur modes we need to overwrite the tasks
    if fleurmode['dos'] or fleurmode['band']:
        parser.iteration_tasks = ['iteration_number', 'fermi_energy']
        if fleurmode['bz_integration'] == 'hist':
            parser.iteration_tasks = ['iteration_number', 'fermi_energy', 'bandgap']

    if fleurmode['relax'] and iteration_to_parse == 'last':
        if 'distances' in parser.iteration_tasks:
            parser.iteration_tasks.remove('distances')
        if 'magnetic_distances' in parser.iteration_tasks:
            parser.iteration_tasks.remove('magnetic_distances')

    if logger is not None:
        logger.debug('The following tasks are performed on the root: %s', parser.general_tasks)

    out_dict = {}

    for task in parser.general_tasks:

        if logger is not None:
            logger.debug('Performing task: %s', task)
        out_dict = parser.perform_task(task, root, out_dict, outschema_dict, constants, logger=logger, use_lists=False)

    return out_dict, constants


def parse_iteration(iteration_node, parser, outschema_dict, out_dict, constants, logger, **kwargs):
    """
    Parses an scf iteration node. Which tasks to perform is stored in parser.iteration_tasks

    Args:
        :param iteration_node: etree Element for a scf iteration
        :param parser: ParseTasks object with all defined tasks
        :param outschema_dict: dict with the information parsed form the OutputSchema
        :param out_dict: dict with the parsed results
        :param constants: dict with all the defined mathematical constants
        :param parser_info_out: dict, with warnings, info, errors, ...

    Kwargs:
        :param strict: bool, if True an error will be raised if an unknown task is encountered
                       otherwise a warning is written to parser_info_out
        :param minimal_mode: bool, if True only total Energy, iteration number and distances are parsed
    """

    minimal_mode = kwargs.get('minimal_mode', False)

    iteration_tasks = copy.deepcopy(parser.iteration_tasks)
    #If the iteration is a forcetheorem calculation
    #Replace all tasks with the given tasks for the calculation
    forcetheorem_tags = ['Forcetheorem_DMI', 'Forcetheorem_SSDISP', 'Forcetheorem_JIJ', 'Forcetheorem_MAE']
    for tag in forcetheorem_tags:
        exists = tag_exists(iteration_node, outschema_dict, tag)
        if exists:
            if minimal_mode:
                iteration_tasks = []
            else:
                iteration_tasks = [tag.lower()]
            break

    if logger is not None:
        logger.debug('The following tasks are performed for the iteration: %s', iteration_tasks)

    for task in iteration_tasks:

        if logger is not None:
            logger.debug('Performing task: %s', task)

        try:
            out_dict = parser.perform_task(task, iteration_node, out_dict, outschema_dict, constants, logger=logger)
        except KeyError:
            if logger is not None:
                logger.exception("Unknown task: '%s'. Skipping this one", task)
            raise

    return out_dict
