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

import os
from .fleur_schema_parser_functions import *  #pylint: disable=unused-wildcard-import
from masci_tools.util.xml.common_functions import clear_xml
from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict, CaseInsensitiveFrozenSet
from masci_tools.util.lockable_containers import LockableDict, LockableList
from typing import Callable
try:
    from typing import TypedDict, Literal
except ImportError:
    from typing_extensions import TypedDict, Literal  #type: ignore
from lxml import etree


class InputSchemaData(TypedDict, total=False):
    """Dict representing the entries in the InputSchemaDict.
       Eventually this should be integrated into the SchemaDict classes
    """
    root_tag: str
    inp_version: str
    tag_paths: CaseInsensitiveDict[str, list[str] | str]
    attrib_types: CaseInsensitiveDict[str, list[AttributeType]]
    text_types: CaseInsensitiveDict[str, list[AttributeType]]
    text_tags: CaseInsensitiveFrozenSet[str]
    unique_attribs: CaseInsensitiveDict[str, str]
    unique_path_attribs: CaseInsensitiveDict[str, list[str]]
    other_attribs: CaseInsensitiveDict[str, list[str]]
    omitt_contained_tags: LockableList[str]
    tag_info: LockableDict[str, TagInfo]
    _basic_types: LockableDict[str, list[AttributeType]]


KEYS = Literal['root_tag', 'tag_paths', '_basic_types', 'attrib_types', 'text_types', 'text_tags', 'unique_attribs',
               'unique_path_attribs', 'other_attribs', 'omitt_contained_tags', 'tag_info']


def create_inpschema_dict(path: os.PathLike, apply_patches: bool = True) -> InputSchemaData:
    """
    Creates dictionary with information about the FleurInputSchema.xsd.
    The functions, whose results are added to the schema_dict and the corresponding keys
    are defined in schema_actions

    :param path: str path to the folder containing the FleurInputSchema.xsd file
    :param apply_patches: bool if True (default) the registered patching functions are applied after creation

    """

    #Add new functionality to this dictionary here
    schema_actions: dict[KEYS, Callable] = {
        'root_tag': get_root_tag,
        'tag_paths': get_tag_paths,
        '_basic_types': get_basic_types,
        'attrib_types': extract_attribute_types,
        'text_types': extract_text_types,
        'text_tags': get_text_tags,
        'unique_attribs': get_unique_attribs,
        'unique_path_attribs': get_unique_path_attribs,
        'other_attribs': get_other_attribs,
        'omitt_contained_tags': get_omittable_tags,
        'tag_info': get_tag_info,
    }
    schema_patches = [convert_string_to_float_expr, patch_forcetheorem_attributes, patch_text_types]

    xmlschema = etree.parse(path)
    xmlschema, _ = clear_xml(xmlschema)

    xmlschema_evaluator = etree.XPathEvaluator(xmlschema, namespaces=NAMESPACES)

    inp_version = eval_single_string_attribute(xmlschema_evaluator, '/xsd:schema/@version')

    inp_version_tuple = convert_str_version_number(inp_version)

    schema_dict: InputSchemaData = {}
    schema_dict['inp_version'] = inp_version
    for key, action in schema_actions.items():
        schema_dict[key] = action(xmlschema_evaluator, **schema_dict)

        if key == '_basic_types' and apply_patches:
            schema_dict[key] = patch_basic_types(schema_dict[key], inp_version_tuple)

    if apply_patches:
        for patch_func in schema_patches:
            patch_func(schema_dict, inp_version_tuple)

    return schema_dict


def convert_string_to_float_expr(schema_dict: InputSchemaData, inp_version: tuple[int, int]) -> None:
    """
    Converts specified string attributes to float_expression for schema_dicts of versions
    0.32 and before.

    This enables the usage of the converted attributes in more xml modifying functions (shift_value) for example

    :param schema_dict: dictionary produced by the fleur_schema_parser_functions (modified in-place)
    :param inp_version: input version converted to tuple of ints
    """

    TYPES_ENTRY: Literal['attrib_types'] = 'attrib_types'
    EXPR_NAME = AttributeType(base_type='float_expression', length=1)

    CHANGE_TYPES = {
        (0, 32): {
            'replace': {'mag_scale', 'mix_b', 'mix_relaxweightoffd', 'vol', 'warp_factor'}
        },
        (0, 30): {
            'replace': {'precondparam'}
        },
        (0, 29): {
            'replace':
            {'vca_charge', 'energy', 'force_converged', 'forcealpha', 'fixed_moment', 'b_field', 'b_field_mt'}
        },
        (0, 27): {
            'replace': {
                'Kmax', 'Gmax', 'GmaxXC', 'alpha', 'beta', 'b_cons_x', 'b_cons_y', 'dtilda', 'dvac', 'epsdisp',
                'epsforce', 'fermismearingenergy', 'fermismearingtemp', 'U', 'J', 'locx1', 'locx2', 'locy1', 'locy2',
                'logincrement', 'm', 'magmom', 'maxeigenval', 'mineigenval', 'maxenergy', 'minenergy',
                'maxtimetostartiter', 'ellow', 'elup', 'minDistance', 'phi', 'theta', 'radius', 'scale', 'sig_b_1',
                'sig_b_2', 'sigma', 'spindown', 'spinup', 'spinf', 'theta', 'thetaJ', 'tworkf', 'valenceelectrons',
                'weight', 'zsigma'
            },
            'add': {'value'}
        }
    }

    if inp_version >= (0, 33):
        #After this version the issue was solved
        return

    replace_set: set[str] = set()
    add_set: set[str] = set()

    for version, changes in sorted(CHANGE_TYPES.items(), key=lambda x: x[0]):

        if inp_version < version:
            continue

        version_replace_set = changes.get('replace', set())
        version_add_set = changes.get('add', set())
        version_remove_set = changes.get('remove', set())

        replace_set = (replace_set | version_replace_set) - version_remove_set
        add_set = (add_set | version_add_set) - version_remove_set

    for name in replace_set:
        if name not in schema_dict[TYPES_ENTRY]:
            raise ValueError(f'convert_string_to_float_expr failed. Attribute {name} does not exist')
        if not any(type_def.base_type in (
                'string',
                'float',
        ) for type_def in schema_dict[TYPES_ENTRY][name]):
            raise ValueError(
                f'convert_string_to_float_expr failed. Attribute {name} does not have string or float type')
        schema_dict[TYPES_ENTRY][name] = [EXPR_NAME]

    for name in add_set:
        if name not in schema_dict[TYPES_ENTRY]:
            raise ValueError(f'convert_string_to_float_expr failed. Attribute {name} does not exist')
        if not any(type_def.base_type == 'string' for type_def in schema_dict[TYPES_ENTRY][name]):
            raise ValueError(f'convert_string_to_float_expr failed. Attribute {name} does not have string type')
        schema_dict[TYPES_ENTRY][name].insert(0, EXPR_NAME)


def patch_forcetheorem_attributes(schema_dict: InputSchemaData, inp_version: tuple[int, int]) -> None:
    """
    Special patch for theta, phi and ef_shift attributes on forceTheorem tags
    In Max5/5.1 They are entered as FleurDouble but can be a list.
    """
    if inp_version >= (0, 35):
        return

    schema_dict['attrib_types']['theta'] = sorted(schema_dict['attrib_types']['theta'] + \
                                                  [AttributeType(base_type='float_expression', length='unbounded')], key=type_order)

    schema_dict['attrib_types']['phi'] = sorted(schema_dict['attrib_types']['phi'] + \
                                                  [AttributeType(base_type='float_expression', length='unbounded')], key=type_order)

    if inp_version >= (0, 34):
        schema_dict['attrib_types']['ef_shift'] = sorted(schema_dict['attrib_types']['ef_shift'] + \
                                                  [AttributeType(base_type='float_expression', length='unbounded')], key=type_order)


def patch_basic_types(basic_types: LockableDict[str, list[AttributeType]],
                      inp_version: tuple[int, int]) -> LockableDict[str, list[AttributeType]]:
    """
    Patch the _basic_types entry to correct ambigouities

    :param schema_dict: dictionary produced by the fleur_schema_parser_functions (modified in-place)
    :param inp_version: input version converted to tuple of ints
    """

    if inp_version >= (0, 33):
        #After this version the issue was solved
        return basic_types

    CHANGE_TYPES = {
        (0, 32): {
            'add': {
                'KPointType': [AttributeType(base_type='float_expression', length=3)]
            }
        },
        (0, 28): {
            'add': {
                'AtomPosType': [AttributeType(base_type='float_expression', length=3)],
                'LatticeParameterType': [AttributeType(base_type='float_expression', length=1)],
                'SpecialPointType': [AttributeType(base_type='float_expression', length=3)]
            }
        },
    }

    all_changes: dict[str, list[AttributeType]] = {}

    for version, changes in sorted(CHANGE_TYPES.items(), key=lambda x: x[0]):

        if inp_version < version:
            continue

        version_add = changes.get('add', {})
        version_remove: set[str] = changes.get('remove', set())  #type: ignore

        all_changes = {key: val for key, val in {**all_changes, **version_add}.items() if key not in version_remove}

    for name, new_definition in all_changes.items():
        if name not in basic_types:
            raise ValueError(f'patch_basic_types failed. Type {name} does not exist')
        basic_types[name] = new_definition

    return basic_types


def patch_text_types(schema_dict: InputSchemaData, inp_version: tuple[int, int]) -> None:
    """
    Patch the simple_elememnts entry to correct ambigouities

    :param schema_dict: dictionary produced by the fleur_schema_parser_functions (modified in-place)
    :param inp_version: input version converted to tuple of ints
    """

    ELEMENTS_ENTRY: Literal['text_types'] = 'text_types'

    if inp_version >= (0, 35):
        #After this version the issue was solved
        return

    CHANGE_TYPES = {
        (0, 33): {
            'remove': {'row-1', 'row-2', 'row-3'}
        },
        (0, 29): {
            'add': {
                'posforce': [AttributeType(base_type='float_expression', length=6)]
            }
        },
        (0, 28): {
            'add': {
                'q': [AttributeType(base_type='float_expression', length=3)]
            },
            'remove': {'abspos', 'relpos', 'filmpos'}
        },
        (0, 27): {
            'add': {
                'abspos': [AttributeType(base_type='float_expression', length=3)],
                'relpos': [AttributeType(base_type='float_expression', length=3)],
                'filmpos': [AttributeType(base_type='float_expression', length=3)],
                'row-1': [
                    AttributeType(base_type='float_expression', length=2),
                    AttributeType(base_type='float_expression', length=3),
                    AttributeType(base_type='float_expression', length=4)
                ],
                'row-2': [
                    AttributeType(base_type='float_expression', length=2),
                    AttributeType(base_type='float_expression', length=3),
                    AttributeType(base_type='float_expression', length=4)
                ],
                'row-3': [
                    AttributeType(base_type='float_expression', length=3),
                    AttributeType(base_type='float_expression', length=4)
                ],
            }
        }
    }

    all_changes: dict[str, list[AttributeType]] = {}

    for version, changes in sorted(CHANGE_TYPES.items(), key=lambda x: x[0]):

        if inp_version < version:
            continue

        version_add = changes.get('add', {})  #type: ignore
        version_remove = changes.get('remove', set())  #type:ignore

        all_changes = {key: val for key, val in {**all_changes, **version_add}.items() if key not in version_remove}

    for name, new_definition in all_changes.items():
        if name not in schema_dict[ELEMENTS_ENTRY]:
            raise ValueError(f'patch_text_types failed. Type {name} does not exist')
        schema_dict[ELEMENTS_ENTRY][name] = new_definition
