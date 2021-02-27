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
"""
from masci_tools.util.schema_dict_util import get_tag_xpath
from masci_tools.util.schema_dict_util import get_attrib_xpath


def create_tag(xmltree, schema_dict, tag_name, complex_xpath=None, create_parents=False, **kwargs):

    from masci_tools.util.xml.xml_setters_xpaths import create_tag_schema_dict

    base_xpath = get_tag_xpath(schema_dict, tag_name, **kwargs)

    parent_xpath, tag_name = '/'.join(base_xpath.split('/')[:-1]), base_xpath.split('/')[-1]

    if complex_xpath is None:
        complex_xpath = parent_xpath

    xmltree = create_tag_schema_dict(xmltree,
                                     schema_dict,
                                     complex_xpath,
                                     parent_xpath,
                                     tag_name,
                                     create_parents=create_parents)

    return xmltree


def add_number_to_attrib(xmltree, schema_dict, attributename, add_number, mode='abs', occurrences=None, **kwargs):

    from masci_tools.util.xml.xml_setters_xpaths import xml_add_number_to_attrib

    attrib_xpath = get_attrib_xpath(schema_dict, attributename, **kwargs)

    base_xpath, attributename = tuple(attrib_xpath.split('/@'))

    xmltree = xml_add_number_to_attrib(xmltree,
                                       schema_dict,
                                       attrib_xpath,
                                       base_xpath,
                                       attributename,
                                       add_number,
                                       mode=mode,
                                       occurrences=occurrences)


def add_number_to_first_attrib(xmltree, schema_dict, attributename, add_number, mode='abs', **kwargs):

    return add_number_to_attrib(xmltree, schema_dict, attributename, add_number, mode='abs', occurrences=0, **kwargs)


def set_attrib_value(xmltree,
                     schema_dict,
                     attributename,
                     attribv,
                     complex_xpath=None,
                     occurrences=None,
                     create=False,
                     **kwargs):

    from masci_tools.util.xml.xml_setters_xpaths import xml_set_attrib_value

    base_xpath = get_attrib_xpath(schema_dict, attributename, **kwargs)

    base_xpath, attributename = tuple(base_xpath.split('@'))

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

    return set_attrib_value(xmltree,
                            schema_dict,
                            attributename,
                            attribv,
                            complex_xpath=complex_xpath,
                            create=create,
                            occurrences=0,
                            **kwargs)


def set_text(xmltree, schema_dict, tag_name, text, complex_xpath=None, occurrences=None, create=False, **kwargs):

    from masci_tools.util.xml.xml_setters_xpaths import xml_set_text

    base_xpath = get_tag_xpath(schema_dict, tag_name, **kwargs)

    if complex_xpath is None:
        complex_xpath = base_xpath

    xmltree = xml_set_text(xmltree,
                           schema_dict,
                           complex_xpath,
                           base_xpath,
                           tag_name,
                           text,
                           occurrences=occurrences,
                           create=create)

    return xmltree


def set_first_text(xmltree, schema_dict, attributename, attribv, complex_xpath=None, create=False, **kwargs):
    return set_text(xmltree,
                    schema_dict,
                    attributename,
                    attribv,
                    complex_xpath=complex_xpath,
                    create=create,
                    occurrences=0,
                    **kwargs)


def set_simple_tag(xmltree, schema_dict, tag_name, changes, create_parents=False, **kwargs):

    from masci_tools.util.xml.xml_setters_xpaths import xml_set_simple_tag

    base_xpath = get_tag_xpath(schema_dict, tag_name, **kwargs)

    tag_info = schema_dict['tag_info'][base_xpath]

    assert len(tag_info['simple'] | tag_info['complex']) == 0, f"Given tag '{tag_name}' is not simple"

    return xml_set_simple_tag(xmltree,
                              schema_dict,
                              base_xpath,
                              base_xpath,
                              tag_name,
                              changes,
                              create_parents=create_parents)


def set_complex_tag(xmltree, schema_dict, tag_name, changes, create=False, **kwargs):

    from masci_tools.util.xml.xml_setters_xpaths import xml_set_complex_tag

    base_xpath = get_tag_xpath(schema_dict, tag_name, **kwargs)

    return xml_set_complex_tag(xmltree, schema_dict, base_xpath, base_xpath, changes, create=create)


def set_species_label(xmltree, schema_dict, atom_label, attributedict, create=False):
    """
    This method calls :func:`~masci_tools.util.xml.xml_setters_names.set_species()`
    method for a certain atom species that corresponds to an atom with a given label

    :param xmltree: xml etree of the inp.xml
    :param schema_dict: InputSchemaDict containing all information about the structure of the input
    :param atom_label: string, a label of the atom which specie will be changed. 'all' to change all the species
    :param attributedict: a python dict specifying what you want to change.
    :param create: bool, if species does not exist create it and all subtags?
    """
    from masci_tools.util.schema_dict_util import tag_exists, eval_simple_xpath
    from masci_tools.util.xml.common_xml_util import get_xml_attribute

    if atom_label == 'all':
        return set_species(xmltree, schema_dict, 'all', attributedict, create=create)

    atom_label = '{: >20}'.format(atom_label)
    all_groups = eval_simple_xpath(xmltree, schema_dict, 'atomGroup', list_return=True)

    species_to_set = set()

    # set all species, where given label is present
    for group in all_groups:
        if tag_exists(group, schema_dict, 'filmPos'):
            atoms = eval_simple_xpath(group, schema_dict, 'filmPos')
        else:
            atoms = eval_simple_xpath(group, schema_dict, 'relPos')
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
    Shifts value of a specie by label
    if at_label contains 'all' then applies to all species

    :param fleurinp_tree_copy: xml etree of the inp.xml
    :param at_label: string, a label of the atom which specie will be changed. 'all' if set up all species
    :param attr_name: name of the attribute to change
    :param value_given: value to add or to multiply by
    :param mode: 'rel' for multiplication or 'abs' for addition
    """
    from masci_tools.util.schema_dict_util import tag_exists, eval_simple_xpath
    from masci_tools.util.xml.common_xml_util import get_xml_attribute
    from masci_tools.util.xml.xml_setters_xpaths import xml_add_number_to_attrib

    if 'contains' in kwargs:
        contains = kwargs.get('contains')
        if not isinstance(contains, list):
            contains = [contains]
        contains.append('species')
        kwargs['contains'] = contains
    else:
        kwargs['contains'] = 'species'

    if 'exclude' not in kwargs:
        kwargs['exclude'] = ['other']
    elif 'other' not in kwargs['exclude']:
        kwargs['exclude'].append('other')

    species_base_path = get_tag_xpath(schema_dict, 'species')
    attr_base_path = get_attrib_xpath(schema_dict, attributename, **kwargs)
    attrib_base_xpath, attributename = tuple(attr_base_path.split('/@'))

    specie = ''
    if atom_label != 'all':
        atom_label = '{: >20}'.format(atom_label)
    all_groups = eval_simple_xpath(xmltree, schema_dict, 'atomGroup', list_return=True)

    species_to_set = set()

    for group in all_groups:
        if tag_exists(group, schema_dict, 'filmPos'):
            atoms = eval_simple_xpath(group, schema_dict, 'filmPos')
        else:
            atoms = eval_simple_xpath(group, schema_dict, 'relPos')
        for atom in atoms:
            label = get_xml_attribute(atom, 'label')
            if atom_label in ('all', label):
                species_to_set.add(get_xml_attribute(group, 'species'))

    for species_name in species_to_set:

        xpath_species = f'{species_base_path}[@name = "{specie}"]'
        attrib_xpath = attr_base_path.replace(species_base_path, xpath_species)

        xmltree = xml_add_number_to_attrib(xmltree,
                                           schema_dict,
                                           attrib_xpath,
                                           attrib_base_xpath,
                                           attributename,
                                           value_given,
                                           mode=mode)

    return xmltree


def set_atomgroup_label(xmltree, schema_dict, atom_label, attributedict, create=False):
    """
    This method calls :func:`~aiida_fleur.tools.xml_util.change_atomgr_att()`
    method for a certain atom specie that corresponds to an atom with a given label.

    :param fleurinp_tree_copy: xml etree of the inp.xml
    :param at_label: string, a label of the atom which specie will be changed. 'all' to change all the species
    :param attributedict: a python dict specifying what you want to change.

    :return fleurinp_tree_copy: xml etree of the new inp.xml

    **attributedict** is a python dictionary containing dictionaries that specify attributes
    to be set inside the certain specie. For example, if one wants to set a beta noco parameter it
    can be done via::

        'attributedict': {'nocoParams': [('beta', val)]}

    ``force`` and ``nocoParams`` keys are supported.
    To find possible keys of the inner dictionary please refer to the FLEUR documentation flapw.de
    """
    from masci_tools.util.schema_dict_util import tag_exists, eval_simple_xpath
    from masci_tools.util.xml.common_xml_util import get_xml_attribute

    if atom_label == 'all':
        xmltree = set_atomgroup(xmltree, schema_dict, attributedict, position=None, species='all')
        return xmltree

    atom_label = '{: >20}'.format(atom_label)
    all_groups = eval_simple_xpath(xmltree, schema_dict, 'atomGroup', list_return=True)

    species_to_set = set()

    # set all species, where given label is present
    for group in all_groups:
        if tag_exists(group, schema_dict, 'filmPos'):
            atoms = eval_simple_xpath(group, schema_dict, 'filmPos')
        else:
            atoms = eval_simple_xpath(group, schema_dict, 'relPos')
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

    :param fleurinp_tree_copy: xml etree of the inp.xml
    :param attributedict: a python dict specifying what you want to change.
    :param position: position of an atom group to be changed. If equals to 'all', all species will be changed
    :param species: atom groups, corresponding to the given specie will be changed
    :param create: bool, if species does not exist create it and all subtags?

    :return fleurinp_tree_copy: xml etree of the new inp.xml

    **attributedict** is a python dictionary containing dictionaries that specify attributes
    to be set inside the certain specie. For example, if one wants to set a beta noco parameter it
    can be done via::

        'attributedict': {'nocoParams': {'beta': val]}

    ``force`` and ``nocoParams`` keys are supported.
    To find possible keys of the inner dictionary please refer to the FLEUR documentation flapw.de
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
    Shifts numertical values of some tags directly in the inp.xml file.

    :param fleurinp_tree_copy: a lxml tree that represents inp.xml
    :param change_dict: a python dictionary with the keys to shift.
    :param mode: 'abs' if change given is absolute, 'rel' if relative

    :returns new_tree: a lxml tree with shifted values

    An example of change_dict::

            change_dict = {'itmax' : 1, 'dVac': -0.123}
    """

    if path_spec is None:
        path_spec = {}

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
    This modifies the xml-inp file. Makes all the changes wanted by
    the user or sets some default values for certain modes

    :params xmltree: xml-tree of the xml-inp file
    :params change_dict: dictionary {attrib_name : value} with all the wanted changes.

    :returns: an etree of the xml-inp file with changes.
    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_first_attrib_value, xml_set_text

    if path_spec is None:
        path_spec = {}

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
            key_xpath, key = tuple(key_xpath.split('/@'))

        if text_attrib:
            xml_set_text(xmltree, schema_dict, key_xpath, key_xpath, change_value)
        else:
            xml_set_first_attrib_value(xmltree, schema_dict, key_xpath, key_xpath, key, change_value)

    return xmltree
