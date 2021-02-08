# -*- coding: utf-8 -*-
"""
This file contains information parsed from the FleurOutputSchema.xsd
for version 0.30

The keys contain the following information:

    - 'out_version': Version string of the output schema represented in this file
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
from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict, CaseInsensitiveFrozenSet
__out_version__ = '0.30'
schema_dict = {
    '_basic_types': {
        'AdditionalCompilerFlagsType': {
            'base_types': ['string'],
            'length': 'unbounded'
        },
        'AtomPosType': {
            'base_types': ['string'],
            'length': 3
        },
        'BZIntegrationModeEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'CoreConfigEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'CoreSpecEdgeEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'CoreStateListType': {
            'base_types': ['string'],
            'length': 'unbounded'
        },
        'DensityMatrixForType': {
            'base_types': ['string'],
            'length': 'unbounded'
        },
        'DisplaceType': {
            'base_types': ['float'],
            'length': 3
        },
        'Double3DVecType': {
            'base_types': ['float'],
            'length': 3
        },
        'Double4DVecType': {
            'base_types': ['float'],
            'length': 4
        },
        'DoubleVecType': {
            'base_types': ['float'],
            'length': 'unbounded'
        },
        'EParamSelectionEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'EigenvaluesAtType': {
            'base_types': ['float'],
            'length': 'unbounded'
        },
        'ElectronStateEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'FleurVersionType': {
            'base_types': ['string'],
            'length': 1
        },
        'ForceMixEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'IntegerVecType': {
            'base_types': ['int'],
            'length': 'unbounded'
        },
        'KPointSetPurposeEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'KPointType': {
            'base_types': ['float'],
            'length': 3
        },
        'LatnamEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'LatticeParameterType': {
            'base_types': ['string'],
            'length': 1
        },
        'MixingEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'NobleGasConfigEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'NumBandsType': {
            'base_types': ['int', 'string'],
            'length': 1
        },
        'PositionType': {
            'base_types': ['float'],
            'length': 3
        },
        'RDMFTFunctionalEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'SpecialPointType': {
            'base_types': ['string'],
            'length': 3
        },
        'SpgrpEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'SpinNumberType': {
            'base_types': ['int'],
            'length': 1
        },
        'String2DVecType': {
            'base_types': ['string'],
            'length': 2
        },
        'String3DVecType': {
            'base_types': ['string'],
            'length': 3
        },
        'StringVecType': {
            'base_types': ['string'],
            'length': 'unbounded'
        },
        'TargetStructureClassType': {
            'base_types': ['string'],
            'length': 'unbounded'
        },
        'TripleFleurBool': {
            'base_types': ['string'],
            'length': 1
        },
        'ValenceStateListType': {
            'base_types': ['string'],
            'length': 'unbounded'
        },
        'XCFunctionalEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'ZeroToOneNumberType': {
            'base_types': ['float'],
            'length': 1
        }
    },
    '_input_basic_types': {
        'AtomPosType': {
            'base_types': ['string'],
            'length': 3
        },
        'BZIntegrationModeEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'CoreConfigEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'CoreSpecEdgeEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'CoreStateListType': {
            'base_types': ['string'],
            'length': 'unbounded'
        },
        'DisplaceType': {
            'base_types': ['float'],
            'length': 3
        },
        'Double3DVecType': {
            'base_types': ['float'],
            'length': 3
        },
        'Double4DVecType': {
            'base_types': ['float'],
            'length': 4
        },
        'DoubleVecType': {
            'base_types': ['float'],
            'length': 'unbounded'
        },
        'EParamSelectionEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'ElectronStateEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'FleurVersionType': {
            'base_types': ['string'],
            'length': 1
        },
        'ForceMixEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'IntegerVecType': {
            'base_types': ['int'],
            'length': 'unbounded'
        },
        'KPointSetPurposeEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'KPointType': {
            'base_types': ['float'],
            'length': 3
        },
        'LatnamEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'LatticeParameterType': {
            'base_types': ['string'],
            'length': 1
        },
        'MixingEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'NobleGasConfigEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'NumBandsType': {
            'base_types': ['int', 'string'],
            'length': 1
        },
        'PositionType': {
            'base_types': ['float'],
            'length': 3
        },
        'RDMFTFunctionalEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'SpecialPointType': {
            'base_types': ['string'],
            'length': 3
        },
        'SpgrpEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'SpinNumberType': {
            'base_types': ['int'],
            'length': 1
        },
        'String2DVecType': {
            'base_types': ['string'],
            'length': 2
        },
        'String3DVecType': {
            'base_types': ['string'],
            'length': 3
        },
        'StringVecType': {
            'base_types': ['string'],
            'length': 'unbounded'
        },
        'TripleFleurBool': {
            'base_types': ['string'],
            'length': 1
        },
        'ValenceStateListType': {
            'base_types': ['string'],
            'length': 'unbounded'
        },
        'XCFunctionalEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'ZeroToOneNumberType': {
            'base_types': ['float'],
            'length': 1
        }
    },
    'attrib_types':
    CaseInsensitiveDict({
        'fleuroutputversion': ['string'],
        'version': ['string'],
        'date': ['string'],
        'user': ['string'],
        'host': ['string'],
        'flag': ['string'],
        'link': ['string'],
        'lastcommithash': ['string'],
        'branch': ['string'],
        'type': ['string'],
        'ompthreads': ['string'],
        'mpiprocesses': ['string'],
        'memorypernode': ['string'],
        'time': ['string'],
        'zone': ['string'],
        'message': ['string'],
        'nat': ['int'],
        'ntype': ['int'],
        'jmtd': ['int'],
        'n_u': ['int'],
        'n_hia': ['int'],
        'nvd': ['int'],
        'lmaxd': ['int'],
        'nlotot': ['int'],
        'ng3': ['int'],
        'ng2': ['int'],
        'numbands': ['int'],
        'unitcell': ['float'],
        'interstitial': ['float'],
        'omegatilda': ['float'],
        'surfacearea': ['float'],
        'z1': ['float'],
        'atomtype': ['int'],
        'mtradius': ['float'],
        'mtvolume': ['float'],
        'weightscale': ['float'],
        'count': ['int'],
        'numberforcurrentrun': ['int'],
        'overallnumber': ['int'],
        'no': ['int'],
        'angles': ['int'],
        'qpoints': ['int'],
        'configs': ['int'],
        'qvectors': ['int'],
        'q': ['int', 'float'],
        'ev-sum': ['float'],
        'phi': ['float'],
        'theta': ['float'],
        'n': ['int'],
        'iatom': ['int'],
        'jatom': ['int'],
        'phase': ['switch'],
        'units': ['string'],
        'spin': ['int'],
        'branchlowest': ['float'],
        'branchhighest': ['float'],
        'value': ['float'],
        'logderivmt': ['float'],
        'vacuum': ['int'],
        'vzir': ['float'],
        'vzinf': ['float'],
        'ikpt': ['int'],
        'k_x': ['float'],
        'k_y': ['float'],
        'k_z': ['float'],
        'total': ['float'],
        's': ['float'],
        'p': ['float'],
        'd': ['float'],
        'f': ['float'],
        'mtspheres': ['float'],
        'vacuum1': ['float'],
        'vacuum2': ['float'],
        'atomicnumber': ['int'],
        'kinenergy': ['float'],
        'eigvalsum': ['float'],
        'lostelectrons': ['float'],
        'moment': ['float'],
        'spinupcharge': ['float'],
        'spindowncharge': ['float'],
        'l': ['int'],
        'j': ['float'],
        'energy': ['float'],
        'weight': ['float'],
        'x': ['float'],
        'y': ['float'],
        'z': ['float'],
        'f_x': ['float'],
        'f_y': ['float'],
        'f_z': ['float'],
        'uindex': ['int'],
        'u': ['float'],
        'kpoint': ['int'],
        'index': ['int'],
        'occupation': ['float'],
        'comment': ['string'],
        'distance': ['float'],
        'name': ['string']
    }),
    'input_tag':
    'inputData',
    'iteration_other_attribs':
    CaseInsensitiveDict({
        'f_x': ['./totalForcesOnRepresentativeAtoms/forceTotal/@F_x'],
        'f_y': ['./totalForcesOnRepresentativeAtoms/forceTotal/@F_y'],
        'f_z': ['./totalForcesOnRepresentativeAtoms/forceTotal/@F_z'],
        'j': ['./coreStates/state/@j', './ldaUDensityMatrix/densityMatrixFor/@J'],
        'no': ['./Forcetheorem_Loop/@No'],
        'u': ['./ldaUDensityMatrix/densityMatrixFor/@U'],
        'atomtype': [
            './allElectronCharges/mtCharges/mtCharge/@atomType', './coreStates/@atomType',
            './energyParameters/atomicEP/@atomType', './energyParameters/heAtomicEP/@atomType',
            './energyParameters/heloAtomicEP/@atomType', './energyParameters/loAtomicEP/@atomType',
            './ldaUDensityMatrix/densityMatrixFor/@atomType', './magneticMomentsInMTSpheres/magneticMoment/@atomType',
            './orbitalMagneticMomentsInMTSpheres/orbMagMoment/@atomType',
            './totalEnergy/atomTypeDependentContributions/@atomType',
            './totalForcesOnRepresentativeAtoms/forceTotal/@atomType', './valenceDensity/mtCharges/mtCharge/@atomType'
        ],
        'atomicnumber': ['./coreStates/@atomicNumber'],
        'branch': [
            './energyParameters/atomicEP/@branch', './energyParameters/heAtomicEP/@branch',
            './energyParameters/heloAtomicEP/@branch', './energyParameters/loAtomicEP/@branch'
        ],
        'branchhighest': [
            './energyParameters/atomicEP/@branchHighest', './energyParameters/heAtomicEP/@branchHighest',
            './energyParameters/heloAtomicEP/@branchHighest', './energyParameters/loAtomicEP/@branchHighest'
        ],
        'branchlowest': [
            './energyParameters/atomicEP/@branchLowest', './energyParameters/heAtomicEP/@branchLowest',
            './energyParameters/heloAtomicEP/@branchLowest', './energyParameters/loAtomicEP/@branchLowest'
        ],
        'comment': ['./totalEnergy/@comment'],
        'd': ['./allElectronCharges/mtCharges/mtCharge/@d', './valenceDensity/mtCharges/mtCharge/@d'],
        'distance': [
            './densityConvergence/chargeDensity/@distance', './densityConvergence/overallChargeDensity/@distance',
            './densityConvergence/spinDensity/@distance'
        ],
        'eigvalsum': ['./coreStates/@eigValSum'],
        'energy': ['./coreStates/state/@energy', './rdmft/@energy', './rdmft/occupations/state/@energy'],
        'ev-sum': [
            './Forcetheorem_DMI/Entry/@ev-sum', './Forcetheorem_JIJ/Config/@ev-sum', './Forcetheorem_MAE/Angle/@ev-sum',
            './Forcetheorem_SSDISP/Entry/@ev-sum'
        ],
        'f': ['./allElectronCharges/mtCharges/mtCharge/@f', './valenceDensity/mtCharges/mtCharge/@f'],
        'iatom': ['./Forcetheorem_JIJ/Config/@iatom'],
        'ikpt': ['./eigenvalues/eigenvaluesAt/@ikpt'],
        'index': ['./rdmft/occupations/state/@index'],
        'interstitial': [
            './allElectronCharges/fixedCharges/spinDependentCharge/@interstitial',
            './allElectronCharges/spinDependentCharge/@interstitial',
            './valenceDensity/fixedCharges/spinDependentCharge/@interstitial',
            './valenceDensity/spinDependentCharge/@interstitial'
        ],
        'jatom': ['./Forcetheorem_JIJ/Config/@jatom'],
        'k_x': ['./eigenvalues/eigenvaluesAt/@k_x'],
        'k_y': ['./eigenvalues/eigenvaluesAt/@k_y'],
        'k_z': ['./eigenvalues/eigenvaluesAt/@k_z'],
        'kinenergy': ['./coreStates/@kinEnergy'],
        'kpoint': ['./rdmft/occupations/@kpoint'],
        'l': ['./coreStates/state/@l', './ldaUDensityMatrix/densityMatrixFor/@l'],
        'lostelectrons': ['./coreStates/@lostElectrons'],
        'moment': [
            './magneticMomentsInMTSpheres/magneticMoment/@moment',
            './orbitalMagneticMomentsInMTSpheres/orbMagMoment/@moment'
        ],
        'mtspheres': [
            './allElectronCharges/fixedCharges/spinDependentCharge/@mtSpheres',
            './allElectronCharges/spinDependentCharge/@mtSpheres',
            './valenceDensity/fixedCharges/spinDependentCharge/@mtSpheres',
            './valenceDensity/spinDependentCharge/@mtSpheres'
        ],
        'n': ['./Forcetheorem_JIJ/Config/@n', './coreStates/state/@n'],
        'name': ['./timing/timer/@name'],
        'occupation': ['./rdmft/occupations/state/@occupation'],
        'p': ['./allElectronCharges/mtCharges/mtCharge/@p', './valenceDensity/mtCharges/mtCharge/@p'],
        'phase': ['./Forcetheorem_JIJ/Config/@phase'],
        'phi': ['./Forcetheorem_DMI/Entry/@phi', './Forcetheorem_MAE/Angle/@phi'],
        'q': ['./Forcetheorem_DMI/Entry/@q', './Forcetheorem_JIJ/Config/@q', './Forcetheorem_SSDISP/Entry/@q'],
        's': ['./allElectronCharges/mtCharges/mtCharge/@s', './valenceDensity/mtCharges/mtCharge/@s'],
        'spin': [
            './allElectronCharges/fixedCharges/spinDependentCharge/@spin', './allElectronCharges/mtCharges/@spin',
            './allElectronCharges/spinDependentCharge/@spin', './coreStates/@spin',
            './densityConvergence/chargeDensity/@spin', './densityConvergence/overallChargeDensity/@spin',
            './densityConvergence/spinDensity/@spin', './eigenvalues/eigenvaluesAt/@spin',
            './energyParameters/atomicEP/@spin', './energyParameters/heAtomicEP/@spin',
            './energyParameters/heloAtomicEP/@spin', './energyParameters/loAtomicEP/@spin',
            './energyParameters/vacuumEP/@spin', './ldaUDensityMatrix/densityMatrixFor/@spin',
            './rdmft/occupations/@spin', './valenceDensity/fixedCharges/spinDependentCharge/@spin',
            './valenceDensity/mtCharges/@spin', './valenceDensity/spinDependentCharge/@spin'
        ],
        'spindowncharge': [
            './magneticMomentsInMTSpheres/magneticMoment/@spinDownCharge',
            './orbitalMagneticMomentsInMTSpheres/orbMagMoment/@spinDownCharge'
        ],
        'spinupcharge': [
            './magneticMomentsInMTSpheres/magneticMoment/@spinUpCharge',
            './orbitalMagneticMomentsInMTSpheres/orbMagMoment/@spinUpCharge'
        ],
        'theta': ['./Forcetheorem_DMI/Entry/@theta', './Forcetheorem_MAE/Angle/@theta'],
        'total': [
            './allElectronCharges/fixedCharges/spinDependentCharge/@total',
            './allElectronCharges/mtCharges/mtCharge/@total', './allElectronCharges/spinDependentCharge/@total',
            './valenceDensity/fixedCharges/spinDependentCharge/@total', './valenceDensity/mtCharges/mtCharge/@total',
            './valenceDensity/spinDependentCharge/@total'
        ],
        'uindex': ['./ldaUDensityMatrix/densityMatrixFor/@uIndex'],
        'units': [
            './FermiEnergy/@units', './allElectronCharges/fixedCharges/totalCharge/@units',
            './allElectronCharges/totalCharge/@units', './bandgap/@units', './densityConvergence/@units',
            './densityConvergence/chargeDensity/@units', './densityConvergence/overallChargeDensity/@units',
            './densityConvergence/spinDensity/@units', './energyParameters/@units',
            './magneticMomentsInMTSpheres/@units', './orbitalMagneticMomentsInMTSpheres/@units',
            './sumValenceSingleParticleEnergies/@units', './timing/@units', './timing/timer/@units',
            './totalEnergy/@units', './totalEnergy/FockExchangeEnergyCore/@units',
            './totalEnergy/FockExchangeEnergyValence/@units',
            './totalEnergy/atomTypeDependentContributions/MadelungTerm/@units',
            './totalEnergy/atomTypeDependentContributions/electronNucleiInteractionDifferentMTs/@units',
            './totalEnergy/chargeDenXCDenIntegral/@units', './totalEnergy/densityCoulombPotentialIntegral/@units',
            './totalEnergy/densityEffectivePotentialIntegral/@units', './totalEnergy/dftUCorrection/@units',
            './totalEnergy/extrapolationTo0K/@units', './totalEnergy/freeEnergy/@units',
            './totalEnergy/sumOfEigenvalues/@units', './totalEnergy/sumOfEigenvalues/coreElectrons/@units',
            './totalEnergy/sumOfEigenvalues/valenceElectrons/@units', './totalEnergy/tkbTimesEntropy/@units',
            './totalForcesOnRepresentativeAtoms/@units', './totalForcesOnRepresentativeAtoms/forceTotal/@units',
            './valenceDensity/fixedCharges/totalCharge/@units', './valenceDensity/totalCharge/@units'
        ],
        'vacuum': ['./energyParameters/vacuumEP/@vacuum'],
        'vacuum1': [
            './allElectronCharges/fixedCharges/spinDependentCharge/@vacuum1',
            './allElectronCharges/spinDependentCharge/@vacuum1',
            './valenceDensity/fixedCharges/spinDependentCharge/@vacuum1',
            './valenceDensity/spinDependentCharge/@vacuum1'
        ],
        'vacuum2': [
            './allElectronCharges/fixedCharges/spinDependentCharge/@vacuum2',
            './allElectronCharges/spinDependentCharge/@vacuum2',
            './valenceDensity/fixedCharges/spinDependentCharge/@vacuum2',
            './valenceDensity/spinDependentCharge/@vacuum2'
        ],
        'value': [
            './FermiEnergy/@value', './allElectronCharges/fixedCharges/totalCharge/@value',
            './allElectronCharges/totalCharge/@value', './bandgap/@value', './energyParameters/atomicEP/@value',
            './energyParameters/heAtomicEP/@value', './energyParameters/heloAtomicEP/@value',
            './energyParameters/loAtomicEP/@value', './energyParameters/vacuumEP/@value',
            './sumValenceSingleParticleEnergies/@value', './timing/timer/@value', './totalEnergy/@value',
            './totalEnergy/FockExchangeEnergyCore/@value', './totalEnergy/FockExchangeEnergyValence/@value',
            './totalEnergy/atomTypeDependentContributions/MadelungTerm/@value',
            './totalEnergy/atomTypeDependentContributions/electronNucleiInteractionDifferentMTs/@value',
            './totalEnergy/chargeDenXCDenIntegral/@value', './totalEnergy/densityCoulombPotentialIntegral/@value',
            './totalEnergy/densityEffectivePotentialIntegral/@value', './totalEnergy/dftUCorrection/@value',
            './totalEnergy/extrapolationTo0K/@value', './totalEnergy/freeEnergy/@value',
            './totalEnergy/sumOfEigenvalues/@value', './totalEnergy/sumOfEigenvalues/coreElectrons/@value',
            './totalEnergy/sumOfEigenvalues/valenceElectrons/@value', './totalEnergy/tkbTimesEntropy/@value',
            './valenceDensity/fixedCharges/totalCharge/@value', './valenceDensity/totalCharge/@value'
        ],
        'vzir': ['./energyParameters/vacuumEP/@vzIR'],
        'vzinf': ['./energyParameters/vacuumEP/@vzInf'],
        'weight': ['./coreStates/state/@weight'],
        'x': ['./totalForcesOnRepresentativeAtoms/forceTotal/@x'],
        'y': ['./totalForcesOnRepresentativeAtoms/forceTotal/@y'],
        'z': ['./totalForcesOnRepresentativeAtoms/forceTotal/@z'],
        'densitymatrixfor': ['./ldaUDensityMatrix/densityMatrixFor'],
        'eigenvaluesat': ['./eigenvalues/eigenvaluesAt']
    }),
    'iteration_tag_info': {
        './FermiEnergy': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './Forcetheorem_DMI': {
            'attribs': CaseInsensitiveFrozenSet(['Angles', 'qpoints']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['Entry']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['Entry'],
            'several': CaseInsensitiveFrozenSet(['Entry']),
            'simple': CaseInsensitiveFrozenSet(['Entry']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './Forcetheorem_DMI/Entry': {
            'attribs': CaseInsensitiveFrozenSet(['ev-sum', 'phi', 'q', 'theta']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'phi': None,
                'theta': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './Forcetheorem_JIJ': {
            'attribs': CaseInsensitiveFrozenSet(['Configs']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['Config']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['Config'],
            'several': CaseInsensitiveFrozenSet(['Config']),
            'simple': CaseInsensitiveFrozenSet(['Config']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './Forcetheorem_JIJ/Config': {
            'attribs': CaseInsensitiveFrozenSet(['ev-sum', 'iatom', 'jatom', 'n', 'phase', 'q']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './Forcetheorem_Loop': {
            'attribs':
            CaseInsensitiveFrozenSet(['No']),
            'complex':
            CaseInsensitiveFrozenSet([
                'FermiEnergy', 'allElectronCharges', 'bandgap', 'coreStates', 'densityConvergence', 'eigenvalues',
                'energyParameters', 'ldaUDensityMatrix', 'magneticMomentsInMTSpheres',
                'orbitalMagneticMomentsInMTSpheres', 'rdmft', 'sumValenceSingleParticleEnergies', 'timing',
                'totalEnergy', 'totalForcesOnRepresentativeAtoms', 'valenceDensity'
            ]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({}),
            'order': [
                'energyParameters', 'eigenvalues', 'bandgap', 'sumValenceSingleParticleEnergies', 'FermiEnergy',
                'valenceDensity', 'coreStates', 'allElectronCharges', 'magneticMomentsInMTSpheres',
                'orbitalMagneticMomentsInMTSpheres', 'rdmft', 'totalEnergy', 'totalForcesOnRepresentativeAtoms',
                'ldaUDensityMatrix', 'densityConvergence', 'timing'
            ],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        './Forcetheorem_MAE': {
            'attribs': CaseInsensitiveFrozenSet(['Angles']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['Angle']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['Angle'],
            'several': CaseInsensitiveFrozenSet(['Angle']),
            'simple': CaseInsensitiveFrozenSet(['Angle']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './Forcetheorem_MAE/Angle': {
            'attribs': CaseInsensitiveFrozenSet(['ev-sum', 'phi', 'theta']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './Forcetheorem_SSDISP': {
            'attribs': CaseInsensitiveFrozenSet(['qvectors']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['Entry']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['Entry'],
            'several': CaseInsensitiveFrozenSet(['Entry']),
            'simple': CaseInsensitiveFrozenSet(['Entry']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './Forcetheorem_SSDISP/Entry': {
            'attribs': CaseInsensitiveFrozenSet(['ev-sum', 'q']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './allElectronCharges': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet(['fixedCharges', 'mtCharges']),
            'optional': CaseInsensitiveFrozenSet(['fixedCharges', 'mtCharges', 'spinDependentCharge', 'totalCharge']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['mtCharges', 'spinDependentCharge', 'totalCharge', 'fixedCharges'],
            'several': CaseInsensitiveFrozenSet(['fixedCharges', 'mtCharges', 'spinDependentCharge', 'totalCharge']),
            'simple': CaseInsensitiveFrozenSet(['spinDependentCharge', 'totalCharge']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './allElectronCharges/fixedCharges': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['spinDependentCharge', 'totalCharge']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['spinDependentCharge', 'totalCharge'],
            'several': CaseInsensitiveFrozenSet(['spinDependentCharge', 'totalCharge']),
            'simple': CaseInsensitiveFrozenSet(['spinDependentCharge', 'totalCharge']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './allElectronCharges/fixedCharges/spinDependentCharge': {
            'attribs': CaseInsensitiveFrozenSet(['interstitial', 'mtSpheres', 'spin', 'total', 'vacuum1', 'vacuum2']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'spin': '1',
                'vacuum1': None,
                'vacuum2': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './allElectronCharges/fixedCharges/totalCharge': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './allElectronCharges/mtCharges': {
            'attribs': CaseInsensitiveFrozenSet(['spin']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['mtCharge']),
            'optional_attribs': CaseInsensitiveDict({'spin': '1'}),
            'order': ['mtCharge'],
            'several': CaseInsensitiveFrozenSet(['mtCharge']),
            'simple': CaseInsensitiveFrozenSet(['mtCharge']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './allElectronCharges/mtCharges/mtCharge': {
            'attribs': CaseInsensitiveFrozenSet(['atomType', 'd', 'f', 'p', 's', 'total']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './allElectronCharges/spinDependentCharge': {
            'attribs': CaseInsensitiveFrozenSet(['interstitial', 'mtSpheres', 'spin', 'total', 'vacuum1', 'vacuum2']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'spin': '1',
                'vacuum1': None,
                'vacuum2': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './allElectronCharges/totalCharge': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './bandgap': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './coreStates': {
            'attribs':
            CaseInsensitiveFrozenSet(['atomType', 'atomicNumber', 'eigValSum', 'kinEnergy', 'lostElectrons', 'spin']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet(['state']),
            'optional_attribs':
            CaseInsensitiveDict({'spin': '1'}),
            'order': ['state'],
            'several':
            CaseInsensitiveFrozenSet(['state']),
            'simple':
            CaseInsensitiveFrozenSet(['state']),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        './coreStates/state': {
            'attribs': CaseInsensitiveFrozenSet(['energy', 'j', 'l', 'n', 'weight']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './densityConvergence': {
            'attribs': CaseInsensitiveFrozenSet(['units']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['chargeDensity', 'overallChargeDensity', 'spinDensity']),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': ['chargeDensity', 'overallChargeDensity', 'spinDensity'],
            'several': CaseInsensitiveFrozenSet(['chargeDensity', 'overallChargeDensity', 'spinDensity']),
            'simple': CaseInsensitiveFrozenSet(['chargeDensity', 'overallChargeDensity', 'spinDensity']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './densityConvergence/chargeDensity': {
            'attribs': CaseInsensitiveFrozenSet(['distance', 'spin', 'units']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'spin': None,
                'units': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './densityConvergence/overallChargeDensity': {
            'attribs': CaseInsensitiveFrozenSet(['distance', 'spin', 'units']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'spin': None,
                'units': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './densityConvergence/spinDensity': {
            'attribs': CaseInsensitiveFrozenSet(['distance', 'spin', 'units']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'spin': None,
                'units': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './eigenvalues': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['eigenvaluesAt'],
            'several': CaseInsensitiveFrozenSet(['eigenvaluesAt']),
            'simple': CaseInsensitiveFrozenSet(['eigenvaluesAt']),
            'text': CaseInsensitiveFrozenSet(['eigenvaluesAt'])
        },
        './eigenvalues/eigenvaluesAt': {
            'attribs': CaseInsensitiveFrozenSet(['ikpt', 'k_x', 'k_y', 'k_z', 'spin']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'spin': '1',
                'k_x': None,
                'k_y': None,
                'k_z': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './energyParameters': {
            'attribs': CaseInsensitiveFrozenSet(['units']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['atomicEP', 'heAtomicEP', 'heloAtomicEP', 'loAtomicEP', 'vacuumEP']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['atomicEP', 'heAtomicEP', 'loAtomicEP', 'heloAtomicEP', 'vacuumEP'],
            'several': CaseInsensitiveFrozenSet(['atomicEP', 'heAtomicEP', 'heloAtomicEP', 'loAtomicEP', 'vacuumEP']),
            'simple': CaseInsensitiveFrozenSet(['atomicEP', 'heAtomicEP', 'heloAtomicEP', 'loAtomicEP', 'vacuumEP']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './energyParameters/atomicEP': {
            'attribs':
            CaseInsensitiveFrozenSet(['atomType', 'branch', 'branchHighest', 'branchLowest', 'spin', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'spin': '1',
                'branchlowest': None,
                'branchhighest': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './energyParameters/heAtomicEP': {
            'attribs':
            CaseInsensitiveFrozenSet(['atomType', 'branch', 'branchHighest', 'branchLowest', 'spin', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'spin': '1',
                'branchlowest': None,
                'branchhighest': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './energyParameters/heloAtomicEP': {
            'attribs':
            CaseInsensitiveFrozenSet(['atomType', 'branch', 'branchHighest', 'branchLowest', 'spin', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'spin': '1',
                'branchlowest': None,
                'branchhighest': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './energyParameters/loAtomicEP': {
            'attribs':
            CaseInsensitiveFrozenSet(['atomType', 'branch', 'branchHighest', 'branchLowest', 'spin', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'spin': '1',
                'branchlowest': None,
                'branchhighest': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './energyParameters/vacuumEP': {
            'attribs': CaseInsensitiveFrozenSet(['spin', 'vacuum', 'value', 'vzIR', 'vzInf']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'spin': '1',
                'vzir': None,
                'vzinf': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './ldaUDensityMatrix': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['densityMatrixFor']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['densityMatrixFor'],
            'several': CaseInsensitiveFrozenSet(['densityMatrixFor']),
            'simple': CaseInsensitiveFrozenSet(['densityMatrixFor']),
            'text': CaseInsensitiveFrozenSet(['densityMatrixFor'])
        },
        './ldaUDensityMatrix/densityMatrixFor': {
            'attribs': CaseInsensitiveFrozenSet(['J', 'U', 'atomType', 'l', 'spin', 'uIndex']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './magneticMomentsInMTSpheres': {
            'attribs': CaseInsensitiveFrozenSet(['units']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['magneticMoment']),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': ['magneticMoment'],
            'several': CaseInsensitiveFrozenSet(['magneticMoment']),
            'simple': CaseInsensitiveFrozenSet(['magneticMoment']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './magneticMomentsInMTSpheres/magneticMoment': {
            'attribs': CaseInsensitiveFrozenSet(['atomType', 'moment', 'spinDownCharge', 'spinUpCharge']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './orbitalMagneticMomentsInMTSpheres': {
            'attribs': CaseInsensitiveFrozenSet(['units']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['orbMagMoment']),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': ['orbMagMoment'],
            'several': CaseInsensitiveFrozenSet(['orbMagMoment']),
            'simple': CaseInsensitiveFrozenSet(['orbMagMoment']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './orbitalMagneticMomentsInMTSpheres/orbMagMoment': {
            'attribs': CaseInsensitiveFrozenSet(['atomType', 'moment', 'spinDownCharge', 'spinUpCharge']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './rdmft': {
            'attribs': CaseInsensitiveFrozenSet(['energy']),
            'complex': CaseInsensitiveFrozenSet(['occupations']),
            'optional': CaseInsensitiveFrozenSet(['occupations']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['occupations'],
            'several': CaseInsensitiveFrozenSet(['occupations']),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './rdmft/occupations': {
            'attribs': CaseInsensitiveFrozenSet(['kpoint', 'spin']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['state']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['state'],
            'several': CaseInsensitiveFrozenSet(['state']),
            'simple': CaseInsensitiveFrozenSet(['state']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './rdmft/occupations/state': {
            'attribs': CaseInsensitiveFrozenSet(['energy', 'index', 'occupation']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './sumValenceSingleParticleEnergies': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './timing': {
            'attribs': CaseInsensitiveFrozenSet(['units']),
            'complex': CaseInsensitiveFrozenSet(['compositeTimer']),
            'optional': CaseInsensitiveFrozenSet(['compositeTimer', 'timer']),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': ['compositeTimer', 'timer'],
            'several': CaseInsensitiveFrozenSet(['compositeTimer', 'timer']),
            'simple': CaseInsensitiveFrozenSet(['timer']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './timing/timer': {
            'attribs': CaseInsensitiveFrozenSet(['name', 'units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalEnergy': {
            'attribs':
            CaseInsensitiveFrozenSet(['comment', 'units', 'value']),
            'complex':
            CaseInsensitiveFrozenSet(['atomTypeDependentContributions', 'sumOfEigenvalues']),
            'optional':
            CaseInsensitiveFrozenSet([
                'FockExchangeEnergyCore', 'FockExchangeEnergyValence', 'atomTypeDependentContributions',
                'chargeDenXCDenIntegral', 'densityCoulombPotentialIntegral', 'densityEffectivePotentialIntegral',
                'dftUCorrection', 'extrapolationTo0K', 'freeEnergy', 'sumOfEigenvalues', 'tkbTimesEntropy'
            ]),
            'optional_attribs':
            CaseInsensitiveDict({
                'units': None,
                'comment': None
            }),
            'order': [
                'sumOfEigenvalues', 'densityCoulombPotentialIntegral', 'densityEffectivePotentialIntegral',
                'chargeDenXCDenIntegral', 'FockExchangeEnergyValence', 'FockExchangeEnergyCore',
                'atomTypeDependentContributions', 'dftUCorrection', 'tkbTimesEntropy', 'freeEnergy', 'extrapolationTo0K'
            ],
            'several':
            CaseInsensitiveFrozenSet([
                'FockExchangeEnergyCore', 'FockExchangeEnergyValence', 'atomTypeDependentContributions',
                'chargeDenXCDenIntegral', 'densityCoulombPotentialIntegral', 'densityEffectivePotentialIntegral',
                'dftUCorrection', 'extrapolationTo0K', 'freeEnergy', 'sumOfEigenvalues', 'tkbTimesEntropy'
            ]),
            'simple':
            CaseInsensitiveFrozenSet([
                'FockExchangeEnergyCore', 'FockExchangeEnergyValence', 'chargeDenXCDenIntegral',
                'densityCoulombPotentialIntegral', 'densityEffectivePotentialIntegral', 'dftUCorrection',
                'extrapolationTo0K', 'freeEnergy', 'tkbTimesEntropy'
            ]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        './totalEnergy/FockExchangeEnergyCore': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalEnergy/FockExchangeEnergyValence': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalEnergy/atomTypeDependentContributions': {
            'attribs': CaseInsensitiveFrozenSet(['atomType']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['MadelungTerm', 'electronNucleiInteractionDifferentMTs']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['electronNucleiInteractionDifferentMTs', 'MadelungTerm'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['MadelungTerm', 'electronNucleiInteractionDifferentMTs']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalEnergy/atomTypeDependentContributions/MadelungTerm': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalEnergy/atomTypeDependentContributions/electronNucleiInteractionDifferentMTs': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalEnergy/chargeDenXCDenIntegral': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalEnergy/densityCoulombPotentialIntegral': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalEnergy/densityEffectivePotentialIntegral': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalEnergy/dftUCorrection': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalEnergy/extrapolationTo0K': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalEnergy/freeEnergy': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalEnergy/sumOfEigenvalues': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['coreElectrons', 'valenceElectrons']),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': ['coreElectrons', 'valenceElectrons'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['coreElectrons', 'valenceElectrons']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalEnergy/sumOfEigenvalues/coreElectrons': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalEnergy/sumOfEigenvalues/valenceElectrons': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalEnergy/tkbTimesEntropy': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalForcesOnRepresentativeAtoms': {
            'attribs': CaseInsensitiveFrozenSet(['units']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['forceTotal']),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': ['forceTotal'],
            'several': CaseInsensitiveFrozenSet(['forceTotal']),
            'simple': CaseInsensitiveFrozenSet(['forceTotal']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './totalForcesOnRepresentativeAtoms/forceTotal': {
            'attribs': CaseInsensitiveFrozenSet(['F_x', 'F_y', 'F_z', 'atomType', 'units', 'x', 'y', 'z']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './valenceDensity': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet(['fixedCharges', 'mtCharges']),
            'optional': CaseInsensitiveFrozenSet(['fixedCharges', 'mtCharges', 'spinDependentCharge', 'totalCharge']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['mtCharges', 'spinDependentCharge', 'totalCharge', 'fixedCharges'],
            'several': CaseInsensitiveFrozenSet(['fixedCharges', 'mtCharges', 'spinDependentCharge', 'totalCharge']),
            'simple': CaseInsensitiveFrozenSet(['spinDependentCharge', 'totalCharge']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './valenceDensity/fixedCharges': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['spinDependentCharge', 'totalCharge']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['spinDependentCharge', 'totalCharge'],
            'several': CaseInsensitiveFrozenSet(['spinDependentCharge', 'totalCharge']),
            'simple': CaseInsensitiveFrozenSet(['spinDependentCharge', 'totalCharge']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './valenceDensity/fixedCharges/spinDependentCharge': {
            'attribs': CaseInsensitiveFrozenSet(['interstitial', 'mtSpheres', 'spin', 'total', 'vacuum1', 'vacuum2']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'spin': '1',
                'vacuum1': None,
                'vacuum2': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './valenceDensity/fixedCharges/totalCharge': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './valenceDensity/mtCharges': {
            'attribs': CaseInsensitiveFrozenSet(['spin']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['mtCharge']),
            'optional_attribs': CaseInsensitiveDict({'spin': '1'}),
            'order': ['mtCharge'],
            'several': CaseInsensitiveFrozenSet(['mtCharge']),
            'simple': CaseInsensitiveFrozenSet(['mtCharge']),
            'text': CaseInsensitiveFrozenSet([])
        },
        './valenceDensity/mtCharges/mtCharge': {
            'attribs': CaseInsensitiveFrozenSet(['atomType', 'd', 'f', 'p', 's', 'total']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './valenceDensity/spinDependentCharge': {
            'attribs': CaseInsensitiveFrozenSet(['interstitial', 'mtSpheres', 'spin', 'total', 'vacuum1', 'vacuum2']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'spin': '1',
                'vacuum1': None,
                'vacuum2': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        './valenceDensity/totalCharge': {
            'attribs': CaseInsensitiveFrozenSet(['units', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'units': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        }
    },
    'iteration_tag_paths':
    CaseInsensitiveDict({
        'angle':
        './Forcetheorem_MAE/Angle',
        'config':
        './Forcetheorem_JIJ/Config',
        'entry': ['./Forcetheorem_DMI/Entry', './Forcetheorem_SSDISP/Entry'],
        'fermienergy':
        './FermiEnergy',
        'fockexchangeenergycore':
        './totalEnergy/FockExchangeEnergyCore',
        'fockexchangeenergyvalence':
        './totalEnergy/FockExchangeEnergyValence',
        'forcetheorem_dmi':
        './Forcetheorem_DMI',
        'forcetheorem_jij':
        './Forcetheorem_JIJ',
        'forcetheorem_loop':
        './Forcetheorem_Loop',
        'forcetheorem_mae':
        './Forcetheorem_MAE',
        'forcetheorem_ssdisp':
        './Forcetheorem_SSDISP',
        'madelungterm':
        './totalEnergy/atomTypeDependentContributions/MadelungTerm',
        'additionalcompilerflags': [],
        'allelectroncharges':
        './allElectronCharges',
        'atomtypedependentcontributions':
        './totalEnergy/atomTypeDependentContributions',
        'atomicep':
        './energyParameters/atomicEP',
        'atomsincell': [],
        'bandgap':
        './bandgap',
        'bands': [],
        'basis': [],
        'chargedenxcdenintegral':
        './totalEnergy/chargeDenXCDenIntegral',
        'chargedensity':
        './densityConvergence/chargeDensity',
        'compilationinfo': [],
        'compositetimer':
        './timing/compositeTimer',
        'coreelectrons':
        './totalEnergy/sumOfEigenvalues/coreElectrons',
        'corestates':
        './coreStates',
        'density': [],
        'densityconvergence':
        './densityConvergence',
        'densitycoulombpotentialintegral':
        './totalEnergy/densityCoulombPotentialIntegral',
        'densityeffectivepotentialintegral':
        './totalEnergy/densityEffectivePotentialIntegral',
        'densitymatrixfor':
        './ldaUDensityMatrix/densityMatrixFor',
        'dftucorrection':
        './totalEnergy/dftUCorrection',
        'eigenvalues':
        './eigenvalues',
        'eigenvaluesat':
        './eigenvalues/eigenvaluesAt',
        'electronnucleiinteractiondifferentmts':
        './totalEnergy/atomTypeDependentContributions/electronNucleiInteractionDifferentMTs',
        'enddateandtime': [],
        'energyparameters':
        './energyParameters',
        'extrapolationto0k':
        './totalEnergy/extrapolationTo0K',
        'fixedcharges': ['./allElectronCharges/fixedCharges', './valenceDensity/fixedCharges'],
        'fleuroutput': [],
        'forcetotal':
        './totalForcesOnRepresentativeAtoms/forceTotal',
        'freeenergy':
        './totalEnergy/freeEnergy',
        'gitinfo': [],
        'heatomicep':
        './energyParameters/heAtomicEP',
        'heloatomicep':
        './energyParameters/heloAtomicEP',
        'inputdata': [],
        'iteration': [],
        'kpoint': [],
        'kpointlist': [],
        'ldaudensitymatrix':
        './ldaUDensityMatrix',
        'loatomicep':
        './energyParameters/loAtomicEP',
        'magneticmoment':
        './magneticMomentsInMTSpheres/magneticMoment',
        'magneticmomentsinmtspheres':
        './magneticMomentsInMTSpheres',
        'mem': [],
        'mpi': [],
        'mtcharge': ['./allElectronCharges/mtCharges/mtCharge', './valenceDensity/mtCharges/mtCharge'],
        'mtcharges': ['./allElectronCharges/mtCharges', './valenceDensity/mtCharges'],
        'mtvolume': [],
        'numericalparameters': [],
        'occupations':
        './rdmft/occupations',
        'openmp': [],
        'orbmagmoment':
        './orbitalMagneticMomentsInMTSpheres/orbMagMoment',
        'orbitalmagneticmomentsinmtspheres':
        './orbitalMagneticMomentsInMTSpheres',
        'overallchargedensity':
        './densityConvergence/overallChargeDensity',
        'parallelsetup': [],
        'precision': [],
        'programversion': [],
        'rdmft':
        './rdmft',
        'scfloop': [],
        'spindensity':
        './densityConvergence/spinDensity',
        'spindependentcharge': [
            './allElectronCharges/fixedCharges/spinDependentCharge', './allElectronCharges/spinDependentCharge',
            './valenceDensity/fixedCharges/spinDependentCharge', './valenceDensity/spinDependentCharge'
        ],
        'startdateandtime': [],
        'state': ['./coreStates/state', './rdmft/occupations/state'],
        'sumofeigenvalues':
        './totalEnergy/sumOfEigenvalues',
        'sumvalencesingleparticleenergies':
        './sumValenceSingleParticleEnergies',
        'targetcomputerarchitectures': [],
        'targetstructureclass': [],
        'timer':
        './timing/timer',
        'timing':
        './timing',
        'tkbtimesentropy':
        './totalEnergy/tkbTimesEntropy',
        'totalcharge': [
            './allElectronCharges/fixedCharges/totalCharge', './allElectronCharges/totalCharge',
            './valenceDensity/fixedCharges/totalCharge', './valenceDensity/totalCharge'
        ],
        'totalenergy':
        './totalEnergy',
        'totalforcesonrepresentativeatoms':
        './totalForcesOnRepresentativeAtoms',
        'vacuumep':
        './energyParameters/vacuumEP',
        'valencedensity':
        './valenceDensity',
        'valenceelectrons':
        './totalEnergy/sumOfEigenvalues/valenceElectrons',
        'volumes': []
    }),
    'iteration_unique_attribs':
    CaseInsensitiveDict({
        'configs': './Forcetheorem_JIJ/@Configs',
        'numberforcurrentrun': './@numberForCurrentRun',
        'overallnumber': './@overallNumber',
        'qpoints': './Forcetheorem_DMI/@qpoints',
        'qvectors': './Forcetheorem_SSDISP/@qvectors'
    }),
    'iteration_unique_path_attribs':
    CaseInsensitiveDict({'angles': ['./Forcetheorem_DMI/@Angles', './Forcetheorem_MAE/@Angles']}),
    'omitt_contained_tags': ['scfLoop', 'eigenvalues', 'ldaUDensityMatrix'],
    'other_attribs':
    CaseInsensitiveDict({
        'atomtype': ['/fleurOutput/numericalParameters/volumes/mtVolume/@atomType'],
        'mtradius': ['/fleurOutput/numericalParameters/volumes/mtVolume/@mtRadius'],
        'mtvolume': ['/fleurOutput/numericalParameters/volumes/mtVolume/@mtVolume'],
        'kpoint': ['/fleurOutput/numericalParameters/kPointList/kPoint']
    }),
    'out_version':
    '0.30',
    'root_tag':
    'fleurOutput',
    'simple_elements':
    CaseInsensitiveDict({
        'targetcomputerarchitectures': [{
            'type': ['string'],
            'length': 1
        }],
        'targetstructureclass': [{
            'type': ['string'],
            'length': 'unbounded'
        }],
        'additionalcompilerflags': [{
            'type': ['string'],
            'length': 'unbounded'
        }],
        'kpoint': [{
            'type': ['float'],
            'length': 3
        }],
        'eigenvaluesat': [{
            'type': ['float'],
            'length': 'unbounded'
        }],
        'densitymatrixfor': [{
            'type': ['string'],
            'length': 'unbounded'
        }]
    }),
    'tag_info': {
        '/fleurOutput': {
            'attribs':
            CaseInsensitiveFrozenSet(['fleurOutputVersion']),
            'complex':
            CaseInsensitiveFrozenSet(['inputData', 'numericalParameters', 'parallelSetup', 'programVersion',
                                      'scfLoop']),
            'optional':
            CaseInsensitiveFrozenSet([
                'endDateAndTime', 'inputData', 'numericalParameters', 'parallelSetup', 'programVersion', 'scfLoop',
                'startDateAndTime'
            ]),
            'optional_attribs':
            CaseInsensitiveDict({}),
            'order': [
                'programVersion', 'parallelSetup', 'startDateAndTime', 'inputData', 'numericalParameters', 'scfLoop',
                'endDateAndTime'
            ],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet(['endDateAndTime', 'startDateAndTime']),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/endDateAndTime': {
            'attribs': CaseInsensitiveFrozenSet(['date', 'time', 'zone']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/numericalParameters': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet(['kPointList', 'volumes']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['atomsInCell', 'basis', 'density', 'bands', 'volumes', 'kPointList'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['atomsInCell', 'bands', 'basis', 'density']),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/numericalParameters/atomsInCell': {
            'attribs': CaseInsensitiveFrozenSet(['jmtd', 'n_hia', 'n_u', 'nat', 'ntype']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/numericalParameters/bands': {
            'attribs': CaseInsensitiveFrozenSet(['numbands']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/numericalParameters/basis': {
            'attribs': CaseInsensitiveFrozenSet(['lmaxd', 'nlotot', 'nvd']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/numericalParameters/density': {
            'attribs': CaseInsensitiveFrozenSet(['ng2', 'ng3']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/numericalParameters/kPointList': {
            'attribs': CaseInsensitiveFrozenSet(['count', 'weightScale']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['kPoint']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['kPoint'],
            'several': CaseInsensitiveFrozenSet(['kPoint']),
            'simple': CaseInsensitiveFrozenSet(['kPoint']),
            'text': CaseInsensitiveFrozenSet(['kPoint'])
        },
        '/fleurOutput/numericalParameters/volumes': {
            'attribs': CaseInsensitiveFrozenSet(['interstitial', 'omegaTilda', 'surfaceArea', 'unitCell', 'z1']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['mtVolume']),
            'optional_attribs': CaseInsensitiveDict({
                'omegatilda': None,
                'surfacearea': None,
                'z1': None
            }),
            'order': ['mtVolume'],
            'several': CaseInsensitiveFrozenSet(['mtVolume']),
            'simple': CaseInsensitiveFrozenSet(['mtVolume']),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/numericalParameters/volumes/mtVolume': {
            'attribs': CaseInsensitiveFrozenSet(['atomType', 'mtRadius', 'mtVolume']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/parallelSetup': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['mem', 'mpi', 'openMP']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['openMP', 'mpi', 'mem'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['mem', 'mpi', 'openMP']),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/parallelSetup/mem': {
            'attribs': CaseInsensitiveFrozenSet(['memoryPerNode']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/parallelSetup/mpi': {
            'attribs': CaseInsensitiveFrozenSet(['mpiProcesses']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/parallelSetup/openMP': {
            'attribs': CaseInsensitiveFrozenSet(['ompThreads']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/programVersion': {
            'attribs':
            CaseInsensitiveFrozenSet(['version']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([
                'additionalCompilerFlags', 'compilationInfo', 'gitInfo', 'precision', 'targetComputerArchitectures',
                'targetStructureClass'
            ]),
            'optional_attribs':
            CaseInsensitiveDict({}),
            'order': [
                'compilationInfo', 'gitInfo', 'targetComputerArchitectures', 'precision', 'targetStructureClass',
                'additionalCompilerFlags'
            ],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([
                'additionalCompilerFlags', 'compilationInfo', 'gitInfo', 'precision', 'targetComputerArchitectures',
                'targetStructureClass'
            ]),
            'text':
            CaseInsensitiveFrozenSet(['additionalCompilerFlags', 'targetComputerArchitectures', 'targetStructureClass'])
        },
        '/fleurOutput/programVersion/compilationInfo': {
            'attribs': CaseInsensitiveFrozenSet(['date', 'flag', 'host', 'link', 'user']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/programVersion/gitInfo': {
            'attribs': CaseInsensitiveFrozenSet(['branch', 'lastCommitHash', 'version']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/programVersion/precision': {
            'attribs': CaseInsensitiveFrozenSet(['type']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/scfLoop': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet(['iteration']),
            'optional': CaseInsensitiveFrozenSet(['iteration']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['iteration'],
            'several': CaseInsensitiveFrozenSet(['iteration']),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/scfLoop/iteration': {
            'attribs':
            CaseInsensitiveFrozenSet(['numberForCurrentRun', 'overallNumber']),
            'complex':
            CaseInsensitiveFrozenSet([
                'FermiEnergy', 'Forcetheorem_DMI', 'Forcetheorem_JIJ', 'Forcetheorem_Loop', 'Forcetheorem_MAE',
                'Forcetheorem_SSDISP', 'allElectronCharges', 'bandgap', 'coreStates', 'densityConvergence',
                'eigenvalues', 'energyParameters', 'ldaUDensityMatrix', 'magneticMomentsInMTSpheres',
                'orbitalMagneticMomentsInMTSpheres', 'rdmft', 'sumValenceSingleParticleEnergies', 'timing',
                'totalEnergy', 'totalForcesOnRepresentativeAtoms', 'valenceDensity'
            ]),
            'optional':
            CaseInsensitiveFrozenSet([
                'Forcetheorem_DMI', 'Forcetheorem_JIJ', 'Forcetheorem_Loop', 'Forcetheorem_MAE', 'Forcetheorem_SSDISP'
            ]),
            'optional_attribs':
            CaseInsensitiveDict({'overallnumber': None}),
            'order': [
                'energyParameters', 'eigenvalues', 'bandgap', 'sumValenceSingleParticleEnergies', 'FermiEnergy',
                'valenceDensity', 'coreStates', 'allElectronCharges', 'magneticMomentsInMTSpheres',
                'orbitalMagneticMomentsInMTSpheres', 'rdmft', 'totalEnergy', 'totalForcesOnRepresentativeAtoms',
                'ldaUDensityMatrix', 'densityConvergence', 'timing', 'Forcetheorem_Loop', 'Forcetheorem_SSDISP',
                'Forcetheorem_DMI', 'Forcetheorem_MAE', 'Forcetheorem_JIJ'
            ],
            'several':
            CaseInsensitiveFrozenSet(['Forcetheorem_Loop']),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurOutput/startDateAndTime': {
            'attribs': CaseInsensitiveFrozenSet(['date', 'time', 'zone']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        }
    },
    'tag_paths':
    CaseInsensitiveDict({
        'angle': [],
        'config': [],
        'entry': [],
        'fermienergy': [],
        'fockexchangeenergycore': [],
        'fockexchangeenergyvalence': [],
        'forcetheorem_dmi': [],
        'forcetheorem_jij': [],
        'forcetheorem_loop': [],
        'forcetheorem_mae': [],
        'forcetheorem_ssdisp': [],
        'madelungterm': [],
        'additionalcompilerflags': '/fleurOutput/programVersion/additionalCompilerFlags',
        'allelectroncharges': [],
        'atomtypedependentcontributions': [],
        'atomicep': [],
        'atomsincell': '/fleurOutput/numericalParameters/atomsInCell',
        'bandgap': [],
        'bands': '/fleurOutput/numericalParameters/bands',
        'basis': '/fleurOutput/numericalParameters/basis',
        'chargedenxcdenintegral': [],
        'chargedensity': [],
        'compilationinfo': '/fleurOutput/programVersion/compilationInfo',
        'compositetimer': [],
        'coreelectrons': [],
        'corestates': [],
        'density': '/fleurOutput/numericalParameters/density',
        'densityconvergence': [],
        'densitycoulombpotentialintegral': [],
        'densityeffectivepotentialintegral': [],
        'densitymatrixfor': [],
        'dftucorrection': [],
        'eigenvalues': [],
        'eigenvaluesat': [],
        'electronnucleiinteractiondifferentmts': [],
        'enddateandtime': '/fleurOutput/endDateAndTime',
        'energyparameters': [],
        'extrapolationto0k': [],
        'fixedcharges': [],
        'fleuroutput': '/fleurOutput',
        'forcetotal': [],
        'freeenergy': [],
        'gitinfo': '/fleurOutput/programVersion/gitInfo',
        'heatomicep': [],
        'heloatomicep': [],
        'inputdata': '/fleurOutput/inputData',
        'iteration': '/fleurOutput/scfLoop/iteration',
        'kpoint': '/fleurOutput/numericalParameters/kPointList/kPoint',
        'kpointlist': '/fleurOutput/numericalParameters/kPointList',
        'ldaudensitymatrix': [],
        'loatomicep': [],
        'magneticmoment': [],
        'magneticmomentsinmtspheres': [],
        'mem': '/fleurOutput/parallelSetup/mem',
        'mpi': '/fleurOutput/parallelSetup/mpi',
        'mtcharge': [],
        'mtcharges': [],
        'mtvolume': '/fleurOutput/numericalParameters/volumes/mtVolume',
        'numericalparameters': '/fleurOutput/numericalParameters',
        'occupations': [],
        'openmp': '/fleurOutput/parallelSetup/openMP',
        'orbmagmoment': [],
        'orbitalmagneticmomentsinmtspheres': [],
        'overallchargedensity': [],
        'parallelsetup': '/fleurOutput/parallelSetup',
        'precision': '/fleurOutput/programVersion/precision',
        'programversion': '/fleurOutput/programVersion',
        'rdmft': [],
        'scfloop': '/fleurOutput/scfLoop',
        'spindensity': [],
        'spindependentcharge': [],
        'startdateandtime': '/fleurOutput/startDateAndTime',
        'state': [],
        'sumofeigenvalues': [],
        'sumvalencesingleparticleenergies': [],
        'targetcomputerarchitectures': '/fleurOutput/programVersion/targetComputerArchitectures',
        'targetstructureclass': '/fleurOutput/programVersion/targetStructureClass',
        'timer': [],
        'timing': [],
        'tkbtimesentropy': [],
        'totalcharge': [],
        'totalenergy': [],
        'totalforcesonrepresentativeatoms': [],
        'vacuumep': [],
        'valencedensity': [],
        'valenceelectrons': [],
        'volumes': '/fleurOutput/numericalParameters/volumes'
    }),
    'unique_attribs':
    CaseInsensitiveDict({
        'branch': '/fleurOutput/programVersion/gitInfo/@branch',
        'count': '/fleurOutput/numericalParameters/kPointList/@count',
        'flag': '/fleurOutput/programVersion/compilationInfo/@flag',
        'fleuroutputversion': '/fleurOutput/@fleurOutputVersion',
        'host': '/fleurOutput/programVersion/compilationInfo/@host',
        'interstitial': '/fleurOutput/numericalParameters/volumes/@interstitial',
        'jmtd': '/fleurOutput/numericalParameters/atomsInCell/@jmtd',
        'lastcommithash': '/fleurOutput/programVersion/gitInfo/@lastCommitHash',
        'link': '/fleurOutput/programVersion/compilationInfo/@link',
        'lmaxd': '/fleurOutput/numericalParameters/basis/@lmaxd',
        'memorypernode': '/fleurOutput/parallelSetup/mem/@memoryPerNode',
        'mpiprocesses': '/fleurOutput/parallelSetup/mpi/@mpiProcesses',
        'n_hia': '/fleurOutput/numericalParameters/atomsInCell/@n_hia',
        'n_u': '/fleurOutput/numericalParameters/atomsInCell/@n_u',
        'nat': '/fleurOutput/numericalParameters/atomsInCell/@nat',
        'ng2': '/fleurOutput/numericalParameters/density/@ng2',
        'ng3': '/fleurOutput/numericalParameters/density/@ng3',
        'nlotot': '/fleurOutput/numericalParameters/basis/@nlotot',
        'ntype': '/fleurOutput/numericalParameters/atomsInCell/@ntype',
        'numbands': '/fleurOutput/numericalParameters/bands/@numbands',
        'nvd': '/fleurOutput/numericalParameters/basis/@nvd',
        'omegatilda': '/fleurOutput/numericalParameters/volumes/@omegaTilda',
        'ompthreads': '/fleurOutput/parallelSetup/openMP/@ompThreads',
        'surfacearea': '/fleurOutput/numericalParameters/volumes/@surfaceArea',
        'type': '/fleurOutput/programVersion/precision/@type',
        'unitcell': '/fleurOutput/numericalParameters/volumes/@unitCell',
        'user': '/fleurOutput/programVersion/compilationInfo/@user',
        'weightscale': '/fleurOutput/numericalParameters/kPointList/@weightScale',
        'z1': '/fleurOutput/numericalParameters/volumes/@z1',
        'additionalcompilerflags': '/fleurOutput/programVersion/additionalCompilerFlags',
        'targetcomputerarchitectures': '/fleurOutput/programVersion/targetComputerArchitectures',
        'targetstructureclass': '/fleurOutput/programVersion/targetStructureClass'
    }),
    'unique_path_attribs':
    CaseInsensitiveDict({
        'date': [
            '/fleurOutput/endDateAndTime/@date', '/fleurOutput/programVersion/compilationInfo/@date',
            '/fleurOutput/startDateAndTime/@date'
        ],
        'time': ['/fleurOutput/endDateAndTime/@time', '/fleurOutput/startDateAndTime/@time'],
        'version': ['/fleurOutput/programVersion/@version', '/fleurOutput/programVersion/gitInfo/@version'],
        'zone': ['/fleurOutput/endDateAndTime/@zone', '/fleurOutput/startDateAndTime/@zone']
    })
}
