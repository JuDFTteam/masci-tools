"""
Test for the FleurXMLModifier class
"""
import pytest
from masci_tools.io.fleurxmlmodifier import FleurXMLModifier, ModifierTask
from lxml import etree

TEST_INPXML_PATH = 'fleur/Max-R5/FePt_film_SSFT_LO/files/inp2.xml'
TEST_INPXML_LDAU_PATH = 'fleur/Max-R5/GaAsMultiUForceXML/files/inp.xml'
TEST_NMMPMAT_PATH = 'fleur/input_nmmpmat.txt'


def test_fleurxmlmodifier_facade_methods():
    """
    Make sure that adding all facade methods results in the right task list
    """
    from masci_tools.util.xml.collect_xml_setters import XPATH_SETTERS, SCHEMA_DICT_SETTERS, NMMPMAT_SETTERS

    fm = FleurXMLModifier(validate_signatures=False)

    actions = fm.get_avail_actions()

    assert len(fm._tasks) == 0  #pylint: disable=protected-access

    for action in actions.values():
        action('TEST_ARG', random_kwarg='TEST2')

    assert len(actions) == len(fm._tasks)  #pylint: disable=protected-access
    assert set(actions.keys()) == XPATH_SETTERS.keys() | SCHEMA_DICT_SETTERS.keys() | NMMPMAT_SETTERS.keys()

    for task, action in zip(fm._tasks, actions.values()):  #pylint: disable=protected-access
        assert isinstance(task, ModifierTask)
        assert task.name == action.__name__
        assert task.args == ('TEST_ARG',)
        assert task.kwargs == {'random_kwarg': 'TEST2'}


def test_fleurxmlmodifier_facade_methods_validation():
    """
    Make sure that adding all facade methods results in the right task list
    """

    fm = FleurXMLModifier()

    actions = fm.get_avail_actions()

    for name, action in actions.items():
        if name not in ('create_tag', 'delete_tag', 'delete_att'):  #Create tag actually accepts this
            #(since random_kwarg is packed into the kwargs of that function)
            with pytest.raises(TypeError):
                action('TEST_ARG', random_kwarg='TEST2')
        else:
            action('TEST_ARG', random_kwarg='TEST2')


def test_fleurxml_modifier_modify_xmlfile_simple(test_file):
    """Tests if fleurinp_modifier with various modifications on species"""

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
    xmltree, add_files = fm.modify_xmlfile(test_file(TEST_INPXML_PATH))

    assert xmltree is not None
    assert len(add_files) == 0


def test_fleurxml_modifier_modify_xmlfile_undo(test_file):
    """Tests if fleurinp_modifier with various modifications on species"""

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
    xmltree, add_files = fm.modify_xmlfile(test_file(TEST_INPXML_PATH))

    assert xmltree is not None
    assert len(add_files) == 0


def test_fleurxml_modifier_from_list(test_file):
    """Tests if fleurinp_modifier with various modifications on species"""

    task_list = [('set_inpchanges', {
        'changes': {
            'dos': True,
            'Kmax': 3.9
        }
    }), ('shift_value', {
        'changes': {
            'Kmax': 0.1
        },
        'mode': 'rel'
    }),
                 ('shift_value_species_label', {
                     'atom_label': '                 222',
                     'attribute_name': 'radius',
                     'number_to_add': 3,
                     'mode': 'abs'
                 }), ('set_kpointlist', {
                     'kpoints': [[0, 0, 0]],
                     'weights': [1]
                 }), ('set_species', {
                     'species_name': 'all',
                     'changes': {
                         'mtSphere': {
                             'radius': 3.333
                         }
                     }
                 })]

    fm = FleurXMLModifier.fromList(task_list)

    assert fm.changes() == [
        ModifierTask(name='set_inpchanges', args=(), kwargs={'changes': {
            'dos': True,
            'Kmax': 3.9
        }}),
        ModifierTask(name='shift_value', args=(), kwargs={
            'changes': {
                'Kmax': 0.1
            },
            'mode': 'rel'
        }),
        ModifierTask(name='shift_value_species_label',
                     args=(),
                     kwargs={
                         'atom_label': '                 222',
                         'attribute_name': 'radius',
                         'number_to_add': 3,
                         'mode': 'abs'
                     }),
        ModifierTask(name='set_kpointlist', args=(), kwargs={
            'kpoints': [[0, 0, 0]],
            'weights': [1]
        }),
        ModifierTask(name='set_species',
                     args=(),
                     kwargs={
                         'species_name': 'all',
                         'changes': {
                             'mtSphere': {
                                 'radius': 3.333
                             }
                         }
                     })
    ]

    #The underlying methods are tested in the specific tests for the setters
    #We only want to ensure that the procedure finishes without error
    xmltree, add_files = fm.modify_xmlfile(test_file(TEST_INPXML_PATH))

    assert xmltree is not None
    assert len(add_files) == 0


def test_fleurxml_modifier_task_list_construction():
    """Tests if fleurxmlmodifier can produce the task list"""

    fm = FleurXMLModifier()
    fm.set_inpchanges({'dos': True, 'Kmax': 3.9})
    fm.shift_value({'Kmax': 0.1}, 'rel')
    fm.shift_value_species_label('                 222', 'radius', 3, mode='abs')
    fm.set_species('all', {'mtSphere': {'radius': 3.333}})

    assert fm.task_list == [('set_inpchanges', {
        'changes': {
            'dos': True,
            'Kmax': 3.9
        }
    }), ('shift_value', {
        'changes': {
            'Kmax': 0.1
        },
        'mode': 'rel'
    }),
                            ('shift_value_species_label', {
                                'atom_label': '                 222',
                                'attribute_name': 'radius',
                                'number_to_add': 3,
                                'mode': 'abs'
                            }), ('set_species', {
                                'species_name': 'all',
                                'changes': {
                                    'mtSphere': {
                                        'radius': 3.333
                                    }
                                }
                            })]


def test_fleurxml_modifier_task_kwargs_handling():
    """Tests if fleurxmlmodifier can produce the task list if the XML modifier function contains
       an explicit kwargs
    """

    fm = FleurXMLModifier()
    fm.delete_tag('lo', contains='species')

    assert fm.task_list == [('delete_tag', {'tag_name': 'lo', 'contains': 'species'})]


@pytest.mark.parametrize('name, kwargs, expected_task', [
    ('set_inpchanges', {
        'change_dict': {
            'dos': True,
            'Kmax': 3.9
        }
    }, ModifierTask(name='set_inpchanges', kwargs={'changes': {
        'dos': True,
        'Kmax': 3.9
    }})),
    ('shift_value', {
        'change_dict': {
            'Kmax': 0.1
        },
        'mode': 'rel'
    }, ModifierTask(name='shift_value', kwargs={
        'changes': {
            'Kmax': 0.1
        },
        'mode': 'rel'
    })),
    ('set_species', {
        'species_name': 'all',
        'attributedict': {
            'element': 'T'
        }
    }, ModifierTask(name='set_species', kwargs={
        'species_name': 'all',
        'changes': {
            'element': 'T'
        }
    })),
    ('set_species_label', {
        'atom_label': 'all',
        'attributedict': {
            'element': 'T'
        }
    }, ModifierTask(name='set_species_label', kwargs={
        'atom_label': 'all',
        'changes': {
            'element': 'T'
        }
    })),
    ('shift_value_species_label', {
        'atom_label': '                 222',
        'attributename': 'radius',
        'value_given': 3,
        'mode': 'abs'
    },
     ModifierTask(name='shift_value_species_label',
                  kwargs={
                      'atom_label': '                 222',
                      'attribute_name': 'radius',
                      'number_to_add': 3,
                      'mode': 'abs'
                  })),
    ('set_atomgroup', {
        'species': 'all',
        'attributedict': {
            'species': 'T'
        },
        'create': True,
    }, ModifierTask(name='set_atomgroup', kwargs={
        'species': 'all',
        'changes': {
            'species': 'T'
        },
    })),
    ('set_atomgroup_label', {
        'atom_label': '                 222',
        'attributedict': {
            'species': 'T'
        },
        'create': True,
    },
     ModifierTask(name='set_atomgroup_label',
                  kwargs={
                      'atom_label': '                 222',
                      'changes': {
                          'species': 'T'
                      },
                  })),
    ('delete_att', {
        'attrib_name': 'test'
    }, ModifierTask(name='delete_att', kwargs={'name': 'test'})),
    ('replace_tag', {
        'tag_name': 'test',
        'newelement': 'NEW'
    }, ModifierTask(name='replace_tag', kwargs={
        'tag_name': 'test',
        'element': 'NEW'
    })),
    ('set_attrib_value', {
        'attributename': 'test',
        'attribv': 'NEW'
    }, ModifierTask(name='set_attrib_value', kwargs={
        'name': 'test',
        'value': 'NEW'
    })),
    ('set_first_attrib_value', {
        'attributename': 'test',
        'attribv': 'NEW'
    }, ModifierTask(name='set_first_attrib_value', kwargs={
        'name': 'test',
        'value': 'NEW'
    })),
    ('add_number_to_attrib', {
        'attributename': 'test',
        'add_number': 1.0
    }, ModifierTask(name='add_number_to_attrib', kwargs={
        'name': 'test',
        'number_to_add': 1.0
    })),
    ('add_number_to_first_attrib', {
        'attributename': 'test',
        'add_number': 1.0
    }, ModifierTask(name='add_number_to_first_attrib', kwargs={
        'name': 'test',
        'number_to_add': 1.0
    })),
    ('xml_replace_tag', {
        'xpath': './test',
        'newelement': 'NEW'
    }, ModifierTask(name='xml_replace_tag', kwargs={
        'xpath': './test',
        'element': 'NEW'
    })),
    ('xml_delete_att', {
        'xpath': './test',
        'attributename': 'test'
    }, ModifierTask(name='xml_delete_att', kwargs={
        'xpath': './test',
        'name': 'test'
    })),
    ('xml_set_attrib_value_no_create', {
        'xpath': './test',
        'attributename': 'test',
        'attribv': 'NEW'
    }, ModifierTask(name='xml_set_attrib_value_no_create', kwargs={
        'xpath': './test',
        'name': 'test',
        'value': 'NEW'
    })),
])
def test_fleurxml_modifier_deprecated_arguments(name, kwargs, expected_task):
    """Test the various deprecations in the fleurxmlmodifier"""

    fm = FleurXMLModifier()

    action = fm.get_avail_actions()[name]
    with pytest.deprecated_call():
        action(**kwargs)
    assert fm.changes() == [expected_task]
    assert fm.task_list == [(name, expected_task.kwargs)]


def test_fleurxml_modifier_modify_xmlfile_undo_revert_all(test_file):
    """Tests if fleurinp_modifier with various modifications on species"""

    fm = FleurXMLModifier()
    fm.set_inpchanges({'dos': True, 'Kmax': 3.9})
    fm.shift_value({'Kmax': 0.1}, 'rel')
    fm.shift_value_species_label('                 222', 'radius', 3, mode='abs')
    fm.set_species('all', {'mtSphere': {'radius': 3.333}})

    fm.undo(revert_all=True)

    assert len(fm.changes()) == 0

    #The underlying methods are tested in the specific tests for the setters
    #We only want to ensure that the procedure finishes without error
    xmltree, add_files = fm.modify_xmlfile(test_file(TEST_INPXML_PATH))

    assert xmltree is not None
    assert len(add_files) == 0


def test_fleurxmlmodifier_nmmpmat(test_file):
    """Tests if set_nmmpmat works on fleurinp modifier works, with right interface"""

    fm = FleurXMLModifier()
    fm.set_nmmpmat('Ga-1', orbital=2, spin=1, state_occupations=[1, 2, 3, 4, 5])
    fm.set_nmmpmat('As-2', orbital=1, spin=1, denmat=[[1, -2, 3], [4, -5, 6], [7, -8, 9]])

    # Does not validate
    # Found invalid diagonal element for species Ga-1, spin 1 and l=2
    with pytest.raises(ValueError, match=r'Changes were not valid \(n_mmp_mat file is not compatible\)'):
        fm.modify_xmlfile(test_file(TEST_INPXML_LDAU_PATH))
    xmltree, add_files = fm.modify_xmlfile(test_file(TEST_INPXML_LDAU_PATH), validate_changes=False)

    assert xmltree is not None
    assert add_files['n_mmp_mat'] is not None

    xmltree, add_files = fm.modify_xmlfile(test_file(TEST_INPXML_LDAU_PATH),
                                           original_nmmp_file=test_file(TEST_NMMPMAT_PATH),
                                           validate_changes=False)

    assert xmltree is not None
    assert add_files['n_mmp_mat'] is not None


def test_fleurxmlmodifier_deprecated_validate():
    """Check that the deprecated _validate_signature is working correctly"""
    #pylint: disable=protected-access

    fm = FleurXMLModifier()
    with pytest.deprecated_call():
        fm._validate_signature('delete_att', 'test')

    with pytest.deprecated_call():
        with pytest.raises(TypeError):
            fm._validate_signature('delete_att', non_existent_arg='test')


def test_fleurxmlmodifier_included_files(file_regression, test_file):
    """Tests if fleurinp_modifier with various other modifications methods,
    the detailed tests for method functionality is tested elsewhere."""

    fm = FleurXMLModifier()
    #Modify main inp.xml file
    fm.set_inpchanges({'dos': True, 'Kmax': 3.9})
    fm.shift_value({'Kmax': 0.1}, 'rel')

    #Modify included xml files
    fm.delete_tag('symmetryOperations')
    fm.create_tag('symmetryOperations')
    fm.create_tag('kPointList')
    fm.create_tag('kPoint', occurrences=0)
    fm.set_attrib_value('name', 'TEST', contains='kPointList', occurrences=0)
    fm.set_text('kPoint', [0.0, 0.0, 0.0],
                complex_xpath="/fleurInput/cell/bzIntegration/kPointLists/kPointList[@name='TEST']/kPoint")

    xmltree, add_files = fm.modify_xmlfile(test_file('fleur/test_clear.xml'), validate_changes=False)

    assert len(add_files) == 0
    file_regression.check(etree.tostring(xmltree, encoding='unicode', pretty_print=True), extension='.xml')
