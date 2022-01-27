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
functions to extract information about the fleur schema input or output
"""
from __future__ import annotations

from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict, CaseInsensitiveFrozenSet
from functools import wraps
from typing import Callable, NamedTuple, Any
from lxml import etree
try:
    from typing import Literal, TypedDict
except ImportError:
    from typing_extensions import Literal, TypedDict  #type: ignore[misc]
import warnings
import math

#These types have infinite recursive paths and CANNOT BE PARSED in the path generation
_RECURSIVE_TYPES = ['CompositeTimerType']
#Name of the type of an scf iteration in the out schema (At this point the paths are split up)
_ITERATION_TYPE = 'IterationType'
_ITERATION_GROUP_TYPE = 'GeneralIterationType'
_INPUT_TYPE = 'FleurInputType'

# The types defined here should not be reduced further and are associated with one clear base type
# AngularMomentumNumberType and MainQuantumNumberType are here because they are integers
# but are implemented as xsd:string with a regex
BASE_TYPES = {
    'switch': {'FleurBool'},
    'int': {
        'xsd:nonNegativeInteger', 'xsd:positiveInteger', 'xsd:integer', 'AngularMomentumNumberType',
        'MainQuantumNumberType'
    },
    'float': {'xsd:double'},
    'float_expression': {'FleurDouble'},
    'string': {'xsd:string'},
    'complex': {'FortranComplex'}
}
NAMESPACES = {'xsd': 'http://www.w3.org/2001/XMLSchema'}


def convert_str_version_number(version_str: str) -> tuple[int, int]:
    """
    Convert the version number as a integer for easy comparisons

    :param version_str: str of the version number, e.g. '0.33'

    :returns: tuple of ints representing the version str
    """

    version_numbers = version_str.split('.')

    if len(version_numbers) != 2:
        raise ValueError(f"Version number is malformed: '{version_str}'")

    return tuple(int(part) for part in version_numbers)  #type: ignore[return-value]


class AttributeType(NamedTuple):
    """Type for describing the types of attributes/text"""
    base_type: str
    length: int | Literal['unbounded'] | None


class TagInfo(TypedDict):
    """Dict representing the entries for the tag information.
    """
    attribs: CaseInsensitiveFrozenSet[str]
    optional_attribs: CaseInsensitiveDict[str, str]
    optional: CaseInsensitiveFrozenSet[str]
    several: CaseInsensitiveFrozenSet[str]
    order: list[str]
    simple: CaseInsensitiveFrozenSet[str]
    complex: CaseInsensitiveFrozenSet[str]
    text: CaseInsensitiveFrozenSet[str]


#We define some decorators to cache results to not repeat too many similar xpath calls or recursive function calls


def _cache_xpath_construction(func: Callable[..., set[str]]) -> Callable[..., set[str]]:
    """
    Decorator for the `_get_xpath` and `_get_attrib_xpath` functions to speed up the parsing of
    xml schemas by caching results
    """

    results: dict[str, dict[int, set[str]]] = {}

    @wraps(func)
    def wrapper(xmlschema_evaluator: etree.XPathDocumentEvaluator, name: str, **kwargs: Any) -> set[str]:
        """
        This function produces a hash from all the arguments modifying the behaviour of the wrapped function
        and looks up results in dict based on this hash. If the version of the schema
        is different than before or the dict contains more than 1024 entries the cache is cleared
        """

        version = str(xmlschema_evaluator('/xsd:schema/@version')[0])
        root_tag = str(xmlschema_evaluator('/xsd:schema/xsd:element/@name')[0])

        arg_tuple = (version, root_tag, name, kwargs.get('enforce_end_type', ''), kwargs.get('ref', '')) + \
                    tuple(key for key in kwargs if kwargs.get(key, False))

        hash_args = hash(arg_tuple)
        if version not in results:
            results.clear()
            results[version] = {}

        if hash_args not in results[version]:
            res = func(xmlschema_evaluator, name, **kwargs)
            if len(results[version]) >= 1024:
                results[version].clear()
                return res
            results[version][hash_args] = res

        return results[version][hash_args].copy()

    return wrapper


def _cache_xpath_eval(func: Callable) -> Callable:
    """
    Decorator for the `_xpath_eval` function to speed up concrete xpath calls on the schema
    by caching the results
    """
    results: dict[str, dict[int, etree._XPathObject]] = {}

    @wraps(func)
    def wrapper(xmlschema_evaluator: etree.XPathDocumentEvaluator, xpath: str,
                **variables: etree._XPathObject) -> etree._XPathObject:
        """
        This function produces a hash from all the arguments modifying the behaviour of the wrapped function
        and looks up results in dict based on this hash. If the version of the schema
        is different than before or the dict contains more than 1024 entries the cache is cleared
        """

        version = str(xmlschema_evaluator('/xsd:schema/@version')[0])
        root_tag = str(xmlschema_evaluator('/xsd:schema/xsd:element/@name')[0])

        arg_tuple = (version, root_tag, xpath, *variables.items())

        hash_args = hash(arg_tuple)
        if version not in results:
            results.clear()
            results[version] = {}

        if hash_args not in results[version]:
            res = func(xmlschema_evaluator, xpath, **variables)
            if len(results[version]) >= 1024:
                results[version].clear()
                return res
            results[version][hash_args] = res
        else:
            res = results[version][hash_args]

        return res.copy() if getattr(res, 'copy', None) is not None else res

    return wrapper


@_cache_xpath_eval
def _xpath_eval(xmlschema_evaluator: etree.XPathDocumentEvaluator, xpath: str,
                **variables: etree._XPathObject) -> etree._XPathObject:
    """
    Wrapper around the xpath calls in this module. Used for caching the
    results

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema
    :param xpath: str, xpath expression to evaluate
    """
    return xmlschema_evaluator(xpath, **variables)


def _normalized_name(tag: str) -> str:
    """
    Strips the namespace prefixes from tags to make the functions more understandable

    :param tag: tag containing the namespace prefix

    :return: tag with the xsd namespace removed
    """
    return etree.QName(tag).localname


def _is_base_type(type_name: str) -> bool:
    """
    Return whether the given type_name appears in the sets in the BASE_TYPES dict
    """
    return any(type_name in types for types in BASE_TYPES.values())


def _get_parent_fleur_type(elem: etree._Element,
                           stop_non_unique: bool = False) -> tuple[etree._Element | None, str | None]:
    """
    Returns the parent simple or complexType to the given element
    If stop_sequence is given and True None is returned when a sequence is encountered
    in the parent chain

    :param elem: etree element, starting element
    :param stop_sequence: If a sequence is encountered in the loop it also terminates

    :return: the element of the parent type and the tag of the parent type with the namespaces removed
    """
    valid_end_types = ['simpleType', 'complexType', 'group']
    parent = elem.getparent()
    if parent is None:
        raise ValueError('Element has no parent')
    parent_type = _normalized_name(parent.tag)
    if stop_non_unique:
        if 'maxOccurs' in parent.attrib:
            if parent.attrib['maxOccurs'] != '1':
                return None, None
    while parent_type not in valid_end_types:
        parent = parent.getparent()
        if parent is None:
            raise ValueError('Element has no parent')
        parent_type = _normalized_name(parent.tag)
        if stop_non_unique:
            if 'maxOccurs' in parent.attrib:
                if parent.attrib['maxOccurs'] != '1':
                    return None, None
    return parent, parent_type


def _get_base_types(xmlschema_evaluator: etree.XPathDocumentEvaluator,
                    type_elem: etree._Element,
                    convert_to_base: bool = True,
                    basic_types_mapping: dict[str, list[AttributeType]] | None = None) -> list[AttributeType]:
    """
    Analyses the given type element to deduce its base_types and length restrictions

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema
    :param type_elem: etree element of the type to analyse
    :param convert_to_base: if True all possible types are converted to their base_types using either base_types
                            or basic_types_mapping
    :param basic_types_mapping: dictionary with definitions of basic_types (used for the outputschema to get the
                                definitions from the inputschema)

    :return: list of valid possibilities (AttributeType tuples) of base types and length restrictions
    """

    if basic_types_mapping is None:
        basic_types_mapping = {}

    length = _get_length(xmlschema_evaluator, type_elem)

    possible_types = set()
    for child in type_elem:
        child_type = _normalized_name(child.tag)

        types = None
        if child_type in ('restriction', 'extension'):
            types = [str(child.attrib['base'])]
        elif child_type == 'list':
            types = [str(child.attrib['itemType'])]
        elif child_type == 'union' and 'memberTypes' in child.attrib:
            types = str(child.attrib['memberTypes']).split(' ')
        elif child_type in ('union', 'simpleType'):
            new_types = _get_base_types(xmlschema_evaluator,
                                        child,
                                        convert_to_base=False,
                                        basic_types_mapping=basic_types_mapping)
            possible_types.update(new_types)

        #Reduce the found types to types that can be converted to base types
        if types is not None:

            for found_type in types:

                if _is_base_type(found_type):
                    possible_types.add(AttributeType(base_type=found_type, length=length))
                elif found_type in basic_types_mapping:
                    possible_types.add(AttributeType(base_type=found_type, length=length))
                else:
                    sub_types = _xpath_eval(xmlschema_evaluator, '//xsd:simpleType[@name=$name]', name=found_type)
                    if len(sub_types) == 0:
                        sub_types = _xpath_eval(xmlschema_evaluator,
                                                '//xsd:complexType[@name=$name]/xsd:simpleContent',
                                                name=found_type)

                    if len(sub_types) == 0:
                        raise ValueError(f"No such type '{found_type}'")

                    if len(sub_types) > 1:
                        raise ValueError(f"No unique type found for '{found_type}'")

                    new_types = _get_base_types(xmlschema_evaluator,
                                                sub_types[0],
                                                convert_to_base=False,
                                                basic_types_mapping=basic_types_mapping)

                    if length != 1:
                        possible_types.update(
                            AttributeType(base_type=base_type, length=length) for base_type, _ in new_types)
                    else:
                        possible_types.update(new_types)

    if convert_to_base:
        converted_types = set()
        for found_type, length in possible_types:
            if found_type in basic_types_mapping:
                converted_types.update(basic_types_mapping[found_type])
            else:
                for base_type, possible_base_types in BASE_TYPES.items():
                    if found_type in possible_base_types:
                        converted_types.add(AttributeType(base_type=base_type, length=length))

        if any(type_def.length is None for type_def in converted_types):
            raise ValueError(f'Length determination failed {type_elem}: {possible_types}')

        return sorted(converted_types, key=type_order)

    return list(possible_types)


def _get_length(xmlschema_evaluator: etree.XPathDocumentEvaluator,
                type_elem: etree._Element) -> int | Literal['unbounded'] | None:
    """
    Analyse the given type to determine, whether there is a length restriction

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema
    :param type_elem: etree.Element of the type to analyse

    :return: if a length restriction is found return the value,
             if a list with no restriction is found return 'unbounded',
             if neither are found return 1
    """

    type_tag = _normalized_name(type_elem.tag)

    if type_tag == 'simpleType':

        children = list(type_elem)
        if len(children) != 1:
            return 1
        child = children[0]

        child_type = _normalized_name(child.tag)
        if child_type == 'restriction':
            for restriction_child in child:
                restr_type = _normalized_name(restriction_child.tag)
                if restr_type == 'length':
                    return int(restriction_child.attrib['value'])
        elif child_type == 'list':
            return 'unbounded'

        return 1

    if type_tag in ('complexType', 'simpleContent'):
        if 'name' in type_elem.attrib:
            type_name = type_elem.attrib['name']
        else:
            parent = type_elem.getparent()
            if parent is None:
                raise ValueError('Element has no parent')
            type_name = parent.attrib['name']

        base_type = _xpath_eval(xmlschema_evaluator,
                                '//xsd:complexType[@name=$name]/xsd:simpleContent/xsd:extension/@base',
                                name=type_name)
        if len(base_type) == 0:
            return 1

        base_type_elem = _xpath_eval(xmlschema_evaluator, '//xsd:simpleType[@name=$name]', name=base_type[0])

        if len(base_type_elem) == 0:
            return 1

        return _get_length(xmlschema_evaluator, base_type_elem[0])
    return None


@_cache_xpath_construction
def _get_xpath(xmlschema_evaluator: etree.XPathDocumentEvaluator,
               tag_name: str,
               enforce_end_type: str | None = None,
               ref: str | None = None,
               stop_non_unique: bool = False,
               stop_iteration: bool = False,
               iteration_root: bool = False) -> set[str]:
    """
    construct all possible simple xpaths to a given tag

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema
    :param tag_name: name of the starting tag
    :param enforce_end_type: If given the type of the starting tag has o match this string
    :param ref: If given we start from a group reference with this name
    :param stop_non_unique: If True all paths, where one tag has maxOccurs!=1 is discarded
    :param stop_iteration: If True the path generation discards all paths going through a iteration element
    :param iteration_root: If True the path generation only generates paths going through a iteration but
                       terminates as if the group element is the root of the file
    :return: None if no path is found, if a single path is found return the string of the path,
             otherwise a list with all possible paths is returned
    """

    possible_paths: set[str] = set()
    if enforce_end_type in _RECURSIVE_TYPES:
        return possible_paths
    root_tag = get_root_tag(xmlschema_evaluator)
    if tag_name == root_tag:
        if not iteration_root:
            possible_paths.add(f'/{root_tag}')
        return possible_paths

    #Get all possible starting points
    if ref is not None:
        startPoints = _xpath_eval(xmlschema_evaluator, '//xsd:group[@ref=$ref]', ref=ref)
    else:
        if enforce_end_type is None:
            startPoints = _xpath_eval(xmlschema_evaluator, '//xsd:element[@name=$name]', name=tag_name)
        else:
            startPoints = _xpath_eval(xmlschema_evaluator,
                                      '//xsd:element[@name=$name and @type=$type]',
                                      name=tag_name,
                                      type=enforce_end_type)
    if stop_non_unique:
        startPoints_copy = startPoints.copy()
        for point in startPoints_copy:
            if 'maxOccurs' in point.attrib:
                if point.attrib['maxOccurs'] != '1':
                    startPoints.remove(point)
    for elem in startPoints:
        currentelem = elem
        currentTag = tag_name
        parent_type, parent_tag = _get_parent_fleur_type(currentelem, stop_non_unique=stop_non_unique)
        if parent_type is None:
            continue
        next_type = str(parent_type.attrib['name'])

        if next_type == _ITERATION_TYPE:
            if stop_iteration:
                continue
            if iteration_root:
                possible_paths.add(f'./{currentTag}')
                return possible_paths

        if parent_tag == 'group':
            possible_paths_group = _get_xpath(xmlschema_evaluator,
                                              currentTag,
                                              ref=next_type,
                                              stop_non_unique=stop_non_unique,
                                              stop_iteration=stop_iteration,
                                              iteration_root=iteration_root)
            possible_paths.update(possible_paths_group)
        else:
            if stop_non_unique:
                currentelem = _xpath_eval(
                    xmlschema_evaluator,
                    '//xsd:element[@type=$type and @maxOccurs=1] | //xsd:element[@type=$type and not(@maxOccurs)]',
                    type=next_type)
            else:
                currentelem = _xpath_eval(xmlschema_evaluator, '//xsd:element[@type=$type]', type=next_type)

            if len(currentelem) == 0:
                continue
            for new_elem in currentelem:
                newTag = new_elem.attrib['name']
                possible_paths_tag = _get_xpath(xmlschema_evaluator,
                                                newTag,
                                                enforce_end_type=next_type,
                                                stop_non_unique=stop_non_unique,
                                                stop_iteration=stop_iteration,
                                                iteration_root=iteration_root)
                possible_paths.update(f'{tagpath}/{tag_name}' for tagpath in possible_paths_tag)

    if iteration_root:
        #Remove any path that slipped through and contains the root tag of the out file
        possible_paths = {path for path in possible_paths if root_tag not in path}

    return possible_paths


def _get_contained_optional_attribs(xmlschema_evaluator: etree.XPathDocumentEvaluator,
                                    elem: etree._Element) -> CaseInsensitiveDict[str, str]:
    """
    Get all defined attributes contained in the given etree Element of the schema

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema
    :param elem: etree Element to analyse

    :raises: AssertionError if case insensitivity lead to lost information

    :returns: CaseInsensitiveDict with the attribute names and defaults
    """
    attrib_list = []
    for child in elem:
        child_type = _normalized_name(child.tag)

        if child_type == 'attribute':
            if child.attrib.get('use', 'required') == 'optional':
                name = str(child.attrib['name'])
                default = child.attrib.get('default')
                if default is not None:
                    default = str(default)
                attrib_list.append((name, default))
        elif child_type in ['simpleContent', 'extension']:
            new_attribs = _get_contained_optional_attribs(xmlschema_evaluator, child)
            for entry in new_attribs.items():
                attrib_list.append(entry)

    return CaseInsensitiveDict(attrib_list)


def _get_contained_attribs(xmlschema_evaluator: etree.XPathDocumentEvaluator,
                           elem: etree._Element) -> CaseInsensitiveFrozenSet[str]:
    """
    Get all defined attributes contained in the given etree Element of the schema

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema
    :param elem: etree Element to analyse

    :raises: AssertionError if case insensitivity lead to lost information

    :returns: CaseInsensitiveFrozenSet with the attribute names
    """
    attrib_list = []
    for child in elem:
        child_type = _normalized_name(child.tag)

        if child_type == 'attribute':
            attrib_list.append(str(child.attrib['name']))
        elif child_type in ['simpleContent', 'extension']:
            new_attribs = _get_contained_attribs(xmlschema_evaluator, child)
            for attrib in new_attribs:
                attrib_list.append(new_attribs.original_case[attrib])

    attrib_res = CaseInsensitiveFrozenSet(attrib_list)
    assert len(set(attrib_list)) == len(attrib_res), f'Lost Information: {attrib_list}'
    return attrib_res


def _get_optional_tags(xmlschema_evaluator: etree.XPathDocumentEvaluator,
                       elem: etree._Element) -> CaseInsensitiveFrozenSet[str]:
    """
    Get all defined tags contained in the given etree Element of the schema
    with minOccurs=0

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema
    :param elem: etree Element to analyse

    :raises: AssertionError if case insensitivity lead to lost information

    :returns: CaseInsensitiveFrozenSet with the tag names
    """
    optional_list = []
    for child in elem:
        child_type = _normalized_name(child.tag)

        if child_type == 'element':
            if 'minOccurs' in child.attrib:
                if child.attrib['minOccurs'] == '0':
                    optional_list.append(str(child.attrib['name']))
        elif child_type in ['sequence', 'all', 'choice']:
            new_optionals = _get_optional_tags(xmlschema_evaluator, child)
            for opt in new_optionals:
                optional_list.append(new_optionals.original_case[opt])

    optional_set = CaseInsensitiveFrozenSet(optional_list)
    assert len(set(optional_list)) == len(optional_set), f'Lost Information: {optional_list}'

    return optional_set


def _is_simple(elem: etree._Element) -> bool:
    """
    Determine if a given etree element is simple (only contains attributes or text (no sub elements))

    :param elem: etree Element to analyse

    :raises: ValueError if an unknown type is encountered

    :returns: bool determining, whether the element is simple
    """
    simple = True
    for child in elem:
        child_type = _normalized_name(child.tag)

        if child_type in ['attribute', 'simpleContent']:
            continue
        if child_type in ['element', 'sequence', 'choice', 'all']:
            simple = False
        else:
            raise ValueError(f"Don't know what to do with '{child_type}'")

    return simple


def _get_simple_tags(xmlschema_evaluator: etree.XPathDocumentEvaluator,
                     elem: etree._Element,
                     input_mapping: dict[str, list[AttributeType]] | None = None) -> CaseInsensitiveFrozenSet[str]:
    """
    Get all defined tags contained in the given etree Element of the schema
    which can only contain attributes or text (no sub elements)

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema
    :param elem: etree Element to analyse
    :param input_mapping: dict, with the defined types from the input schema

    :raises: AssertionError if case insensitivity lead to lost information

    :returns: CaseInsensitiveFrozenSet with the tag names
    """

    if input_mapping is None:
        input_mapping = {}

    simple_list = []
    for child in elem:
        child_type = _normalized_name(child.tag)

        if child_type == 'element':
            if child.attrib['type'] == _INPUT_TYPE:
                continue
            if child.attrib['type'] in input_mapping:
                simple_list.append(str(child.attrib['name']))
                continue

            type_name = str(child.attrib['type'])
            type_elem = _xpath_eval(xmlschema_evaluator, '//xsd:simpleType[@name=$name]', name=type_name)
            if len(type_elem) != 0:
                simple_list.append(str(child.attrib['name']))
            else:
                type_elem = _xpath_eval(xmlschema_evaluator, '//xsd:complexType[@name=$name]', name=type_name)
                if len(type_elem) == 0:
                    simple_list.append(str(child.attrib['name']))
                elif _is_simple(type_elem[0]):
                    simple_list.append(str(child.attrib['name']))
        elif child_type in ['sequence', 'all', 'choice']:
            new_simple = _get_simple_tags(xmlschema_evaluator, child, input_mapping=input_mapping)
            for simple in new_simple:
                simple_list.append(new_simple.original_case[simple])

    simple_set = CaseInsensitiveFrozenSet(simple_list)
    assert len(set(simple_list)) == len(simple_set), f'Lost Information: {simple_list}'

    return simple_set


def _get_several_tags(xmlschema_evaluator: etree.XPathDocumentEvaluator,
                      elem: etree._Element) -> CaseInsensitiveFrozenSet[str]:
    """
    Get all defined tags contained in the given etree Element of the schema
    which can occur multiple times (maxOccurs!=1)

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema
    :param elem: etree Element to analyse

    :raises: AssertionError if case insensitivity lead to lost information

    :returns: CaseInsensitiveFrozenSet with the tag names
    """
    several_list = []
    for child in elem:
        child_type = _normalized_name(child.tag)

        if child_type == 'element':
            if 'maxOccurs' in child.attrib:
                if child.attrib['maxOccurs'] != '1':
                    several_list.append(str(child.attrib['name']))
        elif child_type in ['sequence', 'all', 'choice']:
            if 'maxOccurs' in child.attrib:
                if child.attrib['maxOccurs'] != '1':
                    new_several = _get_sequence_order(xmlschema_evaluator, child)
                    for tag in new_several:
                        several_list.append(tag)
            else:
                new_several_set = _get_several_tags(xmlschema_evaluator, child)
                for tag in new_several_set:
                    several_list.append(new_several_set.original_case[tag])

    several_set = CaseInsensitiveFrozenSet(several_list)
    assert len(set(several_list)) == len(several_set), f'Lost Information: {several_list}'

    return several_set


def _get_contained_text_tags(xmlschema_evaluator: etree.XPathDocumentEvaluator, elem: etree._Element,
                             text_tags: set[str]) -> CaseInsensitiveFrozenSet[str]:
    """
    Get all defined tags contained in the given etree Element of the schema
    which can contain text

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema
    :param elem: etree Element to analyse
    :param text_tags: set with all known types of test elements

    :raises: AssertionError if case insensitivity lead to lost information

    :returns: CaseInsensitiveFrozenSet with the tag names
    """
    text_list = []
    for child in elem:
        child_type = _normalized_name(child.tag)

        if child_type == 'element':
            if child.attrib['name'] in text_tags:
                text_list.append(str(child.attrib['name']))
        elif child_type in ['sequence', 'all', 'choice']:
            new_tags_set = _get_contained_text_tags(xmlschema_evaluator, child, text_tags)
            for tag in new_tags_set:
                text_list.append(new_tags_set.original_case[tag])

    text_set = CaseInsensitiveFrozenSet(text_list)
    assert len(set(text_list)) == len(text_set), f'Lost Information: {text_list}'

    return text_set


@_cache_xpath_construction
def _get_attrib_xpath(xmlschema_evaluator: etree.XPathDocumentEvaluator,
                      attrib_name: str,
                      stop_non_unique: bool = False,
                      stop_iteration: bool = False,
                      iteration_root: bool = False) -> set[str]:
    """
    construct all possible simple xpaths to a given attribute

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema
    :param attrib_name: name of the attribute
    :param stop_non_unique: If True all paths, where one tag has maxOccurs!=1 is discarded
    :param stop_iteration: If True the path generation discards all paths going through a iteration element
    :param iteration_root: If True the path generation only generates paths going through a iteration but
                       terminates as if the iteration element is the root of the file
    :return: None if no path is found, if a single path is found return the string of the path,
             otherwise a list with all possible paths is returned
    """
    possible_paths = set()
    attribute_tags = _xpath_eval(xmlschema_evaluator, '//xsd:attribute[@name=$name]', name=attrib_name)
    for attrib in attribute_tags:
        parent_type, _ = _get_parent_fleur_type(attrib, stop_non_unique=stop_non_unique)
        if parent_type is None:
            continue

        start_type = str(parent_type.attrib['name'])
        if start_type == _ITERATION_TYPE:
            if stop_iteration:
                continue
            if iteration_root:
                possible_paths.add(f'./@{attrib_name}')
                continue

        if stop_non_unique:
            element_tags = _xpath_eval(
                xmlschema_evaluator,
                '//xsd:element[@type=$type and @maxOccurs=1]/@name | //xsd:element[@type=$type and not(@maxOccurs)]/@name',
                type=start_type)
        else:
            element_tags = _xpath_eval(xmlschema_evaluator, '//xsd:element[@type=$type]/@name', type=start_type)

        for tag in element_tags:
            tag_paths = _get_xpath(xmlschema_evaluator,
                                   tag,
                                   enforce_end_type=start_type,
                                   stop_non_unique=stop_non_unique,
                                   stop_iteration=stop_iteration,
                                   iteration_root=iteration_root)
            possible_paths.update(f'{path}/@{attrib_name}' for path in tag_paths)

    return possible_paths


def _get_sequence_order(xmlschema_evaluator: etree.XPathDocumentEvaluator, sequence_elem: etree._Element) -> list[str]:
    """
    Extract the enforced order of elements in the given sequence element

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema
    :param sequence_elem: element of the sequence to analyse

    :return: list of tags, in the order they have to occur in
    """
    elem_order = []
    for child in sequence_elem:
        child_type = _normalized_name(child.tag)

        if child_type == 'element':
            elem_order.append(str(child.attrib['name']))
        elif child_type in ['choice', 'sequence']:
            new_order = _get_sequence_order(xmlschema_evaluator, child)
            for elem in new_order:
                elem_order.append(elem)
        elif child_type == 'group':
            group = _xpath_eval(xmlschema_evaluator, '//xsd:group[@name=$name]/xsd:sequence', name=child.attrib['ref'])
            new_order = _get_sequence_order(xmlschema_evaluator, group[0])
            for elem in new_order:
                elem_order.append(elem)
        elif child_type in ['attribute', 'simpleContent', 'all']:
            continue
        else:
            raise KeyError(f'Dont know what to do with {child_type}')

    return elem_order


def _get_valid_tags(xmlschema_evaluator: etree.XPathDocumentEvaluator, sequence_elem: etree._Element) -> list[str]:
    """
    Extract all allowed elements in the given sequence element

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema
    :param sequence_elem: element of the sequence to analyse

    :return: list of tags, in the order they have to occur in
    """
    elems = []
    for child in sequence_elem:
        child_type = _normalized_name(child.tag)

        if child_type == 'element':
            elems.append(str(child.attrib['name']))
        elif child_type in ['choice', 'sequence', 'all']:
            new_elems = _get_valid_tags(xmlschema_evaluator, child)
            for elem in new_elems:
                elems.append(elem)
        elif child_type == 'group':
            group = _xpath_eval(xmlschema_evaluator, '//xsd:group[@name=$name]/xsd:sequence', name=child.attrib['ref'])
            new_elems = _get_valid_tags(xmlschema_evaluator, group[0])
            for elem in new_elems:
                elems.append(elem)
        elif child_type in ['attribute', 'simpleContent']:
            continue
        else:
            raise KeyError(f'Dont know what to do with {child_type}')

    return elems


def _extract_all_types(elems: list[etree._Element],
                       ignore_unknown: bool = False,
                       **kwargs: Any) -> CaseInsensitiveDict[str, set[AttributeType]]:
    """
    Determine the required type of all given attributes/elements

    :param elems: List of etree._Element to analyse
    :param ignore_unknown: bool, if True and a type cannot be traced back to a base type
                           nothing is done, otherwise a warning is issued

    :return: possible types of the attributes in a dictionary, if multiple
             types are possible a list is inserted for the tag
    """

    types_dict: CaseInsensitiveDict[str, set[AttributeType]] = CaseInsensitiveDict()
    for elem in elems:
        name = str(elem.attrib['name'])
        type_name = str(elem.attrib['type'])

        possible_types = set()

        if _is_base_type(type_name):
            for base_type, types in BASE_TYPES.items():
                if type_name in types:
                    possible_types.add(AttributeType(base_type=base_type, length=1))
        else:
            if type_name in kwargs['_basic_types']:
                possible_types.update(kwargs['_basic_types'][type_name])
            elif not ignore_unknown:
                warnings.warn(f'Unsorted type:{type_name}')
            else:
                continue

        if name in types_dict:
            types_dict[name] = types_dict[name] | possible_types
        else:
            types_dict[name] = possible_types

    return types_dict


def type_order(type_def: AttributeType) -> tuple[int, float]:
    """
    Key function for sorting the type definitions to avoid conflicts

    Sorted by base_type first (bool before int, string at the end)
    and then by length in ascending order (unbounded last)

    :param type_def: definition to be sorted
    """

    if not isinstance(type_def, AttributeType):
        raise ValueError('Wrong type for type_def')

    BASE_TYPE_ORDER = ('switch', 'int', 'float', 'float_expression', 'complex', 'string')

    type_index = BASE_TYPE_ORDER.index(type_def.base_type)
    if type_def.length is None:
        length = 0.0
    elif type_def.length != 'unbounded':
        length = float(type_def.length)
    else:
        length = math.inf

    return type_index, length


def extract_attribute_types(xmlschema_evaluator: etree.XPathDocumentEvaluator,
                            **kwargs: Any) -> CaseInsensitiveDict[str, list[AttributeType]]:
    """
    Determine the required type of all attributes

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema

    :return: possible types of the attributes in a dictionary, if multiple
             types are possible a list is inserted for the tag
    """
    possible_attrib = _xpath_eval(xmlschema_evaluator, '//xsd:attribute')

    types_dict = _extract_all_types(possible_attrib, **kwargs)

    types_dict_sorted: CaseInsensitiveDict[str, list[AttributeType]] = CaseInsensitiveDict()
    for name, types in types_dict.items():
        types_dict_sorted[name] = sorted(types, key=type_order)

    return types_dict_sorted


def extract_text_types(xmlschema_evaluator: etree.XPathDocumentEvaluator,
                       **kwargs: Any) -> CaseInsensitiveDict[str, list[AttributeType]]:
    """
    Determine the required type of all elements with text

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema

    :return: possible types of the attributes in a dictionary, if multiple
             types are possible a list is inserted for the tag
    """
    possible_elems = _xpath_eval(xmlschema_evaluator, '//xsd:element')

    types_dict = _extract_all_types(possible_elems, ignore_unknown=True, **kwargs)

    types_dict_sorted: CaseInsensitiveDict[str, list[AttributeType]] = CaseInsensitiveDict()
    for name, types in types_dict.items():
        types_dict_sorted[name] = sorted(types, key=type_order)

    return types_dict_sorted


def get_tag_paths(xmlschema_evaluator: etree.XPathDocumentEvaluator,
                  **kwargs: Any) -> CaseInsensitiveDict[str, list[str] | str]:
    """
    Determine simple xpaths to all possible tags

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema

    :return: possible paths of all tags in a dictionary, if multiple
             paths are possible a list is inserted for the tag
    """

    stop_iteration = kwargs.get('stop_iteration', False)
    iteration_root = kwargs.get('iteration_root', False)

    possible_tags = set(_xpath_eval(xmlschema_evaluator, '//xsd:element/@name'))
    tag_paths: CaseInsensitiveDict[str, list[str] | str] = CaseInsensitiveDict()
    for tag in sorted(possible_tags):
        paths = _get_xpath(xmlschema_evaluator, tag, stop_iteration=stop_iteration, iteration_root=iteration_root)
        if len(paths) == 1:
            tag_paths[tag] = paths.pop()
        elif len(paths) != 0:
            tag_paths[tag] = sorted(paths)
    return tag_paths


def get_unique_attribs(xmlschema_evaluator: etree.XPathDocumentEvaluator,
                       **kwargs: Any) -> CaseInsensitiveDict[str, str]:
    """
    Determine all attributes, which can be set through set_inpchanges in aiida_fleur
    Meaning ONE possible path and no tags in the path with maxOccurs!=1

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema

    :return: dictionary with all settable attributes and the corresponding path to the tag
    """

    stop_iteration = kwargs.get('stop_iteration', False)
    iteration_root = kwargs.get('iteration_root', False)

    settable: CaseInsensitiveDict[str, str] = CaseInsensitiveDict()
    possible_attrib = set(_xpath_eval(xmlschema_evaluator, '//xsd:attribute/@name'))
    for attrib in sorted(possible_attrib):
        path = _get_attrib_xpath(xmlschema_evaluator,
                                 attrib,
                                 stop_non_unique=True,
                                 stop_iteration=stop_iteration,
                                 iteration_root=iteration_root)
        if len(path) == 1:
            if attrib in settable:
                settable.pop(attrib)
            else:
                settable[attrib] = path.pop()

    for attrib in sorted(kwargs['text_tags'].original_case.values()):
        path = _get_xpath(xmlschema_evaluator,
                          attrib,
                          stop_non_unique=True,
                          stop_iteration=stop_iteration,
                          iteration_root=iteration_root)

        if len(path) == 1:
            if attrib in settable:
                settable.pop(attrib)
            else:
                settable[attrib] = path.pop()

    return settable


def get_unique_path_attribs(xmlschema_evaluator: etree.XPathDocumentEvaluator,
                            **kwargs: Any) -> CaseInsensitiveDict[str, list[str]]:
    """
    Determine all attributes, with multiple possible path that do have at
    least one path with all contained tags maxOccurs!=1

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema

    :return: dictionary with all attributes and the corresponding list of paths to the tag
    """

    stop_iteration = kwargs.get('stop_iteration', False)
    iteration_root = kwargs.get('iteration_root', False)
    iteration = kwargs.get('iteration', False)

    if iteration:
        settable_key = 'iteration_unique_attribs'
        settable_contains_key = 'iteration_unique_path_attribs'
    else:
        settable_key = 'unique_attribs'
        settable_contains_key = 'unique_path_attribs'

    settable: CaseInsensitiveDict[str, list[str]] = CaseInsensitiveDict()
    possible_attrib = set(_xpath_eval(xmlschema_evaluator, '//xsd:attribute/@name'))
    for attrib in sorted(possible_attrib):
        if attrib in kwargs[settable_key]:
            continue
        path = _get_attrib_xpath(xmlschema_evaluator,
                                 attrib,
                                 stop_non_unique=True,
                                 stop_iteration=stop_iteration,
                                 iteration_root=iteration_root)
        if len(path) != 0:
            settable[attrib] = sorted(set(settable.get(attrib, [])).union(path))

    for attrib in sorted(kwargs['text_tags'].original_case.values()):
        if attrib in kwargs[settable_key]:
            continue
        path = _get_xpath(xmlschema_evaluator,
                          attrib,
                          stop_non_unique=True,
                          stop_iteration=stop_iteration,
                          iteration_root=iteration_root)
        if len(path) != 0:
            settable[attrib] = sorted(set(settable.get(attrib, [])).union(path))

    return settable


def get_other_attribs(xmlschema_evaluator: etree.XPathDocumentEvaluator,
                      **kwargs: Any) -> CaseInsensitiveDict[str, list[str]]:
    """
    Determine all other attributes not contained in settable or settable_contains

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema

    :return: dictionary with all attributes and the corresponding list of paths to the tag
    """

    stop_iteration = kwargs.get('stop_iteration', False)
    iteration_root = kwargs.get('iteration_root', False)
    iteration = kwargs.get('iteration', False)

    if iteration:
        settable_key = 'iteration_unique_attribs'
        settable_contains_key = 'iteration_unique_path_attribs'
    else:
        settable_key = 'unique_attribs'
        settable_contains_key = 'unique_path_attribs'

    other: CaseInsensitiveDict[str, list[str]] = CaseInsensitiveDict()
    possible_attrib = set(_xpath_eval(xmlschema_evaluator, '//xsd:attribute/@name'))
    for attrib in sorted(possible_attrib):
        path = _get_attrib_xpath(xmlschema_evaluator,
                                 attrib,
                                 stop_iteration=stop_iteration,
                                 iteration_root=iteration_root)
        if len(path) != 0:
            if attrib in kwargs[settable_key]:
                path.discard(kwargs[settable_key][attrib])
            if attrib in kwargs[settable_contains_key]:
                for contains_path in kwargs[settable_contains_key][attrib]:
                    path.discard(contains_path)

            if len(path) != 0:
                other[attrib] = sorted(set(other.get(attrib, [])).union(path))

    for attrib in sorted(kwargs['text_tags'].original_case.values()):
        path = _get_xpath(xmlschema_evaluator, attrib, stop_iteration=stop_iteration, iteration_root=iteration_root)
        if len(path) != 0:

            if attrib in kwargs[settable_key]:
                path.discard(kwargs[settable_key][attrib])
            if attrib in kwargs[settable_contains_key]:
                for contains_path in kwargs[settable_contains_key][attrib]:
                    path.discard(contains_path)

            if len(path) != 0:
                other[attrib] = sorted(set(other.get(attrib, [])).union(path))

    return other


def get_omittable_tags(xmlschema_evaluator: etree.XPathDocumentEvaluator, **kwargs: Any) -> list[str]:
    """
    find tags with no attributes and, which are only used to mask a list of one other possible tag (e.g. atomSpecies)

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema

    :return: list of tags, containing only a sequence of one allowed tag
    """

    possible_tags = _xpath_eval(xmlschema_evaluator, '//xsd:element')

    omittable_tags = []
    for tag in possible_tags:
        tag_type = tag.attrib['type']
        tag_name = tag.attrib['name']

        if tag_name not in omittable_tags:
            type_elem = _xpath_eval(xmlschema_evaluator, '//xsd:complexType[@name=$name]', name=tag_type)
            if len(type_elem) == 0:
                continue
            type_elem = type_elem[0]

            omittable = False
            for child in type_elem:
                child_type = _normalized_name(child.tag)

                if child_type == 'sequence':
                    allowed_tags = 0
                    for sequence_elem in child:
                        elem_type = _normalized_name(sequence_elem.tag)
                        if elem_type == 'element':
                            allowed_tags += 1
                        else:
                            allowed_tags = 0  #So that it is not unintentionally accepted
                            break
                    if allowed_tags == 1:
                        omittable = True
                else:
                    omittable = False

            if omittable:
                omittable_tags.append(tag_name)
    return omittable_tags


def get_text_tags(xmlschema_evaluator: etree.XPathDocumentEvaluator, **kwargs: Any) -> CaseInsensitiveFrozenSet[str]:
    """
    find all elements, who can contain text

    :param xmlschema: xmltree representing the schema

    :return: dictionary with tags and their corresponding type_definition
             meaning a dictionary with possible base types and evtl. length restriction
    """

    elements = _xpath_eval(xmlschema_evaluator, '//xsd:element')

    text_tag_list = []
    for elem in elements:
        name_elem = elem.attrib['name']
        type_name = elem.attrib['type']

        if _is_base_type(type_name) or type_name in kwargs['_basic_types']:
            text_tag_list.append(name_elem)
        else:
            continue  #This type cannot be traced back to a basic type

    text_tags = CaseInsensitiveFrozenSet(text_tag_list)
    assert len(set(text_tag_list)) == len(text_tags), f'Lost Information: {text_tag_list}'

    return text_tags


def get_basic_types(xmlschema_evaluator: etree.XPathDocumentEvaluator, **kwargs: Any) -> dict[str, list[AttributeType]]:
    """
    find all types, which can be traced back directly to a base_type

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema

    :return: dictionary with type names and their corresponding type_definition
             meaning a dictionary with possible base types and evtl. length restriction
    """
    basic_type_elems = _xpath_eval(xmlschema_evaluator, '//xsd:simpleType[@name]')
    complex_type_elems = _xpath_eval(xmlschema_evaluator, '//xsd:complexType/xsd:simpleContent')

    basic_types = {}
    for type_elem in basic_type_elems + complex_type_elems:
        if 'name' in type_elem.attrib:
            type_name = type_elem.attrib['name']
        else:
            type_name = type_elem.getparent().attrib['name']

        if _is_base_type(type_name):
            continue  #Already a base type

        types = _get_base_types(xmlschema_evaluator, type_elem, basic_types_mapping=kwargs.get('input_basic_types'))

        if type_name not in basic_types:
            basic_types[type_name] = types
        else:
            raise ValueError(f'Already defined type {type_name}')

    #Append the definitions form the inputschema since including it directly is very messy
    if 'input_basic_types' in kwargs:
        if any(key in basic_types for key in kwargs['input_basic_types']):
            raise ValueError('Doubled type definitions from Inputschema')
        basic_types.update(kwargs['input_basic_types'])

    return basic_types


def get_tag_info(xmlschema_evaluator: etree.XPathDocumentEvaluator, **kwargs: Any) -> dict[str, TagInfo]:
    """
    Get all important information about the tags
        - allowed attributes
        - contained tags (simple (only attributes), optional (with default values), several, order, text tags)

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema

    :return: dictionary with the tag information
    """

    stop_iteration = kwargs.get('stop_iteration', False)
    iteration_root = kwargs.get('iteration_root', False)

    tag_info = {}

    possible_tags = _xpath_eval(xmlschema_evaluator, '//xsd:element')

    for tag in possible_tags:

        name_tag = tag.attrib['name']
        type_tag = tag.attrib['type']

        #Get the xpath for this tag
        tag_path = _get_xpath(xmlschema_evaluator,
                              name_tag,
                              enforce_end_type=type_tag,
                              stop_iteration=stop_iteration,
                              iteration_root=iteration_root)

        type_elem = _xpath_eval(xmlschema_evaluator, '//xsd:complexType[@name=$name]', name=type_tag)
        if len(type_elem) == 0:
            continue
        type_elem = type_elem[0]

        valid_tags = _get_valid_tags(xmlschema_evaluator, type_elem)
        simple_tags = _get_simple_tags(xmlschema_evaluator, type_elem, input_mapping=kwargs.get('_input_basic_types'))

        info_dict: TagInfo = {
            'attribs': _get_contained_attribs(xmlschema_evaluator, type_elem),
            'optional_attribs': _get_contained_optional_attribs(xmlschema_evaluator, type_elem),
            'optional': _get_optional_tags(xmlschema_evaluator, type_elem),
            'several': _get_several_tags(xmlschema_evaluator, type_elem),
            'order': _get_sequence_order(xmlschema_evaluator, type_elem),
            'simple': simple_tags,
            'complex': CaseInsensitiveFrozenSet(valid_tags).difference(simple_tags),
            'text': _get_contained_text_tags(xmlschema_evaluator, type_elem, kwargs['text_tags'])
        }

        if any(len(elem) != 0 for elem in info_dict.values()):  #type: ignore
            for path in tag_path:
                tag_info[path] = info_dict

    return tag_info


def get_root_tag(xmlschema_evaluator: etree.XPathDocumentEvaluator, **kwargs: Any) -> str:
    """
    Returns the tag for the root element of the xmlschema

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema

    :return: name of the single element defined in the first level of the schema
    """
    return str(_xpath_eval(xmlschema_evaluator, '/xsd:schema/xsd:element/@name')[0])


def get_input_tag(xmlschema_evaluator: etree.XPathDocumentEvaluator, **kwargs: Any) -> str:
    """
    Returns the tag for the input type element of the outxmlschema

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema

    :return: name of the element with the type 'FleurInputType'
    """
    return str(_xpath_eval(xmlschema_evaluator, '//xsd:element[@type=$type]/@name', type=_INPUT_TYPE)[0])


def get_iteration_tags(xmlschema_evaluator: etree.XPathDocumentEvaluator,
                       **kwargs: Any) -> CaseInsensitiveFrozenSet[str]:
    """
    Returns the tags that can contain the information from a SCF iteration

    :param xmlschema_evaluator: etree.XPathEvaluator for the schema

    :return: set of tag names that contain elements from the group 'GeneralIterationType'
    """
    tag_names: set[str] = set()
    group_nodes = _xpath_eval(xmlschema_evaluator, '//xsd:group[@ref=$ref]', ref=_ITERATION_GROUP_TYPE)

    for node in group_nodes:
        parent, _ = _get_parent_fleur_type(node)
        if parent is None:
            continue
        tag_names.update(
            str(name) for name in _xpath_eval(
                xmlschema_evaluator, '//xsd:element[@type=$type]/@name', type=parent.attrib['name']))

    tag_names_frozen = CaseInsensitiveFrozenSet(tag_names)
    assert len(set(tag_names)) == len(tag_names_frozen), f'Lost Information: {tag_names}'

    return tag_names_frozen
