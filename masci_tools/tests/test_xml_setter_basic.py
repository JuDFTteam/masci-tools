"""
Tests for the basic xml setter functions
"""
import os
import pytest

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_INPXML_PATH = os.path.join(FILE_PATH, 'files/fleur/Max-R5/FePt_film_SSFT_LO/files/inp2.xml')

def test_xml_set_attrib_value_no_create(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_set_attrib_value_no_create


    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/@TEST_ATT', list_return=True)) == 0

    xmltree = xml_set_attrib_value_no_create(xmltree, '/fleurInput', 'TEST_ATT', 'test')

    assert str(eval_xpath(root, '/fleurInput/@TEST_ATT')) == 'test'

def test_xml_set_attrib_value_no_create_not_str(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_set_attrib_value_no_create


    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/@TEST_ATT', list_return=True)) == 0

    xmltree = xml_set_attrib_value_no_create(xmltree, '/fleurInput', 'TEST_ATT', 2145)

    assert str(eval_xpath(root, '/fleurInput/@TEST_ATT')) == '2145'


TEST_ATTRIB_RESULTS = [['test', 'test'],['test', 'test2'],['test', '2214'], ['test', '2.20000000'], ['2.20000000', 'test']]
TEST_ATTRIBV = ['test', ['test', 'test2'], ['test', 2214], 'test', ['test']]
TEST_OCCURENCES = [None,None,None,0,[-1]]

@pytest.mark.parametrize('attribv, expected_result,occurrences', zip(TEST_ATTRIBV,TEST_ATTRIB_RESULTS,TEST_OCCURENCES))
def test_xml_set_attrib_value_no_create_all(load_inpxml, attribv, expected_result, occurrences):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_set_attrib_value_no_create


    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == ['2.20000000', '2.20000000']

    xmltree = xml_set_attrib_value_no_create(xmltree, '/fleurInput/atomSpecies/species/mtSphere', 'radius', attribv, occurrences=occurrences)

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == expected_result


def test_xml_set_text_no_create(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_set_text_no_create


    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()


    assert eval_xpath(root, '/fleurInput').text.strip() == ''

    xmltree = xml_set_text_no_create(xmltree, '/fleurInput', 'TEST_TEXT')

    assert eval_xpath(root, '/fleurInput').text == 'TEST_TEXT'


TEST_TEXT_RESULTS = [['test', 'test'],['test', 'test2'], ['test', '    0.250000     0.250000     0.000000'], ['   -0.250000     0.250000     0.000000', 'test']]
TEST_TEXTS = ['test', ['test', 'test2'], 'test', ['test']]
TEST_TEXT_OCCURENCES = [None,None,0,[-1]]

@pytest.mark.parametrize('text, expected_result,occurrences', zip(TEST_TEXTS,TEST_TEXT_RESULTS,TEST_TEXT_OCCURENCES))
def test_xml_set_text_no_create_all(load_inpxml,text, expected_result,occurrences):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_set_text_no_create

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    kpoints_xpath = '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint'

    assert eval_xpath(root, f'{kpoints_xpath}/text()') == ['   -0.250000     0.250000     0.000000', '    0.250000     0.250000     0.000000']

    xmltree = xml_set_text_no_create(xmltree, kpoints_xpath, text, occurrences=occurrences)

    assert eval_xpath(root, f'{kpoints_xpath}/text()') == expected_result


def test_delete_tag_single(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import delete_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/calculationSetup', list_return=True)) == 1

    xmltree = delete_tag(xmltree, '/fleurInput/calculationSetup')

    assert len(eval_xpath(root, '/fleurInput/calculationSetup', list_return=True)) == 0


def test_delete_tag_multiple(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import delete_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species', list_return=True)) == 2

    xmltree = delete_tag(xmltree, '/fleurInput/atomSpecies/species')

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species', list_return=True)) == 0

def test_delete_att_single(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import delete_att

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    keys = set([('Kmax', '4.00000000'), ('Gmax', '10.00000000'), ('GmaxXC', '8.70000000'), ('numbands', '0')])

    node = eval_xpath(root, '/fleurInput/calculationSetup/cutoffs')

    assert set(node.attrib.items()) == keys

    xmltree = delete_att(xmltree, '/fleurInput/calculationSetup/cutoffs', 'Kmax')

    node = eval_xpath(root, '/fleurInput/calculationSetup/cutoffs')

    keys.discard(('Kmax', '4.00000000'))
    assert set(node.attrib.items()) == keys

def test_delete_att_multiple(load_inpxml):

    from masci_tools.util.xml.common_xml_util import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import delete_att

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == ['2.20000000', '2.20000000']

    xmltree = delete_att(xmltree, '/fleurInput/atomSpecies/species/mtSphere', 'radius')

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius')) == 0






