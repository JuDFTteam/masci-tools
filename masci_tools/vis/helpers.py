"""
Collection of routines to be reused in plotting routines
"""
from __future__ import annotations

import numpy as np

from .data import PlotData


def exclude_points(plot_data: PlotData,
                   *data_keys: str,
                   limits: dict[str, tuple[float, float]] | None,
                   padding: float = 0.1) -> None:
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
            data_limits = data_limits[0] - padding * (1 + abs(data_limits[0])), data_limits[1] + padding * (
                1 + abs(data_limits[1]))

            mask_func = lambda x, data_limits=tuple(data_limits): np.logical_and(x > data_limits[0], x < data_limits[1])
            data_mask = plot_data.get_mask(mask_func, data_key=data_key)

            if mask is None:
                mask = data_mask
            else:
                mask = [x & y for x, y, in zip(data_mask, mask)]

    if mask is not None:
        plot_data.mask_data(mask)


def _mpl_single_line_or_area(axis,
                             entry,
                             source,
                             area=False,
                             area_vertical=False,
                             area_enclosing_line=True,
                             advance_color_cycle=False,
                             area_line_alpha=1.0,
                             **kwargs):

    if any(key not in entry._fields for key in ('x', 'y')):
        raise ValueError('Entry has to contain x and y fields')

    if area and 'shift' not in entry._fields:
        raise ValueError('For area plots entry has to contain shift fields')

    yerr = entry.yerr if 'yerr' in entry._fields else None
    xerr = entry.xerr if 'xerr' in entry._fields else None

    if area:
        linecolor = kwargs.pop('area_linecolor', None)
        #Workaround for https://github.com/JuDFTteam/masci-tools/issues/129
        #fill_between does not advance the color cycle messing up the following colors
        if kwargs.get('color') is None:
            #This is not ideal but it is the only way I found
            #of accessing the state of the color cycle
            kwargs['color'] = axis._get_lines.get_next_color()  #pylint: disable=protected-access

        if area_vertical:
            result = axis.fill_betweenx(entry.y, entry.x, x2=entry.shift, data=source, **kwargs)
        else:
            result = axis.fill_between(entry.x, entry.y, y2=entry.shift, data=source, **kwargs)

        kwargs['alpha'] = area_line_alpha
        kwargs['label'] = None
        kwargs['color'] = linecolor or result.get_facecolor()[0]

        if area_enclosing_line:
            axis.errorbar(entry.x, entry.y, yerr=yerr, xerr=xerr, data=source, **kwargs)
    else:
        if kwargs.get('color') is not None and advance_color_cycle:
            axis._get_lines.get_next_color()  #pylint: disable=protected-access
        axis.errorbar(entry.x, entry.y, yerr=yerr, xerr=xerr, data=source, **kwargs)

    return axis
