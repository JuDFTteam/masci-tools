"""
Tests of the FleurElementMaker class
"""
import pytest
from masci_tools.io.parsers.fleur_schema import NoPathFound


def test_xml_builder():
    from masci_tools.util.xml.builder import FleurElementMaker
    from lxml import etree

    E = FleurElementMaker.fromVersion('0.34')
    elem = E.kpointlist(
        *(E.kpoint(kpt, weight=weight) for kpt, weight in zip([[0, 0, 0], [1, 2, 3], [4, 5, 6]], [9, 8, 7])),
        name='test',
        COUNT=100,
        TyPe='mesh')

    xmlstring = etree.tostring(elem, encoding='unicode', pretty_print=True)
    assert xmlstring == """<kPointList name="test" count="100" type="mesh">
  <kPoint weight="9.0000000000"> 0.0000000000000  0.0000000000000  0.0000000000000</kPoint>
  <kPoint weight="8.0000000000"> 1.0000000000000  2.0000000000000  3.0000000000000</kPoint>
  <kPoint weight="7.0000000000"> 4.0000000000000  5.0000000000000  6.0000000000000</kPoint>
</kPointList>
"""


def test_xml_builder_wrong_text_types():
    from masci_tools.util.xml.builder import FleurElementMaker

    E = FleurElementMaker.fromVersion('0.34')
    with pytest.raises(ValueError):
        E.kpointlist(*(E.kpoint(kpt, weight=weight) for kpt, weight in zip([False, [1, 2, 3], [4, 5, 6]], [9, 8, 7])),
                     name='test',
                     count=100,
                     type='mesh')


def test_xml_builder_wrong_attrib_types():
    from masci_tools.util.xml.builder import FleurElementMaker

    E = FleurElementMaker.fromVersion('0.34')
    with pytest.raises(ValueError):
        E.kpointlist(
            *(E.kpoint(kpt, weight=weight) for kpt, weight in zip([[0, 0, 0], [1, 2, 3], [4, 5, 6]], [9, 8, 7])),
            name='test',
            count=1.203,
            type='mesh')


def test_xml_builder_wrong_tag_names():
    from masci_tools.util.xml.builder import FleurElementMaker

    E = FleurElementMaker.fromVersion('0.34')

    with pytest.raises(NoPathFound):
        E.kpointlist(
            *(E.not_existent(kpt, weight=weight) for kpt, weight in zip([[0, 0, 0], [1, 2, 3], [4, 5, 6]], [9, 8, 7])),
            name='test',
            count=100,
            type='mesh')


def test_xml_builder_wrong_attrib_names():
    from masci_tools.util.xml.builder import FleurElementMaker

    E = FleurElementMaker.fromVersion('0.34')
    with pytest.raises(KeyError, match='The attribute NOT_EXISTENT is not allowed'):
        E.kpointlist(*(E.kpoint(kpt, weight=weight)
                       for kpt, weight in zip([[False, False, False], [1, 2, 3], [4, 5, 6]], [9, 8, 7])),
                     name='test',
                     NOT_EXISTENT=True,
                     type='mesh')
