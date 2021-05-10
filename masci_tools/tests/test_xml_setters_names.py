# -*- coding: utf-8 -*-
"""
Tests for the functions in xml_setters_names

These tests do not extensively test all possible functionality. this is done in the
tests for the underlying functions in xml_setters_xpaths and xml_setters_basic
"""
import os
from lxml import etree
import pytest

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_INPXML_PATH = os.path.join(FILE_PATH, 'files/fleur/Max-R5/FePt_film_SSFT_LO/files/inp2.xml')
TEST_MAX4_INPXML_PATH = os.path.join(FILE_PATH, 'files/fleur/aiida_fleur/inpxml/FePt/inp.xml')
TEST_MULTIPLE_KPOINT_SETS_PATH = os.path.join(FILE_PATH, 'files/fleur/test_multiple_ksets.xml')


def test_create_tag(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    tags = [child.tag for child in node.iterchildren()]
    tags.append('greensFunction')

    create_tag(xmltree, schema_dict, 'greensFunction')

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    assert [child.tag for child in node.iterchildren()] == tags


def test_create_tag_element(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import create_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    tags = [child.tag for child in node.iterchildren()]
    tags.append('greensFunction')

    create_tag(xmltree, schema_dict, etree.Element('greensFunction'))

    node = eval_xpath(root, '/fleurInput/calculationSetup')

    assert [child.tag for child in node.iterchildren()] == tags


def test_create_tag_specification(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
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

    from masci_tools.util.xml.common_functions import eval_xpath
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

    from masci_tools.util.xml.common_functions import eval_xpath
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

    from masci_tools.util.xml.common_functions import eval_xpath
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


def test_delete_tag(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import delete_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species', list_return=True)) == 2

    delete_tag(xmltree, schema_dict, 'species')

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species', list_return=True)) == 0


def test_delete_tag_specification(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import delete_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/lo', list_return=True)) == 3

    with pytest.raises(ValueError, match='The tag lo has multiple possible paths with the current specification.'):
        delete_tag(xmltree, schema_dict, 'lo')

    delete_tag(xmltree, schema_dict, 'lo', contains='species')

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/lo', list_return=True)) == 0


def test_delete_tag_complex_xpath(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import delete_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/lo', list_return=True)) == 3

    delete_tag(xmltree,
               schema_dict,
               'lo',
               contains='species',
               complex_xpath="/fleurInput/atomSpecies/species[@name='Fe-1']/lo")

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species/lo', list_return=True)

    assert len(nodes) == 1
    assert [node.getparent().attrib['name'] for node in nodes] == ['Pt-1']


def test_delete_tag_occurrences(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import delete_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/lo', list_return=True)) == 3

    delete_tag(xmltree, schema_dict, 'lo', contains='species', occurrences=[0, 2])

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species/lo', list_return=True)

    assert len(nodes) == 1
    assert [node.getparent().attrib['name'] for node in nodes] == ['Fe-1']


def test_delete_att(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import delete_att

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert eval_xpath(root, '/fleurInput/calculationSetup/cutoffs/@Kmax') == '4.00000000'

    delete_att(xmltree, schema_dict, 'kmax')

    assert eval_xpath(root, '/fleurInput/calculationSetup/cutoffs/@Kmax') == []


def test_delete_att_specification(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import delete_att

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius',
                      list_return=True) == ['2.20000000', '2.20000000']

    with pytest.raises(ValueError,
                       match='The attrib radius has multiple possible paths with the current specification.'):
        delete_att(xmltree, schema_dict, 'radius')

    delete_att(xmltree, schema_dict, 'radius', contains='species')

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius', list_return=True) == []


def test_delete_att_complex_xpath(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import delete_att

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius',
                      list_return=True) == ['2.20000000', '2.20000000']

    delete_att(xmltree,
               schema_dict,
               'radius',
               contains='species',
               complex_xpath="/fleurInput/atomSpecies/species[@name='Fe-1']/mtSphere")

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == '2.20000000'
    assert eval_xpath(root, "/fleurInput/atomSpecies/species[@name='Pt-1']/mtSphere/@radius") == '2.20000000'


def test_delete_att_occurrences(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import delete_att

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius',
                      list_return=True) == ['2.20000000', '2.20000000']

    delete_att(xmltree, schema_dict, 'radius', contains='species', occurrences=[1])

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == '2.20000000'
    assert eval_xpath(root, "/fleurInput/atomSpecies/species[@name='Fe-1']/mtSphere/@radius") == '2.20000000'


def test_replace_tag(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import replace_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    new_elem = etree.Element('test_tag')

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species', list_return=True)) == 2

    replace_tag(xmltree, schema_dict, 'species', new_elem)

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species', list_return=True)) == 0
    assert len(eval_xpath(root, '/fleurInput/atomSpecies/test_tag', list_return=True)) == 2


def test_replace_tag_specification(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import replace_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    new_elem = etree.Element('test_tag')

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/lo', list_return=True)) == 3

    with pytest.raises(ValueError, match='The tag lo has multiple possible paths with the current specification.'):
        replace_tag(xmltree, schema_dict, 'lo', new_elem)

    replace_tag(xmltree, schema_dict, 'lo', new_elem, contains='species')

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/lo', list_return=True)) == 0
    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/test_tag', list_return=True)) == 3


def test_replace_tag_complex_xpath(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import replace_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    new_elem = etree.Element('test_tag')

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/lo', list_return=True)) == 3

    replace_tag(xmltree,
                schema_dict,
                'lo',
                new_elem,
                contains='species',
                complex_xpath="/fleurInput/atomSpecies/species[@name='Fe-1']/lo")

    lo_nodes = eval_xpath(root, '/fleurInput/atomSpecies/species/lo', list_return=True)
    replaced_nodes = eval_xpath(root, '/fleurInput/atomSpecies/species/test_tag', list_return=True)

    assert len(lo_nodes) == 1
    assert [node.getparent().attrib['name'] for node in lo_nodes] == ['Pt-1']
    assert len(replaced_nodes) == 2
    assert [node.getparent().attrib['name'] for node in replaced_nodes] == ['Fe-1', 'Fe-1']


def test_replace_tag_occurrences(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import replace_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    new_elem = etree.Element('test_tag')

    assert len(eval_xpath(root, '/fleurInput/atomSpecies/species/lo', list_return=True)) == 3

    replace_tag(xmltree, schema_dict, 'lo', new_elem, contains='species', occurrences=[0, 2])

    lo_nodes = eval_xpath(root, '/fleurInput/atomSpecies/species/lo', list_return=True)
    replaced_nodes = eval_xpath(root, '/fleurInput/atomSpecies/species/test_tag', list_return=True)

    assert len(lo_nodes) == 1
    assert [node.getparent().attrib['name'] for node in lo_nodes] == ['Fe-1']
    assert len(replaced_nodes) == 2
    assert [node.getparent().attrib['name'] for node in replaced_nodes] == ['Fe-1', 'Pt-1']


def test_set_attrib_value(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_attrib_value(xmltree, schema_dict, 'kmax', 5.321)

    kmax = eval_xpath(root, '/fleurInput/calculationSetup/cutoffs/@Kmax')

    assert kmax == '5.3210000000'


def test_set_attrib_value_xcFunctional(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_attrib_value(xmltree, schema_dict, 'xcFunctional', 'TEST')

    res = eval_xpath(root, '/fleurInput/calculationSetup/xcFunctional/@name')

    assert res == 'TEST'


def test_set_attrib_forcetheorem_angles(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_attrib_value(xmltree, schema_dict, 'theta', 5.321, contains='DMI', create=True)
    assert eval_xpath(root, '/fleurInput/forceTheorem/DMI/@theta') == '5.3210000000'
    set_attrib_value(xmltree, schema_dict, 'phi', [1, 2, 3.14], contains='DMI', create=True)
    assert eval_xpath(root, '/fleurInput/forceTheorem/DMI/@phi') == '1.0000000000 2.0000000000 3.1400000000'
    set_attrib_value(xmltree, schema_dict, 'ef_shift', [10.0], contains='DMI', create=True)
    assert eval_xpath(root, '/fleurInput/forceTheorem/DMI/@ef_shift') == '10.0000000000'


def test_set_attrib_value_specification(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
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
    from masci_tools.util.xml.common_functions import eval_xpath
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
    from masci_tools.util.xml.common_functions import eval_xpath
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
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_attrib_value(xmltree, schema_dict, 'type', 'TEST', contains='species', occurrences=-2)

    lo_types = eval_xpath(root, '/fleurInput/atomSpecies/species/lo/@type')

    assert lo_types == ['SCLO', 'TEST', 'SCLO']


def test_set_first_attrib_value(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_first_attrib_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_first_attrib_value(xmltree, schema_dict, 'type', 'TEST', contains='species')

    lo_types = eval_xpath(root, '/fleurInput/atomSpecies/species/lo/@type')

    assert lo_types == ['TEST', 'SCLO', 'SCLO']


def test_set_first_attrib_value_complex_xpath(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
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

    from masci_tools.util.xml.common_functions import eval_xpath
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


def test_set_text(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_text

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_text(xmltree, schema_dict, 'comment', 'This is a test comment')

    res = eval_xpath(root, '/fleurInput/comment/text()')

    assert res == 'This is a test comment'


def test_set_text_specification_create(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_text

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError, match='The tag s has multiple possible paths with the current specification'):
        set_text(xmltree, schema_dict, 's', [False, False, False, True])

    with pytest.raises(
            ValueError,
            match=
            "Could not set text on path '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/s' because atleast one subtag is missing."
    ):
        set_text(xmltree, schema_dict, 's', [False, False, False, True], contains={'species', 'torgue'})

    set_text(xmltree, schema_dict, 's', [False, False, False, True], contains={'species', 'torgue'}, create=True)

    res = eval_xpath(root, '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/s/text()')

    assert res == ['F F F T', 'F F F T']


def test_set_text_specification_complex_xpath(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_text

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_text(xmltree,
             schema_dict,
             'kPoint', [10.0, 10.0, 10.0],
             complex_xpath='/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint[1]')

    res = eval_xpath(root, '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint/text()')

    assert res == ['10.0000000000000 10.0000000000000 10.0000000000000', '    0.250000     0.250000     0.000000']


def test_set_text_specification_occurrences(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_text

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_text(xmltree, schema_dict, 'kPoint', [10.0, 10.0, 10.0], occurrences=-1)

    res = eval_xpath(root, '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint/text()')

    assert res == ['   -0.250000     0.250000     0.000000', '10.0000000000000 10.0000000000000 10.0000000000000']


def test_set_first_text(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_first_text

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_first_text(xmltree, schema_dict, 'kPoint', [10.0, 10.0, 10.0])

    res = eval_xpath(root, '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint/text()')

    assert res == ['10.0000000000000 10.0000000000000 10.0000000000000', '    0.250000     0.250000     0.000000']


def test_set_first_text_complex_xpath(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_first_text

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_first_text(xmltree,
                   schema_dict,
                   'kPoint', [10.0, 10.0, 10.0],
                   complex_xpath='/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint[2]')

    res = eval_xpath(root, '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint/text()')

    assert res == ['   -0.250000     0.250000     0.000000', '10.0000000000000 10.0000000000000 10.0000000000000']


def test_set_first_text_create(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_first_text

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError, match='The tag s has multiple possible paths with the current specification'):
        set_first_text(xmltree, schema_dict, 's', [False, False, False, True])

    with pytest.raises(
            ValueError,
            match=
            "Could not set text on path '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/s' because atleast one subtag is missing."
    ):
        set_first_text(xmltree, schema_dict, 's', [False, False, False, True], contains={'species', 'torgue'})

    set_first_text(xmltree, schema_dict, 's', [False, False, False, True], contains={'species', 'torgue'}, create=True)

    res = eval_xpath(root, '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/s/text()')

    assert res == 'F F F T'


def test_add_number_to_attrib(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import add_number_to_attrib

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    add_number_to_attrib(xmltree, schema_dict, 'kmax', 10)

    res = eval_xpath(root, '/fleurInput/calculationSetup/cutoffs/@Kmax')

    assert res == '14.0000000000'


def test_add_number_to_attrib_rel(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import add_number_to_attrib

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    add_number_to_attrib(xmltree, schema_dict, 'kmax', 10, mode='rel')

    res = eval_xpath(root, '/fleurInput/calculationSetup/cutoffs/@Kmax')

    assert res == '40.0000000000'


def test_add_number_to_attrib_specification(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import add_number_to_attrib

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError,
                       match='The attrib radius has multiple possible paths with the current specification.'):
        add_number_to_attrib(xmltree, schema_dict, 'radius', 0.5)

    add_number_to_attrib(xmltree, schema_dict, 'radius', 0.5, not_contains='Group')

    res = eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius')

    assert res == ['2.7000000000', '2.7000000000']


def test_add_number_to_attrib_complex_xpath(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import add_number_to_attrib

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    add_number_to_attrib(xmltree,
                         schema_dict,
                         'radius',
                         0.5,
                         not_contains='Group',
                         complex_xpath="/fleurInput/atomSpecies/species[@name='Pt-1']/mtSphere")

    res = eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius')

    assert res == ['2.20000000', '2.7000000000']


def test_add_number_to_attrib_occurrences(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import add_number_to_attrib

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    add_number_to_attrib(xmltree, schema_dict, 'radius', 0.5, not_contains='Group', occurrences=[0])

    res = eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius')

    assert res == ['2.7000000000', '2.20000000']


def test_add_number_to_first_attrib(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import add_number_to_first_attrib

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    add_number_to_first_attrib(xmltree, schema_dict, 'kmax', 10)

    res = eval_xpath(root, '/fleurInput/calculationSetup/cutoffs/@Kmax')

    assert res == '14.0000000000'


def test_add_number_to_first_attrib_rel(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import add_number_to_first_attrib

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    add_number_to_first_attrib(xmltree, schema_dict, 'kmax', 10, mode='rel')

    res = eval_xpath(root, '/fleurInput/calculationSetup/cutoffs/@Kmax')

    assert res == '40.0000000000'


def test_add_number_to_first_attrib_specification(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import add_number_to_first_attrib

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError,
                       match='The attrib radius has multiple possible paths with the current specification.'):
        add_number_to_first_attrib(xmltree, schema_dict, 'radius', 0.5)

    add_number_to_first_attrib(xmltree, schema_dict, 'radius', 0.5, not_contains='Group')

    res = eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius')

    assert res == ['2.7000000000', '2.20000000']


def test_add_number_to_first_attrib_complex_xpath(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import add_number_to_first_attrib

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    add_number_to_first_attrib(xmltree,
                               schema_dict,
                               'radius',
                               0.5,
                               not_contains='Group',
                               complex_xpath="/fleurInput/atomSpecies/species[@name='Pt-1']/mtSphere")

    res = eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius')

    assert res == ['2.20000000', '2.7000000000']


def test_set_simple_tag(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_simple_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_simple_tag(xmltree, schema_dict, 'cutoffs', {'gmax': 34.0, 'gmaxxc': 40.0})

    node = eval_xpath(root, '/fleurInput/calculationSetup/cutoffs')

    assert node.attrib == {'Kmax': '4.00000000', 'Gmax': '34.0000000000', 'GmaxXC': '40.0000000000', 'numbands': '0'}


def test_set_simple_tag_error(load_inpxml):
    from masci_tools.util.xml.xml_setters_names import set_simple_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)

    with pytest.raises(AssertionError, match="Given tag 'species' is not simple"):
        set_simple_tag(xmltree, schema_dict, 'species', {'mtSphere': {'radius': 10}})


def test_set_simple_tag_specification(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_simple_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError, match='The tag lo has multiple possible paths with the current specification.'):
        set_simple_tag(xmltree, schema_dict, 'lo', [{'type': 'TEST', 'n': 12}, {'type': 'TEST', 'n': 15}])

    set_simple_tag(xmltree,
                   schema_dict,
                   'lo', [{
                       'type': 'TEST',
                       'n': 12
                   }, {
                       'type': 'TEST',
                       'n': 15
                   }],
                   contains='species')

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert [node.getparent().attrib['name'] for node in nodes] == ['Fe-1', 'Fe-1', 'Pt-1', 'Pt-1']
    assert [node.attrib.items() for node in nodes] == [
        [('type', 'TEST'), ('n', '12')],
        [('type', 'TEST'), ('n', '15')],
        [('type', 'TEST'), ('n', '12')],
        [('type', 'TEST'), ('n', '15')],
    ]


def test_set_simple_tag_create(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_simple_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError, match="Could not create tag 'realAxis' because atleast one subtag is missing."):
        set_simple_tag(xmltree, schema_dict, 'realAxis', {'ne': 100000, 'ellow': -13})

    set_simple_tag(xmltree, schema_dict, 'realAxis', {'ne': 100000, 'ellow': -13}, create_parents=True)

    node = eval_xpath(root, '/fleurInput/calculationSetup/greensFunction/realAxis')

    assert node.attrib == {'ne': '100000', 'ellow': '-13.0000000000'}


def test_set_simple_tag_create_multiple(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_simple_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError,
                       match="Could not create tag 'contourSemicircle' because atleast one subtag is missing."):
        set_simple_tag(xmltree, schema_dict, 'contourSemicircle', [{'n': 12, 'eb': -13}, {'n': 12, 'eb': 55}])

    set_simple_tag(xmltree,
                   schema_dict,
                   'contourSemicircle', [{
                       'n': 12,
                       'eb': -13
                   }, {
                       'n': 12,
                       'eb': 55
                   }],
                   create_parents=True)

    nodes = eval_xpath(root, '/fleurInput/calculationSetup/greensFunction/contourSemicircle')

    assert [node.attrib.items() for node in nodes] == [[('n', '12'), ('eb', '-13.0000000000')],
                                                       [('n', '12'), ('eb', '55.0000000000')]]


def test_set_simple_tag_complex_xpath(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_simple_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_simple_tag(xmltree,
                   schema_dict,
                   'lo', [{
                       'type': 'TEST',
                       'n': 12
                   }, {
                       'type': 'TEST',
                       'n': 15
                   }],
                   contains='species',
                   complex_xpath="/fleurInput/atomSpecies/species[@name='Pt-1']")

    nodes = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert [node.getparent().attrib['name'] for node in nodes] == ['Fe-1', 'Fe-1', 'Pt-1', 'Pt-1']
    assert [node.attrib.items() for node in nodes] == [
        [('type', 'SCLO'), ('l', '0'), ('n', '3'), ('eDeriv', '0')],
        [('type', 'SCLO'), ('l', '1'), ('n', '3'), ('eDeriv', '0')],
        [('type', 'TEST'), ('n', '12')],
        [('type', 'TEST'), ('n', '15')],
    ]


def test_set_complex_tag(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_complex_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {'jspins': 4, 'mtNocoParams': {'l_mtNocoPot': True}, 'qss': [0.0, 1.0, 2.0]}

    set_complex_tag(
        xmltree,
        schema_dict,
        'magnetism',
        changes,
    )

    assert str(eval_xpath(root, '/fleurInput/calculationSetup/magnetism/@jspins')) == '4'
    assert str(eval_xpath(root, '/fleurInput/calculationSetup/magnetism/mtNocoParams/@l_mtNocoPot')) == 'T'
    assert str(eval_xpath(
        root,
        '/fleurInput/calculationSetup/magnetism/qss/text()')) == ' 0.0000000000000  1.0000000000000  2.0000000000000'


def test_set_complex_tag_create_specification(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_complex_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {'kkintgrcutoff': 'd', 'greensfElements': {'s': [False, True, False, True]}}

    with pytest.raises(ValueError,
                       match='The tag torgueCalculation has multiple possible paths with the current specification.'):
        set_complex_tag(
            xmltree,
            schema_dict,
            'torgueCalculation',
            changes,
        )

    with pytest.raises(
            ValueError,
            match=
            "Could not set attribute 'kkintgrCutoff' on path '/fleurInput/atomSpecies/species/torgueCalculation' because atleast one subtag is missing."
    ):
        set_complex_tag(xmltree, schema_dict, 'torgueCalculation', changes, not_contains='Group')

    set_complex_tag(xmltree, schema_dict, 'torgueCalculation', changes, not_contains='Group', create=True)

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/torgueCalculation/@kkintgrCutoff') == ['d', 'd']
    assert eval_xpath(
        root, '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/s/text()') == ['F T F T', 'F T F T']


def test_set_complex_tag_complex_xpath(load_inpxml):

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_complex_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {'kkintgrcutoff': 'd', 'greensfElements': {'s': [False, True, False, True]}}

    set_complex_tag(xmltree,
                    schema_dict,
                    'torgueCalculation',
                    changes,
                    not_contains='Group',
                    create=True,
                    complex_xpath="/fleurInput/atomSpecies/species[@name='Pt-1']/torgueCalculation")

    node = eval_xpath(root, '/fleurInput/atomSpecies/species/torgueCalculation')

    assert node.getparent().attrib['name'] == 'Pt-1'
    assert eval_xpath(root, '/fleurInput/atomSpecies/species/torgueCalculation/@kkintgrCutoff') == 'd'
    assert eval_xpath(root, '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/s/text()') == 'F T F T'


def test_set_species(load_inpxml):
    """
    Test of the set_species function (underlying functionality is tested in tests for xml_set_complex_tag)

    Here only the species selection is tested extensively
    """

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_species

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {
        'mtSphere': {
            'radius': 10.0
        },
        'lo': {
            'type': 'TEST',
            'n': 5,
            'l': 12
        },
        'electronConfig': {
            'stateOccupation': [{
                'state': 'state'
            }, {
                'state': 'state2'
            }]
        }
    }

    set_species(xmltree, schema_dict, 'Fe-1', changes)

    los = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == ['10.0000000000', '2.20000000']
    assert eval_xpath(root, '/fleurInput/atomSpecies/species/electronConfig/stateOccupation/@state') == [
        'state', 'state2', '(6s1/2)', '(5d5/2)'
    ]
    assert [lo.attrib for lo in los] == [{
        'type': 'TEST',
        'n': '5',
        'l': '12'
    }, {
        'type': 'SCLO',
        'l': '1',
        'n': '5',
        'eDeriv': '0'
    }]


def test_set_species_label(load_inpxml):
    """
    Test of the set_species function (underlying functionality is tested in tests for xml_set_complex_tag)

    Here only the species selection is tested extensively
    """

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_species_label

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {
        'mtSphere': {
            'radius': 10.0
        },
        'lo': {
            'type': 'TEST',
            'n': 5,
            'l': 12
        },
        'electronConfig': {
            'stateOccupation': [{
                'state': 'state'
            }, {
                'state': 'state2'
            }]
        }
    }

    set_species_label(xmltree, schema_dict, '                 222', changes)

    los = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == ['10.0000000000', '2.20000000']
    assert eval_xpath(root, '/fleurInput/atomSpecies/species/electronConfig/stateOccupation/@state') == [
        'state', 'state2', '(6s1/2)', '(5d5/2)'
    ]
    assert [lo.attrib for lo in los] == [{
        'type': 'TEST',
        'n': '5',
        'l': '12'
    }, {
        'type': 'SCLO',
        'l': '1',
        'n': '5',
        'eDeriv': '0'
    }]


def test_set_species_all(load_inpxml):
    """
    Test of the set_species function (underlying functionality is tested in tests for xml_set_complex_tag)

    Here only the species selection is tested extensively
    """

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_species

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {
        'mtSphere': {
            'radius': 10.0
        },
        'lo': {
            'type': 'TEST',
            'n': 5,
            'l': 12
        },
        'electronConfig': {
            'stateOccupation': [{
                'state': 'state'
            }, {
                'state': 'state2'
            }]
        }
    }

    set_species(xmltree, schema_dict, 'all', changes)

    los = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == ['10.0000000000', '10.0000000000']
    assert eval_xpath(root, '/fleurInput/atomSpecies/species/electronConfig/stateOccupation/@state') == [
        'state', 'state2', 'state', 'state2'
    ]
    assert [lo.attrib for lo in los] == [{'type': 'TEST', 'n': '5', 'l': '12'}, {'type': 'TEST', 'l': '12', 'n': '5'}]


def test_set_species_label_all(load_inpxml):
    """
    Test of the set_species function (underlying functionality is tested in tests for xml_set_complex_tag)

    Here only the species selection is tested extensively
    """

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_species_label

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {
        'mtSphere': {
            'radius': 10.0
        },
        'lo': {
            'type': 'TEST',
            'n': 5,
            'l': 12
        },
        'electronConfig': {
            'stateOccupation': [{
                'state': 'state'
            }, {
                'state': 'state2'
            }]
        }
    }

    set_species_label(xmltree, schema_dict, 'all', changes)

    los = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == ['10.0000000000', '10.0000000000']
    assert eval_xpath(root, '/fleurInput/atomSpecies/species/electronConfig/stateOccupation/@state') == [
        'state', 'state2', 'state', 'state2'
    ]
    assert [lo.attrib for lo in los] == [{'type': 'TEST', 'n': '5', 'l': '12'}, {'type': 'TEST', 'l': '12', 'n': '5'}]


def test_set_species_all_search_string(load_inpxml):
    """
    Test of the set_species function (underlying functionality is tested in tests for xml_set_complex_tag)

    Here only the species selection is tested extensively
    """

    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_species

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {
        'mtSphere': {
            'radius': 10.0
        },
        'lo': {
            'type': 'TEST',
            'n': 5,
            'l': 12
        },
        'electronConfig': {
            'stateOccupation': [{
                'state': 'state'
            }, {
                'state': 'state2'
            }]
        }
    }

    set_species(xmltree, schema_dict, 'all-Pt', changes)

    los = eval_xpath(root, '/fleurInput/atomSpecies/species/lo')

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/mtSphere/@radius') == ['2.20000000', '10.0000000000']
    assert eval_xpath(root, '/fleurInput/atomSpecies/species/electronConfig/stateOccupation/@state') == [
        '(3d3/2)', '(3d5/2)', 'state', 'state2'
    ]
    assert [lo.attrib for lo in los] == [{
        'type': 'SCLO',
        'l': '0',
        'n': '3',
        'eDeriv': '0'
    }, {
        'type': 'SCLO',
        'l': '1',
        'n': '3',
        'eDeriv': '0'
    }, {
        'type': 'TEST',
        'n': '5',
        'l': '12'
    }]


def test_set_atomgroup(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_atomgroup

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {'force': {'relaxXYZ': 'FFF'}, 'nocoParams': {'beta': 7.0}, 'cFCoeffs': {'potential': True}}

    set_atomgroup(xmltree, schema_dict, changes, position=1)

    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/force/@relaxXYZ') == ['FFF', 'TTT']
    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/nocoParams/@beta') == ['7.0000000000', '1.570796326']
    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/cFCoeffs/@potential') == 'T'


def test_set_atomgroup_species(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_atomgroup

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {'force': {'relaxXYZ': 'FFF'}, 'nocoParams': {'beta': 7.0}, 'cFCoeffs': {'potential': True}}

    set_atomgroup(xmltree, schema_dict, changes, species='Fe-1')

    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/force/@relaxXYZ') == ['FFF', 'TTT']
    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/nocoParams/@beta') == ['7.0000000000', '1.570796326']
    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/cFCoeffs/@potential') == 'T'


def test_set_atomgroup_all(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_atomgroup

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {'force': {'relaxXYZ': 'FFF'}, 'nocoParams': {'beta': 7.0}, 'cFCoeffs': {'potential': True}}

    set_atomgroup(xmltree, schema_dict, changes, species='all')

    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/force/@relaxXYZ') == ['FFF', 'FFF']
    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/nocoParams/@beta') == ['7.0000000000', '7.0000000000']
    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/cFCoeffs/@potential') == ['T', 'T']


def test_set_atomgroup_all_position(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_atomgroup

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {'force': {'relaxXYZ': 'FFF'}, 'nocoParams': {'beta': 7.0}, 'cFCoeffs': {'potential': True}}

    set_atomgroup(xmltree, schema_dict, changes, position='all')

    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/force/@relaxXYZ') == ['FFF', 'FFF']
    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/nocoParams/@beta') == ['7.0000000000', '7.0000000000']
    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/cFCoeffs/@potential') == ['T', 'T']


def test_set_atomgroup_label(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_atomgroup_label

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {'force': {'relaxXYZ': 'FFF'}, 'nocoParams': {'beta': 7.0}, 'cFCoeffs': {'potential': True}}

    set_atomgroup_label(xmltree, schema_dict, '                 222', changes)

    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/force/@relaxXYZ') == ['FFF', 'TTT']
    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/nocoParams/@beta') == ['7.0000000000', '1.570796326']
    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/cFCoeffs/@potential') == 'T'


def test_set_atomgroup_label_all(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_atomgroup_label

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    changes = {'force': {'relaxXYZ': 'FFF'}, 'nocoParams': {'beta': 7.0}, 'cFCoeffs': {'potential': True}}

    set_atomgroup_label(xmltree, schema_dict, 'all', changes)

    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/force/@relaxXYZ') == ['FFF', 'FFF']
    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/nocoParams/@beta') == ['7.0000000000', '7.0000000000']
    assert eval_xpath(root, '/fleurInput/atomGroups/atomGroup/cFCoeffs/@potential') == ['T', 'T']


def test_shift_value_species_label(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import shift_value_species_label

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    shift_value_species_label(xmltree, schema_dict, '222', 'lmax', 15)

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/atomicCutoffs/@lmax') == ['25', '10']


def test_shift_value_species_label_rel(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import shift_value_species_label

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    shift_value_species_label(xmltree, schema_dict, '222', 'lmax', 15, mode='rel')

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/atomicCutoffs/@lmax') == ['150', '10']


def test_shift_value_species_label_all(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import shift_value_species_label

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    shift_value_species_label(
        xmltree,
        schema_dict,
        'all',
        'lmax',
        15,
    )

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/atomicCutoffs/@lmax') == ['25', '25']


def test_shift_value_species_label_specification(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import shift_value_species_label

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError, match='The attrib s has multiple possible paths with the current specification.'):
        shift_value_species_label(xmltree, schema_dict, '222', 's', 3)

    shift_value_species_label(xmltree, schema_dict, '222', 's', 3, contains='energyParameters')

    assert eval_xpath(root, '/fleurInput/atomSpecies/species/energyParameters/@s') == ['7', '6']


def test_shift_value_single(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import shift_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    shift_value(xmltree, schema_dict, {'itmax': 2})

    assert eval_xpath(root, '/fleurInput/calculationSetup/scfLoop/@itmax') == '3'


def test_shift_value_multiple(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import shift_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    shift_value(xmltree, schema_dict, {'itmax': 2, 'kmax': 5.0})

    assert eval_xpath(root, '/fleurInput/calculationSetup/scfLoop/@itmax') == '3'
    assert eval_xpath(root, '/fleurInput/calculationSetup/cutoffs/@Kmax') == '9.0000000000'


def test_shift_value_rel(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import shift_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    shift_value(xmltree, schema_dict, {'itmax': 2, 'kmax': 5.0}, mode='rel')

    assert eval_xpath(root, '/fleurInput/calculationSetup/scfLoop/@itmax') == '2'
    assert eval_xpath(root, '/fleurInput/calculationSetup/cutoffs/@Kmax') == '20.0000000000'


def test_shift_value_specification(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import shift_value

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError,
                       match='The attrib spinf has multiple possible paths with the current specification.'):
        shift_value(xmltree, schema_dict, {'itmax': 2, 'kmax': 5.0, 'spinf': 0.5}, mode='rel')

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    shift_value(xmltree,
                schema_dict, {
                    'itmax': 2,
                    'kmax': 5.0,
                    'spinf': 0.5
                },
                mode='rel',
                path_spec={
                    'spinf': {
                        'contains': 'scfLoop'
                    },
                    'KMAX': {
                        'not_contains': 'species'
                    }
                })

    assert eval_xpath(root, '/fleurInput/calculationSetup/scfLoop/@itmax') == '2'
    assert eval_xpath(root, '/fleurInput/calculationSetup/cutoffs/@Kmax') == '20.0000000000'
    assert eval_xpath(root, '/fleurInput/calculationSetup/scfLoop/@spinf') == '1.0000000000'


def test_set_inpchanges_single(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_inpchanges

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_inpchanges(xmltree, schema_dict, {'itmax': 20})

    assert eval_xpath(root, '/fleurInput/calculationSetup/scfLoop/@itmax') == '20'


def test_set_inpchanges_single_text(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_inpchanges

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_inpchanges(xmltree, schema_dict, {'qss': [10, 10, 10]})

    assert eval_xpath(
        root,
        '/fleurInput/calculationSetup/magnetism/qss/text()') == '10.0000000000000 10.0000000000000 10.0000000000000'


def test_set_inpchanges_multiple(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_inpchanges

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    set_inpchanges(xmltree, schema_dict, {'itmax': 20, 'qss': [10, 10, 10], 'xcFunctional': 'TEST', 'l_linmix': True})

    assert eval_xpath(root, '/fleurInput/calculationSetup/scfLoop/@itmax') == '20'
    assert eval_xpath(
        root,
        '/fleurInput/calculationSetup/magnetism/qss/text()') == '10.0000000000000 10.0000000000000 10.0000000000000'
    assert eval_xpath(root, '/fleurInput/calculationSetup/xcFunctional/@name') == 'TEST'
    assert eval_xpath(root, '/fleurInput/calculationSetup/ldaU/@l_linMix') == 'T'


def test_set_inpchanges_specification(load_inpxml):
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.xml_setters_names import set_inpchanges

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    with pytest.raises(ValueError,
                       match='The attrib spinf has multiple possible paths with the current specification.'):
        set_inpchanges(xmltree, schema_dict, {
            'itmax': 20,
            'qss': [10, 10, 10],
            'xcFunctional': 'TEST',
            'l_linmix': True,
            'spinf': 10.0
        })

    set_inpchanges(xmltree,
                   schema_dict, {
                       'itmax': 20,
                       'qss': [10, 10, 10],
                       'xcFunctional': 'TEST',
                       'l_linmix': True,
                       'spinf': 10.0
                   },
                   path_spec={
                       'qss': {
                           'contains': 'magnetism'
                       },
                       'SPINF': {
                           'not_contains': 'scfLoop'
                       }
                   })

    assert eval_xpath(root, '/fleurInput/calculationSetup/scfLoop/@itmax') == '20'
    assert eval_xpath(
        root,
        '/fleurInput/calculationSetup/magnetism/qss/text()') == '10.0000000000000 10.0000000000000 10.0000000000000'
    assert eval_xpath(root, '/fleurInput/calculationSetup/xcFunctional/@name') == 'TEST'
    assert eval_xpath(root, '/fleurInput/calculationSetup/ldaU/@l_linMix') == 'T'
    assert eval_xpath(root, '/fleurInput/calculationSetup/ldaU/@spinf') == '10.0000000000'


def test_set_inpchanges_error(load_inpxml):
    from masci_tools.util.xml.xml_setters_names import set_inpchanges

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)

    with pytest.raises(
            ValueError,
            match="You try to set the key:'does_not_exist' to : 'TEST', but the key is unknown to the fleur plug-in"):
        set_inpchanges(xmltree, schema_dict, {
            'itmax': 20,
            'qss': [10, 10, 10],
            'does_not_exist': 'TEST',
            'xcFunctional': 'TEST',
            'l_linmix': True
        })


def test_set_nkpts_max5(load_inpxml):

    from masci_tools.util.xml.xml_setters_names import set_nkpts

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)

    with pytest.raises(NotImplementedError):
        set_nkpts(xmltree, schema_dict, 1337)


def test_set_nkpts_max4(load_inpxml):

    from masci_tools.util.xml.xml_setters_names import set_nkpts
    from masci_tools.util.xml.common_functions import eval_xpath

    xmltree, schema_dict = load_inpxml(TEST_MAX4_INPXML_PATH)
    root = xmltree.getroot()

    xmltree = set_nkpts(xmltree, schema_dict, 1337)

    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/kPointList') == []
    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/kPointCount/@count') == '1337'
    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/kPointCount/@gamma') == 'F'

    xmltree = set_nkpts(xmltree, schema_dict, 666, gamma=True)

    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/kPointList') == []
    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/kPointCount/@count') == '666'
    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/kPointCount/@gamma') == 'T'


def test_set_kpath_max5(load_inpxml):

    from masci_tools.util.xml.xml_setters_names import set_kpath

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)

    with pytest.raises(NotImplementedError):
        set_kpath(xmltree, schema_dict, {'Test': [0, 0, 0]}, 120)


def test_set_kpath_max4(load_inpxml):

    from masci_tools.util.xml.xml_setters_names import set_kpath
    from masci_tools.util.xml.common_functions import eval_xpath

    xmltree, schema_dict = load_inpxml(TEST_MAX4_INPXML_PATH)
    root = xmltree.getroot()

    xmltree = set_kpath(xmltree, schema_dict, {'Test': [0, 0, 0]}, 120)

    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/@count') == '120'
    assert eval_xpath(
        root, '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/specialPoint/@name') == 'Test'
    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/specialPoint/text()'
                      ) == ' 0.0000000000000  0.0000000000000  0.0000000000000'
    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/@gamma') == 'F'

    xmltree = set_kpath(xmltree, schema_dict, {'Test': [0, 0, 0], 'Test2': [1, 1, 1]}, 500, gamma=True)

    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/@count') == '500'
    assert eval_xpath(
        root,
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/specialPoint/@name') == ['Test', 'Test2']
    assert eval_xpath(root,
                      '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/specialPoint/text()') == [
                          ' 0.0000000000000  0.0000000000000  0.0000000000000',
                          ' 1.0000000000000  1.0000000000000  1.0000000000000'
                      ]
    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/@gamma') == 'T'


def test_switch_kpointset_max4(load_inpxml):
    from masci_tools.util.xml.xml_setters_names import switch_kpointset

    xmltree, schema_dict = load_inpxml(TEST_MAX4_INPXML_PATH)

    with pytest.raises(NotImplementedError):
        switch_kpointset(xmltree, schema_dict, 'Test')


def test_switch_kpointset_max5(load_inpxml):
    from masci_tools.util.xml.xml_setters_names import switch_kpointset
    from masci_tools.util.xml.common_functions import eval_xpath

    xmltree, schema_dict = load_inpxml(TEST_MULTIPLE_KPOINT_SETS_PATH)
    root = xmltree.getroot()

    xmltree = switch_kpointset(xmltree, schema_dict, 'second-set')

    assert eval_xpath(root, '/fleurInput/cell/bzIntegration/kPointListSelection/@listName') == 'second-set'

    with pytest.raises(ValueError, match='The given kPointList non_existent does not exist'):
        switch_kpointset(xmltree, schema_dict, 'non_existent')


def test_set_kpointlist_max5(load_inpxml):
    from masci_tools.util.xml.xml_setters_names import set_kpointlist
    from masci_tools.util.xml.common_functions import eval_xpath

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    kpoints = [[0, 0, 0], [1, 1, 1]]
    weights = [1, 2]

    xmltree = set_kpointlist(xmltree, schema_dict, kpoints, weights, name='second-set')

    assert eval_xpath(root, "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='default']/kPoint/text()") == [
        '   -0.250000     0.250000     0.000000', '    0.250000     0.250000     0.000000'
    ]
    assert eval_xpath(root,
                      "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='second-set']/kPoint/text()") == [
                          ' 0.0000000000000  0.0000000000000  0.0000000000000',
                          ' 1.0000000000000  1.0000000000000  1.0000000000000'
                      ]
    assert eval_xpath(root,
                      "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='second-set']/kPoint/@weight") == [
                          '1.0000000000', '2.0000000000'
                      ]
    assert eval_xpath(root, "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='second-set']/@count") == '2'


def test_set_kpointlist_max5_special_labels_and_type(load_inpxml):
    from masci_tools.util.xml.xml_setters_names import set_kpointlist
    from masci_tools.util.xml.common_functions import eval_xpath

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    kpoints = [[0, 0, 0], [1, 1, 1]]
    weights = [1, 2]

    xmltree = set_kpointlist(xmltree,
                             schema_dict,
                             kpoints,
                             weights,
                             name='second-set',
                             kpoint_type='mesh',
                             special_labels={1: 'TEST'})

    assert eval_xpath(root, "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='default']/kPoint/text()") == [
        '   -0.250000     0.250000     0.000000', '    0.250000     0.250000     0.000000'
    ]
    assert eval_xpath(root,
                      "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='second-set']/kPoint/text()") == [
                          ' 0.0000000000000  0.0000000000000  0.0000000000000',
                          ' 1.0000000000000  1.0000000000000  1.0000000000000'
                      ]
    assert eval_xpath(root,
                      "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='second-set']/kPoint/@weight") == [
                          '1.0000000000', '2.0000000000'
                      ]
    assert eval_xpath(root, "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='second-set']/@count") == '2'
    assert eval_xpath(
        root, "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='second-set']/kPoint[2]/@label") == 'TEST'
    assert eval_xpath(root, "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='second-set']/@type") == 'mesh'


def test_set_kpointlist_max5_default_name(load_inpxml):
    from masci_tools.util.xml.xml_setters_names import set_kpointlist
    from masci_tools.util.xml.common_functions import eval_xpath

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    kpoints = [[0, 0, 0], [1, 1, 1]]
    weights = [1, 2]

    xmltree = set_kpointlist(xmltree, schema_dict, kpoints, weights)

    assert eval_xpath(root, "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='default']/kPoint/text()") == [
        '   -0.250000     0.250000     0.000000', '    0.250000     0.250000     0.000000'
    ]
    assert eval_xpath(root,
                      "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='default-2']/kPoint/text()") == [
                          ' 0.0000000000000  0.0000000000000  0.0000000000000',
                          ' 1.0000000000000  1.0000000000000  1.0000000000000'
                      ]
    assert eval_xpath(root, "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='default-2']/@count") == '2'
    assert eval_xpath(root,
                      "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='default-2']/kPoint/@weight") == [
                          '1.0000000000', '2.0000000000'
                      ]


def test_set_kpointlist_max5_switch(load_inpxml):
    from masci_tools.util.xml.xml_setters_names import set_kpointlist
    from masci_tools.util.xml.common_functions import eval_xpath

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    kpoints = [[0, 0, 0], [1, 1, 1]]
    weights = [1, 2]

    xmltree = set_kpointlist(xmltree, schema_dict, kpoints, weights, switch=True)

    assert eval_xpath(root, "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='default']/kPoint/text()") == [
        '   -0.250000     0.250000     0.000000', '    0.250000     0.250000     0.000000'
    ]
    assert eval_xpath(root,
                      "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='default-2']/kPoint/text()") == [
                          ' 0.0000000000000  0.0000000000000  0.0000000000000',
                          ' 1.0000000000000  1.0000000000000  1.0000000000000'
                      ]
    assert eval_xpath(root,
                      "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='default-2']/kPoint/@weight") == [
                          '1.0000000000', '2.0000000000'
                      ]
    assert eval_xpath(root, "/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='default-2']/@count") == '2'
    assert eval_xpath(root, '/fleurInput/cell/bzIntegration/kPointListSelection/@listName') == 'default-2'


def test_set_kpointlist_max5_overwrite(load_inpxml):
    from masci_tools.util.xml.xml_setters_names import set_kpointlist
    from masci_tools.util.xml.common_functions import eval_xpath

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH)
    root = xmltree.getroot()

    kpoints = [[0, 0, 0], [1, 1, 1]]
    weights = [1, 2]

    with pytest.raises(ValueError, match='kPointList named default already exists'):
        xmltree = set_kpointlist(xmltree, schema_dict, kpoints, weights, name='default')

    xmltree = set_kpointlist(xmltree, schema_dict, kpoints, weights, name='default', overwrite=True)

    assert eval_xpath(root, '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint/text()') == [
        ' 0.0000000000000  0.0000000000000  0.0000000000000', ' 1.0000000000000  1.0000000000000  1.0000000000000'
    ]
    assert eval_xpath(root, '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint/@weight') == [
        '1.0000000000', '2.0000000000'
    ]
    assert eval_xpath(root, '/fleurInput/cell/bzIntegration/kPointLists/kPointList/@count') == '2'
    assert eval_xpath(root, '/fleurInput/cell/bzIntegration/kPointLists/kPointList/@name') == 'default'
    assert eval_xpath(root, '/fleurInput/cell/bzIntegration/kPointLists/kPointList/@type') == 'path'


def test_set_kpointlist_max4(load_inpxml):
    from masci_tools.util.xml.xml_setters_names import set_kpointlist
    from masci_tools.util.xml.common_functions import eval_xpath

    xmltree, schema_dict = load_inpxml(TEST_MAX4_INPXML_PATH)
    root = xmltree.getroot()

    kpoints = [[0, 0, 0], [1, 1, 1]]
    weights = [1, 2]

    xmltree = set_kpointlist(xmltree, schema_dict, kpoints, weights)

    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint/text()') == [
        ' 0.0000000000000  0.0000000000000  0.0000000000000', ' 1.0000000000000  1.0000000000000  1.0000000000000'
    ]
    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint/@weight') == [
        '1.0000000000', '2.0000000000'
    ]
    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/kPointList/@count') == '2'


def test_set_kpointlist_max4_overwrite_kpointcount(load_inpxml):
    from masci_tools.util.xml.xml_setters_names import set_kpointlist, set_nkpts
    from masci_tools.util.xml.common_functions import eval_xpath

    xmltree, schema_dict = load_inpxml(TEST_MAX4_INPXML_PATH)
    root = xmltree.getroot()

    kpoints = [[0, 0, 0], [1, 1, 1]]
    weights = [1, 2]

    xmltree = set_nkpts(xmltree, schema_dict, 240)

    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/kPointCount/@count') == '240'

    xmltree = set_kpointlist(xmltree, schema_dict, kpoints, weights)

    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint/text()') == [
        ' 0.0000000000000  0.0000000000000  0.0000000000000', ' 1.0000000000000  1.0000000000000  1.0000000000000'
    ]
    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint/@weight') == [
        '1.0000000000', '2.0000000000'
    ]
    assert eval_xpath(root, '/fleurInput/calculationSetup/bzIntegration/kPointList/@count') == '2'
