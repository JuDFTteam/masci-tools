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
    Plot the bandstructure previously extracted from a `banddos.hdf` via the
    :py:class:`~masci_tools.io.parsers.hdf5.reader.HDF5Reader`

    This routine expects datasets and attributes read in with the `FleurBands`
    recipe from :py:mod:`~masci_tools.io.parsers.hdf5.recipes` or something
    producing equivalent data

    :param dosdata: dataset dict produced by the `FleurBands` recipe
    :param attributes: attributes dict produced by the `FleurBands` recipe
    :param spinpol: bool, if True (default) use the plot for spin-polarized bands if the data is spin-polarized
    :param bokeh_plot: bool (default False), if True use the bokeh routines for plotting
    :param weight: str, name of the weight (without spin suffix `_up` or `_dn`) you want to emphasize

    All other Kwargs are passed on to the underlying plot routines
        - Matplotlib: :py:func:`~masci_tools.vis.plot_methods.plot_bands()`, :py:func:`~masci_tools.vis.plot_methods.plot_spinpol_bands()`
        - Bokeh: :py:func:`~masci_tools.vis.bokeh_plots.bokeh_bands()`, :py:func:`~masci_tools.vis.bokeh_plots.bokeh_spinpol_bands()`
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
        if isinstance(weight, list):
            if all(w in bandsdata for w in weight):
                if not bokeh_plot:
                    weight = [bandsdata[w] for w in weight]
            else:
                raise ValueError(f'List of weights provided but not all weights are present in bandsdata: {weight}')
        elif weight in bandsdata:
            if not bokeh_plot:
                weight = bandsdata[weight]
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
            fig = bokeh_spinpol_bands(bandsdata,
                                      weight=weight,
                                      special_kpoints=special_kpoints,
                                      legend_label=plot_label,
                                      **kwargs)
        else:
            fig = bokeh_bands(bandsdata, weight=weight, special_kpoints=special_kpoints, **kwargs)
    else:
        if bandsattributes['spins'] == 2:
            fig = plot_spinpol_bands(bandsdata['kpath'],
                                     bandsdata['eigenvalues_up'],
                                     bandsdata['eigenvalues_down'],
                                     size_data=weight,
                                     special_kpoints=special_kpoints,
                                     plot_label=plot_label,
                                     **kwargs)
        else:
            fig = plot_bands(bandsdata['kpath'],
                             bandsdata['eigenvalues_up'],
                             size_data=weight,
                             special_kpoints=special_kpoints,
                             **kwargs)

    return fig


def plot_fleur_dos(dosdata,
                   attributes,
                   spinpol=True,
                   bokeh_plot=False,
                   multiply_by_equiv_atoms=False,
                   plot_keys=None,
                   show_total=True,
                   show_interstitial=True,
                   show_sym=False,
                   show_atoms='all',
                   show_lresolved=None,
                   key_mask=None,
                   **kwargs):
    """
    Plot the density of states previously extracted from a `banddos.hdf` via the
    :py:class:`~masci_tools.io.parsers.hdf5.reader.HDF5Reader`

    This routine expects datasets and attributes read in with the `FleurDOS` (Or related DOS modes)
    recipe from :py:mod:`~masci_tools.io.parsers.hdf5.recipes` or something
    producing equivalent data

    :param dosdata: dataset dict produced by the `FleurDOS` recipe
    :param attributes: attributes dict produced by the `FleurDOS` recipe
    :param spinpol: bool, if True (default) use the plot for spin-polarized dos if the data is spin-polarized
    :param bokeh_plot: bool (default False), if True use the bokeh routines for plotting

    Arguments for selecting the DOS components to plot:
        :param plot_keys: optional str list of str, defines the labels you want to plot
        :param show_total: bool, if True (default) the total DOS is shown
        :param show_interstitial: bool, if True (default) the interstitial DOS is shown
        :param show_atoms: either 'all', None, or int or list of ints, defines, which total atom projections to show
        :param show_atoms: either 'all', None, or int or list of ints, defines, which total atom projections to show
        :param key_mask: list of bools of the same length as the number of datasets, alternative way
                         to specify, which entries to plot

    All other Kwargs are passed on to the underlying plot routines
        - Matplotlib: :py:func:`~masci_tools.vis.plot_methods.plot_dos()`, :py:func:`~masci_tools.vis.plot_methods.plot_spinpol_dos()`
        - Bokeh: :py:func:`~masci_tools.vis.bokeh_plots.bokeh_dos()`, :py:func:`~masci_tools.vis.bokeh_plots.bokeh_spinpol_dos()`
    """
    from masci_tools.vis.plot_methods import plot_dos, plot_spinpol_dos
    from masci_tools.vis.bokeh_plots import bokeh_dos, bokeh_spinpol_dos
    import pandas as pd
    import numpy as np
    from collections import Counter

    dosdata = pd.DataFrame(data=dosdata)

    if multiply_by_equiv_atoms:
        n_equiv = Counter(attributes['atoms_groups'])
        for natom in range(1, attributes['n_types'] + 1):
            for key in dosdata.keys():
                if f'MT:{natom}' in key:
                    dosdata[key] *= n_equiv[natom]

    spinpol = attributes['spins'] == 2 and spinpol and any('_down' in key for key in dosdata.keys())
    legend_labels, keys = _generate_dos_labels(dosdata, attributes, spinpol)

    if key_mask is None:
        key_mask = _select_from_Local(keys,
                                      plot_keys,
                                      spinpol,
                                      show_total=show_total,
                                      show_interstitial=show_interstitial,
                                      show_sym=show_sym,
                                      show_atoms=show_atoms,
                                      show_lresolved=show_lresolved)

    #Select the keys
    legend_labels, keys = np.array(legend_labels)[key_mask].tolist(), np.array(keys)[key_mask].tolist()

    if bokeh_plot:
        if spinpol:
            fig = bokeh_spinpol_dos(dosdata, ynames=keys, legend_label=legend_labels, **kwargs)
        else:
            fig = bokeh_dos(dosdata, ynames=keys, legend_label=legend_labels, **kwargs)
    else:
        if spinpol:
            #Remove second half of legend labels
            legend_labels[len(legend_labels) // 2:] = [None] * (len(legend_labels) // 2)

            dosdata_up = [dosdata[key].to_numpy() for key in keys if '_up' in key]
            dosdata_dn = [dosdata[key].to_numpy() for key in keys if '_down' in key]
            fig = plot_spinpol_dos(dosdata['energy_grid'], dosdata_up, dosdata_dn, plot_label=legend_labels, **kwargs)
        else:
            dosdata_up = [dosdata[key].to_numpy() for key in keys if '_up' in key]
            fig = plot_dos(dosdata['energy_grid'], dosdata_up, plot_label=legend_labels, **kwargs)

    return fig


def _dos_order(key):
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
            return (spin, len(general) + atom_type, str(orbital_order.index(tail)))
        else:
            return (spin, len(general) + atom_type, tail)

    return None


def _generate_dos_labels(dosdata, attributes, spinpol):

    labels = []
    plot_order = []
    only_spin_up = not spinpol and any('_down' in key for key in dosdata.keys())

    types_elements = []
    for itype in range(1, attributes['n_types'] + 1):
        ind = list(attributes['atoms_groups']).index(itype)
        types_elements.append(attributes['atoms_elements'][ind])

    for key in sorted(dosdata.keys(), key=_dos_order):
        if key == 'energy_grid':
            continue

        if only_spin_up and '_down' in key:
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

            if types_elements.count(atom_label) != 1:
                atom_occ = types_elements[:atom_type].count(atom_label)

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


def _select_from_Local(keys, plot_keys, spinpol, show_total, show_interstitial, show_sym, show_atoms, show_lresolved):

    #TODO: How do we do other dos modes

    if not isinstance(show_atoms, list) and show_atoms != 'all':
        if show_atoms is not None:
            show_atoms = [show_atoms]

    if not isinstance(show_lresolved, list) and show_lresolved != 'all':
        if show_lresolved is not None:
            show_lresolved = [show_lresolved]

    #initialize mask
    if spinpol:
        mask = [False] * (len(keys) // 2)
    else:
        mask = [False] * len(keys)

    mask[0] = show_total
    mask[1] = show_interstitial
    mask[2] = show_sym

    natoms = (len(mask) - 3) // 5

    if show_atoms is not None:
        for iatom in range(1, natoms + 1):
            mask[3 + (iatom - 1) * 5] = show_atoms == 'all' or iatom in show_atoms

    if show_lresolved is not None:
        for iatom in range(1, natoms + 1):
            if show_lresolved == 'all' or iatom in show_lresolved:
                mask[3 + (iatom - 1) * 5 + 1:3 + iatom * 5] = [True, True, True, True]

    if plot_keys is not None:
        if not isinstance(plot_keys, list):
            plot_keys = [plot_keys]

        for key in plot_keys:
            mask[keys.index(f'{key}_up')] = True

    if spinpol:
        mask.extend(mask)

    return mask
