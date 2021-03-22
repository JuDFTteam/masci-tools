# -*- coding: utf-8 -*-
"""
Tests for the load functions in io_fleurxml
"""
from lxml import etree
import os
import pytest

FILE_PATH = os.path.dirname(os.path.abspath(__file__))


def test_load_inpxml():
    from masci_tools.io.io_fleurxml import load_inpxml

    TEST_INPXML_PATH = os.path.join(FILE_PATH, 'files/fleur/Max-R5/FePt_film_SSFT_LO/files/inp2.xml')

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)

    assert xmltree is not None
    assert schema_dict['inp_version'] == '0.34'

    #Parse before
    parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8')
    xmltree = etree.parse(TEST_INPXML_PATH, parser)
    xmltree, schema_dict = load_inpxml(xmltree)

    assert xmltree is not None
    assert schema_dict['inp_version'] == '0.34'

    #Pass file handle
    with open(TEST_INPXML_PATH, 'r') as inpfile:
        xmltree, schema_dict = load_inpxml(inpfile)

    assert xmltree is not None
    assert schema_dict['inp_version'] == '0.34'


def test_load_outxml():
    from masci_tools.io.io_fleurxml import load_outxml

    TEST_OUTXML_PATH = os.path.join(FILE_PATH, 'files/fleur/Max-R5/SiLOXML/files/out.xml')

    xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.34'
    assert schema_dict['inp_version'] == '0.34'

    #Parse before
    parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8')
    xmltree = etree.parse(TEST_OUTXML_PATH, parser)
    xmltree, schema_dict = load_outxml(xmltree)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.34'
    assert schema_dict['inp_version'] == '0.34'

    #Pass file handle
    with open(TEST_OUTXML_PATH, 'r') as inpfile:
        xmltree, schema_dict = load_outxml(inpfile)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.34'
    assert schema_dict['inp_version'] == '0.34'


def test_loadoutxml_mixedversions():
    from masci_tools.io.io_fleurxml import load_outxml

    TEST_OUTXML_PATH = os.path.join(FILE_PATH, 'files/fleur/output_mixed_versions.xml')

    xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.34'
    assert schema_dict['inp_version'] == '0.33'


def test_loadoutxml_max50():
    from masci_tools.io.io_fleurxml import load_outxml

    TEST_OUTXML_PATH = os.path.join(FILE_PATH, 'files/fleur/old_versions/Max5_0_test_out.xml')

    with pytest.warns(UserWarning):
        xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.33'
    assert schema_dict['inp_version'] == '0.33'


def test_loadoutxml_max40():
    from masci_tools.io.io_fleurxml import load_outxml

    TEST_OUTXML_PATH = os.path.join(FILE_PATH, 'files/fleur/old_versions/Max4_test_out.xml')

    with pytest.warns(UserWarning):
        xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.31'
    assert schema_dict['inp_version'] == '0.31'


def test_loadoutxml_max31():
    from masci_tools.io.io_fleurxml import load_outxml

    TEST_OUTXML_PATH = os.path.join(FILE_PATH, 'files/fleur/old_versions/Max3_1_test_out.xml')

    with pytest.warns(UserWarning):
        xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.30'
    assert schema_dict['inp_version'] == '0.30'


def test_loadoutxml_premax31():
    from masci_tools.io.io_fleurxml import load_outxml

    TEST_OUTXML_PATH = os.path.join(FILE_PATH, 'files/fleur/old_versions/Max3_0_test_out.xml')

    with pytest.warns(UserWarning):
        xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.29'
    assert schema_dict['inp_version'] == '0.29'
