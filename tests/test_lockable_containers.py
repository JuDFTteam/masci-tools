# -*- coding: utf-8 -*-
"""
Tests of the Lockable containers
"""
import pytest

TEST_DICT = {'A': 3, 'B': {'Test': [], 'Test2': 'A'}}
TEST_LIST = [3, {'Test': [], 'Test2': 'A'}]


def test_lockable_dict():
    """
   test the LockableDict behaviour
   """
    from masci_tools.util.lockable_containers import LockableDict, LockableList

    l = LockableDict(TEST_DICT)

    l['test_set'] = 'iamallowedtochange'

    assert l['test_set'] == 'iamallowedtochange'

    l.freeze()

    assert l._locked
    assert isinstance(l['B'], LockableDict)
    assert l['B']._locked
    assert isinstance(l['B']['Test'], LockableList)
    assert l['B']['Test']._locked

    with pytest.raises(RuntimeError, match='Modification not allowed'):
        l['test_set'] = 'notanymore'

    with pytest.raises(RuntimeError, match='Modification not allowed'):
        l.pop('B')


def test_lockable_list():
    """
   test the LockableList behaviour
   """
    from masci_tools.util.lockable_containers import LockableDict, LockableList

    l = LockableList(TEST_LIST)
    print([type(val) for val in l])

    l.append('iamallowedtochange')

    assert l[-1] == 'iamallowedtochange'

    l.freeze()

    assert l._locked
    assert isinstance(l[1], LockableDict)
    assert l[1]._locked
    assert isinstance(l[1]['Test'], LockableList)
    assert l[1]['Test']._locked

    with pytest.raises(RuntimeError, match='Modification not allowed'):
        l[2] = 'notanymore'

    with pytest.raises(RuntimeError, match='Modification not allowed'):
        l.append('B')

    with pytest.raises(RuntimeError, match='Modification not allowed'):
        l.pop()


def test_lock_container_contextmanager():
    """
   Test the LockContainer contextmanager
   """
    from masci_tools.util.lockable_containers import LockableDict, LockableList, LockContainer

    l_dict = LockableDict(TEST_DICT)
    l_list = LockableList(TEST_LIST)

    with LockContainer(l_dict):
        l_list.append('test')
        assert l_list[-1] == 'test'
        with pytest.raises(RuntimeError, match='Modification not allowed'):
            l_dict['Test2'] = {'subdict': 4}

    assert not l_dict._locked
    assert l_dict['B'].pop('Test2') == 'A'

    with LockContainer(l_list):
        with pytest.raises(RuntimeError, match='Modification not allowed'):
            l_list.append('test')
        l_dict['Test2'] = {'subdict': 4}

    assert not l_list._locked
    l_list[1]['A2'] = 'A3'

    l_dict.freeze()

    with pytest.raises(AssertionError, match='LockableDict was already locked before entering the contextmanager'):
        with LockContainer(l_dict):
            pass

    with pytest.raises(AssertionError, match='Wrong type Got:'):
        with LockContainer([]):
            pass
