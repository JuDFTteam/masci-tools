# -*- coding: utf-8 -*-
"""
Test of the utility functions for the schema dictionaries
both path finding and easy information extraction
"""
import pytest
import os
import copy
import numpy as np
from masci_tools.io.parsers.fleur.fleur_schema import load_inpschema

#Load different schema versions (for now only input schemas)
schema_dict_33 = load_inpschema('0.33')
schema_dict_27 = load_inpschema('0.27')

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_INPXML_PATH = os.path.join(FILE_PATH, 'files/fleur/Max-R5/FePt_film_SSFT_LO/files/inp2.xml')

CONSTANTS = {
    'Pi': np.pi,
    'Deg': 2 * np.pi / 360.0,
    'Ang': 1.8897261247728981,
    'nm': 18.897261247728981,
    'pm': 0.018897261247728981,
    'Bohr': 1.0
}


def test_get_tag_xpath_input():
    """
    Test the path finding for tags for the input schema without additional options
    And verify with different version of the schema
    """
    from masci_tools.util.schema_dict_util import get_tag_xpath

    #First example easy (magnetism tag is unique and should not differ between the versions)
    assert get_tag_xpath(schema_dict_27, 'magnetism') == '/fleurInput/calculationSetup/magnetism'
    assert get_tag_xpath(schema_dict_33, 'magnetism') == '/fleurInput/calculationSetup/magnetism'

    #Differing paths between the version
    assert get_tag_xpath(schema_dict_27, 'bzIntegration') == '/fleurInput/calculationSetup/bzIntegration'
    assert get_tag_xpath(schema_dict_33, 'bzIntegration') == '/fleurInput/cell/bzIntegration'

    #Non existent tag in old version
    assert get_tag_xpath(schema_dict_33, 'DMI') == '/fleurInput/forceTheorem/DMI'
    with pytest.raises(ValueError, match='The tag DMI has no possible paths with the current specification.'):
        get_tag_xpath(schema_dict_27, 'DMI')

    #Multiple possible paths
    with pytest.raises(ValueError, match='The tag ldaU has multiple possible paths with the current specification.'):
        get_tag_xpath(schema_dict_27, 'ldaU')
    with pytest.raises(ValueError, match='The tag ldaU has multiple possible paths with the current specification.'):
        get_tag_xpath(schema_dict_33, 'ldaU')


def test_get_tag_xpath_contains():
    """
    Test the selection of paths based on a contained keyword
    """
    from masci_tools.util.schema_dict_util import get_tag_xpath

    schema_dict = copy.deepcopy(schema_dict_33)

    with pytest.raises(ValueError, match='The tag ldaU has multiple possible paths with the current specification.'):
        get_tag_xpath(schema_dict, 'ldaU')
    with pytest.raises(ValueError, match='The tag ldaU has multiple possible paths with the current specification.'):
        get_tag_xpath(schema_dict, 'ldaU', contains='atom')

    assert get_tag_xpath(schema_dict, 'ldaU', contains='calculationSetup') == '/fleurInput/calculationSetup/ldaU'
    assert get_tag_xpath(schema_dict, 'ldaU', contains='species') == '/fleurInput/atomSpecies/species/ldaU'
    assert get_tag_xpath(schema_dict, 'ldaU', contains='Group') == '/fleurInput/atomGroups/atomGroup/ldaU'

    with pytest.raises(ValueError, match='The tag ldaU has no possible paths with the current specification.'):
        get_tag_xpath(schema_dict, 'ldaU', contains='group')

    #Make sure that this did not modify the schema dict
    assert schema_dict == schema_dict_33


def test_get_tag_xpath_notcontains():
    """
    Test the selection of paths based on a not contained keyword
    """
    from masci_tools.util.schema_dict_util import get_tag_xpath

    schema_dict = copy.deepcopy(schema_dict_33)

    with pytest.raises(ValueError, match='The tag ldaU has multiple possible paths with the current specification.'):
        get_tag_xpath(schema_dict, 'ldaU')
    with pytest.raises(ValueError, match='The tag ldaU has multiple possible paths with the current specification.'):
        path = get_tag_xpath(schema_dict, 'ldaU', not_contains='calculationSetup')

    assert get_tag_xpath(schema_dict, 'ldaU', not_contains='atom') == '/fleurInput/calculationSetup/ldaU'
    with pytest.raises(ValueError, match='The tag ldaU has multiple possible paths with the current specification.'):
        assert get_tag_xpath(schema_dict, 'ldaU', not_contains='Group') == '/fleurInput/atomSpecies/species/ldaU'

    assert get_tag_xpath(schema_dict, 'ldaU', contains='atom',
                         not_contains='species') == '/fleurInput/atomGroups/atomGroup/ldaU'

    #Make sure that this did not modify the schema dict
    assert schema_dict == schema_dict_33


def test_get_attrib_xpath_input():
    """
    Test the path finding for tags for the input schema without additional options
    And verify with different version of the schema
    """
    from masci_tools.util.schema_dict_util import get_attrib_xpath

    #First example easy (magnetism tag is unique and should not differ between the versions)
    assert get_attrib_xpath(schema_dict_27, 'jspins') == '/fleurInput/calculationSetup/magnetism'
    assert get_attrib_xpath(schema_dict_33, 'jspins') == '/fleurInput/calculationSetup/magnetism'

    #Differing paths between the version
    assert get_attrib_xpath(schema_dict_27, 'mode') == '/fleurInput/calculationSetup/bzIntegration'
    assert get_attrib_xpath(schema_dict_33, 'mode') == '/fleurInput/cell/bzIntegration'

    #Non existent tag in old version
    assert get_attrib_xpath(schema_dict_33, 'l_mtNocoPot') == '/fleurInput/calculationSetup/magnetism/mtNocoParams'
    with pytest.raises(ValueError,
                       match='The attrib l_mtNocoPot has no possible paths with the current specification.'):
        get_attrib_xpath(schema_dict_27, 'l_mtNocoPot')

    #Multiple possible paths
    with pytest.raises(ValueError,
                       match='The attrib l_amf has multiple possible paths with the current specification.'):
        get_attrib_xpath(schema_dict_27, 'l_amf')
    with pytest.raises(ValueError,
                       match='The attrib l_amf has multiple possible paths with the current specification.'):
        get_attrib_xpath(schema_dict_33, 'l_amf')


def test_get_attrib_xpath_contains():
    """
    Test the selection of paths based on a contained keyword
    """
    from masci_tools.util.schema_dict_util import get_attrib_xpath

    schema_dict = copy.deepcopy(schema_dict_33)

    with pytest.raises(ValueError,
                       match='The attrib l_mperp has multiple possible paths with the current specification.'):
        get_attrib_xpath(schema_dict, 'l_mperp')

    assert get_attrib_xpath(schema_dict, 'l_mperp',
                            contains='magnetism') == '/fleurInput/calculationSetup/magnetism/mtNocoParams'
    assert get_attrib_xpath(schema_dict, 'l_mperp',
                            contains='greensFunction') == '/fleurInput/calculationSetup/greensFunction'

    with pytest.raises(ValueError, match='The attrib l_mperp has no possible paths with the current specification.'):
        get_attrib_xpath(schema_dict, 'l_mperp', contains='atom')

    #Make sure that this did not modify the schema dict
    assert schema_dict == schema_dict_33


def test_get_attrib_xpath_notcontains():
    """
    Test the selection of paths based on a contained keyword
    """
    from masci_tools.util.schema_dict_util import get_attrib_xpath

    schema_dict = copy.deepcopy(schema_dict_33)

    with pytest.raises(ValueError,
                       match='The attrib l_mperp has multiple possible paths with the current specification.'):
        get_attrib_xpath(schema_dict, 'l_mperp')

    assert get_attrib_xpath(schema_dict, 'l_mperp',
                            not_contains='greensFunction') == '/fleurInput/calculationSetup/magnetism/mtNocoParams'
    assert get_attrib_xpath(schema_dict, 'l_mperp',
                            not_contains='magnetism') == '/fleurInput/calculationSetup/greensFunction'

    assert get_attrib_xpath(schema_dict, 'l_mperp', contains='greensFunction',
                            not_contains='magnetism') == '/fleurInput/calculationSetup/greensFunction'

    with pytest.raises(ValueError, match='The attrib l_mperp has no possible paths with the current specification.'):
        get_attrib_xpath(schema_dict, 'l_mperp', not_contains='calculationSetup')

    #Make sure that this did not modify the schema dict
    assert schema_dict == schema_dict_33


def test_get_attrib_xpath_exclude():
    """
    Test the selection of paths based on a contained keyword
    """
    from masci_tools.util.schema_dict_util import get_attrib_xpath

    schema_dict = copy.deepcopy(schema_dict_33)

    assert get_attrib_xpath(schema_dict, 'alpha') == '/fleurInput/calculationSetup/scfLoop'
    assert get_attrib_xpath(schema_dict, 'alpha', exclude=['unique_path',
                                                           'other']) == '/fleurInput/calculationSetup/scfLoop'
    with pytest.raises(ValueError,
                       match='The attrib alpha has multiple possible paths with the current specification.'):
        get_attrib_xpath(schema_dict, 'alpha', exclude=['unique'])

    assert get_attrib_xpath(schema_dict, 'alpha', not_contains='atom',
                            exclude=['unique']) == '/fleurInput/calculationSetup/greensFunction/contourSemicircle'

    #Make sure that this did not modify the schema dict
    assert schema_dict == schema_dict_33


def test_evaluate_attribute():
    """
    Test of the evaluate_attribute function
    """
    from lxml import etree
    from masci_tools.util.schema_dict_util import evaluate_attribute

    schema_dict = copy.deepcopy(schema_dict_33)

    parser = etree.XMLParser(attribute_defaults=True, recover=False, encoding='utf-8')
    xmltree = etree.parse(TEST_INPXML_PATH, parser)

    root = xmltree.getroot()

    assert evaluate_attribute(root, schema_dict, 'jspins', CONSTANTS) == 2
    assert evaluate_attribute(root, schema_dict, 'l_noco', CONSTANTS)
    assert evaluate_attribute(root, schema_dict, 'mode', CONSTANTS) == 'hist'
    assert pytest.approx(evaluate_attribute(root, schema_dict, 'radius', CONSTANTS, contains='species')) == [2.2, 2.2]

    with pytest.raises(ValueError, match='The attrib beta has multiple possible paths with the current specification.'):
        evaluate_attribute(root, schema_dict, 'beta', CONSTANTS, exclude=['unique'])

    assert pytest.approx(
        evaluate_attribute(root,
                           schema_dict,
                           'beta',
                           CONSTANTS,
                           exclude=['unique'],
                           contains='nocoParams',
                           not_contains='species')) == [np.pi / 2.0, np.pi / 2.0]

    with pytest.raises(ValueError, match='The attrib l_Noco has no possible paths with the current specification.'):
        evaluate_attribute(root, schema_dict, 'l_Noco', CONSTANTS)

    with pytest.raises(ValueError,
                       match='The attrib spinf has multiple possible paths with the current specification.'):
        evaluate_attribute(root, schema_dict, 'spinf', CONSTANTS)

    expected_info = {'parser_warnings': ['No values found for attribute radius']}

    parser_info_out = {'parser_warnings': []}
    assert evaluate_attribute(
        root, schema_dict, 'radius', CONSTANTS, not_contains='species', parser_info_out=parser_info_out) is None
    assert parser_info_out == expected_info
    assert schema_dict == schema_dict_33


def test_evaluate_text():
    """
    Test of the evaluate_text function
    """
    from lxml import etree
    from masci_tools.util.schema_dict_util import evaluate_text

    schema_dict = copy.deepcopy(schema_dict_33)

    parser = etree.XMLParser(attribute_defaults=True, recover=False, encoding='utf-8')
    xmltree = etree.parse(TEST_INPXML_PATH, parser)

    root = xmltree.getroot()

    assert pytest.approx(evaluate_text(root, schema_dict, 'qss', CONSTANTS)) == [0.0, 0.0, 0.0]
    kpoints = evaluate_text(root, schema_dict, 'kPoint', CONSTANTS)
    expected = [[-0.25, 0.25, 0.0], [0.25, 0.25, 0.0]]
    for val, result in zip(kpoints, expected):
        assert pytest.approx(val) == result

    positions = evaluate_text(root, schema_dict, 'filmPos', CONSTANTS)
    expected = [[0.0, 0.0, -0.9964250044], [0.5, 0.5, 0.9964250044]]
    for val, result in zip(positions, expected):
        assert pytest.approx(val) == result

    with pytest.raises(ValueError, match='The tag row-1 has multiple possible paths with the current specification.'):
        evaluate_text(root, schema_dict, 'row-1', CONSTANTS)
    #Test the correct passing of contains parameters

    sym_row1 = evaluate_text(root, schema_dict, 'row-1', CONSTANTS, contains='symOp')
    expected = [[1.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0]]
    for val, result in zip(sym_row1, expected):
        assert pytest.approx(val) == result
    assert pytest.approx(
        evaluate_text(root, schema_dict, 'row-1', CONSTANTS, not_contains='symOp',
                      contains='filmLattice/bravaisMatrix')) == [5.3011797029, 0.0, 0.0]

    with pytest.raises(ValueError, match='The tag Magnetism has no possible paths with the current specification.'):
        evaluate_text(root, schema_dict, 'Magnetism', CONSTANTS)

    expected_info = {'parser_warnings': ['No text found for tag magnetism']}
    parser_info_out = {'parser_warnings': []}
    assert evaluate_text(root, schema_dict, 'magnetism', CONSTANTS, parser_info_out=parser_info_out) is None
    assert parser_info_out == expected_info

    assert schema_dict == schema_dict_33
