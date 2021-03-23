# -*- coding: utf-8 -*-
"""
Tests of the bokeh visualization. Since the concrete visualization is difficult
to test we check the content of the underlying json for correctness
"""
from bokeh.io import curdoc
import numpy as np
import pandas as pd


def prepare_for_regression(data):
    """
    Make the dict form the produced json data
    suitable for data_regression

    - remove any reference to ids
    - sort lists after types and given attributes for reproducible order

    :param data: dict with the json data produced for the bokeh figure
    """

    for key, val in list(data.items()):
        if key in ('id', 'root_ids'):
            del data[key]
        elif isinstance(val, dict):
            data[key] = prepare_for_regression(val)
        elif isinstance(val, list):
            for index, entry in enumerate(val):
                if isinstance(entry, dict):
                    val[index] = prepare_for_regression(entry)
            if all(isinstance(x, dict) for x in val):
                data[key] = sorted(val, key=lambda x: (x['type'], *x.get('attributes', {}).items()))
            else:
                data[key] = val

    return data


class TestBokehScatter:  #pylint: disable=missing-class-docstring

    def test_default(self, data_regression):
        """
        Test with default values
        """
        from masci_tools.vis.bokeh_plots import bokeh_scatter
        x = np.linspace(-10, 10, 100)
        y = x**2

        source = pd.DataFrame(data={'x': x, 'y': y})

        p = bokeh_scatter(source, show=False)

        curdoc().clear()
        curdoc().add_root(p)
        data_regression.check(prepare_for_regression(curdoc().to_json()))
