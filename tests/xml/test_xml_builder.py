"""
Tests of the FleurElementMaker class
"""


def test_xml_builder():
    from masci_tools.util.xml.builder import FleurElementMaker
    from lxml import etree

    E = FleurElementMaker.fromVersion('0.34')
    elem = E.kpointlist(
        *(E.kpoint(kpt, weight=weight) for kpt, weight in zip([[0, 0, 0], [1, 2, 3], [4, 5, 6]], [9, 8, 7])),
        name='test',
        count=100,
        type='mesh')

    print(etree.tostring(elem, encoding='unicode', pretty_print=True))
    assert False
