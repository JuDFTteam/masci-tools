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


@pytest.mark.parametrize('inpxmlfilepath', inpxmlfilelist3, ids=['Fe_film_SSFT_LO'])
def test_inpxml_todict(data_regression, inpxmlfilepath):
    """
    test if valid inp.xml files are translated to the correct inp_dict
    """

    inp_dict = inpxml_parser(inpxmlfilepath)
    data_regression.check(inp_dict)


def test_inpxml_todict_warnings(data_regression, clean_parser_log):
    """
    test if valid inp.xml files are translated to the correct inp_dict
    """

    input_invalid_attr = os.path.abspath(os.path.join(inpxmlfilefolder, 'files/fleur/inp_invalid_attributes.xml'))
    warnings = {}

    #The parser shoul not raise and just log all the failed conversions
    inp_dict = inpxml_parser(input_invalid_attr, parser_info_out=warnings)
    data_regression.check({'input_dict': inp_dict, 'warnings': clean_parser_log(warnings)})


def test_inpxml_newer_version(data_regression, clean_parser_log):
    """
    test if valid inp.xml files with not yet existent versions are parsed correctly (fall back to latest available)
    """

    INPXML_FILEPATH = os.path.abspath(os.path.join(inpxmlfilefolder, 'files/fleur/input_newer_version.xml'))
    warnings = {}
    #The parser shoul not raise and just log all the failed conversions
    inp_dict = inpxml_parser(INPXML_FILEPATH, parser_info_out=warnings)
    data_regression.check({'input_dict': inp_dict, 'warnings': clean_parser_log(warnings)})
