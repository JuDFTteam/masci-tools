.. _hdf5_parser:

General ``HDF5`` file reader
+++++++++++++++++++++++++++++

Fleur uses the HDF5 library for output files containing large datasets. The masci-tools library provides the :py:class:`~masci_tools.io.parsers.hdf5.reader.HDF5Reader` class to extract and transform information from these files. The ``h5py`` library is used to get information from ``.hdf`` files

Basic Usage
------------

The specifications of what to extract and how to transform the data are given in the form of a python dictionary. Let us look at a usage example; extracting data for a bandstructure calculation from the ``banddos.hdf`` file produced by Fleur.

.. code-block:: python

   from masci_tools.io.parsers.hdf5 import HDF5Reader
   from masci_tools.io.parsers.hdf5.recipes import FleurBands

   #The HDF5Reader is used with a contextmanager to safely handle
   #opening/closing the h5py.File object that is produced to extract information
   with HDF5Reader('/path/to/banddos.hdf') as h5reader:
      datasets, attributes = h5reader.read(recipe=FleurBands)

The method :py:meth:`~masci_tools.io.parsers.hdf5.reader.HDF5Reader.read` produces two python dictionaries. In the case of the ``FleurBands`` recipe these contain the following information.

   - `datasets`
      - Eigenvalues converted to eV shited to ``E_F=0`` (if available in the ``banddos.hdf``) and split up into spin-up/down and flattened to one dimension
      - The kpath projected to 1D and reshaped to same length as weights/eigenvalues
      - The weights (flattened) of the interstitial region, each atom, each orbital on each atom for all eigenvalues
   - `attributes`
      - The coordinates of the used kpoints
      - Positions, atomic symbols and indices of symmetry equivalent atoms
      - Dimensions of eigenvalues (``nkpts`` and ``nbands``)
      - Bravais matrix/Reciprocal cell of the system
      - Indices and labels of special k-points
      - Fermi energy
      - Number of spins in the calculation

The following pre-defined recipes are stored in :py:mod:`~masci_tools.io.parsers.hdf5.recipes`:

   - Recipe for ``banddos.hdf`` for bandstructure calculations
   - Recipe for ``banddos.hdf`` for standard density of states calculations
   - Different DOS modes are also supported (``jDOS``, ``orbcomp``, ``mcd``)

If no recipe is provided to the :py:class:`~masci_tools.io.parsers.hdf5.reader.HDF5Reader`, it will create the ``datasets`` and ``attributes`` as two nested dictionaries, exactly mirroring the structure of the ``.hdf`` file and converting datasets into numpy arrays.

For big datasets it might be useful to keep the dataset as a reference to the file and not load the
dataset into memory. To achieve this you can pass ``move_to_memory=False``, when initializing the reader.
Notice that most of the transformations will still implicitly create numpy arrays and after the hdf file is closed the datasets will no longer be available.

Structure of recipes for the :py:class:`~masci_tools.io.parsers.hdf5.reader.HDF5Reader`
-------------------------------------------------------------------------------------------

The recipe for extracting bandstructure information form the ``banddos.hdf`` looks like this:

.. literalinclude:: ../../../masci_tools/io/parsers/hdf5/recipes.py
   :language: python
   :lines: 161-291
   :linenos:

Each recipe can define the `datasets` and `attributes` entry (if one is not defined, a empty dict is returned in its place). Each entry in these sections has the same strucuture.

.. code-block:: python

   #Example entry from the FleurBands recipe

   'fermi_energy': {
            'h5path':
            '/general',
            'description':
            'fermi_energy of the system',
            'transforms': [
                Transformation(name='get_attribute', args=('lastFermiEnergy',), kwargs={}),
                Transformation(name='get_first_element', args=(), kwargs={})
            ]
        }

All entries must define the key ``h5path``. This gives the initial dataset for this key, which will be extracted from the given ``.hdf`` file. The key of the entry corresponds to the key under which the result will be saved to the output dictionary.

If the dataset should be transformed in some way after reading it, there are a number of defined transformations in :py:mod:`~masci_tools.io.parsers.hdf5.transforms`. These are added to an entry by adding a list of namedtuples (:py:class:`~masci_tools.io.parsers.hdf5.reader.Transformation` for general transformations; :py:class:`~masci_tools.io.parsers.hdf5.reader.AttribTransformation` for attribute transformations) under the key ``transforms``. General Transformations can be used in all entries, while transformations using an attribute value can only be used in the ``datasets`` entries. Each namedtuple takes the ``name`` of the transformation function and the positional (``args``), and keyword arguments (``kwargs``) for the transformation. Attribute transformations also take the name of the attribute, whose value should be passed to the transformation in ``attrib_name``.

At the moment the following transformation functions are pre-defined:

General Transformations:
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.get_first_element()`: Get the index ``0`` of the dataset
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.index_dataset()`: Get the index ``index`` of the dataset
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.slice_dataset()`: Slice the given dataset with the given argument
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.get_shape()`: Get the shape of the dataset
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.tile_array()`: Use np.tile to repeat dataset a given amount of times
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.repeat_array()`: Use np.repeat to repeat each element in the dataset a given amount of times
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.get_all_child_datasets()`: extract all datasets contained in the current hdf group and enter them into a dict
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.shift_dataset()`: Shift the given dataset with a scalar value
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.multiply_scalar()`: Multiply the given dataset with a scalar value
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.multiply_array()`: Mutiply the given dataset with a given array
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.convert_to_complex_array()`: Convert real dataset to complex array
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.calculate_norm()`: Calculate norm of list of vectors (either absolute or difference between subsequent entries)
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.cumulative_sum()`: Calculative cumulative sum of dataset
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.get_attribute()`: Get the value of one given attribute on the dataset
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.attributes()`: Get all defined attributes on the dataset as a dict
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.move_to_memory()`: Convert dataset to numpy array (if not already done implicitly)
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.flatten_array()`: Create copy of dataset flattened into one dimension
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.split_array()`: Split the given dataset along its first index and store result in a dictionary with keys with suffixes
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.convert_to_str()`: Convert datatype of dataset to string
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.periodic_elements()`: Convert atomic numbers to their atomic symbols

Transformations using an attribute:
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.multiply_by_attribute()`: Multiply dataset by value of attribute (both scalar and matrix)
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.shift_by_attribute()`: Shift the given dataset with the value of an attribute
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.repeat_array_by_attribute()`: Call :py:func:`~masci_tools.io.parsers.hdf5.transforms.repeat_array()` with the value of an attribute as argument
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.tile_array_by_attribute()`: Call :py:func:`~masci_tools.io.parsers.hdf5.transforms.tile_array()` with the value of an attribute as argument
   - :py:func:`~masci_tools.io.parsers.hdf5.transforms.add_partial_sums()`: Sum over entries in dictionary datasets with given patterns in the key (Pattern is formatted with given attribute value)

Custom transformation functions can also be defined using the :py:func:`~masci_tools.io.parsers.hdf5.transforms.hdf5_transformation()` decorator. For some transformation, e.g. :py:func:`~masci_tools.io.parsers.hdf5.transforms.get_all_child_datasets()`, the result will be a subdictionary in the ``datasets`` or ``attributes`` dictionary. If this is not desired the entry can include ``'unpack_dict': True``. With this all keys from the resulting dict will be extracted after all transformations and put into the root dictionary.
