# -*- coding: utf-8 -*-
"""
Test to make sure that signatures of the functions exposed to the FleurXMLModifier
are not changed by accident.
"""


def test_xml_setter_signatures(data_regression):
    """
    This tests compares the signatures of the xml setter functions to a stored version
    to make sure that changes are noticed. Also makes sure, that the functions ahve the right expected
    arguments for their classification

    If the change is not a completely optional added new keyword argument the change
    should be considered carefully, since the signature will be exposed to the FleurinpModifier in
    aiida-fleur. So changes should be clearly communicated.
    """
    from masci_tools.util.xml.collect_xml_setters import XPATH_SETTERS, SCHEMA_DICT_SETTERS, NMMPMAT_SETTERS
    from inspect import signature

    signature_dict = {'xpath': {}, 'schema_dict': {}, 'nmmpmat': {}}

    for func_name, func in XPATH_SETTERS.items():
        sig = signature(func)

        assert list(sig.parameters.keys())[:2] == ['xmltree', 'xpath'], \
               f'Function {func_name} should take xmltree and xpath as its first arguments. Got: {list(sig.parameters.keys())[:2]}'

        signature_dict['xpath'][func_name] = []

        for name, param in sig.parameters.items():
            signature_dict['xpath'][func_name].append(
                (name, param.default if param.default is not param.empty else None))

    for func_name, func in SCHEMA_DICT_SETTERS.items():
        sig = signature(func)

        assert list(sig.parameters.keys())[:2] == ['xmltree', 'schema_dict'], \
               f'Function {func_name} should take xmltree and schema_dict as its first arguments. Got: {list(sig.parameters.keys())[:2]}'

        signature_dict['schema_dict'][func_name] = []

        for name, param in sig.parameters.items():
            signature_dict['schema_dict'][func_name].append(
                (name, param.default if param.default is not param.empty else None))

    for func_name, func in NMMPMAT_SETTERS.items():
        sig = signature(func)

        assert list(sig.parameters.keys())[:3] == ['xmltree', 'nmmplines', 'schema_dict'], \
               f'Function {func_name} should take xmltree, nmmplinesa and schema_dict as its first arguments. Got: {list(sig.parameters.keys())[:3]}'

        signature_dict['nmmpmat'][func_name] = []

        for name, param in sig.parameters.items():
            signature_dict['nmmpmat'][func_name].append(
                (name, param.default if param.default is not param.empty else None))

    data_regression.check(signature_dict)
