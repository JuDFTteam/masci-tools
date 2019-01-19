from collections import Counter

import numpy as np

from studenproject18ws.hdf.output_types import DataBands


def get_dos(filepath_dos, data_bands: DataBands, mask_groups, mask_characters,
            select_groups, interstitial, all_characters):
    """

    Notes
    -----
    Assumed DOS file format:

    A DOS file has (num_atom_groups * 5 + 5) = num_columns columns.

    The DOS file columns are separated into three sections:
    - section1: 5 columns: E, dos_tot, interstitial, vac1, vac2;
    - section2: num_groups columns: dos for all characters per atoms group;
    - section3: 4 * num_groups columns: (dos per atoms group) per character.
      - so section3 has 4 subsections each of length num_groups.

    Currently, a bad_hck_offset is used. Unsure if correct. See code for info.

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
    num_chars = data_bands.num_char

    # read from file
    dos_data = np.genfromtxt(filepath_dos).T
    num_cols = dos_data.shape[0]
    num_rows = dos_data.shape[1]
    # the DOS file format has three sections:
    # - 5 columns: E, dos_tot, interstitial, vac1, vac2;
    # - num_groups columns: dos for all characters per atoms group,
    # - 4 * num_groups columns: (dos per atoms group) per character.
    #   - so section3 has 4 subsections each of length num_groups.
    index = {
        'section1': {'E': 0, "dos_tot": 1, 'interstitial': 2, 'vac1': 3, 'vac2': 4},
        'section2': [g for g in range(5, 5 + num_groups)],
        'section3': [[(5 + num_groups + g)
                      for g in range(c * num_groups, (c + 1) * num_groups)]
                     for c in range(num_chars)]
    }

    # define method for column access
    col_indices_accessed = []
    def col(col_index):
        """
        :param col_index:
        :return: DOS file column
        """
        col_indices_accessed.append(col_index)
        if (col_index >= num_cols):
            # this happens if
            # - a) the DOS file has only spd inseat of spdf characters. Legitimate.
            # - b) if bad_hack_offset (see below) is used. Illegitimate?
            return np.zeros_like(dos_data[0])
        else:
            return dos_data[col_index]

    # get section1 variables
    E = col(index['section1']['E'])
    dos_tot = col(index['section1']['dos_tot'])
    dos_lim = (np.min(dos_tot), np.max(dos_tot))
    dos_interstitial = col(index['section1']['interstitial'])

    # sum up dos based on selection
    dos = np.zeros(len(dos_data[0]))
    if select_groups:
        for group in range(num_groups):
            if mask_groups[group]:
                if all_characters:
                    dos += col(index['section2'][group]) * atoms_per_group[group]
                else:
                    for char in range(num_chars):
                        if mask_characters[char]:
                            bad_hack_offset = 1
                            dos += col(index['section3'][char][group] + bad_hack_offset) * atoms_per_group[group]
                            # Note 1:
                            # Introduced bad_hack_offset of 1 cause when comparing bandplot to DOS plot,
                            # they seem to match only if this offset is added.
                            # But if the DOS file format above is correct, the consequences are:
                            # - DOS of (character 0 (s of spdf), group 0) is never accessed.
                            # - DOS of (last character (f), last group) is out-of-bounds, so returns zero.
                            # - all other DOS are shifted:
                            #    - DOS of (char x, group y+1) is reassigned to (char x, group y)
                            #    - DOS of (char x+1,  group 0) is reassigned to (char x, last group)
                            # This can't be correct.
                            #
                            # Note 2:
                            # For the summed DOS plot size (all groups, all characters), the following holds:
                            # section3 with bad_hack_offset < section2 < section3 without bad_hack_offset.

    if interstitial:
        dos += dos_interstitial

    # # for testing:
    # print(
    #     f"get_dos: for selection groups {mask_groups}, "
    #     f"characters {mask_characters}, "
    #     f"num_groups {num_groups}, "
    #     f"atoms_per_group {atoms_per_group}, "
    #     f"accessed dos columns (0,1,2 are E,tot_dos,interstitial and always accessed):\n{col_indices_accessed}")

    return (E, dos, dos_lim)
