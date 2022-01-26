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
This module provides the functionality to create/load the schema_dict for the
FleurInputSchema.xsd
"""
from __future__ import annotations

from .fleur_schema_parser_functions import *  #pylint: disable=unused-wildcard-import
from masci_tools.util.xml.common_functions import clear_xml
from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict, CaseInsensitiveFrozenSet
from masci_tools.util.lockable_containers import LockableDict, LockableList
from lxml import etree
import copy
from collections import UserList
from typing import AnyStr, Callable
try:
    from typing import TypedDict, Literal
except ImportError:
    from typing_extensions import TypedDict, Literal  #type:ignore
from . import inpschema_todict


class OutputSchemaData(TypedDict, total=False):
    """Dict representing the entries in the OutputSchemaDict.
       Eventually this should be integrated into the SchemaDict classes
    """
    root_tag: str
    input_tag: str
    iteration_tags: CaseInsensitiveFrozenSet[str]
    inp_version: str
    out_version: str
    tag_paths: CaseInsensitiveDict[str, list[str] | str]
    iteration_tag_paths: CaseInsensitiveDict[str, list[str] | str]
    attrib_types: CaseInsensitiveDict[str, list[AttributeType]]
    text_types: CaseInsensitiveDict[str, list[AttributeType]]
    text_tags: CaseInsensitiveFrozenSet[str]
    unique_attribs: CaseInsensitiveDict[str, str]
    unique_path_attribs: CaseInsensitiveDict[str, list[str]]
    other_attribs: CaseInsensitiveDict[str, list[str]]
    iteration_unique_attribs: CaseInsensitiveDict[str, str]
    iteration_unique_path_attribs: CaseInsensitiveDict[str, list[str]]
    iteration_other_attribs: CaseInsensitiveDict[str, list[str]]
    omitt_contained_tags: LockableList[str]
    tag_info: LockableDict[str, TagInfo]
    iteration_tag_info: LockableDict[str, TagInfo]
    _basic_types: LockableDict[str, list[AttributeType]]
    _input_basic_types: LockableDict[str, list[AttributeType]]


KEYS = Literal['root_tag', 'input_tag', 'iteration_tags', 'tag_paths', 'iteration_tag_paths', '_basic_types',
               'attrib_types', 'text_types', 'text_tags', 'unique_attribs', 'unique_path_attribs', 'other_attribs',
               'iteration_unique_attribs', 'iteration_unique_path_attribs', 'iteration_other_attribs',
               'omitt_contained_tags', 'tag_info', 'iteration_tag_info']


def create_outschema_dict(path: AnyStr,
                          inpschema_dict: inpschema_todict.InputSchemaData,
                          apply_patches: bool = True) -> OutputSchemaData:
    """
    Creates dictionary with information about the FleurOutputSchema.xsd.
    The functions, whose results are added to the schema_dict and the corresponding keys
    are defined in schema_actions

    :param path: str path to the folder containing the FleurOutputSchema.xsd file
    :param inp_path: str path to the FleurInputSchema.xsd file (defaults to the same folder as path)
    """

    #Add new functionality to this dictionary here
    schema_actions: dict[KEYS, Callable] = {
        'input_tag': get_input_tag,
        'root_tag': get_root_tag,
        'iteration_tags': get_iteration_tags,
        '_basic_types': get_basic_types,
        'attrib_types': extract_attribute_types,
        'text_types': extract_text_types,
        'text_tags': get_text_tags,
        'tag_paths': get_tag_paths,
        'iteration_tag_paths': get_tag_paths,
        'unique_attribs': get_unique_attribs,
        'unique_path_attribs': get_unique_path_attribs,
        'other_attribs': get_other_attribs,
        'iteration_unique_attribs': get_unique_attribs,
        'iteration_unique_path_attribs': get_unique_path_attribs,
        'iteration_other_attribs': get_other_attribs,
        'tag_info': get_tag_info,
        'iteration_tag_info': get_tag_info,
        'omitt_contained_tags': get_omittable_tags,
    }
    schema_patches = [fix_qpoints_typo, patch_text_types]

    #print(f'processing: {path}/FleurOutputSchema.xsd')
    xmlschema = etree.parse(path)
    xmlschema, _ = clear_xml(xmlschema)

    xmlschema_evaluator = etree.XPathEvaluator(xmlschema, namespaces=NAMESPACES)
    out_version = str(xmlschema_evaluator('/xsd:schema/@version')[0])
    out_version_tuple = convert_str_version_number(out_version)

    input_basic_types = inpschema_dict['_basic_types'].get_unlocked()

    schema_dict: OutputSchemaData = {}
    schema_dict['out_version'] = out_version
    for key, action in schema_actions.items():
        addargs: dict[str, dict[str, list[AttributeType]] | bool] = {'input_basic_types': input_basic_types}
        if key in ['unique_attribs', 'unique_path_attribs', 'other_attribs', 'tag_paths', 'tag_info']:
            addargs['stop_iteration'] = True
        elif key in [
                'iteration_unique_attribs', 'iteration_unique_path_attribs', 'iteration_other_attribs',
                'iteration_tag_paths', 'iteration_tag_info'
        ]:
            addargs['iteration_root'] = True
            addargs['iteration'] = True
        schema_dict[key] = action(xmlschema_evaluator, **schema_dict, **addargs)

    schema_dict['_input_basic_types'] = LockableDict(input_basic_types)

    if apply_patches:
        for patch_func in schema_patches:
            patch_func(schema_dict, out_version_tuple)

    return schema_dict


def fix_qpoints_typo(schema_dict: OutputSchemaData, out_version: tuple[int, int]) -> None:
    """
    In versions before 0.35 the attribute qPoints was mistakenly called qpoints
    in the FleurOutputSchema.xsd
    """
    if out_version >= (0, 35):
        #Typo was corrected after this version
        return

    schema_dict['iteration_unique_attribs']['qpoints'] = schema_dict['iteration_unique_attribs']['qpoints'].replace(
        '@qpoints', '@qPoints')

    PATH = './Forcetheorem_DMI'
    old_attribs = set(schema_dict['iteration_tag_info'][PATH]['attribs'].original_case.values())
    old_attribs.discard('qpoints')
    old_attribs.add('qPoints')
    schema_dict['iteration_tag_info'][PATH]['attribs'] = CaseInsensitiveFrozenSet(old_attribs)


def patch_text_types(schema_dict: OutputSchemaData, out_version: tuple[int, int]) -> None:
    """
    Patch the text_types entry to correct ambigouities

    :param schema_dict: dictionary produced by the fleur_schema_parser_functions (modified in-place)
    :param inp_version: input version converted to tuple of ints
    """

    ELEMENTS_ENTRY: Literal['text_types'] = 'text_types'

    if out_version >= (0, 35):
        #After this version the issue was solved
        return

    CHANGE_TYPES = {
        (0, 29): {
            'add': {
                'densityMatrixFor': [AttributeType(base_type='complex', length='unbounded')]
            }
        },
    }

    all_changes: dict[str, list[AttributeType]] = {}

    for version, changes in sorted(CHANGE_TYPES.items(), key=lambda x: x[0]):

        if out_version < version:
            continue

        version_add = changes.get('add', {})
        version_remove = changes.get('remove', set())  #type:ignore

        all_changes = {key: val for key, val in {**all_changes, **version_add}.items() if key not in version_remove}

    for name, new_definition in all_changes.items():
        if name not in schema_dict[ELEMENTS_ENTRY]:
            raise ValueError(f'patch_text_types failed. Type {name} does not exist')
        schema_dict[ELEMENTS_ENTRY][name] = new_definition


def merge_schema_dicts(inputschema_dict: inpschema_todict.InputSchemaData,
                       outputschema_dict: OutputSchemaData) -> OutputSchemaData:
    """
    Merge the information from the input schema into the outputschema
    This combines the type information and adjusts the paths from the inputschema
    to be valid in the out.xml file, i.e. `/fleurInput/cell` becomes `/fleurOutput/fleurInput/cell`
    or `/fleurOutput/inputData/cell` (depending on the version of the output)

    `_basic_types` and `_input_basic_types` stay untouched since they should not be used outside
    of the construction and are merely a informational entry

    :param inputschema_dict: schema dict for the input schema
    :param outputschema_dict: schema dict for the output schema

    :returns: schema dictionary with the information merged
    """
    merged_outschema_dict = copy.deepcopy(outputschema_dict)
    merged_outschema_dict['inp_version'] = inputschema_dict['inp_version']

    input_tag_path = outputschema_dict['tag_paths'][outputschema_dict['input_tag']]
    input_root_tag = inputschema_dict['root_tag']

    #
    # 1. Merge path entries and modify the input paths
    #
    path_entries: set[Literal['tag_paths', 'unique_attribs', 'unique_path_attribs', 'other_attribs']] = {
        'tag_paths', 'unique_attribs', 'unique_path_attribs', 'other_attribs'
    }
    for entry in path_entries:
        for key, val in inputschema_dict[entry].items():

            paths: list[str] | str = merged_outschema_dict[entry].get(key, UserList())

            if not isinstance(paths, (UserList, list)):
                paths = [paths]
            paths_set = set(paths)

            if not isinstance(val, (UserList, list)):
                val = [val]
            new_paths_set = {f"{input_tag_path}{inp_path.replace(f'/{input_root_tag}','')}" for inp_path in val}

            new_paths = sorted(paths_set.union(new_paths_set))
            if len(new_paths) == 1:
                merged_outschema_dict[entry][key] = new_paths[0]
            else:
                merged_outschema_dict[entry][key] = new_paths

    #Remove the root_tag of the input if it is different from the input tag in the out.xml
    if input_root_tag != outputschema_dict['input_tag']:
        merged_outschema_dict['tag_paths'].pop(input_root_tag)

    #
    # 2. Insert tag_info paths (There is no possibility for overlap here)
    #
    new_tag_info_entries = {
        f"{input_tag_path}{path.replace(f'/{input_root_tag}','')}": info
        for path, info in inputschema_dict['tag_info'].items()
    }
    merged_outschema_dict['tag_info'].update(new_tag_info_entries)

    #
    # 3. Merge the attribute type information
    #
    for attrib, types in inputschema_dict['attrib_types'].items():
        out_types = set(merged_outschema_dict['attrib_types'].get(attrib, []))

        new_types = sorted(out_types.union(set(types)), key=type_order)

        merged_outschema_dict['attrib_types'][attrib] = new_types

    #
    # 4. Merge the definition information for text tags
    #
    for tag, types in inputschema_dict['text_types'].items():
        out_types = set(merged_outschema_dict['text_types'].get(tag, []))

        new_types = sorted(out_types.union(set(types)), key=type_order)

        merged_outschema_dict['text_types'][tag] = new_types

    merged_outschema_dict['text_tags'] = merged_outschema_dict['text_tags'] | inputschema_dict['text_tags']

    #
    # 5. Merge the omittable tags
    #
    merged_outschema_dict['omitt_contained_tags'] = LockableList(
        sorted(set(merged_outschema_dict['omitt_contained_tags']).union(inputschema_dict['omitt_contained_tags'])))

    return merged_outschema_dict
