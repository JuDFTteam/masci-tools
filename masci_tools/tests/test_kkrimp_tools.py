#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import pytest
from masci_tools.io.modify_potential import modify_potential
from masci_tools.io.parsers.kkrimp_parser_functions import KkrimpParserFunctions


class Test_modify_potential(object):
    """ Tests for the modify_potential class functions. """

    def test_shapefun_from_scoef(self, file_regression):
        shapefun_path = '../tests/files/mod_pot/test2/shapefun'
        scoefpath = '../tests/files/mod_pot/test2/scoef'
        atom2shapes = [1]
        shapefun_new = '../tests/files/mod_pot/test2/shapefun_new'
        modify_potential().shapefun_from_scoef(scoefpath, shapefun_path, atom2shapes, shapefun_new)
        txt = open(shapefun_new).read().strip()
        file_regression.check(txt)

    def test_neworder_potential_no_replace(self, file_regression):
        path = '../tests/files/mod_pot/test1/'
        pot = path + 'pot'
        out_pot = path + 'pot_new'
        neworder = [0, 1, 2]
        # test 1: neworder_potential standard
        modify_potential().neworder_potential(pot, out_pot, neworder)
        txt = open(out_pot).read().strip()
        file_regression.check(txt)

    def test_neworder_potential_with_replace(self, file_regression):
        path = '../tests/files/mod_pot/test1/'
        pot1 = path + 'out_potential'
        pot2 = path + 'pot'
        out_pot = path + 'pot_new'
        neworder = [0, 1, 2]
        # test 2: neworder_potential with replace from second potential
        replace_newpos = [[0, 0], [2, 0]]
        modify_potential().neworder_potential(pot1, out_pot, neworder, potfile_2=pot2, replace_from_pot2=replace_newpos)
        txt = open(out_pot).read().strip()
        file_regression.check(txt)


class Test_KkrimpParserFunctions(object):
    """ Tests for the KKRimp parser functions. """

    def test_parse_outfiles_full(self, data_regression):
        path = 'files/kkrimp_parser/test1/'
        files = {}
        files['outfile'] = path + 'out_kkrimp'
        files['out_log'] = path + 'out_log.000.txt'
        files['out_pot'] = path + 'out_potential'
        files['out_enersp_at'] = path + 'out_energysp_per_atom_eV'
        files['out_enertot_at'] = path + 'out_energytotal_per_atom_eV'
        files['out_timing'] = path + 'out_timing.000.txt'
        files['kkrflex_llyfac'] = path + 'out_timing.000.txt'
        files['kkrflex_angles'] = path + 'out_timing.000.txt'
        files['out_spinmoms'] = path + 'out_magneticmoments.txt'
        files['out_orbmoms'] = path + 'out_magneticmoments.txt'
        s, m, o = KkrimpParserFunctions().parse_kkrimp_outputfile({}, files, debug=True)
        print('files:', files)
        print('\nsuccess?\n{}\n'.format(s))
        print('\nmessages?\n{}\n'.format(m))
        print('\nout_dict?\n{}\n'.format(o))

        assert s
        assert m == []
        data_regression.check(o)

    def test_parse_outfiles_full_filehandle(self, data_regression):
        path = 'files/kkrimp_parser/test1/'
        files = {}
        files['outfile'] = open(path + 'out_kkrimp')
        files['out_log'] = open(path + 'out_log.000.txt')
        files['out_pot'] = open(path + 'out_potential')
        files['out_enersp_at'] = open(path + 'out_energysp_per_atom_eV')
        files['out_enertot_at'] = open(path + 'out_energytotal_per_atom_eV')
        files['out_timing'] = open(path + 'out_timing.000.txt')
        files['kkrflex_llyfac'] = open(path + 'out_timing.000.txt')  # file not there yet and not parsed
        files['kkrflex_angles'] = open(path + 'out_timing.000.txt')  # file not there yet and not parsed
        files['out_spinmoms'] = open(path + 'out_timing.000.txt')  # file not there yet and not parsed
        files['out_orbmoms'] = open(path + 'out_timing.000.txt')  # file not there yet and not parsed
        s, m, o = KkrimpParserFunctions().parse_kkrimp_outputfile({}, files)
        print('files:', files)
        print('\nsuccess?\n{}\n'.format(s))
        print('\nmessages?\n{}\n'.format(m))
        print('\nout_dict?\n{}\n'.format(o))

        assert s
        assert m == []
        data_regression.check(o)

    def test_parse_file_errors(self):
        files = {}
        files['outfile'] = 'no_file_there'
        files['out_log'] = 'no_file_there'
        files['out_pot'] = 'no_file_there'
        files['out_enersp_at'] = 'no_file_there'
        files['out_enertot_at'] = 'no_file_there'
        files['out_timing'] = 'no_file_there'
        files['kkrflex_llyfac'] = 'no_file_there'
        files['kkrflex_angles'] = 'no_file_there'
        files['out_spinmoms'] = 'no_file_there'
        files['out_orbmoms'] = 'no_file_there'
        s, m, o = KkrimpParserFunctions().parse_kkrimp_outputfile({}, files, debug=True)
        print('\nsuccess?\n{}\n'.format(s))
        print('\nmessages?\n{}\n'.format(m))
        print('\nout_dict?\n{}\n'.format(o))
        assert not s
        assert set(m) == set([
            'Error parsing output of KKRimp: Version Info', 'Error parsing output of KKRimp: rms-error',
            'Error parsing output of KKRimp: nspin/natom', 'Error parsing output of KKRimp: total magnetic moment',
            'Error parsing output of KKRimp: spin moment per atom', 'Error parsing output of KKRimp: orbital moment',
            'Error parsing output of KKRimp: EF', 'Error parsing output of KKRimp: total energy',
            'Error parsing output of KKRimp: search for warnings', 'Error parsing output of KKRimp: timings',
            'Error parsing output of KKRimp: single particle energies', 'Error parsing output of KKRimp: charges',
            'Error parsing output of KKRimp: energy contour', 'Error parsing output of KKRimp: core_states',
            'Error parsing output of KKRimp: scfinfo'
        ])
        assert o == {'convergence_group': {}}
