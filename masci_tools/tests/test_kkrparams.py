#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 16:43:31 2017

@author: ruess
"""

import pytest
from masci_tools.io.kkr_params import kkrparams
    
        
# helper functions

def check_full_dict(p,p0):
    """
    helper function that compares full dictionary
    """
    from numpy import ndarray, array
    for key in [i[0] for i in p.get_set_values()]:
        v = p.get_value(key)
        v0 = p0.get_value(key)
        if type(v) != list and type(v) != ndarray:
            if v!=v0:
                print(key, v, v0)
            assert v==v0
        elif type(v[0]) != str:
            if abs(array(v)-array(v0)).max()>=10**-14:
                print(key, abs(array(v)-array(v0)).max())
            assert abs(array(v)-array(v0)).max()<10**-14
        else:
            if set(v)-set(v0)!=set():
                print(key, set(v)-set(v0))
            assert set(v)-set(v0)==set()

# tests
    

class Test_create_and_set_keys():
    def test_create_params_with_inital_values(self):
        p = kkrparams(RBASIS=[0,0,0], params_type='voronoi')
        assert type(p)==kkrparams
        assert p.values['<RBASIS>'] == [0,0,0]
    
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
        assert p.values['EMIN']== 1.
        assert p.values['EMAX']== 2.

    
class Test_capture_wrong_input():
    def test_wrong_input_type(self):
        p = kkrparams()
        known_error = False
        try:
            p.set_value('EMIN', '2')
        except TypeError:
            known_error = True
        assert known_error
        
        known_error = False
        try:
            p.set_value('EMIN', False)
        except TypeError:
            known_error = True
        assert known_error
        
    def test_wrong_input_array_dimension(self):
        p = kkrparams()
        from numpy import array, sqrt
        bravais = array([[0.7071067812, -0.5, 0.0], [0.7071067812, 0.5, 0.0], [sqrt(2), 0.0, 0.866025404]])
        
        # atom positions in relative coordinates
        basis_vectors = []
        for iatom in range(6):
            tmp = array([0, 0, 0])+iatom*array([0.5, 0.5, bravais[2, 2]])
            tmp[0] = tmp[0]%1
            tmp[1] = tmp[1]%1
            print(iatom, tmp)
            basis_vectors.append(tmp)
        basis_vectors = array(basis_vectors)
        p.set_value('INTERFACE', True)
        p.set_value('<RBLEFT>', array([[1,1],[0,1]]))
        
    def test_input_consistency_check_fail(self):
        knownError = False
        try: 
            p = kkrparams(ZATOM=29., LMAX=2, NAEZ=1, BRAVAIS=[[1,0,0],[0,1,0],[0,0,1]], RMAX=7, GMAX=65, NSPIN=2, RBASIS=[0,0,0], ALATBASIS=1)
            p.set_value('LDAU_PARA', [1,2])
            p._check_input_consistency()
        except TypeError:
           knownError = True
        assert knownError

    def test_inconsistency_bulk_mode_bravais(self):
        p = kkrparams(LMAX=2, NAEZ=1, BRAVAIS=[[1,0,0],[0,1,0],[0,0,0]], NSPIN=2, RBASIS=[0,0,0], ALATBASIS=1, RMAX=7, GMAX=65, ZATOM=29.)
        knownError = False
        try:
            p.fill_keywords_to_inputfile()
        except ValueError:
            knownError = True
        assert knownError
    
        
class Test_get_info():
    def test_get_mandatory(self):
        p = kkrparams()
        manlist = p.get_all_mandatory()
        assert set(manlist)==set(['LMAX', 'NAEZ', 'BRAVAIS', 'RMAX', 'GMAX', 'NSPIN', '<RBASIS>', 'ALATBASIS', '<ZATOM>'])
        
    def test_get_set_values(self):
        p = kkrparams()
        setlist = p.get_set_values()
        assert setlist==[]
        
    def test_get_set_values2(self):
        from numpy import array
        p = kkrparams()
        p.set_multiple_values(EMIN=1, EMAX=2)
        setlist = p.get_set_values()
        assert set(array(setlist).flatten()) == set(array([['EMIN', 1.], ['EMAX', 2.]]).flatten())
        
    def test_get_description(self):
        p = kkrparams()
        desc = p.get_description('EMIN')
        assert desc=='Accuracy, Valence energy contour: Lower value (in Ryd) for the energy contour'
        
    def test_get_type(self):
        p = kkrparams()
        tlist = p.get_type('BRAVAIS')
        assert tlist == [float, float, float, float, float, float, float, float, float]
        
    def test_is_mandatory(self):
        p = kkrparams()
        man = p.is_mandatory('EMAX')
        assert (not man)
        
    def test_get_value(self):
        p = kkrparams(LMAX=3)
        # check for KeyError if wrong key is checked
        known_error = False
        try:
            p.get_value('something_wrong')
        except KeyError:
            known_error = True
        assert known_error
        # check for returning unset value
        npol = p.get_value('NPOL')
        assert npol == None
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
        

    
class Test_fill_inputfile():
    def test_fill_inputfile_minimal_Voronoi(self):
        p = kkrparams(ZATOM=29., LMAX=2, NAEZ=1, BRAVAIS=[[1,0,0],[0,1,0],[0,0,1]], RCLUSTZ=1.5, NSPIN=2, RBASIS=[0,0,0], ALATBASIS=1)
        p.fill_keywords_to_inputfile(is_voro_calc=True)
        txt = open('inputcard').readlines()
        ref = ['ALATBASIS= 1.00000000000000\n', 'BRAVAIS\n', '1.00000000000000 0.00000000000000 0.00000000000000\n',
               '0.00000000000000 1.00000000000000 0.00000000000000\n', '0.00000000000000 0.00000000000000 1.00000000000000\n', 'NAEZ= 1\n', '<RBASIS>\n',
               '0.00000000000000 0.00000000000000 0.00000000000000\n', '<ZATOM>\n', '29.00000000000000\n', 'NSPIN= 2\n', 'LMAX= 2\n', 'RCLUSTZ= 1.50000000000000\n']
        done=False
        while not done:
            try:
                txt.remove('\n')
            except ValueError:
                done = True
        assert len(txt)==len(ref)
        txt.sort()
        ref.sort()
        print(txt, ref)
        for i in range(len(txt)):
            print(i, txt[i], ref[i])
            assert set(txt[i].split())==set(ref[i].split()) 
            
    def test_fill_inputfile_KKR(self):
        reffile = ['ALATBASIS= 1.00000000000000\n', 'BRAVAIS\n', '1.00000000000000 0.00000000000000 0.00000000000000\n', '<ZATOM>\n', '29.00000000000000\n',
                   '0.00000000000000 1.00000000000000 0.00000000000000\n', '0.00000000000000 0.00000000000000 1.00000000000000\n', 'NAEZ= 1\n',
                   '<RBASIS>\n', '0.00000000000000 0.00000000000000 0.00000000000000\n', 'NSPIN= 2\n', 'LMAX= 2\n', 
                   'RCLUSTZ= 1.50000000000000\n', 'RMAX=      7.00000000000000\n', 'GMAX=      65.00000000000000\n']
        p = kkrparams(ZATOM=29., LMAX=2, NAEZ=1, BRAVAIS=[[1,0,0],[0,1,0],[0,0,1]], RMAX=7, GMAX=65, RCLUSTZ=1.5, NSPIN=2, RBASIS=[0,0,0], ALATBASIS=1)
        p.fill_keywords_to_inputfile()
        txt = open('inputcard').readlines()
        done=False
        while not done:
            try:
                txt.remove('\n')
            except ValueError:
                done = True
        assert len(txt)==len(reffile)
        txt.sort()
        reffile.sort()
        for i in range(len(txt)):
            assert set(txt[i].split())==set(reffile[i].split())
        
    def test_fill_inputfile_empty_check(self):
        p = kkrparams(LMAX=2, NAEZ=1)
        known_error = False
        try:
            p.fill_keywords_to_inputfile()
        except ValueError:
            known_error = True
        assert known_error
        
    def test_fill_inputfile_all_keys(self):  
        """Example filling all keys"""      
        from numpy import array, sqrt
       
        alat=5.416871386
        naez=6
        bravais=array([[0.7071067812, -0.5, 0.0], [0.7071067812, 0.5, 0.0], [sqrt(2), 0.0, 0.866025404]])
        lmax=2
        nspin=2
        nucl_numbers=[0,0,26,27,26,27,0,0]
        cpa_info = [naez+2, [1., 1., 0.98, 0.02, 0.98, 0.02, 1., 1.], [1, 2, 3, 3, 4, 4, 5, 6]]
        npol=4
        npt1, npt2, npt3 = 3, 10, 3
        tempr= 800
        basis_vectors = []
        for iatom in range(naez):
            tmp = array([0, 0, 0])+iatom*array([0.5, 0.5, bravais[2, 2]])
            tmp[0] = tmp[0]%1
            tmp[1] = tmp[1]%1
            print(iatom, tmp)
            basis_vectors.append(tmp)
        basis_vectors = array(basis_vectors)
        natyp = cpa_info[0]
        cpa_conc = cpa_info[1]
        cpa_sites = cpa_info[2]
        ins=1
        kshape=ins
        rmax, gmax= 7, 65
        rcls=1.5
        bzdivide=[10,10,0]
        emin=-0.4
        p = kkrparams()
        p.set_multiple_values(ZATOM=nucl_numbers, RBASIS=basis_vectors, BRAVAIS=bravais, NAEZ=naez, ALATBASIS=alat)
        p.set_multiple_values(NSPIN=nspin, LMAX=lmax, NPOL=npol, NPT1=npt1, NPT2=npt2, NPT3=npt3, TEMPR=tempr)
        p.set_multiple_values(RMAX=rmax, GMAX=gmax)
        p.set_multiple_values(RCLUSTZ=rcls, BZDIVIDE=bzdivide, EMIN=emin)
        p.set_multiple_values(INS=ins, KSHAPE=kshape)
        p.set_multiple_values(INTERFACE=True, NLBASIS=1, NRBASIS=1,
                              ZPERIODL=array([-0.5, -0.5, -bravais[2, 2]]), 
                              ZPERIODR=array([0.5, 0.5, bravais[2, 2]]), 
                              RBLEFT=basis_vectors[0]+array([-0.5, -0.5, -bravais[2, 2]]), 
                              RBRIGHT=basis_vectors[naez-1]+array([0.5, 0.5, bravais[2, 2]]))
        p.set_value('LINIPOL', True)
        p.set_value('XINIPOL', [1 for i in range(natyp)])
        p.set_value('HFIELD', 0.02)
        p.set_value('NSTEPS', 1)
        p.set_value('IMIX', 0)
        p.set_value('STRMIX', 0.01)
        p.set_value('CARTESIAN', False)
        p.set_multiple_values(KAOEZR=1, KAOEZL=1, FPRADIUS=[-1 for i in range(natyp)], RCLUSTXY=rcls, 
                              TKSEMI=800,EMAX=1, NPOLSEMI=0, N2SEMI=0, N1SEMI=0, N3SEMI=0, FSEMICORE=0, 
                              KVREL=1, NCHEB=7, VCONST=0, SOCSCL=[1 for i in range(natyp)], 
                              LAMBDA_XC=1, FCM=20, ITDBRY=20, KREADLDAU=0, RUNOPT=['LDAU', 'SEMICORE', 'IRGENDWAS FALSCHES'],
                              TESTOPT=['TSTOPTX0', 'TSTOPTX1', 'TSTOPTX2', 'TSTOPTX3', 'TSTOPTX4', 'TSTOPTX5', 'TSTOPTX6', 'TSTOPTX7', 'TSTOPTX8', 'TSTOPTXYZZZZZZ'], QBOUND=10**-3, 
                              NPAN_LOG=3, NPAN_EQ=4, CPAINFO=[10**-3, 20], LLOYD=0, EMUSEMI=0, ICST=2, 
                              TOLRDIF=0.01, BRYMIX=0.01, EBOTSEMI=0, NRIGHTHO=10, KEXCOR=2, NLEFTHOS=10,
                              R_LOG=0.4, LDAU_PARA=[1, 2, 0, 0, 0], NAT_LDAU=0, 
                              RMTREFL=2.3, RMTREFR=2.3, DELTAE=[10**-5, 0], RMTREF=[2.3 for i in range(natyp)])
        p.set_value('<SHAPE>', [1 for i in range(natyp)])
        p.set_multiple_values(NATYP=natyp, SITE=cpa_sites)
        p.set_value('<CPA-CONC>', cpa_conc)
        p.set_value('FILES', ['output.pot', ''])
        p.fill_keywords_to_inputfile(is_voro_calc=True)
        
    def test_set_rmtcore(self):
        #test rmtcore
        from numpy import array
        from masci_tools.io.common_functions import search_string
        
        para_dict = dict([(u'INS', 0),
            (u'RCLUSTZ', 1.69),
            (u'LMAX', 2),
            (u'GMAX', 65.0),
            (u'<RMTCORE>', [0.3535533906, 0.3535533906, 0.3535533906, 0.3535533906]),
            (u'RMAX', 7.0),
            (u'NSPIN', 1)])
        zatom = array([ 47.,  47.,  47.,  47.])
        alat = 7.8692316414074615
        natom = 4
        positions = array([[ 0. ,  0. ,  0. ],
                           [ 0. ,  0.5,  0.5],
                           [ 0.5,  0. ,  0.5],
                           [ 0.5,  0.5,  0. ]])
        bravais = array([[ 1.,  0.,  0.],
                         [ 0.,  1.,  0.],
                         [ 0.,  0.,  1.]])
        k =kkrparams(**para_dict)
        k.set_multiple_values(ZATOM=zatom, NAEZ=natom, ALATBASIS=alat, RBASIS=positions, BRAVAIS=bravais)
        k.fill_keywords_to_inputfile()
        
        txt = open('inputcard').readlines()
        naez = int(txt[search_string('NAEZ', txt)].split()[-1])
        rmtcore = []
        l_offset = search_string('RMTCORE', txt)
        for iatom in range(naez):
            rmtcore_at = float(txt[l_offset+1+iatom].split()[-1])
            rmtcore.append(rmtcore_at)
        maxdiff = (max(abs(array(para_dict['<RMTCORE>']) - array(rmtcore))))
        assert maxdiff < 10**-6
         
    def test_set_kkrimp_params_full(self):
        p = kkrparams(params_type='kkrimp')
        p.set_multiple_values(CALCORBITALMOMENT=0, RUNFLAG='', QBOUND=10**-7, NSPIN=1, 
                              TESTFLAG='', NPAN_EQ=7, CALCFORCE=0, NPAN_LOGPANELFAC=2, 
                              SPINORBIT=0, ITDBRY=20, NPAN_LOG=5, INS=1, ICST=2, 
                              CALCJIJMAT=0, NCHEB=10, HFIELD=[0.00, 0], BRYMIX=0.05, 
                              KVREL=1, IMIX=0, RADIUS_MIN=-1, NCOLL=0, RADIUS_LOGPANELS=0.6, 
                              MIXFAC=0.05, SCFSTEPS=1, XC='LDA-VWN')
        p.fill_keywords_to_inputfile(output='config.cfg')
        reftxt = ['RUNFLAG=\n', 'TESTFLAG=\n', '\n', 'INS= 1\n', 'KVREL= 1\n', 'NSPIN= 1\n', '\n', 'SCFSTEPS= 1\n', 'IMIX= 0\n', 'ITDBRY= 20\n', 'MIXFAC=      0.05000000000000\n', 'BRYMIX=      0.05000000000000\n', 'QBOUND= 1.000000e-07\n', '\n', 'XC= LDA-VWN\n', 'ICST= 2\n', 'SPINORBIT= 0\n', 'NCOLL= 0\n', 'NPAN_LOGPANELFAC= 2\n', 'RADIUS_LOGPANELS=      0.60000000000000\n', 'RADIUS_MIN= -1\n', 'NPAN_LOG= 5\n', 'NPAN_EQ= 7\n', 'NCHEB= 10\n', '\n', 'HFIELD=      0.00000000000000 0\n', '\n', 'CALCORBITALMOMENT= 0\n', 'CALCFORCE= 0\n', 'CALCJIJMAT= 0\n']
        txt = open('config.cfg').readlines()
        assert txt==reftxt
        
               
class Test_read_inputfile():
    def test_read_minimal_inputfile(self):
        p = kkrparams(ZATOM=26., LMAX=2, NAEZ=1, BRAVAIS=[[1,0,0],[0,1,0],[0,0,1]], RCLUSTZ=1.5, NSPIN=2, RBASIS=[0,0,0], ALATBASIS=1)
        p.fill_keywords_to_inputfile(is_voro_calc=True)
        p2 = kkrparams(params_type='voronoi')
        p2.read_keywords_from_inputcard()
        check_full_dict(p,p2)
        
    def test_read_unsorted_inputfile(self):
        p = kkrparams(ZATOM=26., LMAX=2, NAEZ=1, BRAVAIS=[[1,0,0],[0,1,0],[0,0,1]], RCLUSTZ=1.5, NSPIN=2, RBASIS=[0,0,0], ALATBASIS=1, RMAX=7, GMAX=65)
        p.fill_keywords_to_inputfile(output='input.temp.txt')
        txt = open('input.temp.txt', 'r').readlines()
        # exchange some lines
        tmp = txt[0]; txt[0] = txt[5]; txt[5]=tmp
        tmp = txt[-1]; txt[-1] = txt[-2]; txt[-2]=tmp
        tmp = txt[-2]; txt[-2] = txt[-4]; txt[-4]=tmp
        tmp = txt[-3]; txt[-3] = txt[-1]; txt[-1]=tmp
        open('input.temp_unsorted.txt', 'w').writelines(txt)
        p2 = kkrparams()
        p2.read_keywords_from_inputcard(inputcard='input.temp_unsorted.txt')
        print(p2.get_dict())
        print(dict(p2.get_set_values()))
        check_full_dict(p,p2)
        
    def test_read_slab(self):
        from numpy import array
        from masci_tools.io.common_functions import get_Ang2aBohr
        p = kkrparams(params_type='kkr')
        
        # automatically read keywords from inpucard
        p.read_keywords_from_inputcard(inputcard='../tests/files/kkr/import_calc_old_style/inputcard')
        # convert some read-in stuff back from Ang. units to alat units
        rbl = p.get_value('<RBLEFT>')
        rbr = p.get_value('<RBRIGHT>')
        zper_l = p.get_value('ZPERIODL')
        zper_r = p.get_value('ZPERIODR')
        ang2alat = get_Ang2aBohr()/p.get_value('ALATBASIS')
        if rbl is not None: p.set_value('<RBLEFT>', array(rbl)*ang2alat)
        if rbr is not None: p.set_value('<RBRIGHT>', array(rbr)*ang2alat)
        if zper_l is not None: p.set_value('ZPERIODL', array(zper_l)*ang2alat)
        if zper_r is not None: p.set_value('ZPERIODR', array(zper_r)*ang2alat)
        
        # set parameters of expected values manually
        p0 = kkrparams(RUNOPT=['xigid-ef','LLOYD', 'ewald2d', 'NEWSOSOL', 'DOS'], TESTOPT=['ie','RMESH','clusters','MPIenerg','fullBZ','DOS'], LMAX=3, NSPIN=2, NATYP=80, NAEZ=80, CARTESIAN=True, ALATBASIS=20.156973053, BRAVAIS=[[0.38437499, 0., 0.], [0.19218749, -0.33287851, 0.], [0.19218749, -0.11095950, 1.]], INTERFACE=True, NRIGHTHO=10, NLEFTHOS=10, NLBASIS=10, NRBASIS=10, ZPERIODL=[-1.92187500000000e-01, 1.10959504859881e-01, -1.00000000000000e+00], ZPERIODR=[1.92187500000000e-01, -1.10959504859881e-01, 1.00000000000000e+00], RCLUSTZ=0.65, RCLUSTXY=0.65, EMIN=-1.2, EMAX=1.2, TEMPR=473., NPOL=7, NPT1=7, NPT2=40, NPT3=6, KSHAPE=2, INS=1, ICST=2, KEXCOR=2, HFIELD=0, VCONST=0, NPAN_LOG=17, NPAN_EQ=7, NCHEB=12, R_LOG=0.8, BZDIVIDE=[40, 40, 1], NSTEPS=500, IMIX=5, STRMIX=0.02, FCM=20., QBOUND=10**-7, BRYMIX=0.02, ITDBRY=30, LINIPOL=False, FILES=['potential', 'shapefun'], RMAX=15., GMAX=900.)
        p0.set_value('<ZATOM>', [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 52.0, 0.0, 51.0, 0.0, 52.0, 0.0, 51.0, 0.0, 52.0, 0.0, 52.0, 0.0, 51.0, 0.0, 52.0, 0.0, 51.0, 0.0, 52.0, 0.0, 52.0, 0.0, 51.0, 0.0, 52.0, 0.0, 51.0, 0.0, 52.0, 0.0, 52.0, 0.0, 51.0, 0.0, 52.0, 0.0, 51.0, 0.0, 52.0, 0.0, 52.0, 0.0, 51.0, 0.0, 52.0, 0.0, 51.0, 0.0, 52.0, 0.0, 52.0, 0.0, 51.0, 0.0, 52.0, 0.0, 51.0, 0.0, 52.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        p0.set_value('<SHAPE>', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        p0.set_multiple_values(KAOEZR=[i for i in range(1,11)], KAOEZL=[i for i in range(1,11)], KVREL=1, RMTREFL=[2.2671000, 2.2671000, 2.4948000, 2.3562000, 2.3562000, 2.3562000, 2.4948000, 2.2671000, 2.2671000, 2.5740000], RMTREFR=[2.2671000, 2.2671000, 2.4948000, 2.3562000, 2.3562000, 2.3562000, 2.4948000, 2.2671000, 2.2671000, 2.5740000])
        p0.set_multiple_values(RMTREF=[2.2671000, 2.2671000, 2.4948000, 2.3562000, 2.3562000, 2.3562000, 2.4948000, 2.2671000, 2.2671000, 2.5740000, 2.2671000, 2.2671000, 2.4948000, 2.3562000, 2.3562000, 2.3562000, 2.4948000, 2.2671000, 2.2671000, 2.5740000, 2.2671000, 2.2671000, 2.4948000, 2.3562000, 2.3562000, 2.3562000, 2.4948000, 2.2671000, 2.2671000, 2.5740000, 2.2671000, 2.2671000, 2.4948000, 2.3562000, 2.3562000, 2.3562000, 2.4948000, 2.2671000, 2.2671000, 2.5740000, 2.2671000, 2.2671000, 2.4948000, 2.3562000, 2.3562000, 2.3562000, 2.4948000, 2.2671000, 2.2671000, 2.5740000, 2.2671000, 2.2671000, 2.4948000, 2.3562000, 2.3562000, 2.3562000, 2.4948000, 2.2671000, 2.2671000, 2.5740000, 2.2671000, 2.2671000, 2.4948000, 2.3562000, 2.3562000, 2.3562000, 2.4948000, 2.2671000, 2.2671000, 2.5740000, 2.2671000, 2.2671000, 2.4948000, 2.3562000, 2.3562000, 2.3562000, 2.4948000, 2.2671000, 2.2671000, 2.5740000])
        p0.set_multiple_values(RBLEFT=[[-1.92187500000000e-01,  1.10959504859881e-01, -1.00000000000000e+00], [ 8.32667268468867e-17,  2.77555756156289e-17, -9.49500000000000e-01], [ 1.92187500000000e-01, -1.10959504859881e-01, -8.33000000000000e-01], [ 3.84375000000000e-01, -2.21919009719762e-01, -7.16500000000000e-01], [ 8.32667268468867e-17,  0.00000000000000e+00, -6.33000000000000e-01], [ 1.92187500000000e-01, -1.10959504859881e-01, -5.49500000000000e-01],  [ 3.84375000000000e-01, -2.21919009719762e-01, -4.33000000000000e-01], [ 2.77555756156289e-17,  1.38777878078145e-17, -3.16500000000000e-01], [ 1.92187500000000e-01, -1.10959504859881e-01, -2.66000000000000e-01], [ 3.84375000000000e-01, -2.21919009719762e-01, -1.33000000000000e-01]],
                               RBRIGHT=[[1.53750000000000e+00, -8.87676038879049e-01,  8.00000000000000e+00], [1.72968750000000e+00, -9.98635543738930e-01,  8.05050000000000e+00], [1.92187500000000e+00, -1.10959504859881e+00,  8.16700000000000e+00], [2.11406250000000e+00, -1.22055455345869e+00,  8.28350000000000e+00], [1.72968750000000e+00, -9.98635543738930e-01,  8.36700000000000e+00], [1.92187500000000e+00, -1.10959504859881e+00,  8.45050000000000e+00], [2.11406250000000e+00, -1.22055455345869e+00,  8.56700000000000e+00], [1.72968750000000e+00, -9.98635543738930e-01,  8.68350000000000e+00], [1.92187500000000e+00, -1.10959504859881e+00,  8.73400000000000e+00], [2.11406250000000e+00, -1.22055455345869e+00,  8.86700000000000e+00]],
                               RBASIS=[[0.0, 0.0, 0.0], [0.1921875, -0.110959504859881, 0.0505000000000001], [0.384375, -0.221919009719762, 0.167], [0.5765625, -0.332878514579644, 0.2835], [0.1921875, -0.110959504859881, 0.367], [0.384375, -0.221919009719762, 0.4505], [0.5765625, -0.332878514579644, 0.567], [0.1921875, -0.110959504859881, 0.6835], [0.384375, -0.221919009719762, 0.734], [0.5765625, -0.332878514579644, 0.867], [0.1921875, -0.110959504859881, 1.0], [0.384375, -0.221919009719762, 1.0505], [0.5765625, -0.332878514579643, 1.167], [0.76875, -0.443838019439525, 1.2835], [0.384375, -0.221919009719762, 1.367], [0.5765625, -0.332878514579643, 1.4505], [0.76875, -0.443838019439525, 1.567], [0.384375, -0.221919009719762, 1.6835], [0.5765625, -0.332878514579643, 1.734], [0.76875, -0.443838019439525, 1.867], [0.384375, -0.221919009719762, 2.0], [0.5765625, -0.332878514579643, 2.0505], [0.76875, -0.443838019439525, 2.167], [0.9609375, -0.554797524299406, 2.2835], [0.5765625, -0.332878514579643, 2.367], [0.76875, -0.443838019439525, 2.4505], [0.9609375, -0.554797524299406, 2.567], [0.5765625, -0.332878514579643, 2.6835], [0.76875, -0.443838019439525, 2.734], [0.9609375, -0.554797524299406, 2.867], [0.5765625, -0.332878514579643, 3.0], [0.76875, -0.443838019439525, 3.0505], [0.9609375, -0.554797524299406, 3.167], [1.153125, -0.665757029159287, 3.2835], [0.76875, -0.443838019439525, 3.367], [0.9609375, -0.554797524299406, 3.4505], [1.153125, -0.665757029159287, 3.567], [0.76875, -0.443838019439525, 3.6835], [0.9609375, -0.554797524299406, 3.734], [1.153125, -0.665757029159287, 3.867], [0.76875, -0.443838019439525, 4.0], [0.9609375, -0.554797524299406, 4.0505], [1.153125, -0.665757029159287, 4.167], [1.3453125, -0.776716534019168, 4.2835], [0.9609375, -0.554797524299406, 4.367], [1.153125, -0.665757029159287, 4.4505], [1.3453125, -0.776716534019168, 4.567], [0.9609375, -0.554797524299406, 4.6835], [1.153125, -0.665757029159287, 4.734], [1.3453125, -0.776716534019168, 4.867], [0.9609375, -0.554797524299406, 5.0], [1.153125, -0.665757029159287, 5.0505], [1.3453125, -0.776716534019168, 5.167], [1.5375, -0.887676038879049, 5.2835], [1.153125, -0.665757029159287, 5.367], [1.3453125, -0.776716534019168, 5.4505], [1.5375, -0.887676038879049, 5.567], [1.153125, -0.665757029159287, 5.6835], [1.3453125, -0.776716534019168, 5.734], [1.5375, -0.887676038879049, 5.867], [1.153125, -0.665757029159287, 6.0], [1.3453125, -0.776716534019168, 6.0505], [1.5375, -0.887676038879049, 6.167], [1.7296875, -0.99863554373893, 6.2835], [1.3453125, -0.776716534019168, 6.367], [1.5375, -0.887676038879049, 6.4505], [1.7296875, -0.99863554373893, 6.567], [1.3453125, -0.776716534019168, 6.6835], [1.5375, -0.887676038879049, 6.734], [1.7296875, -0.99863554373893, 6.867], [1.3453125, -0.776716534019168, 7.0], [1.5375, -0.887676038879049, 7.0505], [1.7296875, -0.99863554373893, 7.167], [1.921875, -1.10959504859881, 7.2835], [1.5375, -0.887676038879049, 7.367], [1.7296875, -0.99863554373893, 7.4505], [1.921875, -1.10959504859881, 7.567], [1.5375, -0.887676038879049, 7.6835], [1.7296875, -0.99863554373893, 7.734], [1.921875, -1.10959504859881, 7.867]])
    
        # check all values
        check_full_dict(p,p0)
        
        
class Test_other():
    def test_get_missing_keys(self): 
        p = kkrparams()
        missing = p.get_missing_keys()
        assert set(missing)==set(['<ZATOM>', 'BRAVAIS', 'LMAX', 'GMAX', 'RMAX', 'NAEZ', '<RBASIS>', 'NSPIN', 'ALATBASIS'])
        missing = p.get_missing_keys(use_aiida=True)
        assert set(missing)==set(['LMAX', 'GMAX', 'RMAX', 'NSPIN'])
        
        p = kkrparams(params_type='voronoi', EMIN=-2, LMAX=3)
        missing = p.get_missing_keys()
        assert set(missing)==set(['<ZATOM>', 'BRAVAIS', 'RCLUSTZ', 'NAEZ', '<RBASIS>', 'NSPIN', 'ALATBASIS'])
    
    def test_set_value_None(self): 
        p = kkrparams()
        p.set_value('EMIN', -1)
        assert p.values['EMIN'] == -1
        
        p.set_value('EMIN',None)
        assert p.values['EMIN'] == -1
        
        p.remove_value('EMIN')
        assert p.values['EMIN'] is None
        
    def test_set_potname_empty(self):  
        p = kkrparams()
        p.set_multiple_values(RMAX=1, GMAX=1, NSPIN=1, RBASIS=[0,0,0], LMAX=2, RCLUSTZ=1.2, NAEZ=1, ZATOM=[0], BRAVAIS=[[1,0,0],[0,1,0],[0,0,1]], ALATBASIS=1, FILES=['','shapenew'])
        p.fill_keywords_to_inputfile()
        from masci_tools.io.common_functions import search_string
        txt = open('inputcard').readlines()
        itmp = search_string('FILES', txt)
        potname = txt[itmp+2].split()[0]
        shapename = txt[itmp+4].split()[0]
        assert 'potential' == potname
        assert 'shapenew' == shapename
    
    def test_get_dict(self):
        d0 = {'<RMTCORE>':  None, 'ICST': None, '<RMTREF>': None, 'N1SEMI': None, '<FPRADIUS>': None, '<NRBASIS>': None, '<SOCSCL>': None, 'XINIPOL': None, 'EMAX': None, '<RBLEFT>': None, 'NLEFTHOS': None, '<ZATOM>': [0.0], 'RCLUSTXY': None, 'NPAN_EQ': None, '<RBRIGHT>': None, 'BRAVAIS': [[1, 0, 0], [0, 1, 0], [0, 0, 1]], 'INS': None, 'NAT_LDAU': None, '<RMTREFR>': None, 'ZPERIODL': None, 'TESTOPT': None, 'KEXCOR': None, '<TOLRDIF>': None, 'TEMPR': None, 'EBOTSEMI': None, 'NATYP': None, 'RUNOPT': None, 'HFIELD': None, 'NPOL': None, 'RCLUSTZ': 1.2, 'ZPERIODR': None, 'N3SEMI': None, 'LMAX': 2, 'ITDBRY': None, '<KAOEZR>': None, '<LLOYD>': None, 'STRMIX': None, 'CPAINFO': None, 'FCM': None, '<SHAPE>': None, 'NPAN_LOG': None, 'CARTESIAN': None, 'FSEMICORE': None, 'LAMBDA_XC': None, 'GMAX': None, '<CPA-CONC>': None, 'RMAX': None, 'NCHEB': None, 'EMIN': None, 'NAEZ': 1, '<DELTAE>': None, 'KREADLDAU': None, '<RBASIS>': [0, 0, 0], '<SITE>': None, 'NPT2': None, 'NPT3': None, 'NPT1': None, 'N2SEMI': None, 'NPOLSEMI': None, '<RMTREFL>': None, 'FILES': ['', 'shapenew'], 'LDAU_PARA': None, 'NSPIN': 1, 'QBOUND': None, 'NRIGHTHO': None, 'KVREL': None, 'TKSEMI': None, '<KAOEZL>': None, 'NSTEPS': None, 'KSHAPE': None, '<NLBASIS>': None, 'LINIPOL': None, 'BZDIVIDE': None, 'INTERFACE': None, 'BRYMIX': None, 'EMUSEMI': None, 'ALATBASIS': 1.0, 'R_LOG': None, 'IMIX': None, 'VCONST': None, 'JIJRAD': None, 'JIJRADXY': None, 'JIJSITEI': None, 'JIJSITEJ': None}
        p = kkrparams()
        p.set_multiple_values(RMAX=1, GMAX=1, NSPIN=1, RBASIS=[0,0,0], LMAX=2, RCLUSTZ=1.2, NAEZ=1, ZATOM=[0], BRAVAIS=[[1,0,0],[0,1,0],[0,0,1]], ALATBASIS=1, FILES=['','shapenew'])
        assert set(d0.keys()) == set(p.get_dict().keys())
        
        l0 = ['<SHAPE>', 'KSHAPE', 'ZPERIODL', '<NRBASIS>', '<NLBASIS>', '<RBASIS>', 'NAEZ', 'CARTESIAN', '<RBRIGHT>', '<RBLEFT>', 'INTERFACE', 'BRAVAIS', 'ALATBASIS', 'ZPERIODR']
        assert p.get_dict(group='lattice').keys() == l0
        
        l0 = ['ZPERIODL', '<NRBASIS>', '<NLBASIS>', '<RBRIGHT>', '<RBLEFT>', 'INTERFACE', 'ZPERIODR']
        assert l0 == p.get_dict(group='lattice', subgroup='2D mode').keys() 
        
    def test_get_KKRcalc_parameter_defaults(self):
        d = kkrparams.get_KKRcalc_parameter_defaults()
        from masci_tools.io.kkr_params import __kkr_default_params__
        d0 = __kkr_default_params__
        assert d[0]==d0
