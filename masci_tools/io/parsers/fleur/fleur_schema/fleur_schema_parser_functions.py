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
functions to extract information about the fleur schema input or output
"""
from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict, CaseInsensitiveFrozenSet
from functools import wraps

#These types have infinite recursive paths and CANNOT BE PARSED in the path generation
_RECURSIVE_TYPES = ['CompositeTimerType']
#Name of the type of an scf iteration in the out schema (At this point the paths are split up)
_ITERATION_TYPE = 'IterationType'
_INPUT_TYPE = 'FleurInputType'

#We define some decorators to cache results to not repeat too many similar xpath calls or recursive function calls


def _cache_xpath_construction(func):
    """
    Decorator for the `_get_xpath` and `_get_attrib_xpath` functions to speed up the parsing of
    xml schemas by caching results
    """

    results = {}

    @wraps(func)
    def wrapper(xmlschema, namespaces, name, **kwargs):
        """
        This function produces a hash from all the arguments modifying the behaviour of the wrapped function
        and looks up results in dict based on this hash. If the version of the schema
        is different than before or the dict contains more than 1024 entries the cache is cleared
        """

        version = str(xmlschema.xpath('/xsd:schema/@version', namespaces=namespaces)[0])
        root_tag = str(xmlschema.xpath('/xsd:schema/xsd:element/@name', namespaces=namespaces)[0])

        arg_tuple = (version, root_tag, name, kwargs.get('enforce_end_type', ''), kwargs.get('ref', '')) + \
                    tuple(key for key in kwargs if kwargs.get(key, False))

        hash_args = hash(arg_tuple)
        if version not in results:
            results.clear()
            results[version] = {}

        if hash_args not in results[version]:
            res = func(xmlschema, namespaces, name, **kwargs)
            if len(results[version]) >= 1024:
                results[version].clear()
                return res
            results[version][hash_args] = res

        return results[version][hash_args].copy()

    return wrapper


def _cache_xpath_eval(func):
    """
    Decorator for the `_xpath_eval` function to speed up concrete xpath calls on the schema
    by caching the results
    """
    results = {}

    @wraps(func)
    def wrapper(xmlschema, xpath, namespaces):
        """
        This function produces a hash from all the arguments modifying the behaviour of the wrapped function
        and looks up results in dict based on this hash. If the version of the schema
        is different than before or the dict contains more than 1024 entries the cache is cleared
        """

        version = str(xmlschema.xpath('/xsd:schema/@version', namespaces=namespaces)[0])
        root_tag = str(xmlschema.xpath('/xsd:schema/xsd:element/@name', namespaces=namespaces)[0])

        arg_tuple = (version, root_tag, xpath, *namespaces.values())

        hash_args = hash(arg_tuple)
        if version not in results:
            results.clear()
            results[version] = {}

        if hash_args not in results[version]:
            res = func(xmlschema, xpath, namespaces)
            if len(results[version]) >= 1024:
                results[version].clear()
                return res
            results[version][hash_args] = res

        return results[version][hash_args].copy()

    return wrapper


@_cache_xpath_eval
def _xpath_eval(xmlschema, xpath, namespaces):
    """
    Wrapper around the xpath calls in this module. Used for caching the
    results

    :param xmlschema: xmltree representing the schema
    :param xpath: str, xpath expression to evaluate
    :param namespaces: dictionary with the defined namespaces
    """
    return xmlschema.xpath(xpath, namespaces=namespaces)


def _get_base_types():
    """
    The types defined here should not be reduced further and are associated with one clear base type
    AngularMomentumNumberType and MainQuantumNumberType are here because they are integers
    but are implemented as xsd:string with a regex
    """
    base_types = {}
    base_types['switch'] = ['FleurBool']
    base_types['int'] = [
        'xsd:nonNegativeInteger', 'xsd:positiveInteger', 'xsd:integer', 'AngularMomentumNumberType',
        'MainQuantumNumberType'
    ]
    base_types['float'] = ['xsd:double']
    base_types['float_expression'] = ['FleurDouble']
    base_types['string'] = ['xsd:string']

    return base_types


def _remove_xsd_namespace(tag, namespaces):
    """
    Strips the xsd namespace prefix from tags to make the functions more understandable

    :param tag: tag containing the xsd namespace prefix
    :param namespaces: dictionary with the defined namespaces

    :return: tag with the xsd namespace removed
    """
    return tag.replace(f"{'{'}{namespaces['xsd']}{'}'}", '')


def _get_parent_fleur_type(elem, namespaces, stop_non_unique=False):
    """
    Returns the parent simple or complexType to the given element
    If stop_sequence is given and True None is returned when a sequence is encountered
    in the parent chain

    :param elem: etree element, starting element
    :param namespaces: dictionary with the defined namespaces
    :param stop_sequence: If a sequence is encountered in the loop it alos terminates

    :return: the element of the parent type and the tag of the parent type with the namespaces removed
    """
    valid_end_types = ['simpleType', 'complexType', 'group']
    parent = elem.getparent()
    parent_type = _remove_xsd_namespace(parent.tag, namespaces)
    if stop_non_unique:
        if 'maxOccurs' in parent.attrib:
            if parent.attrib['maxOccurs'] != '1':
                return None, None
    while parent_type not in valid_end_types:
        parent = parent.getparent()
        parent_type = _remove_xsd_namespace(parent.tag, namespaces)
        if stop_non_unique:
            if 'maxOccurs' in parent.attrib:
                if parent.attrib['maxOccurs'] != '1':
                    return None, None
    return parent, parent_type


def _analyse_type_elem(xmlschema, namespaces, type_elem, base_types, convert_to_base=True, basic_types_mapping=None):
    """
    Analyses the given type element to deduce its base_types

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces
    :param type_elem: etree element of the type to analyse
    :param base_types: dict with all types, which can be mapped directly to a base_type
    :param convert_to_base: if True all possible types are converted to their base_types using either base_types
                            or basic_types_mapping
    :param basic_types_mapping: dictionary with definitions of basic_types (used for the ouputschema to get the
                                definitions from the inputschema)

    :return: list of valid base_types
    """

    possible_base_types = []

    for child in type_elem:
        child_type = _remove_xsd_namespace(child.tag, namespaces)

        base_type_list = None
        if child_type in ['restriction', 'extension']:
            base_type_list = [child.attrib['base']]
        elif child_type == 'list':
            base_type_list = [child.attrib['itemType']]
        elif child_type == 'union' and 'memberTypes' in child.attrib:
            base_type_list = child.attrib['memberTypes'].split(' ')
        elif child_type in ['union', 'simpleType']:
            possible_base_types_new = _analyse_type_elem(xmlschema,
                                                         namespaces,
                                                         child,
                                                         base_types,
                                                         convert_to_base=False,
                                                         basic_types_mapping=basic_types_mapping)
            for base_type in possible_base_types_new:
                possible_base_types.append(base_type)

        if base_type_list is not None:
            for detected_base_type in base_type_list:
                is_base = False
                for type_names in base_types.values():
                    if detected_base_type in type_names:
                        is_base = True
                if not is_base:  #We need to go deeper
                    if basic_types_mapping is not None:
                        if detected_base_type in basic_types_mapping:
                            possible_base_types.append(detected_base_type)
                    else:
                        next_type_elems = _xpath_eval(xmlschema,
                                                      f"//xsd:simpleType[@name='{detected_base_type}']",
                                                      namespaces=namespaces)
                        if len(next_type_elems) == 0:
                            next_type_elems = _xpath_eval(
                                xmlschema,
                                f"//xsd:complexType[@name='{detected_base_type}']/xsd:simpleContent",
                                namespaces=namespaces)
                            if len(next_type_elems) == 0:
                                raise ValueError('No such type')
                        next_type_elems = next_type_elems[0]
                        possible_base_types_new = _analyse_type_elem(xmlschema,
                                                                     namespaces,
                                                                     next_type_elems,
                                                                     base_types,
                                                                     convert_to_base=False,
                                                                     basic_types_mapping=basic_types_mapping)

                        for base_type in possible_base_types_new:
                            possible_base_types.append(base_type)
                else:
                    if detected_base_type not in possible_base_types:
                        possible_base_types.append(detected_base_type)

    return_types = []
    if convert_to_base:
        if basic_types_mapping is not None:
            length = None
            for index, type_name in enumerate(possible_base_types):
                if type_name in basic_types_mapping:
                    map_types = basic_types_mapping[type_name]['base_types']
                    if length is None:
                        length = basic_types_mapping[type_name]['length']
                    if not isinstance(map_types, list):
                        map_types = [map_types]
                    for map_type in map_types:
                        if map_type not in return_types:
                            return_types.append(map_type)
            return return_types, length
        else:
            for type_name in possible_base_types:
                for base_type, type_names in base_types.items():
                    if type_name in type_names and base_type not in return_types:
                        return_types.append(base_type)
    else:
        return_types = possible_base_types

    return return_types


def _get_length(xmlschema, namespaces, type_name):
    """
    Analyse the given type to determine, whether there is a length restriction

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces
    :param type_name: name of the type to analyse

    :return: if a length restriction is found return the value,
             if a list with no restriction is found return 'unbounded',
             if neither are found return 1
    """
    type_elem = _xpath_eval(xmlschema, f"//xsd:simpleType[@name='{type_name}']", namespaces=namespaces)
    if len(type_elem) == 0:
        #I know that this is not general but this is the only other case than simpleType, which occurs at the moment
        type_elem = _xpath_eval(xmlschema,
                                f"//xsd:complexType[@name='{type_name}']/xsd:simpleContent/xsd:extension/@base",
                                namespaces=namespaces)
        if len(type_elem) == 0:
            return 1
        length = _get_length(xmlschema, namespaces, type_elem[0])
        return length

    child = type_elem[0].getchildren()
    if len(child) != 1:
        return 1
    child = child[0]

    child_type = _remove_xsd_namespace(child.tag, namespaces)

    if child_type == 'restriction':
        for restriction_child in child:
            restr_type = _remove_xsd_namespace(restriction_child.tag, namespaces)
            if restr_type == 'length':
                return int(restriction_child.attrib['value'])
    elif child_type == 'list':
        return 'unbounded'

    return 1


@_cache_xpath_construction
def _get_xpath(xmlschema,
               namespaces,
               tag_name,
               enforce_end_type=None,
               ref=None,
               stop_non_unique=False,
               stop_iteration=False,
               iteration_root=False):
    """
    construct all possible simple xpaths to a given tag

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces
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

    possible_paths = set()
    if enforce_end_type in _RECURSIVE_TYPES:
        return possible_paths
    root_tag = get_root_tag(xmlschema, namespaces)
    if tag_name == root_tag:
        if not iteration_root:
            possible_paths.add(f'/{root_tag}')
        return possible_paths

    #Get all possible starting points
    if ref is not None:
        startPoints = _xpath_eval(xmlschema, f"//xsd:group[@ref='{ref}']", namespaces=namespaces)
    else:
        if enforce_end_type is None:
            startPoints = _xpath_eval(xmlschema, f"//xsd:element[@name='{tag_name}']", namespaces=namespaces)
        else:
            startPoints = _xpath_eval(xmlschema,
                                      f"//xsd:element[@name='{tag_name}' and @type='{enforce_end_type}']",
                                      namespaces=namespaces)
    if stop_non_unique:
        startPoints_copy = startPoints.copy()
        for point in startPoints_copy:
            if 'maxOccurs' in point.attrib:
                if point.attrib['maxOccurs'] != '1':
                    startPoints.remove(point)
    for elem in startPoints:
        currentelem = elem
        currentTag = tag_name
        parent_type, parent_tag = _get_parent_fleur_type(currentelem, namespaces, stop_non_unique=stop_non_unique)
        if parent_type is None:
            continue
        next_type = parent_type.attrib['name']

        if next_type == _ITERATION_TYPE:
            if stop_iteration:
                continue
            if iteration_root:
                possible_paths.add(f'./{currentTag}')
                return possible_paths

        if parent_tag == 'group':
            possible_paths_group = _get_xpath(xmlschema,
                                              namespaces,
                                              currentTag,
                                              ref=next_type,
                                              stop_non_unique=stop_non_unique,
                                              stop_iteration=stop_iteration,
                                              iteration_root=iteration_root)
            for grouppath in possible_paths_group:
                possible_paths.add(grouppath)
        else:
            if stop_non_unique:
                currentelem = _xpath_eval(
                    xmlschema,
                    f"//xsd:element[@type='{next_type}' and @maxOccurs=1] | //xsd:element[@type='{next_type}' and not(@maxOccurs)]",
                    namespaces=namespaces)
            else:
                currentelem = _xpath_eval(xmlschema, f"//xsd:element[@type='{next_type}']", namespaces=namespaces)

            if len(currentelem) == 0:
                continue
            for new_elem in currentelem:
                newTag = new_elem.attrib['name']
                possible_paths_tag = _get_xpath(xmlschema,
                                                namespaces,
                                                newTag,
                                                enforce_end_type=next_type,
                                                stop_non_unique=stop_non_unique,
                                                stop_iteration=stop_iteration,
                                                iteration_root=iteration_root)
                for tagpath in possible_paths_tag:
                    possible_paths.add(f'{tagpath}/{tag_name}')

    if iteration_root:
        #Remove any path that slipped through and contains the root tag of the out file
        possible_paths_copy = possible_paths.copy()
        for path in possible_paths_copy:
            if root_tag in path:
                possible_paths.discard(path)

    return possible_paths


def _get_contained_attribs(xmlschema, namespaces, elem, optional=False):
    """
    Get all defined attributes contained in the given etree Element of the schema

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces
    :param elem: etree Element to analyse
    :param optional: bool, if True only the attributes which have use='optional'
                     are added and their default value (defaults to None) is returned in a
                     :py:class:`masci_tools.util.case_insensitive_dict.CaseInsensitiveDict`

    :raises: AssertionError if case insensitivity lead to lost information

    :returns: CaseInsensitiveDict (optional=True) or CaseInsensitiveFrozenSet with
              the attribute names
    """
    attrib_list = []
    for child in elem:
        child_type = _remove_xsd_namespace(child.tag, namespaces)

        if child_type == 'attribute':
            if optional and child.attrib.get('use', 'required') == 'optional':
                name = child.attrib['name']
                default = child.attrib.get('default', None)
                attrib_list.append((name, default))
            elif not optional:
                attrib_list.append(child.attrib['name'])
        elif child_type in ['simpleContent', 'extension']:
            new_attribs = _get_contained_attribs(xmlschema, namespaces, child, optional=optional)
            if optional:
                for entry in new_attribs.items():
                    attrib_list.append(entry)
            else:
                for attrib in new_attribs:
                    attrib_list.append(new_attribs.original_case[attrib])

    if not optional:
        attrib_res = CaseInsensitiveFrozenSet(attrib_list)
        assert len(set(attrib_list)) == len(attrib_res), f'Lost Information: {attrib_list}'
    else:
        attrib_res = CaseInsensitiveDict(attrib_list)

    return attrib_res


def _get_optional_tags(xmlschema, namespaces, elem):
    """
    Get all defined tags contained in the given etree Element of the schema
    with minOccurs=0

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces
    :param elem: etree Element to analyse

    :raises: AssertionError if case insensitivity lead to lost information

    :returns: CaseInsensitiveFrozenSet with the tag names
    """
    optional_list = []
    for child in elem:
        child_type = _remove_xsd_namespace(child.tag, namespaces)

        if child_type == 'element':
            if 'minOccurs' in child.attrib:
                if child.attrib['minOccurs'] == '0':
                    optional_list.append(child.attrib['name'])
        elif child_type in ['sequence', 'all', 'choice']:
            new_optionals = _get_optional_tags(xmlschema, namespaces, child)
            for opt in new_optionals:
                optional_list.append(new_optionals.original_case[opt])

    optional_set = CaseInsensitiveFrozenSet(optional_list)
    assert len(set(optional_list)) == len(optional_set), f'Lost Information: {optional_list}'

    return optional_set


def _is_simple(namespaces, elem):
    """
    Determine if a given etree element is simple (only contains attributes or text (no sub elements))

    :param namespaces: dictionary with the defined namespaces
    :param elem: etree Element to analyse

    :raises: ValueError if an unknown type is encountered

    :returns: bool determining, whether the element is simple
    """
    simple = True
    for child in elem:
        child_type = _remove_xsd_namespace(child.tag, namespaces)

        if child_type in ['attribute', 'simpleContent']:
            continue
        if child_type in ['element', 'sequence', 'choice', 'all']:
            simple = False
        else:
            raise ValueError(f"Don't know what to do with '{child_type}'")

    return simple


def _get_simple_tags(xmlschema, namespaces, elem, input_mapping=None):
    """
    Get all defined tags contained in the given etree Element of the schema
    which can only contain attributes or text (no sub elements)

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces
    :param elem: etree Element to analyse
    :param input_mapping: dict, with the defined types from the input schema

    :raises: AssertionError if case insensitivity lead to lost information

    :returns: CaseInsensitiveFrozenSet with the tag names
    """

    if input_mapping is None:
        input_mapping = {}

    simple_list = []
    for child in elem:
        child_type = _remove_xsd_namespace(child.tag, namespaces)

        if child_type == 'element':
            if child.attrib['type'] == _INPUT_TYPE:
                continue
            if child.attrib['type'] in input_mapping:
                simple_list.append(child.attrib['name'])
                continue

            type_elem = _xpath_eval(xmlschema,
                                    f"//xsd:simpleType[@name='{child.attrib['type']}']",
                                    namespaces=namespaces)
            if len(type_elem) != 0:
                simple_list.append(child.attrib['name'])
            else:
                type_elem = _xpath_eval(xmlschema,
                                        f"//xsd:complexType[@name='{child.attrib['type']}']",
                                        namespaces=namespaces)
                if len(type_elem) == 0:
                    simple_list.append(child.attrib['name'])
                elif _is_simple(namespaces, type_elem[0]):
                    simple_list.append(child.attrib['name'])
        elif child_type in ['sequence', 'all', 'choice']:
            new_simple = _get_simple_tags(xmlschema, namespaces, child)
            for simple in new_simple:
                simple_list.append(new_simple.original_case[simple])

    simple_set = CaseInsensitiveFrozenSet(simple_list)
    assert len(set(simple_list)) == len(simple_set), f'Lost Information: {simple_list}'

    return simple_set


def _get_several_tags(xmlschema, namespaces, elem):
    """
    Get all defined tags contained in the given etree Element of the schema
    which can occur multiple times (maxOccurs!=1)

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces
    :param elem: etree Element to analyse

    :raises: AssertionError if case insensitivity lead to lost information

    :returns: CaseInsensitiveFrozenSet with the tag names
    """
    several_list = []
    for child in elem:
        child_type = _remove_xsd_namespace(child.tag, namespaces)

        if child_type == 'element':
            if 'maxOccurs' in child.attrib:
                if child.attrib['maxOccurs'] != '1':
                    several_list.append(child.attrib['name'])
        elif child_type in ['sequence', 'all', 'choice']:
            if 'maxOccurs' in child.attrib:
                if child.attrib['maxOccurs'] != '1':
                    new_several = _get_sequence_order(xmlschema, namespaces, child)
                    for tag in new_several:
                        several_list.append(tag)
            else:
                new_several = _get_several_tags(xmlschema, namespaces, child)
                for tag in new_several:
                    several_list.append(new_several.original_case[tag])

    several_set = CaseInsensitiveFrozenSet(several_list)
    assert len(set(several_list)) == len(several_set), f'Lost Information: {several_list}'

    return several_set


def _get_text_tags(xmlschema, namespaces, elem, simple_elements):
    """
    Get all defined tags contained in the given etree Element of the schema
    which can contain text

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces
    :param elem: etree Element to analyse
    :param simple_elements: dict with all known types of test elements

    :raises: AssertionError if case insensitivity lead to lost information

    :returns: CaseInsensitiveFrozenSet with the tag names
    """
    text_list = []
    for child in elem:
        child_type = _remove_xsd_namespace(child.tag, namespaces)

        if child_type == 'element':
            if child.attrib['name'] in simple_elements:
                text_list.append(child.attrib['name'])
        elif child_type in ['sequence', 'all', 'choice']:
            new_tags = _get_text_tags(xmlschema, namespaces, child, simple_elements)
            for tag in new_tags:
                text_list.append(new_tags.original_case[tag])

    text_set = CaseInsensitiveFrozenSet(text_list)
    assert len(set(text_list)) == len(text_set), f'Lost Information: {text_list}'

    return text_set


@_cache_xpath_construction
def _get_attrib_xpath(xmlschema,
                      namespaces,
                      attrib_name,
                      stop_non_unique=False,
                      stop_iteration=False,
                      iteration_root=False):
    """
    construct all possible simple xpaths to a given attribute

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces
    :param attrib_name: name of the attribute
    :param stop_non_unique: If True all paths, where one tag has maxOccurs!=1 is discarded
    :param stop_iteration: If True the path generation discards all paths going through a iteration element
    :param iteration_root: If True the path generation only generates paths going through a iteration but
                       terminates as if the iteration element is the root of the file
    :return: None if no path is found, if a single path is found return the string of the path,
             otherwise a list with all possible paths is returned
    """
    possible_paths = set()
    attribute_tags = _xpath_eval(xmlschema, f"//xsd:attribute[@name='{attrib_name}']", namespaces=namespaces)
    for attrib in attribute_tags:
        parent_type, parent_tag = _get_parent_fleur_type(attrib, namespaces, stop_non_unique=stop_non_unique)
        if parent_type is None:
            continue

        start_type = parent_type.attrib['name']
        if start_type == _ITERATION_TYPE:
            if stop_iteration:
                continue
            if iteration_root:
                possible_paths.add(f'./@{attrib_name}')
                continue

        if stop_non_unique:
            element_tags = _xpath_eval(
                xmlschema,
                f"//xsd:element[@type='{start_type}' and @maxOccurs=1]/@name | //xsd:element[@type='{start_type}' and not(@maxOccurs)]/@name",
                namespaces=namespaces)
        else:
            element_tags = _xpath_eval(xmlschema, f"//xsd:element[@type='{start_type}']/@name", namespaces=namespaces)

        for tag in element_tags:
            tag_paths = _get_xpath(xmlschema,
                                   namespaces,
                                   tag,
                                   enforce_end_type=start_type,
                                   stop_non_unique=stop_non_unique,
                                   stop_iteration=stop_iteration,
                                   iteration_root=iteration_root)
            for path in tag_paths:
                possible_paths.add(f'{path}/@{attrib_name}')

    return possible_paths


def _get_sequence_order(xmlschema, namespaces, sequence_elem):
    """
    Extract the enforced order of elements in the given sequence element

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces
    :param sequence_elem: element of the sequence to analyse

    :return: list of tags, in the order they have to occur in
    """
    elem_order = []
    for child in sequence_elem:
        child_type = _remove_xsd_namespace(child.tag, namespaces)

        if child_type == 'element':
            elem_order.append(child.attrib['name'])
        elif child_type in ['choice', 'sequence']:
            new_order = _get_sequence_order(xmlschema, namespaces, child)
            for elem in new_order:
                elem_order.append(elem)
        elif child_type == 'group':
            group = _xpath_eval(xmlschema,
                                f"//xsd:group[@name='{child.attrib['ref']}']/xsd:sequence",
                                namespaces=namespaces)
            new_order = _get_sequence_order(xmlschema, namespaces, group[0])
            for elem in new_order:
                elem_order.append(elem)
        elif child_type in ['attribute', 'simpleContent', 'all']:
            continue
        else:
            raise KeyError(f'Dont know what to do with {child_type}')

    return elem_order


def _get_valid_tags(xmlschema, namespaces, sequence_elem):
    """
    Extract all allowed elements in the given sequence element

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces
    :param sequence_elem: element of the sequence to analyse

    :return: list of tags, in the order they have to occur in
    """
    elems = []
    for child in sequence_elem:
        child_type = _remove_xsd_namespace(child.tag, namespaces)

        if child_type == 'element':
            elems.append(child.attrib['name'])
        elif child_type in ['choice', 'sequence', 'all']:
            new_elems = _get_valid_tags(xmlschema, namespaces, child)
            for elem in new_elems:
                elems.append(elem)
        elif child_type == 'group':
            group = _xpath_eval(xmlschema,
                                f"//xsd:group[@name='{child.attrib['ref']}']/xsd:sequence",
                                namespaces=namespaces)
            new_elems = _get_valid_tags(xmlschema, namespaces, group[0])
            for elem in new_elems:
                elems.append(elem)
        elif child_type in ['attribute', 'simpleContent']:
            continue
        else:
            raise KeyError(f'Dont know what to do with {child_type}')

    return elems


def extract_attribute_types(xmlschema, namespaces, **kwargs):
    """
    Determine the required type of all attributes

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: possible types of the attributes in a dictionary, if multiple
             types are possible a list is inserted for the tag
    """
    possible_attrib = _xpath_eval(xmlschema, '//xsd:attribute', namespaces=namespaces)

    base_types = _get_base_types()

    types_dict = CaseInsensitiveDict()
    for attrib in possible_attrib:
        name_attrib = attrib.attrib['name']
        type_attrib = attrib.attrib['type']

        if name_attrib not in types_dict:
            types_dict[name_attrib] = []

        is_base = False
        for base_type, type_names in base_types.items():
            if type_attrib in type_names:
                is_base = True
                if base_type not in types_dict[name_attrib]:
                    types_dict[name_attrib].append(base_type)

        if not is_base:
            if type_attrib in kwargs['_basic_types']:
                for base_type in kwargs['_basic_types'][type_attrib]['base_types']:
                    if base_type not in types_dict[name_attrib]:
                        types_dict[name_attrib].append(base_type)
            else:
                print(f'Unsorted type:{type_attrib}')
                types_dict[name_attrib].append('unknown')
        if 'string' in types_dict[name_attrib]:
            #This makes sure that string is always the last element (for cascading conversion)
            types_dict[name_attrib].remove('string')
            types_dict[name_attrib].append('string')

    return types_dict


def get_tag_paths(xmlschema, namespaces, **kwargs):
    """
    Determine simple xpaths to all possible tags

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: possible paths of all tags in a dictionary, if multiple
             paths are possible a list is inserted for the tag
    """

    stop_iteration = kwargs.get('stop_iteration', False)
    iteration_root = kwargs.get('iteration_root', False)

    possible_tags = set(_xpath_eval(xmlschema, '//xsd:element/@name', namespaces=namespaces))
    tag_paths = CaseInsensitiveDict()
    for tag in sorted(possible_tags):
        paths = _get_xpath(xmlschema, namespaces, tag, stop_iteration=stop_iteration, iteration_root=iteration_root)
        if len(paths) == 1:
            tag_paths[tag] = paths.pop()
        elif len(paths) != 0:
            tag_paths[tag] = sorted(paths)
    return tag_paths


def get_unique_attribs(xmlschema, namespaces, **kwargs):
    """
    Determine all attributes, which can be set through set_inpchanges in aiida_fleur
    Meaning ONE possible path and no tags in the path with maxOccurs!=1

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: dictionary with all settable attributes and the corresponding path to the tag
    """

    stop_iteration = kwargs.get('stop_iteration', False)
    iteration_root = kwargs.get('iteration_root', False)

    settable = CaseInsensitiveDict()
    possible_attrib = set(_xpath_eval(xmlschema, '//xsd:attribute/@name', namespaces=namespaces))
    for attrib in sorted(possible_attrib):
        path = _get_attrib_xpath(xmlschema,
                                 namespaces,
                                 attrib,
                                 stop_non_unique=True,
                                 stop_iteration=stop_iteration,
                                 iteration_root=iteration_root)
        if len(path) == 1:
            if attrib in settable:
                settable.pop(attrib)
            else:
                settable[attrib] = path.pop()

    for attrib in sorted(kwargs['simple_elements']):
        path = _get_xpath(xmlschema,
                          namespaces,
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


def get_unique_path_attribs(xmlschema, namespaces, **kwargs):
    """
    Determine all attributes, with multiple possible path that do have at
    least one path with all contained tags maxOccurs!=1

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

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

    settable = CaseInsensitiveDict()
    possible_attrib = set(_xpath_eval(xmlschema, '//xsd:attribute/@name', namespaces=namespaces))
    for attrib in sorted(possible_attrib):
        if attrib in kwargs[settable_key]:
            continue
        path = _get_attrib_xpath(xmlschema,
                                 namespaces,
                                 attrib,
                                 stop_non_unique=True,
                                 stop_iteration=stop_iteration,
                                 iteration_root=iteration_root)
        if len(path) != 0:
            settable[attrib] = sorted(set(settable.get(attrib, [])).union(path))

    for attrib in sorted(kwargs['simple_elements']):
        if attrib in kwargs[settable_key]:
            continue
        path = _get_xpath(xmlschema,
                          namespaces,
                          attrib,
                          stop_non_unique=True,
                          stop_iteration=stop_iteration,
                          iteration_root=iteration_root)
        if len(path) != 0:
            settable[attrib] = sorted(set(settable.get(attrib, [])).union(path))

    return settable


def get_other_attribs(xmlschema, namespaces, **kwargs):
    """
    Determine all other attributes not contained in settable or settable_contains

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

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

    other = CaseInsensitiveDict()
    possible_attrib = set(_xpath_eval(xmlschema, '//xsd:attribute/@name', namespaces=namespaces))
    for attrib in sorted(possible_attrib):
        path = _get_attrib_xpath(xmlschema,
                                 namespaces,
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

    for attrib in sorted(kwargs['simple_elements']):
        path = _get_xpath(xmlschema, namespaces, attrib, stop_iteration=stop_iteration, iteration_root=iteration_root)
        if len(path) != 0:

            if attrib in kwargs[settable_key]:
                path.discard(kwargs[settable_key][attrib])
            if attrib in kwargs[settable_contains_key]:
                for contains_path in kwargs[settable_contains_key][attrib]:
                    path.discard(contains_path)

            if len(path) != 0:
                other[attrib] = sorted(set(other.get(attrib, [])).union(path))

    return other


def get_omittable_tags(xmlschema, namespaces, **kwargs):
    """
    find tags with no attributes and, which are only used to mask a list of one other possible tag (e.g. atomSpecies)

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: list of tags, containing only a sequence of one allowed tag
    """

    possible_tags = _xpath_eval(xmlschema, '//xsd:element', namespaces=namespaces)

    omittable_tags = []
    for tag in possible_tags:
        tag_type = tag.attrib['type']
        tag_name = tag.attrib['name']

        if tag_name not in omittable_tags:
            type_elem = _xpath_eval(xmlschema, f"//xsd:complexType[@name='{tag_type}']", namespaces=namespaces)
            if len(type_elem) == 0:
                continue
            type_elem = type_elem[0]

            omittable = False
            for child in type_elem:
                child_type = _remove_xsd_namespace(child.tag, namespaces)

                if child_type == 'sequence':
                    allowed_tags = 0
                    for sequence_elem in child:
                        elem_type = _remove_xsd_namespace(sequence_elem.tag, namespaces)
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


def get_basic_elements(xmlschema, namespaces, **kwargs):
    """
    find all elements, whose type can be directly trace back to a basic_type

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: dictionary with tags and their corresponding type_definition
             meaning a dicationary with possible base types and evtl. length restriction
    """

    elements = _xpath_eval(xmlschema, '//xsd:element', namespaces=namespaces)

    base_types = _get_base_types()

    basic_elements = {}
    for elem in elements:
        name_elem = elem.attrib['name']
        type_elem = elem.attrib['type']

        is_base = False
        for base_type, type_names in base_types.items():
            if type_elem in type_names:
                is_base = True
                possible_types = [base_type]
                length = 1

        if not is_base:
            if type_elem in kwargs['_basic_types']:
                possible_types = kwargs['_basic_types'][type_elem]['base_types']
                length = kwargs['_basic_types'][type_elem]['length']
            else:
                continue

        new_dict = {}
        new_dict['type'] = possible_types
        new_dict['length'] = length

        if name_elem in basic_elements:
            for index, old_dict in enumerate(basic_elements[name_elem]):
                equal_dicts = True
                for key, value in old_dict.items():
                    if new_dict[key] != value:
                        equal_dicts = False
                if equal_dicts:
                    break
                if index == len(basic_elements[name_elem]) - 1:
                    basic_elements[name_elem].append(new_dict)

        else:
            basic_elements[name_elem] = [new_dict]

    return basic_elements


def get_basic_types(xmlschema, namespaces, **kwargs):
    """
    find all types, which can be traced back directly to a base_type

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: dictionary with type names and their corresponding type_definition
             meaning a dicationary with possible base types and evtl. length restriction
    """
    basic_type_elems = _xpath_eval(xmlschema, '//xsd:simpleType[@name]', namespaces=namespaces)
    complex_type_elems = _xpath_eval(xmlschema, '//xsd:complexType/xsd:simpleContent', namespaces=namespaces)

    for elem in complex_type_elems:
        basic_type_elems.append(elem)

    base_types = _get_base_types()
    basic_types = {}
    for type_elem in basic_type_elems:
        if 'name' in type_elem.attrib:
            name_elem = type_elem.attrib['name']
        else:
            name_elem = type_elem.getparent().attrib['name']

        is_base = False
        for base_type, type_names in base_types.items():
            if name_elem in type_names:
                is_base = True
                possible_types = [base_type]
        if is_base:
            continue  #Already done

        if 'input_basic_types' in kwargs:
            possible_types, length = _analyse_type_elem(xmlschema,
                                                        namespaces,
                                                        type_elem,
                                                        base_types,
                                                        basic_types_mapping=kwargs['input_basic_types'])
            if len(possible_types) == 0:
                possible_types = _analyse_type_elem(xmlschema, namespaces, type_elem, base_types)
            if length is None:
                length = _get_length(xmlschema, namespaces, name_elem)
        else:
            possible_types = _analyse_type_elem(xmlschema, namespaces, type_elem, base_types)
            length = _get_length(xmlschema, namespaces, name_elem)

        if type_elem not in basic_types:
            basic_types[name_elem] = {}
            basic_types[name_elem]['base_types'] = possible_types
            basic_types[name_elem]['length'] = length

    #Append the definitions form the inputschema since including it directly is very messy
    if 'input_basic_types' in kwargs:
        for key, value in kwargs['input_basic_types'].items():
            if key not in basic_types:
                basic_types[key] = value
    return basic_types


def get_tag_info(xmlschema, namespaces, **kwargs):
    """
    Get all important information about the tags
        - allowed attributes
        - contained tags (simple (only attributes), optional (with default values), several, order, text tags)

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: dictionary with the tag information
    """

    stop_iteration = kwargs.get('stop_iteration', False)
    iteration_root = kwargs.get('iteration_root', False)

    tag_info = {}

    possible_tags = _xpath_eval(xmlschema, '//xsd:element', namespaces=namespaces)

    for tag in possible_tags:

        name_tag = tag.attrib['name']
        type_tag = tag.attrib['type']

        #Get the xpath for this tag
        tag_path = _get_xpath(xmlschema,
                              namespaces,
                              name_tag,
                              enforce_end_type=type_tag,
                              stop_iteration=stop_iteration,
                              iteration_root=iteration_root)

        tag_path = list(tag_path)

        type_elem = _xpath_eval(xmlschema, f"//xsd:complexType[@name='{type_tag}']", namespaces=namespaces)
        if len(type_elem) == 0:
            continue
        type_elem = type_elem[0]

        info_dict = {}
        info_dict['attribs'] = _get_contained_attribs(xmlschema, namespaces, type_elem)
        info_dict['optional_attribs'] = _get_contained_attribs(xmlschema, namespaces, type_elem, optional=True)
        info_dict['optional'] = _get_optional_tags(xmlschema, namespaces, type_elem)
        info_dict['several'] = _get_several_tags(xmlschema, namespaces, type_elem)
        info_dict['order'] = _get_sequence_order(xmlschema, namespaces, type_elem)
        info_dict['simple'] = _get_simple_tags(xmlschema,
                                               namespaces,
                                               type_elem,
                                               input_mapping=kwargs.get('_input_basic_types', None))
        valid_tags = _get_valid_tags(xmlschema, namespaces, type_elem)
        info_dict['complex'] = CaseInsensitiveFrozenSet(valid_tags).difference(info_dict['simple'])
        info_dict['text'] = _get_text_tags(xmlschema, namespaces, type_elem, kwargs['simple_elements'])

        if any(len(elem) != 0 for elem in info_dict.values()):
            for path in tag_path:
                tag_info[path] = info_dict

    return tag_info


def get_root_tag(xmlschema, namespaces, **kwargs):
    """
    Returns the tag for the root element of the xmlschema

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: name of the single element defined in the first level of the schema
    """
    return str(_xpath_eval(xmlschema, '/xsd:schema/xsd:element/@name', namespaces=namespaces)[0])


def get_input_tag(xmlschema, namespaces, **kwargs):
    """
    Returns the tag for the input type element of the outxmlschema

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: name of the element with the type 'FleurInputType'
    """
    return str(_xpath_eval(xmlschema, f"//xsd:element[@type='{_INPUT_TYPE}']/@name", namespaces=namespaces)[0])
