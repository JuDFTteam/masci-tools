# -*- coding: utf-8 -*-
"""
This file contains information parsed from the FleurOutputSchema.xsd
for version 0.34

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
from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict
__out_version__ = '0.34'
schema_dict = {
    '_basic_types': {
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
        'FleurOutputVersionType': {
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
    '_input_basic_types': {
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
        'calculationtype': ['string'],
        'angles': ['int'],
        'qpoints': ['int'],
        'units': ['string'],
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
        'h_so': ['float'],
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
        'sigma_x': ['float'],
        'sigma_y': ['float'],
        'sigma_z': ['float'],
        'delta': ['float'],
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
    'fleurInput',
    'iteration_other_attribs':
    CaseInsensitiveDict({
        'delta': ['./onSiteExchangeSplitting/excSplit/@Delta'],
        'f_x': ['./totalForcesOnRepresentativeAtoms/forceTotal/@F_x'],
        'f_y': ['./totalForcesOnRepresentativeAtoms/forceTotal/@F_y'],
        'f_z': ['./totalForcesOnRepresentativeAtoms/forceTotal/@F_z'],
        'h_so': ['./Forcetheorem_DMI/allAtoms/@H_so', './Forcetheorem_DMI/singleAtom/@H_so'],
        'j': ['./coreStates/state/@j', './ldaUDensityMatrix/densityMatrixFor/@J'],
        'no': ['./Forcetheorem_Loop/@No'],
        'u': ['./ldaUDensityMatrix/densityMatrixFor/@U'],
        'atomtype': [
            './Forcetheorem_DMI/allAtoms/@atomType', './Forcetheorem_DMI/singleAtom/@atomType',
            './allElectronCharges/mtCharges/mtCharge/@atomType', './allElectronCharges/mtCharges/mtJcharge/@atomType',
            './coreStates/@atomType', './energyParameters/atomicEP/@atomType',
            './energyParameters/heAtomicEP/@atomType', './energyParameters/heloAtomicEP/@atomType',
            './energyParameters/loAtomicEP/@atomType', './ldaUDensityMatrix/densityMatrixFor/@atomType',
            './magneticMomentsInMTSpheres/magneticMoment/@atomType', './noncollinearTorgue/torgue/@atomType',
            './onSiteExchangeSplitting/excSplit/@atomType',
            './orbitalMagneticMomentsInMTSpheres/orbMagMoment/@atomType', './spinorbitTorgue/torgue/@atomType',
            './totalEnergy/atomTypeDependentContributions/@atomType',
            './totalForcesOnRepresentativeAtoms/forceTotal/@atomType', './valenceDensity/mtCharges/mtCharge/@atomType',
            './valenceDensity/mtCharges/mtJcharge/@atomType'
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
        'calculationtype': ['./Forcetheorem_Loop/@calculationType'],
        'comment': ['./totalEnergy/@comment'],
        'd': [
            './allElectronCharges/mtCharges/mtCharge/@d', './allElectronCharges/mtCharges/mtJcharge/highJ/@d',
            './allElectronCharges/mtCharges/mtJcharge/lowJ/@d', './valenceDensity/mtCharges/mtCharge/@d',
            './valenceDensity/mtCharges/mtJcharge/highJ/@d', './valenceDensity/mtCharges/mtJcharge/lowJ/@d'
        ],
        'distance': [
            './densityConvergence/chargeDensity/@distance', './densityConvergence/overallChargeDensity/@distance',
            './densityConvergence/spinDensity/@distance', './ldaUDensityMatrixConvergence/distance/@distance'
        ],
        'eigvalsum': ['./coreStates/@eigValSum'],
        'energy': ['./coreStates/state/@energy', './rdmft/@energy', './rdmft/occupations/state/@energy'],
        'ev-sum': [
            './Forcetheorem_DMI/Entry/@ev-sum', './Forcetheorem_JIJ/Config/@ev-sum', './Forcetheorem_MAE/Angle/@ev-sum',
            './Forcetheorem_SSDISP/Entry/@ev-sum'
        ],
        'f': [
            './allElectronCharges/mtCharges/mtCharge/@f', './allElectronCharges/mtCharges/mtJcharge/highJ/@f',
            './allElectronCharges/mtCharges/mtJcharge/lowJ/@f', './valenceDensity/mtCharges/mtCharge/@f',
            './valenceDensity/mtCharges/mtJcharge/highJ/@f', './valenceDensity/mtCharges/mtJcharge/lowJ/@f'
        ],
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
        'l':
        ['./coreStates/state/@l', './ldaUDensityMatrix/densityMatrixFor/@l', './onSiteExchangeSplitting/excSplit/@l'],
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
        'p': [
            './allElectronCharges/mtCharges/mtCharge/@p', './allElectronCharges/mtCharges/mtJcharge/highJ/@p',
            './allElectronCharges/mtCharges/mtJcharge/lowJ/@p', './valenceDensity/mtCharges/mtCharge/@p',
            './valenceDensity/mtCharges/mtJcharge/highJ/@p', './valenceDensity/mtCharges/mtJcharge/lowJ/@p'
        ],
        'phase': ['./Forcetheorem_JIJ/Config/@phase'],
        'phi': [
            './Forcetheorem_DMI/Entry/@phi', './Forcetheorem_DMI/allAtoms/@phi', './Forcetheorem_DMI/singleAtom/@phi',
            './Forcetheorem_MAE/Angle/@phi'
        ],
        'q': [
            './Forcetheorem_DMI/Entry/@q', './Forcetheorem_DMI/allAtoms/@q', './Forcetheorem_DMI/singleAtom/@q',
            './Forcetheorem_JIJ/Config/@q', './Forcetheorem_SSDISP/Entry/@q'
        ],
        's': ['./allElectronCharges/mtCharges/mtCharge/@s', './valenceDensity/mtCharges/mtCharge/@s'],
        'sigma_x': ['./noncollinearTorgue/torgue/@sigma_x', './spinorbitTorgue/torgue/@sigma_x'],
        'sigma_y': ['./noncollinearTorgue/torgue/@sigma_y', './spinorbitTorgue/torgue/@sigma_y'],
        'sigma_z': ['./noncollinearTorgue/torgue/@sigma_z', './spinorbitTorgue/torgue/@sigma_z'],
        'spin': [
            './allElectronCharges/fixedCharges/spinDependentCharge/@spin', './allElectronCharges/mtCharges/@spin',
            './allElectronCharges/spinDependentCharge/@spin', './coreStates/@spin',
            './densityConvergence/chargeDensity/@spin', './densityConvergence/overallChargeDensity/@spin',
            './densityConvergence/spinDensity/@spin', './eigenvalues/eigenvaluesAt/@spin',
            './energyParameters/atomicEP/@spin', './energyParameters/heAtomicEP/@spin',
            './energyParameters/heloAtomicEP/@spin', './energyParameters/loAtomicEP/@spin',
            './energyParameters/vacuumEP/@spin', './ldaUDensityMatrix/densityMatrixFor/@spin',
            './ldaUDensityMatrixConvergence/distance/@spin', './rdmft/occupations/@spin',
            './valenceDensity/fixedCharges/spinDependentCharge/@spin', './valenceDensity/mtCharges/@spin',
            './valenceDensity/spinDependentCharge/@spin'
        ],
        'spindowncharge': [
            './magneticMomentsInMTSpheres/magneticMoment/@spinDownCharge',
            './orbitalMagneticMomentsInMTSpheres/orbMagMoment/@spinDownCharge'
        ],
        'spinupcharge': [
            './magneticMomentsInMTSpheres/magneticMoment/@spinUpCharge',
            './orbitalMagneticMomentsInMTSpheres/orbMagMoment/@spinUpCharge'
        ],
        'theta': [
            './Forcetheorem_DMI/Entry/@theta', './Forcetheorem_DMI/allAtoms/@theta',
            './Forcetheorem_DMI/singleAtom/@theta', './Forcetheorem_MAE/Angle/@theta'
        ],
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
            './magneticMomentsInMTSpheres/@units', './noncollinearTorgue/torgue/@units',
            './onSiteExchangeSplitting/excSplit/@units', './orbitalMagneticMomentsInMTSpheres/@units',
            './spinorbitTorgue/torgue/@units', './sumValenceSingleParticleEnergies/@units', './timing/@units',
            './timing/timer/@units', './totalEnergy/@units', './totalEnergy/FockExchangeEnergyCore/@units',
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
            'attribs': ['value', 'units'],
            'optional': [],
            'optional_attribs': ['units'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        './Forcetheorem_DMI': {
            'attribs': ['Angles', 'qpoints', 'units'],
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
            'attribs': ['Configs', 'units'],
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
            'attribs': ['No', 'calculationType'],
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
            'attribs': ['Angles', 'units'],
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
            'attribs': ['qvectors', 'units'],
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
                'densityCoulombPotentialIntegral', 'densityEffectivePotentialIntegral', 'chargeDenXCDenIntegral',
                'FockExchangeEnergyValence', 'FockExchangeEnergyCore', 'dftUCorrection', 'tkbTimesEntropy',
                'freeEnergy', 'extrapolationTo0K'
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
    'iteration_tag_paths':
    CaseInsensitiveDict({
        'angle':
        './Forcetheorem_MAE/Angle',
        'config':
        './Forcetheorem_JIJ/Config',
        'error': [],
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
        'allatoms':
        './Forcetheorem_DMI/allAtoms',
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
        'distance':
        './ldaUDensityMatrixConvergence/distance',
        'eigenvalues':
        './eigenvalues',
        'eigenvaluesat':
        './eigenvalues/eigenvaluesAt',
        'electronnucleiinteractiondifferentmts':
        './totalEnergy/atomTypeDependentContributions/electronNucleiInteractionDifferentMTs',
        'enddateandtime': [],
        'energyparameters':
        './energyParameters',
        'excsplit':
        './onSiteExchangeSplitting/excSplit',
        'extrapolationto0k':
        './totalEnergy/extrapolationTo0K',
        'fixedcharges': ['./allElectronCharges/fixedCharges', './valenceDensity/fixedCharges'],
        'fleurinput': [],
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
        'highj': ['./allElectronCharges/mtCharges/mtJcharge/highJ', './valenceDensity/mtCharges/mtJcharge/highJ'],
        'iteration': [],
        'kpoint': [],
        'kpointlist': [],
        'ldaudensitymatrix':
        './ldaUDensityMatrix',
        'ldaudensitymatrixconvergence':
        './ldaUDensityMatrixConvergence',
        'loatomicep':
        './energyParameters/loAtomicEP',
        'lowj': ['./allElectronCharges/mtCharges/mtJcharge/lowJ', './valenceDensity/mtCharges/mtJcharge/lowJ'],
        'magneticmoment':
        './magneticMomentsInMTSpheres/magneticMoment',
        'magneticmomentsinmtspheres':
        './magneticMomentsInMTSpheres',
        'mem': [],
        'mpi': [],
        'mtcharge': ['./allElectronCharges/mtCharges/mtCharge', './valenceDensity/mtCharges/mtCharge'],
        'mtcharges': ['./allElectronCharges/mtCharges', './valenceDensity/mtCharges'],
        'mtjcharge': ['./allElectronCharges/mtCharges/mtJcharge', './valenceDensity/mtCharges/mtJcharge'],
        'mtvolume': [],
        'noncollineartorgue':
        './noncollinearTorgue',
        'numericalparameters': [],
        'occupations':
        './rdmft/occupations',
        'onsiteexchangesplitting':
        './onSiteExchangeSplitting',
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
        'singleatom':
        './Forcetheorem_DMI/singleAtom',
        'spindensity':
        './densityConvergence/spinDensity',
        'spindependentcharge': [
            './allElectronCharges/fixedCharges/spinDependentCharge', './allElectronCharges/spinDependentCharge',
            './valenceDensity/fixedCharges/spinDependentCharge', './valenceDensity/spinDependentCharge'
        ],
        'spinorbittorgue':
        './spinorbitTorgue',
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
        'torgue': ['./noncollinearTorgue/torgue', './spinorbitTorgue/torgue'],
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
    CaseInsensitiveDict({
        'angles': ['./Forcetheorem_DMI/@Angles', './Forcetheorem_MAE/@Angles'],
        'units': [
            './Forcetheorem_DMI/@units', './Forcetheorem_JIJ/@units', './Forcetheorem_MAE/@units',
            './Forcetheorem_SSDISP/@units'
        ]
    }),
    'omitt_contained_tags': [
        'scfLoop', 'eigenvalues', 'onSiteExchangeSplitting', 'noncollinearTorgue', 'spinorbitTorgue',
        'ldaUDensityMatrix', 'ldaUDensityMatrixConvergence'
    ],
    'other_attribs':
    CaseInsensitiveDict({
        'atomtype': ['/fleurOutput/numericalParameters/volumes/mtVolume/@atomType'],
        'mtradius': ['/fleurOutput/numericalParameters/volumes/mtVolume/@mtRadius'],
        'mtvolume': ['/fleurOutput/numericalParameters/volumes/mtVolume/@mtVolume'],
        'kpoint': ['/fleurOutput/numericalParameters/kPointList/kPoint']
    }),
    'out_version':
    '0.34',
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
            'simple': ['startDateAndTime', 'ERROR', 'endDateAndTime'],
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
    'tag_paths':
    CaseInsensitiveDict({
        'angle': [],
        'config': [],
        'error': '/fleurOutput/ERROR',
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
        'allatoms': [],
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
        'distance': [],
        'eigenvalues': [],
        'eigenvaluesat': [],
        'electronnucleiinteractiondifferentmts': [],
        'enddateandtime': '/fleurOutput/endDateAndTime',
        'energyparameters': [],
        'excsplit': [],
        'extrapolationto0k': [],
        'fixedcharges': [],
        'fleurinput': '/fleurOutput/fleurInput',
        'fleuroutput': '/fleurOutput',
        'forcetotal': [],
        'freeenergy': [],
        'gitinfo': '/fleurOutput/programVersion/gitInfo',
        'heatomicep': [],
        'heloatomicep': [],
        'highj': [],
        'iteration': '/fleurOutput/scfLoop/iteration',
        'kpoint': '/fleurOutput/numericalParameters/kPointList/kPoint',
        'kpointlist': '/fleurOutput/numericalParameters/kPointList',
        'ldaudensitymatrix': [],
        'ldaudensitymatrixconvergence': [],
        'loatomicep': [],
        'lowj': [],
        'magneticmoment': [],
        'magneticmomentsinmtspheres': [],
        'mem': '/fleurOutput/parallelSetup/mem',
        'mpi': '/fleurOutput/parallelSetup/mpi',
        'mtcharge': [],
        'mtcharges': [],
        'mtjcharge': [],
        'mtvolume': '/fleurOutput/numericalParameters/volumes/mtVolume',
        'noncollineartorgue': [],
        'numericalparameters': '/fleurOutput/numericalParameters',
        'occupations': [],
        'onsiteexchangesplitting': [],
        'openmp': '/fleurOutput/parallelSetup/openMP',
        'orbmagmoment': [],
        'orbitalmagneticmomentsinmtspheres': [],
        'overallchargedensity': [],
        'parallelsetup': '/fleurOutput/parallelSetup',
        'precision': '/fleurOutput/programVersion/precision',
        'programversion': '/fleurOutput/programVersion',
        'rdmft': [],
        'scfloop': '/fleurOutput/scfLoop',
        'singleatom': [],
        'spindensity': [],
        'spindependentcharge': [],
        'spinorbittorgue': [],
        'startdateandtime': '/fleurOutput/startDateAndTime',
        'state': [],
        'sumofeigenvalues': [],
        'sumvalencesingleparticleenergies': [],
        'targetcomputerarchitectures': '/fleurOutput/programVersion/targetComputerArchitectures',
        'targetstructureclass': '/fleurOutput/programVersion/targetStructureClass',
        'timer': [],
        'timing': [],
        'tkbtimesentropy': [],
        'torgue': [],
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
        'message': '/fleurOutput/ERROR/@Message',
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
