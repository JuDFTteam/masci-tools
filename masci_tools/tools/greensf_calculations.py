"""
This module collects functions for calculating properties with the greens functions
calculated by Fleur. At the moment the following are implemented:

   * Calculating Heisenberg J_0 (spin stiffness) from onsite Green's functions
   * Calculating Heisenberg J_ij exchange constants from intersite Green's functions
   * Calculating the hybridization function from onsite Greens functions
"""
from __future__ import annotations

from .greensfunction import intersite_shells, intersite_shells_from_file

import numpy as np
from scipy import constants
from collections import defaultdict


def calculate_heisenberg_jij(hdffileORgreensfunctions, reference_atom, onsite_delta, show=False):
    r"""
    Calculate the Heisenberg exchange constants form Green's functions using the formula

    .. math::
        J_{ij} = \frac{1}{4\pi} \mathrm{Im}\ \mathrm{Tr_L} \int_{-\infty}^{E_F}\!\mathrm{dz} \Delta_iG_{ij}(z)\Delta_jG_{ji}(z)

    :param hdffileORgreensfunctions: either pat/file-like object for the ``greensf.hdf`` file to use or list of :py:class:`~masci_tools.tools.greensfunction.GreensFunction`
    :param reference_atom: integer index of the atom to calculate the Jijs from
    :param onsite_delta: List of floats containing the onsite exchange splitting for each atom type and l-channel
    :param show: bool if True additional information about the used Greens functions is printed out

    :returns: dict mapping the distances to all the calculated Jijs for that distance
    """

    if isinstance(hdffileORgreensfunctions, list):
        shells = intersite_shells(hdffileORgreensfunctions, reference_atom, show=show)
    else:
        shells = intersite_shells_from_file(hdffileORgreensfunctions, reference_atom, show=show)

    jij_constants: dict[float, list[float]] = defaultdict(list)

    for dist, g1, g2 in shells:

        dist = round(dist, 12)

        jij = 0.0
        gij = g1.energy_dependence(spin=1, both_contours=True)
        gji = g2.energy_dependence(spin=2, both_contours=True)

        for weight, gijz, gjiz in zip(g1.weights, gij, gji):

            jij += 0.5 * 1/(8.0*np.pi*1j) * onsite_delta[g1.atomType-1,g1.l] * onsite_delta[g1.atomTypep-1,g1.l]\
                  * (weight * np.trace(gijz[...,0] @ gjiz[...,0]) \
                     - weight.conj() * np.trace(gijz[...,1] @ gjiz[...,1]))

        jij_constants[dist].append(jij.real * 1000.0)
        if show:
            print(f'distance: {dist}; J_{g1.l}{g1.lp}: {jij.real*1000.0} meV')

    if show:
        print(f'J_0 calculated as sum of J_ij constants: {sum(np.sum(jijs) for jijs in jij_constants.values())} meV')

    return dict(jij_constants)


def calculate_heisenberg_j0(greensfunction, onsite_delta, show=False):
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


def calculate_hybridization(greensfunction):
    r"""
    Calculate the hybridization function as

    .. math::
        \Delta(z) = \frac{1}{2*l+1} \mathrm{Tr} G^{-1}(z)

    :returns: numpy array of the hybridization function
    """
    gz = greensfunction.trace_energy_dependence()
    delta = 1 / (2 * greensfunction.l + 1) * np.linalg.inv(gz)
    return delta.real
