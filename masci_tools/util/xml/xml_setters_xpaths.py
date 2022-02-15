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
Functions for modifying the xml input file of Fleur with explicit xpath arguments
These can still use the schema dict for finding information about the xpath
"""
from __future__ import annotations

from typing import Any, Iterable, cast
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  #type:ignore

from masci_tools.util.xml.xpathbuilder import XPathBuilder
from masci_tools.util.typing import XPathLike, XMLLike
from masci_tools.util.xml.common_functions import eval_xpath, add_tag
from masci_tools.io.parsers import fleur_schema

from lxml import etree


def xml_create_tag_schema_dict(xmltree: XMLLike,
                               schema_dict: fleur_schema.SchemaDict,
                               xpath: XPathLike,
                               base_xpath: str,
                               element: str | etree._Element,
                               create_parents: bool = False,
                               number_nodes: int = 1,
                               occurrences: int | Iterable[int] | None = None) -> XMLLike:
    """
    This method evaluates an xpath expression and creates a tag in a xmltree under the
    returned nodes.
    If there are no nodes evaluated the subtags can be created with `create_parents=True`

    The tag is always inserted in the correct place if a order is enforced by the schema

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param xpath: a path where to place a new tag
    :param base_xpath: path where to place a new tag without complex syntax ([] conditions and so on)
    :param element: a tag name or etree Element to be created
    :param create_parents: bool optional (default False), if True and the given xpath has no results the
                           the parent tags are created recursively
    :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag.
                        By default all nodes are used.
    :param number_nodes: how many identical nodes to create

    :raises ValueError: If the nodes are missing and `create_parents=False`

    :returns: xmltree with created tags
    """
    from masci_tools.util.xml.xml_setters_basic import xml_create_tag
    from masci_tools.util.xml.common_functions import check_complex_xpath, split_off_tag

    check_complex_xpath(xmltree, base_xpath, xpath)

    tag_info = schema_dict['tag_info'][base_xpath]

    if not etree.iselement(element):
        #Get original case of the tag
        element_name = (tag_info['simple'] | tag_info['complex']).original_case[element]
        try:
            element = etree.Element(element_name)
        except ValueError as exc:
            raise ValueError(f"Failed to construct etree Element from '{element_name}'") from exc
    else:
        element_name = element.tag  #type:ignore

    if len(tag_info['order']) == 0:
        tag_order = None
    else:
        tag_order = tag_info['order']

    several_tags = element_name in tag_info['several']

    if not several_tags and number_nodes > 1:
        raise ValueError(f'Can not create {number_nodes} nodes of tag {element_name}: Tag only allowed once')

    parent_nodes: list[etree._Element] = eval_xpath(xmltree, xpath, list_return=True)  #type:ignore

    if len(parent_nodes) == 0:
        if create_parents:
            parent_xpath, parent_name = split_off_tag(base_xpath)
            complex_parent_xpath, _ = split_off_tag(xpath)
            xmltree = xml_create_tag_schema_dict(xmltree,
                                                 schema_dict,
                                                 complex_parent_xpath,
                                                 parent_xpath,
                                                 parent_name,
                                                 create_parents=create_parents)
        else:
            raise ValueError(f"Could not create tag '{element_name}' because at least one subtag is missing. "
                             'Use create=True to create the subtags')

    for _ in range(number_nodes):
        xml_create_tag(xmltree, xpath, element, tag_order=tag_order, occurrences=occurrences, several=several_tags)
    return xmltree


def eval_xpath_create(xmltree: XMLLike,
                      schema_dict: fleur_schema.SchemaDict,
                      xpath: XPathLike,
                      base_xpath: str,
                      create_parents: bool = False,
                      occurrences: int | Iterable[int] | None = None,
                      number_nodes: int = 1,
                      list_return: bool = False) -> list[etree._Element]:
    """
    Evaluates and xpath and creates tag if the result is empty

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param xpath: a path where to place a new tag
    :param base_xpath: path where to place a new tag without complex syntax ([] conditions and so on)
    :param create_parents: bool optional (default False), if True also the parents of the tag are created
                           if they are missing
    :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag if the tag is missing.
                        By default all nodes are used.
    :param list_return: if True, the returned quantity is always a list even if only one element is in it
    :param number_nodes: how many identical nodes to create

    :returns: list of nodes from the result of the xpath expression
    """
    from masci_tools.util.xml.common_functions import check_complex_xpath, split_off_tag

    check_complex_xpath(xmltree, base_xpath, xpath)

    nodes: list[etree._Element] = eval_xpath(xmltree, xpath, list_return=True)  #type:ignore

    if len(nodes) == 0:
        parent_xpath, tag_name = split_off_tag(base_xpath)
        complex_parent_xpath, _ = split_off_tag(xpath)
        xmltree = xml_create_tag_schema_dict(xmltree,
                                             schema_dict,
                                             complex_parent_xpath,
                                             parent_xpath,
                                             tag_name,
                                             create_parents=create_parents,
                                             number_nodes=number_nodes,
                                             occurrences=occurrences)
        nodes = eval_xpath(xmltree, xpath, list_return=True)  #type:ignore

    if len(nodes) == 1 and not list_return:
        nodes = nodes[0]  #type:ignore

    return nodes


def xml_set_attrib_value(xmltree: XMLLike,
                         schema_dict: fleur_schema.SchemaDict,
                         xpath: XPathLike,
                         base_xpath: str,
                         attributename: str,
                         attribv: Any,
                         occurrences: int | Iterable[int] | None = None,
                         create: bool = False) -> XMLLike:
    """
    Sets an attribute in a xmltree to a given value. By default the attribute will be set
    on all nodes returned for the specified xpath.
    If there are no nodes under the specified xpath a tag can be created with `create=True`.
    The attribute values are converted automatically according to the types of the attribute
    with :py:func:`~masci_tools.util.xml.converters.convert_to_xml()` if they
    are not `str` already.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param xpath: a path where to set the attributes
    :param base_xpath: path where to place a new tag without complex syntax ([] conditions and so on)
    :param attributename: the attribute name to set
    :param attribv: value or list of values to set
    :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.
    :param create: bool optional (default False), if True the tag is created if is missing

    :raises ValueError: If the conversion to string failed
    :raises ValueError: If the tag is missing and `create=False`
    :raises ValueError: If the attributename is not allowed on the base_xpath

    :returns: xmltree with set attribute
    """

    from masci_tools.util.xml.xml_setters_basic import xml_set_attrib_value_no_create
    from masci_tools.util.xml.converters import convert_to_xml
    from masci_tools.util.xml.common_functions import check_complex_xpath, split_off_tag
    from masci_tools.io.common_functions import is_sequence

    check_complex_xpath(xmltree, base_xpath, xpath)

    _, tag_name = split_off_tag(base_xpath)

    attribs = schema_dict['tag_info'][base_xpath]['attribs']
    if attributename not in attribs:
        raise ValueError(
            f"The key '{attributename}' is not expected for this version of the input for the '{tag_name}' tag. "
            f'Allowed attributes are: {sorted(attribs.original_case.values())}')
    attributename = attribs.original_case[attributename]

    converted_attribv, _ = convert_to_xml(attribv, schema_dict, attributename, text=False)
    n_nodes = len(converted_attribv) if is_sequence(converted_attribv) else 1

    if create:
        nodes: list[etree._Element] = eval_xpath_create(xmltree,
                                                        schema_dict,
                                                        xpath,
                                                        base_xpath,
                                                        create_parents=True,
                                                        occurrences=occurrences,
                                                        number_nodes=n_nodes,
                                                        list_return=True)
    else:
        nodes = eval_xpath(xmltree, xpath, list_return=True)  #type:ignore

    if len(nodes) == 0:
        raise ValueError(
            f"Could not set attribute '{attributename}' on path '{str(xpath.path) if isinstance(xpath, XPathBuilder) else str(xpath)}' "
            'because at least one subtag is missing. '
            'Use create=True to create the subtags')

    return xml_set_attrib_value_no_create(xmltree, xpath, attributename, converted_attribv, occurrences=occurrences)


def xml_set_first_attrib_value(xmltree: XMLLike,
                               schema_dict: fleur_schema.SchemaDict,
                               xpath: XPathLike,
                               base_xpath: str,
                               attributename: str,
                               attribv: Any,
                               create: bool = False) -> XMLLike:
    """
    Sets the first occurrence attribute in a xmltree to a given value.
    If there are no nodes under the specified xpath a tag can be created with `create=True`.
    The attribute values are converted automatically according to the types of the attribute
    with :py:func:`~masci_tools.util.xml.converters.convert_to_xml()` if they
    are not `str` already.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param xpath: a path where to set the attribute
    :param base_xpath: path where to place a new tag without complex syntax ([] conditions and so on)
    :param attributename: the attribute name to set
    :param attribv: value or list of values to set
    :param create: bool optional (default False), if True the tag is created if is missing

    :raises ValueError: If the conversion to string failed
    :raises ValueError: If the tag is missing and `create=False`
    :raises ValueError: If the attributename is not allowed on the base_xpath

    :returns: xmltree with set attribute
    """

    return xml_set_attrib_value(xmltree,
                                schema_dict,
                                xpath,
                                base_xpath,
                                attributename,
                                attribv,
                                create=create,
                                occurrences=0)


def xml_set_text(xmltree: XMLLike,
                 schema_dict: fleur_schema.SchemaDict,
                 xpath: XPathLike,
                 base_xpath: str,
                 text: Any,
                 occurrences: int | Iterable[int] | None = None,
                 create: bool = False) -> XMLLike:
    """
    Sets the text on tags in a xmltree to a given value. By default the text will be set
    on all nodes returned for the specified xpath.
    If there are no nodes under the specified xpath a tag can be created with `create=True`.
    The text values are converted automatically according to the types
    with :py:func:`~masci_tools.util.xml.converters.convert_to_xml()` if they
    are not `str` already.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param xpath: a path where to set the text
    :param base_xpath: path where to place a new tag without complex syntax ([] conditions and so on)
    :param text: value or list of values to set
    :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.
    :param create: bool optional (default False), if True the tag is created if is missing

    :raises ValueError: If the conversion to string failed
    :raises ValueError: If the tag is missing and `create=False`

    :returns: xmltree with set text
    """
    from masci_tools.util.xml.xml_setters_basic import xml_set_text_no_create
    from masci_tools.util.xml.converters import convert_to_xml
    from masci_tools.util.xml.common_functions import check_complex_xpath, split_off_tag
    from masci_tools.io.common_functions import is_sequence

    check_complex_xpath(xmltree, base_xpath, xpath)

    _, tag_name = split_off_tag(base_xpath)

    converted_text, _ = convert_to_xml(text, schema_dict, tag_name, text=True)
    n_nodes = len(converted_text) if is_sequence(converted_text) else 1

    if create:
        nodes: list[etree._Element] = eval_xpath_create(xmltree,
                                                        schema_dict,
                                                        xpath,
                                                        base_xpath,
                                                        create_parents=True,
                                                        occurrences=occurrences,
                                                        number_nodes=n_nodes,
                                                        list_return=True)
    else:
        nodes = eval_xpath(xmltree, xpath, list_return=True)  #type:ignore

    if len(nodes) == 0:
        raise ValueError(
            f"Could not set text on path '{str(xpath.path) if isinstance(xpath, XPathBuilder) else str(xpath)}' because at least one subtag is missing. "
            'Use create=True to create the subtags')

    return xml_set_text_no_create(xmltree, xpath, converted_text, occurrences=occurrences)


def xml_set_first_text(xmltree: XMLLike,
                       schema_dict: fleur_schema.SchemaDict,
                       xpath: XPathLike,
                       base_xpath: str,
                       text: Any,
                       create: bool = False) -> XMLLike:
    """
    Sets the text on the first occurrence of a tag in a xmltree to a given value.
    If there are no nodes under the specified xpath a tag can be created with `create=True`.
    The text values are converted automatically according to the types
    with :py:func:`~masci_tools.util.xml.converters.convert_to_xml()` if they
    are not `str` already.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param xpath: a path where to set the text
    :param base_xpath: path where to place a new tag without complex syntax ([] conditions and so on)
    :param text: value or list of values to set
    :param create: bool optional (default False), if True the tag is created if is missing

    :raises ValueError: If the conversion to string failed
    :raises ValueError: If the tag is missing and `create=False`

    :returns: xmltree with set text
    """
    return xml_set_text(xmltree, schema_dict, xpath, base_xpath, text, create=create, occurrences=0)


def xml_add_number_to_attrib(xmltree: XMLLike,
                             schema_dict: fleur_schema.SchemaDict,
                             xpath: XPathLike,
                             base_xpath: str,
                             attributename: str,
                             add_number: Any,
                             mode: Literal['abs', 'rel'] = 'abs',
                             occurrences: int | Iterable[int] | None = None) -> XMLLike:
    """
    Adds a given number to the attribute value in a xmltree. By default the attribute will be shifted
    on all nodes returned for the specified xpath.
    If there are no nodes under the specified xpath an error is raised

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param xpath: a path where to set the attributes
    :param base_xpath: path where to place a new tag without complex syntax ([] conditions and so on)
    :param attributename: the attribute name to change
    :param add_number: number to add/multiply with the old attribute value
    :param mode: str (either `rel` or `abs`).
                 `rel` multiplies the old value with `add_number`
                 `abs` adds the old value and `add_number`
    :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.

    :raises ValueError: If the attribute is unknown or cannot be float or int
    :raises ValueError: If the evaluation of the old values failed
    :raises ValueError: If a float result is written to a integer attribute

    :returns: xmltree with shifted attribute
    """
    from masci_tools.util.schema_dict_util import read_constants
    from masci_tools.util.xml.converters import convert_from_xml
    from masci_tools.io.common_functions import is_sequence
    from masci_tools.util.xml.common_functions import check_complex_xpath, split_off_attrib, split_off_tag

    check_complex_xpath(xmltree, base_xpath, xpath)

    if attributename not in schema_dict['attrib_types']:
        raise ValueError(
            f"You try to shift the attribute:'{attributename}' , but the key is unknown to the fleur plug-in")

    possible_types = schema_dict['attrib_types'][attributename]

    if not etree.iselement(xmltree):
        constants = read_constants(xmltree.getroot(), schema_dict)
    else:
        constants = read_constants(xmltree, schema_dict)

    types = {definition.base_type for definition in possible_types}
    if 'float' not in types and \
       'float_expression' not in types and \
       'int' not in types:
        raise ValueError(f"Given attribute name '{attributename}' is not float or int")

    attribs = schema_dict['tag_info'][base_xpath]['attribs']
    _, tag_name = split_off_tag(base_xpath)
    if attributename not in attribs:
        raise ValueError(
            f"The key '{attributename}' is not expected for this version of the input for the '{tag_name}' tag. "
            f'Allowed attributes are: {sorted(attribs.original_case.values())}')
    attributename = attribs.original_case[attributename]

    if isinstance(xpath, XPathBuilder):
        if '@' not in xpath.components[-1]:
            xpath.append_tag(f'@{attributename}')
    elif not str(xpath).endswith(f'/@{attributename}'):
        xpath = '/@'.join([str(xpath), attributename])

    stringattribute: list[str] = eval_xpath(xmltree, xpath, list_return=True)  #type:ignore

    tag_xpath, attributename = split_off_attrib(xpath)

    if len(stringattribute) == 0:
        raise ValueError(f"No attribute values found for '{attributename}'. Cannot add number")

    res: tuple[list[int | float], bool] = convert_from_xml(stringattribute,
                                                           schema_dict,
                                                           attributename,
                                                           text=False,
                                                           constants=constants,
                                                           list_return=True)  #type:ignore
    attribvalues, _ = res

    if occurrences is not None:
        if not is_sequence(occurrences):
            occurrences = [occurrences]  #type:ignore
        try:
            attribvalues = [attribvalues[occ] for occ in cast(Iterable[int], occurrences)]
        except IndexError as exc:
            raise ValueError('Wrong value for occurrences') from exc

    if mode == 'abs':
        attribvalues = [value + float(add_number) for value in attribvalues]
    elif mode == 'rel':
        attribvalues = [value * float(add_number) for value in attribvalues]

    if 'float' in types or 'float_expression' in types:
        pass
    elif 'int' in types:
        if any(not value.is_integer() for value in attribvalues):
            raise ValueError('You are trying to write a float to an integer attribute')
        attribvalues = [int(value) for value in attribvalues]

    xmltree = xml_set_attrib_value(xmltree,
                                   schema_dict,
                                   tag_xpath,
                                   base_xpath,
                                   attributename,
                                   attribvalues,
                                   occurrences=occurrences)

    return xmltree


def xml_add_number_to_first_attrib(xmltree: XMLLike,
                                   schema_dict: fleur_schema.SchemaDict,
                                   xpath: XPathLike,
                                   base_xpath: str,
                                   attributename: str,
                                   add_number: Any,
                                   mode: Literal['abs', 'rel'] = 'abs') -> XMLLike:
    """
    Adds a given number to the first occurrence of a attribute value in a xmltree.
    If there are no nodes under the specified xpath an error is raised

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param xpath: a path where to set the attributes
    :param base_xpath: path where to place a new tag without complex syntax ([] conditions and so on)
    :param attributename: the attribute name to change
    :param add_number: number to add/multiply with the old attribute value
    :param mode: str (either `rel` or `abs`).
                 `rel` multiplies the old value with `add_number`
                 `abs` adds the old value and `add_number`

    :raises ValueError: If the attribute is unknown or cannot be float or int
    :raises ValueError: If the evaluation of the old values failed
    :raises ValueError: If a float result is written to a integer attribute

    :returns: xmltree with shifted attribute
    """
    return xml_add_number_to_attrib(xmltree,
                                    schema_dict,
                                    xpath,
                                    base_xpath,
                                    attributename,
                                    add_number,
                                    mode=mode,
                                    occurrences=0)


def xml_set_simple_tag(xmltree: XMLLike,
                       schema_dict: fleur_schema.SchemaDict,
                       xpath: XPathLike,
                       base_xpath: str,
                       tag_name: str,
                       changes: list[dict[str, Any]] | dict[str, Any],
                       create_parents: bool = False) -> XMLLike:
    """
    Sets one or multiple `simple` tag(s) in an xmltree. A simple tag can only hold attributes and has no
    subtags.
    If the tag can occur multiple times all existing tags are DELETED and new ones are written.
    If the tag only occurs once it will automatically be created if its missing.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param xpath: a path where to set the attributes
    :param base_xpath: path where to place a new tag without complex syntax ([] conditions and so on)
    :param tag_name: name of the tag to set
    :param changes: list of dicts or dict with the changes. Elements in list describe multiple tags.
                    Keys in the dictionary correspond to {'attributename': attributevalue}
    :param create_parents: bool optional (default False), if True and the path, where the simple tags are
                           set does not exist it is created

    :returns: xmltree with set simple tags
    """
    from masci_tools.util.xml.xml_setters_basic import xml_delete_tag
    from masci_tools.util.xml.common_functions import check_complex_xpath

    check_complex_xpath(xmltree, base_xpath, xpath)

    tag_info = schema_dict['tag_info'][base_xpath]

    tag_xpath = add_tag(xpath, tag_name)
    tag_base_xpath = f'{base_xpath}/{tag_name}'

    if tag_name in tag_info['several']:
        #change_dict can either be a list or a dict
        if isinstance(changes, dict):
            changes = [changes]

        if len(eval_xpath(xmltree, tag_xpath, list_return=True)) > 0:  #type:ignore
            # policy: we DELETE all existing tags, and create new ones from the given parameters.
            xml_delete_tag(xmltree, tag_xpath)

        xml_create_tag_schema_dict(xmltree,
                                   schema_dict,
                                   xpath,
                                   base_xpath,
                                   tag_name,
                                   create_parents=create_parents,
                                   number_nodes=len(changes))

        for indx, change in enumerate(changes):
            for attrib, value in change.items():
                occurrences = [
                    k * len(changes) + indx
                    for k in range(len(eval_xpath(xmltree, tag_xpath, list_return=True)) // len(changes))  #type:ignore
                ]
                xml_set_attrib_value(xmltree,
                                     schema_dict,
                                     tag_xpath,
                                     tag_base_xpath,
                                     attrib,
                                     value,
                                     occurrences=occurrences)
    else:
        if not isinstance(changes, dict):
            raise ValueError(f"Tag '{tag_name}' can only occur once. But 'set_simple_tag' got a list")

        #eval and ggf. create tag
        eval_xpath_create(xmltree, schema_dict, tag_xpath, tag_base_xpath, create_parents=create_parents)

        for attrib, value in changes.items():
            xml_set_attrib_value(xmltree, schema_dict, tag_xpath, tag_base_xpath, attrib, value)

    return xmltree


def xml_set_complex_tag(xmltree: XMLLike,
                        schema_dict: fleur_schema.SchemaDict,
                        xpath: XPathLike,
                        base_xpath: str,
                        attributedict: dict[str, Any],
                        create: bool = False) -> XMLLike:
    """
    Recursive Function to correctly set tags/attributes for a given tag.
    Goes through the attributedict and decides based on the schema_dict, how the corresponding
    key has to be handled.

    Supports:

        - attributes
        - tags with text only
        - simple tags, i.e. only attributes (can be optional single/multiple)
        - complex tags, will recursively create/modify them

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param xpath: a path where to set the attributes
    :param base_xpath: path where to place a new tag without complex syntax ([] conditions and so on)
    :param tag_name: name of the tag to set
    :param attributedict: Keys in the dictionary correspond to names of tags and the values are the modifications
                          to do on this tag (attributename, subdict with changes to the subtag, ...)
    :param create: bool optional (default False), if True and the path, where the complex tag is
                   set does not exist it is created

    :returns: xmltree with changes to the complex tag
    """
    import copy
    from masci_tools.util.xml.xml_setters_basic import xml_delete_tag
    from masci_tools.util.xml.common_functions import check_complex_xpath, split_off_tag

    check_complex_xpath(xmltree, base_xpath, xpath)

    tag_info = schema_dict['tag_info'][base_xpath]
    _, tag_name = split_off_tag(base_xpath)

    if create:
        #eval complex tag and ggf create
        eval_xpath_create(xmltree, schema_dict, xpath, base_xpath, create_parents=True)

    for key, val in attributedict.items():

        if key not in tag_info['complex'] | tag_info['simple'] | tag_info['attribs']:
            raise ValueError(
                f"The key '{key}' is not expected for this version of the input for the '{tag_name}' tag. "
                f"Allowed tags are: {sorted((tag_info['complex']|tag_info['simple']).original_case.values())}"
                f"Allowed attributes are: {sorted(tag_info['attribs'].original_case.values())}")

        key = (tag_info['complex'] | tag_info['simple'] | tag_info['attribs']).original_case[key]

        sub_xpath = add_tag(xpath, key)
        sub_base_xpath = f'{base_xpath}/{key}'
        if key in tag_info['attribs']:
            xml_set_attrib_value(xmltree, schema_dict, xpath, base_xpath, key, val, create=create)

        elif key in tag_info['text']:
            xml_set_text(xmltree, schema_dict, sub_xpath, sub_base_xpath, val, create=create)

        elif key in tag_info['simple']:
            xml_set_simple_tag(xmltree, schema_dict, xpath, base_xpath, key, val, create_parents=create)

        elif key not in tag_info['several']:  #Complex tag but only one (electronConfig)

            # eval and ggf create tag at right place.
            eval_xpath_create(xmltree, schema_dict, sub_xpath, sub_base_xpath, create_parents=create)

            xmltree = xml_set_complex_tag(xmltree, schema_dict, sub_xpath, sub_base_xpath, val, create=create)

        else:
            if len(eval_xpath(xmltree, sub_xpath, list_return=True)) > 0:  #type:ignore
                # policy: we DELETE all existing tags, and create new ones from the given parameters.
                xml_delete_tag(xmltree, sub_xpath)

            if isinstance(val, dict):
                val = [val]

            for indx in range(0, len(val)):
                xml_create_tag_schema_dict(xmltree, schema_dict, xpath, base_xpath, key, create_parents=create)

            for indx, tagdict in enumerate(val):
                for k in range(len(eval_xpath(xmltree, sub_xpath, list_return=True)) // len(val)):  #type:ignore
                    current_elem_xpath: XPathLike
                    if isinstance(sub_xpath, XPathBuilder):
                        current_elem_xpath = copy.deepcopy(sub_xpath)
                        current_elem_xpath.add_filter(sub_xpath.components[-1], {'index': k * len(val) + indx + 1})
                    elif isinstance(sub_xpath, etree.XPath):
                        current_elem_xpath = etree.XPath(f'{str(sub_xpath)}[{k*len(val)+indx+1}]')
                    else:
                        current_elem_xpath = f'{str(sub_xpath)}[{k*len(val)+indx+1}]'
                    xmltree = xml_set_complex_tag(xmltree,
                                                  schema_dict,
                                                  current_elem_xpath,
                                                  sub_base_xpath,
                                                  tagdict,
                                                  create=create)

    return xmltree
