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

import io
import warnings

def fleur_plot_bands(bandsfile, bandsfile_dn=None, **kwargs):
    """
    Plot the bandstructure either from a `banddos.hdf` or text output
    """
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands

    if isinstance(bandsfile, io.IOBase):
        filename = bandsfile.name
    else:
        filename = bandsfile

    if filename.endswith('.hdf'):
        if bandsfile_dn is not None:
            warnings.warn('bandsfile_dn is ignored for hdf input')

        with HDF5Reader(bandsfile) as h5reader:
            bandsdata, bandsattributes = h5reader.read(recipe=FleurBands)

    else:
        raise NotImplementedError

    return plot_fleur_bandsdata(bandsdata, bandsattributes, **kwargs)



def plot_fleur_bandsdata(bandsdata, bandsattributes, spinpol=True, bokeh_plot=False, weight=None, **kwargs):
    """
    Plot the data extracted from a `banddos.hdf` file
    """
    from masci_tools.vis.plot_methods import plot_bands, plot_spinpol_bands
    from masci_tools.vis.bokeh_plots import bokeh_bands, bokeh_spinpol_bands
    import pandas as pd


    bandsdata = pd.DataFrame(data=bandsdata)
    special_kpoints_dict = {label: bandsdata['kpath'][k_index] for k_index, label in zip(bandsattributes['special_kpoint_indices'],bandsattributes['special_kpoint_labels'])}


    if weight is not None:
        if not bokeh_plot:
            if bandsattributes['spins'] == 2:
                weight = [bandsdata[f'{weight}_up'], bandsdata[f'{weight}_down']]
            else:
                weight = bandsdata[f'{weight}_up']
        else:
            if bandsattributes['spins'] == 2:
                weight = [f'{weight}_up',f'{weight}_down']
            else:
                weight = f'{weight}_up'

    plot_label = None
    if spinpol:
        plot_label = ['Spin-Up', 'Spin-Down']

    if bokeh_plot:
        if bandsattributes['spins'] == 2:
            fig = bokeh_spinpol_bands(bandsdata, **kwargs)
        else:
            fig = bokeh_bands(bandsdata, weight=weight, special_kpoints=special_kpoints_dict, **kwargs)
    else:
        if bandsattributes['spins'] == 2:
            fig = plot_spinpol_bands(bandsdata['kpath'], bandsdata['eigenvalues_up'], bandsdata['eigenvalues_down'], weight, special_kpoints=special_kpoints_dict, plot_label=plot_label, **kwargs)
        else:
            fig = plot_bands(bandsdata['kpath'], bandsdata['eigenvalues_up'], weight, special_kpoints=special_kpoints_dict, **kwargs)

    return fig