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


def convert_xml_attribute(stringattribute, possible_types, constants=None, logger=None):
    """
    Tries to converts a given string attribute to the types given in possible_types.
    First succeeded conversion will be returned

    If no logger is given and a attribute cannot be converted an error is raised

    :param stringattribute: str, Attribute to convert.
    :param possible_types: list of str What types it will try to convert to
    :param constants: dict, of constants defined in fleur input
    :param logger: logger object for logging warnings
                   if given the errors are logged and the list is returned with the unconverted values
                   otherwise a error is raised, when the first conversion fails

    :return: The converted value of the first succesful conversion
    """
    from masci_tools.util.fleur_calculate_expression import calculate_expression

    if not isinstance(stringattribute, list):
        stringattribute = [stringattribute]

    exceptions = []

    converted_list = []
    all_success = True
    for attrib in stringattribute:
        for value_type in possible_types:
            if value_type == 'float':
                try:
                    converted_value = float(attrib)
                except (ValueError, TypeError) as exc:
                    exceptions.append(exc)
                    continue

            elif value_type == 'float_expression':
                if constants is None:
                    raise ValueError(
                        "For calculating attributes of the type 'float_expression' constants have to be given")
                try:
                    converted_value = calculate_expression(attrib, constants)
                except ValueError as exc:
                    exceptions.append(exc)
                    continue

            elif value_type == 'int':
                try:
                    converted_value = int(attrib)
                except (ValueError, TypeError) as exc:
                    exceptions.append(exc)
                    continue

            elif value_type == 'switch':
                try:
                    converted_value = convert_from_fortran_bool(attrib)
                except (ValueError, TypeError) as exc:
                    exceptions.append(exc)
                    continue

            elif value_type == 'string':
                converted_value = str(attrib)

            converted_list.append(converted_value)
            break
        else:
            if logger is None:
                raise ValueError(f"Could not convert '{attrib}'. Tried: {possible_types}.\n"
                                 'The following errors occurred:\n   ' + '\n   '.join([str(exc) for exc in exceptions]))
            else:
                logger.warning("Could not convert '%s'. The following errors occurred:", attrib)

                for exc in exceptions:
                    logger.warning('   %s', str(exc))
                    logger.debug(exc, exc_info=exc)

            converted_list.append(attrib)
            all_success = False

    ret_value = converted_list
    if len(converted_list) == 1:
        ret_value = converted_list[0]

    return ret_value, all_success


def convert_attribute_to_xml(attributevalue, possible_types, logger=None, float_format='.10'):
    """
    Tries to converts a given attributevalue to a string for a xml file according
    to the types given in possible_types.
    First succeeded conversion will be returned

    :param attributevalue: value to convert.
    :param possible_types: list of str What types it will try to convert from
    :param logger: logger object for logging warnings
                   if given the errors are logged and the list is returned with the unconverted values
                   otherwise a error is raised, when the first conversion fails

    :return: The converted str of the value of the first succesful conversion
    """

    if not isinstance(attributevalue, list):
        attributevalue = [attributevalue]

    possible_types = possible_types.copy()

    if 'int' in possible_types:  #Since it just converts to string
        possible_types.remove('int')
        possible_types.append('int')

    if 'string' in possible_types:  #Move string to back
        possible_types.remove('string')

    possible_types.append('string')  #Always try string

    converted_list = []
    exceptions = []
    all_success = True
    for value in attributevalue:

        for value_type in possible_types:
            if value_type in ('float', 'float_expression'):
                try:
                    converted_value = f'{value:{float_format}f}'
                except ValueError as exc:
                    exceptions.append(exc)
                    continue

            elif value_type == 'switch':
                try:
                    converted_value = convert_to_fortran_bool(value)
                except (ValueError, TypeError) as exc:
                    exceptions.append(exc)
                    continue

            elif value_type in ('string', 'int'):
                converted_value = str(value)

            converted_list.append(converted_value)
            break
        else:
            if logger is None:
                raise ValueError(f"Could not convert '{value}' to text. Tried: {possible_types}.\n"
                                 'The following errors occurred:\n   ' + '\n   '.join([str(exc) for exc in exceptions]))
            else:
                logger.warning("Could not convert '%s' to text. The following errors occurred:", value)

                for exc in exceptions:
                    logger.warning('   %s', str(exc))
                    logger.debug(exc, exc_info=exc)

            converted_list.append(value)
            all_success = False

    ret_value = converted_list
    if len(converted_list) == 1:
        ret_value = converted_list[0]

    return ret_value, all_success


def convert_xml_text(tagtext, possible_definitions, constants=None, logger=None):
    """
    Tries to converts a given string text based on the definitions (length and type).
    First succeeded conversion will be returned

    :param tagtext: str, text to convert.
    :param possible_defintions: list of dicts What types it will try to convert to
    :param constants: dict, of constants defined in fleur input
    :param logger: logger object for logging warnings
                   if given the errors are logged and the list is returned with the unconverted values
                   otherwise a error is raised, when the first conversion fails

    :return: The converted value of the first succesful conversion
    """

    if not isinstance(tagtext, list):
        tagtext = [tagtext]

    converted_list = []
    all_success = True
    for text in tagtext:

        base_text = text.strip()
        split_text = text.split(' ')
        while '' in split_text:
            split_text.remove('')

        text_definition = None
        for definition in possible_definitions:
            if definition['length'] == len(split_text):
                text_definition = definition

        if text_definition is None:
            for definition in possible_definitions:
                if definition['length'] == 'unbounded' or \
                   definition['length'] == 1:
                    text_definition = definition

        if text_definition is None:
            if logger is None:
                raise ValueError(f"Failed to convert '{text}', no matching definition found")
            else:
                logger.warning("Failed to convert '%s', no matching definition found", text)
            converted_list.append(text)
            all_success = False
            continue

        #Avoid splitting the text accidentally if there is no length restriction
        if text_definition['length'] == 1:
            split_text = [base_text]

        converted_text = []
        for value in split_text:
            converted_value, suc = convert_xml_attribute(value,
                                                         text_definition['type'],
                                                         constants=constants,
                                                         logger=logger)
            converted_text.append(converted_value)
            if not suc:
                all_success = False

        if len(converted_text) == 1 and text_definition['length'] != 'unbounded':
            converted_text = converted_text[0]

        converted_list.append(converted_text)

    ret_value = converted_list
    if len(converted_list) == 1:
        ret_value = converted_list[0]

    return ret_value, all_success


def convert_text_to_xml(textvalue, possible_definitions, logger=None, float_format='16.13'):
    """
    Tries to convert a given list of values to str for a xml file based on the definitions (length and type).
    First succeeded conversion will be returned

    :param textvalue: value to convert
    :param possible_definitions: list of dicts What types it will try to convert to
    :param logger: logger object for logging warnings
                   if given the errors are logged and the list is returned with the unconverted values
                   otherwise a error is raised, when the first conversion fails

    :return: The converted value of the first succesful conversion
    """

    if not isinstance(textvalue, list):
        textvalue = [textvalue]
    elif not isinstance(textvalue[0], list):
        textvalue = [textvalue]

    converted_list = []
    all_success = True
    for text in textvalue:

        if not isinstance(text, list):
            text = [text]

        text_definition = None
        for definition in possible_definitions:
            if definition['length'] == len(text):
                text_definition = definition

        if text_definition is None:
            for definition in possible_definitions:
                if definition['length'] == 'unbounded':
                    text_definition = definition

        if text_definition is None:
            if isinstance(text, str):
                converted_list.append(text)
                continue

            if logger is None:
                raise ValueError(f"Failed to convert '{text}', no matching definition found")
            else:
                logger.warning("Failed to convert '%s', no matching definition found", text)

            converted_list.append('')
            all_success = False
            continue

        converted_text = []
        for value in text:
            converted_value, suc = convert_attribute_to_xml(value,
                                                            text_definition['type'],
                                                            logger=logger,
                                                            float_format=float_format)
            converted_text.append(converted_value)
            if not suc:
                if isinstance(value, str):
                    converted_list.append(value)
                    continue
                all_success = False

        converted_list.append(' '.join(converted_text))

    ret_value = converted_list
    if len(converted_list) == 1:
        ret_value = converted_list[0]

    return ret_value, all_success


def convert_from_fortran_bool(stringbool):
    """
    Converts a string in this case ('T', 'F', or 't', 'f') to True or False

    :param stringbool: a string ('t', 'f', 'F', 'T')

    :return: boolean  (either True or False)
    """

    true_items = ['True', 't', 'T']
    false_items = ['False', 'f', 'F']
    if isinstance(stringbool, str):
        if stringbool in false_items:
            return False
        elif stringbool in true_items:
            return True
        else:
            raise ValueError(f"Could not convert: '{stringbool}' to boolean, "
                             "which is not 'True', 'False', 't', 'T', 'F' or 'f'")
    elif isinstance(stringbool, bool):
        return stringbool  # no conversion needed...

    raise TypeError(f"Could not convert: '{stringbool}' to boolean, " 'only accepts str or boolean')


def convert_to_fortran_bool(boolean):
    """
    Converts a Boolean as string to the format defined in the input

    :param boolean: either a boolean or a string ('True', 'False', 'F', 'T')

    :return: a string (either 't' or 'f')
    """

    if isinstance(boolean, bool):
        if boolean:
            return 'T'
        else:
            return 'F'
    elif isinstance(boolean, str):  # basestring):
        if boolean in ('True', 't', 'T'):
            return 'T'
        elif boolean in ('False', 'f', 'F'):
            return 'F'
        else:
            raise ValueError(f"A string: {boolean} for a boolean was given, which is not 'True',"
                             "'False', 't', 'T', 'F' or 'f'")

    raise TypeError('convert_to_fortran_bool accepts only a string or ' f'bool as argument, given {boolean} ')


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

    if isinstance(node, etree._Element):
        if node.tag != xpath.split('/')[1] and xpath.split('/')[0] != '.':
            #absolute path with a different root tag than node
            if node.tag in xpath:
                if '@' not in xpath:
                    xpath = xpath + '/'
                xpath = xpath.replace('/'.join(xpath.split(node.tag + '/')[:-1]) + node.tag, '.')
                xpath = xpath.rstrip('/')

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

def convert_str_version_number(version_str):
    """
    Convert the version number as a integer for easy comparisons

    :param version_str: str of the version number, e.g. '0.33'

    :returns: tuple of ints representing the version str
    """

    version_numbers = version_str.split('.')

    if len(version_numbers) != 2:
        raise ValueError(f"Version number is malformed: '{version_str}'")

    return tuple(int(part) for part in version_numbers)
