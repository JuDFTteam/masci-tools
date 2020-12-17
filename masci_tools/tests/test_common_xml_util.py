# -*- coding: utf-8 -*-
"""
Test of the functions in common_xml_util
"""
import pytest
from masci_tools.util.constants import FLEUR_DEFINED_CONSTANTS

def test_convert_to_float():
    """
    Test of the convert_to_float function
    """
    from masci_tools.util.xml.common_xml_util import convert_to_float

    ret_val, suc = convert_to_float('0.45')
    assert suc
    assert pytest.approx(ret_val) == 0.45

    ret_val = convert_to_float('-99999231.2143543', suc_return=False)
    assert pytest.approx(ret_val) == -99999231.2143543

    ret_val, suc = convert_to_float('1.5324324e-9', suc_return=True)
    assert suc
    assert pytest.approx(ret_val) == 1.5324324e-9

    warnings = []
    ret_val, suc = convert_to_float({}, conversion_warnings=warnings)
    assert not suc
    assert ret_val == {}
    assert warnings == ["Could not convert: '{}' to float, TypeError"]


    warnings = []
    ret_val, suc = convert_to_float('1,23', conversion_warnings=warnings)
    assert not suc
    assert ret_val == '1,23'
    assert warnings == ["Could not convert: '1,23' to float, ValueError"]

    warnings = []
    ret_val, suc = convert_to_float('.325352', conversion_warnings=warnings)
    assert suc
    assert pytest.approx(ret_val) == .325352
    assert warnings == []

def test_convert_to_int():
    """
    Test of the convert_to_int function
    """
    from masci_tools.util.xml.common_xml_util import convert_to_int

    ret_val, suc = convert_to_int('1241412')
    assert suc
    assert ret_val == 1241412

    ret_val = convert_to_int('-9999999999999999999999', suc_return=False)
    assert ret_val == -9999999999999999999999

    ret_val, suc = convert_to_int('12031', suc_return=True)
    assert suc
    assert ret_val == 12031

    warnings = []
    ret_val, suc = convert_to_int((), conversion_warnings=warnings)
    assert not suc
    assert ret_val == ()
    assert warnings == ["Could not convert: '()' to int, TypeError"]


    warnings = []
    ret_val, suc = convert_to_int('1.231', conversion_warnings=warnings)
    assert not suc
    assert ret_val == '1.231'
    assert warnings == ["Could not convert: '1.231' to int, ValueError"]

    warnings = []
    ret_val, suc = convert_to_int('213', conversion_warnings=warnings)
    assert suc
    assert ret_val == 213
    assert warnings == []

def test_convert_from_fortran_bool():
    """
    Test of the convert_from_fortran_bool function
    """
    from masci_tools.util.xml.common_xml_util import convert_from_fortran_bool

    TRUE_ITEMS = ('T', 't', True)
    FALSE_ITEMS = ('F', 'f', False)

    for true_item in TRUE_ITEMS:
        ret_val, suc = convert_from_fortran_bool(true_item)
        assert suc
        assert ret_val

    for false_item in FALSE_ITEMS:
        ret_val, suc = convert_from_fortran_bool(false_item)
        assert suc
        assert not ret_val

    ret_val = convert_from_fortran_bool('T', suc_return=False)
    assert ret_val
    ret_val, suc = convert_from_fortran_bool('f', suc_return=True)
    assert suc
    assert not ret_val

    warnings = []
    ret_val, suc = convert_from_fortran_bool('TEST', conversion_warnings=warnings)
    assert not suc
    assert ret_val == 'TEST'
    assert warnings == ["Could not convert: 'TEST' to boolean, "
                        "which is not 'True', 'False', 't', 'T', 'F' or 'f'"]

    warnings = []
    ret_val, suc = convert_from_fortran_bool({}, conversion_warnings=warnings)
    assert not suc
    assert ret_val == {}
    assert warnings == ["Could not convert: '{}' to boolean, only accepts str or boolean"]

    warnings = []
    ret_val, suc = convert_from_fortran_bool(True, conversion_warnings=warnings)
    assert suc
    assert ret_val
    assert warnings == []




