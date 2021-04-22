# -*- coding: utf-8 -*-
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
from masci_tools.util.schema_dict_util import get_tag_xpath
from masci_tools.util.schema_dict_util import get_attrib_xpath
from masci_tools.io.parsers.fleur.fleur_schema import schema_dict_version_dispatch


def create_tag(xmltree, schema_dict, tag, complex_xpath=None, create_parents=False, occurrences=None, **kwargs):
    """
    This method creates a tag with a uniquely identified xpath under the nodes of its parent.
    If there are no nodes evaluated the subtags can be created with `create_parents=True`

    The tag is always inserted in the correct place if a order is enforced by the schema

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param tag: str of the tag to create or etree Element with the same name to insert
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param create_parents: bool optional (default False), if True and the given xpath has no results the
                           the parent tags are created recursively
    :param occurrences: int or list of int. Which occurence of the parent nodes to create a tag.
                        By default all nodes are used.

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: xmltree with created tags
    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_create_tag_schema_dict
    from masci_tools.util.xml.common_functions import split_off_tag
    from lxml import etree

    if etree.iselement(tag):
        tag_name = tag.tag
    else:
        tag_name = tag

    base_xpath = get_tag_xpath(schema_dict, tag_name, **kwargs)

    parent_xpath, tag_name = split_off_tag(base_xpath)

    if complex_xpath is None:
        complex_xpath = parent_xpath

    xmltree = xml_create_tag_schema_dict(xmltree,
                                         schema_dict,
                                         complex_xpath,
                                         parent_xpath,
                                         tag,
                                         create_parents=create_parents,
                                         occurrences=occurrences)

    return xmltree


def add_number_to_attrib(xmltree,
                         schema_dict,
                         attributename,
                         add_number,
                         complex_xpath=None,
                         mode='abs',
                         occurrences=None,
                         **kwargs):
    """
    Adds a given number to the attribute value in a xmltree specified by the name of the attribute
    and optional further specification
    If there are no nodes under the specified xpath an error is raised

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param attributename: the attribute name to change
    :param add_number: number to add/multiply with the old attribute value
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param mode: str (either `rel` or `abs`).
                 `rel` multiplies the old value with `add_number`
                 `abs` adds the old value and `add_number`
    :param occurrences: int or list of int. Which occurence of the node to set. By default all are set.

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

    attrib_xpath = get_attrib_xpath(schema_dict, attributename, **kwargs)

    base_xpath, attributename = split_off_attrib(attrib_xpath)

    if complex_xpath is None:
        complex_xpath = base_xpath

    xmltree = xml_add_number_to_attrib(xmltree,
                                       schema_dict,
                                       complex_xpath,
                                       base_xpath,
                                       attributename,
                                       add_number,
                                       mode=mode,
                                       occurrences=occurrences)

    return xmltree


def add_number_to_first_attrib(xmltree,
                               schema_dict,
                               attributename,
                               add_number,
                               complex_xpath=None,
                               mode='abs',
                               **kwargs):
    """
    Adds a given number to the first occurrence of an attribute value in a xmltree specified by the name of the attribute
    and optional further specification
    If there are no nodes under the specified xpath an error is raised

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param attributename: the attribute name to change
    :param add_number: number to add/multiply with the old attribute value
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param mode: str (either `rel` or `abs`).
                 `rel` multiplies the old value with `add_number`
                 `abs` adds the old value and `add_number`

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
                                attributename,
                                add_number,
                                complex_xpath=complex_xpath,
                                mode=mode,
                                occurrences=0,
                                **kwargs)


def set_attrib_value(xmltree,
                     schema_dict,
                     attributename,
                     attribv,
                     complex_xpath=None,
                     occurrences=None,
                     create=False,
                     **kwargs):
    """
    Sets an attribute in a xmltree to a given value, specified by its name and further
    specifications.
    If there are no nodes under the specified xpath a tag can be created with `create=True`.
    The attribute values are converted automatically according to the types of the attribute
    with :py:func:`~masci_tools.util.xml.converters.convert_attribute_to_xml()` if they
    are not `str` already.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param attributename: the attribute name to set
    :param attribv: value or list of values to set
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param occurrences: int or list of int. Which occurence of the node to set. By default all are set.
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
    if attributename == 'xcFunctional':
        attributename = 'name'
        if 'exclude' not in kwargs:
            kwargs['exclude'] = ['other']
        elif 'other' not in kwargs['exclude']:
            kwargs['exclude'].append('other')

    base_xpath = get_attrib_xpath(schema_dict, attributename, **kwargs)

    base_xpath, attributename = split_off_attrib(base_xpath)

    if complex_xpath is None:
        complex_xpath = base_xpath

    xmltree = xml_set_attrib_value(xmltree,
                                   schema_dict,
                                   complex_xpath,
                                   base_xpath,
                                   attributename,
                                   attribv,
                                   occurrences=occurrences,
                                   create=create)

    return xmltree


def set_first_attrib_value(xmltree, schema_dict, attributename, attribv, complex_xpath=None, create=False, **kwargs):
    """
    Sets the first occurrence of an attribute in a xmltree to a given value, specified by its name and further
    specifications.
    If there are no nodes under the specified xpath a tag can be created with `create=True`.
    The attribute values are converted automatically according to the types of the attribute
    with :py:func:`~masci_tools.util.xml.converters.convert_attribute_to_xml()` if they
    are not `str` already.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param attributename: the attribute name to set
    :param attribv: value or list of values to set
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
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
                            attributename,
                            attribv,
                            complex_xpath=complex_xpath,
                            create=create,
                            occurrences=0,
                            **kwargs)


def set_text(xmltree, schema_dict, tag_name, text, complex_xpath=None, occurrences=None, create=False, **kwargs):
    """
    Sets the text on tags in a xmltree to a given value, specified by the name of the tag and
    further specifications. By default the text will be set on all nodes returned for the specified xpath.
    If there are no nodes under the specified xpath a tag can be created with `create=True`.
    The text values are converted automatically according to the types
    with :py:func:`~masci_tools.util.xml.converters.convert_text_to_xml()` if they
    are not `str` already.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param tag_name: str name of the tag, where the text should be set
    :param text: value or list of values to set
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param occurrences: int or list of int. Which occurence of the node to set. By default all are set.
    :param create: bool optional (default False), if True the tag is created if is missing

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: xmltree with set text
    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_text

    base_xpath = get_tag_xpath(schema_dict, tag_name, **kwargs)

    if complex_xpath is None:
        complex_xpath = base_xpath

    xmltree = xml_set_text(xmltree,
                           schema_dict,
                           complex_xpath,
                           base_xpath,
                           text,
                           occurrences=occurrences,
                           create=create)

    return xmltree


def set_first_text(xmltree, schema_dict, attributename, attribv, complex_xpath=None, create=False, **kwargs):
    """
    Sets the text the first occurrence of a tag in a xmltree to a given value, specified by the name of the tag and
    further specifications. By default the text will be set on all nodes returned for the specified xpath.
    If there are no nodes under the specified xpath a tag can be created with `create=True`.
    The text values are converted automatically according to the types
    with :py:func:`~masci_tools.util.xml.converters.convert_text_to_xml()` if they
    are not `str` already.

    :param xmltree: an xmltree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param tag_name: str name of the tag, where the text should be set
    :param text: value or list of values to set
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param create: bool optional (default False), if True the tag is created if is missing

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: xmltree with set text
    """
    return set_text(xmltree,
                    schema_dict,
                    attributename,
                    attribv,
                    complex_xpath=complex_xpath,
                    create=create,
                    occurrences=0,
                    **kwargs)


def set_simple_tag(xmltree, schema_dict, tag_name, changes, complex_xpath=None, create_parents=False, **kwargs):
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
    :param create_parents: bool optional (default False), if True and the path, where the simple tags are
                           set does not exist it is created

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: xmltree with set simple tags
    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_simple_tag
    from masci_tools.util.xml.common_functions import split_off_tag

    base_xpath = get_tag_xpath(schema_dict, tag_name, **kwargs)

    #Since we can set multiple simple tags we need to provide the path for the parent
    parent_xpath, tag_name = split_off_tag(base_xpath)

    tag_info = schema_dict['tag_info'][base_xpath]

    assert len(tag_info['simple'] | tag_info['complex']) == 0, f"Given tag '{tag_name}' is not simple"

    if complex_xpath is None:
        complex_xpath = parent_xpath

    return xml_set_simple_tag(xmltree,
                              schema_dict,
                              complex_xpath,
                              parent_xpath,
                              tag_name,
                              changes,
                              create_parents=create_parents)


def set_complex_tag(xmltree, schema_dict, tag_name, changes, complex_xpath=None, create=False, **kwargs):
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
    :param attributedict: Keys in the dictionary correspond to names of tags and the values are the modifications
                          to do on this tag (attributename, subdict with changes to the subtag, ...)
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param create: bool optional (default False), if True and the path, where the complex tag is
                   set does not exist it is created

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: xmltree with changes to the complex tag
    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_complex_tag

    base_xpath = get_tag_xpath(schema_dict, tag_name, **kwargs)

    if complex_xpath is None:
        complex_xpath = base_xpath

    return xml_set_complex_tag(xmltree, schema_dict, complex_xpath, base_xpath, changes, create=create)


def set_species_label(xmltree, schema_dict, atom_label, attributedict, create=False):
    """
    This method calls :func:`~masci_tools.util.xml.xml_setters_names.set_species()`
    method for a certain atom species that corresponds to an atom with a given label

    :param xmltree: xml etree of the inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param atom_label: string, a label of the atom which specie will be changed. 'all' to change all the species
    :param attributedict: a python dict specifying what you want to change.
    :param create: bool, if species does not exist create it and all subtags?

    :returns: xml etree of the new inp.xml
    """
    from masci_tools.util.schema_dict_util import tag_exists, eval_simple_xpath
    from masci_tools.util.xml.common_functions import get_xml_attribute

    if atom_label == 'all':
        return set_species(xmltree, schema_dict, 'all', attributedict, create=create)

    atom_label = '{: >20}'.format(atom_label)
    all_groups = eval_simple_xpath(xmltree, schema_dict, 'atomGroup', list_return=True)

    species_to_set = set()

    # set all species, where given label is present
    for group in all_groups:
        if tag_exists(group, schema_dict, 'filmPos'):
            atoms = eval_simple_xpath(group, schema_dict, 'filmPos', list_return=True)
        else:
            atoms = eval_simple_xpath(group, schema_dict, 'relPos', list_return=True)
        for atom in atoms:
            label = get_xml_attribute(atom, 'label')
            if label == atom_label:
                species_to_set.add(get_xml_attribute(group, 'species'))

    for species_name in species_to_set:
        xmltree = set_species(xmltree, schema_dict, species_name, attributedict, create=create)

    return xmltree


def set_species(xmltree, schema_dict, species_name, attributedict, create=False):
    """
    Method to set parameters of a species tag of the fleur inp.xml file.

    :param xmltree: xml etree of the inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param species_name: string, name of the specie you want to change
                         Can be name of the species, 'all' or 'all-<string>' (sets species with the string in the species name)
    :param attributedict: a python dict specifying what you want to change.
    :param create: bool, if species does not exist create it and all subtags?

    :raises ValueError: if species name is non existent in inp.xml and should not be created.
                        also if other given tags are garbage. (errors from eval_xpath() methods)

    :return xmltree: xml etree of the new inp.xml

    **attributedict** is a python dictionary containing dictionaries that specify attributes
    to be set inside the certain specie. For example, if one wants to set a MT radius it
    can be done via::

        attributedict = {'mtSphere' : {'radius' : 2.2}}

    Another example::

        'attributedict': {'special': {'socscale': 0.0}}

    that switches SOC terms on a sertain specie. ``mtSphere``, ``atomicCutoffs``,
    ``energyParameters``, ``lo``, ``electronConfig``, ``nocoParams``, ``ldaU`` and
    ``special`` keys are supported. To find possible
    keys of the inner dictionary please refer to the FLEUR documentation flapw.de
    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_complex_tag

    base_xpath_species = get_tag_xpath(schema_dict, 'species')

    # TODO lowercase everything
    # TODO make a general specifier for species, not only the name i.e. also
    # number, other parameters
    if species_name == 'all':
        xpath_species = base_xpath_species
    elif species_name[:4] == 'all-':  #format all-<string>
        xpath_species = f'{base_xpath_species}[contains(@name,"{species_name[4:]}")]'
    else:
        xpath_species = f'{base_xpath_species}[@name = "{species_name}"]'

    return xml_set_complex_tag(xmltree, schema_dict, xpath_species, base_xpath_species, attributedict, create=create)


def shift_value_species_label(xmltree, schema_dict, atom_label, attributename, value_given, mode='abs', **kwargs):
    """
    Shifts the value of an attribute on a species by label
    if atom_label contains 'all' then applies to all species

    :param xmltree: xml etree of the inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param atom_label: string, a label of the atom which specie will be changed. 'all' if set up all species
    :param attributename: name of the attribute to change
    :param value_given: value to add or to multiply by
    :param mode: 'rel' for multiplication or 'abs' for addition

    Kwargs if the attributename does not correspond to a unique path:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: xml etree of the new inp.xml
    """
    from masci_tools.util.schema_dict_util import tag_exists, eval_simple_xpath
    from masci_tools.util.xml.common_functions import get_xml_attribute
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

    species_base_path = get_tag_xpath(schema_dict, 'species')
    attr_base_path = get_attrib_xpath(schema_dict, attributename, **kwargs)
    tag_base_xpath, attributename = split_off_attrib(attr_base_path)

    if atom_label != 'all':
        atom_label = '{: >20}'.format(atom_label)
    all_groups = eval_simple_xpath(xmltree, schema_dict, 'atomGroup', list_return=True)

    species_to_set = set()

    for group in all_groups:
        if tag_exists(group, schema_dict, 'filmPos'):
            atoms = eval_simple_xpath(group, schema_dict, 'filmPos', list_return=True)
        else:
            atoms = eval_simple_xpath(group, schema_dict, 'relPos', list_return=True)
        for atom in atoms:
            label = get_xml_attribute(atom, 'label')
            if atom_label in ('all', label):
                species_to_set.add(get_xml_attribute(group, 'species'))

    for species_name in species_to_set:

        xpath_species = f'{species_base_path}[@name="{species_name}"]'
        tag_xpath = tag_base_xpath.replace(species_base_path, xpath_species)

        xmltree = xml_add_number_to_first_attrib(xmltree,
                                                 schema_dict,
                                                 tag_xpath,
                                                 tag_base_xpath,
                                                 attributename,
                                                 value_given,
                                                 mode=mode)

    return xmltree


def set_atomgroup_label(xmltree, schema_dict, atom_label, attributedict, create=False):
    """
    This method calls :func:`~masci_tools.util.xml.xml_setters_names.set_atomgroup()`
    method for a certain atom species that corresponds to an atom with a given label.

    :param xmltree: xml etree of the inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param atom_label: string, a label of the atom which specie will be changed. 'all' to change all the species
    :param attributedict: a python dict specifying what you want to change.
    :param create: bool, if species does not exist create it and all subtags?

    :returns: xml etree of the new inp.xml

    **attributedict** is a python dictionary containing dictionaries that specify attributes
    to be set inside the certain specie. For example, if one wants to set a beta noco parameter it
    can be done via::

        'attributedict': {'nocoParams': {'beta': val}}

    """
    from masci_tools.util.schema_dict_util import tag_exists, eval_simple_xpath
    from masci_tools.util.xml.common_functions import get_xml_attribute

    if atom_label == 'all':
        xmltree = set_atomgroup(xmltree, schema_dict, attributedict, position=None, species='all')
        return xmltree

    atom_label = '{: >20}'.format(atom_label)
    all_groups = eval_simple_xpath(xmltree, schema_dict, 'atomGroup', list_return=True)

    species_to_set = set()

    # set all species, where given label is present
    for group in all_groups:
        if tag_exists(group, schema_dict, 'filmPos'):
            atoms = eval_simple_xpath(group, schema_dict, 'filmPos', list_return=True)
        else:
            atoms = eval_simple_xpath(group, schema_dict, 'relPos', list_return=True)
        for atom in atoms:
            label = get_xml_attribute(atom, 'label')
            if label == atom_label:
                species_to_set.add(get_xml_attribute(group, 'species'))

    for species_name in species_to_set:
        xmltree = set_atomgroup(xmltree, schema_dict, attributedict, position=None, species=species_name)

    return xmltree


def set_atomgroup(xmltree, schema_dict, attributedict, position=None, species=None, create=False):
    """
    Method to set parameters of an atom group of the fleur inp.xml file.

    :param xmltree: xml etree of the inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param attributedict: a python dict specifying what you want to change.
    :param position: position of an atom group to be changed. If equals to 'all', all species will be changed
    :param species: atom groups, corresponding to the given species will be changed
    :param create: bool, if species does not exist create it and all subtags?

    :returns: xml etree of the new inp.xml

    **attributedict** is a python dictionary containing dictionaries that specify attributes
    to be set inside the certain specie. For example, if one wants to set a beta noco parameter it
    can be done via::

        'attributedict': {'nocoParams': {'beta': val}}

    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_complex_tag

    atomgroup_base_path = get_tag_xpath(schema_dict, 'atomGroup')
    atomgroup_xpath = atomgroup_base_path

    if not position and not species:  # not specfied what to change
        return xmltree

    if position:
        if not position == 'all':
            atomgroup_xpath = f'{atomgroup_base_path}[{position}]'
    if species:
        if not species == 'all':
            atomgroup_xpath = f'{atomgroup_base_path}[@species = "{species}"]'

    xmltree = xml_set_complex_tag(xmltree,
                                  schema_dict,
                                  atomgroup_xpath,
                                  atomgroup_base_path,
                                  attributedict,
                                  create=create)

    return xmltree


def shift_value(xmltree, schema_dict, change_dict, mode='abs', path_spec=None):
    """
    Shifts numerical values of attributes directly in the inp.xml file.

    The first occurrence of the attribute is shifted

    :param xmltree: xml tree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param change_dict: a python dictionary with the keys to shift and the shift values.
    :param mode: 'abs' if change given is absolute, 'rel' if relative
    :param path_spec: dict, with ggf. necessary further specifications for the path of the attribute

    :returns: a xml tree with shifted values

    An example of change_dict::

            change_dict = {'itmax' : 1, 'dVac': -0.123}
    """
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict

    if path_spec is None:
        path_spec = {}
    path_spec = CaseInsensitiveDict(path_spec)

    for key, value_given in change_dict.items():

        key_spec = path_spec.get(key, {})
        #This method only support unique and unique_path attributes
        if 'exclude' not in key_spec:
            key_spec['exclude'] = ['other']
        elif 'other' not in key_spec['exclude']:
            key_spec['exclude'].append('other')

        xmltree = add_number_to_first_attrib(xmltree, schema_dict, key, value_given, mode=mode, **key_spec)

    return xmltree


def set_inpchanges(xmltree, schema_dict, change_dict, path_spec=None):
    """
    This method sets all the attribute and texts provided in the change_dict.

    The first occurrence of the attribute/tag is set

    :param xmltree: xml tree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :params change_dict: dictionary {attrib_name : value} with all the wanted changes.
    :param path_spec: dict, with ggf. necessary further specifications for the path of the attribute

    An example of change_dict::

            change_dict = {'itmax' : 1,
                           'l_noco': True,
                           'ctail': False,
                           'l_ss': True}

    :returns: an xmltree of the inp.xml file with changes.
    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_first_attrib_value, xml_set_first_text
    from masci_tools.util.xml.common_functions import split_off_attrib
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict

    if path_spec is None:
        path_spec = {}
    path_spec = CaseInsensitiveDict(path_spec)

    for key, change_value in change_dict.items():

        #Special alias for xcFunctional since name is not a very telling attribute name
        if key == 'xcFunctional':
            key = 'name'

        if key not in schema_dict['attrib_types'] and key not in schema_dict['simple_elements']:
            raise ValueError(f"You try to set the key:'{key}' to : '{change_value}', but the key is unknown"
                             ' to the fleur plug-in')

        text_attrib = key not in schema_dict['attrib_types']

        key_spec = path_spec.get(key, {})
        #This method only support unique and unique_path attributes
        if 'exclude' not in key_spec:
            key_spec['exclude'] = ['other']
        elif 'other' not in key_spec['exclude']:
            key_spec['exclude'].append('other')

        key_xpath = get_attrib_xpath(schema_dict, key, **key_spec)

        if not text_attrib:
            #Split up path into tag path and attribute name (original name of key could have different cases)
            key_xpath, key = split_off_attrib(key_xpath)

        if text_attrib:
            xml_set_first_text(xmltree, schema_dict, key_xpath, key_xpath, change_value)
        else:
            xml_set_first_attrib_value(xmltree, schema_dict, key_xpath, key_xpath, key, change_value)

    return xmltree


@schema_dict_version_dispatch(output_schema=False)
def set_kpointlist(xmltree,
                   schema_dict,
                   kpoints,
                   weights,
                   name=None,
                   kpoint_type='path',
                   special_labels=None,
                   switch=False,
                   overwrite=False):
    """
    Explicitely create a kPointList from the given kpoints and weights. This routine will add the
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
    from masci_tools.util.schema_dict_util import evaluate_attribute
    from masci_tools.util.xml.converters import convert_text_to_xml, convert_attribute_to_xml
    from masci_tools.util.xml.xml_setters_basic import xml_delete_tag
    from lxml import etree
    import numpy as np

    if not isinstance(kpoints, (list, np.ndarray)) or not isinstance(weights, (list, np.ndarray)):
        raise ValueError('kPoints and weights have to be given as a list or array')

    if len(kpoints) != len(weights):
        raise ValueError('kPoints and weights do not have the same length')

    kpointlist_xpath = get_tag_xpath(schema_dict, 'kPointList')
    nkpts = len(kpoints)

    if special_labels is None:
        special_labels = {}

    existing_labels = evaluate_attribute(xmltree, schema_dict, 'name', contains='kPointList', list_return=True)

    if name is None:
        name = f'default-{len(existing_labels)+1}'

    if name in existing_labels:
        if not overwrite:
            raise ValueError(f'kPointList named {name} already exists. Use overwrite=True to ignore')

        xmltree = xml_delete_tag(xmltree, f"{kpointlist_xpath}[@name='{name}']")

    new_kpo = etree.Element('kPointList', name=name, count=f'{nkpts:d}', type=kpoint_type)
    for indx, (kpoint, weight) in enumerate(zip(kpoints, weights)):
        weight, _ = convert_attribute_to_xml(weight, ['float', 'float_expression'])
        if indx in special_labels:
            new_k = etree.Element('kPoint', weight=weight, label=special_labels[indx])
        else:
            new_k = etree.Element('kPoint', weight=weight)
        text, _ = convert_text_to_xml(kpoint, [{'type': ['float', 'float_expression'], 'length': 3}])
        new_k.text = text
        new_kpo.append(new_k)

    xmltree = create_tag(xmltree, schema_dict, new_kpo)

    if switch:
        xmltree = switch_kpointset(xmltree, schema_dict, name)

    return xmltree


@set_kpointlist.register(max_version='0.31')
def set_kpointlist_max4(xmltree, schema_dict, kpoints, weights):
    """
    Explicitely create a kPointList from the given kpoints and weights. This
    routine is specific to input versions Max4 and before and will replace any
    existing kPointCount, kPointMesh, ... with the specified kPointList

    :param xmltree: xml tree that represents inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param kpoints: list or array containing the **relative** coordinates of the kpoints
    :param weights: list or array containing the weights of the kpoints

    :returns: an xmltree of the inp.xml file with changes.
    """
    from masci_tools.util.schema_dict_util import eval_simple_xpath
    from masci_tools.util.xml.converters import convert_text_to_xml, convert_attribute_to_xml
    from lxml import etree
    import numpy as np

    if not isinstance(kpoints, (list, np.ndarray)) or not isinstance(weights, (list, np.ndarray)):
        raise ValueError('kPoints and weights have to be given as a list or array')

    if len(kpoints) != len(weights):
        raise ValueError('kPoints and weights do not have the same length')

    nkpts = len(kpoints)

    bzintegration_tag = eval_simple_xpath(xmltree, schema_dict, 'bzIntegration')

    for child in bzintegration_tag.iterchildren():
        if 'kPoint' in child.tag:
            bzintegration_tag.remove(child)

    new_kpo = etree.Element('kPointList', posScale='1.0', weightScale='1.0', count=f'{nkpts:d}')
    for kpoint, weight in zip(kpoints, weights):
        weight, _ = convert_attribute_to_xml(weight, ['float', 'float_expression'])
        new_k = etree.Element('kPoint', weight=weight)
        text, _ = convert_text_to_xml(kpoint, [{'type': ['float', 'float_expression'], 'length': 3}])
        new_k.text = text
        new_kpo.append(new_k)

    xmltree = create_tag(xmltree, schema_dict, new_kpo, not_contains='altKPoint')

    return xmltree


@schema_dict_version_dispatch(output_schema=False)
def switch_kpointset(xmltree, schema_dict, list_name):
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
def switch_kpointset_max4(xmltree, schema_dict, list_name):
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
def set_nkpts(xmltree, schema_dict, count, gamma=False):
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
def set_nkpts_max4(xmltree, schema_dict, count, gamma=False):
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
        bzintegration_tag = eval_simple_xpath(xmltree, schema_dict, 'bzIntegration')

        for child in bzintegration_tag.iterchildren():
            if 'kPoint' in child.tag:
                bzintegration_tag.remove(child)

        xmltree = create_tag(xmltree, schema_dict, 'kPointCount', not_contains='altKPoint')

    xmltree = set_attrib_value(xmltree, schema_dict, 'count', count, contains='kPointCount', not_contains='altKPoint')
    xmltree = set_attrib_value(xmltree, schema_dict, 'gamma', gamma, contains='kPointCount', not_contains='altKPoint')

    return xmltree


@schema_dict_version_dispatch(output_schema=False)
def set_kpath(xmltree, schema_dict, kpath, count, gamma=False):
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
def set_kpath_max4(xmltree, schema_dict, kpath, count, gamma=False):
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
    from masci_tools.util.schema_dict_util import tag_exists
    from masci_tools.util.xml.converters import convert_to_fortran_bool, convert_text_to_xml
    from masci_tools.util.xml.xml_setters_basic import xml_replace_tag
    from lxml import etree

    alt_kpt_set_xpath = get_tag_xpath(schema_dict, 'altKPointSet')

    if not tag_exists(xmltree, schema_dict, 'kPointCount', contains='altKPoint'):
        xmltree = create_tag(xmltree, schema_dict, 'kPointCount', contains='altKPoint', create_parents=True)
        xmltree = set_first_attrib_value(xmltree, schema_dict, 'purpose', 'bands')

    new_kpo = etree.Element('kPointCount', count='{}'.format(count), gamma='{}'.format(convert_to_fortran_bool(gamma)))
    for label, coord in kpath.items():
        new_k = etree.Element('specialPoint', name='{}'.format(label))
        text, _ = convert_text_to_xml(coord, [{'type': ['float', 'float_expression'], 'length': 3}])
        new_k.text = text
        new_kpo.append(new_k)

    kpath_xpath = f"{alt_kpt_set_xpath}[@purpose='bands']/kPointCount"

    xmltree = xml_replace_tag(xmltree, kpath_xpath, new_kpo)

    return xmltree
