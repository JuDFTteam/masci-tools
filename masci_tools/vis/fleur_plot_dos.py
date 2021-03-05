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
                   interstitial=True,
                   atoms='all',
                   atoms_lresolved=None,
                   atoms_area=False,
                   **kwargs):
    """
    Plot the density of states either from a `banddos.hdf` or text output
    """
    from masci_tools.io.io_hdf5 import read_hdf
    from masci_tools.vis.plot_methods import plot_dos, plot_spinpol_dos
    from masci_tools.util.constants import HTR_TO_EV

    dos_data_dn = None

    if path_to_dosfile.endswith('.hdf'):
        if path_to_dosfile_dn is not None:
            warnings.warn('path_to_dosfile_dn is ignored for hdf files')
        data, attrs = read_hdf(path_to_dosfile)

        natoms = attrs['atoms']['nTypes']

        dos_data = data[hdf_group].get('DOS')

        if dos_data is None:
            raise ValueError(f"DOS entry is missing in {hdf_group} for file '{path_to_dosfile}'."
                             ' Are you sure this is a DOS calculation?')

        energy_grid = dos_data.pop('energyGrid') * HTR_TO_EV

        #Compute atom sums
        for atom in range(1, natoms + 1):
            dos_data[f'MT:{atom}'] = sum(dos_data[f'MT:{atom}{orbital}'] for orbital in 'spdf')

        if dos_data[list(dos_data.keys())[0]].shape[0] == 1:
            spin_pol = False
            dos_data_up = {key: data[0, ...] / HTR_TO_EV for key, data in dos_data.items()}
        else:
            spin_pol = True
            dos_data_up = {key: data[0, ...] / HTR_TO_EV for key, data in dos_data.items()}
            dos_data_dn = {key: data[1, ...] / HTR_TO_EV for key, data in dos_data.items()}

    else:
        #TODO: txt input
        raise NotImplementedError

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

    if atoms_lresolved == 'all':
        atoms_lresolved = range(1, natoms + 1)
    elif atoms_lresolved is not None:
        if not isinstance(atoms_lresolved, list):
            atoms_lresolved = [atoms_lresolved]

    if atoms_lresolved is not None:
        keys_to_plot.update(f'MT:{atom}{orbital}' for atom in atoms_lresolved for orbital in 'spdf')

    keys_to_plot = sorted(keys_to_plot)
    dos_data_up = [dos_data_up[key] for key in keys_to_plot]
    if dos_data_dn is not None:
        dos_data_dn = [dos_data_dn[key] for key in keys_to_plot]

    if spin_pol:
        plot_spinpol_dos(dos_data_up, dos_data_dn, energy_grid, plot_label=keys_to_plot, **kwargs)
    else:
        plot_dos(dos_data_up, energy_grid, plot_label=keys_to_plot, **kwargs)
