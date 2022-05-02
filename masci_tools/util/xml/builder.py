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
from __future__ import annotations

from lxml.builder import ElementMaker  #pylint: disable=no-name-in-module
from lxml import etree

from masci_tools.util.xml.converters import convert_to_xml
from masci_tools.io.parsers.fleur_schema import InputSchemaDict, SchemaDict

from typing import Any, Callable, Iterable


class FleurElementMaker(ElementMaker):  #type: ignore[misc]
    """
    Class to create XML elements for fleur XML files
    utilizing the schema dict.
    For more information refer to the lxml documentation
    on :py:class:`lxml.builder.ElementMaker`

    :param schema_dict: InputSchemaDict to use for validation/conversion
    :param typemap: dict to add functions to handle given types
    :param namespace: str of the xml namespace to use
    :param nsmap: mapping between namespace names and uris
    :param makeelement: optional function to construct XML elements

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

    @classmethod
    def fromVersion(cls, version: str, **kwargs: Any) -> FleurElementMaker:
        """
        Create a FleurElementMaker for the given input version

        :param version: version string
        """

        schema_dict = InputSchemaDict.fromVersion(version)
        return cls(schema_dict, **kwargs)

    def __init__(self,
                 schema_dict: SchemaDict,
                 typemap: dict | None = None,
                 namespace: str | None = None,
                 nsmap: dict[str, str] | None = None,
                 makeelement: Callable | None = None) -> None:
        super().__init__(typemap=typemap, namespace=namespace, nsmap=nsmap, makeelement=makeelement)
        self.schema_dict = schema_dict

    def __call__(self,
                 tag: str,
                 *children: Any,
                 contains: str | Iterable[str] | None = None,
                 not_contains: str | Iterable[str] | None = None,
                 **attrib: Any) -> etree._Element:
        """
        Construct a element with the given tag, text children tags and attributes

        Args are used to set child elements if they are `etree._Element` or text of the given tag
        Kwargs are used to set attributes on the given tag

        :param tag: str of the tag name. Is passed to :py:meth:`masci_tools.io.parsers.fleur_schema.InputSchemaDict.tag_xpath()`
        :param contains: specification of the tag name. Is passed to :py:meth:`masci_tools.io.parsers.fleur_schema.InputSchemaDict.tag_xpath()`
        :param not_contains: specification of the tag name. Is passed to :py:meth:`masci_tools.io.parsers.fleur_schema.InputSchemaDict.tag_xpath()`

        :returns: `etree._Element` constructed from the given information
        """
        tag_info = self.schema_dict.tag_info(tag, contains=contains, not_contains=not_contains)
        tag = tag_info['name']  #original case

        children_converted = list(children)
        for indx, child in enumerate(children_converted):
            if isinstance(child, str) or etree.iselement(child):
                continue
            value, success = convert_to_xml(child, self.schema_dict, tag, text=True)
            if not success:
                raise ValueError(
                    f'Failed to convert value `{value}` for text of {tag}. The types are probably not right')
            children_converted[indx] = value

        #convert attributes
        attrib_converted = {}
        for key, value in attrib.items():

            if key not in tag_info['attribs']:
                raise KeyError(f'The attribute {key} is not allowed for the given tag {tag}')

            attrib_name = tag_info['attribs'].original_case[key]
            if not isinstance(value, str):
                value, success = convert_to_xml(value, self.schema_dict, attrib_name)
                if not success:
                    raise ValueError(
                        f'Failed to convert value `{value}` for attribute {attrib_name}. The types are probably not right'
                    )

            attrib_converted[attrib_name] = value

        return super().__call__(tag, *children_converted, **attrib_converted)
