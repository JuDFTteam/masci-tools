"""
Test of the Jij calculations in masci_tools.tools.greensf_calculations
"""
import pandas as pd
import numpy as np

ONSITE_DELTA = np.array([[None, None, 1.8348, None]])  #eV


def test_jij(test_file, dataframe_regression):
    """
    Test of the Jij constant calculations
    """
    from masci_tools.tools.greensf_calculations import calculate_heisenberg_jij

    jij_constants = calculate_heisenberg_jij(test_file('fleur/greensf/greensf_jij_mz.hdf'),
                                             reference_atom=1,
                                             onsite_delta=ONSITE_DELTA)

    assert isinstance(jij_constants, pd.DataFrame)
    print(jij_constants.head())
    dataframe_regression.check(jij_constants)


def test_jij_greensfunction_list(test_file, dataframe_regression):
    """
    Test of the Jij constant calculations
    """
    from masci_tools.tools.greensfunction import GreensFunction
    from masci_tools.tools.greensf_calculations import calculate_heisenberg_jij

    n_elements = 15
    g = []
    for index in range(1, n_elements + 1):
        g.append(GreensFunction.fromFile(test_file('fleur/greensf/greensf_jij_mz.hdf'), index=index))

    jij_constants = calculate_heisenberg_jij(g, reference_atom=1, onsite_delta=ONSITE_DELTA)

    assert isinstance(jij_constants, pd.DataFrame)
    print(jij_constants.head())
    dataframe_regression.check(jij_constants, basename='test_jij')


def test_jij_max_shells(test_file, dataframe_regression):
    """
    Test of the Jij constant calculations
    """
    from masci_tools.tools.greensf_calculations import calculate_heisenberg_jij

    jij_constants = calculate_heisenberg_jij(test_file('fleur/greensf/greensf_jij_mz.hdf'),
                                             reference_atom=1,
                                             onsite_delta=ONSITE_DELTA,
                                             max_shells=1)

    assert isinstance(jij_constants, pd.DataFrame)
    dataframe_regression.check(jij_constants)


def test_jij_tensor(test_file, dataframe_regression):
    """
    Test of the Jij constant calculations
    """
    from masci_tools.tools.greensf_calculations import calculate_heisenberg_tensor, decompose_jij_tensor

    jij_constants = calculate_heisenberg_tensor(test_file('fleur/greensf/greensf_jij_mz.hdf'),
                                                reference_atom=1,
                                                onsite_delta=ONSITE_DELTA)

    assert isinstance(jij_constants, pd.DataFrame)
    decompose_jij_tensor(jij_constants, 'z')
    dataframe_regression.check(jij_constants)


def test_jij_tensor_greensfunction_list(test_file, dataframe_regression):
    """
    Test of the Jij constant calculations
    """
    from masci_tools.tools.greensfunction import GreensFunction
    from masci_tools.tools.greensf_calculations import calculate_heisenberg_tensor

    n_elements = 15
    g = []
    for index in range(1, n_elements + 1):
        g.append(GreensFunction.fromFile(test_file('fleur/greensf/greensf_jij_mz.hdf'), index=index))

    jij_constants = calculate_heisenberg_tensor(g, reference_atom=1, onsite_delta=ONSITE_DELTA)

    assert isinstance(jij_constants, pd.DataFrame)
    print(jij_constants.head())
    dataframe_regression.check(jij_constants, basename='test_jij_tensor')


def test_jij_tensor_x(test_file, dataframe_regression):
    """
    Test of the Jij constant calculations magnetic moment in x-direction
    """
    from masci_tools.tools.greensf_calculations import calculate_heisenberg_tensor, decompose_jij_tensor

    jij_constants = calculate_heisenberg_tensor(test_file('fleur/greensf/greensf_jij_mx.hdf'),
                                                reference_atom=1,
                                                onsite_delta=ONSITE_DELTA)

    assert isinstance(jij_constants, pd.DataFrame)
    decompose_jij_tensor(jij_constants, 'x')
    dataframe_regression.check(jij_constants)


def test_jij_tensor_y(test_file, dataframe_regression):
    """
    Test of the Jij constant calculations magnetic moment in y-direction
    """
    from masci_tools.tools.greensf_calculations import calculate_heisenberg_tensor, decompose_jij_tensor

    jij_constants = calculate_heisenberg_tensor(test_file('fleur/greensf/greensf_jij_my.hdf'),
                                                reference_atom=1,
                                                onsite_delta=ONSITE_DELTA)

    assert isinstance(jij_constants, pd.DataFrame)
    decompose_jij_tensor(jij_constants, 'y')
    dataframe_regression.check(jij_constants)


def test_jij_tensor_max_shells(test_file, dataframe_regression):
    """
    Test of the Jij constant calculations
    """
    from masci_tools.tools.greensf_calculations import calculate_heisenberg_tensor

    jij_constants = calculate_heisenberg_tensor(test_file('fleur/greensf/greensf_jij_mz.hdf'),
                                                reference_atom=1,
                                                onsite_delta=ONSITE_DELTA,
                                                max_shells=1)

    assert isinstance(jij_constants, pd.DataFrame)
    dataframe_regression.check(jij_constants)
