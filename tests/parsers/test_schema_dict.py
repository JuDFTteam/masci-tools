"""
Test of the consistency the input schema dictionaries with the SchemaFiles in the same folder
"""
import pytest

from masci_tools.io.parsers.fleur_schema import InputSchemaDict, OutputSchemaDict, NoPathFound, NoUniquePathFound, list_available_versions, IncompatibleSchemaVersions
from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict, CaseInsensitiveFrozenSet
from masci_tools.util.lockable_containers import LockableDict, LockableList

MAIN_TEST_VERSION = '0.34'
OLD_TEST_VERSION = '0.27'

AVAILABLE_INPUT_VERSIONS = list_available_versions(output_schema=False)
AVAILABLE_OUTPUT_VERSIONS = list_available_versions(output_schema=True)


def test_inpschema_dict_structure():
    """
    Test the types of the keys in the inpschemadict
    """

    inputschema = InputSchemaDict.fromVersion(MAIN_TEST_VERSION)

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
                assert val._locked  #pylint: disable=protected-access
            if EXPECTED_TYPES[key] != CaseInsensitiveDict:
                assert not isinstance(val,
                                      CaseInsensitiveDict)  #since CaseInsensitiveDict is a subclass of LockableDict


def test_outschema_dict_structure():
    """
    Test the types of the keys in the inpschemadict
    """

    outputschema = OutputSchemaDict.fromVersion(MAIN_TEST_VERSION)

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
        'iteration_tags': CaseInsensitiveFrozenSet,
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
                assert val._locked  #pylint: disable=protected-access
            if EXPECTED_TYPES[key] != CaseInsensitiveDict:
                assert not isinstance(val,
                                      CaseInsensitiveDict)  #since CaseInsensitiveDict is a subclass of LockableDict


@pytest.mark.parametrize('schema_version', AVAILABLE_INPUT_VERSIONS)
def test_inpschema_dict(data_regression, schema_version):
    """
    Test the produced inputschema dicts
    """

    inputschema = InputSchemaDict.fromVersion(version=schema_version)

    data_regression.check(clean_for_reg_dump(inputschema.get_unlocked()))


@pytest.mark.parametrize('inp_version', AVAILABLE_INPUT_VERSIONS)
@pytest.mark.parametrize('out_version', AVAILABLE_OUTPUT_VERSIONS)
def test_outschema_dict(data_regression, inp_version, out_version):
    """
    Test the fleur_schema_parser_functions to make sure that they match the stored inputschema_dict
    """
    out_version_tuple = tuple(int(x) for x in out_version.split('.'))
    inp_version_tuple = tuple(int(x) for x in inp_version.split('.'))
    if out_version_tuple >= (0, 35) and inp_version_tuple <= (0, 32):
        with pytest.raises(IncompatibleSchemaVersions):
            outputschema = OutputSchemaDict.fromVersion(version=out_version, inp_version=inp_version)
    else:
        outputschema = OutputSchemaDict.fromVersion(version=out_version, inp_version=inp_version)

        data_regression.check(clean_for_reg_dump(outputschema.get_unlocked()))


def test_tag_xpath_input():
    """
    Test the path finding for tags for the input schema without additional options
    And verify with different version of the schema
    """

    schema_dict = InputSchemaDict.fromVersion(OLD_TEST_VERSION)

    #First example easy (magnetism tag is unique and should not differ between the versions)
    assert schema_dict.tag_xpath('magnetism') == '/fleurInput/calculationSetup/magnetism'
    #Differing paths between the version
    assert schema_dict.tag_xpath('bzIntegration') == '/fleurInput/calculationSetup/bzIntegration'

    #Non existent tag in old version
    with pytest.raises(NoPathFound):
        schema_dict.tag_xpath('DMI')
    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_xpath('ldaU')

    schema_dict = InputSchemaDict.fromVersion(MAIN_TEST_VERSION)

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

    schema_dict = InputSchemaDict.fromVersion(MAIN_TEST_VERSION)

    assert schema_dict.relative_tag_xpath('magnetism', 'calculationSetup') == './magnetism'
    assert schema_dict.relative_tag_xpath('magnetism', 'magnetism') == '.'

    assert schema_dict.relative_tag_xpath('DMI', 'forceTheorem') == './DMI'
    with pytest.raises(NoUniquePathFound):
        schema_dict.relative_tag_xpath('ldaU', 'fleurInput')

    assert schema_dict.relative_tag_xpath('ldaU', 'fleurInput', contains='species') == './atomSpecies/species/ldaU'
    assert schema_dict.relative_tag_xpath('ldaU', 'species') == './ldaU'

    schema_dict = InputSchemaDict.fromVersion(OLD_TEST_VERSION)
    with pytest.raises(NoPathFound):
        schema_dict.relative_tag_xpath('DMI', 'forceTheorem')

def test_relative_tag_xpath_tag_containing_root_tag():
    """
    Test the path finding for tags for other tagnames completely including the root tag name 
    """
    schema_dict = InputSchemaDict.fromVersion('0.35')
    assert schema_dict.relative_tag_xpath('row-1', 'bravaisMatrix') == './row-1'

def test_tag_xpath_output():
    """
    Test the path finding for tags for the output schema without additional options
    And verify with different version of the schema
    """

    schema_dict = OutputSchemaDict.fromVersion(MAIN_TEST_VERSION)

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

    schema_dict = OutputSchemaDict.fromVersion(MAIN_TEST_VERSION)

    assert schema_dict.relative_tag_xpath('iteration', 'scfLoop') == './iteration'
    assert schema_dict.relative_tag_xpath('iteration', 'iteration') == '.'
    assert schema_dict.relative_tag_xpath('densityMatrixFor', 'ldaUDensityMatrix') == './densityMatrixFor'


def test_iteration_tag_xpath():
    """
    Test the iteration_tag_xpath method for constructing absolute xpaths into
    iteration elements
    """
    schema_dict = OutputSchemaDict.fromVersion(MAIN_TEST_VERSION)

    assert schema_dict.iteration_tag_xpath('fermienergy') == '/fleurOutput/scfLoop/iteration/FermiEnergy'

    with pytest.raises(NoPathFound):
        schema_dict.iteration_tag_xpath('iteration')
    with pytest.raises(NoUniquePathFound):
        schema_dict.iteration_tag_xpath('mtcharge')

    assert schema_dict.iteration_tag_xpath(
        'mtcharge', contains='valence') == '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtCharge'
    assert schema_dict.iteration_tag_xpath(
        'mtcharge', not_contains='valence') == '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtCharge'


def test_relative_iteration_tag_xpath():
    """
    Test the relative_iteration_tag_xpath method for constructing relative xpaths from absolute xpaths into
    iteration elements
    """
    schema_dict = OutputSchemaDict.fromVersion(MAIN_TEST_VERSION)

    assert schema_dict.relative_iteration_tag_xpath('fermienergy', 'scfLoop') == './iteration/FermiEnergy'
    assert schema_dict.relative_iteration_tag_xpath('fermienergy', 'FermiEnergy') == '.'

    with pytest.raises(NoPathFound):
        schema_dict.relative_iteration_tag_xpath('iteration', 'scfLoop')
    with pytest.raises(NoUniquePathFound):
        schema_dict.relative_iteration_tag_xpath('mtcharge', 'scfLoop')

    assert schema_dict.relative_iteration_tag_xpath(
        'mtcharge', 'scfLoop', contains='valence') == './iteration/valenceDensity/mtCharges/mtCharge'
    assert schema_dict.relative_iteration_tag_xpath(
        'mtcharge', 'scfLoop', not_contains='valence') == './iteration/allElectronCharges/mtCharges/mtCharge'

def test_relative_iteration_tag_xpath_tag_containing_root_tag():
    """
    Test the path finding for tags for other tagnames completely including the root tag name 
    """
    schema_dict = OutputSchemaDict.fromVersion(MAIN_TEST_VERSION)
    assert schema_dict.relative_iteration_tag_xpath(
        'mtcharge', 'mtCharge', not_contains='valence') == '.'


def test_iteration_attrib_xpath():
    """
    Test the iteration_attrib_xpath method for constructing absolute xpaths into
    iteration elements to attributes
    """
    schema_dict = OutputSchemaDict.fromVersion(MAIN_TEST_VERSION)

    assert schema_dict.iteration_attrib_xpath(
        'numberforcurrentrun') == '/fleurOutput/scfLoop/iteration/@numberForCurrentRun'

    with pytest.raises(NoPathFound):
        schema_dict.iteration_attrib_xpath('non_existent')
    with pytest.raises(NoUniquePathFound):
        schema_dict.iteration_attrib_xpath('value')

    assert schema_dict.iteration_attrib_xpath('value',
                                              contains='Fermi') == '/fleurOutput/scfLoop/iteration/FermiEnergy/@value'
    assert schema_dict.iteration_attrib_xpath(
        'value', tag_name='fermienergy') == '/fleurOutput/scfLoop/iteration/FermiEnergy/@value'
    assert schema_dict.iteration_attrib_xpath('total', not_contains={
        'spin', 'valence'
    }) == '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtCharge/@total'


def test_relative_iteration_attrib_xpath():
    """
    Test the relative_iteration_attrib_xpath method for constructing relative paths from absolute xpaths into
    iteration elements to attributes
    """
    schema_dict = OutputSchemaDict.fromVersion(MAIN_TEST_VERSION)

    assert schema_dict.relative_iteration_attrib_xpath('numberforcurrentrun',
                                                       'scfLoop') == './iteration/@numberForCurrentRun'
    assert schema_dict.relative_iteration_attrib_xpath('value', 'FermiEnergy', tag_name='fermienergy') == './@value'

    with pytest.raises(NoPathFound):
        schema_dict.relative_iteration_attrib_xpath('non_existent', 'root')
    with pytest.raises(NoUniquePathFound):
        schema_dict.relative_iteration_attrib_xpath('value', 'iteration')

    assert schema_dict.relative_iteration_attrib_xpath('value', 'iteration', contains='Fermi') == './FermiEnergy/@value'
    assert schema_dict.relative_iteration_attrib_xpath('total', 'valenceDensity',
                                                       not_contains={'mt', 'fixed'}) == './spinDependentCharge/@total'


def test_tag_xpath_contains():
    """
    Test the selection of paths based on a contained keyword
    """

    schema_dict = InputSchemaDict.fromVersion(MAIN_TEST_VERSION)

    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_xpath('ldaU')
    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_xpath('ldaU', contains='atom')

    assert schema_dict.tag_xpath('ldaU', contains='calculationSetup') == '/fleurInput/calculationSetup/ldaU'
    assert schema_dict.tag_xpath('ldaU', contains='species') == '/fleurInput/atomSpecies/species/ldaU'
    assert schema_dict.tag_xpath('ldaU', contains='Group') == '/fleurInput/atomGroups/atomGroup/ldaU'

    with pytest.raises(NoPathFound):
        schema_dict.tag_xpath('ldaU', contains='group')


def test_tag_xpath_notcontains():
    """
    Test the selection of paths based on a not contained keyword
    """

    schema_dict = InputSchemaDict.fromVersion(MAIN_TEST_VERSION)

    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_xpath('ldaU')
    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_xpath('ldaU', not_contains='calculationSetup')

    assert schema_dict.tag_xpath('ldaU', not_contains='atom') == '/fleurInput/calculationSetup/ldaU'
    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_xpath('ldaU', not_contains='Group')

    assert schema_dict.tag_xpath('ldaU', contains='atom',
                                 not_contains='species') == '/fleurInput/atomGroups/atomGroup/ldaU'


def test_tagattrib_xpath_case_insensitivity():
    """
    Test that the selection works with case insensitivity
    """

    schema_dict = InputSchemaDict.fromVersion(MAIN_TEST_VERSION)

    assert schema_dict.tag_xpath('bzIntegration') == '/fleurInput/cell/bzIntegration'
    assert schema_dict.tag_xpath('BZINTEGRATION') == '/fleurInput/cell/bzIntegration'
    assert schema_dict.tag_xpath('bzintegration') == '/fleurInput/cell/bzIntegration'
    assert schema_dict.tag_xpath('bZInTegrAtIon') == '/fleurInput/cell/bzIntegration'

    assert schema_dict.attrib_xpath('jspins') == '/fleurInput/calculationSetup/magnetism/@jspins'
    assert schema_dict.attrib_xpath('JSPINS') == '/fleurInput/calculationSetup/magnetism/@jspins'
    assert schema_dict.attrib_xpath('jSpInS') == '/fleurInput/calculationSetup/magnetism/@jspins'


def test_attrib_xpath_input():
    """
    Test the path finding for tags for the input schema without additional options
    And verify with different version of the schema
    """

    schema_dict = InputSchemaDict.fromVersion(MAIN_TEST_VERSION)

    assert schema_dict.attrib_xpath('jspins') == '/fleurInput/calculationSetup/magnetism/@jspins'
    assert schema_dict.attrib_xpath('mode') == '/fleurInput/cell/bzIntegration/@mode'
    assert schema_dict.attrib_xpath('l_mtNocoPot',
                                    exclude=['other'
                                             ]) == '/fleurInput/calculationSetup/magnetism/mtNocoParams/@l_mtNocoPot'
    with pytest.raises(NoUniquePathFound):
        schema_dict.attrib_xpath('l_amf')

    schema_dict = InputSchemaDict.fromVersion(OLD_TEST_VERSION)

    assert schema_dict.attrib_xpath('jspins') == '/fleurInput/calculationSetup/magnetism/@jspins'
    assert schema_dict.attrib_xpath('mode') == '/fleurInput/calculationSetup/bzIntegration/@mode'
    with pytest.raises(NoPathFound):
        schema_dict.attrib_xpath('l_mtNocoPot')

    #Multiple possible paths
    with pytest.raises(NoUniquePathFound):
        schema_dict.attrib_xpath('l_amf')


def test_relative_attrib_xpath_input():
    """
    Test the path finding for tags for the input schema without additional options
    And verify with different version of the schema
    """

    schema_dict = InputSchemaDict.fromVersion(MAIN_TEST_VERSION)

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


def test_attrib_xpath_output():
    """
    Test the path finding for tags for the input schema without additional options
    And verify with different version of the schema
    """

    schema_dict = OutputSchemaDict.fromVersion(MAIN_TEST_VERSION)
    assert schema_dict.attrib_xpath('nat') == '/fleurOutput/numericalParameters/atomsInCell/@nat'
    assert schema_dict.attrib_xpath('qvectors') == './Forcetheorem_SSDISP/@qvectors'

    schema_dict = OutputSchemaDict.fromVersion('0.31')
    assert schema_dict.attrib_xpath('nat') == '/fleurOutput/numericalParameters/atomsInCell/@nat'
    assert schema_dict.attrib_xpath('qvectors') == './Forcetheorem_SSDISP/@qvectors'


def test_relative_attrib_xpath_output():
    """
    Test the path finding for tags for the input schema without additional options
    And verify with different version of the schema
    """
    schema_dict = OutputSchemaDict.fromVersion(MAIN_TEST_VERSION)

    assert schema_dict.relative_attrib_xpath('nat', 'numericalParameters') == './atomsInCell/@nat'
    assert schema_dict.relative_attrib_xpath('nat', 'atomsInCell') == './@nat'

    assert schema_dict.relative_attrib_xpath('qvectors', '.') == './Forcetheorem_SSDISP/@qvectors'
    assert schema_dict.relative_attrib_xpath('qvectors', 'Forcetheorem_SSDISP') == './@qvectors'


def test_attrib_xpath_contains():
    """
    Test the selection of paths based on a contained keyword
    """

    schema_dict = InputSchemaDict.fromVersion(MAIN_TEST_VERSION)

    with pytest.raises(NoUniquePathFound):
        schema_dict.attrib_xpath('l_mperp')

    assert schema_dict.attrib_xpath(
        'l_mperp', contains='magnetism') == '/fleurInput/calculationSetup/magnetism/mtNocoParams/@l_mperp'
    assert schema_dict.attrib_xpath('l_mperp',
                                    contains='greensFunction') == '/fleurInput/calculationSetup/greensFunction/@l_mperp'

    with pytest.raises(NoPathFound):
        schema_dict.attrib_xpath('l_mperp', contains='atom')


def test_attrib_xpath_notcontains():
    """
    Test the selection of paths based on a contained keyword
    """

    schema_dict = InputSchemaDict.fromVersion(MAIN_TEST_VERSION)

    with pytest.raises(NoUniquePathFound):
        schema_dict.attrib_xpath('l_mperp')

    assert schema_dict.attrib_xpath(
        'l_mperp', not_contains='greensFunction') == '/fleurInput/calculationSetup/magnetism/mtNocoParams/@l_mperp'
    assert schema_dict.attrib_xpath('l_mperp',
                                    not_contains='magnetism') == '/fleurInput/calculationSetup/greensFunction/@l_mperp'

    assert schema_dict.attrib_xpath('l_mperp', contains='greensFunction',
                                    not_contains='magnetism') == '/fleurInput/calculationSetup/greensFunction/@l_mperp'

    with pytest.raises(NoPathFound):
        schema_dict.attrib_xpath('l_mperp', not_contains='calculationSetup')


def test_attrib_xpath_exclude():
    """
    Test the selection of paths based on a contained keyword
    """

    schema_dict = InputSchemaDict.fromVersion(MAIN_TEST_VERSION)

    with pytest.raises(NoUniquePathFound):
        schema_dict.attrib_xpath('alpha')

    assert schema_dict.attrib_xpath('alpha', exclude=['unique_path',
                                                      'other']) == '/fleurInput/calculationSetup/scfLoop/@alpha'
    with pytest.raises(NoUniquePathFound):
        schema_dict.attrib_xpath('alpha', exclude=['unique'])

    assert schema_dict.attrib_xpath(
        'alpha', not_contains='atom',
        exclude=['unique']) == '/fleurInput/calculationSetup/greensFunction/contourSemicircle/@alpha'


def test_attrib_xpath_exclude_output():
    """
    Test the selection of paths based on a contained keyword
    """

    schema_dict = OutputSchemaDict.fromVersion(MAIN_TEST_VERSION)

    with pytest.raises(NoUniquePathFound):
        schema_dict.attrib_xpath('units')

    assert schema_dict.attrib_xpath('units', contains='DMI') == './Forcetheorem_DMI/@units'
    assert schema_dict.attrib_xpath('units', exclude=['other'], contains='DMI') == './Forcetheorem_DMI/@units'

    with pytest.raises(NoPathFound):
        schema_dict.attrib_xpath('units', exclude=['unique_path'], contains='DMI')


def test_tag_info():
    """
    Basic test of the `get_tag_info()` function
    """

    schema_dict = InputSchemaDict.fromVersion(MAIN_TEST_VERSION)

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

    res = schema_dict.tag_info('species')

    assert res == EXPECTED_RESULT

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

    with pytest.raises(NoUniquePathFound):
        schema_dict.tag_info('ldaHIA')

    res = schema_dict.tag_info('ldaHIA', contains='species')

    assert res == EXPECTED_RESULT

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

    res = schema_dict.tag_info('ldaHIA', not_contains='atom')

    assert res == EXPECTED_RESULT

    with pytest.raises(NoPathFound):
        schema_dict.tag_info('ldaHIA', not_contains='atom', contains='species')


def clean_for_reg_dump(value_to_clean):
    """
    Clean for data regression converts CaseInsensitiveFrozenSet to set
    Lockable containers are to be converted berfore via `get_unlocked()`
    """
    from masci_tools.io.parsers.fleur_schema import AttributeType

    if isinstance(value_to_clean, dict):
        for key, val in value_to_clean.items():
            value_to_clean[key] = clean_for_reg_dump(val)
    elif isinstance(value_to_clean, list):
        for indx, val in enumerate(value_to_clean):
            value_to_clean[indx] = clean_for_reg_dump(val)
    elif isinstance(value_to_clean, CaseInsensitiveFrozenSet):
        value_to_clean = {clean_for_reg_dump(val) for val in value_to_clean}
    elif isinstance(value_to_clean, AttributeType):
        value_to_clean = dict(value_to_clean._asdict())

    return value_to_clean
