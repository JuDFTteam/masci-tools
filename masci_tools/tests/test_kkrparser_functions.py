# -*- coding: utf-8 -*-
"""
@author: ruess
"""

from __future__ import absolute_import
from __future__ import print_function
from builtins import object
import pytest
from masci_tools.io.parsers.kkrparser_functions import parse_kkr_outputfile, check_error_category


class Test_kkr_parser_functions(object):
    """
    Tests for the kkr parser functions
    """
    #some global definitions
    global dref, grouping_ref, outfile, outfile_0init, outfile_000, timing_file, potfile_out, nonco_out_file
    dref = {'code_info_group': {'code_version': 'v2.2-22-g4f8f5ff', 'compile_options': 'openmp', 'calculation_serial_number': 'kkrjm_v2.2-22-g4f8f5ff_openmp_20171208103325'}, 'nspin': 2, 'number_of_atoms_in_unit_cell': 6, 'use_newsosol': True, 'warnings_group': {'number_of_warnings': 1, 'warnings_list': ['WARNING: HFIELD>0.0 found, set KHFIELD to 1']}, 'timings_group': {'main0': 1.101, 'main1a  ': 22.6248, 'main1b  ': 2.9331, 'main1c  ': 46.1649, 'main2': 0.4791, 'Time in Iteration': 72.2019}, 'timings_unit': 'seconds', 'energy_contour_group': {'emin': -0.6, 'emin_unit': 'Rydberg', 'number_of_energy_points': 45, 'temperature': 800.0, 'temperature_unit': 'Kelvin', 'npol': 7, 'n1': 3, 'n2': 32, 'n3': 3}, 'alat_internal': 5.423514, 'two_pi_over_alat_internal': 1.15850818, 'alat_internal_unit': 'a_Bohr', 'two_pi_over_alat_internal_unit': '1/a_Bohr', 'kmesh_group': {'number_different_kmeshes': 4, 'number_kpoints_per_kmesh': {'number_of_kpts': [1000, 343, 125, 27], 'n_kx': [10, 7, 5, 3], 'n_ky': [10, 7, 5, 3], 'n_kz': [10, 7, 5, 3]}, 'kmesh_energypoint': [4, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 2, 1]}, 'symmetries_group': {'number_of_lattice_symmetries': 4, 'number_of_used_symmetries': 1, 'symmetry_description': {'E': {'has_inversion': 0, 'is_unitary': 1, 'euler_angles': [0.0, 0.0, 0.0]}}}, 'ewald_sum_group': {'ewald_summation_mode': '3D', 'rsum_cutoff': 37.9646, 'rsum_number_of_vectors': 425, 'rsum_number_of_shells': 74, 'rsum_cutoff_unit': 'a_Bohr', 'gsum_cutoff': 11.98427, 'gsum_number_of_vectors': 16167, 'gsum_number_of_shells': 1496, 'gsum_cutoff_unit': '1/a_Bohr'}, 'direct_bravais_matrix': [[1.0, 0.0], [0.5, 0.707107]], 'reciprocal_bravais_matrix': [[1.0, -0.707107], [0.0, 1.414214]], 'direct_bravais_matrix_unit': 'alat', 'reciprocal_bravais_matrix_unit': '2*pi / alat', 'core_states_group': {'number_of_core_states_per_atom': [0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0], 'energy_highest_lying_core_state_per_atom': [None, None, None, None, -3.38073664131, -3.38073663703, -3.38073664131, -3.38073663703, None, None, None, None], 'energy_highest_lying_core_state_per_atom_unit': 'Rydberg', 'descr_highest_lying_core_state_per_atom': ['no core states', 'no core states', 'no core states', 'no core states', '3p', '3p', '3p', '3p', 'no core states', 'no core states', 'no core states', 'no core states']}, 'convergence_group': {'rms': 0.23807, 'rms_all_iterations': [2.3466, 0.2333, 0.23309, 0.23439, 0.23513, 0.23596, 0.23664, 0.23724, 0.23771, 0.23807], 'rms_per_atom': [0.31221, 0.092203, 0.15861, 0.15861, 0.092203, 0.31221], 'rms_spin': 3.4092e-07, 'rms_spin_all_iterations': [2.54e-06, 2.032e-06, 1.6256e-06, 1.3005e-06, 1.0404e-06, 8.3232e-07, 6.6585e-07, 5.3268e-07, 4.2615e-07, 3.4092e-07], 'rms_spin_per_atom': [0.31221, 0.092203, 0.15861, 0.15861, 0.092203, 0.31221], 'rms_unit': 'unitless', 'charge_neutrality': -0.275847, 'charge_neutrality_all_iterations': [-4.899746, -0.590384, -0.298448, -0.371115, -0.329622, -0.324519, -0.309258, -0.298029, -0.286475, -0.275847], 'charge_neutrality_unit': 'electrons', 'total_spin_moment_all_iterations': [0.0, 0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0], 'spin_moment_per_atom_all_iterations': [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0]], 'orbital_moment_per_atom_all_iterations': [[-0.0, -0.0, 0.0, 0.0, -0.0, -0.0], [-0.0, -0.0, -0.0, -0.0, -0.0, -0.0], [-0.0, -0.0, -0.0, -0.0, -0.0, -0.0], [-0.0, -0.0, -0.0, -0.0, -0.0, -0.0], [-0.0, -0.0, -0.0, -0.0, -0.0, -0.0], [-0.0, 0.0, -0.0, -0.0, 0.0, -0.0], [-0.0, 0.0, -0.0, -0.0, 0.0, -0.0], [-0.0, 0.0, -0.0, -0.0, 0.0, -0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0]], 'fermi_energy_all_iterations': [0.459241, 0.4656657829, 0.468897589, 0.4729407141, 0.4765411904, 0.4800983619, 0.4834984885, 0.4867848704, 0.4899526366, 0.4930109676], 'fermi_energy_all_iterations_units': 'Ry', 'dos_at_fermi_energy_all_iterations': [10.238607, 15.315281, 15.391192, 15.298192, 15.258272, 15.20493, 15.159147, 15.114337, 15.072376, 15.032559], 'total_energy_Ry_all_iterations': [-5079.95190252, -5081.86670188, -5081.87281356, -5081.88207486, -5081.88933086, -5081.89617526, -5081.9022393, -5081.90772537, -5081.91266074, -5081.91711436], 'number_of_iterations': 10, 'number_of_iterations_max': 10, 'calculation_converged': False, 'nsteps_exhausted': True, 'imix': 0, 'strmix': 0.01, 'qbound': 0.0, 'fcm': 20.0, 'idtbry': 40, 'brymix': 0.01}, 'magnetism_group': {'total_spin_moment': -0.0, 'total_spin_moment_unit': 'mu_Bohr', 'spin_moment_per_atom': [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], 'spin_moment_vector_per_atom': [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [-0.0, -0.0, -0.0], [-0.0, -0.0, -0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]], 'spin_moment_angles_per_atom': [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], 'spin_moment_angles_per_atom_unit': 'degree', 'spin_moment_unit': 'mu_Bohr', 'total_orbital_moment': 0.0, 'orbital_moment_per_atom': [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], 'orbital_moment_unit': 'mu_Bohr'}, 'fermi_energy': 0.4930109676, 'fermi_energy_units': 'Ry', 'dos_at_fermi_energy': 15.032559, 'energy': -69143.0041551653, 'energy_unit': 'eV', 'total_energy_Ry': -5081.91711436, 'total_energy_Ry_unit': 'Rydberg', 'single_particle_energies': [0.3301642569173711, 1.5169676617833023, 38.200748406400834, 38.200748406400834, 1.5169676617833023, 0.3301642569173711], 'single_particle_energies_unit': 'eV', 'total_charge_per_atom': [0.0, 0.0, 26.0, 26.0, 0.0, 0.0], 'charge_core_states_per_atom': [0.0, 0.0, 18.0, 18.0, 0.0, 0.0], 'charge_valence_states_per_atom': [0.004026, 0.229862, 7.628188999999999, 7.628188999999999, 0.229862, 0.004026], 'total_charge_per_atom_unit': 'electron charge', 'charge_core_states_per_atom_unit': 'electron charge', 'charge_valence_states_per_atom_unit': 'electron charge', 'parser_warnings': []}
    grouping_ref = ['energy_contour_group', 'warnings_group', 'ewald_sum_group', 'timings_group', 'core_states_group', 'convergence_group', 'magnetism_group', 'kmesh_group', 'symmetries_group', 'code_info_group']
    path0 = './files/kkr/kkr_run_slab_soc_simple/'
    outfile = path0+'out_kkr'
    outfile_0init = path0+'output.0.txt'
    outfile_000 = path0+'output.000.txt'
    timing_file = path0+'out_timing.000.txt'
    potfile_out = path0+'out_potential'
    nonco_out_file = path0+'nonco_angle_out.dat'


    def test_complete_kkr_output(self):
        """
        Parse complete output of kkr calculation
        """
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, outfile, outfile_0init, outfile_000, timing_file, potfile_out, nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert success
        assert set(out_dict.keys()) == set(dref.keys())
        print(out_dict)
        assert out_dict == dref
        assert msg_list == []
        groups = [i for i in list(out_dict.keys()) if 'group' in i]
        assert set(groups) == set(grouping_ref)

    def test_complete_kkr_output_filehandle(self):
        """
        Parse complete output of kkr calculation but using file handles as done in aiida-kkr
        """
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, open(outfile), open(outfile_0init), open(outfile_000), open(timing_file), open(potfile_out), open(nonco_out_file))
        out_dict['parser_warnings'] = msg_list
        assert success
        assert set(out_dict.keys()) == set(dref.keys())
        print(out_dict)
        assert out_dict == dref
        assert msg_list == []
        groups = [i for i in list(out_dict.keys()) if 'group' in i]
        assert set(groups) == set(grouping_ref)

    def test_mag_orbmom_kkr_output(self):
        """
        Parse complete output of kkr calculation with orbital moments
        """
        dref = {'code_info_group': {'code_version': 'v2.2-22-g4f8f5ff', 'compile_options': 'openmp', 'calculation_serial_number': 'kkrjm_v2.2-22-g4f8f5ff_openmp_20171208132839'}, 'nspin': 2, 'number_of_atoms_in_unit_cell': 6, 'use_newsosol': True, 'warnings_group': {'number_of_warnings': 1, 'warnings_list': ['WARNING: HFIELD>0.0 found, set KHFIELD to 1']}, 'timings_group': {'main0': 1.1051, 'main1a  ': 22.7591, 'main1b  ': 2.9598, 'main1c  ': 46.5031, 'main2': 0.4782, 'Time in Iteration': 72.7002}, 'timings_unit': 'seconds', 'energy_contour_group': {'emin': -0.6, 'emin_unit': 'Rydberg', 'number_of_energy_points': 45, 'temperature': 800.0, 'temperature_unit': 'Kelvin', 'npol': 7, 'n1': 3, 'n2': 32, 'n3': 3}, 'alat_internal': 5.423514, 'two_pi_over_alat_internal': 1.15850818, 'alat_internal_unit': 'a_Bohr', 'two_pi_over_alat_internal_unit': '1/a_Bohr', 'kmesh_group': {'number_different_kmeshes': 4, 'number_kpoints_per_kmesh': {'number_of_kpts': [1000, 343, 125, 27], 'n_kx': [10, 7, 5, 3], 'n_ky': [10, 7, 5, 3], 'n_kz': [10, 7, 5, 3]}, 'kmesh_energypoint': [4, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 2, 1]}, 'symmetries_group': {'number_of_lattice_symmetries': 4, 'number_of_used_symmetries': 1, 'symmetry_description': {'E': {'has_inversion': 0, 'is_unitary': 1, 'euler_angles': [0.0, 0.0, 0.0]}}}, 'ewald_sum_group': {'ewald_summation_mode': '3D', 'rsum_cutoff': 37.9646, 'rsum_number_of_vectors': 425, 'rsum_number_of_shells': 74, 'rsum_cutoff_unit': 'a_Bohr', 'gsum_cutoff': 11.98427, 'gsum_number_of_vectors': 16167, 'gsum_number_of_shells': 1496, 'gsum_cutoff_unit': '1/a_Bohr'}, 'direct_bravais_matrix': [[1.0, 0.0], [0.5, 0.707107]], 'reciprocal_bravais_matrix': [[1.0, -0.707107], [0.0, 1.414214]], 'direct_bravais_matrix_unit': 'alat', 'reciprocal_bravais_matrix_unit': '2*pi / alat', 'core_states_group': {'number_of_core_states_per_atom': [0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0], 'energy_highest_lying_core_state_per_atom': [None, None, None, None, -3.3177936736, -3.43532196688, -3.3177936736, -3.43532196688, None, None, None, None], 'energy_highest_lying_core_state_per_atom_unit': 'Rydberg', 'descr_highest_lying_core_state_per_atom': ['no core states', 'no core states', 'no core states', 'no core states', '3p', '3p', '3p', '3p', 'no core states', 'no core states', 'no core states', 'no core states']}, 'convergence_group': {'rms': 0.21679, 'rms_all_iterations': [2.17, 0.22841, 0.22738, 0.22601, 0.22458, 0.22304, 0.22139, 0.21969, 0.21811, 0.21679], 'rms_per_atom': [0.26244, 0.052778, 0.17549, 0.17549, 0.052778, 0.26244], 'rms_spin': 0.0048928, 'rms_spin_all_iterations': [0.011171, 0.0095327, 0.0081824, 0.0072193, 0.0065592, 0.0060872, 0.005726, 0.0054255, 0.0051542, 0.0048928], 'rms_spin_per_atom': [0.26244, 0.052778, 0.17549, 0.17549, 0.052778, 0.26244], 'rms_unit': 'unitless', 'charge_neutrality': -0.171726, 'charge_neutrality_all_iterations': [-4.914607, -0.4306, -0.254987, -0.262482, -0.239525, -0.215776, -0.190357, -0.173403, -0.168785, -0.171726], 'charge_neutrality_unit': 'electrons', 'total_spin_moment_all_iterations': [1.150471, 2.201148, 2.530913, 2.835644, 3.131747, 3.409436, 3.669548, 3.912214, 4.137758, 4.346569], 'spin_moment_per_atom_all_iterations': [[0.0005, 0.0214, 0.5534, 0.5534, 0.0214, 0.0005], [0.0005, 0.0156, 1.0844, 1.0844, 0.0156, 0.0005], [0.0005, 0.0152, 1.2497, 1.2497, 0.0152, 0.0005], [0.0005, 0.0159, 1.4015, 1.4015, 0.0159, 0.0005], [0.0005, 0.0166, 1.5488, 1.5488, 0.0166, 0.0005], [0.0005, 0.0174, 1.6869, 1.6869, 0.0174, 0.0005], [0.0004, 0.0181, 1.8162, 1.8162, 0.0181, 0.0004], [0.0004, 0.0187, 1.937, 1.937, 0.0187, 0.0004], [0.0004, 0.0193, 2.0492, 2.0492, 0.0193, 0.0004], [0.0003, 0.02, 2.153, 2.153, 0.02, 0.0003]], 'orbital_moment_per_atom_all_iterations': [[-0.0, -0.0001, -0.0063, -0.0063, -0.0001, -0.0], [0.0, -0.0001, 0.0464, 0.0464, -0.0001, 0.0], [0.0, -0.0001, 0.052, 0.052, -0.0001, 0.0], [0.0, -0.0001, 0.053, 0.053, -0.0001, 0.0], [0.0, -0.0001, 0.0539, 0.0539, -0.0001, 0.0], [0.0, -0.0001, 0.0547, 0.0547, -0.0001, 0.0], [0.0, -0.0001, 0.0558, 0.0558, -0.0001, 0.0], [0.0, -0.0002, 0.0572, 0.0572, -0.0002, 0.0], [0.0, -0.0002, 0.0585, 0.0585, -0.0002, 0.0], [-0.0, -0.0002, 0.0599, 0.0599, -0.0002, -0.0]], 'fermi_energy_all_iterations': [0.459241, 0.4644579419, 0.4677093646, 0.4712454875, 0.4746715679, 0.4779445657, 0.4809944912, 0.4839164583, 0.4868973048, 0.4900727042], 'fermi_energy_all_iterations_units': 'Ry', 'dos_at_fermi_energy_all_iterations': [10.778086, 13.756463, 13.070528, 12.371442, 11.652055, 10.987681, 10.402299, 9.890784, 9.437221, 9.013371], 'total_energy_Ry_all_iterations': [-5080.21763742, -5081.87827258, -5081.89042264, -5081.90349614, -5081.91552341, -5081.92632203, -5081.93573754, -5081.94396567, -5081.95138589, -5081.95840149], 'number_of_iterations': 10, 'number_of_iterations_max': 10, 'calculation_converged': False, 'nsteps_exhausted': True, 'imix': 0, 'strmix': 0.01, 'qbound': 0.0, 'fcm': 20.0, 'idtbry': 40, 'brymix': 0.01}, 'magnetism_group': {'total_spin_moment': 4.346569, 'total_spin_moment_unit': 'mu_Bohr', 'spin_moment_per_atom': [0.0003, 0.02, 2.153, 2.153, 0.02, 0.0003], 'spin_moment_vector_per_atom': [[0.0, 0.0, 0.0003], [0.0, 0.0, 0.02], [0.0, 0.0, 2.153], [0.0, 0.0, 2.153], [0.0, 0.0, 0.02], [0.0, 0.0, 0.0003]], 'spin_moment_angles_per_atom': [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], 'spin_moment_angles_per_atom_unit': 'degree', 'spin_moment_unit': 'mu_Bohr', 'total_orbital_moment': 0.1194, 'orbital_moment_per_atom': [-0.0, -0.0002, 0.0599, 0.0599, -0.0002, -0.0], 'orbital_moment_unit': 'mu_Bohr'}, 'fermi_energy': 0.4900727042, 'fermi_energy_units': 'Ry', 'dos_at_fermi_energy': 9.013371, 'energy': -69143.56589518131, 'energy_unit': 'eV', 'total_energy_Ry': -5081.95840149, 'total_energy_Ry_unit': 'Rydberg', 'single_particle_energies': [0.2097247970611916, 1.2887334935546728, 37.826589199624905, 37.826589199624905, 1.2887334935546728, 0.2097247970611916], 'single_particle_energies_unit': 'eV', 'total_charge_per_atom': [0.0, 0.0, 26.0, 26.0, 0.0, 0.0], 'charge_core_states_per_atom': [0.0, 0.0, 18.0, 18.0, 0.0, 0.0], 'charge_valence_states_per_atom': [0.003503, 0.21339, 7.697244000000001, 7.697244000000001, 0.21339, 0.003503], 'total_charge_per_atom_unit': 'electron charge', 'charge_core_states_per_atom_unit': 'electron charge', 'charge_valence_states_per_atom_unit': 'electron charge', 'parser_warnings': []}
        path0 = './files/kkr/kkr_run_slab_soc_mag/'
        outfile = path0+'out_kkr'
        outfile_0init = path0+'output.0.txt'
        outfile_000 = path0+'output.000.txt'
        timing_file = path0+'out_timing.000.txt'
        potfile_out = path0+'out_potential'
        nonco_out_file = path0+'nonco_angle_out.dat'
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, outfile, outfile_0init, outfile_000, timing_file, potfile_out, nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert success
        assert set(out_dict.keys()) == set(dref.keys())
        print(out_dict)
        assert out_dict == dref
        assert msg_list == []

    def test_nosoc_kkr_output(self):
        """
        Parse complete output of kkr calculation nosoc, magnetic
        """
        dref = {'code_info_group': {'code_version': 'v2.2-22-g4f8f5ff', 'compile_options': 'openmp', 'calculation_serial_number': 'kkrjm_v2.2-22-g4f8f5ff_openmp_20171208160428'}, 'nspin': 2, 'number_of_atoms_in_unit_cell': 6, 'use_newsosol': False, 'warnings_group': {'number_of_warnings': 1, 'warnings_list': ['WARNING: HFIELD>0.0 found, set KHFIELD to 1']}, 'timings_group': {'main0': 0.976, 'main1a  ': 4.7957, 'main1b  ': 1.562, 'main1c  ': 10.57, 'main2': 0.5074, 'Time in Iteration': 17.4351}, 'timings_unit': 'seconds', 'energy_contour_group': {'emin': -0.6, 'emin_unit': 'Rydberg', 'number_of_energy_points': 45, 'temperature': 800.0, 'temperature_unit': 'Kelvin', 'npol': 7, 'n1': 3, 'n2': 32, 'n3': 3}, 'alat_internal': 5.423514, 'two_pi_over_alat_internal': 1.15850818, 'alat_internal_unit': 'a_Bohr', 'two_pi_over_alat_internal_unit': '1/a_Bohr', 'kmesh_group': {'number_different_kmeshes': 4, 'number_kpoints_per_kmesh': {'number_of_kpts': [310, 112, 45, 12], 'n_kx': [10, 7, 5, 3], 'n_ky': [10, 7, 5, 3], 'n_kz': [10, 7, 5, 3]}, 'kmesh_energypoint': [4, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 2, 1, 4, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 2, 1]}, 'symmetries_group': {'number_of_lattice_symmetries': 4, 'number_of_used_symmetries': 4, 'symmetry_description': {'E': {'has_inversion': 0, 'is_unitary': 1, 'euler_angles': [0.0, 0.0, 0.0]}, 'C2z': {'has_inversion': 0, 'is_unitary': 1, 'euler_angles': [180.0, 0.0, 0.0]}, 'IC2x': {'has_inversion': 1, 'is_unitary': 1, 'euler_angles': [180.0, 180.0, 0.0]}, 'IC2y': {'has_inversion': 1, 'is_unitary': 1, 'euler_angles': [0.0, 180.0, 0.0]}}}, 'ewald_sum_group': {'ewald_summation_mode': '3D', 'rsum_cutoff': 37.9646, 'rsum_number_of_vectors': 425, 'rsum_number_of_shells': 74, 'rsum_cutoff_unit': 'a_Bohr', 'gsum_cutoff': 11.98427, 'gsum_number_of_vectors': 16167, 'gsum_number_of_shells': 1496, 'gsum_cutoff_unit': '1/a_Bohr'}, 'direct_bravais_matrix': [[1.0, 0.0], [0.5, 0.707107]], 'reciprocal_bravais_matrix': [[1.0, -0.707107], [0.0, 1.414214]], 'direct_bravais_matrix_unit': 'alat', 'reciprocal_bravais_matrix_unit': '2*pi / alat', 'core_states_group': {'number_of_core_states_per_atom': [0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0], 'energy_highest_lying_core_state_per_atom': [None, None, None, None, -3.3808088817, -3.3808088774, -3.3808088817, -3.3808088774, None, None, None, None], 'energy_highest_lying_core_state_per_atom_unit': 'Rydberg', 'descr_highest_lying_core_state_per_atom': ['no core states', 'no core states', 'no core states', 'no core states', '3p', '3p', '3p', '3p', 'no core states', 'no core states', 'no core states', 'no core states']}, 'convergence_group': {'rms': 0.23827, 'rms_all_iterations': [2.3414, 0.23344, 0.23332, 0.2346, 0.23535, 0.23618, 0.23686, 0.23745, 0.23792, 0.23827], 'rms_per_atom': [0.31264, 0.092533, 0.15846, 0.15846, 0.092533, 0.31264], 'rms_spin': 3.4092e-07, 'rms_spin_all_iterations': [2.54e-06, 2.032e-06, 1.6256e-06, 1.3005e-06, 1.0404e-06, 8.3232e-07, 6.6585e-07, 5.3268e-07, 4.2615e-07, 3.4092e-07], 'rms_spin_per_atom': [0.31264, 0.092533, 0.15846, 0.15846, 0.092533, 0.31264], 'rms_unit': 'unitless', 'charge_neutrality': -0.275844, 'charge_neutrality_all_iterations': [-4.90193, -0.576195, -0.303203, -0.369647, -0.330104, -0.324371, -0.309302, -0.298009, -0.286475, -0.275844], 'charge_neutrality_unit': 'electrons', 'total_spin_moment_all_iterations': [0.0, 0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0], 'spin_moment_per_atom_all_iterations': [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], [0.0, 0.0, -0.0, -0.0, 0.0, 0.0]], 'fermi_energy_all_iterations': [0.459241, 0.4654901812, 0.4687657284, 0.472782771, 0.476380134, 0.4799276602, 0.4833209134, 0.4866002281, 0.4897616294, 0.4928139832], 'fermi_energy_all_iterations_units': 'Ry', 'dos_at_fermi_energy_all_iterations': [10.260433, 15.367202, 15.427578, 15.336628, 15.293781, 15.239316, 15.191993, 15.145917, 15.102739, 15.061817], 'total_energy_Ry_all_iterations': [-5079.95660683, -5081.8656148, -5081.87192003, -5081.88104897, -5081.88827002, -5081.89505638, -5081.90107597, -5081.90651978, -5081.91141803, -5081.91583836], 'number_of_iterations': 10, 'number_of_iterations_max': 10, 'calculation_converged': False, 'nsteps_exhausted': True, 'imix': 0, 'strmix': 0.01, 'qbound': 0.0, 'fcm': 20.0, 'idtbry': 40, 'brymix': 0.01}, 'magnetism_group': {'total_spin_moment': -0.0, 'total_spin_moment_unit': 'mu_Bohr', 'spin_moment_per_atom': [0.0, 0.0, -0.0, -0.0, 0.0, 0.0], 'spin_moment_unit': 'mu_Bohr'}, 'fermi_energy': 0.4928139832, 'fermi_energy_units': 'Ry', 'dos_at_fermi_energy': 15.061817, 'energy': -69142.98679430102, 'energy_unit': 'eV', 'total_energy_Ry': -5081.91583836, 'total_energy_Ry_unit': 'Rydberg', 'single_particle_energies': [0.3300528004408107, 1.5175235386980168, 38.20540868007191, 38.20540868007191, 1.5175235386980168, 0.3300528004408107], 'single_particle_energies_unit': 'eV', 'total_charge_per_atom': [0.0, 0.0, 26.0, 26.0, 0.0, 0.0], 'charge_core_states_per_atom': [0.0, 0.0, 18.0, 18.0, 0.0, 0.0], 'charge_valence_states_per_atom': [0.004028, 0.229975, 7.628074000000002, 7.628074000000002, 0.229975, 0.004028], 'total_charge_per_atom_unit': 'electron charge', 'charge_core_states_per_atom_unit': 'electron charge', 'charge_valence_states_per_atom_unit': 'electron charge', 'parser_warnings': []}
        path0 = './files/kkr/kkr_run_slab_nosoc/'
        outfile = path0+'out_kkr'
        outfile_0init = path0+'output.0.txt'
        outfile_000 = path0+'output.000.txt'
        timing_file = path0+'out_timing.000.txt'
        potfile_out = path0+'out_potential'
        nonco_out_file = path0+'nonco_angle_out.dat'
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, outfile, outfile_0init, outfile_000, timing_file, potfile_out, nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert success
        assert set(out_dict.keys()) == set(dref.keys())
        print(out_dict)
        assert out_dict == dref
        assert msg_list == []

    def test_missing_outfile(self):
        """
        Parse kkr output where out_kkr is missing. Compares error messages
        """
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, 'wrong_name', outfile_0init, outfile_000, timing_file, potfile_out, nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert not success
        assert set(msg_list) == set(['Error parsing output of KKR: Version Info', 'Error parsing output of KKR: rms-error', 'Error parsing output of KKR: charge neutrality', 'Error parsing output of KKR: total magnetic moment', 'Error parsing output of KKR: spin moment per atom', 'Error parsing output of KKR: orbital moment', 'Error parsing output of KKR: EF', 'Error parsing output of KKR: DOS@EF', 'Error parsing output of KKR: total energy', 'Error parsing output of KKR: search for warnings', 'Error parsing output of KKR: charges', 'Error parsing output of KKR: scfinfo'])

    def test_missing_outfile0init(self):
        """
        Parse kkr output where output.0.txt is missing. Compares error messages
        """
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, outfile, 'wrong_name', outfile_000, timing_file, potfile_out, nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert not success
        assert set(msg_list) == set(['Error parsing output of KKR: nspin/natom', 'Error parsing output of KKR: spin moment per atom', 'Error parsing output of KKR: orbital moment', 'Error parsing output of KKR: energy contour', 'Error parsing output of KKR: alat, 2*pi/alat', 'Error parsing output of KKR: scfinfo', 'Error parsing output of KKR: kmesh', 'Error parsing output of KKR: symmetries', 'Error parsing output of KKR: ewald summation for madelung poterntial', 'Error parsing output of KKR: lattice vectors (direct/reciprocal)'])

    def test_missing_outfile000(self):
        """
        Parse kkr output where output.000.txt is missing. Compares error messages
        """
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, outfile, outfile_0init, 'wrong_name', timing_file, potfile_out, nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert not success
        assert set(msg_list) == set(['Error parsing output of KKR: rms-error', 'Error parsing output of KKR: single particle energies', 'Error parsing output of KKR: charges', 'Error parsing output of KKR: scfinfo', 'Error parsing output of KKR: kmesh'])

    def test_missing_timingfile(self):
        """
        Parse kkr output where out_timing.000.txt is missing. Compares error messages
        """
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, outfile, outfile_0init, outfile_000, 'wrong_name', potfile_out, nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert not success
        assert msg_list == ['Error parsing output of KKR: timings']

    def test_missing_potfile(self):
        """
        Parse kkr output where out_potential is missing. Compares error messages
        """
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, outfile, outfile_0init, outfile_000, timing_file, 'wrong_name', nonco_out_file)
        out_dict['parser_warnings'] = msg_list
        assert not success
        assert msg_list == ['Error parsing output of KKR: core_states']


    def test_missing_nonco_angles(self):
        """
        Parse kkr output where out_potential is missing. Compares error messages
        """
        path0 = './files/kkr/kkr_run_slab_soc_mag/'
        outfile = path0+'out_kkr'
        outfile_0init = path0+'output.0.txt'
        outfile_000 = path0+'output.000.txt'
        timing_file = path0+'out_timing.000.txt'
        potfile_out = path0+'out_potential'
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, outfile, outfile_0init, outfile_000, timing_file, potfile_out, 'wrong_name')
        out_dict['parser_warnings'] = msg_list
        assert not success
        assert msg_list == ['Error parsing output of KKR: spin moment per atom']

    def test_check_error_category(self):
        """
        Check check_error_category function used in parser after parse_kkr_outputfile is used
        """
        fname = 'nonco_angles_out.dat'
        err_cat, err_msg = (2, "Error! NONCO_ANGLES_OUT not found {}".format(fname))
        assert not check_error_category(err_cat, err_msg, {'use_newsosol': False})
        assert check_error_category(err_cat, err_msg, {'use_newsosol': True})

    def test_parse_dosout(self):
        """
        Parse output of dos calculation since ouput changes slightly (e.g. no ewald sum)
        """
        path0 = './files/kkr/kkr_run_dos_output/'
        outfile = path0+'out_kkr'
        outfile_0init = path0+'output.0.txt'
        outfile_000 = path0+'output.000.txt'
        timing_file = path0+'out_timing.000.txt'
        potfile_out = path0+'out_potential'
        dref = {'code_info_group': {'code_version': 'v2.2-22-g4f8f5ff', 'compile_options': 'openmp-mac', 'calculation_serial_number': 'kkrjm_v2.2-22-g4f8f5ff_openmp-mac_20171214102522'}, 'nspin': 1, 'number_of_atoms_in_unit_cell': 4, 'use_newsosol': False, 'warnings_group': {'number_of_warnings': 0, 'warnings_list': []}, 'timings_group': {'main0': 0.136, 'main1a - tbref': 0.9809, 'main1a  ': 1.4302, 'main1b - calctref13': 0.1511, 'main1b  ': 3.537, 'main1c - serial part': 0.0054, 'main1c  ': 0.7165, 'main2': 0.2291, 'Time in Iteration': 5.9128}, 'timings_unit': 'seconds', 'energy_contour_group': {'emin': -1.0, 'emin_unit': 'Rydberg', 'number_of_energy_points': 21, 'temperature': 200.0, 'temperature_unit': 'Kelvin', 'npol': 0, 'n1': 0, 'n2': 21, 'n3': 0}, 'alat_internal': 7.869273, 'two_pi_over_alat_internal': 0.79844546, 'alat_internal_unit': 'a_Bohr', 'two_pi_over_alat_internal_unit': '1/a_Bohr', 'kmesh_group': {'number_different_kmeshes': 1, 'number_kpoints_per_kmesh': {'number_of_kpts': [216], 'n_kx': [10], 'n_ky': [10], 'n_kz': [10]}, 'kmesh_energypoint': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}, 'symmetries_group': {'number_of_lattice_symmetries': 8, 'number_of_used_symmetries': 8, 'symmetry_description': {'E': {'has_inversion': 0, 'is_unitary': 1, 'euler_angles': [0.0, 0.0, 0.0]}, 'C2x': {'has_inversion': 0, 'is_unitary': 1, 'euler_angles': [180.0, 180.0, 0.0]}, 'C2y': {'has_inversion': 0, 'is_unitary': 1, 'euler_angles': [0.0, 180.0, 0.0]}, 'C2z': {'has_inversion': 0, 'is_unitary': 1, 'euler_angles': [180.0, 0.0, 0.0]}, 'IE': {'has_inversion': 1, 'is_unitary': 1, 'euler_angles': [0.0, 0.0, 0.0]}, 'IC2x': {'has_inversion': 1, 'is_unitary': 1, 'euler_angles': [180.0, 180.0, 0.0]}, 'IC2y': {'has_inversion': 1, 'is_unitary': 1, 'euler_angles': [0.0, 180.0, 0.0]}, 'IC2z': {'has_inversion': 1, 'is_unitary': 1, 'euler_angles': [180.0, 0.0, 0.0]}}}, 'direct_bravais_matrix': [[1.0, 0.0, 0.0], [0.0, 1.0, 1.0], [0.0, 0.0, 0.0]], 'reciprocal_bravais_matrix': [[1.0, 0.0, 0.0], [0.0, 1.0, 1.0], [0.0, 0.0, 0.0]], 'direct_bravais_matrix_unit': 'alat', 'reciprocal_bravais_matrix_unit': '2*pi / alat', 'core_states_group': {'number_of_core_states_per_atom': [8, 8, 8, 8], 'energy_highest_lying_core_state_per_atom': [-3.83243200276, -3.83243200276, -3.83243200276, -3.83243200276], 'energy_highest_lying_core_state_per_atom_unit': 'Rydberg', 'descr_highest_lying_core_state_per_atom': ['4p', '4p', '4p', '4p']}, 'convergence_group': {'rms': 12.977, 'rms_all_iterations': [12.977], 'rms_per_atom': [12.977, 12.977, 12.977, 12.977], 'rms_spin': None, 'rms_spin_all_iterations': [], 'rms_spin_per_atom': [12.977, 12.977, 12.977, 12.977], 'rms_unit': 'unitless', 'charge_neutrality': -137.449522, 'charge_neutrality_all_iterations': [-137.449522], 'charge_neutrality_unit': 'electrons', 'fermi_energy_all_iterations': [1.05], 'fermi_energy_all_iterations_units': 'Ry', 'dos_at_fermi_energy_all_iterations': [3.672746], 'total_energy_Ry_all_iterations': [-28679.93406508], 'number_of_iterations': 1, 'number_of_iterations_max': 1, 'calculation_converged': False, 'nsteps_exhausted': True, 'imix': 0, 'strmix': 0.0, 'qbound': 0.0, 'fcm': 20.0, 'idtbry': 40, 'brymix': 0.01}, 'fermi_energy': 1.05, 'fermi_energy_units': 'Ry', 'dos_at_fermi_energy': 3.672746, 'energy': -390210.3784078399, 'energy_unit': 'eV', 'total_energy_Ry': -28679.93406508, 'total_energy_Ry_unit': 'Rydberg', 'single_particle_energies': [489.0712275918133, 489.0712275918133, 489.0712275918133, 489.0712275918133], 'single_particle_energies_unit': 'eV', 'total_charge_per_atom': [], 'charge_core_states_per_atom': [], 'total_charge_per_atom_unit': 'electron charge', 'charge_core_states_per_atom_unit': 'electron charge', 'charge_valence_states_per_atom_unit': 'electron charge', 'parser_warnings': []}
        out_dict = {}
        success, msg_list, out_dict = parse_kkr_outputfile(out_dict, outfile, outfile_0init, outfile_000, timing_file, potfile_out, 'wrong_name')
        out_dict['parser_warnings'] = msg_list
        assert success
        assert msg_list == []
        assert set(out_dict.keys()) == set(dref.keys())
        print(out_dict)
        assert out_dict == dref

    def test_parse_3Dsymmetries(self):
        """
        Parse output of a dos calculation in 3D (used to fail due to symmetries reading)
        """
        p = './files/kkr/parser_3Dsymmetries/'
        dref = {'code_info_group': {'code_version': 'v2.2-23-g4a095c6', 'compile_options': 'openmp-mac', 'calculation_serial_number': 'kkrjm_v2.2-23-g4a095c6_openmp-mac_20180105092029'}, 'nspin': 2, 'number_of_atoms_in_unit_cell': 4, 'use_newsosol': False, 'warnings_group': {'number_of_warnings': 0, 'warnings_list': []}, 'timings_group': {'main0': 0.1273, 'main1a - tbref': 0.5523, 'main1a  ': 0.6874, 'main1b - calctref13': 0.4801, 'main1b  ': 60.1609, 'main1c - serial part': 0.0136, 'main1c  ': 0.0975, 'main2': 0.1171, 'Time in Iteration': 61.063}, 'timings_unit': 'seconds', 'energy_contour_group': {'emin': -0.673499, 'emin_unit': 'Rydberg', 'number_of_energy_points': 61, 'temperature': 400.0, 'temperature_unit': 'Kelvin', 'npol': 0, 'n1': 0, 'n2': 61, 'n3': 0}, 'alat_internal': 7.869273, 'two_pi_over_alat_internal': 0.79844546, 'alat_internal_unit': 'a_Bohr', 'two_pi_over_alat_internal_unit': '1/a_Bohr', 'kmesh_group': {'number_different_kmeshes': 1, 'number_kpoints_per_kmesh': {'number_of_kpts': [1331], 'n_kx': [20], 'n_ky': [20], 'n_kz': [20]}, 'kmesh_energypoint': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}, 'symmetries_group': {'number_of_lattice_symmetries': 8, 'number_of_used_symmetries': 8, 'symmetry_description': {'E': {'has_inversion': 0, 'is_unitary': 1, 'euler_angles': [0.0, 0.0, 0.0]}, 'C2x': {'has_inversion': 0, 'is_unitary': 1, 'euler_angles': [180.0, 180.0, 0.0]}, 'C2y': {'has_inversion': 0, 'is_unitary': 1, 'euler_angles': [0.0, 180.0, 0.0]}, 'C2z': {'has_inversion': 0, 'is_unitary': 1, 'euler_angles': [180.0, 0.0, 0.0]}, 'IE': {'has_inversion': 1, 'is_unitary': 1, 'euler_angles': [0.0, 0.0, 0.0]}, 'IC2x': {'has_inversion': 1, 'is_unitary': 1, 'euler_angles': [180.0, 180.0, 0.0]}, 'IC2y': {'has_inversion': 1, 'is_unitary': 1, 'euler_angles': [0.0, 180.0, 0.0]}, 'IC2z': {'has_inversion': 1, 'is_unitary': 1, 'euler_angles': [180.0, 0.0, 0.0]}}}, 'direct_bravais_matrix': [[1.0, 0.0, 0.0], [0.0, 1.0, 1.0], [0.0, 0.0, 0.0]], 'reciprocal_bravais_matrix': [[1.0, 0.0, 0.0], [0.0, 1.0, 1.0], [0.0, 0.0, 0.0]], 'direct_bravais_matrix_unit': 'alat', 'reciprocal_bravais_matrix_unit': '2*pi / alat', 'core_states_group': {'number_of_core_states_per_atom': [8, 8, 8, 8, 8, 8, 8, 8], 'energy_highest_lying_core_state_per_atom': [-3.5445692, -3.5445692, -3.5445692, -3.5445692, -3.5445692, -3.5445692, -3.5445692, -3.5445692], 'energy_highest_lying_core_state_per_atom_unit': 'Rydberg', 'descr_highest_lying_core_state_per_atom': ['4p', '4p', '4p', '4p', '4p', '4p', '4p', '4p']}, 'convergence_group': {'rms': 18.83, 'rms_all_iterations': [18.83], 'rms_per_atom': [18.83, 18.83, 18.83, 18.83], 'rms_spin': 0.0, 'rms_spin_all_iterations': [0.0], 'rms_spin_per_atom': [18.83, 18.83, 18.83, 18.83], 'rms_unit': 'unitless', 'charge_neutrality': -147.800777, 'charge_neutrality_all_iterations': [-147.800777], 'charge_neutrality_unit': 'electrons', 'total_spin_moment_all_iterations': [0.0], 'spin_moment_per_atom_all_iterations': [[0.0, 0.0, 0.0, 0.0]], 'fermi_energy_all_iterations': [0.153577], 'fermi_energy_all_iterations_units': 'Ry', 'dos_at_fermi_energy_all_iterations': [7.537613], 'total_energy_Ry_all_iterations': [-27548.13340937], 'number_of_iterations': 1, 'number_of_iterations_max': 1, 'calculation_converged': False, 'nsteps_exhausted': True, 'imix': 0, 'strmix': 0.0, 'qbound': 0.0, 'fcm': 20.0, 'idtbry': 40, 'brymix': 0.01}, 'magnetism_group': {'total_spin_moment': 0.0, 'total_spin_moment_unit': 'mu_Bohr', 'spin_moment_per_atom': [0.0, 0.0, 0.0, 0.0], 'spin_moment_unit': 'mu_Bohr'}, 'fermi_energy': 0.153577, 'fermi_energy_units': 'Ry', 'dos_at_fermi_energy': 7.537613, 'energy': -374811.44613886473, 'energy_unit': 'eV', 'total_energy_Ry': -27548.13340937, 'total_energy_Ry_unit': 'Rydberg', 'single_particle_energies': [49.62180968957991, 49.62180968957991, 49.62180968957991, 49.62180968957991], 'single_particle_energies_unit': 'eV', 'total_charge_per_atom': [], 'charge_core_states_per_atom': [], 'total_charge_per_atom_unit': 'electron charge', 'charge_core_states_per_atom_unit': 'electron charge', 'charge_valence_states_per_atom_unit': 'electron charge'}
        success, msg_list, out_dict = parse_kkr_outputfile({}, p+'out_kkr', p+'output.0.txt', p+'output.000.txt', p+'out_timing.000.txt', p+'out_potential', p+'nonco_angle_out.dat')
        assert success
        assert msg_list == []
        assert set(out_dict.keys()) == set(dref.keys())
        print(out_dict)
        assert out_dict == dref

    def test_Nan_output(self):
        """
        Parse output of a dos calculation in 3D (used to fail due to symmetries reading)
        """
        p = './files/kkr/parser_3Dsymmetries/'
        success, msg_list, out_dict = parse_kkr_outputfile({}, p+'out_kkr', p+'output.0.txt', p+'output.000.txt', p+'out_timing.000.txt', p+'out_potential', p+'nonco_angle_out.dat', p+'output.2.txt')
        from numpy import isnan
        captured_nan = False
        for key, val in out_dict['convergence_group'].items():
            if key in ['charge_neutrality', 'rms']:
                if isnan(val):
                    captured_nan = True
            elif key in ['charge_neutrality_all_iterations', 'dos_at_fermi_energy_all_iterations', 'fermi_energy_all_iterations', 'rms_all_iterations', 'total_energy_Ry_all_iterations', 'rms_per_atom']:
                for isub in val:
                    if isnan(isub):
                        captured_nan = True
        assert success
        assert not captured_nan
