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
Functions for modifying the xml input file of Fleur utilizing explicit xpaths
"""
from lxml import etree
from masci_tools.util.xml.common_xml_util import eval_xpath

def create_tag_xpath(xmltree, xpath, element, place_index=None, tag_order=None, create=False, schema_dict_func=None):
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
    #TODO reimplement create functionality
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

    print(tag_order)
    if len(parent_nodes) == 0:
        parent_xpath, parent_name = '/'.join(xpath.split('/')[:-1]), xpath.split('/')[-1]
        if create:
            #Recursively go down and create the subtags
            #What kind of assertions can we on order here?
            if schema_dict_func is not None:
                #go back to the schema_dict function and get the tag_order for the next subtag
                xmltree = schema_dict_func(xmltree=xmltree, tag_name=parent_name, create=create, xpath=parent_xpath, contains=parent_xpath)
            else:
                #In the pure xpath version we can do nothing
                xmltree = create_tag_xpath(xmltree, parent_xpath, parent_name, create=create)
            parent_nodes = eval_xpath(xmltree, xpath, list_return=True)
        else:
            raise ValueError(f"Could not create tag '{element_name}' because atleast the subtag '{parent_name}' "
                             f"at '{parent_xpath}' is missing. Use 'create=True' to create this tag")

    for parent in parent_nodes:
        element_to_write = copy.deepcopy(element)
        if tag_order is not None:
            try:
                tag_index = tag_order.index(element_name)
            except ValueError as exc:
                raise ValueError(f"The tag '{element_name}' was not found in the order list"
                                 f"Allowed tags are: {tag_order}") from exc

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
            if sorted(existing_order, key=lambda key: tag_order.index(key)) != existing_order:
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

            else: #This is the construct for reaching the end of the loop without breaking
                try:
                    parent.insert(0, element_to_write)
                except ValueError as exc:
                    raise ValueError(f"Failed to insert element '{element_name}' at the beginning of the order") from exc

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
