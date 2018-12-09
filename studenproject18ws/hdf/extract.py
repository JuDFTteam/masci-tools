# -*- coding: utf-8 -*-
"""Holds the main class of this module, the Extractor, a generic HDF file reader. See it's docstring.

Notes
=====
Benefit of all this:
- together, the Extractor, Extract Configs and Transform classes become a utility that can  be reused
  for any kind of hdf5 file readout (extraction-transform-load). For different applications, a new
  extract config (a dict) can be added or passed in to the extractor. Same goes for the Transform class
  that holds the transform functions: if needed, derive a new one.
- benefit of the namedtupple as data output over directly using the dict: autompletion, refactoring
  works (in an IDE), no input clutter.
"""
import inspect
import logging
import ntpath
import os
from collections import namedtuple
from enum import Enum

import h5py
from h5py._hl.dataset import Dataset

from studenproject18ws.hdf.config import Extract
from studenproject18ws.hdf.exceptions import Hdf5_DatasetNotFoundError
from studenproject18ws.hdf.transform import Transform, TransformBands


class Extractor(object):
    """Generic Reader class for HDF5 files following the Extract-Transform-Load (ETL) approach.

    Idea: reader receives:
    - A h5 file
    - An 'Extract Config': a dict with one enttry per h5 dataset
    - An Transform class: holding functions to be applied to the datasets
    Return a data object that holds all transformed datasets as attributes.

    Benefits:
    - clearly defined Extract Configs for different application cases, reuse infrastructure
    - reusable (base class) and extendable (derived class) Transform functions

    Examples
    --------
    Extract a band structure. (tested with doctest: passed)

    >>> from studenproject18ws.hdf.config import Extract
    >>> from studenproject18ws.hdf.transform import TransformBands
    >>> from studenproject18ws.hdf.extract import Extractor
    >>>
    >>> # filename = 'banddos_4x4.hdf'
    >>> # filename = 'banddos.hdf'
    >>> filename = 'banddos_Co.hdf'
    >>>
    >>> filepath = ['..', 'data', 'input', filename]
    >>> filepath = os.path.join(*filepath)
    >>>
    >>> data = None
    >>> extractor = Extractor(filepath=filepath)
    >>> with extractor as h5file:
    ...    data = extractor.get(extract=Extract.Bands, transform=TransformBands)
    ...    #
    ...    # Note:
    ...    # Inside the with statement (context manager),
    ...    # all HDF5 datasets are available. When the statement is left,
    ...    # the HDF5 file gets closed and the datasets are closed.
    ...    # Should they be left available, apply Transform.to_memory to them.
    ...    #
    ...    print(len(data.k_distances))
    500
    >>> # Left HDF5 file with statement: file and all open datasets are now closed.
    >>> print(len(extractor.transformer.k_points))
    500

    Notes
    -----


    TODO
    ====
    - For return type, use a Metaclass instead of namedtuple. That way, could reuse input extract dict
      for the output's attributes, AND add functions to the new class for further processing, like weight
      functions needed for the bands plotting. These could also be stored per application base. If that
      could be achieved, the ETL terminology would have to be shifted: current 'Transform' functions would
      be relabeled 'Extract' functions, and the further-processing functions would become the new 'Transform'
      functions. Right now, those have to live decoupled from this module, which I think is worse.
      Example from [1]: Foo = type('Foo',(FooBase,),{'some_attr': 100,'some_func': func})

    References
    ----------
        .. [1] Real Python. Python Metaclasses.
           URL: https://realpython.com/python-metaclasses/#defining-a-class-dynamically
    """

    def __init__(self, filepath):
        """

        :param filepath: relative or absolute filepath
        :type filepath: str
        """
        self._f_path = filepath
        self.filename = ntpath.basename(filepath)
        self.filename = os.path.splitext(self.filename)[0]
        self.transformer = None

    def __enter__(self):
        # trysetattr etc goes here
        self._f = h5py.File(self._f_path, 'r')
        return self._f

    def __exit__(self, type, value, traceback):
        # exception handling goes here
        self._f.close()

    def _dataset(self, h5path, strict=False):
        """

        Parameters
        ----------
        h5path : str
            HDF5 group path in file.
        strict : bool
            If no dataset at h5path: True: return None, False: raise error

        Returns
        -------
        Dataset
            h5py.Dataset or None

        Raises
        ------
        Hdf2Mic_HDF5DatasetNotFoundError
            if file has no such Dataset
        """
        if h5path == '/' or h5path == '':
            if strict:
                return None
            else:
                pass

        dset = self._f.get(h5path)
        if dset is not None:
            return dset
        elif not strict:
            raise Hdf5_DatasetNotFoundError('ERROR: HDF5 input file {} has no Dataset at {}. Aborting.'
                                            .format(self._f.filename, h5path))
        return None

    def get(self, extract: dict, transform=Transform, logging_level=logging.WARN):
        """Extracts datasets from HDF5 file, transforms them and puts all into a namedtuple.

        :param extract: dict conforming to the prescribed format
        :type extract: dict
        :param  transform: class or instance that does the transforms.
        :param logging_level: tell function how much info to print. Default: only warnings and errors.
        :return: data namedtuple with named, transformed datasets as attributes
        """
        logging.basicConfig(level=logging_level)
        if (inspect.isclass(transform)):
            # create instance
            self.transformer = transform()
        else:
            # use instance
            self.transformer = transform
        # assert that transformer is derived from correct base class
        assert (isinstance(self.transformer, Transform))

        # TODO: check dict format: in isolation, or in combination with readout (faster)

        # remove entries whose key is an empty string
        extract = {key: val for key, val in extract.items() if key}

        dataset_names = list(extract.keys())  # not equal to HDF5 Dataset names (last part of h5path)!

        # get h5 datasets
        h5paths = [item['h5path'] for item in list(extract.values())]
        datasets = list(map(lambda h5path: self._dataset(h5path, strict=True), h5paths))
        logging.info("Loaded datasets.")

        # # get Transform function names and/or arguments
        # # But some prep work is needed. A transform entry is optional. Since I put everything from
        # # the extract dictionary into separate lists, I rely on those list entries to be index-matched.
        # # So first must check if there are fewer transform items than dataset items. In that case must
        # # insert dummy entries at the appripriate spots.
        # # The dummy item is the Transform base class's identity function. This is needed because even
        # # if no transformation if performed, every dataset must be checked if it is a dependee, and every
        # # function runs that check, even identity.
        # # If the same length would be guaranteed:
        # transforms = [item['transforms'] for item in list(extract.values())] # if same length would be guaranteed
        # # But instead, we have to build the list manually:
        transforms = []
        index_check_count = 0
        for key, value in extract.items():
            if not key == dataset_names[index_check_count]:
                msg = f"Transforms list has different order than other lists derived from extract dict. " \
                      f"Abort. Cannot guarantee correct behavior anymore. Contact and send error developer."
                logging.error(msg)
                raise ValueError(msg)
            if not value.get('transforms'):
                value['transforms'] = [Transform.id]
            elif not value['transforms']:  # empty list or similar
                value['transforms'] = [Transform.id]
            elif not isinstance(value['transforms'], list):  # e.g. one fct, but not in a list
                value['transforms'] = [value['transforms']]  # do check if valid ref to Transform fct later
            transforms.append(value['transforms'])
            index_check_count += 1

        # if a transform fct name was supplied as fct object Transform.foo,
        # instead of Transform.foo.__name__, or "foo" (equivalent), turn it into a string.
        # This is a bit dumb, since in the end want the function objects again.
        # But in the interim, need the function names for dependency checking. And it's not that expensive.
        for i, tf_group in enumerate(transforms):
            for j, tf_unit in enumerate(tf_group):
                if isinstance(tf_unit, list):  # i.e. a transform fct name plus arguments
                    transforms[i][j][0] = tf_unit[0].__name__ if callable(tf_unit[0]) else tf_unit[0]
                else:  # just a transform function name
                    transforms[i][j] = tf_unit.__name__ if callable(tf_unit) else tf_unit

        # TODO: pre-check: is there is a transform dependency that cannot be satisfied?
        # this is the case if there is a dependee dataset that's not in the list of read-in datasets.
        # But the check must not include all dependencies listed in Transform, but only those that
        # are going to be used. That means those, whose respective Transform functions are actually
        # going to be called.
        transform_names_set = set(
            [item for sublist in  # flattens list of lists
             [[tf[0] if isinstance(tf, list) else tf for tf in tfsub]  # get tf name, discard tf arg names
              for tfsub in transforms]  # for each dataset's list of transforms
             for item in sublist]  # flattens list of list
        )

        dataset_names_set = set(dataset_names)
        differences = {}
        for transform_name, dependees in self.transformer.DEPENDENCIES.items():
            if transform_name in transform_names_set:
                difference = set(dependees) - dataset_names_set
                if difference:
                    differences[transform_name] = difference
        if differences:
            raise ValueError(f"Cannot extract & transform data: the input dictionary specifies transforms "
                             f"with unmet dependencies (needed datasets not specified in the extract): \n"
                             f"{differences}")

        # now loop over the datasets until all are transformed. First do those
        # with no Transform dependencies, skip those with dependencies. Then
        # do the latter ones until all dependencies are satisifed.
        transformed = set()
        i = 0
        logging.debug("Transforming datasets: ------------------------------------------------")
        while (len(transformed) < len(datasets)):
            logging.debug(f"i = {i}, dataset = '{dataset_names[i]}', h5path = '{h5paths[i]}',"
                          f" transform = '{transforms[i]}':")
            if (datasets[i] is None):
                logging.debug(f"\tdataset '{dataset_names[i]}' does not exist, pass.")
                transformed.add(dataset_names[i])
            if (dataset_names[i] in transformed):
                logging.debug(f"\tdataset '{dataset_names[i]}'' is already transformed, continue.")
            else:
                difference = []  # list of dependee datasets for transformations
                logging.debug("\tcheck dependencies:")
                for transform in transforms[i]:
                    # extract transform function names list (in case one of them has args and this is list)
                    transform_name = transform[0] if isinstance(transform, list) else transform
                    logging.debug(f"\t\tfor transform_function: '{transform_name}'")
                    if (transform_name in self.transformer.DEPENDENCIES.keys()):
                        # now have to check: is the dependency resolved?
                        # I.e. are all dependee-datasets already transformed.
                        dependees = self.transformer.DEPENDENCIES[transform_name]  # list
                        if set(dependees).issubset(transformed):
                            pass
                        else:
                            difference.extend(set(dependees) - transformed)
                            logging.debug(
                                f"\tis dependent on untransformed datasets {difference}, try next dataset first")
                            break
                if (not difference):
                    logging.debug("\tnot dependent or all dependencies satisfied, transform:")
                    for transform in transforms[i]:
                        transform_name = transform
                        transform_args = [dataset_names[i], datasets[i]]
                        if isinstance(transform, list):
                            transform_name = transform[0]
                            # in case there are enum arguments, convert them to  string for uniform processing
                            args_additional = transform[1:]
                            logging.debug(f"args_additional before: {args_additional}")
                            args_additional = [arg.name if isinstance(arg, Enum) else arg for arg in args_additional]
                            logging.debug(f"args_additional after: {args_additional}")
                            transform_args.extend(args_additional)
                        transform_function = getattr(self.transformer, transform_name)
                        logging.debug(f"\t\ttransform_function: '{transform_name}', transform_args: '{transform_args}'")
                        datasets[i] = transform_function(*transform_args)
                        transformed.add(dataset_names[i])
                    logging.debug(f"\ttransformed dataset '{dataset_names[i]}'.")
            i = (i + 1) % len(datasets)
        logging.info("transformed datasets.")

        # creaet namedtyple type, values will be the transformed datasets
        Data = namedtuple('Data', dataset_names)
        logging.debug(f"dsets: len = {len(datasets)}, attr_names = {dataset_names}")
        data = Data(*datasets)
        return data


if __name__ == '__main__':
    pass