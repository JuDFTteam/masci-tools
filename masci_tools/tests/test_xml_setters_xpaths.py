# -*- coding: utf-8 -*-
"""
Tests of the functions xml_setter_xpaths
"""
import os
from lxml import etree
import pytest

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_INPXML_PATH = os.path.join(FILE_PATH, 'files/fleur/Max-R5/FePt_film_SSFT_LO/files/inp2.xml')


def test_xml_create_tag_schema_dict(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_create_tag_schema_dict

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    los_before = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert [node.getparent().attrib['name'] for node in los_before] == ['Fe-1', 'Fe-1', 'Pt-1']
    assert [node.attrib.items() for node in los_before] == [[('type', 'SCLO'), ('l', '0'), ('n', '3'), ('eDeriv', '0')],
                                                            [('type', 'SCLO'), ('l', '1'), ('n', '3'), ('eDeriv', '0')],
                                                            [('type', 'SCLO'), ('l', '1'), ('n', '5'), ('eDeriv', '0')]]

    xml_create_tag_schema_dict(xmltree, schema_dict, '/fleurInput/atomSpecies/species',
                               '/fleurInput/atomSpecies/species', 'lo')

    los_after = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert [node.getparent().attrib['name'] for node in los_after] == ['Fe-1', 'Fe-1', 'Fe-1', 'Pt-1', 'Pt-1']
    assert [node.attrib.items() for node in los_after] == [[],
                                                           [('type', 'SCLO'), ('l', '0'), ('n', '3'), ('eDeriv', '0')],
                                                           [('type', 'SCLO'), ('l', '1'), ('n', '3'), ('eDeriv', '0')],
                                                           [],
                                                           [('type', 'SCLO'), ('l', '1'), ('n', '5'), ('eDeriv', '0')]]


def test_xml_create_tag_schema_dict_differing_xpaths(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_create_tag_schema_dict

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    los_before = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert [node.getparent().attrib['name'] for node in los_before] == ['Fe-1', 'Fe-1', 'Pt-1']
    assert [node.attrib.items() for node in los_before] == [[('type', 'SCLO'), ('l', '0'), ('n', '3'), ('eDeriv', '0')],
                                                            [('type', 'SCLO'), ('l', '1'), ('n', '3'), ('eDeriv', '0')],
                                                            [('type', 'SCLO'), ('l', '1'), ('n', '5'), ('eDeriv', '0')]]

    xml_create_tag_schema_dict(xmltree, schema_dict, "/fleurInput/atomSpecies/species[@name='Fe-1']",
                               '/fleurInput/atomSpecies/species', 'lo')

    los_after = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert [node.getparent().attrib['name'] for node in los_after] == ['Fe-1', 'Fe-1', 'Fe-1', 'Pt-1']
    assert [node.attrib.items() for node in los_after] == [[],
                                                           [('type', 'SCLO'), ('l', '0'), ('n', '3'), ('eDeriv', '0')],
                                                           [('type', 'SCLO'), ('l', '1'), ('n', '3'), ('eDeriv', '0')],
                                                           [('type', 'SCLO'), ('l', '1'), ('n', '5'), ('eDeriv', '0')]]


def test_xml_create_tag_schema_dict_element(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_create_tag_schema_dict

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    new_element = etree.Element('ldaU')
    new_element.attrib['test_attrib'] = 'test'

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/ldaU', list_return=True)) == 0

    xml_create_tag_schema_dict(xmltree, schema_dict, '/fleurInput/atomSpecies/species',
                               '/fleurInput/atomSpecies/species', new_element)

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species/ldaU', list_return=True)

    assert [node.getparent().attrib['name'] for node in nodes] == ['Fe-1', 'Pt-1']
    assert [node.attrib.items() for node in nodes] == [[('test_attrib', 'test')], [('test_attrib', 'test')]]


def test_xml_create_tag_schema_dict_create_parents(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_create_tag_schema_dict

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError, match="Could not create tag 'addArg' because atleast one subtag is missing."):
        xml_create_tag_schema_dict(xmltree, schema_dict, "/fleurInput/atomSpecies/species[@name='Fe-1']/ldaHIA",
                                   '/fleurInput/atomSpecies/species/ldaHIA', 'addArg')

    xml_create_tag_schema_dict(xmltree,
                               schema_dict,
                               "/fleurInput/atomSpecies/species[@name='Fe-1']/ldaHIA",
                               '/fleurInput/atomSpecies/species/ldaHIA',
                               'addArg',
                               create_parents=True)

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/ldaHIA/addArg', list_return=True)) == 1


def test_eval_xpath_create_existing(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import eval_xpath_create

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/lo')) == 3

    nodes = eval_xpath_create(xmltree, schema_dict, '/fleurInput/atomSpecies/species/lo',
                              '/fleurInput/atomSpecies/species/lo')

    assert len(nodes) == 3


def test_eval_xpath_create_non_existing(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import eval_xpath_create

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/ldaU')) == 0

    nodes = eval_xpath_create(xmltree, schema_dict, '/fleurInput/atomSpecies/species/ldaU',
                              '/fleurInput/atomSpecies/species/ldaU')

    assert len(nodes) == 2
    assert [node.getparent().attrib['name'] for node in nodes] == ['Fe-1', 'Pt-1']


def test_eval_xpath_create_differing_xpaths(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import eval_xpath_create

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/ldaU')) == 0

    nodes = eval_xpath_create(xmltree, schema_dict, "/fleurInput/atomSpecies/species[@name='Fe-1']/ldaU",
                              '/fleurInput/atomSpecies/species/ldaU')

    assert len(nodes) == 1
    assert [node.getparent().attrib['name'] for node in nodes] == ['Fe-1']


def test_eval_xpath_create_create_parents(load_inpxml):

    from masci_tools.util.xml.xml_setters_xpaths import eval_xpath_create

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)

    with pytest.raises(ValueError, match="Could not create tag 'addArg' because atleast one subtag is missing."):
        eval_xpath_create(xmltree, schema_dict, "/fleurInput/atomSpecies/species[@name='Fe-1']/ldaHIA/addArg",
                          '/fleurInput/atomSpecies/species/ldaHIA/addArg')

    nodes = eval_xpath_create(xmltree,
                              schema_dict,
                              "/fleurInput/atomSpecies/species[@name='Fe-1']/ldaHIA/addArg",
                              '/fleurInput/atomSpecies/species/ldaHIA/addArg',
                              create_parents=True)

    assert len(nodes) == 1


TEST_ATTRIB_NAME = ['Kmax', 'kmax', 'KMAX']
TEST_VALUES = ['9.000000', 5.321, 'Pi/4.0']
TEST_RESULTS = ['9.000000', '5.3210000000', 'Pi/4.0']


@pytest.mark.parametrize('attribname, attribvalue, result', zip(TEST_ATTRIB_NAME, TEST_VALUES, TEST_RESULTS))
def test_xml_set_attrib_value(load_inpxml, attribname, attribvalue, result):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    xml_set_attrib_value(xmltree, schema_dict, '/fleurInput/calculationSetup/cutoffs',
                         '/fleurInput/calculationSetup/cutoffs', attribname, attribvalue)

    assert str(eval_xpath(root, '/fleurInput/calculationSetup/cutoffs/@Kmax')) == result
