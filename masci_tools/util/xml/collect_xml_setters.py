# -*- coding: utf-8 -*-
"""
Collect all functions that should be exposed to the fleurinpmodifier in aiida_fleur
"""

from .xml_setters_names import set_inpchanges, shift_value, set_species, set_species_label, shift_value_species_label,\
                               set_complex_tag, set_simple_tag, create_tag, set_text, set_first_text, set_attrib_value,\
                               set_first_attrib_value, set_atomgroup, set_atomgroup_label, add_number_to_attrib, add_number_to_first_attrib

from .xml_setters_basic import xml_create_tag, xml_set_attrib_value_no_create, xml_set_text_no_create, \
                               xml_replace_tag, xml_delete_tag, xml_delete_att

from .xml_setters_nmmpmat import set_nmmpmat, rotate_nmmpmat

__XPATH_SET = {
    xml_create_tag, xml_set_text_no_create, xml_set_attrib_value_no_create, xml_replace_tag, xml_delete_att, xml_delete_tag
}

__SCHEMA_DICT_SET = {
    set_inpchanges, shift_value, set_species, set_species_label, shift_value_species_label, set_complex_tag,
    set_simple_tag, create_tag, set_text, set_first_text, set_attrib_value, set_first_attrib_value, set_atomgroup,
    set_atomgroup_label, add_number_to_attrib, add_number_to_first_attrib
}

__NMMPMAT_SET = {set_nmmpmat, rotate_nmmpmat}

XPATH_SETTERS = {func.__name__: func for func in __XPATH_SET}
SCHEMA_DICT_SETTERS = {func.__name__: func for func in __SCHEMA_DICT_SET}
NMMPMAT_SETTERS = {func.__name__: func for func in __NMMPMAT_SET}
