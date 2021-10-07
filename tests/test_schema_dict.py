# -*- coding: utf-8 -*-
"""
Test of the consistency the input schema dictionaries with the SchemaFiles in the same folder
"""
import pytest
import os
from masci_tools.io.parsers.fleur.fleur_schema import InputSchemaDict, OutputSchemaDict, NoPathFound, NoUniquePathFound
from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict, CaseInsensitiveFrozenSet
from masci_tools.util.lockable_containers import LockableDict, LockableList

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = '../masci_tools/io/parsers/fleur/fleur_schema'

#Collect all schemas from the folder
schema_versions = {'inp': [], 'out': []}
for root, dirs, files in os.walk(os.path.abspath(os.path.join(CURRENT_DIR, SCHEMA_DIR))):
    for folder in dirs:
        if '0.' in folder:
            schema_versions['inp'].append(folder)
            if int(folder.split('.')[1]) >= 33 or folder in ('0.31', '0.30', '0.29'):
                schema_versions['out'].append(folder)


def test_inpschema_dict_structure():
    """
    Test the types of the keys in the inpschemadict
    """

    inputschema = InputSchemaDict.fromVersion('0.34')

    EXPECTED_TYPES = {
        'tag_paths': CaseInsensitiveDict,
        'unique_attribs': CaseInsensitiveDict,
        'unique_path_attribs': CaseInsensitiveDict,
        'other_attribs': CaseInsensitiveDict,
        'attrib_types': CaseInsensitiveDict,
        'text_types': CaseInsensitiveDict,
        'text_tags': CaseInsensitiveFrozenSet,
        '_basic_types': LockableDict,
        'root_tag': str,
        'inp_version': str,
        'omitt_contained_tags': LockableList,
        'tag_info': LockableDict
    }

    for key, val in inputschema.items():
        assert isinstance(val, EXPECTED_TYPES[key])
        if EXPECTED_TYPES[key] != str:
            if not isinstance(val, CaseInsensitiveFrozenSet):
                assert val._locked
            if EXPECTED_TYPES[key] != CaseInsensitiveDict:
                assert not isinstance(val,
                                      CaseInsensitiveDict)  #since CaseInsensitiveDict is a subclass of LockableDict


def test_outschema_dict_structure():
    """
    Test the types of the keys in the inpschemadict
    """

    outputschema = OutputSchemaDict.fromVersion('0.34')

    EXPECTED_TYPES = {
        'tag_paths': CaseInsensitiveDict,
        'unique_attribs': CaseInsensitiveDict,
        'unique_path_attribs': CaseInsensitiveDict,
        'other_attribs': CaseInsensitiveDict,
        'iteration_tag_paths': CaseInsensitiveDict,
        'iteration_unique_attribs': CaseInsensitiveDict,
        'iteration_unique_path_attribs': CaseInsensitiveDict,
        'iteration_other_attribs': CaseInsensitiveDict,
        'attrib_types': CaseInsensitiveDict,
        'text_types': CaseInsensitiveDict,
        'text_tags': CaseInsensitiveFrozenSet,
        '_basic_types': LockableDict,
        '_input_basic_types': LockableDict,
        'root_tag': str,
        'input_tag': str,
        'out_version': str,
        'inp_version': str,
        'omitt_contained_tags': LockableList,
        'tag_info': LockableDict,
        'iteration_tag_info': LockableDict
    }

    for key, val in outputschema.items():
        assert isinstance(val, EXPECTED_TYPES[key])
        if EXPECTED_TYPES[key] != str:
            if not isinstance(val, CaseInsensitiveFrozenSet):
                assert val._locked
            if EXPECTED_TYPES[key] != CaseInsensitiveDict:
                assert not isinstance(val,
                                      CaseInsensitiveDict)  #since CaseInsensitiveDict is a subclass of LockableDict


@pytest.mark.parametrize('schema_version', schema_versions['inp'])
def test_inpschema_dict(data_regression, schema_version):
    """
    Test the produced inputschema dicts
    """

    inputschema = InputSchemaDict.fromVersion(version=schema_version)

    data_regression.check(clean_for_reg_dump(inputschema.get_unlocked()))


@pytest.mark.parametrize('inp_version', schema_versions['inp'])
@pytest.mark.parametrize('out_version', schema_versions['out'])
def test_outschema_dict(data_regression, inp_version, out_version):
    """
    Test the fleur_schema_parser_functions to make sure that they match the stored inputschema_dict
    """

    outputschema = OutputSchemaDict.fromVersion(version=out_version, inp_version=inp_version)

    data_regression.check(clean_for_reg_dump(outputschema.get_unlocked()))

def test_tag_xpath_input():
    """
    Test the path finding for tags for the input schema without additional options
    And verify with different version of the schema
    """

    schema_dict = InputSchemaDict.fromVersion('0.27')


    #First example easy (magnetism tag is unique and should not differ between the versions)
    assert schema_dict.tag_xpath('magnetism') == '/fleurInput/calculationSetup/magnetism'
    #Differing paths between the version
    assert schema_dict.tag_xpath('bzIntegration') == '/fleurInput/calculationSetup/bzIntegration'

    #Non existent tag in old version
    with pytest.raises(NoPathFound):
        schema_dict.tag_xpath('DMI')
    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_xpath('ldaU')

    schema_dict = InputSchemaDict.fromVersion('0.34')

    assert schema_dict.tag_xpath('magnetism') == '/fleurInput/calculationSetup/magnetism'
    assert schema_dict.tag_xpath('bzIntegration') == '/fleurInput/cell/bzIntegration'

    assert schema_dict.tag_xpath('DMI') == '/fleurInput/forceTheorem/DMI'
    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_xpath('ldaU')

def test_relative_tag_xpath_input():
    """
    Test the path finding for tags for the input schema without additional options
    And verify with different version of the schema
    """

    schema_dict = InputSchemaDict.fromVersion('0.34')

    assert schema_dict.relative_tag_xpath('magnetism', 'calculationSetup') == './magnetism'
    assert schema_dict.relative_tag_xpath('magnetism', 'magnetism') == '.'

    assert schema_dict.relative_tag_xpath('DMI', 'forceTheorem') == './DMI'
    with pytest.raises(NoUniquePathFound):
        schema_dict.relative_tag_xpath('ldaU', 'fleurInput')

    assert schema_dict.relative_tag_xpath('ldaU', 'fleurInput',
                                  contains='species') == './atomSpecies/species/ldaU'
    assert schema_dict.relative_tag_xpath('ldaU', 'species') == './ldaU'

    schema_dict = InputSchemaDict.fromVersion('0.27')
    with pytest.raises(NoPathFound):
        schema_dict.relative_tag_xpath('DMI', 'forceTheorem')

def test_tag_xpath_output():
    """
    Test the path finding for tags for the output schema without additional options
    And verify with different version of the schema
    """
    from masci_tools.util.schema_dict_util import get_tag_xpath

    schema_dict = OutputSchemaDict.fromVersion('0.34')

    assert schema_dict.tag_xpath('iteration') == '/fleurOutput/scfLoop/iteration'
    assert schema_dict.tag_xpath('totalEnergy') == './totalEnergy'
    assert schema_dict.tag_xpath('fleurInput') == '/fleurOutput/fleurInput'
    with pytest.raises(NoPathFound):
        schema_dict.tag_xpath('inputData')
    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_xpath('spinDependentCharge')
   
    schema_dict = OutputSchemaDict.fromVersion('0.31')

    assert schema_dict.tag_xpath('iteration') == '/fleurOutput/scfLoop/iteration'
    assert schema_dict.tag_xpath('totalEnergy') == './totalEnergy' 
    with pytest.raises(NoPathFound):
        schema_dict.tag_xpath('fleurInput')
    assert schema_dict.tag_xpath('inputData') == '/fleurOutput/inputData'
    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_xpath('spinDependentCharge')
   

def test_relative_tag_xpath_output():
    """
    Test the path finding for tags for the input schema without additional options
    And verify with different version of the schema
    """

    schema_dict = OutputSchemaDict.fromVersion('0.34')

    assert schema_dict.relative_tag_xpath('iteration', 'scfLoop') == './iteration'
    assert schema_dict.relative_tag_xpath('iteration', 'iteration') == '.'
    assert schema_dict.relative_tag_xpath('densityMatrixFor', 'ldaUDensityMatrix') == './densityMatrixFor'


def test_get_tag_xpath_contains():
    """
    Test the selection of paths based on a contained keyword
    """

    schema_dict = InputSchemaDict.fromVersion('0.34')

    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_xpath('ldaU')
    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_xpath('ldaU', contains='atom')

    assert schema_dict.tag_xpath('ldaU', contains='calculationSetup') == '/fleurInput/calculationSetup/ldaU'
    assert schema_dict.tag_xpath('ldaU', contains='species') == '/fleurInput/atomSpecies/species/ldaU'
    assert schema_dict.tag_xpath('ldaU', contains='Group') == '/fleurInput/atomGroups/atomGroup/ldaU'

    with pytest.raises(NoPathFound):
        schema_dict.tag_xpath('ldaU', contains='group')


def test_get_tag_xpath_notcontains():
    """
    Test the selection of paths based on a not contained keyword
    """

    schema_dict = InputSchemaDict.fromVersion('0.34')

    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_xpath('ldaU')
    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_xpath('ldaU', not_contains='calculationSetup')

    assert schema_dict.tag_xpath('ldaU', not_contains='atom') == '/fleurInput/calculationSetup/ldaU'
    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_xpath('ldaU', not_contains='Group')

    assert schema_dict.tag_xpath('ldaU', contains='atom',
                         not_contains='species') == '/fleurInput/atomGroups/atomGroup/ldaU'


def test_get_tagattrib_xpath_case_insensitivity():
    """
    Test that the selection works with case insensitivity
    """

    schema_dict = InputSchemaDict.fromVersion('0.34')

    assert schema_dict.tag_xpath('bzIntegration') == '/fleurInput/cell/bzIntegration'
    assert schema_dict.tag_xpath( 'BZINTEGRATION') == '/fleurInput/cell/bzIntegration'
    assert schema_dict.tag_xpath('bzintegration') == '/fleurInput/cell/bzIntegration'
    assert schema_dict.tag_xpath('bZInTegrAtIon') == '/fleurInput/cell/bzIntegration'

    assert schema_dict.attrib_xpath('jspins') == '/fleurInput/calculationSetup/magnetism/@jspins'
    assert schema_dict.attrib_xpath('JSPINS') == '/fleurInput/calculationSetup/magnetism/@jspins'
    assert schema_dict.attrib_xpath('jSpInS') == '/fleurInput/calculationSetup/magnetism/@jspins'


def test_get_attrib_xpath_input():
    """
    Test the path finding for tags for the input schema without additional options
    And verify with different version of the schema
    """

    schema_dict = InputSchemaDict.fromVersion('0.34')
    
    assert schema_dict.attrib_xpath('jspins') == '/fleurInput/calculationSetup/magnetism/@jspins'
    assert schema_dict.attrib_xpath( 'mode') == '/fleurInput/cell/bzIntegration/@mode'
    assert schema_dict.attrib_xpath('l_mtNocoPot',
                            exclude=['other']) == '/fleurInput/calculationSetup/magnetism/mtNocoParams/@l_mtNocoPot'
    with pytest.raises(NoUniquePathFound):
        schema_dict.attrib_xpath('l_amf')

    schema_dict = InputSchemaDict.fromVersion('0.27')

    assert schema_dict.attrib_xpath('jspins') == '/fleurInput/calculationSetup/magnetism/@jspins'
    assert schema_dict.attrib_xpath('mode') == '/fleurInput/calculationSetup/bzIntegration/@mode'
    with pytest.raises(NoPathFound):
        schema_dict.attrib_xpath('l_mtNocoPot')

    #Multiple possible paths
    with pytest.raises(NoUniquePathFound):
        schema_dict.attrib_xpath('l_amf')


def test_get_relative_attrib_xpath_input():
    """
    Test the path finding for tags for the input schema without additional options
    And verify with different version of the schema
    """
    
    schema_dict = InputSchemaDict.fromVersion('0.34')

    #First example easy (magnetism tag is unique and should not differ between the versions)
    assert schema_dict.relative_attrib_xpath('jspins', 'calculationSetup') == './magnetism/@jspins'
    assert schema_dict.relative_attrib_xpath('jspins', 'magnetism') == './@jspins'

    assert schema_dict.relative_attrib_xpath('jspins', 'magnetism', tag_name='magnetism') == './@jspins'

    with pytest.raises(NoPathFound):
        schema_dict.relative_attrib_xpath('jspins', 'calculationSetup', tag_name='calculationSetup')

    #Non existent tag in old version
    assert schema_dict.relative_attrib_xpath('l_mtNocoPot', 'magnetism') == './mtNocoParams/@l_mtNocoPot'
    with pytest.raises(NoUniquePathFound):
        schema_dict.relative_attrib_xpath('l_mtNocoPot', 'fleurInput')

    with pytest.raises(NoPathFound):
        schema_dict.relative_attrib_xpath('l_mtNocoPot', 'output')

    #Multiple possible paths
    with pytest.raises(NoUniquePathFound):
        schema_dict.relative_attrib_xpath('l_amf', 'fleurInput')

    assert schema_dict.relative_attrib_xpath('l_amf', 'fleurInput', contains='species',
                                     not_contains='ldaHIA') == './atomSpecies/species/ldaU/@l_amf'
    assert schema_dict.relative_attrib_xpath('l_amf', 'ldaU') == './@l_amf'


def test_get_attrib_xpath_output():
    """
    Test the path finding for tags for the input schema without additional options
    And verify with different version of the schema
    """

    schema_dict = OutputSchemaDict.fromVersion('0.34')
    assert schema_dict.attrib_xpath('nat') == '/fleurOutput/numericalParameters/atomsInCell/@nat'
    assert schema_dict.attrib_xpath('qvectors') == './Forcetheorem_SSDISP/@qvectors'

    schema_dict = OutputSchemaDict.fromVersion('0.31')
    assert schema_dict.attrib_xpath('nat') == '/fleurOutput/numericalParameters/atomsInCell/@nat'
    assert schema_dict.attrib_xpath('qvectors') == './Forcetheorem_SSDISP/@qvectors'


def test_get_relative_attrib_xpath_output():
    """
    Test the path finding for tags for the input schema without additional options
    And verify with different version of the schema
    """
    schema_dict = OutputSchemaDict.fromVersion('0.34')

    assert schema_dict.relative_attrib_xpath('nat', 'numericalParameters') == './atomsInCell/@nat'
    assert schema_dict.relative_attrib_xpath('nat', 'atomsInCell') == './@nat'

    assert schema_dict.relative_attrib_xpath('qvectors', '.') == './Forcetheorem_SSDISP/@qvectors'
    assert schema_dict.relative_attrib_xpath('qvectors', 'Forcetheorem_SSDISP') == './@qvectors'


def test_get_attrib_xpath_contains():
    """
    Test the selection of paths based on a contained keyword
    """

    schema_dict = InputSchemaDict.fromVersion('0.34')

    with pytest.raises(NoUniquePathFound):
        schema_dict.attrib_xpath('l_mperp')

    assert schema_dict.attrib_xpath('l_mperp',
                            contains='magnetism') == '/fleurInput/calculationSetup/magnetism/mtNocoParams/@l_mperp'
    assert schema_dict.attrib_xpath('l_mperp',
                            contains='greensFunction') == '/fleurInput/calculationSetup/greensFunction/@l_mperp'

    with pytest.raises(NoPathFound):
        schema_dict.attrib_xpath('l_mperp', contains='atom')


def test_get_attrib_xpath_notcontains():
    """
    Test the selection of paths based on a contained keyword
    """

    schema_dict = InputSchemaDict.fromVersion('0.34')

    with pytest.raises(NoUniquePathFound):
        schema_dict.attrib_xpath('l_mperp')

    assert  schema_dict.attrib_xpath('l_mperp',
        not_contains='greensFunction') == '/fleurInput/calculationSetup/magnetism/mtNocoParams/@l_mperp'
    assert  schema_dict.attrib_xpath('l_mperp',
                            not_contains='magnetism') == '/fleurInput/calculationSetup/greensFunction/@l_mperp'

    assert  schema_dict.attrib_xpath('l_mperp', contains='greensFunction',
                            not_contains='magnetism') == '/fleurInput/calculationSetup/greensFunction/@l_mperp'

    with pytest.raises(NoPathFound):
         schema_dict.attrib_xpath('l_mperp', not_contains='calculationSetup')


def test_get_attrib_xpath_exclude():
    """
    Test the selection of paths based on a contained keyword
    """

    schema_dict = InputSchemaDict.fromVersion('0.34')

    with pytest.raises(NoUniquePathFound):
         schema_dict.attrib_xpath('alpha')

    assert  schema_dict.attrib_xpath('alpha', exclude=['unique_path',
                                                           'other']) == '/fleurInput/calculationSetup/scfLoop/@alpha'
    with pytest.raises(NoUniquePathFound):
         schema_dict.attrib_xpath('alpha', exclude=['unique'])

    assert  schema_dict.attrib_xpath('alpha', not_contains='atom',
                            exclude=['unique'
                                     ]) == '/fleurInput/calculationSetup/greensFunction/contourSemicircle/@alpha'


def test_get_attrib_xpath_exclude_output():
    """
    Test the selection of paths based on a contained keyword
    """

    schema_dict = OutputSchemaDict.fromVersion('0.34')

    with pytest.raises(NoUniquePathFound):
        schema_dict.attrib_xpath('units')

    assert  schema_dict.attrib_xpath('units', contains='DMI') == './Forcetheorem_DMI/@units'
    assert schema_dict.attrib_xpath('units', exclude=['other'], contains='DMI') == './Forcetheorem_DMI/@units'

    with pytest.raises(NoPathFound):
        schema_dict.attrib_xpath('units', exclude=['unique_path'], contains='DMI')


def test_get_tag_info():
    """
    Basic test of the `get_tag_info()` function
    """

    schema_dict = InputSchemaDict.fromVersion('0.34')

    EXPECTED_RESULT = {
        'attribs': {'name', 'element', 'atomicNumber'},
        'optional': {
            'energyParameters', 'prodBasis', 'special', 'force', 'nocoParams', 'modInitDen', 'ldaU', 'ldaHIA',
            'greensfCalculation', 'torgueCalculation', 'lo'
        },
        'optional_attribs': {
            'element': None
        },
        'order': [
            'mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'prodBasis', 'special', 'force',
            'nocoParams', 'modInitDen', 'ldaU', 'ldaHIA', 'greensfCalculation', 'torgueCalculation', 'lo'
        ],
        'several': {'ldaU', 'ldaHIA', 'greensfCalculation', 'lo'},
        'simple': {
            'mtSphere', 'atomicCutoffs', 'energyParameters', 'prodBasis', 'special', 'force', 'nocoParams',
            'modInitDen', 'ldaU', 'lo'
        },
        'text':
        set(),
        'complex': {'electronConfig', 'ldaHIA', 'greensfCalculation', 'torgueCalculation'}
    }

    res, path = schema_dict.tag_info('species')

    assert res == EXPECTED_RESULT
    assert path == '/fleurInput/atomSpecies/species'

    res = schema_dict.tag_info('species', path_return=False)

    assert res == EXPECTED_RESULT

    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_info('ldaHIA')

    EXPECTED_RESULT = {
        'attribs': {'l', 'U', 'J', 'phi', 'theta', 'l_amf', 'init_occ', 'kkintgrCutoff', 'label'},
        'optional': {'exc', 'cFCoeff', 'addArg'},
        'optional_attribs': {
            'phi': '0.0',
            'theta': '0.0',
            'init_occ': 'calc',
            'kkintgrcutoff': 'calc',
            'label': 'default'
        },
        'order': ['exc', 'cFCoeff', 'addArg'],
        'several': {'exc', 'cFCoeff', 'addArg'},
        'simple': {'exc', 'cFCoeff', 'addArg'},
        'text': set(),
        'complex': set()
    }

    res, path = schema_dict.tag_info('ldaHIA', contains='species')

    assert res == EXPECTED_RESULT
    assert path == '/fleurInput/atomSpecies/species/ldaHIA'

    EXPECTED_RESULT = {
        'attribs': {
            'itmaxHubbard1', 'beta', 'minoccDistance', 'minmatDistance', 'n_occpm', 'dftspinpol', 'fullMatch',
            'l_nonsphDC', 'l_correctEtot', 'l_forceHIAiteration'
        },
        'optional': set(),
        'optional_attribs': {
            'beta': '100.0',
            'minoccdistance': '0.01',
            'minmatdistance': '0.001',
            'n_occpm': '2',
            'dftspinpol': 'F',
            'fullmatch': 'T',
            'l_nonsphdc': 'T',
            'l_correctetot': 'T',
            'l_forcehiaiteration': 'F',
        },
        'order': [],
        'several': set(),
        'simple': set(),
        'text': set(),
        'complex': set()
    }

    res, path = schema_dict.tag_info('ldaHIA', not_contains='atom')

    assert res == EXPECTED_RESULT
    assert path == '/fleurInput/calculationSetup/ldaHIA'

    with pytest.raises(NoPathFound):
        schema_dict.tag_info('ldaHIA', not_contains='atom', contains='species')



def clean_for_reg_dump(value_to_clean):
    """
    Clean for data regression converts CaseInsensitiveFrozenSet to set
    Lockable containers are to be converted berfore via `get_unlocked()`
    """
    from masci_tools.io.parsers.fleur.fleur_schema import AttributeType

    if isinstance(value_to_clean, dict):
        for key, val in value_to_clean.items():
            value_to_clean[key] = clean_for_reg_dump(val)
    elif isinstance(value_to_clean, list):
        for indx, val in enumerate(value_to_clean):
            value_to_clean[indx] = clean_for_reg_dump(val)
    elif isinstance(value_to_clean, CaseInsensitiveFrozenSet):
        value_to_clean = set(clean_for_reg_dump(val) for val in value_to_clean)
    elif isinstance(value_to_clean, AttributeType):
        value_to_clean = dict(value_to_clean._asdict())

    return value_to_clean
