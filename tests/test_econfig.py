# -*- coding: utf-8 -*-
"""
Tests of the econfig module
"""
import pytest


def test_get_econfig_all():
    """
    Make sure all options in PERIODIC_TABLE_ELEMENTS lead to some econfig
    """
    from masci_tools.util.constants import PERIODIC_TABLE_ELEMENTS
    from masci_tools.util.econfig import get_econfig

    for number, info in PERIODIC_TABLE_ELEMENTS.items():

        if number == 0:
            assert get_econfig(number) is None
            assert get_econfig(info['symbol']) is None
        else:
            assert get_econfig(number) is not None
            assert get_econfig(info['symbol']) is not None


elements = ['Ne', 'O', 'Gd', 'U']
numbers = [10, 8, 64, 92]
short_econfig = [
    '[He] 2s2 | 2p6', '[He] 2s2 | 2p4', '[Kr] 4d10 5s2 5p6 | 6s2 4f7 5d1', '[Xe] 4f14 5d10 6s2 6p6| 7s2 5f4'
]
full_econfig = [
    '1s2 2s2 | 2p6', '1s2 2s2 | 2p4', '1s2 2s2 2p6 3s2 3p6 3d10 4s2 4p6 4d10 5s2 5p6 | 6s2 4f7 5d1',
    '1s2 2s2 2p6 3s2 3p6 3d10 4s2 4p6 4d10 5s2 5p6 4f14 5d10 6s2 6p6| 7s2 5f4'
]
short_core_config = ['[He] 2s2', '[He] 2s2', '[Kr] 4d10 5s2 5p6', '[Xe] 4f14 5d10 6s2 6p6']
full_core_config = [
    '1s2 2s2', '1s2 2s2', '1s2 2s2 2p6 3s2 3p6 3d10 4s2 4p6 4d10 5s2 5p6',
    '1s2 2s2 2p6 3s2 3p6 3d10 4s2 4p6 4d10 5s2 5p6 4f14 5d10 6s2 6p6'
]


@pytest.mark.parametrize('element, econf', zip(elements, short_econfig))
def test_get_econfig_name(element, econf):
    """
    Test of the get_econfig function with element names
    """
    from masci_tools.util.econfig import get_econfig

    res = get_econfig(element)
    assert res == econf


@pytest.mark.parametrize('number, econf', zip(numbers, short_econfig))
def test_get_econfig_atomic_number(number, econf):
    """
    Test of the get_econfig function with element names
    """
    from masci_tools.util.econfig import get_econfig

    res = get_econfig(number)
    assert res == econf


@pytest.mark.parametrize('element, econf', zip(elements, full_econfig))
def test_get_econfig_full(element, econf):
    """
    Test of the get_econfig function with element names
    """
    from masci_tools.util.econfig import get_econfig

    res = get_econfig(element, full=True)
    assert res == econf


def test_get_coreconfig_all():
    """
    Make sure all options in PERIODIC_TABLE_ELEMENTS lead to some econfig
    """
    from masci_tools.util.constants import PERIODIC_TABLE_ELEMENTS
    from masci_tools.util.econfig import get_coreconfig

    for number, info in PERIODIC_TABLE_ELEMENTS.items():

        if number == 0:
            assert get_coreconfig(number) is None
            assert get_coreconfig(info['symbol']) is None
        else:
            assert get_coreconfig(number) is not None
            assert get_coreconfig(info['symbol']) is not None


@pytest.mark.parametrize('element, econf', zip(elements, short_core_config))
def test_get_coreconfig_name(element, econf):
    """
    Test of the get_econfig function with element names
    """
    from masci_tools.util.econfig import get_coreconfig

    res = get_coreconfig(element)
    assert res == econf


@pytest.mark.parametrize('number, econf', zip(numbers, short_core_config))
def test_get_coreconfig_atomic_number(number, econf):
    """
    Test of the get_econfig function with element names
    """
    from masci_tools.util.econfig import get_coreconfig

    res = get_coreconfig(number)
    assert res == econf


@pytest.mark.parametrize('element, econf', zip(elements, full_core_config))
def test_get_coreconfig_full(element, econf):
    """
    Test of the get_econfig function with element names
    """
    from masci_tools.util.econfig import get_coreconfig

    res = get_coreconfig(element, full=True)
    assert res == econf
