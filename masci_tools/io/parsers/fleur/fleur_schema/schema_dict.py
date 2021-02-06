# -*- coding: utf-8 -*-
from masci_tools.util.lockable_containers import LockableDict
from masci_tools.util.schema_dict_util import get_tag_xpath, get_attrib_xpath, get_tag_info
from .inpschema_todict import load_inpschema
from .outschema_todict import load_outschema

PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def _get_latest_available_version():
    latest_version = 0
    #Get latest version available
    for root, dirs, files in os.walk(PACKAGE_DIRECTORY):
        for folder in dirs:
            if '0.' in folder:
                latest_version = max(latest_version, int(folder.split('.')[1]))
    return f'0.{latest_version}'


class SchemaDict(LockableDict):

    def __init__(self, *args, xmlschema=None, **kwargs):
        self.xmlschema = xmlschema
        super().__init__(*args, **kwargs)
        super().freeze()

    def get_tag_xpath(self, name, contains=None, not_contains=None):
        return get_tag_xpath(self, name, contains=contains, not_contains=not_contains)

    def get_attrib_xpath(self, name, contains=None, not_contains=None, exclude=None, tag_name=None):
        return get_attrib_xpath(self,
                                name,
                                contains=contains,
                                not_contains=not_contains,
                                exclude=exclude,
                                tag_name=tag_name)

    def get_tag_info(self, name, contains=None, not_contains=None):
        return get_tag_info(self, name, contains=contains, not_contains=not_contains)



class InputSchemaDict(SchemaDict):
    """
    This class contains information parsed from the FleurInputSchema.xsd

    The keys contain the following information:

        - 'inp_version': Version string of the input schema represented in this object
        - 'tag_paths': simple xpath expressions to all valid tag names
                       Multiple paths or ambiguous tag names are parsed as a list
        - '_basic_types': Parsed definitions of all simple Types with their respective
                          base type (int, float, ...) and evtl. length restrictions
                         (Only used in the schema construction itself)
        - 'attrib_types': All possible base types for all valid attributes. If multiple are
                          possible a list, with 'string' always last (if possible)
        - 'simple_elements': All elements with simple types and their type definition
                             with the additional attributes
        - 'unique_attribs': All attributes and their paths, which occur only once and
                            have a unique path
        - 'unique_path_attribs': All attributes and their paths, which have a unique path
                                 but occur in multiple places
        - 'other_attribs': All attributes and their paths, which are not in 'unique_attribs' or
                           'unique_path_attribs'
        - 'omitt_contained_tags': All tags, which only contain a list of one other tag
        - 'tag_info': For each tag (path), the valid attributes and tags (optional, several,
                      order, simple, text)
    """
    __schema_dict_cache = {}

    @classmethod
    def fromVersion(cls, version, parser_info_out=None):

        if version in cls.__schema_dict_cache:
            return cls.__schema_dict_cache[version]

        schema_dict, xmlschema = load_inpschema(version, schema_return=True, parser_info_out=parser_info_out)

        new_schema = cls(schema_dict, xmlschema=xmlschema)

        cls.__schema_dict_cache[version] = new_schema

        return new_schema


class OutputSchemaDict(SchemaDict):
    """
    This object contains information parsed from the FleurOutputSchema.xsd

    The keys contain the following information:

        - 'out_version': Version string of the output schema represented in this class
        - 'input_tag': Name of the element containing the fleur input
        - 'tag_paths': simple xpath expressions to all valid tag names not in an iteration
                       Multiple paths or ambiguous tag names are parsed as a list
        - 'iteration_tag_paths': simple relative xpath expressions to all valid tag names
                                 inside an iteration. Multiple paths or ambiguous tag names
                                 are parsed as a list
        - '_basic_types': Parsed definitions of all simple Types with their respective
                          base type (int, float, ...) and evtl. length restrictions
                         (Only used in the schema construction itself)
        - '_input_basic_types': Part of the parsed definitions of all simple Types with their
                                respective base type (int, float, ...) and evtl. length
                                restrictions from the input schema
                                (Only used in the schema construction itself)
        - 'attrib_types': All possible base types for all valid attributes. If multiple are
                          possible a list, with 'string' always last (if possible)
        - 'simple_elements': All elements with simple types and their type definition
                             with the additional attributes
        - 'unique_attribs': All attributes and their paths, which occur only once and
                            have a unique path outside of an iteration
        - 'unique_path_attribs': All attributes and their paths, which have a unique path
                                 but occur in multiple places outside of an iteration
        - 'other_attribs': All attributes and their paths, which are not in 'unique_attribs' or
                           'unique_path_attribs' outside of an iteration
        - 'iteration_unique_attribs': All attributes and their relative paths, which occur
                                      only once and have a unique path inside of an iteration
        - 'iteration_unique_path_attribs': All attributes and their relative paths, which have
                                           a unique path but occur in multiple places inside
                                           of an iteration
        - 'iteration_other_attribs': All attributes and their relative paths, which are not
                                     in 'unique_attribs' or 'unique_path_attribs' inside
                                     of an iteration
        - 'omitt_contained_tags': All tags, which only contain a list of one other tag
        - 'tag_info': For each tag outside of an iteration (path), the valid attributes
                      and tags (optional, several, order, simple, text)
        - 'iteration_tag_info': For each tag inside of an iteration (relative path),
                                the valid attributes and tags (optional, several,
                                order, simple, text)
    """
    __schema_dict_cache = {}

    @classmethod
    def fromVersion(cls, version, inp_version=None, parser_info_out=None):

        if inp_version is None:
            inp_version = version
        version_hash = hash((version, inp_version))

        if version_hash in cls.__schema_dict_cache:
            return cls.__schema_dict_cache[version_hash]

        schema_dict, xmlschema = load_outschema(version, schema_return=True, inp_version=inp_version, parser_info_out=parser_info_out)

        new_schema = cls(schema_dict, xmlschema=xmlschema)

        cls.__schema_dict_cache[version_hash] = new_schema

        return new_schema
