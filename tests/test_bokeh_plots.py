# -*- coding: utf-8 -*-
"""
Tests of the bokeh visualization. Since the concrete visualization is difficult
to test we check the content of the underlying json for correctness
"""
import numpy as np
import pandas as pd
import pytest


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
