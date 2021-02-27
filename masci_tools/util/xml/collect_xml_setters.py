"""
Collect all functions that should be exposed to the fleurinpmodifier in aiida_fleur
"""

from .xml_setters_names import set_inpchanges, set_species, set_complex_tag, set_simple_tag,\
                               create_tag
from .xml_setters_basic import create_tag_xpath, xml_set_attrib_value_no_create, xml_set_text_no_create, \
                               replace_tag, delete_tag, delete_att

__XPATH_SET = {create_tag_xpath, xml_set_text_no_create, xml_set_attrib_value_no_create, replace_tag, delete_att, delete_tag}
__SCHEMA_DICT_SET = {set_inpchanges, set_species, set_complex_tag, set_simple_tag, create_tag}

XPATH_SETTERS = {func.__name__: func for func in __XPATH_SET}
SCHEMA_DICT_SETTERS = {func.__name__: func for func in __SCHEMA_DICT_SET}




