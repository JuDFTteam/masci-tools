"""
Spinx extension for masci-tools

This adds the ability for giving usage examples atm specific
to the FleurXMLModifier. A template can be given, which is filled
in with the options and content from `usage-example` directives in
the docstrings of the specified methods

Example of the usage-example directive without a connected template.

.. usage-example::
    :title: This is how it's done
    :description: Simply do the stuff

    print('Hello World')

"""
from .usage_examples import UsageExampleBlock, generate_usage_example_files, DEFAULT_CONF


def setup(app):
    """
    This function sets up the Sphinx extension. It is called, when
    ``masci_tools.util.sphinxext`` is added to the extensions in a conf.py file
    """

    app.add_config_value('usage_examples_conf', DEFAULT_CONF, 'html')

    app.add_directive('usage-example', UsageExampleBlock)
    # app.add_directive('usage-example-gallery', UsageExampleGallery)

    app.connect('builder-inited', generate_usage_example_files)
