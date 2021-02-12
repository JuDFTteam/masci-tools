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
This module provides the classes for easy acces to information
from the fleur input and output xsd schema files
"""
from masci_tools.util.lockable_containers import LockableDict
from masci_tools.util.schema_dict_util import get_tag_xpath, get_attrib_xpath, get_tag_info
from .inpschema_todict import create_inpschema_dict
from .outschema_todict import create_outschema_dict, merge_schema_dicts
import os
import warnings
import tempfile
import shutil
from lxml import etree

PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def _get_latest_available_version(output_schema):
    """
    Determine the newest available version for the schema

    :param output_schema: bool, if True search for FleurOutputSchema.xsd otherwise FleurInputSchema.xsd

    :returns: version string of the latest version
    """
    latest_version = 0
    #Get latest version available
    for root, dirs, files in os.walk(PACKAGE_DIRECTORY):
        for folder in dirs:
            if '0.' in folder:
                if output_schema and os.path.isfile(os.path.join(root, folder, 'FleurOutputSchema.xsd')):
                    latest_version = max(latest_version, int(folder.split('.')[1]))
                elif not output_schema and os.path.isfile(os.path.join(root, folder, 'FleurInputSchema.xsd')):
                    latest_version = max(latest_version, int(folder.split('.')[1]))
    return f'0.{latest_version}'


class SchemaDict(LockableDict):
    """
    Base class for schema dictionaries. Is  locked on initialization with :py:meth:`~masci_tools.util.lockable_containers.LockableDict.freeze()`.
    Holds a reference to the xmlSchema for validating files.

    Also provides interfaces for utility functions

    :param xmlschema: etree.XMLSchema object for validating files

    All other arguments are passed on to :py:class:`~masci_tools.util.lockable_containers.LockableDict`

    """

    def __init__(self, *args, xmlschema=None, **kwargs):
        self.xmlschema = xmlschema
        super().__init__(*args, **kwargs)
        super().freeze()

    def get_tag_xpath(self, name, contains=None, not_contains=None):
        """
        Tries to find a unique path from the schema_dict based on the given name of the tag
        and additional further specifications

        :param name: str, name of the tag
        :param contains: str or list of str, this string has to be in the final path
        :param not_contains: str or list of str, this string has to NOT be in the final path

        :returns: str, xpath to the given tag

        :raises ValueError: If no unique path could be found
        """
        return get_tag_xpath(self, name, contains=contains, not_contains=not_contains)

    def get_attrib_xpath(self, name, contains=None, not_contains=None, exclude=None, tag_name=None):
        """
        Tries to find a unique path from the schema_dict based on the given name of the attribute
        and additional further specifications

        :param name: str, name of the attribute
        :param contains: str or list of str, this string has to be in the final path
        :param not_contains: str or list of str, this string has to NOT be in the final path
        :param exclude: list of str, here specific types of attributes can be excluded
                        valid values are: settable, settable_contains, other
        :param tag_name: str, if given this name will be used to find a path to a tag with the
                         same name in :py:func:`get_tag_xpath()`

        :returns: str, xpath to the tag with the given attribute

        :raises ValueError: If no unique path could be found
        """
        return get_attrib_xpath(self,
                                name,
                                contains=contains,
                                not_contains=not_contains,
                                exclude=exclude,
                                tag_name=tag_name)

    def get_tag_info(self, name, contains=None, not_contains=None, path_return=True, convert_to_builtin=False):
        """
        Tries to find a unique path from the schema_dict based on the given name of the tag
        and additional further specifications and returns the tag_info entry for this tag

        :param name: str, name of the tag
        :param contains: str or list of str, this string has to be in the final path
        :param not_contains: str or list of str, this string has to NOT be in the final path
        :param path_return: bool, if True the found path will be returned alongside the tag_info
        :param convert_to_builtin: bool, if True the CaseInsensitiveFrozenSets are converetd to normal sets
                                   with the rigth case of the attributes

        :returns: dict, tag_info for the found xpath
        :returns: str, xpath to the tag if `path_return=True`
        """
        return get_tag_info(self,
                            name,
                            contains=contains,
                            not_contains=not_contains,
                            path_return=path_return,
                            convert_to_builtin=convert_to_builtin)


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
    __schema_dict_cache = {}

    __version__ = '0.1.0'

    @classmethod
    def fromVersion(cls, version, parser_info_out=None, no_cache=False):
        """
        load the FleurInputSchema dict for the specified version

        :param version: str with the desired version, e.g. '0.33'
        :param parser_info_out: dict with warnings, errors and information, ...

        :return: InputSchemaDict object with the information for the provided version
        """
        fleur_schema_path = f'./{version}/FleurInputSchema.xsd'
        schema_file_path = os.path.abspath(os.path.join(PACKAGE_DIRECTORY, fleur_schema_path))

        if not os.path.isfile(schema_file_path):

            latest_version = _get_latest_available_version(output_schema=False)

            if int(version.split('.')[1]) < int(latest_version.split('.')[1]):
                message = f'No FleurInputSchema.xsd found at {schema_file_path}'
                raise FileNotFoundError(message)
            else:
                if parser_info_out is not None:
                    parser_info_out['parser_warnings'].append(
                        f"No Input Schema available for version '{version}'; falling back to '{latest_version}'")
                else:
                    warnings.warn(
                        f"No Input Schema available for version '{version}'; falling back to '{latest_version}'")

                fleur_schema_path = f'./{latest_version}/FleurInputSchema.xsd'
                schema_file_path = os.path.abspath(os.path.join(PACKAGE_DIRECTORY, fleur_schema_path))

        if version in cls.__schema_dict_cache and not no_cache:
            return cls.__schema_dict_cache[version]

        cls.__schema_dict_cache[version] = cls.fromPath(schema_file_path)

        return cls.__schema_dict_cache[version]

    @classmethod
    def fromPath(cls, path):
        """
        load the FleurInputSchema dict for the specified FleurInputSchema file

        :param path: path to the input schema file
        :param parser_info_out: dict with warnings, errors and information, ...

        :return: InputSchemaDict object with the information for the provided file
        """
        schema_dict = create_inpschema_dict(path)

        xmlschema_doc = etree.parse(path)
        xmlschema = etree.XMLSchema(xmlschema_doc)

        return cls(schema_dict, xmlschema=xmlschema)


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
    __schema_dict_cache = {}

    __version__ = '0.1.0'

    @classmethod
    def fromVersion(cls, version, inp_version=None, parser_info_out=None, no_cache=False):
        """
        load the FleurOutputSchema dict for the specified version

        :param version: str with the desired version, e.g. '0.33'
        :param inp_version: str with the desired input version, e.g. '0.33' (defaults to version)
        :param parser_info_out: dict with warnings, errors and information, ...

        :return: OutputSchemaDict object with the information for the provided versions
        """
        fleur_schema_path = f'./{version}/FleurOutputSchema.xsd'
        schema_file_path = os.path.abspath(os.path.join(PACKAGE_DIRECTORY, fleur_schema_path))

        if inp_version is None:
            inp_version = version

        fleur_inpschema_path = f'./{inp_version}/FleurInputSchema.xsd'
        inpschema_file_path = os.path.abspath(os.path.join(PACKAGE_DIRECTORY, fleur_inpschema_path))

        if not os.path.isfile(schema_file_path):
            latest_version = _get_latest_available_version(output_schema=True)

            if int(version.split('.')[1]) < int(latest_version.split('.')[1]):
                message = f'No FleurOutputSchema.xsd found at {schema_file_path}'
                raise FileNotFoundError(message)
            else:
                if parser_info_out is not None:
                    parser_info_out['parser_warnings'].append(
                        f"No Output Schema available for version '{version}'; falling back to '{latest_version}'")
                else:
                    warnings.warn(
                        f"No Output Schema available for version '{version}'; falling back to '{latest_version}'")

                fleur_schema_path = f'./{latest_version}/FleurOutputSchema.xsd'
                schema_file_path = os.path.abspath(os.path.join(PACKAGE_DIRECTORY, fleur_schema_path))
                version = latest_version

        if not os.path.isfile(inpschema_file_path):
            latest_inpversion = _get_latest_available_version(output_schema=False)

            if int(inp_version.split('.')[1]) < int(latest_inpversion.split('.')[1]):
                message = f'No FleurInputSchema.xsd found at {inpschema_file_path}'
                raise FileNotFoundError(message)
            else:
                if parser_info_out is not None:
                    parser_info_out['parser_warnings'].append(
                        f"No Input Schema available for version '{inp_version}'; falling back to '{latest_inpversion}'")
                else:
                    warnings.warn(
                        f"No Input Schema available for version '{inp_version}'; falling back to '{latest_inpversion}'")

                fleur_inpschema_path = f'./{latest_inpversion}/FleurInputSchema.xsd'
                inpschema_file_path = os.path.abspath(os.path.join(PACKAGE_DIRECTORY, fleur_inpschema_path))
                inp_version = latest_inpversion

        if inp_version != version and parser_info_out is not None:
            parser_info_out['parser_warnings'].append(
                f'Creating OutputSchemaDict object for differing versions (out: {version}; inp: {inp_version})')

        version_hash = hash((version, inp_version))

        if version_hash in cls.__schema_dict_cache and not no_cache:
            return cls.__schema_dict_cache[version_hash]

        inpschema_dict = InputSchemaDict.fromVersion(inp_version, no_cache=no_cache)
        cls.__schema_dict_cache[version_hash] = cls.fromPath(schema_file_path,
                                                             inp_path=inpschema_file_path,
                                                             inpschema_dict=inpschema_dict)

        return cls.__schema_dict_cache[version_hash]

    @classmethod
    def fromPath(cls, path, inp_path=None, inpschema_dict=None):
        """
        load the FleurOutputSchema dict for the specified paths

        :param path: str path to the FleurOutputSchema file
        :param inp_path: str path to the FleurInputSchema file (defaults to same folder as path)
        :param parser_info_out: dict with warnings, errors and information, ...

        :return: OutputSchemaDict object with the information for the provided files
        """

        if inp_path is None:
            inp_path = path.replace('FleurOutputSchema', 'FleurInputSchema')

        if inpschema_dict is None:
            inpschema_dict = create_inpschema_dict(inp_path)

        schema_dict = create_outschema_dict(path, inpschema_dict=inpschema_dict)
        schema_dict = merge_schema_dicts(inpschema_dict, schema_dict)

        with tempfile.TemporaryDirectory() as td:
            temp_input_schema_path = os.path.join(td, 'FleurInputSchema.xsd')
            shutil.copy(inp_path, temp_input_schema_path)

            temp_output_schema_path = os.path.join(td, 'FleurOutputSchema.xsd')
            shutil.copy(path, temp_output_schema_path)
            xmlschema_doc = etree.parse(temp_output_schema_path)
            xmlschema = etree.XMLSchema(xmlschema_doc)

        return cls(schema_dict, xmlschema=xmlschema)
