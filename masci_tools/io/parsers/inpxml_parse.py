from lxml import etree
from pprint import pprint
from masci_tools.io.parsers.inpschema_todict import load_inpschema
from masci_tools.io.parsers.common_fleur_xml_utils import clear_xml, convert_xml_attribute

def inpxml_parse(inpxmlfile, return_errmsg=False):

    if isinstance(inpxmlfile,str):
        parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8')
        xmltree = etree.parse(inpxmlfile, parser)
    else:
        xmltree = inpxmlfile

    xmltree = clear_xml(xmltree)

    try:
        root = xmltree.getroot()
        version = root.attrib['fleurInputVersion']
    except:
        raise ValueError('Failed to extract inputVersion')

    xmlschema, schema_dict = load_inpschema(version, schmema_return=True)

    message = ''
    success = xmlschema.validate(xmltree)
    if not success:
        # get a more information on what does not validate
        message = ''
        parser_on_fly = etree.XMLParser(attribute_defaults=True, schema=xmlschema, encoding='utf-8')
        inpxmlfile = etree.tostring(xmltree)
        try:
            tree_x = etree.fromstring(inpxmlfile, parser_on_fly)
        except etree.XMLSyntaxError as msg:
            message = msg
        message = 'Reason is unknown'

    inp_dict = inpxml_todict(root, schema_dict)

    if return_errmsg:
        return inp_dict, success , message
    else:
        if not success:
            raise ValueError(f'Failed to validate the inp.xml against the Schema: {message}')
        return inp_dict


def inpxml_todict(parent, schema_dict, omitted_tags=False):
    """
    Recursive operation which transforms an xml etree to
    python nested dictionaries and lists.
    Decision to add a list is if the tag name is in the given list tag_several

    :param parent: some xmltree, or xml element
    :param schema_dict: structure/layout of the xml file in python dictionary
    :param omitted_tags: switch. If True only a list of the contained tags is returned
                         Used to omitt useless tags like e.g ['atomSpecies']['species'][3]
                         becomes ['atomSpecies'][3]

    :return: a python dictionary
    """

    return_dict = {}
    if list(parent.items()):
        return_dict = dict(list(parent.items()))
        # Now we have to convert lazy fortan style into pretty things for the Database
        for key in return_dict:
            if key in schema_dict['attrib_types']:
                converted_value = convert_xml_attribute(return_dict[key], schema_dict['attrib_types'][key])
                if converted_value is not None:
                    return_dict[key] = converted_value
            else:
                pass #This key should be in simple_elements

    if parent.text:  # TODO more detal, exp: relPos, basic_elements should have all tags with text and can split them apart and convert to the given type
        # has text, but we don't want all the '\n' s and empty stings in the database
        if parent.text.strip() != '':  # might not be the best solutions
            base_text = parent.text.strip()
            split_text = base_text.split(' ')
            while '' in split_text:
                split_text.remove('')
            if parent.tag not in schema_dict['simple_elements']:
                raise KeyError(f'Something is wrong in the schema_dict: {parent.tag} is not in simple_elements')
            text_definition = None
            if isinstance(schema_dict['simple_elements'][parent.tag],dict):
                text_definition = schema_dict['simple_elements'][parent.tag]
            else:
                for possible_def in schema_dict['simple_elements'][parent.tag]:
                    if possible_def['length'] == len(split_text) or \
                       (possible_def['length'] == 1 and len(split_text) != 1):
                       text_definition = possible_def
            if text_definition['length'] == 1:
                converted_value = convert_xml_attribute(base_text, text_definition['type'])
                if converted_value is not None:
                    if not return_dict:
                        return_dict = converted_value
                    else:
                        return_dict['value'] = converted_value
            else:
                text_list = []
                for value in split_text:
                    converted_value = convert_xml_attribute(value, text_definition['type'])
                    if converted_value is not None:
                        text_list.append(converted_value)
                if not return_dict:
                    return_dict = text_list
                else:
                    return_dict['value'] = text_list


    for element in parent:
        if element.tag in schema_dict['tags_several']:
            # make a list, otherwise the tag will be overwritten in the dict
            if element.tag not in return_dict:  # is this the first occurence?
                if omitted_tags:
                    if len(return_dict) == 0:
                        return_dict = []
                else:
                    return_dict[element.tag] = []
            if omitted_tags:
                return_dict.append(inpxml_todict(element, schema_dict))
            else:
                return_dict[element.tag].append(inpxml_todict(element, schema_dict))
        elif element.tag in schema_dict['omitt_contained_tags']:
            #The tags on level deeper are not useful in a parsed python dictionary
            return_dict[element.tag] = inpxml_todict(element, schema_dict, omitted_tags=True)
        else:
            return_dict[element.tag] = inpxml_todict(element, schema_dict)

    return return_dict

