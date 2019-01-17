from collections import Counter

import numpy as np

from studenproject18ws.hdf.output_types import DataBands


def get_dos(filepath_dos, data_bands: DataBands, mask_groups, mask_characters, select_groups, interstitial, all_characters):

    num_groups = data_bands.num_groups
    atoms_per_group = data_bands.atoms_per_group
    num_char = data_bands.num_char

    # read from file
    dos_data = np.genfromtxt(filepath_dos).T
    skip = num_char + 1
    E = dos_data[0]
    dos = np.zeros(len(dos_data[0]))

    # # Simulate user selection: all groups, all characters selected
    # def_groups = range(num_groups)  # 0 to N-1
    # mask_groups = data_bands._mask_groups(def_groups)  # True for all
    # num_char = data_bands.num_char
    # def_characters = range(num_char)  # 0 to M-1
    # mask_characters = data_bands._mask_characters(def_characters)  # True for all

    if select_groups:
        for (i, mask_group) in enumerate(mask_groups):
            if mask_group:
                if (all_characters):
                    dos += dos_data[skip + i] * atoms_per_group[i]
                else:
                    for (j, mask_character) in enumerate(mask_characters):
                        dos += dos_data[skip + i + num_groups * (j+1)] * atoms_per_group[i]

    if interstitial:
        dos += dos_data[2]

    return (E, dos)
