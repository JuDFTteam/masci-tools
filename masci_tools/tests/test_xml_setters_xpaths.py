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

    from masci_tools.util.xml.common_functions import eval_xpath
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

    from masci_tools.util.xml.common_functions import eval_xpath
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

    from masci_tools.util.xml.common_functions import eval_xpath
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

    from masci_tools.util.xml.common_functions import eval_xpath
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

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import eval_xpath_create

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/lo')) == 3

    nodes = eval_xpath_create(xmltree, schema_dict, '/fleurInput/atomSpecies/species/lo',
                              '/fleurInput/atomSpecies/species/lo')

    assert len(nodes) == 3


def test_eval_xpath_create_non_existing(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import eval_xpath_create

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/ldaU')) == 0

    nodes = eval_xpath_create(xmltree, schema_dict, '/fleurInput/atomSpecies/species/ldaU',
                              '/fleurInput/atomSpecies/species/ldaU')

    assert len(nodes) == 2
    assert [node.getparent().attrib['name'] for node in nodes] == ['Fe-1', 'Pt-1']


def test_eval_xpath_create_differing_xpaths(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import eval_xpath_create

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/ldaU')) == 0

    nodes = eval_xpath_create(xmltree,
                              schema_dict,
                              "/fleurInput/atomSpecies/species[@name='Fe-1']/ldaU",
                              '/fleurInput/atomSpecies/species/ldaU',
                              list_return=True)

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
                              create_parents=True,
                              list_return=True)

    assert len(nodes) == 1


TEST_ATTRIB_NAME = ['Kmax', 'kmax', 'KMAX']
TEST_VALUES = ['9.000000', 5.321, 'Pi/4.0']
TEST_RESULTS = ['9.000000', '5.3210000000', 'Pi/4.0']


@pytest.mark.parametrize('attribname, attribvalue, result', zip(TEST_ATTRIB_NAME, TEST_VALUES, TEST_RESULTS))
def test_xml_set_attrib_value(load_inpxml, attribname, attribvalue, result):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    xml_set_attrib_value(xmltree, schema_dict, '/fleurInput/calculationSetup/cutoffs',
                         '/fleurInput/calculationSetup/cutoffs', attribname, attribvalue)

    assert str(eval_xpath(root, '/fleurInput/calculationSetup/cutoffs/@Kmax')) == result


#The integer argument is converted to float since the arguemnt radius is float_expression (either float or str)
TEST_ATTRIB_RESULTS = [['test', 'test'], ['test', 'test2'], ['test', '2214.0000000000'], ['test', '2.20000000'],
                       ['2.20000000', 'test']]
TEST_ATTRIBV = ['test', ['test', 'test2'], ['test', 2214], 'test', ['test']]
TEST_OCCURENCES = [None, None, None, 0, [-1]]


@pytest.mark.parametrize('attribv, expected_result,occurrences', zip(TEST_ATTRIBV, TEST_ATTRIB_RESULTS,
                                                                     TEST_OCCURENCES))
def test_xml_set_attrib_value_all(load_inpxml, attribv, expected_result, occurrences):
    """
    Test of the functionality of xml_set_attrib_value_no_create with multiple occurrences
    of the sttribute and different values for occurrences
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == ['2.20000000', '2.20000000']

    xmltree = xml_set_attrib_value(xmltree,
                                   schema_dict,
                                   '/fleurInput/atomSpecies/species/mtSphere',
                                   '/fleurInput/atomSpecies/species/mtSphere',
                                   'radius',
                                   attribv,
                                   occurrences=occurrences)

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == expected_result


def test_xml_set_attrib_value_differing_xpaths(load_inpxml):
    """
    Test of the functionality of xml_set_attrib_value_no_create with multiple occurrences
    of the attribute and different values for occurrences
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == ['2.20000000', '2.20000000']

    xmltree = xml_set_attrib_value(xmltree, schema_dict, "/fleurInput/atomSpecies/species[@name='Fe-1']/mtSphere",
                                   '/fleurInput/atomSpecies/species/mtSphere', 'radius', 'TEST')

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == ['TEST', '2.20000000']


def test_xml_set_attrib_value_create(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError, match="Could not set attribute 'key' on path "):
        xml_set_attrib_value(xmltree, schema_dict, "/fleurInput/atomSpecies/species[@name='Fe-1']/ldaHIA/addArg",
                             '/fleurInput/atomSpecies/species/ldaHIA/addArg', 'key', 'TEST')

    xml_set_attrib_value(xmltree,
                         schema_dict,
                         "/fleurInput/atomSpecies/species[@name='Fe-1']/ldaHIA/addArg",
                         '/fleurInput/atomSpecies/species/ldaHIA/addArg',
                         'key',
                         'TEST',
                         create=True)

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/ldaHIA/addArg/@key') == 'TEST'


def test_xml_set_first_attrib_value(load_inpxml):
    """
    Test of the functionality of xml_set_attrib_value_no_create with multiple occurrences
    of the sttribute and different values for occurrences
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_first_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == ['2.20000000', '2.20000000']

    xmltree = xml_set_first_attrib_value(xmltree, schema_dict, '/fleurInput/atomSpecies/species/mtSphere',
                                         '/fleurInput/atomSpecies/species/mtSphere', 'radius', 'TEST')

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == ['TEST', '2.20000000']


def test_xml_set_first_attrib_value_create(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_first_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError, match="Could not set attribute 'key' on path "):
        xml_set_first_attrib_value(xmltree, schema_dict, "/fleurInput/atomSpecies/species[@name='Fe-1']/ldaHIA/addArg",
                                   '/fleurInput/atomSpecies/species/ldaHIA/addArg', 'key', 'TEST')

    xml_set_first_attrib_value(xmltree,
                               schema_dict,
                               "/fleurInput/atomSpecies/species[@name='Fe-1']/ldaHIA/addArg",
                               '/fleurInput/atomSpecies/species/ldaHIA/addArg',
                               'key',
                               'TEST',
                               create=True)

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/ldaHIA/addArg/@key') == 'TEST'


def test_xml_set_text(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_text

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    xml_set_text(xmltree, schema_dict, '/fleurInput/comment', '/fleurInput/comment', 'TEST_COMMENT')

    assert str(eval_xpath(root, '/fleurInput/comment/text()')) == 'TEST_COMMENT'


TEST_TEXT_RESULTS = [
    [' 1.0000000000000  1.0000000000000  1.0000000000000', ' 1.0000000000000  1.0000000000000  1.0000000000000'],
    ['1.0 1.0 1.0', '1.0 1.0 1.0'],
    [' 1.0000000000000  1.0000000000000  1.0000000000000', ' 2.0000000000000  2.0000000000000  2.0000000000000'],
    ['   -0.250000     0.250000     0.000000', '-20 30 40']
]
TEST_TEXTS = [[1.0, 1.0, 1.0], ['1.0', '1.0', '1.0'], [[1.0, 1.0, 1.0], [2.0, 2.0, 2.0]], ['-20', '30', '40']]
TEST_TEXT_OCCURENCES = [None, None, None, [-1]]


@pytest.mark.parametrize('text, expected_result,occurrences', zip(TEST_TEXTS, TEST_TEXT_RESULTS, TEST_TEXT_OCCURENCES))
def test_xml_set_text_all(load_inpxml, text, expected_result, occurrences):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_text

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    kpoints_xpath = '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint'

    assert eval_xpath(root, f'{kpoints_xpath}/text()') == [
        '   -0.250000     0.250000     0.000000', '    0.250000     0.250000     0.000000'
    ]

    xmltree = xml_set_text(xmltree, schema_dict, kpoints_xpath, kpoints_xpath, text, occurrences=occurrences)

    assert eval_xpath(root, f'{kpoints_xpath}/text()') == expected_result


def test_xml_set_text_differing_xpaths(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_text

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    kpoints_xpath = '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint'

    assert eval_xpath(root, f'{kpoints_xpath}/text()') == [
        '   -0.250000     0.250000     0.000000', '    0.250000     0.250000     0.000000'
    ]

    xmltree = xml_set_text(xmltree, schema_dict, f'{kpoints_xpath}[2]', kpoints_xpath, ['1.0', '1.0', '1.0'])

    assert eval_xpath(root, f'{kpoints_xpath}/text()') == ['   -0.250000     0.250000     0.000000', '1.0 1.0 1.0']


def test_xml_set_text_create(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_text

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError, match='Could not set text on path'):
        xml_set_text(xmltree, schema_dict,
                     "/fleurInput/atomSpecies/species[@name='Fe-1']/torgueCalculation/greensfElements/s",
                     '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/s', [False, False, True, False])

    xml_set_text(xmltree,
                 schema_dict,
                 "/fleurInput/atomSpecies/species[@name='Fe-1']/torgueCalculation/greensfElements/s",
                 '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/s', [False, False, True, False],
                 create=True)

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/s/text()') == 'F F T F'


def test_xml_set_first_text(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_first_text

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    kpoints_xpath = '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint'

    assert eval_xpath(root, f'{kpoints_xpath}/text()') == [
        '   -0.250000     0.250000     0.000000', '    0.250000     0.250000     0.000000'
    ]

    xmltree = xml_set_first_text(xmltree, schema_dict, kpoints_xpath, kpoints_xpath, [1.0, 1.0, 1.0])

    assert eval_xpath(root, f'{kpoints_xpath}/text()') == [
        ' 1.0000000000000  1.0000000000000  1.0000000000000', '    0.250000     0.250000     0.000000'
    ]


def test_xml_set_first_text_create(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_first_text

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError, match='Could not set text on path'):
        xml_set_first_text(xmltree, schema_dict,
                           "/fleurInput/atomSpecies/species[@name='Fe-1']/torgueCalculation/greensfElements/s",
                           '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/s',
                           [False, False, True, False])

    xml_set_first_text(xmltree,
                       schema_dict,
                       "/fleurInput/atomSpecies/species[@name='Fe-1']/torgueCalculation/greensfElements/s",
                       '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/s',
                       [False, False, True, False],
                       create=True)

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/s/text()') == 'F F T F'


TEST_SHIFT_ATTRIB_NAME = ['Kmax', 'kmax', 'KMAX']
TEST_SHIFT_VALUES = ['9.000000', 5.321, '9.000000']
TEST_SHIFT_RESULTS = ['13.0000000000', '9.3210000000', '13.0000000000']


@pytest.mark.parametrize('attribname, shift_value, result',
                         zip(TEST_SHIFT_ATTRIB_NAME, TEST_SHIFT_VALUES, TEST_SHIFT_RESULTS))
def test_xml_add_number_to_attrib(load_inpxml, attribname, shift_value, result):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_add_number_to_attrib

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    xml_add_number_to_attrib(xmltree, schema_dict, '/fleurInput/calculationSetup/cutoffs',
                             '/fleurInput/calculationSetup/cutoffs', attribname, shift_value)

    assert str(eval_xpath(root, '/fleurInput/calculationSetup/cutoffs/@Kmax')) == result


TEST_SHIFT_VALUES_ALL = [1.0, 0.5, 3.0]
TEST_SHIFT_RESULTS_ALL_ABS = [['3.2000000000', '3.2000000000'], ['2.7000000000', '2.7000000000'],
                              ['5.2000000000', '2.20000000']]
TEST_SHIFT_RESULTS_ALL_REL = [['2.2000000000', '2.2000000000'], ['1.1000000000', '1.1000000000'],
                              ['6.6000000000', '2.20000000']]
TEST_SHIFT_OCCURRENCES = [None, None, 0]


@pytest.mark.parametrize('shift_value, result, occurrences',
                         zip(TEST_SHIFT_VALUES_ALL, TEST_SHIFT_RESULTS_ALL_ABS, TEST_SHIFT_OCCURRENCES))
def test_xml_add_number_to_attrib_all_abs(load_inpxml, shift_value, result, occurrences):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_add_number_to_attrib

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    xml_add_number_to_attrib(xmltree,
                             schema_dict,
                             '/fleurInput/atomSpecies/species/mtSphere',
                             '/fleurInput/atomSpecies/species/mtSphere',
                             'radius',
                             shift_value,
                             occurrences=occurrences)

    radius = eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius')

    assert [str(val) for val in radius] == result


@pytest.mark.parametrize('shift_value, result, occurrences',
                         zip(TEST_SHIFT_VALUES_ALL, TEST_SHIFT_RESULTS_ALL_REL, TEST_SHIFT_OCCURRENCES))
def test_xml_add_number_to_attrib_all_rel(load_inpxml, shift_value, result, occurrences):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_add_number_to_attrib

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    xml_add_number_to_attrib(xmltree,
                             schema_dict,
                             '/fleurInput/atomSpecies/species/mtSphere',
                             '/fleurInput/atomSpecies/species/mtSphere',
                             'radius',
                             shift_value,
                             occurrences=occurrences,
                             mode='rel')

    radius = eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius')

    assert [str(val) for val in radius] == result


def test_xml_add_number_to_attrib_differing_xpaths(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_add_number_to_attrib

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    xml_add_number_to_attrib(xmltree, schema_dict, "/fleurInput/atomSpecies/species[@name='Fe-1']/mtSphere",
                             '/fleurInput/atomSpecies/species/mtSphere', 'radius', 2.0)

    radius = eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius')

    assert [str(val) for val in radius] == ['4.2000000000', '2.20000000']


def test_xml_add_number_to_attrib_differing_int(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_add_number_to_attrib

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    xml_add_number_to_attrib(xmltree, schema_dict, '/fleurInput/calculationSetup/cutoffs',
                             '/fleurInput/calculationSetup/cutoffs', 'numbands', 100)

    numbands = eval_xpath(root, '/fleurInput/calculationSetup/cutoffs/@numbands')

    assert numbands == '100'

    with pytest.raises(ValueError, match='You are trying to write a float to an integer attribute'):
        xml_add_number_to_attrib(xmltree, schema_dict, '/fleurInput/calculationSetup/cutoffs',
                                 '/fleurInput/calculationSetup/cutoffs', 'numbands', 55.5)


def test_xml_add_number_to_first_attrib(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_add_number_to_first_attrib

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    xml_add_number_to_first_attrib(xmltree, schema_dict, '/fleurInput/atomSpecies/species/mtSphere',
                                   '/fleurInput/atomSpecies/species/mtSphere', 'radius', 2.0)

    radius = eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius')

    assert [str(val) for val in radius] == ['4.2000000000', '2.20000000']


def test_xml_set_simple_tag_single(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_simple_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {'s': 2, 'p': 3, 'd': 4, 'f': 5}

    xml_set_simple_tag(xmltree, schema_dict, '/fleurInput/atomSpecies/species', '/fleurInput/atomSpecies/species',
                       'energyParameters', changes)

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species/energyParameters')

    assert [node.attrib.items() for node in nodes] == [[(key, str(val)) for key, val in changes.items()]] * 2


def test_xml_set_simple_tag_multiple_dict(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_simple_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {'type': 'SCLO', 'n': 21, 'l': 3, 'eDeriv': 0}

    xml_set_simple_tag(xmltree, schema_dict, '/fleurInput/atomSpecies/species', '/fleurInput/atomSpecies/species', 'lo',
                       changes)

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert [node.attrib.items() for node in nodes] == [[(key, str(val)) for key, val in changes.items()]] * 2


def test_xml_set_simple_tag_multiple_list(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_simple_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = [{'type': 'SCLO', 'n': 21, 'l': 3, 'eDeriv': 0}, {'type': 'SCLO', 'n': 22, 'l': 4, 'eDeriv': 0}]

    xml_set_simple_tag(xmltree, schema_dict, '/fleurInput/atomSpecies/species', '/fleurInput/atomSpecies/species', 'lo',
                       changes)

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert [node.attrib.items() for node in nodes
            ] == [[(key, str(val)) for key, val in change.items()] for change in changes] * 2


def test_xml_set_simple_tag_differing_xpaths(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_simple_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = [{'type': 'SCLO', 'n': 21, 'l': 3, 'eDeriv': 0}, {'type': 'SCLO', 'n': 22, 'l': 4, 'eDeriv': 0}]

    xml_set_simple_tag(xmltree, schema_dict, "/fleurInput/atomSpecies/species[@name='Fe-1']",
                       '/fleurInput/atomSpecies/species', 'lo', changes)

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert [node.attrib.items() for node in nodes] == [[('type', 'SCLO'), ('n', '21'), ('l', '3'), ('eDeriv', '0')],
                                                       [('type', 'SCLO'), ('n', '22'), ('l', '4'), ('eDeriv', '0')],
                                                       [('type', 'SCLO'), ('l', '1'), ('n', '5'), ('eDeriv', '0')]]


def test_xml_set_simple_tag_create_single(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_simple_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {'ne': 6}

    with pytest.raises(ValueError, match="Could not create tag 'realAxis' because atleast one subtag is missing"):
        xml_set_simple_tag(xmltree, schema_dict, '/fleurInput/calculationSetup/greensFunction',
                           '/fleurInput/calculationSetup/greensFunction', 'realAxis', changes)

    xml_set_simple_tag(xmltree,
                       schema_dict,
                       '/fleurInput/calculationSetup/greensFunction',
                       '/fleurInput/calculationSetup/greensFunction',
                       'realAxis',
                       changes,
                       create_parents=True)
    node = eval_xpath(root, '/fleurInput/calculationSetup/greensFunction/realAxis')

    assert node.attrib.items() == [('ne', '6')]


def test_xml_set_simple_tag_create_multiple(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_simple_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = [{'n': 6}, {'n': 7}]

    with pytest.raises(ValueError,
                       match="Could not create tag 'contourSemicircle' because atleast one subtag is missing"):
        xml_set_simple_tag(xmltree, schema_dict, '/fleurInput/calculationSetup/greensFunction',
                           '/fleurInput/calculationSetup/greensFunction', 'contourSemicircle', changes)

    xml_set_simple_tag(xmltree,
                       schema_dict,
                       '/fleurInput/calculationSetup/greensFunction',
                       '/fleurInput/calculationSetup/greensFunction',
                       'contourSemicircle',
                       changes,
                       create_parents=True)
    nodes = eval_xpath(root, '/fleurInput/calculationSetup/greensFunction/contourSemicircle')

    assert [node.attrib.items() for node in nodes] == [[('n', '6')], [('n', '7')]]


def test_xml_set_complex_tag(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_complex_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {'jspins': 4, 'mtNocoParams': {'l_mtNocoPot': True}, 'qss': [0.0, 1.0, 2.0]}

    xml_set_complex_tag(xmltree, schema_dict, '/fleurInput/calculationSetup/magnetism',
                        '/fleurInput/calculationSetup/magnetism', changes)

    assert str(eval_xpath(root, '/fleurInput/calculationSetup/magnetism/@jspins')) == '4'
    assert str(eval_xpath(root, '/fleurInput/calculationSetup/magnetism/mtNocoParams/@l_mtNocoPot')) == 'T'
    assert str(eval_xpath(
        root,
        '/fleurInput/calculationSetup/magnetism/qss/text()')) == ' 0.0000000000000  1.0000000000000  2.0000000000000'


def test_xml_set_complex_tag_differing_xpaths_recursive_complex_single(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_complex_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {'electronConfig': {'valenceConfig': 'TEST'}}

    xml_set_complex_tag(xmltree, schema_dict, "/fleurInput/atomSpecies/species[@name='Fe-1']",
                        '/fleurInput/atomSpecies/species', changes)

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species/electronConfig/valenceConfig/text()')
    assert [str(node) for node in nodes] == ['TEST', '(5p1/2) (5p3/2) (6s1/2) (5d3/2) (5d5/2)']


def test_xml_set_complex_tag_recursive_complex_multiple(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_complex_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {'ldaHIA': [{'addArg': {'key': 'TEST'}}, {'addArg': {'key': 'TEST2'}}]}

    xml_set_complex_tag(xmltree, schema_dict, "/fleurInput/atomSpecies/species[@name='Fe-1']",
                        '/fleurInput/atomSpecies/species', changes)

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species/ldaHIA/addArg/@key')
    assert [str(node) for node in nodes] == ['TEST', 'TEST2']
