# -*- coding: utf-8 -*-
"""
Test of the consistency the input schema dictionaries with the SchemaFiles in the same folder
"""
import pytest
import os
from masci_tools.io.parsers.fleur.fleur_schema import load_inpschema, create_inpschema_dict
from masci_tools.io.parsers.fleur.fleur_schema import load_outschema, create_outschema_dict

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

schema_directory = '../io/parsers/fleur/fleur_schema'

schema_versions = []
schema_paths = []
outschema_versions = []
outschema_paths = []
for root, dirs, files in os.walk(os.path.abspath(os.path.join(CURRENT_DIRECTORY, schema_directory))):
    for folder in dirs:
        if '0.' in folder:
            schema_versions.append(folder)
            schema_paths.append(os.path.join(root, folder))
            if int(folder.split('.')[1]) >= 33:
                outschema_versions.append(folder)
                outschema_paths.append(os.path.join(root, folder))


@pytest.mark.parametrize('schema_version,schema_path', zip(schema_versions, schema_paths))
def test_inpschema_dict(schema_version, schema_path):
    """
    Test the fleur_schema_parser_functions to make sure that they match the stored inputschema_dict
    """
    dict_created, created_version = create_inpschema_dict(schema_path, save_to_file=False)
    dict_stored = load_inpschema(schema_version, create=False)

    assert created_version == schema_version
    assert dict_created == dict_stored


@pytest.mark.parametrize('schema_version,schema_path', zip(outschema_versions, outschema_paths))
def test_outschema_dict(schema_version, schema_path):
    """
    Test the fleur_schema_parser_functions to make sure that they match the stored inputschema_dict
    """
    dict_created, created_version = create_outschema_dict(schema_path, save_to_file=False)
    dict_stored = load_outschema(schema_version, create=False)

    assert created_version == schema_version
    assert dict_created == dict_stored
