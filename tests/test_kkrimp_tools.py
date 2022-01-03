#!/usr/bin/env python3
"""
Test of kkrimp tools
"""
#import pytest
from masci_tools.io.modify_potential import modify_potential
from masci_tools.io.parsers.kkrimp_parser_functions import KkrimpParserFunctions
from pathlib import Path
import os

DIR = Path(__file__).parent.resolve()


class Test_modify_potential:
    """ Tests for the modify_potential class functions. """

    def test_shapefun_from_scoef(self, file_regression):
        shapefun_path = os.fspath(DIR / Path('files/mod_pot/test2/shapefun'))
        scoefpath = os.fspath(DIR / Path('files/mod_pot/test2/scoef'))
        atom2shapes = [1]
        shapefun_new = os.fspath(DIR / Path('files/mod_pot/test2/shapefun_new'))
        modify_potential().shapefun_from_scoef(scoefpath, shapefun_path, atom2shapes, shapefun_new)
        with open(shapefun_new, encoding='utf-8') as f:
            txt = f.read().strip()
        file_regression.check(txt)

    def test_neworder_potential_no_replace(self, file_regression):
        path = DIR / Path('files/mod_pot/test1/')
        pot = os.fspath(path / 'pot')
        out_pot = os.fspath(path / 'pot_new')
        neworder = [0, 1, 2]
        # test 1: neworder_potential standard
        modify_potential().neworder_potential(pot, out_pot, neworder)
        with open(out_pot, encoding='utf-8') as f:
            txt = f.read().strip()
        file_regression.check(txt)

    def test_neworder_potential_with_replace(self, file_regression):
        path = DIR / Path('files/mod_pot/test1/')
        pot1 = os.fspath(path / 'out_potential')
        pot2 = os.fspath(path / 'pot')
        out_pot = os.fspath(path / 'pot_new')
        neworder = [0, 1, 2]
        # test 2: neworder_potential with replace from second potential
        replace_newpos = [[0, 0], [2, 0]]
        modify_potential().neworder_potential(pot1, out_pot, neworder, potfile_2=pot2, replace_from_pot2=replace_newpos)
        with open(out_pot, encoding='utf-8') as f:
            txt = f.read().strip()
        file_regression.check(txt)


class Test_KkrimpParserFunctions:
    """ Tests for the KKRimp parser functions. """

    def test_parse_outfiles_full(self, data_regression):
        path = DIR / Path('files/kkrimp_parser/test1/')
        files = {}
        files['outfile'] = os.fspath(path / 'out_kkrimp')
        files['out_log'] = os.fspath(path / 'out_log.000.txt')
        files['out_pot'] = os.fspath(path / 'out_potential')
        files['out_enersp_at'] = os.fspath(path / 'out_energysp_per_atom_eV')
        files['out_enertot_at'] = os.fspath(path / 'out_energytotal_per_atom_eV')
        files['out_timing'] = os.fspath(path / 'out_timing.000.txt')
        files['kkrflex_llyfac'] = os.fspath(path / 'out_timing.000.txt')
        files['kkrflex_angles'] = os.fspath(path / 'out_timing.000.txt')
        files['out_spinmoms'] = os.fspath(path / 'out_magneticmoments.txt')
        files['out_orbmoms'] = os.fspath(path / 'out_magneticmoments.txt')
        s, m, o = KkrimpParserFunctions().parse_kkrimp_outputfile({}, files, debug=True)
        print('files:', files)
        print(f'\nsuccess?\n{s}\n')
        print(f'\nmessages?\n{m}\n')
        print(f'\nout_dict?\n{o}\n')

        assert s
        assert m == []
        data_regression.check(o)

    def test_parse_outfiles_full_filehandle(self, data_regression):
        path = DIR / Path('files/kkrimp_parser/test1/')
        files = {}

        with open(path / 'out_kkrimp', encoding='utf-8') as out_kkrimp:
            with open(path / 'out_log.000.txt', encoding='utf-8') as out_log:
                with open(path / 'out_potential', encoding='utf-8') as out_potential:
                    with open(path / 'out_energysp_per_atom_eV', encoding='utf-8') as out_energysp_per_atom_eV:
                        with open(path / 'out_energytotal_per_atom_eV',
                                  encoding='utf-8') as out_energytotal_per_atom_eV:
                            with open(path / 'out_timing.000.txt', encoding='utf-8') as out_timing:
                                files['outfile'] = out_kkrimp
                                files['out_log'] = out_log
                                files['out_pot'] = out_potential
                                files['out_enersp_at'] = out_energysp_per_atom_eV
                                files['out_enertot_at'] = out_energytotal_per_atom_eV
                                files['out_timing'] = out_timing
                                files['kkrflex_llyfac'] = out_timing  # file not there yet and not parsed
                                files['kkrflex_angles'] = out_timing  # file not there yet and not parsed
                                files['out_spinmoms'] = out_timing  # file not there yet and not parsed
                                files['out_orbmoms'] = out_timing  # file not there yet and not parsed
                                s, m, o = KkrimpParserFunctions().parse_kkrimp_outputfile({}, files)
        print('files:', files)
        print(f'\nsuccess?\n{s}\n')
        print(f'\nmessages?\n{m}\n')
        print(f'\nout_dict?\n{o}\n')

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
        print(f'\nsuccess?\n{s}\n')
        print(f'\nmessages?\n{m}\n')
        print(f'\nout_dict?\n{o}\n')
        assert not s
        assert set(m) == {
            'Error parsing output of KKRimp: Version Info', 'Error parsing output of KKRimp: rms-error',
            'Error parsing output of KKRimp: nspin/natom', 'Error parsing output of KKRimp: total magnetic moment',
            'Error parsing output of KKRimp: spin moment per atom', 'Error parsing output of KKRimp: orbital moment',
            'Error parsing output of KKRimp: EF', 'Error parsing output of KKRimp: total energy',
            'Error parsing output of KKRimp: search for warnings', 'Error parsing output of KKRimp: timings',
            'Error parsing output of KKRimp: single particle energies', 'Error parsing output of KKRimp: charges',
            'Error parsing output of KKRimp: energy contour', 'Error parsing output of KKRimp: core_states',
            'Error parsing output of KKRimp: scfinfo'
        }
        assert o == {'convergence_group': {}}
