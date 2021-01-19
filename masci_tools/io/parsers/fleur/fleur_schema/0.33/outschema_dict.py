# -*- coding: utf-8 -*-
"""
This file contains information parsed from the FleurOutputSchema.xsd
for version 0.33

The keys contain the following information:

    - 'out_version': Version string of the output schema represented in this file
    - 'input_tag': Name of the element containing the fleur input
    - 'tag_paths': simple xpath expressions to all valid tag names not in an iteration
                   Multiple paths or ambiguous tag names are parsed as a list
    - 'iteration_tag_paths': simple relative xpath expressions to all valid tag names
                             inside an iteration. Multiple paths or ambiguous tag names
                             are parsed as a list
    - 'basic_types': Parsed definitions of all simple Types with their respective
                     base type (int, float, ...) and evtl. length restrictions
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
__out_version__ = '0.33'
schema_dict = {
    'attrib_types': {
        'Angles': ['int'],
        'Configs': ['int'],
        'Delta': ['float'],
        'F_x': ['float'],
        'F_y': ['float'],
        'F_z': ['float'],
        'H_so': ['float'],
        'J': ['float'],
        'Message': ['string'],
        'No': ['int'],
        'U': ['float'],
        'atomType': ['int'],
        'atomicNumber': ['int'],
        'branch': ['string'],
        'branchHighest': ['float'],
        'branchLowest': ['float'],
        'comment': ['string'],
        'count': ['int'],
        'd': ['float'],
        'date': ['string'],
        'distance': ['float'],
        'eigValSum': ['float'],
        'energy': ['float'],
        'ev-sum': ['float'],
        'f': ['float'],
        'flag': ['string'],
        'fleurOutputVersion': ['string'],
        'host': ['string'],
        'iatom': ['int'],
        'ikpt': ['int'],
        'index': ['int'],
        'interstitial': ['float'],
        'j': ['float'],
        'jatom': ['int'],
        'jmtd': ['int'],
        'k_x': ['float'],
        'k_y': ['float'],
        'k_z': ['float'],
        'kinEnergy': ['float'],
        'kpoint': ['int'],
        'l': ['int'],
        'lastCommitHash': ['string'],
        'link': ['string'],
        'lmaxd': ['int'],
        'logDerivMT': ['float'],
        'lostElectrons': ['float'],
        'memoryPerNode': ['string'],
        'moment': ['float'],
        'mpiProcesses': ['string'],
        'mtRadius': ['float'],
        'mtSpheres': ['float'],
        'mtVolume': ['float'],
        'n': ['int'],
        'n_hia': ['int'],
        'n_u': ['int'],
        'name': ['string'],
        'nat': ['int'],
        'ng2': ['int'],
        'ng3': ['int'],
        'nlotot': ['int'],
        'ntype': ['int'],
        'numbands': ['int'],
        'numberForCurrentRun': ['int'],
        'nvd': ['int'],
        'occupation': ['float'],
        'omegaTilda': ['float'],
        'ompThreads': ['string'],
        'overallNumber': ['int'],
        'p': ['float'],
        'phase': ['switch'],
        'phi': ['float'],
        'q': ['int', 'float'],
        'qpoints': ['int'],
        'qvectors': ['int'],
        's': ['float'],
        'sigma_x': ['float'],
        'sigma_y': ['float'],
        'sigma_z': ['float'],
        'spin': ['int'],
        'spinDownCharge': ['float'],
        'spinUpCharge': ['float'],
        'surfaceArea': ['float'],
        'theta': ['float'],
        'time': ['string'],
        'total': ['float'],
        'type': ['string'],
        'uIndex': ['int'],
        'unitCell': ['float'],
        'units': ['string'],
        'user': ['string'],
        'vacuum': ['int'],
        'vacuum1': ['float'],
        'vacuum2': ['float'],
        'value': ['float'],
        'version': ['string'],
        'vzIR': ['float'],
        'vzInf': ['float'],
        'weight': ['float'],
        'weightScale': ['float'],
        'x': ['float'],
        'y': ['float'],
        'z': ['float'],
        'z1': ['float'],
        'zone': ['string']
    },
    'basic_types': {
        'AdditionalCompilerFlagsType': {
            'base_types': ['string'],
            'length': 'unbounded'
        },
        'AtomPosType': {
            'base_types': ['float_expression'],
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
        'FleurBool4DVecType': {
            'base_types': ['switch'],
            'length': 4
        },
        'FleurBoolVecType': {
            'base_types': ['switch'],
            'length': 'unbounded'
        },
        'FleurDouble2DVecType': {
            'base_types': ['float_expression'],
            'length': 2
        },
        'FleurDouble3DVecType': {
            'base_types': ['float_expression'],
            'length': 3
        },
        'FleurDoubleVecType': {
            'base_types': ['float_expression'],
            'length': 'unbounded'
        },
        'FleurVersionType': {
            'base_types': ['string'],
            'length': 1
        },
        'ForceMixEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'ForceTheoremEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'Integer3DVecType': {
            'base_types': ['int'],
            'length': 3
        },
        'Integer4DVecType': {
            'base_types': ['int'],
            'length': 4
        },
        'IntegerVecType': {
            'base_types': ['int'],
            'length': 'unbounded'
        },
        'KPointListPurposeEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'KPointType': {
            'base_types': ['float_expression'],
            'length': 3
        },
        'LatticeParameterType': {
            'base_types': ['float_expression'],
            'length': 1
        },
        'ManualCutoffType': {
            'base_types': ['float', 'string'],
            'length': 1
        },
        'ManualKKintgrCutoffType': {
            'base_types': ['float', 'string'],
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
            'base_types': ['float_expression'],
            'length': 3
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
        },
        'kPointListTypeEnum': {
            'base_types': ['string'],
            'length': 1
        }
    },
    'input_tag':
    'fleurInput',
    'iteration_other_attribs': {
        'Delta': ['./onSiteExchangeSplitting/excSplit'],
        'F_x': ['./totalForcesOnRepresentativeAtoms/forceTotal'],
        'F_y': ['./totalForcesOnRepresentativeAtoms/forceTotal'],
        'F_z': ['./totalForcesOnRepresentativeAtoms/forceTotal'],
        'H_so': ['./Forcetheorem_DMI/allAtoms', './Forcetheorem_DMI/singleAtom'],
        'J': ['./ldaUDensityMatrix/densityMatrixFor'],
        'No': ['./Forcetheorem_Loop'],
        'U': ['./ldaUDensityMatrix/densityMatrixFor'],
        'atomType': [
            './Forcetheorem_DMI/allAtoms', './Forcetheorem_DMI/singleAtom', './energyParameters/atomicEP',
            './energyParameters/heAtomicEP', './energyParameters/loAtomicEP', './energyParameters/heloAtomicEP',
            './valenceDensity/mtCharges/mtCharge', './allElectronCharges/mtCharges/mtCharge',
            './valenceDensity/mtCharges/mtJcharge', './allElectronCharges/mtCharges/mtJcharge', './coreStates',
            './magneticMomentsInMTSpheres/magneticMoment', './orbitalMagneticMomentsInMTSpheres/orbMagMoment',
            './totalForcesOnRepresentativeAtoms/forceTotal', './noncollinearTorgue/torgue', './spinorbitTorgue/torgue',
            './onSiteExchangeSplitting/excSplit', './ldaUDensityMatrix/densityMatrixFor',
            './totalEnergy/atomTypeDependentContributions'
        ],
        'atomicNumber': ['./coreStates'],
        'branch': [
            './energyParameters/atomicEP', './energyParameters/heAtomicEP', './energyParameters/loAtomicEP',
            './energyParameters/heloAtomicEP'
        ],
        'branchHighest': [
            './energyParameters/atomicEP', './energyParameters/heAtomicEP', './energyParameters/loAtomicEP',
            './energyParameters/heloAtomicEP'
        ],
        'branchLowest': [
            './energyParameters/atomicEP', './energyParameters/heAtomicEP', './energyParameters/loAtomicEP',
            './energyParameters/heloAtomicEP'
        ],
        'comment': ['./totalEnergy'],
        'd': [
            './valenceDensity/mtCharges/mtCharge', './allElectronCharges/mtCharges/mtCharge',
            './valenceDensity/mtCharges/mtJcharge/lowJ', './allElectronCharges/mtCharges/mtJcharge/lowJ',
            './valenceDensity/mtCharges/mtJcharge/highJ', './allElectronCharges/mtCharges/mtJcharge/highJ'
        ],
        'densityMatrixFor': ['./ldaUDensityMatrix/densityMatrixFor'],
        'distance': [
            './ldaUDensityMatrixConvergence/distance', './densityConvergence/chargeDensity',
            './densityConvergence/overallChargeDensity', './densityConvergence/spinDensity'
        ],
        'eigValSum': ['./coreStates'],
        'eigenvaluesAt': ['./eigenvalues/eigenvaluesAt'],
        'energy': ['./coreStates/state', './rdmft', './rdmft/occupations/state'],
        'ev-sum': [
            './Forcetheorem_SSDISP/Entry', './Forcetheorem_MAE/Angle', './Forcetheorem_JIJ/Config',
            './Forcetheorem_DMI/Entry'
        ],
        'f': [
            './valenceDensity/mtCharges/mtCharge', './allElectronCharges/mtCharges/mtCharge',
            './valenceDensity/mtCharges/mtJcharge/lowJ', './allElectronCharges/mtCharges/mtJcharge/lowJ',
            './valenceDensity/mtCharges/mtJcharge/highJ', './allElectronCharges/mtCharges/mtJcharge/highJ'
        ],
        'iatom': ['./Forcetheorem_JIJ/Config'],
        'ikpt': ['./eigenvalues/eigenvaluesAt'],
        'index': ['./rdmft/occupations/state'],
        'interstitial': [
            './valenceDensity/spinDependentCharge', './allElectronCharges/spinDependentCharge',
            './valenceDensity/fixedCharges/spinDependentCharge', './allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'j': ['./coreStates/state'],
        'jatom': ['./Forcetheorem_JIJ/Config'],
        'k_x': ['./eigenvalues/eigenvaluesAt'],
        'k_y': ['./eigenvalues/eigenvaluesAt'],
        'k_z': ['./eigenvalues/eigenvaluesAt'],
        'kinEnergy': ['./coreStates'],
        'kpoint': ['./rdmft/occupations'],
        'l': ['./coreStates/state', './onSiteExchangeSplitting/excSplit', './ldaUDensityMatrix/densityMatrixFor'],
        'lostElectrons': ['./coreStates'],
        'moment': ['./magneticMomentsInMTSpheres/magneticMoment', './orbitalMagneticMomentsInMTSpheres/orbMagMoment'],
        'mtSpheres': [
            './valenceDensity/spinDependentCharge', './allElectronCharges/spinDependentCharge',
            './valenceDensity/fixedCharges/spinDependentCharge', './allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'n': ['./Forcetheorem_JIJ/Config', './coreStates/state'],
        'name': ['./timing/timer'],
        'occupation': ['./rdmft/occupations/state'],
        'p': [
            './valenceDensity/mtCharges/mtCharge', './allElectronCharges/mtCharges/mtCharge',
            './valenceDensity/mtCharges/mtJcharge/lowJ', './allElectronCharges/mtCharges/mtJcharge/lowJ',
            './valenceDensity/mtCharges/mtJcharge/highJ', './allElectronCharges/mtCharges/mtJcharge/highJ'
        ],
        'phase': ['./Forcetheorem_JIJ/Config'],
        'phi': [
            './Forcetheorem_MAE/Angle', './Forcetheorem_DMI/Entry', './Forcetheorem_DMI/allAtoms',
            './Forcetheorem_DMI/singleAtom'
        ],
        'q': [
            './Forcetheorem_SSDISP/Entry', './Forcetheorem_JIJ/Config', './Forcetheorem_DMI/Entry',
            './Forcetheorem_DMI/allAtoms', './Forcetheorem_DMI/singleAtom'
        ],
        's': ['./valenceDensity/mtCharges/mtCharge', './allElectronCharges/mtCharges/mtCharge'],
        'sigma_x': ['./noncollinearTorgue/torgue', './spinorbitTorgue/torgue'],
        'sigma_y': ['./noncollinearTorgue/torgue', './spinorbitTorgue/torgue'],
        'sigma_z': ['./noncollinearTorgue/torgue', './spinorbitTorgue/torgue'],
        'spin': [
            './energyParameters/atomicEP', './energyParameters/heAtomicEP', './energyParameters/loAtomicEP',
            './energyParameters/heloAtomicEP', './energyParameters/vacuumEP', './eigenvalues/eigenvaluesAt',
            './valenceDensity/mtCharges', './allElectronCharges/mtCharges', './valenceDensity/spinDependentCharge',
            './allElectronCharges/spinDependentCharge', './valenceDensity/fixedCharges/spinDependentCharge',
            './allElectronCharges/fixedCharges/spinDependentCharge', './coreStates',
            './ldaUDensityMatrix/densityMatrixFor', './rdmft/occupations', './ldaUDensityMatrixConvergence/distance',
            './densityConvergence/chargeDensity', './densityConvergence/overallChargeDensity',
            './densityConvergence/spinDensity'
        ],
        'spinDownCharge':
        ['./magneticMomentsInMTSpheres/magneticMoment', './orbitalMagneticMomentsInMTSpheres/orbMagMoment'],
        'spinUpCharge':
        ['./magneticMomentsInMTSpheres/magneticMoment', './orbitalMagneticMomentsInMTSpheres/orbMagMoment'],
        'theta': [
            './Forcetheorem_MAE/Angle', './Forcetheorem_DMI/Entry', './Forcetheorem_DMI/allAtoms',
            './Forcetheorem_DMI/singleAtom'
        ],
        'total': [
            './valenceDensity/mtCharges/mtCharge', './allElectronCharges/mtCharges/mtCharge',
            './valenceDensity/spinDependentCharge', './allElectronCharges/spinDependentCharge',
            './valenceDensity/fixedCharges/spinDependentCharge', './allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'uIndex': ['./ldaUDensityMatrix/densityMatrixFor'],
        'units': [
            './energyParameters', './bandgap', './sumValenceSingleParticleEnergies', './FermiEnergy',
            './valenceDensity/totalCharge', './allElectronCharges/totalCharge',
            './valenceDensity/fixedCharges/totalCharge', './allElectronCharges/fixedCharges/totalCharge',
            './totalEnergy/densityCoulombPotentialIntegral', './totalEnergy/densityEffectivePotentialIntegral',
            './totalEnergy/chargeDenXCDenIntegral', './totalEnergy/FockExchangeEnergyValence',
            './totalEnergy/FockExchangeEnergyCore', './totalEnergy/dftUCorrection', './totalEnergy/tkbTimesEntropy',
            './totalEnergy/freeEnergy', './totalEnergy/extrapolationTo0K',
            './totalEnergy/sumOfEigenvalues/coreElectrons', './totalEnergy/sumOfEigenvalues/valenceElectrons',
            './totalEnergy/atomTypeDependentContributions/electronNucleiInteractionDifferentMTs',
            './totalEnergy/atomTypeDependentContributions/MadelungTerm', './magneticMomentsInMTSpheres',
            './orbitalMagneticMomentsInMTSpheres', './totalForcesOnRepresentativeAtoms',
            './totalForcesOnRepresentativeAtoms/forceTotal', './noncollinearTorgue/torgue', './spinorbitTorgue/torgue',
            './onSiteExchangeSplitting/excSplit', './totalEnergy', './totalEnergy/sumOfEigenvalues',
            './densityConvergence', './densityConvergence/chargeDensity', './densityConvergence/overallChargeDensity',
            './densityConvergence/spinDensity', './timing', './timing/timer'
        ],
        'vacuum': ['./energyParameters/vacuumEP'],
        'vacuum1': [
            './valenceDensity/spinDependentCharge', './allElectronCharges/spinDependentCharge',
            './valenceDensity/fixedCharges/spinDependentCharge', './allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'vacuum2': [
            './valenceDensity/spinDependentCharge', './allElectronCharges/spinDependentCharge',
            './valenceDensity/fixedCharges/spinDependentCharge', './allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'value': [
            './energyParameters/atomicEP', './energyParameters/heAtomicEP', './energyParameters/loAtomicEP',
            './energyParameters/heloAtomicEP', './energyParameters/vacuumEP', './bandgap',
            './sumValenceSingleParticleEnergies', './FermiEnergy', './valenceDensity/totalCharge',
            './allElectronCharges/totalCharge', './valenceDensity/fixedCharges/totalCharge',
            './allElectronCharges/fixedCharges/totalCharge', './totalEnergy/densityCoulombPotentialIntegral',
            './totalEnergy/densityEffectivePotentialIntegral', './totalEnergy/chargeDenXCDenIntegral',
            './totalEnergy/FockExchangeEnergyValence', './totalEnergy/FockExchangeEnergyCore',
            './totalEnergy/dftUCorrection', './totalEnergy/tkbTimesEntropy', './totalEnergy/freeEnergy',
            './totalEnergy/extrapolationTo0K', './totalEnergy/sumOfEigenvalues/coreElectrons',
            './totalEnergy/sumOfEigenvalues/valenceElectrons',
            './totalEnergy/atomTypeDependentContributions/electronNucleiInteractionDifferentMTs',
            './totalEnergy/atomTypeDependentContributions/MadelungTerm', './totalEnergy',
            './totalEnergy/sumOfEigenvalues', './timing/timer'
        ],
        'vzIR': ['./energyParameters/vacuumEP'],
        'vzInf': ['./energyParameters/vacuumEP'],
        'weight': ['./coreStates/state'],
        'x': ['./totalForcesOnRepresentativeAtoms/forceTotal'],
        'y': ['./totalForcesOnRepresentativeAtoms/forceTotal'],
        'z': ['./totalForcesOnRepresentativeAtoms/forceTotal']
    },
    'iteration_tag_info': {
        './FermiEnergy': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './Forcetheorem_DMI': {
            'attribs': ['Angles', 'qpoints'],
            'optional': ['Entry', 'allAtoms', 'singleAtom'],
            'optional_attribs': [],
            'order': ['Entry', 'allAtoms', 'singleAtom'],
            'several': ['Entry', 'allAtoms', 'singleAtom'],
            'simple': ['Entry', 'allAtoms', 'singleAtom'],
            'text': []
        },
        './Forcetheorem_DMI/Entry': {
            'attribs': ['q', 'phi', 'theta', 'ev-sum'],
            'optional': [],
            'optional_attribs': ['phi', 'theta'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './Forcetheorem_DMI/allAtoms': {
            'attribs': ['atomType', 'q', 'phi', 'theta', 'H_so'],
            'optional': [],
            'optional_attribs': ['atomType'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './Forcetheorem_DMI/singleAtom': {
            'attribs': ['atomType', 'q', 'phi', 'theta', 'H_so'],
            'optional': [],
            'optional_attribs': ['atomType'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './Forcetheorem_JIJ': {
            'attribs': ['Configs'],
            'optional': ['Config'],
            'optional_attribs': [],
            'order': ['Config'],
            'several': ['Config'],
            'simple': ['Config'],
            'text': []
        },
        './Forcetheorem_JIJ/Config': {
            'attribs': ['n', 'q', 'iatom', 'jatom', 'phase', 'ev-sum'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './Forcetheorem_Loop': {
            'attribs': ['No'],
            'optional': [],
            'optional_attribs': [],
            'order': [
                'energyParameters', 'eigenvalues', 'bandgap', 'sumValenceSingleParticleEnergies', 'FermiEnergy',
                'valenceDensity', 'onSiteExchangeSplitting', 'noncollinearTorgue', 'spinorbitTorgue', 'coreStates',
                'allElectronCharges', 'magneticMomentsInMTSpheres', 'orbitalMagneticMomentsInMTSpheres', 'rdmft',
                'totalEnergy', 'totalForcesOnRepresentativeAtoms', 'ldaUDensityMatrix', 'ldaUDensityMatrixConvergence',
                'densityConvergence', 'timing'
            ],
            'several': [],
            'simple': [],
            'text': []
        },
        './Forcetheorem_MAE': {
            'attribs': ['Angles'],
            'optional': ['Angle'],
            'optional_attribs': [],
            'order': ['Angle'],
            'several': ['Angle'],
            'simple': ['Angle'],
            'text': []
        },
        './Forcetheorem_MAE/Angle': {
            'attribs': ['phi', 'theta', 'ev-sum'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './Forcetheorem_SSDISP': {
            'attribs': ['qvectors'],
            'optional': ['Entry'],
            'optional_attribs': [],
            'order': ['Entry'],
            'several': ['Entry'],
            'simple': ['Entry'],
            'text': []
        },
        './Forcetheorem_SSDISP/Entry': {
            'attribs': ['q', 'ev-sum'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './allElectronCharges': {
            'attribs': [],
            'optional': ['mtCharges', 'spinDependentCharge', 'totalCharge', 'fixedCharges'],
            'optional_attribs': [],
            'order': ['mtCharges', 'spinDependentCharge', 'totalCharge', 'fixedCharges'],
            'several': ['mtCharges', 'spinDependentCharge', 'totalCharge', 'fixedCharges'],
            'simple': ['spinDependentCharge', 'totalCharge'],
            'text': []
        },
        './allElectronCharges/fixedCharges': {
            'attribs': [],
            'optional': ['spinDependentCharge', 'totalCharge'],
            'optional_attribs': [],
            'order': ['spinDependentCharge', 'totalCharge'],
            'several': ['spinDependentCharge', 'totalCharge'],
            'simple': ['spinDependentCharge', 'totalCharge'],
            'text': []
        },
        './allElectronCharges/fixedCharges/spinDependentCharge': {
            'attribs': ['spin', 'total', 'interstitial', 'mtSpheres', 'vacuum1', 'vacuum2'],
            'optional': [],
            'optional_attribs': ['spin', 'vacuum1', 'vacuum2'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './allElectronCharges/fixedCharges/totalCharge': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './allElectronCharges/mtCharges': {
            'attribs': ['spin'],
            'optional': ['mtCharge', 'mtJcharge'],
            'optional_attribs': ['spin'],
            'order': ['mtCharge', 'mtJcharge'],
            'several': ['mtCharge', 'mtJcharge'],
            'simple': ['mtCharge'],
            'text': []
        },
        './allElectronCharges/mtCharges/mtCharge': {
            'attribs': ['atomType', 'total', 's', 'p', 'd', 'f'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './allElectronCharges/mtCharges/mtJcharge': {
            'attribs': ['atomType'],
            'optional': [],
            'optional_attribs': [],
            'order': ['lowJ', 'highJ'],
            'several': [],
            'simple': ['lowJ', 'highJ'],
            'text': []
        },
        './allElectronCharges/mtCharges/mtJcharge/highJ': {
            'attribs': ['p', 'd', 'f'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './allElectronCharges/mtCharges/mtJcharge/lowJ': {
            'attribs': ['p', 'd', 'f'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './allElectronCharges/spinDependentCharge': {
            'attribs': ['spin', 'total', 'interstitial', 'mtSpheres', 'vacuum1', 'vacuum2'],
            'optional': [],
            'optional_attribs': ['spin', 'vacuum1', 'vacuum2'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './allElectronCharges/totalCharge': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './bandgap': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './coreStates': {
            'attribs': ['atomType', 'atomicNumber', 'spin', 'kinEnergy', 'eigValSum', 'lostElectrons'],
            'optional': ['state'],
            'optional_attribs': ['spin'],
            'order': ['state'],
            'several': ['state'],
            'simple': ['state'],
            'text': []
        },
        './coreStates/state': {
            'attribs': ['n', 'l', 'j', 'energy', 'weight'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './densityConvergence': {
            'attribs': ['units'],
            'optional': ['chargeDensity', 'overallChargeDensity', 'spinDensity'],
            'optional_attribs': ['units'],
            'order': ['chargeDensity', 'overallChargeDensity', 'spinDensity'],
            'several': ['chargeDensity', 'overallChargeDensity', 'spinDensity'],
            'simple': ['chargeDensity', 'overallChargeDensity', 'spinDensity'],
            'text': []
        },
        './densityConvergence/chargeDensity': {
            'attribs': ['spin', 'distance', 'units'],
            'optional': [],
            'optional_attribs': ['spin', 'units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './densityConvergence/overallChargeDensity': {
            'attribs': ['spin', 'distance', 'units'],
            'optional': [],
            'optional_attribs': ['spin', 'units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './densityConvergence/spinDensity': {
            'attribs': ['spin', 'distance', 'units'],
            'optional': [],
            'optional_attribs': ['spin', 'units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './eigenvalues': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['eigenvaluesAt'],
            'several': ['eigenvaluesAt'],
            'simple': ['eigenvaluesAt'],
            'text': ['eigenvaluesAt']
        },
        './eigenvalues/eigenvaluesAt': {
            'attribs': ['spin', 'ikpt', 'k_x', 'k_y', 'k_z'],
            'optional': [],
            'optional_attribs': ['spin', 'k_x', 'k_y', 'k_z'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './energyParameters': {
            'attribs': ['units'],
            'optional': ['atomicEP', 'heAtomicEP', 'loAtomicEP', 'heloAtomicEP', 'vacuumEP'],
            'optional_attribs': [],
            'order': ['atomicEP', 'heAtomicEP', 'loAtomicEP', 'heloAtomicEP', 'vacuumEP'],
            'several': ['atomicEP', 'heAtomicEP', 'loAtomicEP', 'heloAtomicEP', 'vacuumEP'],
            'simple': ['atomicEP', 'heAtomicEP', 'loAtomicEP', 'heloAtomicEP', 'vacuumEP'],
            'text': []
        },
        './energyParameters/atomicEP': {
            'attribs': ['atomType', 'spin', 'branch', 'branchLowest', 'branchHighest', 'value'],
            'optional': [],
            'optional_attribs': ['spin', 'branchLowest', 'branchHighest'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './energyParameters/heAtomicEP': {
            'attribs': ['atomType', 'spin', 'branch', 'branchLowest', 'branchHighest', 'value'],
            'optional': [],
            'optional_attribs': ['spin', 'branchLowest', 'branchHighest'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './energyParameters/heloAtomicEP': {
            'attribs': ['atomType', 'spin', 'branch', 'branchLowest', 'branchHighest', 'value'],
            'optional': [],
            'optional_attribs': ['spin', 'branchLowest', 'branchHighest'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './energyParameters/loAtomicEP': {
            'attribs': ['atomType', 'spin', 'branch', 'branchLowest', 'branchHighest', 'value'],
            'optional': [],
            'optional_attribs': ['spin', 'branchLowest', 'branchHighest'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './energyParameters/vacuumEP': {
            'attribs': ['vacuum', 'spin', 'vzIR', 'vzInf', 'value'],
            'optional': [],
            'optional_attribs': ['spin', 'vzIR', 'vzInf'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './ldaUDensityMatrix': {
            'attribs': [],
            'optional': ['densityMatrixFor'],
            'optional_attribs': [],
            'order': ['densityMatrixFor'],
            'several': ['densityMatrixFor'],
            'simple': ['densityMatrixFor'],
            'text': ['densityMatrixFor']
        },
        './ldaUDensityMatrix/densityMatrixFor': {
            'attribs': ['spin', 'atomType', 'uIndex', 'l', 'U', 'J'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './ldaUDensityMatrixConvergence': {
            'attribs': [],
            'optional': ['distance'],
            'optional_attribs': [],
            'order': ['distance'],
            'several': ['distance'],
            'simple': ['distance'],
            'text': []
        },
        './ldaUDensityMatrixConvergence/distance': {
            'attribs': ['spin', 'distance'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './magneticMomentsInMTSpheres': {
            'attribs': ['units'],
            'optional': ['magneticMoment'],
            'optional_attribs': ['units'],
            'order': ['magneticMoment'],
            'several': ['magneticMoment'],
            'simple': ['magneticMoment'],
            'text': []
        },
        './magneticMomentsInMTSpheres/magneticMoment': {
            'attribs': ['atomType', 'moment', 'spinUpCharge', 'spinDownCharge'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './noncollinearTorgue': {
            'attribs': [],
            'optional': ['torgue'],
            'optional_attribs': [],
            'order': ['torgue'],
            'several': ['torgue'],
            'simple': ['torgue'],
            'text': []
        },
        './noncollinearTorgue/torgue': {
            'attribs': ['atomType', 'sigma_x', 'sigma_y', 'sigma_z', 'units'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './onSiteExchangeSplitting': {
            'attribs': [],
            'optional': ['excSplit'],
            'optional_attribs': [],
            'order': ['excSplit'],
            'several': ['excSplit'],
            'simple': ['excSplit'],
            'text': []
        },
        './onSiteExchangeSplitting/excSplit': {
            'attribs': ['atomType', 'l', 'Delta', 'units'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './orbitalMagneticMomentsInMTSpheres': {
            'attribs': ['units'],
            'optional': ['orbMagMoment'],
            'optional_attribs': ['units'],
            'order': ['orbMagMoment'],
            'several': ['orbMagMoment'],
            'simple': ['orbMagMoment'],
            'text': []
        },
        './orbitalMagneticMomentsInMTSpheres/orbMagMoment': {
            'attribs': ['atomType', 'moment', 'spinUpCharge', 'spinDownCharge'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './rdmft': {
            'attribs': ['energy'],
            'optional': ['occupations'],
            'optional_attribs': [],
            'order': ['occupations'],
            'several': ['occupations'],
            'simple': [],
            'text': []
        },
        './rdmft/occupations': {
            'attribs': ['spin', 'kpoint'],
            'optional': ['state'],
            'optional_attribs': [],
            'order': ['state'],
            'several': ['state'],
            'simple': ['state'],
            'text': []
        },
        './rdmft/occupations/state': {
            'attribs': ['index', 'energy', 'occupation'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './spinorbitTorgue': {
            'attribs': [],
            'optional': ['torgue'],
            'optional_attribs': [],
            'order': ['torgue'],
            'several': ['torgue'],
            'simple': ['torgue'],
            'text': []
        },
        './spinorbitTorgue/torgue': {
            'attribs': ['atomType', 'sigma_x', 'sigma_y', 'sigma_z', 'units'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './sumValenceSingleParticleEnergies': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './timing': {
            'attribs': ['units'],
            'optional': ['compositeTimer', 'timer'],
            'optional_attribs': ['units'],
            'order': ['compositeTimer', 'timer'],
            'several': ['compositeTimer', 'timer'],
            'simple': ['timer'],
            'text': []
        },
        './timing/timer': {
            'attribs': ['name', 'value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './totalEnergy': {
            'attribs': ['value', 'units', 'comment'],
            'optional': [
                'sumOfEigenvalues', 'densityCoulombPotentialIntegral', 'densityEffectivePotentialIntegral',
                'chargeDenXCDenIntegral', 'FockExchangeEnergyValence', 'FockExchangeEnergyCore',
                'atomTypeDependentContributions', 'dftUCorrection', 'tkbTimesEntropy', 'freeEnergy', 'extrapolationTo0K'
            ],
            'optional_attribs': ['units', 'comment'],
            'order': [
                'sumOfEigenvalues', 'densityCoulombPotentialIntegral', 'densityEffectivePotentialIntegral',
                'chargeDenXCDenIntegral', 'FockExchangeEnergyValence', 'FockExchangeEnergyCore',
                'atomTypeDependentContributions', 'dftUCorrection', 'tkbTimesEntropy', 'freeEnergy', 'extrapolationTo0K'
            ],
            'several': [
                'sumOfEigenvalues', 'densityCoulombPotentialIntegral', 'densityEffectivePotentialIntegral',
                'chargeDenXCDenIntegral', 'FockExchangeEnergyValence', 'FockExchangeEnergyCore',
                'atomTypeDependentContributions', 'dftUCorrection', 'tkbTimesEntropy', 'freeEnergy', 'extrapolationTo0K'
            ],
            'simple': [
                'sumOfEigenvalues', 'densityCoulombPotentialIntegral', 'densityEffectivePotentialIntegral',
                'chargeDenXCDenIntegral', 'FockExchangeEnergyValence', 'FockExchangeEnergyCore',
                'atomTypeDependentContributions', 'dftUCorrection', 'tkbTimesEntropy', 'freeEnergy', 'extrapolationTo0K'
            ],
            'text': []
        },
        './totalEnergy/FockExchangeEnergyCore': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './totalEnergy/FockExchangeEnergyValence': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './totalEnergy/atomTypeDependentContributions': {
            'attribs': ['atomType'],
            'optional': ['electronNucleiInteractionDifferentMTs', 'MadelungTerm'],
            'optional_attribs': [],
            'order': ['electronNucleiInteractionDifferentMTs', 'MadelungTerm'],
            'several': [],
            'simple': ['electronNucleiInteractionDifferentMTs', 'MadelungTerm'],
            'text': []
        },
        './totalEnergy/atomTypeDependentContributions/MadelungTerm': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './totalEnergy/atomTypeDependentContributions/electronNucleiInteractionDifferentMTs': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './totalEnergy/chargeDenXCDenIntegral': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './totalEnergy/densityCoulombPotentialIntegral': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './totalEnergy/densityEffectivePotentialIntegral': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './totalEnergy/dftUCorrection': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './totalEnergy/extrapolationTo0K': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './totalEnergy/freeEnergy': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './totalEnergy/sumOfEigenvalues': {
            'attribs': ['value', 'units'],
            'optional': ['coreElectrons', 'valenceElectrons'],
            'optional_attribs': ['units'],
            'order': ['coreElectrons', 'valenceElectrons'],
            'several': [],
            'simple': ['coreElectrons', 'valenceElectrons'],
            'text': []
        },
        './totalEnergy/sumOfEigenvalues/coreElectrons': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './totalEnergy/sumOfEigenvalues/valenceElectrons': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './totalEnergy/tkbTimesEntropy': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './totalForcesOnRepresentativeAtoms': {
            'attribs': ['units'],
            'optional': ['forceTotal'],
            'optional_attribs': ['units'],
            'order': ['forceTotal'],
            'several': ['forceTotal'],
            'simple': ['forceTotal'],
            'text': []
        },
        './totalForcesOnRepresentativeAtoms/forceTotal': {
            'attribs': ['atomType', 'x', 'y', 'z', 'F_x', 'F_y', 'F_z', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './valenceDensity': {
            'attribs': [],
            'optional': ['mtCharges', 'spinDependentCharge', 'totalCharge', 'fixedCharges'],
            'optional_attribs': [],
            'order': ['mtCharges', 'spinDependentCharge', 'totalCharge', 'fixedCharges'],
            'several': ['mtCharges', 'spinDependentCharge', 'totalCharge', 'fixedCharges'],
            'simple': ['spinDependentCharge', 'totalCharge'],
            'text': []
        },
        './valenceDensity/fixedCharges': {
            'attribs': [],
            'optional': ['spinDependentCharge', 'totalCharge'],
            'optional_attribs': [],
            'order': ['spinDependentCharge', 'totalCharge'],
            'several': ['spinDependentCharge', 'totalCharge'],
            'simple': ['spinDependentCharge', 'totalCharge'],
            'text': []
        },
        './valenceDensity/fixedCharges/spinDependentCharge': {
            'attribs': ['spin', 'total', 'interstitial', 'mtSpheres', 'vacuum1', 'vacuum2'],
            'optional': [],
            'optional_attribs': ['spin', 'vacuum1', 'vacuum2'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './valenceDensity/fixedCharges/totalCharge': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './valenceDensity/mtCharges': {
            'attribs': ['spin'],
            'optional': ['mtCharge', 'mtJcharge'],
            'optional_attribs': ['spin'],
            'order': ['mtCharge', 'mtJcharge'],
            'several': ['mtCharge', 'mtJcharge'],
            'simple': ['mtCharge'],
            'text': []
        },
        './valenceDensity/mtCharges/mtCharge': {
            'attribs': ['atomType', 'total', 's', 'p', 'd', 'f'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './valenceDensity/mtCharges/mtJcharge': {
            'attribs': ['atomType'],
            'optional': [],
            'optional_attribs': [],
            'order': ['lowJ', 'highJ'],
            'several': [],
            'simple': ['lowJ', 'highJ'],
            'text': []
        },
        './valenceDensity/mtCharges/mtJcharge/highJ': {
            'attribs': ['p', 'd', 'f'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './valenceDensity/mtCharges/mtJcharge/lowJ': {
            'attribs': ['p', 'd', 'f'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './valenceDensity/spinDependentCharge': {
            'attribs': ['spin', 'total', 'interstitial', 'mtSpheres', 'vacuum1', 'vacuum2'],
            'optional': [],
            'optional_attribs': ['spin', 'vacuum1', 'vacuum2'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './valenceDensity/totalCharge': {
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        }
    },
    'iteration_tag_paths': {
        'Angle':
        './Forcetheorem_MAE/Angle',
        'Config':
        './Forcetheorem_JIJ/Config',
        'Entry': ['./Forcetheorem_DMI/Entry', './Forcetheorem_SSDISP/Entry'],
        'FermiEnergy':
        './FermiEnergy',
        'FockExchangeEnergyCore':
        './totalEnergy/FockExchangeEnergyCore',
        'FockExchangeEnergyValence':
        './totalEnergy/FockExchangeEnergyValence',
        'Forcetheorem_DMI':
        './Forcetheorem_DMI',
        'Forcetheorem_JIJ':
        './Forcetheorem_JIJ',
        'Forcetheorem_Loop':
        './Forcetheorem_Loop',
        'Forcetheorem_MAE':
        './Forcetheorem_MAE',
        'Forcetheorem_SSDISP':
        './Forcetheorem_SSDISP',
        'MadelungTerm':
        './totalEnergy/atomTypeDependentContributions/MadelungTerm',
        'allAtoms':
        './Forcetheorem_DMI/allAtoms',
        'allElectronCharges':
        './allElectronCharges',
        'atomTypeDependentContributions':
        './totalEnergy/atomTypeDependentContributions',
        'atomicEP':
        './energyParameters/atomicEP',
        'bandgap':
        './bandgap',
        'chargeDenXCDenIntegral':
        './totalEnergy/chargeDenXCDenIntegral',
        'chargeDensity':
        './densityConvergence/chargeDensity',
        'compositeTimer':
        './timing/compositeTimer',
        'coreElectrons':
        './totalEnergy/sumOfEigenvalues/coreElectrons',
        'coreStates':
        './coreStates',
        'densityConvergence':
        './densityConvergence',
        'densityCoulombPotentialIntegral':
        './totalEnergy/densityCoulombPotentialIntegral',
        'densityEffectivePotentialIntegral':
        './totalEnergy/densityEffectivePotentialIntegral',
        'densityMatrixFor':
        './ldaUDensityMatrix/densityMatrixFor',
        'dftUCorrection':
        './totalEnergy/dftUCorrection',
        'distance':
        './ldaUDensityMatrixConvergence/distance',
        'eigenvalues':
        './eigenvalues',
        'eigenvaluesAt':
        './eigenvalues/eigenvaluesAt',
        'electronNucleiInteractionDifferentMTs':
        './totalEnergy/atomTypeDependentContributions/electronNucleiInteractionDifferentMTs',
        'energyParameters':
        './energyParameters',
        'excSplit':
        './onSiteExchangeSplitting/excSplit',
        'extrapolationTo0K':
        './totalEnergy/extrapolationTo0K',
        'fixedCharges': ['./valenceDensity/fixedCharges', './allElectronCharges/fixedCharges'],
        'forceTotal':
        './totalForcesOnRepresentativeAtoms/forceTotal',
        'freeEnergy':
        './totalEnergy/freeEnergy',
        'heAtomicEP':
        './energyParameters/heAtomicEP',
        'heloAtomicEP':
        './energyParameters/heloAtomicEP',
        'highJ': ['./valenceDensity/mtCharges/mtJcharge/highJ', './allElectronCharges/mtCharges/mtJcharge/highJ'],
        'ldaUDensityMatrix':
        './ldaUDensityMatrix',
        'ldaUDensityMatrixConvergence':
        './ldaUDensityMatrixConvergence',
        'loAtomicEP':
        './energyParameters/loAtomicEP',
        'lowJ': ['./valenceDensity/mtCharges/mtJcharge/lowJ', './allElectronCharges/mtCharges/mtJcharge/lowJ'],
        'magneticMoment':
        './magneticMomentsInMTSpheres/magneticMoment',
        'magneticMomentsInMTSpheres':
        './magneticMomentsInMTSpheres',
        'mtCharge': ['./valenceDensity/mtCharges/mtCharge', './allElectronCharges/mtCharges/mtCharge'],
        'mtCharges': ['./valenceDensity/mtCharges', './allElectronCharges/mtCharges'],
        'mtJcharge': ['./valenceDensity/mtCharges/mtJcharge', './allElectronCharges/mtCharges/mtJcharge'],
        'noncollinearTorgue':
        './noncollinearTorgue',
        'occupations':
        './rdmft/occupations',
        'onSiteExchangeSplitting':
        './onSiteExchangeSplitting',
        'orbMagMoment':
        './orbitalMagneticMomentsInMTSpheres/orbMagMoment',
        'orbitalMagneticMomentsInMTSpheres':
        './orbitalMagneticMomentsInMTSpheres',
        'overallChargeDensity':
        './densityConvergence/overallChargeDensity',
        'rdmft':
        './rdmft',
        'singleAtom':
        './Forcetheorem_DMI/singleAtom',
        'spinDensity':
        './densityConvergence/spinDensity',
        'spinDependentCharge': [
            './valenceDensity/spinDependentCharge', './allElectronCharges/spinDependentCharge',
            './valenceDensity/fixedCharges/spinDependentCharge', './allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'spinorbitTorgue':
        './spinorbitTorgue',
        'state': ['./coreStates/state', './rdmft/occupations/state'],
        'sumOfEigenvalues':
        './totalEnergy/sumOfEigenvalues',
        'sumValenceSingleParticleEnergies':
        './sumValenceSingleParticleEnergies',
        'timer':
        './timing/timer',
        'timing':
        './timing',
        'tkbTimesEntropy':
        './totalEnergy/tkbTimesEntropy',
        'torgue': ['./noncollinearTorgue/torgue', './spinorbitTorgue/torgue'],
        'totalCharge': [
            './valenceDensity/totalCharge', './allElectronCharges/totalCharge',
            './valenceDensity/fixedCharges/totalCharge', './allElectronCharges/fixedCharges/totalCharge'
        ],
        'totalEnergy':
        './totalEnergy',
        'totalForcesOnRepresentativeAtoms':
        './totalForcesOnRepresentativeAtoms',
        'vacuumEP':
        './energyParameters/vacuumEP',
        'valenceDensity':
        './valenceDensity',
        'valenceElectrons':
        './totalEnergy/sumOfEigenvalues/valenceElectrons'
    },
    'iteration_unique_attribs': {
        'Configs': './Forcetheorem_JIJ',
        'numberForCurrentRun': './',
        'overallNumber': './',
        'qpoints': './Forcetheorem_DMI',
        'qvectors': './Forcetheorem_SSDISP'
    },
    'iteration_unique_path_attribs': {
        'Angles': ['./Forcetheorem_DMI', './Forcetheorem_MAE']
    },
    'omitt_contained_tags': [
        'scfLoop', 'eigenvalues', 'onSiteExchangeSplitting', 'noncollinearTorgue', 'spinorbitTorgue',
        'ldaUDensityMatrix', 'ldaUDensityMatrixConvergence'
    ],
    'other_attribs': {
        'atomType': ['/fleurOutput/numericalParameters/volumes/mtVolume'],
        'kPoint': ['/fleurOutput/numericalParameters/kPointList/kPoint'],
        'mtRadius': ['/fleurOutput/numericalParameters/volumes/mtVolume'],
        'mtVolume': ['/fleurOutput/numericalParameters/volumes/mtVolume']
    },
    'out_version':
    '0.33',
    'root_tag':
    'fleurOutput',
    'simple_elements': {
        'additionalCompilerFlags': [{
            'length': 'unbounded',
            'type': ['string']
        }],
        'densityMatrixFor': [{
            'length': 'unbounded',
            'type': ['string']
        }],
        'eigenvaluesAt': [{
            'length': 'unbounded',
            'type': ['float']
        }],
        'kPoint': [{
            'length': 3,
            'type': ['float_expression']
        }],
        'targetComputerArchitectures': [{
            'length': 1,
            'type': ['string']
        }],
        'targetStructureClass': [{
            'length': 'unbounded',
            'type': ['string']
        }]
    },
    'tag_info': {
        '/fleurOutput': {
            'attribs': ['fleurOutputVersion'],
            'optional': [
                'programVersion', 'parallelSetup', 'startDateAndTime', 'fleurInput', 'numericalParameters', 'scfLoop',
                'ERROR', 'endDateAndTime'
            ],
            'optional_attribs': [],
            'order': [
                'programVersion', 'parallelSetup', 'startDateAndTime', 'fleurInput', 'numericalParameters', 'scfLoop',
                'ERROR', 'endDateAndTime'
            ],
            'several': [],
            'simple': ['programVersion', 'startDateAndTime', 'fleurInput', 'ERROR', 'endDateAndTime'],
            'text': []
        },
        '/fleurOutput/ERROR': {
            'attribs': ['Message'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/endDateAndTime': {
            'attribs': ['date', 'time', 'zone'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/numericalParameters': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['atomsInCell', 'basis', 'density', 'bands', 'volumes', 'kPointList'],
            'several': [],
            'simple': ['atomsInCell', 'basis', 'density', 'bands'],
            'text': []
        },
        '/fleurOutput/numericalParameters/atomsInCell': {
            'attribs': ['nat', 'ntype', 'jmtd', 'n_u', 'n_hia'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/numericalParameters/bands': {
            'attribs': ['numbands'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/numericalParameters/basis': {
            'attribs': ['nvd', 'lmaxd', 'nlotot'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/numericalParameters/density': {
            'attribs': ['ng3', 'ng2'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/numericalParameters/kPointList': {
            'attribs': ['weightScale', 'count'],
            'optional': ['kPoint'],
            'optional_attribs': [],
            'order': ['kPoint'],
            'several': ['kPoint'],
            'simple': ['kPoint'],
            'text': ['kPoint']
        },
        '/fleurOutput/numericalParameters/volumes': {
            'attribs': ['unitCell', 'interstitial', 'omegaTilda', 'surfaceArea', 'z1'],
            'optional': ['mtVolume'],
            'optional_attribs': ['omegaTilda', 'surfaceArea', 'z1'],
            'order': ['mtVolume'],
            'several': ['mtVolume'],
            'simple': ['mtVolume'],
            'text': []
        },
        '/fleurOutput/numericalParameters/volumes/mtVolume': {
            'attribs': ['atomType', 'mtRadius', 'mtVolume'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/parallelSetup': {
            'attribs': [],
            'optional': ['openMP', 'mpi', 'mem'],
            'optional_attribs': [],
            'order': ['openMP', 'mpi', 'mem'],
            'several': [],
            'simple': ['openMP', 'mpi', 'mem'],
            'text': []
        },
        '/fleurOutput/parallelSetup/mem': {
            'attribs': ['memoryPerNode'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/parallelSetup/mpi': {
            'attribs': ['mpiProcesses'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/parallelSetup/openMP': {
            'attribs': ['ompThreads'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/programVersion': {
            'attribs': ['version'],
            'optional': [
                'compilationInfo', 'gitInfo', 'targetComputerArchitectures', 'precision', 'targetStructureClass',
                'additionalCompilerFlags'
            ],
            'optional_attribs': [],
            'order': [
                'compilationInfo', 'gitInfo', 'targetComputerArchitectures', 'precision', 'targetStructureClass',
                'additionalCompilerFlags'
            ],
            'several': [],
            'simple': [
                'compilationInfo', 'gitInfo', 'targetComputerArchitectures', 'precision', 'targetStructureClass',
                'additionalCompilerFlags'
            ],
            'text': ['targetComputerArchitectures', 'targetStructureClass', 'additionalCompilerFlags']
        },
        '/fleurOutput/programVersion/compilationInfo': {
            'attribs': ['date', 'user', 'host', 'flag', 'link'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/programVersion/gitInfo': {
            'attribs': ['version', 'lastCommitHash', 'branch'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/programVersion/precision': {
            'attribs': ['type'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop': {
            'attribs': [],
            'optional': ['iteration'],
            'optional_attribs': [],
            'order': ['iteration'],
            'several': ['iteration'],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration': {
            'attribs': ['numberForCurrentRun', 'overallNumber'],
            'optional':
            ['Forcetheorem_Loop', 'Forcetheorem_SSDISP', 'Forcetheorem_DMI', 'Forcetheorem_MAE', 'Forcetheorem_JIJ'],
            'optional_attribs': ['overallNumber'],
            'order': [
                'energyParameters', 'eigenvalues', 'bandgap', 'sumValenceSingleParticleEnergies', 'FermiEnergy',
                'valenceDensity', 'onSiteExchangeSplitting', 'noncollinearTorgue', 'spinorbitTorgue', 'coreStates',
                'allElectronCharges', 'magneticMomentsInMTSpheres', 'orbitalMagneticMomentsInMTSpheres', 'rdmft',
                'totalEnergy', 'totalForcesOnRepresentativeAtoms', 'ldaUDensityMatrix', 'ldaUDensityMatrixConvergence',
                'densityConvergence', 'timing', 'Forcetheorem_Loop', 'Forcetheorem_SSDISP', 'Forcetheorem_DMI',
                'Forcetheorem_MAE', 'Forcetheorem_JIJ'
            ],
            'several': ['Forcetheorem_Loop'],
            'simple': [],
            'text': []
        },
        '/fleurOutput/startDateAndTime': {
            'attribs': ['date', 'time', 'zone'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        }
    },
    'tag_paths': {
        'ERROR': '/fleurOutput/ERROR',
        'additionalCompilerFlags': '/fleurOutput/programVersion/additionalCompilerFlags',
        'atomsInCell': '/fleurOutput/numericalParameters/atomsInCell',
        'bands': '/fleurOutput/numericalParameters/bands',
        'basis': '/fleurOutput/numericalParameters/basis',
        'compilationInfo': '/fleurOutput/programVersion/compilationInfo',
        'density': '/fleurOutput/numericalParameters/density',
        'endDateAndTime': '/fleurOutput/endDateAndTime',
        'fleurInput': '/fleurOutput/fleurInput',
        'fleurOutput': '/fleurOutput',
        'gitInfo': '/fleurOutput/programVersion/gitInfo',
        'iteration': '/fleurOutput/scfLoop/iteration',
        'kPoint': '/fleurOutput/numericalParameters/kPointList/kPoint',
        'kPointList': '/fleurOutput/numericalParameters/kPointList',
        'mem': '/fleurOutput/parallelSetup/mem',
        'mpi': '/fleurOutput/parallelSetup/mpi',
        'mtVolume': '/fleurOutput/numericalParameters/volumes/mtVolume',
        'numericalParameters': '/fleurOutput/numericalParameters',
        'openMP': '/fleurOutput/parallelSetup/openMP',
        'parallelSetup': '/fleurOutput/parallelSetup',
        'precision': '/fleurOutput/programVersion/precision',
        'programVersion': '/fleurOutput/programVersion',
        'scfLoop': '/fleurOutput/scfLoop',
        'startDateAndTime': '/fleurOutput/startDateAndTime',
        'targetComputerArchitectures': '/fleurOutput/programVersion/targetComputerArchitectures',
        'targetStructureClass': '/fleurOutput/programVersion/targetStructureClass',
        'volumes': '/fleurOutput/numericalParameters/volumes'
    },
    'unique_attribs': {
        'Message': '/fleurOutput/ERROR',
        'additionalCompilerFlags': '/fleurOutput/programVersion/additionalCompilerFlags',
        'branch': '/fleurOutput/programVersion/gitInfo',
        'count': '/fleurOutput/numericalParameters/kPointList',
        'flag': '/fleurOutput/programVersion/compilationInfo',
        'fleurOutputVersion': '/fleurOutput',
        'host': '/fleurOutput/programVersion/compilationInfo',
        'interstitial': '/fleurOutput/numericalParameters/volumes',
        'jmtd': '/fleurOutput/numericalParameters/atomsInCell',
        'lastCommitHash': '/fleurOutput/programVersion/gitInfo',
        'link': '/fleurOutput/programVersion/compilationInfo',
        'lmaxd': '/fleurOutput/numericalParameters/basis',
        'memoryPerNode': '/fleurOutput/parallelSetup/mem',
        'mpiProcesses': '/fleurOutput/parallelSetup/mpi',
        'n_hia': '/fleurOutput/numericalParameters/atomsInCell',
        'n_u': '/fleurOutput/numericalParameters/atomsInCell',
        'nat': '/fleurOutput/numericalParameters/atomsInCell',
        'ng2': '/fleurOutput/numericalParameters/density',
        'ng3': '/fleurOutput/numericalParameters/density',
        'nlotot': '/fleurOutput/numericalParameters/basis',
        'ntype': '/fleurOutput/numericalParameters/atomsInCell',
        'numbands': '/fleurOutput/numericalParameters/bands',
        'nvd': '/fleurOutput/numericalParameters/basis',
        'omegaTilda': '/fleurOutput/numericalParameters/volumes',
        'ompThreads': '/fleurOutput/parallelSetup/openMP',
        'surfaceArea': '/fleurOutput/numericalParameters/volumes',
        'targetComputerArchitectures': '/fleurOutput/programVersion/targetComputerArchitectures',
        'targetStructureClass': '/fleurOutput/programVersion/targetStructureClass',
        'type': '/fleurOutput/programVersion/precision',
        'unitCell': '/fleurOutput/numericalParameters/volumes',
        'user': '/fleurOutput/programVersion/compilationInfo',
        'weightScale': '/fleurOutput/numericalParameters/kPointList',
        'z1': '/fleurOutput/numericalParameters/volumes'
    },
    'unique_path_attribs': {
        'date':
        ['/fleurOutput/programVersion/compilationInfo', '/fleurOutput/startDateAndTime', '/fleurOutput/endDateAndTime'],
        'time': ['/fleurOutput/startDateAndTime', '/fleurOutput/endDateAndTime'],
        'version': ['/fleurOutput/programVersion', '/fleurOutput/programVersion/gitInfo'],
        'zone': ['/fleurOutput/startDateAndTime', '/fleurOutput/endDateAndTime']
    }
}
