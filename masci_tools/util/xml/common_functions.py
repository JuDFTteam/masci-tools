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
from __future__ import annotations

from masci_tools.util.typing import XMLLike, XPathLike, TXPathLike
from lxml import etree
import warnings
import copy
import logging
from typing import cast

from .xpathbuilder import XPathBuilder


def clear_xml(tree: etree._ElementTree) -> tuple[etree._ElementTree, set[str]]:
    """
    Removes comments and executes xinclude tags of an
    xml tree.

    :param tree: an xml-tree which will be processed

    :returns: cleared_tree, an xmltree without comments and with replaced xinclude tags
    """
    cleared_tree = copy.deepcopy(tree)

    #Remove comments outside the root element (Since they have no parents this would lead to a crash)
    root = cleared_tree.getroot()
    prev_sibling = root.getprevious()
    while prev_sibling is not None:
        if prev_sibling.tag is etree.Comment:
            root.append(prev_sibling)
            root.remove(prev_sibling)
        prev_sibling = prev_sibling.getprevious()

    next_sibling = root.getnext()
    while next_sibling is not None:
        if next_sibling.tag is etree.Comment:
            root.append(next_sibling)
            root.remove(next_sibling)
        next_sibling = next_sibling.getnext()

    #find any include tags
    include_tags: list[etree._Element] = eval_xpath(cleared_tree,
                                                    '//xi:include',
                                                    namespaces={'xi': 'http://www.w3.org/2001/XInclude'},
                                                    list_return=True)  #type:ignore

    parents = []
    known_tags = []
    for tag in include_tags:
        parent = tag.getparent()
        if parent is None:
            raise ValueError('Could not find parent of included tag')
        parents.append(parent)
        known_tags.append({elem.tag for elem in parent if isinstance(elem.tag, str)})

    # replace XInclude parts to validate against schema
    if len(include_tags) != 0:
        cleared_tree.xinclude()

    all_included_tags: set[str] = set()
    # get rid of xml:base attribute in the included parts
    for parent, old_tags in zip(parents, known_tags):
        new_tags = {elem.tag for elem in parent if isinstance(elem.tag, str)}

        #determine the elements not in old_tags, which are in tags
        #so what should have been included
        included_tag_names = new_tags.difference(old_tags)

        #Check for empty set (relax.xml include may not insert something)
        if not included_tag_names:
            continue

        all_included_tags = all_included_tags.union(included_tag_names)
        for tag_name in included_tag_names:
            for elem in parent.iterchildren(tag=tag_name):
                for attribute in elem.attrib.keys():
                    if 'base' in attribute:
                        elem.attrib.pop(attribute, '')

    # remove comments from inp.xml
    comments: list[etree._Element] = cleared_tree.xpath('//comment()')  #type:ignore
    for comment in comments:
        com_parent = comment.getparent()
        if com_parent is None:
            raise ValueError('Could not find parent of comment tag')
        com_parent.remove(comment)

    etree.indent(cleared_tree)

    return cleared_tree, all_included_tags


def reverse_xinclude(xmltree, schema_dict, included_tags, **kwargs):
    """
    DEPRECATED ALIAS: Moved to masci_tools.util.schema_dict_util

    Split the xmltree back up according to the given included tags.
    The original xmltree will be returned with the corresponding xinclude tags
    and the included trees are returned in a dict mapping the inserted filename
    to the extracted tree

    Tags for which no known filename is known are returned under unknown-1.xml, ...
    The following tags have known filenames:

        - `relaxation`: ``relax.xml``
        - `kPointLists`: ``kpts.xml``
        - `symmetryOperations`: ``sym.xml``
        - `atomSpecies`: ``species.xml``
        - `atomGroups`: ``atoms.xml``

    Additional mappings can be given in the keyword arguments

    :param xmltree: an xml-tree which will be processed
    :param schema_dict: Schema dictionary containing all the necessary information
    :param included_tags: Iterable of str, containing the names of the tags to be excluded

    :returns: xmltree with the inseerted xinclude tags and a dict mapping the filenames
              to the excluded trees

    :raises ValueError: if the tag can not be found in the given xmltree
    """
    from masci_tools.util.schema_dict_util import reverse_xinclude  #pylint: disable=redefined-outer-name
    warnings.warn('DEPRECATED: reverse_xinclude moved to masci_tools.util.schema_dict_util', DeprecationWarning)
    return reverse_xinclude(xmltree, schema_dict, included_tags, **kwargs)


def validate_xml(xmltree: etree._ElementTree,
                 schema: etree.XMLSchema,
                 error_header: str = 'File does not validate') -> None:
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
        cleared_tree, _ = clear_xml(xmltree)
        schema.assertValid(cleared_tree)
    except etree.DocumentInvalid as exc:
        error_log = sorted(schema.error_log, key=lambda x: x.message)  #type: ignore[call-overload]
        error_output = []
        first_occurence = []
        for message, group in groupby(error_log, key=lambda x: cast(object, x.message)):
            err_occurences = list(group)
            error_message = f'Line {err_occurences[0].line}: {message}'
            error_lines = ''
            if len(err_occurences) > 1:
                error_lines = f"; This error also occurred on the lines {', '.join([str(x.line) for x in err_occurences[1:]])}"
            error_output.append(f'{error_message}{error_lines} \n')
            first_occurence.append(err_occurences[0].line)

        error_output = [line for _, line in sorted(zip(first_occurence, error_output))]
        errmsg = f"{error_header}: \n{''.join(error_output)}"
        raise etree.DocumentInvalid(errmsg) from exc


def eval_xpath(node: XMLLike | etree.XPathElementEvaluator,
               xpath: XPathLike,
               logger: logging.Logger | None = None,
               list_return: bool = False,
               namespaces: dict[str, str] | None = None,
               **variables: etree._XPathObject) -> etree._XPathObject:
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
    if isinstance(xpath, XPathBuilder):
        xpath_str = xpath.path
        variables = {**variables, **xpath.path_variables}
        xpath = xpath_str

    if logger is not None:
        logger.debug('XPath: %s', xpath)
        logger.debug('XPath Variables: %s', variables)

    if not isinstance(node, (etree._Element, etree._ElementTree, etree.XPathElementEvaluator)):
        if logger is not None:
            logger.error('Wrong Type for xpath eval; Got: %s', type(node))
        raise TypeError(f'Wrong Type for xpath eval; Got: {type(node)}')

    if namespaces is not None and (isinstance(xpath, etree.XPath) or isinstance(node, etree.XPathElementEvaluator)):
        if logger is not None:
            logger.exception(
                'Passing namespaces is only supported for string xpaths and nodes. for etree.XPath or XPathEvaluatore use namespaces in the init function'
            )
        raise ValueError(
            'Passing namespaces is only supported for string xpaths and nodes. for etree.XPath or XPathEvaluatore use namespaces in the init function'
        )

    try:
        if isinstance(node, etree.XPathElementEvaluator):
            if isinstance(xpath, etree.XPath):
                if logger is not None:
                    logger.error('Got an XPath object and an XPathEvaluator in eval_xpath')
                raise TypeError('Got an XPath object and an XPathEvaluator in eval_xpath')
            return_value = node(xpath, **variables)  #[arg-type]
        elif isinstance(xpath, etree.XPath):
            return_value = xpath(node, **variables)
        else:
            return_value = node.xpath(xpath, namespaces=namespaces, smart_strings=True, extensions=None, **variables)
    except etree.XPathEvalError as err:
        if logger is not None:
            logger.exception(
                'There was a XpathEvalError on the xpath: %s \n'
                'The following variables were passed: %s \n'
                'Either it does not exist, or something is wrong with the expression.', xpath, variables)
        raise ValueError(f'There was a XpathEvalError on the xpath: {str(xpath)} \n'
                         f'The following variables were passed: {variables} \n'
                         'Either it does not exist, or something is wrong with the expression.') from err

    if logger is not None:
        logger.debug('XPath Result: %s', return_value)

    if isinstance(return_value, list):
        if len(return_value) == 1 and not list_return:
            return return_value[0]  #type:ignore
    return return_value


def get_xml_attribute(node: etree._Element, attributename: str, logger: logging.Logger | None = None) -> str | None:
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
        if logger is None:
            raise ValueError(f'Tried to get attribute: "{attributename}" from element {node.tag}.\n '
                             f'I received "{attrib_value}", maybe the attribute does not exist')
        logger.warning(
            'Tried to get attribute: "%s" from element %s.\n '
            'I received "%s", maybe the attribute does not exist', attributename, node.tag, attrib_value)

    else:  # something doesn't work here, some nodes get through here
        if logger is None:
            raise TypeError(f'Can not get attributename: "{attributename}" from node of type {type(node)}, '
                            f'because node is not an element of etree.')
        logger.error(
            'Can not get attributename: "%s" from node of type %s, '
            'because node is not an element of etree.', attributename, type(node))

    return None


def split_off_tag(xpath: TXPathLike) -> tuple[TXPathLike, str]:
    """
    Splits off the last part of the given xpath

    .. note::
        etree.XPath objects could lose context in here, i.e.
        non-default options passed at init

    :param xpath:  xpath to split up
    """
    if isinstance(xpath, XPathBuilder):
        xpath = copy.deepcopy(xpath)  #type:ignore[assignment]
        tag = xpath.strip_off_tag()
        return xpath, tag  #type:ignore[return-value]

    if isinstance(xpath, etree.XPath):
        xpath_str = xpath.path
    else:
        xpath_str = xpath  #type:ignore[assignment]

    split_xpath = xpath_str.split('/')
    if split_xpath[-1] == '':
        xpath_str, tag = '/'.join(split_xpath[:-2]), split_xpath[-2]
    else:
        xpath_str, tag = '/'.join(split_xpath[:-1]), split_xpath[-1]

    if isinstance(xpath, etree.XPath):
        xpath = etree.XPath(xpath_str)  #type:ignore [assignment]
    else:
        xpath = xpath_str  #type:ignore[assignment]

    return xpath, tag


def add_tag(xpath: TXPathLike, tag: str) -> TXPathLike:
    """
    Add tag to xpath

    .. note::
        etree.XPath objects could lose context in here, i.e.
        non-default options passed at init

    :param xpath: xpath to change
    :param tag: str of the tag to add

    :returns: xpath with the form {old_xpath}/tag
    """
    if isinstance(xpath, XPathBuilder):
        xpath = copy.deepcopy(xpath)  #type:ignore[assignment]
        xpath.append_tag(tag)
    elif isinstance(xpath, etree.XPath):
        xpath = etree.XPath(f'{str(xpath.path)}/{tag}')  #type:ignore [assignment]
    else:
        xpath = f"{str(xpath).rstrip('/')}/{tag}"  #type:ignore[assignment]
    return xpath


def split_off_attrib(xpath: TXPathLike) -> tuple[TXPathLike, str]:
    """
    Splits off attribute of the given xpath (part after @)

    .. note::
        etree.XPath objects could lose context in here, i.e.
        non-default options passed at init

    :param xpath: xpath to split up
    """
    if isinstance(xpath, XPathBuilder):
        xpath = copy.deepcopy(xpath)  #type:ignore[assignment]
        attrib = xpath.strip_off_tag()
        if '@' not in attrib:
            raise ValueError('Path does not end with an attribute')
        return xpath, attrib.lstrip('@')  #type:ignore[return-value]

    if isinstance(xpath, etree.XPath):
        xpath_str = xpath.path
    else:
        xpath_str = xpath  #type:ignore[assignment]

    split_xpath = xpath_str.split('/@')
    if len(split_xpath) != 2:
        raise ValueError(f"Splitting off attribute failed for: '{split_xpath}'")
    xpath_str, attrib = tuple(split_xpath)

    if isinstance(xpath, etree.XPath):
        xpath = etree.XPath(xpath_str)  #type:ignore [assignment]
    else:
        xpath = xpath_str  #type:ignore[assignment]

    return xpath, attrib


def check_complex_xpath(node: XMLLike | etree.XPathElementEvaluator, base_xpath: XPathLike,
                        complex_xpath: XPathLike) -> None:
    """
    Check that the given complex xpath produces a subset of the results
    for the simple xpath

    :param node: root node of an etree or an etree
    :param base_xpath: str of the xpath without complex syntax
    :param complex_xpath: str of the xpath to check

    :raises ValueError: If the complex_xpath does not produce a subset of the results
                        of the base_xpath
    """
    results_base = set(eval_xpath(node, base_xpath, list_return=True))  #type:ignore
    results_complex = set(eval_xpath(node, complex_xpath, list_return=True))  #type:ignore

    if not results_base.issuperset(results_complex):
        raise ValueError(f"Complex xpath '{complex_xpath!r}' is not compatible with the base_xpath '{base_xpath!r}'")


def abs_to_rel_xpath(xpath: str, new_root: str) -> str:
    """
    Convert a given xpath to be relative from a tag appearing in the
    original xpath.

    :param xpath: str of the xpath to convert
    :param new_root: str of the tag from which the new xpath should be relative

    :returns: str of the relative xpath
    """
    if contains_tag(xpath, new_root):
        xpath = xpath + '/'
        xpath_to_root = '/'.join(xpath.split(new_root + '/')[:-1]) + new_root
        xpath = xpath.replace(f'{xpath_to_root}/', './')
        xpath = xpath.rstrip('/')
    else:
        raise ValueError(f'New root element {new_root} does not appear in xpath {xpath}')

    return xpath


def normalize_xmllike(xmllike: XMLLike) -> etree._Element:
    """
    Returns the root of the xmltree
    """
    if etree.iselement(xmllike):
        return xmllike
    xmllike, _ = clear_xml(xmllike)  #type:ignore[arg-type]
    return xmllike.getroot()


def contains_tag(xpath: XPathLike, tag: str) -> bool:
    """
    Return whether a given xpath contains a given tag
    This assumes that predicates of xpaths can't be nested
    since otherwise the regex for removing them could fail

    This function will only return True if one of the
    tags exactly matches the tag argument not if one tag contains the
    given name in it's name

    :param xpath: xpath expression
    :param tag: tag to check for

    :returns: whether a tag is contained in the xpath
    """
    import re
    if isinstance(xpath, XPathBuilder):
        return tag in xpath.components

    if isinstance(xpath, etree.XPath):
        xpath_str = xpath.path
    else:
        xpath_str = str(xpath)

    #Strip out predicates
    xpath_str = re.sub(r'[\[].*?[\]]', '', xpath_str)
    return tag in xpath_str.split('/')


def is_valid_tag(tag: str) -> bool:
    """
    Return whether the given string is a valid XML tag name

    :param tag: tag to check
    """
    try:
        etree.QName(tag)
        return True
    except ValueError:
        return False
