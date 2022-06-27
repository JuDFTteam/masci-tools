"""
Tests for the load functions in fleur_xml
"""
from lxml import etree
import pytest
from pathlib import Path


def test_load_inpxml(test_file):
    from masci_tools.io.fleur_xml import load_inpxml

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

    #Pass file content as bytes
    with open(TEST_INPXML_PATH, 'rb') as inpfile:
        content = inpfile.read()
    xmltree, schema_dict = load_inpxml(content, base_url=TEST_INPXML_PATH)

    #Pass file content as string
    with open(TEST_INPXML_PATH, encoding='utf-8') as inpfile:
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
    with open(TEST_INPXML_PATH, encoding='utf-8') as inpfile:
        content = inpfile.read()
    with pytest.warns(UserWarning):
        xmltree, schema_dict = load_inpxml(content)

    assert xmltree is not None
    assert schema_dict['inp_version'] == '0.34'


def test_load_outxml(test_file):
    from masci_tools.io.fleur_xml import load_outxml

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

    #Pass file content as bytes
    with open(TEST_OUTXML_PATH, 'rb') as outfile:
        content = outfile.read()
    xmltree, schema_dict = load_outxml(content, base_url=TEST_OUTXML_PATH)

    #Pass file content as string
    with open(TEST_OUTXML_PATH, encoding='utf-8') as outfile:
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
    with open(TEST_OUTXML_PATH, encoding='utf-8') as outfile:
        content = outfile.read()
    with pytest.warns(UserWarning):
        xmltree, schema_dict = load_outxml(content)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.34'
    assert schema_dict['inp_version'] == '0.34'


def test_loadoutxml_mixedversions(test_file):
    from masci_tools.io.fleur_xml import load_outxml

    TEST_OUTXML_PATH = test_file('fleur/output_mixed_versions.xml')

    xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.34'
    assert schema_dict['inp_version'] == '0.33'


def test_loadoutxml_max50(test_file):
    from masci_tools.io.fleur_xml import load_outxml

    TEST_OUTXML_PATH = test_file('fleur/old_versions/Max5_0_test_out.xml')

    with pytest.warns(UserWarning):
        xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.33'
    assert schema_dict['inp_version'] == '0.33'


def test_loadoutxml_max40(test_file):
    from masci_tools.io.fleur_xml import load_outxml

    TEST_OUTXML_PATH = test_file('fleur/old_versions/Max4_test_out.xml')

    with pytest.warns(UserWarning):
        xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.31'
    assert schema_dict['inp_version'] == '0.31'


def test_loadoutxml_max31(test_file):
    from masci_tools.io.fleur_xml import load_outxml

    TEST_OUTXML_PATH = test_file('fleur/old_versions/Max3_1_test_out.xml')

    with pytest.warns(UserWarning):
        xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.30'
    assert schema_dict['inp_version'] == '0.30'


def test_loadoutxml_premax31(test_file):
    from masci_tools.io.fleur_xml import load_outxml

    TEST_OUTXML_PATH = test_file('fleur/old_versions/Max3_0_test_out.xml')

    with pytest.warns(UserWarning):
        xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH)

    assert xmltree is not None
    assert schema_dict['out_version'] == '0.29'
    assert schema_dict['inp_version'] == '0.29'


def test_get_constants(load_inpxml, load_outxml):
    """
    Test of the get_constants function
    """
    from masci_tools.io.fleur_xml import get_constants

    VALID_INP_CONSTANTS_PATH = 'fleur/inp_with_constants.xml'
    INVALID_INP_CONSTANTS_PATH = 'fleur/inp_invalid_constants.xml'
    VALID_OUT_CONSTANTS_PATH = 'fleur/out_with_constants.xml'

    xmltree, schema_dict = load_inpxml(VALID_INP_CONSTANTS_PATH, absolute=False)
    invalidxmltree, _ = load_inpxml(INVALID_INP_CONSTANTS_PATH, absolute=False)
    outxmltree, outschema_dict = load_outxml(VALID_OUT_CONSTANTS_PATH, absolute=False)

    expected_constants = {
        'A': -3.14,
        'Ang': 1.889726124772898,
        'Bohr': 1.0,
        'Deg': 0.017453292519943295,
        'Pi': 3.141592653589793,
        'nm': 18.89726124772898,
        'notPi': 3.0,
        'pm': 0.01889726124772898,
        'Htr': 1.0,
        'Ry': 0.5,
        'eV': 0.03674932217565499
    }
    result = get_constants(xmltree, schema_dict)
    assert result == expected_constants

    result = get_constants(outxmltree, outschema_dict)
    assert result == expected_constants

    with pytest.raises(KeyError, match='Ambiguous definition of constant Pi'):
        result = get_constants(invalidxmltree, schema_dict)
