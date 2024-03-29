"""
Test of the DOS/bandstructure visualizations
"""
import os
import pytest
from matplotlib.pyplot import gcf

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HDFTEST_DIR = os.path.join(CURRENT_DIR, '../files/hdf5_reader')
MPL_BASELINE_DIR = os.path.join(CURRENT_DIR, '../files/fleur_vis')


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='bands_defaults.png')
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


def test_plot_bands_defaults_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    fig = plot_fleur_bands(data, attributes, show=False, backend='bokeh')

    check_bokeh_plot(fig)


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='bands_weighted_non_spinpol.png')
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


def test_plot_bands_weighted_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    fig = plot_fleur_bands(data, attributes, weight='MT:1d', show=False, backend='bokeh')

    check_bokeh_plot(fig)


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='bands_line.png')
def test_plot_bands_line_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    gcf().clear()

    plot_fleur_bands(data, attributes, show=False, line_plot=True)

    return gcf()


def test_plot_bands_line_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    fig = plot_fleur_bands(data, attributes, show=False, backend='bokeh', line_plot=True)

    check_bokeh_plot(fig)


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='bands_separate.png')
def test_plot_bands_separate_bands_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    gcf().clear()

    plot_fleur_bands(data, attributes, show=False, separate_bands=True, line_plot=True, color={5: 'red', 3: 'blue'})

    return gcf()


def test_plot_bands_separate_bands_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    p = plot_fleur_bands(data,
                         attributes,
                         backend='bokeh',
                         show=False,
                         separate_bands=True,
                         line_plot=True,
                         color={
                             5: 'red',
                             3: 'blue'
                         })

    check_bokeh_plot(p)


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='bands_defaults_spinpol.png')
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


def test_plot_bands_spinpol_defaults_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    fig = plot_fleur_bands(data, attributes, show=False, backend='bokeh')

    check_bokeh_plot(fig)


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='bands_weighted_spinpol.png')
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


def test_plot_bands_spinpol_weighted_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    fig = plot_fleur_bands(data, attributes, show=False, backend='bokeh', weight='MT:1d')

    check_bokeh_plot(fig)


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='bands_spinpol_line.png')
def test_plot_bands_spinpol_line_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    gcf().clear()

    plot_fleur_bands(data, attributes, show=False, line_plot=True)

    return gcf()


def test_plot_bands_spinpol_line_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    fig = plot_fleur_bands(data, attributes, show=False, backend='bokeh', line_plot=True)

    check_bokeh_plot(fig)


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='bands_spinpol_separate.png')
def test_plot_bands_spinpol_separate_bands_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    gcf().clear()

    plot_fleur_bands(data,
                     attributes,
                     show=False,
                     separate_bands=True,
                     line_plot=True,
                     color={indx: 'green' for indx in range(4, 10)},
                     plot_label={
                         **{
                             0: 'Spin Up',
                             18: 'Spin Down'
                         },
                         **{
                             indx: 'Green Bands' for indx in range(4, 10)
                         }
                     })

    return gcf()


def test_plot_bands_spinpol_separate_bands_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    p = plot_fleur_bands(data,
                         attributes,
                         show=False,
                         backend='bokeh',
                         separate_bands=True,
                         line_plot=True,
                         color={indx: 'green' for indx in range(4, 10)},
                         legend_label={
                             **{
                                 0: 'Spin Up',
                                 18: 'Spin Down'
                             },
                             **{
                                 indx: 'Green Bands' for indx in range(4, 10)
                             }
                         })

    check_bokeh_plot(p)


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='bands_spinpol_hide.png')
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


def test_plot_bands_spinpol_no_spinpol_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    fig = plot_fleur_bands(data, attributes, show=False, backend='bokeh', spinpol=False)

    check_bokeh_plot(fig)


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='bands_only_spin.png')
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


def test_plot_bands_spinpol_only_spin_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    fig = plot_fleur_bands(data, attributes, show=False, backend='bokeh', only_spin='up')

    check_bokeh_plot(fig)


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='dos_defaults.png')
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


def test_plot_dos_defaults_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS
    from masci_tools.vis.fleur import plot_fleur_dos

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurDOS)

    fig = plot_fleur_dos(data, attributes, show=False, backend='bokeh')

    check_bokeh_plot(fig)


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='dos_param_by_label.png')
def test_plot_dos_param_change_by_label_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS
    from masci_tools.vis.fleur import plot_fleur_dos

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurDOS)

    gcf().clear()

    plot_fleur_dos(data, attributes, show=False, color={'MT:1_up': 'red'}, linewidth={'Total_up': 6})

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='dos_param_by_label_with_general_params.png')
def test_plot_dos_param_change_by_label_general_dicts_mpl():
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
                   color={'MT:1_up': 'red'},
                   linewidth={'Total_up': 6},
                   limits={'energy': (-5, 5)},
                   lines={'vertical': [-1, 0, 1]})

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='spinpol_dos_defaults.png')
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


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='spinpol_dos_param_changes.png')
def test_plot_spinpol_dos_param_changes_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS
    from masci_tools.vis.fleur import plot_fleur_dos

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurDOS)

    gcf().clear()

    plot_fleur_dos(data, attributes, show=False, linestyle=['-', ':', '--'])

    return gcf()


def test_plot_spinpol_dos_defaults_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS
    from masci_tools.vis.fleur import plot_fleur_dos

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurDOS)

    fig = plot_fleur_dos(data, attributes, show=False, backend='bokeh')

    check_bokeh_plot(fig)


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='dos_selection.png')
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


def test_plot_dos_selection_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS
    from masci_tools.vis.fleur import plot_fleur_dos

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurDOS)

    fig = plot_fleur_dos(data,
                         attributes,
                         show=False,
                         show_total=False,
                         show_interstitial=False,
                         show_atoms=1,
                         show_lresolved=2,
                         plot_keys='MT:1p',
                         backend='bokeh')

    check_bokeh_plot(fig)


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='spinpol_dos_non_spinpol.png')
def test_plot_spinpol_dos_non_spinpol_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS
    from masci_tools.vis.fleur import plot_fleur_dos

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurDOS)

    gcf().clear()

    plot_fleur_dos(data, attributes, show=False, spinpol=False)

    return gcf()


def test_plot_spinpol_dos_non_spinpol_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS
    from masci_tools.vis.fleur import plot_fleur_dos

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurDOS)

    fig = plot_fleur_dos(data, attributes, show=False, backend='bokeh', spinpol=False)

    check_bokeh_plot(fig)


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='spinpol_dos_only_spin.png')
def test_plot_spinpol_dos_only_spin_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS
    from masci_tools.vis.fleur import plot_fleur_dos

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurDOS)

    gcf().clear()

    plot_fleur_dos(data, attributes, show=False, only_spin='down')

    return gcf()


def test_plot_spinpol_dos_only_spin_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS
    from masci_tools.vis.fleur import plot_fleur_dos

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurDOS)

    fig = plot_fleur_dos(data, attributes, show=False, backend='bokeh', only_spin='down')

    check_bokeh_plot(fig)


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='bands_character.png')
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


def test_plot_bands_characterize_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands_characterize

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    fig = plot_fleur_bands_characterize(data,
                                        attributes, ['MT:1s', 'MT:1p', 'MT:1d', 'MT:1f'],
                                        ['darkblue', 'darkred', 'darkgreen', 'darkorange'],
                                        show=False,
                                        backend='bokeh',
                                        only_spin='up')

    check_bokeh_plot(fig)


#See issue https://github.com/JuDFTteam/masci-tools/issues/129
@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='spinpol_dos_area.png')
def test_plot_spinpol_dos_area_plot():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS
    from masci_tools.vis.fleur import plot_fleur_dos

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurDOS)

    gcf().clear()

    plot_fleur_dos(data, attributes, show=False, area_plot={'MT:1_up': True, 'MT:1_down': True}, area_alpha=0.3)

    return gcf()


def test_plot_spinpol_dos_area_plot_bokeh(check_bokeh_plot):
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS
    from masci_tools.vis.fleur import plot_fleur_dos

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurDOS)

    p = plot_fleur_dos(data,
                       attributes,
                       show=False,
                       area_plot={
                           'MT:1_up': True,
                           'MT:1_down': True
                       },
                       fill_alpha=0.3,
                       backend='bokeh')
    check_bokeh_plot(p)


#See issue https://github.com/JuDFTteam/masci-tools/issues/129
@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='spinpol_dos_omit_spin.png')
def test_plot_spinpol_dos_param_change_by_label_omit_spin():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS
    from masci_tools.vis.fleur import plot_fleur_dos

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurDOS)

    gcf().clear()

    plot_fleur_dos(data, attributes, show=False, color={'MT:1': 'red'}, linestyle={'MT:1': '--'}, area_alpha=0.3)

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='spinpol_dos_custom_plot_keys.png')
def test_plot_spinpol_dos_plot_keys_and_kwargs_custom_weight():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS
    from masci_tools.vis.fleur import plot_fleur_dos

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurDOS)

    gcf().clear()

    data['Custom_up'] = data['MT:1f_up'] * 0.5
    data['Custom_down'] = data['MT:1f_down'] * 0.5

    plot_fleur_dos(data,
                   attributes,
                   show=False,
                   color={'Custom': 'red'},
                   linestyle={'Custom': '--'},
                   area_alpha=0.3,
                   plot_keys=['Custom'])

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='bands_weighted_log_scale_colorbar.png')
def test_plot_bands_weighted_log_scale_colorbar_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands
    from matplotlib.colors import LogNorm

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    gcf().clear()

    plot_fleur_bands(data,
                     attributes,
                     show=False,
                     weight='MT:1d',
                     norm=LogNorm(),
                     colorbar=True,
                     limits={'color': (1e-2, 1)})

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='bands_weighted_log_scale_colorbar_spinpol.png')
def test_plot_bands_weighted_log_scale_colorbar_spinpol_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands
    from matplotlib.colors import LogNorm

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    gcf().clear()

    plot_fleur_bands(data,
                     attributes,
                     show=False,
                     weight='MT:1d',
                     norm=LogNorm(),
                     colorbar=True,
                     limits={'color': (1e-3, 1)})

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='bands_weighted_non_spinpol_custom_weight.png')
def test_plot_bands_weighted_non_spinpol_custom_weight_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands
    from matplotlib.colors import LogNorm

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    data['Custom'] = data['MT:1s_up'] * data['MT:1p_up']

    gcf().clear()

    plot_fleur_bands(data, attributes, show=False, weight='Custom')

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR, filename='bands_weighted_spinpol_custom_weight.png')
def test_plot_bands_weighted_spinpol_custom_weight_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands
    from matplotlib.colors import LogNorm

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    data['Custom'] =  (data['MT:1s_up']+data['MT:1s_down']) \
                    * (data['MT:1d_up']+data['MT:1d_down'])

    data['Custom2'] =  (data['MT:1s_up']+data['MT:1s_down']) \
                     * (data['MT:1d_up']+data['MT:1d_down'])

    gcf().clear()

    plot_fleur_bands(data, attributes, show=False, weight=['Custom', 'Custom2'])

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir=MPL_BASELINE_DIR,
                               filename='bands_weighted_spinpol_force_non_spinpol_custom_weight.png')
def test_plot_bands_weighted_spinpol_force_non_spinpol_custom_weight_mpl():
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    from masci_tools.vis.fleur import plot_fleur_bands
    from matplotlib.colors import LogNorm

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as h5reader:
        data, attributes = h5reader.read(recipe=FleurBands)

    data['Custom'] =  (data['MT:1s_up']+data['MT:1s_down']) \
                    * (data['MT:1d_up']+data['MT:1d_down'])

    gcf().clear()

    plot_fleur_bands(data, attributes, show=False, spinpol=False, weight='Custom')

    return gcf()
