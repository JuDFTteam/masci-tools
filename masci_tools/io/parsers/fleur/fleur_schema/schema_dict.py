# -*- coding: utf-8 -*-
from masci_tools.util.lockable_containers import LockableDict
from masci_tools.util.schema_dict_util import get_tag_xpath, get_attrib_xpath, get_tag_info
from .inpschema_todict import load_inpschema
from .outschema_todict import load_outschema


class SchemaDict(LockableDict):

    def __init__(self, *args, input_schema=True, **kwargs):

        if input_schema:
            schema_dict, self.xmlschema = load_inpschema(*args, schema_return=True, **kwargs)
        else:
            schema_dict, self.xmlschema = load_outschema(*args, schema_return=True, **kwargs)

        #Here we initialize the LockableDict and lock it immediately afterwards
        super().__init__(schema_dict)
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
