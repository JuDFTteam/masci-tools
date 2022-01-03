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
import pandas as pd
import warnings

__all__ = (
    'plot_fleur_bands',
    'plot_fleur_dos',
    'plot_fleur_bands_characterize',
    'sum_weights_over_atoms',
)


def sum_weights_over_atoms(data, attributes, atoms_to_sum, entry_name):
    """
    Create sums of atom components over specified atoms. They are entered with the same
    suffixes as in the original data, but with the given entry_name as prefix

    :param data: datasets dict produced by the HDF5Reader with a recipe for DOS or bandstructure
    :param attributes: attributes dict produced by the HDF5Reader with a recipe for DOS or bandstructure
    :param atoms_to_sum: list of ints for the atoms, which should be summed
    :param entry_name: str prefix to be entered for the summed entries

    :returns: dict with the summed entries
    """
    import re
    import numpy as np

    if attributes['group_name'] == 'Local':
        atom_prefix = 'MT:'
    elif attributes['group_name'] == 'jDOS':
        atom_prefix = 'jDOS:'
    elif attributes['group_name'] == 'Orbcomp':
        atom_prefix = 'ORB:'
    elif attributes['group_name'] == 'MCD':
        atom_prefix = 'At'
    else:
        raise ValueError(f"Unknown group: {attributes['group_name']}")

    split_keys = [re.split(f'{atom_prefix}+[1-9]', key) for key in data.keys() if atom_prefix in key]
    component_keys = {split[1] for split in split_keys if len(split) == 2}

    if len(component_keys) == 0:
        raise ValueError('No matching components found. Are you sure you provided the right group name?')

    for component in component_keys:
        for atom in atoms_to_sum:
            current_key = f'{atom_prefix}{atom}{component}'

            if f'{entry_name}{component}' not in data:
                data[f'{entry_name}{component}'] = np.zeros(data[current_key].shape)
            data[f'{entry_name}{component}'] += data[current_key]

    return data


def plot_fleur_bands_characterize(bandsdata,
                                  bandsattributes,
                                  weight_names,
                                  weight_colors,
                                  spinpol=True,
                                  only_spin=None,
                                  backend=None,
                                  **kwargs):
    """
    Plot the bandstructure previously extracted from a `banddos.hdf` via the
    :py:class:`~masci_tools.io.parsers.hdf5.reader.HDF5Reader` with points colored
    according to the maximum weight from a selection of weights. Can be used to show
    what character dominates each band

    This routine expects datasets and attributes read in with a `FleurBands`
    recipe from :py:mod:`~masci_tools.io.parsers.hdf5.recipes` or something
    producing equivalent data

    :param bandsdata: dataset dict produced by the `FleurBands` recipe
    :param attributes: attributes dict produced by the `FleurBands` recipe
    :param weight_names: list of str with the names of the weights that should be considered
                         in the characterization
    :param weight_color: list of colors associated with each weight. If spin-polarized bandstructures
                         should be shown with different colors the list should be twice as long as the weights
    :param spinpol: bool, if True (default) use the plot for spin-polarized bands if the data is spin-polarized
    :param only_spin: optional str, if given only the speicified spin components are plotted
    :param backend: specify which plotting library to use ('matplotlib' or 'bokeh')

    All other Kwargs are passed on to :py:func:`~masci_tools.vis.fleur.plot_fleur_bands()`
    """

    spinpol_data = bandsattributes['spins'] == 2 and any('_down' in key for key in bandsdata.keys())

    colors = {}
    if spinpol and spinpol_data and only_spin is None:
        if 2 * len(weight_names) != len(weight_colors):
            raise ValueError(
                f'Wrong length of colors/names Expected {len(weight_colors)} names got {2 *len(weight_names)}')

        for weight, color in zip(weight_names, weight_colors[:len(weight_names)]):
            colors[f'{weight}_up'] = color

        for weight, color in zip(weight_names, weight_colors[len(weight_names):]):
            colors[f'{weight}_down'] = color

    else:
        if len(weight_names) != len(weight_colors):
            raise ValueError(
                f'Wrong length of colors/names Expected {len(weight_colors)} names got {len(weight_names)}')

        for weight, color in zip(weight_names, weight_colors):
            colors[f'{weight}_up'] = color

        if spinpol_data:
            for weight, color in zip(weight_names, weight_colors):
                colors[f'{weight}_down'] = color

    bandsdata = pd.DataFrame(data=bandsdata)

    bandscharacter_up = bandsdata[[f'{name}_up' for name in weight_names]].idxmax(axis=1)
    bandsdata['max_weight_up'] = bandsdata[[f'{name}_up' for name in weight_names]].max(axis=1)
    if spinpol_data:
        bandscharacter_down = bandsdata[[f'{name}_down' for name in weight_names]].idxmax(axis=1)
        bandsdata['max_weight_down'] = bandsdata[[f'{name}_down' for name in weight_names]].max(axis=1)

    bandsdata['color_up'] = bandscharacter_up.replace(colors)
    if spinpol_data:
        bandsdata['color_down'] = bandscharacter_down.replace(colors)

    if only_spin is not None:
        if only_spin not in ('up', 'down'):
            raise ValueError(f'Invalid value for only spin {only_spin} (Valid are up or down)')
        color_data = f'color_{only_spin}'
    else:
        color_data = 'color_up'
        if spinpol_data:
            color_data = ['color_up', 'color_down']

    return plot_fleur_bands(bandsdata,
                            bandsattributes,
                            spinpol=spinpol,
                            only_spin=only_spin,
                            backend=backend,
                            weight='max_weight',
                            scale_color=False,
                            color_data=color_data,
                            **kwargs)


def plot_fleur_bands(bandsdata, bandsattributes, spinpol=True, only_spin=None, backend=None, weight=None, **kwargs):
    """
    Plot the bandstructure previously extracted from a `banddos.hdf` via the
    :py:class:`~masci_tools.io.parsers.hdf5.reader.HDF5Reader`

    This routine expects datasets and attributes read in with a `FleurBands`
    recipe from :py:mod:`~masci_tools.io.parsers.hdf5.recipes` or something
    producing equivalent data

    :param bandsdata: dataset dict produced by the `FleurBands` recipe
    :param attributes: attributes dict produced by the `FleurBands` recipe
    :param spinpol: bool, if True (default) use the plot for spin-polarized bands if the data is spin-polarized
    :param only_spin: optional str, if given only the speicified spin components are plotted
    :param backend: specify which plotting library to use ('matplotlib' or 'bokeh')
    :param weight: str, name of the weight (without spin suffix `_up` or `_dn`) you want to emphasize

    All other Kwargs are passed on to the underlying plot routines
        - Matplotlib: :py:func:`~masci_tools.vis.plot_methods.plot_bands()`, :py:func:`~masci_tools.vis.plot_methods.plot_spinpol_bands()`
        - Bokeh: :py:func:`~masci_tools.vis.bokeh_plots.bokeh_bands()`, :py:func:`~masci_tools.vis.bokeh_plots.bokeh_spinpol_bands()`
    """
    from .common import bands, spinpol_bands, PlotBackend

    if 'bokeh_plot' in kwargs:
        warnings.warn(
            'The argument bokeh_plot is deprecated. Use the argument backend to specify'
            'the plotting library to use', DeprecationWarning)
        backend = 'bokeh' if kwargs.pop('bokeh_plot') else 'matplotlib'

    nbands = bandsattributes['nbands']

    if not isinstance(bandsdata, pd.DataFrame):
        bandsdata = pd.DataFrame(data=bandsdata)

    special_kpoints = []
    for k_index, label in zip(bandsattributes['special_kpoint_indices'], bandsattributes['special_kpoint_labels']):
        special_kpoints.append((label, bandsdata['kpath'][(k_index * nbands) + 1]))

    band_index = pd.Series(data=[index % nbands for index in range(len(bandsdata['kpath']))], name='band_index')
    new_bandsdata = pd.concat([bandsdata, band_index], axis=1)
    bandsdata = new_bandsdata

    if only_spin is not None:
        if only_spin not in ('up', 'down'):
            raise ValueError(f'Invalid value for only spin {only_spin} (Valid are up or down)')

        if not any(f'_{only_spin}' in key for key in bandsdata.keys()) or \
           f'eigenvalues_{only_spin}' not in bandsdata.keys():
            raise ValueError(f'No data for spin {only_spin} available')

        bandsdata = bandsdata[[
            key for key in bandsdata.keys() if f'_{only_spin}' in key or key in ('kpath', 'band_index')
        ]]

        if only_spin == 'down':
            bandsdata = bandsdata.rename(columns={key: key.replace('_down', '_up') for key in bandsdata.columns})

    spinpol_data = bandsattributes['spins'] == 2 and any('_down' in key for key in bandsdata.keys())

    if weight is not None:
        if isinstance(weight, list):
            if len(weight) != 2:
                raise ValueError(f'Expected 2 weight names. Got: {len(weight)}')
            if not all(w in bandsdata for w in weight):
                raise ValueError(f'List of weights provided but not all weights are present in bandsdata: {weight}')
        elif weight in bandsdata:
            if spinpol_data:
                raise ValueError('For spin-polarized bandstructure two weights have to be given for spin-up and down')
        else:
            if spinpol_data:
                weight = [f'{weight}_up', f'{weight}_down']
            else:
                weight = f'{weight}_up'

    if spinpol_data and not spinpol:
        #Concatenate the _up and _down columns
        spin_up = bandsdata[[label for label in bandsdata.columns if label.endswith('_up')]]
        spin_dn = bandsdata[[label for label in bandsdata.columns if label.endswith('_down')]]
        kpath = bandsdata['kpath']
        band_index = bandsdata['band_index']

        spin_dn = spin_dn.rename(columns={key: key.replace('_down', '_up') for key in spin_dn.columns})

        #Double kpath and extend spin up data
        kpath = kpath.append(kpath, ignore_index=True)
        band_index = band_index.append(band_index + nbands + 1, ignore_index=True)
        complete_spin = pd.concat([spin_up, spin_dn], ignore_index=True)

        #And now add the new kpath and overwrite bandsdata
        new_bandsdata = pd.concat([complete_spin, kpath, band_index], axis=1)
        bandsdata = new_bandsdata

        if isinstance(weight, list):
            weight = weight[0]

        if 'color_data' in kwargs:
            color_data = kwargs.pop('color_data')
            if isinstance(color_data[0], str):
                color_data = color_data[0]
            kwargs['color_data'] = color_data

    spinpol = spinpol_data and spinpol

    backend = PlotBackend.from_str(backend)

    if spinpol:
        plot_label = ['Spin-Up', 'Spin-Down']
        if backend == PlotBackend.bokeh:
            if 'legend_label' not in kwargs:
                kwargs['legend_label'] = plot_label
        else:
            if 'plot_label' not in kwargs:
                kwargs['plot_label'] = plot_label

    if spinpol:
        fig = spinpol_bands('kpath',
                            'eigenvalues_up',
                            'eigenvalues_down',
                            data=bandsdata,
                            size_data=weight,
                            special_kpoints=special_kpoints,
                            band_index='band_index',
                            backend=backend,
                            **kwargs)
    else:
        fig = bands('kpath',
                    'eigenvalues_up',
                    data=bandsdata,
                    size_data=weight,
                    special_kpoints=special_kpoints,
                    band_index='band_index',
                    backend=backend,
                    **kwargs)

    return fig


def plot_fleur_dos(dosdata,
                   attributes,
                   spinpol=True,
                   multiply_by_equiv_atoms=True,
                   plot_keys=None,
                   show_total=True,
                   show_interstitial=True,
                   show_sym=False,
                   show_atoms='all',
                   show_lresolved=None,
                   key_mask=None,
                   backend=None,
                   **kwargs):
    """
    Plot the density of states previously extracted from a `banddos.hdf` via the
    :py:class:`~masci_tools.io.parsers.hdf5.reader.HDF5Reader`

    This routine expects datasets and attributes read in with the `FleurDOS` (Or related DOS modes)
    recipe from :py:mod:`~masci_tools.io.parsers.hdf5.recipes` or something
    producing equivalent data

    The limits for the axes can be specified either with ``x`` and ``y`` or
    ``energy`` and ``dos``. Mixing the two options is not possible

    :param dosdata: dataset dict produced by the `FleurDOS` recipe
    :param attributes: attributes dict produced by the `FleurDOS` recipe
    :param spinpol: bool, if True (default) use the plot for spin-polarized dos if the data is spin-polarized
    :param backend: specify which plotting library to use ('matplotlib' or 'bokeh')

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
    from .common import dos, spinpol_dos, PlotBackend
    import numpy as np
    from collections import Counter

    if 'bokeh_plot' in kwargs:
        warnings.warn(
            'The argument bokeh_plot is deprecated. Use the argument backend to specify'
            'the plotting library to use', DeprecationWarning)
        backend = 'bokeh' if kwargs.pop('bokeh_plot') else 'matplotlib'

    dosdata = pd.DataFrame(data=dosdata)

    if multiply_by_equiv_atoms:
        n_equiv = Counter(attributes['atoms_groups'])
        for natom in range(1, attributes['n_types'] + 1):
            for key in dosdata.keys():
                if f'MT:{natom}' in key:
                    after = key[len(f'MT:{natom}'):]
                    if after == '' or not after[0].isdecimal():
                        dosdata[key] *= n_equiv[natom]

    spinpol = attributes['spins'] == 2 and spinpol and any('_down' in key for key in dosdata.keys())
    legend_labels, keys = _generate_dos_labels(dosdata, attributes, spinpol)

    if key_mask is None:
        key_mask = _select_entries(keys,
                                   attributes['group_name'],
                                   plot_keys,
                                   spinpol,
                                   show_total=show_total,
                                   show_interstitial=show_interstitial,
                                   show_sym=show_sym,
                                   show_atoms=show_atoms,
                                   show_lresolved=show_lresolved)

    #Select the keys
    legend_labels, keys = np.array(legend_labels)[key_mask].tolist(), np.array(keys)[key_mask].tolist()

    kwargs = _process_dos_kwargs(keys, backend=backend, **kwargs)

    if spinpol:
        dosdata_up = [key for key in keys if '_up' in key]
        dosdata_dn = [key for key in keys if '_down' in key]

    backend = PlotBackend.from_str(backend)

    if backend == PlotBackend.bokeh:
        if 'legend_label' not in kwargs:
            kwargs['legend_label'] = legend_labels
    else:
        if 'plot_label' not in kwargs:
            kwargs['plot_label'] = legend_labels

    if spinpol:
        fig = spinpol_dos('energy_grid', dosdata_up, dosdata_dn, data=dosdata, backend=backend, **kwargs)
    else:
        fig = dos('energy_grid', keys, data=dosdata, backend=backend, **kwargs)

    return fig


def _process_dos_kwargs(ordered_keys, backend=None, **kwargs):
    """
    Convert any kwarg in dict form with str keys to the correct dict with integer index
    for the plotting functions.

    :param ordered_keys: ordered (!!!) list of the labels in the dos plot

    :returns: kwargs with the dicts converted to integer indexed dicts
    """
    from .common import get_plotter

    params = get_plotter(backend)

    for key, value in kwargs.items():
        if params.is_general(key):
            continue
        if isinstance(value, dict):
            new_dict = value.copy()
            for plot_label in value:
                if not isinstance(plot_label, int):
                    if plot_label in ordered_keys:
                        new_dict[ordered_keys.index(plot_label)] = new_dict.pop(plot_label)
                    else:
                        raise ValueError(f'The label {plot_label} is not a valid label for the current plot')
            kwargs[key] = new_dict
    return kwargs


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
    if ':' in key:
        _, after = key.split(':', maxsplit=1)
        tail = after.lstrip('0123456789')
        index = int(after[:-len(tail)]) if len(tail) > 0 else int(after)

        tail = tail.lstrip(',')
        if tail.startswith('ind:'):
            tail = int(tail[4:])
        if tail in orbital_order:
            return (spin, len(general) + index, orbital_order.index(tail), '')
        if isinstance(tail, int):
            return (spin, len(general) + index, tail, '')
        return (spin, len(general) + index, float('inf'), tail)

    return None


def _generate_dos_labels(dosdata, attributes, spinpol):
    """
    Generate nice labels for the weights in the dictionary. Only
    processes standard names

    :param dosdata: dict with the datasets from the HDF5Reader
    :param attributes: dict with the attributes from the HDF5Reader
    :param spinpol: bool, whether to include spin direction in the labels

    :returns: tuple of two lists, the first with the labels the second with the
              corresponding keys in the data dict
    """
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

            before, after = key.split(':', maxsplit=1)
            tail = after.lstrip('0123456789')
            index = int(after[:-len(tail)]) if len(tail) > 0 else int(after)

            if before == 'MT':
                label = types_elements[index - 1]

                if types_elements.count(label) != 1:
                    atom_occ = types_elements[:index].count(label)

                    label = f'{label}-{atom_occ}'
            elif before in ('jDOS', 'ORB'):
                label = attributes['atoms_elements'][index - 1]
                atom_occ = list(attributes['atoms_elements'][:index]).count(label)
                label = f'{before} {label}-{atom_occ}'

            tail = tail.lstrip(',')
            if '_up' in tail:
                tail = tail.split('_up')[0]
                if spinpol:
                    tail = f'{tail} up/down'
            else:
                tail = tail.split('_down')[0]
                if spinpol:
                    tail = f'{tail} up/down'
            label += ' ' + tail

            labels.append(label)

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


def _select_entries(keys, group_name, plot_keys, spinpol, show_total, show_interstitial, show_sym, show_atoms,
                    show_lresolved):

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

    if group_name == 'Local':
        mask[0] = show_total
        mask[1] = show_interstitial
        mask[2] = show_sym

        general_keys = 3
        entries_per_atom = 5
    elif group_name == 'Orbcomp':
        general_keys = 0
        entries_per_atom = 24
    else:
        general_keys = 0
        entries_per_atom = 5
        warnings.warn(f'Selection for group {group_name} not yet implemented. Plotting all DOS components')

    natoms = (len(mask) - general_keys) // entries_per_atom

    if show_atoms is not None:
        for iatom in range(1, natoms + 1):
            mask[general_keys + (iatom - 1) * entries_per_atom] = show_atoms == 'all' or iatom in show_atoms

    if show_lresolved is not None:
        for iatom in range(1, natoms + 1):
            if show_lresolved == 'all' or iatom in show_lresolved:
                mask[general_keys + (iatom - 1) * entries_per_atom + 1:general_keys +
                     iatom * entries_per_atom] = [True] * (entries_per_atom - 1)

    if plot_keys is not None:
        if not isinstance(plot_keys, list):
            plot_keys = [plot_keys]

        for key in plot_keys:
            mask[keys.index(f'{key}_up')] = True

    if spinpol:
        mask.extend(mask)

    return mask
