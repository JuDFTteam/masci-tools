# -*- coding: utf-8 -*-
"""
Test of the DOS/bandstructure visualizations
"""
import os
import pytest
from matplotlib.pyplot import gcf

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HDFTEST_DIR = os.path.join(CURRENT_DIR, 'files/hdf5_reader')


@pytest.mark.mpl_image_compare(baseline_dir='files/fleur_vis/', filename='bands_defaults.png')
def test_plot_bands_defaults_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    gcf().clear()

    plot_fleur_bands(data, attributes, show=False, markersize=30)

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir='files/fleur_vis/', filename='bands_weighted_non_spinpol.png')
def test_plot_bands_weighted_non_spinpol_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    gcf().clear()

    plot_fleur_bands(data, attributes, show=False, weight='MT:1d')

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir='files/fleur_vis/', filename='bands_defaults_spinpol.png')
def test_plot_bands_spinpol_defaults_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    gcf().clear()

    plot_fleur_bands(data, attributes, show=False, markersize=30)

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir='files/fleur_vis/', filename='bands_weighted_spinpol.png')
def test_plot_bands_weighted_spinpol_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    gcf().clear()

    plot_fleur_bands(data, attributes, show=False, weight='MT:1d')

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir='files/fleur_vis/', filename='bands_spinpol_hide.png')
def test_plot_bands_spinpol_no_spinpol_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    gcf().clear()

    plot_fleur_bands(data, attributes, show=False, markersize=30, spinpol=False)

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir='files/fleur_vis/', filename='bands_only_spin.png')
def test_plot_bands_spinpol_only_spin_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    gcf().clear()

    plot_fleur_bands(data, attributes, show=False, markersize=30, only_spin='up')

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir='files/fleur_vis/', filename='dos_defaults.png')
def test_plot_dos_defaults_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS
    from masci_tools.vis.fleur import plot_fleur_dos

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurDOS)

    gcf().clear()

    plot_fleur_dos(data, attributes, show=False)

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir='files/fleur_vis/', filename='spinpol_dos_defaults.png')
def test_plot_spinpol_dos_defaults_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS
    from masci_tools.vis.fleur import plot_fleur_dos

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurDOS)

    gcf().clear()

    plot_fleur_dos(data, attributes, show=False)

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir='files/fleur_vis/', filename='dos_selection.png')
def test_plot_dos_selection_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS
    from masci_tools.vis.fleur import plot_fleur_dos

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurDOS)

    gcf().clear()

    plot_fleur_dos(data,
                   attributes,
                   show=False,
                   show_total=False,
                   show_interstitial=False,
                   show_atoms=1,
                   show_lresolved=2,
                   plot_keys='MT:1p')

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir='files/fleur_vis/', filename='bands_character.png')
def test_plot_bands_characterize_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands_characterize

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    gcf().clear()

    plot_fleur_bands_characterize(data,
                                  attributes, ['MT:1s', 'MT:1p', 'MT:1d', 'MT:1f'],
                                  ['darkblue', 'darkred', 'darkgreen', 'darkorange'],
                                  show=False,
                                  markersize=30,
                                  only_spin='up')

    return gcf()
