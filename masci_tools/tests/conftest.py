# -*- coding: utf-8 -*-
"""
Configurations for masci_tools tests
"""
import pytest


@pytest.fixture
def load_inpxml():
    """Returns the etree and schema_dict generator"""

    def _load_inpxml(path):
        from lxml import etree
        from masci_tools.io.parsers.fleur.fleur_schema import InputSchemaDict
        with open(path, 'r') as inpxmlfile:
            tree = etree.parse(inpxmlfile)
            version = str(tree.xpath('//@fleurInputVersion')[0])
            schema_dict = InputSchemaDict.fromVersion(version)
        return tree, schema_dict

    return _load_inpxml
