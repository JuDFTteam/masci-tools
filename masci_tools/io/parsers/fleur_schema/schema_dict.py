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
This module provides the classes for easy access to information
from the fleur input and output xsd schema files
"""
from __future__ import annotations

import os
import warnings
import tempfile
import shutil
from functools import update_wrapper, wraps
from pathlib import Path
from typing import Callable, Iterable, TypeVar, Any, cast

from .fleur_schema_parser_functions import TagInfo, convert_str_version_number
try:
    from typing import Literal, Protocol
except ImportError:
    from typing_extensions import Literal, Protocol  #type: ignore

from logging import Logger

from lxml import etree

from masci_tools.util.lockable_containers import LockableDict, LockableList
from masci_tools.util.case_insensitive_dict import CaseInsensitiveFrozenSet, CaseInsensitiveDict
from masci_tools.util.xml.common_functions import abs_to_rel_xpath, split_off_tag, contains_tag
from .inpschema_todict import create_inpschema_dict, InputSchemaData
from .outschema_todict import create_outschema_dict, merge_schema_dicts

PACKAGE_DIRECTORY = Path(__file__).parent.resolve()


class NoPathFound(ValueError):
    """
    Exception raised when no path is found for a given tag/attribute
    """


class NoUniquePathFound(ValueError):
    """
    Exception raised when no unique path is found for a given tag/attribute
    """


class IncompatibleSchemaVersions(Exception):
    """
    Exeption raised when it is known that a given output version and input version
    cannot be compiled into a complete fleur output xml schema
    """


F = TypeVar('F', bound=Callable[..., Any])
"""Generic Type variable for callable"""


class SchemaDictDispatch(Protocol[F]):
    """Protocol representing function decorated by the schema_dict_version_dispatch decorator"""
    registry: dict[Callable[[tuple[int, int]], bool] | Literal['default'], F]

    def register(self, min_version: str | None = ..., max_version: str | None = ...) -> Callable[[F], F]:
        ...

    dispatch: Callable[[tuple[int, int]], F]
    __call__: F


def schema_dict_version_dispatch(output_schema: bool = False) -> Callable[[F], SchemaDictDispatch]:
    """
    Decorator for creating variations of functions based on the inp/out
    version of the schema_dict. All functions here need to have the signature::

        def f(node, schema_dict, *args, **kwargs):
            pass

    So schema_dict is the second positional argument

    Inspired by singledispatch in the functools module
    """

    def schema_dict_version_dispatch_dec(func: F) -> SchemaDictDispatch:

        registry: dict[Callable[[tuple[int, int]], bool] | Literal['default'], F] = {}

        def dispatch(version: tuple[int, int]) -> F:

            default_match = None
            matches = []
            for condition, func in registry.items():

                if isinstance(condition, str):
                    default_match = func
                elif condition(version):
                    matches.append(func)

            if default_match is None:
                raise ValueError('No default function registered for schema_dict_version dispatch')

            matches.append(default_match)

            if len(matches) > 2:
                raise ValueError('Ambiguous possibilities for schema_dict_version_dispatch for version {version}')

            return matches[0]

        def register(min_version: str | None = None, max_version: str | None = None) -> Callable[[F], F]:

            if min_version is not None:
                min_version_tuple = convert_str_version_number(min_version)

            if max_version is not None:
                max_version_tuple = convert_str_version_number(max_version)

            def register_dec(func: F) -> F:

                if min_version is None and max_version is None:
                    raise ValueError('Either a minimum or maximum version has to be given')

                if min_version is not None and max_version is not None:
                    cond_func = lambda version: min_version_tuple <= version <= max_version_tuple
                elif min_version is not None:
                    cond_func = lambda version: version >= min_version_tuple
                else:
                    cond_func = lambda version: version <= max_version_tuple

                registry[cond_func] = func

                return func

            return register_dec

        @wraps(func)
        def wrapper(node: Any, schema_dict: InputSchemaDict | OutputSchemaDict, *args: Any, **kwargs: Any) -> Any:

            if not isinstance(schema_dict, SchemaDict):
                raise ValueError('Second positional argument is not a SchemaDict')

            if output_schema:
                if not isinstance(schema_dict, OutputSchemaDict):
                    raise ValueError('Second positional argument is not a OutputSchemaDict')
                version = schema_dict.out_version
            else:
                version = schema_dict.inp_version

            return dispatch(version)(node, schema_dict, *args, **kwargs)

        registry['default'] = func
        wrapper.register = register  #type:ignore
        wrapper.dispatch = dispatch  #type:ignore
        wrapper.registry = registry  #type:ignore
        update_wrapper(wrapper, func)

        return cast(SchemaDictDispatch, wrapper)

    return schema_dict_version_dispatch_dec


def list_available_versions(output_schema: bool) -> list[str]:
    """
    List the available versions for the schema

    :param output_schema: bool, if True search for FleurOutputSchema.xsd otherwise FleurInputSchema.xsd

    :returns: list version string of the available versions
    """
    versions: list[str] = []
    for f in os.scandir(PACKAGE_DIRECTORY):
        if f.is_dir() and '.' in f.name:
            if output_schema and not (Path(f) / 'FleurOutputSchema.xsd').is_file():
                continue
            if not output_schema and not (Path(f) / 'FleurInputSchema.xsd').is_file():
                continue
            versions.append(f.name)
    return versions


def _get_latest_available_version(output_schema: bool) -> str:
    """
    Determine the newest available version for the schema

    :param output_schema: bool, if True search for FleurOutputSchema.xsd otherwise FleurInputSchema.xsd

    :returns: version string of the latest version
    """
    versions = list_available_versions(output_schema=output_schema)
    return max(versions, key=convert_str_version_number)


def _add_condition(specification: str | Iterable[str] | None, condition: str) -> set[str]:
    """Add element to specification making it into a set if necessary"""

    if specification is None:
        specification = set()
    elif isinstance(specification, str):
        specification = {specification}
    else:
        specification = set(specification)

    specification.add(condition)

    return specification


class SchemaDict(LockableDict):
    """
    Base class for schema dictionaries. Is  locked on initialization with :py:meth:`~masci_tools.util.lockable_containers.LockableDict.freeze()`.
    Holds a reference to the xmlSchema for validating files.

    Also provides interfaces for utility functions

    :param xmlschema: etree.XMLSchema object for validating files

    All other arguments are passed on to :py:class:`~masci_tools.util.lockable_containers.LockableDict`

    """
    _schema_dict_cache: dict[Any, SchemaDict] = {}
    _tag_entries: tuple[str, ...] = ()
    _attrib_entries: tuple[str, ...] = ()
    _info_entries: tuple[str, ...] = ()

    @classmethod
    def clear_cache(cls) -> None:
        """
        Remove all stored entries in the schema dictionary cache
        """
        cls._schema_dict_cache.clear()

    def __init__(self, *args: Any, xmlschema: etree.XMLSchema | None = None, **kwargs: Any):
        if xmlschema is None:
            raise ValueError('xmlschema has to be supplied')
        self.xmlschema = xmlschema
        super().__init__(*args, **kwargs)
        super().freeze()

    def _find_paths(self,
                    name: str,
                    entries: Iterable[str],
                    contains: str | Iterable[str] | None = None,
                    not_contains: str | Iterable[str] | None = None) -> list[str]:
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
            contains = {contains}
        else:
            contains = set(contains)

        if not_contains is None:
            not_contains = set()
        elif isinstance(not_contains, str):
            not_contains = {not_contains}
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
                  contains: str | Iterable[str] | None = None,
                  not_contains: str | Iterable[str] | None = None) -> str:
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
        if len(paths) == 0:
            raise NoPathFound(f'The tag {name} has no possible paths with the current specification.\n'
                              f'contains: {contains}, not_contains: {not_contains}')
        raise NoUniquePathFound(f'The tag {name} has multiple possible paths with the current specification.\n'
                                f'contains: {contains}, not_contains: {not_contains} \n'
                                f'These are possible: {paths}')

    def relative_tag_xpath(self,
                           name: str,
                           root_tag: str,
                           contains: str | Iterable[str] | None = None,
                           not_contains: str | Iterable[str] | None = None) -> str:
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
        contains = _add_condition(contains, root_tag)

        paths = self._find_paths(name, self._tag_entries, contains=contains, not_contains=not_contains)
        #Filter out paths which contain the rootTag explicitly not a tag name containing the root tag
        #e.g. bravaisMatrix vs. bravaisMatrixFilm
        paths = [path for path in paths if contains_tag(path, root_tag)]

        relative_paths = {abs_to_rel_xpath(xpath, root_tag) for xpath in paths}

        if len(relative_paths) == 1:
            return relative_paths.pop()
        if len(relative_paths) == 0:
            raise NoPathFound(f'The tag {name} has no possible relative paths with the current specification.\n'
                              f'contains: {contains}, not_contains: {not_contains}, root_tag {root_tag}')
        raise NoUniquePathFound(f'The tag {name} has multiple possible relative paths with the current specification.\n'
                                f'contains: {contains}, not_contains: {not_contains}, root_tag {root_tag} \n'
                                f'These are possible: {relative_paths}')

    def attrib_xpath(self,
                     name: str,
                     contains: str | Iterable[str] | None = None,
                     not_contains: str | Iterable[str] | None = None,
                     exclude: Iterable[str] | None = None,
                     tag_name: str | None = None) -> str:
        """
        Tries to find a unique path from the schema_dict based on the given name of the attribute
        and additional further specifications

        :param name: str, name of the attribute
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

        if exclude is None:
            exclude = []

        if tag_name is not None:
            tag_xpath = self.tag_xpath(tag_name, contains=contains, not_contains=not_contains)

            tag_info = self.tag_info(
                tag_name,
                contains=contains,
                not_contains=not_contains,
            )

            if name not in tag_info['attribs']:
                raise NoPathFound(f'No attribute {name} found at tag {tag_name}')
            original_case = tag_info['attribs'].original_case[name]
            return f'{tag_xpath}/@{original_case}'

        entries = [entry for entry in self._attrib_entries if all(f'{excl}_attribs' not in entry for excl in exclude)]

        paths = self._find_paths(name, entries, contains=contains, not_contains=not_contains)

        if len(paths) == 1:
            return paths[0]
        if len(paths) == 0:
            raise NoPathFound(f'The attrib {name} has no possible paths with the current specification.\n'
                              f'contains: {contains}, not_contains: {not_contains}, exclude {exclude}')
        raise NoUniquePathFound(f'The attrib {name} has multiple possible paths with the current specification.\n'
                                f'contains: {contains}, not_contains: {not_contains}, exclude {exclude}\n'
                                f'These are possible: {paths}')

    def relative_attrib_xpath(self,
                              name: str,
                              root_tag: str,
                              contains: str | Iterable[str] | None = None,
                              not_contains: str | Iterable[str] | None = None,
                              exclude: Iterable[str] | None = None,
                              tag_name: str | None = None) -> str:
        """
        Tries to find a unique relative path from the schema_dict based on the given name of the attribute
        name of the root, from which the path should be relative and additional further specifications

        :param schema_dict: dict, containing all the path information and more
        :param name: str, name of the attribute
        :param root_tag: str, name of the tag from which the path should be relative
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

        if exclude is None:
            exclude = []

        if tag_name is not None:
            tag_xpath = self.relative_tag_xpath(tag_name, root_tag, contains=contains, not_contains=not_contains)

            tag_info = self.tag_info(tag_name, contains=contains, not_contains=not_contains)

            if name not in tag_info['attribs']:
                raise NoPathFound(f'No attribute {name} found at tag {tag_name}')

            original_case = tag_info['attribs'].original_case[name]

            if tag_xpath.endswith('/'):
                return f'{tag_xpath}@{original_case}'
            return f'{tag_xpath}/@{original_case}'

        entries = [entry for entry in self._attrib_entries if all(f'{excl}_attribs' not in entry for excl in exclude)]

        #The paths have to include the root_tag
        contains = _add_condition(contains, root_tag)

        paths = self._find_paths(name, entries, contains=contains, not_contains=not_contains)
        #Filter out paths which contain the rootTag explicitly not a tag name containing the root tag
        #e.g. bravaisMatrix vs. bravaisMatrixFilm
        paths = [path for path in paths if contains_tag(path, root_tag)]
        relative_paths = {abs_to_rel_xpath(xpath, root_tag) for xpath in paths}

        if len(relative_paths) == 1:
            return relative_paths.pop()
        if len(relative_paths) == 0:
            raise NoPathFound(f'The attrib {name} has no possible relative paths with the current specification.\n'
                              f'contains: {contains}, not_contains: {not_contains}, root_tag {root_tag}')
        raise NoUniquePathFound(
            f'The attrib {name} has multiple possible relative paths with the current specification.\n'
            f'contains: {contains}, not_contains: {not_contains}, root_tag {root_tag} \n'
            f'These are possible: {relative_paths}')

    def tag_info(self,
                 name: str,
                 contains: str | Iterable[str] | None = None,
                 not_contains: str | Iterable[str] | None = None,
                 parent: bool = False,
                 **kwargs: Any) -> TagInfo:
        """
        Tries to find a unique path from the schema_dict based on the given name of the tag
        and additional further specifications and returns the tag_info entry for this tag

        :param schema_dict: dict, containing all the path information and more
        :param name: str, name of the tag
        :param contains: str or list of str, this string has to be in the final path
        :param not_contains: str or list of str, this string has to NOT be in the final path
        :param parent: bool, if True the tag_info for the parent of the tag is returned

        :returns: dict, tag_info for the found xpath
        """

        multiple_paths = True
        if 'multiple_paths' in kwargs:
            warnings.warn('multiple_paths argument is deprecated. It is used by default', DeprecationWarning)
            multiple_paths = kwargs['multiple_paths']

        path_return = False
        if 'path_return' in kwargs:
            warnings.warn('path_return argument is deprecated. It is not used by default', DeprecationWarning)
            path_return = kwargs['path_return']

        convert_to_builtin = False
        if 'convert_to_builtin' in kwargs:
            warnings.warn('convert_to_builtin argument is deprecated. It is not used by default', DeprecationWarning)
            convert_to_builtin = kwargs['convert_to_builtin']

        if not self._tag_entries or not self._info_entries:
            raise NotImplementedError(f"The method 'tag_info' cannot be executed for {self.__class__.__name__}"
                                      ' since no tag or info entries are defined')

        if multiple_paths:
            paths = self._find_paths(name, self._tag_entries, contains=contains, not_contains=not_contains)
        else:
            paths = [self.tag_xpath(name, contains=contains, not_contains=not_contains)]

        if len(paths) == 0:
            raise NoPathFound(f'The tag {name} has no possible paths with the current specification.\n'
                              f'contains: {contains}, not_contains: {not_contains}')

        EMPTY_TAG_INFO: TagInfo = {
            'attribs': CaseInsensitiveFrozenSet(),
            'optional_attribs': CaseInsensitiveDict(),
            'optional': CaseInsensitiveFrozenSet(),
            'order': [],
            'several': CaseInsensitiveFrozenSet(),
            'simple': CaseInsensitiveFrozenSet(),
            'complex': CaseInsensitiveFrozenSet(),
            'text': CaseInsensitiveFrozenSet()
        }

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
                    raise NoUniquePathFound(f'Differing tag_info for the found with the current specification\n'
                                            f'contains: {contains}, not_contains: {not_contains}\n'
                                            f'These are possible:  {paths}')
            else:
                tag_info = entry

        if tag_info is None:
            raise ValueError(f'No tag info found for paths: {paths}')

        if convert_to_builtin:
            tag_info = {
                key: set(val.original_case.values()) if isinstance(val, CaseInsensitiveFrozenSet) else val
                for key, val in tag_info.items()
            }

        if path_return:
            if not multiple_paths:
                return tag_info, paths[0]  #type:ignore
            return tag_info, paths  #type:ignore
        return tag_info  #type:ignore


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

    _schema_dict_cache: dict[str, InputSchemaDict] = {}  #type:ignore
    _tag_entries = ('tag_paths',)
    _attrib_entries = (
        'unique_attribs',
        'unique_path_attribs',
        'other_attribs',
    )
    _info_entries = ('tag_info',)

    @classmethod
    def fromVersion(cls, version: str, logger: Logger | None = None, no_cache: bool = False) -> InputSchemaDict:
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

            if logger is not None:
                logger.warning("No Input Schema available for version '%s'; falling back to '%s'", version,
                               latest_version)
            else:
                warnings.warn(f"No Input Schema available for version '{version}'; falling back to '{latest_version}'")

            version = latest_version
            schema_file_path = PACKAGE_DIRECTORY / version / 'FleurInputSchema.xsd'

        if version in cls._schema_dict_cache and not no_cache:
            return cls._schema_dict_cache[version]

        cls._schema_dict_cache[version] = cls.fromPath(schema_file_path)

        return cls._schema_dict_cache[version]

    @classmethod
    def fromPath(cls, path: os.PathLike) -> InputSchemaDict:
        """
        load the FleurInputSchema dict for the specified FleurInputSchema file

        :param path: path to the input schema file

        :return: InputSchemaDict object with the information for the provided file
        """
        fspath = os.fspath(path)
        schema_dict = create_inpschema_dict(fspath)

        xmlschema_doc = etree.parse(fspath)
        xmlschema = etree.XMLSchema(xmlschema_doc)

        return cls(schema_dict, xmlschema=xmlschema)

    @property
    def inp_version(self) -> tuple[int, int]:
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
        :iteration_tags: Names of the elements that can contain all iteration tags
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

    _schema_dict_cache: dict[tuple[str, str], OutputSchemaDict] = {}  #type:ignore
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
                    inp_version: str | None = None,
                    logger: Logger | None = None,
                    no_cache: bool = False) -> OutputSchemaDict:
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

            if logger is not None:
                logger.warning("No Output Schema available for version '%s'; falling back to '%s'", version,
                               latest_version)
            else:
                warnings.warn(f"No Output Schema available for version '{version}'; falling back to '{latest_version}'")

            version = latest_version
            schema_file_path = PACKAGE_DIRECTORY / version / 'FleurOutputSchema.xsd'

        if not inpschema_file_path.is_file():
            latest_inpversion = _get_latest_available_version(output_schema=False)

            if int(inp_version.split('.')[1]) < int(latest_inpversion.split('.')[1]):
                message = f'No FleurInputSchema.xsd found at {inpschema_file_path}'
                raise FileNotFoundError(message)

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

        #Check for known incompatibilities
        if int(version.split('.')[1]) >= 35 and int(inp_version.split('.')[1]) <= 32:
            raise IncompatibleSchemaVersions('Output schemas starting from version 0.35 cannot be compiled '
                                             'to a XML schema with Input schemas before version 0.33')

        inpschema_dict = InputSchemaDict.fromVersion(inp_version, no_cache=no_cache)
        cls._schema_dict_cache[(version, inp_version)] = cls.fromPath(schema_file_path,
                                                                      inp_path=inpschema_file_path,
                                                                      inpschema_dict=inpschema_dict)

        return cls._schema_dict_cache[(version, inp_version)]

    @classmethod
    def fromPath(cls,
                 path: os.PathLike,
                 inp_path: os.PathLike | None = None,
                 inpschema_dict: InputSchemaDict | None = None) -> OutputSchemaDict:
        """
        load the FleurOutputSchema dict for the specified paths

        :param path: path to the FleurOutputSchema file
        :param inp_path: path to the FleurInputSchema file (defaults to same folder as path)

        :return: OutputSchemaDict object with the information for the provided files
        """

        if inp_path is None:
            inp_path = Path(path).parent / 'FleurInputSchema.xsd'

        fspath = os.fspath(path)
        fsinp_path = os.fspath(inp_path)

        if inpschema_dict is None:
            inpschema_dict = create_inpschema_dict(fsinp_path)  #type:ignore
        inpschema_data = cast(InputSchemaData, inpschema_dict)

        schema_dict = create_outschema_dict(fspath, inpschema_dict=inpschema_data)
        schema_dict = merge_schema_dicts(inpschema_data, schema_dict)

        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            temp_input_schema_path = td_path / 'FleurInputSchema.xsd'
            shutil.copy(fsinp_path, temp_input_schema_path)

            temp_output_schema_path = td_path / 'FleurOutputSchema.xsd'
            shutil.copy(fspath, temp_output_schema_path)
            xmlschema_doc = etree.parse(os.fspath(temp_output_schema_path))
            xmlschema = etree.XMLSchema(xmlschema_doc)

        return cls(schema_dict, xmlschema=xmlschema)

    @property
    def inp_version(self) -> tuple[int, int]:
        """
        Returns the input version as an integer for comparisons (`>` or `<`)
        """
        return convert_str_version_number(self.get('inp_version', ''))

    @property
    def out_version(self) -> tuple[int, int]:
        """
        Returns the output version as an integer for comparisons (`>` or `<`)
        """
        return convert_str_version_number(self.get('out_version', ''))

    def iteration_tag_xpath(self,
                            name: str,
                            contains: str | Iterable[str] | None = None,
                            not_contains: str | Iterable[str] | None = None,
                            iteration_tag: str = 'iteration') -> str:
        """
        Tries to find a unique path from the schema_dict based on the given name of the tag
        and additional further specifications in the iteration section of the out.xml and returns
        the absolute path to it

        :param name: str, name of the tag
        :param contains: str or list of str, this string has to be in the final path
        :param not_contains: str or list of str, this string has to NOT be in the final path
        :param iteration_tag: name of the tag containing the iteration information

        :returns: str, xpath for the given tag

        :raises NoPathFound: If no path matching the criteria could be found
        :raises NoUniquePathFound: If multiple paths matching the criteria are found
        """

        if iteration_tag not in self['iteration_tags']:
            raise ValueError(f"{iteration_tag} is not a valid iteration tag valid are: {list(self['iteration_tags'])}")
        iteration_path = self.tag_xpath(iteration_tag)

        paths = self._find_paths(name, ('iteration_tag_paths',), contains=contains, not_contains=not_contains)
        paths = [f"{iteration_path}{path.lstrip('.')}" for path in paths]

        if len(paths) == 1:
            return paths[0]
        if len(paths) == 0:
            raise NoPathFound(f'The tag {name} has no possible iteration paths with the current specification.\n'
                              f'contains: {contains}, not_contains: {not_contains}')
        raise NoUniquePathFound(
            f'The tag {name} has multiple possible iteration paths with the current specification.\n'
            f'contains: {contains}, not_contains: {not_contains} \n'
            f'These are possible: {paths}')

    def relative_iteration_tag_xpath(self,
                                     name: str,
                                     root_tag: str,
                                     contains: str | Iterable[str] | None = None,
                                     not_contains: str | Iterable[str] | None = None,
                                     iteration_tag: str = 'iteration') -> str:
        """
        Tries to find a unique path from the schema_dict based on the given name of the tag
        and additional further specifications in the iteration section of the out.xml and returns
        the absolute path to it

        :param name: str, name of the tag
        :param contains: str or list of str, this string has to be in the final path
        :param not_contains: str or list of str, this string has to NOT be in the final path
        :param iteration_tag: name of the tag containing the iteration information

        :returns: str, xpath for the given tag

        :raises NoPathFound: If no path matching the criteria could be found
        :raises NoUniquePathFound: If multiple paths matching the criteria are found
        """

        if iteration_tag not in self['iteration_tags']:
            raise ValueError(f"{iteration_tag} is not a valid iteration tag valid are: {list(self['iteration_tags'])}")
        iteration_path = self.tag_xpath(iteration_tag)

        if not contains_tag(iteration_path, root_tag):
            #The paths have to include the root_tag
            contains = _add_condition(contains, root_tag)

        paths = self._find_paths(name, ('iteration_tag_paths',), contains=contains, not_contains=not_contains)
        if not contains_tag(iteration_path, root_tag):
            #Filter out paths which contain the rootTag explicitly not a tag name containing the root tag
            #e.g. bravaisMatrix vs. bravaisMatrixFilm
            paths = [path for path in paths if contains_tag(path, root_tag)]
        paths = [f"{iteration_path}{path.lstrip('.')}" for path in paths]
        relative_paths = {abs_to_rel_xpath(xpath, root_tag) for xpath in paths}

        if len(paths) == 1:
            return relative_paths.pop()
        if len(paths) == 0:
            raise NoPathFound(
                f'The tag {name} has no possible relative iteration paths with the current specification.\n'
                f'contains: {contains}, not_contains: {not_contains}, root_tag {root_tag}')
        raise NoUniquePathFound(
            f'The tag {name} has multiple possible relative iteration paths with the current specification.\n'
            f'contains: {contains}, not_contains: {not_contains}, root_tag {root_tag} \n'
            f'These are possible: {relative_paths}')

    def iteration_attrib_xpath(self,
                               name: str,
                               contains: str | Iterable[str] | None = None,
                               not_contains: str | Iterable[str] | None = None,
                               exclude: Iterable[str] | None = None,
                               tag_name: str | None = None,
                               iteration_tag: str = 'iteration') -> str:
        """
        Tries to find a unique path from the schema_dict based on the given name of the attribute
        and additional further specifications in the iteration section of the out.xml and returns
        the absolute path to it

        :param name: str, name of the attribute
        :param contains: str or list of str, this string has to be in the final path
        :param not_contains: str or list of str, this string has to NOT be in the final path
        :param exclude: list of str, here specific types of attributes can be excluded
                        valid values are: settable, settable_contains, other
        :param tag_name: str, if given this name will be used to find a path to a tag with the
                        same name in :py:meth:`iteration_tag_xpath()`
        :param iteration_tag: name of the tag containing the iteration information

        :returns: str, xpath to the tag with the given attribute

        :raises NoPathFound: If no path matching the criteria could be found
        :raises NoUniquePathFound: If multiple paths matching the criteria are found
        """

        if not self._attrib_entries or not self._info_entries:
            raise NotImplementedError(
                f"The method 'iteration_attrib_xpath' cannot be executed for {self.__class__.__name__}"
                ' since no attrib entries are defined')

        if iteration_tag not in self['iteration_tags']:
            raise ValueError(f"{iteration_tag} is not a valid iteration tag valid are: {list(self['iteration_tags'])}")
        iteration_path = self.tag_xpath(iteration_tag)

        if exclude is None:
            exclude = []

        if tag_name is not None:
            tag_xpath = self.iteration_tag_xpath(tag_name, contains=contains, not_contains=not_contains)

            tag_info = self.tag_info(
                tag_name,
                contains=contains,
                not_contains=not_contains,
            )

            if name not in tag_info['attribs']:
                raise NoPathFound(f'No attribute {name} found at tag {tag_name}')
            original_case = tag_info['attribs'].original_case[name]
            return f'{tag_xpath}/@{original_case}'

        entries = [
            entry for entry in self._attrib_entries
            if 'iteration' in entry and all(f'{excl}_attribs' not in entry for excl in exclude)
        ]

        paths = self._find_paths(name, entries, contains=contains, not_contains=not_contains)
        paths = [f"{iteration_path}{path.lstrip('.')}" for path in paths]

        if len(paths) == 1:
            return paths[0]
        if len(paths) == 0:
            raise NoPathFound(f'The attrib {name} has no possible iteration paths with the current specification.\n'
                              f'contains: {contains}, not_contains: {not_contains}, exclude {exclude}')
        raise NoUniquePathFound(
            f'The attrib {name} has multiple possible iteration paths with the current specification.\n'
            f'contains: {contains}, not_contains: {not_contains}, exclude {exclude}\n'
            f'These are possible: {paths}')

    def relative_iteration_attrib_xpath(self,
                                        name: str,
                                        root_tag: str,
                                        contains: str | Iterable[str] | None = None,
                                        not_contains: str | Iterable[str] | None = None,
                                        exclude: Iterable[str] | None = None,
                                        tag_name: str | None = None,
                                        iteration_tag: str = 'iteration') -> str:
        """
        Tries to find a unique relative path from the schema_dict based on the given name of the attribute
        name of the root, from which the path should be relative and additional further specifications

        :param schema_dict: dict, containing all the path information and more
        :param name: str, name of the attribute
        :param root_tag: str, name of the tag from which the path should be relative
        :param contains: str or list of str, this string has to be in the final path
        :param not_contains: str or list of str, this string has to NOT be in the final path
        :param exclude: list of str, here specific types of attributes can be excluded
                        valid values are: settable, settable_contains, other
        :param tag_name: str, if given this name will be used to find a path to a tag with the
                        same name in :py:meth:`relative_iteration_tag_xpath()`
        :param iteration_tag: name of the tag containing the iteration information

        :returns: str, xpath for the given tag

        :raises NoPathFound: If no path matching the criteria could be found
        :raises NoUniquePathFound: If multiple paths matching the criteria are found
        """

        if not self._attrib_entries or not self._info_entries:
            raise NotImplementedError(
                f"The method 'iteration_relative_attrib_xpath' cannot be executed for {self.__class__.__name__}"
                ' since no attrib entries are defined')

        if iteration_tag not in self['iteration_tags']:
            raise ValueError(f"{iteration_tag} is not a valid iteration tag valid are: {list(self['iteration_tags'])}")
        iteration_path = self.tag_xpath(iteration_tag)

        if exclude is None:
            exclude = []

        if tag_name is not None:
            tag_xpath = self.relative_iteration_tag_xpath(tag_name,
                                                          root_tag,
                                                          contains=contains,
                                                          not_contains=not_contains)

            tag_info = self.tag_info(tag_name, contains=contains, not_contains=not_contains)

            if name not in tag_info['attribs']:
                raise NoPathFound(f'No attribute {name} found at tag {tag_name}')

            original_case = tag_info['attribs'].original_case[name]

            if tag_xpath.endswith('/'):
                return f'{tag_xpath}@{original_case}'
            return f'{tag_xpath}/@{original_case}'

        entries = [
            entry for entry in self._attrib_entries
            if 'iteration' in entry and all(f'{excl}_attribs' not in entry for excl in exclude)
        ]

        if not contains_tag(iteration_path, root_tag):
            contains = _add_condition(contains, root_tag)

        paths = self._find_paths(name, entries, contains=contains, not_contains=not_contains)
        if not contains_tag(iteration_path, root_tag):
            #Filter out paths which contain the rootTag explicitly not a tag name containing the root tag
            #e.g. bravaisMatrix vs. bravaisMatrixFilm
            paths = [path for path in paths if contains_tag(path, root_tag)]
        paths = [f"{iteration_path}{path.lstrip('.')}" for path in paths]
        relative_paths = {abs_to_rel_xpath(xpath, root_tag) for xpath in paths}

        if len(relative_paths) == 1:
            return relative_paths.pop()
        if len(relative_paths) == 0:
            raise NoPathFound(
                f'The attrib {name} has no possible relative iteration paths with the current specification.\n'
                f'contains: {contains}, not_contains: {not_contains}, root_tag {root_tag}')
        raise NoUniquePathFound(
            f'The attrib {name} has multiple possible relative iteration paths with the current specification.\n'
            f'contains: {contains}, not_contains: {not_contains}, root_tag {root_tag} \n'
            f'These are possible: {relative_paths}')
