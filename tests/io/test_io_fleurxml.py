"""
Tests for the load functions in io_fleurxml
"""
from lxml import etree
import pytest
from pathlib import Path


def test_load_inpxml(test_file):
    from masci_tools.io.io_fleurxml import load_inpxml

    TEST_INPXML_PATH = test_file('fleur/Max-R5/FePt_film_SSFT_LO/files/inp2.xml')

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
    with open(TEST_INPXML_PATH, encoding='utf-8') as inpfile:
        xmltree, schema_dict = load_inpxml(inpfile)

    assert xmltree is not None
    assert schema_dict['inp_version'] == '0.34'

    #Pass file content
    with open(TEST_INPXML_PATH, 'rb') as inpfile:
        content = inpfile.read()
    xmltree, schema_dict = load_inpxml(content, base_url=TEST_INPXML_PATH)

    assert xmltree is not None
    assert schema_dict['inp_version'] == '0.34'

    #Pass file content with pathlib base_url
    with open(TEST_INPXML_PATH, 'rb') as inpfile:
        content = inpfile.read()
    xmltree, schema_dict = load_inpxml(content, base_url=Path(TEST_INPXML_PATH))

    assert xmltree is not None
    assert schema_dict['inp_version'] == '0.34'

    #Pass file content
    with open(TEST_INPXML_PATH, 'rb') as inpfile:
        content = inpfile.read()
    with pytest.warns(UserWarning):
        xmltree, schema_dict = load_inpxml(content)

    assert xmltree is not None
    assert schema_dict['inp_version'] == '0.34'


def test_load_outxml(test_file):
    from masci_tools.io.io_fleurxml import load_outxml

    TEST_OUTXML_PATH = test_file('fleur/Max-R5/SiLOXML/files/out.xml')

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
    with open(TEST_OUTXML_PATH, encoding='utf-8') as outfile:
        xmltree, schema_dict = load_outxml(outfile)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.34'
    assert schema_dict['inp_version'] == '0.34'

    #Pass file content
    with open(TEST_OUTXML_PATH, 'rb') as outfile:
        content = outfile.read()
    xmltree, schema_dict = load_outxml(content, base_url=TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.34'
    assert schema_dict['inp_version'] == '0.34'

    #Pass file content with pathlib base_url
    with open(TEST_OUTXML_PATH, 'rb') as outfile:
        content = outfile.read()
    xmltree, schema_dict = load_outxml(content, base_url=Path(TEST_OUTXML_PATH))

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.34'
    assert schema_dict['inp_version'] == '0.34'

    #Pass file content with pathlib base_url
    with open(TEST_OUTXML_PATH, 'rb') as outfile:
        content = outfile.read()
    with pytest.warns(UserWarning):
        xmltree, schema_dict = load_outxml(content)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.34'
    assert schema_dict['inp_version'] == '0.34'


def test_loadoutxml_mixedversions(test_file):
    from masci_tools.io.io_fleurxml import load_outxml

    TEST_OUTXML_PATH = test_file('fleur/output_mixed_versions.xml')

    xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.34'
    assert schema_dict['inp_version'] == '0.33'


def test_loadoutxml_max50(test_file):
    from masci_tools.io.io_fleurxml import load_outxml

    TEST_OUTXML_PATH = test_file('fleur/old_versions/Max5_0_test_out.xml')

    with pytest.warns(UserWarning):
        xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.33'
    assert schema_dict['inp_version'] == '0.33'


def test_loadoutxml_max40(test_file):
    from masci_tools.io.io_fleurxml import load_outxml

    TEST_OUTXML_PATH = test_file('fleur/old_versions/Max4_test_out.xml')

    with pytest.warns(UserWarning):
        xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.31'
    assert schema_dict['inp_version'] == '0.31'


def test_loadoutxml_max31(test_file):
    from masci_tools.io.io_fleurxml import load_outxml

    TEST_OUTXML_PATH = test_file('fleur/old_versions/Max3_1_test_out.xml')

    with pytest.warns(UserWarning):
        xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.30'
    assert schema_dict['inp_version'] == '0.30'


def test_loadoutxml_premax31(test_file):
    from masci_tools.io.io_fleurxml import load_outxml

    TEST_OUTXML_PATH = test_file('fleur/old_versions/Max3_0_test_out.xml')

    with pytest.warns(UserWarning):
        xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.29'
    assert schema_dict['inp_version'] == '0.29'
