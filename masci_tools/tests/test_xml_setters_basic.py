# -*- coding: utf-8 -*-
"""
Tests for the basic xml setter functions
"""
import os
import pytest

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_INPXML_PATH = os.path.join(FILE_PATH, 'files/fleur/Max-R5/FePt_film_SSFT_LO/files/inp2.xml')


def test_xml_set_attrib_value_no_create(load_inpxml):
    """
    Basic test of the functionality of xml_set_attrib_value_no_create
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_set_attrib_value_no_create

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/@TEST_ATT', list_return=True)) == 0

    xmltree = xml_set_attrib_value_no_create(xmltree, '/fleurInput', 'TEST_ATT', 'test')

    assert str(eval_xpath(root, '/fleurInput/@TEST_ATT')) == 'test'


def test_xml_set_attrib_value_no_create_not_str(load_inpxml):
    """
    Test of the automatic conversion to string xml_set_attrib_value_no_create
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_set_attrib_value_no_create

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/@TEST_ATT', list_return=True)) == 0

    xmltree = xml_set_attrib_value_no_create(xmltree, '/fleurInput', 'TEST_ATT', 2145)

    assert str(eval_xpath(root, '/fleurInput/@TEST_ATT')) == '2145'


def test_xml_set_attrib_value_no_create_errors(load_inpxml):
    """
    Test of the error messages in xml_set_attrib_value_no_create
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_set_attrib_value_no_create

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError, match='Wrong value for occurrences'):
        xml_set_attrib_value_no_create(xmltree,
                                       '/fleurInput/atomSpecies/species/mtSphere',
                                       'radius',
                                       'test',
                                       occurrences=5)

    with pytest.raises(ValueError, match='Wrong length for attribute values'):
        xml_set_attrib_value_no_create(xmltree,
                                       '/fleurInput/atomSpecies/species/mtSphere',
                                       'radius', ['test', 'too_much'],
                                       occurrences=[1])

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == ['2.20000000', '2.20000000']


TEST_ATTRIB_RESULTS = [['test', 'test'], ['test', 'test2'], ['test', '2214'], ['test', '2.20000000'],
                       ['2.20000000', 'test']]
TEST_ATTRIBV = ['test', ['test', 'test2'], ['test', 2214], 'test', ['test']]
TEST_OCCURENCES = [None, None, None, 0, [-1]]


@pytest.mark.parametrize('attribv, expected_result,occurrences', zip(TEST_ATTRIBV, TEST_ATTRIB_RESULTS,
                                                                     TEST_OCCURENCES))
def test_xml_set_attrib_value_no_create_all(load_inpxml, attribv, expected_result, occurrences):
    """
    Test of the functionality of xml_set_attrib_value_no_create with multiple occurrences
    of the sttribute and different values for occurrences
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_set_attrib_value_no_create

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == ['2.20000000', '2.20000000']

    xmltree = xml_set_attrib_value_no_create(xmltree,
                                             '/fleurInput/atomSpecies/species/mtSphere',
                                             'radius',
                                             attribv,
                                             occurrences=occurrences)

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == expected_result


def test_xml_set_text_no_create(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_set_text_no_create

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert eval_xpath(root, '/fleurInput').text.strip() == ''

    xmltree = xml_set_text_no_create(xmltree, '/fleurInput', 'TEST_TEXT')

    assert eval_xpath(root, '/fleurInput').text == 'TEST_TEXT'


def test_xml_set_text_no_create_errors(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_set_text_no_create

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    kpoints_xpath = '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint'

    with pytest.raises(ValueError, match='Wrong value for occurrences'):
        xml_set_text_no_create(xmltree, kpoints_xpath, 'test', occurrences=5)

    with pytest.raises(ValueError, match='Wrong length for text values'):
        xml_set_text_no_create(xmltree, kpoints_xpath, ['test', 'too_much'], occurrences=[1])

    assert eval_xpath(root, f'{kpoints_xpath}/text()') == [
        '   -0.250000     0.250000     0.000000', '    0.250000     0.250000     0.000000'
    ]


TEST_TEXT_RESULTS = [['test', 'test'], ['test', 'test2'], ['test', '    0.250000     0.250000     0.000000'],
                     ['   -0.250000     0.250000     0.000000', 'test']]
TEST_TEXTS = ['test', ['test', 'test2'], 'test', ['test']]
TEST_TEXT_OCCURENCES = [None, None, 0, [-1]]


@pytest.mark.parametrize('text, expected_result,occurrences', zip(TEST_TEXTS, TEST_TEXT_RESULTS, TEST_TEXT_OCCURENCES))
def test_xml_set_text_no_create_all(load_inpxml, text, expected_result, occurrences):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_set_text_no_create

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    kpoints_xpath = '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint'

    assert eval_xpath(root, f'{kpoints_xpath}/text()') == [
        '   -0.250000     0.250000     0.000000', '    0.250000     0.250000     0.000000'
    ]

    xmltree = xml_set_text_no_create(xmltree, kpoints_xpath, text, occurrences=occurrences)

    assert eval_xpath(root, f'{kpoints_xpath}/text()') == expected_result


def test_xml_delete_tag_single(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_delete_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/calculationSetup', list_return=True)) == 1

    xmltree = xml_delete_tag(xmltree, '/fleurInput/calculationSetup')

    assert len(eval_xpath(root, '/fleurInput/calculationSetup', list_return=True)) == 0


def test_xml_delete_tag_multiple(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_delete_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species', list_return=True)) == 2

    xmltree = xml_delete_tag(xmltree, '/fleurInput/atomSpecies/species')

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species', list_return=True)) == 0


def test_xml_delete_att_single(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_delete_att

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    keys = set([('Kmax', '4.00000000'), ('Gmax', '10.00000000'), ('GmaxXC', '8.70000000'), ('numbands', '0')])

    node = eval_xpath(root, '/fleurInput/calculationSetup/cutoffs')

    assert set(node.attrib.items()) == keys

    xmltree = xml_delete_att(xmltree, '/fleurInput/calculationSetup/cutoffs', 'Kmax')

    node = eval_xpath(root, '/fleurInput/calculationSetup/cutoffs')

    keys.discard(('Kmax', '4.00000000'))
    assert set(node.attrib.items()) == keys


def test_xml_delete_att_multiple(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_delete_att

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == ['2.20000000', '2.20000000']

    xmltree = xml_delete_att(xmltree, '/fleurInput/atomSpecies/species/mtSphere', 'radius')

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius')) == 0


def test_xml_replace_tag_single(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_replace_tag
    from lxml import etree

    replace_element = etree.Element('test_tag')
    replace_element.attrib['test_attrib'] = 'test'

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/calculationSetup/cutoffs', list_return=True)) == 1

    xmltree = xml_replace_tag(xmltree, '/fleurInput/calculationSetup/cutoffs', replace_element)

    assert len(eval_xpath(root, '/fleurInput/calculationSetup/cutoffs', list_return=True)) == 0

    nodes = eval_xpath(root, '/fleurInput/calculationSetup/test_tag', list_return=True)

    assert len(nodes) == 1
    assert nodes[0].attrib.items() == [('test_attrib', 'test')]


def test_xml_replace_tag_multiple(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_replace_tag
    from lxml import etree

    replace_element = etree.Element('test_tag')
    replace_element.attrib['test_attrib'] = 'test'

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere', list_return=True)) == 2

    xmltree = xml_replace_tag(xmltree, '/fleurInput/atomSpecies/species/mtSphere', replace_element)

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere', list_return=True)) == 0

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species/test_tag', list_return=True)

    assert len(nodes) == 2
    assert nodes[0].attrib.items() == [('test_attrib', 'test')]
    assert nodes[1].attrib.items() == [('test_attrib', 'test')]


def test_xml_create_tag_string_append(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    tags = [
        'cutoffs', 'scfLoop', 'coreElectrons', 'xcFunctional', 'magnetism', 'soc', 'prodBasis', 'expertModes',
        'geometryOptimization', 'ldaU'
    ]

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    assert [child.tag for child in node.iterchildren()] == tags

    xmltree = xml_create_tag(xmltree, '/fleurInput/calculationSetup', 'test_tag')

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    tags.append('test_tag')
    assert [child.tag for child in node.iterchildren()] == tags


def test_xml_create_tag_element_append(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_create_tag
    from lxml import etree

    new_element = etree.Element('test_tag')
    new_element.attrib['test_attrib'] = 'test'

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    tags = [
        'cutoffs', 'scfLoop', 'coreElectrons', 'xcFunctional', 'magnetism', 'soc', 'prodBasis', 'expertModes',
        'geometryOptimization', 'ldaU'
    ]

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    assert [child.tag for child in node.iterchildren()] == tags

    xmltree = xml_create_tag(xmltree, '/fleurInput/calculationSetup', new_element)

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    tags.append('test_tag')
    assert [child.tag for child in node.iterchildren()] == tags
    assert [child.attrib.items() for child in node.iterchildren()][-1] == [('test_attrib', 'test')]


def test_xml_create_tag_insert_first(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    tags = [
        'cutoffs', 'scfLoop', 'coreElectrons', 'xcFunctional', 'magnetism', 'soc', 'prodBasis', 'expertModes',
        'geometryOptimization', 'ldaU'
    ]

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    assert [child.tag for child in node.iterchildren()] == tags

    xmltree = xml_create_tag(xmltree, '/fleurInput/calculationSetup', 'test_tag', place_index=0)

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    assert [child.tag for child in node.iterchildren()] == [
        'test_tag', 'cutoffs', 'scfLoop', 'coreElectrons', 'xcFunctional', 'magnetism', 'soc', 'prodBasis',
        'expertModes', 'geometryOptimization', 'ldaU'
    ]


def test_xml_create_tag_insert_middle(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    tags = [
        'cutoffs', 'scfLoop', 'coreElectrons', 'xcFunctional', 'magnetism', 'soc', 'prodBasis', 'expertModes',
        'geometryOptimization', 'ldaU'
    ]

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    assert [child.tag for child in node.iterchildren()] == tags

    xmltree = xml_create_tag(xmltree, '/fleurInput/calculationSetup', 'test_tag', place_index=5)

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    assert [child.tag for child in node.iterchildren()] == [
        'cutoffs', 'scfLoop', 'coreElectrons', 'xcFunctional', 'magnetism', 'test_tag', 'soc', 'prodBasis',
        'expertModes', 'geometryOptimization', 'ldaU'
    ]


def test_xml_create_tag_tag_order_all_single(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    tags = [
        'cutoffs', 'scfLoop', 'coreElectrons', 'xcFunctional', 'magnetism', 'soc', 'prodBasis', 'expertModes',
        'geometryOptimization', 'ldaU'
    ]

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    assert [child.tag for child in node.iterchildren()] == tags

    order = [
        'cutoffs', 'scfLoop', 'coreElectrons', 'xcFunctional', 'magnetism', 'test_tag', 'soc', 'prodBasis',
        'expertModes', 'geometryOptimization', 'ldaU'
    ]
    xmltree = xml_create_tag(xmltree, '/fleurInput/calculationSetup', 'test_tag', tag_order=order)

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    assert [child.tag for child in node.iterchildren()] == order


def test_xml_create_tag_tag_order_multiple(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    tags = [[
        'mtSphere',
        'atomicCutoffs',
        'electronConfig',
        'energyParameters',
        'lo',
        'lo',
    ], ['mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'lo']]

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species')

    assert [[child.tag for child in node.iterchildren()] for node in nodes] == tags

    order = ['mtSphere', 'atomicCutoffs', 'electronConfig', 'test_tag', 'energyParameters', 'lo']
    xmltree = xml_create_tag(xmltree, '/fleurInput/atomSpecies/species', 'test_tag', tag_order=order)

    tags = [[
        'mtSphere',
        'atomicCutoffs',
        'electronConfig',
        'test_tag',
        'energyParameters',
        'lo',
        'lo',
    ], ['mtSphere', 'atomicCutoffs', 'electronConfig', 'test_tag', 'energyParameters', 'lo']]

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species')

    assert [[child.tag for child in node.iterchildren()] for node in nodes] == tags


def test_xml_create_tag_tag_order_multiple_selection(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    tags = [[
        'mtSphere',
        'atomicCutoffs',
        'electronConfig',
        'energyParameters',
        'lo',
        'lo',
    ], ['mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'lo']]

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species')

    assert [[child.tag for child in node.iterchildren()] for node in nodes] == tags

    order = ['mtSphere', 'atomicCutoffs', 'electronConfig', 'test_tag', 'energyParameters', 'lo']
    xmltree = xml_create_tag(xmltree, "/fleurInput/atomSpecies/species[@name='Fe-1']", 'test_tag', tag_order=order)

    tags = [[
        'mtSphere',
        'atomicCutoffs',
        'electronConfig',
        'test_tag',
        'energyParameters',
        'lo',
        'lo',
    ], ['mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'lo']]

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species')

    assert [[child.tag for child in node.iterchildren()] for node in nodes] == tags


def test_xml_create_tag_tag_order_multiple_beginning(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    tags = [[
        'mtSphere',
        'atomicCutoffs',
        'electronConfig',
        'energyParameters',
        'lo',
        'lo',
    ], ['mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'lo']]

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species')

    assert [[child.tag for child in node.iterchildren()] for node in nodes] == tags

    order = ['test_tag', 'mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'lo']
    xmltree = xml_create_tag(xmltree, '/fleurInput/atomSpecies/species', 'test_tag', tag_order=order)

    tags = [[
        'test_tag',
        'mtSphere',
        'atomicCutoffs',
        'electronConfig',
        'energyParameters',
        'lo',
        'lo',
    ], ['test_tag', 'mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'lo']]

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species')

    assert [[child.tag for child in node.iterchildren()] for node in nodes] == tags


def test_xml_create_tag_tag_order_multiple_occurrences_single(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    tags = [[
        'mtSphere',
        'atomicCutoffs',
        'electronConfig',
        'energyParameters',
        'lo',
        'lo',
    ], ['mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'lo']]

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species')

    assert [[child.tag for child in node.iterchildren()] for node in nodes] == tags

    order = ['test_tag', 'mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'lo']
    xmltree = xml_create_tag(xmltree, '/fleurInput/atomSpecies/species', 'test_tag', tag_order=order, occurrences=0)

    tags = [[
        'test_tag',
        'mtSphere',
        'atomicCutoffs',
        'electronConfig',
        'energyParameters',
        'lo',
        'lo',
    ], ['mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'lo']]

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species')

    assert [[child.tag for child in node.iterchildren()] for node in nodes] == tags


def test_xml_create_tag_tag_order_multiple_occurrences_list(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_basic import xml_create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    tags = [[
        'mtSphere',
        'atomicCutoffs',
        'electronConfig',
        'energyParameters',
        'lo',
        'lo',
    ], ['mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'lo']]

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species')

    assert [[child.tag for child in node.iterchildren()] for node in nodes] == tags

    order = ['test_tag', 'mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'lo']
    xmltree = xml_create_tag(xmltree, '/fleurInput/atomSpecies/species', 'test_tag', tag_order=order, occurrences=[-1])

    tags = [[
        'mtSphere',
        'atomicCutoffs',
        'electronConfig',
        'energyParameters',
        'lo',
        'lo',
    ], ['test_tag', 'mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'lo']]

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species')

    assert [[child.tag for child in node.iterchildren()] for node in nodes] == tags


def test_xml_create_tag_errors(load_inpxml):

    from masci_tools.util.xml.xml_setters_basic import xml_create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)

    with pytest.raises(ValueError, match=r"Could not create tag 'test_tag' because atleast one subtag is missing."):
        xml_create_tag(xmltree, '/fleurInput/calculationSetup/not_existent', 'test_tag')

    order = ['mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'lo']
    with pytest.raises(ValueError, match=r"The tag 'test_tag' was not found in the order list"):
        xml_create_tag(xmltree, '/fleurInput/atomSpecies/species', 'test_tag', tag_order=order)

    order = ['atomicCutoffs', 'electronConfig', 'energyParameters', 'lo']
    with pytest.raises(ValueError, match=r"Did not find existing elements in the tag_order list: {'mtSphere'}"):
        xml_create_tag(xmltree, '/fleurInput/atomSpecies/species', 'lo', tag_order=order)


def test_xml_create_tag_misaligned_order(load_inpxml):
    """
    Test automatic correction of order
    """

    from masci_tools.util.xml.xml_setters_basic import xml_create_tag
    from masci_tools.util.xml.common_functions import eval_xpath

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    xml_create_tag(xmltree, '/fleurInput/atomSpecies/species', 'ldaU')  #This creates an invalid order
    xml_create_tag(xmltree, '/fleurInput/atomSpecies/species', 'lo')

    order = ['mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'ldaU', 'lo']
    with pytest.raises(ValueError, match=r'Existing order does not correspond to tag_order list'):
        xml_create_tag(xmltree, '/fleurInput/atomSpecies/species', 'ldaU', tag_order=order, correct_order=False)

    with pytest.warns(UserWarning, match=r'Existing order does not correspond to tag_order list. Correcting it'):
        xml_create_tag(xmltree, '/fleurInput/atomSpecies/species', 'ldaU', tag_order=order)

    tags = [['mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'ldaU', 'ldaU', 'lo', 'lo', 'lo'],
            ['mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'ldaU', 'ldaU', 'lo', 'lo']]

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species')

    assert [[child.tag for child in node.iterchildren()] for node in nodes] == tags
