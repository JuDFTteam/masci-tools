"""
Tests for the ParseTasks class
"""


def test_default_parse_tasks():
    """
    Test the default parsing tasks for inconsitencies/typos
    """
    from masci_tools.util.parse_tasks import ParseTasks

    expected_keys = {
        'relax_info', 'distances', 'forcetheorem_jij', 'ldau_info', 'orbital_magnetic_moments', 'forcetheorem_mae',
        'charges', 'magnetic_distances', 'bandgap', 'forcetheorem_ssdisp', 'total_energy_contributions',
        'ldau_energy_correction', 'general_out_info', 'forces', 'nmmp_distances', 'total_energy', 'magnetic_moments',
        'iteration_number', 'forcetheorem_dmi', 'general_inp_info', 'fermi_energy', 'torques', 'noco_angles',
        'corelevels', 'hubbard1_distances', 'ldahia_info'
    }

    p = ParseTasks('0.33', validate_defaults=True)

    print(set(p.tasks.keys()))
    assert set(p.tasks.keys()) == expected_keys


def test_find_migration():
    """
    Test the finding of migrations
    """
    from masci_tools.util.parse_tasks import ParseTasks, find_migration

    migrations = ParseTasks('0.33').migrations

    assert len(find_migration('0.34', '0.34', migrations)) == 0
    assert len(find_migration('0.34', '0.33', migrations)) == 1
    assert len(find_migration('0.34', '0.31', migrations)) == 2
    assert find_migration('0.34', '0.01', migrations) is None
