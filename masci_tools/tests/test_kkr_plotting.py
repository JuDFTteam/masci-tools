#!/usr/bin/env python
from builtins import range
from builtins import object
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

class Test_kkr_plotting(object):
    """
    Test for KKR plotting functions
    """

    @pytest.mark.mpl_image_compare(baseline_dir='files/voronoi/', filename='test.png')
    def test_plot_shapefun(self):
        # clear previous figure, if still there
        gcf().clear()
        pos, out = read_shapefun('files/voronoi/')
        plot_shapefun(pos, out, 'all')
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/kkr/kkr_run_dos_output/', filename='test.png')
    def test_plot_dos(self):
        gcf().clear()
        dosplot('files/kkr/kkr_run_dos_output/')
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/kkr/kkr_run_dos_output/', filename='test2.png')
    def test_plot_dos2(self):
        gcf().clear()
        dosplot('files/kkr/kkr_run_dos_output/', units='eV_rel', nofig=True, allatoms=True, totonly=False)
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/kkr/kkr_run_dos_output/', filename='test3.png')
    def test_plot_dos3(self):
        gcf().clear()
        dosplot('files/kkr/kkr_run_dos_output/', units='eV_rel', nofig=True, allatoms=True, filled=True, normalized=True, xyswitch=True, color='r')
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/kkr/kkr_run_dos_output/', filename='test4.png')
    def test_plot_dos4(self):
        gcf().clear()
        dosplot('files/kkr/kkr_run_dos_output/', units='eV_rel', nofig=True, allatoms=True, lm=list(range(1,5)))
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/kkr/kkr_run_qdos/', filename='test.png')
    def test_plot_qdos(self):
        gcf().clear()
        dispersionplot('files/kkr/kkr_run_qdos', reload_data=True); title('')
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/kkr/kkr_run_qdos/', filename='test2.png')
    def test_plot_qdos2(self):
        gcf().clear()
        dispersionplot('files/kkr/kkr_run_qdos', reload_data=True, ratios=False, units='eV_rel', clrbar=False); title('')
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/kkr/kkr_run_qdos_FS/', filename='test.png')
    def test_plot_qdos_FS(self):
        gcf().clear()
        FSqdos2D('files/kkr/kkr_run_qdos_FS/', reload_data=True)
        return gcf()

