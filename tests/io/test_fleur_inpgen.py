"""
Tests of the fleur_inpgen module
"""
import tempfile
from pathlib import Path
import numpy as np
from masci_tools.io.common_functions import convert_to_pystd


def test_write_inpgen_file_defaults_dict(file_regression):

    from masci_tools.io.fleur_inpgen import write_inpgen_file

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

    with tempfile.TemporaryFile('w+') as tmp:

        write_inpgen_file(cell, sites, kinds, file=tmp)
        tmp.seek(0)
        content = tmp.read()

    file_regression.check(content)


def test_write_inpgen_file_magmom_str(file_regression):

    from masci_tools.io.fleur_inpgen import write_inpgen_file

    param = 5.43
    cell = [[0, param / 2., param / 2.], [param / 2., 0, param / 2.], [param / 2., param / 2., 0]]
    kinds = [{'symbols': ('Si',), 'weights': (1.0,), 'mass': 28.0855, 'name': 'Si'}]
    sites = [{
        'position': (0.0, 0.0, 0.0),
        'kind_name': 'Si',
        'magnetic_moment': 'up'
    }, {
        'position': (1.3575, 1.3575, 1.3575),
        'kind_name': 'Si',
        'magnetic_moment': 'down'
    }]

    with tempfile.TemporaryFile('w+') as tmp:

        write_inpgen_file(cell, sites, kinds, file=tmp)
        tmp.seek(0)
        content = tmp.read()

    file_regression.check(content)


def test_write_inpgen_file_magmom_float(file_regression):

    from masci_tools.io.fleur_inpgen import write_inpgen_file

    param = 5.43
    cell = [[0, param / 2., param / 2.], [param / 2., 0, param / 2.], [param / 2., param / 2., 0]]
    kinds = [{'symbols': ('Si',), 'weights': (1.0,), 'mass': 28.0855, 'name': 'Si'}]
    sites = [{
        'position': (0.0, 0.0, 0.0),
        'kind_name': 'Si',
        'magnetic_moment': 1
    }, {
        'position': (1.3575, 1.3575, 1.3575),
        'kind_name': 'Si',
        'magnetic_moment': 2
    }]

    with tempfile.TemporaryFile('w+') as tmp:

        write_inpgen_file(cell, sites, kinds, file=tmp)
        tmp.seek(0)
        content = tmp.read()

    file_regression.check(content)


def test_write_inpgen_file_magmom_list(file_regression):

    from masci_tools.io.fleur_inpgen import write_inpgen_file

    param = 5.43
    cell = [[0, param / 2., param / 2.], [param / 2., 0, param / 2.], [param / 2., param / 2., 0]]
    kinds = [{'symbols': ('Si',), 'weights': (1.0,), 'mass': 28.0855, 'name': 'Si'}]
    sites = [{
        'position': (0.0, 0.0, 0.0),
        'kind_name': 'Si',
        'magnetic_moment': [1, 2, 3]
    }, {
        'position': (1.3575, 1.3575, 1.3575),
        'kind_name': 'Si',
        'magnetic_moment': [4, 5, 6]
    }]

    with tempfile.TemporaryFile('w+') as tmp:

        write_inpgen_file(cell, sites, kinds, file=tmp)
        tmp.seek(0)
        content = tmp.read()

    file_regression.check(content)


def test_write_inpgen_file_defaults_dict_filename(file_regression):

    from masci_tools.io.fleur_inpgen import write_inpgen_file

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

    with tempfile.TemporaryDirectory() as td:

        write_inpgen_file(cell, sites, kinds, file=Path(td) / 'result.txt')

        with open(Path(td) / 'result.txt', encoding='utf-8') as file:
            content = file.read()

    file_regression.check(content, basename='test_write_inpgen_file_defaults_dict')


def test_write_inpgen_file_defaults_str(file_regression):

    from masci_tools.io.fleur_inpgen import write_inpgen_file

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

    content = write_inpgen_file(cell, sites, kinds, return_contents=True)
    file_regression.check(content)


def test_write_inpgen_file_defaults_tuple(file_regression):

    from masci_tools.io.fleur_inpgen import write_inpgen_file

    param = 5.43
    cell = [[0, param / 2., param / 2.], [param / 2., 0, param / 2.], [param / 2., param / 2., 0]]
    sites = [((0.0, 0.0, 0.0), 'Si', 'Si'), ((1.3575, 1.3575, 1.3575), 'Si', 'Si')]

    with tempfile.TemporaryFile('w+') as tmp:

        write_inpgen_file(cell, sites, file=tmp)
        tmp.seek(0)
        content = tmp.read()

    file_regression.check(content)


def test_write_inpgen_file_defaults_direct(file_regression):

    from masci_tools.io.fleur_inpgen import write_inpgen_file
    from masci_tools.io.common_functions import AtomSiteProperties

    param = 5.43
    cell = [[0, param / 2., param / 2.], [param / 2., 0, param / 2.], [param / 2., param / 2., 0]]
    sites = [
        AtomSiteProperties(position=(0.0, 0.0, 0.0), symbol='Si', kind='Si'),
        AtomSiteProperties(position=(1.3575, 1.3575, 1.3575), symbol='Si', kind='Si')
    ]

    with tempfile.TemporaryFile('w+') as tmp:

        write_inpgen_file(cell, sites, file=tmp)
        tmp.seek(0)
        content = tmp.read()

    file_regression.check(content)


def test_write_inpgen_file_parameters(file_regression):

    from masci_tools.io.fleur_inpgen import write_inpgen_file

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

    with tempfile.TemporaryFile('w+') as tmp:

        write_inpgen_file(cell, sites, kinds, input_params=parameters, file=tmp)
        tmp.seek(0)
        content = tmp.read()

    file_regression.check(content)


def test_write_inpgen_file_econfig(file_regression):

    from masci_tools.io.fleur_inpgen import write_inpgen_file

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
            'lnonsph': 6,
            'econfig': '[He] 2s2 2p6 | 3s2 3p2',
            'lo': ''
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

    with tempfile.TemporaryFile('w+') as tmp:

        write_inpgen_file(cell, sites, kinds, input_params=parameters, file=tmp)
        tmp.seek(0)
        content = tmp.read()

    file_regression.check(content)


def test_write_inpgen_file_soc_qss(file_regression):

    from masci_tools.io.fleur_inpgen import write_inpgen_file

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

    with tempfile.TemporaryFile('w+') as tmp:

        write_inpgen_file(cell, sites, kinds, input_params=parameters, file=tmp)
        tmp.seek(0)
        content = tmp.read()

    file_regression.check(content)


def test_write_inpgen_file_film(file_regression):

    from masci_tools.io.fleur_inpgen import write_inpgen_file

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

    with tempfile.TemporaryFile('w+') as tmp:

        write_inpgen_file(cell, sites, kinds, input_params=parameters, file=tmp, pbc=(True, True, False))
        tmp.seek(0)
        content = tmp.read()

    file_regression.check(content)


def test_write_inpgen_file_x_and_bunchatom(file_regression):

    from masci_tools.io.fleur_inpgen import write_inpgen_file

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
    }, {
        'symbols': ('X',),
        'weights': (1.0,),
        'mass': 1.0,
        'name': 'X'
    }]
    sites = [{
        'position': (0.0, 0.0, 1.1726940557829),
        'kind_name': 'X'
    }, {
        'position': (1.6584398382215, 0.0, 3.5180821673487),
        'kind_name': 'X'
    }, {
        'position': (0.0, 0.0, 5.8634702789145),
        'kind_name': 'X'
    }, {
        'position': (1.6584398382215, 0.0, 8.2088583904803),
        'kind_name': 'Fe'
    }, {
        'position': (0.0, 0.0, 10.096376717551),
        'kind_name': 'Nb'
    }, {
        'position': (1.6584398382215, 0.0, 12.46832205832),
        'kind_name': 'Nb'
    }]

    with tempfile.TemporaryFile('w+') as tmp:

        write_inpgen_file(cell, sites, kinds, file=tmp, pbc=(True, True, False))
        tmp.seek(0)
        content = tmp.read()

    file_regression.check(content)


def test_read_inpgen_file(datadir, data_regression):
    from masci_tools.io.fleur_inpgen import read_inpgen_file

    TESTFILE = datadir / 'test_write_inpgen_file_defaults_dict.txt'

    cell, atom_sites, pbc, input_params = read_inpgen_file(TESTFILE)

    data_regression.check({
        'cell': convert_to_pystd(cell),
        'atom_sites': [tuple(convert_to_pystd(site)) for site in atom_sites],
        'pbc': pbc,
        'params': convert_to_pystd(input_params)
    })


def test_read_inpgen_file_contents(datadir, data_regression):
    from masci_tools.io.fleur_inpgen import read_inpgen_file

    TESTFILE = datadir / 'test_write_inpgen_file_defaults_dict.txt'

    with open(TESTFILE, encoding='utf-8') as f:
        content = f.read()

    cell, atom_sites, pbc, input_params = read_inpgen_file(content)

    data_regression.check({
        'cell': convert_to_pystd(cell),
        'atom_sites': [tuple(convert_to_pystd(site)) for site in atom_sites],
        'pbc': pbc,
        'params': convert_to_pystd(input_params)
    })


def test_read_inpgen_file_handle(datadir, data_regression):
    from masci_tools.io.fleur_inpgen import read_inpgen_file

    TESTFILE = datadir / 'test_write_inpgen_file_defaults_dict.txt'

    with open(TESTFILE, encoding='utf-8') as f:
        cell, atom_sites, pbc, input_params = read_inpgen_file(f)

    data_regression.check({
        'cell': convert_to_pystd(cell),
        'atom_sites': [tuple(convert_to_pystd(site)) for site in atom_sites],
        'pbc': pbc,
        'params': convert_to_pystd(input_params)
    })


def test_read_inpgen_file_parameters(datadir, data_regression):
    from masci_tools.io.fleur_inpgen import read_inpgen_file

    TESTFILE = datadir / 'test_write_inpgen_file_parameters.txt'

    cell, atom_sites, pbc, input_params = read_inpgen_file(TESTFILE)

    data_regression.check({
        'cell': convert_to_pystd(cell),
        'atom_sites': [tuple(convert_to_pystd(site)) for site in atom_sites],
        'pbc': pbc,
        'params': convert_to_pystd(input_params)
    })


def test_read_inpgen_file_econfig(datadir, data_regression):
    from masci_tools.io.fleur_inpgen import read_inpgen_file

    TESTFILE = datadir / 'test_write_inpgen_file_econfig.txt'

    cell, atom_sites, pbc, input_params = read_inpgen_file(TESTFILE)

    data_regression.check({
        'cell': convert_to_pystd(cell),
        'atom_sites': [tuple(convert_to_pystd(site)) for site in atom_sites],
        'pbc': pbc,
        'params': convert_to_pystd(input_params)
    })


def test_read_inpgen_file_soc_qss(datadir, data_regression):
    from masci_tools.io.fleur_inpgen import read_inpgen_file

    TESTFILE = datadir / 'test_write_inpgen_file_soc_qss.txt'

    cell, atom_sites, pbc, input_params = read_inpgen_file(TESTFILE)

    data_regression.check({
        'cell': convert_to_pystd(cell),
        'atom_sites': [tuple(convert_to_pystd(site)) for site in atom_sites],
        'pbc': pbc,
        'params': convert_to_pystd(input_params)
    })


def test_read_inpgen_file_film(datadir, data_regression):
    from masci_tools.io.fleur_inpgen import read_inpgen_file

    TESTFILE = datadir / 'test_write_inpgen_file_film.txt'

    cell, atom_sites, pbc, input_params = read_inpgen_file(TESTFILE)

    data_regression.check({
        'cell': convert_to_pystd(cell),
        'atom_sites': [tuple(convert_to_pystd(site)) for site in atom_sites],
        'pbc': pbc,
        'params': convert_to_pystd(input_params)
    })


def test_read_inpgen_file_comments(datadir, data_regression):
    from masci_tools.io.fleur_inpgen import read_inpgen_file

    TESTFILE = datadir / 'inpgen_file_with_comments.txt'

    cell, atom_sites, pbc, input_params = read_inpgen_file(TESTFILE)

    data_regression.check({
        'cell': convert_to_pystd(cell),
        'atom_sites': [tuple(convert_to_pystd(site)) for site in atom_sites],
        'pbc': pbc,
        'params': convert_to_pystd(input_params)
    })


def test_read_inpgen_file_magmom_str(datadir, data_regression):
    from masci_tools.io.fleur_inpgen import read_inpgen_file

    TESTFILE = datadir / 'test_write_inpgen_file_magmom_str.txt'

    cell, atom_sites, pbc, input_params = read_inpgen_file(TESTFILE)

    data_regression.check({
        'cell': convert_to_pystd(cell),
        'atom_sites': [tuple(convert_to_pystd(site)) for site in atom_sites],
        'pbc': pbc,
        'params': convert_to_pystd(input_params)
    })


def test_read_inpgen_file_magmom_float(datadir, data_regression):
    from masci_tools.io.fleur_inpgen import read_inpgen_file

    TESTFILE = datadir / 'test_write_inpgen_file_magmom_float.txt'

    cell, atom_sites, pbc, input_params = read_inpgen_file(TESTFILE)

    data_regression.check({
        'cell': convert_to_pystd(cell),
        'atom_sites': [tuple(convert_to_pystd(site)) for site in atom_sites],
        'pbc': pbc,
        'params': convert_to_pystd(input_params)
    })


def test_read_inpgen_file_magmom_list(datadir, data_regression):
    from masci_tools.io.fleur_inpgen import read_inpgen_file

    TESTFILE = datadir / 'test_write_inpgen_file_magmom_list.txt'

    cell, atom_sites, pbc, input_params = read_inpgen_file(TESTFILE)

    data_regression.check({
        'cell': convert_to_pystd(cell),
        'atom_sites': [tuple(convert_to_pystd(site)) for site in atom_sites],
        'pbc': pbc,
        'params': convert_to_pystd(input_params)
    })


def test_get_parameter_write_inpgen_roundtrip(file_regression, load_inpxml):
    """
    Test that the get_parameterdata and get_structuredata methods produces the right inpgen input
    to produce the right roundtrip
    """
    from masci_tools.io.fleur_inpgen import write_inpgen_file
    from masci_tools.util.xml.xml_getters import get_parameterdata, get_structuredata

    xmltree, schema_dict = load_inpxml('fleur/Max-R5/SiLOXML/files/inp.xml', absolute=False)

    params = get_parameterdata(xmltree, schema_dict)
    atoms, cell, pbc = get_structuredata(xmltree, schema_dict)

    with tempfile.TemporaryFile('w+') as tmp:

        write_inpgen_file(cell, atoms, input_params=params, file=tmp)
        tmp.seek(0)
        content = tmp.read()

    file_regression.check(content)


def test_mag_mom_list_write_inpgen_roundtrip(file_regression, load_inpxml):
    """
    Test that the get_structuredata methods produces the right inpgen input with noco angles
    to produce the right roundtrip
    """
    from masci_tools.io.fleur_inpgen import write_inpgen_file
    from masci_tools.util.xml.xml_getters import get_structuredata

    xmltree, schema_dict = load_inpxml('fleur/Max-R5/Fe_bctXML/files/inp.xml', absolute=False)

    atoms, cell, pbc = get_structuredata(xmltree, schema_dict)

    with tempfile.TemporaryFile('w+') as tmp:

        write_inpgen_file(cell, atoms, file=tmp)
        tmp.seek(0)
        content = tmp.read()

    file_regression.check(content)


def test_mag_mom_float_write_inpgen_roundtrip(file_regression, load_inpxml):
    """
    Test that the get_structuredata methods produces the right inpgen input with collinear setup
    to produce the right roundtrip
    """
    from masci_tools.io.fleur_inpgen import write_inpgen_file
    from masci_tools.util.xml.xml_getters import get_structuredata

    xmltree, schema_dict = load_inpxml('fleur/Max-R6/inp_NiO.xml', absolute=False)

    atoms, cell, pbc = get_structuredata(xmltree, schema_dict)

    with tempfile.TemporaryFile('w+') as tmp:

        write_inpgen_file(cell, atoms, file=tmp)
        tmp.seek(0)
        content = tmp.read()

    file_regression.check(content)


def test_mag_mom_list_noco_angle_write_inpgen_roundtrip(file_regression, load_inpxml):
    """
    Test that the get_structuredata methods produces the right inpgen input with collinear setup
    to produce the right roundtrip
    """
    from masci_tools.io.fleur_inpgen import write_inpgen_file
    from masci_tools.util.xml.xml_getters import get_structuredata

    xmltree, schema_dict = load_inpxml('fleur/Max-R5/Fe_fccXML/files/inp.xml', absolute=False)

    atoms, cell, pbc = get_structuredata(xmltree, schema_dict)

    with tempfile.TemporaryFile('w+') as tmp:

        write_inpgen_file(cell, atoms, file=tmp)
        tmp.seek(0)
        content = tmp.read()

    file_regression.check(content)
