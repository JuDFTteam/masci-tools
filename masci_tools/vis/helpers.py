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

    combined_mask = None
    for data_key in data_keys:

        if data_key in limits:
            data_limits = limits[data_key]

            #Add padding to both sides of the limits
            data_limits = data_limits[0] - padding * (1 + abs(data_limits[0])), data_limits[1] + padding * (
                1 + abs(data_limits[1]))

            mask = plot_data.get_mask(
                lambda x, data_limits=tuple(data_limits): np.logical_and(x > data_limits[0], x < data_limits[1]),
                data_key=data_key)

            if combined_mask is None:
                combined_mask = mask
            else:
                combined_mask = [x & y for x, y in zip(mask, combined_mask)]

    if combined_mask is not None:
        plot_data.mask_data(combined_mask)


def mpl_single_line_or_area(axis,
                            entry,
                            source,
                            area=False,
                            area_vertical=False,
                            area_enclosing_line=True,
                            advance_color_cycle=False,
                            area_line_alpha=1.0,
                            **kwargs):
    """
    Create a scatterplot, lineplot or area plot for the given entry
    on the matplotlib axis

    :param axis: Axes to plot on
    :param entry: namedtuple of the entries to plot
    :param source: mapping containing the data to plot
    :param area: bool, if True fill_betweenx/y will be used to create an area plot
    :param area_vertical: bool, if True fill_betweeny will be used
    :param area_enclosing_line: bool if True the area plot will have another
                                line plot around the edge
    :param advance_color_cycle: bool, if True the matplotlib color cycle will be advanced
                                no matter what else is specified
    :param area_line_alpha: if an area plot is done this is the alpha parameter (transparency)

    Kwargs are passed to the respective plotting routines
    """
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


def get_special_kpoint_ticks(kpoints: list[tuple[str, float]], math_mode: str = '$') -> tuple[list[float], list[str]]:
    r"""
    Process the high symmetry kpoints and ggf. replace with appropiate latex symbol

    - Gamma/G is replaced with $\Gamma$

    :param kpoints: list of tuples with label and position of the points
    :param math_mode: Determines the symbol to enter math mode in latex

    :returns: Ticks and their respective labels
    """
    if kpoints is None:
        kpoints = []

    ticks = []
    ticklabels = []
    for label, position in kpoints:
        if label.lower() in ('gamma', 'g'):
            label = rf'{math_mode}\Gamma{math_mode}'
        ticklabels.append(label)
        ticks.append(position)

    return ticks, ticklabels
