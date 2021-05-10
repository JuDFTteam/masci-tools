# -*- coding: utf-8 -*-
"""
Tests for the case insensitive containers implemented in util/case_insensitive_dict.py
"""
import pytest

TEST_DICT = {'ABC': 123, 'SUBDICT': {'TEST': 'test_string'}, 'miXedCase4': 5}
EXPECTED_REPR = "CaseInsensitiveDict({'abc': 123, 'subdict': {'TEST': 'test_string'}, 'mixedcase4': 5})"
EXPECTED_REPR_UPPER = "CaseInsensitiveDict({'ABC': 123, 'SUBDICT': {'TEST': 'test_string'}, 'MIXEDCASE4': 5})"

TEST_LOOKUPS = [('ABC', 123), ('abc', 123), ('aBc', 123), ('sUbDiCT', {'TEST': 'test_string'}), ('MIXEDCASE4', 5)]
TEST_LOOKUPS_NOT_EXISTENT = ['not_existent', 'MIXEDCASE$', 'AB_C']


@pytest.mark.parametrize('key, result', TEST_LOOKUPS)
def test_case_insensitive_dict_get(key, result):
    """
   Test case insensitive lookup in CaseInsensitiveDict
   """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict

    d = CaseInsensitiveDict(TEST_DICT)

    assert key in d
    assert d[key] == result
    assert repr(d) == EXPECTED_REPR


@pytest.mark.parametrize('key, result', TEST_LOOKUPS)
def test_case_insensitive_dict_upper_get(key, result):
    """
   Test case insensitive lookup in CaseInsensitiveDict with upper() as normalizing function
   """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict

    d = CaseInsensitiveDict(TEST_DICT, upper=True)

    assert key in d
    assert d[key] == result
    assert repr(d) == EXPECTED_REPR_UPPER


@pytest.mark.parametrize('key', TEST_LOOKUPS_NOT_EXISTENT)
def test_case_insensitive_dict_get_not_existent(key):
    """
   Test case insensitive lookup (non existent keys) in CaseInsensitiveDict
   """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict

    d = CaseInsensitiveDict(TEST_DICT)

    assert key not in d
    with pytest.raises(KeyError):
        val = d[key]


@pytest.mark.parametrize('key', TEST_LOOKUPS_NOT_EXISTENT)
def test_case_insensitive_dict_upper_get_not_existent(key):
    """
   Test case insensitive lookup (non existent keys) in CaseInsensitiveDict with upper() as normalizing function
   """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict

    d = CaseInsensitiveDict(TEST_DICT, upper=True)

    assert key not in d
    with pytest.raises(KeyError):
        val = d[key]


@pytest.mark.parametrize('key, result', TEST_LOOKUPS)
def test_case_insensitive_dict_pop(key, result):
    """
   Test case insensitive pop in CaseInsensitiveDict
   """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict

    d = CaseInsensitiveDict(TEST_DICT)

    assert key in d
    assert d.pop(key) == result
    assert key not in d


@pytest.mark.parametrize('key, result', TEST_LOOKUPS)
def test_case_insensitive_dict_pop_upper(key, result):
    """
   Test case insensitive pop in CaseInsensitiveDict with upper() as normalizing function
   """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict

    d = CaseInsensitiveDict(TEST_DICT, upper=True)

    assert key in d
    assert d.pop(key) == result
    assert key not in d
