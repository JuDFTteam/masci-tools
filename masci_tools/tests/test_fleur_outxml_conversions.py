# -*- coding: utf-8 -*-
"""
Tests for fleur outxml_parser specific conversion functions
"""
import pytest

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

TEST_WARNINGS = [
    {
        'parser_warnings': []
    },
    {
        'parser_warnings': []
    },
    {
        'parser_warnings': []
    },
    {
        'parser_warnings': []
    },
    {
        'parser_warnings': []
    },
    {
        'parser_warnings': [
            'Endtime was unparsed, inp.xml prob not complete, do not believe the walltime!',
            'Enddate was unparsed, inp.xml prob not complete, do not believe the walltime!'
        ]
    },
    {
        'parser_warnings': [
            'Starttime was unparsed, inp.xml prob not complete, do not believe the walltime!',
            'Startdate was unparsed, inp.xml prob not complete, do not believe the walltime!'
        ]
    },
    {
        'parser_warnings': [
            'Starttime was unparsed, inp.xml prob not complete, do not believe the walltime!',
            'Endtime was unparsed, inp.xml prob not complete, do not believe the walltime!',
            'Startdate was unparsed, inp.xml prob not complete, do not believe the walltime!',
            'Enddate was unparsed, inp.xml prob not complete, do not believe the walltime!'
        ]
    },
]


@pytest.mark.parametrize('input_dict, walltime, warnings', zip(TEST_DICTS, TEST_WALLTIMES, TEST_WARNINGS))
def test_calculate_walltime(input_dict, walltime, warnings):
    """
   Test of the calculate_walltime function
   """
    from masci_tools.util.fleur_outxml_conversions import calculate_walltime

    parser_warnings = {'parser_warnings': []}
    out_dict = calculate_walltime(input_dict, parser_info_out=parser_warnings)

    assert out_dict['walltime_units'] == 'seconds'
    assert out_dict['walltime'] == walltime
    print(parser_warnings)
    assert parser_warnings == warnings
