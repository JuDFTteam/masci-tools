# -*- coding: utf-8 -*-
"""
Test for the case insensitive, immutable set implemented in util
"""
import pytest

TEST_INIT = ['ABC', 'abC', 'RanDomEntry5', 'snake_case_entry', 'camelCaseEntry', 'camelcaseentry']
TEST_MEMBER = [('randomentry5', True, 'RanDomEntry5'), ('snakecaseentry', False, None),
               ('camelcaseentry', True, 'camelCaseEntry'), ('aBc', True, 'ABC'), ('not_existent', False, None)]


@pytest.mark.parametrize('key,is_member,original_case', TEST_MEMBER)
def test_case_insensitive_frozenset_member(key, is_member, original_case):
    """
   Test CaseInsensitiveFrozenSet for correct membership tests and the right stored original case
   """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveFrozenSet

    s = CaseInsensitiveFrozenSet(TEST_INIT)

    if is_member:
        assert key in s
        assert s.original_case[key] == original_case
    else:
        assert key not in s


TEST_SET = [{'ABC', 'abC', 'RanDomEntry5', 'snake_case_entry', 'camelCaseEntry', 'camelcaseentry'},
            {'ABC', 'not_existent', 'snakecaseentry'}]

TEST_EQUAL = [True, False]


@pytest.mark.parametrize('test_set,is_equal', zip(TEST_SET, TEST_EQUAL))
def test_case_insensitive_frozenset_eq(test_set, is_equal):
    """
   Test CaseInsensitiveFrozenSet for correct equality
   """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveFrozenSet

    s = CaseInsensitiveFrozenSet(TEST_INIT)

    if is_equal:
        assert s == test_set
    else:
        assert s != test_set


TEST_DIFFERENCES = [set(), {'camelcaseentry', 'randomentry5', 'snake_case_entry'}]
TEST_DIFF_CASES = [{}, {
    'randomentry5': 'RanDomEntry5',
    'camelcaseentry': 'camelCaseEntry',
    'snake_case_entry': 'snake_case_entry'
}]


@pytest.mark.parametrize('test_set,exp_diff,exp_case', zip(TEST_SET, TEST_DIFFERENCES, TEST_DIFF_CASES))
def test_case_insensitive_frozenset_difference(test_set, exp_diff, exp_case):
    """
   Test CaseInsensitiveFrozenSet for correct difference
   """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveFrozenSet

    s = CaseInsensitiveFrozenSet(TEST_INIT)

    actual = s.difference(test_set)

    assert isinstance(actual, CaseInsensitiveFrozenSet)
    assert s - test_set == actual
    assert actual.original_case == exp_case


TEST_UNIONS = [{'camelcaseentry', 'snake_case_entry', 'randomentry5', 'abc'},
               {'camelcaseentry', 'snake_case_entry', 'randomentry5', 'abc', 'not_existent', 'snakecaseentry'}]
TEST_UNION_CASES = [{
    'camelcaseentry': 'camelCaseEntry',
    'abc': 'ABC',
    'randomentry5': 'RanDomEntry5',
    'snake_case_entry': 'snake_case_entry'
}, {
    'not_existent': 'not_existent',
    'camelcaseentry': 'camelCaseEntry',
    'snakecaseentry': 'snakecaseentry',
    'snake_case_entry': 'snake_case_entry',
    'abc': 'ABC',
    'randomentry5': 'RanDomEntry5'
}]


@pytest.mark.parametrize('test_set,exp_union,exp_case', zip(TEST_SET, TEST_UNIONS, TEST_UNION_CASES))
def test_case_insensitive_frozenset_union(test_set, exp_union, exp_case):
    """
   Test CaseInsensitiveFrozenSet for correct union
   """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveFrozenSet

    s = CaseInsensitiveFrozenSet(TEST_INIT)

    actual = s.union(test_set)

    assert isinstance(actual, CaseInsensitiveFrozenSet)
    assert actual == exp_union
    assert s | test_set == actual
    assert actual.original_case == exp_case


TEST_SYM_DIFFERENCES = [set(), {'camelcaseentry', 'randomentry5', 'snake_case_entry', 'not_existent', 'snakecaseentry'}]
TEST_SYMDIFF_CASES = [{}, {
    'snakecaseentry': 'snakecaseentry',
    'randomentry5': 'RanDomEntry5',
    'camelcaseentry': 'camelCaseEntry',
    'not_existent': 'not_existent',
    'snake_case_entry': 'snake_case_entry'
}]


@pytest.mark.parametrize('test_set,exp_diff,exp_case', zip(TEST_SET, TEST_SYM_DIFFERENCES, TEST_SYMDIFF_CASES))
def test_case_insensitive_frozenset_sym_difference(test_set, exp_diff, exp_case):
    """
   Test CaseInsensitiveFrozenSet for correct symmetric difference
   """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveFrozenSet

    s = CaseInsensitiveFrozenSet(TEST_INIT)

    actual = s.symmetric_difference(test_set)
    print(actual.original_case)
    assert isinstance(actual, CaseInsensitiveFrozenSet)
    assert actual == exp_diff
    assert s ^ test_set == actual
    assert actual.original_case == exp_case


TEST_INTERSECTIONS = [{'camelcaseentry', 'snake_case_entry', 'randomentry5', 'abc'}, {'abc'}]
TEST_INTERSECTIONS_CASES = [{
    'abc': 'ABC',
    'randomentry5': 'RanDomEntry5',
    'snake_case_entry': 'snake_case_entry',
    'camelcaseentry': 'camelCaseEntry'
}, {
    'abc': 'ABC'
}]


@pytest.mark.parametrize('test_set,exp_intersect,exp_case', zip(TEST_SET, TEST_INTERSECTIONS, TEST_INTERSECTIONS_CASES))
def test_case_insensitive_frozenset_intersection(test_set, exp_intersect, exp_case):
    """
   Test CaseInsensitiveFrozenSet for correct intersection
   """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveFrozenSet

    s = CaseInsensitiveFrozenSet(TEST_INIT)

    actual = s.intersection(test_set)
    print(actual.original_case)
    assert isinstance(actual, CaseInsensitiveFrozenSet)
    assert s & test_set == actual
    assert actual.original_case == exp_case
