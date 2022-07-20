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
Basic functions for modifying the xml input file of Fleur. These functions DO NOT
have the ability to create missing tags on the fly. This functionality is added on top
in :py:mod:`~masci_tools.util.xml.xml_setters_xpaths` since we need the schema dictionary
to do these operations robustly
"""
from __future__ import annotations

from typing import Iterable, Any
from lxml import etree
import warnings

from masci_tools.util.typing import XPathLike, XMLLike
from masci_tools.util.xml.common_functions import eval_xpath_all, is_valid_tag


def xml_replace_tag(xmltree: XMLLike,
                    xpath: XPathLike,
                    element: str | etree._Element,
                    occurrences: int | Iterable[int] | None = None) -> XMLLike:
    """
    Replace XML tags by a given tag on the given XML tree

    :param xmltree: an xmltree that represents inp.xml
    :param xpath: a path to the tag to be replaced
    :param element: an Element or string representing the Element to replace the found tags with
    :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag.
                        By default all nodes are used.

    :returns: xmltree with replaced tag
    """
    import copy

    if not etree.iselement(xmltree):
        root = xmltree.getroot()  #type:ignore[union-attr]
    else:
        root = xmltree

    if not etree.iselement(element):
        element = etree.fromstring(element)  #type:ignore[arg-type]

    nodes = eval_xpath_all(root, xpath, etree._Element)

    if len(nodes) == 0:
        warnings.warn(f'No nodes to replace found on xpath: {xpath!r}')

    if occurrences is not None:
        if not isinstance(occurrences, Iterable):
            occurrences = [occurrences]
        try:
            nodes = [nodes[occ] for occ in occurrences]
        except IndexError as exc:
            raise ValueError('Wrong value for occurrences') from exc

    for node in nodes:
        parent = node.getparent()
        if parent is None:
            raise ValueError('Could not find parent of node')
        index = parent.index(node)
        parent.remove(node)
        parent.insert(index, copy.deepcopy(element))

    etree.indent(xmltree)
    return xmltree


def xml_delete_att(xmltree: XMLLike,
                   xpath: XPathLike,
                   name: str,
                   occurrences: int | Iterable[int] | None = None) -> XMLLike:
    """
    Deletes an attribute in the XML tree

    :param xmltree: an xmltree that represents inp.xml
    :param xpath: a path to the attribute to be deleted
    :param name: the name of an attribute to delete
    :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag.
                        By default all nodes are used.

    :returns: xmltree with deleted attribute
    """

    if not etree.iselement(xmltree):
        root = xmltree.getroot()  #type:ignore[union-attr]
    else:
        root = xmltree

    nodes = eval_xpath_all(root, xpath, etree._Element)

    if len(nodes) == 0:
        warnings.warn(f'No nodes to delete attributes on found on xpath: {xpath!r}')

    if occurrences is not None:
        if not isinstance(occurrences, Iterable):
            occurrences = [occurrences]
        try:
            nodes = [nodes[occ] for occ in occurrences]
        except IndexError as exc:
            raise ValueError('Wrong value for occurrences') from exc

    for node in nodes:
        node.attrib.pop(name, '')

    return xmltree


def xml_delete_tag(xmltree: XMLLike, xpath: XPathLike, occurrences: int | Iterable[int] | None = None) -> XMLLike:
    """
    Deletes a tag in the XML tree.

    :param xmltree: an xmltree that represents inp.xml
    :param xpath: a path to the tag to be deleted
    :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag.
                        By default all nodes are used.

    :returns: xmltree with deleted tag
    """

    if not etree.iselement(xmltree):
        root = xmltree.getroot()  #type:ignore[union-attr]
    else:
        root = xmltree

    nodes = eval_xpath_all(root, xpath, etree._Element)

    if len(nodes) == 0:
        warnings.warn(f'No nodes to delete found on xpath: {xpath!r}')

    if occurrences is not None:
        if not isinstance(occurrences, Iterable):
            occurrences = [occurrences]
        try:
            nodes = [nodes[occ] for occ in occurrences]
        except IndexError as exc:
            raise ValueError('Wrong value for occurrences') from exc

    for node in nodes:
        parent = node.getparent()
        if parent is None:
            raise ValueError('Could not find parent of node')
        parent.remove(node)

    etree.indent(xmltree)
    return xmltree


def _reorder_tags(node: etree._Element, tag_order: list[str]) -> etree._Element:
    """
    Order the children of the given node into the given order

    Prerequisites for this function:
        - We already know that all nodes on the node are valid in the order

    :param node: Element of the node to reorder
    :param tag_order: list of the names of the tags

    :returns: The reordered node
    """
    import copy

    ordered_node = copy.deepcopy(node)

    #Remove all child nodes from new_tag (deepcopied so they are still on node)
    for child in ordered_node.iterchildren():
        ordered_node.remove(child)

    for tag in tag_order:
        #Iterate over all children with the given tag on the node and append to the new_tag
        for child in node.iterchildren(tag=tag):
            ordered_node.append(child)

    #Now replace the node with the reordered node
    parent = node.getparent()
    if parent is None:
        raise ValueError('Could not find parent of node')
    index = parent.index(node)
    parent.remove(node)
    parent.insert(index, ordered_node)
    return ordered_node


def xml_create_tag(xmltree: XMLLike,
                   xpath: XPathLike,
                   element: etree.QName | str | etree._Element,
                   place_index: int | None = None,
                   tag_order: list[str] | None = None,
                   occurrences: int | Iterable[int] | None = None,
                   correct_order: bool = True,
                   several: bool = True) -> XMLLike:
    """
    This method evaluates an xpath expression and creates a tag in a xmltree under the
    returned nodes.
    If there are no nodes under the specified xpath an error is raised.

    The tag is appended by default, but can be inserted at a certain index (`place_index`)
    or can be inserted according to a given order of tags

    :param xmltree: an xmltree that represents inp.xml
    :param xpath: a path where to place a new tag
    :param element: a tag name, etree Element or string representing the XML element to be created
    :param place_index: defines the place where to put a created tag
    :param tag_order: defines a tag order
    :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag.
                        By default all nodes are used.
    :param correct_order: bool, if True (default) and a tag_order is given, that does not correspond to the given order
                          in the xmltree (only order wrong no unknown tags) it will be corrected and a warning is given
                          This is necessary for some edge cases of the xml schemas of fleur
    :param several: bool, if True multiple tags od the given name are allowed

    :raises ValueError: If the insertion failed in any way (tag_order does not match, failed to insert, ...)

    :returns: xmltree with created tags
    """
    import copy
    from more_itertools import unique_justseen

    if not etree.iselement(element):
        if isinstance(element, etree.QName) or is_valid_tag(element):  #type:ignore[arg-type]
            element = etree.Element(element)  #type:ignore[arg-type]
        else:
            try:
                element = etree.fromstring(element)  #type:ignore[arg-type]
            except etree.XMLSyntaxError as exc:
                raise ValueError(f"Failed to construct etree Element from '{element}'") from exc
        element_name = element.tag
    else:
        element_name = element.tag

    parent_nodes = eval_xpath_all(xmltree, xpath, etree._Element)

    if len(parent_nodes) == 0:
        raise ValueError(f"Could not create tag '{element_name}' because at least one subtag is missing. "
                         'Use create=True to create the subtags')

    if occurrences is not None:
        if not isinstance(occurrences, Iterable):
            occurrences = [occurrences]
        try:
            parent_nodes = [parent_nodes[occ] for occ in occurrences]
        except IndexError as exc:
            raise ValueError('Wrong value for occurrences') from exc

    for parent in parent_nodes:
        element_to_write: etree._Element = copy.deepcopy(element)
        if tag_order is not None:
            try:
                tag_index = tag_order.index(element_name)
            except ValueError as exc:
                raise ValueError(f"The tag '{element_name}' was not found in the order list. "
                                 f'Allowed tags are: {tag_order}') from exc

            behind_tags = tag_order[:tag_index]

            child_tags = [child.tag for child in parent.iterchildren()]

            #This ignores serial duplicates. With this out of order tags will be obvious e.g ['ldaU', 'lo','lo', 'ldaU']
            #will result in ['ldaU', 'lo', 'ldaU']
            existing_order = list(unique_justseen(child_tags))

            #Does the input file have unknown tags
            extra_tags = set(existing_order).difference(set(tag_order))
            if extra_tags:
                raise ValueError(f'Did not find existing elements in the tag_order list: {extra_tags}')

            if element_name in existing_order and not several:
                raise ValueError(f'The given tag {element_name} is not allowed to appear multiple times')

            #Is the existing order in line with the given tag_order
            if sorted(existing_order, key=tag_order.index) != existing_order:
                if not correct_order:
                    raise ValueError('Existing order does not correspond to tag_order list\n'
                                     f'Expected order: {tag_order}\n'
                                     f'Actual order: {existing_order}')
                #Here we know that there are no unexpected tags in the order, so we can 'repair' the order
                warnings.warn('Existing order does not correspond to tag_order list. Correcting it\n'
                              f'Expected order: {tag_order}\n'
                              f'Actual order: {existing_order}')
                parent = _reorder_tags(parent, tag_order)

            for tag in reversed(behind_tags):
                existing_tags = list(parent.iterchildren(tag=tag))

                if len(existing_tags) != 0:
                    insert_index = parent.index(existing_tags[-1]) + 1
                    try:
                        parent.insert(insert_index, element_to_write)
                    except ValueError as exc:
                        raise ValueError(f"Failed to insert element '{element_name}' behind '{tag}' tag") from exc
                    break

            else:  #This is the construct for reaching the end of the loop without breaking
                try:
                    parent.insert(0, element_to_write)
                except ValueError as exc:
                    raise ValueError(
                        f"Failed to insert element '{element_name}' at the beginning of the order") from exc

        elif place_index is not None:
            #We just try to insert the new element at the index
            try:
                parent.insert(place_index, element_to_write)
            except ValueError as exc:
                raise ValueError(f"Failed to create element '{element_name}' at the place index '{place_index}' "
                                 f"to the parent '{parent.tag}'") from exc
        else:
            #We append the node and hope nothing breaks
            try:
                parent.append(element_to_write)
            except ValueError as exc:
                raise ValueError(f"Failed to append element '{element_name}' to the parent '{parent.tag}'") from exc

    etree.indent(xmltree)
    return xmltree


def xml_set_attrib_value_no_create(xmltree: XMLLike,
                                   xpath: XPathLike,
                                   name: str,
                                   value: Any,
                                   occurrences: int | Iterable[int] | None = None) -> XMLLike:
    """
    Sets an attribute in a xmltree to a given value. By default the attribute will be set
    on all nodes returned for the specified xpath.

    :param xmltree: an xmltree that represents inp.xml
    :param xpath: a path where to set the attributes
    :param name: the attribute name to set
    :param value: value or list of values to set (if not str they will be converted with `str(value)`)
    :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.

    :raises ValueError: If the lengths of attribv or occurrences do not match number of nodes

    :returns: xmltree with set attribute
    """
    from masci_tools.io.common_functions import is_sequence

    if not etree.iselement(xmltree):
        root = xmltree.getroot()  #type:ignore[union-attr]
    else:
        root = xmltree

    nodes = eval_xpath_all(root, xpath, etree._Element)

    if len(nodes) == 0:
        warnings.warn(f'No nodes to set attribute {name} on found on xpath: {xpath!r}')
        return xmltree

    if occurrences is not None:
        if not isinstance(occurrences, Iterable):
            occurrences = [occurrences]
        try:
            nodes = [nodes[occ] for occ in occurrences]
        except IndexError as exc:
            raise ValueError('Wrong value for occurrences') from exc

    if is_sequence(value):
        if len(value) != len(nodes):
            raise ValueError(f'Wrong length for attribute values. Expected {len(nodes)} items. Got: {len(value)}')
    else:
        value = [value] * len(nodes)

    value = [val if isinstance(val, str) else str(val) for val in value]

    for node, val in zip(nodes, value):
        node.set(name, val)

    return xmltree


def xml_set_text_no_create(xmltree: XMLLike,
                           xpath: XPathLike,
                           text: Any,
                           occurrences: int | Iterable[int] | None = None) -> XMLLike:
    """
    Sets the text of a tag in a xmltree to a given value.
    By default the text will be set on all nodes returned for the specified xpath.

    :param xmltree: an xmltree that represents inp.xml
    :param xpath: a path where to set the text
    :param text: value or list of values to set (if not str they will be converted with `str(value)`)
    :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.

    :raises ValueError: If the lengths of text or occurrences do not match number of nodes

    :returns: xmltree with set text
    """
    from masci_tools.io.common_functions import is_sequence

    if not etree.iselement(xmltree):
        root = xmltree.getroot()  #type:ignore[union-attr]
    else:
        root = xmltree

    nodes = eval_xpath_all(root, xpath, etree._Element)

    if len(nodes) == 0:
        warnings.warn(f'No nodes to set text on found on xpath: {xpath!r}')
        return xmltree

    if occurrences is not None:
        if not isinstance(occurrences, Iterable):
            occurrences = [occurrences]
        try:
            nodes = [nodes[occ] for occ in occurrences]
        except IndexError as exc:
            raise ValueError('Wrong value for occurrences') from exc

    if is_sequence(text):
        if len(text) != len(nodes):
            raise ValueError(f'Wrong length for text values. Expected {len(nodes)} items. Got: {text}')
    else:
        text = [text] * len(nodes)

    for node, text_val in zip(nodes, text):
        node.text = text_val

    return xmltree
