#!/usr/bin/env python
from builtins import range
from builtins import object
import pytest

# prevent issue with not having a display on travis-ci
# this needs to go *before* pyplot imports
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import gcf, title
#from masci_tools.io.kkr_read_shapefun_info import read_shapefun
#from masci_tools.vis.kkr_plot_shapefun import plot_shapefun
#from masci_tools.vis.kkr_plot_dos import dosplot
#from masci_tools.vis.kkr_plot_bandstruc_qdos import dispersionplot
#from masci_tools.vis.kkr_plot_FS_qdos import FSqdos2D

# TODO: test if interfaces stay the same...
# I do not write extensive testing, since plot_methods should be redesigned anyway....

class Test_plot_methods_imports(object):
    """
    Test plotting functions
    """
    
    #from masci_tools.vis.plot_methods import *
    from masci_tools.vis.plot_methods import set_plot_defaults
    from masci_tools.vis.plot_methods import single_scatterplot
    from masci_tools.vis.plot_methods import multiple_scatterplots
    from masci_tools.vis.plot_methods import multi_scatter_plot
    from masci_tools.vis.plot_methods import waterfall_plot
    from masci_tools.vis.plot_methods import multiplot_moved
    from masci_tools.vis.plot_methods import histogram
    from masci_tools.vis.plot_methods import default_histogram
    from masci_tools.vis.plot_methods import plot_convex_hull2d
    from masci_tools.vis.plot_methods import plot_residuen
    from masci_tools.vis.plot_methods import plot_convergence_results
    from masci_tools.vis.plot_methods import plot_convergence_results_m
    from masci_tools.vis.plot_methods import plot_lattice_constant
    from masci_tools.vis.plot_methods import plot_relaxation_results
    from masci_tools.vis.plot_methods import plot_dos
    from masci_tools.vis.plot_methods import plot_bands
    from masci_tools.vis.plot_methods import plot_one_element_corelv
    from masci_tools.vis.plot_methods import construct_corelevel_spectrum
    from masci_tools.vis.plot_methods import plot_corelevel_spectra
    from masci_tools.vis.plot_methods import plot_fleur_bands

    def test_set_defaults(self):
        from masci_tools.vis.plot_methods import linewidth_g  
        from masci_tools.vis.plot_methods import set_plot_defaults
        set_plot_defaults(linewidth=3.0)
        assert(linewidth_g==2.0) # if worked should be 3.0
