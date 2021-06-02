# -*- coding: utf-8 -*-
"""
Tests of the calculator of mathematical expressions in the inp.xml files
"""
import pytest
from masci_tools.util.fleur_calculate_expression import calculate_expression
from masci_tools.util.constants import FLEUR_DEFINED_CONSTANTS
import numpy as np


def test_calculate_expression():

    assert pytest.approx(calculate_expression('1.0+3.0-2.45*8.45', FLEUR_DEFINED_CONSTANTS)) == -16.7025
    assert pytest.approx(calculate_expression('Pi/4.0', FLEUR_DEFINED_CONSTANTS)) == 0.78539816339
    assert pytest.approx(calculate_expression('cos(Pi)-exp(2)*(4.0+sin(Pi/2))',
                                              FLEUR_DEFINED_CONSTANTS)) == -37.94528049
    assert pytest.approx(calculate_expression('(2+5)**(1/2.0)', FLEUR_DEFINED_CONSTANTS)) == 2.64575
    assert pytest.approx(calculate_expression('-0.5**(4%(2.0+1.0))', FLEUR_DEFINED_CONSTANTS)) == -0.5


def test_calculate_expression_errors():

    with pytest.raises(ValueError, match=r'Invalid expression: Expected Bracket after function name'):
        calculate_expression('sin1.0)', FLEUR_DEFINED_CONSTANTS)
    with pytest.raises(ValueError, match=r'Invalid expression: log\(x\), x\<\=0'):
        calculate_expression('log(0.0)', FLEUR_DEFINED_CONSTANTS)
    with pytest.raises(ValueError, match=r'Invalid expression: sqrt\(x\), x\<0'):
        calculate_expression('sqrt(-1.0)', FLEUR_DEFINED_CONSTANTS)
    with pytest.raises(ValueError, match=r'Invalid expression: asin\(x\), \|x\|\>1'):
        calculate_expression('asin(2.0)', FLEUR_DEFINED_CONSTANTS)
    with pytest.raises(ValueError, match=r'Invalid expression: acos\(x\), \|x\|\>1'):
        calculate_expression('acos(2.0)', FLEUR_DEFINED_CONSTANTS)
    with pytest.raises(ValueError, match=r'Unknown string expression: A'):
        calculate_expression('(3.0 + A)*5', FLEUR_DEFINED_CONSTANTS)
    with pytest.raises(ValueError, match=r'Invalid Expression: Found operator / in the beginning of expression'):
        calculate_expression('/1.0', FLEUR_DEFINED_CONSTANTS)
    with pytest.raises(ValueError, match=r'Invalid Expression: Operator following operator'):
        calculate_expression('(3.0 + /1.0)*5', FLEUR_DEFINED_CONSTANTS)
    with pytest.raises(ValueError, match=r'Undefined Expression: Division by zero'):
        calculate_expression('1.0/(3.0-3.0)', FLEUR_DEFINED_CONSTANTS)
    with pytest.raises(ValueError, match=r'Undefined Expression: 0\^0'):
        calculate_expression('0.0^(3.0-3.0)', FLEUR_DEFINED_CONSTANTS)
    with pytest.raises(ValueError, match=r'Undefined Expression: x\^y, x\<0 and y not integer'):
        calculate_expression('-1.0^(1.0-1.0/2.0)', FLEUR_DEFINED_CONSTANTS)
    with pytest.raises(ValueError, match=r'Invalid expression: Found unexpected character &'):
        calculate_expression('1.0&4', FLEUR_DEFINED_CONSTANTS)
    with pytest.raises(ValueError, match=r'Cannot parse number: Found two decimal points'):
        calculate_expression('1..09', FLEUR_DEFINED_CONSTANTS)
    with pytest.raises(ValueError, match=r'Invalid Expression: Unbalanced parentheses'):
        calculate_expression('(1.04+7.89*(6.3/Pi)', FLEUR_DEFINED_CONSTANTS)
