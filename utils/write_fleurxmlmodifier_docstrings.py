"""
Script to keep docstrings of XML setter functions and their corresponding methods
on the FleurXMLModifier in sync
Is used as a pre-commit hook
"""
from masci_tools.util.xml.collect_xml_setters import XPATH_SETTERS, NMMPMAT_SETTERS, SCHEMA_DICT_SETTERS
import inspect
import ast
import sys

from masci_tools.io import fleurxmlmodifier

ALL_SETTERS = {**XPATH_SETTERS, **NMMPMAT_SETTERS, **SCHEMA_DICT_SETTERS}
INDENT = 4


def get_method_docstring(func):
    """
    Get the corresponding method docstring of a given XML setter function

    This changes three things.
        - Strip out references to the arguments handled by the FleurXMLModifier
        - Add two standardized lines explaining the actual effect of callind the method
          (append an entry to the tasks)
        - Indentation is adjusted to two levels (function -> method)
    """

    lines = [line for line in func.__doc__.split('\n') \
                if all(x not in line for x in (':param xmltree:', ':param schema_dict:', ':param nmmplines:', ':returns'))]

    module_name = inspect.getmodule(func).__name__
    additional_lines = [
        INDENT * ' ' + f'Appends a :py:func:`~{module_name}.{func.__name__}()` to',
        INDENT * ' ' + 'the list of tasks that will be done on the xmltree.', INDENT * ' '
    ]
    if lines[0]:
        lines[0] = INDENT * ' ' + lines[0]
        lines.insert(0, '')

    for line in reversed(additional_lines):
        lines.insert(1, line)

    while all(not line.strip() for line in lines[-2:]):
        lines.pop()
    lines = [INDENT * ' ' + line if line.strip() else line.lstrip() for line in lines]
    lines[-1] = 2 * INDENT * ' '
    #One level of indentation has to be added since the original docstrings are in functions
    #and the final ones should be in methods
    return '\n'.join(lines)


def rewrite_docstrings(module_file, modifier_class_name):
    """
    Rewrite all the docstrings of the XMl setter methods of the
    FleurXMLModifier class to be in sync with their corresponding functions
    """

    with open(module_file, encoding='utf-8') as f:
        content = f.read()
        module = ast.parse(content)
    class_definitions = [node for node in module.body if isinstance(node, ast.ClassDef)]
    method_definitions = []
    failed = False
    for class_def in class_definitions:
        if class_def.name != modifier_class_name:
            continue
        function_definitions = [node for node in class_def.body if isinstance(node, ast.FunctionDef)]
        for f in function_definitions:
            if f.name in ALL_SETTERS:
                try:
                    docstring = get_method_docstring(ALL_SETTERS[f.name])
                except Exception as exc:  #pylint: disable=broad-except
                    print(f'Docstring generation failed for: {f.name} ({exc})')
                    failed = True
                    continue
                old_docstring = ast.get_docstring(f, clean=False)
                if old_docstring != docstring:
                    print(f'Rewriting docstring of method: {f.name}')
                    content = content.replace(old_docstring, docstring)

    with open(module_file, 'w', encoding='utf-8') as f:
        f.write(content)

    if failed:
        sys.exit(1)


if __name__ == '__main__':
    rewrite_docstrings(fleurxmlmodifier.__file__, 'FleurXMLModifier')
