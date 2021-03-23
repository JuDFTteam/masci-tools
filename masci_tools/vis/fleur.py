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
Plotting routine for fleur density of states and bandstructures
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


def plot_fleur_dos(dosdata, attributes, spinpol=True, bokeh_plot=False, **kwargs):
    """
    Plot the density of states previously extracted from a `banddos.hdf` via the HDF5reader
    """
    from masci_tools.vis.plot_methods import plot_dos, plot_spinpol_dos
    from masci_tools.vis.bokeh_plots import bokeh_dos, bokeh_spinpol_dos
    import pandas as pd

    dosdata = pd.DataFrame(data=dosdata)

    spinpol = attributes['spins'] == 2 and spinpol
    legend_labels, keys = generate_dos_labels(dosdata, attributes, spinpol)

    if bokeh_plot:
        if spinpol:
            fig = bokeh_spinpol_dos(dosdata, ynames=keys, legend_label=legend_labels, **kwargs)
        else:
            fig = bokeh_dos(dosdata, ynames=keys, legend_label=legend_labels, **kwargs)
    else:
        if spinpol:
            dosdata_up = [dosdata[key].to_numpy() for key in keys if '_up' in key]
            dosdata_dn = [dosdata[key].to_numpy() for key in keys if '_down' in key]
            fig = plot_spinpol_dos(dosdata_up, dosdata_dn, dosdata['energy_grid'], plot_label=legend_labels, **kwargs)
        else:
            dosdata_up = [dosdata[key].to_numpy() for key in keys if '_up' in key]
            fig = plot_dos(dosdata_up, dosdata['energy_grid'], plot_label=legend_labels, **kwargs)

    return fig


def dos_order(key):
    """
    Key function for sorting DOS entries in predictable order:
        1. Energy Grid
        2. General keys (Total, interstitial, ...)
        3. Atom contribution (total, orbital resolved)
    """

    if key == 'energy_grid':
        return (-1,)

    if '_up' in key:
        key = key.split('_up')[0]
        spin = 0
    else:
        key = key.split('_down')[0]
        spin = 1

    general = ('Total', 'INT', 'Sym')
    orbital_order = ('', 's', 'p', 'd', 'f')

    if key in general:
        return (spin, general.index(key))
    elif ':' in key:
        before, after = key.split(':')

        tail = after.lstrip('0123456789')
        atom_type = int(after[:-len(tail)]) if len(tail) > 0 else int(after[0])

        if tail in orbital_order:
            return (spin, len(general) + atom_type, orbital_order.index(tail))
        else:
            return (spin, len(general) + atom_type, orbital_order)

    return None


def generate_dos_labels(dosdata, attributes, spinpol):

    labels = []
    plot_order = []

    atom_elements = list(attributes['atoms_elements'])

    for key in sorted(dosdata.keys(), key=dos_order):
        if key == 'energy_grid':
            continue

        plot_order.append(key)
        if 'INT' in key:
            key = 'Interstitial'
            if spinpol:
                key = 'Interstitial up/down'
            labels.append(key)
        elif ':' in key:  #Atom specific DOS

            before, after = key.split(':')

            tail = after.lstrip('0123456789')
            atom_type = int(after[:-len(tail)])

            atom_label = attributes['atoms_elements'][atom_type - 1]

            if atom_elements.count(atom_label) != 1:
                atom_occ = atom_elements[:atom_type].count(atom_label)

                atom_label = f'{atom_label}-{atom_occ}'

            if '_up' in tail:
                tail = tail.split('_up')[0]
                if spinpol:
                    tail = f'{tail} up/down'
            else:
                tail = tail.split('_down')[0]
                if spinpol:
                    tail = f'{tail} up/down'

            labels.append(f'{atom_label} {tail}')

        else:
            if '_up' in key:
                key = key.split('_up')[0]
                if spinpol:
                    key = f'{key} up/down'
            elif '_down' in key:
                key = key.split('_down')[0]
                if spinpol:
                    key = f'{key} up/down'
            labels.append(key)

    return labels, plot_order


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
