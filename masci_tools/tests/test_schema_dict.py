# -*- coding: utf-8 -*-
"""
Test of the consistency the input schema dictionaries with the SchemaFiles in the same folder
"""
import pytest
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = '../io/parsers/fleur/fleur_schema'

#Collect all schemas from the folder
schema_versions = {'inp': [], 'out': []}
for root, dirs, files in os.walk(os.path.abspath(os.path.join(CURRENT_DIR, SCHEMA_DIR))):
    for folder in dirs:
        if '0.' in folder:
            schema_versions['inp'].append(folder)
            if int(folder.split('.')[1]) >= 33 or folder == '0.31':
                schema_versions['out'].append(folder)


@pytest.mark.parametrize('schema_version', schema_versions['inp'])
def test_inpschema_dict(data_regression,schema_version):
    """
    Test the produced inputschema dicts
    """
    from masci_tools.io.parsers.fleur.fleur_schema import InputSchemaDict

    inputschema = InputSchemaDict.fromVersion(version=schema_version)

    data_regression.check(clean_for_reg_dump(inputschema.get_unlocked()))


@pytest.mark.parametrize('inp_version', schema_versions['inp'])
@pytest.mark.parametrize('out_version', schema_versions['out'])
def test_outschema_dict(data_regression,inp_version, out_version):
    """
    Test the fleur_schema_parser_functions to make sure that they match the stored inputschema_dict
    """
    from masci_tools.io.parsers.fleur.fleur_schema import OutputSchemaDict

    outputschema = OutputSchemaDict.fromVersion(version=out_version, inp_version=inp_version)

    data_regression.check(clean_for_reg_dump(outputschema.get_unlocked()))



def clean_for_reg_dump(dict_to_clean):
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveFrozenSet

    for key, val in dict_to_clean.items():
        if isinstance(val, CaseInsensitiveFrozenSet):
            dict_to_clean[key] = set(val)
        elif isinstance(val, dict):
            dict_to_clean[key] = clean_for_reg_dump(val)

    return dict_to_clean
