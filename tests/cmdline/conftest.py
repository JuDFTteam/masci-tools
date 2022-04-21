"""
Fixtures used for testing the cli commands
"""
from pathlib import Path
import pytest
from lxml import etree
import os
import shutil


@pytest.fixture
def fake_schemas_and_test_files(tmp_path, test_file):
    """
    Helper fixture for add fleur schema tests

    Creates a Schema form the 0.34 schemas by just changing the version number to
    0.01
    removes the corresponding folder after the tests
    """
    import masci_tools
    from masci_tools.io.parsers.fleur import register_migration
    from masci_tools.io.parsers.fleur.fleur_outxml_parser import _TaskParser

    #Create migration to be able to use the outxml_parser
    @register_migration(base_version='0.34', target_version='0.01')
    def dummy_migration(definitions):
        return definitions

    #We need to use the __file__ attribute, since we do not know, whether the package was installed with -e
    package_root = Path(masci_tools.__file__).parent.resolve()
    schema_folder = package_root / Path('io/parsers/fleur_schema/0.34/')
    created_schema_folder = package_root / Path('io/parsers/fleur_schema/0.01/')

    schema_file = schema_folder / 'FleurInputSchema.xsd'

    inputschema = etree.parse(schema_file)
    namespaces = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
    root = inputschema.xpath('/xsd:schema', namespaces=namespaces)[0]
    root.attrib['version'] = '0.01'
    root = inputschema.xpath("//xsd:simpleType[@name='FleurVersionType']/xsd:restriction/xsd:enumeration",
                             namespaces=namespaces)[0]
    root.attrib['value'] = '0.01'

    inputschema.write(tmp_path / 'FleurInputSchema.xsd', encoding='utf-8', pretty_print=True)

    schema_file = schema_folder / 'FleurOutputSchema.xsd'

    outputschema = etree.parse(schema_file)
    namespaces = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
    root = outputschema.xpath('/xsd:schema', namespaces=namespaces)[0]
    root.attrib['version'] = '0.01'
    root = outputschema.xpath("//xsd:simpleType[@name='FleurOutputVersionType']/xsd:restriction/xsd:enumeration",
                              namespaces=namespaces)[0]
    root.attrib['value'] = '0.01'

    outputschema.write(tmp_path / 'FleurOutputSchema.xsd', encoding='utf-8', pretty_print=True)

    xml_file = test_file('fleur/Max-R5/SiLOXML/files/inp.xml')
    xmltree = etree.parse(xml_file)
    root = xmltree.xpath('/fleurInput')[0]
    root.attrib['fleurInputVersion'] = '0.01'
    xmltree.write(tmp_path / 'inp.xml', encoding='utf-8', pretty_print=True)

    xml_file = test_file('fleur/Max-R5/SiLOXML/files/out.xml')
    xmltree = etree.parse(xml_file)
    root = xmltree.xpath('/fleurOutput')[0]
    root.attrib['fleurOutputVersion'] = '0.01'
    root = xmltree.xpath('//fleurInput')[0]
    root.attrib['fleurInputVersion'] = '0.01'
    xmltree.write(tmp_path / 'out.xml', encoding='utf-8', pretty_print=True)

    try:
        yield tmp_path
    finally:
        #Cleanup the folder created in the masci-tools repository
        shutil.rmtree(created_schema_folder)
        _TaskParser._migrations['0.34'].pop('0.01')  #pylint: disable=protected-access


@pytest.fixture
def remove_conversion(tmp_path):
    """
    Helper fixture for fleur inpxml converter tests

    Moves conversion to a temporary directory and back afterwards
    """
    import masci_tools

    #We need to use the __file__ attribute, since we do not know, whether the package was installed with -e
    package_root = Path(masci_tools.__file__).parent.resolve()
    conversion_folder = package_root / Path('tools/conversions')

    shutil.move(os.fspath(conversion_folder / 'conversion_031_to_034.json'), os.fspath(tmp_path))

    try:
        yield conversion_folder / 'conversion_031_to_034.json'
    finally:
        #Move the conversion back
        shutil.copy(os.fspath(tmp_path / 'conversion_031_to_034.json'), os.fspath(conversion_folder))
