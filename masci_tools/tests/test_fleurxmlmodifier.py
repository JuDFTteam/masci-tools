# -*- coding: utf-8 -*-
"""
Test for the FleurXMLModifier calss
"""
import os
import pytest

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_INPXML_PATH = os.path.join(FILE_PATH, 'files/fleur/Max-R5/FePt_film_SSFT_LO/files/inp2.xml')
TEST_INPXML_LDAU_PATH = os.path.join(FILE_PATH, 'files/fleur/Max-R5/GaAsMultiUForceXML/files/inp.xml')
TEST_NMMPMAT_PATH = os.path.join(FILE_PATH, 'files/fleur/input_nmmpmat.txt')


def test_fleurxmlmodifier_facade_methods():
    """
    Make sure that adding all facade methods results in the right task list
    """
    from masci_tools.io.fleurxmlmodifier import FleurXMLModifier, ModifierTask

    fm = FleurXMLModifier()

    actions = fm.get_avail_actions()

    assert fm._tasks == []

    for action in actions.values():
        action('TEST_ARG', random_kwarg='TEST2')

    assert len(actions) == len(fm._tasks)

    for task, action in zip(fm._tasks, actions.values()):
        assert isinstance(task, ModifierTask)
        assert task.name == action.__name__
        assert task.args == ('TEST_ARG',)
        assert task.kwargs == {'random_kwarg': 'TEST2'}


def test_fleurxml_modifier_modify_xmlfile_simple():
    """Tests if fleurinp_modifier with various modifations on species"""
    from masci_tools.io.fleurxmlmodifier import FleurXMLModifier, ModifierTask

    fm = FleurXMLModifier()
    fm.set_inpchanges({'dos': True, 'Kmax': 3.9})
    fm.shift_value({'Kmax': 0.1}, 'rel')
    fm.shift_value_species_label('                 222', 'radius', 3, mode='abs')
    fm.set_species('all', {'mtSphere': {'radius': 3.333}})
    fm.xml_set_attrib_value_no_create('/fleurInput/calculationSetup/cutoffs', 'Gmax', '14.0')

    assert fm.changes() == [
        ModifierTask(name='set_inpchanges', args=({
            'dos': True,
            'Kmax': 3.9
        },), kwargs={}),
        ModifierTask(name='shift_value', args=({
            'Kmax': 0.1
        }, 'rel'), kwargs={}),
        ModifierTask(name='shift_value_species_label',
                     args=(
                         '                 222',
                         'radius',
                         3,
                     ),
                     kwargs={'mode': 'abs'}),
        ModifierTask(name='set_species', args=('all', {
            'mtSphere': {
                'radius': 3.333
            }
        }), kwargs={}),
        ModifierTask(name='xml_set_attrib_value_no_create',
                     args=(
                         '/fleurInput/calculationSetup/cutoffs',
                         'Gmax',
                         '14.0',
                     ),
                     kwargs={})
    ]

    #The underlying methods are tested in the specific tests for the setters
    #We only want to ensure that the procedure finishes without error
    xmltree = fm.modify_xmlfile(TEST_INPXML_PATH)

    assert xmltree is not None


def test_fleurxml_modifier_modify_xmlfile_undo():
    """Tests if fleurinp_modifier with various modifations on species"""
    from masci_tools.io.fleurxmlmodifier import FleurXMLModifier, ModifierTask

    fm = FleurXMLModifier()
    fm.set_inpchanges({'dos': True, 'Kmax': 3.9})
    fm.shift_value({'Kmax': 0.1}, 'rel')
    fm.shift_value_species_label('                 222', 'radius', 3, mode='abs')
    fm.set_species('all', {'mtSphere': {'radius': 3.333}})

    fm.undo()

    assert fm.changes() == [
        ModifierTask(name='set_inpchanges', args=({
            'dos': True,
            'Kmax': 3.9
        },), kwargs={}),
        ModifierTask(name='shift_value', args=({
            'Kmax': 0.1
        }, 'rel'), kwargs={}),
        ModifierTask(name='shift_value_species_label',
                     args=(
                         '                 222',
                         'radius',
                         3,
                     ),
                     kwargs={'mode': 'abs'})
    ]

    #The underlying methods are tested in the specific tests for the setters
    #We only want to ensure that the procedure finishes without error
    xmltree = fm.modify_xmlfile(TEST_INPXML_PATH)

    assert xmltree is not None


def test_fleurxml_modifier_modify_xmlfile_undo_revert_all():
    """Tests if fleurinp_modifier with various modifations on species"""
    from masci_tools.io.fleurxmlmodifier import FleurXMLModifier

    fm = FleurXMLModifier()
    fm.set_inpchanges({'dos': True, 'Kmax': 3.9})
    fm.shift_value({'Kmax': 0.1}, 'rel')
    fm.shift_value_species_label('                 222', 'radius', 3, mode='abs')
    fm.set_species('all', {'mtSphere': {'radius': 3.333}})

    fm.undo(revert_all=True)

    assert fm.changes() == []

    #The underlying methods are tested in the specific tests for the setters
    #We only want to ensure that the procedure finishes without error
    xmltree = fm.modify_xmlfile(TEST_INPXML_PATH)

    assert xmltree is not None


def test_fleurxmlmodifier_nmmpmat():
    """Tests if set_nmmpmat works on fleurinp modifier works, with right interface"""
    from masci_tools.io.fleurxmlmodifier import FleurXMLModifier

    fm = FleurXMLModifier()
    fm.set_nmmpmat('Ga-1', orbital=2, spin=1, state_occupations=[1, 2, 3, 4, 5])
    fm.set_nmmpmat('As-2', orbital=1, spin=1, denmat=[[1, -2, 3], [4, -5, 6], [7, -8, 9]])

    # Does not validate
    # Found invalid diagonal element for species Ga-1, spin 1 and l=2
    with pytest.raises(ValueError, match=r'Changes were not valid \(n_mmp_mat file is not compatible\)'):
        fm.modify_xmlfile(TEST_INPXML_LDAU_PATH)
    xmltree, nmmpmat = fm.modify_xmlfile(TEST_INPXML_LDAU_PATH, validate_changes=False)

    assert xmltree is not None
    assert nmmpmat is not None

    xmltree, nmmpmat = fm.modify_xmlfile(TEST_INPXML_LDAU_PATH,
                                         original_nmmp_file=TEST_NMMPMAT_PATH,
                                         validate_changes=False)

    assert xmltree is not None
    assert nmmpmat is not None
