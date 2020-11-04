from lxml import etree
from pprint import pprint
from masci_tools.io.parsers.fleur_schema_parser_functions import load_schema_dict

def inpxml_parse(file):

    parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8')

    with open(file, mode='r') as inpxmlfile:
        xmltree = etree.parse(inpxmlfile, parser)

    try:
        root = xmltree.getroot()
        version = root.attrib['fleurInputVersion']
    except:
        raise ValueError('Failed to extract inputVersion')

    xmlschema, schema_dict = load_schema_dict(version)

    if not xmlschema.validate(xmltree):
        raise ValueError('File does not validate against schema')

    inp_dict = inpxml_todict(root, schema_dict)

    pprint(inp_dict)


def inpxml_todict(parent, schema_dict, return_dict=None):
    """
    Recursive operation which transforms an xml etree to
    python nested dictionaries and lists.
    Decision to add a list is if the tag name is in the given list tag_several

    :param parent: some xmltree, or xml element
    :param schema_dict: structure/layout of the xml file in python dictionary

    :return: a python dictionary
    """

    if return_dict is None:
        return_dict = {}
    if list(parent.items()):
        return_dict = dict(list(parent.items()))
        # Now we have to convert lazy fortan style into pretty things for the Database
        for key in return_dict:

            converted_value = convert_xml_attribute(return_dict[key], schema_dict['attrib_types'][key])
            if converted_value is not None:
                return_dict[key] = converted_value
            else:
                pass
                # this key is not know to plug-in TODO maybe make this a method
                # of the parser and log this as warning, or add here make a log
                # list, to which you always append messages, pass them back to
                # the parser, who locks it then
                # raise TypeError("Parser wanted to convert the key:'{}' with
                # value '{}', from the inpxml file but the key is unknown to the
                # fleur plug-in".format(key, return_dict[key]))

    if parent.text:  # TODO more detal, exp: relPos, basic_elements should have all tags with text and can split them apart and convert to the given type
        # has text, but we don't want all the '\n' s and empty stings in the database
        if parent.text.strip() != '':  # might not be the best solution
            # set text
            return_dict = parent.text.strip()

    for element in parent:
        if element.tag in schema_dict['tags_several']:
            # make a list, otherwise the tag will be overwritten in the dict
            if element.tag not in return_dict:  # is this the first occurence?
                return_dict[element.tag] = []
            return_dict[element.tag].append(inpxml_todict(element, schema_dict))
        elif element.tag in schema_dict['omittable_tags']: #The tag is not useful in a parsed python dictionary
            return_dict = inpxml_todict(element, schema_dict, return_dict=return_dict)
        else:
            return_dict[element.tag] = inpxml_todict(element, schema_dict)

    return return_dict


def convert_xml_attribute(stringattribute, possible_types):

    if not isinstance(possible_types, list):
        possible_types = [possible_types]

    for value_type in possible_types:
        if value_type == 'float':
            converted_value, suc = convert_to_float(stringattribute)
        elif value_type == 'int':
            converted_value, suc = convert_to_int(stringattribute)
        elif value_type == 'switch':
            converted_value, suc = convert_from_fortran_bool(stringattribute)
        elif value_type == 'string':
            suc = True
            converted_value = str(stringattribute)
        if suc:
            return converted_value

    return None

def convert_to_float(value_string):
    """
    Tries to make a float out of a string. If it can't it logs a warning
    and returns True or False if convertion worked or not.

    :param value_string: a string
    :returns value: the new float or value_string: the string given
    :returns: True if convertation was successfull, False otherwise
    """
    try:
        value = float(value_string)
    except:
        return value_string, False
    return value, True

def convert_to_int(value_string):
    """
    Tries to make a int out of a string. If it can't it logs a warning
    and returns True or False if convertion worked or not.

    :param value_string: a string
    :returns value: the new int or value_string: the string given
    :returns: True or False
    """
    try:
        value = int(value_string)
    except:
        return value_string, False
    return value, True


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
            return False, True
        if stringbool in true_items:
            return True, True
        else:
            return stringbool, False
    elif isinstance(stringbool, bool):
        return stringbool, True  # no conversion needed...
    else:
        return stringbool, False