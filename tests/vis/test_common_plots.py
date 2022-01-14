"""
Tests of the vis.common module Only the general routines are tested here (e.g. dos and bands routines are tested via the higher level fleur tests)
"""
import pytest
import numpy as np
import matplotlib

matplotlib.use('Agg')
from matplotlib.pyplot import gcf
import matplotlib.pyplot as plt


def test_get_plotter():
    """
    Test of the get_plotter method
    """
    from masci_tools.vis.common import get_plotter, set_default_backend
    import masci_tools.vis.plot_methods as mpl
    import masci_tools.vis.bokeh_plots as bok

    assert get_plotter('mpl') is mpl.plot_params
    assert get_plotter('matplotlib') is mpl.plot_params
    assert get_plotter('bokeh') is bok.plot_params

    assert get_plotter() is mpl.plot_params
    set_default_backend('bokeh')
    assert get_plotter() is bok.plot_params
    set_default_backend('mpl')
    assert get_plotter() is mpl.plot_params


@pytest.mark.mpl_image_compare(baseline_dir='test_common_plots/', filename='scatter_mpl.png')
def test_scatter_mpl():
    """
    Test of the scatter function with mpl backend
    """
    from masci_tools.vis.common import scatter

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()

    scatter(x, y, legend=True, color='red', markersize=6, backend='mpl', plot_label='test', show=False)

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir='test_common_plots/', filename='scatter_mpl.png')
def test_scatter_defaults():
    """
    Test of the scatter function with mpl backend
    """
    from masci_tools.vis.common import scatter

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()

    scatter(x, y, legend=True, color='red', markersize=6, plot_label='test', show=False)

    return gcf()


def test_scatter_bokeh(check_bokeh_plot):
    """
    Test of the scatter function with mpl backend
    """
    from masci_tools.vis.common import scatter

    x = np.linspace(-10, 10, 100)
    y = x**2

    p = scatter(x, y, color='red', marker_size=6, backend='bokeh', show=False)

    check_bokeh_plot(p)


@pytest.mark.mpl_image_compare(baseline_dir='test_common_plots/', filename='line_mpl.png')
def test_line_mpl():
    """
    Test of the scatter function with mpl backend
    """
    from masci_tools.vis.common import line

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()

    line(x, y, legend=True, color='red', markersize=6, backend='mpl', plot_label='test', show=False)

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir='test_common_plots/', filename='line_mpl.png')
def test_line_defaults():
    """
    Test of the line function with mpl backend
    """
    from masci_tools.vis.common import line

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()

    line(x, y, legend=True, color='red', markersize=6, plot_label='test', show=False)

    return gcf()


def test_line_bokeh(check_bokeh_plot):
    """
    Test of the line function with mpl backend
    """
    from masci_tools.vis.common import line

    x = np.linspace(-10, 10, 100)
    y = x**2

    p = line(x, y, color='red', marker_size=6, backend='bokeh', show=False)

    check_bokeh_plot(p)


@pytest.mark.mpl_image_compare(baseline_dir='test_common_plots/', filename='eos_mpl.png')
def test_eos_mpl():
    """
    Test of the eos_plot function with mpl backend
    """
    from masci_tools.vis.common import eos_plot

    scaling = np.linspace(0.95, 1.04, 10)
    energy = -500.0 + 500.0 * (0.99 - scaling)**2

    gcf().clear()

    eos_plot(scaling, total_energy=energy, show=False)

    return gcf()


def test_eos_bokeh(check_bokeh_plot):
    """
    Test of the eos_plot function with bokeh backend
    """
    from masci_tools.vis.common import eos_plot

    scaling = np.linspace(0.95, 1.04, 10)
    energy = -500.0 + 500.0 * (0.99 - scaling)**2

    p = eos_plot(scaling, total_energy=energy, backend='bokeh', show=False)

    check_bokeh_plot(p)


CONVERGENCE_ENERGIES = [
    -69269.46134019217, -69269.42108466873, -69269.35509388152, -69269.62486438647, -69269.51102655893,
    -69269.48862754989, -69269.48874847183, -69269.48459145911, -69269.47327003669, -69269.47248623992,
    -69269.47244891679, -69269.47645687914, -69269.47922946361, -69269.4793222245, -69269.47901836311,
    -69269.47895198638, -69269.47886053707, -69269.47875692157, -69269.47890881824, -69269.47887586526
]

CONVERGENCE_DISTANCES = [
    11.6508412231, 10.5637525546, 7.1938351319, 2.6117836621, 2.4735288205, 2.9455389405, 1.8364080301, 1.4740568937,
    1.8542068593, 0.9186745766, 0.900191025, 0.5290019787, 0.0979035892, 0.1098240811, 0.0717916768, 0.0258508395,
    0.0300810883, 0.0067904499, 0.0085097364, 0.0073435947
]

CONVERGENCE_ITERATIONS = range(len(CONVERGENCE_DISTANCES))


@pytest.mark.mpl_image_compare(baseline_dir='test_common_plots/', filename='convergence_mpl.png')
def test_convergence_mpl():
    """
    Test of the convergence_plot function with mpl backend
    """
    from masci_tools.vis.common import convergence_plot

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    convergence_plot(CONVERGENCE_ITERATIONS,
                     CONVERGENCE_DISTANCES,
                     CONVERGENCE_ENERGIES,
                     show=False,
                     axis_energy=ax1,
                     axis_distance=ax2)

    return fig


def test_convergence_bokeh(check_bokeh_plot):
    """
    Test of the convergence_plot function with bokeh backend
    """
    from masci_tools.vis.common import convergence_plot
    from bokeh.layouts import gridplot

    p1, p2 = convergence_plot(CONVERGENCE_ITERATIONS,
                              CONVERGENCE_DISTANCES,
                              CONVERGENCE_ENERGIES,
                              backend='bokeh',
                              show=False)

    p = gridplot([p1, p2], ncols=1)

    check_bokeh_plot(p)
