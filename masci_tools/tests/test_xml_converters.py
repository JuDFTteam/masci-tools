# -*- coding: utf-8 -*-
"""
Test of the functions in masci_tools.util.xml.converters
"""
import pytest
import os
from masci_tools.util.constants import FLEUR_DEFINED_CONSTANTS
from pprint import pprint
import logging

TEST_FOLDER = os.path.dirname(os.path.abspath(__file__))
CLEAR_XML_TEST_FILE = os.path.abspath(os.path.join(TEST_FOLDER, 'files/fleur/test_clear.xml'))

LOGGER = logging.getLogger(__name__)


def test_convert_from_fortran_bool():
    """
    Test of the convert_from_fortran_bool function
    """
    from masci_tools.util.xml.converters import convert_from_fortran_bool

    TRUE_ITEMS = ('T', 't', True)
    FALSE_ITEMS = ('F', 'f', False)

    for true_item in TRUE_ITEMS:
        assert convert_from_fortran_bool(true_item)

    for false_item in FALSE_ITEMS:
        assert not convert_from_fortran_bool(false_item)

    with pytest.raises(ValueError, match="Could not convert: 'TEST' to boolean"):
        convert_from_fortran_bool('TEST')

    with pytest.raises(TypeError, match="Could not convert: '{}' to boolean"):
        convert_from_fortran_bool({})


def test_convert_to_fortran_bool():
    """
    Test of the function convert_to_fortran_bool
    """
    from masci_tools.util.xml.converters import convert_to_fortran_bool

    TRUE_ITEMS = (True, 'True', 't', 'T')
    FALSE_ITEMS = (False, 'False', 'f', 'F')

    for item in TRUE_ITEMS:
        assert convert_to_fortran_bool(item) == 'T'

    for item in FALSE_ITEMS:
        assert convert_to_fortran_bool(item) == 'F'

    with pytest.raises(ValueError, match='A string: NOT_A_BOOL for a boolean was given,'):
        convert_to_fortran_bool('NOT_A_BOOL')

    with pytest.raises(TypeError, match='convert_to_fortran_bool accepts only a string or bool as argument'):
        convert_to_fortran_bool(())


TEST_STRINGS = ['1.2314', 'all', ['all', '213', '-12'], ['PI', 'NOT_PI', '1.2'], ['F', 'T'], ['F', 'T']]

TEST_TYPES = [['float'], ['int', 'string'], ['int', 'string'], ['float', 'float_expression'], ['int'],
              ['int', 'switch']]

TEST_RESULTS = [(pytest.approx(1.2314), True), ('all', True), (['all', 213, -12], True),
                (['PI', 'NOT_PI', pytest.approx(1.2)], False), (['F', 'T'], False), ([False, True], True)]

TEST_WARNINGS = [[], [], [], [
    "Could not convert 'PI'",
    "Could not convert 'NOT_PI'",
], ["Could not convert 'F'", "Could not convert 'T'"]]


@pytest.mark.parametrize('string_attr,types,results', zip(TEST_STRINGS, TEST_TYPES, TEST_RESULTS))
def test_convert_xml_attribute(string_attr, types, results):
    """
    Test of the convert_xml_attribute function
    """
    from masci_tools.util.xml.converters import convert_xml_attribute

    expected_val, expected_suc = results

    if not expected_suc:
        with pytest.raises(ValueError, match='Could not convert'):
            ret_val, suc = convert_xml_attribute(string_attr, types, FLEUR_DEFINED_CONSTANTS)
    else:
        ret_val, suc = convert_xml_attribute(string_attr, types, FLEUR_DEFINED_CONSTANTS)

        assert ret_val == expected_val
        assert suc == expected_suc


@pytest.mark.parametrize('string_attr,types,results, warnings',
                         zip(TEST_STRINGS, TEST_TYPES, TEST_RESULTS, TEST_WARNINGS))
def test_convert_xml_attribute_warnings(caplog, string_attr, types, results, warnings):
    """
    Test of the convert_xml_attribute function
    """
    from masci_tools.util.xml.converters import convert_xml_attribute

    expected_val, expected_suc = results

    with caplog.at_level(logging.WARNING):
        ret_val, suc = convert_xml_attribute(string_attr, types, FLEUR_DEFINED_CONSTANTS, logger=LOGGER)
    assert ret_val == expected_val
    assert suc == expected_suc

    if len(warnings) == 0:
        assert caplog.text == ''
    else:
        for expected_warning in warnings:
            assert expected_warning in caplog.text


TEST_ATTR_VALUES = [1.2134, 'all', ['all', 213, '-12'], ['3.14', 'NOT_PI', 1.2], [False, 'True']]

TEST_ATTR_TYPES = [['float'], ['int', 'string'], ['int', 'string'], ['float', 'float_expression'], ['int', 'switch']]

TEST_ATTR_RESULTS = [('1.2134000000', True), ('all', True), (['all', '213', '-12'], True),
                     (['3.14', 'NOT_PI', '1.2000000000'], True), (['F', 'T'], True)]

TEST_ATTR_WARNINGS = [[], [], [], [], []]


@pytest.mark.parametrize('attr_value,types,results', zip(TEST_ATTR_VALUES, TEST_ATTR_TYPES, TEST_ATTR_RESULTS))
def test_convert_attribute_to_xml(attr_value, types, results):
    """
    Test of the convert_xml_attribute function
    """
    from masci_tools.util.xml.converters import convert_attribute_to_xml

    expected_val, expected_suc = results
    if not expected_suc:
        with pytest.raises(ValueError):
            ret_val, suc = convert_attribute_to_xml(attr_value, types)
    else:
        ret_val, suc = convert_attribute_to_xml(attr_value, types)
        assert ret_val == expected_val
        assert suc == expected_suc


@pytest.mark.parametrize('attr_value,types,results,warnings',
                         zip(TEST_ATTR_VALUES, TEST_ATTR_TYPES, TEST_ATTR_RESULTS, TEST_ATTR_WARNINGS))
def test_convert_attribute_to_xml_warnings(caplog, attr_value, types, results, warnings):
    """
    Test of the convert_xml_attribute function
    """
    from masci_tools.util.xml.converters import convert_attribute_to_xml

    expected_val, expected_suc = results

    with caplog.at_level(logging.WARNING):
        ret_val, suc = convert_attribute_to_xml(attr_value, types, logger=LOGGER)
    assert ret_val == expected_val
    assert suc == expected_suc

    if len(warnings) == 0:
        assert caplog.text == ''
    else:
        for expected_warning in warnings:
            assert expected_warning in caplog.text


TEST_TEXT_STRINGS = [
    '0.0 Pi/4.0 6.3121', '0.0 Pi/4.0 6.3121', '0.0 Pi/4.0 6.3121', '0.0 Pi/4.0 6.3121',
    ['0.0 Pi/4.0 6.3121', 'Bohr Pi/4.0 all', '0.0 Pi/*4.0 0.0'], ['F asd', 'T'],
    ['12 213 4215 412', '12 213 4215 412 123 14124']
]

TEST_DEFINITIONS = [[{
    'length': 3,
    'type': ['float', 'float_expression']
}], [{
    'length': 4,
    'type': ['float', 'float_expression']
}],
                    [{
                        'length': 4,
                        'type': ['float', 'float_expression']
                    }, {
                        'length': 'unbounded',
                        'type': ['float', 'float_expression']
                    }], [{
                        'length': 1,
                        'type': ['float', 'float_expression']
                    }], [{
                        'length': 3,
                        'type': ['float', 'float_expression']
                    }], [{
                        'length': 'unbounded',
                        'type': ['switch', 'string']
                    }], [{
                        'length': 4,
                        'type': ['switch', 'int']
                    }, {
                        'length': 'unbounded',
                        'type': ['int']
                    }]]

TEST_TEXT_RESULTS = [(pytest.approx([0.0, 0.7853981633974483, 6.3121]), True), ('0.0 Pi/4.0 6.3121', False),
                     (pytest.approx([0.0, 0.7853981633974483, 6.3121]), True), ('0.0 Pi/4.0 6.3121', False),
                     ([[0.0, 0.7853981633974483, 6.3121], [1.0, 0.7853981633974483, 'all'], [0.0, 'Pi/*4.0',
                                                                                             0.0]], False),
                     ([[False, 'asd'], [True]], True), ([[12, 213, 4215, 412], [12, 213, 4215, 412, 123, 14124]], True)]

TEST_TEXT_WARNINGS = [[], ["Failed to convert '0.0 Pi/4.0 6.3121', no matching definition found"], [],
                      [
                          "Could not convert '0.0 Pi/4.0 6.3121'",
                      ], [
                          "Could not convert 'all'",
                          "Could not convert 'Pi/*4.0'",
                      ], [], []]


@pytest.mark.parametrize('string_text,definitions, results', zip(TEST_TEXT_STRINGS, TEST_DEFINITIONS,
                                                                 TEST_TEXT_RESULTS))
def test_convert_xml_text(string_text, definitions, results):
    """
    Test of the convert_xml_attribute function
    """
    from masci_tools.util.xml.converters import convert_xml_text

    expected_val, expected_suc = results

    if not expected_suc:
        with pytest.raises(ValueError):
            ret_val, suc = convert_xml_text(string_text, definitions, FLEUR_DEFINED_CONSTANTS)
    else:
        ret_val, suc = convert_xml_text(string_text, definitions, FLEUR_DEFINED_CONSTANTS)
        assert ret_val == expected_val
        assert suc == expected_suc


@pytest.mark.parametrize('string_text,definitions,results,warnings',
                         zip(TEST_TEXT_STRINGS, TEST_DEFINITIONS, TEST_TEXT_RESULTS, TEST_TEXT_WARNINGS))
def test_convert_xml_text_warnings(caplog, string_text, definitions, results, warnings):
    """
    Test of the convert_xml_attribute function
    """
    from masci_tools.util.xml.converters import convert_xml_text

    expected_val, expected_suc = results

    with caplog.at_level(logging.WARNING):
        ret_val, suc = convert_xml_text(string_text, definitions, FLEUR_DEFINED_CONSTANTS, logger=LOGGER)
    assert ret_val == expected_val
    assert suc == expected_suc
    if len(warnings) == 0:
        assert caplog.text == ''
    else:
        for expected_warning in warnings:
            assert expected_warning in caplog.text


TEST_TEXT_VALUES = [[0.0, 'Pi/4.0', 6.3121], [0.0, 'Pi/4.0', 6.3121], [0.0, 'Pi/4.0', 6.3121], [0.0, 'Pi/4.0', 6.3121],
                    [[0.0, 'Pi/4.0', 6.3121], ['Bohr', 'Pi/4.0', 'all']], [[False, 'asd'], 'T'],
                    [[12, '213', 4215, 412], [12, '213', 4215, '412', 123, 14124]]]

TEST_TEXT_XML_STRINGS = [(' 0.0000000000000 Pi/4.0  6.3121000000000', True), ('', False),
                         (' 0.0000000000000 Pi/4.0  6.3121000000000', True), ('', False),
                         ([' 0.0000000000000 Pi/4.0  6.3121000000000', 'Bohr Pi/4.0 all'], True), (['F asd',
                                                                                                    'T'], True),
                         (['12 213 4215 412', '12 213 4215 412 123 14124'], True)]

TEST_TEXT_XML_WARNINGS = [[], ["Failed to convert '[0.0, 'Pi/4.0', 6.3121]', no matching definition found"], [],
                          ["Failed to convert '[0.0, 'Pi/4.0', 6.3121]', no matching definition found"], [], [], []]


@pytest.mark.parametrize('text_value,definitions, results',
                         zip(TEST_TEXT_VALUES, TEST_DEFINITIONS, TEST_TEXT_XML_STRINGS))
def test_convert_text_to_xml(text_value, definitions, results):
    """
    Test of the convert_xml_attribute function
    """
    from masci_tools.util.xml.converters import convert_text_to_xml

    expected_val, expected_suc = results
    if not expected_suc:
        with pytest.raises(ValueError):
            ret_val, suc = convert_text_to_xml(text_value, definitions)
    else:
        ret_val, suc = convert_text_to_xml(text_value, definitions)
        assert ret_val == expected_val
        assert suc == expected_suc


@pytest.mark.parametrize('text_value,definitions, results, warnings',
                         zip(TEST_TEXT_VALUES, TEST_DEFINITIONS, TEST_TEXT_XML_STRINGS, TEST_TEXT_XML_WARNINGS))
def test_convert_text_to_xml_warnings(caplog, text_value, definitions, results, warnings):
    """
    Test of the convert_xml_attribute function
    """
    from masci_tools.util.xml.converters import convert_text_to_xml

    expected_val, expected_suc = results

    with caplog.at_level(logging.WARNING):
        ret_val, suc = convert_text_to_xml(text_value, definitions, logger=LOGGER)
    assert ret_val == expected_val
    assert suc == expected_suc
    if len(warnings) == 0:
        assert caplog.text == ''
    else:
        for expected_warning in warnings:
            assert expected_warning in caplog.text
