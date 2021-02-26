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


def get_tag_or_create(xmltree, schema_dict, tag_name, create_parents=False, complex_xpath=None, **kwargs):

    from masci_tools.util.xml.xml_setters_xpaths import eval_xpath_create

    base_xpath = get_tag_xpath(schema_dict, tag_name, **kwargs)

    parent_xpath, tag_name = '/'.join(base_xpath.split('/')[:-1]), base_xpath.split('/')[-1]
    if complex_xpath is None:
        complex_xpath = parent_xpath

    xmltree = eval_xpath_create(xmltree, schema_dict, complex_xpath, base_xpath, create_parents=create_parents)

    return xmltree


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


def set_species(xmltree, schema_dict, species_name, attributedict, create=False):
    """
    Method to set parameters of a species tag of the fleur inp.xml file.

    :param fleurinp_tree_copy: xml etree of the inp.xml
    :param species_name: string, name of the specie you want to change
    :param attributedict: a python dict specifying what you want to change.
    :param create: bool, if species does not exist create it and all subtags?

    :raises ValueError: if species name is non existent in inp.xml and should not be created.
                        also if other given tags are garbage. (errors from eval_xpath() methods)

    :return fleurinp_tree_copy: xml etree of the new inp.xml

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


def set_inpchanges(xmltree, schema_dict, change_dict, path_spec=None):
    """
    This modifies the xml-inp file. Makes all the changes wanted by
    the user or sets some default values for certain modes

    :params xmltree: xml-tree of the xml-inp file
    :params change_dict: dictionary {attrib_name : value} with all the wanted changes.

    :returns: an etree of the xml-inp file with changes.
    """
    from masci_tools.util.xml.xml_setters_xpaths import xml_set_first_attrib_value, xml_set_text
    from masci_tools.util.xml.common_xml_util import convert_to_fortran_bool

    if path_spec is None:
        path_spec = {}

    for key, change_value in change_dict.items():

        #Special alias for xcFunctional since name is not a very telling attribute name
        if key == 'xcFunctional':
            key = 'name'

        if key not in schema_dict['attrib_types'] and key not in schema_dict['simple_elements']:
            raise ValueError(f"You try to set the key:'{key}' to : '{change_value}', but the key is unknown"
                             ' to the fleur plug-in')

        text_attrib = False
        if key in schema_dict['attrib_types']:
            possible_types = schema_dict['attrib_types'][key]
        else:
            text_attrib = True

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
            if 'switch' in possible_types:
                # TODO: a test here if path is plausible and if exist
                # ggf. create tags and key.value is 'T' or 'F' if not convert,
                # if garbage, exception
                # convert user input into 'fleurbool'
                fleur_bool = convert_to_fortran_bool(change_value)

                # TODO: check if something in setup is inconsitent?
                xml_set_first_attrib_value(xmltree, schema_dict, key_xpath, key_xpath, key, fleur_bool)
            elif 'float' in possible_types:
                newfloat = '{:.10f}'.format(change_value)
                xml_set_first_attrib_value(xmltree, schema_dict, key_xpath, key_xpath, key, newfloat)
            elif 'float_expression' in possible_types:
                try:
                    newfloat = '{:.10f}'.format(change_value)
                except ValueError:
                    newfloat = change_value
                xml_set_first_attrib_value(xmltree, schema_dict, key_xpath, key_xpath, key, newfloat)
            else:
                xml_set_first_attrib_value(xmltree, schema_dict, key_xpath, key_xpath, key, change_value)

    return xmltree
