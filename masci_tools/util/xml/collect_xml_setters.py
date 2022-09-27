"""
Collect all functions that should be exposed to the :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`
and classify them according to their interface. This makes extending functionality for the Modifier relatively easy

   1. Implement the method in the correct module for its level of functionality
         :xml_setters_basic: Xpath as argument and no ability to create missing subtags on the fly
         :xml_setters_xpaths: Xpath(s) and schema dictionary as argument. Can add creation type/checking and so on
         :xml_setters_names: No Xpaths as arguments Only names/identifiers for the schema dict
   2. Import it in this file and put the method in the correct SET at the bottom
   3. Write facade method to add task for this function in :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier`
      This is not automated to guarantee that we have some nice docstrings for all the modifiying functions at the surface level
"""

from typing import Callable, Set
from .xml_setters_names import set_inpchanges, shift_value, set_species, set_species_label, shift_value_species_label,\
                               set_complex_tag, set_simple_tag, create_tag, set_text, set_first_text, set_attrib_value,\
                               set_first_attrib_value, set_atomgroup, set_atomgroup_label, add_number_to_attrib, add_number_to_first_attrib, \
                               set_nkpts, set_kpath, switch_kpointset, set_kpointlist, delete_att, delete_tag, replace_tag, \
                               clone_species, switch_species, switch_species_label, set_xcfunctional, set_kpointpath, set_kpointmesh

from .xml_setters_basic import xml_create_tag, xml_set_attrib_value_no_create, xml_set_text_no_create, \
                               xml_replace_tag, xml_delete_tag, xml_delete_att

from .xml_setters_nmmpmat import set_nmmpmat, rotate_nmmpmat, align_nmmpmat_to_sqa

__XPATH_SET: Set[Callable] = {
    xml_create_tag, xml_set_text_no_create, xml_set_attrib_value_no_create, xml_replace_tag, xml_delete_att,
    xml_delete_tag
}

__SCHEMA_DICT_SET: Set[Callable] = {
    set_inpchanges, shift_value, set_species, set_species_label, shift_value_species_label, set_complex_tag,
    set_simple_tag, create_tag, set_text, set_first_text, set_attrib_value, set_first_attrib_value, set_atomgroup,
    set_atomgroup_label, add_number_to_attrib, add_number_to_first_attrib, set_nkpts, set_kpath, switch_kpointset,
    set_kpointlist, delete_att, delete_tag, replace_tag, switch_species, switch_species_label, clone_species,
    set_xcfunctional, set_kpointpath, set_kpointmesh
}

__NMMPMAT_SET: Set[Callable] = {set_nmmpmat, rotate_nmmpmat, align_nmmpmat_to_sqa}

XPATH_SETTERS = {func.__name__: func for func in __XPATH_SET}
SCHEMA_DICT_SETTERS = {func.__name__: func for func in __SCHEMA_DICT_SET}
NMMPMAT_SETTERS = {func.__name__: func for func in __NMMPMAT_SET}
