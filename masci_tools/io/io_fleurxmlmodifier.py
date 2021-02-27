from collections import namedtuple
from lxml import etree
import copy

ModifierTask = namedtuple('ModifierTask', ['name', 'args', 'kwargs'])

class FleurXMLModifier:

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
        from masci_tools.io.parsers.fleur.fleur_schema import InputSchemaDict

        version = eval_xpath(new_xmltree, '//@fleurInputVersion')
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
            'create_tag_xpath': self.create_tag_xpath,
            'replace_tag': self.replace_tag,
            'delete_tag': self.delete_tag,
            'delete_att': self.delete_att,
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

    def create_tag_xpath(self, *args, **kwargs):
        self._tasks.append(ModifierTask('create_tag_xpath', args, kwargs))

    def replace_tag(self, *args, **kwargs):
        self._tasks.append(ModifierTask('replace_tag', args, kwargs))

    def delete_tag(self, *args, **kwargs):
        self._tasks.append(ModifierTask('delete_tag', args, kwargs))

    def delete_att(self, *args, **kwargs):
        self._tasks.append(ModifierTask('delete_att', args, kwargs))

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
            if isinstance(original_nmmp_file, str)
                with open(original_nmmp_file, mode='r') as n_mmp_file:
                    original_nmmp_lines = n_mmp_file.read().split('\n')
            else:
                original_nmmp_lines = original_nmmp_file

        new_xmltree = copy.deepcopy(original_xmltree)
        new_nmmp_lines = copy.deepcopy(original_nmmp_lines)

        self.apply_modifications(new_xmltree, new_nmmp_lines, self._tasks, inpschema)

        return new_xmltree, new_nmmp_lines



