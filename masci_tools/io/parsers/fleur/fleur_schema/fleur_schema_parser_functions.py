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
functions to extract information about the fleur schema input or output
"""
from __future__ import absolute_import
from __future__ import print_function
from lxml import etree


def get_base_types():
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


def remove_xsd_namespace(tag, namespaces):
    """
    Strips the xsd namespace prefix from tags to make the functions more understandable

    :param tag: tag containing the xsd namespace prefix
    :param namespaces: dictionary with the defined namespaces

    :return: tag with the xsd namespace removed
    """
    return tag.replace(f"{'{'}{namespaces['xsd']}{'}'}", '')


def get_parent_fleur_type(elem, namespaces, stop_sequence=False):
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
    if stop_sequence:
        valid_end_types.append('sequence')
    parent = elem.getparent()
    parent_type = remove_xsd_namespace(parent.tag, namespaces)
    while parent_type not in valid_end_types:
        parent = parent.getparent()
        parent_type = remove_xsd_namespace(parent.tag, namespaces)
    return parent, parent_type


def get_root_tag(xmlschema, namespaces):
    """
    Returns the tag for the root element of the xmlschema

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: name of the single element defined in the first level of the schema
    """
    return xmlschema.xpath('/xsd:schema/xsd:element/@name', namespaces=namespaces)[0]


def analyse_type_elem(xmlschema, namespaces, type_elem, base_types, convert_to_base=True, basic_types_mapping=None):
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
        child_type = remove_xsd_namespace(child.tag, namespaces)

        base_type_list = None
        if child_type in ['restriction', 'extension']:
            base_type_list = [child.attrib['base']]
        elif child_type == 'list':
            base_type_list = [child.attrib['itemType']]
        elif child_type == 'union' and 'memberTypes' in child.attrib:
            base_type_list = child.attrib['memberTypes'].split(' ')
        elif child_type in ['union', 'simpleType']:
            possible_base_types_new = analyse_type_elem(xmlschema,
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
                        next_type_elems = xmlschema.xpath(f"//xsd:simpleType[@name='{detected_base_type}']",
                                                          namespaces=namespaces)
                        if len(next_type_elems) == 0:
                            next_type_elems = xmlschema.xpath(
                                f"//xsd:complexType[@name='{detected_base_type}']/xsd:simpleContent",
                                namespaces=namespaces)
                            if len(next_type_elems) == 0:
                                raise ValueError('No such type')
                        next_type_elems = next_type_elems[0]
                        possible_base_types_new = analyse_type_elem(xmlschema,
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


def get_length(xmlschema, namespaces, type_name):
    """
    Analyse the given type to determine, whether there is a length restriction

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces
    :param type_name: name of the type to analyse

    :return: if a length restriction is found return the value,
             if a list with no restriction is found return 'unbounded',
             if neither are found return 1
    """
    type_elem = xmlschema.xpath(f"//xsd:simpleType[@name='{type_name}']", namespaces=namespaces)
    if len(type_elem) == 0:
        #I know that this is not general but this is the only other case than simpleType, which occurs at the moment
        type_elem = xmlschema.xpath(f"//xsd:complexType[@name='{type_name}']/xsd:simpleContent/xsd:extension/@base",
                                    namespaces=namespaces)
        if len(type_elem) == 0:
            return 1
        length = get_length(xmlschema, namespaces, type_elem[0])
        return length

    child = type_elem[0].getchildren()
    if len(child) != 1:
        return 1
    child = child[0]

    child_type = remove_xsd_namespace(child.tag, namespaces)

    if child_type == 'restriction':
        for restriction_child in child:
            restr_type = remove_xsd_namespace(restriction_child.tag, namespaces)
            if restr_type == 'length':
                return int(restriction_child.attrib['value'])
    elif child_type == 'list':
        return 'unbounded'

    return 1


def get_xpath(xmlschema,
              namespaces,
              tag_name,
              enforce_end_type=None,
              ref=None,
              stop_non_unique=False,
              stop_group=False,
              group_root=False):
    """
    construct all possible simple xpaths to a given tag

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces
    :param tag_name: name of the starting tag
    :param enforce_end_type: If given the type of the starting tag has o match this string
    :param ref: If given we start from a group reference with this name
    :param stop_non_unique: If True all paths, where one tag has maxOccurs!=1 is discarded
    :param stop_group: If True the path generation discards all paths going through a group element
    :param group_root: If True the path generation only generates paths going through a group but
                       terminates as if the group element is the root of the file
    :return: None if no path is found, if a single path is found return the string of the path,
             otherwise a list with all possible paths is returned
    """
    skip = ['CompositeTimerType']  #These types have infinite recursive paths and CANNOT BE PARSED
    if enforce_end_type in skip:
        return None
    possible_paths = []
    root_tag = get_root_tag(xmlschema, namespaces)
    if tag_name == root_tag:
        if group_root:
            return None
        else:
            return f'/{root_tag}'
    #Get all possible starting points
    if ref is not None:
        startPoints = xmlschema.xpath(f"//xsd:group[@ref='{ref}']", namespaces=namespaces)
    else:
        if enforce_end_type is None:
            startPoints = xmlschema.xpath(f"//xsd:element[@name='{tag_name}']", namespaces=namespaces)
        else:
            startPoints = xmlschema.xpath(f"//xsd:element[@name='{tag_name}' and @type='{enforce_end_type}']",
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
        parent_type, parent_tag = get_parent_fleur_type(currentelem, namespaces)
        next_type = parent_type.attrib['name']
        if parent_tag == 'group':
            if stop_group:
                continue
            if group_root:
                return f'/{currentTag}'
            possible_paths_group = get_xpath(xmlschema,
                                             namespaces,
                                             currentTag,
                                             ref=next_type,
                                             stop_non_unique=stop_non_unique,
                                             stop_group=stop_group,
                                             group_root=group_root)
            if possible_paths_group is None:
                continue
            if not isinstance(possible_paths_group, list):
                possible_paths_group = [possible_paths_group]
            for grouppath in possible_paths_group:
                if f'{grouppath}' not in possible_paths:
                    possible_paths.append(f'{grouppath}')
        else:
            if stop_non_unique:
                currentelem = xmlschema.xpath(
                    f"//xsd:element[@type='{next_type}' and @maxOccurs=1] | //xsd:element[@type='{next_type}' and not(@maxOccurs)]",
                    namespaces=namespaces)
            else:
                currentelem = xmlschema.xpath(f"//xsd:element[@type='{next_type}']", namespaces=namespaces)

            if len(currentelem) == 0:
                continue
            for new_elem in currentelem:
                newTag = new_elem.attrib['name']
                possible_paths_tag = get_xpath(xmlschema,
                                               namespaces,
                                               newTag,
                                               enforce_end_type=next_type,
                                               stop_non_unique=stop_non_unique,
                                               stop_group=stop_group,
                                               group_root=group_root)
                if possible_paths_tag is None:
                    continue
                if not isinstance(possible_paths_tag, list):
                    possible_paths_tag = [possible_paths_tag]
                for tagpath in possible_paths_tag:
                    if f'{tagpath}/{tag_name}' not in possible_paths:
                        possible_paths.append(f'{tagpath}/{tag_name}')

    if group_root:
        possible_paths_copy = possible_paths.copy()
        for path in possible_paths_copy:
            if root_tag in path:
                possible_paths.remove(path)

    if len(possible_paths) > 1:
        return possible_paths
    elif len(possible_paths) == 0:
        return None
    else:
        return possible_paths[0]

def get_contained_attribs(xmlschema, namespaces, elem):

    attrib_list = []
    for child in elem:
        child_type = remove_xsd_namespace(child.tag, namespaces)

        if child_type == 'attribute':
            attrib_list.append(child.attrib['name'])
        elif child_type in ['simpleContent', 'extension']:
            new_attribs = get_contained_attribs(xmlschema, namespaces, child)
            for attrib in new_attribs:
                attrib_list.append(attrib)

    return attrib_list

def get_optional_tags(xmlschema, namespaces, elem):

    optional_list = []
    for child in elem:
        child_type = remove_xsd_namespace(child.tag, namespaces)

        if child_type == 'element':
            if 'minOccurs' in child.attrib:
                if child.attrib['minOccurs'] == '0':
                    optional_list.append(child.attrib['name'])
        elif child_type in ['sequence', 'all', 'choice']:
            new_optionals = get_optional_tags(xmlschema, namespaces, child)
            for opt in new_optionals:
                optional_list.append(opt)

    return optional_list

def get_several_tags(xmlschema, namespaces, elem):

    several_list = []
    for child in elem:
        child_type = remove_xsd_namespace(child.tag, namespaces)

        if child_type == 'element':
            if 'maxOccurs' in child.attrib:
                if child.attrib['maxOccurs'] != '1':
                    several_list.append(child.attrib['name'])
        elif child_type in ['sequence', 'all', 'choice']:
            if 'maxOccurs' in child.attrib:
                if child.attrib['maxOccurs'] != '1':
                    new_several = get_sequence_order(xmlschema, namespaces, child)
                    for tag in new_several:
                        several_list.append(tag)
            else:
                new_several = get_several_tags(xmlschema, namespaces, child)
                for tag in new_several:
                    several_list.append(tag)

    return several_list

def get_attrib_xpath(xmlschema, namespaces, attrib_name, stop_non_unique=False, stop_group=False, group_root=False):
    """
    construct all possible simple xpaths to a given attribute

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces
    :param attrib_name: name of the attribute
    :param stop_non_unique: If True all paths, where one tag has maxOccurs!=1 is discarded
    :param stop_group: If True the path generation discards all paths going through a group element
    :param group_root: If True the path generation only generates paths going through a group but
                       terminates as if the group element is the root of the file
    :return: None if no path is found, if a single path is found return the string of the path,
             otherwise a list with all possible paths is returned
    """
    possible_paths = []
    attribute_tags = xmlschema.xpath(f"//xsd:attribute[@name='{attrib_name}']", namespaces=namespaces)
    for attrib in attribute_tags:
        parent_type, parent_tag = get_parent_fleur_type(attrib, namespaces)
        start_type = parent_type.attrib['name']
        if stop_non_unique:
            element_tags = xmlschema.xpath(
                f"//xsd:element[@type='{start_type}' and @maxOccurs=1]/@name | //xsd:element[@type='{start_type}' and not(@maxOccurs)]/@name",
                namespaces=namespaces)
        else:
            element_tags = xmlschema.xpath(f"//xsd:element[@type='{start_type}']/@name", namespaces=namespaces)
        if len(element_tags) == 0:
            continue
        for tag in element_tags:
            tag_paths = get_xpath(xmlschema,
                                  namespaces,
                                  tag,
                                  enforce_end_type=start_type,
                                  stop_non_unique=stop_non_unique,
                                  stop_group=stop_group,
                                  group_root=group_root)
            if tag_paths is None:
                continue
            if not isinstance(tag_paths, list):
                tag_paths = [tag_paths]
            for path in tag_paths:
                if f'{path}/@{attrib_name}' not in possible_paths:
                    possible_paths.append(f'{path}/@{attrib_name}')
    if len(possible_paths) == 1:
        return possible_paths[0]
    elif len(possible_paths) == 0:
        return None
    else:
        return possible_paths


def get_group_tags(xmlschema, namespaces, **kwargs):
    """
    get all names of reference elements referring to a group

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: list of tags referring to a group element
    """
    group_tags = []
    group_refs = xmlschema.xpath('//xsd:group[@ref]', namespaces=namespaces)

    for ref in group_refs:
        parent_type, parent_tag = get_parent_fleur_type(ref, namespaces)
        type_ref = xmlschema.xpath(f"//xsd:element[@type='{parent_type.attrib['name']}']", namespaces=namespaces)

        for elem in type_ref:
            if elem.attrib['name'] not in group_tags:
                group_tags.append(elem.attrib['name'])
    return group_tags


def get_tags_several(xmlschema, namespaces, **kwargs):
    """
    get all tags, that have maxOccurs!=1 or a surrounding sequence/choice with maxOccurs!=1

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: list of tags, which can occur multiple times in the same place
    """
    tags_several = []
    tags = xmlschema.xpath('//xsd:*[@maxOccurs!=1]', namespaces=namespaces)
    for tag in tags:
        tag_type = remove_xsd_namespace(tag.tag, namespaces)
        if tag_type == 'element':
            name_list = [tag.attrib['name']]
        elif tag_type in ['choice', 'sequence']:
            name_list = get_sequence_order(xmlschema, namespaces, tag)
        else:
            raise ValueError(f"Don't know what to do with {tag_type}")
        for name in name_list:
            if name not in tags_several:
                tags_several.append(name)
    return tags_several


def get_sequence_order(xmlschema, namespaces, sequence_elem):
    """
    Extract the enforced order of elements in the given sequence element

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces
    :param sequence_elem: element of the sequence to analyse

    :return: list of tags, in the order they have to occur in
    """
    elem_order = []
    for child in sequence_elem:
        child_type = remove_xsd_namespace(child.tag, namespaces)

        if child_type == 'element':
            elem_order.append(child.attrib['name'])
        elif child_type in ['choice', 'sequence', 'all']:
            new_order = get_sequence_order(xmlschema, namespaces, child)
            for elem in new_order:
                elem_order.append(elem)
        elif child_type == 'group':
            group = xmlschema.xpath(f"//xsd:group[@name='{child.attrib['ref']}']/xsd:sequence", namespaces=namespaces)
            new_order = get_sequence_order(xmlschema, namespaces, group[0])
            for elem in new_order:
                elem_order.append(elem)
        elif child_type in ['attribute', 'simpleContent']:
            continue
        else:
            raise KeyError(f'Dont know what to do with {child_type}')

    return elem_order


def extract_attribute_types(xmlschema, namespaces, **kwargs):
    """
    Determine the required type of all attributes

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: possible types of the attributes in a dictionary, if multiple
             types are possible a list is inserted for the tag
    """
    possible_attrib = xmlschema.xpath('//xsd:attribute', namespaces=namespaces)

    base_types = get_base_types()

    types_dict = {}
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
            if type_attrib in kwargs['basic_types']:
                for base_type in kwargs['basic_types'][type_attrib]['base_types']:
                    if base_type not in types_dict[name_attrib]:
                        types_dict[name_attrib].append(base_type)
            else:
                print(f'Unsorted type:{type_attrib}')
                types_dict[name_attrib].append('unknown')
        if 'string' in types_dict[name_attrib]:
            #This makes sure that string is always the last element (for cascading conversion)
            types_dict[name_attrib].remove('string')
            types_dict[name_attrib].append('string')

    #For unambiguously defined types only return the element
    for key, value in types_dict.items():
        if len(types_dict[key]) == 1:
            types_dict[key] = value[0]

    return types_dict


def get_tag_paths(xmlschema, namespaces, **kwargs):
    """
    Determine simple xpaths to all possible tags

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: possible paths of all tags in a dictionary, if multiple
             paths are possible a list is inserted for the tag
    """
    possible_tags = xmlschema.xpath('//xsd:element/@name', namespaces=namespaces)
    tag_paths = {}
    for tag in possible_tags:
        paths = get_xpath(xmlschema, namespaces, tag)
        if paths is not None:
            tag_paths[tag] = paths
    return tag_paths


def get_tag_paths_outschema(xmlschema, namespaces, **kwargs):
    """
    Determine simple xpaths to all possible tags.
    Excludes path going through a group element (iteration groups)

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: possible paths of all tags in a dictionary, if multiple
             paths are possible a list is inserted for the tag
    """
    possible_tags = xmlschema.xpath('//xsd:element/@name', namespaces=namespaces)
    tag_paths = {}
    for tag in possible_tags:
        paths = get_xpath(xmlschema, namespaces, tag, stop_group=True)
        if paths is not None:
            tag_paths[tag] = paths
    return tag_paths


def get_group_paths(xmlschema, namespaces, **kwargs):
    """
    Determine simple xpaths to all possible tags.
    Only includes path going through a group element (iteration groups)
    and stops, when a group element is encountered

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: possible paths of all tags in a dictionary, if multiple
             paths are possible a list is inserted for the tag
    """
    possible_tags = xmlschema.xpath('//xsd:element/@name', namespaces=namespaces)
    tag_paths = {}
    for tag in possible_tags:
        paths = get_xpath(xmlschema, namespaces, tag, group_root=True)
        if paths is not None:
            tag_paths[tag] = paths
    return tag_paths


def get_attrib_paths_outschema(xmlschema, namespaces, **kwargs):
    """
    Determine simple xpaths to all possible attributes.
    Excludes path going through a group element (iteration groups)

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: possible paths of all tags in a dictionary, if multiple
             paths are possible a list is inserted for the tag
    """
    attrib_paths = {}
    possible_attrib = xmlschema.xpath('//xsd:attribute/@name', namespaces=namespaces)
    for attrib in possible_attrib:
        paths = get_attrib_xpath(xmlschema, namespaces, attrib, stop_group=True)
        if paths is not None:
            attrib_paths[attrib] = paths
    return attrib_paths


def get_attrib_group_paths(xmlschema, namespaces, **kwargs):
    """
    Determine simple xpaths to all possible tags.
    Only includes path going through a group element (iteration groups)
    and stops, when a group element is encountered

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: possible paths of all tags in a dictionary, if multiple
             paths are possible a list is inserted for the tag
    """
    attrib_paths = {}
    possible_attrib = xmlschema.xpath('//xsd:attribute/@name', namespaces=namespaces)
    for attrib in possible_attrib:
        paths = get_attrib_xpath(xmlschema, namespaces, attrib, group_root=True)
        if paths is not None:
            attrib_paths[attrib] = paths
    return attrib_paths


def get_attrib_paths(xmlschema, namespaces, **kwargs):
    """
    Determine simple xpaths to all possible tags

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: possible paths of all tags in a dictionary, if multiple
             paths are possible a list is inserted for the tag
    """
    attrib_paths = {}
    possible_attrib = xmlschema.xpath('//xsd:attribute/@name', namespaces=namespaces)
    for attrib in possible_attrib:
        paths = get_attrib_xpath(xmlschema, namespaces, attrib)
        if paths is not None:
            attrib_paths[attrib] = paths
    return attrib_paths


def get_tags_order(xmlschema, namespaces, **kwargs):
    """
    Determine the order of contained tags for all elements
    inclusing a sequence

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: dictionary with all tags and their corresponding order list
    """
    tag_order = {}
    sequences = xmlschema.xpath('//xsd:sequence', namespaces=namespaces)

    for sequence in sequences:
        parent, parent_tag = get_parent_fleur_type(sequence, namespaces, stop_sequence=True)
        if parent_tag == 'sequence':
            continue
        parent_type = parent.attrib['name']
        tag_name = xmlschema.xpath(f"//xsd:element[@type='{parent_type}']/@name", namespaces=namespaces)
        if tag_name:
            tag_name = tag_name[0]
        else:
            continue
        tag_order[tag_name] = get_sequence_order(xmlschema, namespaces, sequence)
    return tag_order


def get_settable_attributes(xmlschema, namespaces, **kwargs):
    """
    Determine all attributes, which can be set through set_inpchanges in aiida_fleur
    Meaning ONE possible path and no tags in the path with maxOccurs!=1

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: dictionary with all settable attributes and the corresponding path to the tag
    """
    settable = {}
    possible_attrib = xmlschema.xpath('//xsd:attribute/@name', namespaces=namespaces)
    for attrib in possible_attrib:
        path = get_attrib_xpath(xmlschema, namespaces, attrib, stop_non_unique=True)
        if path is not None and not isinstance(path, list):
            settable[attrib] = path.replace(f'/@{attrib}', '')

    for attrib, attrib_dict in kwargs['simple_elements'].items():
        path = get_xpath(xmlschema, namespaces, attrib, stop_non_unique=True)
        if path is not None:
            if not isinstance(path, list):
                settable[attrib] = path.replace(f'/@{attrib}', '')

    return settable


def get_settable_contains_attributes(xmlschema, namespaces, **kwargs):
    """
    Determine all attributes, with multiple possible path that do have at
    least one path with all contained tags maxOccurs!=1

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: dictionary with all attributes and the corresponding list of paths to the tag
    """
    settable = {}
    possible_attrib = xmlschema.xpath('//xsd:attribute/@name', namespaces=namespaces)
    for attrib in possible_attrib:
        path = get_attrib_xpath(xmlschema, namespaces, attrib, stop_non_unique=True)
        if path is not None and attrib not in kwargs['settable_attribs']:
            if not isinstance(path, list):
                path = [path]
            settable[attrib] = [x.replace(f'/@{attrib}', '') for x in path]

    for attrib, attrib_dict in kwargs['simple_elements'].items():
        path = get_xpath(xmlschema, namespaces, attrib, stop_non_unique=True)
        if path is not None:
            if not isinstance(path, list):
                path = [path]
            if attrib not in kwargs['settable_attribs']:
                settable[attrib] = [x.replace(f'/@{attrib}', '') for x in path]

    return settable


def get_omittable_tags(xmlschema, namespaces, **kwargs):
    """
    find tags with no attributes and, which are only used to mask a list of one other possible tag (e.g. atomSpecies)

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: list of tags, containing only a sequence of one allowed tag
    """

    possible_tags = xmlschema.xpath('//xsd:element', namespaces=namespaces)

    omittable_tags = []
    for tag in possible_tags:
        tag_type = tag.attrib['type']
        tag_name = tag.attrib['name']

        if tag_name not in omittable_tags:
            type_elem = xmlschema.xpath(f"//xsd:complexType[@name='{tag_type}']", namespaces=namespaces)
            if len(type_elem) == 0:
                continue
            type_elem = type_elem[0]

            omittable = False
            for child in type_elem:
                child_type = remove_xsd_namespace(child.tag, namespaces)

                if child_type == 'sequence':
                    allowed_tags = 0
                    for sequence_elem in child:
                        elem_type = remove_xsd_namespace(sequence_elem.tag, namespaces)
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

    elements = xmlschema.xpath('//xsd:element', namespaces=namespaces)

    base_types = get_base_types()

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
            if type_elem in kwargs['basic_types']:
                possible_types = kwargs['basic_types'][type_elem]['base_types']
                length = kwargs['basic_types'][type_elem]['length']
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

    for key, value in basic_elements.items():
        if len(value) == 1:
            basic_elements[key] = value[0]

    return basic_elements


def get_basic_types(xmlschema, namespaces, **kwargs):
    """
    find all types, which can be traced back directly to a base_type

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: dictionary with type names and their corresponding type_definition
             meaning a dicationary with possible base types and evtl. length restriction
    """
    basic_type_elems = xmlschema.xpath('//xsd:simpleType[@name]', namespaces=namespaces)
    complex_type_elems = xmlschema.xpath('//xsd:complexType/xsd:simpleContent', namespaces=namespaces)

    for elem in complex_type_elems:
        basic_type_elems.append(elem)

    base_types = get_base_types()
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
            possible_types, length = analyse_type_elem(xmlschema,
                                                       namespaces,
                                                       type_elem,
                                                       base_types,
                                                       basic_types_mapping=kwargs['input_basic_types'])
            if len(possible_types) == 0:
                possible_types = analyse_type_elem(xmlschema, namespaces, type_elem, base_types)
            if length is None:
                length = get_length(xmlschema, namespaces, name_elem)
        else:
            possible_types = analyse_type_elem(xmlschema, namespaces, type_elem, base_types)
            length = get_length(xmlschema, namespaces, name_elem)

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
        - contained tags (simple (only attributes), optional, several, order)

    :param xmlschema: xmltree representing the schema
    :param namespaces: dictionary with the defined namespaces

    :return: dictionary with the tag information
    """

    tag_info = {}

    possible_tags = xmlschema.xpath('//xsd:element', namespaces=namespaces)

    for tag in possible_tags:

        name_tag = tag.attrib['name']
        type_tag = tag.attrib['type']

        #Get the xpath for this tag
        tag_path = get_xpath(xmlschema, namespaces, name_tag, enforce_end_type=type_tag)

        if tag_path is None:
            continue
        if not isinstance(tag_path, list):
            tag_path = [tag_path]

        type_elem = xmlschema.xpath(f"//xsd:complexType[@name='{type_tag}']", namespaces=namespaces)
        if len(type_elem) == 0:
            continue
        type_elem = type_elem[0]


        info_dict = {}
        attrib_list = get_contained_attribs(xmlschema, namespaces, type_elem)
        if len(attrib_list) != 0:
            info_dict['attribs'] = attrib_list

        elem_list = get_optional_tags(xmlschema, namespaces, type_elem)
        if len(elem_list) != 0:
            info_dict['optional'] = elem_list

        elem_list = get_several_tags(xmlschema, namespaces, type_elem)
        if len(elem_list) != 0:
            info_dict['several'] = elem_list

        elem_list = get_sequence_order(xmlschema, namespaces, type_elem)
        if len(elem_list) != 0:
            info_dict['order'] = elem_list

        if info_dict:
            for path in tag_path:
                tag_info[path] = info_dict

    return tag_info
