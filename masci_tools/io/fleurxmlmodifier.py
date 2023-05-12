###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools.   #
# For further information on the license, see the LICENSE.txt file.           #
# For further information please visit http://judft.de/.                      #
#                                                                             #
###############################################################################
"""
This module contains a class for organizing and grouping changes to a input file
of fleur in a robust way.

Essentially a low-level version of the FleurinpModifier in aiida_fleur.

.. note::
    The docstrings for the setter methods are generated from their actual implementations
    in the :py:mod:`~masci_tools.util.xml` modules via a pre-commit hook. Changes in the docstrings
    here will be overwritten
"""
from __future__ import annotations

from typing import Any, Callable, NamedTuple
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  #type: ignore

from masci_tools.util.xml.collect_xml_setters import XPATH_SETTERS, SCHEMA_DICT_SETTERS, NMMPMAT_SETTERS
from masci_tools.util.xml.xml_setters_names import set_attrib_value
from masci_tools.util.xml.common_functions import clear_xml, eval_xpath_one, get_inpgen_comments, readd_inpgen_comments
from masci_tools.util.schema_dict_util import ensure_relaxation_xinclude
from masci_tools.io.fleur_xml import load_inpxml
from masci_tools.util.typing import XMLFileLike, FileLike
from pathlib import Path
from lxml import etree
import warnings
#Enable warnings for missing docstrings
#pylint: enable=missing-function-docstring


class ModifierTask(NamedTuple):
    name: str
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = {}


class FleurXMLModifier:
    """
    Class for grouping and organizing changes to a inp.xml file of fleur via the
    xml setting methods in :py:mod:`~masci_tools.util.xml.xml_setters_names` and
    :py:mod:`~masci_tools.util.xml.xml_setters_basic`

    The basic usage is shown below

    .. code-block:: python

        from masci_tools.io.fleurxmlmodifier import FleurXMLModifier

        fmode = FleurXMLModifier()

        #Add changes by calling the methods on this class
        #(names correspond to the setting methods in the xml_setters modules)
        #They are not modifying a input file directly
        #Instead all the tasks are collected and performed in one go

        fmode.set_inpchanges({'Kmax': 4.0}) #Set Kmax to 4.0
        fmode.shift_value({'Gmax': 5.0}) #Add 5 to the current value of Gmax

        #Set the local orbital configuration on all iron atoms to '3s 3p'
        fmode.set_species('all-Fe', {'lo': [{'n':3, 'l': 's', 'type': 'SCLO'},
                                            {'n':3, 'l': 'p', 'type': 'SCLO'}]})

        #To undo the last change call undo
        #fmode.undo()

        #revert_all=True resets all added tasks
        #fmode.undo(revert_all=True)

        #To apply the changes to an input file use the modify_xmlfile method
        new_xmltree, additional_files = fmode.modify_xmlfile('/path/to/input/file/inp.xml')

    """

    _xpath_functions: dict[str, Callable] = XPATH_SETTERS
    _schema_dict_functions: dict[str, Callable] = SCHEMA_DICT_SETTERS
    _nmmpmat_functions: dict[str, Callable] = NMMPMAT_SETTERS

    _extra_functions: dict[Literal['xpath', 'schema_dict', 'nmmpmat'], dict[str, Callable]] = {}

    def __new__(cls, validate_signatures=True):

        if getattr(cls, 'xpath_functions', None) is None:
            cls.xpath_functions = {**cls._xpath_functions, **cls._extra_functions.get('xpath', {})}
            cls.schema_dict_functions = {**cls._schema_dict_functions, **cls._extra_functions.get('schema_dict', {})}
            cls.nmmpmat_functions = {**cls._nmmpmat_functions, **cls._extra_functions.get('nmmpmat', {})}

        return super().__new__(cls)

    def __init__(self, validate_signatures: bool = True) -> None:

        self._tasks: list[ModifierTask] = []
        self.validate_signatures = validate_signatures

    @classmethod
    def fromList(cls, task_list: list[tuple[str, dict[str, Any]]], *args: Any, **kwargs: Any) -> FleurXMLModifier:
        """
        Instantiate the FleurXMLModifier from a list of tasks to be added immediately

        :param task_list: list of tuples first index is the name of the method
                          second is defining the arguments by keyword in a dict

        Other arguments are passed on to the __init__ method

        :returns: class with the task list instantiated
        """

        fm = cls(*args, **kwargs)
        fm.add_task_list(task_list)
        return fm

    def add_task_list(self, task_list: list[tuple[str, dict[str, Any]]]) -> None:
        """
        Add a list of tasks to be added

        :param task_list: list of tuples first index is the name of the method
                          second is defining the arguments by keyword in a dict
        """

        facade_methods = self.get_avail_actions()

        for name, kwargs in task_list:
            try:
                facade_methods[name](**kwargs)
            except KeyError as exc:
                raise ValueError(f"Unknown modification method '{name}'") from exc

    def _validate_signature(self, name: str, *args: Any, **kwargs: Any) -> None:
        """
        DEPRECATED: use `_validate_arguments` instead without unpacking args/kwargs
        """
        warnings.warn(
            'The _validate_signature method is deprecated. '
            'Please use _validate_arguments without unpacking args/kwargs instead', DeprecationWarning)
        self._validate_arguments(name, args, kwargs)

    def _get_setter_function_and_prefix(self, name: str) -> tuple[Callable[[Any], Any], tuple[str, ...]]:
        """
        Get the setter function and a prefix standing in for the arguments that
        are substituted when performing the modification
        """
        if name in self.xpath_functions:
            func = self.xpath_functions[name]
            prefix: tuple[str, ...] = ('xmltree',)
        elif name in self.schema_dict_functions:
            func = self.schema_dict_functions[name]
            prefix = ('xmltree', 'schema_dict')
        elif name in self.nmmpmat_functions:
            func = self.nmmpmat_functions[name]
            prefix = ('xmltree', 'nmmplines', 'schema_dict')

        if func is None:
            raise ValueError(f'Failed to validate setter {name}. Maybe the function was'
                             'not registered in masci_tools.util.xml.collect_xml_setters')

        #For functions decorated with the schema_dict_version_dispatch
        #We check only the default (This function should have a compatible signature for all registered functions)
        if getattr(func, 'registry', None) is not None:
            func = func.registry['default']

        return func, prefix

    def _get_setter_func_kwargs(self, name: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> dict[str, Any]:
        """
        Map the given args and kwargs to just kwargs for the
        setter function with the given name

        :param name: name of the setter function
        :param args: positional arguments to the setter function
        :param kwargs: keyword arguments to the setter function
        """
        from inspect import signature
        func, prefix = self._get_setter_function_and_prefix(name)

        sig = signature(func)
        bound = sig.bind(*prefix, *args, **kwargs)

        kwargs_complete = {k: v for k, v in bound.arguments.items() if k not in ('xmltree', 'nmmplines', 'schema_dict')}

        #Fix if the XML modifying function has an explicit kwargs
        if 'kwargs' in kwargs_complete:
            kwargs_explicit = kwargs_complete.pop('kwargs')
            kwargs_complete = {**kwargs_complete, **kwargs_explicit}

        return kwargs_complete

    def _validate_arguments(self, name: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> None:
        """
        Validate that the given arguments to the registration
        method can be used to call the corresponding XML modifying function
        """
        from inspect import signature

        if self.validate_signatures:
            func, prefix = self._get_setter_function_and_prefix(name)
            try:
                sig = signature(func)
                sig.bind(*prefix, *args, **kwargs)
            except TypeError as exc:
                raise TypeError(
                    f"The given arguments for the registration method '{name}' are not valid for the XML modifying function"
                    f'The following error was raised: {exc}') from exc

    @classmethod
    def apply_modifications(cls,
                            xmltree: etree._ElementTree,
                            nmmp_lines: list[str] | None,
                            modification_tasks: list[ModifierTask],
                            validate_changes: bool = True,
                            adjust_version_for_dev_version: bool = True) -> tuple[etree._ElementTree, list[str] | None]:
        """
        Applies given modifications to the fleurinp lxml tree.
        It also checks if a new lxml tree is validated against schema.
        Does not rise an error if inp.xml is not validated, simple prints a message about it.

        :param xmltree: a lxml tree to be modified (IS MODIFIED INPLACE)
        :param nmmp_lines: a n_mmp_mat file to be modified (IS MODIFIED INPLACE)
        :param modification_tasks: a list of modification tuples
        :param validate_changes: bool optional (default True), if True after all tasks are performed
                                 both the xmltree and nmmp_lines are checked for consistency
        :param adjust_version_for_dev_version: bool optional (default True), if True and the schema_dict
                                               and file version differ, e.g. a development version is used
                                               the version is temporarily modified to swallow the validation
                                               error that would occur

        :returns: a modified lxml tree and a modified n_mmp_mat file
        """
        from masci_tools.util.xml.xml_setters_nmmpmat import validate_nmmpmat

        xmltree, schema_dict = load_inpxml(xmltree)
        xmltree, _ = clear_xml(xmltree)

        file_version = eval_xpath_one(xmltree, '//@fleurInputVersion', str)
        is_dev_version = schema_dict['inp_version'] != file_version

        for task in modification_tasks:
            if task.name in cls.xpath_functions:
                action = cls.xpath_functions[task.name]
                xmltree = action(xmltree, *task.args, **task.kwargs)

            elif task.name in cls.schema_dict_functions:
                action = cls.schema_dict_functions[task.name]
                xmltree = action(xmltree, schema_dict, *task.args, **task.kwargs)

            elif task.name in cls.nmmpmat_functions:
                action = cls.nmmpmat_functions[task.name]
                nmmp_lines = action(xmltree, nmmp_lines, schema_dict, *task.args, **task.kwargs)

            else:
                raise ValueError(f'Unknown task {task.name}')

        if validate_changes:
            if is_dev_version and adjust_version_for_dev_version:
                set_attrib_value(xmltree, schema_dict, 'fleurinputversion', schema_dict['inp_version'])
                schema_dict.validate(xmltree, header='Changes were not valid')
                set_attrib_value(xmltree, schema_dict, 'fleurinputversion', file_version)
            else:
                schema_dict.validate(xmltree, header='Changes were not valid')
            try:
                validate_nmmpmat(xmltree, nmmp_lines, schema_dict)
            except ValueError as exc:
                msg = f'Changes were not valid (n_mmp_mat file is not compatible): {modification_tasks}'
                raise ValueError(msg) from exc

        return xmltree, nmmp_lines

    @property
    def task_list(self) -> list[tuple[str, dict[str, Any]]]:
        """
        Return the current changes in a format accepted by :py:meth:`add_task_list()`
        and :py:meth:`fromList()`
        """

        tasks = []
        for change in self._tasks:
            #Here we already validated the arguments so we know we can just get the kwargs
            kwargs = self._get_setter_func_kwargs(change.name, change.args, change.kwargs)
            tasks.append((change.name, kwargs))

        return tasks

    def get_avail_actions(self) -> dict[str, Callable]:
        """
        Returns the allowed functions from FleurXMLModifier
        """
        outside_actions = {
            'set_inpchanges': self.set_inpchanges,
            'shift_value': self.shift_value,
            'set_xcfunctional': self.set_xcfunctional,
            'set_species': self.set_species,
            'set_species_label': self.set_species_label,
            'clone_species': self.clone_species,
            'switch_species': self.switch_species,
            'switch_species_label': self.switch_species_label,
            'shift_value_species_label': self.shift_value_species_label,
            'set_atomgroup': self.set_atomgroup,
            'set_atomgroup_label': self.set_atomgroup_label,
            'set_complex_tag': self.set_complex_tag,
            'set_simple_tag': self.set_simple_tag,
            'create_tag': self.create_tag,
            'delete_tag': self.delete_tag,
            'delete_att': self.delete_att,
            'replace_tag': self.replace_tag,
            'set_text': self.set_text,
            'set_first_text': self.set_first_text,
            'set_attrib_value': self.set_attrib_value,
            'set_first_attrib_value': self.set_first_attrib_value,
            'add_number_to_attrib': self.add_number_to_attrib,
            'add_number_to_first_attrib': self.add_number_to_first_attrib,
            'xml_create_tag': self.xml_create_tag,
            'xml_replace_tag': self.xml_replace_tag,
            'xml_delete_tag': self.xml_delete_tag,
            'xml_delete_att': self.xml_delete_att,
            'xml_set_attrib_value_no_create': self.xml_set_attrib_value_no_create,
            'xml_set_text_no_create': self.xml_set_text_no_create,
            'set_nmmpmat': self.set_nmmpmat,
            'rotate_nmmpmat': self.rotate_nmmpmat,
            'align_nmmpmat_to_sqa': self.align_nmmpmat_to_sqa,
            'set_nkpts': self.set_nkpts,
            'set_kpath': self.set_kpath,
            'set_kpointlist': self.set_kpointlist,
            'switch_kpointset': self.switch_kpointset,
            'set_kpointpath': self.set_kpointpath,
            'set_kpointmesh': self.set_kpointmesh
        }
        return outside_actions

    def undo(self, revert_all: bool = False) -> list[ModifierTask]:
        """
        Cancels the last change or all of them

        :param revert_all: set True if need to cancel all the changes, False if the last one.
        """
        if revert_all:
            self._tasks = []
        else:
            if self._tasks:
                self._tasks.pop()
                #TODO delete nodes from other nodes
                #del self._tasks[-1]
        return self._tasks

    def changes(self) -> list[ModifierTask]:
        """
        Prints out all changes currently registered on this instance
        """
        from pprint import pprint
        pprint(self._tasks)
        return self._tasks

    def modify_xmlfile(self,
                       original_inpxmlfile: XMLFileLike,
                       original_nmmp_file: FileLike | list[str] | None = None,
                       validate_changes: bool = True,
                       adjust_version_for_dev_version: bool = True,
                       keep_inpgen_comments: bool = True) -> tuple[etree._ElementTree, dict[str, str]]:
        """
        Applies the registered modifications to a given inputfile

        :param original_inpxmlfile: either path to the inp.xml file, opened file handle
                                    or a xml etree to be parsed
        :param original_nmmp_file: path or list of str to a corresponding density matrix
                                   file

        :raises ValueError: if the parsing of the input file

        :returns: a modified xmltree and if existent a modified density matrix file
        """
        original_xmltree, schema_dict = load_inpxml(original_inpxmlfile)
        comments = get_inpgen_comments(original_xmltree)

        if original_nmmp_file is not None:
            if isinstance(original_nmmp_file, str) and not Path(original_nmmp_file).is_file():
                original_nmmp_lines = original_nmmp_file.split('\n')
            elif isinstance(original_nmmp_file, (str, Path)):
                with open(original_nmmp_file, encoding='utf-8') as n_mmp_file:
                    original_nmmp_lines = n_mmp_file.read().split('\n')
            else:
                original_nmmp_lines = original_nmmp_file  #type:ignore[assignment]
        else:
            original_nmmp_lines = None

        new_xmltree, new_nmmp_lines = self.apply_modifications(
            original_xmltree,
            original_nmmp_lines,
            self._tasks,
            validate_changes=validate_changes,
            adjust_version_for_dev_version=adjust_version_for_dev_version)

        ensure_relaxation_xinclude(new_xmltree, schema_dict)

        if keep_inpgen_comments:
            readd_inpgen_comments(new_xmltree, comments)

        etree.indent(new_xmltree)

        additional_files = {}
        if new_nmmp_lines is not None:
            additional_files['n_mmp_mat'] = '\n'.join(new_nmmp_lines)
        return new_xmltree, additional_files

    def set_inpchanges(self, *args: Any, **kwargs: Any) -> None:
        """Set the value of attributes/text occurring once in the XML tree

        The first occurrence of the attribute/tag is set

        :param changes: dictionary {attrib_name : value} with all the wanted changes.
        :param path_spec: dict, with ggf. necessary further specifications for the path of the attribute

        An example of changes::

            changes = {
                'itmax' : 1,
                'l_noco': True,
                'ctail': False,
                'l_ss': True
            }


        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.set_inpchanges({'itmax' : 1, 'kmax': 4.3})

        .. usage-example::
            :title: Attribute selection not unique
            :result: Error
            :description: If no or multiple locations could be possible an error is raised

            fm.set_inpchanges({'itmax' : 1, 'theta': 1.57})

        .. usage-example::
            :title: Attribute selection
            :description: Selection can be done by adding conditions on what the XPath should(n't) contain
                          in the ``path_spec`` argument

            fm.set_inpchanges({'itmax' : 1, 'theta': 1.57},
                              path_spec={'theta': {'contains': 'soc'}})

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_inpchanges()` to
        the list of tasks that will be done on the xmltree.
        """
        if 'change_dict' in kwargs:
            warnings.warn('The argument change_dict is deprecated. Use changes instead', DeprecationWarning)
            kwargs['changes'] = kwargs.pop('change_dict')
        self._validate_arguments('set_inpchanges', args, kwargs)
        self._tasks.append(ModifierTask('set_inpchanges', args, kwargs))

    def shift_value(self, *args: Any, **kwargs: Any) -> None:
        """Add/Multiply values of attributes occurring once in the XML tree

        The first occurrence of the attribute is shifted

        :param changes: a python dictionary with the keys to shift and the shift values.
        :param mode: str (either `rel`/`relative` or `abs`/`absolute`).
                     `rel`/`relative` multiplies the old value with the given value
                     `abs`/`absolute` adds the old value and the given value
        :param path_spec: dict, with ggf. necessary further specifications for the path of the attribute


        An example of changes::

                changes = {'itmax' : 1, 'dVac': -0.123}

        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.shift_value({'itmax' : 5, 'mindistance': 1})

        .. usage-example::
            :title: Relative shift
            :description: Passing ``mode="rel"`` or ``mode="relative"`` will multiply
                          the initial attribute values with the provided number instead
                          of adding them

            fm.shift_value({'itmax' : 2, 'mindistance': 3}, mode="relative")

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.shift_value()` to
        the list of tasks that will be done on the xmltree.
        """
        if 'change_dict' in kwargs:
            warnings.warn('The argument change_dict is deprecated. Use changes instead', DeprecationWarning)
            kwargs['changes'] = kwargs.pop('change_dict')
        self._validate_arguments('shift_value', args, kwargs)
        self._tasks.append(ModifierTask('shift_value', args, kwargs))

    def set_species(self, *args: Any, **kwargs: Any) -> None:
        """Set the attributes of a species, specified by name position, etc.

        :param species_name: string, name of the specie you want to change
                             Can be name of the species, 'all' or 'all-<string>' (sets species with the string in the species name)
        :param changes: a python dict specifying what you want to change.
        :param create: bool, if species does not exist create it and all subtags?
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

        :raises ValueError: if species name is non existent in inp.xml and should not be created.
                            also if other given tags are garbage. (errors from eval_xpath() methods)

        :return xmltree: xml etree of the new inp.xml

        **changes** is a python dictionary containing dictionaries that specify attributes
        to be set inside the certain specie. For example, if one wants to set a MT radius it
        can be done via

        .. usage-example::

            fm.set_species('Fe-1', {'mtSphere' : {'radius' : 2.7}})

        .. usage-example::
            :title: Adding child elements
            :description: The `changes` dictionary is not limited to setting attributes
                          Child elements can also be created. Notice here that if multiple
                          elements of a given name are allowed all previously existing elements
                          are deleted and replaced with the ones specified in `changes`

            fm.set_species('Fe-1', {'ldaU' : {'l' : 3, 'U': 4.0, 'J': 0.5, 'l_amf': True},
                                    'lo': [{'l': 0, 'n': 6, 'type': 'SCLO'},
                                           {'l': 1, 'n': 6, 'type': 'SCLO'}]})

        .. usage-example::
            :title: Modifying all species
            :description: Providing `'all'` as the first argument applies the changes
                          to all species

            fm.set_species('all', {'mtSphere' : {'radius' : 2.7}})

        .. usage-example::
            :title: Modifying a subset of species
            :description: Providing `'all-<search string>'` as the first argument applies the changes
                          to all species which contain the search string in it's name

            fm.set_species('all-Pt', {'mtSphere' : {'radius' : 2.7},
                                      'lo': {'l': 0, 'n': 6, 'type': 'SCLO'},})

        Example species. All these attributes tags can be modified.
        Additional keys can for example be found in the FLEUR documentation flapw.de

        .. code-block:: xml

          <species name="Fe-1" element="Fe" atomicNumber="26">
             <mtSphere radius="2.20000000" gridPoints="787" logIncrement=".01600000"/>
             <atomicCutoffs lmax="10" lnonsphr="6"/>
                 <electronConfig>
                <coreConfig>[Ne]</coreConfig>
                <valenceConfig>(3s1/2) (3p1/2) (3p3/2) (4s1/2) (3d3/2) (3d5/2)</valenceConfig>
                <stateOccupation state="(3d3/2)" spinUp="2.00000000" spinDown="1.00000000"/>
                <stateOccupation state="(3d5/2)" spinUp="3.00000000" spinDown=".00000000"/>
             </electronConfig>
             <energyParameters s="4" p="4" d="3" f="4"/>
             <lo type="SCLO" l="0" n="3" eDeriv="0"/>
             <lo type="SCLO" l="1" n="3" eDeriv="0"/>
          </species>

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_species()` to
        the list of tasks that will be done on the xmltree.
        """
        if 'attributedict' in kwargs:
            warnings.warn('The argument attributedict is deprecated. Use changes instead', DeprecationWarning)
            kwargs['changes'] = kwargs.pop('attributedict')
        self._validate_arguments('set_species', args, kwargs)
        self._tasks.append(ModifierTask('set_species', args, kwargs))

    def set_species_label(self, *args: Any, **kwargs: Any) -> None:
        """Set the attributes of a species, given by an atom label occurring in it's atom type

        This method calls :func:`~masci_tools.util.xml.xml_setters_names.set_species()`
        method for a certain atom species that corresponds to an atom with a given label

        :param atom_label: string, a label of the atom which specie will be changed. 'all' to change all the species
        :param changes: a python dict specifying what you want to change.
        :param create: bool, if species does not exist create it and all subtags?


        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.set_species_label('222', {'mtSphere' : {'radius' : 2.7}})

        .. usage-example::
            :title: Adding child elements
            :description: The `changes` dictionary is not limited to setting attributes
                          Child elements can also be created. Notice here that if multiple
                          elements of a given name are allowed all previously existing elements
                          are deleted and replaced with the ones specified in `changes`

            fm.set_species_label('222', {'ldaU' : {'l' : 3, 'U': 4.0, 'J': 0.5, 'l_amf': True},
                                         'lo': [{'l': 0, 'n': 6, 'type': 'SCLO'},
                                                {'l': 1, 'n': 6, 'type': 'SCLO'}]})

        .. usage-example::
            :title: Modifying all species
            :description: Providing `'all'` as the first argument applies the changes
                          to all species

            fm.set_species_label('all', {'mtSphere' : {'radius' : 2.7}})

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_species_label()` to
        the list of tasks that will be done on the xmltree.
        """
        if 'attributedict' in kwargs:
            warnings.warn('The argument attributedict is deprecated. Use changes instead', DeprecationWarning)
            kwargs['changes'] = kwargs.pop('attributedict')
        self._validate_arguments('set_species_label', args, kwargs)
        self._tasks.append(ModifierTask('set_species_label', args, kwargs))

    def clone_species(self, *args: Any, **kwargs: Any) -> None:
        """Clone (and possibly change) a species in the XML tree

        For reference of the changes dictionary look at :py:func:`set_species()`

        :param species_name: string, name of the specie you want to clone
                             Has to correspond to one single species (no 'all'/'all-<search_string>')
        :param new_name: new name of the cloned species
        :param changes: a optional python dict specifying what you want to change.


        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.clone_species('Fe-1', 'Fe-clone-1')

        .. usage-example::
            :title: Modifying the cloned species
            :description: The `changes` dictionary is passed on to ``set_species``
                          to modify the cloned species

            fm.clone_species('Fe-1', 'Fe-clone-1', {'mtSphere' : {'radius' : 2.7}})

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.clone_species()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('clone_species', args, kwargs)
        self._tasks.append(ModifierTask('clone_species', args, kwargs))

    def switch_species(self, *args: Any, **kwargs: Any) -> None:
        """Change the species of an atom group, identified by species name, position, etc.

        :param new_species_name: name of the species to switch to
        :param position: position of an atom group to be changed. If equals to 'all', all species will be changed
        :param species: atom groups, corresponding to the given species will be changed
        :param clone: if True and the new species name does not exist and it corresponds to changing
                      from one species the species will be cloned with :py:func:`clone_species()`
        :param changes: changes to do if the species is cloned
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details


        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.switch_species('Pt-1', species='Fe-1')


        .. usage-example::
            :title: Specifying the number of the atromgroup
            :description: Providing the ``position`` argument will modify the n-th
                          atomgroup in the ``inp.xml`` file. (Indexing starts at 1)

            fm.switch_species('Pt-1', position=1)

        .. usage-example::
            :title: Create a clone of the old species
            :description: Specifying a non-existent new species name and ``clone=True``
                          will create a clone of the old species with that name. Additionally
                          the ``changes`` argument can then be used to apply changes to the new
                          clone

            fm.switch_species('Fe-clone-2', species='Fe-1', clone=True, changes={'mtSphere' : {'radius' : 2.7}})

        .. usage-example::
            :title: Modifying all species
            :description: Providing `'all'` to either ``position`` or ``species```
                          will modify the species of all atomgroups

            fm.switch_species('Fe-1', species='all')

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.switch_species()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('switch_species', args, kwargs)
        self._tasks.append(ModifierTask('switch_species', args, kwargs))

    def switch_species_label(self, *args: Any, **kwargs: Any) -> None:
        """Change the species of an atom group, identified by the lable of an atom in it's group

        :param atom_label: string, a label of the atom which group will be changed. 'all' to change all the groups
        :param new_species_name: name of the species to switch to
        :param clone: if True and the new species name does not exist and it corresponds to changing
                      from one species the species will be cloned with :py:func:`clone_species()`
        :param changes: changes to do if the species is cloned

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.switch_species_label()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('switch_species_label', args, kwargs)
        self._tasks.append(ModifierTask('switch_species_label', args, kwargs))

    def shift_value_species_label(self, *args: Any, **kwargs: Any) -> None:
        """Add/Multiply numeric attributes in a or multiple atom species
        Shifts the value of an attribute on a species by label
        if atom_label contains 'all' then applies to all species

        :param atom_label: string, a label of the atom which specie will be changed. 'all' if set up all species
        :param attribute_name: name of the attribute to change
        :param number_to_add: value to add or to multiply by
        :param mode: str (either `rel`/`relative` or `abs`/`absolute`).
                     `rel`/`relative` multiplies the old value with `number_to_add`
                     `abs`/`absolute` adds the old value and `number_to_add`

        Kwargs if the attribute_name does not correspond to a unique path:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path


        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.shift_value_species_label('222', 'radius', 1)

        .. usage-example::
            :title: Relative shift
            :description: Passing ``mode="rel"`` or ``mode="relative"`` will multiply
                          the initial attribute value with the provided number instead
                          of adding them

            fm.shift_value_species_label('222', 'radius', 1.2, mode="relative")

        .. usage-example::
            :title: Modifying all species
            :description: Providing `'all'` as the first argument applies the changes
                          to all atomgroups

            fm.shift_value_species_label('all', 'lmax', 2)

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.shift_value_species_label()` to
        the list of tasks that will be done on the xmltree.
        """
        if 'attributename' in kwargs:
            warnings.warn('The argument attributename is deprecated. Use attribute_name instead', DeprecationWarning)
            kwargs['attribute_name'] = kwargs.pop('attributename')
        if 'value_given' in kwargs:
            warnings.warn('The argument value_given is deprecated. Use number_to_add instead', DeprecationWarning)
            kwargs['number_to_add'] = kwargs.pop('value_given')
        self._validate_arguments('shift_value_species_label', args, kwargs)
        self._tasks.append(ModifierTask('shift_value_species_label', args, kwargs))

    def set_atomgroup(self, *args: Any, **kwargs: Any) -> None:
        """Set the attributes of a atom group, specified by species name, position, etc.

        :param changes: a python dict specifying what you want to change.
        :param position: position of an atom group to be changed. If equals to 'all', all species will be changed
        :param species: atom groups, corresponding to the given species will be changed
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details


        **changes** is a python dictionary containing dictionaries that specify attributes
        to be set inside the certain specie. For example, if one wants to set a beta noco parameter it
        can be done via::

            'changes': {'nocoParams': {'beta': val}}

        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.set_atomgroup({'nocoParams': {'alpha': 1.57}}, species='Fe-1')

        .. usage-example::
            :title: Specifying the number of the atromgroup
            :description: Providing the ``position`` argument will modify the n-th
                          atomgroup in the ``inp.xml`` file. (Indexing starts at 1)

            fm.set_atomgroup({'nocoParams': {'alpha': 1.57}}, position=1)

        .. usage-example::
            :title: Modifying all species
            :description: Providing `'all'` to either ``position`` or ``species```
                          will modify all atomgroups

            fm.set_atomgroup({'nocoParams': {'alpha': 1.57}}, species='all')

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_atomgroup()` to
        the list of tasks that will be done on the xmltree.
        """
        if 'attributedict' in kwargs:
            warnings.warn('The argument attributedict is deprecated. Use changes instead', DeprecationWarning)
            kwargs['changes'] = kwargs.pop('attributedict')
        if 'create' in kwargs:
            warnings.warn('The argument create is deprecated and is ignored.', DeprecationWarning)
            kwargs.pop('create')
        self._validate_arguments('set_atomgroup', args, kwargs)
        self._tasks.append(ModifierTask('set_atomgroup', args, kwargs))

    def set_atomgroup_label(self, *args: Any, **kwargs: Any) -> None:
        """Set the attributes of a atom group, given by an atom label occuring in it's definition

        This method calls :py:func:`~masci_tools.util.xml.xml_setters_names.set_atomgroup()`
        method for a certain atom species that corresponds to an atom with a given label.

        :param atom_label: string, a label of the atom which specie will be changed. 'all' to change all the species
        :param changes: a python dict specifying what you want to change.


        **changes** is a python dictionary containing dictionaries that specify attributes
        to be set inside the certain specie. For example, if one wants to set a beta noco parameter it
        can be done via::

            'changes': {'nocoParams': {'beta': val}}


        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.set_atomgroup_label('222', {'nocoParams': {'alpha': 1.57}})

        .. usage-example::
            :title: Modifying all species
            :description: Providing `'all'` as the first argument applies the changes
                          to all species

            fm.set_atomgroup_label('all', {'nocoParams': {'alpha': 1.57}})

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_atomgroup_label()` to
        the list of tasks that will be done on the xmltree.
        """
        if 'attributedict' in kwargs:
            warnings.warn('The argument attributedict is deprecated. Use changes instead', DeprecationWarning)
            kwargs['changes'] = kwargs.pop('attributedict')
        if 'create' in kwargs:
            warnings.warn('The argument create is deprecatedand is ignored.', DeprecationWarning)
            kwargs.pop('create')
        self._validate_arguments('set_atomgroup_label', args, kwargs)
        self._tasks.append(ModifierTask('set_atomgroup_label', args, kwargs))

    def create_tag(self, *args: Any, **kwargs: Any) -> None:
        """Create a tag with a given name in the XML tree
        This method creates a tag with a uniquely identified xpath under the nodes of its parent.
        If there are no nodes evaluated the subtags can be created with `create_parents=True`

        The tag is always inserted in the correct place if a order is enforced by the schema

        :param tag: str of the tag to create or etree Element or string representing the XML element with the same name to insert
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
        :param create_parents: bool optional (default False), if True and the given xpath has no results the
                               the parent tags are created recursively
        :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag.
                            By default all nodes are used.

        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path

        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.create_tag('mtnocoparams')

        .. usage-example::
            :title: Tag selection not unique
            :result: Error
            :description: If no or multiple locations could be possible an error is raised

            fm.create_tag('lo')

        .. usage-example::
            :title: Tag selection
            :description: Selection can be done by adding conditions on what the XPath should(n't) contain

            fm.create_tag('lo', contains='species')

        .. usage-example::
            :title: Nested creation
            :description: With ``create_parents=True`` evtl. missing parent tags are also created

            fm.create_tag('diagElements',
                          create_parents=True,
                          contains='species',
                          not_contains='torque')

        .. usage-example::
            :title: Creation of pre-created XML element
            :description: Passing a XML element instead of a name will insert this element at the correct position

            fm.create_tag(etree.Element('lo', n='5', l='0', type='SCLO'),
                          contains='species')

        .. usage-example::
            :title: Added filters
            :description: The filters argument allows to be more specific

            fm.create_tag(etree.Element('lo', n='5', l='0', type='SCLO'),
                          contains='species',
                          filters={
                            'species': {
                                'name': {'contains': 'Fe'}
                            }
                          })

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.create_tag()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('create_tag', args, kwargs)
        self._tasks.append(ModifierTask('create_tag', args, kwargs))

    def delete_tag(self, *args: Any, **kwargs: Any) -> None:
        """Delete a tag with a given name from the XML tree

        :param tag: str of the tag to delete
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
        :param occurrences: int or list of int. Which occurrence of the parent nodes to delete a tag.
                            By default all nodes are used.

        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path

        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.delete_tag('expertModes')

        .. usage-example::
            :title: Tag selection not unique
            :result: Error
            :description: If no or multiple locations could be possible an error is raised

            fm.delete_tag('lo')

        .. usage-example::
            :title: Tag selection
            :description: Selection can be done by adding conditions on what the XPath should(n't) contain

            fm.delete_tag('lo', contains='species')

        .. usage-example::
            :title: Added filters
            :description: The filters argument allows to be more specific

            fm.delete_tag('lo',
                          contains='species',
                          filters={
                            'species': {
                                'name': {'contains': 'Fe'}
                            }
                          })

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.delete_tag()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('delete_tag', args, kwargs)
        self._tasks.append(ModifierTask('delete_tag', args, kwargs))

    def delete_att(self, *args: Any, **kwargs: Any) -> None:
        """Delete an attribute with a given name from the XML tree

        :param name: str of the attribute to delete
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
        :param occurrences: int or list of int. Which occurrence of the parent nodes to delete a attribute.
                            By default all nodes are used.

        Kwargs:
            :param tag_name: str, name of the tag where the attribute should be parsed
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param exclude: list of str, here specific types of attributes can be excluded
                            valid values are: settable, settable_contains, other

        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.delete_att('mixparam')

        .. usage-example::
            :title: Tag selection not unique
            :result: Error
            :description: If no or multiple locations could be possible an error is raised

            fm.delete_att('alpha')

        .. usage-example::
            :title: Tag selection
            :description: Selection can be done by adding conditions on what the XPath should(n't) contain

            fm.delete_att('alpha', contains='nocoParams', not_contains='species')

        .. usage-example::
            :title: Added filters
            :description: The filters argument allows to be more specific

            fm.delete_att('alpha',
                          contains='nocoParams',
                          not_contains='species',
                          filters={
                            'atomGroup': {
                                'species': {'not-contains': 'Fe'}
                            }
                          })

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.delete_att()` to
        the list of tasks that will be done on the xmltree.
        """
        if 'attrib_name' in kwargs:
            warnings.warn('The argument attrib_name is deprecated. Use name instead', DeprecationWarning)
            kwargs['name'] = kwargs.pop('attrib_name')
        self._validate_arguments('delete_att', args, kwargs)
        self._tasks.append(ModifierTask('delete_att', args, kwargs))

    def replace_tag(self, *args: Any, **kwargs: Any) -> None:
        """Replace a tag with a given name with a different XML element

        :param tag: str of the tag to replace
        :param element: etree Element or string representing the XML element to replace the tag
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
        :param occurrences: int or list of int. Which occurrence of the parent nodes to replace a tag.
                            By default all nodes are used.

        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path

        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.replace_tag('expertmodes', etree.Element('greensFunction'))

        .. usage-example::
            :title: Tag selection not unique
            :result: Error
            :description: If no or multiple locations could be possible an error is raised

            fm.replace_tag('lo', etree.Element('ldaU', l='3'))

        .. usage-example::
            :title: Tag selection
            :description: Selection can be done by adding conditions on what the XPath should(n't) contain

            fm.replace_tag('lo', etree.Element('ldaU', l='3'), contains='species')

        .. usage-example::
            :title: Added filters
            :description: The filters argument allows to be more specific

            fm.replace_tag('lo',
                          etree.Element('ldaU', l='3'),
                          contains='species',
                          filters={
                            'species': {
                                'atomicNumber': {'>': 30}
                          }})

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.replace_tag()` to
        the list of tasks that will be done on the xmltree.
        """
        if 'newelement' in kwargs:
            warnings.warn('The argument newelement is deprecated. Use element instead', DeprecationWarning)
            kwargs['element'] = kwargs.pop('newelement')
        self._validate_arguments('replace_tag', args, kwargs)
        self._tasks.append(ModifierTask('replace_tag', args, kwargs))

    def set_complex_tag(self, *args: Any, **kwargs: Any) -> None:
        """Setattributes, text and subtags of a given tag in the XML tree

        Function to correctly set tags/attributes for a given tag.
        Goes through the attributedict and decides based on the schema_dict, how the corresponding
        key has to be handled.
        The tag is specified via its name and evtl. further specification

        Supports:

            - attributes
            - tags with text only
            - simple tags, i.e. only attributes (can be optional single/multiple)
            - complex tags, will recursively create/modify them

        :param tag_name: name of the tag to set
        :param changes: Keys in the dictionary correspond to names of tags and the values are the modifications
                        to do on this tag (attributename, subdict with changes to the subtag, ...)
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
        :param create: bool optional (default False), if True and the path, where the complex tag is
                       set does not exist it is created

        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_complex_tag()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('set_complex_tag', args, kwargs)
        self._tasks.append(ModifierTask('set_complex_tag', args, kwargs))

    def set_simple_tag(self, *args: Any, **kwargs: Any) -> None:
        """Sets one or multiple ``simple`` tag(s) (no subtags/text) in an xmltree.

        A simple tag can only hold attributes and has no
        subtags. The tag is specified by its name and further specification
        If the tag can occur multiple times all existing tags are DELETED and new ones are written.
        If the tag only occurs once it will automatically be created if its missing.

        :param tag_name: str name of the tag to modify/set
        :param changes: list of dicts or dict with the changes. Elements in list describe multiple tags.
                        Keys in the dictionary correspond to {'attributename': attributevalue}
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
        :param create_parents: bool optional (default False), if True and the path, where the simple tags are
                               set does not exist it is created

        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path

        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.set_simple_tag('soc', {'theta': 0.1, 'phi': 0.2, 'l_soc': True})

        .. usage-example::
            :title: Tag selection not unique
            :result: Error
            :description: If no or multiple locations could be possible an error is raised

            fm.set_simple_tag('lo', [{'l': 0, 'n': 6, 'type': 'SCLO'},
                                     {'l': 1, 'n': 6, 'type': 'SCLO'}])

        .. usage-example::
            :title: Tag selection
            :description: Selection can be done by adding conditions on what the XPath should(n't) contain

            fm.set_simple_tag('lo', [{'l': 0, 'n': 6, 'type': 'SCLO'},
                                     {'l': 1, 'n': 6, 'type': 'SCLO'}],
                              contains='species')

        .. usage-example::
            :title: Nested creation
            :description: With `create_parents=True` if the parents of the tag are missing they are
                          created

            fm.set_simple_tag('realAxis', {'ne': 1300, 'ellow': -1.0, 'elup': 1.0}, create_parents=True)

        .. usage-example::
            :title: Added filters
            :description: The filters argument allows to be more specific

            fm.set_simple_tag('lo', [{'l': 0, 'n': 6, 'type': 'SCLO'},
                                     {'l': 1, 'n': 6, 'type': 'SCLO'}],
                              contains='species',
                              filters={
                                 'species': {
                                     'atomicNumber': {'>': 30}
                             }})

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_simple_tag()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('set_simple_tag', args, kwargs)
        self._tasks.append(ModifierTask('set_simple_tag', args, kwargs))

    def set_text(self, *args: Any, **kwargs: Any) -> None:
        """Set the value of text of tags in the XML tree possibly occurring mutliple times

        By default the text will be set on all nodes returned for the specified xpath.
        If there are no nodes under the specified xpath a tag can be created with `create=True`.
        The text values are converted automatically according to the types
        with :py:func:`~masci_tools.util.xml.converters.convert_to_xml()` if they
        are not `str` already.

        :param tag_name: str name of the tag, where the text should be set
        :param text: value or list of values to set
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
        :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.
        :param create: bool optional (default False), if True the tag is created if is missing

        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path

        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.set_text('kpoint', [[1,2,3], [4,5,6]])

        .. usage-example::
            :title: Setting one value
            :description: If only one value for the text is given all elements are set ot the same value
                          in this case only one list of three coordinates is set

            fm.set_text('kpoint', [4,4,4])

        .. usage-example::
            :title: Tag selection not unique
            :result: Error
            :description: If no or multiple locations could be possible an error is raised

            fm.set_text('q', '1 1 1')

        .. usage-example::
            :title: Tag selection
            :description: Selection can be done by adding conditions on what the XPath should(n't) contain

            fm.set_text('q', '1 1 1', contains='spinSpiral')

        .. usage-example::
            :title: Added filters
            :description: The filters argument allows to be more specific

            fm.set_text('valenceConfig',
                        '(1s1/2)',
                        contains='species',
                        filters={
                            'species': {
                                './lo/@n': {'>': 4}
                        }})

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_text()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('set_text', args, kwargs)
        self._tasks.append(ModifierTask('set_text', args, kwargs))

    def set_first_text(self, *args: Any, **kwargs: Any) -> None:
        """Set the value of text of the first occurrence of a tag in the XML tree

        By default the text will be set on all nodes returned for the specified xpath.
        If there are no nodes under the specified xpath a tag can be created with `create=True`.
        The text values are converted automatically according to the types
        with :py:func:`~masci_tools.util.xml.converters.convert_to_xml()` if they
        are not `str` already.

        :param tag_name: str name of the tag, where the text should be set
        :param text: value or list of values to set
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
        :param create: bool optional (default False), if True the tag is created if is missing

        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path

        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.set_first_text('kpoint', [1,2,3])

        .. usage-example::
            :title: Tag selection not unique
            :result: Error
            :description: If no or multiple locations could be possible an error is raised

            fm.set_first_text('valenceConfig', '(1s1/2)')

        .. usage-example::
            :title: Tag selection
            :description: Selection can be done by adding conditions on what the XPath should(n't) contain

            fm.set_first_text('valenceConfig', '(1s1/2)', contains='species')

        .. usage-example::
            :title: Added filters
            :description: The filters argument allows to be more specific

            fm.set_first_text('valenceConfig',
                             '(1s1/2)',
                             contains='species',
                             filters={
                                 'species': {
                                     './lo/@n': {'>': 4}
                             }})

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_first_text()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('set_first_text', args, kwargs)
        self._tasks.append(ModifierTask('set_first_text', args, kwargs))

    def set_attrib_value(self, *args: Any, **kwargs: Any) -> None:
        """Set the value of an attribute possibly occurring multiple times

        If there are no nodes under the specified xpath a tag can be created with `create=True`.
        The attribute values are converted automatically according to the types of the attribute
        with :py:func:`~masci_tools.util.xml.converters.convert_to_xml()` if they
        are not `str` already.

        :param name: the attribute name to set
        :param value: value or list of values to set
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
        :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.
        :param create: bool optional (default False), if True the tag is created if is missing

        Kwargs:
            :param tag_name: str, name of the tag where the attribute should be parsed
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param exclude: list of str, here specific types of attributes can be excluded
                            valid values are: settable, settable_contains, other

        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.set_attrib_value('itmax', 180)

        .. usage-example::
            :title: Tag selection not unique
            :result: Error
            :description: If no or multiple locations could be possible an error is raised

            fm.set_attrib_value('radius', 1.05)

        .. usage-example::
            :title: Tag selection
            :description: Selection can be done by adding conditions on what the XPath should(n't) contain

            fm.set_attrib_value('radius', 1.05, contains='species')

        .. usage-example::
            :title: Added filters
            :description: The filters argument allows to be more specific

            fm.set_attrib_value('spinUp',
                                1,
                                contains='species',
                                filters={
                                    'species': {
                                        'atomicNumber': {'>': 30}
                                }})

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_attrib_value()` to
        the list of tasks that will be done on the xmltree.
        """
        if 'attributename' in kwargs:
            warnings.warn('The argument attributename is deprecated. Use name instead', DeprecationWarning)
            kwargs['name'] = kwargs.pop('attributename')
        if 'attribv' in kwargs:
            warnings.warn('The argument attribv is deprecated. Use value instead', DeprecationWarning)
            kwargs['value'] = kwargs.pop('attribv')
        self._validate_arguments('set_attrib_value', args, kwargs)
        self._tasks.append(ModifierTask('set_attrib_value', args, kwargs))

    def set_first_attrib_value(self, *args: Any, **kwargs: Any) -> None:
        """Set the value of the first occurrence of an attribute

        If there are no nodes under the specified xpath a tag can be created with `create=True`.
        The attribute values are converted automatically according to the types of the attribute
        with :py:func:`~masci_tools.util.xml.converters.convert_to_xml()` if they
        are not `str` already.

        :param name: the attribute name to set
        :param value: value or list of values to set
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
        :param create: bool optional (default False), if True the tag is created if is missing

        Kwargs:
            :param tag_name: str, name of the tag where the attribute should be parsed
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param exclude: list of str, here specific types of attributes can be excluded
                            valid values are: settable, settable_contains, other

        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.set_first_attrib_value('itmax', 180)

        .. usage-example::
            :title: Tag selection not unique
            :result: Error
            :description: If no or multiple locations could be possible an error is raised

            fm.set_first_attrib_value('radius', 1.05)

        .. usage-example::
            :title: Tag selection
            :description: Selection can be done by adding conditions on what the XPath should(n't) contain

            fm.set_first_attrib_value('radius', 1.05, contains='species')

        .. usage-example::
            :title: Added filters
            :description: The filters argument allows to be more specific

            fm.set_first_attrib_value('spinUp',
                                      1,
                                      contains='species',
                                      filters={
                                          'species': {
                                              'atomicNumber': {'>': 30}
                                      }})

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_first_attrib_value()` to
        the list of tasks that will be done on the xmltree.
        """
        if 'attributename' in kwargs:
            warnings.warn('The argument attributename is deprecated. Use name instead', DeprecationWarning)
            kwargs['name'] = kwargs.pop('attributename')
        if 'attribv' in kwargs:
            warnings.warn('The argument attribv is deprecated. Use value instead', DeprecationWarning)
            kwargs['value'] = kwargs.pop('attribv')
        self._validate_arguments('set_first_attrib_value', args, kwargs)
        self._tasks.append(ModifierTask('set_first_attrib_value', args, kwargs))

    def add_number_to_attrib(self, *args: Any, **kwargs: Any) -> None:
        """Add/Multiply values for multiple occurrences in the XML tree

        :param name: the attribute name to change
        :param number_to_add: number to add/multiply with the old attribute value
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
        :param mode: str (either `rel`/`relative` or `abs`/`absolute`).
                     `rel`/`relative` multiplies the old value with `number_to_add`
                     `abs`/`absolute` adds the old value and `number_to_add`
        :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.

        Kwargs:
            :param tag_name: str, name of the tag where the attribute should be parsed
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param exclude: list of str, here specific types of attributes can be excluded
                            valid values are: settable, settable_contains, other

        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.add_number_to_attrib('itmax', 10)

        .. usage-example::
            :title: Tag selection not unique
            :result: Error
            :description: If no or multiple locations could be possible an error is raised

            fm.add_number_to_attrib('radius', 1.05, mode='rel')

        .. usage-example::
            :title: Tag selection
            :description: Selection can be done by adding conditions on what the XPath should(n't) contain

            fm.add_number_to_attrib('radius', 1.05, mode='rel', contains='species')

        .. usage-example::
            :title: Added filters
            :description: The filters argument allows to be more specific

            fm.add_number_to_attrib('spinUp',
                                    -1,
                                    contains='species',
                                    filters={
                                        'species': {
                                            'atomicNumber': {'>': 30}
                                    }})

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.add_number_to_attrib()` to
        the list of tasks that will be done on the xmltree.
        """
        if 'attributename' in kwargs:
            warnings.warn('The argument attributename is deprecated. Use name instead', DeprecationWarning)
            kwargs['name'] = kwargs.pop('attributename')
        if 'add_number' in kwargs:
            warnings.warn('The argument add_number is deprecated. Use number_to_add instead', DeprecationWarning)
            kwargs['number_to_add'] = kwargs.pop('add_number')
        self._validate_arguments('add_number_to_attrib', args, kwargs)
        self._tasks.append(ModifierTask('add_number_to_attrib', args, kwargs))

    def add_number_to_first_attrib(self, *args: Any, **kwargs: Any) -> None:
        """Add/Multiply value for the first occurrences of an attribute in the XML tree

        :param name: the attribute name to change
        :param number_to_add: number to add/multiply with the old attribute value
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param mode: str (either `rel`/`relative` or `abs`/`absolute`).
                     `rel`/`relative` multiplies the old value with `number_to_add`
                     `abs`/`absolute` adds the old value and `number_to_add`
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

        Kwargs:
            :param tag_name: str, name of the tag where the attribute should be parsed
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param exclude: list of str, here specific types of attributes can be excluded
                            valid values are: settable, settable_contains, other

        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.add_number_to_first_attrib('itmax', 10)

        .. usage-example::
            :title: Tag selection not unique
            :result: Error
            :description: If no or multiple locations could be possible an error is raised

            fm.add_number_to_first_attrib('radius', 1.05, mode='rel')

        .. usage-example::
            :title: Tag selection
            :description: Selection can be done by adding conditions on what the XPath should(n't) contain

            fm.add_number_to_first_attrib('radius', 1.05, mode='rel', contains='species')

        .. usage-example::
            :title: Added filters
            :description: The filters argument allows to be more specific

            fm.add_number_to_first_attrib('spinUp',
                                          -1,
                                          contains='species',
                                          filters={
                                              'species': {
                                                  'atomicNumber': {'>': 30}
                                          }})

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.add_number_to_first_attrib()` to
        the list of tasks that will be done on the xmltree.
        """
        if 'attributename' in kwargs:
            warnings.warn('The argument attributename is deprecated. Use name instead', DeprecationWarning)
            kwargs['name'] = kwargs.pop('attributename')
        if 'add_number' in kwargs:
            warnings.warn('The argument add_number is deprecated. Use number_to_add instead', DeprecationWarning)
            kwargs['number_to_add'] = kwargs.pop('add_number')
        self._validate_arguments('add_number_to_first_attrib', args, kwargs)
        self._tasks.append(ModifierTask('add_number_to_first_attrib', args, kwargs))

    def xml_create_tag(self, *args: Any, **kwargs: Any) -> None:
        """Creates a tag under the given XPath
        This method evaluates an xpath expression and creates a tag in a xmltree under the
        returned nodes.
        If there are no nodes under the specified xpath an error is raised.

        The tag is appended by default, but can be inserted at a certain index (`place_index`)
        or can be inserted according to a given order of tags

        :param xpath: a path where to place a new tag
        :param element: a tag name, etree Element or string representing the XML element to be created
        :param place_index: defines the place where to put a created tag
        :param tag_order: defines a tag order
        :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag.
                            By default all nodes are used.
        :param correct_order: bool, if True (default) and a tag_order is given, that does not correspond to the given order
                              in the xmltree (only order wrong no unknown tags) it will be corrected and a warning is given
                              This is necessary for some edge cases of the xml schemas of fleur
        :param several: bool, if True multiple tags od the given name are allowed

        :raises ValueError: If the insertion failed in any way (tag_order does not match, failed to insert, ...)

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_basic.xml_create_tag()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('xml_create_tag', args, kwargs)
        self._tasks.append(ModifierTask('xml_create_tag', args, kwargs))

    def xml_replace_tag(self, *args: Any, **kwargs: Any) -> None:
        """Replace XML tags under the XPath by a given tag

        :param xpath: a path to the tag to be replaced
        :param element: an Element or string representing the Element to replace the found tags with
        :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag.
                            By default all nodes are used.

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_basic.xml_replace_tag()` to
        the list of tasks that will be done on the xmltree.
        """
        if 'newelement' in kwargs:
            warnings.warn('The argument newelement is deprecated. Use element instead', DeprecationWarning)
            kwargs['element'] = kwargs.pop('newelement')

        self._validate_arguments('xml_replace_tag', args, kwargs)
        self._tasks.append(ModifierTask('xml_replace_tag', args, kwargs))

    def xml_delete_tag(self, *args: Any, **kwargs: Any) -> None:
        """Deletes a tag under the XPath in the XML tree.

        :param xpath: a path to the tag to be deleted
        :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag.
                            By default all nodes are used.

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_basic.xml_delete_tag()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('xml_delete_tag', args, kwargs)
        self._tasks.append(ModifierTask('xml_delete_tag', args, kwargs))

    def xml_delete_att(self, *args: Any, **kwargs: Any) -> None:
        """Deletes an attribute on the tags of the given XPath in the XML tree

        :param xpath: a path to the attribute to be deleted
        :param name: the name of an attribute to delete
        :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag.
                            By default all nodes are used.

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_basic.xml_delete_att()` to
        the list of tasks that will be done on the xmltree.
        """
        if 'attributename' in kwargs:
            warnings.warn('The argument attributename is deprecated. Use name instead', DeprecationWarning)
            kwargs['name'] = kwargs.pop('attributename')
        self._validate_arguments('xml_delete_att', args, kwargs)
        self._tasks.append(ModifierTask('xml_delete_att', args, kwargs))

    def xml_set_attrib_value_no_create(self, *args: Any, **kwargs: Any) -> None:
        """Sets the value of an attribute under the XPath
        By default the attribute will be set
        on all nodes returned for the specified xpath.

        :param xpath: a path where to set the attributes
        :param name: the attribute name to set
        :param value: value or list of values to set (if not str they will be converted with `str(value)`)
        :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.

        :raises ValueError: If the lengths of attribv or occurrences do not match number of nodes

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_basic.xml_set_attrib_value_no_create()` to
        the list of tasks that will be done on the xmltree.
        """
        if 'attributename' in kwargs:
            warnings.warn('The argument attributename is deprecated. Use name instead', DeprecationWarning)
            kwargs['name'] = kwargs.pop('attributename')
        if 'attribv' in kwargs:
            warnings.warn('The argument attribv is deprecated. Use value instead', DeprecationWarning)
            kwargs['value'] = kwargs.pop('attribv')
        self._validate_arguments('xml_set_attrib_value_no_create', args, kwargs)
        self._tasks.append(ModifierTask('xml_set_attrib_value_no_create', args, kwargs))

    def xml_set_text_no_create(self, *args: Any, **kwargs: Any) -> None:
        """Sets the text of a tag under the XPath
        By default the text will be set on all nodes returned for the specified xpath.

        :param xpath: a path where to set the text
        :param text: value or list of values to set (if not str they will be converted with `str(value)`)
        :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.

        :raises ValueError: If the lengths of text or occurrences do not match number of nodes

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_basic.xml_set_text_no_create()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('xml_set_text_no_create', args, kwargs)
        self._tasks.append(ModifierTask('xml_set_text_no_create', args, kwargs))

    def set_nmmpmat(self, *args: Any, **kwargs: Any) -> None:
        """Routine sets the block in the n_mmp_mat file specified by species_name, orbital and spin
        to the desired density matrix

        :param species_name: string, name of the species you want to change
        :param orbital: integer, orbital quantum number of the LDA+U procedure to be modified
        :param spin: integer, specifies which spin block should be modified
        :param state_occupations: list, sets the diagonal elements of the density matrix and everything
                                  else to zero
        :param denmat: matrix, specify the density matrix explicitly
        :param phi: float, optional angle (radian), by which to rotate the density matrix before writing it
        :param theta: float, optional angle (radian), by which to rotate the density matrix before writing it
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

        :raises ValueError: If something in the input is wrong
        :raises KeyError: If no LDA+U procedure is found on a species

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_nmmpmat.set_nmmpmat()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('set_nmmpmat', args, kwargs)
        self._tasks.append(ModifierTask('set_nmmpmat', args, kwargs))

    def rotate_nmmpmat(self, *args: Any, **kwargs: Any) -> None:
        """Rotate the density matrix with the given angles phi and theta

        :param species_name: string, name of the species you want to change
        :param orbital: integer or string ('all'), orbital quantum number of the LDA+U procedure to be modified
        :param phi: float, angle (radian), by which to rotate the density matrix
        :param theta: float, angle (radian), by which to rotate the density matrix
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

        :raises ValueError: If something in the input is wrong
        :raises KeyError: If no LDA+U procedure is found on a species

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_nmmpmat.rotate_nmmpmat()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('rotate_nmmpmat', args, kwargs)
        self._tasks.append(ModifierTask('rotate_nmmpmat', args, kwargs))

    def align_nmmpmat_to_sqa(self, *args: Any, **kwargs: Any) -> None:
        """Align the density matrix with the given SQA of the associated species

        :param species_name: string, name of the species you want to change
        :param orbital: integer or string ('all'), orbital quantum number of the LDA+U procedure to be modified
        :param phi_before: float or list of floats, angle (radian),
                           values for phi for the previous alignment of the density matrix
        :param theta_before: float or list of floats, angle (radian),
                             values for theta for the previous alignment of the density matrix
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

        :raises ValueError: If something in the input is wrong
        :raises KeyError: If no LDA+U procedure is found on a species

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_nmmpmat.align_nmmpmat_to_sqa()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('align_nmmpmat_to_sqa', args, kwargs)
        self._tasks.append(ModifierTask('align_nmmpmat_to_sqa', args, kwargs))

    def set_kpointlist(self, *args: Any, **kwargs: Any) -> None:
        """Create a k-point list with the given points and weights

        .. note::
            If no name is given, a name of the form ``default-<number>`` is generated

        .. warning::
            For input versions Max4 and older **all** keyword arguments are not valid (`name`, `kpoint_type`,
            `special_labels`, `switch` and `overwrite`)

        :param kpoints: list or array containing the **relative** coordinates of the kpoints
        :param weights: list or array containing the weights of the kpoints
        :param name: str for the name of the list, if not given a default name is generated
        :param kpoint_type: str specifying the type of the kPointList ('path', 'mesh', 'spex', 'tria', ...)
        :param special_labels: dict mapping indices to labels. The labels will be inserted for the kpoints
                               corresponding to the given index
        :param switch: bool, if True the kPointlist will be used by Fleur when starting the next calculation
        :param overwrite: bool, if True and a kPointlist with the given name already exists it will be overwritten


        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.set_kpointlist([[0,0,0],[0.5,0.5,0.5]],
                              [1,1], switch=True)

        .. usage-example::
            :title: MaX 4 compatibility
            :description: For input files before the MaX 5 release the previous kpoint list will always
                          be overwritten and the ``switch`` argument has no effect
            :inputfile: inp_max4.xml

            fm.set_kpointlist([[0,0,0],[0.5,0.5,0.5]],
                              [1,1])

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_kpointlist()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('set_kpointlist', args, kwargs)
        self._tasks.append(ModifierTask('set_kpointlist', args, kwargs))

    def switch_kpointset(self, *args: Any, **kwargs: Any) -> None:
        """Switch the used k-point set

        .. warning::
            This method is only supported for input versions after the Max5 release

        :param list_name: name of the kPoint set to use

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.switch_kpointset()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('switch_kpointset', args, kwargs)
        self._tasks.append(ModifierTask('switch_kpointset', args, kwargs))

    def set_nkpts(self, *args: Any, **kwargs: Any) -> None:
        """Sets a k-point mesh directly specific for inputs of version Max4

        .. warning::
            This method is only supported for input versions before the Max5 release

        :param count: number of k-points
        :param gamma: bool that controls if the gamma-point should be included
                      in the k-point mesh


        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::
            :inputfile: inp_max4.xml

            fm.set_nkpts(200)


        .. usage-example::
            :title: Include Gamma point
            :inputfile: inp_max4.xml

            fm.set_nkpts(200, gamma=True)

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_nkpts()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('set_nkpts', args, kwargs)
        self._tasks.append(ModifierTask('set_nkpts', args, kwargs))

    def set_kpath(self, *args: Any, **kwargs: Any) -> None:
        """Sets a k-path directly as an alternative kpoint set with purpose 'bands'

        .. warning::
            This method is only supported for input versions before the Max5 release

        :param kpath: a dictionary with kpoint name as key and k point coordinate as value
        :param count: number of k-points
        :param gamma: bool that controls if the gamma-point should be included
                      in the k-point mesh


        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::
            :inputfile: inp_max4.xml

            fm.set_kpath({'Point': [0, 0, 0], 'Point2': [1, 1, 1]}, 200)

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_kpath()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('set_kpath', args, kwargs)
        self._tasks.append(ModifierTask('set_kpath', args, kwargs))

    def set_kpointpath(self, *args: Any, **kwargs: Any) -> None:
        """Create a kpoint list for a bandstructure calculation (using ASE kpath generation)

        The path can be defined explictly (see :py:func:`~ase.dft.kpoints.bandpath`) or derived from the unit cell

        :param path: str, list of str or None defines the path to interpolate (for syntax :py:func:`~ase.dft.kpoints.bandpath`)
        :param nkpts: int number of kpoints in the path
        :param density: float number of kpoints per Angstroem
        :param name: Name of the created kpoint list. If not given a name is generated
        :param switch: bool if True the kpoint list is direclty set as the used set
        :param overwrite: if True and a kpoint list of the given name already exists it will be overwritten
        :param special_points: dict mapping names to coordinates for special points to use


        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.set_kpointpath(nkpts=50, switch=True)

        .. usage-example::
            :title: Specifying custom points
            :description: By default the path is chosen by ASE. By providing path
                          this can be modified

            fm.set_kpointpath(path='CA',
                              nkpts=25,
                              special_points={
                                    'C': [0, 0, 0],
                                    'A': [0, 0, 0.5]
                              })

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_kpointpath()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('set_kpointpath', args, kwargs)
        self._tasks.append(ModifierTask('set_kpointpath', args, kwargs))

    def set_kpointmesh(self, *args: Any, **kwargs: Any) -> None:
        """Create a kpoint mesh using spglib

        for details see :py:func:`~spglib.get_stabilized_reciprocal_mesh`

        :param mesh: list-like woth three elements, giving the size of the kpoint set in each direction
        :param use_symmetry: bool if True the available symmetry operations in the inp.xml will be used
                             to reduce the kpoint set otherwise only the identity matrix is used
        :param name: Name of the created kpoint list. If not given a name is generated
        :param switch: bool if True the kpoint list is direclty set as the used set
        :param overwrite: if True and a kpoint list of the given name already exists it will be overwritten
        :param shift: shift the center of the kpint set
        :param time_reversal: bool if True time reversal symmetry will be used to reduce the kpoint set
        :param map_to_first_bz: bool if True the kpoints are mapped into the [0,1] interval


        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.set_kpointmesh([4, 4, 1], switch=True)

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_kpointmesh()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('set_kpointmesh', args, kwargs)
        self._tasks.append(ModifierTask('set_kpointmesh', args, kwargs))

    def set_xcfunctional(self, *args: Any, **kwargs: Any) -> None:
        """Set the Exchange Correlation potential tag

        :param xc_functional: str or dict. If str it is the name of a inbuilt XC functional. If it is a dict it
                              specifies either the name or id for LibXC functionals for the keys
                              `'exchange', 'correlation', 'etot_exchange' and 'etot_correlation'`
        :param xc_functional_options: dict with further general changes to the `xcFunctional` tag
        :param libxc: bool if True the functional is a LibXC functional


        Usage Examples (fm refers to an instance of :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`)

        .. usage-example::

            fm.set_xcfunctional('vwn')


        .. usage-example::
            :title: Setting a LibXC functional

            fm.set_xcfunctional({'exchange': 'lda_x', 'correlation':"lda_c_xalpha"}, libxc=True)

        This registration method does not modify the file immediately but only appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_xcfunctional()` to
        the list of tasks that will be done on the xmltree.
        """
        self._validate_arguments('set_xcfunctional', args, kwargs)
        self._tasks.append(ModifierTask('set_xcfunctional', args, kwargs))
