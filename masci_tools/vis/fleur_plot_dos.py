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
Plotting routines for fleur density of states with and without hdf
"""
import warnings


def fleur_plot_dos(path_to_dosfile,
                   path_to_dosfile_dn=None,
                   hdf_group='Local',
                   spinpol=True,
                   bokeh_plot=False,
                   **kwargs):
    """
    Plot the density of states either from a `banddos.hdf` or text output
    """
    from masci_tools.io.io_hdf5 import read_hdf
    from masci_tools.vis.plot_methods import plot_dos, plot_spinpol_dos
    from masci_tools.vis.bokeh_plots import bokeh_dos, bokeh_spinpol_dos
    from masci_tools.util.constants import HTR_TO_EV
    import pandas as pd

    dos_data_dn = None

    if path_to_dosfile.endswith('.hdf'):
        if path_to_dosfile_dn is not None:
            warnings.warn('path_to_dosfile_dn is ignored for hdf files')
        data, attrs = read_hdf(path_to_dosfile)

        natoms = attrs['atoms']['nTypes']
        spinpol = attrs['general']['spins'] == 2 and spinpol

        dos_data = data[hdf_group].get('DOS')

        if dos_data is None:
            raise ValueError(f"DOS entry is missing in {hdf_group} for file '{path_to_dosfile}'."
                             ' Are you sure this is a DOS calculation?')

        energy_grid = dos_data.pop('energyGrid') * HTR_TO_EV

        #Compute atom sums
        if hdf_group == 'Local':
            for atom in range(1, natoms + 1):
                dos_data[f'MT:{atom}'] = sum(value for key, value in dos_data.items() if f'MT:{atom}' in key)
        elif hdf_group == 'jDOS':
            for atom in range(1, natoms + 1):
                dos_data[f'MT:{atom}'] = sum(value for key, value in dos_data.items() if f'jDOS:{atom}' in key)
        elif hdf_group == 'Orbcomp':
            for atom in range(1, natoms + 1):
                dos_data[f'MT:{atom}'] = sum(value for key, value in dos_data.items() if f'ORB:{atom}' in key)

        if not spinpol:
            dos_data_up = {key: data[0, ...] / HTR_TO_EV for key, data in dos_data.items()}
        else:
            dos_data_up = {key: data[0, ...] / HTR_TO_EV for key, data in dos_data.items()}
            dos_data_dn = {key: data[1, ...] / HTR_TO_EV for key, data in dos_data.items()}

    else:
        #TODO: txt input
        raise NotImplementedError

    if hdf_group == 'Local':
        interstitial = kwargs.pop('interstitial', True)
        atoms = kwargs.pop('atoms', 'all')
        l_resolved = kwargs.pop('l_resolved', None)
        dos_data_up, dos_data_dn, keys_to_plot = select_from_Local(dos_data_up, dos_data_dn, natoms, interstitial,
                                                                   atoms, l_resolved)
    else:
        keys_to_plot = list(dos_data_up.keys())
        dos_data_up = list(dos_data_up.values())
        if dos_data_dn is not None:
            dos_data_dn = list(dos_data_dn.values())

    if bokeh_plot:
        if spinpol:
            dos_data = {key: data for key, data in zip(keys_to_plot, dos_data_up)}
            dos_data['energy'] = energy_grid
            dos_data_dn = {key: data for key, data in zip(keys_to_plot, dos_data_dn)}
            dos_data_dn['energy'] = energy_grid
            data = pd.DataFrame(data=dos_data)
            data_dn = pd.DataFrame(data=dos_data_dn)
            fig = bokeh_spinpol_dos(data, data_dn, **kwargs)
        else:
            dos_data = {key: data for key, data in zip(keys_to_plot, dos_data_up)}
            dos_data['energy'] = energy_grid
            data = pd.DataFrame(data=dos_data)
            fig = bokeh_dos(data, **kwargs)
    else:
        if spinpol:
            fig = plot_spinpol_dos(dos_data_up, dos_data_dn, energy_grid, plot_label=keys_to_plot, **kwargs)
        else:
            fig = plot_dos(dos_data_up, energy_grid, plot_label=keys_to_plot, **kwargs)

    return fig


def select_from_Local(dos_data_up, dos_data_dn, natoms, interstitial, atoms, l_resolved):

    keys_to_plot = {'Total'}

    if interstitial:
        keys_to_plot.add('INT')

    if atoms == 'all':
        atoms = range(1, natoms + 1)
    elif atoms is not None:
        if not isinstance(atoms, list):
            atoms = [atoms]

    if atoms is not None:
        keys_to_plot.update(f'MT:{atom}' for atom in atoms)

    if l_resolved == 'all':
        l_resolved = range(1, natoms + 1)
    elif l_resolved is not None:
        if not isinstance(l_resolved, list):
            l_resolved = [l_resolved]

    if l_resolved is not None:
        keys_to_plot.update(f'MT:{atom}{orbital}' for atom in l_resolved for orbital in 'spdf')

    keys_to_plot = sorted(keys_to_plot)
    dos_data_up = [dos_data_up[key] for key in keys_to_plot]
    if dos_data_dn is not None:
        dos_data_dn = [dos_data_dn[key] for key in keys_to_plot]

    return dos_data_up, dos_data_dn, keys_to_plot
