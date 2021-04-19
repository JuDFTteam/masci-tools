# -*- coding: utf-8 -*-
"""
Test of the functions in masci_tools.util.xml.common_functions
"""
import pytest
import os
from pprint import pprint
import logging

TEST_FOLDER = os.path.dirname(os.path.abspath(__file__))
CLEAR_XML_TEST_FILE = os.path.abspath(os.path.join(TEST_FOLDER, 'files/fleur/test_clear.xml'))

LOGGER = logging.getLogger(__name__)


def test_eval_xpath(caplog):
    """
    Test of the eval_xpath function
    """
    from lxml import etree
    from masci_tools.util.xml.common_functions import eval_xpath

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

    species_z = eval_xpath(root, "//species[@name='Cu-1']/@atomicNumber")
    assert species_z == '29'

    ldau_tags = eval_xpath(root, "//species[@name='Cu-1']/ldaU")
    assert ldau_tags == []

    with pytest.raises(ValueError, match='There was a XpathEvalError on the xpath:'):
        ldau_tags = eval_xpath(root, "//species/[@name='Cu-1']/ldaU")

    with caplog.at_level(logging.WARNING):
        with pytest.raises(ValueError, match='There was a XpathEvalError on the xpath:'):
            ldau_tags = eval_xpath(root, "//species/[@name='Cu-1']/ldaU", logger=LOGGER)

    assert 'There was a XpathEvalError on the xpath:' in caplog.text


def test_clear_xml():
    """
    Test of the clear_xml function
    """
    from lxml import etree
    from masci_tools.util.xml.common_functions import eval_xpath, clear_xml
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


def test_get_xml_attribute(caplog):
    """
    Test of the clear_xml function
    """
    from lxml import etree
    from masci_tools.util.xml.common_functions import get_xml_attribute, eval_xpath
    parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8')
    xmltree = etree.parse(CLEAR_XML_TEST_FILE, parser)
    root = xmltree.getroot()

    scfLoop = eval_xpath(root, '//scfLoop')
    assert get_xml_attribute(scfLoop, 'alpha') == '.05000000'
    assert get_xml_attribute(scfLoop, 'itmax') == '1'
    assert get_xml_attribute(scfLoop, 'maxIterBroyd') == '99'

    with pytest.raises(ValueError, match='Tried to get attribute: "TEST" from element scfLoop.'):
        get_xml_attribute(scfLoop, 'TEST')

    with caplog.at_level(logging.WARNING):
        assert get_xml_attribute(scfLoop, 'TEST', logger=LOGGER) is None
    assert 'Tried to get attribute: "TEST" from element scfLoop.' in caplog.text

    with pytest.raises(TypeError,
                       match='Can not get attributename: "TEST" from node of type <class \'lxml.etree._ElementTree\'>'):
        get_xml_attribute(xmltree, 'TEST')

    with caplog.at_level(logging.WARNING):
        assert get_xml_attribute(xmltree, 'TEST', logger=LOGGER) is None
    assert 'Can not get attributename: "TEST" from node of type <class \'lxml.etree._ElementTree\'>' in caplog.text


def test_split_off_tag():
    """
    Test of the split_off_tag function
    """
    from masci_tools.util.xml.common_functions import split_off_tag

    assert split_off_tag('/fleurInput/calculationSetup/cutoffs') == ('/fleurInput/calculationSetup', 'cutoffs')
    assert split_off_tag('/fleurInput/calculationSetup/cutoffs/') == ('/fleurInput/calculationSetup', 'cutoffs')
    assert split_off_tag('./calculationSetup/cutoffs') == ('./calculationSetup', 'cutoffs')


def test_split_off_attrib():
    """
    Test of the split_off_tag function
    """
    from masci_tools.util.xml.common_functions import split_off_attrib

    assert split_off_attrib('/fleurInput/calculationSetup/cutoffs/@Kmax') == ('/fleurInput/calculationSetup/cutoffs',
                                                                              'Kmax')
    with pytest.raises(AssertionError):
        split_off_attrib('/fleurInput/calculationSetup/cutoffs')
    with pytest.raises(AssertionError):
        split_off_attrib("/fleurInput/atomSpecies/species[@name='TEST']")
    assert split_off_attrib('./calculationSetup/cutoffs/@Kmax') == ('./calculationSetup/cutoffs', 'Kmax')


def test_check_complex_xpath(load_inpxml):
    """
    Test of the check_complex_xpath function
    """
    from masci_tools.util.xml.common_functions import check_complex_xpath

    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    TEST_INPXML_PATH = os.path.join(FILE_PATH, 'files/fleur/Max-R5/FePt_film_SSFT_LO/files/inp2.xml')

    xmltree, _ = load_inpxml(TEST_INPXML_PATH)

    check_complex_xpath(xmltree, '/fleurInput/atomSpecies/species', "/fleurInput/atomSpecies/species[@name='Fe-1']")

    with pytest.raises(ValueError):
        check_complex_xpath(xmltree, '/fleurInput/atomSpecies/species',
                            "/fleurInput/atomSpecies/species[@name='Fe-1']/lo")

    with pytest.raises(ValueError):
        check_complex_xpath(xmltree, '/fleurInput/atomSpecies/species',
                            "/fleurInput/atomSpecies/species[@name='Fe-1']/@name")

    check_complex_xpath(xmltree, '/fleurInput/atomSpecies/species', '/fleurInput/atomSpecies/species')
    check_complex_xpath(xmltree, '/fleurInput/atomSpecies/species',
                        "/fleurInput/atomSpecies/species[@name='does_not_exist']")
    check_complex_xpath(xmltree, '/fleurInput/atomSpecies/species/lo', "//species[@name='Pt-1']/lo")


def test_abs_to_rel_xpath():

    from masci_tools.util.xml.common_functions import abs_to_rel_xpath

    assert abs_to_rel_xpath('/test/new_root/relative/path', 'new_root') == './relative/path'
    assert abs_to_rel_xpath('/test/new_root/relative/path/@attrib', 'new_root') == './relative/path/@attrib'
    assert abs_to_rel_xpath('/test/new_root/relative/path', 'path') == './'
    assert abs_to_rel_xpath('/test/new_root/relative/path/@attrib', 'path') == './@attrib'

    with pytest.raises(ValueError):
        abs_to_rel_xpath('/test/new_root/relative/path/@attrib', 'non_existent')
