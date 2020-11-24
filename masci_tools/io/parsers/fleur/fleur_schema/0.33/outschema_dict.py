# -*- coding: utf-8 -*-
__out_version__ = '0.33'
schema_dict = {
    'attrib_types': {
        'Delta': ['float'],
        'F_x': ['float'],
        'F_y': ['float'],
        'F_z': ['float'],
        'J': ['float'],
        'Message': ['string'],
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
        'f': ['float'],
        'flag': ['string'],
        'fleurOutputVersion': ['string'],
        'host': ['string'],
        'ikpt': ['int'],
        'interstitial': ['float'],
        'j': ['float'],
        'jmtd': ['int'],
        'k_x': ['float'],
        'k_y': ['float'],
        'k_z': ['float'],
        'kinEnergy': ['float'],
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
        'omegaTilda': ['float'],
        'ompThreads': ['string'],
        'overallNumber': ['int'],
        'p': ['float'],
        's': ['float'],
        'spin': ['int'],
        'spinDownCharge': ['float'],
        'spinUpCharge': ['float'],
        'surfaceArea': ['float'],
        'time': ['string'],
        'total': ['float'],
        'type': ['string'],
        'uIndex': ['int'],
        'unit': ['string'],
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
        'TriaType': {
            'base_types': ['int'],
            'length': 3
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
    'group_tags': ['iteration'],
    'iteration_attrib_paths': {
        'Delta':
        '/onSiteExchangeSplitting/excSplit',
        'F_x':
        '/totalForcesOnRepresentativeAtoms/forceTotal',
        'F_y':
        '/totalForcesOnRepresentativeAtoms/forceTotal',
        'F_z':
        '/totalForcesOnRepresentativeAtoms/forceTotal',
        'J':
        '/ldaUDensityMatrix/densityMatrixFor',
        'U':
        '/ldaUDensityMatrix/densityMatrixFor',
        'atomType': [
            '/energyParameters/atomicEP', '/energyParameters/heAtomicEP', '/energyParameters/loAtomicEP',
            '/energyParameters/heloAtomicEP', '/valenceDensity/mtCharges/mtCharge',
            '/allElectronCharges/mtCharges/mtCharge', '/valenceDensity/mtCharges/mtJcharge',
            '/allElectronCharges/mtCharges/mtJcharge', '/coreStates', '/magneticMomentsInMTSpheres/magneticMoment',
            '/orbitalMagneticMomentsInMTSpheres/orbMagMoment', '/totalForcesOnRepresentativeAtoms/forceTotal',
            '/onSiteExchangeSplitting/excSplit', '/ldaUDensityMatrix/densityMatrixFor',
            '/totalEnergy/atomTypeDependentContributions'
        ],
        'atomicNumber':
        '/coreStates',
        'branch': [
            '/energyParameters/atomicEP', '/energyParameters/heAtomicEP', '/energyParameters/loAtomicEP',
            '/energyParameters/heloAtomicEP'
        ],
        'branchHighest': [
            '/energyParameters/atomicEP', '/energyParameters/heAtomicEP', '/energyParameters/loAtomicEP',
            '/energyParameters/heloAtomicEP'
        ],
        'branchLowest': [
            '/energyParameters/atomicEP', '/energyParameters/heAtomicEP', '/energyParameters/loAtomicEP',
            '/energyParameters/heloAtomicEP'
        ],
        'comment':
        '/totalEnergy',
        'd': [
            '/valenceDensity/mtCharges/mtCharge', '/allElectronCharges/mtCharges/mtCharge',
            '/valenceDensity/mtCharges/mtJcharge/lowJ', '/allElectronCharges/mtCharges/mtJcharge/lowJ',
            '/valenceDensity/mtCharges/mtJcharge/highJ', '/allElectronCharges/mtCharges/mtJcharge/highJ'
        ],
        'distance': [
            '/ldaUDensityMatrixConvergence/distance', '/densityConvergence/chargeDensity',
            '/densityConvergence/overallChargeDensity', '/densityConvergence/spinDensity'
        ],
        'eigValSum':
        '/coreStates',
        'energy':
        '/coreStates/state',
        'f': [
            '/valenceDensity/mtCharges/mtCharge', '/allElectronCharges/mtCharges/mtCharge',
            '/valenceDensity/mtCharges/mtJcharge/lowJ', '/allElectronCharges/mtCharges/mtJcharge/lowJ',
            '/valenceDensity/mtCharges/mtJcharge/highJ', '/allElectronCharges/mtCharges/mtJcharge/highJ'
        ],
        'ikpt':
        '/eigenvalues/eigenvaluesAt',
        'interstitial': [
            '/valenceDensity/spinDependentCharge', '/allElectronCharges/spinDependentCharge',
            '/valenceDensity/fixedCharges/spinDependentCharge', '/allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'j':
        '/coreStates/state',
        'k_x':
        '/eigenvalues/eigenvaluesAt',
        'k_y':
        '/eigenvalues/eigenvaluesAt',
        'k_z':
        '/eigenvalues/eigenvaluesAt',
        'kinEnergy':
        '/coreStates',
        'l': ['/coreStates/state', '/onSiteExchangeSplitting/excSplit', '/ldaUDensityMatrix/densityMatrixFor'],
        'lostElectrons':
        '/coreStates',
        'moment': ['/magneticMomentsInMTSpheres/magneticMoment', '/orbitalMagneticMomentsInMTSpheres/orbMagMoment'],
        'mtSpheres': [
            '/valenceDensity/spinDependentCharge', '/allElectronCharges/spinDependentCharge',
            '/valenceDensity/fixedCharges/spinDependentCharge', '/allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'n':
        '/coreStates/state',
        'name':
        '/timing/timer',
        'p': [
            '/valenceDensity/mtCharges/mtCharge', '/allElectronCharges/mtCharges/mtCharge',
            '/valenceDensity/mtCharges/mtJcharge/lowJ', '/allElectronCharges/mtCharges/mtJcharge/lowJ',
            '/valenceDensity/mtCharges/mtJcharge/highJ', '/allElectronCharges/mtCharges/mtJcharge/highJ'
        ],
        's': ['/valenceDensity/mtCharges/mtCharge', '/allElectronCharges/mtCharges/mtCharge'],
        'spin': [
            '/energyParameters/atomicEP', '/energyParameters/heAtomicEP', '/energyParameters/loAtomicEP',
            '/energyParameters/heloAtomicEP', '/energyParameters/vacuumEP', '/eigenvalues/eigenvaluesAt',
            '/valenceDensity/mtCharges', '/allElectronCharges/mtCharges', '/valenceDensity/spinDependentCharge',
            '/allElectronCharges/spinDependentCharge', '/valenceDensity/fixedCharges/spinDependentCharge',
            '/allElectronCharges/fixedCharges/spinDependentCharge', '/coreStates',
            '/ldaUDensityMatrix/densityMatrixFor', '/ldaUDensityMatrixConvergence/distance',
            '/densityConvergence/chargeDensity', '/densityConvergence/overallChargeDensity',
            '/densityConvergence/spinDensity'
        ],
        'spinDownCharge':
        ['/magneticMomentsInMTSpheres/magneticMoment', '/orbitalMagneticMomentsInMTSpheres/orbMagMoment'],
        'spinUpCharge':
        ['/magneticMomentsInMTSpheres/magneticMoment', '/orbitalMagneticMomentsInMTSpheres/orbMagMoment'],
        'total': [
            '/valenceDensity/mtCharges/mtCharge', '/allElectronCharges/mtCharges/mtCharge',
            '/valenceDensity/spinDependentCharge', '/allElectronCharges/spinDependentCharge',
            '/valenceDensity/fixedCharges/spinDependentCharge', '/allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'uIndex':
        '/ldaUDensityMatrix/densityMatrixFor',
        'unit':
        '/onSiteExchangeSplitting/excSplit',
        'units': [
            '/energyParameters', '/bandgap', '/sumValenceSingleParticleEnergies', '/FermiEnergy',
            '/valenceDensity/totalCharge', '/allElectronCharges/totalCharge',
            '/valenceDensity/fixedCharges/totalCharge', '/allElectronCharges/fixedCharges/totalCharge',
            '/totalEnergy/densityCoulombPotentialIntegral', '/totalEnergy/densityEffectivePotentialIntegral',
            '/totalEnergy/chargeDenXCDenIntegral', '/totalEnergy/FockExchangeEnergyValence',
            '/totalEnergy/FockExchangeEnergyCore', '/totalEnergy/dftUCorrection', '/totalEnergy/tkbTimesEntropy',
            '/totalEnergy/freeEnergy', '/totalEnergy/extrapolationTo0K', '/totalEnergy/sumOfEigenvalues/coreElectrons',
            '/totalEnergy/sumOfEigenvalues/valenceElectrons',
            '/totalEnergy/atomTypeDependentContributions/electronNucleiInteractionDifferentMTs',
            '/totalEnergy/atomTypeDependentContributions/MadelungTerm', '/magneticMomentsInMTSpheres',
            '/orbitalMagneticMomentsInMTSpheres', '/totalForcesOnRepresentativeAtoms',
            '/totalForcesOnRepresentativeAtoms/forceTotal', '/totalEnergy', '/totalEnergy/sumOfEigenvalues',
            '/densityConvergence', '/densityConvergence/chargeDensity', '/densityConvergence/overallChargeDensity',
            '/densityConvergence/spinDensity', '/timing', '/timing/timer'
        ],
        'vacuum':
        '/energyParameters/vacuumEP',
        'vacuum1': [
            '/valenceDensity/spinDependentCharge', '/allElectronCharges/spinDependentCharge',
            '/valenceDensity/fixedCharges/spinDependentCharge', '/allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'vacuum2': [
            '/valenceDensity/spinDependentCharge', '/allElectronCharges/spinDependentCharge',
            '/valenceDensity/fixedCharges/spinDependentCharge', '/allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'value': [
            '/energyParameters/atomicEP', '/energyParameters/heAtomicEP', '/energyParameters/loAtomicEP',
            '/energyParameters/heloAtomicEP', '/energyParameters/vacuumEP', '/bandgap',
            '/sumValenceSingleParticleEnergies', '/FermiEnergy', '/valenceDensity/totalCharge',
            '/allElectronCharges/totalCharge', '/valenceDensity/fixedCharges/totalCharge',
            '/allElectronCharges/fixedCharges/totalCharge', '/totalEnergy/densityCoulombPotentialIntegral',
            '/totalEnergy/densityEffectivePotentialIntegral', '/totalEnergy/chargeDenXCDenIntegral',
            '/totalEnergy/FockExchangeEnergyValence', '/totalEnergy/FockExchangeEnergyCore',
            '/totalEnergy/dftUCorrection', '/totalEnergy/tkbTimesEntropy', '/totalEnergy/freeEnergy',
            '/totalEnergy/extrapolationTo0K', '/totalEnergy/sumOfEigenvalues/coreElectrons',
            '/totalEnergy/sumOfEigenvalues/valenceElectrons',
            '/totalEnergy/atomTypeDependentContributions/electronNucleiInteractionDifferentMTs',
            '/totalEnergy/atomTypeDependentContributions/MadelungTerm', '/totalEnergy', '/totalEnergy/sumOfEigenvalues',
            '/timing/timer'
        ],
        'vzIR':
        '/energyParameters/vacuumEP',
        'vzInf':
        '/energyParameters/vacuumEP',
        'weight':
        '/coreStates/state',
        'x':
        '/totalForcesOnRepresentativeAtoms/forceTotal',
        'y':
        '/totalForcesOnRepresentativeAtoms/forceTotal',
        'z':
        '/totalForcesOnRepresentativeAtoms/forceTotal'
    },
    'iteration_paths': {
        'FermiEnergy':
        '/FermiEnergy',
        'FockExchangeEnergyCore':
        '/totalEnergy/FockExchangeEnergyCore',
        'FockExchangeEnergyValence':
        '/totalEnergy/FockExchangeEnergyValence',
        'MadelungTerm':
        '/totalEnergy/atomTypeDependentContributions/MadelungTerm',
        'allElectronCharges':
        '/allElectronCharges',
        'atomTypeDependentContributions':
        '/totalEnergy/atomTypeDependentContributions',
        'atomicEP':
        '/energyParameters/atomicEP',
        'bandgap':
        '/bandgap',
        'chargeDenXCDenIntegral':
        '/totalEnergy/chargeDenXCDenIntegral',
        'chargeDensity':
        '/densityConvergence/chargeDensity',
        'compositeTimer':
        '/timing/compositeTimer',
        'coreElectrons':
        '/totalEnergy/sumOfEigenvalues/coreElectrons',
        'coreStates':
        '/coreStates',
        'densityConvergence':
        '/densityConvergence',
        'densityCoulombPotentialIntegral':
        '/totalEnergy/densityCoulombPotentialIntegral',
        'densityEffectivePotentialIntegral':
        '/totalEnergy/densityEffectivePotentialIntegral',
        'densityMatrixFor':
        '/ldaUDensityMatrix/densityMatrixFor',
        'dftUCorrection':
        '/totalEnergy/dftUCorrection',
        'distance':
        '/ldaUDensityMatrixConvergence/distance',
        'eigenvalues':
        '/eigenvalues',
        'eigenvaluesAt':
        '/eigenvalues/eigenvaluesAt',
        'electronNucleiInteractionDifferentMTs':
        '/totalEnergy/atomTypeDependentContributions/electronNucleiInteractionDifferentMTs',
        'energyParameters':
        '/energyParameters',
        'excSplit':
        '/onSiteExchangeSplitting/excSplit',
        'extrapolationTo0K':
        '/totalEnergy/extrapolationTo0K',
        'fixedCharges': ['/valenceDensity/fixedCharges', '/allElectronCharges/fixedCharges'],
        'forceTotal':
        '/totalForcesOnRepresentativeAtoms/forceTotal',
        'freeEnergy':
        '/totalEnergy/freeEnergy',
        'heAtomicEP':
        '/energyParameters/heAtomicEP',
        'heloAtomicEP':
        '/energyParameters/heloAtomicEP',
        'highJ': ['/valenceDensity/mtCharges/mtJcharge/highJ', '/allElectronCharges/mtCharges/mtJcharge/highJ'],
        'ldaUDensityMatrix':
        '/ldaUDensityMatrix',
        'ldaUDensityMatrixConvergence':
        '/ldaUDensityMatrixConvergence',
        'loAtomicEP':
        '/energyParameters/loAtomicEP',
        'lowJ': ['/valenceDensity/mtCharges/mtJcharge/lowJ', '/allElectronCharges/mtCharges/mtJcharge/lowJ'],
        'magneticMoment':
        '/magneticMomentsInMTSpheres/magneticMoment',
        'magneticMomentsInMTSpheres':
        '/magneticMomentsInMTSpheres',
        'mtCharge': ['/valenceDensity/mtCharges/mtCharge', '/allElectronCharges/mtCharges/mtCharge'],
        'mtCharges': ['/valenceDensity/mtCharges', '/allElectronCharges/mtCharges'],
        'mtJcharge': ['/valenceDensity/mtCharges/mtJcharge', '/allElectronCharges/mtCharges/mtJcharge'],
        'onSiteExchangeSplitting':
        '/onSiteExchangeSplitting',
        'orbMagMoment':
        '/orbitalMagneticMomentsInMTSpheres/orbMagMoment',
        'orbitalMagneticMomentsInMTSpheres':
        '/orbitalMagneticMomentsInMTSpheres',
        'overallChargeDensity':
        '/densityConvergence/overallChargeDensity',
        'spinDensity':
        '/densityConvergence/spinDensity',
        'spinDependentCharge': [
            '/valenceDensity/spinDependentCharge', '/allElectronCharges/spinDependentCharge',
            '/valenceDensity/fixedCharges/spinDependentCharge', '/allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'state':
        '/coreStates/state',
        'sumOfEigenvalues':
        '/totalEnergy/sumOfEigenvalues',
        'sumValenceSingleParticleEnergies':
        '/sumValenceSingleParticleEnergies',
        'timer':
        '/timing/timer',
        'timing':
        '/timing',
        'tkbTimesEntropy':
        '/totalEnergy/tkbTimesEntropy',
        'totalCharge': [
            '/valenceDensity/totalCharge', '/allElectronCharges/totalCharge',
            '/valenceDensity/fixedCharges/totalCharge', '/allElectronCharges/fixedCharges/totalCharge'
        ],
        'totalEnergy':
        '/totalEnergy',
        'totalForcesOnRepresentativeAtoms':
        '/totalForcesOnRepresentativeAtoms',
        'vacuumEP':
        '/energyParameters/vacuumEP',
        'valenceDensity':
        '/valenceDensity',
        'valenceElectrons':
        '/totalEnergy/sumOfEigenvalues/valenceElectrons'
    },
    'other_attribs': {
        'Delta': ['/fleurOutput/scfLoop/iteration/onSiteExchangeSplitting/excSplit'],
        'F_x': ['/fleurOutput/scfLoop/iteration/totalForcesOnRepresentativeAtoms/forceTotal'],
        'F_y': ['/fleurOutput/scfLoop/iteration/totalForcesOnRepresentativeAtoms/forceTotal'],
        'F_z': ['/fleurOutput/scfLoop/iteration/totalForcesOnRepresentativeAtoms/forceTotal'],
        'J': ['/fleurOutput/scfLoop/iteration/ldaUDensityMatrix/densityMatrixFor'],
        'U': ['/fleurOutput/scfLoop/iteration/ldaUDensityMatrix/densityMatrixFor'],
        'atomType': [
            '/fleurOutput/numericalParameters/volumes/mtVolume',
            '/fleurOutput/scfLoop/iteration/energyParameters/atomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/heAtomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/loAtomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/heloAtomicEP',
            '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtJcharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtJcharge',
            '/fleurOutput/scfLoop/iteration/coreStates',
            '/fleurOutput/scfLoop/iteration/magneticMomentsInMTSpheres/magneticMoment',
            '/fleurOutput/scfLoop/iteration/orbitalMagneticMomentsInMTSpheres/orbMagMoment',
            '/fleurOutput/scfLoop/iteration/totalForcesOnRepresentativeAtoms/forceTotal',
            '/fleurOutput/scfLoop/iteration/onSiteExchangeSplitting/excSplit',
            '/fleurOutput/scfLoop/iteration/ldaUDensityMatrix/densityMatrixFor',
            '/fleurOutput/scfLoop/iteration/totalEnergy/atomTypeDependentContributions'
        ],
        'atomicNumber': ['/fleurOutput/scfLoop/iteration/coreStates'],
        'branch': [
            '/fleurOutput/scfLoop/iteration/energyParameters/atomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/heAtomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/loAtomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/heloAtomicEP'
        ],
        'branchHighest': [
            '/fleurOutput/scfLoop/iteration/energyParameters/atomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/heAtomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/loAtomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/heloAtomicEP'
        ],
        'branchLowest': [
            '/fleurOutput/scfLoop/iteration/energyParameters/atomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/heAtomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/loAtomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/heloAtomicEP'
        ],
        'comment': ['/fleurOutput/scfLoop/iteration/totalEnergy'],
        'd': [
            '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtJcharge/lowJ',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtJcharge/lowJ',
            '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtJcharge/highJ',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtJcharge/highJ'
        ],
        'densityMatrixFor': ['/fleurOutput/scfLoop/iteration/ldaUDensityMatrix/densityMatrixFor'],
        'distance': [
            '/fleurOutput/scfLoop/iteration/ldaUDensityMatrixConvergence/distance',
            '/fleurOutput/scfLoop/iteration/densityConvergence/chargeDensity',
            '/fleurOutput/scfLoop/iteration/densityConvergence/overallChargeDensity',
            '/fleurOutput/scfLoop/iteration/densityConvergence/spinDensity'
        ],
        'eigValSum': ['/fleurOutput/scfLoop/iteration/coreStates'],
        'eigenvaluesAt': ['/fleurOutput/scfLoop/iteration/eigenvalues/eigenvaluesAt'],
        'energy': ['/fleurOutput/scfLoop/iteration/coreStates/state'],
        'f': [
            '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtJcharge/lowJ',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtJcharge/lowJ',
            '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtJcharge/highJ',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtJcharge/highJ'
        ],
        'ikpt': ['/fleurOutput/scfLoop/iteration/eigenvalues/eigenvaluesAt'],
        'interstitial': [
            '/fleurOutput/scfLoop/iteration/valenceDensity/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/valenceDensity/fixedCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'j': ['/fleurOutput/scfLoop/iteration/coreStates/state'],
        'kPoint': ['/fleurOutput/numericalParameters/kPointList/kPoint'],
        'k_x': ['/fleurOutput/scfLoop/iteration/eigenvalues/eigenvaluesAt'],
        'k_y': ['/fleurOutput/scfLoop/iteration/eigenvalues/eigenvaluesAt'],
        'k_z': ['/fleurOutput/scfLoop/iteration/eigenvalues/eigenvaluesAt'],
        'kinEnergy': ['/fleurOutput/scfLoop/iteration/coreStates'],
        'l': [
            '/fleurOutput/scfLoop/iteration/coreStates/state',
            '/fleurOutput/scfLoop/iteration/onSiteExchangeSplitting/excSplit',
            '/fleurOutput/scfLoop/iteration/ldaUDensityMatrix/densityMatrixFor'
        ],
        'lostElectrons': ['/fleurOutput/scfLoop/iteration/coreStates'],
        'moment': [
            '/fleurOutput/scfLoop/iteration/magneticMomentsInMTSpheres/magneticMoment',
            '/fleurOutput/scfLoop/iteration/orbitalMagneticMomentsInMTSpheres/orbMagMoment'
        ],
        'mtRadius': ['/fleurOutput/numericalParameters/volumes/mtVolume'],
        'mtSpheres': [
            '/fleurOutput/scfLoop/iteration/valenceDensity/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/valenceDensity/fixedCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'mtVolume': ['/fleurOutput/numericalParameters/volumes/mtVolume'],
        'n': ['/fleurOutput/scfLoop/iteration/coreStates/state'],
        'name': ['/fleurOutput/scfLoop/iteration/timing/timer'],
        'numberForCurrentRun': ['/fleurOutput/scfLoop/iteration'],
        'overallNumber': ['/fleurOutput/scfLoop/iteration'],
        'p': [
            '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtJcharge/lowJ',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtJcharge/lowJ',
            '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtJcharge/highJ',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtJcharge/highJ'
        ],
        's': [
            '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtCharge'
        ],
        'spin': [
            '/fleurOutput/scfLoop/iteration/energyParameters/atomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/heAtomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/loAtomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/heloAtomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/vacuumEP',
            '/fleurOutput/scfLoop/iteration/eigenvalues/eigenvaluesAt',
            '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges',
            '/fleurOutput/scfLoop/iteration/valenceDensity/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/valenceDensity/fixedCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/fixedCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/coreStates',
            '/fleurOutput/scfLoop/iteration/ldaUDensityMatrix/densityMatrixFor',
            '/fleurOutput/scfLoop/iteration/ldaUDensityMatrixConvergence/distance',
            '/fleurOutput/scfLoop/iteration/densityConvergence/chargeDensity',
            '/fleurOutput/scfLoop/iteration/densityConvergence/overallChargeDensity',
            '/fleurOutput/scfLoop/iteration/densityConvergence/spinDensity'
        ],
        'spinDownCharge': [
            '/fleurOutput/scfLoop/iteration/magneticMomentsInMTSpheres/magneticMoment',
            '/fleurOutput/scfLoop/iteration/orbitalMagneticMomentsInMTSpheres/orbMagMoment'
        ],
        'spinUpCharge': [
            '/fleurOutput/scfLoop/iteration/magneticMomentsInMTSpheres/magneticMoment',
            '/fleurOutput/scfLoop/iteration/orbitalMagneticMomentsInMTSpheres/orbMagMoment'
        ],
        'total': [
            '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/iteration/valenceDensity/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/valenceDensity/fixedCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'uIndex': ['/fleurOutput/scfLoop/iteration/ldaUDensityMatrix/densityMatrixFor'],
        'unit': ['/fleurOutput/scfLoop/iteration/onSiteExchangeSplitting/excSplit'],
        'units': [
            '/fleurOutput/scfLoop/iteration/energyParameters', '/fleurOutput/scfLoop/iteration/bandgap',
            '/fleurOutput/scfLoop/iteration/sumValenceSingleParticleEnergies',
            '/fleurOutput/scfLoop/iteration/FermiEnergy', '/fleurOutput/scfLoop/iteration/valenceDensity/totalCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/totalCharge',
            '/fleurOutput/scfLoop/iteration/valenceDensity/fixedCharges/totalCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/fixedCharges/totalCharge',
            '/fleurOutput/scfLoop/iteration/totalEnergy/densityCoulombPotentialIntegral',
            '/fleurOutput/scfLoop/iteration/totalEnergy/densityEffectivePotentialIntegral',
            '/fleurOutput/scfLoop/iteration/totalEnergy/chargeDenXCDenIntegral',
            '/fleurOutput/scfLoop/iteration/totalEnergy/FockExchangeEnergyValence',
            '/fleurOutput/scfLoop/iteration/totalEnergy/FockExchangeEnergyCore',
            '/fleurOutput/scfLoop/iteration/totalEnergy/dftUCorrection',
            '/fleurOutput/scfLoop/iteration/totalEnergy/tkbTimesEntropy',
            '/fleurOutput/scfLoop/iteration/totalEnergy/freeEnergy',
            '/fleurOutput/scfLoop/iteration/totalEnergy/extrapolationTo0K',
            '/fleurOutput/scfLoop/iteration/totalEnergy/sumOfEigenvalues/coreElectrons',
            '/fleurOutput/scfLoop/iteration/totalEnergy/sumOfEigenvalues/valenceElectrons',
            '/fleurOutput/scfLoop/iteration/totalEnergy/atomTypeDependentContributions/electronNucleiInteractionDifferentMTs',
            '/fleurOutput/scfLoop/iteration/totalEnergy/atomTypeDependentContributions/MadelungTerm',
            '/fleurOutput/scfLoop/iteration/magneticMomentsInMTSpheres',
            '/fleurOutput/scfLoop/iteration/orbitalMagneticMomentsInMTSpheres',
            '/fleurOutput/scfLoop/iteration/totalForcesOnRepresentativeAtoms',
            '/fleurOutput/scfLoop/iteration/totalForcesOnRepresentativeAtoms/forceTotal',
            '/fleurOutput/scfLoop/iteration/totalEnergy', '/fleurOutput/scfLoop/iteration/totalEnergy/sumOfEigenvalues',
            '/fleurOutput/scfLoop/iteration/densityConvergence',
            '/fleurOutput/scfLoop/iteration/densityConvergence/chargeDensity',
            '/fleurOutput/scfLoop/iteration/densityConvergence/overallChargeDensity',
            '/fleurOutput/scfLoop/iteration/densityConvergence/spinDensity', '/fleurOutput/scfLoop/iteration/timing',
            '/fleurOutput/scfLoop/iteration/timing/timer'
        ],
        'vacuum': ['/fleurOutput/scfLoop/iteration/energyParameters/vacuumEP'],
        'vacuum1': [
            '/fleurOutput/scfLoop/iteration/valenceDensity/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/valenceDensity/fixedCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'vacuum2': [
            '/fleurOutput/scfLoop/iteration/valenceDensity/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/valenceDensity/fixedCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/fixedCharges/spinDependentCharge'
        ],
        'value': [
            '/fleurOutput/scfLoop/iteration/energyParameters/atomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/heAtomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/loAtomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/heloAtomicEP',
            '/fleurOutput/scfLoop/iteration/energyParameters/vacuumEP', '/fleurOutput/scfLoop/iteration/bandgap',
            '/fleurOutput/scfLoop/iteration/sumValenceSingleParticleEnergies',
            '/fleurOutput/scfLoop/iteration/FermiEnergy', '/fleurOutput/scfLoop/iteration/valenceDensity/totalCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/totalCharge',
            '/fleurOutput/scfLoop/iteration/valenceDensity/fixedCharges/totalCharge',
            '/fleurOutput/scfLoop/iteration/allElectronCharges/fixedCharges/totalCharge',
            '/fleurOutput/scfLoop/iteration/totalEnergy/densityCoulombPotentialIntegral',
            '/fleurOutput/scfLoop/iteration/totalEnergy/densityEffectivePotentialIntegral',
            '/fleurOutput/scfLoop/iteration/totalEnergy/chargeDenXCDenIntegral',
            '/fleurOutput/scfLoop/iteration/totalEnergy/FockExchangeEnergyValence',
            '/fleurOutput/scfLoop/iteration/totalEnergy/FockExchangeEnergyCore',
            '/fleurOutput/scfLoop/iteration/totalEnergy/dftUCorrection',
            '/fleurOutput/scfLoop/iteration/totalEnergy/tkbTimesEntropy',
            '/fleurOutput/scfLoop/iteration/totalEnergy/freeEnergy',
            '/fleurOutput/scfLoop/iteration/totalEnergy/extrapolationTo0K',
            '/fleurOutput/scfLoop/iteration/totalEnergy/sumOfEigenvalues/coreElectrons',
            '/fleurOutput/scfLoop/iteration/totalEnergy/sumOfEigenvalues/valenceElectrons',
            '/fleurOutput/scfLoop/iteration/totalEnergy/atomTypeDependentContributions/electronNucleiInteractionDifferentMTs',
            '/fleurOutput/scfLoop/iteration/totalEnergy/atomTypeDependentContributions/MadelungTerm',
            '/fleurOutput/scfLoop/iteration/totalEnergy', '/fleurOutput/scfLoop/iteration/totalEnergy/sumOfEigenvalues',
            '/fleurOutput/scfLoop/iteration/timing/timer'
        ],
        'vzIR': ['/fleurOutput/scfLoop/iteration/energyParameters/vacuumEP'],
        'vzInf': ['/fleurOutput/scfLoop/iteration/energyParameters/vacuumEP'],
        'weight': ['/fleurOutput/scfLoop/iteration/coreStates/state'],
        'x': ['/fleurOutput/scfLoop/iteration/totalForcesOnRepresentativeAtoms/forceTotal'],
        'y': ['/fleurOutput/scfLoop/iteration/totalForcesOnRepresentativeAtoms/forceTotal'],
        'z': ['/fleurOutput/scfLoop/iteration/totalForcesOnRepresentativeAtoms/forceTotal']
    },
    'settable_attribs': {
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
    'settable_contains_attribs': {
        'date':
        ['/fleurOutput/programVersion/compilationInfo', '/fleurOutput/startDateAndTime', '/fleurOutput/endDateAndTime'],
        'time': ['/fleurOutput/startDateAndTime', '/fleurOutput/endDateAndTime'],
        'version': ['/fleurOutput/programVersion', '/fleurOutput/programVersion/gitInfo'],
        'zone': ['/fleurOutput/startDateAndTime', '/fleurOutput/endDateAndTime']
    },
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
    'tags_info': {
        '/fleurOutput': {
            'attribs': ['fleurOutputVersion'],
            'optional': [
                'programVersion', 'parallelSetup', 'startDateAndTime', 'fleurInput', 'numericalParameters', 'scfLoop',
                'ERROR', 'endDateAndTime'
            ],
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
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/endDateAndTime': {
            'attribs': ['date', 'time', 'zone'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/numericalParameters': {
            'attribs': [],
            'optional': [],
            'order': ['atomsInCell', 'basis', 'density', 'bands', 'volumes', 'kPointList'],
            'several': [],
            'simple': ['atomsInCell', 'basis', 'density', 'bands'],
            'text': []
        },
        '/fleurOutput/numericalParameters/atomsInCell': {
            'attribs': ['nat', 'ntype', 'jmtd', 'n_u', 'n_hia'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/numericalParameters/bands': {
            'attribs': ['numbands'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/numericalParameters/basis': {
            'attribs': ['nvd', 'lmaxd', 'nlotot'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/numericalParameters/density': {
            'attribs': ['ng3', 'ng2'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/numericalParameters/kPointList': {
            'attribs': ['weightScale', 'count'],
            'optional': ['kPoint'],
            'order': ['kPoint'],
            'several': ['kPoint'],
            'simple': ['kPoint'],
            'text': ['kPoint']
        },
        '/fleurOutput/numericalParameters/volumes': {
            'attribs': ['unitCell', 'interstitial', 'omegaTilda', 'surfaceArea', 'z1'],
            'optional': ['mtVolume'],
            'order': ['mtVolume'],
            'several': ['mtVolume'],
            'simple': ['mtVolume'],
            'text': []
        },
        '/fleurOutput/numericalParameters/volumes/mtVolume': {
            'attribs': ['atomType', 'mtRadius', 'mtVolume'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/parallelSetup': {
            'attribs': [],
            'optional': ['openMP', 'mpi', 'mem'],
            'order': ['openMP', 'mpi', 'mem'],
            'several': [],
            'simple': ['openMP', 'mpi', 'mem'],
            'text': []
        },
        '/fleurOutput/parallelSetup/mem': {
            'attribs': ['memoryPerNode'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/parallelSetup/mpi': {
            'attribs': ['mpiProcesses'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/parallelSetup/openMP': {
            'attribs': ['ompThreads'],
            'optional': [],
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
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/programVersion/gitInfo': {
            'attribs': ['version', 'lastCommitHash', 'branch'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/programVersion/precision': {
            'attribs': ['type'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop': {
            'attribs': [],
            'optional': ['iteration'],
            'order': ['iteration'],
            'several': ['iteration'],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration': {
            'attribs': ['numberForCurrentRun', 'overallNumber'],
            'optional': [],
            'order': [
                'energyParameters', 'eigenvalues', 'bandgap', 'sumValenceSingleParticleEnergies', 'FermiEnergy',
                'valenceDensity', 'onSiteExchangeSplitting', 'coreStates', 'allElectronCharges',
                'magneticMomentsInMTSpheres', 'orbitalMagneticMomentsInMTSpheres', 'totalEnergy',
                'totalForcesOnRepresentativeAtoms', 'ldaUDensityMatrix', 'ldaUDensityMatrixConvergence',
                'densityConvergence', 'timing'
            ],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/FermiEnergy': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/allElectronCharges': {
            'attribs': [],
            'optional': ['mtCharges', 'spinDependentCharge', 'totalCharge', 'fixedCharges'],
            'order': ['mtCharges', 'spinDependentCharge', 'totalCharge', 'fixedCharges'],
            'several': ['mtCharges', 'spinDependentCharge', 'totalCharge', 'fixedCharges'],
            'simple': ['spinDependentCharge', 'totalCharge'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/allElectronCharges/fixedCharges': {
            'attribs': [],
            'optional': ['spinDependentCharge', 'totalCharge'],
            'order': ['spinDependentCharge', 'totalCharge'],
            'several': ['spinDependentCharge', 'totalCharge'],
            'simple': ['spinDependentCharge', 'totalCharge'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/allElectronCharges/fixedCharges/spinDependentCharge': {
            'attribs': ['spin', 'total', 'interstitial', 'mtSpheres', 'vacuum1', 'vacuum2'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/allElectronCharges/fixedCharges/totalCharge': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges': {
            'attribs': ['spin'],
            'optional': ['mtCharge', 'mtJcharge'],
            'order': ['mtCharge', 'mtJcharge'],
            'several': ['mtCharge', 'mtJcharge'],
            'simple': ['mtCharge'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtCharge': {
            'attribs': ['atomType', 'total', 's', 'p', 'd', 'f'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtJcharge': {
            'attribs': ['atomType'],
            'optional': [],
            'order': ['lowJ', 'highJ'],
            'several': [],
            'simple': ['lowJ', 'highJ'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtJcharge/highJ': {
            'attribs': ['p', 'd', 'f'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/allElectronCharges/mtCharges/mtJcharge/lowJ': {
            'attribs': ['p', 'd', 'f'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/allElectronCharges/spinDependentCharge': {
            'attribs': ['spin', 'total', 'interstitial', 'mtSpheres', 'vacuum1', 'vacuum2'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/allElectronCharges/totalCharge': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/bandgap': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/coreStates': {
            'attribs': ['atomType', 'atomicNumber', 'spin', 'kinEnergy', 'eigValSum', 'lostElectrons'],
            'optional': ['state'],
            'order': ['state'],
            'several': ['state'],
            'simple': ['state'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/coreStates/state': {
            'attribs': ['n', 'l', 'j', 'energy', 'weight'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/densityConvergence': {
            'attribs': ['units'],
            'optional': ['chargeDensity', 'overallChargeDensity', 'spinDensity'],
            'order': ['chargeDensity', 'overallChargeDensity', 'spinDensity'],
            'several': ['chargeDensity', 'overallChargeDensity', 'spinDensity'],
            'simple': ['chargeDensity', 'overallChargeDensity', 'spinDensity'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/densityConvergence/chargeDensity': {
            'attribs': ['spin', 'distance', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/densityConvergence/overallChargeDensity': {
            'attribs': ['spin', 'distance', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/densityConvergence/spinDensity': {
            'attribs': ['spin', 'distance', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/eigenvalues': {
            'attribs': [],
            'optional': [],
            'order': ['eigenvaluesAt'],
            'several': ['eigenvaluesAt'],
            'simple': ['eigenvaluesAt'],
            'text': ['eigenvaluesAt']
        },
        '/fleurOutput/scfLoop/iteration/eigenvalues/eigenvaluesAt': {
            'attribs': ['spin', 'ikpt', 'k_x', 'k_y', 'k_z'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/energyParameters': {
            'attribs': ['units'],
            'optional': ['atomicEP', 'heAtomicEP', 'loAtomicEP', 'heloAtomicEP', 'vacuumEP'],
            'order': ['atomicEP', 'heAtomicEP', 'loAtomicEP', 'heloAtomicEP', 'vacuumEP'],
            'several': ['atomicEP', 'heAtomicEP', 'loAtomicEP', 'heloAtomicEP', 'vacuumEP'],
            'simple': ['atomicEP', 'heAtomicEP', 'loAtomicEP', 'heloAtomicEP', 'vacuumEP'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/energyParameters/atomicEP': {
            'attribs': ['atomType', 'spin', 'branch', 'branchLowest', 'branchHighest', 'value'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/energyParameters/heAtomicEP': {
            'attribs': ['atomType', 'spin', 'branch', 'branchLowest', 'branchHighest', 'value'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/energyParameters/heloAtomicEP': {
            'attribs': ['atomType', 'spin', 'branch', 'branchLowest', 'branchHighest', 'value'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/energyParameters/loAtomicEP': {
            'attribs': ['atomType', 'spin', 'branch', 'branchLowest', 'branchHighest', 'value'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/energyParameters/vacuumEP': {
            'attribs': ['vacuum', 'spin', 'vzIR', 'vzInf', 'value'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/ldaUDensityMatrix': {
            'attribs': [],
            'optional': ['densityMatrixFor'],
            'order': ['densityMatrixFor'],
            'several': ['densityMatrixFor'],
            'simple': ['densityMatrixFor'],
            'text': ['densityMatrixFor']
        },
        '/fleurOutput/scfLoop/iteration/ldaUDensityMatrix/densityMatrixFor': {
            'attribs': ['spin', 'atomType', 'uIndex', 'l', 'U', 'J'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/ldaUDensityMatrixConvergence': {
            'attribs': [],
            'optional': ['distance'],
            'order': ['distance'],
            'several': ['distance'],
            'simple': ['distance'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/ldaUDensityMatrixConvergence/distance': {
            'attribs': ['spin', 'distance'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/magneticMomentsInMTSpheres': {
            'attribs': ['units'],
            'optional': ['magneticMoment'],
            'order': ['magneticMoment'],
            'several': ['magneticMoment'],
            'simple': ['magneticMoment'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/magneticMomentsInMTSpheres/magneticMoment': {
            'attribs': ['atomType', 'moment', 'spinUpCharge', 'spinDownCharge'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/onSiteExchangeSplitting': {
            'attribs': [],
            'optional': ['excSplit'],
            'order': ['excSplit'],
            'several': ['excSplit'],
            'simple': ['excSplit'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/onSiteExchangeSplitting/excSplit': {
            'attribs': ['atomType', 'l', 'Delta', 'unit'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/orbitalMagneticMomentsInMTSpheres': {
            'attribs': ['units'],
            'optional': ['orbMagMoment'],
            'order': ['orbMagMoment'],
            'several': ['orbMagMoment'],
            'simple': ['orbMagMoment'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/orbitalMagneticMomentsInMTSpheres/orbMagMoment': {
            'attribs': ['atomType', 'moment', 'spinUpCharge', 'spinDownCharge'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/sumValenceSingleParticleEnergies': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/timing': {
            'attribs': ['units'],
            'optional': ['compositeTimer', 'timer'],
            'order': ['compositeTimer', 'timer'],
            'several': ['compositeTimer', 'timer'],
            'simple': ['timer'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/timing/timer': {
            'attribs': ['name', 'value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalEnergy': {
            'attribs': ['value', 'units', 'comment'],
            'optional': [
                'sumOfEigenvalues', 'densityCoulombPotentialIntegral', 'densityEffectivePotentialIntegral',
                'chargeDenXCDenIntegral', 'FockExchangeEnergyValence', 'FockExchangeEnergyCore',
                'atomTypeDependentContributions', 'dftUCorrection', 'tkbTimesEntropy', 'freeEnergy', 'extrapolationTo0K'
            ],
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
        '/fleurOutput/scfLoop/iteration/totalEnergy/FockExchangeEnergyCore': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalEnergy/FockExchangeEnergyValence': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalEnergy/atomTypeDependentContributions': {
            'attribs': ['atomType'],
            'optional': ['electronNucleiInteractionDifferentMTs', 'MadelungTerm'],
            'order': ['electronNucleiInteractionDifferentMTs', 'MadelungTerm'],
            'several': [],
            'simple': ['electronNucleiInteractionDifferentMTs', 'MadelungTerm'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalEnergy/atomTypeDependentContributions/MadelungTerm': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalEnergy/atomTypeDependentContributions/electronNucleiInteractionDifferentMTs':
        {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalEnergy/chargeDenXCDenIntegral': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalEnergy/densityCoulombPotentialIntegral': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalEnergy/densityEffectivePotentialIntegral': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalEnergy/dftUCorrection': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalEnergy/extrapolationTo0K': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalEnergy/freeEnergy': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalEnergy/sumOfEigenvalues': {
            'attribs': ['value', 'units'],
            'optional': ['coreElectrons', 'valenceElectrons'],
            'order': ['coreElectrons', 'valenceElectrons'],
            'several': [],
            'simple': ['coreElectrons', 'valenceElectrons'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalEnergy/sumOfEigenvalues/coreElectrons': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalEnergy/sumOfEigenvalues/valenceElectrons': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalEnergy/tkbTimesEntropy': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalForcesOnRepresentativeAtoms': {
            'attribs': ['units'],
            'optional': ['forceTotal'],
            'order': ['forceTotal'],
            'several': ['forceTotal'],
            'simple': ['forceTotal'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/totalForcesOnRepresentativeAtoms/forceTotal': {
            'attribs': ['atomType', 'x', 'y', 'z', 'F_x', 'F_y', 'F_z', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/valenceDensity': {
            'attribs': [],
            'optional': ['mtCharges', 'spinDependentCharge', 'totalCharge', 'fixedCharges'],
            'order': ['mtCharges', 'spinDependentCharge', 'totalCharge', 'fixedCharges'],
            'several': ['mtCharges', 'spinDependentCharge', 'totalCharge', 'fixedCharges'],
            'simple': ['spinDependentCharge', 'totalCharge'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/valenceDensity/fixedCharges': {
            'attribs': [],
            'optional': ['spinDependentCharge', 'totalCharge'],
            'order': ['spinDependentCharge', 'totalCharge'],
            'several': ['spinDependentCharge', 'totalCharge'],
            'simple': ['spinDependentCharge', 'totalCharge'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/valenceDensity/fixedCharges/spinDependentCharge': {
            'attribs': ['spin', 'total', 'interstitial', 'mtSpheres', 'vacuum1', 'vacuum2'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/valenceDensity/fixedCharges/totalCharge': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges': {
            'attribs': ['spin'],
            'optional': ['mtCharge', 'mtJcharge'],
            'order': ['mtCharge', 'mtJcharge'],
            'several': ['mtCharge', 'mtJcharge'],
            'simple': ['mtCharge'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtCharge': {
            'attribs': ['atomType', 'total', 's', 'p', 'd', 'f'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtJcharge': {
            'attribs': ['atomType'],
            'optional': [],
            'order': ['lowJ', 'highJ'],
            'several': [],
            'simple': ['lowJ', 'highJ'],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtJcharge/highJ': {
            'attribs': ['p', 'd', 'f'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/valenceDensity/mtCharges/mtJcharge/lowJ': {
            'attribs': ['p', 'd', 'f'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/valenceDensity/spinDependentCharge': {
            'attribs': ['spin', 'total', 'interstitial', 'mtSpheres', 'vacuum1', 'vacuum2'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/scfLoop/iteration/valenceDensity/totalCharge': {
            'attribs': ['value', 'units'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurOutput/startDateAndTime': {
            'attribs': ['date', 'time', 'zone'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        }
    }
}
