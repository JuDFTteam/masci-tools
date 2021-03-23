# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools.   #
# For further information on the license, see the LICENSE.txt file.           #
# For further information please visit http://judft.de/.                      #
#                                                                             #
###############################################################################
"""
Plotting routine for fleur density of states with and without hdf
"""

def plot_fleur_bands(bandsdata, bandsattributes, spinpol=True, bokeh_plot=False, weight=None, **kwargs):
    """
    Plot the data previously extracted from a `banddos.hdf` file vie the HDF5Reader
    """
    from masci_tools.vis.plot_methods import plot_bands, plot_spinpol_bands
    from masci_tools.vis.bokeh_plots import bokeh_bands, bokeh_spinpol_bands
    import pandas as pd

    nbands = bandsattributes['nbands']

    bandsdata = pd.DataFrame(data=bandsdata)
    special_kpoints = []
    for k_index, label in zip(bandsattributes['special_kpoint_indices'], bandsattributes['special_kpoint_labels']):
        special_kpoints.append((label, bandsdata['kpath'][(k_index * nbands) + 1]))

    if weight is not None:
        if not bokeh_plot:
            if bandsattributes['spins'] == 2:
                weight = [bandsdata[f'{weight}_up'], bandsdata[f'{weight}_down']]
            else:
                weight = bandsdata[f'{weight}_up']
        else:
            if bandsattributes['spins'] == 2:
                weight = [f'{weight}_up', f'{weight}_down']
            else:
                weight = f'{weight}_up'

    plot_label = None
    if spinpol:
        plot_label = ['Spin-Up', 'Spin-Down']

    if bokeh_plot:
        if bandsattributes['spins'] == 2:
            fig = bokeh_spinpol_bands(bandsdata, **kwargs)
        else:
            fig = bokeh_bands(bandsdata, weight=weight, special_kpoints=special_kpoints, **kwargs)
    else:
        if bandsattributes['spins'] == 2:
            fig = plot_spinpol_bands(bandsdata['kpath'],
                                     bandsdata['eigenvalues_up'],
                                     bandsdata['eigenvalues_down'],
                                     weight,
                                     special_kpoints=special_kpoints,
                                     plot_label=plot_label,
                                     **kwargs)
        else:
            fig = plot_bands(bandsdata['kpath'],
                             bandsdata['eigenvalues_up'],
                             weight,
                             special_kpoints=special_kpoints,
                             **kwargs)

    return fig
