"""
Script to keep docstrings of XML setter functions and their corresponding methods
on the FleurXMLModifier in sync
Is used as a pre-commit hook
"""
import ast
import sys
from pathlib import Path

INDENT = 4
MASCI_TOOLS_PATH = Path(__file__).parent.parent / 'masci_tools'


def get_method_docstring(name, docstring, module):
    """
    Get the corresponding method docstring of a given XML setter function

    This changes three things.
        - Strip out references to the arguments handled by the FleurXMLModifier
        - Add two standardized lines explaining the actual effect of callind the method
          (append an entry to the tasks)
        - Indentation is adjusted to two levels (function -> method)
    """

    lines = [line for line in docstring.split('\n') \
                if all(x not in line for x in (':param xmltree:', ':param schema_dict:', ':param nmmplines:', ':returns'))]

    additional_lines = [
        f'Appends a :py:func:`~masci_tools.util.xml.{module}.{name}()` to',
        'the list of tasks that will be done on the xmltree.', ''
    ]
    if lines[0]:
        lines.insert(0, '')
    if lines[-1]:
        lines.append('')

    for line in reversed(additional_lines):
        lines.insert(1, line)

    while all(not line.strip() for line in lines[-2:]):
        lines.pop()
    lines = [2 * INDENT * ' ' + line if line.strip() else line.lstrip() for line in lines]
    lines[-1] = 2 * INDENT * ' '
    #Two levels of indentation have to be added since the docstrings go into methods
    return '\n'.join(lines)


def rewrite_docstrings(module_file, modifier_class_name, setters, modules):
    """
    Rewrite all the docstrings of the XMl setter methods of the
    FleurXMLModifier class to be in sync with their corresponding functions
    """

    with open(module_file, encoding='utf-8') as f:
        content = f.read()
        module = ast.parse(content)
    class_definitions = [node for node in module.body if isinstance(node, ast.ClassDef)]

    failed = False
    for class_def in class_definitions:
        if class_def.name != modifier_class_name:
            continue
        function_definitions = [node for node in class_def.body if isinstance(node, ast.FunctionDef)]
        for f in function_definitions:
            if f.name in setters:
                try:
                    docstring = get_method_docstring(f.name, setters[f.name], modules[f.name])
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


def gather_setter_functions(module_names, collection_file):
    """
    Gather all setter functions that are imported in collect_xml_setters
    """

    setter_files = [MASCI_TOOLS_PATH / f'util/xml/{name}.py' for name in module_names]
    docstrings = {}

    for file in setter_files:
        with open(file, encoding='utf-8') as f:
            module = ast.parse(f.read())

        function_definitions = [node for node in module.body if isinstance(node, ast.FunctionDef)]
        for f in function_definitions:
            docstrings[f.name] = ast.get_docstring(f)

    with open(collection_file, encoding='utf-8') as f:
        module = ast.parse(f.read())

    imports = [node for node in module.body if isinstance(node, ast.ImportFrom)]

    collected_docstrings = {}
    modules = {}

    for import_stmt in imports:
        if import_stmt.module in module_names:
            for alias in import_stmt.names:
                collected_docstrings[alias.name] = docstrings[alias.name]
                modules[alias.name] = import_stmt.module

    return collected_docstrings, modules


if __name__ == '__main__':

    setter_module_names = ('xml_setters_names', 'xml_setters_nmmpmat', 'xml_setters_basic')
    setter_docstrings, setter_modules = gather_setter_functions(setter_module_names,
                                                                MASCI_TOOLS_PATH / 'util/xml/collect_xml_setters.py')
    rewrite_docstrings(MASCI_TOOLS_PATH / 'io/fleurxmlmodifier.py', 'FleurXMLModifier', setter_docstrings,
                       setter_modules)
