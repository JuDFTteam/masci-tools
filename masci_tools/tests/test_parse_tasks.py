# -*- coding: utf-8 -*-
"""
Tests for the ParseTasks class
"""


def test_default_parse_tasks():
    """
    Test the default parsing tasks fro inconsitencies/typos
    """
    from masci_tools.io.parsers.fleur import ParseTasks

    expected_keys = {
        'film_relax_info', 'distances', 'forcetheorem_jij', 'ldau_info', 'bulk_relax_info', 'orbital_magnetic_moments',
        'forcetheorem_mae', 'fleur_modes', 'charges', 'magnetic_distances', 'bandgap', 'forcetheorem_ssdisp',
        'total_energy_contributions', 'ldau_energy_correction', 'general_out_info', 'forces', 'nmmp_distances',
        'total_energy', 'magnetic_moments', 'iteration_number', 'forcetheorem_dmi', 'general_inp_info', 'fermi_energy'
    }

    p = ParseTasks('0.33', validate_defaults=True)

    print(set(p.tasks.keys()))
    assert set(p.tasks.keys()) == expected_keys
