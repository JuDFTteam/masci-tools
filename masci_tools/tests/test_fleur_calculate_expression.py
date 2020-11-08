# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from builtins import object
import pytest
from masci_tools.io.parsers.fleur_calculate_expression import calculate_expression
import numpy as np


class TestFleurExpressionCalculation(object):
    def test_calculate_expression():
        const_dict = {'Pi': np.pi,
                      'Deg': 2*np.pi/360.0,
                      'Ang': 1.8897261247728981,
                      'nm': 18.897261247728981,
                      'pm': 0.018897261247728981,
                      'Bohr': 1.0}

        assert(pytest.approx(calculate_expression('1.0+3.0-2.45*8.45', const_dict))==-16.7025)
        assert(pytest.approx(calculate_expression('Pi/4.0', const_dict))==0.78539816339)
        assert(pytest.approx(calculate_expression('cos(Pi)-exp(2)*(4.0+sin(Pi/2))', const_dict))==-37.94528049)
        assert(pytest.approx(calculate_expression('(2+5)**(1/2.0)', const_dict))==2.64575)

    def test_calculate_expression_errors():
        const_dict = {'Pi': np.pi,
                      'Deg': 2*np.pi/360.0,
                      'Ang': 1.8897261247728981,
                      'nm': 18.897261247728981,
                      'pm': 0.018897261247728981,
                      'Bohr': 1.0}

        with pytest.raises(ValueError,match=r'Invalid expression: Expected Bracket after function name'):
            calculate_expression('sin1.0)', const_dict)
        with pytest.raises(ValueError,match=r'Invalid expression: log\(x\), x\<\=0'):
            calculate_expression('log(0.0)', const_dict)
        with pytest.raises(ValueError,match=r'Invalid expression: sqrt\(x\), x\<0'):
            calculate_expression('sqrt(-1.0)', const_dict)
        with pytest.raises(ValueError,match=r'Invalid expression: asin\(x\), \|x\|\>1'):
            calculate_expression('asin(2.0)', const_dict)
        with pytest.raises(ValueError,match=r'Invalid expression: acos\(x\), \|x\|\>1'):
            calculate_expression('acos(2.0)', const_dict)
        with pytest.raises(ValueError,match=r'Unknown string expression: A'):
            calculate_expression('(3.0 + A)*5', const_dict)
        with pytest.raises(ValueError,match=r'Invalid Expression: Found operator / in the beginning of expression'):
            calculate_expression('/1.0', const_dict)
        with pytest.raises(ValueError,match=r'Invalid Expression: Operator following operator'):
            calculate_expression('(3.0 + /1.0)*5', const_dict)
        with pytest.raises(ValueError,match=r'Undefined Expression: Division by zero'):
            calculate_expression('1.0/(3.0-3.0)', const_dict)
        with pytest.raises(ValueError,match=r'Undefined Expression: 0\^0'):
            calculate_expression('0.0^(3.0-3.0)', const_dict)
        with pytest.raises(ValueError,match=r'Undefined Expression: x\^y, x\<0 and y not integer'):
            calculate_expression('-1.0^(1.0-1.0/2.0)', const_dict)
        with pytest.raises(ValueError,match=r'Invalid expression: Found unexpected character &'):
            calculate_expression('1.0&4', const_dict)
        with pytest.raises(ValueError,match=r'Cannot parse number: Found two decimal points'):
            calculate_expression('1..09', const_dict)
        with pytest.raises(ValueError,match=r'Invalid Expression: Unbalanced parentheses'):
            calculate_expression('(1.04+7.89*(6.3/Pi)', const_dict)