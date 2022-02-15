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
"""
from __future__ import annotations

from typing import Any, Callable, NamedTuple
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  #type: ignore

from masci_tools.util.xml.collect_xml_setters import XPATH_SETTERS, SCHEMA_DICT_SETTERS, NMMPMAT_SETTERS
from masci_tools.io.io_fleurxml import load_inpxml
from masci_tools.util.typing import XMLFileLike, FileLike
from pathlib import Path
from lxml import etree
#Enable warnings for missing docstrings
#pylint: enable=missing-function-docstring


class ModifierTask(NamedTuple):
    name: str
    args: tuple[Any, ...]
    kwargs: dict[str, Any]


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
        new_xmltree = fmode.modify_xmlfile('/path/to/input/file/inp.xml')

    """

    _xpath_functions: dict[str, Callable] = XPATH_SETTERS
    _schema_dict_functions: dict[str, Callable] = SCHEMA_DICT_SETTERS
    _nmmpmat_functions: dict[str, Callable] = NMMPMAT_SETTERS

    _extra_functions: dict[str, dict[Literal['xpath', 'schema_dict', 'nmmpmat'], Callable]] = {}

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
        Validate that the given arguments to the registration
        method can be used to call the corresponding XML modifying function
        """
        from inspect import signature

        if self.validate_signatures:

            if name in self.xpath_functions:
                func = self.xpath_functions[name]
                prefix: tuple[str, ...] = ('xmltree',)
            elif name in self.schema_dict_functions:
                func = self.schema_dict_functions[name]
                prefix = ('xmltree', 'schema_dict')
            elif name in self.nmmpmat_functions:
                func = self.nmmpmat_functions[name]
                prefix = ('xmltree', 'schema_dict', 'n_mmp_mat')

            if func is None:
                raise ValueError(f'Failed to validate setter {name}. Maybe the function was'
                                 'not registered in masci_tools.util.xml.collect_xml_setters')

            #For functions decorated with the schema_dict_version_dispatch
            #We check only the default (This function should have a compatible signature for all registered functions)
            if getattr(func, 'registry', None) is not None:
                func = func.registry['default']

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
                            validate_changes: bool = True) -> tuple[etree._ElementTree, list[str] | None]:
        """
        Applies given modifications to the fleurinp lxml tree.
        It also checks if a new lxml tree is validated against schema.
        Does not rise an error if inp.xml is not validated, simple prints a message about it.

        :param xmltree: a lxml tree to be modified (IS MODIFIED INPLACE)
        :param nmmp_lines: a n_mmp_mat file to be modified (IS MODIFIED INPLACE)
        :param modification_tasks: a list of modification tuples
        :param validate_changes: bool optional (default True), if True after all tasks are performed
                                 both the xmltree and nmmp_lines are checked for consistency

        :returns: a modified lxml tree and a modified n_mmp_mat file
        """
        from masci_tools.util.xml.common_functions import validate_xml, eval_xpath
        from masci_tools.util.xml.xml_setters_nmmpmat import validate_nmmpmat
        from masci_tools.io.parsers.fleur_schema import InputSchemaDict

        version = eval_xpath(xmltree, '//@fleurInputVersion')
        version = str(version)
        if version is None:
            raise ValueError('Failed to extract inputVersion')

        schema_dict = InputSchemaDict.fromVersion(version)

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
            validate_xml(xmltree, schema_dict.xmlschema, error_header='Changes were not valid')

            try:
                validate_nmmpmat(xmltree, nmmp_lines, schema_dict)
            except ValueError as exc:
                msg = f'Changes were not valid (n_mmp_mat file is not compatible): {modification_tasks}'
                raise ValueError(msg) from exc

        return xmltree, nmmp_lines

    def get_avail_actions(self) -> dict[str, Callable]:
        """
        Returns the allowed functions from FleurXMLModifier
        """
        outside_actions = {
            'set_inpchanges': self.set_inpchanges,
            'shift_value': self.shift_value,
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
            'set_nkpts': self.set_nkpts,
            'set_kpath': self.set_kpath,
            'set_kpointlist': self.set_kpointlist,
            'switch_kpointset': self.switch_kpointset,
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
                       validate_changes: bool = True) -> tuple[etree._ElementTree, list[str]] | etree._ElementTree:
        """
        Applies the registered modifications to a given inputfile

        :param original_inpxmlfile: either path to the inp.xml file, opened file handle
                                    or a xml etree to be parsed
        :param original_nmmp_file: path or list of str to a corresponding density matrix
                                   file

        :raises ValueError: if the parsing of the input file

        :returns: a modified xmltree and if existent a modified density matrix file
        """
        original_xmltree, _ = load_inpxml(original_inpxmlfile)

        if original_nmmp_file is not None:
            if isinstance(original_nmmp_file, (str, Path)):
                with open(original_nmmp_file, encoding='utf-8') as n_mmp_file:
                    original_nmmp_lines = n_mmp_file.read().split('\n')
            else:
                original_nmmp_lines = original_nmmp_file
        else:
            original_nmmp_lines = None

        new_xmltree, new_nmmp_lines = self.apply_modifications(original_xmltree,
                                                               original_nmmp_lines,
                                                               self._tasks,
                                                               validate_changes=validate_changes)

        if new_nmmp_lines is None:
            return new_xmltree
        return new_xmltree, new_nmmp_lines

    def set_inpchanges(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_inpchanges()` to
        the list of tasks that will be done on the xmltree.

        :param change_dict: a dictionary with changes
        :param path_spec: dict, with ggf. necessary further specifications for the path of the attribute

        An example of change_dict::

            change_dict = {'itmax' : 1,
                           'l_noco': True,
                           'ctail': False,
                           'l_ss': True}
        """
        self._validate_signature('set_inpchanges', *args, **kwargs)
        self._tasks.append(ModifierTask('set_inpchanges', args, kwargs))

    def shift_value(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.shift_value()` to
        the list of tasks that will be done on the xmltree.

        :param change_dict: a python dictionary with the keys to shift and the shift values.
        :param mode: 'abs' if change given is absolute, 'rel' if relative
        :param path_spec: dict, with ggf. necessary further specifications for the path of the attribute

        An example of change_dict::

                change_dict = {'itmax' : 1, 'dVac': -0.123}
        """
        self._validate_signature('shift_value', *args, **kwargs)
        self._tasks.append(ModifierTask('shift_value', args, kwargs))

    def set_species(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_species()` to
        the list of tasks that will be done on the xmltree.

        :param species_name: string, name of the specie you want to change
                             Can be name of the species, 'all' or 'all-<string>' (sets species with the string in the species name)
        :param attributedict: a python dict specifying what you want to change.
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
        :param create: bool, if species does not exist create it and all subtags?

        **attributedict** is a python dictionary containing dictionaries that specify attributes
        to be set inside the certain specie. For example, if one wants to set a MT radius it
        can be done via::

            attributedict = {'mtSphere' : {'radius' : 2.2}}

        Another example::

            'attributedict': {'special': {'socscale': 0.0}}

        that switches SOC terms on a sertain specie. ``mtSphere``, ``atomicCutoffs``,
        ``energyParameters``, ``lo``, ``electronConfig``, ``nocoParams``, ``ldaU`` and
        ``special`` keys are supported. To find possible
        keys of the inner dictionary please refer to the FLEUR documentation flapw.de
        """
        self._validate_signature('set_species', *args, **kwargs)
        self._tasks.append(ModifierTask('set_species', args, kwargs))

    def set_species_label(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_species_label()` to
        the list of tasks that will be done on the xmltree.

        :param atom_label: string, a label of the atom which specie will be changed. 'all' to change all the species
        :param attributedict: a python dict specifying what you want to change.

        """
        self._validate_signature('set_species_label', *args, **kwargs)
        self._tasks.append(ModifierTask('set_species_label', args, kwargs))

    def clone_species(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.clone_species()` to
        the list of tasks that will be done on the xmltree.

        :param species_name: string, name of the specie you want to clone
                            Has to correspond to one single species (no 'all'/'all-<search_string>')
        :param new_name: new name of the cloned species
        :param changes: a optional python dict specifying what you want to change.
        """
        self._validate_signature('clone_species', *args, **kwargs)
        self._tasks.append(ModifierTask('clone_species', args, kwargs))

    def switch_species(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.switch_species()` to
        the list of tasks that will be done on the xmltree.

        :param new_species_name: name of the species to switch to
        :param position: position of an atom group to be changed. If equals to 'all', all species will be changed
        :param species: atom groups, corresponding to the given species will be changed
        :param clone: if True and the new species name does not exist and it corresponds to changing
                  from one species the species will be cloned with :py:func:`clone_species()`
        :param changes: changes to do if the species is cloned
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details`
        """
        self._validate_signature('switch_species', *args, **kwargs)
        self._tasks.append(ModifierTask('switch_species', args, kwargs))

    def switch_species_label(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.switch_species_label()` to
        the list of tasks that will be done on the xmltree.

        :param atom_label: string, a label of the atom which group will be changed. 'all' to change all the groups
        :param new_species_name: name of the species to switch to
        :param clone: if True and the new species name does not exist and it corresponds to changing
                  from one species the species will be cloned with :py:func:`clone_species()`
        :param changes: changes to do if the species is cloned
        """
        self._validate_signature('switch_species_label', *args, **kwargs)
        self._tasks.append(ModifierTask('switch_species_label', args, kwargs))

    def shift_value_species_label(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.shift_value_species_label()` to
        the list of tasks that will be done on the xmltree.

        :param atom_label: string, a label of the atom which specie will be changed. 'all' if set up all species
        :param attributename: name of the attribute to change
        :param value_given: value to add or to multiply by
        :param mode: 'rel' for multiplication or 'abs' for addition

        Kwargs if the attributename does not correspond to a unique path:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path

        """
        self._validate_signature('shift_value_species_label', *args, **kwargs)
        self._tasks.append(ModifierTask('shift_value_species_label', args, kwargs))

    def set_atomgroup(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_atomgroup()` to
        the list of tasks that will be done on the xmltree.

        :param attributedict: a python dict specifying what you want to change.
        :param position: position of an atom group to be changed. If equals to 'all', all species will be changed
        :param species: atom groups, corresponding to the given species will be changed
        :param create: bool, if species does not exist create it and all subtags?
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

        **attributedict** is a python dictionary containing dictionaries that specify attributes
        to be set inside the certain specie. For example, if one wants to set a beta noco parameter it
        can be done via::

            'attributedict': {'nocoParams': {'beta': val}}

        """
        self._validate_signature('set_atomgroup', *args, **kwargs)
        self._tasks.append(ModifierTask('set_atomgroup', args, kwargs))

    def set_atomgroup_label(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_atomgroup_label()` to
        the list of tasks that will be done on the xmltree.

        :param atom_label: string, a label of the atom which specie will be changed. 'all' to change all the species
        :param attributedict: a python dict specifying what you want to change.
        :param create: bool, if species does not exist create it and all subtags?

        **attributedict** is a python dictionary containing dictionaries that specify attributes
        to be set inside the certain specie. For example, if one wants to set a beta noco parameter it
        can be done via::

            'attributedict': {'nocoParams': {'beta': val}}

        """
        self._validate_signature('set_atomgroup_label', *args, **kwargs)
        self._tasks.append(ModifierTask('set_atomgroup_label', args, kwargs))

    def create_tag(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.create_tag()` to
        the list of tasks that will be done on the xmltree.

        :param tag: str of the tag to create or etree Element with the same name
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param create_parents: bool optional (default False), if True and the given xpath has no results the
                               the parent tags are created recursively
        :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag.
                            By default all nodes are used.
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details


        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
        """
        self._validate_signature('create_tag', *args, **kwargs)
        self._tasks.append(ModifierTask('create_tag', args, kwargs))

    def delete_tag(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.delete_tag()` to
        the list of tasks that will be done on the xmltree.

        :param tag: str of the tag to delete
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param occurrences: int or list of int. Which occurrence of the parent nodes to delete a tag.
                            By default all nodes are used.
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details


        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
        """
        self._validate_signature('delete_tag', *args, **kwargs)
        self._tasks.append(ModifierTask('delete_tag', args, kwargs))

    def delete_att(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.delete_att()` to
        the list of tasks that will be done on the xmltree.

        :param tag: str of the attribute to delete
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param occurrences: int or list of int. Which occurrence of the parent nodes to delete a attribute.
                            By default all nodes are used.
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details


        Kwargs:
            :param tag_name: str, name of the tag where the attribute should be parsed
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param exclude: list of str, here specific types of attributes can be excluded
                            valid values are: settable, settable_contains, other
        """
        self._validate_signature('delete_att', *args, **kwargs)
        self._tasks.append(ModifierTask('delete_att', args, kwargs))

    def replace_tag(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.replace_tag()` to
        the list of tasks that will be done on the xmltree.

        :param tag: str of the tag to replace
        :param newelement: a new tag
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param occurrences: int or list of int. Which occurrence of the parent nodes to replace a tag.
                            By default all nodes are used.
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details


        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
        """
        self._validate_signature('replace_tag', *args, **kwargs)
        self._tasks.append(ModifierTask('replace_tag', args, kwargs))

    def set_complex_tag(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_complex_tag()` to
        the list of tasks that will be done on the xmltree.

        :param tag_name: name of the tag to set
        :param attributedict: Keys in the dictionary correspond to names of tags and the values are the modifications
                              to do on this tag (attributename, subdict with changes to the subtag, ...)
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param create: bool optional (default False), if True and the path, where the complex tag is
                       set does not exist it is created
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details


        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path

        """
        self._validate_signature('set_complex_tag', *args, **kwargs)
        self._tasks.append(ModifierTask('set_complex_tag', args, kwargs))

    def set_simple_tag(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_simple_tag()` to
        the list of tasks that will be done on the xmltree.

        :param tag_name: str name of the tag to modify/set
        :param changes: list of dicts or dict with the changes. Elements in list describe multiple tags.
                        Keys in the dictionary correspond to {'attributename': attributevalue}
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param create_parents: bool optional (default False), if True and the path, where the simple tags are
                               set does not exist it is created
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details


        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
        """
        self._validate_signature('set_simple_tag', *args, **kwargs)
        self._tasks.append(ModifierTask('set_simple_tag', args, kwargs))

    def set_text(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_text()` to
        the list of tasks that will be done on the xmltree.

        :param tag_name: str name of the tag, where the text should be set
        :param text: value or list of values to set
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.
        :param create: bool optional (default False), if True the tag is created if is missing
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details


        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path

        """
        self._validate_signature('set_text', *args, **kwargs)
        self._tasks.append(ModifierTask('set_text', args, kwargs))

    def set_first_text(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_first_text()` to
        the list of tasks that will be done on the xmltree.

        :param tag_name: str name of the tag, where the text should be set
        :param text: value or list of values to set
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param create: bool optional (default False), if True the tag is created if is missing
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details


        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path

        """
        self._validate_signature('set_first_text', *args, **kwargs)
        self._tasks.append(ModifierTask('set_first_text', args, kwargs))

    def set_attrib_value(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_attrib_value()` to
        the list of tasks that will be done on the xmltree.

        :param attributename: the attribute name to set
        :param attribv: value or list of values to set
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.
        :param create: bool optional (default False), if True the tag is created if is missing
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details


        Kwargs:
            :param tag_name: str, name of the tag where the attribute should be parsed
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param exclude: list of str, here specific types of attributes can be excluded
                            valid values are: settable, settable_contains, other

        """
        self._validate_signature('set_attrib_value', *args, **kwargs)
        self._tasks.append(ModifierTask('set_attrib_value', args, kwargs))

    def set_first_attrib_value(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_first_attrib_value()` to
        the list of tasks that will be done on the xmltree.

        :param attributename: the attribute name to set
        :param attribv: value or list of values to set
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param create: bool optional (default False), if True the tag is created if is missing
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details


        Kwargs:
            :param tag_name: str, name of the tag where the attribute should be parsed
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param exclude: list of str, here specific types of attributes can be excluded
                            valid values are: settable, settable_contains, other

        """
        self._validate_signature('set_first_attrib_value', *args, **kwargs)
        self._tasks.append(ModifierTask('set_first_attrib_value', args, kwargs))

    def add_number_to_attrib(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.add_number_to_attrib()` to
        the list of tasks that will be done on the xmltree.

        :param attributename: the attribute name to change
        :param add_number: number to add/multiply with the old attribute value
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param mode: str (either `rel` or `abs`).
                     `rel` multiplies the old value with `add_number`
                     `abs` adds the old value and `add_number`
        :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details


        Kwargs:
            :param tag_name: str, name of the tag where the attribute should be parsed
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param exclude: list of str, here specific types of attributes can be excluded
                            valid values are: settable, settable_contains, other

        """
        self._validate_signature('add_number_to_attrib', *args, **kwargs)
        self._tasks.append(ModifierTask('add_number_to_attrib', args, kwargs))

    def add_number_to_first_attrib(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.add_number_to_first_attrib()` to
        the list of tasks that will be done on the xmltree.

        :param attributename: the attribute name to change
        :param add_number: number to add/multiply with the old attribute value
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param mode: str (either `rel` or `abs`).
                     `rel` multiplies the old value with `add_number`
                     `abs` adds the old value and `add_number`
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details


        Kwargs:
            :param tag_name: str, name of the tag where the attribute should be parsed
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param exclude: list of str, here specific types of attributes can be excluded
                            valid values are: settable, settable_contains, other

        """
        self._validate_signature('add_number_to_first_attrib', *args, **kwargs)
        self._tasks.append(ModifierTask('add_number_to_first_attrib', args, kwargs))

    def xml_create_tag(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_basic.xml_create_tag()` to
        the list of tasks that will be done on the xmltree.

        :param xpath: a path where to place a new tag
        :param element: a tag name or etree Element to be created
        :param place_index: defines the place where to put a created tag
        :param tag_order: defines a tag order
        :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag.
                            By default all nodes are used.
        """
        self._validate_signature('xml_create_tag', *args, **kwargs)
        self._tasks.append(ModifierTask('xml_create_tag', args, kwargs))

    def xml_replace_tag(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_basic.xml_replace_tag()` to
        the list of tasks that will be done on the xmltree.

        :param xpath: a path to the tag to be replaced
        :param newelement: a new tag
        :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag.
                            By default all nodes are used.
        """
        self._validate_signature('xml_replace_tag', *args, **kwargs)
        self._tasks.append(ModifierTask('xml_replace_tag', args, kwargs))

    def xml_delete_tag(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_basic.xml_delete_tag()` to
        the list of tasks that will be done on the xmltree.

        :param xpath: a path to the tag to be deleted
        :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag.
                            By default all nodes are used.
        """
        self._validate_signature('xml_delete_tag', *args, **kwargs)
        self._tasks.append(ModifierTask('xml_delete_tag', args, kwargs))

    def xml_delete_att(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_basic.xml_delete_att()` to
        the list of tasks that will be done on the xmltree.

        :param xpath: a path to the attribute to be deleted
        :param attrib: the name of an attribute
        :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag.
                            By default all nodes are used.
        """
        self._validate_signature('xml_delete_att', *args, **kwargs)
        self._tasks.append(ModifierTask('xml_delete_att', args, kwargs))

    def xml_set_attrib_value_no_create(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_basic.xml_set_attrib_value_no_create()` to
        the list of tasks that will be done on the xmltree.

        :param xpath: a path where to set the attributes
        :param attributename: the attribute name to set
        :param attribv: value or list of values to set (if not str they will be converted with `str(value)`)
        :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.
        """
        self._validate_signature('xml_set_attrib_value_no_create', *args, **kwargs)
        self._tasks.append(ModifierTask('xml_set_attrib_value_no_create', args, kwargs))

    def xml_set_text_no_create(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_basic.xml_set_text_no_create()` to
        the list of tasks that will be done on the xmltree.

        :param xpath: a path where to set the attributes
        :param text: value or list of values to set (if not str they will be converted with `str(value)`)
        :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.
        """
        self._validate_signature('xml_set_text_no_create', *args, **kwargs)
        self._tasks.append(ModifierTask('xml_set_text_no_create', args, kwargs))

    def set_nmmpmat(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_nmmpmat.set_nmmpmat()` to
        the list of tasks that will be done on the xmltree.

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
        """
        self._validate_signature('set_nmmpmat', *args, **kwargs)
        self._tasks.append(ModifierTask('set_nmmpmat', args, kwargs))

    def rotate_nmmpmat(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_nmmpmat.rotate_nmmpmat()` to
        the list of tasks that will be done on the xmltree.

        :param species_name: string, name of the species you want to change
        :param orbital: integer, orbital quantum number of the LDA+U procedure to be modified
        :param phi: float, angle (radian), by which to rotate the density matrix
        :param theta: float, angle (radian), by which to rotate the density matrix
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
        """
        self._validate_signature('rotate_nmmpmat', *args, **kwargs)
        self._tasks.append(ModifierTask('rotate_nmmpmat', args, kwargs))

    def set_kpointlist(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_kpointlist()` to
        the list of tasks that will be done on the xmltree.

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
        """
        self._validate_signature('set_kpointlist', *args, **kwargs)
        self._tasks.append(ModifierTask('set_kpointlist', args, kwargs))

    def switch_kpointset(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.switch_kpointset()` to
        the list of tasks that will be done on the xmltree.

        .. warning::
            This method is only supported for input versions after the Max5 release

        :param list_name: name of the kPoint set to use
        """
        self._validate_signature('switch_kpointset', *args, **kwargs)
        self._tasks.append(ModifierTask('switch_kpointset', args, kwargs))

    def set_nkpts(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_nkpts()` to
        the list of tasks that will be done on the xmltree.

        .. warning::
            This method is only supported for input versions before the Max5 release

        :param count: number of k-points
        :param gamma: bool that controls if the gamma-point should be included
                      in the k-point mesh
        """
        self._validate_signature('set_nkpts', *args, **kwargs)
        self._tasks.append(ModifierTask('set_nkpts', args, kwargs))

    def set_kpath(self, *args: Any, **kwargs: Any) -> None:
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_kpath()` to
        the list of tasks that will be done on the xmltree.

        .. warning::
            This method is only supported for input versions before the Max5 release

        :param kpath: a dictionary with kpoint name as key and k point coordinate as value
        :param count: number of k-points
        :param gamma: bool that controls if the gamma-point should be included
                      in the k-point mesh
        """
        self._validate_signature('set_kpath', *args, **kwargs)
        self._tasks.append(ModifierTask('set_kpath', args, kwargs))
