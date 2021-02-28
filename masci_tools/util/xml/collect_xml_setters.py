# -*- coding: utf-8 -*-
"""
Collect all functions that should be exposed to the :py:class:`~masci_tools.io.io_fleurxmlmodifier.FleurXMLModifier`
and classify them according to their interface. This makes extending functionality for the Modifier relatively easy

   1. Implement the method in the correct module for its level of functionality
         :xml_setters_basic: Xpath as argument and no ability to create missing subtags on the fly
         :xml_setters_xpaths: Xpath(s) and schema dictionary as argument. Can add creation type/checking and so on
         :xml_setters_names: No Xpaths as arguments Only names/identifiers for the schema dict
   2. Import it in this file and put the method in the correct SET at the bottom
   3. Write facade method to add task for this function in :py:class:`~masci_tools.io.io_fleurxmlmodifier.FleurXMLModifier`
      This is not automatized to guarantee that we have some nice docstrings for all the modifiying functions at the surface level
"""

from .xml_setters_names import set_inpchanges, shift_value, set_species, set_species_label, shift_value_species_label,\
                               set_complex_tag, set_simple_tag, create_tag, set_text, set_first_text, set_attrib_value,\
                               set_first_attrib_value, set_atomgroup, set_atomgroup_label, add_number_to_attrib, add_number_to_first_attrib

from .xml_setters_basic import xml_create_tag, xml_set_attrib_value_no_create, xml_set_text_no_create, \
                               xml_replace_tag, xml_delete_tag, xml_delete_att

from .xml_setters_nmmpmat import set_nmmpmat, rotate_nmmpmat

__XPATH_SET = {
    xml_create_tag, xml_set_text_no_create, xml_set_attrib_value_no_create, xml_replace_tag, xml_delete_att,
    xml_delete_tag
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
