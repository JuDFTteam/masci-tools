#!/usr/bin/env python
"""
Tests for kkr-specific plotting functions
"""
import pytest

# prevent issue with not having a display on travis-ci
# this needs to go *before* pyplot imports
import matplotlib

matplotlib.use('Agg')
from matplotlib.pyplot import gcf, title
from masci_tools.io.kkr_read_shapefun_info import read_shapefun
from masci_tools.vis.kkr_plot_shapefun import plot_shapefun
from masci_tools.vis.kkr_plot_dos import dosplot
from masci_tools.vis.kkr_plot_bandstruc_qdos import dispersionplot
from masci_tools.vis.kkr_plot_FS_qdos import FSqdos2D
from pathlib import Path
import os

DIR = Path(__file__).parent.resolve()


@pytest.mark.mpl_image_compare(baseline_dir=DIR / Path('files/voronoi/'), filename='test.png')
def test_plot_shapefun():
    # clear previous figure, if still there
    gcf().clear()
    pos, out = read_shapefun(os.fspath(DIR / Path('files/voronoi/')))
    plot_shapefun(pos, out, 'all')
    # need to return the figure in order for mpl checks to work
    return gcf()


@pytest.mark.skipif(os.name == 'nt', reason='Broken on Windows')
@pytest.mark.mpl_image_compare(baseline_dir=DIR / Path('files/kkr/kkr_run_dos_output/'),
                               filename='test.png',
                               tolerance=5)
def test_plot_dos():
    gcf().clear()
    dosplot(os.fspath(DIR / Path('files/kkr/kkr_run_dos_output/')))
    return gcf()


@pytest.mark.skipif(os.name == 'nt', reason='Broken on Windows')
@pytest.mark.mpl_image_compare(baseline_dir=DIR / Path('files/kkr/kkr_run_dos_output/'), filename='test2.png')
def test_plot_dos2():
    gcf().clear()
    dosplot(os.fspath(DIR / Path('files/kkr/kkr_run_dos_output/')),
            units='eV_rel',
            nofig=True,
            allatoms=True,
            totonly=False)
    return gcf()


@pytest.mark.skipif(os.name == 'nt', reason='Broken on Windows')
@pytest.mark.mpl_image_compare(baseline_dir=DIR / Path('files/kkr/kkr_run_dos_output/'), filename='test3.png')
def test_plot_dos3():
    gcf().clear()
    dosplot(os.fspath(DIR / Path('files/kkr/kkr_run_dos_output/')),
            units='eV_rel',
            nofig=True,
            allatoms=True,
            filled=True,
            normalized=True,
            xyswitch=True,
            color='r')
    return gcf()


@pytest.mark.skipif(os.name == 'nt', reason='Broken on Windows')
@pytest.mark.mpl_image_compare(baseline_dir=DIR / Path('files/kkr/kkr_run_dos_output/'), filename='test4.png')
def test_plot_dos4():
    gcf().clear()
    dosplot(os.fspath(DIR / Path('files/kkr/kkr_run_dos_output/')),
            units='eV_rel',
            nofig=True,
            allatoms=True,
            lm=list(range(1, 5)))
    return gcf()


@pytest.mark.skipif(os.name == 'nt', reason='Broken on Windows')
@pytest.mark.mpl_image_compare(baseline_dir=DIR / Path('files/kkr/kkr_run_qdos/'), filename='test.png')
def test_plot_qdos():
    gcf().clear()
    dispersionplot(os.fspath(DIR / Path('files/kkr/kkr_run_qdos')), reload_data=True)
    title('')
    return gcf()


@pytest.mark.skipif(os.name == 'nt', reason='Broken on Windows')
@pytest.mark.mpl_image_compare(baseline_dir=DIR / Path('files/kkr/kkr_run_qdos/'), filename='test2.png')
def test_plot_qdos2():
    gcf().clear()
    dispersionplot(os.fspath(DIR / Path('files/kkr/kkr_run_qdos')),
                   reload_data=True,
                   ratios=False,
                   units='eV_rel',
                   clrbar=False,
                   shading='nearest')
    title('')
    return gcf()


@pytest.mark.skipif(os.name == 'nt', reason='Broken on Windows')
@pytest.mark.mpl_image_compare(baseline_dir=DIR / Path('files/kkr/kkr_run_qdos_FS/'), filename='test.png')
def test_plot_qdos_FS():
    gcf().clear()
    FSqdos2D(os.fspath(DIR / Path('files/kkr/kkr_run_qdos_FS/')), reload_data=True)
    return gcf()
