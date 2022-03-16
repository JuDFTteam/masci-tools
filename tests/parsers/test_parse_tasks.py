"""
Tests for the ParseTasks class
"""


def test_default_parse_tasks():
    """
    Test the default parsing tasks for inconsitencies/typos
    """
    from masci_tools.util.parse_tasks import ParseTasks

    from masci_tools.io.parsers.fleur import default_parse_tasks as tasks

    expected_keys = set(tasks.TASKS_DEFINITION.keys())
    p = ParseTasks(tasks.__base_version__, validate_defaults=True)

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
