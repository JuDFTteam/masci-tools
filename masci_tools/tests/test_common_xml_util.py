# -*- coding: utf-8 -*-
"""
Test of the functions in common_xml_util
"""
import pytest
import os
from masci_tools.util.constants import FLEUR_DEFINED_CONSTANTS

TEST_FOLDER = os.path.dirname(os.path.abspath(__file__))
CLEAR_XML_TEST_FILE = os.path.abspath(os.path.join(TEST_FOLDER, 'files/fleur/test_clear.xml'))


def test_convert_to_float():
    """
    Test of the convert_to_float function
    """
    from masci_tools.util.xml.common_xml_util import convert_to_float

    ret_val, suc = convert_to_float('0.45')
    assert suc
    assert pytest.approx(ret_val) == 0.45

    ret_val = convert_to_float('-99999231.2143543', suc_return=False)
    assert pytest.approx(ret_val) == -99999231.2143543

    ret_val, suc = convert_to_float('1.5324324e-9', suc_return=True)
    assert suc
    assert pytest.approx(ret_val) == 1.5324324e-9

    warnings = []
    ret_val, suc = convert_to_float({}, conversion_warnings=warnings)
    assert not suc
    assert ret_val == {}
    assert warnings == ["Could not convert: '{}' to float, TypeError"]

    warnings = []
    ret_val, suc = convert_to_float('1,23', conversion_warnings=warnings)
    assert not suc
    assert ret_val == '1,23'
    assert warnings == ["Could not convert: '1,23' to float, ValueError"]

    warnings = []
    ret_val, suc = convert_to_float('.325352', conversion_warnings=warnings)
    assert suc
    assert pytest.approx(ret_val) == .325352
    assert warnings == []


def test_convert_to_int():
    """
    Test of the convert_to_int function
    """
    from masci_tools.util.xml.common_xml_util import convert_to_int

    ret_val, suc = convert_to_int('1241412')
    assert suc
    assert ret_val == 1241412

    ret_val = convert_to_int('-9999999999999999999999', suc_return=False)
    assert ret_val == -9999999999999999999999

    ret_val, suc = convert_to_int('12031', suc_return=True)
    assert suc
    assert ret_val == 12031

    warnings = []
    ret_val, suc = convert_to_int((), conversion_warnings=warnings)
    assert not suc
    assert ret_val == ()
    assert warnings == ["Could not convert: '()' to int, TypeError"]

    warnings = []
    ret_val, suc = convert_to_int('1.231', conversion_warnings=warnings)
    assert not suc
    assert ret_val == '1.231'
    assert warnings == ["Could not convert: '1.231' to int, ValueError"]

    warnings = []
    ret_val, suc = convert_to_int('213', conversion_warnings=warnings)
    assert suc
    assert ret_val == 213
    assert warnings == []


def test_convert_from_fortran_bool():
    """
    Test of the convert_from_fortran_bool function
    """
    from masci_tools.util.xml.common_xml_util import convert_from_fortran_bool

    TRUE_ITEMS = ('T', 't', True)
    FALSE_ITEMS = ('F', 'f', False)

    for true_item in TRUE_ITEMS:
        ret_val, suc = convert_from_fortran_bool(true_item)
        assert suc
        assert ret_val

    for false_item in FALSE_ITEMS:
        ret_val, suc = convert_from_fortran_bool(false_item)
        assert suc
        assert not ret_val

    ret_val = convert_from_fortran_bool('T', suc_return=False)
    assert ret_val
    ret_val, suc = convert_from_fortran_bool('f', suc_return=True)
    assert suc
    assert not ret_val

    warnings = []
    ret_val, suc = convert_from_fortran_bool('TEST', conversion_warnings=warnings)
    assert not suc
    assert ret_val == 'TEST'
    assert warnings == ["Could not convert: 'TEST' to boolean, " "which is not 'True', 'False', 't', 'T', 'F' or 'f'"]

    warnings = []
    ret_val, suc = convert_from_fortran_bool({}, conversion_warnings=warnings)
    assert not suc
    assert ret_val == {}
    assert warnings == ["Could not convert: '{}' to boolean, only accepts str or boolean"]

    warnings = []
    ret_val, suc = convert_from_fortran_bool(True, conversion_warnings=warnings)
    assert suc
    assert ret_val
    assert warnings == []


def test_eval_xpath():
    """
    Test of the eval_xpath function
    """
    from lxml import etree
    from masci_tools.util.xml.common_xml_util import eval_xpath

    parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8')
    xmltree = etree.parse(CLEAR_XML_TEST_FILE, parser)
    root = xmltree.getroot()

    scfLoop = eval_xpath(root, '//scfLoop')
    assert isinstance(scfLoop, etree._Element)

    scfLoop = eval_xpath(root, '//scfLoop', list_return=True)
    assert len(scfLoop) == 1
    assert isinstance(scfLoop[0], etree._Element)

    include_tags = eval_xpath(root,
                              '//xi:include',
                              namespaces={'xi': 'http://www.w3.org/2001/XInclude'},
                              list_return=True)
    assert len(include_tags) == 2
    assert isinstance(include_tags[0], etree._Element)

    parser_info_out = {'parser_warnings': []}
    species_z = eval_xpath(root, "//species[@name='Cu-1']/@atomicNumber", parser_info_out=parser_info_out)
    assert species_z == '29'
    assert parser_info_out == {'parser_warnings': []}

    parser_info_out = {'parser_warnings': []}
    ldau_tags = eval_xpath(root, "//species[@name='Cu-1']/ldaU", parser_info_out=parser_info_out)
    assert ldau_tags == []
    assert parser_info_out == {'parser_warnings': []}

    parser_info_out = {'parser_warnings': []}
    ldau_tags = eval_xpath(root, "//species/[@name='Cu-1']/ldaU", parser_info_out=parser_info_out)
    assert ldau_tags == []
    assert parser_info_out == {
        'parser_warnings': [
            "There was a XpathEvalError on the xpath: //species/[@name='Cu-1']/ldaU \n Either it does not exist, or something is wrong with the expression."
        ]
    }


def test_clear_xml():
    """
    Test of the clear_xml function
    """
    from lxml import etree
    from masci_tools.util.xml.common_xml_util import eval_xpath, clear_xml
    parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8')
    xmltree = etree.parse(CLEAR_XML_TEST_FILE, parser)

    #Check that the file contains comments and includes
    root = xmltree.getroot()
    comments = eval_xpath(root, '//comment()', list_return=True)
    assert len(comments) == 3

    include_tags = eval_xpath(root,
                              '//xi:include',
                              namespaces={'xi': 'http://www.w3.org/2001/XInclude'},
                              list_return=True)
    assert len(include_tags) == 2

    symmetry_tags = eval_xpath(root, '//symOp', list_return=True)
    assert len(symmetry_tags) == 0

    cleared_tree = clear_xml(xmltree)
    cleared_root = cleared_tree.getroot()
    old_root = xmltree.getroot()

    #Make sure that the original tree was not modified
    comments = eval_xpath(old_root, '//comment()', list_return=True)
    assert len(comments) == 3

    #Check that the cleared tree is correct
    comments = eval_xpath(cleared_root, '//comment()', list_return=True)
    assert len(comments) == 0

    include_tags = eval_xpath(cleared_root,
                              '//xi:include',
                              namespaces={'xi': 'http://www.w3.org/2001/XInclude'},
                              list_return=True)
    assert len(include_tags) == 0

    symmetry_tags = eval_xpath(cleared_root, '//symOp', list_return=True)
    assert len(symmetry_tags) == 16


def test_get_xml_attribute():
    """
    Test of the clear_xml function
    """
    from lxml import etree
    from masci_tools.util.xml.common_xml_util import get_xml_attribute, eval_xpath
    parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8')
    xmltree = etree.parse(CLEAR_XML_TEST_FILE, parser)
    root = xmltree.getroot()

    scfLoop = eval_xpath(root, '//scfLoop')
    assert get_xml_attribute(scfLoop, 'alpha') == '.05000000'
    assert get_xml_attribute(scfLoop, 'itmax') == '1'

    parser_info_out = {'parser_warnings': []}
    assert get_xml_attribute(scfLoop, 'maxIterBroyd', parser_info_out=parser_info_out) == '99'
    assert parser_info_out == {'parser_warnings': []}

    parser_info_out = {'parser_warnings': []}
    assert get_xml_attribute(scfLoop, 'TEST', parser_info_out=parser_info_out) is None
    assert parser_info_out == {
        'parser_warnings': [
            'Tried to get attribute: "TEST" from element scfLoop.\n I recieved "None", maybe the attribute does not exist'
        ]
    }

    parser_info_out = {'parser_warnings': []}
    assert get_xml_attribute(xmltree, 'TEST', parser_info_out=parser_info_out) is None
    assert parser_info_out == {
        'parser_warnings': [
            'Can not get attributename: "TEST" from node of type <class \'lxml.etree._ElementTree\'>, because node is not an element of etree.'
        ]
    }
