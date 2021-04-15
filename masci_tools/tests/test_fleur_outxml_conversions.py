# -*- coding: utf-8 -*-
"""
Tests for fleur outxml_parser specific conversion functions
"""
import pytest
import logging

LOGGER = logging.getLogger(__name__)

TEST_DICTS = [{
    'end_date': {
        'date': '2020/12/10',
        'time': '16:51:35'
    },
    'start_date': {
        'date': '2020/12/10',
        'time': '16:51:21'
    }
}, {
    'end_date': {
        'date': '2020/12/10',
        'time': '16:58:49'
    },
    'start_date': {
        'date': '2020/12/10',
        'time': '16:51:21'
    }
}, {
    'end_date': {
        'date': '2020/12/10',
        'time': '22:31:67'
    },
    'start_date': {
        'date': '2020/12/10',
        'time': '16:51:21'
    }
}, {
    'end_date': {
        'date': '2020/12/11',
        'time': '16:51:35'
    },
    'start_date': {
        'date': '2020/12/10',
        'time': '16:51:35'
    }
}, {
    'end_date': {
        'date': '2020/12/31',
        'time': '09:12:45'
    },
    'start_date': {
        'date': '2020/12/10',
        'time': '16:51:21'
    }
}, {
    'end_date': {
        'date': None,
        'time': None
    },
    'start_date': {
        'date': '2020/12/10',
        'time': '16:51:21'
    }
}, {
    'end_date': {
        'date': '2020/12/10',
        'time': '16:51:35'
    },
    'start_date': {
        'date': None,
        'time': None
    }
}, {
    'end_date': {
        'date': None,
        'time': None
    },
    'start_date': {
        'date': None,
        'time': None
    }
}]

TEST_WALLTIMES = [14, 448, 20446, 86400, 1786884, -60681, 60695, 0]

TEST_WARNINGS = [[], [], [], [], [],
                 [
                     'Endtime was unparsed, inp.xml prob not complete, do not believe the walltime!',
                     'Enddate was unparsed, inp.xml prob not complete, do not believe the walltime!'
                 ],
                 [
                     'Starttime was unparsed, inp.xml prob not complete, do not believe the walltime!',
                     'Startdate was unparsed, inp.xml prob not complete, do not believe the walltime!'
                 ],
                 [
                     'Starttime was unparsed, inp.xml prob not complete, do not believe the walltime!',
                     'Endtime was unparsed, inp.xml prob not complete, do not believe the walltime!',
                     'Startdate was unparsed, inp.xml prob not complete, do not believe the walltime!',
                     'Enddate was unparsed, inp.xml prob not complete, do not believe the walltime!'
                 ]]


@pytest.mark.parametrize('input_dict, walltime, warnings', zip(TEST_DICTS, TEST_WALLTIMES, TEST_WARNINGS))
def test_calculate_walltime(caplog, input_dict, walltime, warnings):
    """
   Test of the calculate_walltime function
   """
    from masci_tools.io.parsers.fleur.outxml_conversions import calculate_walltime

    with caplog.at_level(logging.WARNING):
        out_dict = calculate_walltime(input_dict, logger=LOGGER)

        assert out_dict['walltime_units'] == 'seconds'
        assert out_dict['walltime'] == walltime

    if len(warnings) == 0:
        assert caplog.text == ''
    else:
        for expected_warning in warnings:
            assert expected_warning in caplog.text
