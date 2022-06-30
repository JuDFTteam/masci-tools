"""
This module collects functions for calculating properties with the greens functions
calculated by Fleur. At the moment the following are implemented:

   * Calculating Heisenberg J_0 (spin stiffness) from onsite Green's functions
   * Calculating Heisenberg J_ij exchange constants from intersite Green's functions
   * Calculating the hybridization function from onsite Greens functions
"""
from __future__ import annotations

from masci_tools.util.typing import FileLike

from .greensfunction import GreensFunction, intersite_shells, intersite_shells_from_file
from masci_tools.io.common_functions import get_pauli_matrix

import numpy as np
import pandas as pd
from scipy import constants
from collections import defaultdict
from typing import Any

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  #type:ignore

#TODO:
# - Integration as one numpy operation
# - Parallelization/threading
# - multiple blocks/orbital contributions
# - custom decompositions (e.g. e2g/t2g)


def calculate_heisenberg_jij(
    hdffileORgreensfunctions: FileLike | list[GreensFunction],
    reference_atom: int,
    onsite_delta: np.ndarray,
    max_shells: int | None = None,
) -> pd.DataFrame:
    r"""
    Calculate the Heisenberg exchange constants form Green's functions using the formula

    .. math::
        J_{ij} = \frac{1}{4\pi} \mathrm{Im}\ \mathrm{Tr_L} \int_{-\infty}^{E_F}\!\mathrm{dz} \Delta_iG^\uparrow_{ij}(z)\Delta_jG^\downarrow_{ji}(z)

    :param hdffileORgreensfunctions: either pat/file-like object for the ``greensf.hdf`` file to use or list of :py:class:`~masci_tools.tools.greensfunction.GreensFunction`
    :param reference_atom: integer index of the atom to calculate the Jijs from
    :param onsite_delta: List of floats containing the onsite exchange splitting for each atom type and l-channel
    :param max_shells: optional int, if given only the first max_shells shells are constructed

    :returns: pandas DataFrame containing all the Jij constants
    """

    if isinstance(hdffileORgreensfunctions, list):
        shells = intersite_shells(hdffileORgreensfunctions, reference_atom, max_shells=max_shells)
    else:
        shells = intersite_shells_from_file(hdffileORgreensfunctions, reference_atom, max_shells=max_shells)

    jij_constants: dict[str, list[Any]] = defaultdict(list)

    for dist, g1, g2 in shells:

        dist = round(dist, 12)

        g1.to_global_frame()
        g2.to_global_frame()

        gij = g1.energy_dependence(both_contours=True, spin=1)
        gji = g2.energy_dependence(both_contours=True, spin=2)

        delta_square = onsite_delta[g1.atomType - 1, g1.l] * onsite_delta[g1.atomTypep - 1, g1.l]
        weights = np.array([g1.weights, -g1.weights.conj()]).T

        integral = np.einsum('zm,zijm,zjim->', weights, gij, gji)
        jij = 0.5 * 1 / (8.0 * np.pi * 1j) * delta_square * integral

        jij_constants['R'].append(dist)
        jij_constants['R_ij_x'].append(g1.atomDiff.tolist()[0])
        jij_constants['R_ij_y'].append(g1.atomDiff.tolist()[1])
        jij_constants['R_ij_z'].append(g1.atomDiff.tolist()[2])
        jij_constants['Atom i'].append(f"{g1.extras['atom_label']}({g1.extras['element']})")
        jij_constants['Atom j'].append(f"{g1.extras['atom_labelp']}({g1.extras['elementp']})")
        jij_constants['J_ij'].append(jij.real * 1000)  #Convert to meV

    return pd.DataFrame.from_dict(jij_constants)


def calculate_heisenberg_tensor(hdffileORgreensfunctions: FileLike | list[GreensFunction],
                                reference_atom: int,
                                onsite_delta: np.ndarray,
                                max_shells: int | None = None) -> pd.DataFrame:
    r"""
    Calculate the Heisenberg exchange tensor :math:`\mathbf{J}` from Green's functions using the formula

    .. math::
        J^{\alpha\beta}_{ij} = \frac{1}{4\pi} \mathrm{Im}\ \mathrm{Tr_L} \int_{-\infty}^{E_F}\!\mathrm{dz} \Delta_i\sigma_{\alpha}G_{ij}(z)\Delta_j\sigma_{\beta}G_{ji}(z)

    for all :math:`\alpha\ \mathrm{and}\ \beta=x,y,z`.

    :param hdffileORgreensfunctions: either pat/file-like object for the ``greensf.hdf`` file to use or list of :py:class:`~masci_tools.tools.greensfunction.GreensFunction`
    :param reference_atom: integer index of the atom to calculate the Jijs from
    :param onsite_delta: List of floats containing the onsite exchange splitting for each atom type and l-channel
    :param max_shells: optional int, if given only the first max_shells shells are constructed

    :returns: pandas DataFrame containing all the J_xx, J_xy, etc. constants
    """

    if isinstance(hdffileORgreensfunctions, list):
        shells = intersite_shells(hdffileORgreensfunctions, reference_atom, max_shells=max_shells)
    else:
        shells = intersite_shells_from_file(hdffileORgreensfunctions, reference_atom, max_shells=max_shells)

    jij_tensor: dict[str, list[Any]] = defaultdict(list)

    for dist, g1, g2 in shells:

        dist = round(dist, 12)

        g1.to_global_frame()
        g2.to_global_frame()
        gij = g1.energy_dependence(both_contours=True)
        gji = g2.energy_dependence(both_contours=True)

        delta_square = onsite_delta[g1.atomType - 1, g1.l] * onsite_delta[g1.atomTypep - 1, g1.l]
        weights = np.array([g1.weights, -g1.weights.conj()]).T

        jij_tensor['R'].append(dist)
        jij_tensor['R_ij_x'].append(g1.atomDiff.tolist()[0])
        jij_tensor['R_ij_y'].append(g1.atomDiff.tolist()[1])
        jij_tensor['R_ij_z'].append(g1.atomDiff.tolist()[2])
        jij_tensor['Atom i'].append(f"{g1.extras['atom_label']}({g1.extras['element']})")
        jij_tensor['Atom j'].append(f"{g1.extras['atom_labelp']}({g1.extras['elementp']})")

        for sigmai_str in ('x', 'y', 'z'):
            for sigmaj_str in ('x', 'y', 'z'):

                sigmai = get_pauli_matrix(sigmai_str)  #type: ignore[arg-type]
                sigmaj = get_pauli_matrix(sigmaj_str)  #type: ignore[arg-type]

                integral = np.einsum('zm,ab,zijbcm,cd,zjidam->', weights, sigmai, gij, sigmaj, gji)
                jij = 1 / 4 * 1 / (8.0 * np.pi * 1j) * delta_square * integral
                jij_tensor[f'J_{sigmai_str}{sigmaj_str}'].append(jij.real * 1000)  #Convert to meV

    return pd.DataFrame.from_dict(jij_tensor)


def decompose_jij_tensor(jij_tensor: pd.DataFrame, moment_direction: Literal['x', 'y', 'z']) -> pd.DataFrame:
    r"""
    Decompose the Heisenberg tensor as calculated by :py:func:`calculate_heisenberg_tensor()`
    into three parts

    - Isotropic :math:`J = \frac{1}{3} \mathrm{Tr}\left[\mathbf{J}\right]`
    - Symmetric traceless :math:`J_S = \frac{1}{2} \left(\mathbf{J} + \mathbf{J}^T\right) - J`
    - Antisymmetric :math:`J_A = \frac{1}{2} \left(\mathbf{J} - \mathbf{J}^T\right)`

    :param jij_tensor: Heisenberg tensor

    :returns: tuple of the three aforementioned components
    """

    if moment_direction == 'x':
        jij_tensor['J_ij'] = 1 / 2 * (jij_tensor['J_yy'] + jij_tensor['J_zz'])  #Isotropic
        jij_tensor['A_ij'] = 1 / 2 * (jij_tensor['J_yy'] - jij_tensor['J_zz'])  #Difference in diagonal
        jij_tensor['S_ij'] = 1 / 2 * (jij_tensor['J_yz'] + jij_tensor['J_zy'])  #Offdiagonal symmetric
        jij_tensor['D_ij'] = 1 / 2 * (jij_tensor['J_yz'] - jij_tensor['J_zy'])  #Offdiagonal asymmetric
    elif moment_direction == 'y':
        jij_tensor['J_ij'] = 1 / 2 * (jij_tensor['J_xx'] + jij_tensor['J_zz'])  #Isotropic
        jij_tensor['A_ij'] = 1 / 2 * (jij_tensor['J_xx'] - jij_tensor['J_zz'])  #Difference in diagonal
        jij_tensor['S_ij'] = 1 / 2 * (jij_tensor['J_xz'] + jij_tensor['J_zx'])  #Offdiagonal symmetric
        jij_tensor['D_ij'] = 1 / 2 * (jij_tensor['J_xz'] - jij_tensor['J_zx'])  #Offdiagonal asymmetric
    elif moment_direction == 'z':
        jij_tensor['J_ij'] = 1 / 2 * (jij_tensor['J_xx'] + jij_tensor['J_yy'])  #Isotropic
        jij_tensor['A_ij'] = 1 / 2 * (jij_tensor['J_xx'] - jij_tensor['J_yy'])  #Difference in diagonal
        jij_tensor['S_ij'] = 1 / 2 * (jij_tensor['J_xy'] + jij_tensor['J_yx'])  #Offdiagonal symmetric
        jij_tensor['D_ij'] = 1 / 2 * (jij_tensor['J_xy'] - jij_tensor['J_yx'])  #Offdiagonal asymmetric

    else:
        raise ValueError(f'Invalid direction: {moment_direction}')

    return jij_tensor


def heisenberg_reciprocal(qpoints: np.ndarray, jij_data: pd.DataFrame, entry: str = 'J_ij') -> np.ndarray:
    r"""
    Calculate the fourier transform of an entry for interaction constants

    Example for :math:`J_{ij}`

    .. math::
        J(\mathbf{q})\ =\ \sum_{ij} J_{ij} e^{i\mathbf{q}\cdot\mathbf{R}_{ij}}

    where :math:`\mathbf{R}_{ij}` is the connecting vector associated with the :math:`J_{ij}`

    :param qpoints: numpy array containing the coordinates of the qpoints
    :param jij_data: DataFrame generated by the above calculation functions
    :param entry: str of the entry to calculate

    :returns: numpy array containing the Fourier transform
    """
    interactions = jij_data[entry]
    r_vectors = np.array([jij_data['R_ij_x'], jij_data['R_ij_y'], jij_data['R_ij_z']]).T
    expo = np.exp(1j * np.einsum('qi,ki->qk', qpoints, r_vectors))

    interactions_reciprocal = np.einsum('k,qk->q', interactions, expo)
    return interactions_reciprocal


def calculate_heisenberg_j0(greensfunction: GreensFunction, onsite_delta: float, show: bool = False) -> float:
    r"""
    Calculate spin stiffness J_0 for the given green's function using the formula

    .. math::
        J_{0} = \frac{1}{4\pi} \mathrm{Im}\ \mathrm{Tr_L} \int_{-\infty}^{E_F}\!\mathrm{dz} \Delta\left(G^\uparrow(z)-G^\downarrow(z)\right) + \Delta^2G^\uparrow(z)G^\downarrow(z)

    :param greensfunction: :py:class:`~masci_tools.tools.greensfunction.GreensFunction` to use for the calculation
    :param onsite_delta: onsite exchange splitting to use for the calculation
    :param show: bool if True additional information about the used Greens functions is printed out

    :returns: the value of the spin stiffness in meV
    """

    g_up = greensfunction.energy_dependence(spin=1, both_contours=True)
    g_dn = greensfunction.energy_dependence(spin=2, both_contours=True)

    j0 = 0.0
    for weight, g_upz, g_dnz in zip(greensfunction.weights, g_up, g_dn):

        j0 += 1/(8.0*np.pi*1j) * (\
              weight *        (onsite_delta * (np.trace(g_upz[...,0])-np.trace(g_dnz[...,0])) \
                                + onsite_delta**2 * np.trace(g_upz[...,0].dot(g_dnz[...,0]))) \
             -weight.conj() * (onsite_delta * (np.trace(g_upz[...,1])-np.trace(g_dnz[...,1])) \
                                + onsite_delta**2 * np.trace(g_upz[...,1].dot(g_dnz[...,1]))))

    j0 = j0.real * 1000.0
    if show:
        print(f'Effective exchange Interaction: {j0:.4f} meV')
        print(f"Curie Temperature: {2.0/3.0*j0*1.0/constants.value('Boltzmann constant in eV/K')*1/1000.0:.4f} K"
              )  #1/1000 to convert to meV

    return j0


def calculate_hybridization(greensfunction: GreensFunction) -> np.ndarray:
    r"""
    Calculate the hybridization function as

    .. math::
        \Delta(z) = \frac{1}{2*l+1} \mathrm{Tr} G^{-1}(z)

    :returns: numpy array of the hybridization function
    """
    gz = greensfunction.trace_energy_dependence()
    delta = 1 / (2 * greensfunction.l + 1) * np.linalg.inv(gz)
    return delta.real
