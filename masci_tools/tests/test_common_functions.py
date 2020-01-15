# -*- coding: utf-8 -*-
"""
@author: ruess
"""
from __future__ import division

from __future__ import absolute_import
from builtins import object
import pytest
from masci_tools.io.common_functions import (interpolate_dos, get_alat_from_bravais,
                                             search_string, angles_to_vec,
                                             vec_to_angles, get_version_info,
                                             get_corestates_from_potential,
                                             get_highest_core_state,
                                             get_ef_from_potfile, open_general,
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
        assert l1==l2
        assert l2>0

    def test_interpolate_dos(self):
        from numpy import load, loadtxt, shape
        d0 = '../tests/files/interpol/complex.dos'
        ef, dos, dos_int = interpolate_dos(d0, return_original=True)
        assert ef == 0.5256
        dos_ref = loadtxt('../tests/files/interpol/new3.dos')
        assert (dos_int.reshape(shape(dos_ref))-dos_ref).max()<10**-4
        assert (dos == load('../tests/files/interpol/ref_dos.npy')).all()

    def test_interpolate_dos_filehandle(self):
        from numpy import load, loadtxt, shape
        d0 = open('../tests/files/interpol/complex.dos')
        d0 = '../tests/files/interpol/complex.dos'
        ef, dos, dos_int = interpolate_dos(d0, return_original=True)
        assert ef == 0.5256
        dos_ref = loadtxt('../tests/files/interpol/new3.dos')
        assert (dos_int.reshape(shape(dos_ref))-dos_ref).max()<10**-4
        assert (dos == load('../tests/files/interpol/ref_dos.npy')).all()

    def test_get_alat_from_bravais(self):
        from numpy import array, sqrt
        bravais = array([[0.0, 0.5, 0.5], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]])
        alat = get_alat_from_bravais(bravais)
        assert abs(alat - sqrt(2)/2) < 10**-10

    def test_search_string(self):
        txt = open('files/kkr/kkr_run_dos_output/output.0.txt', 'r').readlines()
        alatline = search_string('ALAT', txt)
        noline = search_string('ALT', txt)
        assert alatline == 23
        assert noline == -1

    def test_angles_to_vec(self):
        from numpy import pi, sqrt, array, sum
        vec = angles_to_vec(2., 45./180.*pi, 45./180.*pi)
        assert abs(vec[0] - 1.) < 10**-10
        assert abs(vec[1] - 1.) < 10**-10
        assert abs(vec[2] - sqrt(2)) < 10**-10
        vec = angles_to_vec(array([2., 3.]), array([45./180.*pi, pi]), array([45./180.*pi, pi/2]))
        assert sum(abs(vec - array([[1., 1., sqrt(2)], [0, 0, -3]]))) < 10**-10

    def test_vec_to_angles(self):
        from numpy import array, sqrt, sum, pi
        m, t, p = vec_to_angles(array([[0, 0, 1], [1, 1, sqrt(2)]]))
        assert sum(abs(m - array([1, 2]))) < 10**-10
        assert sum(abs(t - array([0, pi/4.]))) < 10**-10
        assert sum(abs(p - array([0, pi/4.]))) < 10**-10
        m, t, p = vec_to_angles([1, 1, sqrt(2)])
        assert (m, t, p) == (2, pi/4., pi/4.)

    def test_get_version_info(self):
        version = get_version_info('files/kkr/kkr_run_dos_output/output.0.txt')
        assert version == ('v2.2-22-g4f8f5ff', 'openmp-mac', 'kkrjm_v2.2-22-g4f8f5ff_openmp-mac_20171214102522')

    def test_get_corestates_from_potential(self):
        from numpy import sum, array
        corestates = get_corestates_from_potential('files/kkr/kkr_run_dos_output/out_potential')
        ref = ([8, 8, 8, 8],
               [array([-1866.96096949,  -275.8348967 ,   -50.32089052,    -6.5316706 , -248.12312965,   -41.13200278,    -3.832432  ,   -26.5129925 ]),
                array([-1866.96096949,  -275.8348967 ,   -50.32089052,    -6.5316706 , -248.12312965,   -41.13200278,    -3.832432  ,   -26.5129925 ]),
                array([-1866.96096949,  -275.8348967 ,   -50.32089052,    -6.5316706 , -248.12312965,   -41.13200278,    -3.832432  ,   -26.5129925 ]),
                array([-1866.96096949,  -275.8348967 ,   -50.32089052,    -6.5316706 , -248.12312965,   -41.13200278,    -3.832432  ,   -26.5129925 ])],
               [array([0, 0, 0, 0, 1, 1, 1, 2]),
                array([0, 0, 0, 0, 1, 1, 1, 2]),
                array([0, 0, 0, 0, 1, 1, 1, 2]),
                array([0, 0, 0, 0, 1, 1, 1, 2])])
        assert corestates[0] == ref[0]
        assert sum(abs(array(corestates[1]) - array(ref[1]))) < 10**-7
        assert sum(abs(array(corestates[2]) - array(ref[2]))) < 10**-7

    def test_get_highest_core_state(self):
        from numpy import array
        ncore = 8
        ener = array([-1866.96096949,  -275.8348967 ,   -50.32089052,    -6.5316706 , -248.12312965,   -41.13200278,    -3.832432  ,   -26.5129925 ])
        lval = array([0, 0, 0, 0, 1, 1, 1, 2])
        out = get_highest_core_state(ncore, ener, lval)
        assert out == (1, -3.832432, '4p')

    def test_get_ef_from_potfile(self):
        ef = get_ef_from_potfile('files/kkr/kkr_run_dos_output/out_potential')
        assert ef == 1.05

    def test_convert_to_pystd(self):
        import numpy as np
        test = {'list': [0,1,2], 'nparray': np.array([0,1,2]), 'nparray_conv_list': list(np.array([0,1,2])), 
                'int': 9, 'float': 0.9, 'np.int': np.int64(8), 'np.float': np.float128(9), 
                'dict':{'list':[0,1,2], 'nparray': np.array([0,1,2]), 'nparray_conv_list': list(np.array([0,1,2])),
                        'int': 9, 'float': 0.9, 'np.int': np.int64(8), 'np.float': np.float128(9), 
                        'dict':{'list':[0,1,2], 'nparray': np.array([0,1,2]), 'nparray_conv_list': list(np.array([0,1,2])),
                                'int': 9, 'float': 0.9, 'np.int': np.int64(8), 'np.float': np.float128(9)}
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
            if i=='list':
                out0 = []
            print(i, type(ii))
            out0.append(type(ii))
            if i in ['list', 'nparray', 'nparray_conv_list']:
                for j in ii:
                    print(j, type(j))
                    out0.append(type(j))
            # converted datatypes:
            ii = test1[i]
            if i=='list':
                out = []
            print(i, type(ii))
            out.append(type(ii))
            if i in ['list', 'nparray', 'nparray_conv_list']:
                for j in ii:
                    print(j, type(j))
                    out.append(type(j))

        # now compare datatypes:
        assert out0 == [list, int, int, int, np.ndarray, np.int64, np.int64,
                        np.int64, list, int, int, int, int, float, np.int64, np.float128]
        assert out == [list, int, int, int, list, int, int, int, list, int, int, int, int, float, int, float]


