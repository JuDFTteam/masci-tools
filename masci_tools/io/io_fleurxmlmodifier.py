from collections import namedtuple
from lxml import etree
import copy

ModifierTask = namedtuple('ModifierTask', ['name', 'args', 'kwargs'])

class FleurXMLModifier:

    def __init__(self):
        self._tasks = []

    @staticmethod
    def apply_modifications(xmltree, nmmp_lines, modification_tasks, validate_changes=True):
        """
        Applies given modifications to the fleurinp lxml tree.
        It also checks if a new lxml tree is validated against schema.
        Does not rise an error if inp.xml is not validated, simple prints a message about it.

        :param xmltree: a lxml tree to be modified (IS MODIFIED INPLACE)
        :param n_mmp_lines: a n_mmp_mat file to be modified (IS MODIFIED INPLACE)
        :param modification_tasks: a list of modification tuples

        :returns: a modified lxml tree and a modified n_mmp_mat file
        """
        from masci_tools.util.xml.collect_xml_setters import XPATH_SETTERS, SCHEMA_DICT_SETTERS
        from masci_tools.util.xml.common_xml_util import validate_xml, eval_xpath
        from masci_tools.io.parsers.fleur.fleur_schema import InputSchemaDict

        version = eval_xpath(new_xmltree, '//@fleurInputVersion')
        version = str(version)
        if version is None:
            raise ValueError('Failed to extract inputVersion')

        schema_dict = InputSchemaDict.fromVersion(version)

        for task in modification_tasks:
            if task.name in XPATH_SETTERS:
                action = XPATH_SETTERS[task.name]
                xmltree = action(xmltree, *task.args, **task.kwargs)

            elif task.name in SCHEMA_DICT_SETTERS:
                action = SCHEMA_DICT_SETTERS[task.name]
                xmltree = action(xmltree, schema_dict, *task.args, **task.kwargs)

            else:
                raise ValueError(f'Unknown task {task.name}')

        if validate_changes:
            validate_xml(xmltree, schema_dict.xmlschema, error_header='Changes were not valid')


    def get_avail_actions(self):
        """
        Returns the allowed functions from FleurXMLModifier
        """
        outside_actions = {
            'set_inpchanges': self.set_inpchanges,
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

        self.modify_xmlfile(new_xmltree, new_nmmp_lines, self._tasks, inpschema)

        return new_xmltree, new_nmmp_lines



