# -*- coding: utf-8 -*-
"""
Tests of the inp.xml parser for Fleur
"""
import pytest
from masci_tools.io.parsers.fleur.fleur_inpxml_parser import inpxml_parser
import os

# Collect the input files
file_path1 = 'files/fleur/aiida_fleur/inpxml'
file_path2 = 'files/fleur/Max-R5'
file_path3 = 'files/fleur/aiida_fleur/nonvalid_inpxml'

inpxmlfilefolder = os.path.dirname(os.path.abspath(__file__))
inpxmlfilefolder_non_valid = [os.path.abspath(os.path.join(inpxmlfilefolder, file_path3))]

inpxmlfilefolder_valid = [
    os.path.abspath(os.path.join(inpxmlfilefolder, file_path1)),
    os.path.abspath(os.path.join(inpxmlfilefolder, file_path2))
]

#Thes inputs are currently broken in the fleur tests
broken_inputs = [
    'CoHybridPBE0', 'CoUnfold', 'gw1Interface', 'GaAsWannSOC', 'TiO2eelsXML', 'gw2Interface', 'Fe_film_SS_conv',
    'SiHybrid8kpt_nosym', 'Fe_bulk_SS_conv', 'Fe_film_SSFT', 'Max-R5/NiO_ldauXML', 'Max-R5/Bi2Te3XML'
]

inp_dict_input = ['FePt_film_SSFT_LO/files/inp2.xml']

inpxmlfilelist = []
inpxmlfilelist2 = []
inpxmlfilelist3 = []
for folder in inpxmlfilefolder_valid:
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.xml') and 'inp' in file:
                non_valid = False
                for broken in broken_inputs:
                    if broken in subdir:
                        inpxmlfilelist2.append(os.path.join(subdir, file))
                        non_valid = True
                if not non_valid:
                    inpxmlfilelist.append(os.path.join(subdir, file))
                    for inp_dictfolder in inp_dict_input:
                        if inp_dictfolder in os.path.join(subdir, file):
                            inpxmlfilelist3.append(os.path.join(subdir, file))

for folder in inpxmlfilefolder_non_valid:
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.xml') and 'inp' in file:
                inpxmlfilelist2.append(os.path.join(subdir, file))

expected_inp_dicts = [{
    'atomGroups': [{
        'filmPos': [[0.0, 0.0, -0.9964250044]],
        'force': {
            'calculate': True,
            'relaxXYZ': 'TTT'
        },
        'labels': {
            '                 222': [0.0, 0.0, -0.9964250044]
        },
        'nocoParams': {
            'alpha': 0.0,
            'beta': 1.570796326
        },
        'species': 'Fe-1'
    }, {
        'filmPos': [[0.5, 0.5, 0.9964250044]],
        'force': {
            'calculate': True,
            'relaxXYZ': 'TTT'
        },
        'labels': {
            '                   2': [0.5, 0.5, 0.9964250044]
        },
        'nocoParams': {
            'alpha': 0.0,
            'beta': 1.570796326
        },
        'species': 'Pt-1'
    }],
    'atomSpecies': [{
        'atomicCutoffs': {
            'lmax': 10,
            'lnonsphr': 6
        },
        'atomicNumber': 26,
        'electronConfig': {
            'coreConfig': ['[Ne]'],
            'stateOccupation': [{
                'spinDown': 1.0,
                'spinUp': 2.0,
                'state': '(3d3/2)'
            }, {
                'spinDown': 0.0,
                'spinUp': 3.0,
                'state': '(3d5/2)'
            }],
            'valenceConfig': ['(3s1/2)', '(3p1/2)', '(3p3/2)', '(4s1/2)', '(3d3/2)', '(3d5/2)']
        },
        'element': 'Fe',
        'energyParameters': {
            'd': 3,
            'f': 4,
            'p': 4,
            's': 4
        },
        'lo': [{
            'eDeriv': 0,
            'l': 0,
            'n': 3,
            'type': 'SCLO'
        }, {
            'eDeriv': 0,
            'l': 1,
            'n': 3,
            'type': 'SCLO'
        }],
        'mtSphere': {
            'gridPoints': 787,
            'logIncrement': 0.016,
            'radius': 2.2
        },
        'name': 'Fe-1'
    }, {
        'atomicCutoffs': {
            'lmax': 10,
            'lnonsphr': 6
        },
        'atomicNumber': 78,
        'electronConfig': {
            'coreConfig': ['[Kr]', '(5s1/2)', '(4d3/2)', '(4d5/2)', '(4f5/2)', '(4f7/2)'],
            'stateOccupation': [{
                'spinDown': 0.5,
                'spinUp': 0.5,
                'state': '(6s1/2)'
            }, {
                'spinDown': 2.0,
                'spinUp': 3.0,
                'state': '(5d5/2)'
            }],
            'valenceConfig': ['(5p1/2)', '(5p3/2)', '(6s1/2)', '(5d3/2)', '(5d5/2)']
        },
        'element': 'Pt',
        'energyParameters': {
            'd': 5,
            'f': 5,
            'p': 6,
            's': 6
        },
        'lo': [{
            'eDeriv': 0,
            'l': 1,
            'n': 5,
            'type': 'SCLO'
        }],
        'mtSphere': {
            'gridPoints': 787,
            'logIncrement': 0.017,
            'radius': 2.2
        },
        'name': 'Pt-1'
    }],
    'calculationSetup': {
        'coreElectrons': {
            'coretail_lmax': 0,
            'ctail': False,
            'frcor': False,
            'kcrel': 0
        },
        'cutoffs': {
            'Gmax': 10.0,
            'GmaxXC': 8.7,
            'Kmax': 4.0,
            'numbands': 0
        },
        'expertModes': {
            'gw': 0,
            'secvar': False
        },
        'geometryOptimization': {
            'epsdisp': 1e-05,
            'epsforce': 1e-05,
            'forcealpha': 1.0,
            'forcemix': 'BFGS',
            'l_f': False
        },
        'ldaU': {
            'l_linMix': False,
            'mixParam': 0.05,
            'spinf': 1.0
        },
        'magnetism': {
            'jspins': 2,
            'l_noco': True,
            'l_ss': True,
            'lflip': False,
            'qss': [0.0, 0.0, 0.0],
            'swsp': False
        },
        'prodBasis': {
            'bands': 0,
            'ewaldlambda': 3,
            'gcutm': 2.9,
            'lexp': 16,
            'tolerance': 0.0001
        },
        'scfLoop': {
            'alpha': 0.05,
            'imix': 'Anderson',
            'itmax': 1,
            'maxIterBroyd': 99,
            'minDistance': 1e-05,
            'precondParam': 0.0,
            'spinf': 2.0
        },
        'soc': {
            'l_soc': False,
            'phi': 0.0,
            'spav': False,
            'theta': 0.0
        },
        'xcFunctional': {
            'name': 'vwn',
            'relativisticCorrections': False
        }
    },
    'cell': {
        'bzIntegration': {
            'fermiSmearingEnergy':
            0.001,
            'kPointListSelection': {
                'listName': 'default'
            },
            'kPointLists': [{
                'count': 2,
                'kPoint': [[-0.25, 0.25, 0.0], [0.25, 0.25, 0.0]],
                'name': 'default',
                'weight': [0.5, 0.5]
            }],
            'mode':
            'hist',
            'valenceElectrons':
            32.0
        },
        'filmLattice': {
            'bravaisMatrix': {
                'row-1': [5.3011797029, 0.0, 0.0],
                'row-2': [0.0, 7.497000033, 0.0],
                'row-3': [0.0, 0.0, 7.9928500088]
            },
            'dTilda':
            10.91,
            'dVac':
            7.35,
            'scale':
            1.0,
            'vacuumEnergyParameters': [{
                'spinDown': -0.25,
                'spinUp': -0.25,
                'vacuum': 1
            }, {
                'spinDown': -0.25,
                'spinUp': -0.25,
                'vacuum': 2
            }]
        },
        'symmetryOperations': [{
            'row-1': [1.0, 0.0, 0.0, 0.0],
            'row-2': [0.0, 1.0, 0.0, 0.0],
            'row-3': [0.0, 0.0, 1.0, 0.0]
        }, {
            'row-1': [1.0, 0.0, 0.0, 0.0],
            'row-2': [0.0, -1.0, 0.0, 0.0],
            'row-3': [0.0, 0.0, 1.0, 0.0]
        }]
    },
    'comment':
    'A Fleur input generator calculation with aiida',
    'fleurInputVersion':
    '0.34',
    'forceTheorem': {
        'spinSpiralDispersion': ['0.0 0.0 0.0', '0.2 0.0 0.0']
    },
    'output': {
        'band': False,
        'chargeDensitySlicing': {
            'maxEigenval': 0.0,
            'minEigenval': 0.0,
            'nnne': 0,
            'numkpt': 0,
            'pallst': False
        },
        'checks': {
            'cdinf': False,
            'vchk': False
        },
        'dos': False,
        'plotting': {
            'iplot': 0
        },
        'slice': False,
        'specialOutput': {
            'bmt': False,
            'eonly': False
        },
        'unfoldingBand': {
            'supercellX': 1,
            'supercellY': 1,
            'supercellZ': 1,
            'unfoldBand': False
        }
    }
}]


@pytest.mark.parametrize('inpxmlfilepath', inpxmlfilelist)
def test_inpxml_valid_inpxml(inpxmlfilepath):
    """
    test if valid inp.xml files are recognized by the inpxml_parser
    """
    from lxml import etree

    #Pass inpxmlfile
    inp_dict = inpxml_parser(inpxmlfilepath)

    assert inp_dict is not None
    assert isinstance(inp_dict, dict)
    assert inp_dict != {}

    #Parse before
    parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8')
    xmltree = etree.parse(inpxmlfilepath, parser)
    inp_dict = inpxml_parser(xmltree)

    assert inp_dict is not None
    assert isinstance(inp_dict, dict)
    assert inp_dict != {}

    #Pass file handle
    with open(inpxmlfilepath, 'r') as inpfile:
        inp_dict = inpxml_parser(inpfile)

    assert inp_dict is not None
    assert isinstance(inp_dict, dict)
    assert inp_dict != {}


@pytest.mark.parametrize('inpxmlfilepath', inpxmlfilelist2)
def test_inpxml_non_valid_inpxml(inpxmlfilepath):
    """
    test if valid inp.xml files are recognized by the inpxml_parser
    """

    #Pass Path
    with pytest.raises((ValueError, FileNotFoundError)):
        inp_dict = inpxml_parser(inpxmlfilepath)


@pytest.mark.parametrize('inpxmlfilepath,expected_result', zip(inpxmlfilelist3, expected_inp_dicts))
def test_inpxml_todict(inpxmlfilepath, expected_result):
    """
    test if valid inp.xml files are translated to the correct inp_dict
    """

    inp_dict = inpxml_parser(inpxmlfilepath)
    assert inp_dict == expected_result


def test_inpxml_todict_warnings():
    """
    test if valid inp.xml files are translated to the correct inp_dict
    """
    expected_warnings = {
        'parser_warnings': [
            "Failed to convert attribute 'GmaxXC': Below are the warnings raised from convert_xml_attribute",
            "Could not evaluate expression '2..041' The following error was raised: Cannot parse number: Found two decimal points",
            "Failed to convert attribute 'minDistance': Below are the warnings raised from convert_xml_attribute",
            "Could not evaluate expression '1e5' The following error was raised: Unknown string expression: e",
            "Failed to convert text of 'qss': Below are the warnings raised from convert_xml_text",
            "Could not evaluate expression 'pi*2.0' The following error was raised: Unknown string expression: pi",
            "Could not evaluate expression 'cos1.0)' The following error was raised: Invalid expression: Expected Bracket after function name",
            "Could not evaluate expression 'Pi/(3.0-3.0)' The following error was raised: Undefined Expression: Division by zero"
        ],
        'parser_info':
        'Masci-Tools Fleur inp.xml Parser v0.1.1',
        'fleur_inp_version':
        '0.34'
    }

    input_invalid_attr = os.path.abspath(os.path.join(inpxmlfilefolder, 'files/fleur/inp_invalid_attributes.xml'))
    warnings = {'parser_warnings': []}

    #The parser shoul not raise and just log all the failed conversions
    inp_dict = inpxml_parser(input_invalid_attr, parser_info_out=warnings)

    assert warnings == expected_warnings
