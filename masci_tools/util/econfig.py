"""
Functions for expanding/splitting or converting electron configuration strings
"""
from __future__ import annotations

from masci_tools.util.constants import PERIODIC_TABLE_ELEMENTS, ATOMIC_NUMBERS

all_econfig = [
    '1s2', '2s2', '2p6', '3s2', '3p6', '4s2', '3d10', '4p6', '5s2', '4d10', '5p6', '6s2', '4f14', '5d10', '6p6', '7s2',
    '5f14', '6d10', '7p6', '8s2', '6f14'
]
states_spin = {'s': ['1/2'], 'p': ['1/2', '3/2'], 'd': ['3/2', '5/2'], 'f': ['5/2', '7/2']}
max_state_occ = {'s': 2., 'p': 6., 'd': 10., 'f': 14.}
max_state_occ_spin = {'1/2': 2., '3/2': 4., '5/2': 6., '7/2': 8.}


def get_econfig(element: str | int, full: bool = False) -> str | None:
    """
    returns the econfiguration as a string of an element.

    :param element: element string
    :param full: a bool if True the econfig without [He]... is returned
    :returns: a econfig string
    """
    if isinstance(element, int):
        econ: str | None = PERIODIC_TABLE_ELEMENTS.get(element, {}).get('econfig')  #type:ignore
    elif isinstance(element, str):
        element_num = ATOMIC_NUMBERS.get(element, None)
        if element_num is None:
            raise ValueError(f'No element available called {element}')
        econ: str = PERIODIC_TABLE_ELEMENTS.get(element_num, {}).get('econfig')  #type:ignore
    else:
        raise ValueError('element has to be and int or string')

    if full and econ is not None:
        econ = rek_econ(econ)

    return econ


def get_coreconfig(element: str | int, full: bool = False) -> str | None:
    """
    returns the econfiguration as a string of an element.

    :param element: element string
    :param full: a bool if True the econfig without [He]... is returned
    :return: coreconfig string
    """
    econ = get_econfig(element, full=full)
    return econ.split('|', maxsplit=1)[0].rstrip() if econ is not None else None


def rek_econ(econfigstr: str) -> str | None:
    """
    recursive routine to return a full econfig
    '[Xe] 4f14 | 5d10 6s2 6p4' -> '1s 2s ... 4f14 | 5d10 6s2 6p4'

    :param econfigstr: electron config string to expand

    :returns: expanded econfig string
    """
    split_econ = econfigstr.strip('[').split(']')
    if len(split_econ) == 1:
        return econfigstr
    rest = split_econ[1]
    elem = split_econ[0]
    econfig = get_econfig(elem)
    if econfig is not None:
        econ = econfig.replace(' |', '')
        return rek_econ(econ + rest)  # for now
    return None


def convert_fleur_config_to_econfig(fleurconf_str: str, keep_spin: bool = False) -> str:
    """
    '[Kr] (4d3/2) (4d5/2) (4f5/2) (4f7/2)' -> '[Kr] 4d10 4f14', or '[Kr] 4d3/2 4d5/2 4f5/2 4f7/2'

    # for now only use for coreconfig, it will fill all orbitals, since it has no information on the filling.

    :param fleurconf_str: string of the electron config like it is read from the inp.xml
    :param keep_spin: bool if True the spin indices will be kept in the converted string

    :returns: string of the electron config to be used in the inpgen
    """

    econfstring = fleurconf_str.replace('(', '').replace(')', '')

    if keep_spin:
        econfstring.split()
    else:
        elist = econfstring.split()
        econfstring_new = ''
        for state in elist:
            if '/' in state:
                # check if nl was added before if not add it with full occ
                base = state[:2]
                spin = state[2:]
                occ = max_state_occ_spin.get(spin)
                if occ is None:
                    raise ValueError(f'Failed to get maximum occupation for spin {spin}')
                if base not in econfstring_new:
                    econfstring_new = f'{econfstring_new}{base}{int(occ)} '
                else:
                    max_occ = max_state_occ.get(base[1])
                    if max_occ is None:
                        raise ValueError(f'Failed to get maximum occupation for orbital {base[1]}')
                    econfstring_new = econfstring_new.split(base, maxsplit=1)[0] + f'{base}{int(max_occ)} '
                    # we assume here that the two states come behind each other, ... rather bad
                    #econfstring_new.replace('{}'.format(base)
            else:
                econfstring_new = econfstring_new + state + ' '
        econfstring = econfstring_new

    return econfstring.strip()
