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
from functools import partial

from masci_tools.util.xml.common_functions import clear_xml
from masci_tools.util.xml.converters import convert_str_version_number
from masci_tools.util.xml import xml_getters
from masci_tools.util.xml.xpathbuilder import FilterType
from masci_tools.util.parse_utils import Conversion
from masci_tools.io.fleur_xml import FleurXMLContext, load_outxml_and_check_for_broken_xml, _EvalContext
from masci_tools.util.logging_util import DictHandler, OutParserLogAdapter
from masci_tools.util.typing import XMLFileLike
import copy
import warnings
import logging
from typing import Any, Callable, Iterable, TypeVar
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  #type:ignore
import sys
if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

__all__ = ('outxml_parser', 'conversion_function', 'register_migration')


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

    :param outxmlfile: either path to the out.xml file, opened file handle (in bytes modes i.e. rb)
                       or a xml etree to be parsed
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
                        occurred during parsing
    :raises FileNotFoundError: If no Schema file for the given version was found
    :raises KeyError: If an unknown task is encountered
    """

    __parser_version__ = '0.7.0'

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

    try:
        xmltree, schema_dict, outfile_broken = load_outxml_and_check_for_broken_xml(outxmlfile,
                                                                                    logger=logger,
                                                                                    base_url=base_url)
    except ValueError as err:
        if logger is not None:
            logger.error(str(err))
        if 'Skipping the parsing of the XML file' in str(err):
            return {}
        raise
    xmltree, _ = clear_xml(xmltree)

    with FleurXMLContext(xmltree, schema_dict, logger=logger) as root:

        out_version = root.attribute('fleurOutputVersion')
        if out_version == '0.27':
            inp_version = out_version
        else:
            inp_version = root.attribute('fleurInputVersion')

        if schema_dict['out_version'] != out_version or \
           schema_dict['inp_version'] != inp_version:
            ignore_validation = True
            out_version = schema_dict['out_version']
            inp_version = schema_dict['inp_version']

        if logger is not None:
            logger.info('Found fleur out file with the versions out: %s; inp: %s', out_version, inp_version)

        try:
            schema_dict.validate(xmltree, logger=logger)
        except ValueError as err:
            if not ignore_validation:
                if logger is not None:
                    logger.exception(err)
                raise

        parser = _TaskParser(out_version)
        if additional_tasks is None:
            additional_tasks = {}
        for task_name, task_definition in additional_tasks.items():
            parser.add_task(task_name, task_definition, overwrite=overwrite, append=append)

        if logger is not None:
            logger.info('The following defined constants were found: %s', root.constants)

        fleur_modes = xml_getters.get_fleur_modes(xmltree, schema_dict, logger=logger)
        if logger is not None:
            logger.info('The following Fleur modes were found: %s', fleur_modes)
        parser.determine_tasks(fleur_modes, optional_tasks, minimal=minimal_mode, iteration_to_parse=iteration_to_parse)

        out_dict = {'input_file_version': schema_dict['inp_version'], 'fleur_modes': fleur_modes}
        if logger is not None:
            logger.debug('The following tasks are performed on the root: %s', parser.general_tasks)
        for task in parser.general_tasks:

            if logger is not None:
                logger.debug('Performing task: %s', task)
            out_dict = parser.perform_task(task, root, out_dict, use_lists=False)

        iteration_filter = _determine_iteration_condition(iteration_to_parse, root.number_nodes('iteration'),
                                                          outfile_broken, logger)

        logger_info: dict[str, Any] = {}
        iteration_logger: logging.LoggerAdapter | None = None
        if logger is not None:
            iteration_logger = OutParserLogAdapter(logger, logger_info)

        for iteration in root.iter('iteration', filters=iteration_filter):
            iteration.logger = iteration_logger  #type:ignore[assignment] #TODO: Should this be allowed to be overwritten in iter?
            logger_info['iteration'] = iteration.attribute('numberForCurrentRun', default='unknown')

            iteration_tasks = parser.iteration_tasks
            #If the iteration is a forcetheorem calculation
            #Replace all tasks with the given tasks for the calculation
            forcetheorem_tags = ['Forcetheorem_DMI', 'Forcetheorem_SSDISP', 'Forcetheorem_JIJ', 'Forcetheorem_MAE']
            for tag in forcetheorem_tags:
                if iteration.tag_exists(tag):
                    if minimal_mode:
                        iteration_tasks = []
                    else:
                        iteration_tasks = [tag.lower()]
                    break

            if iteration.logger is not None:
                iteration.logger.debug('The following tasks are performed for the iteration: %s', iteration_tasks)

            for task in iteration_tasks:

                if iteration.logger is not None:
                    iteration.logger.debug('Performing task: %s', task)

                try:
                    out_dict = parser.perform_task(task, iteration, out_dict)
                except KeyError:
                    if logger is not None:
                        logger.exception("Unknown task: '%s'. Skipping this one", task)
                    raise

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


def _determine_iteration_condition(iteration_to_parse: Literal['all', 'first', 'last'] | int, n_iters: int,
                                   broken: bool, logger: logging.Logger | None) -> FilterType:
    """
    Determine which iterations should be parsed
    If the XML file is broken the last stable iteration is parsed if possible

    :param iteration_to_parse: either str or int, (optional, default 'last')
                               determines which iteration should be parsed.
                               Accepted are 'all', 'first', 'last' or an index for the iteration
    :param n_iters: How many iterations are in the file
    :param broken: if True the last iteration is assumed to be broken
    :param logger: logger for warnings
    """
    if n_iters == 0:
        # there was no iteration found.
        # only the starting charge density could be generated
        msg = 'There was no iteration found in the outfile, either just a ' \
              'starting density was generated or something went wrong.'
        if logger is None:
            raise ValueError(msg)
        logger.error(msg)
        return {}

    if logger is not None and broken and n_iters == 1:
        logger.info('The last parsed iteration is %s', n_iters)

    index_condition: int | dict[str, int] | None = None
    if iteration_to_parse == 'last':
        index_condition = -1
        if broken and n_iters >= 2:
            index_condition = -2
            if logger is not None:
                logger.info('The last parsed iteration is %s', n_iters - 2)
    elif iteration_to_parse == 'first':
        index_condition = 1
    elif isinstance(iteration_to_parse, int):
        if iteration_to_parse >= n_iters or iteration_to_parse < -n_iters:
            if logger is not None:
                logger.error("Invalid value for iteration_to_parse: Got '%s'", iteration_to_parse)
            raise ValueError(f"Invalid value for iteration_to_parse: Got '{iteration_to_parse}'"
                             f"; but only '{n_iters}' iterations are available")
        index_condition = iteration_to_parse if iteration_to_parse < 0 else iteration_to_parse + 1  #1-based indexing in XPaths
    elif iteration_to_parse == 'all':
        if broken and n_iters >= 2:
            index_condition = {'<=': -2}
            if logger is not None:
                logger.info('The last parsed iteration is %s', n_iters - 2)
    else:
        if logger is not None:
            logger.error(
                "Invalid value for iteration_to_parse: Got '%s' "
                "Valid values are: 'first', 'last', 'all', or int", iteration_to_parse)
        raise ValueError(f"Invalid value for iteration_to_parse: Got '{iteration_to_parse}' "
                         "Valid values are: 'first', 'last', 'all', or int")

    filters = {}
    if index_condition is not None:
        filters['iteration'] = {'index': index_condition}
    return filters


MigrationDict: TypeAlias = "dict[str, dict[str, Literal['compatible'] | Callable]]"
"""
Type describing the dictionary defining the migration pathways
"""


def _find_migration(start: str, target: str, migrations: MigrationDict) -> list[Callable] | None:
    """
    Tries to find a migration path from the start to the target version
    via the defined migration functions

    :param start: str of the starting version
    :param target: str of the target version
    :param migrations: dict of funcs registered via the register_migration_function decorator

    :returns: list of migration functions to be called to go from start to target
    """

    if start == target:
        return []

    if start not in migrations:
        return None

    possible_migrations = migrations[start]
    if target in possible_migrations:
        migration = possible_migrations[target]
        if isinstance(migration, str) and migration == 'compatible':
            return []
        return [migration]

    for migrated_version, migration in possible_migrations.items():
        new_call_list = _find_migration(migrated_version, target, migrations)
        if new_call_list is None:
            #Cannot migrate to target from this version
            continue

        if isinstance(migration, str) and migration == 'compatible':
            call_list = []
        else:
            call_list = [migration]
        call_list += new_call_list
        return call_list
    return None


class _TaskParser:
    """
    Representation of all known parsing tasks for the out.xml file

    When set up it will initialize the known default tasks and check if they work
    for the given output version

    Accessing definition of task example

    .. code-block:: python

        from masci_tools.io.parsers.fleur.fleur_outxml_parser import _TaskParser

        p = _TaskParser('0.33')
        totE_definition = p.tasks['total_energy']
    """

    PARSE_FUNCTIONS = {
        'attrib', 'text', 'allAttribs', 'parentAttribs', 'singleValue', 'exists', 'attrib_exists', 'numberNodes'
    }
    ALL_ATTRIBS_FUNCTIONS = {'allAttribs', 'parentAttribs', 'singleValue'}

    CONTROL_KEYS = {'_general', '_modes', '_minimal', '_special', '_conversions', '_optional', '_minimum_version'}
    REQUIRED_KEYS = {'parse_type'}
    REQUIRED_KEYS_XML_GETTER = {'parse_type', 'name'}
    REQUIRED_KEYS_UTIL = {'parse_type', 'path_spec'}
    ALLOWED_KEYS = {'parse_type', 'path_spec', 'subdict', 'overwrite_last', 'force_list', 'kwargs'}
    ALLOWED_KEYS_ALLATTRIBS = {'parse_type', 'path_spec', 'subdict', 'base_value', 'overwrite', 'flat', 'kwargs'}
    ALLOWED_KEYS_XML_GETTER = {'parse_type', 'name', 'kwargs', 'result_names'}

    _version = '0.4.0'
    migrations: MigrationDict = {}
    conversion_functions: dict[str, Callable] = {}

    def __init__(self, version: str, validate_defaults: bool = False) -> None:
        """
        Initialize the default parse tasks
        Terminates if the version is not marked as working with the default tasks

        :param version: str of the wanted output version
        :param task_file: optional, file to override default_parse_tasks
        :param validate_defaults: bool, if True all tasks from the default tasks
                                  are added one by one and are checked for
                                  inconsistent keys
        """
        from . import default_parse_tasks as tasks

        self.iteration_tasks: list[str] = []
        self.general_tasks: list[str] = []
        self.version = convert_str_version_number(version)

        tasks_dict: dict[str, dict[str, Any]] = copy.deepcopy(tasks.TASKS_DEFINITION)  #type: ignore[arg-type]
        if validate_defaults:
            #Manually add each task to make sure that there are no typos/inconsitencies in the keys
            self.tasks = {}
            for task_name, task in tasks_dict.items():
                self.add_task(task_name, task)
        else:
            self.tasks = tasks_dict

        working: set[str] = tasks.__working_out_versions__
        #Look if the base version is compatible if not look for a migration
        if version not in working:

            working_version_tuples = {convert_str_version_number(v) for v in working}
            if all(working_version < self.version for working_version in working_version_tuples):
                warnings.warn(
                    f"Output version '{version}' is not explicitly stated as 'working'\n"
                    'with the current version of the outxml_parser.\n'
                    'Since the given version is newer than the latest working version\n'
                    'I will continue. Errors and warnings can occur!', UserWarning)
            else:
                base: str = tasks.__base_version__
                migration_list = _find_migration(base, version, self.migrations)

                if migration_list is None:
                    raise ValueError(f'Unsupported output version: {version}')

                for migration in migration_list:
                    self.tasks = migration(self.tasks)

    @property
    def optional_tasks(self) -> set[str]:
        """
        Return a set of the available optional defined tasks
        """
        return {key for key, val in self.tasks.items() if val.get('_optional', False)}

    def add_task(self,
                 task_name: str,
                 task_definition: dict[str, Any],
                 append: bool = False,
                 overwrite: bool = False) -> None:
        """
        Add a new task definition to the tasks dictionary

        Will first check if the definition has all the required keys

        :param task_name: str, key in the tasks dict
        :param task_definition: dict with the defined tasks
        :param overwrite: bool (optional), if True and the key is present in the dictionary it will be
                          overwritten with the new definition
        :param append: bool (optional), if True and the key is present in the dictionary the new definitions
                       will be inserted into this dictionary (inner keys WILL BE OVERWRITTEN). Additionally
                       if an inner key is overwritten with an empty dict the inner key will be removed

        The following keys are expected in each entry of the task_definition dictionary:
            :param parse_type: str, defines which methods to use when extracting the information
            :param path_spec: dict with all the arguments that should be passed to tag_xpath
                              or attrib_xpath to get the correct path
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

        if task_name in self.tasks and not (append or overwrite):
            raise ValueError(f"Task '{task_name}' is already defined."
                             'Use append=True to append them (conflicting keys are overwritten)'
                             'or overwrite=True to remove all existing tasks')

        for task_key, definition in task_definition.items():

            if task_key.startswith('_'):
                if task_key not in self.CONTROL_KEYS:
                    raise ValueError(f'Unknown control key: {task_key}')
                continue

            task_keys = set(definition.keys())

            if not task_keys and task_key in self.tasks[task_name]:
                continue

            parse_type = definition['parse_type']
            if parse_type not in self.PARSE_FUNCTIONS | {'xmlGetter'}:
                raise ValueError(f'Unknown parse_type: {parse_type}')

            required = self.REQUIRED_KEYS
            allowed = self.ALLOWED_KEYS
            if parse_type == 'xmlGetter':
                required = required | self.REQUIRED_KEYS_XML_GETTER
                allowed = self.ALLOWED_KEYS_XML_GETTER
            else:
                required = required | self.REQUIRED_KEYS_UTIL
                if parse_type in self.ALL_ATTRIBS_FUNCTIONS:
                    allowed = self.ALLOWED_KEYS_ALLATTRIBS

            missing_required = required.difference(task_keys)
            if missing_required:
                raise ValueError(f'Reqired Keys missing: {missing_required}')

            extra_keys = task_keys.difference(allowed)
            if extra_keys:
                raise ValueError(f'Got extra Keys: {extra_keys}')

        if append:
            self.tasks.setdefault(task_name, {})
            for key, definition in task_definition.items():
                if definition:
                    self.tasks[task_name][key] = definition
                elif key in self.tasks[task_name]:
                    self.tasks[task_name].pop(key)
        else:
            self.tasks[task_name] = task_definition

    def determine_tasks(self,
                        fleurmodes: dict[str, Any],
                        optional_tasks: Iterable[str] | None = None,
                        minimal: bool = False,
                        iteration_to_parse: Literal['all', 'last', 'first'] | int = 'last') -> None:
        """
        Determine, which tasks to perform based on the fleur_modes

        :param fleurmodes: dict with the calculation modes
        :param minimal: bool, whether to only perform minimal tasks
        """

        if optional_tasks is None:
            optional_tasks = set()

        unknown = {name for name in optional_tasks if name not in self.optional_tasks}
        if unknown:
            raise ValueError(f"Unknown optional task(s): '{unknown}'\n"
                             f'The following are available: {self.optional_tasks}')

        for task_name, definition in self.tasks.items():

            if '_minimum_version' in definition:
                min_version = convert_str_version_number(definition['_minimum_version'])
                if self.version < min_version:
                    continue

            optional = definition.get('_optional', False)
            if optional and task_name not in optional_tasks:
                continue

            if minimal and not definition.get('_minimal', False):
                continue

            #These tasks are always added manually
            if definition.get('_special', False):
                continue

            requirements = definition.get('_modes', [])
            check = [fleurmodes[mode] == required_value for mode, required_value in requirements]
            if not all(check):
                continue

            if definition.get('_general', False):
                self.general_tasks.append(task_name)
            else:
                self.iteration_tasks.append(task_name)

        #Manual overrides for certain fleur modes
        if fleurmodes['dos'] or fleurmodes['band'] or fleurmodes['cf_coeff']:
            self.iteration_tasks = ['iteration_number', 'fermi_energy']
            if fleurmodes['bz_integration'] == 'hist':
                self.iteration_tasks = ['iteration_number', 'fermi_energy', 'bandgap']

        if fleurmodes['plot']:
            self.iteration_tasks = []  #In this case there are multiple possibilities where fleur terminates
            #So we discard all the iteration tasks

        if fleurmodes['relax'] and iteration_to_parse == 'last':
            if 'distances' in self.iteration_tasks:
                self.iteration_tasks.remove('distances')
            if 'magnetic_distances' in self.iteration_tasks:
                self.iteration_tasks.remove('magnetic_distances')
            if 'nmmp_distances' in self.iteration_tasks:
                self.iteration_tasks.remove('nmmp_distances')

    def perform_task(self, task_name: str, context: _EvalContext, out_dict: dict, use_lists: bool = True) -> dict:
        """
        Evaluates the task given in the tasks_definition dict

        :param task_name: str, specifies the task to perform
        :param node: etree.Element, the xpath expressions are evaluated from this node
        :param out_dict: dict, output will be put in this dictionary
        :param schema_dict: dict, here all paths and attributes are stored according to the
                            outputschema
        :param constants: dict with all the defined mathematical constants
        :param logger: logger object for logging warnings, errors
        :param root_tag: str, this string will be appended in front of any xpath before it is evaluated
        :param use_lists: bool, if True lists are created for each key if not otherwise specified

        """
        from masci_tools.io.common_functions import camel_to_snake

        #TODO: Could be moved into _EvalContext.__getitem__
        parse_functions = {
            'attrib': context.attribute,
            'text': context.text,
            'allAttribs': context.all_attributes,
            'parentAttribs': context.parent_attributes,
            'singleValue': context.single_value,
            'exists': context.tag_exists,
            'attrib_exists': context.attribute_exists,
            'numberNodes': context.number_nodes
        }

        try:
            tasks_definition = self.tasks[task_name]
        except KeyError as exc:
            raise KeyError(f'Unknown Task: {task_name}') from exc

        for task_key, spec in tasks_definition.items():

            if task_key.startswith('_'):
                continue

            if spec['parse_type'] == 'xmlGetter':
                action = getattr(xml_getters, spec['name'])
                action = partial(action,
                                 context.node,
                                 context.schema_dict,
                                 logger=context.logger,
                                 constants=context.constants)
                args = spec.get('kwargs', {}).copy()
            else:
                action = parse_functions[spec['parse_type']]
                args = spec['path_spec'].copy()
                args = {**args, **spec.get('kwargs', {})}

            if spec['parse_type'] == 'singleValue':
                args.setdefault('ignore', []).append('comment')

            parsed_dict = out_dict
            if 'subdict' in spec:
                parsed_dict = out_dict.setdefault(spec['subdict'], {})

            parsed_value = action(**args)

            if spec['parse_type'] == 'xmlGetter' and 'result_names' in spec:
                if isinstance(parsed_value, tuple):
                    if len(spec['result_names']) != len(parsed_value):
                        raise ValueError('Wrong number of result names given.'
                                         f"Got {len(parsed_value)} values and {len(spec['result_names'])} names")
                    parsed_value = dict(zip(spec['result_names'], parsed_value))
                else:
                    task_key = spec['result_names'][0]

            if isinstance(parsed_value, dict):

                if spec['parse_type'] == 'singleValue':
                    base_value = 'value'
                    no_list = ['units']
                    flat = True
                elif spec['parse_type'] in ['allAttribs', 'parentAttribs']:
                    base_value = spec.get('base_value', '')
                    no_list = spec.get('overwrite', [])
                    flat = spec.get('flat', True)

                if flat:
                    for key, val in parsed_value.items():
                        current_key = f'{task_key}_{camel_to_snake(key)}' if key != base_value else task_key
                        if key in no_list or not use_lists:
                            parsed_dict[current_key] = val
                        else:
                            parsed_dict.setdefault(current_key, []).append(val)

                else:
                    parsed_dict[task_key] = {camel_to_snake(key): val for key, val in parsed_value.items()}

            else:
                overwrite = spec.get('overwrite_last', False)
                force_list = spec.get('force_list', use_lists)
                if force_list and not overwrite:
                    parsed_dict.setdefault(task_key, []).append(parsed_value)
                else:
                    parsed_dict[task_key] = parsed_value if parsed_value is not None else parsed_dict.get(task_key)

        conversions = tasks_definition.get('_conversions', [])
        for conversion in conversions:
            if not isinstance(conversion, Conversion):
                warnings.warn(
                    'Providing the _conversions as a list of strings is deprecated'
                    'Use the Conversion namedtuple from masci_tools.util.parse_utils instead', DeprecationWarning)
                conversion = Conversion(name=conversion)

            action = self.conversion_functions[conversion.name]
            out_dict = action(out_dict, *conversion.args, logger=context.logger, **conversion.kwargs)

        return out_dict


F = TypeVar('F', bound=Callable[..., Any])
"""Generic Callable type"""


def register_migration(base_version: str, target_version: str | list[str]) -> Callable[[F], F]:
    """
    Decorator to add migration for task definition dictionary to the _TaskParser class
    The function should only take the dict of task definitions as an argument

    :param base_version: str of the version, from which the migration starts
    :param target_version: str or list of str with the versions that work after
                           the migration has been performed

    """

    def migration_decorator(func: F) -> F:
        """
        Return decorated _TaskParser object with migrations dict attribute
        Here all registered migrations are inserted
        """

        target_version_list = target_version
        if not isinstance(target_version_list, list):
            target_version_list = [target_version_list]

        for valid_version in target_version_list:
            _TaskParser.migrations.setdefault(base_version, {})[valid_version] = func

            for valid_version_2 in target_version_list:
                if valid_version == valid_version_2:
                    continue
                if int(valid_version.split('.')[1]) > int(valid_version_2.split('.')[1]):
                    _TaskParser.migrations.setdefault(valid_version, {})[valid_version_2] = 'compatible'
                else:
                    _TaskParser.migrations.setdefault(valid_version_2, {})[valid_version] = 'compatible'

        return func

    return migration_decorator


def conversion_function(func: F) -> F:
    """
    Marks a function as a conversion function, which can be called after
    performing a parsing task. The function can be specified via the _conversions
    control key in the task definitions.

    A conversion function has to have the following arguments:
        :param out_dict: dict with the previously parsed information
        :param parser_info_out: dict, with warnings, info, errors, ...

    and return only the modified output dict
    """
    _TaskParser.conversion_functions[func.__name__] = func

    return func
