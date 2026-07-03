#
# Fleur plugin documentation build configuration file, created by
# sphinx-quickstart on Wed Dec  7 16:39:12 2016.
#
# This file is execfile()d with the current directory set to its
# containing dir.

import masci_tools
import os


# -- General configuration ------------------------------------------------

extensions = ['myst_nb',
              'sphinx.ext.autodoc',
              'sphinx.ext.doctest',
              'sphinx.ext.todo',
              'sphinx.ext.coverage',
              'sphinx.ext.imgmath',
              'sphinx.ext.ifconfig',
              'sphinx.ext.viewcode',
              'sphinx.ext.intersphinx',
              'sphinx_autodoc_typehints',
              'sphinx_design',
              'sphinx_copybutton',
              'sphinx_click',
              'masci_tools.util.sphinxext']

intersphinx_mapping = {'numpy': ('https://numpy.org/doc/stable/', None),
                       'python': ('https://docs.python.org/3', None),
                       'lxml': ('https://lxml.de/apidoc/',None),
                       'h5py': ('https://docs.h5py.org/en/latest/', None),
                       'pandas': ('http://pandas.pydata.org/pandas-docs/dev', None),
                       'spglib': ('http://spglib.github.io/spglib', None)}

myst_enable_extensions = ['colon_fence',
                          'fieldlist',
                          'dollarmath',
                          'deflist']

todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

usage_examples_conf = {
    'template_dirs': ['user_guide/fleurxmlmodifier_usage_examples']
}

autodoc_mock_imports = ['bokeh', '_typeshed']

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Masci-tools'
copyright = '2016-2021, Forschungszentrum Jülich GmbH, PGI-1/IAS-1 Quantum Theory of Materials'

version = '.'.join(masci_tools.__version__.split('.')[:2])
# The full version, including alpha/beta/rc tags.
release = masci_tools.__version__
author = 'The JuDFT team'

exclude_patterns = ['_build']
pygments_style = 'sphinx'


# -- Options for HTML output ---------------------------------------------

html_theme = 'default'
htmlhelp_basename = 'masci-toolsdoc'
# These folders are copied to the documentation's HTML output
html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'theme_overrides.css',
]
# on_rtd is whether we are on readthedocs.org, this line of code grabbed
# from docs.readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:  # only import and set the theme if we're building docs locally
    try:
        import sphinx_rtd_theme
        html_theme = 'sphinx_rtd_theme'
        html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
    except ImportError:
        # No sphinx_rtd_theme installed
        pass


# -- Options for LaTeX output ---------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  ('index', 'masci-tools.tex', 'Masci-tools Documentation',
   'The JuDFT team', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'masci-tools', 'Masci-tools Documentation',
     ['The JuDFT team'], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'masci-tools', 'Masci-tools Documentation',
   'The JuDFT team', 'masci-tools', 'Tools for Computational Material Science.',
   'Miscellaneous'),
]

# -- Options for Epub output ---------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = 'Masci-tools'
epub_author = author
epub_publisher = author
epub_copyright = copyright

# Warnings to ignore when using the -n (nitpicky) option
# We should ignore any python built-in exception, for instance
nitpick_ignore = [
    ('py:exc', 'ArithmeticError'),
    ('py:exc', 'AssertionError'),
    ('py:exc', 'AttributeError'),
    ('py:exc', 'BaseException'),
    ('py:exc', 'BufferError'),
    ('py:exc', 'DeprecationWarning'),
    ('py:exc', 'EOFError'),
    ('py:exc', 'EnvironmentError'),
    ('py:exc', 'Exception'),
    ('py:exc', 'FloatingPointError'),
    ('py:exc', 'FutureWarning'),
    ('py:exc', 'GeneratorExit'),
    ('py:exc', 'IOError'),
    ('py:exc', 'ImportError'),
    ('py:exc', 'ImportWarning'),
    ('py:exc', 'IndentationError'),
    ('py:exc', 'IndexError'),
    ('py:exc', 'KeyError'),
    ('py:exc', 'KeyboardInterrupt'),
    ('py:exc', 'LookupError'),
    ('py:exc', 'MemoryError'),
    ('py:exc', 'NameError'),
    ('py:exc', 'NotImplementedError'),
    ('py:exc', 'OSError'),
    ('py:exc', 'OverflowError'),
    ('py:exc', 'PendingDeprecationWarning'),
    ('py:exc', 'ReferenceError'),
    ('py:exc', 'RuntimeError'),
    ('py:exc', 'RuntimeWarning'),
    ('py:exc', 'StandardError'),
    ('py:exc', 'StopIteration'),
    ('py:exc', 'SyntaxError'),
    ('py:exc', 'SyntaxWarning'),
    ('py:exc', 'SystemError'),
    ('py:exc', 'SystemExit'),
    ('py:exc', 'TabError'),
    ('py:exc', 'TypeError'),
    ('py:exc', 'UnboundLocalError'),
    ('py:exc', 'UnicodeDecodeError'),
    ('py:exc', 'UnicodeEncodeError'),
    ('py:exc', 'UnicodeError'),
    ('py:exc', 'UnicodeTranslateError'),
    ('py:exc', 'UnicodeWarning'),
    ('py:exc', 'UserWarning'),
    ('py:exc', 'VMSError'),
    ('py:exc', 'ValueError'),
    ('py:exc', 'Warning'),
    ('py:exc', 'WindowsError'),
    ('py:exc', 'ZeroDivisionError'),
    ('py:obj', 'str'),
    ('py:obj', 'list'),
    ('py:obj', 'tuple'),
    ('py:obj', 'int'),
    ('py:obj', 'float'),
    ('py:obj', 'bool'),
    ('py:obj', 'Mapping'),
    ('py:obj', 'plum'),
    ('py:class', 'etree._XPathObject'),
    ('py:class', 'h5py._hl.group.Group'),
    ('py:class', 'TypeAlias'),
    ('py:class', 'contextlib._GeneratorContextManager'),
    ('py:data', 'masci_tools.io.parsers.fleur.fleur_outxml_parser.F'),
    ('py:class', 'np.ndarray')
]
