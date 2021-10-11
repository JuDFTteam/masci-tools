# -*- coding: utf-8 -*-
"""
@author: ruess
"""

# pylint: disable=E0602,W0602

import pytest
from masci_tools.io.parsers.kkrparser_functions import parse_kkr_outputfile, check_error_category
from pathlib import Path
import os

DIR = Path(__file__).parent.resolve()


class Test_kkr_parser_functions(object):
    """
    Tests for the kkr parser functions
    """

    grouping_ref = [
        'energy_contour_group', 'warnings_group', 'ewald_sum_group', 'timings_group', 'core_states_group',
        'convergence_group', 'magnetism_group', 'kmesh_group', 'symmetries_group', 'code_info_group'
    ]
    path0 = DIR / Path('files/kkr/kkr_run_slab_soc_simple/')
    outfile = os.fspath(path0 / 'out_kkr')
    outfile_0init = os.fspath(path0 / 'output.0.txt')
    outfile_000 = os.fspath(path0 / 'output.000.txt')
    timing_file = os.fspath(path0 / 'out_timing.000.txt')
    potfile_out = os.fspath(path0 / 'out_potential')
    nonco_out_file = os.fspath(path0 / 'nonco_angle_out.dat')

    def test_complete_kkr_output(self, data_regression):
        """
        Parse complete output of kkr calculation
        """
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, self.outfile, self.outfile_0init, self.outfile_000,
                                                           self.timing_file, self.potfile_out, self.nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert success
        assert msg_list == []
        groups = [i for i in list(out_dict.keys()) if 'group' in i]
        assert set(groups) == set(self.grouping_ref)
        data_regression.check(out_dict)

    def test_complete_kkr_output_filehandle(self, data_regression):
        """
        Parse complete output of kkr calculation but using file handles as done in aiida-kkr
        """
        out_dict = {}
        with open(self.outfile, encoding='utf-8') as outfile:
            with open(self.outfile_0init, encoding='utf-8') as outfile_0init:
                with open(self.outfile_000, encoding='utf-8') as outfile_000:
                    with open(self.timing_file, encoding='utf-8') as timing_file:
                        with open(self.potfile_out, encoding='utf-8') as potfile_out:
                            with open(self.nonco_out_file, encoding='utf-8') as nonco_out_file:
                                success, msg_list, out_dict = parse_kkr_outputfile(out_dict, outfile, outfile_0init,
                                                                                   outfile_000, timing_file,
                                                                                   potfile_out, nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert success
        assert msg_list == []
        groups = [i for i in list(out_dict.keys()) if 'group' in i]
        assert set(groups) == set(self.grouping_ref)
        data_regression.check(out_dict)

    def test_mag_orbmom_kkr_output(self, data_regression):
        """
        Parse complete output of kkr calculation with orbital moments
        """
        path0 = DIR / Path('files/kkr/kkr_run_slab_soc_mag/')
        outfile = os.fspath(path0 / 'out_kkr')
        outfile_0init = os.fspath(path0 / 'output.0.txt')
        outfile_000 = os.fspath(path0 / 'output.000.txt')
        timing_file = os.fspath(path0 / 'out_timing.000.txt')
        potfile_out = os.fspath(path0 / 'out_potential')
        nonco_out_file = os.fspath(path0 / 'nonco_angle_out.dat')
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, outfile, outfile_0init, outfile_000, timing_file,
                                                           potfile_out, nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert success
        assert msg_list == []
        data_regression.check(out_dict)

    def test_nosoc_kkr_output(self, data_regression):
        """
        Parse complete output of kkr calculation nosoc, magnetic
        """

        path0 = DIR / Path('files/kkr/kkr_run_slab_nosoc/')
        outfile = os.fspath(path0 / 'out_kkr')
        outfile_0init = os.fspath(path0 / 'output.0.txt')
        outfile_000 = os.fspath(path0 / 'output.000.txt')
        timing_file = os.fspath(path0 / 'out_timing.000.txt')
        potfile_out = os.fspath(path0 / 'out_potential')
        nonco_out_file = os.fspath(path0 / 'nonco_angle_out.dat')
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, outfile, outfile_0init, outfile_000, timing_file,
                                                           potfile_out, nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert success
        assert msg_list == []
        data_regression.check(out_dict)

    def test_missing_outfile(self):
        """
        Parse kkr output where out_kkr is missing. Compares error messages
        """
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, 'wrong_name', self.outfile_0init, self.outfile_000,
                                                           self.timing_file, self.potfile_out, self.nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert not success
        assert set(msg_list) == set([
            'Error parsing output of KKR: Version Info', 'Error parsing output of KKR: rms-error',
            'Error parsing output of KKR: charge neutrality', 'Error parsing output of KKR: total magnetic moment',
            'Error parsing output of KKR: spin moment per atom', 'Error parsing output of KKR: orbital moment',
            'Error parsing output of KKR: EF', 'Error parsing output of KKR: DOS@EF',
            'Error parsing output of KKR: total energy', 'Error parsing output of KKR: search for warnings',
            'Error parsing output of KKR: charges', 'Error parsing output of KKR: scfinfo'
        ])

    def test_missing_outfile0init(self):
        """
        Parse kkr output where output.0.txt is missing. Compares error messages
        """
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, self.outfile, 'wrong_name', self.outfile_000,
                                                           self.timing_file, self.potfile_out, self.nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert not success
        assert set(msg_list) == set([
            'Error parsing output of KKR: nspin/natom',
            'Error parsing output of KKR: spin moment per atom',
            'Error parsing output of KKR: orbital moment',
            'Error parsing output of KKR: energy contour',
            'Error parsing output of KKR: alat, 2*pi/alat',
            'Error parsing output of KKR: scfinfo',
            'Error parsing output of KKR: kmesh',
            'Error parsing output of KKR: symmetries',
            'Error parsing output of KKR: ewald summation for madelung poterntial',
            'Error parsing output of KKR: lattice vectors (direct/reciprocal)',
            'Error parsing output of KKR: noco angles rms value',
            'Error parsing output of KKR: BdG',
        ])

    def test_missing_outfile000(self):
        """
        Parse kkr output where output.000.txt is missing. Compares error messages
        """
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, self.outfile, self.outfile_0init, 'wrong_name',
                                                           self.timing_file, self.potfile_out, self.nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert not success
        assert set(msg_list) == set([
            'Error parsing output of KKR: rms-error', 'Error parsing output of KKR: single particle energies',
            'Error parsing output of KKR: charges', 'Error parsing output of KKR: scfinfo',
            'Error parsing output of KKR: kmesh'
        ])

    def test_missing_timingfile(self):
        """
        Parse kkr output where out_timing.000.txt is missing. Compares error messages
        """
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, self.outfile, self.outfile_0init, self.outfile_000,
                                                           'wrong_name', self.potfile_out, self.nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert not success
        assert msg_list == ['Error parsing output of KKR: timings']

    def test_missing_potfile(self):
        """
        Parse kkr output where out_potential is missing. Compares error messages
        """
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, self.outfile, self.outfile_0init, self.outfile_000,
                                                           self.timing_file, 'wrong_name', self.nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert not success
        assert msg_list == ['Error parsing output of KKR: core_states']

    def test_missing_nonco_angles(self):
        """
        Parse kkr output where out_potential is missing. Compares error messages
        """
        path0 = DIR / Path('files/kkr/kkr_run_slab_soc_mag/')
        outfile = os.fspath(path0 / 'out_kkr')
        outfile_0init = os.fspath(path0 / 'output.0.txt')
        outfile_000 = os.fspath(path0 / 'output.000.txt')
        timing_file = os.fspath(path0 / 'out_timing.000.txt')
        potfile_out = os.fspath(path0 / 'out_potential')
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, outfile, outfile_0init, outfile_000, timing_file,
                                                           potfile_out, 'wrong_name')
        out_dict['parser_warnings'] = msg_list
        assert not success
        assert msg_list == ['Error parsing output of KKR: spin moment per atom']

    def test_check_error_category(self):
        """
        Check check_error_category function used in parser after parse_kkr_outputfile is used
        """
        fname = 'nonco_angles_out.dat'
        err_cat, err_msg = (2, f'Error! NONCO_ANGLES_OUT not found {fname}')
        assert not check_error_category(err_cat, err_msg, {'use_newsosol': False})
        assert check_error_category(err_cat, err_msg, {'use_newsosol': True})

    def test_parse_dosout(self, data_regression):
        """
        Parse output of dos calculation since ouput changes slightly (e.g. no ewald sum)
        """
        path0 = DIR / Path('files/kkr/kkr_run_dos_output/')
        outfile = os.fspath(path0 / 'out_kkr')
        outfile_0init = os.fspath(path0 / 'output.0.txt')
        outfile_000 = os.fspath(path0 / 'output.000.txt')
        timing_file = os.fspath(path0 / 'out_timing.000.txt')
        potfile_out = os.fspath(path0 / 'out_potential')
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, outfile, outfile_0init, outfile_000, timing_file,
                                                           potfile_out, 'wrong_name')
        out_dict['parser_warnings'] = msg_list
        assert success
        assert msg_list == []
        data_regression.check(out_dict)

    def test_parse_3Dsymmetries(self, data_regression):
        """
        Parse output of a dos calculation in 3D (used to fail due to symmetries reading)
        """
        p = DIR / Path('files/kkr/parser_3Dsymmetries/')
        success, msg_list, out_dict = parse_kkr_outputfile({}, os.fspath(p / 'out_kkr'), os.fspath(p / 'output.0.txt'),
                                                           os.fspath(p / 'output.000.txt'),
                                                           os.fspath(p / 'out_timing.000.txt'),
                                                           os.fspath(p / 'out_potential'),
                                                           os.fspath(p / 'nonco_angle_out.dat'))
        assert success
        assert msg_list == []
        data_regression.check(out_dict)
