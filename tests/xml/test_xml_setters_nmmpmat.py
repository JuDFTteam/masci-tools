"""Contains tests for the set_nmmpmat routine used for modifying the
   density matrix for LDA+U calculations."""

import pytest
import numpy as np

TEST_INPXML_LDAU_PATH = 'fleur/Max-R5/GaAsMultiUForceXML/files/inp.xml'
TEST_NMMPMAT_PATH = 'fleur/input_nmmpmat.txt'


def test_set_nmmpmat_nofile(load_inpxml, file_regression):
    """Test setting of nmmpmat with no initial nmmpmat file given"""
    from masci_tools.util.xml.xml_setters_nmmpmat import set_nmmpmat

    xmltree, schema_dict = load_inpxml(TEST_INPXML_LDAU_PATH, absolute=False)

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


def test_set_nmmpmat_file(load_inpxml, file_regression, test_file):
    """Test setting of nmmpmat with initial nmmpmat file given"""
    from masci_tools.util.xml.xml_setters_nmmpmat import set_nmmpmat

    xmltree, schema_dict = load_inpxml(TEST_INPXML_LDAU_PATH, absolute=False)

    with open(test_file(TEST_NMMPMAT_PATH), encoding='utf-8') as nmmpfile:
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

    xmltree, schema_dict = load_inpxml(TEST_INPXML_LDAU_PATH, absolute=False)

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

    xmltree, schema_dict = load_inpxml(TEST_INPXML_LDAU_PATH, absolute=False)

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


def test_rotate_nmmpmat_inverse(load_inpxml, file_regression):
    """Test get_wigner_matrix by calling set_nmmpmat_file with theta, or phi != None"""
    from masci_tools.util.xml.xml_setters_nmmpmat import set_nmmpmat, rotate_nmmpmat

    xmltree, schema_dict = load_inpxml(TEST_INPXML_LDAU_PATH, absolute=False)

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

    nmmp_lines = rotate_nmmpmat(xmltree,
                                nmmp_lines,
                                schema_dict,
                                'Ga-1',
                                orbital=1,
                                phi=0.0,
                                theta=np.pi / 2.0,
                                inverse=True)
    nmmp_lines = rotate_nmmpmat(xmltree,
                                nmmp_lines,
                                schema_dict,
                                'As-2',
                                orbital=1,
                                theta=np.pi / 2.0,
                                phi=np.pi / 4.0,
                                inverse=True)

    file_regression.check(prepare_for_file_dump(nmmp_lines))


def test_rotate_nmmpmat_all(load_inpxml, file_regression):
    """Test rotate_nmmpmat for all blocks with the same angle"""
    from masci_tools.util.xml.xml_setters_nmmpmat import set_nmmpmat, rotate_nmmpmat

    xmltree, schema_dict = load_inpxml(TEST_INPXML_LDAU_PATH, absolute=False)

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

    nmmp_lines = rotate_nmmpmat(xmltree,
                                nmmp_lines,
                                schema_dict,
                                'all',
                                orbital='all',
                                phi=np.pi / 4.0,
                                theta=np.pi / 2.0,
                                inverse=True)

    file_regression.check(prepare_for_file_dump(nmmp_lines))


def test_align_to_sqa_secvar_soc(load_inpxml, file_regression):
    """Test get_wigner_matrix by calling set_nmmpmat_file with theta, or phi != None"""
    from masci_tools.util.xml.xml_setters_nmmpmat import set_nmmpmat, align_nmmpmat_to_sqa
    from masci_tools.util.xml.xml_setters_names import set_inpchanges

    xmltree, schema_dict = load_inpxml(TEST_INPXML_LDAU_PATH, absolute=False)

    # Set up rotated SQA with second variation SOC
    # (we use the mathematical expressions to not loose accuracy when comparing with the explicit rotation)
    set_inpchanges(xmltree,
                   schema_dict, {
                       'l_soc': True,
                       'theta': 'Pi/2',
                       'phi': 'Pi/4'
                   },
                   path_spec={
                       'theta': {
                           'contains': 'soc'
                       },
                       'phi': {
                           'contains': 'soc'
                       }
                   })

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

    nmmp_lines = align_nmmpmat_to_sqa(xmltree, nmmp_lines, schema_dict)

    #This should rotate the same way as the test_rotate_nmmpmat_all test
    file_regression.check(prepare_for_file_dump(nmmp_lines), basename='test_rotate_nmmpmat_all')


def test_align_to_sqa_noco(load_inpxml, file_regression):
    """Test get_wigner_matrix by calling set_nmmpmat_file with theta, or phi != None"""
    from masci_tools.util.xml.xml_setters_nmmpmat import set_nmmpmat, align_nmmpmat_to_sqa
    from masci_tools.util.xml.xml_setters_names import set_inpchanges, set_atomgroup

    xmltree, schema_dict = load_inpxml(TEST_INPXML_LDAU_PATH, absolute=False)

    # Set up rotated SQA with second variation SOC (with weird values to make sure they are not used)
    set_inpchanges(xmltree,
                   schema_dict, {
                       'l_noco': True,
                       'l_soc': True,
                       'theta': -1.0,
                       'phi': 1.33
                   },
                   path_spec={
                       'theta': {
                           'contains': 'soc'
                       },
                       'phi': {
                           'contains': 'soc'
                       }
                   })

    #Set up rotated SQA for noco
    # (we use the mathematical expressions to not loose accuracy when comparing with the explicit rotation)
    set_atomgroup(xmltree, schema_dict, {'nocoparams': {'alpha': 0.0, 'beta': 'Pi/2'}}, species='Ga-1')
    set_atomgroup(xmltree, schema_dict, {'nocoparams': {'alpha': 'Pi/4', 'beta': 'Pi/2'}}, species='As-2')

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

    nmmp_lines = align_nmmpmat_to_sqa(xmltree, nmmp_lines, schema_dict)

    #This should rotate the same way as the test_rotate_nmmpmat_inverse test
    file_regression.check(prepare_for_file_dump(nmmp_lines), basename='test_rotate_nmmpmat_inverse')


def test_set_nmmpmat_orbital_occupations(load_inpxml, file_regression):
    """Test setting of nmmpmat with no initial nmmpmat file given"""
    from masci_tools.util.xml.xml_setters_nmmpmat import set_nmmpmat

    xmltree, schema_dict = load_inpxml(TEST_INPXML_LDAU_PATH, absolute=False)

    nmmp_lines = None
    nmmp_lines = set_nmmpmat(xmltree,
                             nmmp_lines,
                             schema_dict,
                             species_name='Ga-1',
                             orbital=2,
                             spin=1,
                             orbital_occupations=[1, 2, 3, 4, 5])
    nmmp_lines = set_nmmpmat(xmltree,
                             nmmp_lines,
                             schema_dict,
                             'As-2',
                             orbital=1,
                             spin=1,
                             denmat=[[1, -2, 3], [4, -5, 6], [7, -8, 9]])

    file_regression.check(prepare_for_file_dump(nmmp_lines))


def test_validate_nmmpmat(load_inpxml, test_file):
    """Test validation method of nmmpmat file together with inp.xml file"""
    from masci_tools.util.xml.xml_setters_nmmpmat import set_nmmpmat, validate_nmmpmat

    xmltree, schema_dict = load_inpxml(TEST_INPXML_LDAU_PATH, absolute=False)

    with open(test_file(TEST_NMMPMAT_PATH), encoding='utf-8') as nmmpfile:
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


def test_validate_mmpmat_issue134(load_inpxml, test_file):
    """
    Test for the bug reported in
    https://github.com/JuDFTteam/masci-tools/issues/134
    """
    from masci_tools.util.xml.xml_setters_nmmpmat import validate_nmmpmat

    xmltree, schema_dict = load_inpxml('fleur/issue134_files/inp.xml', absolute=False)

    with open(test_file('fleur/issue134_files/input_nmmpmat.txt'), encoding='utf-8') as nmmpfile:
        nmmp_lines = nmmpfile.read().split('\n')

    validate_nmmpmat(xmltree, nmmp_lines, schema_dict)  #should not raise


def prepare_for_file_dump(file_lines):
    """
    Join lines together with linebreaks and remove negative zeros
    """
    return '\n'.join([line.replace('-0.0000000000000', ' 0.0000000000000') for line in file_lines])
