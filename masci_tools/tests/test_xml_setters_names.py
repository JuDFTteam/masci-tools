# -*- coding: utf-8 -*-
"""
Tests for the functions in xml_setters_names
"""
import os
from lxml import etree
import pytest

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_INPXML_PATH = os.path.join(FILE_PATH, 'files/fleur/Max-R5/FePt_film_SSFT_LO/files/inp2.xml')


def test_create_tag(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_names import create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    tags = [child.tag for child in node.iterchildren()]
    tags.append('greensFunction')

    create_tag(xmltree, schema_dict, 'greensFunction')

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    assert [child.tag for child in node.iterchildren()] == tags


def test_create_tag_specification(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_names import create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError, match='The tag lo has multiple possible paths with the current specification.'):
        create_tag(xmltree, schema_dict, 'lo')

    create_tag(xmltree, schema_dict, 'lo', contains='species')

    los_after = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert [node.getparent().attrib['name'] for node in los_after] == ['Fe-1', 'Fe-1', 'Fe-1', 'Pt-1', 'Pt-1']
    assert [node.attrib.items() for node in los_after] == [[],
                                                           [('type', 'SCLO'), ('l', '0'), ('n', '3'), ('eDeriv', '0')],
                                                           [('type', 'SCLO'), ('l', '1'), ('n', '3'), ('eDeriv', '0')],
                                                           [],
                                                           [('type', 'SCLO'), ('l', '1'), ('n', '5'), ('eDeriv', '0')]]


def test_create_tag_create_parents(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_names import create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    tags = [child.tag for child in node.iterdescendants()]
    tags.extend(['greensFunction', 'realAxis'])

    with pytest.raises(ValueError, match="Could not create tag 'realAxis' because atleast one subtag is missing."):
        create_tag(xmltree, schema_dict, 'realAxis')

    create_tag(xmltree, schema_dict, 'realAxis', create_parents=True)

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    assert [child.tag for child in node.iterdescendants()] == tags


def test_create_tag_complex_xpath(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_names import create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    create_tag(xmltree,
               schema_dict,
               'lo',
               contains='species',
               complex_xpath="/fleurInput/atomSpecies/species[@name='Fe-1']")

    los_after = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert [node.getparent().attrib['name'] for node in los_after] == ['Fe-1', 'Fe-1', 'Fe-1', 'Pt-1']
    assert [node.attrib.items() for node in los_after] == [[],
                                                           [('type', 'SCLO'), ('l', '0'), ('n', '3'), ('eDeriv', '0')],
                                                           [('type', 'SCLO'), ('l', '1'), ('n', '3'), ('eDeriv', '0')],
                                                           [('type', 'SCLO'), ('l', '1'), ('n', '5'), ('eDeriv', '0')]]


def test_create_tag_occurrences(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_names import create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    create_tag(xmltree, schema_dict, 'lo', contains='species', occurrences=[-1])

    los_after = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert [node.getparent().attrib['name'] for node in los_after] == ['Fe-1', 'Fe-1', 'Pt-1', 'Pt-1']
    assert [node.attrib.items() for node in los_after] == [[('type', 'SCLO'), ('l', '0'), ('n', '3'), ('eDeriv', '0')],
                                                           [('type', 'SCLO'), ('l', '1'), ('n', '3'), ('eDeriv', '0')],
                                                           [],
                                                           [('type', 'SCLO'), ('l', '1'), ('n', '5'), ('eDeriv', '0')]]


def test_set_attrib_value(load_inpxml):
    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_attrib_value(xmltree, schema_dict, 'kmax', 5.321)

    kmax = eval_xpath(root, '/fleurInput/calculationSetup/cutoffs/@Kmax')

    assert kmax == '5.3210000000'


def test_set_attrib_value_specification(load_inpxml):
    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError,
                       match='The attrib radius has multiple possible paths with the current specification.'):
        set_attrib_value(xmltree, schema_dict, 'radius', [40, 42])

    set_attrib_value(xmltree, schema_dict, 'radius', [40, 42], contains='species')

    radius = eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius')

    assert radius == ['40.0000000000', '42.0000000000']


def test_set_attrib_value_create(load_inpxml):
    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(
            ValueError,
            match=
            "Could not set attribute 'ne' on path '/fleurInput/calculationSetup/greensFunction/realAxis' because atleast one subtag is missing."
    ):
        set_attrib_value(xmltree, schema_dict, 'ne', 1000, contains='realAxis')

    set_attrib_value(xmltree, schema_dict, 'ne', 1000, contains='realAxis', create=True)

    ne = eval_xpath(root, '/fleurInput/calculationSetup/greensFunction/realAxis/@ne')

    assert ne == '1000'


def test_set_attrib_value_complex_xpath(load_inpxml):
    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_attrib_value(xmltree,
                     schema_dict,
                     'type',
                     'TEST',
                     contains='species',
                     complex_xpath="/fleurInput/atomSpecies/species[@name='Fe-1']/lo")

    lo_types = eval_xpath(root, '/fleurInput/atomSpecies/species/lo/@type')

    assert lo_types == ['TEST', 'TEST', 'SCLO']


def test_set_attrib_value_occurrences(load_inpxml):
    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_attrib_value(xmltree, schema_dict, 'type', 'TEST', contains='species', occurrences=-2)

    lo_types = eval_xpath(root, '/fleurInput/atomSpecies/species/lo/@type')

    assert lo_types == ['SCLO', 'TEST', 'SCLO']


def test_set_first_attrib_value(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_first_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_first_attrib_value(xmltree, schema_dict, 'type', 'TEST', contains='species')

    lo_types = eval_xpath(root, '/fleurInput/atomSpecies/species/lo/@type')

    assert lo_types == ['TEST', 'SCLO', 'SCLO']


def test_set_first_attrib_value_complex_xpath(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_first_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_first_attrib_value(xmltree,
                           schema_dict,
                           'type',
                           'TEST',
                           contains='species',
                           complex_xpath="/fleurInput/atomSpecies/species[@name='Pt-1']/lo")

    lo_types = eval_xpath(root, '/fleurInput/atomSpecies/species/lo/@type')

    assert lo_types == ['SCLO', 'SCLO', 'TEST']


def test_set_first_attrib_value_create(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_first_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(
            ValueError,
            match=
            "Could not set attribute 'U' on path '/fleurInput/atomSpecies/species/ldaU' because atleast one subtag is missing."
    ):
        set_first_attrib_value(xmltree, schema_dict, 'U', 42, contains={'species', 'ldaU'})

    set_first_attrib_value(xmltree, schema_dict, 'U', 42, contains={'species', 'ldaU'}, create=True)

    ldaU_node = eval_xpath(root, '/fleurInput/atomSpecies/species/ldaU')

    assert ldaU_node.attrib == {'U': '42.0000000000'}
