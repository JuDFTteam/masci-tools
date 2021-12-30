"""
@author: ruess
"""

import pytest
from masci_tools.io.parsers.voroparser_functions import parse_voronoi_output
from pathlib import Path
import os

DIR = Path(__file__).parent.resolve()


class Test_voronoi_parser_functions:
    """
    Tests for the voronoi parser functions
    """

    grouping_ref = ['volumes_group', 'radii_atoms_group', 'code_info_group', 'core_states_group', 'cluster_info_group']

    path0 = DIR / Path('files/voronoi/')
    outfile = os.fspath(path0 / 'out_voronoi')
    potfile = os.fspath(path0 / 'output.pot')
    atominfo = os.fspath(path0 / 'atominfo.txt')
    radii = os.fspath(path0 / 'radii.dat')
    inputfile = os.fspath(path0 / 'inputcard')

    def test_complete_voro_output(self, data_regression):
        """
        Parse complete output of voronoi calculation and compare out_dict, grouping, warnings
        """
        out_dict = {'parser_version': 'some_version_number'}
        success, msg_list, out_dict = parse_voronoi_output(out_dict, self.outfile, self.potfile, self.atominfo,
                                                           self.radii, self.inputfile)
        out_dict['parser_warnings'] = msg_list

        assert success
        assert msg_list == []
        groups = [i for i in list(out_dict.keys()) if 'group' in i]
        assert set(groups) == set(self.grouping_ref)

        data_regression.check(out_dict)

    def test_complete_voro_output_filehandle(self, data_regression):
        """
        Parse complete output of voronoi calculation from open file handles as done in aiida-kkr and compare out_dict, grouping, warnings
        """
        out_dict = {'parser_version': 'some_version_number'}
        with open(self.outfile, encoding='utf-8') as outfile:
            with open(self.potfile, encoding='utf-8') as potfile:
                with open(self.atominfo, encoding='utf-8') as atominfo:
                    with open(self.radii, encoding='utf-8') as radii:
                        with open(self.inputfile, encoding='utf-8') as inputfile:
                            success, msg_list, out_dict = parse_voronoi_output(out_dict, outfile, potfile, atominfo,
                                                                               radii, inputfile)
        out_dict['parser_warnings'] = msg_list
        assert success
        assert msg_list == []
        groups = [i for i in list(out_dict.keys()) if 'group' in i]
        assert set(groups) == set(self.grouping_ref)

        data_regression.check(out_dict)

    def test_missing_outfile(self, data_regression):
        """
        Parse output where out_voronoi is missing and compare error messages/rest of out_dict
        """
        out_dict = {'parser_version': 'some_version_number'}
        success, msg_list, out_dict = parse_voronoi_output(out_dict, '', self.potfile, self.atominfo, self.radii,
                                                           self.inputfile)
        out_dict['parser_warnings'] = msg_list

        assert not success
        data_regression.check({'msg_list': msg_list, 'output': out_dict})

    def test_missing_atominfo(self, data_regression):
        """
        Parse output where atominfo.txt is missing and compare error messages/rest of out_dict
        """
        out_dict = {'parser_version': 'some_version_number'}
        success, msg_list, out_dict = parse_voronoi_output(out_dict, self.outfile, self.potfile, 'wrong_name',
                                                           self.radii, self.inputfile)
        out_dict['parser_warnings'] = msg_list
        assert not success
        data_regression.check({'msg_list': msg_list, 'output': out_dict})

    def test_missing_inputfile(self, data_regression):
        """
        Parse output where inputcard is missing and compare error messages/rest of out_dict
        """
        out_dict = {'parser_version': 'some_version_number'}
        success, msg_list, out_dict = parse_voronoi_output(out_dict, self.outfile, self.potfile, self.atominfo,
                                                           self.radii, 'wrong_name')
        out_dict['parser_warnings'] = msg_list
        assert not success
        data_regression.check({'msg_list': msg_list, 'output': out_dict})

    def test_missing_potfile(self, data_regression):
        """
        Parse output where output.pot is missing and compare error messages/rest of out_dict
        """
        out_dict = {'parser_version': 'some_version_number'}
        success, msg_list, out_dict = parse_voronoi_output(out_dict, self.outfile, 'wrong_name', self.atominfo,
                                                           self.radii, self.inputfile)
        out_dict['parser_warnings'] = msg_list

        assert not success
        data_regression.check({'msg_list': msg_list, 'output': out_dict})

    def test_missing_radii(self, data_regression):
        """
        Parse output where radii.dat is missing and compare error messages/rest of out_dict
        """
        out_dict = {'parser_version': 'some_version_number'}
        success, msg_list, out_dict = parse_voronoi_output(out_dict, self.outfile, self.potfile, self.atominfo,
                                                           'wrong_name', self.inputfile)
        out_dict['parser_warnings'] = msg_list

        assert not success
        data_regression.check({'msg_list': msg_list, 'output': out_dict})
