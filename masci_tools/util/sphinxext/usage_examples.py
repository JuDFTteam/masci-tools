"""
Spinx extension for masci-tools

This adds the ability for giving usage examples atm specific
to the FleurXMLModifier. A template can be given, which is filled
in with the options and content from `usage-example` directives in
the docstrings of the specified methods
"""
import os
from pathlib import Path
import copy
import ast
from contextlib import redirect_stderr, contextmanager
import yaml
import io

from sphinx.util.logging import getLogger
from sphinx.errors import ConfigError, ExtensionError
from sphinx.util.docutils import register_directive
from sphinx.util.docutils import SphinxDirective

from docutils.core import publish_doctree
from docutils.parsers.rst.directives.body import CodeBlock
from docutils.parsers.rst import directives
from docutils import nodes
from docutils.parsers.rst.roles import set_classes
from docutils.utils.code_analyzer import Lexer, LexerError

from jinja2 import Environment, FileSystemLoader

logger = getLogger('masci-tools-usage-examples')

# yapf: disable
DEFAULT_CONF = {
    'template_dirs': os.path.join('..', 'usage_examples'),
    'template_file': 'template.md.jinja'
}
# yapf: enable

TEMPLATE_CONFIG_FILE = 'config.yml'
DEFAULT_TEMPLATE_CONFIG = {
    'module-file': None,  # Required
    'class-name': None,  # Required (TODO: Could be made optional if there's only one class definition)
    'exclude-methods': None,
    'include-private-methods': False,
    'output-folder': 'examples'
}


class UsageExampleBlock(SphinxDirective):
    """
    Directive for usage examples

    These are rendered as admonitions containing the
    optional description and title and the content in the
    form of a python code-block
    """

    final_argument_whitespace = True
    option_spec = {
        'class': directives.class_option,
        'name': directives.unchanged,
        'title': directives.unchanged,
        'description': directives.unchanged,
        'result': directives.unchanged,
        'inputfile': directives.unchanged,
    }
    has_content = True

    node_class = nodes.admonition
    """Subclasses must set this to the appropriate admonition node class."""

    def run(self):
        set_classes(self.options)
        self.assert_has_content()

        description = self.options.pop('description', '')
        title_text = self.options.pop('title', 'Simple Usage')
        for key in ('result', 'inputfile'):
            self.options.pop(key, None)

        admonition_node = self.node_class(description, **self.options)
        self.add_name(admonition_node)

        textnodes, messages = self.state.inline_text(title_text, self.lineno)
        title = nodes.title(title_text, '', *textnodes)
        title.source, title.line = (self.state_machine.get_source_and_line(self.lineno))
        admonition_node += title
        admonition_node += messages
        text_nodes, messages = self.state.inline_text(description.strip(), self.lineno)
        line = nodes.line(description, '', *text_nodes)
        admonition_node += line
        if not 'classes' in self.options:
            admonition_node['classes'] += ['admonition-' + nodes.make_id(title_text)]

        classes = ['code', 'python']

        # set up lexical analyzer
        try:
            tokens = Lexer('\n'.join(self.content), 'python', self.state.document.settings.syntax_highlight)
        except LexerError as error:
            raise self.warning(error)

        code_node = nodes.literal_block('\n'.join(self.content), classes=classes)
        self.add_name(code_node)

        # analyze content and add nodes for every token
        for classes, value in tokens:
            if classes:
                code_node += nodes.inline(value, value, classes=classes)
            else:
                # insert as Text to decrease the verbosity of the output
                code_node += nodes.Text(value)

        admonition_node += code_node

        return [admonition_node]


def generate_usage_example_files(app):
    """
    Generate the markdown files for the specified usage examples
    """
    logger.info('Generating usage examples ...')

    config = copy.deepcopy(DEFAULT_CONF)
    config.update(app.config.usage_examples_conf)

    for template_folder in config['template_dirs']:
        template_folder, template_conf = _load_template_conf(template_folder, app.builder.srcdir)
        usage_examples = _gather_usage_examples(**template_conf)
        _render_templates(template_folder, usage_examples, config, template_conf)


def _load_template_conf(template_folder, srcdir):
    """
    Load the configuration for the current template folder

    :param template_folder: Filepath to the folder containing the template
    :param srcdir: directory containing the conf.py
    """
    template_folder = Path(srcdir) / template_folder

    config = copy.deepcopy(DEFAULT_TEMPLATE_CONFIG)
    with open(template_folder / TEMPLATE_CONFIG_FILE, encoding='utf-8') as file:
        config.update(yaml.safe_load(file))

    if config['exclude-methods'] is not None:
        config['exclude-methods'] = set(config['exclude-methods'])

    if config['module-file'] is None:
        raise ConfigError(f'The template in {template_folder} does not define a module')
    config['module-file'] = template_folder / config['module-file']

    if config['class-name'] is None:
        raise ConfigError(f'The template in {template_folder} does not define a class')

    config = {k.replace('-', '_'): v for k, v in config.items()}
    return template_folder, config


def _render_templates(template_folder, usage_examples, config, template_config):
    """
    Render all usage-example with the specified jinja template

    :param template_folder: Filepath to the folder containing the template
    :param usage_examples: Dict of all usage examples
    :param config: global configuration of the extension
    :param template_config: configuration specific to the current template
    """
    template_env = Environment(
        loader=FileSystemLoader(template_folder),
        keep_trailing_newline=True,
        lstrip_blocks=True,
        trim_blocks=True,
    )

    for name, examples in usage_examples.items():
        if not examples:
            continue
        template = template_env.get_template(config['template_file'])

        output_folder = template_folder / template_config['output_folder']
        if not output_folder.exists():
            output_folder.mkdir()

        with open(output_folder / f'{name}.md', 'w', encoding='utf-8') as file:
            file.write(template.render(examples=examples, title=f'``{name}``'))
            logger.info('Rendered Usage example to "%s".', os.fspath(template_folder / f'{name}.md'))


def _gather_usage_examples(module_file, class_name, exclude_methods=None, include_private_methods=False, **kwargs):
    """
    Gather all usage-example blocks for the specified methods

    :param module_file: Filepath to the module to analyze
    :param class_name: Name of the class to analyze
    :param exclude_methods: set of str, these methods will not be analyzed
    :param include_private_methods: bool, if True methods starting with `_` will be analyzed

    :returns: dict mapping method names to the list of usage examples defined in it's docstring
    """

    class UsageExampleTemplateBlock(CodeBlock):
        """
        Dummy directive which extract the information
        of usage-example directives
        and collects them in a class variable for later use
        """

        #This directive should contain the template rendering logic
        #In conf.py another one will be defined, which creates a admonition
        # with code block
        option_spec = {
            'title': directives.unchanged,
            'description': directives.unchanged,
            'result': directives.unchanged,
            'inputfile': directives.unchanged,
        }
        has_content = True
        collected_examples = []

        def run(self):
            self.assert_has_content()

            self.options.setdefault('classes', []).append(
                'usage-example')  #For checking after the fact if there were usage examples provided

            example = {
                'title': self.options.get('title', 'Simple Usage'),
                'error': self.options.get('result', 'success').lower() == 'error',
                'inputfile': self.options.get('inputfile', 'inp.xml'),
                'code': '\n'.join(self.content)
            }
            if 'description' in self.options:
                example['description'] = self.options['description']
            self.collected_examples.append(example)
            return super().run()

        @classmethod
        def reset(cls):
            cls.collected_examples = []

    if exclude_methods is None:
        exclude_methods = set()

    with open(module_file, encoding='utf-8') as file:
        module = ast.parse(file.read())

    usage_examples = {}
    with patch_directive('usage-example', UsageExampleTemplateBlock):

        class_definitions = [node for node in module.body if isinstance(node, ast.ClassDef)]

        for class_def in class_definitions:
            if class_def.name == class_name:
                method_definition = [node for node in class_def.body if isinstance(node, ast.FunctionDef)]
                for method in method_definition:
                    if method.name in exclude_methods:
                        continue
                    if method.name.startswith('_') and not include_private_methods:
                        continue

                    docstring = ast.get_docstring(method, clean=True)
                    short_desc = ast.get_docstring(method, clean=False).split('\n')[0]

                    #Ignore unknown directive errors
                    with redirect_stderr(io.StringIO()):
                        publish_doctree(docstring)

                    method_examples = UsageExampleTemplateBlock.collected_examples
                    if len(method_examples) == 0:
                        logger.warning(f'Method {method.name} of class {class_name} has no usage-example')

                    for entry in method_examples:
                        if not 'description' in entry and short_desc:
                            entry['description'] = short_desc

                    usage_examples[method.name] = method_examples
                    UsageExampleTemplateBlock.reset()

    return usage_examples


@contextmanager
def patch_directive(name, directive):
    """
    Temporarily replace the directive of the given name
    with a different one
    """
    #pylint: disable=protected-access

    before = directives._directives.get(name, None)
    try:
        register_directive(name, directive)
        yield
    finally:
        directives._directives.pop(name)
        if before is not None:
            directives._directives[name] = before
