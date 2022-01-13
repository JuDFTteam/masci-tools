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
from __future__ import annotations

from masci_tools.util.parse_tasks import ParseTasks
from masci_tools.util.schema_dict_util import tag_exists, read_constants, eval_simple_xpath, evaluate_attribute
from masci_tools.util.xml.common_functions import clear_xml, validate_xml
from masci_tools.io.io_fleurxml import load_outxml
from masci_tools.util.logging_util import DictHandler, OutParserLogAdapter
from masci_tools.io.parsers.fleur_schema import OutputSchemaDict
from masci_tools.util.typing import XMLFileLike
from lxml import etree
import copy
import warnings
import logging
from typing import Any, Iterable
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  #type:ignore


def outxml_parser(outxmlfile: XMLFileLike,
                  parser_info_out: dict[str, Any] | None = None,
                  iteration_to_parse: Literal['all', 'last', 'first'] | int = 'last',
                  minimal_mode: bool = False,
                  additional_tasks: dict[str, dict[str, Any]] | None = None,
                  optional_tasks: Iterable[str] | None = None,
                  overwrite: bool = False,
                  append: bool = False,
                  list_return: bool = False,
                  strict: bool = False,
                  debug: bool = False,
                  ignore_validation: bool = False,
                  base_url: str | None = None) -> dict[str, Any]:
    """
    Parses the out.xml file to a dictionary based on the version and the given tasks

    :param outxmlfile: either path to the out.xml file, opened file handle or a xml etree to be parsed
    :param parser_info_out: dict, with warnings, info, errors, ...
    :param iteration_to_parse: either str or int, (optional, default 'last')
                               determines which iteration should be parsed.
                               Accepted are 'all', 'first', 'last' or an index for the iteration
    :param minimal_mode: bool, if True only total Energy, iteration number and distances are parsed
    :param additional_tasks: dict to define custom parsing tasks. For detailed explanation
                             See :py:mod:`~masci_tools.io.parsers.fleur.default_parse_tasks`.
    :param overwrite: bool, if True and keys in additional_tasks collide with defaults
                      The defaults will be overwritten
    :param append: bool, if True and keys in additional_tasks collide with defaults
                   The inner tasks will be written into the dict. If inner keys collide
                   they are overwritten
    :param optional_tasks: Iterable of strings, defines additional tasks to perform.
                           See :py:mod:`~masci_tools.io.parsers.fleur.default_parse_tasks` for examples.
    :param list_return: bool, if True one-item lists in the output dict are not converted to simple values
    :param strict: bool if True  and no parser_info_out is provided any encountered error will immediately be raised
    :param debug: bool if True additional information is printed out in the logs
    :param ignore_validation: bool, if True schema validation errors are only logged

    :return: python dictionary with the information parsed from the out.xml

    :raises ValueError: If the validation against the schema failed, or an irrecoverable error
                        occured during parsing
    :raises FileNotFoundError: If no Schema file for the given version was found
    :raises KeyError: If an unknown task is encountered
    """

    __parser_version__ = '0.6.0'

    logger: logging.Logger | None = logging.getLogger(__name__)
    if strict:
        logger = None

    parser_log_handler = None
    if logger is not None:
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

    if logger is not None:
        logger.info('Masci-Tools Fleur out.xml Parser v%s', __parser_version__)

    outfile_broken = False
    try:
        xmltree, outschema_dict = load_outxml(outxmlfile, logger=logger, base_url=base_url, recover=False)
    except ValueError as err:
        if 'Failed to parse output file' in str(err):
            outfile_broken = True
            if logger is None:
                warnings.warn('The out.xml file is broken I try to repair it.')
            else:
                logger.warning('The out.xml file is broken I try to repair it.')
        else:
            if logger is not None:
                logger.error(str(err))
            raise

    if outfile_broken:
        try:
            xmltree, outschema_dict = load_outxml(outxmlfile, logger=logger, base_url=base_url, recover=True)
        except ValueError as err:
            if 'Failed to parse output file' in str(err):
                if logger is None:
                    raise ValueError('Skipping the parsing of the xml file. Repairing was not possible.') from err
                logger.exception('Skipping the parsing of the xml file. Repairing was not possible.')
                return {}
            if logger is not None:
                logger.error(str(err))
            raise

    actual_out_version = evaluate_attribute(xmltree, outschema_dict, 'fleurOutputVersion', logger=logger)
    if actual_out_version == '0.27':
        actual_inp_version = actual_out_version
    else:
        actual_inp_version = evaluate_attribute(xmltree, outschema_dict, 'fleurInputVersion', logger=logger)

    out_version = actual_out_version
    inp_version = actual_inp_version
    if outschema_dict['out_version'] != actual_out_version or \
       outschema_dict['inp_version'] != actual_inp_version:
        ignore_validation = True
        out_version = outschema_dict['out_version']
        inp_version = outschema_dict['inp_version']

    if logger is not None:
        logger.info('Found fleur out file with the versions out: %s; inp: %s', out_version, inp_version)

    xmltree, _ = clear_xml(xmltree)
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

    if not outschema_dict.xmlschema.validate(xmltree) and errmsg == '':  #type:ignore
        msg = 'Output file does not validate against the schema: Reason is unknown'
        if logger is not None:
            logger.warning(msg)
        if not ignore_validation:
            if logger is not None:
                logger.exception(msg)
            raise ValueError(msg)

    parser = ParseTasks(out_version)
    if additional_tasks is None:
        additional_tasks = {}
    for task_name, task_definition in additional_tasks.items():
        parser.add_task(task_name, task_definition, overwrite=overwrite, append=append)

    out_dict, constants = parse_general_information(root,
                                                    parser,
                                                    outschema_dict,
                                                    logger=logger,
                                                    iteration_to_parse=iteration_to_parse,
                                                    minimal_mode=minimal_mode,
                                                    optional_tasks=optional_tasks)

    out_dict['input_file_version'] = outschema_dict['inp_version']
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
        logger.error(msg)

    if iteration_to_parse == 'last':
        iteration_nodes = [iteration_nodes[-1]]
    elif iteration_to_parse == 'first':
        iteration_nodes = [iteration_nodes[0]]
    elif iteration_to_parse == 'all':
        pass
    elif isinstance(iteration_to_parse, int):
        try:
            iteration_nodes = [iteration_nodes[iteration_to_parse]]
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

    logger_info = {'iteration': 'unknown'}
    iteration_logger: logging.LoggerAdapter | None = None
    if logger is not None:
        iteration_logger = OutParserLogAdapter(logger, logger_info)

    for node in iteration_nodes:
        iteration_number = evaluate_attribute(node, outschema_dict, 'numberForCurrentRun', optional=True)

        if iteration_number is not None:
            logger_info['iteration'] = iteration_number

        out_dict = parse_iteration(node,
                                   parser,
                                   outschema_dict,
                                   out_dict,
                                   constants,
                                   logger=iteration_logger,
                                   minimal_mode=minimal_mode)

        logger_info['iteration'] = 'unknown'

    if not list_return:
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


def parse_general_information(root: etree._Element, parser: ParseTasks, outschema_dict: OutputSchemaDict,
                              logger: logging.Logger | None,
                              iteration_to_parse: (Literal['all', 'last', 'first'] | int), minimal_mode: bool,
                              optional_tasks: Iterable[str] | None) -> tuple[dict[str, Any], dict[str, float]]:
    """
    Parses the information from the out.xml outside scf iterations

    Also defined constants and fleur calculation modes are read in

    :param root: etree Element for the root of the out.xml
    :param parser: ParseTasks object with all defined tasks
    :param outschema_dict: dict with the information parsed from the OutputSchema
    :param parser_info_out: dict, with warnings, info, errors, ...
    :param minimal_mode: bool, if True only total Energy, iteration number and distances are parsed
    :param optional_tasks: Iterable of strings, defines additional tasks to perform.
                           See :py:mod:`~masci_tools.io.parsers.fleur.default_parse_tasks` for examples.
    """
    from masci_tools.util.xml.xml_getters import get_fleur_modes

    constants = read_constants(root, outschema_dict, logger=logger)
    if logger is not None:
        logger.info('The following defined constants were found: %s', constants)

    fleurmode = get_fleur_modes(root, outschema_dict, logger=logger)
    if logger is not None:
        logger.info('The following Fleur modes were found: %s', fleurmode)

    parser.determine_tasks(fleurmode, minimal=minimal_mode, optional_tasks=optional_tasks)

    #For certain fleur modes we need to overwrite the tasks
    if fleurmode['dos'] or fleurmode['band'] or fleurmode['cf_coeff']:
        parser.iteration_tasks = ['iteration_number', 'fermi_energy']
        if fleurmode['bz_integration'] == 'hist':
            parser.iteration_tasks = ['iteration_number', 'fermi_energy', 'bandgap']

    if fleurmode['plot']:
        parser.iteration_tasks = []  #In this case there are multiple possibilities where fleur terminates
        #So we discard all the iteration tasks

    if fleurmode['relax'] and iteration_to_parse == 'last':
        if 'distances' in parser.iteration_tasks:
            parser.iteration_tasks.remove('distances')
        if 'magnetic_distances' in parser.iteration_tasks:
            parser.iteration_tasks.remove('magnetic_distances')
        if 'nmmp_distances' in parser.iteration_tasks:
            parser.iteration_tasks.remove('nmmp_distances')

    if logger is not None:
        logger.debug('The following tasks are performed on the root: %s', parser.general_tasks)

    out_dict = {'fleur_modes': fleurmode}

    for task in parser.general_tasks:

        if logger is not None:
            logger.debug('Performing task: %s', task)
        out_dict = parser.perform_task(task, root, out_dict, outschema_dict, constants, logger=logger, use_lists=False)

    return out_dict, constants


def parse_iteration(iteration_node: etree._Element, parser: ParseTasks, outschema_dict: OutputSchemaDict,
                    out_dict: dict[str, Any], constants: dict[str, float], logger: logging.LoggerAdapter | None,
                    minimal_mode: bool) -> dict[str, Any]:
    """
    Parses an scf iteration node. Which tasks to perform is stored in parser.iteration_tasks

    :param iteration_node: etree Element for a scf iteration
    :param parser: ParseTasks object with all defined tasks
    :param outschema_dict: dict with the information parsed form the OutputSchema
    :param out_dict: dict with the parsed results
    :param constants: dict with all the defined mathematical constants
    :param parser_info_out: dict, with warnings, info, errors, ...
    :param minimal_mode: bool, if True only total Energy, iteration number and distances are parsed
    """

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
