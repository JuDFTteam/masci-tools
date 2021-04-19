# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools.   #
# For further information on the license, see the LICENSE.txt file.           #
# For further information please visit http://judft.de/.                      #
#                                                                             #
###############################################################################
"""
This module contains the functions necessary to parse mathematical expressions
with predefined constants given in the inp.xml file of Fleur
"""
from __future__ import absolute_import
import numpy as np


def calculate_expression(expression, constants, prevCommand=None, exp_return=False):
    """
    Recursively evaluates the given expression string with the given defined constants

    :param expression: str containing the expression to be parsed
    :param constants: dict with all defined constants (predefined in the Fleur code or defined in the inp.xml)
    :param prevCommand: str, which gives the command before the beginning of the current block
                        if it is given the calculation is stopped, when a command is encountered, which should
                        be exectuted after prevCommand (order of operations)
    :param exp_return: bool, determines whether to return the remaining string of the expression

    :return: float value of the given expression string
    """

    #Map the keywords recognized by fleur to the corresponding numpy function
    functions_dict = {
        'sin': np.sin,
        'cos': np.cos,
        'tan': np.tan,
        'exp': np.exp,
        'log': np.log,
        'abs': np.abs,
        'sqrt': np.sqrt,
        'acos': np.arccos,
        'asin': np.arcsin,
        'atan': np.arctan,
        'cosh': np.cosh,
        'sinh': np.sinh,
        'tanh': np.tanh,
    }

    #Define order of operations
    order_dict = {'+': 10, '-': 10, '*': 100, '/': 100, '%': 100, '**': 1000, '^': 1000}

    stop_loop = False
    loop_count = 0

    if expression is None:
        raise ValueError('Invalid expression: Got None for expression')

    if isinstance(expression, (float, int)):
        return expression

    expression = expression.replace(' ', '')
    value = None
    while not stop_loop and len(expression) != 0:
        loop_count += 1
        firstchar = expression[0]
        if firstchar.isdecimal() or firstchar == '.' or \
           (firstchar in ['+', '-'] and loop_count == 1):
            value, expression = get_first_number(expression)
            stop_loop = False
        elif firstchar.isalpha():
            string, expression = get_first_string(expression)
            if string in functions_dict:
                if expression[0] != '(':
                    raise ValueError('Invalid expression: Expected Bracket after function name')
                function = functions_dict[string]
                function_value, expression = evaluate_bracket(expression, constants)
                #Check conditions for functions
                if string == 'log' and function_value <= 0.0:
                    raise ValueError('Invalid expression: log(x), x<=0')
                elif string == 'sqrt' and function_value < 0.0:
                    raise ValueError('Invalid expression: sqrt(x), x<0')
                elif string == 'asin' and abs(function_value) > 1.0:
                    raise ValueError('Invalid expression: asin(x), |x|>1')
                elif string == 'acos' and abs(function_value) > 1.0:
                    raise ValueError('Invalid expression: acos(x), |x|>1')
                value = function(function_value)
            elif string in constants:
                value = constants[string]
            else:
                raise ValueError(f'Unknown string expression: {string}')
            stop_loop = False
        elif firstchar in ['+', '-', '*', '/', '%', '^']:
            if loop_count == 1:
                raise ValueError(f'Invalid Expression: Found operator {firstchar} in the beginning of expression')
            operator = firstchar
            if expression[1] in ['+', '-', '*', '/', '%', '^']:
                if expression[:2] == '**':
                    operator = expression[:2]
                else:
                    raise ValueError('Invalid Expression: Operator following operator')
            if prevCommand is not None:
                prevOrder = order_dict[prevCommand]
            else:
                prevOrder = 0
            operatorOrder = order_dict[operator]
            if operatorOrder > prevOrder:
                #Evaluate the next block
                block_value, expression = calculate_expression(expression[len(operator):],
                                                               constants,
                                                               prevCommand=operator,
                                                               exp_return=True)
                #Perform the operation
                if operator == '+':
                    value += block_value
                elif operator == '-':
                    value -= block_value
                elif operator == '*':
                    value *= block_value
                elif operator == '/':
                    if abs(block_value) < 1e-12:
                        raise ValueError('Undefined Expression: Division by zero')
                    value *= 1.0 / block_value
                elif operator == '%':
                    value = value % block_value
                elif operator in ['^', '**']:
                    if abs(value) < 1e-12 and abs(block_value) < 1e-12:
                        raise ValueError('Undefined Expression: 0^0')
                    if value < 0.0 and abs(int(block_value) - block_value) > 1e-12:
                        raise ValueError('Undefined Expression: x^y, x<0 and y not integer')
                    elif value < 0.0:
                        block_value = int(block_value)
                    value = value**block_value
            else:
                stop_loop = True
        elif firstchar == '(':
            value, expression = evaluate_bracket(expression, constants)
            stop_loop = False
        else:
            raise ValueError(f'Invalid expression: Found unexpected character {firstchar}')

    if exp_return:
        return value, expression
    else:
        return value


def get_first_number(expression):
    """
    Reads the number in the beginning of the expression string.
    This number can begin with a sign +-, a number or the decimal point

    :param expression: str of the expression

    :return: float value of the number in the beginning and the string of the remaining
             expression
    """
    numberstring = ''
    found_decimal_point = False
    for char in expression:
        if char.isdecimal():
            numberstring += char
        elif char == '.':
            if found_decimal_point:
                raise ValueError('Cannot parse number: Found two decimal points')
            found_decimal_point = True
            numberstring += char
        elif char in ['+', '-']:
            if len(numberstring) == 0:
                numberstring += char
            else:
                break
        else:
            break
    return float(numberstring), expression[len(numberstring):]


def get_first_string(expression):
    """
    Reads the letter string in the beginning of the expression string.

    :param expression: str of the expression

    :return: letter string in the beginning and the string of the remaining
             expression
    """
    found_string = ''
    for char in expression:
        if char.isalpha():
            found_string += char
        else:
            break

    return found_string, expression[len(found_string):]


def evaluate_bracket(expression, constants):
    """
    Evaluates the bracket opened at the start of the expression

    :param expression: expression to be parsed
    :param constants: dict with defined constants

    :return: value of the expression inside the brackets and remaining string of the expression
             after the corresponding closed bracket
    """
    closing_pos = 0
    opened_brackets = 0
    for char in expression:
        if char == '(':
            opened_brackets += 1
        elif char == ')':
            opened_brackets -= 1
        if opened_brackets == 0:
            break
        closing_pos += 1
    if opened_brackets != 0:
        raise ValueError('Invalid Expression: Unbalanced parentheses')

    value = calculate_expression(expression[1:closing_pos], constants)

    return value, expression[closing_pos + 1:]
