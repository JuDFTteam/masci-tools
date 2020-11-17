from __future__ import absolute_import
import pytest
from masci_tools.io.parsers.fleur.fleur_inpxml_parser import inpxml_parser
import os

# Collect the input files
file_path1 = 'files/fleur/aiida_fleur/inpxml'
file_path2 = 'files/fleur/Max-R5'
file_path3 = 'files/fleur/aiida_fleur/nonvalid_inpxml'

inpxmlfilefolder = os.path.dirname(os.path.abspath(__file__))
inpxmlfilefolder_non_valid = [os.path.abspath(os.path.join(inpxmlfilefolder, file_path3))]

inpxmlfilefolder_valid = [os.path.abspath(os.path.join(inpxmlfilefolder, file_path1)),
                          os.path.abspath(os.path.join(inpxmlfilefolder, file_path2))]


ignore_inputs = ['NiO_ldauXML', 'Bi2Te3XML'] #These should fail but don't (except when they do)
#Thes inputs are currently broken in the fleur tests
broken_inputs = ['CoHybridPBE0', 'CoUnfold', 'Gd_Hubbard1',
                 'Gd_Hubbard1_noSYM', 'gw1Interface', 'GaAsWannSOC',
                  'TiO2eelsXML', 'gw2Interface',
                 'Fe_film_SS_conv', 'SiHybrid8kpt_nosym', 'Diamond_SCAN',
                 'Fe_bulk_SS_conv', 'Fe_film_SSFT']
inpxmlfilelist = []
inpxmlfilelist2 = []
for folder in inpxmlfilefolder_valid:
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.xml') and 'inp' in file:
                non_valid = False
                for broken in broken_inputs:
                    if broken in subdir:
                        inpxmlfilelist2.append(os.path.join(subdir, file))
                        non_valid = True
                for broken in ignore_inputs:
                    if broken in subdir:
                        non_valid = True
                if not non_valid:
                    inpxmlfilelist.append(os.path.join(subdir, file))

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

    #Parse before
    parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8')
    xmltree = etree.parse(inpxmlfilepath, parser)
    inp_dict = inpxml_parser(xmltree)



@pytest.mark.parametrize('inpxmlfilepath', inpxmlfilelist2)
def test_inpxml_non_valid_inpxml(inpxmlfilepath):
    """
    test if valid inp.xml files are recognized by the inpxml_parser
    """

    #Pass Path
    with pytest.raises((ValueError,FileNotFoundError)):
        inp_dict = inpxml_parser(inpxmlfilepath)
