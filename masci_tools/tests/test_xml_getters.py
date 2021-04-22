# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Tests of the xml_getters
"""
import pytest
import os

#file_path1 = 'files/fleur/aiida_fleur/inpxml'
file_path2 = 'files/fleur/Max-R5'

inpxmlfilefolder = os.path.dirname(os.path.abspath(__file__))

inpxmlfilefolder_valid = [
    #    os.path.abspath(os.path.join(inpxmlfilefolder, file_path1)),
    os.path.abspath(os.path.join(inpxmlfilefolder, file_path2))
]

broken_inputs = [
    'CoHybridPBE0', 'CoUnfold', 'gw1Interface', 'GaAsWannSOC', 'TiO2eelsXML', 'gw2Interface', 'Fe_film_SS_conv',
    'SiHybrid8kpt_nosym', 'SiHybrid8kpt_sym', 'SiHybridGammaNoInv', 'Fe_bulk_SS_conv', 'Fe_film_SSFT',
    'Max-R5/NiO_ldauXML', 'Max-R5/Bi2Te3XML'
]

TEST_FILM_INPXML_PATH = os.path.join(inpxmlfilefolder, 'files/fleur/Max-R5/FePt_film_SSFT_LO/files/inp2.xml')
TEST_BULK_INPXML_PATH = os.path.join(inpxmlfilefolder, 'files/fleur/Max-R5/SiLOXML/files/inp.xml')
TEST_SINGLE_KPOINT_PATH = os.path.join(inpxmlfilefolder, 'files/fleur/Max-R5/SmAtomjDOS/files/inp.xml')
TEST_MULTIPLE_KPOINT_SETS_PATH = os.path.join(inpxmlfilefolder, 'files/fleur/test_multiple_ksets.xml')
TEST_MAX4_INPXML_PATH = os.path.join(inpxmlfilefolder, 'files/fleur/aiida_fleur/inpxml/FePt/inp.xml')
TEST_RELAX_INPXML_PATH = os.path.join(inpxmlfilefolder, 'files/fleur/Max-R5/GaAsMultiUForceXML/files/inp-3.xml')
TEST_RELAX_OUTXML_PATH = os.path.join(inpxmlfilefolder, 'files/fleur/Max-R5/GaAsMultiUForceXML/files/out.xml')
TEST_RELAX_RELAXXML_PATH = os.path.join(inpxmlfilefolder, 'files/fleur/Max-R5/GaAsMultiUForceXML/files/relax.xml')

inpxmlfilelist = []
inpxmlfilelist_content = []
for folder in inpxmlfilefolder_valid:
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.xml') and 'inp' in file:
                non_valid = False
                for broken in broken_inputs:
                    if broken in subdir:
                        non_valid = True
                if not non_valid:
                    inpxmlfilelist.append(os.path.join(subdir, file))


@pytest.mark.parametrize('inpxmlfilepath', inpxmlfilelist)
def test_get_cell(load_inpxml, inpxmlfilepath):
    """
    Test that get_cell works for all input files
    """
    from masci_tools.util.xml.xml_getters import get_cell
    import numpy as np

    xmltree, schema_dict = load_inpxml(inpxmlfilepath)

    cell, pbc = get_cell(xmltree, schema_dict)

    assert isinstance(cell, np.ndarray)
    assert cell.shape == (3, 3)
    assert isinstance(pbc, list)
    assert len(pbc) == 3


@pytest.mark.parametrize('inpxmlfilepath', inpxmlfilelist)
def test_get_structure_data(load_inpxml, inpxmlfilepath):
    """
    Test that get_cell works for all input files
    """
    from masci_tools.util.xml.xml_getters import get_structure_data
    import numpy as np

    xmltree, schema_dict = load_inpxml(inpxmlfilepath)

    atoms, cell, pbc = get_structure_data(xmltree, schema_dict)

    assert isinstance(atoms, list)
    assert len(atoms) != 0
    assert isinstance(cell, np.ndarray)
    assert cell.shape == (3, 3)
    assert isinstance(pbc, list)
    assert len(pbc) == 3


@pytest.mark.parametrize('inpxmlfilepath', inpxmlfilelist)
def test_get_parameter_data(load_inpxml, inpxmlfilepath):
    """
    Test that get_cell works for all input files
    """
    from masci_tools.util.xml.xml_getters import get_parameter_data

    xmltree, schema_dict = load_inpxml(inpxmlfilepath)

    para = get_parameter_data(xmltree, schema_dict)

    assert isinstance(para, dict)
    assert para != {}


@pytest.mark.parametrize('inpxmlfilepath', inpxmlfilelist)
def test_get_fleur_modes(load_inpxml, inpxmlfilepath):
    """
    Test that get_cell works for all input files
    """
    from masci_tools.util.xml.xml_getters import get_fleur_modes

    xmltree, schema_dict = load_inpxml(inpxmlfilepath)

    modes = get_fleur_modes(xmltree, schema_dict)

    assert isinstance(modes, dict)
    assert modes != {}


@pytest.mark.parametrize('inpxmlfilepath', inpxmlfilelist)
def test_get_kpoints_data(load_inpxml, inpxmlfilepath):
    """
    Test that get_cell works for all input files
    """
    from masci_tools.util.xml.xml_getters import get_kpoints_data
    import numpy as np

    xmltree, schema_dict = load_inpxml(inpxmlfilepath)

    kpoints, weights, cell, pbc = get_kpoints_data(xmltree, schema_dict)

    assert kpoints is not None
    assert weights is not None
    assert isinstance(cell, np.ndarray)
    assert cell.shape == (3, 3)
    assert isinstance(pbc, list)
    assert len(pbc) == 3


@pytest.mark.parametrize('inpxmlfilepath', inpxmlfilelist)
def test_get_nkpts(load_inpxml, inpxmlfilepath):
    """
    Test that get_nkpts works for all input files
    """
    from masci_tools.util.xml.xml_getters import get_nkpts

    xmltree, schema_dict = load_inpxml(inpxmlfilepath)

    nkpts = get_nkpts(xmltree, schema_dict)

    assert isinstance(nkpts, int)
    assert nkpts != 0


def test_get_cell_film(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_cell
    from masci_tools.io.common_functions import convert_to_pystd

    xmltree, schema_dict = load_inpxml(TEST_FILM_INPXML_PATH)

    cell, pbc = get_cell(xmltree, schema_dict)

    data_regression.check({'cell': convert_to_pystd(cell), 'pbc': pbc})


def test_get_cell_bulk(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_cell
    from masci_tools.io.common_functions import convert_to_pystd

    xmltree, schema_dict = load_inpxml(TEST_BULK_INPXML_PATH)

    cell, pbc = get_cell(xmltree, schema_dict)

    data_regression.check({'cell': convert_to_pystd(cell), 'pbc': pbc})


def test_get_structure_film(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_structure_data
    from masci_tools.io.common_functions import convert_to_pystd

    xmltree, schema_dict = load_inpxml(TEST_FILM_INPXML_PATH)

    atoms, cell, pbc = get_structure_data(xmltree, schema_dict)

    data_regression.check({'atoms': convert_to_pystd(atoms), 'cell': convert_to_pystd(cell), 'pbc': pbc})


def test_get_structure_bulk(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_structure_data
    from masci_tools.io.common_functions import convert_to_pystd

    xmltree, schema_dict = load_inpxml(TEST_BULK_INPXML_PATH)

    atoms, cell, pbc = get_structure_data(xmltree, schema_dict)

    data_regression.check({'atoms': convert_to_pystd(atoms), 'cell': convert_to_pystd(cell), 'pbc': pbc})


def test_fleur_modes_film(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_fleur_modes

    xmltree, schema_dict = load_inpxml(TEST_FILM_INPXML_PATH)

    modes = get_fleur_modes(xmltree, schema_dict)

    data_regression.check(modes)


def test_fleur_modes_bulk(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_fleur_modes

    xmltree, schema_dict = load_inpxml(TEST_BULK_INPXML_PATH)

    modes = get_fleur_modes(xmltree, schema_dict)

    data_regression.check(modes)


def test_parameter_film(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_parameter_data

    xmltree, schema_dict = load_inpxml(TEST_FILM_INPXML_PATH)

    para = get_parameter_data(xmltree, schema_dict)

    data_regression.check(para)


def test_parameter_bulk(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_parameter_data

    xmltree, schema_dict = load_inpxml(TEST_BULK_INPXML_PATH)

    para = get_parameter_data(xmltree, schema_dict)

    data_regression.check(para)


def test_kpoints_film(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_kpoints_data
    from masci_tools.io.common_functions import convert_to_pystd

    xmltree, schema_dict = load_inpxml(TEST_FILM_INPXML_PATH)

    kpoints, weights, cell, pbc = get_kpoints_data(xmltree, schema_dict)

    data_regression.check({'kpoints': kpoints, 'weights': weights, 'cell': convert_to_pystd(cell), 'pbc': pbc})


def test_kpoints_bulk(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_kpoints_data
    from masci_tools.io.common_functions import convert_to_pystd

    xmltree, schema_dict = load_inpxml(TEST_BULK_INPXML_PATH)

    kpoints, weights, cell, pbc = get_kpoints_data(xmltree, schema_dict)

    data_regression.check({'kpoints': kpoints, 'weights': weights, 'cell': convert_to_pystd(cell), 'pbc': pbc})


def test_kpoints_single_kpoint(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_kpoints_data
    from masci_tools.io.common_functions import convert_to_pystd

    xmltree, schema_dict = load_inpxml(TEST_SINGLE_KPOINT_PATH)

    kpoints, weights, cell, pbc = get_kpoints_data(xmltree, schema_dict)

    data_regression.check({'kpoints': kpoints, 'weights': weights, 'cell': convert_to_pystd(cell), 'pbc': pbc})


def test_kpoints_multiple_sets(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_kpoints_data
    from masci_tools.io.common_functions import convert_to_pystd

    xmltree, schema_dict = load_inpxml(TEST_MULTIPLE_KPOINT_SETS_PATH)

    kpoints, weights, cell, pbc = get_kpoints_data(xmltree, schema_dict)

    data_regression.check({'kpoints': kpoints, 'weights': weights, 'cell': convert_to_pystd(cell), 'pbc': pbc})


def test_kpoints_multiple_sets_selection(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_kpoints_data
    from masci_tools.io.common_functions import convert_to_pystd

    xmltree, schema_dict = load_inpxml(TEST_MULTIPLE_KPOINT_SETS_PATH)

    kpoints, weights, cell, pbc = get_kpoints_data(xmltree, schema_dict, name='default')

    data_regression.check({'kpoints': kpoints, 'weights': weights, 'cell': convert_to_pystd(cell), 'pbc': pbc})


def test_kpoints_max4(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_kpoints_data
    from masci_tools.io.common_functions import convert_to_pystd

    xmltree, schema_dict = load_inpxml(TEST_MAX4_INPXML_PATH)

    kpoints, weights, cell, pbc = get_kpoints_data(xmltree, schema_dict)

    data_regression.check({'kpoints': kpoints, 'weights': weights, 'cell': convert_to_pystd(cell), 'pbc': pbc})


def test_parameter_max4(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_parameter_data

    xmltree, schema_dict = load_inpxml(TEST_MAX4_INPXML_PATH)

    para = get_parameter_data(xmltree, schema_dict)

    data_regression.check(para)


def test_fleur_modes_max4(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_fleur_modes

    xmltree, schema_dict = load_inpxml(TEST_MAX4_INPXML_PATH)

    modes = get_fleur_modes(xmltree, schema_dict)

    data_regression.check(modes)


def test_get_structure_max4(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_structure_data
    from masci_tools.io.common_functions import convert_to_pystd

    xmltree, schema_dict = load_inpxml(TEST_MAX4_INPXML_PATH)

    atoms, cell, pbc = get_structure_data(xmltree, schema_dict)

    data_regression.check({'atoms': convert_to_pystd(atoms), 'cell': convert_to_pystd(cell), 'pbc': pbc})


def test_get_cell_max4(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_cell
    from masci_tools.io.common_functions import convert_to_pystd

    xmltree, schema_dict = load_inpxml(TEST_MAX4_INPXML_PATH)

    cell, pbc = get_cell(xmltree, schema_dict)

    data_regression.check({'cell': convert_to_pystd(cell), 'pbc': pbc})


def test_get_nkpts_single(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_nkpts

    xmltree, schema_dict = load_inpxml(TEST_SINGLE_KPOINT_PATH)

    nkpts = get_nkpts(xmltree, schema_dict)

    assert isinstance(nkpts, int)
    assert nkpts == 1


def test_get_nkpts_multiple(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_nkpts

    xmltree, schema_dict = load_inpxml(TEST_MULTIPLE_KPOINT_SETS_PATH)

    nkpts = get_nkpts(xmltree, schema_dict)

    assert isinstance(nkpts, int)
    assert nkpts == 20


def test_get_nkpts_max4(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_nkpts

    xmltree, schema_dict = load_inpxml(TEST_MAX4_INPXML_PATH)

    nkpts = get_nkpts(xmltree, schema_dict)

    assert isinstance(nkpts, int)
    assert nkpts == 1


def test_get_nkpts_max4_altkpoint(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_nkpts
    from masci_tools.util.xml.xml_setters_names import set_inpchanges

    xmltree, schema_dict = load_inpxml(TEST_MAX4_INPXML_PATH)

    #Activate band calculations
    xmltree = set_inpchanges(xmltree, schema_dict, {'band': True})

    with pytest.warns(UserWarning):
        nkpts = get_nkpts(xmltree, schema_dict)

    assert isinstance(nkpts, int)
    assert nkpts == 240


def test_get_relaxation_information_inpxml(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_relaxation_information

    xmltree, schema_dict = load_inpxml(TEST_RELAX_INPXML_PATH)

    relax_dict = get_relaxation_information(xmltree, schema_dict)

    data_regression.check(relax_dict)


def test_get_relaxation_information_outxml(load_outxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_relaxation_information

    xmltree, schema_dict = load_outxml(TEST_RELAX_OUTXML_PATH)

    relax_dict = get_relaxation_information(xmltree, schema_dict)

    data_regression.check(relax_dict)


def test_get_relaxation_information_relaxxml(load_inpxml, data_regression):

    from masci_tools.util.xml.xml_getters import get_relaxation_information
    from lxml import etree

    xmltree, schema_dict = load_inpxml(TEST_RELAX_INPXML_PATH)  #schema_dict has to come from somewhere
    xmltree = etree.parse(TEST_RELAX_RELAXXML_PATH)

    with pytest.warns(UserWarning, match='Cannot extract custom constants'):
        relax_dict = get_relaxation_information(xmltree, schema_dict)

    data_regression.check(relax_dict)
