"""
Collection of routines to be reused in plotting routines
"""
from __future__ import annotations

import numpy as np

from .data import PlotData

def exclude_points(plot_data: PlotData, *data_keys: str, limits: dict[str,tuple[float,float]] | None, padding: float=0.1) -> None:
    """
    Exclude points outside the given limits

    :param plot_data: PlotData instance containing all the data for plots
    :param data_keys: str of the keys to consider for excluding points
    :param limits: dict of the set plot limits
    :param padding: float, determines how far beyond the plot limits a point has to lie to be excluded (default 10%)
    """

    if limits is None:
        return

    mask = None
    for data_key in data_keys:

        if data_key in limits:
            data_limits = limits[data_key]

            #Add padding to both sides of the limits
            data_limits = data_limits[0] - padding * (1 + abs(data_limits[0])), data_limits[1] + padding * (1 + abs(data_limits[1]))

            mask_func = lambda x, data_limits=tuple(data_limits): np.logical_and(x > data_limits[0], x < data_limits[1])
            data_mask = plot_data.get_mask(mask_func, data_key=data_key)

            if mask is None:
                mask = data_mask
            else:
                mask = [x & y for x, y, in zip(data_mask, mask)]

    if mask is not None:
        plot_data.mask_data(mask)
