# -*- coding: utf-8 -*-
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
from collections import namedtuple
from lxml import etree
import copy
#Enable warnings for missing docstrings
#pylint: enable=missing-function-docstring

ModifierTask = namedtuple('ModifierTask', ['name', 'args', 'kwargs'])


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

    def __init__(self):
        self._tasks = []

    @staticmethod
    def apply_modifications(xmltree, nmmp_lines, modification_tasks, validate_changes=True, extra_funcs=None):
        """
        Applies given modifications to the fleurinp lxml tree.
        It also checks if a new lxml tree is validated against schema.
        Does not rise an error if inp.xml is not validated, simple prints a message about it.

        :param xmltree: a lxml tree to be modified (IS MODIFIED INPLACE)
        :param nmmp_lines: a n_mmp_mat file to be modified (IS MODIFIED INPLACE)
        :param modification_tasks: a list of modification tuples

        :returns: a modified lxml tree and a modified n_mmp_mat file
        """
        from masci_tools.util.xml.collect_xml_setters import XPATH_SETTERS, SCHEMA_DICT_SETTERS, NMMPMAT_SETTERS
        from masci_tools.util.xml.common_xml_util import validate_xml, eval_xpath
        from masci_tools.util.xml.xml_setters_nmmpmat import validate_nmmpmat
        from masci_tools.io.parsers.fleur.fleur_schema import InputSchemaDict

        version = eval_xpath(xmltree, '//@fleurInputVersion')
        version = str(version)
        if version is None:
            raise ValueError('Failed to extract inputVersion')

        schema_dict = InputSchemaDict.fromVersion(version)

        xpath_functions = copy.deepcopy(XPATH_SETTERS)
        schema_dict_functions = copy.deepcopy(SCHEMA_DICT_SETTERS)
        nmmpmat_functions = copy.deepcopy(NMMPMAT_SETTERS)

        if extra_funcs is not None:
            xpath_functions.update(extra_funcs.get('xpath'))
            schema_dict_functions.update(extra_funcs.get('schema_dict'))
            nmmpmat_functions.update(extra_funcs.get('nmmpmat'))

        for task in modification_tasks:
            if task.name in xpath_functions:
                action = xpath_functions[task.name]
                xmltree = action(xmltree, *task.args, **task.kwargs)

            elif task.name in schema_dict_functions:
                action = schema_dict_functions[task.name]
                xmltree = action(xmltree, schema_dict, *task.args, **task.kwargs)

            elif task.name in nmmpmat_functions:
                action = nmmpmat_functions[task.name]
                xmltree = action(xmltree, nmmp_lines, schema_dict, *task.args, **task.kwargs)

            else:
                raise ValueError(f'Unknown task {task.name}')

        if validate_changes:
            validate_xml(xmltree, schema_dict.xmlschema, error_header='Changes were not valid')

            try:
                validate_nmmpmat(xmltree, nmmp_lines, schema_dict)
            except ValueError as exc:
                msg = f'Changes were not valid (n_mmp_mat file is not compatible): {modification_tasks}'
                raise ValueError(msg) from exc

    def get_avail_actions(self):
        """
        Returns the allowed functions from FleurXMLModifier
        """
        outside_actions = {
            'set_inpchanges': self.set_inpchanges,
            'shift_value': self.shift_value,
            'set_species': self.set_species,
            'set_species_label': self.set_species_label,
            'shift_value_species_label': self.shift_value_species_label,
            'set_atomgroup': self.set_atomgroup,
            'set_atomgroup_label': self.set_atomgroup_label,
            'set_complex_tag': self.shift_value,
            'set_simple_tag': self.set_simple_tag,
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
        }
        return outside_actions

    def set_inpchanges(self, *args, **kwargs):
        """
        Appends a :py:func:`~masci_tools.util.xml.xml_setters_names.set_inpchanges()` to
        the list of tasks that will be done on the xmltree.

        :param change_dict: a dictionary with changes

        An example of change_dict::

            change_dict = {'itmax' : 1,
                           'l_noco': True,
                           'ctail': False,
                           'l_ss': True}
        """
        self._tasks.append(ModifierTask('set_inpchanges', args, kwargs))

    def shift_value(self, *args, **kwargs):
        self._tasks.append(ModifierTask('shift_value', args, kwargs))

    def set_species(self, *args, **kwargs):
        self._tasks.append(ModifierTask('set_species', args, kwargs))

    def set_species_label(self, *args, **kwargs):
        self._tasks.append(ModifierTask('set_species_label', args, kwargs))

    def shift_value_species_label(self, *args, **kwargs):
        self._tasks.append(ModifierTask('shift_value_species_label', args, kwargs))

    def set_atomgroup(self, *args, **kwargs):
        self._tasks.append(ModifierTask('set_atomgroup', args, kwargs))

    def set_atomgroup_label(self, *args, **kwargs):
        self._tasks.append(ModifierTask('set_atomgroup_label', args, kwargs))

    def create_tag(self, *args, **kwargs):
        self._tasks.append(ModifierTask('create_tag', args, kwargs))

    def set_complex_tag(self, *args, **kwargs):
        self._tasks.append(ModifierTask('set_complex_tag', args, kwargs))

    def set_simple_tag(self, *args, **kwargs):
        self._tasks.append(ModifierTask('set_simple_tag', args, kwargs))

    def set_text(self, *args, **kwargs):
        self._tasks.append(ModifierTask('set_text', args, kwargs))

    def set_first_text(self, *args, **kwargs):
        self._tasks.append(ModifierTask('set_first_text', args, kwargs))

    def set_attrib_value(self, *args, **kwargs):
        self._tasks.append(ModifierTask('set_attrib_value', args, kwargs))

    def set_first_attrib_value(self, *args, **kwargs):
        self._tasks.append(ModifierTask('set_first_attrib_value', args, kwargs))

    def add_number_to_attrib(self, *args, **kwargs):
        self._tasks.append(ModifierTask('add_number_to_attrib', args, kwargs))

    def add_number_to_first_attrib(self, *args, **kwargs):
        self._tasks.append(ModifierTask('add_number_to_first_attrib', args, kwargs))

    def xml_create_tag(self, *args, **kwargs):
        self._tasks.append(ModifierTask('xml_create_tag', args, kwargs))

    def xml_replace_tag(self, *args, **kwargs):
        self._tasks.append(ModifierTask('xml_replace_tag', args, kwargs))

    def xml_delete_tag(self, *args, **kwargs):
        self._tasks.append(ModifierTask('xml_delete_tag', args, kwargs))

    def xml_delete_att(self, *args, **kwargs):
        self._tasks.append(ModifierTask('xml_delete_att', args, kwargs))

    def xml_set_attrib_value_no_create(self, *args, **kwargs):
        self._tasks.append(ModifierTask('xml_set_attrib_value_no_create', args, kwargs))

    def xml_set_text_no_create(self, *args, **kwargs):
        self._tasks.append(ModifierTask('xml_set_text_no_create', args, kwargs))

    def set_nmmpmat(self, *args, **kwargs):
        self._tasks.append(ModifierTask('set_nmmpmat', args, kwargs))

    def rotate_nmmpmat(self, *args, **kwargs):
        self._tasks.append(ModifierTask('rotate_nmmpmat', args, kwargs))

    def undo(self, revert_all=False):
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

    def changes(self):
        """
        Prints out all changes given in a
        :class:`~masci_tools.io.io_fleurxmlmodifier.FleurXMLModifier` instance.
        """
        from pprint import pprint
        pprint(self._tasks)
        return self._tasks

    def modify_xmlfile(self, original_inpxmlfile, original_nmmp_file=None):

        if isinstance(original_inpxmlfile, etree._ElementTree):
            original_xmltree = original_inpxmlfile
        else:
            parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8')
            try:
                original_xmltree = etree.parse(original_inpxmlfile, parser)
            except etree.XMLSyntaxError as msg:
                raise ValueError(f'Failed to parse input file: {msg}') from msg

        if original_nmmp_file is not None:
            if isinstance(original_nmmp_file, str):
                with open(original_nmmp_file, mode='r') as n_mmp_file:
                    original_nmmp_lines = n_mmp_file.read().split('\n')
            else:
                original_nmmp_lines = original_nmmp_file
        else:
            original_nmmp_lines = None

        new_xmltree = copy.deepcopy(original_xmltree)
        new_nmmp_lines = copy.deepcopy(original_nmmp_lines)

        self.apply_modifications(new_xmltree, new_nmmp_lines, self._tasks)

        if new_nmmp_lines is None:
            return new_xmltree
        else:
            return new_xmltree, new_nmmp_lines
