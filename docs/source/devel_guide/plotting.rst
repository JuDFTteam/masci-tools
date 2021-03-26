.. _devguideplotting:

Using the :py:class:`~masci_tools.vis.Plotter` class
++++++++++++++++++++++++++++++++++++++++++++++++++++

Description
------------

The :py:class:`~masci_tools.vis.Plotter` class aims to provide a framework, which can be used to handle default values and collect common codeblocks needed for different plotting frameworks.

The :py:class:`~masci_tools.vis.Plotter` class is a base class that should be subclassed for different Plotting backends. See :py:class:`~masci_tools.vis.matplotlib_plotter.MatplotlibPlotter` or :py:class:`~masci_tools.vis.bokeh_plotter.BokehPlotter` for examples. The Subclass provides a dictionary of all the keys that should be handled by the plotter class. The Plotter class provides a hierachy of overwriting these parameters (Higher numbers take precedence).

   1. Function defaults set with :py:meth:`~masci_tools.vis.Plotter.set_defaults()` with ``default_type='function'``
   2. Global defaults set with :py:meth:`~masci_tools.vis.Plotter.set_defaults()`
   3. Parameters set with :py:meth:`~masci_tools.vis.Plotter.set_parameters()`

The subclasses should then also provide the plotting backend specific useful code snippets. For example showing colorbars, legends, and so on ...

For a list of these functions you can look at the respective documentation (:py:class:`~masci_tools.vis.matplotlib_plotter.MatplotlibPlotter` or :py:class:`~masci_tools.vis.bokeh_plotter.BokehPlotter`)

Writing a plotting function
----------------------------

In the following we will go through a few examples of how to write a simple plotting function using the :py:class:`~masci_tools.vis.Plotter` class. We will be focusing on the :py:class:`~masci_tools.vis.matplotlib_plotter.MatplotlibPlotter`, but all of this is very similar for other plotting backends.

Local instance
^^^^^^^^^^^^^^^

Even though the :py:class:`~masci_tools.vis.Plotter` class is meant to be used globally or on the module level, it can also be useful locally for simplifying simple plotting scripts. Here we have a example of a function producing a single plot with the given data for the x and y coordinates.

.. code-block:: python

   def plot_with_defaults(x,y,**kwargs):
      from masci_tools.vis.matplotlib_plotter import MatplotlibPlotter

      #First we instantiate the MatplotlibPlotter class
      plot_params = MatplotlibPlotter()

      #Now we process the given arguments
      plot_params.set_parameters(**kwargs)

      #Set up the axis, on which to plot the data
      ax = plot_params.prepare_plot(xlabel='X', ylabel='Y', title='Single Scatterplot')

      #The plot_kwargs provides a way to get the keyword arguments for the
      #actual plotting call to `plot` in this case.
      plot_kwargs = plot_params.plot_kwargs()

      ax.plot(x, y, **plot_kwargs)

      #The MatplotlibPlotter has a lot of small helper functions
      #In this case we just want to set the limits and scale of the
      #axis if they were given
      plot_params.set_scale(ax)
      plot_params.set_limits(ax)

      return ax

   import numpy as np

   x = np.linspace(-1, 1, 10)
   y = x**2

   #Some examples
   plot_with_defaults(x, y)
   plot_with_defaults(x, y, limits={'x': (0,1)})
   plot_with_defaults(x, y, marker='s', markersize=20)

Global/Module level instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The local instance already gives us reusable code snippets to avoid common pitfalls when doing matplotlib/bokeh plots. But when instantiating the :py:class:`~masci_tools.vis.Plotter` class locally we have no way of letting the user modify the global defaults.

However, when handling global state we need to be careful to not leave the instance of the :py:class:`~masci_tools.vis.Plotter` class in an inconsistent state. If an error is thrown inside the plotting routine the parameters would stay set and may lead to very unexpected results. For this reason every plotting function using a global or module level instance of these plotters should be decorated with the :py:func:`~masci_tools.vis.ensure_plotter_consistency()` decorator. This does two  things:

   1. If an error occurs in the decorated function the parameters will be reset before the error is raised
   2. It makes sure that nothing inside the plotting routine changed the user defined defaults

Let us take the previous example and convert it to use a global instance

.. code-block:: python

   from masci_tools.vis.matplotlib_plotter import MatplotlibPlotter
   from masci_tools.vis import ensure_plotter_consistency

   #First we instantiate the MatplotlibPlotter class
   plot_params = MatplotlibPlotter()

   #The decorator needs to get the plotter object
   #that is used inside the function
   @ensure_plotter_consistency(plot_params)
   def plot_with_defaults(x,y,**kwargs):

      #Now we process the given arguments
      plot_params.set_parameters(**kwargs)

      #Set up the axis, on which to plot the data
      ax = plot_params.prepare_plot(xlabel='X', ylabel='Y', title='Single Scatterplot')

      #The plot_kwargs provides a way to get the keyword arguments for the
      #actual plotting call to `plot` in this case.
      plot_kwargs = plot_params.plot_kwargs()

      ax.plot(x, y, **plot_kwargs)

      #The MatplotlibPlotter has a lot of small helper functions
      #In this case we just want to set the limits and scale of the
      #axis if they were given
      plot_params.set_scale(ax)
      plot_params.set_limits(ax)

      return ax

   import numpy as np

   x = np.linspace(-1, 1, 10)
   y = x**2

   #Some examples
   plot_with_defaults(x, y)
   plot_params.set_defaults(marker='s', markersize=20)
   plot_with_defaults(x, y, limits={'x': (0,1)})
   plot_with_defaults(x, y)

The :py:meth:`masci_tools.vis.Plotter.set_defaults()` method is exposed in the two main modules for plotting :py:mod:`masci_tools.vis.plot_methods` :py:mod:`masci_tools.vis.bokeh_plots` as the functions :py:func:`masci_tools.vis.plot_methods.set_mpl_plot_defaults()` and  :py:func:`masci_tools.vis.bokeh_plots.set_bokeh_plot_defaults()` specific to the plotter instance that is used in these modules.

Function defaults
^^^^^^^^^^^^^^^^^^

Some functions may want to set function specific defaults, that make sense inside the function, but may not be useful globally. The following example sets the default ``linewidth`` for our function to ``6``.

.. note::
   Function defaults are also reset by the :py:func:`~masci_tools.vis.ensure_plotter_consistency()` decorator, when the plotting function terminates successfully or in an error

.. code-block:: python

   from masci_tools.vis.matplotlib_plotter import MatplotlibPlotter
   from masci_tools.vis import ensure_plotter_consistency

   #First we instantiate the MatplotlibPlotter class
   plot_params = MatplotlibPlotter()

   #The decorator needs to get the plotter object
   #that is used inside the function
   @ensure_plotter_consistency(plot_params)
   def plot_with_defaults(x,y,**kwargs):

      #Set the function defaults
      plot_params.set_defaults(default_type='function', linewidth=6)

      #Now we process the given arguments
      plot_params.set_parameters(**kwargs)

      #Set up the axis, on which to plot the data
      ax = plot_params.prepare_plot(xlabel='X', ylabel='Y', title='Single Scatterplot')

      #The plot_kwargs provides a way to get the keyword arguments for the
      #actual plotting call to `plot` in this case.
      plot_kwargs = plot_params.plot_kwargs()

      ax.plot(x, y, **plot_kwargs)

      #The MatplotlibPlotter has a lot of small helper functions
      #In this case we just want to set the limits and scale of the
      #axis if they were given
      plot_params.set_scale(ax)
      plot_params.set_limits(ax)

      return ax

   import numpy as np

   x = np.linspace(-1, 1, 10)
   y = x**2

   #Some examples
   plot_with_defaults(x, y)
   plot_params.set_defaults(marker='s', markersize=20)
   plot_with_defaults(x, y, limits={'x': (0,1)})
   plot_with_defaults(x, y)


Passing keyword arguments directly to plot calls
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The plotter classes have a restricted set of keys that they recognize as valid parameters. This set is of course not complete, since there is a vast number of parameters you can set for all plotting backends. In our previous examples unknown keys will immediately lead to an error in the call to :py:meth:`~masci_tools.vis.Plotter.set_parameters()`. To enable this functionality we can provide the ``continue_on_error=True`` as an argument to this method.

Then the unknown keys are ignored and are returned in a dictionary. Additionally you can explicitly bypass the plotter object if you provide arguments in a dictionary with the name ``extra_kwargs`` it will be ignored, unpacked and returned along with the unknown keys

.. warning::
   Be careful with the this feature and especially the ``extra_kwargs``, since there is no check for name clashes with this argument. You might also run into situations, where arguments of different names collide with arguments provided by the :py:class:`~masci_tools.vis.Plotter`

.. code-block:: python

   from masci_tools.vis.matplotlib_plotter import MatplotlibPlotter
   from masci_tools.vis import ensure_plotter_consistency

   #First we instantiate the MatplotlibPlotter class
   plot_params = MatplotlibPlotter()

   #The decorator needs to get the plotter object
   #that is used inside the function
   @ensure_plotter_consistency(plot_params)
   def plot_with_defaults(x,y,**kwargs):

      #Set the function defaults
      plot_params.set_defaults(default_type='function', linewidth=6)

      #Now we process the given arguments (unknown ones are returned)
      kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)

      #Set up the axis, on which to plot the data
      ax = plot_params.prepare_plot(xlabel='X', ylabel='Y', title='Single Scatterplot')

      #The plot_kwargs provides a way to get the keyword arguments for the
      #actual plotting call to `plot` in this case.
      plot_kwargs = plot_params.plot_kwargs()

      ax.plot(x, y, **plot_kwargs, **kwargs)

      #The MatplotlibPlotter has a lot of small helper functions
      #In this case we just want to set the limits and scale of the
      #axis if they were given
      plot_params.set_scale(ax)
      plot_params.set_limits(ax)

      return ax

   import numpy as np

   x = np.linspace(-1, 1, 10)
   y = x**2

   #The key markerfacecolor is not known to the MatplotlibPlotter
   plot_with_defaults(x, y, markerfacecolor='red', markersize=20)

Multiple plotting calls
^^^^^^^^^^^^^^^^^^^^^^^^

The plotter classes also provide support for multiple plotting calls with different data sets in a single plotting function. To enable this feature we need to set two properties on the :py:class:`masci_tools.vis.Plotter`; ``single_plot`` to `False`` and ``num_plots`` to the number of plot calls made in this function. The plot specific parameters can then be specified in two ways. Shown behind the two ways is the way to set the color of the second data set to ``red``.

   1. List of values (``None`` for unspecified values) ``[None,'red']``
   2. Dict with integer indices for the specified values ``{1: 'red'}``

Unspecified values are replaced with the previously set defaults.

.. note::
   The ``num_plots`` and ``single_plot`` properties are also reset by the :py:func:`~masci_tools.vis.ensure_plotter_consistency()`

.. code-block:: python

   from masci_tools.vis.matplotlib_plotter import MatplotlibPlotter
   from masci_tools.vis import ensure_plotter_consistency

   #First we instantiate the MatplotlibPlotter class
   plot_params = MatplotlibPlotter()

   #The decorator needs to get the plotter object
   #that is used inside the function
   @ensure_plotter_consistency(plot_params)
   def plot_2lines_with_defaults(x,y,**kwargs):

      plot_params.single_plot = False
      plot_params.num_plots = 2

      #Set the function defaults
      plot_params.set_defaults(default_type='function', linewidth=6)

      #Now we process the given arguments (unknown ones are returned)
      kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)

      #Set up the axis, on which to plot the data
      ax = plot_params.prepare_plot(xlabel='X', ylabel='Y', title='Single Scatterplot')

      #The plot_kwargs provides a way to get the keyword arguments for the
      #actual plotting call to `plot` in this case.
      #For multiple plots this will be a list of dicts
      #of length `num_plots`
      plot_kwargs = plot_params.plot_kwargs()

      ax.plot(x[0], y[0], **plot_kwargs[0], **kwargs)
      ax.plot(x[1], y[1], **plot_kwargs[1], **kwargs)

      #The MatplotlibPlotter has a lot of small helper functions
      #In this case we just want to set the limits and scale of the
      #axis if they were given
      plot_params.set_scale(ax)
      plot_params.set_limits(ax)

      return ax

   import numpy as np

   x = np.linspace(-1, 1, 10)
   y = x**2
   y2 = x**3

   #The key markerfacecolor is not known to the MatplotlibPlotter
   plot_2lines_with_defaults([x,x], [y,y2])
   plot_2lines_with_defaults([x,x], [y,y2],
                             color={1:'red'}, linestyle=['--',None])

Custom function specific parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You might have situations, where you want to have some function specific parameters, that should pull from the previously set defaults or even a custom default value.

The :py:meth:`~masci_tools.vis.Plotter.add_parameter()` method is implemented exactly for this purpose. It creates a new key to be handled by the plotter class and with the arguments ``default_from`` or ``default_value`` we can specify what the defaults should be. ``default_value`` sets a specific value, ``default_from`` specifies a key from the plotter class from which to take the default value.

The :py:meth:`~masci_tools.vis.matplotlib_plotter.MatplotlibPlotter.plot_kwargs()` method then can take keyword arguments to replace the arguments to take with your custom parameters

.. note::
   These added parameters live on the function defaults and parameters level, meaning they will be removed by the :py:func:`~masci_tools.vis.ensure_plotter_consistency()` decorator after the function finishes

.. code-block:: python

   from masci_tools.vis.matplotlib_plotter import MatplotlibPlotter
   from masci_tools.vis import ensure_plotter_consistency

   #First we instantiate the MatplotlibPlotter class
   plot_params = MatplotlibPlotter()

   #The decorator needs to get the plotter object
   #that is used inside the function
   @ensure_plotter_consistency(plot_params)
   def plot_shifted_with_defaults(x,y,**kwargs):

      #Set the function defaults
      plot_params.set_defaults(default_type='function', linewidth=6)

      plot_params.add_parameter('linestyle_shifted',
                                default_from='linestyle')

      #Now we process the given arguments (unknown ones are returned)
      kwargs = plot_params.set_parameters(continue_on_error=True, **kwargs)

      #Set up the axis, on which to plot the data
      ax = plot_params.prepare_plot(xlabel='X', ylabel='Y', title='Single Scatterplot')

      #The plot_kwargs provides a way to get the keyword arguments for the
      #actual plotting call to `plot` in this case.
      plot_kwargs = plot_params.plot_kwargs()
      ax.plot(x, y, **plot_kwargs, **kwargs)

      #This call replaces the parameter linestyle with our custom
      #parameter linestyle_shifted
      plot_kwargs = plot_params.plot_kwargs(linestyle='linestyle_shifted')
      ax.plot(x, y+2, **plot_kwargs, **kwargs)

      #The MatplotlibPlotter has a lot of small helper functions
      #In this case we just want to set the limits and scale of the
      #axis if they were given
      plot_params.set_scale(ax)
      plot_params.set_limits(ax)

      return ax

   import numpy as np

   x = np.linspace(-1, 1, 10)
   y = x**2

   plot_shifted_with_defaults(x, y)
   plot_shifted_with_defaults(x, y, linestyle_shifted='--')


Nested plotting functions
^^^^^^^^^^^^^^^^^^^^^^^^^^

More complex plotting routines might want to call other plotting routines to simplify their structure. However, this has a side-effect when working with the :py:class:`~masci_tools.vis.Plotter` class and the :py:func:`~masci_tools.vis.ensure_plotter_consistency()` decorator. Since the decorator resets the parameters and function defaults after a plotting function has been called you lose everything that you might have modified in the enclosing plotting function.

If you do need access to these parameters after calling a nested plotting function the :py:func:`~masci_tools.vis.NestedPlotParameters()` contextmanager is implemented. It defines a local scope, in which a plotting function can change the parameters and function defaults. After exiting the local scope the parameters and function defaults are always in the same state as when the ``with`` block was entered (Even if an error is raised). The nested plotting function will also start with the state that was set before.

Usage is shown here:

.. code-block:: python

   from masci_tools.vis.matplotlib_plotter import MatplotlibPlotter
   from masci_tools.vis import ensure_plotter_consistency
   from masci_tools.vis import NestedPlotParameters


   #First we instantiate the MatplotlibPlotter class
   plot_params = MatplotlibPlotter()

   @ensure_plotter_consistency(plot_params)
   def nested_plot_function(x, y, **kwargs):

      plot_params.set_defaults(default_type='function',
                               linewidth=10, linestyle='--')

      #The contextmanager also needs a reference to the plotter object
      #to manage
      with NestedPlotParameters(plot_params):
         ax = plot_with_defaults(x,y,**kwargs)

      #Will plot with the above set defaults
      plot_kwargs = plot_params.plot_kwargs()
      ax.plot(x, y+2, **plot_kwargs)

   @ensure_plotter_consistency(plot_params)
   def plot_with_defaults(x,y,**kwargs):

      #Set the function defaults
      plot_params.set_defaults(default_type='function', linewidth=6)

      #Now we process the given arguments
      plot_params.set_parameters(**kwargs)

      #Set up the axis, on which to plot the data
      ax = plot_params.prepare_plot(xlabel='X', ylabel='Y', title='Single Scatterplot')

      #The plot_kwargs provides a way to get the keyword arguments for the
      #actual plotting call to `plot` in this case.
      plot_kwargs = plot_params.plot_kwargs()

      ax.plot(x, y, **plot_kwargs)

      #The MatplotlibPlotter has a lot of small helper functions
      #In this case we just want to set the limits and scale of the
      #axis if they were given
      plot_params.set_scale(ax)
      plot_params.set_limits(ax)

      return ax

   import numpy as np

   x = np.linspace(-1, 1, 10)
   y = x**2

   nested_plot_function(x, y)
   nested_plot_function(x, y, linewidth=1)
