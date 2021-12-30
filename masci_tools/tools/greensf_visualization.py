"""
Modules with functions for visualizing things related to greensfunctions from fleur
"""
from masci_tools.vis.common import spectral_function


def plot_kresolved_greensfunction(greensfunction, spin=None, backend=None, **kwargs):
    """
    Plot a k-resolved :py:class:`~masci_tools.tools.greensfunction.GreensFunction` calculated
    on a kpoint path as a colormesh plot. The energy contour should be chosen to be a equidistant
    grid

    :param greensfunction: :py:class:`~masci_tools.tools.greensfunction.GreensFunction` to plot
    :param spin: int which spin index to plot

    All other Kwargs are passed on to :py:func:`~masci_tools.vis.plot_methods.plot_spectral_function()`
    """

    if not greensfunction.kresolved:
        raise ValueError("Only kresolved green's functions can be plotted as spectral functions")

    if greensfunction.kpath is None:
        raise ValueError("Only green's functions calculated on a k-path can be plotted as spectral functions")

    special_kpoints = []
    for k_index, label in zip(greensfunction.extras['special_kpoint_indices'],
                              greensfunction.extras['special_kpoint_labels']):
        special_kpoints.append((label, greensfunction.kpath[k_index]))

    if spin is not None:
        spectral_func = greensfunction.trace_energy_dependence(spin=spin)
    else:
        spectral_func = greensfunction.trace_energy_dependence(spin=1)
        if greensfunction.nspins == 2:
            spectral_func += greensfunction.trace_energy_dependence(spin=2)

    return spectral_function(greensfunction.kpath,
                             greensfunction.points.real,
                             spectral_func,
                             special_kpoints=special_kpoints,
                             backend=backend,
                             **kwargs)
