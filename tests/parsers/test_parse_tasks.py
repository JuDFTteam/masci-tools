"""
Tests for the ParseTasks class
"""


def test_default_parse_tasks():
    """
    Test the default parsing tasks for inconsitencies/typos
    """
    from masci_tools.io.parsers.fleur.fleur_outxml_parser import _TaskParser

    from masci_tools.io.parsers.fleur import default_parse_tasks as tasks

    expected_keys = set(tasks.TASKS_DEFINITION.keys())
    p = _TaskParser(tasks.__base_version__, validate_defaults=True)

    print(set(p.tasks.keys()))
    assert set(p.tasks.keys()) == expected_keys


def test_find_migration():
    """
    Test the finding of migrations
    """
    from masci_tools.io.parsers.fleur.fleur_outxml_parser import _TaskParser, _find_migration

    migrations = _TaskParser('0.33').migrations

    assert len(_find_migration('0.34', '0.34', migrations)) == 0
    assert len(_find_migration('0.34', '0.33', migrations)) == 1
    assert len(_find_migration('0.34', '0.31', migrations)) == 2
    assert _find_migration('0.34', '0.01', migrations) is None
