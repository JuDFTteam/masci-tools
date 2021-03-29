# -*- coding: utf-8 -*-
"""Contains tests for the set_nmmpmat routine used for modifying the
   density matrix for LDA+U calculations."""
import os
import pytest
import numpy as np

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_INPXML_LDAU_PATH = os.path.join(FILE_PATH, 'files/fleur/Max-R5/GaAsMultiUForceXML/files/inp.xml')
TEST_NMMPMAT_PATH = os.path.join(FILE_PATH, 'files/fleur/input_nmmpmat.txt')


def test_set_nmmpmat_nofile(load_inpxml, file_regression):
    """Test setting of nmmpmat with no initial nmmpmat file given"""
    from masci_tools.util.xml.xml_setters_nmmpmat import set_nmmpmat

    xmltree, schema_dict = load_inpxml(TEST_INPXML_LDAU_PATH)

    nmmp_lines = None
    nmmp_lines = set_nmmpmat(xmltree,
                             nmmp_lines,
                             schema_dict,
                             species_name='Ga-1',
                             orbital=2,
                             spin=1,
                             state_occupations=[1, 2, 3, 4, 5])
    nmmp_lines = set_nmmpmat(xmltree,
                             nmmp_lines,
                             schema_dict,
                             'As-2',
                             orbital=1,
                             spin=1,
                             denmat=[[1, -2, 3], [4, -5, 6], [7, -8, 9]])

    file_regression.check(prepare_for_file_dump(nmmp_lines))


def test_set_nmmpmat_file(load_inpxml, file_regression):
    """Test setting of nmmpmat with initial nmmpmat file given"""
    from masci_tools.util.xml.xml_setters_nmmpmat import set_nmmpmat

    xmltree, schema_dict = load_inpxml(TEST_INPXML_LDAU_PATH)

    with open(TEST_NMMPMAT_PATH, mode='r') as nmmpfile:
        nmmp_lines = nmmpfile.read().split('\n')

    nmmp_lines = set_nmmpmat(xmltree,
                             nmmp_lines,
                             schema_dict,
                             species_name='Ga-1',
                             orbital=2,
                             spin=1,
                             state_occupations=[1, 2, 3, 4, 5])
    nmmp_lines = set_nmmpmat(xmltree,
                             nmmp_lines,
                             schema_dict,
                             'As-2',
                             orbital=1,
                             spin=1,
                             denmat=[[1, -2, 3], [4, -5, 6], [7, -8, 9]])

    file_regression.check(prepare_for_file_dump(nmmp_lines))


def test_set_nmmpmat_file_get_wigner_matrix(load_inpxml, file_regression):
    """Test get_wigner_matrix by calling set_nmmpmat_file with theta, or phi != None"""
    from masci_tools.util.xml.xml_setters_nmmpmat import set_nmmpmat

    xmltree, schema_dict = load_inpxml(TEST_INPXML_LDAU_PATH)

    nmmp_lines = None
    nmmp_lines = set_nmmpmat(xmltree,
                             nmmp_lines,
                             schema_dict,
                             species_name='Ga-1',
                             orbital=1,
                             spin=1,
                             state_occupations=[1, 0, 1],
                             theta=np.pi / 2.0)
    nmmp_lines = set_nmmpmat(xmltree,
                             nmmp_lines,
                             schema_dict,
                             'As-2',
                             orbital=1,
                             spin=1,
                             denmat=[[1, 0, 1], [0, 0, 0], [1, 0, 1]],
                             phi=np.pi / 4.0,
                             theta=np.pi / 2.0)

    file_regression.check(prepare_for_file_dump(nmmp_lines))


def test_rotate_nmmpmat(load_inpxml, file_regression):
    """Test get_wigner_matrix by calling set_nmmpmat_file with theta, or phi != None"""
    from masci_tools.util.xml.xml_setters_nmmpmat import set_nmmpmat, rotate_nmmpmat

    xmltree, schema_dict = load_inpxml(TEST_INPXML_LDAU_PATH)

    nmmp_lines = None
    nmmp_lines = set_nmmpmat(xmltree,
                             nmmp_lines,
                             schema_dict,
                             species_name='Ga-1',
                             orbital=1,
                             spin=1,
                             state_occupations=[1, 0, 1])
    nmmp_lines = set_nmmpmat(xmltree,
                             nmmp_lines,
                             schema_dict,
                             'As-2',
                             orbital=1,
                             spin=1,
                             denmat=[[1, 0, 1], [0, 0, 0], [1, 0, 1]])

    nmmp_lines = rotate_nmmpmat(xmltree, nmmp_lines, schema_dict, 'Ga-1', orbital=1, phi=0.0, theta=np.pi / 2.0)
    nmmp_lines = rotate_nmmpmat(xmltree, nmmp_lines, schema_dict, 'As-2', orbital=1, theta=np.pi / 2.0, phi=np.pi / 4.0)

    file_regression.check(prepare_for_file_dump(nmmp_lines))


def test_validate_nmmpmat(load_inpxml):
    """Test validation method of nmmpmat file together with inp.xml file"""
    from masci_tools.util.xml.xml_setters_nmmpmat import set_nmmpmat, validate_nmmpmat

    xmltree, schema_dict = load_inpxml(TEST_INPXML_LDAU_PATH)

    with open(TEST_NMMPMAT_PATH, mode='r') as nmmpfile:
        nmmp_lines_orig = nmmpfile.read().split('\n')

    validate_nmmpmat(xmltree, nmmp_lines_orig, schema_dict)  #should not raise

    #Test number of lines error
    nmmp_lines = nmmp_lines_orig.copy()
    nmmp_lines.append('0.0')
    with pytest.raises(ValueError):
        validate_nmmpmat(xmltree, nmmp_lines, schema_dict)
    nmmp_lines.remove('0.0')

    #Test invalid diagonal element error
    nmmp_lines = nmmp_lines_orig.copy()
    nmmp_lines = set_nmmpmat(xmltree,
                             nmmp_lines,
                             schema_dict,
                             species_name='Ga-1',
                             orbital=2,
                             spin=1,
                             state_occupations=[1, 2, 3, 4, 5])
    nmmp_lines = set_nmmpmat(xmltree,
                             nmmp_lines,
                             schema_dict,
                             'As-2',
                             orbital=1,
                             spin=1,
                             denmat=[[1, -2, 3], [4, -5, 6], [7, -8, 9]])
    with pytest.raises(ValueError):
        validate_nmmpmat(xmltree, nmmp_lines, schema_dict)

    #Test invalid outsied value error
    nmmp_lines = nmmp_lines_orig.copy()
    nmmp_lines[
        0] = '     0.0000000000000     9.0000000000000     0.0000000000000     0.0000000000000     0.0000000000000     0.0000000000000     0.0000000000000'

    with pytest.raises(ValueError):
        validate_nmmpmat(xmltree, nmmp_lines, schema_dict)


def prepare_for_file_dump(file_lines):
    """
    Join lines together with linebreaks and remove negative zeros
    """
    return '\n'.join([line.replace('-0.0000000000000', ' 0.0000000000000') for line in file_lines])
