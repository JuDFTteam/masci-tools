"""
Common interface for plotting functions in different backends
"""
from enum import Enum

_DEFAULT_BACKEND = 'mpl'

def set_default_backend(backend):

    global _DEFAULT_BACKEND
    backend = PlotBackend.from_str(backend)
    _DEFAULT_BACKEND = backend.value

class PlotBackend(Enum):
    mpl = 'matplotlib'
    bokeh = 'bokeh'

    @staticmethod
    def from_str(label):
        if label is None:
            #Default backend
            return PlotBackend.default()
        elif label.lower() in ('mpl', 'matplotlib'):
            return PlotBackend.mpl
        elif label.lower() in ('bokeh', ):
            return PlotBackend.bokeh
        else:
            raise NotImplementedError

    @staticmethod
    def default():
        return PlotBackend.from_str(_DEFAULT_BACKEND)


def set_defaults(backend=None, **kwargs):
    from .plot_methods import set_mpl_plot_defaults
    from .bokeh_plots import set_bokeh_plot_defaults

    backend = PlotBackend.from_str(backend)

    if backend == PlotBackend.mpl:
        set_mpl_plot_defaults(**kwargs)
    elif backend == PlotBackend.bokeh:
        set_bokeh_plot_defaults(**kwargs)
    else:
        raise NotImplementedError

def reset_defaults(backend=None):
    from .plot_methods import reset_mpl_plot_defaults
    from .bokeh_plots import reset_bokeh_plot_defaults

    backend = PlotBackend.from_str(backend)

    if backend == PlotBackend.mpl:
        reset_mpl_plot_defaults()
    elif backend == PlotBackend.bokeh:
        reset_bokeh_plot_defaults()
    else:
        raise NotImplementedError

def show_defaults(backend=None):
    from .plot_methods import show_mpl_plot_defaults
    from .bokeh_plots import show_bokeh_plot_defaults

    backend = PlotBackend.from_str(backend)

    if backend == PlotBackend.mpl:
        show_mpl_plot_defaults()
    elif backend == PlotBackend.bokeh:
        show_bokeh_plot_defaults()
    else:
        raise NotImplementedError

def get_help(key, backend=None):
    from .plot_methods import get_mpl_help
    from .bokeh_plots import get_bokeh_help

    backend = PlotBackend.from_str(backend)

    if backend == PlotBackend.mpl:
        get_mpl_help(key)
    elif backend == PlotBackend.bokeh:
        get_bokeh_help(key)
    else:
        raise NotImplementedError

def get_plotter(backend=None):
    import masci_tools.vis.plot_methods as mpl
    import masci_tools.vis.bokeh_plots as bok

    backend = PlotBackend.from_str(backend)

    if backend == PlotBackend.mpl:
        return mpl.plot_params
    elif backend == PlotBackend.bokeh:
        return bok.plot_params
    else:
        raise NotImplementedError

def dos(*args, backend=None, **kwargs):
    """

    """
    from .plot_methods import plot_dos
    from .bokeh_plots import bokeh_dos

    plot_funcs = {PlotBackend.mpl: plot_dos,
                  PlotBackend.bokeh: bokeh_dos}

    backend = PlotBackend.from_str(backend)

    return plot_funcs[backend](*args, **kwargs)

def spinpol_dos(*args, backend=None, **kwargs):
    """

    """
    from .plot_methods import plot_spinpol_dos
    from .bokeh_plots import bokeh_spinpol_dos

    plot_funcs = {PlotBackend.mpl: plot_spinpol_dos,
                  PlotBackend.bokeh: bokeh_spinpol_dos}

    backend = PlotBackend.from_str(backend)

    return plot_funcs[backend](*args, **kwargs)

def bands(*args, backend=None, **kwargs):
    """

    """
    from .plot_methods import plot_bands
    from .bokeh_plots import bokeh_bands

    plot_funcs = {PlotBackend.mpl: plot_bands,
                  PlotBackend.bokeh: bokeh_bands}

    backend = PlotBackend.from_str(backend)

    return plot_funcs[backend](*args, **kwargs)

def spinpol_bands(*args, backend=None, **kwargs):
    """

    """
    from .plot_methods import plot_spinpol_bands
    from .bokeh_plots import bokeh_spinpol_bands

    plot_funcs = {PlotBackend.mpl: plot_spinpol_bands,
                  PlotBackend.bokeh: bokeh_spinpol_bands}

    backend = PlotBackend.from_str(backend)

    return plot_funcs[backend](*args, **kwargs)

def single_scatter(*args, backend=None, **kwargs):
    """

    """
    from .plot_methods import single_scatterplot
    from .bokeh_plots import bokeh_scatter

    plot_funcs = {PlotBackend.mpl: single_scatterplot
                  PlotBackend.bokeh: bokeh_scatter}

    backend = PlotBackend.from_str(backend)

    return plot_funcs[backend](*args, **kwargs)



