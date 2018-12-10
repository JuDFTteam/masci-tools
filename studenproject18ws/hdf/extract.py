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
import copy
import functools
import inspect
import logging
import ntpath
import os
import sys
from enum import Enum
from collections import OrderedDict

import h5py
from h5py._hl.dataset import Dataset

from studenproject18ws.hdf.config import Extract
from studenproject18ws.hdf.exceptions import Hdf5_DatasetNotFoundError
import studenproject18ws.hdf.load as load
from studenproject18ws.hdf.load import *
from studenproject18ws.hdf.transform import *


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
    ...    data = extractor.get(extract=Extract.Bands)
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

    def _str_to_type(self, type_name):
        """Returns type represeneted in string.

        Type must be loaded in current module.
        Example: A defined locally. "A.foo" will return fct A.foo. "A" will return class A.
        """
        a_type = None
        try:
            a_type = functools.reduce(getattr, type_name.split("."), sys.modules[__name__])
        except AttributeError:
            pass
        return a_type

    def _get_class(self, method):
        """py3-compatible version of getting a method's type.
        :return:
        """
        if inspect.ismethod(method):
            for cls in inspect.getmro(method.__self__.__class__):
                if cls.__dict__.get(method.__name__) is method:
                    return cls
            method = method.__func__  # fallback to __qualname__ parsing
        if inspect.isfunction(method):
            cls = getattr(inspect.getmodule(method),
                          method.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
            if isinstance(cls, type):
                return cls
        return getattr(method, '__objclass__', None)  # handle special descriptor objects

    def get(self, config: dict, logging_level=logging.WARN):
        """Extracts datasets from HDF5 file, transforms them and puts all into a namedtuple.

        :param config: dict conforming to the prescribed format
        :type config: dict
        :param logging_level: tell function how much info to print. Default: only warnings and errors.
        :return: dynamic Data class with transformed datasets as attributes and methods specified in config
        """
        logging.basicConfig(level=logging_level)

        extract = config['datasets']
        data_classes_functions_specified = config['data_classes_functions']

        # extract data output classes and functions. Will be needed at the end.




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
        transforms_class_instances = {}
        index_check_count = 0
        for key, value in extract.items():
            if not key == dataset_names[index_check_count]:
                msg = f"Transforms list has different order than other lists derived from extract dict. " \
                      f"Abort. Cannot guarantee correct behavior anymore. Contact and send error to developers."
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
        transforms_str = copy.deepcopy(transforms)
        transforms_func = copy.deepcopy(transforms)
        for i, tf_group in enumerate(transforms):
            for j, tf_unit in enumerate(tf_group):
                tf_func_name = ""
                tf_func = None
                if isinstance(tf_unit, list):  # i.e. a transform fct name plus arguments
                    # str:
                    if callable(tf_unit[0]):
                        tf_func_name = tf_unit[0].__name__
                        tf_func = tf_unit[0]
                    else:
                        tf_func_name = tf_unit[0]
                        tf_func = self._str_to_type(tf_unit[0])

                    transforms_func[i][j][0] = tf_func
                    transforms_str[i][j][0] = tf_func_name
                else:  # just a transform function name
                    if callable(tf_unit):
                        tf_func_name = tf_unit.__name__
                        tf_func = tf_unit
                    else:
                        tf_func_name = tf_unit
                        tf_func = self._str_to_type(tf_unit)

                    transforms_func[i][j] = tf_func
                    transforms_str[i][j] = tf_func_name
                # tf_func_name is of form "packageX.moduleY.TransformZ.foo". Split off last part and create instance
                # tf_func = self._str_to_type(tf_func_name)
                tf_cls = self._get_class(tf_func)
                if not tf_cls:
                    msg = f"Preprocessing of config failed: config specifies transform function '{tf_func_name}'. " \
                          f"The class specified has no such method, or the proper class cannot be inferred."
                    logging.error(msg)
                    raise AttributeError(msg)
                # tf_cls_name = ".".join(tf_func_name.split(".")[:-1]) # does not work
                tf_cls_name = tf_cls.__name__  # works


                # needed for call to getattr below, and addition to transforms_str:
                if "." in tf_func_name: # and probably .startswith(tf_cls_name)
                    tf_func_name = tf_func_name.split(".")[1]
                if isinstance(tf_unit, list):
                    transforms_str[i][j][0] = ".".join([tf_cls_name, tf_func_name])
                else:
                    transforms_str[i][j] = ".".join([tf_cls_name, tf_func_name])

                tf_cls_instance = tf_cls()
                tf_func_from_instance = getattr(tf_cls_instance, tf_func_name)
                if isinstance(tf_unit, list):
                    transforms_func[i][j][0] = tf_func_from_instance
                else:
                    transforms_func[i][j] = tf_func_from_instance

                if tf_cls_name not in transforms_class_instances:
                    transforms_class_instances[tf_cls] = tf_cls_instance
        # check
        transforms_base_cls = Transform  # hard-coded. Could instead use a common feature to find arbitrary base, like attribute DEPENDENCIES.
        for cls, instance in transforms_class_instances.items():
            if transforms_base_cls not in inspect.getmro(cls):
                msg = f"The hdf extract config contains transform functions whose class is not derived from " \
                      f"the Transform base class {transforms_base_cls}."
                logging.error(msg)
                raise TypeError(msg)
        if transforms_base_cls not in transforms_class_instances:
            transforms_class_instances[transforms_base_cls] = transforms_base_cls()
        self.transformer = transforms_class_instances[transforms_base_cls]
        print(f"transforms_base_class: {transforms_base_cls}")
        debug_break_point = 42

        # TODO: pre-check: is there is a transform dependency that cannot be satisfied?
        # this is the case if there is a dependee dataset that's not in the list of read-in datasets.
        # But the check must not include all dependencies listed in Transform, but only those that
        # are going to be used. That means those, whose respective Transform functions are actually
        # going to be called.
        transform_names_set = set(
            [item for sublist in  # flattens list of lists
             [[tf[0] if isinstance(tf, list) else tf for tf in tfsub]  # get tf name, discard tf arg names
              for tfsub in transforms_str]  # for each dataset's list of transforms
             for item in sublist]  # flattens list of list
        )
        dataset_names_set = set(dataset_names)
        differences = {}
        for transform_name, dependees in self.transformer.DEPENDENCIES.items():
            # first check that the class in transform_name 'X.foo' actually has a method 'foo'.
            for cls in transforms_class_instances.keys():
                if cls.__name__ == transform_name.split(".")[0]:
                    try:
                        getattr(transforms_class_instances[cls], transform_name.split(".")[1])
                    except AttributeError as dependencies_key_error:
                        logging.exception(f"Error in the Transform base dependencies keys: the method {transform_name} "
                                          f"does not exist.")
                        raise dependencies_key_error
            # okay, now check the dependencies themself (the datasets)
            if transform_name in transform_names_set:
                difference = set(dependees) - dataset_names_set
                if difference:
                    differences[transform_name] = difference
        if differences:
            msg = f"Cannot extract & transform data: the input dictionary specifies transforms with unmet " \
                  f"dependencies (needed datasets not specified in the extract): \n {differences}"
            logging.error(msg)
            raise ValueError(msg)

        # new approach: assume that there may transform functions from many different classes involved.
        # in hat case i cannot just check against one classe's DEPENDENCIES anymore.
        # instead, must

        # now loop over the datasets until all are transformed. First do those
        # with no Transform dependencies, skip those with dependencies. Then
        # do the latter ones until all dependencies are satisifed.
        transformed = set()
        i = 0
        logging.debug("Transforming datasets: ------------------------------------------------")
        while (len(transformed) < len(datasets)):
            logging.debug(f"i = {i}, dataset = '{dataset_names[i]}', h5path = '{h5paths[i]}',"
                          f" transform = '{transforms_str[i]}':")
            if (datasets[i] is None):
                logging.debug(f"\tdataset '{dataset_names[i]}' does not exist, pass.")
                transformed.add(dataset_names[i])
            if (dataset_names[i] in transformed):
                logging.debug(f"\tdataset '{dataset_names[i]}'' is already transformed, continue.")
            else:
                if (dataset_names[i] == 'bravaisMatrix'):
                    debug_break_point = 42
                    print(f"{dataset_names[i]}:\n {datasets[i][:]}")
                difference = []  # list of dependee datasets for transformations
                logging.debug("\tcheck dependencies:")
                for j, transform_str in enumerate(transforms_str[i]):
                    # extract transform function names list (in case one of them has args and this is list)
                    transform_name = transform_str[0] if isinstance(transform_str, list) else transform_str
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
                    for j, transform_str in enumerate(transforms_str[i]):
                        transform_name = transform_str
                        transform_func = transforms_func[i][j][0] if isinstance(transforms_func[i][j], list) else \
                            transforms_func[i][j]
                        transform_args = [dataset_names[i], datasets[i]]
                        if isinstance(transform_str, list):
                            transform_name = transform_str[0]
                            # in case there are enum arguments, convert them to  string for uniform processing
                            args_additional = transform_str[1:]
                            logging.debug(f"args_additional before: {args_additional}")
                            args_additional = [arg.name if isinstance(arg, Enum) else arg for arg in args_additional]
                            logging.debug(f"args_additional after: {args_additional}")
                            transform_args.extend(args_additional)
                        # transform_func = getattr(self.transformer, transform_name)

                        tf_cls = self._get_class(transform_func)
                        tf_cls_name = tf_cls.__name__  # works
                        assert (tf_cls_name == transform_name.split(".")[0])
                        transform_func = getattr(transforms_class_instances[tf_cls], transform_name.split(".")[1])

                        logging.debug(f"\t\ttransform_function: '{transform_name}', transform_args: '{transform_args}'")
                        datasets[i] = transform_func(*transform_args)

                        # update all transformer classe's dependencies
                        dependees_name = set(
                            [item for sublist in list(transforms_base_cls.DEPENDENCIES.values()) for item in sublist])
                        for dependee_name in dependees_name:
                            dependee = getattr(transforms_class_instances[tf_cls], dependee_name)
                            if dependee is not None:
                                for cls, instance in transforms_class_instances.items():
                                    dependee_other = getattr(transforms_class_instances[cls], dependee_name)
                                    if dependee_other is None:
                                        setattr(transforms_class_instances[cls], dependee_name, dependee)
                        debug_break_point = 42
                        # for cls, instance in transforms_class_instances:

                        # update dependees

                        transformed.add(dataset_names[i])
                    logging.debug(f"\ttransformed dataset '{dataset_names[i]}'.")
            i = (i + 1) % len(datasets)
        logging.info("transformed datasets.")

        # # creaet namedtyple type, values will be the transformed datasets
        # Data = namedtuple('Data', dataset_names)
        # logging.debug(f"dsets: len = {len(datasets)}, attr_names = {dataset_names}")
        # data = Data(*datasets)
        # return data

        # # datasets_dict = dict.fromkeys(extract.keys(), '')
        # datasets_dict = {}
        # for i, dataset_name in enumerate(dataset_names):
        #     datasets_dict[dataset_name] = datasets[i]
        # # add load functions
        # data_fct = load.count_atom_groups
        # datasets_dict[data_fct.__name__] = data_fct
        # Data = type(
        #     'Data',
        #     (),
        #     datasets_dict
        # )
        # data = Data()
        # return data

        # # datasets_dict = dict.fromkeys(extract.keys(), '')
        # data_attributes = {}
        # for i, dataset_name in enumerate(dataset_names):
        #     data_attributes[dataset_name] = datasets[i]
        # # add load functions
        # # data_fct = DataBands.count_atom_groups2
        # # data_attributes[data_fct.__name__] = data_fct
        #
        # DataDerived = type(
        #     data_type.__name__,
        #     (Data,), # could get base class from data_type if more general approach needed
        #     data_attributes
        # )
        # data = DataDerived()
        # return data

        # datasets_dict = dict.fromkeys(extract.keys(), '')
        data_attributes = {}
        for i, dataset_name in enumerate(dataset_names):
            data_attributes[dataset_name] = datasets[i]

        data_type = None
        data_classes_functions_specified
        data_cls_avail = dict([(name, cls) for name, cls in load.__dict__.items() if isinstance(cls, type)])
        print(data_cls_avail)

        # gather all available data classes and methods
        data_cls_instances = {}
        data_methods = {}
        for cls_name, cls in data_cls_avail.items():
            if cls not in load.EXCEPTIONS:
                cls_instance = cls()
                data_cls_instances[cls_name] = cls_instance
                methods_list = inspect.getmembers(cls_instance, predicate=inspect.ismethod)


                # data_cls_instances[cls_name] = cls
                # methods_list = inspect.getmembers(cls, predicate=inspect.ismethod)


                data_methods[cls_name] = {}
                for meth_name, meth in methods_list:
                    if not meth_name.startswith("__"):
                        data_methods[cls_name][meth_name] = meth

        # now go through specified classes and functions.
        # The first specified and available class will be the output data type.
        # All other functions will be added to data_attributes.
        # If there are other available classes specified, all of their methods will be added to data_attributes
        found_classes = OrderedDict()
        found_functions = OrderedDict()
        for type_or_name in data_classes_functions_specified:
            type_name = type_or_name if isinstance(type_or_name, str) else type_or_name.__name__
            type_only = self._str_to_type(type_or_name) if isinstance(type_or_name, str) else type_or_name
            print(f"type_name {type_name}, type_only {type_only}")
            found = False
            # is it a class?
            if type_name in data_cls_instances.keys():
                found_classes[type_name] = data_cls_instances[type_name]
                found = True
            else: # is it a method?
                type_class = self._get_class(type_only)
                type_class_name = type_class.__name__
                print(f"type class {type_class}")
                if data_methods.get(type_class_name):
                    methods = data_methods[type_class_name]
                    type_name = type_name.split(".")[1] if "." in type_name else type_name
                    if type_name in methods.keys():
                        if type_name in found_functions.keys():
                            raise AttributeError(f"The name of method '{type_name}' from class '{type_class_name}' specified in "
                                                 f"the config for data output class is already in use by another method of "
                                                 f"another specified data class. Resolve name conflict first.")
                        else:
                            found_functions[type_name] = methods[type_name]
                            found = True
                #
                # for cls_name, methods in data_methods.items():
                #     if type_name in methods.keys():
                #         print(f"methods[type_name] = {methods[type_name]}")
                #         if type_only_instance == methods[type_name]:
                #             found_functions[type_name] = methods[type_name]
                #             found = True
                #             break
            if not found:
                raise TypeError(f"The data type '{type_name}' specified in config is not a valid "
                                f"data class or one of their methods.")

        # now set thee first found class as data_type, and add all stuff to the data_attributes
        first = True
        for cls_name, cls in found_classes.items():
            if first:
                data_type = data_cls_avail[cls_name]
                first = False
            else:
                for meth_name, meth in data_methods[cls_name].items():
                    if data_attributes.get(meth_name) is not None:
                        raise AttributeError(f"The name of method '{meth_name}' from class '{cls_name}' specified in "
                                             f"the config for data output class is already in use as attribute for "
                                             f"a dataset or by another method of another specified data class. "
                                             f"Resolve name conflict first.")
                    else:
                        data_attributes[meth_name] = meth
        for meth_name, meth in found_functions.items():
            if data_attributes.get(meth_name) is not None:
                raise AttributeError(f"The name of method '{meth_name}' from class '{cls_name}' specified in "
                                     f"the config for data output class is already in use as attribute for "
                                     f"a dataset or by another method of another specified data class. "
                                     f"Resolve name conflict first.")
            else:
                data_attributes[meth_name] = meth

        # finally, print a warning if any of the data_type (type, not instance) members will overwrite the
        data_type_member_names_list = [pair[0] for pair in inspect.getmembers(data_type)]
        intersection = set(data_attributes.keys()).intersection(set(data_type_member_names_list))
        if intersection:
            logging.warning(f"The following datasets or data type functions specified in the config will "
                            f"be overwritten by the primary data type '{data_type.__name__}' members: "
                            f"{intersection}.")

        data = data_type(**data_attributes)
        return data


if __name__ == '__main__':
    # from studenproject18ws.hdf.config import Extract
    # from studenproject18ws.hdf.transform import TransformBands
    # from studenproject18ws.hdf.extract import Extractor

    # filename = 'banddos_4x4.hdf'
    filename = 'banddos.hdf'
    # filename = 'banddos_Co.hdf'

    filepath = ['..', 'data', 'input', filename]
    filepath = os.path.join(*filepath)

    data = None
    extractor = Extractor(filepath=filepath)
    with extractor as h5file:
        data = extractor.get(config=Extract.Bands, logging_level=logging.DEBUG)
        print("hi")
        #
        # Note:
        # Inside the with statement (context manager),
        # all HDF5 datasets are available. When the statement is left,
        # the HDF5 file gets closed and the datasets are closed.
        # Should they be left available, apply Transform.to_memory to them.
        #
        print(len(data.k_distances))
        print(len(data.k_points))
        print(data.bravaisMatrix)
        data.move_datasets_to_memory()

    # Left HDF5 file with statement: file and all open hdf5 Datasets are now closed.
    all_characters = [0, 1, 2, 3]
    all_groups = range(max(data.atom_group_keys))
    all_bands = range(data.eigenvalues.shape[2])
    print(data.weights(all_characters, all_groups, spin=0))
    print(data.combined_weight(all_characters, all_groups, spin=0))
