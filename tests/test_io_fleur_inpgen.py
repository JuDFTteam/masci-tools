# -*- coding: utf-8 -*-
"""
Tests of the io_fleur_inpgen module
"""
import tempfile
import numpy as np
from masci_tools.io.common_functions import convert_to_pystd


def test_write_inpgen_file_defaults(file_regression):

    from masci_tools.io.io_fleur_inpgen import write_inpgen_file

    param = 5.43
    cell = [[0, param / 2., param / 2.], [param / 2., 0, param / 2.], [param / 2., param / 2., 0]]
    kinds = [{'symbols': ('Si',), 'weights': (1.0,), 'mass': 28.0855, 'name': 'Si'}]
    sites = [{
        'position': (0.0, 0.0, 0.0),
        'kind_name': 'Si'
    }, {
        'position': (1.3575, 1.3575, 1.3575),
        'kind_name': 'Si'
    }]

    with tempfile.NamedTemporaryFile('r') as tmp:

        write_inpgen_file(cell, sites, kinds, file=tmp.name)
        content = tmp.read()

    file_regression.check(content)


def test_write_inpgen_file_parameters(file_regression):

    from masci_tools.io.io_fleur_inpgen import write_inpgen_file

    param = 5.43
    cell = [[0, param / 2., param / 2.], [param / 2., 0, param / 2.], [param / 2., param / 2., 0]]
    kinds = [{'symbols': ('Si',), 'weights': (1.0,), 'mass': 28.0855, 'name': 'Si'}]
    sites = [{
        'position': (0.0, 0.0, 0.0),
        'kind_name': 'Si'
    }, {
        'position': (1.3575, 1.3575, 1.3575),
        'kind_name': 'Si'
    }]

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

        write_inpgen_file(cell, sites, kinds, input_params=parameters, file=tmp.name)
        content = tmp.read()

    file_regression.check(content)


def test_write_inpgen_file_soc_qss(file_regression):

    from masci_tools.io.io_fleur_inpgen import write_inpgen_file

    param = 5.43
    cell = [[0, param / 2., param / 2.], [param / 2., 0, param / 2.], [param / 2., param / 2., 0]]
    kinds = [{'symbols': ('Si',), 'weights': (1.0,), 'mass': 28.0855, 'name': 'Si'}]
    sites = [{
        'position': (0.0, 0.0, 0.0),
        'kind_name': 'Si'
    }, {
        'position': (1.3575, 1.3575, 1.3575),
        'kind_name': 'Si'
    }]

    parameters = {
        'soc': {
            'theta': np.pi,
            'phi': np.pi / 2.0
        },
        'qss': {
            'x': 1.0,
            'y': 2.0,
            'z': 3.0
        },
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

        write_inpgen_file(cell, sites, kinds, input_params=parameters, file=tmp.name)
        content = tmp.read()

    file_regression.check(content)


def test_write_inpgen_file_film(file_regression):

    from masci_tools.io.io_fleur_inpgen import write_inpgen_file

    cell = [[3.3168796764431, 0.0, 0.0], [1.6584398382215, 2.3453881115923, 0.0], [0.0, 0.0, 13.349076054836]]
    kinds = [{
        'symbols': ('Fe',),
        'weights': (1.0,),
        'mass': 55.845,
        'name': 'Fe'
    }, {
        'symbols': ('Nb',),
        'weights': (1.0,),
        'mass': 92.90638,
        'name': 'Nb'
    }]
    sites = [{
        'position': (1.6584398382215, 0.0, 8.2088583904803),
        'kind_name': 'Fe'
    }, {
        'position': (0.0, 0.0, 10.096376717551),
        'kind_name': 'Nb'
    }, {
        'position': (1.6584398382215, 0.0, 12.46832205832),
        'kind_name': 'Nb'
    }]

    parameters = {
        'comp': {
            'kmax': 5.0,
            'gmaxxc': 12.5,
            'gmax': 15.0
        },
    }

    with tempfile.NamedTemporaryFile('r') as tmp:

        write_inpgen_file(cell, sites, kinds, input_params=parameters, file=tmp.name, pbc=(True, True, False))
        content = tmp.read()

    file_regression.check(content)


def test_read_inpgen_file(data_regression):
    from masci_tools.io.io_fleur_inpgen import read_inpgen_file

    TESTFILE = 'test_io_fleur_inpgen/test_write_inpgen_file_defaults.txt'

    cell, atoms_dict_list, kind_list, pbc, input_params = read_inpgen_file(TESTFILE)

    data_regression.check({
        'cell': convert_to_pystd(cell),
        'atoms': convert_to_pystd(atoms_dict_list),
        'kinds': kind_list,
        'pbc': pbc,
        'params': convert_to_pystd(input_params)
    })


def test_read_inpgen_file_parameters(data_regression):
    from masci_tools.io.io_fleur_inpgen import read_inpgen_file

    TESTFILE = 'test_io_fleur_inpgen/test_write_inpgen_file_parameters.txt'

    cell, atoms_dict_list, kind_list, pbc, input_params = read_inpgen_file(TESTFILE)

    data_regression.check({
        'cell': convert_to_pystd(cell),
        'atoms': convert_to_pystd(atoms_dict_list),
        'kinds': kind_list,
        'pbc': pbc,
        'params': convert_to_pystd(input_params)
    })


def test_read_inpgen_file_soc_qss(data_regression):
    from masci_tools.io.io_fleur_inpgen import read_inpgen_file

    TESTFILE = 'test_io_fleur_inpgen/test_write_inpgen_file_soc_qss.txt'

    cell, atoms_dict_list, kind_list, pbc, input_params = read_inpgen_file(TESTFILE)

    data_regression.check({
        'cell': convert_to_pystd(cell),
        'atoms': convert_to_pystd(atoms_dict_list),
        'kinds': kind_list,
        'pbc': pbc,
        'params': convert_to_pystd(input_params)
    })


def test_read_inpgen_file_film(data_regression):
    from masci_tools.io.io_fleur_inpgen import read_inpgen_file

    TESTFILE = 'test_io_fleur_inpgen/test_write_inpgen_file_film.txt'

    cell, atoms_dict_list, kind_list, pbc, input_params = read_inpgen_file(TESTFILE)

    data_regression.check({
        'cell': convert_to_pystd(cell),
        'atoms': convert_to_pystd(atoms_dict_list),
        'kinds': kind_list,
        'pbc': pbc,
        'params': convert_to_pystd(input_params)
    })
