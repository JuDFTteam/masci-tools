"""
This module contains a helper class for creating Elements compatible with a given
input version of fleur from scratch

Example of creating a kpointlist

.. code-block:: python
    from masci_tools.util.xml.builder import FleurElementMaker

    E = FleurElementMaker.fromVersion('0.35')

    new_kpointset = E.kpointlist(
        *(
            E.kpoint(kpoint, weight=weight, label=special_labels[indx]) if indx in special_labels else
            E.kpoint(kpoint, weight=weight) for indx, (kpoint, weight) in enumerate(zip(kpoints, weights))
        ),
        name=name,
        count=nkpts,
        type=kpoint_type)

"""
from lxml.builder import ElementMaker  #pylint: disable=no-name-in-module
from lxml import etree

from masci_tools.util.xml.converters import convert_to_xml
from masci_tools.io.parsers.fleur_schema import InputSchemaDict


class FleurElementMaker(ElementMaker):  #type: ignore[misc]
    """
    Subclass to create XML elements for fleur XML files
    utilizing the schema dict
    """

    @classmethod
    def fromVersion(cls, version, **kwargs):

        schema_dict = InputSchemaDict.fromVersion(version)
        return cls(schema_dict, **kwargs)

    def __init__(self, schema_dict, typemap=None, namespace=None, nsmap=None, makeelement=None):
        super().__init__(typemap=typemap, namespace=namespace, nsmap=nsmap, makeelement=None)

        self.schema_dict = schema_dict

    def __call__(self, tag, *children, contains=None, not_contains=None, **attrib):

        tag_info = self.schema_dict.tag_info(tag, contains=contains, not_contains=not_contains)
        tag = tag_info['name']  #original case

        #Convert text
        children = [
            convert_to_xml(child, self.schema_dict, tag, text=True)[0]
            if not isinstance(child, str) and not etree.iselement(child) else child for child in children
        ]

        #convert attributes
        attrib_converted = {}
        for key, value in attrib.items():

            attrib_name = tag_info['attribs'].original_case[key]
            if not isinstance(value, str):
                value, _ = convert_to_xml(value, self.schema_dict, attrib_name)
            attrib_converted[attrib_name] = value

        return super().__call__(tag, *children, **attrib_converted)
