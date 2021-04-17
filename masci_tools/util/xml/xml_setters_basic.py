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
Basic functions for modifying the xml input file of Fleur. These functions DO NOT
have the ability to create missing tags on the fly. This functionality is added on top
in :py:mod:`~masci_tools.util.xml.xml_setters_xpaths` since we need the schema dictionary
to do these operations robustly
"""
from lxml import etree
from masci_tools.util.xml.common_functions import eval_xpath
import warnings


def xml_replace_tag(xmltree, xpath, newelement):
    """
    replaces xml tags by another tag on an xmletree in place

    :param xmltree: an xmltree that represents inp.xml
    :param xpath: a path to the tag to be replaced
    :param newelement: a new tag

    :returns: xmltree with replaced tag
    """
    import copy
    root = xmltree.getroot()

    nodes = eval_xpath(root, xpath, list_return=True)
    for node in nodes:
        parent = node.getparent()
        index = parent.index(node)
        parent.remove(node)
        parent.insert(index, copy.deepcopy(newelement))

    return xmltree


def xml_delete_att(xmltree, xpath, attrib):
    """
    Deletes an xml attribute in an xmletree.

    :param xmltree: an xmltree that represents inp.xml
    :param xpath: a path to the attribute to be deleted
    :param attrib: the name of an attribute

    :returns: xmltree with deleted attribute
    """
    root = xmltree.getroot()
    nodes = eval_xpath(root, xpath, list_return=True)
    for node in nodes:
        try:
            del node.attrib[attrib]
        except BaseException:
            pass
    return xmltree


def xml_delete_tag(xmltree, xpath):
    """
    Deletes a xml tag in an xmletree.

    :param xmltree: an xmltree that represents inp.xml
    :param xpath: a path to the tag to be deleted

    :returns: xmltree with deleted tag
    """
    root = xmltree.getroot()
    nodes = eval_xpath(root, xpath, list_return=True)
    for node in nodes:
        parent = node.getparent()
        parent.remove(node)
    return xmltree


def xml_create_tag(xmltree, xpath, element, place_index=None, tag_order=None, occurrences=None, correct_order=True):
    """
    This method evaluates an xpath expression and creates a tag in a xmltree under the
    returned nodes.
    If there are no nodes under the specified xpath an error is raised.

    The tag is appended by default, but can be inserted at a certain index (`place_index`)
    or can be inserted according to a given order of tags

    :param xmltree: an xmltree that represents inp.xml
    :param xpath: a path where to place a new tag
    :param element: a tag name or etree Element to be created
    :param place_index: defines the place where to put a created tag
    :param tag_order: defines a tag order
    :param occurrences: int or list of int. Which occurence of the parent nodes to create a tag.
                        By default all nodes are used.
    :param correct_order: bool, if True (default) and a tag_order is given, that does not correspond to the given order
                          in the xmltree (only order wrong no unknown tags) it will be corrected and a warning is given
                          This is necessary for some edge cases of the xml schemas of fleur

    :raises ValueError: If the insertion failed in any way (tag_order does not match, failed to insert, ...)

    :returns: xmltree with created tags
    """
    import copy
    from more_itertools import unique_justseen
    from masci_tools.io.common_functions import is_sequence

    if not etree.iselement(element):
        element_name = element
        try:
            element = etree.Element(element)
        except ValueError as exc:
            raise ValueError(f"Failed to construct etree Element from '{element_name}'") from exc
    else:
        element_name = element.tag

    parent_nodes = eval_xpath(xmltree, xpath, list_return=True)

    if len(parent_nodes) == 0:
        raise ValueError(f"Could not create tag '{element_name}' because atleast one subtag is missing. "
                         'Use create=True to create the subtags')

    if occurrences is not None:
        if not is_sequence(occurrences):
            occurrences = [occurrences]
        try:
            parent_nodes = [parent_nodes[occ] for occ in occurrences]
        except IndexError as exc:
            raise ValueError('Wrong value for occurrences') from exc

    for parent in parent_nodes:
        element_to_write = copy.deepcopy(element)
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

            #Is the existing order in line with the given tag_order
            if sorted(existing_order, key=tag_order.index) != existing_order:
                if not correct_order:
                    raise ValueError('Existing order does not correspond to tag_order list\n'
                                     f'Expected order: {tag_order}\n'
                                     f'Actual order: {existing_order}')
                else:
                    #Here we know that there are no unexpected tags in the order, so we can 'repair' the order
                    warnings.warn('Existing order does not correspond to tag_order list. Correcting it\n'
                                  f'Expected order: {tag_order}\n'
                                  f'Actual order: {existing_order}')

                    new_tag = copy.deepcopy(parent)

                    #Remove all child nodes from new_tag (deepcopied so they are still on parent)
                    for node in new_tag.iterchildren():
                        new_tag.remove(node)

                    for tag in tag_order:
                        #Iterate over all children with the given tag on the parent and append to the new_tag
                        for node in parent.iterchildren(tag=tag):
                            new_tag.append(node)

                    #Now replace the parent node with the reordered node
                    parent_of_parent = parent.getparent()
                    index = parent_of_parent.index(parent)
                    parent_of_parent.remove(parent)
                    parent_of_parent.insert(index, new_tag)
                    parent = new_tag

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

    return xmltree


def xml_set_attrib_value_no_create(xmltree, xpath, attributename, attribv, occurrences=None):
    """
    Sets an attribute in a xmltree to a given value. By default the attribute will be set
    on all nodes returned for the specified xpath.

    :param xmltree: an xmltree that represents inp.xml
    :param xpath: a path where to set the attributes
    :param attributename: the attribute name to set
    :param attribv: value or list of values to set (if not str they will be converted with `str(value)`)
    :param occurrences: int or list of int. Which occurence of the node to set. By default all are set.

    :raises ValueError: If the lengths of attribv or occurrences do not match number of nodes

    :returns: xmltree with set attribute
    """
    from masci_tools.io.common_functions import is_sequence

    root = xmltree.getroot()
    nodes = eval_xpath(root, xpath, list_return=True)

    if len(nodes) == 0:
        return xmltree

    if occurrences is not None:
        if not is_sequence(occurrences):
            occurrences = [occurrences]
        try:
            nodes = [nodes[occ] for occ in occurrences]
        except IndexError as exc:
            raise ValueError('Wrong value for occurrences') from exc

    if is_sequence(attribv):
        if len(attribv) != len(nodes):
            raise ValueError(f'Wrong length for attribute values. Expected {len(nodes)} items. Got: {attribv}')
    else:
        attribv = [attribv] * len(nodes)

    attribv = [val if isinstance(val, str) else str(val) for val in attribv]

    for node, value in zip(nodes, attribv):
        node.set(attributename, value)

    return xmltree


def xml_set_text_no_create(xmltree, xpath, text, occurrences=None):
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

    root = xmltree.getroot()
    nodes = eval_xpath(root, xpath, list_return=True)

    if len(nodes) == 0:
        return xmltree

    if occurrences is not None:
        if not is_sequence(occurrences):
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
