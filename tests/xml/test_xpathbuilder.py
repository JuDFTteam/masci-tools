"""
Tests of the XPathBuilder class.
"""
import pytest
from lxml import etree

TEST_INPXML_PATH = 'fleur/Max-R5/FePt_film_SSFT_LO/files/inp2.xml'


def test_xpathbuilder():
    """
    Test the basic behaviour of the XPathBuilder class.
    """
    from masci_tools.util.xml.xpathbuilder import XPathBuilder

    simple_xpath = '/test/xpath/simple'

    xpath = XPathBuilder(simple_xpath)
    assert xpath.path == simple_xpath

    xpath.add_filter('xpath', {'index': -2})
    with pytest.raises(ValueError):
        xpath.add_filter('not-existing', {'index': -3})
    assert xpath.path == '/test/xpath[last() - $xpath_index]/simple'
    assert str(xpath) == '/test/xpath[last() - 1]/simple'
    assert xpath.path_variables == {'xpath_index': 1}

    xpath = XPathBuilder(simple_xpath, strict=True)
    with pytest.raises(ValueError):
        str(xpath)

    xpath = XPathBuilder(etree.XPath(simple_xpath), compile_path=True, smart_strings=True)
    xpath.add_filter('xpath', {'index': -2})
    assert isinstance(xpath.path, etree.XPath)
    assert str(xpath) == '/test/xpath[last() - 1]/simple'

    with pytest.raises(ValueError):
        xpath = XPathBuilder(etree.XPath(simple_xpath), smart_strings=True)


@pytest.mark.parametrize('simple_xpath,filters,expected', [
    ('/fleurInput/atomGroups/atomGroup/@species', {
        'atomGroup': {
            'index': -1
        }
    }, 'Pt-1'),
    ('/fleurInput/atomGroups/atomGroup/@species', {
        'atomGroup': {
            'index': {
                '==': -1
            }
        }
    }, 'Pt-1'),
    ('/fleurInput/atomGroups/atomGroup/@species', {
        'atomGroup': {
            'index': {
                '<': -1
            }
        }
    }, 'Fe-1'),
    ('/fleurInput/atomGroups/atomGroup/@species', {
        'atomGroup': {
            'index': {
                '>=': 2
            }
        }
    }, 'Pt-1'),
    ('/fleurInput/atomSpecies/species/@name', {
        'species': {
            '/mtSphere/@radius': {
                '>=': 2.0
            }
        }
    }, ['Fe-1', 'Pt-1']),
    ('/fleurInput/atomSpecies/species/mtSphere/@radius', {
        'species': {
            'name': {
                '==': 'Fe-1'
            }
        }
    }, '2.20000000'),
    ('/fleurInput/atomSpecies/species/@name', {
        'species': {
            '/mtSphere/@radius': {
                '==': '2.20000000'
            }
        }
    }, ['Fe-1', 'Pt-1']),
    ('/fleurInput/atomSpecies/species/@name', {
        'species': {
            'has': './lo'
        }
    }, ['Fe-1', 'Pt-1']),
    ('/fleurInput/atomSpecies/species/@name', {
        'species': {
            'has-not': './ldaU'
        }
    }, ['Fe-1', 'Pt-1']),
    ('/fleurInput/atomGroups/atomGroup/@species', {
        'atomGroup': {
            'filmPos/@label': {
                'contains': '22'
            }
        }
    }, 'Fe-1'),
    ('/fleurInput/atomGroups/atomGroup/@species', {
        'atomGroup': {
            'filmPos/@label': {
                'not-contains': '22'
            }
        }
    }, 'Pt-1'),
    ('/fleurInput/atomGroups/atomGroup/@species', {
        'atomGroup': {
            'and': [{
                'filmPos/@label': {
                    'not-contains': '22'
                }
            }, {
                'force/@relaxXYZ': 'TTT'
            }]
        }
    }, 'Pt-1'),
    ('/fleurInput/atomGroups/atomGroup/@species', {
        'atomGroup': {
            'or': [{
                'filmPos/@label': {
                    'not-contains': '22'
                }
            }, {
                'filmPos/@label': {
                    'contains': '22'
                }
            }]
        }
    }, ['Fe-1', 'Pt-1']),
    ('/fleurInput/atomSpecies/species/@name', {
        'species': {
            './lo': {
                'number-nodes': {
                    '>': 1
                }
            }
        }
    }, 'Fe-1'),
    ('/fleurInput/atomGroups/atomGroup/@species', {
        'atomGroup': {
            ('relPos/@label', 'filmPos/@label'): {
                'not-contains': '22'
            }
        }
    }, 'Pt-1'),
    ('/fleurInput/atomSpecies/species/@name', {
        'species': {
            'name': {
                'starts-with': 'P'
            }
        }
    }, 'Pt-1'),
    ('/fleurInput/atomGroups/atomGroup/@species', {
        'atomGroup': {
            ('relPos/@label', 'filmPos/@label'): {
                'ends-with': '22'
            }
        }
    }, 'Fe-1'),
    ('/fleurInput/atomSpecies/species/lo/@n', {
        'lo': {
            'l': {
                'in': [0, 1]
            }
        }
    }, ['3', '3', '5']),
    ('/fleurInput/atomSpecies/species/lo/@n', {
        'lo': {
            'l': {
                'not-in': [0, 2]
            }
        }
    }, ['3', '5']),
    ('/fleurInput/atomSpecies/species/electronConfig/coreConfig/text()', {
        'coreConfig': '[Ne]'
    }, '[Ne]'),
    ('/fleurInput/atomGroups/atomGroup/@species', {
        'atomGroup': {
            'species': {
                'string-length': {
                    '>=': 3
                }
            }
        }
    }, ['Fe-1', 'Pt-1']),
])
def test_xpathbuilder_with_eval(load_inpxml, simple_xpath, filters, expected):
    """
    Test the xpathbuilder with a variety of different Xpath expressions and filters
    """
    from masci_tools.util.xml.xpathbuilder import XPathBuilder
    from masci_tools.util.xml.common_functions import eval_xpath

    xmltree, _ = load_inpxml(TEST_INPXML_PATH, absolute=False)

    xpath = XPathBuilder(simple_xpath, filters=filters)
    print(f'Complex XPath: {str(xpath)}')
    res = eval_xpath(xmltree, xpath)
    assert res == expected
    assert str(xpath) != simple_xpath  # make sure the path is not the same as the original
