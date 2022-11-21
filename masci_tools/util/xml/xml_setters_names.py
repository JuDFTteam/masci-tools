###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools.   #
# For further information on the license, see the LICENSE.txt file.           #
# For further information please visit http://judft.de/.                      #
#                                                                             #
###############################################################################
"""
Functions for modifying the xml input file of Fleur utilizing the schema dict
and as little knowledge of the concrete xpaths as possible
"""
from __future__ import annotations

import warnings
from collections.abc import Collection
from typing import Any, Iterable
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  #type:ignore

from masci_tools.util.typing import XPathLike, XMLLike
from masci_tools.util.xml.xpathbuilder import XPathBuilder, FilterType
from masci_tools.util.xml.common_functions import process_xpath_argument
from masci_tools.io.parsers.fleur_schema import schema_dict_version_dispatch
from masci_tools.io.parsers import fleur_schema

from lxml import etree


def create_tag(xmltree: XMLLike,
               schema_dict: fleur_schema.SchemaDict,
               tag: etree.QName | str | etree._Element,
               complex_xpath: XPathLike | None = None,
               filters: FilterType | None = None,
               create_parents: bool = False,
               occurrences: int | Iterable[int] | None = None,
               **kwargs: Any) -> XMLLike:
    """
    This method creates a tag with a uniquely identified xpath under the nodes of its parent.
    If there are no nodes evaluated the subtags can be created with `create_parents=True`

    The tag is always inserted in the correct place if a order is enforced by the schema

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param tag: str of the tag to create or etree Element or string representing the XML element with the same name to insert
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
    :param create_parents: bool optional (default False), if True and the given xpath has no results the
                           the parent tags are created recursively
    :param occurrences: int or list of int. Which occurrence of the parent nodes to create a tag.
                        By default all nodes are used.

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: xmltree with created tags
    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_create_tag_schema_dict
    from masci_tools.util.xml.common_functions import split_off_tag, is_valid_tag

    if etree.iselement(tag):
        tag_name: str = tag.tag
    elif isinstance(tag, etree.QName):
        tag_name = tag.text
    elif is_valid_tag(tag):  #type:ignore[arg-type]
        tag_name = tag  #type:ignore[assignment]
    else:
        try:
            tag_name = etree.fromstring(tag).tag  #type:ignore[arg-type]
        except etree.XMLSyntaxError as exc:
            raise ValueError(f"Failed to construct etree Element from '{tag}'") from exc

    base_xpath = schema_dict.tag_xpath(tag_name, **kwargs)
    parent_xpath, tag_name = split_off_tag(base_xpath)
    complex_xpath = process_xpath_argument(parent_xpath, complex_xpath, filters)

    xmltree = xml_create_tag_schema_dict(xmltree,
                                         schema_dict,
                                         complex_xpath,
                                         parent_xpath,
                                         tag,
                                         create_parents=create_parents,
                                         occurrences=occurrences)

    return xmltree


def delete_tag(xmltree: XMLLike,
               schema_dict: fleur_schema.SchemaDict,
               tag_name: str,
               complex_xpath: XPathLike | None = None,
               filters: FilterType | None = None,
               occurrences: int | Iterable[int] | None = None,
               **kwargs: Any) -> XMLLike:
    """
    This method deletes a tag with a uniquely identified xpath.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param tag: str of the tag to delete
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
    :param occurrences: int or list of int. Which occurrence of the parent nodes to delete a tag.
                        By default all nodes are used.

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: xmltree with deleted tags
    """
    from masci_tools.util.xml.xml_setters_basic import xml_delete_tag
    from masci_tools.util.xml.common_functions import check_complex_xpath

    base_xpath = schema_dict.tag_xpath(tag_name, **kwargs)

    complex_xpath = process_xpath_argument(base_xpath, complex_xpath, filters)
    check_complex_xpath(xmltree, base_xpath, complex_xpath)

    return xml_delete_tag(xmltree, complex_xpath, occurrences=occurrences)


def delete_att(xmltree: XMLLike,
               schema_dict: fleur_schema.SchemaDict,
               name: str,
               complex_xpath: XPathLike | None = None,
               filters: FilterType | None = None,
               occurrences: int | Iterable[int] | None = None,
               **kwargs: Any) -> XMLLike:
    """
    This method deletes a attribute with a uniquely identified xpath.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param name: str of the attribute to delete
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
    :param occurrences: int or list of int. Which occurrence of the parent nodes to delete a attribute.
                        By default all nodes are used.

    Kwargs:
        :param tag_name: str, name of the tag where the attribute should be parsed
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param exclude: list of str, here specific types of attributes can be excluded
                        valid values are: settable, settable_contains, other

    :returns: xmltree with deleted attributes
    """
    from masci_tools.util.xml.xml_setters_basic import xml_delete_att
    from masci_tools.util.xml.common_functions import check_complex_xpath, split_off_attrib

    base_xpath = schema_dict.attrib_xpath(name, **kwargs)
    tag_xpath, name = split_off_attrib(base_xpath)

    complex_xpath = process_xpath_argument(tag_xpath, complex_xpath, filters)
    check_complex_xpath(xmltree, tag_xpath, complex_xpath)

    return xml_delete_att(xmltree, complex_xpath, name, occurrences=occurrences)


def replace_tag(xmltree: XMLLike,
                schema_dict: fleur_schema.SchemaDict,
                tag_name: str,
                element: str | etree._Element,
                complex_xpath: XPathLike | None = None,
                filters: FilterType | None = None,
                occurrences: int | Iterable[int] | None = None,
                **kwargs: Any) -> XMLLike:
    """
    This method deletes a tag with a uniquely identified xpath.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param tag: str of the tag to replace
    :param element: etree Element or string representing the XML element to replace the tag
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
    :param occurrences: int or list of int. Which occurrence of the parent nodes to replace a tag.
                        By default all nodes are used.

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: xmltree with replaced tags
    """
    from masci_tools.util.xml.xml_setters_basic import xml_replace_tag
    from masci_tools.util.xml.common_functions import check_complex_xpath

    base_xpath = schema_dict.tag_xpath(tag_name, **kwargs)

    complex_xpath = process_xpath_argument(base_xpath, complex_xpath, filters)
    check_complex_xpath(xmltree, base_xpath, complex_xpath)

    return xml_replace_tag(xmltree, complex_xpath, element, occurrences=occurrences)


def add_number_to_attrib(xmltree: XMLLike,
                         schema_dict: fleur_schema.SchemaDict,
                         name: str,
                         number_to_add: Any,
                         complex_xpath: XPathLike | None = None,
                         filters: FilterType | None = None,
                         mode: Literal['abs', 'absolute', 'rel', 'relative'] = 'absolute',
                         occurrences: int | Iterable[int] | None = None,
                         **kwargs: Any) -> XMLLike:
    """
    Adds a given number to the attribute value in a xmltree specified by the name of the attribute
    and optional further specification
    If there are no nodes under the specified xpath an error is raised

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param name: the attribute name to change
    :param number_to_add: number to add/multiply with the old attribute value
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
    :param mode: str (either `rel`/`relative` or `abs`/`absolute`).
                 `rel`/`relative` multiplies the old value with `number_to_add`
                 `abs`/`absolute` adds the old value and `number_to_add`
    :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.

    Kwargs:
        :param tag_name: str, name of the tag where the attribute should be parsed
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param exclude: list of str, here specific types of attributes can be excluded
                        valid values are: settable, settable_contains, other

    :returns: xmltree with shifted attribute
    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_add_number_to_attrib
    from masci_tools.util.xml.common_functions import split_off_attrib

    attrib_xpath = schema_dict.attrib_xpath(name, **kwargs)
    base_xpath, name = split_off_attrib(attrib_xpath)
    complex_xpath = process_xpath_argument(base_xpath, complex_xpath, filters)

    return xml_add_number_to_attrib(xmltree,
                                    schema_dict,
                                    complex_xpath,
                                    base_xpath,
                                    name,
                                    number_to_add,
                                    mode=mode,
                                    occurrences=occurrences)


def add_number_to_first_attrib(xmltree: XMLLike,
                               schema_dict: fleur_schema.SchemaDict,
                               name: str,
                               number_to_add: Any,
                               complex_xpath: XPathLike | None = None,
                               filters: FilterType | None = None,
                               mode: Literal['abs', 'absolute', 'rel', 'relative'] = 'absolute',
                               **kwargs: Any) -> XMLLike:
    """
    Adds a given number to the first occurrence of an attribute value in a xmltree specified by the name of the attribute
    and optional further specification
    If there are no nodes under the specified xpath an error is raised

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param name: the attribute name to change
    :param number_to_add: number to add/multiply with the old attribute value
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param mode: str (either `rel`/`relative` or `abs`/`absolute`).
                 `rel`/`relative` multiplies the old value with `number_to_add`
                 `abs`/`absolute` adds the old value and `number_to_add`
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

    Kwargs:
        :param tag_name: str, name of the tag where the attribute should be parsed
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param exclude: list of str, here specific types of attributes can be excluded
                        valid values are: settable, settable_contains, other

    :returns: xmltree with shifted attribute
    """
    return add_number_to_attrib(xmltree,
                                schema_dict,
                                name,
                                number_to_add,
                                complex_xpath=complex_xpath,
                                mode=mode,
                                occurrences=0,
                                filters=filters,
                                **kwargs)


def set_attrib_value(xmltree: XMLLike,
                     schema_dict: fleur_schema.SchemaDict,
                     name: str,
                     value: Any,
                     complex_xpath: XPathLike | None = None,
                     filters: FilterType | None = None,
                     occurrences: int | Iterable[int] | None = None,
                     create: bool = False,
                     **kwargs: Any) -> XMLLike:
    """
    Sets an attribute in a xmltree to a given value, specified by its name and further
    specifications.
    If there are no nodes under the specified xpath a tag can be created with `create=True`.
    The attribute values are converted automatically according to the types of the attribute
    with :py:func:`~masci_tools.util.xml.converters.convert_to_xml()` if they
    are not `str` already.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param name: the attribute name to set
    :param value: value or list of values to set
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
    :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.
    :param create: bool optional (default False), if True the tag is created if is missing

    Kwargs:
        :param tag_name: str, name of the tag where the attribute should be parsed
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param exclude: list of str, here specific types of attributes can be excluded
                        valid values are: settable, settable_contains, other

    :returns: xmltree with set attribute
    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_attrib_value
    from masci_tools.util.xml.common_functions import split_off_attrib

    #Special case for xcFunctional
    #(Also implemented here to not confuse users since it would only work in set_inpchanges otherwise)
    if name.lower() == 'xcfunctional':
        return set_xcfunctional(xmltree, schema_dict, value)

    base_xpath = schema_dict.attrib_xpath(name, **kwargs)
    base_xpath, name = split_off_attrib(base_xpath)
    complex_xpath = process_xpath_argument(base_xpath, complex_xpath, filters)

    return xml_set_attrib_value(xmltree,
                                schema_dict,
                                complex_xpath,
                                base_xpath,
                                name,
                                value,
                                occurrences=occurrences,
                                create=create)


def set_first_attrib_value(xmltree: XMLLike,
                           schema_dict: fleur_schema.SchemaDict,
                           name: str,
                           value: Any,
                           complex_xpath: XPathLike | None = None,
                           filters: FilterType | None = None,
                           create: bool = False,
                           **kwargs: Any) -> XMLLike:
    """
    Sets the first occurrence of an attribute in a xmltree to a given value, specified by its name and further
    specifications.
    If there are no nodes under the specified xpath a tag can be created with `create=True`.
    The attribute values are converted automatically according to the types of the attribute
    with :py:func:`~masci_tools.util.xml.converters.convert_to_xml()` if they
    are not `str` already.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param name: the attribute name to set
    :param value: value or list of values to set
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
    :param create: bool optional (default False), if True the tag is created if is missing

    Kwargs:
        :param tag_name: str, name of the tag where the attribute should be parsed
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param exclude: list of str, here specific types of attributes can be excluded
                        valid values are: settable, settable_contains, other

    :returns: xmltree with set attribute
    """
    return set_attrib_value(xmltree,
                            schema_dict,
                            name,
                            value,
                            complex_xpath=complex_xpath,
                            create=create,
                            occurrences=0,
                            filters=filters,
                            **kwargs)


def set_text(xmltree: XMLLike,
             schema_dict: fleur_schema.SchemaDict,
             tag_name: str,
             text: Any,
             complex_xpath: XPathLike | None = None,
             filters: FilterType | None = None,
             occurrences: int | Iterable[int] | None = None,
             create: bool = False,
             **kwargs: Any) -> XMLLike:
    """
    Sets the text on tags in a xmltree to a given value, specified by the name of the tag and
    further specifications. By default the text will be set on all nodes returned for the specified xpath.
    If there are no nodes under the specified xpath a tag can be created with `create=True`.
    The text values are converted automatically according to the types
    with :py:func:`~masci_tools.util.xml.converters.convert_to_xml()` if they
    are not `str` already.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param tag_name: str name of the tag, where the text should be set
    :param text: value or list of values to set
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
    :param occurrences: int or list of int. Which occurrence of the node to set. By default all are set.
    :param create: bool optional (default False), if True the tag is created if is missing

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: xmltree with set text
    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_text

    base_xpath = schema_dict.tag_xpath(tag_name, **kwargs)
    complex_xpath = process_xpath_argument(base_xpath, complex_xpath, filters)

    return xml_set_text(xmltree, schema_dict, complex_xpath, base_xpath, text, occurrences=occurrences, create=create)


def set_first_text(xmltree: XMLLike,
                   schema_dict: fleur_schema.SchemaDict,
                   tag_name: str,
                   text: Any,
                   complex_xpath: XPathLike | None = None,
                   filters: FilterType | None = None,
                   create: bool = False,
                   **kwargs: Any) -> XMLLike:
    """
    Sets the text the first occurrence of a tag in a xmltree to a given value, specified by the name of the tag and
    further specifications. By default the text will be set on all nodes returned for the specified xpath.
    If there are no nodes under the specified xpath a tag can be created with `create=True`.
    The text values are converted automatically according to the types
    with :py:func:`~masci_tools.util.xml.converters.convert_to_xml()` if they
    are not `str` already.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param tag_name: str name of the tag, where the text should be set
    :param text: value or list of values to set
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
    :param create: bool optional (default False), if True the tag is created if is missing

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: xmltree with set text
    """
    return set_text(xmltree,
                    schema_dict,
                    tag_name,
                    text,
                    complex_xpath=complex_xpath,
                    create=create,
                    occurrences=0,
                    filters=filters,
                    **kwargs)


def set_simple_tag(xmltree: XMLLike,
                   schema_dict: fleur_schema.SchemaDict,
                   tag_name: str,
                   changes: list[dict[str, Any]] | dict[str, Any],
                   complex_xpath: XPathLike | None = None,
                   filters: FilterType | None = None,
                   create_parents: bool = False,
                   **kwargs: Any) -> XMLLike:
    """
    Sets one or multiple `simple` tag(s) in an xmltree. A simple tag can only hold attributes and has no
    subtags. The tag is specified by its name and further specification
    If the tag can occur multiple times all existing tags are DELETED and new ones are written.
    If the tag only occurs once it will automatically be created if its missing.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param tag_name: str name of the tag to modify/set
    :param changes: list of dicts or dict with the changes. Elements in list describe multiple tags.
                    Keys in the dictionary correspond to {'attributename': attributevalue}
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
    :param create_parents: bool optional (default False), if True and the path, where the simple tags are
                           set does not exist it is created

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: xmltree with set simple tags
    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_simple_tag
    from masci_tools.util.xml.common_functions import split_off_tag

    #Since we can set multiple simple tags we need to provide the path for the parent
    base_xpath = schema_dict.tag_xpath(tag_name, **kwargs)
    parent_xpath, tag_name = split_off_tag(base_xpath)

    tag_info = schema_dict['tag_info'][base_xpath]

    assert len(tag_info['simple'] | tag_info['complex']) == 0, f"Given tag '{tag_name}' is not simple"
    complex_xpath = process_xpath_argument(parent_xpath, complex_xpath, filters)

    return xml_set_simple_tag(xmltree,
                              schema_dict,
                              complex_xpath,
                              parent_xpath,
                              tag_name,
                              changes,
                              create_parents=create_parents)


def set_complex_tag(xmltree: XMLLike,
                    schema_dict: fleur_schema.SchemaDict,
                    tag_name: str,
                    changes: dict[str, Any],
                    complex_xpath: XPathLike | None = None,
                    filters: FilterType | None = None,
                    create: bool = False,
                    **kwargs: Any) -> XMLLike:
    """
    Function to correctly set tags/attributes for a given tag.
    Goes through the attributedict and decides based on the schema_dict, how the corresponding
    key has to be handled.
    The tag is specified via its name and evtl. further specification

    Supports:

        - attributes
        - tags with text only
        - simple tags, i.e. only attributes (can be optional single/multiple)
        - complex tags, will recursively create/modify them

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param tag_name: name of the tag to set
    :param changes: Keys in the dictionary correspond to names of tags and the values are the modifications
                    to do on this tag (attributename, subdict with changes to the subtag, ...)
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
    :param create: bool optional (default False), if True and the path, where the complex tag is
                   set does not exist it is created

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: xmltree with changes to the complex tag
    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_complex_tag

    base_xpath = schema_dict.tag_xpath(tag_name, **kwargs)
    complex_xpath = process_xpath_argument(base_xpath, complex_xpath, filters)

    return xml_set_complex_tag(xmltree, schema_dict, complex_xpath, base_xpath, changes, create=create)


def set_species_label(xmltree: XMLLike,
                      schema_dict: fleur_schema.SchemaDict,
                      atom_label: str,
                      changes: dict[str, Any],
                      create: bool = False) -> XMLLike:
    """
    This method calls :func:`~masci_tools.util.xml.xml_setters_names.set_species()`
    method for a certain atom species that corresponds to an atom with a given label

    :param xmltree: xml etree of the inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param atom_label: string, a label of the atom which specie will be changed. 'all' to change all the species
    :param changes: a python dict specifying what you want to change.
    :param create: bool, if species does not exist create it and all subtags?

    :returns: xml etree of the new inp.xml
    """
    from masci_tools.util.schema_dict_util import evaluate_attribute

    if atom_label == 'all':
        return set_species(xmltree, schema_dict, 'all', changes, create=create)

    species_to_set = set(
        evaluate_attribute(xmltree,
                           schema_dict,
                           'species',
                           filters={'atomGroup': {
                               ('/filmPos/@label', '/relPos/@label'): {
                                   '=': f'{atom_label: >20}'
                               }
                           }},
                           list_return=True,
                           optional=True))

    for species_name in species_to_set:
        xmltree = set_species(xmltree, schema_dict, species_name, changes, create=create)

    return xmltree


def set_species(xmltree: XMLLike,
                schema_dict: fleur_schema.SchemaDict,
                species_name: str,
                changes: dict[str, Any],
                filters: FilterType | None = None,
                create: bool = False) -> XMLLike:
    """
    Method to set parameters of a species tag of the fleur inp.xml file.

    :param xmltree: xml etree of the inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param species_name: string, name of the specie you want to change
                         Can be name of the species, 'all' or 'all-<string>' (sets species with the string in the species name)
    :param changes: a python dict specifying what you want to change.
    :param create: bool, if species does not exist create it and all subtags?
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

    :raises ValueError: if species name is non existent in inp.xml and should not be created.
                        also if other given tags are garbage. (errors from eval_xpath() methods)

    :return xmltree: xml etree of the new inp.xml

    **changes** is a python dictionary containing dictionaries that specify attributes
    to be set inside the certain specie. For example, if one wants to set a MT radius it
    can be done via::

        changes = {'mtSphere' : {'radius' : 2.2}}

    Another example::

        'changes': {'special': {'socscale': 0.0}}

    that switches SOC terms on a sertain specie. ``mtSphere``, ``atomicCutoffs``,
    ``energyParameters``, ``lo``, ``electronConfig``, ``nocoParams``, ``ldaU`` and
    ``special`` keys are supported. To find possible
    keys of the inner dictionary please refer to the FLEUR documentation flapw.de
    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_complex_tag

    base_xpath_species = schema_dict.tag_xpath('species')

    xpath_species = XPathBuilder(base_xpath_species, strict=True, filters=filters)
    # TODO lowercase everything
    # TODO make a general specifier for species, not only the name i.e. also
    # number, other parameters
    if species_name[:4] == 'all-':  #format all-<string>
        xpath_species.add_filter('species', {'name': {'contains': species_name[4:]}})
    elif species_name != 'all':
        xpath_species.add_filter('species', {'name': {'=': species_name}})

    return xml_set_complex_tag(xmltree, schema_dict, xpath_species, base_xpath_species, changes, create=create)


def clone_species(xmltree: XMLLike,
                  schema_dict: fleur_schema.SchemaDict,
                  species_name: str,
                  new_name: str,
                  changes: dict[str, Any] | None = None) -> XMLLike:
    """
    Method to create a new species from an existing one with evtl. modifications

    For reference of the changes dictionary look at :py:func:`set_species()`

    :param xmltree: xml etree of the inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param species_name: string, name of the specie you want to clone
                         Has to correspond to one single species (no 'all'/'all-<search_string>')
    :param new_name: new name of the cloned species
    :param changes: a optional python dict specifying what you want to change.

    :returns xmltree: xml etree of the new inp.xml
    """
    from masci_tools.util.schema_dict_util import evaluate_attribute
    from masci_tools.util.xml.common_functions import eval_xpath_one
    import copy

    existing_names = set(evaluate_attribute(xmltree, schema_dict, 'name', contains='species', list_return=True))
    if species_name not in existing_names:
        raise ValueError(f'Species {species_name} does not exist')
    if new_name in existing_names:
        raise ValueError(f'Species {new_name} already exists. Choose another name for the cloned species')

    xpath_species = schema_dict.tag_xpath('species')
    xpath_species = f'{xpath_species}[@name = "{species_name}"]'

    old_species = eval_xpath_one(xmltree, xpath_species, etree._Element)

    parent = old_species.getparent()
    if parent is None:
        raise ValueError('Falied to get species parent tag')

    new_species = copy.deepcopy(old_species)
    new_species.set('name', new_name)
    parent.append(new_species)

    if changes is not None:
        xmltree = set_species(xmltree, schema_dict, new_name, changes)

    return xmltree


def shift_value_species_label(xmltree: XMLLike,
                              schema_dict: fleur_schema.SchemaDict,
                              atom_label: str,
                              attribute_name: str,
                              number_to_add: Any,
                              mode: Literal['abs', 'absolute', 'rel', 'relative'] = 'absolute',
                              **kwargs: Any) -> XMLLike:
    """
    Shifts the value of an attribute on a species by label
    if atom_label contains 'all' then applies to all species

    :param xmltree: xml etree of the inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param atom_label: string, a label of the atom which specie will be changed. 'all' if set up all species
    :param attribute_name: name of the attribute to change
    :param number_to_add: value to add or to multiply by
    :param mode: str (either `rel`/`relative` or `abs`/`absolute`).
                 `rel`/`relative` multiplies the old value with `number_to_add`
                 `abs`/`absolute` adds the old value and `number_to_add`

    Kwargs if the attribute_name does not correspond to a unique path:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: xml etree of the new inp.xml
    """
    from masci_tools.util.schema_dict_util import evaluate_attribute
    from masci_tools.util.xml.xml_setters_xpaths import xml_add_number_to_first_attrib
    from masci_tools.util.xml.common_functions import split_off_attrib

    if 'contains' in kwargs:
        contains = kwargs.get('contains')
        if not isinstance(contains, list):
            contains = [contains]
        contains.append('species')
        kwargs['contains'] = contains
    else:
        kwargs['contains'] = 'species'

    attr_base_path = schema_dict.attrib_xpath(attribute_name, **kwargs)
    tag_base_xpath, attribute_name = split_off_attrib(attr_base_path)

    filters = None
    if atom_label != 'all':
        filters = {'atomGroup': {('/filmPos/@label', '/relPos/@label'): {'=': f'{atom_label: >20}'}}}

    species_to_set = set(evaluate_attribute(xmltree, schema_dict, 'species', filters=filters, list_return=True))

    for species_name in species_to_set:

        tag_xpath = XPathBuilder(tag_base_xpath, strict=True, filters={'species': {'name': {'=': species_name}}})
        xmltree = xml_add_number_to_first_attrib(xmltree,
                                                 schema_dict,
                                                 tag_xpath,
                                                 tag_base_xpath,
                                                 attribute_name,
                                                 number_to_add,
                                                 mode=mode)

    return xmltree


def set_atomgroup_label(xmltree: XMLLike, schema_dict: fleur_schema.SchemaDict, atom_label: str,
                        changes: dict[str, Any]) -> XMLLike:
    """
    This method calls :func:`~masci_tools.util.xml.xml_setters_names.set_atomgroup()`
    method for a certain atom species that corresponds to an atom with a given label.

    :param xmltree: xml etree of the inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param atom_label: string, a label of the atom which specie will be changed. 'all' to change all the species
    :param changes: a python dict specifying what you want to change.

    :returns: xml etree of the new inp.xml

    **changes** is a python dictionary containing dictionaries that specify attributes
    to be set inside the certain specie. For example, if one wants to set a beta noco parameter it
    can be done via::

        'changes': {'nocoParams': {'beta': val}}

    """
    from masci_tools.util.schema_dict_util import evaluate_attribute
    if atom_label == 'all':
        return set_atomgroup(xmltree, schema_dict, changes, species='all')

    species_to_set = set(
        evaluate_attribute(xmltree,
                           schema_dict,
                           'species',
                           filters={'atomGroup': {
                               ('/filmPos/@label', '/relPos/@label'): {
                                   '=': f'{atom_label: >20}'
                               }
                           }},
                           list_return=True,
                           optional=True))

    for species_name in species_to_set:
        xmltree = set_atomgroup(xmltree, schema_dict, changes, species=species_name)

    return xmltree


def set_atomgroup(xmltree: XMLLike,
                  schema_dict: fleur_schema.SchemaDict,
                  changes: dict[str, Any],
                  position: int | Literal['all'] | None = None,
                  species: str | None = None,
                  filters: FilterType | None = None) -> XMLLike:
    """
    Method to set parameters of an atom group of the fleur inp.xml file.

    :param xmltree: xml etree of the inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param changes: a python dict specifying what you want to change.
    :param position: position of an atom group to be changed. If equals to 'all', all species will be changed
    :param species: atom groups, corresponding to the given species will be changed
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

    :returns: xml etree of the new inp.xml

    **changes** is a python dictionary containing dictionaries that specify attributes
    to be set inside the certain specie. For example, if one wants to set a beta noco parameter it
    can be done via::

        'changes': {'nocoParams': {'beta': val}}

    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_complex_tag

    atomgroup_base_path = schema_dict.tag_xpath('atomGroup')
    atomgroup_xpath = XPathBuilder(atomgroup_base_path, strict=True, filters=filters)

    if not position and not species and not filters:  # not specified what to change
        return xmltree

    if position and position != 'all':
        atomgroup_xpath.add_filter('atomGroup', {'index': position})
    if species and species != 'all':
        if species[:4] == 'all-':  #format all-<string>
            atomgroup_xpath.add_filter('atomGroup', {'species': {'contains': species[4:]}})
        else:
            atomgroup_xpath.add_filter('atomGroup', {'species': {'=': species}})

    species_change = dict(changes).pop('species', None)  #dict to avoid mutating changes
    if species_change is not None:
        changes = {k: v for k, v in changes.items() if k != 'species'}
        xmltree = switch_species(xmltree, schema_dict, species_change, position=position, species=species)

    return xml_set_complex_tag(xmltree, schema_dict, atomgroup_xpath, atomgroup_base_path, changes)


def switch_species_label(xmltree: XMLLike,
                         schema_dict: fleur_schema.SchemaDict,
                         atom_label: str,
                         new_species_name: str,
                         clone: bool = False,
                         changes: dict[str, Any] | None = None) -> XMLLike:
    """
    Method to switch the species of an atom group of the fleur inp.xml file based on a label
    of a contained atom

    :param xmltree: xml etree of the inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param atom_label: string, a label of the atom which group will be changed. 'all' to change all the groups
    :param new_species_name: name of the species to switch to
    :param clone: if True and the new species name does not exist and it corresponds to changing
                  from one species the species will be cloned with :py:func:`clone_species()`
    :param changes: changes to do if the species is cloned

    :returns: xml etree of the new inp.xml
    """
    if atom_label == 'all':
        return switch_species(xmltree, schema_dict, new_species_name, species='all', clone=clone, changes=changes)

    return switch_species(xmltree,
                          schema_dict,
                          new_species_name,
                          clone=clone,
                          changes=changes,
                          filters={'atomGroup': {
                              ('/filmPos/@label', '/relPos/@label'): {
                                  '=': f'{atom_label: >20}'
                              }
                          }})


def switch_species(xmltree: XMLLike,
                   schema_dict: fleur_schema.SchemaDict,
                   new_species_name: str,
                   position: int | Literal['all'] | None = None,
                   species: str | None = None,
                   filters: FilterType | None = None,
                   clone: bool = False,
                   changes: dict[str, Any] | None = None) -> XMLLike:
    """
    Method to switch the species of an atom group of the fleur inp.xml file.

    :param xmltree: xml etree of the inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param new_species_name: name of the species to switch to
    :param position: position of an atom group to be changed. If equals to 'all', all species will be changed
    :param species: atom groups, corresponding to the given species will be changed
    :param clone: if True and the new species name does not exist and it corresponds to changing
                  from one species the species will be cloned with :py:func:`clone_species()`
    :param changes: changes to do if the species is cloned
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

    :returns: xml etree of the new inp.xml
    """
    from masci_tools.util.schema_dict_util import evaluate_attribute
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_attrib_value
    from masci_tools.util.xml.common_functions import add_tag

    atomgroup_base_path = schema_dict.tag_xpath('atomGroup')
    atomgroup_xpath = XPathBuilder(atomgroup_base_path, strict=False, filters=filters)

    if not clone and changes is not None:
        raise ValueError('changes should only be passed with clone=True')

    if not position and not species and not filters:  # not specified what to change
        return xmltree

    if position and position != 'all':
        atomgroup_xpath.add_filter('atomGroup', {'index': position})
    if species and species != 'all':
        if species[:4] == 'all-':  #format all-<string>
            atomgroup_xpath.add_filter('atomGroup', {'species': {'contains': species[4:]}})
        else:
            atomgroup_xpath.add_filter('atomGroup', {'species': {'=': species}})

    existing_names = set(evaluate_attribute(xmltree, schema_dict, 'name', contains='species', list_return=True))
    if new_species_name not in existing_names:
        if not clone:
            raise ValueError(f'The species {new_species_name} does not exist')

        changed_names = set(
            evaluate_attribute(xmltree,
                               schema_dict,
                               'species',
                               complex_xpath=add_tag(atomgroup_xpath, '@species'),
                               list_return=True))
        if len(changed_names) > 1:
            raise ValueError('Cannot clone species, since name change does not correspond to one species')
        old_species = changed_names.pop()
        xmltree = clone_species(xmltree, schema_dict, old_species, new_species_name, changes=changes)
    elif clone:
        warnings.warn(f'clone set to True but species {new_species_name} already exists. Ignoring argument')

    return xml_set_attrib_value(xmltree, schema_dict, atomgroup_xpath, atomgroup_base_path, 'species', new_species_name)


def shift_value(xmltree: XMLLike,
                schema_dict: fleur_schema.SchemaDict,
                changes: dict[str, Any],
                mode: Literal['abs', 'absolute', 'rel', 'relative'] = 'absolute',
                path_spec: dict[str, Any] | None = None) -> XMLLike:
    """
    Shifts numerical values of attributes directly in the inp.xml file.

    The first occurrence of the attribute is shifted

    :param xmltree: xml tree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param changes: a python dictionary with the keys to shift and the shift values.
    :param mode: str (either `rel`/`relative` or `abs`/`absolute`).
                 `rel`/`relative` multiplies the old value with the given value
                 `abs`/`absolute` adds the old value and the given value
    :param path_spec: dict, with ggf. necessary further specifications for the path of the attribute

    :returns: a xml tree with shifted values

    An example of changes::

            changes = {'itmax' : 1, 'dVac': -0.123}
    """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict

    if path_spec is None:
        path_spec = {}
    path_spec_case: CaseInsensitiveDict[str, Any] = CaseInsensitiveDict(path_spec)

    for key, value_given in changes.items():

        key_spec = path_spec_case.get(key, {})
        #This method only support unique and unique_path attributes
        key_spec.setdefault('exclude', []).append('other')
        xmltree = add_number_to_first_attrib(xmltree, schema_dict, key, value_given, mode=mode, **key_spec)

    return xmltree


def set_inpchanges(xmltree: XMLLike,
                   schema_dict: fleur_schema.SchemaDict,
                   changes: dict[str, Any],
                   path_spec: dict[str, Any] | None = None) -> XMLLike:
    """
    This method sets all the attribute and texts provided in the change_dict.

    The first occurrence of the attribute/tag is set

    :param xmltree: xml tree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param changes: dictionary {attrib_name : value} with all the wanted changes.
    :param path_spec: dict, with ggf. necessary further specifications for the path of the attribute

    An example of changes::

        changes = {
            'itmax' : 1,
            'l_noco': True,
            'ctail': False,
            'l_ss': True
        }

    :returns: an xmltree of the inp.xml file with changes.
    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_first_attrib_value, xml_set_first_text
    from masci_tools.util.xml.common_functions import split_off_attrib
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict

    if path_spec is None:
        path_spec = {}
    path_spec_case: CaseInsensitiveDict[str, Any] = CaseInsensitiveDict(path_spec)

    for key, change_value in changes.items():

        #Special alias for xcFunctional since name is not a very telling attribute name
        if key.lower() == 'xcfunctional':
            set_xcfunctional(xmltree, schema_dict, change_value, libxc=isinstance(change_value, dict))
            continue

        if key not in schema_dict['attrib_types'] and key not in schema_dict['text_tags']:
            raise ValueError(f"You try to set the key:'{key}' to : '{change_value}', but the key is unknown"
                             ' to the fleur plug-in')

        key_spec = path_spec_case.get(key, {})
        #This method only support unique and unique_path attributes
        key_spec.setdefault('exclude', []).append('other')

        key_xpath = schema_dict.attrib_xpath(key, **key_spec)
        if key not in schema_dict['attrib_types']:
            xml_set_first_text(xmltree, schema_dict, key_xpath, key_xpath, change_value)
        else:
            #Split up path into tag path and attribute name (original name of key could have different cases)
            key_xpath, key = split_off_attrib(key_xpath)
            xml_set_first_attrib_value(xmltree, schema_dict, key_xpath, key_xpath, key, change_value)

    return xmltree


def set_xcfunctional(xmltree: XMLLike,
                     schema_dict: fleur_schema.SchemaDict,
                     xc_functional: str | dict[str, int | str],
                     xc_functional_options: dict[str, Any] | None = None,
                     libxc: bool = False) -> XMLLike:
    """
    Set the Exchange Correlation potential tag

    Setting a inbuilt XC functional
    .. code-block:: python

        set_xcfunctional(xmltree, schema_dict, 'vwn')

    Setting a LibXC XC functional
    .. code-block:: python

        set_xcfunctional(xmltree, schema_dict, {'exchange': 'lda_x', 'correlation':"lda_c_xalpha"}, libxc=True)

    :param xmltree: XML tree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param xc_functional: str or dict. If str it is the name of a inbuilt XC functional. If it is a dict it
                          specifies either the name or id for LibXC functionals for the keys
                          `'exchange', 'correlation', 'etot_exchange' and 'etot_correlation'`
    :param xc_functional_options: dict with further general changes to the `xcFunctional` tag
    :param libxc: bool if True the functional is a LibXC functional

    :returns: an xmltree with modified xcFunctional tag
    """

    if not libxc and isinstance(xc_functional, dict):
        raise ValueError('For non LibXC functionals please only provide the name as a string')
    if libxc and not isinstance(xc_functional, dict):
        raise ValueError('For LibXC functionals please only the names as a a dict of either names or IDs')

    changes = {'name': xc_functional if not libxc else 'LibXC'}
    if isinstance(xc_functional, dict):
        if all(isinstance(v, int) for v in xc_functional.values()):
            changes['libxcid'] = xc_functional
        elif all(isinstance(v, str) for v in xc_functional.values()):
            changes['libxcname'] = xc_functional
        else:
            raise ValueError('For non LibXC functionals provide the used functionals either as IDs or names not mixed')

    if xc_functional_options:
        changes = {**changes, **xc_functional_options}

    return set_complex_tag(xmltree, schema_dict, 'xcFunctional', changes)


@schema_dict_version_dispatch(output_schema=False)
def set_kpointlist(xmltree: XMLLike,
                   schema_dict: fleur_schema.SchemaDict,
                   kpoints: Iterable[Iterable[float]],
                   weights: Iterable[float],
                   name: str | None = None,
                   kpoint_type: Literal['path', 'mesh', 'tria', 'tria-bulk', 'spex-mesh'] = 'path',
                   special_labels: dict[int, str] | None = None,
                   switch: bool = False,
                   overwrite: bool = False,
                   additional_attributes: dict[str, Any] | None = None) -> XMLLike:
    """
    Explicitly create a kPointList from the given kpoints and weights. This routine will add the
    specified kPointList with the given name.

    .. warning::
        For input versions Max4 and older **all** keyword arguments are not valid (`name`, `kpoint_type`,
        `special_labels`, `switch` and `overwrite`)

    :param xmltree: xml tree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param kpoints: list or array containing the **relative** coordinates of the kpoints
    :param weights: list or array containing the weights of the kpoints
    :param name: str for the name of the list, if not given a default name is generated
    :param kpoint_type: str specifying the type of the kPointList ('path', 'mesh', 'spex', 'tria', ...)
    :param special_labels: dict mapping indices to labels. The labels will be inserted for the kpoints
                           corresponding to the given index
    :param switch: bool, if True the kPointlist will be used by Fleur when starting the next calculation
    :param overwrite: bool, if True and a kPointlist with the given name already exists it will be overwritten

    :returns: an xmltree of the inp.xml file with changes.
    """
    from masci_tools.util.xml.builder import FleurElementMaker
    from masci_tools.util.schema_dict_util import evaluate_attribute
    from masci_tools.util.xml.xml_setters_basic import xml_delete_tag
    import numpy as np

    if not isinstance(kpoints, (list, np.ndarray)) or not isinstance(weights, (list, np.ndarray)):
        raise ValueError('kPoints and weights have to be given as a list or array')

    if len(kpoints) != len(weights):
        raise ValueError('kPoints and weights do not have the same length')

    kpointlist_xpath = schema_dict.tag_xpath('kPointList')
    nkpts = len(kpoints)

    if special_labels is None:
        special_labels = {}

    if additional_attributes is None:
        additional_attributes = {}

    existing_labels = evaluate_attribute(xmltree, schema_dict, 'name', contains='kPointList', list_return=True)

    if name is None:
        name = f'default-{len(existing_labels)+1}'

    if name in existing_labels:
        if not overwrite:
            raise ValueError(f'kPointList named {name} already exists. Use overwrite=True to ignore')

        xmltree = xml_delete_tag(xmltree, f"{kpointlist_xpath}[@name='{name}']")

    E = FleurElementMaker(schema_dict)

    new_kpointset = E.kpointlist(*(E.kpoint(kpoint, weight=weight, label=special_labels[indx])
                                   if indx in special_labels else E.kpoint(kpoint, weight=weight)
                                   for indx, (kpoint, weight) in enumerate(zip(kpoints, weights))),
                                 name=name,
                                 count=nkpts,
                                 type=kpoint_type,
                                 **additional_attributes)

    xmltree = create_tag(xmltree, schema_dict, new_kpointset)
    if switch:
        xmltree = switch_kpointset(xmltree, schema_dict, name)

    return xmltree


@set_kpointlist.register(max_version='0.31')
def set_kpointlist_max4(xmltree: XMLLike,
                        schema_dict: fleur_schema.SchemaDict,
                        kpoints: Iterable[Iterable[float]],
                        weights: Iterable[float],
                        name: str | None = None,
                        kpoint_type: Literal['path', 'mesh', 'tria', 'tria-bulk', 'spex-mesh'] = 'path',
                        special_labels: dict[int, str] | None = None,
                        switch: bool = False,
                        overwrite: bool = False,
                        additional_attributes: dict[str, Any] | None = None) -> XMLLike:
    """
    Explicitly create a kPointList from the given kpoints and weights. This
    routine is specific to input versions Max4 and before and will replace any
    existing kPointCount, kPointMesh, ... with the specified kPointList

    :param xmltree: xml tree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param kpoints: list or array containing the **relative** coordinates of the kpoints
    :param weights: list or array containing the weights of the kpoints

    :returns: an xmltree of the inp.xml file with changes.
    """
    from masci_tools.util.xml.builder import FleurElementMaker
    from masci_tools.util.schema_dict_util import eval_simple_xpath
    import numpy as np

    if not isinstance(kpoints, (list, np.ndarray)) or not isinstance(weights, (list, np.ndarray)):
        raise ValueError('kPoints and weights have to be given as a list or array')

    if len(kpoints) != len(weights):
        raise ValueError('kPoints and weights do not have the same length')

    nkpts = len(kpoints)

    if additional_attributes is None:
        additional_attributes = {}

    bzintegration_tag: etree._Element = eval_simple_xpath(xmltree, schema_dict, 'bzIntegration')  #type:ignore

    for child in bzintegration_tag.iterchildren():
        if 'kPoint' in child.tag:
            bzintegration_tag.remove(child)

    E = FleurElementMaker(schema_dict)

    new_kpointset = E.kpointlist(*(E.kpoint(kpoint, weight=weight) for kpoint, weight in zip(kpoints, weights)),
                                 posscale=1,
                                 weightscale=1,
                                 count=nkpts,
                                 **additional_attributes)

    xmltree = create_tag(xmltree, schema_dict, new_kpointset, not_contains='altKPoint')

    return xmltree


@schema_dict_version_dispatch(output_schema=False)
def switch_kpointset(xmltree: XMLLike, schema_dict: fleur_schema.SchemaDict, list_name: str) -> XMLLike:
    """
    Switch the used k-point set

    .. warning::
        This method is only supported for input versions after the Max5 release

    :param xmltree: xml tree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param list_name: name of the kPoint set to use

    :returns: an xmltree of the inp.xml file with changes.
    """
    from masci_tools.util.schema_dict_util import evaluate_attribute

    existing_labels = evaluate_attribute(xmltree, schema_dict, 'name', contains='kPointList', list_return=True)

    if list_name not in existing_labels:
        raise ValueError(f'The given kPointList {list_name} does not exist',
                         f'Available kPointLists: {existing_labels}')

    return set_first_attrib_value(xmltree, schema_dict, 'listName', list_name)


@switch_kpointset.register(max_version='0.31')
def switch_kpointset_max4(xmltree: XMLLike, schema_dict: fleur_schema.SchemaDict, list_name: str) -> XMLLike:
    """
    Sets a k-point mesh directly into inp.xml specific for inputs of version Max4

    .. warning::
        This method is only supported for input versions after the Max5 release

    :param xmltree: xml tree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param list_name: name of the kPoint set to use

    :returns: an xmltree of the inp.xml file with changes.
    """
    raise NotImplementedError(
        f"'switch_kpointset' is not implemented for inputs of version '{schema_dict['inp_version']}'")


@schema_dict_version_dispatch(output_schema=False)
def set_nkpts(xmltree: XMLLike, schema_dict: fleur_schema.SchemaDict, count: int, gamma: bool = False) -> XMLLike:
    """
    Sets a k-point mesh directly into inp.xml

    .. warning::
        This method is only supported for input versions before the Max5 release

    :param xmltree: xml tree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param count: number of k-points
    :param gamma: bool that controls if the gamma-point should be included
                  in the k-point mesh

    :returns: an xmltree of the inp.xml file with changes.
    """

    raise NotImplementedError(f"'set_npkts' is not implemented for inputs of version '{schema_dict['inp_version']}'")


@set_nkpts.register(max_version='0.31')
def set_nkpts_max4(xmltree: XMLLike, schema_dict: fleur_schema.SchemaDict, count: int, gamma: bool = False) -> XMLLike:
    """
    Sets a k-point mesh directly into inp.xml specific for inputs of version Max4

    :param xmltree: xml tree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param count: number of k-points
    :param gamma: bool that controls if the gamma-point should be included
                  in the k-point mesh

    :returns: an xmltree of the inp.xml file with changes.
    """
    from masci_tools.util.schema_dict_util import eval_simple_xpath, tag_exists

    if not tag_exists(xmltree, schema_dict, 'kPointCount', not_contains='altKPoint'):
        bzintegration_tag: etree._Element = eval_simple_xpath(xmltree, schema_dict, 'bzIntegration')  #type:ignore

        for child in bzintegration_tag.iterchildren():
            if 'kPoint' in child.tag:
                bzintegration_tag.remove(child)

        xmltree = create_tag(xmltree, schema_dict, 'kPointCount', not_contains='altKPoint')

    xmltree = set_attrib_value(xmltree, schema_dict, 'count', count, contains='kPointCount', not_contains='altKPoint')
    xmltree = set_attrib_value(xmltree, schema_dict, 'gamma', gamma, contains='kPointCount', not_contains='altKPoint')

    return xmltree


@schema_dict_version_dispatch(output_schema=False)
def set_kpath(xmltree: XMLLike,
              schema_dict: fleur_schema.SchemaDict,
              kpath: dict[str, Iterable[float]],
              count: int,
              gamma: bool = False) -> XMLLike:
    """
    Sets a k-path directly into inp.xml  as a alternative kpoint set with purpose 'bands'

    .. warning::
        This method is only supported for input versions before the Max5 release

    :param xmltree: xml tree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param kpath: a dictionary with kpoint name as key and k point coordinate as value
    :param count: number of k-points
    :param gamma: bool that controls if the gamma-point should be included
                  in the k-point mesh

    :returns: an xmltree of the inp.xml file with changes.
    """

    raise NotImplementedError(
        f"'set_kpath' is not implemented for inputs of version '{schema_dict['inp_version']}. Use 'set_kpointlist' instead'"
    )


@set_kpath.register(max_version='0.31')
def set_kpath_max4(xmltree: XMLLike,
                   schema_dict: fleur_schema.SchemaDict,
                   kpath: dict[str, Iterable[float]],
                   count: int,
                   gamma: bool = False) -> XMLLike:
    """
    Sets a k-path directly into inp.xml as a alternative kpoint set with purpose 'bands'

    :param xmltree: xml tree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param kpath: a dictionary with kpoint name as key and k point coordinate as value
    :param count: number of k-points
    :param gamma: bool that controls if the gamma-point should be included
                  in the k-point mesh

    :returns: an xmltree of the inp.xml file with changes.
    """
    from masci_tools.util.xml.builder import FleurElementMaker
    from masci_tools.util.schema_dict_util import tag_exists

    if not tag_exists(xmltree, schema_dict, 'kPointCount', contains='altKPoint'):
        xmltree = create_tag(xmltree, schema_dict, 'kPointCount', contains='altKPoint', create_parents=True)
        xmltree = set_first_attrib_value(xmltree, schema_dict, 'purpose', 'bands')

    E = FleurElementMaker(schema_dict)

    new_kpointpath = E.kpointcount(
        *(E.specialpoint(kpt, name=name) for name, kpt in kpath.items()),
        count=count,
        gamma=gamma,
    )
    xmltree = replace_tag(xmltree,
                          schema_dict,
                          'kPointCount',
                          new_kpointpath,
                          contains='altKPoint',
                          filters={'altKPointSet': {
                              'purpose': 'bands'
                          }})

    return xmltree


def set_kpointpath(xmltree: XMLLike,
                   schema_dict: fleur_schema.SchemaDict,
                   path: str | list[str] | None = None,
                   nkpts: int | None = None,
                   density: float | None = None,
                   name: str | None = None,
                   switch: bool = False,
                   overwrite: bool = False,
                   special_points: dict[str, Iterable[float]] | None = None) -> XMLLike:
    """
    Create a kpoint list for a bandstructure calculation (using ASE kpath generation)

    The path can be defined explictly (see :py:func:`~ase.dft.kpoints.bandpath`) or derived from the unit cell

    :param xmltree: xml tree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param path: str, list of str or None defines the path to interpolate (for syntax :py:func:`~ase.dft.kpoints.bandpath`)
    :param nkpts: int number of kpoints in the path
    :param density: float number of kpoints per Angstroem
    :param name: Name of the created kpoint list. If not given a name is generated
    :param switch: bool if True the kpoint list is direclty set as the used set
    :param overwrite: if True and a kpoint list of the given name already exists it will be overwritten
    :param special_points: dict mapping names to coordinates for special points to use

    :returns: xmltree with a created kpoint path
    """
    from masci_tools.util.xml.xml_getters import get_cell
    from ase.dft.kpoints import bandpath
    import numpy as np

    cell, pbc = get_cell(xmltree, schema_dict)  #type: ignore[arg-type]
    if not all(pbc):
        #Set unit cell dimension to 0 for non-periodic direction
        cell[2:, 2:] = 0.0

    kptpath = bandpath(path, cell, npoints=nkpts, density=density, special_points=special_points)

    special_kpoints = kptpath.special_points

    labels = {}
    for label, special_kpoint in special_kpoints.items():
        for index, kpoint in enumerate(kptpath.kpts):
            if sum(abs(np.array(special_kpoint) - np.array(kpoint))).max() < 1e-12:
                labels[index] = label
    weights = np.ones(len(kptpath.kpts))

    return set_kpointlist(xmltree,
                          schema_dict,
                          kptpath.kpts,
                          weights,
                          name=name,
                          special_labels=labels,
                          switch=switch,
                          overwrite=overwrite,
                          kpoint_type='path')


def set_kpointmesh(xmltree: XMLLike,
                   schema_dict: fleur_schema.SchemaDict,
                   mesh: Collection[int],
                   name: str | None = None,
                   use_symmetries: bool = True,
                   switch: bool = False,
                   overwrite: bool = False,
                   shift: Iterable[float] | None = None,
                   time_reversal: bool = True,
                   map_to_first_bz: bool = True) -> XMLLike:
    """
    Create a kpoint mesh using spglib

    for details see :py:func:`~spglib.get_stabilized_reciprocal_mesh`

    :param xmltree: xml tree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param mesh: list-like woth three elements, giving the size of the kpoint set in each direction
    :param use_symmetry: bool if True the available symmetry operations in the inp.xml will be used
                         to reduce the kpoint set otherwise only the identity matrix is used
    :param name: Name of the created kpoint list. If not given a name is generated
    :param switch: bool if True the kpoint list is direclty set as the used set
    :param overwrite: if True and a kpoint list of the given name already exists it will be overwritten
    :param shift: shift the center of the kpint set
    :param time_reversal: bool if True time reversal symmetry will be used to reduce the kpoint set
    :param map_to_first_bz: bool if True the kpoints are mapped into the [0,1] interval

    :returns: xmltree with a created kpoint path
    """
    from masci_tools.util.xml.xml_getters import get_symmetry_information, get_cell
    from spglib import get_stabilized_reciprocal_mesh
    import numpy as np

    if len(mesh) != 3:
        raise ValueError('mesh has to be a three element list')

    _, pbc = get_cell(xmltree, schema_dict)  #type: ignore[arg-type]
    if not all(pbc) and mesh[2] != 1:  #type: ignore[index]
        raise ValueError('For film systems only one layer of kpoints in z is allowed')

    if use_symmetries:
        rotations, _ = get_symmetry_information(xmltree, schema_dict)  #type: ignore[arg-type]
    else:
        rotations = [np.eye(3, dtype='intc')]

    grid_mapping, grid_addresses = get_stabilized_reciprocal_mesh(mesh,
                                                                  rotations,
                                                                  is_shift=shift,
                                                                  is_time_reversal=time_reversal)

    if shift is None:
        shift = np.zeros(3)
    kpoints_indices = np.unique(grid_mapping)
    kpoints = (grid_addresses[kpoints_indices] + shift) / mesh

    if map_to_first_bz:
        #This mapping to the 0,1 integral makes it equivalent
        #to the gamma@grid kpoint generator (the same tolerances are also used for the rounding)
        kpoints = np.where(np.abs(kpoints - np.rint(kpoints)) < 1e-8, np.rint(kpoints), kpoints)
        kpoints = kpoints - np.floor(kpoints)

    weights = np.zeros_like(grid_mapping)
    for gp in grid_mapping:
        weights[gp] += 1
    weights = np.array(weights[kpoints_indices])
    mesh_attrs = dict(zip(('nx', 'ny', 'nz'), mesh))

    return set_kpointlist(xmltree,
                          schema_dict,
                          kpoints,
                          weights,
                          name=name,
                          switch=switch,
                          overwrite=overwrite,
                          kpoint_type='mesh',
                          additional_attributes=mesh_attrs)
