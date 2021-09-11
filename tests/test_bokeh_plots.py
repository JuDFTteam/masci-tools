# -*- coding: utf-8 -*-
"""
Tests of the bokeh visualization. Since the concrete visualization is difficult
to test we check the content of the underlying json for correctness
"""
import numpy as np
import pandas as pd
import pytest


def test_bokeh_methods_imports():
    """
    Test that all expected functions are still there
    """
    from masci_tools.vis.bokeh_plots import set_bokeh_plot_defaults
    from masci_tools.vis.bokeh_plots import reset_bokeh_plot_defaults
    from masci_tools.vis.bokeh_plots import show_bokeh_plot_defaults
    from masci_tools.vis.bokeh_plots import save_bokeh_defaults
    from masci_tools.vis.bokeh_plots import load_bokeh_defaults
    from masci_tools.vis.bokeh_plots import bokeh_scatter
    from masci_tools.vis.bokeh_plots import bokeh_multi_scatter
    from masci_tools.vis.bokeh_plots import bokeh_line
    from masci_tools.vis.bokeh_plots import bokeh_dos
    from masci_tools.vis.bokeh_plots import bokeh_spinpol_dos
    from masci_tools.vis.bokeh_plots import bokeh_bands
    from masci_tools.vis.bokeh_plots import bokeh_spinpol_bands
    from masci_tools.vis.bokeh_plots import periodic_table_plot
    from masci_tools.vis.bokeh_plots import plot_convergence_results
    from masci_tools.vis.bokeh_plots import plot_convergence_results_m


TEST_CHANGES = [{'marker_size': 50}, {'show': False}, {'straight_line_options': {'line_color': 'red'}}]

EXPECTED_RESULT = [{
    'marker_size': 50
}, {
    'show': False
}, {
    'straight_line_options': {
        'line_color': 'red',
        'line_width': 1.0,
        'line_dash': 'dashed'
    },
}]


@pytest.mark.parametrize('change_dict, result', zip(TEST_CHANGES, EXPECTED_RESULT))
def test_set_defaults(change_dict, result):
    """
    Test the setting of default values
    """
    from masci_tools.vis.bokeh_plots import plot_params
    from masci_tools.vis.bokeh_plots import set_bokeh_plot_defaults
    from masci_tools.vis.bokeh_plots import reset_bokeh_plot_defaults

    value_before = {}
    for key in change_dict:
        value_before[key] = plot_params[key]

    set_bokeh_plot_defaults(**change_dict)

    for key, val in result.items():
        assert plot_params[key] == val

    reset_bokeh_plot_defaults()

    for key, val in value_before.items():
        assert plot_params[key] == val


def test_bokeh_save_defaults(file_regression):
    """
    Test adding of custom parameters
    """
    import tempfile
    from masci_tools.vis.bokeh_plots import set_bokeh_plot_defaults
    from masci_tools.vis.bokeh_plots import reset_bokeh_plot_defaults
    from masci_tools.vis.bokeh_plots import save_bokeh_defaults

    set_bokeh_plot_defaults(marker_size=50,
                            line_alpha=0.5,
                            figure_kwargs={
                                'x_axis_type': 'log',
                                'active_inspect': 'hover'
                            })

    with tempfile.NamedTemporaryFile('r') as file:
        save_bokeh_defaults(file.name)

        txt = file.read().strip()
        file_regression.check(txt)

    reset_bokeh_plot_defaults()


def test_bokeh_load_defaults(file_regression):
    """
    Test adding of custom parameters
    """
    import tempfile
    from masci_tools.vis.bokeh_plots import set_bokeh_plot_defaults
    from masci_tools.vis.bokeh_plots import reset_bokeh_plot_defaults
    from masci_tools.vis.bokeh_plots import save_bokeh_defaults
    from masci_tools.vis.bokeh_plots import load_bokeh_defaults

    set_bokeh_plot_defaults(marker_size=50,
                            line_alpha=0.5,
                            figure_kwargs={
                                'x_axis_type': 'log',
                                'active_inspect': 'hover'
                            })

    with tempfile.NamedTemporaryFile('r') as file:
        save_bokeh_defaults(file.name)

        reset_bokeh_plot_defaults()

        load_bokeh_defaults(file.name)

    with tempfile.NamedTemporaryFile('r') as file:
        save_bokeh_defaults(file.name)

        txt = file.read().strip()
        file_regression.check(txt)

    reset_bokeh_plot_defaults()


class TestBokehScatter:  #pylint: disable=missing-class-docstring

    def test_default(self, check_bokeh_plot):
        """
        Test with default values
        """
        from masci_tools.vis.bokeh_plots import bokeh_scatter
        x = np.linspace(-10, 10, 100)
        y = x**2

        source = pd.DataFrame(data={'x': x, 'y': y})

        p = bokeh_scatter('x', 'y', data=source, show=False)

        check_bokeh_plot(p)

    def test_deprecated_signature(self, check_bokeh_plot):
        """
        Test with default values and old signature
        """
        from masci_tools.vis.bokeh_plots import bokeh_scatter
        x = np.linspace(-10, 10, 100)
        y = x**2

        source = pd.DataFrame(data={'x': x, 'y': y})

        with pytest.deprecated_call():
            p = bokeh_scatter(source, show=False)

        check_bokeh_plot(p)

    def test_param_change(self, check_bokeh_plot):
        """
        Test with parameters changed
        """
        from masci_tools.vis.bokeh_plots import bokeh_scatter
        x = np.linspace(-10, 10, 100)
        y = x**2

        source = pd.DataFrame(data={'x': x, 'y': y})

        p = bokeh_scatter('x',
                          'y',
                          data=source,
                          show=False,
                          color='darkred',
                          label_fontsize='24pt',
                          marker='square',
                          marker_size=12,
                          alpha=0.8)

        check_bokeh_plot(p)

    def test_limits(self, check_bokeh_plot):
        """
        Test with setting limits
        """
        from masci_tools.vis.bokeh_plots import bokeh_scatter
        x = np.linspace(-10, 10, 100)
        y = x**2

        source = pd.DataFrame(data={'x': x, 'y': y})

        p = bokeh_scatter('x', 'y', data=source, show=False, limits={'x': (0, 10), 'y': (-50, 50)})

        check_bokeh_plot(p)

    def test_straight_lines(self, check_bokeh_plot):
        """
        Test with straight lines
        """
        from masci_tools.vis.bokeh_plots import bokeh_scatter
        x = np.linspace(-10, 10, 100)
        y = x**2

        source = pd.DataFrame(data={'x': x, 'y': y})

        p = bokeh_scatter('x', 'y', data=source, show=False, straight_lines={'vertical': 0, 'horizontal': [10, 20, 30]})

        check_bokeh_plot(p)

    def test_legend(self, check_bokeh_plot):
        """
        Test with straight lines
        """
        from masci_tools.vis.bokeh_plots import bokeh_scatter
        x = np.linspace(-10, 10, 100)
        y = x**2

        source = pd.DataFrame(data={'x': x, 'y': y})

        p = bokeh_scatter('x', 'y', data=source, show=False, legend_label='Test Data')

        check_bokeh_plot(p)


class TestBokehMultiScatter:  #pylint: disable=missing-class-docstring

    def test_default_no_data(self, check_bokeh_plot):
        """
        Test with default values
        """
        from masci_tools.vis.bokeh_plots import bokeh_multi_scatter

        x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
        y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

        p = bokeh_multi_scatter(x, y, show=False)

        check_bokeh_plot(p)

    def test_multi_deprecated_signature(self, check_bokeh_plot):
        """
        Test with default values and old signature
        """
        from masci_tools.vis.bokeh_plots import bokeh_multi_scatter
        x = np.linspace(-10, 10, 100)
        y = x**2

        source = pd.DataFrame(data={'x': x, 'y': y})

        with pytest.deprecated_call():
            p = bokeh_multi_scatter(source, show=False)

        check_bokeh_plot(p)


class TestBokehLine:  #pylint: disable=missing-class-docstring

    def test_default_no_data_line(self, check_bokeh_plot):
        """
        Test with default values
        """
        from masci_tools.vis.bokeh_plots import bokeh_line

        x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
        y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

        p = bokeh_line(x, y, show=False)

        check_bokeh_plot(p)

    def test_multi_deprecated_signature_line(self, check_bokeh_plot):
        """
        Test with default values and old signature
        """
        from masci_tools.vis.bokeh_plots import bokeh_line
        x = np.linspace(-10, 10, 100)
        y = x**2

        source = pd.DataFrame(data={'x': x, 'y': y})

        with pytest.deprecated_call():
            p = bokeh_line(source, show=False)

        check_bokeh_plot(p)


class TestPlotConvergenceResults(object):  #pylint: disable=missing-class-docstring

    energies = [
        -69269.46134019217, -69269.42108466873, -69269.35509388152, -69269.62486438647, -69269.51102655893,
        -69269.48862754989, -69269.48874847183, -69269.48459145911, -69269.47327003669, -69269.47248623992,
        -69269.47244891679, -69269.47645687914, -69269.47922946361, -69269.4793222245, -69269.47901836311,
        -69269.47895198638, -69269.47886053707, -69269.47875692157, -69269.47890881824, -69269.47887586526
    ]

    distances = [
        11.6508412231, 10.5637525546, 7.1938351319, 2.6117836621, 2.4735288205, 2.9455389405, 1.8364080301,
        1.4740568937, 1.8542068593, 0.9186745766, 0.900191025, 0.5290019787, 0.0979035892, 0.1098240811, 0.0717916768,
        0.0258508395, 0.0300810883, 0.0067904499, 0.0085097364, 0.0073435947
    ]

    iteration = range(len(distances))

    def test_defaults(self, check_bokeh_plot):
        """
        Test of convergence plot with default values
        """
        from masci_tools.vis.bokeh_plots import plot_convergence_results

        p = plot_convergence_results(self.iteration, self.distances, self.energies, show=False)

        # need to return the figure in order for mpl checks to work
        check_bokeh_plot(p)

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/convergence/',
                                   filename='param_change.png')
    def test_param_change(self, check_bokeh_plot):
        """
        Test of convergence plot with changed parameters
        """
        from masci_tools.vis.bokeh_plots import plot_convergence_results

        p = plot_convergence_results(self.iteration,
                                     self.distances,
                                     self.energies,
                                     show=False,
                                     color='darkred',
                                     label_fontsize='24pt',
                                     marker='square',
                                     marker_size=12,
                                     alpha=0.8)

        check_bokeh_plot(p)


class TestPlotConvergenceMulti(object):  #pylint: disable=missing-class-docstring

    def test_defaults(self, check_bokeh_plot):
        """
        Test of multiple convergence plot with default values
        """
        from masci_tools.vis.bokeh_plots import plot_convergence_results_m

        np.random.seed(19680801)
        number_iterations = np.random.randint(15, high=50, size=15)
        iteration = [np.array(range(iters)) for iters in number_iterations]

        noise_arr = [0.1 * np.random.randn(iters) + 1.0 for iters in number_iterations]

        distance_decay = np.random.rand(15)
        distance_offset = 100 * np.random.rand(15)

        energy_decay = np.random.rand(15)
        energy_offset = 20000 + 500 * np.random.rand(15)
        energy_offset2 = 1000 * np.random.rand(15)

        distances = [
            noise * offset * np.exp(-decay * iters)
            for iters, noise, decay, offset in zip(iteration, noise_arr, distance_decay, distance_offset)
        ]
        energies = [
            noise * offset2 * np.exp(-decay * iters) + offset for iters, noise, decay, offset, offset2 in zip(
                iteration, noise_arr, energy_decay, energy_offset, energy_offset2)
        ]

        p = plot_convergence_results_m(iteration, distances, energies, show=False)

        # need to return the figure in order for mpl checks to work
        check_bokeh_plot(p)
