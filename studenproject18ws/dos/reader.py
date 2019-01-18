from collections import Counter

import numpy as np

from studenproject18ws.hdf.output_types import DataBands


def get_dos(filepath_dos, data_bands: DataBands, mask_groups, mask_characters,
            select_groups, interstitial, all_characters):
    """

    Notes
    -----
    A DOS file has (num_atom_groups * 5 + 5) = num_columns columns.
    Right now, the indexing is off by one. Selecting the last atom group and character
    just returns zero, because the colum num_colunns would be accessed (out-of-bounds).
    This is a bad hack and should be corrected.

    :param filepath_dos:
    :param data_bands:
    :param mask_groups: list of bool
    :param mask_characters: list of bool
    :param select_groups: bool
    :param interstitial: bool
    :return: tuple of (E, dos, dos_lim). dos_lim tuple of total dos (min,max).
    """

    num_groups = data_bands.num_groups
    atoms_per_group = data_bands.atoms_per_group
    num_char = data_bands.num_char

    # read from file
    dos_data = np.genfromtxt(filepath_dos).T
    num_columns = dos_data.shape[0]

    dos_tot = dos_data[1]
    dos_lim = (np.min(dos_tot), np.max(dos_tot))

    skip = 5
    E = dos_data[0]

    dos = np.zeros(len(dos_data[0]))

    col_indices = []

    def col(col_index):
        col_indices.append(col_index)
        if (col_index == num_columns):
            # this is a bad hack!
            # It occurs if the last atom group and last character (f of spdf)
            # is selected. Obviously the indexing is off. But the DOS looks
            # wrong if the offset (skip + (i+1)) is one index lower.
            return np.zeros_like(E)
        else:
            return dos_data[col_index]

    if select_groups:
        for (i, mask_group) in enumerate(mask_groups):
            if mask_group:
                if (all_characters):
                    dos += col(skip + i) * atoms_per_group[i]
                else:
                    for (j, mask_character) in enumerate(mask_characters):
                        if mask_character:
                            # print(f"skip + (i+1) + (num_groups * (j+1)) = {skip} + ({i+1}) + ({num_groups} * ({j+1}))")
                            dos += col(skip + (i + 1) + (num_groups * (j + 1))) * atoms_per_group[i]

    if interstitial:
        dos += col(2)

    # for testing:
    # print(
    #     f"get_dos: for selection groups {mask_groups}, "
    #     f"characters {mask_characters}, "
    #     f"num_groups {num_groups}, "
    #     f"atoms_per_group {atoms_per_group}, "
    #     f"accessed dos columns: {col_indices}")

    return (E, dos, dos_lim)
