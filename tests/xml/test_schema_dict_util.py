"""
Test of the utility functions for the schema dictionaries
both path finding and easy information extraction
"""
import pytest
import numpy as np
from masci_tools.io.parsers.fleur_schema import NoUniquePathFound, NoPathFound
from masci_tools.util.constants import FLEUR_DEFINED_CONSTANTS
from pprint import pprint
import logging

LOGGER = logging.getLogger(__name__)

TEST_INPXML_PATH = 'fleur/Max-R5/FePt_film_SSFT_LO/files/inp2.xml'
TEST_OUTXML_PATH = 'fleur/Max-R5/GaAsMultiUForceXML/files/out.xml'
TEST_OUTXML_PATH2 = 'fleur/Max-R5/FePt_film_SSFT_LO/files/out.xml'


def test_read_constants(load_inpxml, load_outxml):
    """
    Test of the read_constants function
    """
    from masci_tools.util.schema_dict_util import read_constants

    VALID_INP_CONSTANTS_PATH = 'fleur/inp_with_constants.xml'
    INVALID_INP_CONSTANTS_PATH = 'fleur/inp_invalid_constants.xml'
    VALID_OUT_CONSTANTS_PATH = 'fleur/out_with_constants.xml'

    xmltree, schema_dict = load_inpxml(VALID_INP_CONSTANTS_PATH, absolute=False)
    invalidxmltree, _ = load_inpxml(INVALID_INP_CONSTANTS_PATH, absolute=False)
    outxmltree, outschema_dict = load_outxml(VALID_OUT_CONSTANTS_PATH, absolute=False)

    root1 = xmltree.getroot()
    root2 = outxmltree.getroot()
    root3 = invalidxmltree.getroot()

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
    result = read_constants(root1, schema_dict)
    assert result == expected_constants

    result = read_constants(root2, outschema_dict)
    assert result == expected_constants

    with pytest.raises(KeyError, match='Ambiguous definition of constant Pi'):
        result = read_constants(root3, schema_dict)


def test_evaluate_attribute(caplog, load_inpxml, load_outxml):
    """
    Test of the evaluate_attribute function
    """
    from masci_tools.util.schema_dict_util import evaluate_attribute

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH, absolute=False)
    outxmltree, outschema_dict = load_outxml(TEST_OUTXML_PATH2, absolute=False)

    outroot = outxmltree.getroot()
    root = xmltree.getroot()

    assert evaluate_attribute(root, schema_dict, 'jspins', FLEUR_DEFINED_CONSTANTS) == 2
    assert evaluate_attribute(root, schema_dict, 'l_noco', FLEUR_DEFINED_CONSTANTS)
    assert evaluate_attribute(root, schema_dict, 'mode', FLEUR_DEFINED_CONSTANTS) == 'hist'
    assert pytest.approx(evaluate_attribute(root, schema_dict, 'radius', FLEUR_DEFINED_CONSTANTS,
                                            contains='species')) == [2.2, 2.2]

    with pytest.raises(NoUniquePathFound):
        evaluate_attribute(root, schema_dict, 'beta', FLEUR_DEFINED_CONSTANTS, exclude=['unique'])

    assert pytest.approx(
        evaluate_attribute(root,
                           schema_dict,
                           'beta',
                           FLEUR_DEFINED_CONSTANTS,
                           exclude=['unique'],
                           contains='nocoParams',
                           not_contains='species')) == [np.pi / 2.0, np.pi / 2.0]

    assert pytest.approx(
        evaluate_attribute(root,
                           schema_dict,
                           'beta',
                           FLEUR_DEFINED_CONSTANTS,
                           tag_name='nocoParams',
                           not_contains='species')) == [np.pi / 2.0, np.pi / 2.0]

    with pytest.raises(NoPathFound):
        evaluate_attribute(
            root,
            schema_dict,
            'TEST',
            FLEUR_DEFINED_CONSTANTS,
            tag_name='nocoParams',
            not_contains='species',
        )

    assert pytest.approx(
        evaluate_attribute(outroot,
                           outschema_dict,
                           'beta',
                           FLEUR_DEFINED_CONSTANTS,
                           exclude=['unique'],
                           contains='nocoParams',
                           not_contains='species')) == [np.pi / 2.0, np.pi / 2.0]

    iteration = outroot.xpath('//iteration')[0]

    assert evaluate_attribute(iteration,
                              outschema_dict,
                              'units',
                              FLEUR_DEFINED_CONSTANTS,
                              tag_name='Forcetheorem_SSDISP') == 'Htr'

    with pytest.raises(NoPathFound):
        evaluate_attribute(iteration, outschema_dict, 'TEST', FLEUR_DEFINED_CONSTANTS, tag_name='Forcetheorem_SSDISP')

    with pytest.raises(NoUniquePathFound):
        evaluate_attribute(root, schema_dict, 'spinf', FLEUR_DEFINED_CONSTANTS)

    with pytest.raises(ValueError, match='No values found for attribute radius'):
        evaluate_attribute(root, schema_dict, 'radius', FLEUR_DEFINED_CONSTANTS, not_contains='species')

    with caplog.at_level(logging.WARNING):
        assert evaluate_attribute(
            root, schema_dict, 'radius', FLEUR_DEFINED_CONSTANTS, not_contains='species', logger=LOGGER) is None
    assert 'No values found for attribute radius' in caplog.text


def test_evaluate_text(caplog, load_inpxml, load_outxml):
    """
    Test of the evaluate_text function
    """
    from masci_tools.util.schema_dict_util import evaluate_text

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH, absolute=False)
    outxmltree, outschema_dict = load_outxml(TEST_OUTXML_PATH2, absolute=False)

    outroot = outxmltree.getroot()
    root = xmltree.getroot()

    assert pytest.approx(evaluate_text(root, schema_dict, 'qss', FLEUR_DEFINED_CONSTANTS)) == [0.0, 0.0, 0.0]
    kpoints = evaluate_text(root, schema_dict, 'kPoint', FLEUR_DEFINED_CONSTANTS)
    expected = [[-0.25, 0.25, 0.0], [0.25, 0.25, 0.0]]
    for val, result in zip(kpoints, expected):
        assert pytest.approx(val) == result

    positions = evaluate_text(root, schema_dict, 'filmPos', FLEUR_DEFINED_CONSTANTS)
    positions_out = evaluate_text(outroot, outschema_dict, 'filmPos', FLEUR_DEFINED_CONSTANTS)

    expected = [[0.0, 0.0, -0.9964250044], [0.5, 0.5, 0.9964250044]]
    for val, result in zip(positions, expected):
        assert pytest.approx(val) == result
    for val, result in zip(positions_out, expected):
        assert pytest.approx(val) == result

    with pytest.raises(NoUniquePathFound):
        evaluate_text(root, schema_dict, 'row-1', FLEUR_DEFINED_CONSTANTS)
    #Test the correct passing of contains parameters

    sym_row1 = evaluate_text(root, schema_dict, 'row-1', FLEUR_DEFINED_CONSTANTS, contains='symOp')
    expected = [[1.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0]]
    for val, result in zip(sym_row1, expected):
        assert pytest.approx(val) == result
    assert pytest.approx(
        evaluate_text(root,
                      schema_dict,
                      'row-1',
                      FLEUR_DEFINED_CONSTANTS,
                      not_contains='symOp',
                      contains='filmLattice/bravaisMatrix')) == [5.3011797029, 0.0, 0.0]

    with pytest.raises(NoPathFound):
        evaluate_text(root, schema_dict, 'TEST', FLEUR_DEFINED_CONSTANTS)

    with pytest.raises(ValueError, match='No text found for tag magnetism'):
        evaluate_text(root, schema_dict, 'magnetism', FLEUR_DEFINED_CONSTANTS, not_contains='species')

    with caplog.at_level(logging.WARNING):
        assert evaluate_text(
            root, schema_dict, 'magnetism', FLEUR_DEFINED_CONSTANTS, not_contains='species', logger=LOGGER) is None
    assert 'No text found for tag magnetism' in caplog.text


def test_evaluate_tag(caplog, load_inpxml, load_outxml):
    """
    Test of the evaluate_tag function
    """
    from masci_tools.util.schema_dict_util import evaluate_tag

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH, absolute=False)
    outxmltree, outschema_dict = load_outxml(TEST_OUTXML_PATH2, absolute=False)

    outroot = outxmltree.getroot()
    root = xmltree.getroot()

    expected = {
        'itmax': 1,
        'maxIterBroyd': 99,
        'imix': 'Anderson',
        'alpha': 0.05,
        'precondParam': 0.0,
        'spinf': 2.0,
        'minDistance': 1e-05,
        'maxTimeToStartIter': None
    }
    scfloop = evaluate_tag(root, schema_dict, 'scfLoop', FLEUR_DEFINED_CONSTANTS)
    assert scfloop == expected

    with pytest.raises(NoPathFound):
        evaluate_tag(root, schema_dict, 'TEST', FLEUR_DEFINED_CONSTANTS)
    with pytest.raises(NoUniquePathFound):
        evaluate_tag(root, schema_dict, 'mtSphere', FLEUR_DEFINED_CONSTANTS)

    with pytest.raises(ValueError, match='Failed to evaluate attributes from tag qss'):
        evaluate_tag(root, schema_dict, 'qss', FLEUR_DEFINED_CONSTANTS, text=False)

    with caplog.at_level(logging.WARNING):
        assert len(evaluate_tag(root, schema_dict, 'qss', FLEUR_DEFINED_CONSTANTS, logger=LOGGER, text=False)) == 0
    assert 'Failed to evaluate attributes from tag qss' in caplog.text

    assert evaluate_tag(root, schema_dict, 'qss', FLEUR_DEFINED_CONSTANTS) == {'qss': [0.0, 0.0, 0.0]}

    expected = {'radius': [2.2, 2.2], 'gridPoints': [787, 787], 'logIncrement': [0.016, 0.017]}
    mtRadii = evaluate_tag(root, schema_dict, 'mtSphere', FLEUR_DEFINED_CONSTANTS, contains='species')
    assert mtRadii == expected

    mtRadii = evaluate_tag(outroot, outschema_dict, 'mtSphere', FLEUR_DEFINED_CONSTANTS, contains='species')
    assert mtRadii == expected

    expected = {
        'l_constrained': None,
        'l_mtNocoPot': None,
        'l_relaxSQA': None,
        'l_magn': None,
        'M': None,
        'alpha': [0.0, 0.0],
        'beta': [1.570796326, 1.570796326],
        'b_cons_x': None,
        'b_cons_y': None
    }
    nocoParams = evaluate_tag(root, schema_dict, 'nocoParams', FLEUR_DEFINED_CONSTANTS, contains='atomGroup')
    assert nocoParams == expected

    expected = {
        'alpha': [0.0, 0.0],
        'beta': [1.570796326, 1.570796326],
    }
    nocoParams = evaluate_tag(root,
                              schema_dict,
                              'nocoParams',
                              FLEUR_DEFINED_CONSTANTS,
                              contains='atomGroup',
                              only_required=True)
    assert nocoParams == expected

    expected = {
        'beta': [1.570796326, 1.570796326],
    }
    nocoParams = evaluate_tag(root,
                              schema_dict,
                              'nocoParams',
                              FLEUR_DEFINED_CONSTANTS,
                              contains='atomGroup',
                              only_required=True,
                              ignore=['alpha'])
    assert nocoParams == expected

    expected = {
        'atomicCutoffs': [{
            'lmax': 10,
            'lnonsphr': 6
        }, {
            'lmax': 10,
            'lnonsphr': 6
        }],
        'atomicNumber': [26, 78],
        'electronConfig': [{
            'coreConfig': ['[Ne]']
        }, {
            'coreConfig': ['[Kr]', '(5s1/2)', '(4d3/2)', '(4d5/2)', '(4f5/2)', '(4f7/2)']
        }],
        'mtSphere': [{
            'gridPoints': 787,
            'logIncrement': 0.016,
            'radius': 2.2
        }, {
            'gridPoints': 787,
            'logIncrement': 0.017,
            'radius': 2.2
        }],
        'name': ['Fe-1', 'Pt-1']
    }

    species = evaluate_tag(root, schema_dict, 'species', FLEUR_DEFINED_CONSTANTS, subtags=True, only_required=True)
    assert species == expected

    expected = {'coreConfig': [['[Ne]'], ['[Kr]', '(5s1/2)', '(4d3/2)', '(4d5/2)', '(4f5/2)', '(4f7/2)']]}

    electronconfig = evaluate_tag(root,
                                  schema_dict,
                                  'electronconfig',
                                  FLEUR_DEFINED_CONSTANTS,
                                  subtags=True,
                                  only_required=True)
    assert electronconfig == expected


def test_single_value_tag(caplog, load_outxml):
    """
    Test of the evaluate_single_value_tag function
    """
    from lxml import etree
    from masci_tools.util.schema_dict_util import evaluate_single_value_tag
    from masci_tools.util.xml.common_functions import eval_xpath

    xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH, absolute=False)
    root = xmltree.getroot()

    iteration_xpath = schema_dict.tag_xpath('iteration')
    iteration = eval_xpath(root, iteration_xpath, list_return=True)[0]

    expected = {'comment': None, 'units': 'Htr', 'value': -4204.714048254}
    totalEnergy = evaluate_single_value_tag(iteration, schema_dict, 'totalEnergy', FLEUR_DEFINED_CONSTANTS)
    assert totalEnergy == expected

    expected = {'value': -4204.714048254}
    totalEnergy = evaluate_single_value_tag(iteration,
                                            schema_dict,
                                            'totalEnergy',
                                            FLEUR_DEFINED_CONSTANTS,
                                            only_required=True)
    assert totalEnergy == expected

    with pytest.raises(NoPathFound):
        evaluate_single_value_tag(root, schema_dict, 'total_energy', FLEUR_DEFINED_CONSTANTS)
    with pytest.raises(NoUniquePathFound):
        evaluate_single_value_tag(root, schema_dict, 'totalCharge', FLEUR_DEFINED_CONSTANTS)

    expected = {'units': None, 'value': 63.9999999893}
    with pytest.raises(ValueError,
                       match="Failed to evaluate singleValue from tag totalCharge: Has no 'units' attribute"):
        evaluate_single_value_tag(iteration,
                                  schema_dict,
                                  'totalCharge',
                                  FLEUR_DEFINED_CONSTANTS,
                                  contains='allElectronCharges',
                                  not_contains='fixed')

    with caplog.at_level(logging.WARNING):
        totalCharge = evaluate_single_value_tag(iteration,
                                                schema_dict,
                                                'totalCharge',
                                                FLEUR_DEFINED_CONSTANTS,
                                                contains='allElectronCharges',
                                                not_contains='fixed',
                                                logger=LOGGER)
    assert totalCharge == expected
    assert "Failed to evaluate singleValue from tag totalCharge: Has no 'units' attribute" in caplog.text

    expected = {'value': 63.9999999893}
    totalCharge = evaluate_single_value_tag(iteration,
                                            schema_dict,
                                            'totalCharge',
                                            FLEUR_DEFINED_CONSTANTS,
                                            contains='allElectronCharges',
                                            not_contains='fixed',
                                            ignore=['units'])
    assert totalCharge == expected


def test_evaluate_parent_tag(load_outxml):
    """
    Test of the evaluate_parent_tag function
    """
    from masci_tools.util.schema_dict_util import evaluate_parent_tag

    xmltree, schema_dict = load_outxml(TEST_OUTXML_PATH, absolute=False)
    root = xmltree.getroot()

    expected = {
        'atomicNumber': [31, 31, 33, 33],
        'element': ['Ga', 'Ga', 'As', 'As'],
        'name': ['Ga-1', 'Ga-1', 'As-2', 'As-2']
    }
    ldaU_species = evaluate_parent_tag(root, schema_dict, 'ldaU', FLEUR_DEFINED_CONSTANTS, contains='species')
    pprint(ldaU_species)
    assert ldaU_species == expected

    expected = {'atomicNumber': [31, 31, 33, 33], 'name': ['Ga-1', 'Ga-1', 'As-2', 'As-2']}
    ldaU_species = evaluate_parent_tag(root,
                                       schema_dict,
                                       'ldaU',
                                       FLEUR_DEFINED_CONSTANTS,
                                       contains='species',
                                       only_required=True)
    pprint(ldaU_species)
    assert ldaU_species == expected

    expected = {'name': ['Ga-1', 'Ga-1', 'As-2', 'As-2']}
    ldaU_species = evaluate_parent_tag(root,
                                       schema_dict,
                                       'ldaU',
                                       FLEUR_DEFINED_CONSTANTS,
                                       contains='species',
                                       only_required=True,
                                       ignore=['atomicNumber'])
    pprint(ldaU_species)
    assert ldaU_species == expected


def test_tag_exists(load_inpxml, load_outxml):
    """
    Test of the tag_exists function
    """
    from masci_tools.util.schema_dict_util import tag_exists

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH, absolute=False)
    outxmltree, outschema_dict = load_outxml(TEST_OUTXML_PATH2, absolute=False)

    outroot = outxmltree.getroot()
    root = xmltree.getroot()

    assert tag_exists(root, schema_dict, 'filmPos')
    assert tag_exists(root, schema_dict, 'calculationSetup')

    assert not tag_exists(root, schema_dict, 'ldaU', contains='species')
    assert tag_exists(root, schema_dict, 'ldaU', not_contains='atom')

    assert not tag_exists(outroot, outschema_dict, 'ldaU', contains='species')
    assert tag_exists(outroot, outschema_dict, 'ldaU', not_contains='atom')

    with pytest.raises(NoUniquePathFound):
        tag_exists(root, schema_dict, 'ldaU')
    with pytest.raises(NoPathFound):
        tag_exists(root, schema_dict, 'ldaU', contains='group')


def test_attrib_exists(load_inpxml, load_outxml):
    """
    Test of the tag_exists function
    """
    from masci_tools.util.schema_dict_util import attrib_exists

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH, absolute=False)
    outxmltree, outschema_dict = load_outxml(TEST_OUTXML_PATH2, absolute=False)

    outroot = outxmltree.getroot()
    root = xmltree.getroot()

    assert attrib_exists(root, schema_dict, 'itmax')
    assert attrib_exists(root, schema_dict, 'jspins')

    assert not attrib_exists(root, schema_dict, 'radius', contains='atomGroup')
    assert not attrib_exists(outroot, outschema_dict, 'radius', contains='atomGroup')

    with pytest.raises(NoUniquePathFound):
        attrib_exists(root, schema_dict, 'spinf')
    with pytest.raises(NoPathFound):
        attrib_exists(root, schema_dict, 'spinf', contains='group')


def test_get_number_of_nodes(load_inpxml, load_outxml):
    """
    Test of the get_number_of_nodes function
    """
    from masci_tools.util.schema_dict_util import get_number_of_nodes

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH, absolute=False)
    outxmltree, outschema_dict = load_outxml(TEST_OUTXML_PATH2, absolute=False)

    outroot = outxmltree.getroot()
    root = xmltree.getroot()

    assert get_number_of_nodes(root, schema_dict, 'filmPos') == 2
    assert get_number_of_nodes(root, schema_dict, 'calculationSetup') == 1
    assert get_number_of_nodes(root, schema_dict, 'ldaU', contains='species') == 0
    assert get_number_of_nodes(root, schema_dict, 'ldaU', not_contains='atom') == 1

    assert get_number_of_nodes(outroot, outschema_dict, 'filmPos') == 2
    assert get_number_of_nodes(outroot, outschema_dict, 'calculationSetup') == 1

    with pytest.raises(NoUniquePathFound):
        get_number_of_nodes(root, schema_dict, 'ldaU')
    with pytest.raises(NoPathFound):
        get_number_of_nodes(root, schema_dict, 'ldaU', contains='group')


def test_schema_dict_util_abs_to_rel_path(load_inpxml):
    """
    Test of the absolute to relative xpath conversion in schema_dict_util functions
    """
    from lxml import etree
    from masci_tools.util.schema_dict_util import eval_simple_xpath, get_number_of_nodes, tag_exists, \
                                                  evaluate_attribute, evaluate_tag, evaluate_parent_tag, \
                                                  evaluate_text

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH, absolute=False)
    root = xmltree.getroot()

    species = eval_simple_xpath(root, schema_dict, 'species')

    assert tag_exists(species[0], schema_dict, 'lo')
    assert tag_exists(species[1], schema_dict, 'lo')

    assert get_number_of_nodes(species[0], schema_dict, 'lo') == 2
    assert get_number_of_nodes(species[1], schema_dict, 'lo') == 1

    assert evaluate_attribute(species[0], schema_dict, 'name', constants=FLEUR_DEFINED_CONSTANTS) == 'Fe-1'

    assert evaluate_text(species[0], schema_dict, 'coreConfig', constants=FLEUR_DEFINED_CONSTANTS) == ['[Ne]']

    assert evaluate_tag(species[1], schema_dict, 'lo', constants=FLEUR_DEFINED_CONSTANTS) == {
        'eDeriv': 0,
        'l': 1,
        'n': 5,
        'type': 'SCLO'
    }
    assert evaluate_parent_tag(species[1], schema_dict, 'lo', constants=FLEUR_DEFINED_CONSTANTS) == {
        'atomicNumber': 78,
        'element': 'Pt',
        'name': 'Pt-1'
    }


def test_schema_dict_util_complex_xpath(load_inpxml):
    """
    Test of the complex xpath argument in schema_dict_util functions
    """
    from masci_tools.util.schema_dict_util import evaluate_attribute, evaluate_tag, evaluate_parent_tag, \
                                                  evaluate_text

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH, absolute=False)

    assert evaluate_attribute(
        xmltree,
        schema_dict,
        'type',
        contains='species/lo',
        complex_xpath="/fleurInput/atomSpecies/species[@name='Fe-1']/lo/@type") == ['SCLO', 'SCLO']
    with pytest.raises(ValueError):
        evaluate_attribute(xmltree,
                           schema_dict,
                           'type',
                           contains='species/lo',
                           complex_xpath="/fleurInput/atomSpecies/species[@name='Fe-1']/lo/@type",
                           filters={'lo': {
                               'index': 1
                           }})

    assert evaluate_text(
        xmltree,
        schema_dict,
        'coreConfig',
        contains='species',
        complex_xpath="/fleurInput/atomSpecies/species[@name='Fe-1']/electronConfig/coreConfig") == ['[Ne]']
    with pytest.raises(ValueError):
        evaluate_text(xmltree,
                      schema_dict,
                      'coreConfig',
                      contains='species',
                      complex_xpath="/fleurInput/atomSpecies/species[@name='Fe-1']/electronConfig/coreConfig",
                      filters={'lo': {
                          'index': 1
                      }})

    assert evaluate_tag(xmltree,
                        schema_dict,
                        'lo',
                        contains='species',
                        complex_xpath="/fleurInput/atomSpecies/species[@name='Pt-1']/lo") == {
                            'eDeriv': 0,
                            'l': 1,
                            'n': 5,
                            'type': 'SCLO'
                        }
    with pytest.raises(ValueError):
        evaluate_tag(xmltree,
                     schema_dict,
                     'lo',
                     contains='species',
                     complex_xpath="/fleurInput/atomSpecies/species[@name='Pt-1']/lo",
                     filters={'lo': {
                         'index': 1
                     }})

    assert evaluate_parent_tag(xmltree,
                               schema_dict,
                               'lo',
                               contains='species',
                               complex_xpath="/fleurInput/atomSpecies/species[@name='Pt-1']/lo") == {
                                   'atomicNumber': 78,
                                   'element': 'Pt',
                                   'name': 'Pt-1'
                               }
    with pytest.raises(ValueError):
        evaluate_parent_tag(xmltree,
                            schema_dict,
                            'lo',
                            contains='species',
                            complex_xpath="/fleurInput/atomSpecies/species[@name='Pt-1']/lo",
                            filters={'lo': {
                                'index': 1
                            }})


def test_schema_dict_util_filters(load_inpxml):
    """
    Test of the filters argument in schema_dict_util functions
    """
    from masci_tools.util.schema_dict_util import eval_simple_xpath, get_number_of_nodes, tag_exists, \
                                                  evaluate_attribute, evaluate_tag, evaluate_parent_tag, \
                                                  evaluate_text
    from masci_tools.util.xml.xpathbuilder import XPathBuilder

    xmltree, schema_dict = load_inpxml(TEST_INPXML_PATH, absolute=False)

    species = eval_simple_xpath(xmltree,
                                schema_dict,
                                'species',
                                filters={'species': {
                                    'name': 'Fe-1'
                                }},
                                list_return=True)
    assert len(species) == 1
    assert species[0].attrib['name'] == 'Fe-1'

    assert tag_exists(xmltree, schema_dict, 'lo', contains='species', filters={'species': {'name': 'Fe-1'}})
    assert not tag_exists(xmltree,
                          schema_dict,
                          'filmPos',
                          filters={
                              'atomGroup': {
                                  'species': 'Fe-1'
                              },
                              'filmPos': {
                                  'label': {
                                      'not-contains': '22'
                                  }
                              }
                          })

    assert get_number_of_nodes(xmltree, schema_dict, 'lo', contains='species', filters={'species': {
        'name': 'Fe-1'
    }}) == 2
    assert get_number_of_nodes(xmltree, schema_dict, 'lo', contains='species', filters={'species': {
        'name': 'Pt-1'
    }}) == 1

    assert evaluate_attribute(xmltree,
                              schema_dict,
                              'type',
                              contains='species/lo',
                              filters={'species': {
                                  'name': 'Fe-1'
                              }}) == ['SCLO', 'SCLO']
    assert evaluate_attribute(xmltree,
                              schema_dict,
                              'type',
                              contains='species/lo',
                              complex_xpath=XPathBuilder('/fleurInput/atomSpecies/species/lo/@type'),
                              filters={'species': {
                                  'name': 'Fe-1'
                              }}) == ['SCLO', 'SCLO']

    assert evaluate_text(xmltree, schema_dict, 'coreConfig', contains='species', filters={'species': {
        'name': 'Fe-1'
    }}) == ['[Ne]']
    assert evaluate_text(xmltree,
                         schema_dict,
                         'coreConfig',
                         contains='species',
                         complex_xpath=XPathBuilder('/fleurInput/atomSpecies/species/electronConfig/coreConfig'),
                         filters={'species': {
                             'name': 'Fe-1'
                         }}) == ['[Ne]']

    assert evaluate_tag(xmltree, schema_dict, 'lo', contains='species', filters={'species': {
        'name': 'Pt-1'
    }}) == {
        'eDeriv': 0,
        'l': 1,
        'n': 5,
        'type': 'SCLO'
    }
    assert evaluate_tag(xmltree,
                        schema_dict,
                        'lo',
                        contains='species',
                        complex_xpath=XPathBuilder('/fleurInput/atomSpecies/species/lo'),
                        filters={'species': {
                            'name': 'Pt-1'
                        }}) == {
                            'eDeriv': 0,
                            'l': 1,
                            'n': 5,
                            'type': 'SCLO'
                        }

    assert evaluate_parent_tag(xmltree, schema_dict, 'lo', contains='species', filters={'species': {
        'name': 'Pt-1'
    }}) == {
        'atomicNumber': 78,
        'element': 'Pt',
        'name': 'Pt-1'
    }
    evaluate_parent_tag(xmltree,
                        schema_dict,
                        'lo',
                        contains='species',
                        complex_xpath=XPathBuilder('/fleurInput/atomSpecies/species/lo'),
                        filters={'species': {
                            'name': 'Pt-1'
                        }})
