.. _devguideplotdata:

Using the :py:class:`~masci_tools.vis.data.PlotData` class
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. _matplotlib: https://matplotlib.org/stable/index.html
.. _bokeh: https://docs.bokeh.org/en/latest/index.html

Description
------------

The :py:class:`~masci_tools.vis.data.PlotData` class simplifies supporting data to plotting functions in multiple ways, while keeping the plotting functions themselves simple and easy to understand.

The basic idea of :py:class:`~masci_tools.vis.data.PlotData` is to mimic the behaviour of the ``data`` argument in `matplotlib`_ or the ``source`` argument in `bokeh`_. Suppose we have our data for a plot in a dictionary ``d``, which has the keys ``x``, ``y1`` and ``y2``. If we now want to plot both ``y`` keys against ``x`` we can do this in the following way.

.. code-block::

   from masci_tools.vis.data import PlotData

   plot_data = PlotData(d, x='x', y=['y1', 'y2'])

   for entry, source in plot_data.items():
      #entry has the keys needed to get the data from the source
      #and source is the mapping to use

      print(entry.x, entry.y) #Yields x, y1 in the first loop and x, y2 in the second

      #Now we can plot the data
      #for example plt.plot(entry.x, entry.y, data=source)

The keys are automatically expanded to be of the same length, if this is possible. There are three iteration modes, with the same names as for dicts:

   - ``keys``: Yields ``namedtuple`` with the keys for each plot
   - ``values``: Yields ``namedtuple`` with the values corresponding to the keys for each plot
   - ``items``: Yields the ``keys`` and their corresponding mapping for each plot

All of these functions have an argument ``first``, which will only return the first element if it is given as ``True``.

.. note::
   The names ``x`` and ``y`` in the example above are completely arbitrary. The names for the columns and the fields on the ``namedtuple`` are determined by the keyword arguments given to :py:class:`~masci_tools.vis.data.PlotData` at initialization

.. note::
   At the moment the types of mappings accepted in the :py:class:`~masci_tools.vis.data.PlotData` class are limited to ``dict``, ``pd.DataFrame`` and ``ColumnDataSource`` (`bokeh`_) objects

Initializing :py:class:`~masci_tools.vis.data.PlotData` without a mapping
----------------------------------------------------------------------------------

Users might want to provide data directly as arrays. If this should be allowed, there is a function :py:func:`~masci_tools.vis.data.process_data_arguments()` to allow for this option. This function can either take a ``data`` argument with a mapping and the same keyword arguments as the :py:class:`~masci_tools.vis.data.PlotData`.

.. code-block::

   from masci_tools.vis.data import process_data_arguments

   plot_data = process_data_arguments(data=d, x='x', y=['y1','y2'])

Or you can provide the arrays directly without a ``data`` argument

.. code-block::

   from masci_tools.vis.data import process_data_arguments

   #x,y1,y2 are the actual arrays
   plot_data = process_data_arguments(x=x, y=[y1,y2])

If no ``data`` argument is given the keyword arguments are assumed to contain the data and they will be processed according to three rules:
   1. If the data is a multidimensional array (list of lists, etc.) and it is not forbidden by the given argument the first dimension of the array is iterated over and interpreted as separate entries (if the data was previously split up into multiple sets a length check is performed)
   2. If the data is a one-dimensional array and of a different length than the number of defined data sets it is added to all previously existing entries
   3. If the data is a one-dimensional array and of the same length as the number of defined data sets each entry is added to the corresponding data set

.. note::
   List or array in this context refers to ``list``, ``np.array`` and ``pd.Series``

Available routines on :py:class:`~masci_tools.vis.data.PlotData`
----------------------------------------------------------------------

There are a couple of routines for mutating/copyying or getting information about the data in a :py:class:`~masci_tools.vis.data.PlotData` instance. These are not meant to be used heavily and should be used for typical simple work done for plot data processing, i.e. scaling, shifting, getting limits, ...

.. note::
   The term data key in the following section refers to the keys of the keyword arguments given to :py:class:`~masci_tools.vis.data.PlotData` at initialization or the fields on the namedtuples returned by iterating over an instance

- :py:meth:`~masci_tools.vis.data.PlotData.get_keys()`: Get all the keys for a given data key in a list
- :py:meth:`~masci_tools.vis.data.PlotData.get_values()`: Get all the values for a given data key in a list
- :py:meth:`~masci_tools.vis.data.PlotData.min()`: Get the minimum value for a given data key. A mask can be passed to further select the data. If ``separate=True`` is passed a list of minimum values for each plot is returned
- :py:meth:`~masci_tools.vis.data.PlotData.max()`: Get the maximum value for a given data key. A mask can be passed to further select the data. If ``separate=True`` is passed a list of maximum values for each plot is returned
- :py:meth:`~masci_tools.vis.data.PlotData.apply()`: Apply a lambda function to transform the data of a given data key (in-place!!)
- :py:meth:`~masci_tools.vis.data.PlotData.get_function_result()`: Apply a function to a given data key and return the results (Does not change the data)
- :py:meth:`~masci_tools.vis.data.PlotData.sort_data()`: Sort the data by the given data keys
- :py:meth:`~masci_tools.vis.data.PlotData.group_data()`: Group the data by the given data keys
- :py:meth:`~masci_tools.vis.data.PlotData.shift_data()`: Shift the data of a given data key either globally or with different shifts for each plot
- :py:meth:`~masci_tools.vis.data.PlotData.copy_data()`: Copy data to a of one data key to a new data key
- :py:meth:`~masci_tools.vis.data.PlotData.distinct_datasets()`: Return how many different datasets exist for a given data key

.. warning::
   The methods :py:meth:`~masci_tools.vis.data.PlotData.sort_data()` and :py:meth:`~masci_tools.vis.data.PlotData.group_data()` will always convert the data sources to ``pd.DataFrame`` objects if they are not already.
