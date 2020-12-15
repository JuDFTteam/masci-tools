# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from masci_tools.io.parsers.fleur import outxml_parser
import os

# Collect the input files
file_path = 'files/fleur/Max-R5'

outxmlfilefolder = os.path.dirname(os.path.abspath(__file__))
outxmlfilefolder_valid = [os.path.abspath(os.path.join(outxmlfilefolder, file_path))]

outxmlfilelist = []
for folder in outxmlfilefolder_valid:
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.xml') and 'out' in file:
                outxmlfilelist.append(os.path.join(subdir, file))


@pytest.mark.parametrize('outxmlfilepath', outxmlfilelist)
def test_outxml_valid_outxml(outxmlfilepath):
    """
    test if valid inp.xml files are recognized by the inpxml_parser
    """
    from lxml import etree

    #Pass inpxmlfile
    out_dict = outxml_parser(outxmlfilepath)

    #Parse before
    parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8')
    xmltree = etree.parse(outxmlfilepath, parser)
    out_dict = outxml_parser(xmltree, strict=True)


def test_outxml_lastiter():

    expected_result = {
        'bandgap': 2.2729704824,
        'bandgap_units': 'eV',
        'charge_den_xc_den_integral': -41.7653329254,
        'charge_density': 0.026112816,
        'creator_name': 'fleur 32',
        'creator_target_architecture': 'GEN',
        'density_convergence_units': 'me/bohr^3',
        'end_date': {
            'date': '2020/12/10',
            'time': '16:51:35'
        },
        'energy': -15784.360800784752,
        'energy_core_electrons': -260.7708027749,
        'energy_hartree': -580.0645652222,
        'energy_hartree_units': 'Htr',
        'energy_units': 'eV',
        'energy_valence_electrons': -55.6062832263,
        'fermi_energy': 0.1848170588,
        'fermi_energy_units': 'Htr',
        'gmax': 11.1,
        'kmax': 3.5,
        'number_of_atom_types': 1,
        'number_of_atoms': 2,
        'number_of_iterations': 6,
        'number_of_iterations_total': 6,
        'number_of_species': 1,
        'number_of_spin_components': 1,
        'number_of_symmetries': 48,
        'output_file_version': '0.33',
        'spin_dependent_charge_interstitial': 3.5380095,
        'spin_dependent_charge_mt_spheres': 24.4619905,
        'spin_dependent_charge_total': 28.0,
        'start_date': {
            'date': '2020/12/10',
            'time': '16:51:33'
        },
        'sum_of_eigenvalues': -316.3770860013,
        'title': 'Si bulk',
        'total_charge': 28.0000000002,
        'walltime': 2,
        'walltime_units': 'seconds'
    }

    OUTXML_FILEPATH = os.path.join(outxmlfilefolder_valid[0], 'SiLOXML/files/out.xml')

    out_dict = outxml_parser(OUTXML_FILEPATH, strict=True)

    assert out_dict == expected_result


def test_outxml_firstiter():

    expected_result = {
        'bandgap': 2.5515073686,
        'bandgap_units': 'eV',
        'charge_den_xc_den_integral': -41.7144813139,
        'charge_density': 8.7379598265,
        'creator_name': 'fleur 32',
        'creator_target_architecture': 'GEN',
        'density_convergence_units': 'me/bohr^3',
        'end_date': {
            'date': '2020/12/10',
            'time': '16:51:35'
        },
        'energy': -15784.558462216572,
        'energy_core_electrons': -260.8588755929,
        'energy_hartree': -580.0718291459,
        'energy_hartree_units': 'Htr',
        'energy_units': 'eV',
        'energy_valence_electrons': -56.0370181786,
        'fermi_energy': 0.1670838071,
        'fermi_energy_units': 'Htr',
        'gmax': 11.1,
        'kmax': 3.5,
        'number_of_atom_types': 1,
        'number_of_atoms': 2,
        'number_of_iterations': 6,
        'number_of_iterations_total': 1,
        'number_of_species': 1,
        'number_of_spin_components': 1,
        'number_of_symmetries': 48,
        'output_file_version': '0.33',
        'spin_dependent_charge_interstitial': 3.4450476,
        'spin_dependent_charge_mt_spheres': 24.5549524,
        'spin_dependent_charge_total': 28.0,
        'start_date': {
            'date': '2020/12/10',
            'time': '16:51:33'
        },
        'sum_of_eigenvalues': -316.8958937715,
        'title': 'Si bulk',
        'total_charge': 28.0000000002,
        'walltime': 2,
        'walltime_units': 'seconds'
    }

    OUTXML_FILEPATH = os.path.join(outxmlfilefolder_valid[0], 'SiLOXML/files/out.xml')

    out_dict = outxml_parser(OUTXML_FILEPATH, iteration_to_parse='first', strict=True)

    assert out_dict == expected_result


def test_outxml_alliter():

    expected_result = {
        'bandgap': [2.5515073686, 2.5316946813, 2.2251836966, 2.2557459059, 2.2631994165, 2.2729704824],
        'bandgap_units':
        'eV',
        'charge_den_xc_den_integral':
        [-41.7144813139, -41.7172476721, -41.7835197479, -41.7699610697, -41.7648027154, -41.7653329254],
        'charge_density': [8.7379598265, 8.2515493263, 1.0238480245, 0.5765372317, 0.2277277793, 0.026112816],
        'creator_name':
        'fleur 32',
        'creator_target_architecture':
        'GEN',
        'density_convergence_units':
        'me/bohr^3',
        'end_date': {
            'date': '2020/12/10',
            'time': '16:51:35'
        },
        'energy': [
            -15784.558462216572, -15784.53099477957, -15784.361353401742, -15784.35737835975, -15784.359702783555,
            -15784.360800784752
        ],
        'energy_core_electrons':
        [-260.8588755929, -260.8499161476, -260.706488686, -260.7469665908, -260.7692856056, -260.7708027749],
        'energy_hartree':
        [-580.0718291459, -580.0708197362, -580.0645855305, -580.0644394504, -580.0645248714, -580.0645652222],
        'energy_hartree_units':
        'Htr',
        'energy_units':
        'eV',
        'energy_valence_electrons':
        [-56.0370181786, -55.9991947433, -55.3819222254, -55.5145626436, -55.579927498, -55.6062832263],
        'fermi_energy': [0.1670838071, 0.1682300942, 0.1878849091, 0.1857922767, 0.1853849541, 0.1848170588],
        'fermi_energy_units':
        'Htr',
        'gmax':
        11.1,
        'kmax':
        3.5,
        'number_of_atom_types':
        1,
        'number_of_atoms':
        2,
        'number_of_iterations':
        6,
        'number_of_iterations_total':
        6,
        'number_of_species':
        1,
        'number_of_spin_components':
        1,
        'number_of_symmetries':
        48,
        'output_file_version':
        '0.33',
        'spin_dependent_charge_interstitial': [3.4450476, 3.4514909, 3.5537094, 3.543144, 3.5407065, 3.5380095],
        'spin_dependent_charge_mt_spheres': [24.5549524, 24.5485091, 24.4462906, 24.456856, 24.4592935, 24.4619905],
        'spin_dependent_charge_total': [28.0, 28.0, 28.0, 28.0, 28.0, 28.0],
        'start_date': {
            'date': '2020/12/10',
            'time': '16:51:33'
        },
        'sum_of_eigenvalues':
        [-316.8958937715, -316.8491108909, -316.0884109114, -316.2615292344, -316.3492131037, -316.3770860013],
        'title':
        'Si bulk',
        'total_charge': [28.0000000002, 28.0000000002, 28.0000000002, 28.0000000002, 28.0000000002, 28.0000000002],
        'walltime':
        2,
        'walltime_units':
        'seconds'
    }

    OUTXML_FILEPATH = os.path.join(outxmlfilefolder_valid[0], 'SiLOXML/files/out.xml')

    out_dict = outxml_parser(OUTXML_FILEPATH, iteration_to_parse='all', strict=True)

    assert out_dict == expected_result


def test_outxml_indexiter():

    expected_result = {
        'bandgap': 2.2557459059,
        'bandgap_units': 'eV',
        'charge_den_xc_den_integral': -41.7699610697,
        'charge_density': 0.5765372317,
        'creator_name': 'fleur 32',
        'creator_target_architecture': 'GEN',
        'density_convergence_units': 'me/bohr^3',
        'end_date': {
            'date': '2020/12/10',
            'time': '16:51:35'
        },
        'energy': -15784.35737835975,
        'energy_core_electrons': -260.7469665908,
        'energy_hartree': -580.0644394504,
        'energy_hartree_units': 'Htr',
        'energy_units': 'eV',
        'energy_valence_electrons': -55.5145626436,
        'fermi_energy': 0.1857922767,
        'fermi_energy_units': 'Htr',
        'gmax': 11.1,
        'kmax': 3.5,
        'number_of_atom_types': 1,
        'number_of_atoms': 2,
        'number_of_iterations': 6,
        'number_of_iterations_total': 4,
        'number_of_species': 1,
        'number_of_spin_components': 1,
        'number_of_symmetries': 48,
        'output_file_version': '0.33',
        'spin_dependent_charge_interstitial': 3.543144,
        'spin_dependent_charge_mt_spheres': 24.456856,
        'spin_dependent_charge_total': 28.0,
        'start_date': {
            'date': '2020/12/10',
            'time': '16:51:33'
        },
        'sum_of_eigenvalues': -316.2615292344,
        'title': 'Si bulk',
        'total_charge': 28.0000000002,
        'walltime': 2,
        'walltime_units': 'seconds'
    }

    OUTXML_FILEPATH = os.path.join(outxmlfilefolder_valid[0], 'SiLOXML/files/out.xml')
    print(OUTXML_FILEPATH)
    out_dict = outxml_parser(OUTXML_FILEPATH, iteration_to_parse=3, strict=True)

    assert out_dict == expected_result


def test_outxml_minimal_mode():

    expected_result = {
        'charge_density': [8.7379598265, 8.2515493263, 1.0238480245, 0.5765372317, 0.2277277793, 0.026112816],
        'creator_name':
        'fleur 32',
        'creator_target_architecture':
        'GEN',
        'density_convergence_units':
        'me/bohr^3',
        'end_date': {
            'date': '2020/12/10',
            'time': '16:51:35'
        },
        'energy': [
            -15784.558462216572, -15784.53099477957, -15784.361353401742, -15784.35737835975, -15784.359702783555,
            -15784.360800784752
        ],
        'energy_hartree':
        [-580.0718291459, -580.0708197362, -580.0645855305, -580.0644394504, -580.0645248714, -580.0645652222],
        'energy_hartree_units':
        'Htr',
        'energy_units':
        'eV',
        'gmax':
        11.1,
        'kmax':
        3.5,
        'number_of_atom_types':
        1,
        'number_of_atoms':
        2,
        'number_of_iterations':
        6,
        'number_of_iterations_total':
        6,
        'number_of_species':
        1,
        'number_of_spin_components':
        1,
        'number_of_symmetries':
        48,
        'output_file_version':
        '0.33',
        'start_date': {
            'date': '2020/12/10',
            'time': '16:51:33'
        },
        'title':
        'Si bulk',
        'walltime':
        2,
        'walltime_units':
        'seconds'
    }

    OUTXML_FILEPATH = os.path.join(outxmlfilefolder_valid[0], 'SiLOXML/files/out.xml')

    out_dict = outxml_parser(OUTXML_FILEPATH, iteration_to_parse='all', minimal_mode=True, strict=True)

    assert out_dict == expected_result


def test_outxml_magnetic():

    expected_result = {
        'bandgap': [0.0349628152, 0.0323610284, 0.021741434, 0.0572228408],
        'bandgap_units':
        'eV',
        'charge_den_xc_den_integral': [-111.944467235, -111.9182938603, -111.8007620588, -111.8088374177],
        'charge_density': [[10.9851472966, 6.0389329792], [9.2786635283, 5.4278279348], [2.682660905, 4.3593512086],
                           [2.4271463257, 2.7205971142]],
        'creator_name':
        'fleur 32',
        'creator_target_architecture':
        'GEN',
        'density_convergence_units':
        'me/bohr^3',
        'end_date': {
            'date': '2020/12/10',
            'time': '16:53:09'
        },
        'energy': [-69269.26222704063, -69269.20103443766, -69269.1612911444, -69269.20170072748],
        'energy_core_electrons': [-1455.1337167156, -1455.4152321083, -1456.700254102, -1456.7494708632],
        'energy_hartree': [-2545.5984555924, -2545.5962068057, -2545.5947462666, -2545.5962312914],
        'energy_hartree_units':
        'Htr',
        'energy_units':
        'eV',
        'energy_valence_electrons': [-14.3239528838, -14.4723754179, -15.168729029, -15.3104862098],
        'fermi_energy': [0.3836568571, 0.3782147185, 0.3527552733, 0.3477025411],
        'fermi_energy_units':
        'Htr',
        'gmax':
        10.2,
        'kmax':
        3.4,
        'magnetic_moments': [[1.9248831159, 1.9271597822], [1.9333985458, 1.9345705319], [1.9618319469, 1.9642032919],
                             [1.921322941, 1.9069167578]],
        'magnetic_moments_spin_down_charge': [[5.5287872657, 5.526614088], [5.5306467297, 5.5301342089],
                                              [5.5471397772, 5.5448063511], [5.5571226156, 5.5769454898]],
        'magnetic_moments_spin_up_charge': [[7.4536703815, 7.4537738701], [7.4640452754, 7.4647047409],
                                            [7.5089717241, 7.509009643], [7.4784455566, 7.4838622476]],
        'number_of_atom_types':
        2,
        'number_of_atoms':
        2,
        'number_of_iterations':
        4,
        'number_of_iterations_total':
        4,
        'number_of_species':
        1,
        'number_of_spin_components':
        2,
        'number_of_symmetries':
        16,
        'output_file_version':
        '0.33',
        'overall_charge_density': [13.455846664, 10.8914872112, 3.3253791756, 1.5936155801],
        'spin_density': [11.5422933539, 10.6059102509, 6.4298583438, 4.9036481595],
        'spin_dependent_charge_interstitial': [[1.0181605, 1.0212141], [1.00491, 1.0077593], [0.9449583, 0.9472272],
                                               [0.953185, 0.9525573]],
        'spin_dependent_charge_mt_spheres': [[26.9063802, 23.0542457], [26.927695, 23.059636], [27.0169661, 23.0908487],
                                             [26.961288, 23.1329699]],
        'spin_dependent_charge_total': [[27.9245407, 24.0754597], [27.932605, 24.0673954], [27.9619244, 24.0380759],
                                        [27.914473, 24.0855272]],
        'start_date': {
            'date': '2020/12/10',
            'time': '16:53:07'
        },
        'sum_of_eigenvalues': [-1469.4576695994, -1469.8876075262, -1471.8689831309, -1472.059957073],
        'title':
        'Fe fcc 2',
        'total_charge': [52.0000004, 52.0000003806, 52.0000002753, 52.0000001251],
        'total_magnetic_moment_cell': [3.8490810000000018, 3.8652096, 3.923848500000002, 3.8289457999999996],
        'walltime':
        2,
        'walltime_units':
        'seconds'
    }

    OUTXML_FILEPATH = os.path.join(outxmlfilefolder_valid[0], 'Fe_bct_LOXML/files/out.xml')

    out_dict = outxml_parser(OUTXML_FILEPATH, iteration_to_parse='all', strict=True)

    assert out_dict == expected_result


def test_outxml_ldaurelax():

    expected_result = {
        'abspos_x_type1': [-1.3806, -1.3806],
        'abspos_x_type2': [1.3806, 1.3806],
        'abspos_y_type1': [-1.3806, -1.3806],
        'abspos_y_type2': [1.3806, 1.3806],
        'abspos_z_type1': [-1.3806, -1.3806],
        'abspos_z_type2': [1.3806, 1.3806],
        'bandgap': [4.1667073913, 4.1667065775],
        'bandgap_units': 'eV',
        'charge_den_xc_den_integral': [-159.6317907519, -159.6317901441],
        'charge_density': 0.0003427664,
        'creator_name': 'fleur 32',
        'creator_target_architecture': 'GEN',
        'density_convergence_units': 'me/bohr^3',
        'end_date': {
            'date': '2020/12/10',
            'time': '16:52:15'
        },
        'energy': [-114416.0970707565, -114416.09707142044],
        'energy_core_electrons': [-2406.2024893454, -2406.2024979422],
        'energy_hartree': [-4204.714048254, -4204.7140482784],
        'energy_hartree_units': 'Htr',
        'energy_units': 'eV',
        'energy_valence_electrons': [-16.1166243591, -16.1166281237],
        'fermi_energy': [0.1259314171, 0.1259314083],
        'fermi_energy_units': 'Htr',
        'film': False,
        'force_largest': [0.01798072, 0.01798072],
        'force_units': 'Htr/bohr',
        'force_x_type1': [0.01798072, 0.01798072],
        'force_x_type2': [-0.01797115, -0.01797158],
        'force_y_type1': [0.01798072, 0.01798072],
        'force_y_type2': [-0.01797115, -0.01797158],
        'force_z_type1': [0.01798072, 0.01798072],
        'force_z_type2': [-0.01797115, -0.01797158],
        'gmax': 10.8,
        'kmax': 3.6,
        'ldau_info': {
            'As-2/33': {
                'd': {
                    'double_counting': 'FLL',
                    'j': 0.9,
                    'u': 5.5,
                    'unit': 'eV'
                },
                'p': {
                    'double_counting': 'FLL',
                    'j': 0.9,
                    'u': -6.5,
                    'unit': 'eV'
                }
            },
            'Ga-1/31': {
                'd': {
                    'double_counting': 'FLL',
                    'j': 0.9,
                    'u': 8.0,
                    'unit': 'eV'
                },
                'p': {
                    'double_counting': 'FLL',
                    'j': 0.9,
                    'u': -5.0,
                    'unit': 'eV'
                }
            },
            'density_matrix_distance': 2.3e-05,
            'ldau_energy_correction': [-2.6822617141, -2.6822616556]
        },
        'number_of_atom_types': 2,
        'number_of_atoms': 2,
        'number_of_iterations': 2,
        'number_of_iterations_total': 15,
        'number_of_species': 2,
        'number_of_spin_components': 1,
        'number_of_symmetries': 6,
        'output_file_version': '0.33',
        'relax_atom_positions': [[-0.13, -0.13, -0.13], [0.13, 0.13, 0.13]],
        'relax_atomtype_info': [['Ga-1', 'Ga'], ['As-2', 'As']],
        'relax_brav_vectors': [[0.0, 5.31, 5.31], [5.31, 0.0, 5.31], [5.31, 5.31, 0.0]],
        'spin_dependent_charge_interstitial': [3.5031316, 3.5031315],
        'spin_dependent_charge_mt_spheres': [60.4968684, 60.4968685],
        'spin_dependent_charge_total': [64.0, 64.0],
        'start_date': {
            'date': '2020/12/10',
            'time': '16:52:14'
        },
        'sum_of_eigenvalues': [-2422.3191137045, -2422.3191260659],
        'title': 'GaAs bulk zinc-blende structure',
        'total_charge': [63.9999999893, 63.9999999893],
        'walltime': 1,
        'walltime_units': 'seconds'
    }

    OUTXML_FILEPATH = os.path.join(outxmlfilefolder_valid[0], 'GaAsMultiUForceXML/files/out.xml')

    out_dict = outxml_parser(OUTXML_FILEPATH, iteration_to_parse='all', strict=True)

    assert out_dict == expected_result


def test_outxml_force():

    expected_result = {
        'creator_name': 'fleur 32',
        'creator_target_architecture': 'GEN',
        'end_date': {
            'date': '2020/12/10',
            'time': '16:58:39'
        },
        'gmax': 10.0,
        'kmax': 4.0,
        'number_of_atom_types': 2,
        'number_of_atoms': 2,
        'number_of_iterations': 1,
        'number_of_species': 2,
        'number_of_spin_components': 2,
        'number_of_symmetries': 2,
        'output_file_version': '0.33',
        'spst_force_ev-sum': [-37.3674567, -37.3421158],
        'spst_force_q': [1, 2],
        'spst_force_qs': 2,
        'spst_force_units': 'Htr',
        'start_date': {
            'date': '2020/12/10',
            'time': '16:58:34'
        },
        'title': 'A Fleur input generator calculation with aiida',
        'walltime': 5,
        'walltime_units': 'seconds'
    }

    OUTXML_FILEPATH = os.path.join(outxmlfilefolder_valid[0], 'FePt_film_SSFT_LO/files/out.xml')

    out_dict = outxml_parser(OUTXML_FILEPATH, iteration_to_parse='all', strict=True)

    assert out_dict == expected_result
