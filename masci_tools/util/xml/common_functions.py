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
Common functions for parsing input/output files or XMLschemas from FLEUR
"""
from lxml import etree


def clear_xml(tree):
    """
    Removes comments and executes xinclude tags of an
    xml tree.

    :param tree: an xml-tree which will be processed

    :returns: cleared_tree, an xmltree without comments and with replaced xinclude tags
    """
    import copy

    cleared_tree = copy.deepcopy(tree)

    #Remove comments outside the root element (Since they have no parents this would lead to a crash)
    root = cleared_tree.getroot()
    prev_sibling = root.getprevious()
    while prev_sibling is not None:
        root.append(prev_sibling)
        root.remove(prev_sibling)
        prev_sibling = root.getprevious()

    next_sibling = root.getnext()
    while next_sibling is not None:
        root.append(next_sibling)
        root.remove(next_sibling)
        next_sibling = root.getnext()

    #find any include tags
    include_tags = eval_xpath(cleared_tree,
                              '//xi:include',
                              namespaces={'xi': 'http://www.w3.org/2001/XInclude'},
                              list_return=True)

    parents = []
    known_tags = []
    for tag in include_tags:
        parent = tag.getparent()
        parents.append(parent)
        known_tags.append({elem.tag for elem in parent})

    # replace XInclude parts to validate against schema
    if len(include_tags) != 0:
        cleared_tree.xinclude()

    # get rid of xml:base attribute in the included parts
    for parent, old_tags in zip(parents, known_tags):
        new_tags = {elem.tag for elem in parent}

        #determine the elements not in old_tags, which are in tags
        #so what should have been included
        included_tag_names = new_tags.difference(old_tags)

        #Check for emtpy set (relax.xml include may not insert something)
        if not included_tag_names:
            continue

        for tag_name in included_tag_names:
            for elem in parent:
                if elem.tag == tag_name:
                    for attribute in elem.keys():
                        if 'base' in attribute:
                            try:
                                del elem.attrib[attribute]
                            except BaseException:
                                pass

    # remove comments from inp.xml
    comments = cleared_tree.xpath('//comment()')
    for comment in comments:
        com_parent = comment.getparent()
        com_parent.remove(comment)

    return cleared_tree


def validate_xml(xmltree, schema, error_header='File does not validate'):
    """
    Checks a given xmltree against a schema and produces a nice error message
    with all the validation errors collected

    :param xmltree: xmltree of the file to validate
    :param schema: etree.XMLSchema to validate against
    :param error_header: str to lead a evtl error message with

    :raises: etree.DocumentInvalid if the schema does not validate
    """
    from itertools import groupby

    try:
        schema.assertValid(clear_xml(xmltree))
    except etree.DocumentInvalid as exc:
        error_log = sorted(schema.error_log, key=lambda x: x.message)
        error_output = []
        first_occurence = []
        for message, group in groupby(error_log, key=lambda x: x.message):
            err_occurences = list(group)
            error_message = f'Line {err_occurences[0].line}: {message}'
            error_lines = ''
            if len(err_occurences) > 1:
                error_lines = f"; This error also occured on the lines {', '.join([str(x.line) for x in err_occurences[1:]])}"
            error_output.append(f'{error_message}{error_lines} \n')
            first_occurence.append(err_occurences[0].line)

        error_output = [line for _, line in sorted(zip(first_occurence, error_output))]
        errmsg = f"{error_header}: \n{''.join(error_output)}"
        raise etree.DocumentInvalid(errmsg) from exc


def eval_xpath(node, xpath, logger=None, list_return=False, namespaces=None):
    """
    Tries to evaluate an xpath expression. If it fails it logs it.
    If a absolute path is given (starting with '/') and the tag of the node
    does not match the root.
    It will try to find the tag in the path and convert it into a relative path

    :param node: root node of an etree
    :param xpath: xpath expression (relative, or absolute)
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised
    :param list_return: if True, the returned quantity is always a list even if only one element is in it
    :param namespaces: dict, passed to namespaces argument in xpath call

    :returns: text, attribute or a node list
    """

    if not isinstance(node, (etree._Element, etree._ElementTree)):
        if logger is not None:
            logger.error('Wrong Type for xpath eval; Got: %s', type(node))
        raise TypeError(f'Wrong Type for xpath eval; Got: {type(node)}')

    try:
        return_value = node.xpath(xpath, namespaces=namespaces)
    except etree.XPathEvalError as err:
        if logger is not None:
            logger.exception(
                'There was a XpathEvalError on the xpath: %s \n'
                'Either it does not exist, or something is wrong with the expression.', xpath)
        raise ValueError(f'There was a XpathEvalError on the xpath: {xpath} \n'
                         'Either it does not exist, or something is wrong with the expression.') from err
    if len(return_value) == 1 and not list_return:
        return return_value[0]
    else:
        return return_value


def get_xml_attribute(node, attributename, logger=None):
    """
    Get an attribute value from a node.

    :param node: a node from etree
    :param attributename: a string with the attribute name.
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised
    :returns: either attributevalue, or None
    """

    if etree.iselement(node):
        attrib_value = node.get(attributename)
        if attrib_value:
            return attrib_value
        else:
            if logger is not None:
                logger.warning(
                    'Tried to get attribute: "%s" from element %s.\n '
                    'I received "%s", maybe the attribute does not exist', attributename, node.tag, attrib_value)
            else:
                raise ValueError(f'Tried to get attribute: "{attributename}" from element {node.tag}.\n '
                                 f'I received "{attrib_value}", maybe the attribute does not exist')
    else:  # something doesn't work here, some nodes get through here
        if logger is not None:
            logger.error(
                'Can not get attributename: "%s" from node of type %s, '
                'because node is not an element of etree.', attributename, type(node))
        else:
            raise TypeError(f'Can not get attributename: "{attributename}" from node of type {type(node)}, '
                            f'because node is not an element of etree.')

    return None


def split_off_tag(xpath):
    """
    Splits off the last part of the given xpath

    :param xpath: str of the xpath to split up
    """
    split_xpath = xpath.split('/')
    if split_xpath[-1] == '':
        return '/'.join(split_xpath[:-2]), split_xpath[-2]
    else:
        return '/'.join(split_xpath[:-1]), split_xpath[-1]


def split_off_attrib(xpath):
    """
    Splits off attribute of the given xpath (part after @)

    :param xpath: str of the xpath to split up
    """
    split_xpath = xpath.split('/@')
    assert len(split_xpath) == 2, f"Splitting off attribute failed for: '{split_xpath}'"
    return tuple(split_xpath)


def check_complex_xpath(node, base_xpath, complex_xpath):
    """
    Check that the given complex xpath produces a subset of the results
    for the simple xpath

    :param node: root node of an etree
    :param base_xpath: str of the xpath without complex syntax
    :param complex_xpath: str of the xpath to check

    :raises ValueError: If the complex_xpath does not produce a subset of the results
                        of the base_xpath
    """

    results_base = set(eval_xpath(node, base_xpath, list_return=True))
    results_complex = set(eval_xpath(node, complex_xpath, list_return=True))

    if not results_base.issuperset(results_complex):
        raise ValueError(f"Complex xpath '{complex_xpath}' is not compatible with the base_xpath '{base_xpath}'")


def abs_to_rel_xpath(xpath, new_root):
    """
    Convert a given xpath to be relative from a tag appearing in the
    original xpath.

    :param xpath: str of the xpath to convert
    :param new_root: str of the tag from which the new xpath should be relative

    :returns: str of the relative xpath
    """
    if new_root in xpath:
        if '@' not in xpath:
            xpath = xpath + '/'

        xpath_to_root = '/'.join(xpath.split(new_root + '/')[:-1]) + new_root
        xpath = xpath.replace(xpath_to_root, '.')
        if xpath != './':
            xpath = xpath.rstrip('/')
    else:
        raise ValueError(f'New root element {new_root} does not appear in xpath {xpath}')

    return xpath
