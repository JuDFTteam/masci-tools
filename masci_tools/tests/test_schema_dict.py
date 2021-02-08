# -*- coding: utf-8 -*-
"""
Test of the consistency the input schema dictionaries with the SchemaFiles in the same folder
"""
import pytest
import os
from masci_tools.io.parsers.fleur.fleur_schema import load_inpschema, create_inpschema_dict
from masci_tools.io.parsers.fleur.fleur_schema import load_outschema, create_outschema_dict

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = '../io/parsers/fleur/fleur_schema'

#Collect all schemas from the folder
schema_versions = {'inp': [], 'out': []}
schema_paths = {'inp': [], 'out': []}
for root, dirs, files in os.walk(os.path.abspath(os.path.join(CURRENT_DIR, SCHEMA_DIR))):
    for folder in dirs:
        if '0.' in folder:
            schema_versions['inp'].append(folder)
            schema_paths['inp'].append(os.path.join(root, folder))
            if int(folder.split('.')[1]) >= 33 or folder == '0.31':
                schema_versions['out'].append(folder)
                schema_paths['out'].append(os.path.join(root, folder))


@pytest.mark.parametrize('schema_version,schema_path', zip(schema_versions['inp'], schema_paths['inp']))
def test_inpschema_dict(schema_version, schema_path):
    """
    Test the fleur_schema_parser_functions to make sure that they match the stored inputschema_dict
    """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict

    CASE_INSENSITIVE_KEYS = {'attrib_types', 'tag_paths', 'unique_attribs', 'unique_path_attribs', 'other_attribs'}

    dict_created, created_version = create_inpschema_dict(schema_path, save_to_file=False)
    dict_stored = load_inpschema(schema_version, create=False)

    assert created_version == schema_version
    assert dict_created == dict_stored
    assert all([isinstance(dict_created[key], CaseInsensitiveDict) for key in CASE_INSENSITIVE_KEYS])
    assert all([isinstance(dict_stored[key], CaseInsensitiveDict) for key in CASE_INSENSITIVE_KEYS])


@pytest.mark.parametrize('schema_version,schema_path', zip(schema_versions['out'], schema_paths['out']))
def test_outschema_dict(schema_version, schema_path):
    """
    Test the fleur_schema_parser_functions to make sure that they match the stored inputschema_dict
    """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict

    CASE_INSENSITIVE_KEYS = {
        'attrib_types', 'tag_paths', 'unique_attribs', 'unique_path_attribs', 'other_attribs', 'iteration_tag_paths',
        'iteration_unique_attribs', 'iteration_unique_path_attribs', 'iteration_other_attribs'
    }

    dict_created, created_version = create_outschema_dict(schema_path, save_to_file=False)
    dict_stored = load_outschema(schema_version, create=False)

    assert created_version == schema_version
    assert dict_created == dict_stored
    assert all([isinstance(dict_created[key], CaseInsensitiveDict) for key in CASE_INSENSITIVE_KEYS])
    assert all([isinstance(dict_stored[key], CaseInsensitiveDict) for key in CASE_INSENSITIVE_KEYS])
