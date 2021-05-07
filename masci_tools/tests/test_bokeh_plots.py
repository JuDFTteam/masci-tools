# -*- coding: utf-8 -*-
"""
Tests of the bokeh visualization. Since the concrete visualization is difficult
to test we check the content of the underlying json for correctness
"""
import numpy as np
import pandas as pd


class TestBokehScatter:  #pylint: disable=missing-class-docstring

    def test_default(self, check_bokeh_plot):
        """
        Test with default values
        """
        from masci_tools.vis.bokeh_plots import bokeh_scatter
        x = np.linspace(-10, 10, 100)
        y = x**2

        source = pd.DataFrame(data={'x': x, 'y': y})

        p = bokeh_scatter(source, show=False)

        check_bokeh_plot(p)
