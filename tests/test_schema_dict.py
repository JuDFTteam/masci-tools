# -*- coding: utf-8 -*-
"""
Test of the consistency the input schema dictionaries with the SchemaFiles in the same folder
"""
import pytest
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = '../masci_tools/io/parsers/fleur/fleur_schema'

#Collect all schemas from the folder
schema_versions = {'inp': [], 'out': []}
for root, dirs, files in os.walk(os.path.abspath(os.path.join(CURRENT_DIR, SCHEMA_DIR))):
    for folder in dirs:
        if '0.' in folder:
            schema_versions['inp'].append(folder)
            if int(folder.split('.')[1]) >= 33 or folder in ('0.31', '0.30', '0.29'):
                schema_versions['out'].append(folder)


def test_inpschema_dict_structure():
    """
    Test the types of the keys in the inpschemadict
    """
    from masci_tools.io.parsers.fleur.fleur_schema import InputSchemaDict
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict, CaseInsensitiveFrozenSet
    from masci_tools.util.lockable_containers import LockableDict, LockableList

    inputschema = InputSchemaDict.fromVersion('0.34')

    EXPECTED_TYPES = {
        'tag_paths': CaseInsensitiveDict,
        'unique_attribs': CaseInsensitiveDict,
        'unique_path_attribs': CaseInsensitiveDict,
        'other_attribs': CaseInsensitiveDict,
        'attrib_types': CaseInsensitiveDict,
        'text_types': CaseInsensitiveDict,
        'text_tags': CaseInsensitiveFrozenSet,
        '_basic_types': LockableDict,
        'root_tag': str,
        'inp_version': str,
        'omitt_contained_tags': LockableList,
        'tag_info': LockableDict
    }

    for key, val in inputschema.items():
        assert isinstance(val, EXPECTED_TYPES[key])
        if EXPECTED_TYPES[key] != str:
            if not isinstance(val, CaseInsensitiveFrozenSet):
                assert val._locked
            if EXPECTED_TYPES[key] != CaseInsensitiveDict:
                assert not isinstance(val,
                                      CaseInsensitiveDict)  #since CaseInsensitiveDict is a subclass of LockableDict


def test_outschema_dict_structure():
    """
    Test the types of the keys in the inpschemadict
    """
    from masci_tools.io.parsers.fleur.fleur_schema import OutputSchemaDict
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict, CaseInsensitiveFrozenSet
    from masci_tools.util.lockable_containers import LockableDict, LockableList

    outputschema = OutputSchemaDict.fromVersion('0.34')

    EXPECTED_TYPES = {
        'tag_paths': CaseInsensitiveDict,
        'unique_attribs': CaseInsensitiveDict,
        'unique_path_attribs': CaseInsensitiveDict,
        'other_attribs': CaseInsensitiveDict,
        'iteration_tag_paths': CaseInsensitiveDict,
        'iteration_unique_attribs': CaseInsensitiveDict,
        'iteration_unique_path_attribs': CaseInsensitiveDict,
        'iteration_other_attribs': CaseInsensitiveDict,
        'attrib_types': CaseInsensitiveDict,
        'text_types': CaseInsensitiveDict,
        'text_tags': CaseInsensitiveFrozenSet,
        '_basic_types': LockableDict,
        '_input_basic_types': LockableDict,
        'root_tag': str,
        'input_tag': str,
        'out_version': str,
        'inp_version': str,
        'omitt_contained_tags': LockableList,
        'tag_info': LockableDict,
        'iteration_tag_info': LockableDict
    }

    for key, val in outputschema.items():
        assert isinstance(val, EXPECTED_TYPES[key])
        if EXPECTED_TYPES[key] != str:
            if not isinstance(val, CaseInsensitiveFrozenSet):
                assert val._locked
            if EXPECTED_TYPES[key] != CaseInsensitiveDict:
                assert not isinstance(val,
                                      CaseInsensitiveDict)  #since CaseInsensitiveDict is a subclass of LockableDict


@pytest.mark.parametrize('schema_version', schema_versions['inp'])
def test_inpschema_dict(data_regression, schema_version):
    """
    Test the produced inputschema dicts
    """
    from masci_tools.io.parsers.fleur.fleur_schema import InputSchemaDict

    inputschema = InputSchemaDict.fromVersion(version=schema_version)

    data_regression.check(clean_for_reg_dump(inputschema.get_unlocked()))


@pytest.mark.parametrize('inp_version', schema_versions['inp'])
@pytest.mark.parametrize('out_version', schema_versions['out'])
def test_outschema_dict(data_regression, inp_version, out_version):
    """
    Test the fleur_schema_parser_functions to make sure that they match the stored inputschema_dict
    """
    from masci_tools.io.parsers.fleur.fleur_schema import OutputSchemaDict

    outputschema = OutputSchemaDict.fromVersion(version=out_version, inp_version=inp_version)

    data_regression.check(clean_for_reg_dump(outputschema.get_unlocked()))


def clean_for_reg_dump(value_to_clean):
    """
    Clean for data regression converts CaseInsensitiveFrozenSet to set
    Lockable containers are to be converted berfore via `get_unlocked()`
    """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveFrozenSet
    from masci_tools.io.parsers.fleur.fleur_schema.fleur_schema_parser_functions import AttributeType

    if isinstance(value_to_clean, dict):
        for key, val in value_to_clean.items():
            value_to_clean[key] = clean_for_reg_dump(val)
    elif isinstance(value_to_clean, list):
        for indx, val in enumerate(value_to_clean):
            value_to_clean[indx] = clean_for_reg_dump(val)
    elif isinstance(value_to_clean, CaseInsensitiveFrozenSet):
        value_to_clean = set(clean_for_reg_dump(val) for val in value_to_clean)
    elif isinstance(value_to_clean, AttributeType):
        value_to_clean = dict(value_to_clean._asdict())

    return value_to_clean
