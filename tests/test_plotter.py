# -*- coding: utf-8 -*-
"""
Tests of the plotter base class
"""
from masci_tools.vis import Plotter, ensure_plotter_consistency
import pytest

TEST_DICT = {'A': {'test1': 12, 'test2': 4}, 'B': 3.0, 'C': 'title'}


def test_plotter_access():
    """
   Test basic item acces and make sure the right structure was created
   """
    p = Plotter(TEST_DICT)

    assert dict(p._params) == TEST_DICT

    #Test basic getitem method
    for key, value in TEST_DICT.items():
        assert p[key] == value


def test_plotter_set_parameters():
    """
   Test setting of parameters
   """
    p = Plotter(TEST_DICT)

    p['B'] = 0

    assert p['B'] == 0

    with pytest.raises(KeyError):
        p['D'] = 'not a key'

    p['A'] = {'test3': 'extra'}

    assert p['A'] == {'test1': 12, 'test2': 4, 'test3': 'extra'}

    with pytest.raises(ValueError):
        p['A'] = 2.0

    assert dict(p._params.parents) == TEST_DICT
    p.reset_parameters()

    assert dict(p._params) == TEST_DICT


def test_plotter_set_parameters_function():
    """
   Test setting parameters via the provided function
   """
    p = Plotter(TEST_DICT)

    p.set_parameters(continue_on_error=True, **{'B': 0, 'A': {'test3': 'extra'}, 'D': 'not a key'})

    assert dict(p._params) == {'A': {'test1': 12, 'test2': 4, 'test3': 'extra'}, 'B': 0, 'C': 'title'}

    p.reset_parameters()

    with pytest.raises(KeyError):
        p.set_parameters(**{'B': 0, 'A': {'test3': 'extra'}, 'D': 'not a key'})

    assert dict(p._params) == TEST_DICT


def test_plotter_set_defaults():
    """
   Test setting of defaults
   """

    p = Plotter(TEST_DICT)

    p.set_defaults(continue_on_error=True, **{'B': 0, 'A': {'test3': 'extra'}, 'D': 'not a key'})

    expected_result = {'A': {'test1': 12, 'test2': 4, 'test3': 'extra'}, 'B': 0, 'C': 'title'}

    assert dict(p._params) == expected_result
    assert dict(p._params.parents) == expected_result

    p.reset_defaults()

    assert dict(p._params) == TEST_DICT

    with pytest.raises(KeyError):
        p.set_defaults(**{'B': 0, 'A': {'test3': 'extra'}, 'D': 'not a key'})

    assert dict(p._params) == TEST_DICT


def test_plotter_init_defaults():
    """
   Test setting defaults via initialization
   """
    p = Plotter(TEST_DICT, **{'B': 0, 'A': {'test3': 'extra'}, 'D': 'not a key'})

    expected_result = {'A': {'test1': 12, 'test2': 4, 'test3': 'extra'}, 'B': 0, 'C': 'title'}

    assert dict(p._params) == expected_result
    assert dict(p._params.parents) == expected_result


def test_plotter_add_parameter():
    """
    Test adding of custom parameters
    """

    p = Plotter(TEST_DICT)

    p.add_parameter('D')
    assert p['D'] is None
    p['D'] = 2
    assert p['D'] == 2

    p.add_parameter('E', default_from='C')
    assert p['E'] == 'title'

    p.remove_added_parameters()
    p.reset_parameters()

    assert dict(p._params) == TEST_DICT


def test_plotter_decorator_working():
    """
    Test the ensure_plotter_consistency decorator for a working function
    """

    p = Plotter(TEST_DICT)

    @ensure_plotter_consistency(p)
    def test_function():
        p.set_parameters(B=4.0)

    test_function()

    assert dict(p._params) == TEST_DICT


def test_plotter_decorator_raised_error():
    """
    Test the ensure_plotter_consistency decorator for a function with an error occuring durin execution
    """

    p = Plotter(TEST_DICT)

    @ensure_plotter_consistency(p)
    def test_function():
        p.set_parameters(B=4.0)
        raise ValueError('Test')

    with pytest.raises(ValueError, match='Test'):
        test_function()

    assert dict(p._params) == TEST_DICT


def test_plotter_decorator_set_defaults():
    """
    Test the ensure_plotter_consistency decorator for a function changing the defaults (raises Error)
    """

    p = Plotter(TEST_DICT)

    @ensure_plotter_consistency(p)
    def test_function():
        p.set_defaults(C='TEST')
        p.set_parameters(B=4.0)

    with pytest.raises(ValueError):
        test_function()

    assert dict(p._params) == TEST_DICT


def test_plotter_decorator_add_parameter():
    """
    Test the ensure_plotter_consistency decorator for a function adding custom parameters
    """

    p = Plotter(TEST_DICT)

    @ensure_plotter_consistency(p)
    def test_function():
        p.add_parameter('D')
        p.add_parameter('E', default_from='C')

    test_function()

    assert dict(p._params) == TEST_DICT


def test_plotter_decorator_add_parameter_raised_error():
    """
    Test the ensure_plotter_consistency decorator for a function adding custom parameters with an exception occuring
    """

    p = Plotter(TEST_DICT)

    @ensure_plotter_consistency(p)
    def test_function():
        p.add_parameter('D')
        p.add_parameter('E', default_from='C')
        raise ValueError('Test')

    with pytest.raises(ValueError, match='Test'):
        test_function()

    assert dict(p._params) == TEST_DICT


WORKING_VALUES = [[None, 3, None], 'Test', [1, 2, 3, 4, 5], {4: 'Test2'}, [5.0], {'NotAList': 'Test2'}]
GIVEN_NUM_PLOTS = [5, 3, 5, 5, 2, 1]
SINGLE_PLOT_ERROR = [True, False, True, True, True, False]
EXPECTED_RESULTS = [[None, 3, None, None, None], 'Test', [1, 2, 3, 4, 5], [None, None, None, None, 'Test2'],
                    [5.0, None], {
                        'NotAList': 'Test2'
                    }]
EXPECTED_RESULTS_WITH_DEFAULT = [['default', 3, 'default', 'default', 'default'], 'Test', [1, 2, 3, 4, 5],
                                 ['default', 'default', 'default', 'default', 'Test2'], [5.0, 'default'], {
                                     'NotAList': 'Test2'
                                 }]


@pytest.mark.parametrize('given_value,num_plots,expected_list', zip(WORKING_VALUES, GIVEN_NUM_PLOTS, EXPECTED_RESULTS))
def test_plotter_convert_to_complete_list_multiple_plots_list(given_value, num_plots, expected_list):

    complete_list = Plotter.convert_to_complete_list(given_value, False, num_plots)

    assert complete_list == expected_list


@pytest.mark.parametrize('given_value,num_plots,expected_list',
                         zip(WORKING_VALUES, GIVEN_NUM_PLOTS, EXPECTED_RESULTS_WITH_DEFAULT))
def test_plotter_convert_to_complete_list_multiple_plots_list_default(given_value, num_plots, expected_list):

    complete_list = Plotter.convert_to_complete_list(given_value, False, num_plots, default='default')

    assert complete_list == expected_list


@pytest.mark.parametrize('given_value, error_expected, expected_result',
                         zip(WORKING_VALUES, SINGLE_PLOT_ERROR, EXPECTED_RESULTS))
def test_plotter_convert_to_complete_list_single_plot_no_list_allowed(given_value, error_expected, expected_result):

    if error_expected:
        with pytest.raises(ValueError):
            res = Plotter.convert_to_complete_list(given_value, True, 1)
    else:
        res = Plotter.convert_to_complete_list(given_value, True, 1)

        assert res == expected_result
