# -*- coding: utf-8 -*-
"""
@author: ruess
"""
import pytest
import numpy as np
from masci_tools.io.common_functions import (interpolate_dos, get_alat_from_bravais, search_string, angles_to_vec,
                                             vec_to_angles, get_version_info, get_corestates_from_potential,
                                             get_highest_core_state, get_ef_from_potfile, open_general,
                                             convert_to_pystd)


class Test_common_functions(object):
    """
    Tests for the common functions from tools.common_functions
    """

    def test_open_general(self):
        path = '../tests/files/kkr/kkr_run_slab_nosoc/out_kkr'
        f = open_general(path)
        l1 = len(f.readlines())
        f = open_general(f)
        l2 = len(f.readlines())
        assert l1 == l2
        assert l2 > 0

    def test_interpolate_dos(self):
        d0 = '../tests/files/interpol/complex.dos'
        ef, dos, dos_int = interpolate_dos(d0, return_original=True)
        assert ef == 0.5256
        dos_ref = np.loadtxt('../tests/files/interpol/new3.dos')
        assert (dos_int.reshape(np.shape(dos_ref)) - dos_ref).max() < 10**-4
        assert (dos == np.load('../tests/files/interpol/ref_dos.npy')).all()

    def test_interpolate_dos_filehandle(self):
        d0 = open('../tests/files/interpol/complex.dos')
        d0 = '../tests/files/interpol/complex.dos'
        ef, dos, dos_int = interpolate_dos(d0, return_original=True)
        assert ef == 0.5256
        dos_ref = np.loadtxt('../tests/files/interpol/new3.dos')
        assert (dos_int.reshape(np.shape(dos_ref)) - dos_ref).max() < 10**-4
        assert (dos == np.load('../tests/files/interpol/ref_dos.npy')).all()

    def test_get_alat_from_bravais(self):
        bravais = np.array([[0.0, 0.5, 0.5], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]])
        alat = get_alat_from_bravais(bravais)
        assert abs(alat - np.sqrt(2) / 2) < 10**-10

    def test_search_string(self):
        txt = open('files/kkr/kkr_run_dos_output/output.0.txt', 'r').readlines()
        alatline = search_string('ALAT', txt)
        noline = search_string('ALT', txt)
        assert alatline == 23
        assert noline == -1

    def test_angles_to_vec(self):
        vec = angles_to_vec(2., 45. / 180. * np.pi, 45. / 180. * np.pi)
        assert abs(vec[0] - 1.) < 10**-10
        assert abs(vec[1] - 1.) < 10**-10
        assert abs(vec[2] - np.sqrt(2)) < 10**-10
        vec = angles_to_vec(np.array([2., 3.]), np.array([45. / 180. * np.pi, np.pi]),
                            np.array([45. / 180. * np.pi, np.pi / 2]))
        assert np.sum(abs(vec - np.array([[1., 1., np.sqrt(2)], [0, 0, -3]]))) < 10**-10

    def test_vec_to_angles(self):
        m, t, p = vec_to_angles(np.array([[0, 0, 1], [1, 1, np.sqrt(2)]]))
        assert np.sum(abs(m - np.array([1, 2]))) < 10**-10
        assert np.sum(abs(t - np.array([0, np.pi / 4.]))) < 10**-10
        assert np.sum(abs(p - np.array([0, np.pi / 4.]))) < 10**-10
        m, t, p = vec_to_angles([1, 1, np.sqrt(2)])
        assert (m, t, p) == (2, np.pi / 4., np.pi / 4.)

    def test_get_version_info(self):
        version = get_version_info('files/kkr/kkr_run_dos_output/output.0.txt')
        assert version == ('v2.2-22-g4f8f5ff', 'openmp-mac', 'kkrjm_v2.2-22-g4f8f5ff_openmp-mac_20171214102522')

    def test_get_corestates_from_potential(self):
        corestates = get_corestates_from_potential('files/kkr/kkr_run_dos_output/out_potential')
        ref = ([8, 8, 8, 8], [
            np.array([
                -1866.96096949, -275.8348967, -50.32089052, -6.5316706, -248.12312965, -41.13200278, -3.832432,
                -26.5129925
            ]),
            np.array([
                -1866.96096949, -275.8348967, -50.32089052, -6.5316706, -248.12312965, -41.13200278, -3.832432,
                -26.5129925
            ]),
            np.array([
                -1866.96096949, -275.8348967, -50.32089052, -6.5316706, -248.12312965, -41.13200278, -3.832432,
                -26.5129925
            ]),
            np.array([
                -1866.96096949, -275.8348967, -50.32089052, -6.5316706, -248.12312965, -41.13200278, -3.832432,
                -26.5129925
            ])
        ], [
            np.array([0, 0, 0, 0, 1, 1, 1, 2]),
            np.array([0, 0, 0, 0, 1, 1, 1, 2]),
            np.array([0, 0, 0, 0, 1, 1, 1, 2]),
            np.array([0, 0, 0, 0, 1, 1, 1, 2])
        ])
        assert corestates[0] == ref[0]
        assert np.sum(abs(np.array(corestates[1]) - np.array(ref[1]))) < 10**-7
        assert np.sum(abs(np.array(corestates[2]) - np.array(ref[2]))) < 10**-7

    def test_get_highest_core_state(self):
        ncore = 8
        ener = np.array([
            -1866.96096949, -275.8348967, -50.32089052, -6.5316706, -248.12312965, -41.13200278, -3.832432, -26.5129925
        ])
        lval = np.array([0, 0, 0, 0, 1, 1, 1, 2])
        out = get_highest_core_state(ncore, ener, lval)
        assert out == (1, -3.832432, '4p')

    def test_get_ef_from_potfile(self):
        ef = get_ef_from_potfile('files/kkr/kkr_run_dos_output/out_potential')
        assert ef == 1.05

    def test_convert_to_pystd(self):
        test = {
            'list': [0, 1, 2],
            'nparray': np.array([0, 1, 2]),
            'nparray_conv_list': list(np.array([0, 1, 2])),
            'int': 9,
            'float': 0.9,
            'np.int': np.int64(8),
            'np.float': np.float128(9),
            'dict': {
                'list': [0, 1, 2],
                'nparray': np.array([0, 1, 2]),
                'nparray_conv_list': list(np.array([0, 1, 2])),
                'int': 9,
                'float': 0.9,
                'np.int': np.int64(8),
                'np.float': np.float128(9),
                'dict': {
                    'list': [0, 1, 2],
                    'nparray': np.array([0, 1, 2]),
                    'nparray_conv_list': list(np.array([0, 1, 2])),
                    'int': 9,
                    'float': 0.9,
                    'np.int': np.int64(8),
                    'np.float': np.float128(9)
                }
            }
        }

        # make a copy and convert the dict
        test1 = test.copy()
        test1 = convert_to_pystd(test1)

        print('original ', test)
        print('converted', test1)

        # extract datatypes for comparison
        for i in ['list', 'nparray', 'nparray_conv_list', 'int', 'float', 'np.int', 'np.float']:
            ii = test[i]
            if i == 'list':
                out0 = []
            print(i, type(ii))
            out0.append(type(ii))
            if i in ['list', 'nparray', 'nparray_conv_list']:
                for j in ii:
                    print(j, type(j))
                    out0.append(type(j))
            # converted datatypes:
            ii = test1[i]
            if i == 'list':
                out = []
            print(i, type(ii))
            out.append(type(ii))
            if i in ['list', 'nparray', 'nparray_conv_list']:
                for j in ii:
                    print(j, type(j))
                    out.append(type(j))

        # now compare datatypes:
        assert out0 == [
            list, int, int, int, np.ndarray, np.int64, np.int64, np.int64, list, int, int, int, int, float, np.int64,
            np.float128
        ]
        assert out == [list, int, int, int, list, int, int, int, list, int, int, int, int, float, int, float]


TEST_PYTHON_VALUES = [True, False, 3.14, 4, 'str', 'TEST_STRING']
TEST_QUOTE_STRINGS = [False, False, False, False, False, True]
TEST_FORTRAN_STRING = ['.true.', '.false.', '  3.1400000000d+00', '4', 'str', "'TEST_STRING'"]


@pytest.mark.parametrize('value,expected_result,quote', zip(TEST_PYTHON_VALUES, TEST_FORTRAN_STRING,
                                                            TEST_QUOTE_STRINGS))
def test_convert_to_fortran(value, expected_result, quote):
    from masci_tools.io.common_functions import convert_to_fortran

    res = convert_to_fortran(value, quote_strings=quote)

    assert res == expected_result
