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
from masci_tools.util.xml.common_xml_util import eval_xpath

def replace_tag(xmltree, xpath, newelement):
    """
    replaces a xml tag by another tag on an xmletree in place

    :param xmltree: an xmltree that represents inp.xml
    :param xpathn: a path to the tag to be replaced
    :param newelement: a new tag
    """
    root = xmltree.getroot()

    nodes = eval_xpath(root, xpath, list_return=True)
    for node in nodes:
        parent = node.getparent()
        index = parent.index(node)
        parent.remove(node)
        parent.insert(index, newelement)

    return xmltree

def delete_att(xmltree, xpath, attrib):
    """
    Deletes an xml attribute in an xmletree.

    :param xmltree: an xmltree that represents inp.xml
    :param xpathn: a path to the attribute to be deleted
    :param attrib: the name of an attribute
    """
    root = xmltree.getroot()
    nodes = eval_xpath(root, xpath, list_return=True)
    for node in nodes:
        try:
            del node.attrib[attrib]
        except BaseException:
            pass
    return xmltree


def delete_tag(xmltree, xpath):
    """
    Deletes an xml tag in an xmletree.

    :param xmltree: an xmltree that represents inp.xml
    :param xpathn: a path to the tag to be deleted
    """
    root = xmltree.getroot()
    nodes = eval_xpath(root, xpath, list_return=True)
    for node in nodes:
        parent = node.getparent()
        parent.remove(node)
    return xmltree

def create_tag_xpath(xmltree, xpath, element, place_index=None, tag_order=None):
    """
    This method evaluates an xpath expresion and creates tag in an xmltree under the
    returned nodes. If the path does exist things will be overwritten, or created.
    Per default the new element is appended to the elements, but it can also be
    inserted in a certain position or after certain other tags.

    :param xmlnode: an xmltree that represents inp.xml
    :param xpathn: a path where to place a new tag
    :param newelement: a tag name to be created
    :param create: if True and there is no given xpath in the FleurinpData, creates it
    :param place_index: defines the place where to put a created tag
    :param tag_order: defines a tag order
    """
    import copy
    from more_itertools import unique_justseen

    if not etree.iselement(element):
        element_name = element
        try:
            element = etree.Element(element)
        except ValueError as exc:
            raise ValueError(f"Failed to construct etree Element from '{element_name}'") from exc
    else:
        element_name = element.tag

    parent_nodes = eval_xpath(xmltree, xpath, list_return=True)

    if len(parent_nodes)==0:
        raise ValueError(f"Could not create tag '{element_name}' because atleast one subtag is missing. "
                          'Use create=True to create the subtags')


    for parent in parent_nodes:
        element_to_write = copy.deepcopy(element)
        if tag_order is not None:
            try:
                tag_index = tag_order.index(element_name)
            except ValueError as exc:
                raise ValueError(f"The tag '{element_name}' was not found in the order list"
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
                raise ValueError('Existing order does not correspond to tag_order list')

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
            raise ValueError("Wrong value for occurrences") from exc

    if is_sequence(attribv):
        if len(attribv) != len(nodes):
            raise ValueError(f"Wrong length for attribute values. Expected {len(nodes)} items. Got: {attribv}")
    else:
        attribv = [attribv] * len(nodes)

    attribv = [val if isinstance(val, str) else str(val) for val in attribv]

    for node, value in zip(nodes, attribv):
        node.set(attributename, value)

    return xmltree

def xml_set_text_no_create(xmltree, xpath, text, occurrences=None):

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
            raise ValueError("Wrong value for occurrences") from exc

    if is_sequence(text):
        if len(text) != len(nodes):
            raise ValueError(f"Wrong length for attribute values. Expected {len(nodes)} items. Got: {text}")
    else:
        text = [text] * len(nodes)

    for node, text_val in zip(nodes, text):
        node.text = text_val

    return xmltree





