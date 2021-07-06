"""
Tests of the io_fleur_inpgen module
"""
import tempfile
import numpy as np

def test_write_inpgen_file_defaults(file_regression):

    from masci_tools.io.io_fleur_inpgen import write_inpgen_file

    param = 5.43
    cell = [[0, param / 2., param / 2.], [param / 2., 0, param / 2.], [param / 2., param / 2., 0]]
    kinds = [{'symbols': ('Si',), 'weights': (1.0,), 'mass': 28.0855, 'name': 'Si'}]
    sites = [{'position': (0.0, 0.0, 0.0), 'kind_name': 'Si'},
             {'position': (1.3575, 1.3575, 1.3575), 'kind_name': 'Si'}]

    with tempfile.NamedTemporaryFile('r') as tmp:

        write_inpgen_file(cell, sites, kinds, path = tmp.name)
        content = tmp.read()

    file_regression.check(content)

def test_write_inpgen_file_parameters(file_regression):

    from masci_tools.io.io_fleur_inpgen import write_inpgen_file

    param = 5.43
    cell = [[0, param / 2., param / 2.], [param / 2., 0, param / 2.], [param / 2., param / 2., 0]]
    kinds = [{'symbols': ('Si',), 'weights': (1.0,), 'mass': 28.0855, 'name': 'Si'}]
    sites = [{'position': (0.0, 0.0, 0.0), 'kind_name': 'Si'},
             {'position': (1.3575, 1.3575, 1.3575), 'kind_name': 'Si'}]

    parameters = {
        'atom': {
            'element': 'Si',
            'rmt': 2.1,
            'jri': 981,
            'lmax': 12,
            'lnonsph': 6
        },  #'econfig': '[He] 2s2 2p6 | 3s2 3p2', 'lo': ''},
        'comp': {
            'kmax': 5.0,
            'gmaxxc': 12.5,
            'gmax': 15.0
        },
        'kpt': {
            'div1': 17,
            'div2': 17,
            'div3': 17,
            'tkb': 0.0005
        }
    }

    with tempfile.NamedTemporaryFile('r') as tmp:

        write_inpgen_file(cell, sites, kinds, input_params=parameters, path = tmp.name)
        content = tmp.read()

    file_regression.check(content)

def test_write_inpgen_file_soc_qss(file_regression):

    from masci_tools.io.io_fleur_inpgen import write_inpgen_file

    param = 5.43
    cell = [[0, param / 2., param / 2.], [param / 2., 0, param / 2.], [param / 2., param / 2., 0]]
    kinds = [{'symbols': ('Si',), 'weights': (1.0,), 'mass': 28.0855, 'name': 'Si'}]
    sites = [{'position': (0.0, 0.0, 0.0), 'kind_name': 'Si'},
             {'position': (1.3575, 1.3575, 1.3575), 'kind_name': 'Si'}]

    parameters = {
        'soc': {'theta': np.pi, 'phi': np.pi/2.0},
        'qss': {'x': 1.0, 'y': 2.0, 'z': 3.0},
        'comp': {
            'kmax': 5.0,
            'gmaxxc': 12.5,
            'gmax': 15.0
        },
        'kpt': {
            'div1': 17,
            'div2': 17,
            'div3': 17,
            'tkb': 0.0005
        }
    }

    with tempfile.NamedTemporaryFile('r') as tmp:

        write_inpgen_file(cell, sites, kinds, input_params=parameters, path = tmp.name)
        content = tmp.read()

    file_regression.check(content)

