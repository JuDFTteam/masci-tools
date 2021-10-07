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
This module provides the classes for easy acces to information
from the fleur input and output xsd schema files
"""
import os
import warnings
import tempfile
import shutil
from functools import update_wrapper, wraps
from pathlib import Path
from typing import Callable, Iterable, Union, List, Dict, Tuple, Any
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from logging import Logger

from lxml import etree

from masci_tools.util.lockable_containers import LockableDict, LockableList
from masci_tools.util.case_insensitive_dict import CaseInsensitiveFrozenSet, CaseInsensitiveDict
from masci_tools.util.xml.common_functions import abs_to_rel_xpath, split_off_tag
from masci_tools.util.xml.converters import convert_str_version_number
from .inpschema_todict import create_inpschema_dict
from .outschema_todict import create_outschema_dict, merge_schema_dicts

PACKAGE_DIRECTORY = Path(__file__).parent.resolve()


class NoPathFound(Exception):
    pass


class NoUniquePathFound(Exception):
    pass


def schema_dict_version_dispatch(output_schema: bool = False) -> Callable:
    """
    Decorator for creating variations of functions based on the inp/out
    version of the schema_dict. All functions here need to have the signature::

        def f(node, schema_dict, *args, **kwargs):
            pass

    So schema_dict is the second positional argument

    Inspired by singledispatch in the functools module
    """

    def schema_dict_version_dispatch_dec(func: Callable) -> Callable:

        registry: Dict[Union[Callable[[Tuple[int, int]], bool], Literal['default']], Callable] = {}

        def dispatch(version: Tuple[int, int]) -> Callable:

            default_match = None
            matches = []
            for condition, func in registry.items():

                if isinstance(condition, str):
                    default_match = func
                elif condition(version):
                    matches.append(func)

            matches.append(default_match)

            if len(matches) > 2:
                raise ValueError('Ambiguous possibilites for schema_dict_version_dispatch for version {version}')

            return matches[0]

        def register(min_version: str = None, max_version: str = None):

            if min_version is not None:
                min_version = convert_str_version_number(min_version)

            if max_version is not None:
                max_version = convert_str_version_number(max_version)

            def register_dec(func: Callable) -> Callable:

                if min_version is None and max_version is None:
                    raise ValueError('Either a minimum or maximum version has to be given')

                if min_version is not None and max_version is not None:
                    cond_func = lambda version: min_version <= version <= max_version
                elif min_version is not None:
                    cond_func = lambda version: version >= min_version
                else:
                    cond_func = lambda version: version <= max_version

                registry[cond_func] = func

                return func

            return register_dec

        @wraps(func)
        def wrapper(node: Any, schema_dict: 'SchemaDict', *args: Any, **kwargs: Any) -> Any:

            if not isinstance(schema_dict, SchemaDict):
                raise ValueError('Second positional argument is not a SchemaDict')

            if output_schema:
                if not isinstance(schema_dict, OutputSchemaDict):
                    raise ValueError('Second positional argument is not a OutputSchemaDict')
                version = schema_dict.out_version
            else:
                if not isinstance(schema_dict, InputSchemaDict):
                    raise ValueError('Second positional argument is not a InputSchemaDict')
                version = schema_dict.inp_version

            return dispatch(version)(node, schema_dict, *args, **kwargs)

        registry['default'] = func
        wrapper.register = register  #type:  ignore
        wrapper.dispatch = dispatch  #type:  ignore
        wrapper.registry = registry  #type:  ignore
        update_wrapper(wrapper, func)

        return wrapper

    return schema_dict_version_dispatch_dec


def _get_latest_available_version(output_schema: bool) -> str:
    """
    Determine the newest available version for the schema

    :param output_schema: bool, if True search for FleurOutputSchema.xsd otherwise FleurInputSchema.xsd

    :returns: version string of the latest version
    """

    latest_version = (0, 0)
    #Get latest version available
    for f in os.scandir(PACKAGE_DIRECTORY):
        if f.is_dir() and '.' in f.name:
            if output_schema and not (Path(f) / 'FleurOutputSchema.xsd').is_file():
                continue
            if not output_schema and not (Path(f) / 'FleurOutputSchema.xsd').is_file():
                continue

            latest_version = max(latest_version, convert_str_version_number(f.name))

    return '.'.join(map(str, latest_version))


class SchemaDict(LockableDict):
    """
    Base class for schema dictionaries. Is  locked on initialization with :py:meth:`~masci_tools.util.lockable_containers.LockableDict.freeze()`.
    Holds a reference to the xmlSchema for validating files.

    Also provides interfaces for utility functions

    :param xmlschema: etree.XMLSchema object for validating files

    All other arguments are passed on to :py:class:`~masci_tools.util.lockable_containers.LockableDict`

    """
    _schema_dict_cache: Dict[Any,'SchemaDict'] = {}
    _tag_entries: Tuple[str, ...] = ()
    _attrib_entries: Tuple[str, ...] = ()
    _info_entries: Tuple[str, ...] = ()

    @classmethod
    def clear_cache(cls) -> None:
        """
        Remove all stored entries in the schema dictionary cache
        """
        cls._schema_dict_cache.clear()

    def __init__(self, *args, xmlschema=None, **kwargs):
        self.xmlschema = xmlschema
        super().__init__(*args, **kwargs)
        super().freeze()

    def _find_paths(self,
                    name: str,
                    entries: Iterable[str],
                    contains: Union[str, Iterable[str]] = None,
                    not_contains: Union[str, Iterable[str]] = None) -> List[str]:
        """
        Find all paths in the schema_dict in the given entries for the given name
        and matching the contains/not_contains criteria

        :param name: str, name of the tag
        :param contains: str or list of str, this string has to be in the final path
        :param not_contains: str or list of str, this string has to NOT be in the final path

        :returns: list of str, found xpaths matching the criteria
        """

        if contains is None:
            contains = set()
        elif isinstance(contains, str):
            contains = set([contains])
        else:
            contains = set(contains)

        if not_contains is None:
            not_contains = set()
        elif isinstance(not_contains, str):
            not_contains = set([not_contains])
        else:
            not_contains = set(not_contains)

        path_list = []
        for entry in entries:
            if name in self[entry]:
                entry_paths = self[entry][name]

                if not isinstance(entry_paths, LockableList):
                    entry_paths = [entry_paths]
                else:
                    entry_paths = entry_paths.get_unlocked()

                invalid_paths = set()
                for phrase in contains:
                    for xpath in entry_paths:
                        if phrase not in xpath:
                            invalid_paths.add(xpath)

                for phrase in not_contains:
                    for xpath in entry_paths:
                        if phrase in xpath:
                            invalid_paths.add(xpath)

                for invalid in invalid_paths:
                    entry_paths.remove(invalid)

                path_list += entry_paths

        return path_list

    def tag_xpath(self,
                  name: str,
                  contains: Union[str, Iterable[str]] = None,
                  not_contains: Union[str, Iterable[str]] = None) -> str:
        """
        Tries to find a unique path from the schema_dict based on the given name of the tag
        and additional further specifications

        :param name: str, name of the tag
        :param contains: str or list of str, this string has to be in the final path
        :param not_contains: str or list of str, this string has to NOT be in the final path

        :returns: str, xpath for the given tag

        :raises NoPathFound: If no path matching the criteria could be found
        :raises NoUniquePathFound: If multiple paths matching the criteria are found
        """

        if not self._tag_entries:
            raise NotImplementedError(f"The method 'tag_xpath' cannot be executed for {self.__class__.__name__}"
                                      ' since no tag entries are defined')

        paths = self._find_paths(name, self._tag_entries, contains=contains, not_contains=not_contains)

        if len(paths) == 1:
            return paths[0]
        elif len(paths) == 0:
            raise NoPathFound(f'The tag {name} has no possible paths with the current specification.\n'
                              f'contains: {contains}, not_contains: {not_contains}')
        else:
            raise NoUniquePathFound(f'The tag {name} has multiple possible paths with the current specification.\n'
                                    f'contains: {contains}, not_contains: {not_contains} \n'
                                    f'These are possible: {paths}')

    def relative_tag_xpath(self,
                           name: str,
                           root_tag: str,
                           contains: Union[str, Iterable[str]] = None,
                           not_contains: Union[str, Iterable[str]] = None) -> str:
        """
        Tries to find a unique relative path from the schema_dict based on the given name of the tag
        name of the root, from which the path should be relative and additional further specifications

        :param name: str, name of the tag
        :param root_tag: str, name of the tag from which the path should be relative
        :param contains: str or list of str, this string has to be in the final path
        :param not_contains: str or list of str, this string has to NOT be in the final path

        :returns: str, xpath for the given tag

        :raises ValueError: If no unique path could be found
        """

        if not self._tag_entries:
            raise NotImplementedError(
                f"The method 'relative_tag_xpath' cannot be executed for {self.__class__.__name__}"
                ' since no tag entries are defined')

        #The paths have to include the root_tag
        if contains is None:
            contains = [root_tag]
        else:
            contains = set(contains)
            contains.add(root_tag)

        paths = self._find_paths(name, self._tag_entries, contains=contains, not_contains=not_contains)
        relative_paths = {abs_to_rel_xpath(xpath, root_tag) for xpath in paths}

        if len(relative_paths) == 1:
            return relative_paths.pop()
        elif len(relative_paths) == 0:
            raise NoPathFound(f'The tag {name} has no possible relative paths with the current specification.\n'
                              f'contains: {contains}, not_contains: {not_contains}, root_tag {root_tag}')
        else:
            raise NoUniquePathFound(
                f'The tag {name} has multiple possible relative paths with the current specification.\n'
                f'contains: {contains}, not_contains: {not_contains}, root_tag {root_tag} \n'
                f'These are possible: {relative_paths}')

    def attrib_xpath(self,
                     name: str,
                     contains: Union[str, Iterable[str]] = None,
                     not_contains: Union[str, Iterable[str]] = None,
                     exclude: Iterable[str] = None,
                     tag_name: str = None) -> str:
        """
        Tries to find a unique path from the schema_dict based on the given name of the attribute
        and additional further specifications

        :param name: str, name of the attribute
        :param root_tag: str, name of the tag from which the path should be relative
        :param contains: str or list of str, this string has to be in the final path
        :param not_contains: str or list of str, this string has to NOT be in the final path
        :param exclude: list of str, here specific types of attributes can be excluded
                        valid values are: settable, settable_contains, other
        :param tag_name: str, if given this name will be used to find a path to a tag with the
                        same name in :py:meth:`tag_xpath()`

        :returns: str, xpath to the tag with the given attribute

        :raises NoPathFound: If no path matching the criteria could be found
        :raises NoUniquePathFound: If multiple paths matching the criteria are found
        """
        if not self._attrib_entries or not self._info_entries:
            raise NotImplementedError(f"The method 'attrib_xpath' cannot be executed for {self.__class__.__name__}"
                                      ' since no attrib entries are defined')

        if tag_name is not None:
            tag_xpath = self.tag_xpath(tag_name, contains=contains, not_contains=not_contains)

            tag_info, _ = self.tag_info(
                tag_name,
                contains=contains,
                not_contains=not_contains,
                multiple_paths=True,
            )

            if name not in tag_info['attribs']:
                raise NoPathFound(f'No attribute {name} found at tag {tag_name}')
            original_case = tag_info['attribs'].original_case[name]
            return f'{tag_xpath}/@{original_case}'

        entries = list(self._attrib_entries)
        if exclude is not None:
            for list_name in exclude:
                for entry in entries.copy():
                    if f'{list_name}_attribs' in entry:
                        entries.remove(entry)

        paths = self._find_paths(name, entries, contains=contains, not_contains=not_contains)

        if len(paths) == 1:
            return paths[0]
        elif len(paths) == 0:
            raise NoPathFound(f'The attrib {name} has no possible paths with the current specification.\n'
                              f'contains: {contains}, not_contains: {not_contains}, exclude {exclude}')
        else:
            raise NoUniquePathFound(f'The attrib {name} has multiple possible paths with the current specification.\n'
                                    f'contains: {contains}, not_contains: {not_contains}, exclude {exclude}\n'
                                    f'These are possible: {paths}')

    def relative_attrib_xpath(self,
                              name: str,
                              root_tag: str,
                              contains: Union[str, Iterable[str]] = None,
                              not_contains: Union[str, Iterable[str]] = None,
                              exclude: Iterable[str] = None,
                              tag_name: str = None) -> str:
        """
        Tries to find a unique relative path from the schema_dict based on the given name of the attribute
        name of the root, from which the path should be relative and additional further specifications

        :param schema_dict: dict, containing all the path information and more
        :param name: str, name of the attribute
        :param contains: str or list of str, this string has to be in the final path
        :param not_contains: str or list of str, this string has to NOT be in the final path
        :param exclude: list of str, here specific types of attributes can be excluded
                        valid values are: settable, settable_contains, other
        :param tag_name: str, if given this name will be used to find a path to a tag with the
                        same name in :py:meth:`relative_tag_xpath()`

        :returns: str, xpath for the given tag

        :raises NoPathFound: If no path matching the criteria could be found
        :raises NoUniquePathFound: If multiple paths matching the criteria are found
        """

        if not self._attrib_entries or not self._info_entries:
            raise NotImplementedError(
                f"The method 'relative_attrib_xpath' cannot be executed for {self.__class__.__name__}"
                ' since no attrib entries are defined')

        if tag_name is not None:
            tag_xpath = self.relative_tag_xpath(tag_name, root_tag, contains=contains, not_contains=not_contains)

            tag_info, _ = self.tag_info(tag_name,
                                     multiple_paths=True,
                                     contains=contains,
                                     not_contains=not_contains)

            if name not in tag_info['attribs']:
                raise NoPathFound(f'No attribute {name} found at tag {tag_name}')

            original_case = tag_info['attribs'].original_case[name]

            if tag_xpath.endswith('/'):
                return f'{tag_xpath}@{original_case}'
            else:
                return f'{tag_xpath}/@{original_case}'

        entries = list(self._attrib_entries)
        if exclude is not None:
            for list_name in exclude:
                for entry in entries.copy():
                    if f'{list_name}_attribs' in entry:
                        entries.remove(entry)

        #The paths have to include the root_tag
        if contains is None:
            contains = [root_tag]
        else:
            contains = set(contains)
            contains.add(root_tag)

        paths = self._find_paths(name, entries, contains=contains, not_contains=not_contains)
        relative_paths = {abs_to_rel_xpath(xpath, root_tag) for xpath in paths}

        if len(relative_paths) == 1:
            return relative_paths.pop()
        elif len(relative_paths) == 0:
            raise NoPathFound(f'The attrib {name} has no possible relative paths with the current specification.\n'
                              f'contains: {contains}, not_contains: {not_contains}, root_tag {root_tag}')
        else:
            raise NoUniquePathFound(
                f'The attrib {name} has multiple possible relative paths with the current specification.\n'
                f'contains: {contains}, not_contains: {not_contains}, root_tag {root_tag} \n'
                f'These are possible: {relative_paths}')

    def tag_info(self,
                 name: str,
                 contains: Union[str, Iterable[str]] = None,
                 not_contains: Union[str, Iterable[str]] = None,
                 path_return: bool = True,
                 convert_to_builtin: bool = False,
                 multiple_paths: bool = False,
                 parent: bool = False) -> Tuple[Dict[str, Any], Union[str, List[str]]]:
        """
        Tries to find a unique path from the schema_dict based on the given name of the tag
        and additional further specifications and returns the tag_info entry for this tag

        :param schema_dict: dict, containing all the path information and more
        :param name: str, name of the tag
        :param contains: str or list of str, this string has to be in the final path
        :param not_contains: str or list of str, this string has to NOT be in the final path
        :param path_return: bool, if True the found path will be returned alongside the tag_info
        :param convert_to_builtin: bool, if True the CaseInsensitiveFrozenSets are converetd to normal sets
                                with the rigth case of the attributes
        :param multiple_paths: bool, if True mulitple paths are allowed to match as long as they have the same tag_info
        :param parent: bool, if True the tag_info for the parent of the tag is returned

        :returns: dict, tag_info for the found xpath
        :returns: str, xpath to the tag if `path_return=True`
        """

        if not self._tag_entries or not self._info_entries:
            raise NotImplementedError(f"The method 'tag_info' cannot be executed for {self.__class__.__name__}"
                                      ' since no tag or info entries are defined')

        if multiple_paths:
            paths = self._find_paths(name, self._tag_entries, contains=contains, not_contains=not_contains)
        else:
            paths = [self.tag_xpath(name, contains=contains, not_contains=not_contains)]

        EMPTY_TAG_INFO = CaseInsensitiveDict({
            'attribs': CaseInsensitiveFrozenSet(),
            'optional_attribs': {},
            'optional': CaseInsensitiveFrozenSet(),
            'order': [],
            'several': CaseInsensitiveFrozenSet(),
            'simple': CaseInsensitiveFrozenSet(),
            'complex': CaseInsensitiveFrozenSet(),
            'text': CaseInsensitiveFrozenSet()
        })
        EMPTY_TAG_INFO.freeze()

        tag_info = None
        for path in paths:

            if parent:
                path, _ = split_off_tag(path)

            entry = None
            for info_entry in self._info_entries:
                if path in self[info_entry]:
                    entry = self[info_entry][path]
            if entry is None:
                entry = EMPTY_TAG_INFO

            if tag_info is not None:
                if entry != tag_info:
                    raise ValueError(f'Differing tag_info for the found paths {paths}')
            else:
                tag_info = entry

        if convert_to_builtin:
            tag_info = {
                key: set(val.original_case.values()) if isinstance(val, CaseInsensitiveFrozenSet) else val
                for key, val in tag_info.items()
            }

        if path_return:
            if not multiple_paths:
                return tag_info, paths[0]
            else:
                return tag_info, paths
        else:
            return tag_info


class InputSchemaDict(SchemaDict):
    """
    This class contains information parsed from the FleurInputSchema.xsd

    The keys contain the following information:

        :inp_version: Version string of the input schema represented in this object
        :tag_paths: simple xpath expressions to all valid tag names
                    Multiple paths or ambiguous tag names are parsed as a list
        :_basic_types: Parsed definitions of all simple Types with their respective
                       base type (int, float, ...) and evtl. length restrictions
                       (Only used in the schema construction itself)
        :attrib_types: All possible base types for all valid attributes. If multiple are
                       possible a list, with 'string' always last (if possible)
        :simple_elements: All elements with simple types and their type definition
                          with the additional attributes
        :unique_attribs: All attributes and their paths, which occur only once and
                         have a unique path
        :unique_path_attribs: All attributes and their paths, which have a unique path
                              but occur in multiple places
        :other_attribs: All attributes and their paths, which are not in 'unique_attribs' or
                        'unique_path_attribs'
        :omitt_contained_tags: All tags, which only contain a list of one other tag
        :tag_info: For each tag (path), the valid attributes and tags (optional, several,
                   order, simple, text)
    """
    __version__ = '0.2.0'

    _schema_dict_cache: Dict[str, 'InputSchemaDict'] = {}  #type:ignore
    _tag_entries = ('tag_paths',)
    _attrib_entries = (
        'unique_attribs',
        'unique_path_attribs',
        'other_attribs',
    )
    _info_entries = ('tag_info',)

    @classmethod
    def fromVersion(cls, version: str, logger: Logger = None, no_cache: bool = False) -> 'InputSchemaDict':
        """
        load the FleurInputSchema dict for the specified version

        :param version: str with the desired version, e.g. '0.33'
        :param logger: logger object for warnings, errors and information, ...

        :return: InputSchemaDict object with the information for the provided version
        """
        schema_file_path = PACKAGE_DIRECTORY / version / 'FleurInputSchema.xsd'

        if not schema_file_path.is_file():

            latest_version = _get_latest_available_version(output_schema=False)

            if int(version.split('.')[1]) < int(latest_version.split('.')[1]):
                message = f'No FleurInputSchema.xsd found at {schema_file_path}'
                raise FileNotFoundError(message)
            else:
                if logger is not None:
                    logger.warning("No Input Schema available for version '%s'; falling back to '%s'", version,
                                   latest_version)
                else:
                    warnings.warn(
                        f"No Input Schema available for version '{version}'; falling back to '{latest_version}'")

                version = latest_version
                schema_file_path = schema_file_path = PACKAGE_DIRECTORY / version / 'FleurInputSchema.xsd'

        if version in cls._schema_dict_cache and not no_cache:
            return cls._schema_dict_cache[version]

        cls._schema_dict_cache[version] = cls.fromPath(schema_file_path)

        return cls._schema_dict_cache[version]

    @classmethod
    def fromPath(cls, path: Path) -> 'InputSchemaDict':
        """
        load the FleurInputSchema dict for the specified FleurInputSchema file

        :param path: path to the input schema file

        :return: InputSchemaDict object with the information for the provided file
        """
        path = os.fspath(path)
        schema_dict = create_inpschema_dict(path)

        xmlschema_doc = etree.parse(path)
        xmlschema = etree.XMLSchema(xmlschema_doc)

        return cls(schema_dict, xmlschema=xmlschema)

    @property
    def inp_version(self) -> Tuple[int, int]:
        """
        Returns the input version as an integer for comparisons (`>` or `<`)
        """
        return convert_str_version_number(self.get('inp_version', ''))


class OutputSchemaDict(SchemaDict):
    """
    This object contains information parsed from the FleurOutputSchema.xsd

    The keys contain the following information:

        :out_version: Version string of the output schema represented in this class
        :input_tag: Name of the element containing the fleur input
        :tag_paths: simple xpath expressions to all valid tag names not in an iteration
                    Multiple paths or ambiguous tag names are parsed as a list
        :iteration_tag_paths: simple relative xpath expressions to all valid tag names
                              inside an iteration. Multiple paths or ambiguous tag names
                              are parsed as a list
        :_basic_types: Parsed definitions of all simple Types with their respective
                       base type (int, float, ...) and evtl. length restrictions
                       (Only used in the schema construction itself)
        :_input_basic_types: Part of the parsed definitions of all simple Types with their
                             respective base type (int, float, ...) and evtl. length
                             restrictions from the input schema
                             (Only used in the schema construction itself)
        :attrib_types: All possible base types for all valid attributes. If multiple are
                       possible a list, with 'string' always last (if possible)
        :simple_elements: All elements with simple types and their type definition
                          with the additional attributes
        :unique_attribs: All attributes and their paths, which occur only once and
                         have a unique path outside of an iteration
        :unique_path_attribs: All attributes and their paths, which have a unique path
                              but occur in multiple places outside of an iteration
        :other_attribs: All attributes and their paths, which are not in 'unique_attribs' or
                        'unique_path_attribs' outside of an iteration
        :iteration_unique_attribs: All attributes and their relative paths, which occur
                                   only once and have a unique path inside of an iteration
        :iteration_unique_path_attribs: All attributes and their relative paths, which have
                                        a unique path but occur in multiple places inside
                                        of an iteration
        :iteration_other_attribs: All attributes and their relative paths, which are not
                                  in 'unique_attribs' or 'unique_path_attribs' inside
                                  of an iteration
        :omitt_contained_tags: All tags, which only contain a list of one other tag
        :tag_info: For each tag outside of an iteration (path), the valid attributes
                   and tags (optional, several, order, simple, text)
        :iteration_tag_info: For each tag inside of an iteration (relative path),
                             the valid attributes and tags (optional, several,
                             order, simple, text)
    """

    __version__ = '0.2.0'

    _schema_dict_cache: Dict[Tuple[str,str], 'OutputSchemaDict'] = {}  #type:ignore
    _tag_entries = (
        'tag_paths',
        'iteration_tag_paths',
    )
    _attrib_entries = ('unique_attribs', 'unique_path_attribs', 'other_attribs', 'iteration_unique_attribs',
                       'iteration_unique_path_attribs', 'iteration_other_attribs')
    _info_entries = ('tag_info', 'iteration_tag_info')

    @classmethod
    def fromVersion(cls,
                    version: str,
                    inp_version: str = None,
                    logger: Logger = None,
                    no_cache: bool = False) -> 'OutputSchemaDict':
        """
        load the FleurOutputSchema dict for the specified version

        :param version: str with the desired version, e.g. '0.33'
        :param inp_version: str with the desired input version, e.g. '0.33' (defaults to version)
        :param logger: logger object for warnings, errors and information, ...

        :return: OutputSchemaDict object with the information for the provided versions
        """
        if inp_version is None:
            inp_version = version

        schema_file_path = PACKAGE_DIRECTORY / version / 'FleurOutputSchema.xsd'
        inpschema_file_path = PACKAGE_DIRECTORY / inp_version / 'FleurInputSchema.xsd'

        if not schema_file_path.is_file():
            latest_version = _get_latest_available_version(output_schema=True)

            if int(version.split('.')[1]) < int(latest_version.split('.')[1]):
                message = f'No FleurOutputSchema.xsd found at {schema_file_path}'
                raise FileNotFoundError(message)
            else:
                if logger is not None:
                    logger.warning("No Output Schema available for version '%s'; falling back to '%s'", version,
                                   latest_version)
                else:
                    warnings.warn(
                        f"No Output Schema available for version '{version}'; falling back to '{latest_version}'")

                version = latest_version
                schema_file_path = PACKAGE_DIRECTORY / version / 'FleurOutputSchema.xsd'

        if not inpschema_file_path.is_file():
            latest_inpversion = _get_latest_available_version(output_schema=False)

            if int(inp_version.split('.')[1]) < int(latest_inpversion.split('.')[1]):
                message = f'No FleurInputSchema.xsd found at {inpschema_file_path}'
                raise FileNotFoundError(message)
            else:
                if logger is not None:
                    logger.warning("No Input Schema available for version '%s'; falling back to '%s'", inp_version,
                                   latest_inpversion)
                else:
                    warnings.warn(
                        f"No Input Schema available for version '{inp_version}'; falling back to '{latest_inpversion}'")

                inp_version = latest_inpversion
                inpschema_file_path = PACKAGE_DIRECTORY / version / 'FleurInputSchema.xsd'

        if inp_version != version and logger is not None:
            logger.info('Creating OutputSchemaDict object for differing versions (out: %s; inp: %s)', version,
                        inp_version)

        if (version, inp_version) in cls._schema_dict_cache and not no_cache:
            return cls._schema_dict_cache[(version, inp_version)]

        inpschema_dict = InputSchemaDict.fromVersion(inp_version, no_cache=no_cache)
        cls._schema_dict_cache[(version, inp_version)] = cls.fromPath(schema_file_path,
                                                                      inp_path=inpschema_file_path,
                                                                      inpschema_dict=inpschema_dict)

        return cls._schema_dict_cache[(version, inp_version)]

    @classmethod
    def fromPath(cls, path: Path, inp_path: Path = None, inpschema_dict: InputSchemaDict = None) -> 'OutputSchemaDict':
        """
        load the FleurOutputSchema dict for the specified paths

        :param path: path to the FleurOutputSchema file
        :param inp_path: path to the FleurInputSchema file (defaults to same folder as path)

        :return: OutputSchemaDict object with the information for the provided files
        """

        if inp_path is None:
            inp_path = Path(path).parent / 'FleurInputSchema.xsd'

        path = os.fspath(path)
        inp_path = os.fspath(inp_path)

        if inpschema_dict is None:
            inpschema_dict = create_inpschema_dict(inp_path)

        schema_dict = create_outschema_dict(path, inpschema_dict=inpschema_dict)
        schema_dict = merge_schema_dicts(inpschema_dict, schema_dict)

        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            temp_input_schema_path = td / 'FleurInputSchema.xsd'
            shutil.copy(inp_path, temp_input_schema_path)

            temp_output_schema_path = td / 'FleurOutputSchema.xsd'
            shutil.copy(path, temp_output_schema_path)
            xmlschema_doc = etree.parse(os.fspath(temp_output_schema_path))
            xmlschema = etree.XMLSchema(xmlschema_doc)

        return cls(schema_dict, xmlschema=xmlschema)

    @property
    def inp_version(self) -> Tuple[int, int]:
        """
        Returns the input version as an integer for comparisons (`>` or `<`)
        """
        return convert_str_version_number(self.get('inp_version', ''))

    @property
    def out_version(self) -> Tuple[int, int]:
        """
        Returns the output version as an integer for comparisons (`>` or `<`)
        """
        return convert_str_version_number(self.get('out_version', ''))
