#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 16:43:31 2017

@author: ruess
"""
import pytest
from masci_tools.io.kkr_params import kkrparams
from masci_tools.io.common_functions import open_general
import tempfile
import os

# helper functions


def check_full_dict(p, p0):
    """
    helper function that compares full dictionary
    """
    from numpy import ndarray, array
    for key in [i[0] for i in p.get_set_values()]:
        v = p.get_value(key)
        v0 = p0.get_value(key)
        if not isinstance(v, list) and not isinstance(v, ndarray):
            if v != v0:
                print(key, v, v0)
            assert v == v0
        elif not isinstance(v[0], str):
            if abs(array(v) - array(v0)).max() >= 10**-14:
                print(key, abs(array(v) - array(v0)).max())
            assert abs(array(v) - array(v0)).max() < 10**-14
        else:
            if set(v) - set(v0) != set():
                print(key, set(v) - set(v0))
            assert set(v) - set(v0) == set()


# tests


class Test_create_and_set_keys(object):  # pylint: disable=missing-class-docstring

    def test_create_params_with_inital_values(self):
        p = kkrparams(RBASIS=[0, 0, 0], params_type='voronoi')
        assert isinstance(p, kkrparams)
        assert p.values['<RBASIS>'] == [0, 0, 0]

    def test_default_values(self):
        p = kkrparams()
        assert p.values['EMIN'] is None

    def test_set_single_value(self):
        p = kkrparams()
        p.set_value('EMIN', 2)
        assert p.values['EMIN'] == 2.
        assert p.values['EMAX'] is None

    def test_set_multiple_values(self):
        p = kkrparams()
        p.set_multiple_values(EMIN=1, EMAX=2)
        assert p.values['EMIN'] == 1.
        assert p.values['EMAX'] == 2.


class Test_capture_wrong_input(object):  # pylint: disable=missing-class-docstring

    def test_wrong_input_type(self):
        p = kkrparams()
        with pytest.raises(TypeError):
            p.set_value('EMIN', '2')

        with pytest.raises(TypeError):
            p.set_value('EMIN', False)

    def test_wrong_input_array_dimension(self):
        p = kkrparams()
        from numpy import array, sqrt
        bravais = array([[0.7071067812, -0.5, 0.0], [0.7071067812, 0.5, 0.0], [sqrt(2), 0.0, 0.866025404]])

        # atom positions in relative coordinates
        basis_vectors = []
        for iatom in range(6):
            tmp = array([0, 0, 0]) + iatom * array([0.5, 0.5, bravais[2, 2]])
            tmp[0] = tmp[0] % 1
            tmp[1] = tmp[1] % 1
            print(iatom, tmp)
            basis_vectors.append(tmp)
        basis_vectors = array(basis_vectors)
        p.set_value('INTERFACE', True)
        p.set_value('<RBLEFT>', array([[1, 1], [0, 1]]))

    def test_input_consistency_check_fail(self):

        p = kkrparams(ZATOM=29.,
                      LMAX=2,
                      NAEZ=1,
                      BRAVAIS=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                      RMAX=7,
                      GMAX=65,
                      NSPIN=2,
                      RBASIS=[0, 0, 0],
                      ALATBASIS=1)
        p.set_value('LDAU_PARA', [1, 2])
        with pytest.raises(TypeError):
            p._check_input_consistency()

    def test_inconsistency_bulk_mode_bravais(self):
        p = kkrparams(LMAX=2,
                      NAEZ=1,
                      BRAVAIS=[[1, 0, 0], [0, 1, 0], [0, 0, 0]],
                      NSPIN=2,
                      RBASIS=[0, 0, 0],
                      ALATBASIS=1,
                      RMAX=7,
                      GMAX=65,
                      ZATOM=29.)
        with pytest.raises(ValueError):
            p.fill_keywords_to_inputfile()


class Test_get_info(object):  # pylint: disable=missing-class-docstring

    def test_get_mandatory(self):
        p = kkrparams()
        manlist = p.get_all_mandatory()
        assert set(manlist) == set(
            ['LMAX', 'NAEZ', 'BRAVAIS', 'RMAX', 'GMAX', 'NSPIN', '<RBASIS>', 'ALATBASIS', '<ZATOM>'])

    def test_get_set_values(self):
        p = kkrparams()
        setlist = p.get_set_values()
        assert setlist == []

    def test_get_set_values2(self):
        from numpy import array
        p = kkrparams()
        p.set_multiple_values(EMIN=1, EMAX=2)
        setlist = p.get_set_values()
        assert set(array(setlist).flatten()) == set(array([['EMIN', 1.], ['EMAX', 2.]]).flatten())

    def test_get_description(self):
        p = kkrparams()
        desc = p.get_description('EMIN')
        assert desc == 'Accuracy, Valence energy contour: Lower value (in Ryd) for the energy contour'

    def test_get_type(self):
        p = kkrparams()
        tlist = p.get_type('BRAVAIS')
        assert tlist == [float, float, float, float, float, float, float, float, float]

    def test_is_mandatory(self):
        p = kkrparams()
        man = p.is_mandatory('EMAX')
        assert not man

    def test_get_value(self):
        p = kkrparams(LMAX=3)
        # check for KeyError if wrong key is checked
        with pytest.raises(KeyError):
            p.get_value('something_wrong')

        # check for returning unset value
        npol = p.get_value('NPOL')
        assert npol is None
        # check correct LMAX value
        lmax = p.get_value('LMAX')
        assert lmax == 3
        # check for returning lists for RUNOPT and TESTOPT
        runopt = p.get_value('RUNOPT')
        testopt = p.get_value('TESTOPT')
        assert runopt == []
        assert testopt == []
        p = kkrparams(TESTOPT=['test1', 'test2'], RUNOPT=['NEWSOSOL'])
        runopt = p.get_value('RUNOPT')
        testopt = p.get_value('TESTOPT')
        assert runopt == ['NEWSOSOL']
        assert set(testopt) == set(['test1', 'test2'])


class Test_fill_inputfile(object):
    """
    Tests checking writing an input file
    """

    def test_fill_inputfile_filehandle(self, file_regression):
        p = kkrparams(params_type='kkrimp')
        p.set_multiple_values(CALCORBITALMOMENT=0,
                              RUNFLAG='',
                              QBOUND=10**-7,
                              NSPIN=1,
                              TESTFLAG='',
                              NPAN_EQ=7,
                              CALCFORCE=0,
                              NPAN_LOGPANELFAC=2,
                              SPINORBIT=0,
                              ITDBRY=20,
                              NPAN_LOG=5,
                              INS=1,
                              ICST=2,
                              CALCJIJMAT=0,
                              NCHEB=10,
                              HFIELD=[0.00, 0],
                              BRYMIX=0.05,
                              KVREL=1,
                              IMIX=0,
                              RADIUS_MIN=-1,
                              NCOLL=0,
                              RADIUS_LOGPANELS=0.6,
                              MIXFAC=0.05,
                              SCFSTEPS=1,
                              XC='LDA-VWN')
        with tempfile.NamedTemporaryFile('r') as tmp:
            p.fill_keywords_to_inputfile(output=tmp.name)
            file_content = tmp.read()

        file_regression.check(file_content)

    def test_fill_inputfile_minimal_Voronoi(self, file_regression):
        p = kkrparams(ZATOM=29.,
                      LMAX=2,
                      NAEZ=1,
                      BRAVAIS=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                      RCLUSTZ=1.5,
                      NSPIN=2,
                      RBASIS=[0, 0, 0],
                      ALATBASIS=1)
        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as td:
            os.chdir(td)
            p.fill_keywords_to_inputfile(is_voro_calc=True)
            file_content = open('inputcard').read()
            os.chdir(cwd)

        file_regression.check(file_content)

    def test_fill_inputfile_KKR(self, file_regression):
        p = kkrparams(ZATOM=29.,
                      LMAX=2,
                      NAEZ=1,
                      BRAVAIS=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                      RMAX=7,
                      GMAX=65,
                      RCLUSTZ=1.5,
                      NSPIN=2,
                      RBASIS=[0, 0, 0],
                      ALATBASIS=1)
        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as td:
            os.chdir(td)
            p.fill_keywords_to_inputfile()
            file_content = open('inputcard').read().strip()
            os.chdir(cwd)

        file_regression.check(file_content)

    def test_fill_inputfile_empty_check(self):
        p = kkrparams(LMAX=2, NAEZ=1)

        with pytest.raises(ValueError):
            p.fill_keywords_to_inputfile()

    def test_fill_inputfile_all_keys(self):
        """Example filling all keys"""
        from numpy import array, sqrt

        alat = 5.416871386
        naez = 6
        bravais = array([[0.7071067812, -0.5, 0.0], [0.7071067812, 0.5, 0.0], [sqrt(2), 0.0, 0.866025404]])
        lmax = 2
        nspin = 2
        nucl_numbers = [0, 0, 26, 27, 26, 27, 0, 0]
        cpa_info = [naez + 2, [1., 1., 0.98, 0.02, 0.98, 0.02, 1., 1.], [1, 2, 3, 3, 4, 4, 5, 6]]
        npol = 4
        npt1, npt2, npt3 = 3, 10, 3
        tempr = 800
        basis_vectors = []
        for iatom in range(naez):
            tmp = array([0, 0, 0]) + iatom * array([0.5, 0.5, bravais[2, 2]])
            tmp[0] = tmp[0] % 1
            tmp[1] = tmp[1] % 1
            print(iatom, tmp)
            basis_vectors.append(tmp)
        basis_vectors = array(basis_vectors)
        natyp = cpa_info[0]
        cpa_conc = cpa_info[1]
        cpa_sites = cpa_info[2]
        ins = 1
        kshape = ins
        rmax, gmax = 7, 65
        rcls = 1.5
        bzdivide = [10, 10, 0]
        emin = -0.4
        p = kkrparams()
        p.set_multiple_values(ZATOM=nucl_numbers, RBASIS=basis_vectors, BRAVAIS=bravais, NAEZ=naez, ALATBASIS=alat)
        p.set_multiple_values(NSPIN=nspin, LMAX=lmax, NPOL=npol, NPT1=npt1, NPT2=npt2, NPT3=npt3, TEMPR=tempr)
        p.set_multiple_values(RMAX=rmax, GMAX=gmax)
        p.set_multiple_values(RCLUSTZ=rcls, BZDIVIDE=bzdivide, EMIN=emin)
        p.set_multiple_values(INS=ins, KSHAPE=kshape)
        p.set_multiple_values(INTERFACE=True,
                              NLBASIS=1,
                              NRBASIS=1,
                              ZPERIODL=array([-0.5, -0.5, -bravais[2, 2]]),
                              ZPERIODR=array([0.5, 0.5, bravais[2, 2]]),
                              RBLEFT=basis_vectors[0] + array([-0.5, -0.5, -bravais[2, 2]]),
                              RBRIGHT=basis_vectors[naez - 1] + array([0.5, 0.5, bravais[2, 2]]))
        p.set_value('LINIPOL', True)
        p.set_value('XINIPOL', [1 for i in range(natyp)])
        p.set_value('HFIELD', 0.02)
        p.set_value('NSTEPS', 1)
        p.set_value('IMIX', 0)
        p.set_value('STRMIX', 0.01)
        p.set_value('CARTESIAN', False)
        p.set_multiple_values(KAOEZR=1,
                              KAOEZL=1,
                              FPRADIUS=[-1 for i in range(natyp)],
                              RCLUSTXY=rcls,
                              TKSEMI=800,
                              EMAX=1,
                              NPOLSEMI=0,
                              N2SEMI=0,
                              N1SEMI=0,
                              N3SEMI=0,
                              FSEMICORE=0,
                              KVREL=1,
                              NCHEB=7,
                              VCONST=0,
                              SOCSCL=[1 for i in range(natyp)],
                              LAMBDA_XC=1,
                              FCM=20,
                              ITDBRY=20,
                              KREADLDAU=0,
                              RUNOPT=['LDAU', 'SEMICORE', 'IRGENDWAS FALSCHES'],
                              TESTOPT=[
                                  'TSTOPTX0', 'TSTOPTX1', 'TSTOPTX2', 'TSTOPTX3', 'TSTOPTX4', 'TSTOPTX5', 'TSTOPTX6',
                                  'TSTOPTX7', 'TSTOPTX8', 'TSTOPTXYZZZZZZ'
                              ],
                              QBOUND=10**-3,
                              NPAN_LOG=3,
                              NPAN_EQ=4,
                              CPAINFO=[10**-3, 20],
                              LLOYD=0,
                              EMUSEMI=0,
                              ICST=2,
                              TOLRDIF=0.01,
                              BRYMIX=0.01,
                              EBOTSEMI=0,
                              NRIGHTHO=10,
                              KEXCOR=2,
                              NLEFTHOS=10,
                              R_LOG=0.4,
                              LDAU_PARA=[1, 2, 0, 0, 0],
                              NAT_LDAU=0,
                              RMTREFL=2.3,
                              RMTREFR=2.3,
                              DELTAE=[10**-5, 0],
                              RMTREF=[2.3 for i in range(natyp)])
        p.set_value('<SHAPE>', [1 for i in range(natyp)])
        p.set_multiple_values(NATYP=natyp, SITE=cpa_sites)
        p.set_value('<CPA-CONC>', cpa_conc)
        p.set_value('FILES', ['output.pot', ''])
        with tempfile.NamedTemporaryFile() as tmp:
            p.fill_keywords_to_inputfile(is_voro_calc=True, output=tmp.name)

    def test_set_rmtcore(self):
        #test rmtcore
        from numpy import array
        from masci_tools.io.common_functions import search_string

        para_dict = dict([(u'INS', 0), (u'RCLUSTZ', 1.69), (u'LMAX', 2), (u'GMAX', 65.0),
                          (u'<RMTCORE>', [0.3535533906, 0.3535533906, 0.3535533906, 0.3535533906]), (u'RMAX', 7.0),
                          (u'NSPIN', 1)])
        zatom = array([47., 47., 47., 47.])
        alat = 7.8692316414074615
        natom = 4
        positions = array([[0., 0., 0.], [0., 0.5, 0.5], [0.5, 0., 0.5], [0.5, 0.5, 0.]])
        bravais = array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
        k = kkrparams(**para_dict)
        k.set_multiple_values(ZATOM=zatom, NAEZ=natom, ALATBASIS=alat, RBASIS=positions, BRAVAIS=bravais)
        with tempfile.NamedTemporaryFile('r') as tmp:
            k.fill_keywords_to_inputfile(output=tmp.name)
            txt = tmp.readlines()

        naez = int(txt[search_string('NAEZ', txt)].split()[-1])
        rmtcore = []
        l_offset = search_string('RMTCORE', txt)
        for iatom in range(naez):
            rmtcore_at = float(txt[l_offset + 1 + iatom].split()[-1])
            rmtcore.append(rmtcore_at)
        maxdiff = (max(abs(array(para_dict['<RMTCORE>']) - array(rmtcore))))
        assert maxdiff < 10**-6

    def test_set_kkrimp_params_full(self, file_regression):
        p = kkrparams(params_type='kkrimp')
        p.set_multiple_values(CALCORBITALMOMENT=0,
                              RUNFLAG='',
                              QBOUND=10**-7,
                              NSPIN=1,
                              TESTFLAG='',
                              NPAN_EQ=7,
                              CALCFORCE=0,
                              NPAN_LOGPANELFAC=2,
                              SPINORBIT=0,
                              ITDBRY=20,
                              NPAN_LOG=5,
                              INS=1,
                              ICST=2,
                              CALCJIJMAT=0,
                              NCHEB=10,
                              HFIELD=[0.00, 0],
                              BRYMIX=0.05,
                              KVREL=1,
                              IMIX=0,
                              RADIUS_MIN=-1,
                              NCOLL=0,
                              RADIUS_LOGPANELS=0.6,
                              MIXFAC=0.05,
                              SCFSTEPS=1,
                              XC='LDA-VWN')
        with tempfile.NamedTemporaryFile('r') as tmp:
            p.fill_keywords_to_inputfile(output=tmp.name)
            file_content = tmp.read()

        file_regression.check(file_content)


class Test_read_inputfile(object):  # pylint: disable=missing-class-docstring

    def test_read_minimal_inputfile(self):
        p = kkrparams(ZATOM=26.,
                      LMAX=2,
                      NAEZ=1,
                      BRAVAIS=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                      RCLUSTZ=1.5,
                      NSPIN=2,
                      RBASIS=[0, 0, 0],
                      ALATBASIS=1)
        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as td:
            os.chdir(td)
            p.fill_keywords_to_inputfile(is_voro_calc=True)
            p2 = kkrparams(params_type='voronoi')
            p2.read_keywords_from_inputcard()
            os.chdir(cwd)

        check_full_dict(p, p2)

    def test_read_unsorted_inputfile(self):
        p = kkrparams(ZATOM=26.,
                      LMAX=2,
                      NAEZ=1,
                      BRAVAIS=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                      RCLUSTZ=1.5,
                      NSPIN=2,
                      RBASIS=[0, 0, 0],
                      ALATBASIS=1,
                      RMAX=7,
                      GMAX=65)
        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as td:
            os.chdir(td)
            p.fill_keywords_to_inputfile(output='input.temp.txt')
            txt = open('input.temp.txt', 'r').readlines()
            # exchange some lines
            tmp = txt[0]
            txt[0] = txt[5]
            txt[5] = tmp
            tmp = txt[-1]
            txt[-1] = txt[-2]
            txt[-2] = tmp
            tmp = txt[-2]
            txt[-2] = txt[-4]
            txt[-4] = tmp
            tmp = txt[-3]
            txt[-3] = txt[-1]
            txt[-1] = tmp
            with open('input.temp_unsorted.txt', 'w') as f:
                f.writelines(txt)
            p2 = kkrparams()
            p2.read_keywords_from_inputcard(inputcard='input.temp_unsorted.txt')
            print(p2.get_dict())
            print(dict(p2.get_set_values()))
            check_full_dict(p, p2)
            os.chdir(cwd)

    def test_read_slab(self, data_regression):
        from numpy import array, ndarray
        from masci_tools.io.common_functions import get_aBohr2Ang
        p = kkrparams(params_type='kkr')

        # automatically read keywords from inpucard
        p.read_keywords_from_inputcard(inputcard='../tests/files/kkr/import_calc_old_style/inputcard')
        # convert some read-in stuff back from Ang. units to alat units
        rbl = p.get_value('<RBLEFT>')
        rbr = p.get_value('<RBRIGHT>')
        zper_l = p.get_value('ZPERIODL')
        zper_r = p.get_value('ZPERIODR')
        ang2alat = 1 / (p.get_value('ALATBASIS') * get_aBohr2Ang())
        if rbl is not None:
            p.set_value('<RBLEFT>', array(rbl) * ang2alat)
        if rbr is not None:
            p.set_value('<RBRIGHT>', array(rbr) * ang2alat)
        if zper_l is not None:
            p.set_value('ZPERIODL', array(zper_l) * ang2alat)
        if zper_r is not None:
            p.set_value('ZPERIODR', array(zper_r) * ang2alat)

        # check all values, replace arrays by lists to make data-regression work
        d_check = p.get_dict()
        for k, v in d_check.items():
            if type(v) == ndarray:
                d_check[k] = v.tolist()
        data_regression.check(d_check)


class Test_other(object):  # pylint: disable=missing-class-docstring

    def test_get_missing_keys(self):
        p = kkrparams()
        missing = p.get_missing_keys()
        assert set(missing) == set(
            ['<ZATOM>', 'BRAVAIS', 'LMAX', 'GMAX', 'RMAX', 'NAEZ', '<RBASIS>', 'NSPIN', 'ALATBASIS'])
        missing = p.get_missing_keys(use_aiida=True)
        assert set(missing) == set(['LMAX', 'GMAX', 'RMAX', 'NSPIN'])

        p = kkrparams(params_type='voronoi', EMIN=-2, LMAX=3)
        missing = p.get_missing_keys()
        assert set(missing) == set(['<ZATOM>', 'BRAVAIS', 'RCLUSTZ', 'NAEZ', '<RBASIS>', 'NSPIN', 'ALATBASIS'])

    def test_set_value_None(self):
        p = kkrparams()
        p.set_value('EMIN', -1)
        assert p.values['EMIN'] == -1

        p.set_value('EMIN', None)
        assert p.values['EMIN'] == -1

        p.remove_value('EMIN')
        assert p.values['EMIN'] is None

    def test_set_potname_empty(self):
        from masci_tools.io.common_functions import search_string
        p = kkrparams()
        p.set_multiple_values(RMAX=1,
                              GMAX=1,
                              NSPIN=1,
                              RBASIS=[0, 0, 0],
                              LMAX=2,
                              RCLUSTZ=1.2,
                              NAEZ=1,
                              ZATOM=[0],
                              BRAVAIS=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                              ALATBASIS=1,
                              FILES=['', 'shapenew'])
        with tempfile.NamedTemporaryFile('r') as tmp:
            p.fill_keywords_to_inputfile(output=tmp.name)
            txt = tmp.readlines()
        itmp = search_string('FILES', txt)
        potname = txt[itmp + 2].split()[0]
        shapename = txt[itmp + 4].split()[0]
        assert potname == 'potential'
        assert shapename == 'shapenew'

    def test_get_dict(self, data_regression):
        p = kkrparams()
        p.set_multiple_values(RMAX=1,
                              GMAX=1,
                              NSPIN=1,
                              RBASIS=[0, 0, 0],
                              LMAX=2,
                              RCLUSTZ=1.2,
                              NAEZ=1,
                              ZATOM=[0],
                              BRAVAIS=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                              ALATBASIS=1,
                              FILES=['', 'shapenew'])
        data_regression.check(p.get_dict())

        l0 = [
            '<SHAPE>', 'KSHAPE', 'ZPERIODL', '<NRBASIS>', '<NLBASIS>', '<RBASIS>', 'NAEZ', 'CARTESIAN', '<RBRIGHT>',
            '<RBLEFT>', 'INTERFACE', 'BRAVAIS', 'ALATBASIS', 'ZPERIODR'
        ]
        assert set(p.get_dict(group='lattice').keys()) == set(l0)

        l0 = ['ZPERIODL', '<NRBASIS>', '<NLBASIS>', '<RBRIGHT>', '<RBLEFT>', 'INTERFACE', 'ZPERIODR']
        assert set(l0) == set(p.get_dict(group='lattice', subgroup='2D mode').keys())

    def test_get_KKRcalc_parameter_defaults(self):
        d = kkrparams.get_KKRcalc_parameter_defaults()
        from masci_tools.io.kkr_params import __kkr_default_params__
        d0 = __kkr_default_params__
        assert d[0] == d0
