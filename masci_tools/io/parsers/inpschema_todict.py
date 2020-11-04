"""
This module provides the functionality to create/load the schema_dict for the
FleurInputSchema.xsd
"""
import masci_tools.io.parsers.fleur_schema_parser_functions as schema_parse
from masci_tools.io.parsers.common_fleur_xml_utils import clear_xml
from lxml import etree
from pprint import pprint
import importlib.util
import os

def create_inpschema_dict(path):
    """
    Creates dictionary with information about the FleurInputSchema.xsd and writes
    it to the same folder in a file called schema_dict.py

    The functions, whose results are added to the schema_dict and the corresponding keys
    are defined in schema_actions

    :param parent: str path to the folder containing the FleurInputSchema.xsd file
    """

    #Add new functionality to this dictionary here
    schema_actions = {'tag_paths': schema_parse.get_tag_paths,
                      'attrib_paths': schema_parse.get_attrib_paths,
                      'tags_several': schema_parse.get_tags_several,
                      'tag_order': schema_parse.get_tags_order,
                      'attrib_types': schema_parse.extract_attribute_types,
                      'settable_attribs': schema_parse.get_settable_attributes,
                      'simple_elements': schema_parse.get_basic_elements,
                      'omitt_contained_tags': schema_parse.get_omittable_tags,
                      }

    print(f'processing: {path}/FleurInputSchema.xsd')
    xmlschema = etree.parse(f'{path}/FleurInputSchema.xsd')
    xmlschema = clear_xml(xmlschema)

    namespaces = {"xsd": "http://www.w3.org/2001/XMLSchema"}
    inp_version = xmlschema.xpath("/xsd:schema/@version", namespaces=namespaces)[0]
    schema_dict = {}
    for key, action in schema_actions.items():
        schema_dict[key] = action(xmlschema,namespaces,**schema_dict)

    with open(f'{path}/schema_dict.py','w') as f:
        f.write(f"__inp_version__ = '{inp_version}'\n")
        f.write('inpschema_dict = ')
        pprint(schema_dict, f)


def load_inpschema(version, schmema_return=False):
    """
    load the FleurInputSchema dict for the specified version
    """

    PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

    fleur_schema_path = f'./fleur_schema/input/{version}'

    path = os.path.abspath(os.path.join(PACKAGE_DIRECTORY, fleur_schema_path))

    schema_file_path = os.path.join(path,'FleurInputSchema.xsd')
    schema_dict_path = os.path.join(path,'schema_dict.py')
    if not os.path.isfile(schema_file_path):
        raise ValueError(f'No input schema found at {path}')

    if not os.path.isfile(schema_dict_path):
        print(f'Generating schema_dict file for given input schema: {schema_file_path}')
        create_schema_dict(path)

    #import schema_dict
    spec = importlib.util.spec_from_file_location("schema", schema_dict_path)
    schema = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(schema)
    if schema.__inp_version__ != version:
        raise ValueError(f'Something has gone wrong specified version does not match __inp_version__ in loaded schema_dict')
    print(f'Loaded schema_dict input version {schema.__inp_version__}')

    if schmema_return:
        xmlschema_doc = etree.parse(schema_file_path)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        return xmlschema, schema.inpschema_dict
    else:
        return schema.inpschema_dict