# -*- coding: utf-8 -*-
__out_version__ = '0.33'
schema_dict = {
    'attrib_paths': {
        'No': [
            '/fleurOutput/scfLoop/iteration/Forcetheorem_Loop_MAE',
            '/fleurOutput/scfLoop/iteration/Forcetheorem_Loop_JIJ'
        ],
        'Q-vec': [
            '/fleurOutput/scfLoop/iteration/Forcetheorem_Loop_SSDISP',
            '/fleurOutput/scfLoop/iteration/Forcetheorem_Loop_DMI'
        ],
        'atomType': [
            '/fleurOutput/numericalParameters/volumes/mtVolume', '/fleurOutput/startDensityCharges/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtCharge',
            '/fleurOutput/startDensityCharges/mtCharges/mtJcharge',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtJcharge'
        ],
        'branch':
        '/fleurOutput/programVersion/gitInfo',
        'count':
        '/fleurOutput/numericalParameters/kPointList',
        'd': [
            '/fleurOutput/startDensityCharges/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtCharge',
            '/fleurOutput/startDensityCharges/mtCharges/mtJcharge/lowJ',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtJcharge/lowJ',
            '/fleurOutput/startDensityCharges/mtCharges/mtJcharge/highJ',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtJcharge/highJ'
        ],
        'date':
        ['/fleurOutput/programVersion/compilationInfo', '/fleurOutput/startDateAndTime', '/fleurOutput/endDateAndTime'],
        'ev-sum':
        '/fleurOutput/scfLoop/iteration/Forcetheorem_SSDISP/Entry',
        'f': [
            '/fleurOutput/startDensityCharges/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtCharge',
            '/fleurOutput/startDensityCharges/mtCharges/mtJcharge/lowJ',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtJcharge/lowJ',
            '/fleurOutput/startDensityCharges/mtCharges/mtJcharge/highJ',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtJcharge/highJ'
        ],
        'flag':
        '/fleurOutput/programVersion/compilationInfo',
        'fleurOutputVersion':
        '/fleurOutput',
        'host':
        '/fleurOutput/programVersion/compilationInfo',
        'interstitial': [
            '/fleurOutput/numericalParameters/volumes', '/fleurOutput/startDensityCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/readDensityCharges/spinDependentCharge'
        ],
        'jmtd':
        '/fleurOutput/numericalParameters/atomsInCell',
        'lastCommitHash':
        '/fleurOutput/programVersion/gitInfo',
        'link':
        '/fleurOutput/programVersion/compilationInfo',
        'lmaxd':
        '/fleurOutput/numericalParameters/basis',
        'memoryPerNode':
        '/fleurOutput/parallelSetup/mem',
        'mpiProcesses':
        '/fleurOutput/parallelSetup/mpi',
        'mtRadius':
        '/fleurOutput/numericalParameters/volumes/mtVolume',
        'mtSpheres': [
            '/fleurOutput/startDensityCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/readDensityCharges/spinDependentCharge'
        ],
        'mtVolume':
        '/fleurOutput/numericalParameters/volumes/mtVolume',
        'n_hia':
        '/fleurOutput/numericalParameters/atomsInCell',
        'n_u':
        '/fleurOutput/numericalParameters/atomsInCell',
        'nat':
        '/fleurOutput/numericalParameters/atomsInCell',
        'ng2':
        '/fleurOutput/numericalParameters/density',
        'ng3':
        '/fleurOutput/numericalParameters/density',
        'nlotot':
        '/fleurOutput/numericalParameters/basis',
        'ntype':
        '/fleurOutput/numericalParameters/atomsInCell',
        'numbands':
        '/fleurOutput/numericalParameters/bands',
        'numberForCurrentRun':
        '/fleurOutput/scfLoop/iteration',
        'nvd':
        '/fleurOutput/numericalParameters/basis',
        'omegaTilda':
        '/fleurOutput/numericalParameters/volumes',
        'ompThreads':
        '/fleurOutput/parallelSetup/openMP',
        'overallNumber':
        '/fleurOutput/scfLoop/iteration',
        'p': [
            '/fleurOutput/startDensityCharges/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtCharge',
            '/fleurOutput/startDensityCharges/mtCharges/mtJcharge/lowJ',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtJcharge/lowJ',
            '/fleurOutput/startDensityCharges/mtCharges/mtJcharge/highJ',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtJcharge/highJ'
        ],
        'q':
        '/fleurOutput/scfLoop/iteration/Forcetheorem_SSDISP/Entry',
        'qvectors':
        '/fleurOutput/scfLoop/iteration/Forcetheorem_SSDISP',
        's': [
            '/fleurOutput/startDensityCharges/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtCharge'
        ],
        'spin': [
            '/fleurOutput/startDensityCharges/mtCharges', '/fleurOutput/scfLoop/readDensityCharges/mtCharges',
            '/fleurOutput/startDensityCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/readDensityCharges/spinDependentCharge'
        ],
        'surfaceArea':
        '/fleurOutput/numericalParameters/volumes',
        'time': ['/fleurOutput/startDateAndTime', '/fleurOutput/endDateAndTime'],
        'total': [
            '/fleurOutput/startDensityCharges/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtCharge',
            '/fleurOutput/startDensityCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/readDensityCharges/spinDependentCharge'
        ],
        'type':
        '/fleurOutput/programVersion/precision',
        'unitCell':
        '/fleurOutput/numericalParameters/volumes',
        'units':
        ['/fleurOutput/startDensityCharges/totalCharge', '/fleurOutput/scfLoop/readDensityCharges/totalCharge'],
        'user':
        '/fleurOutput/programVersion/compilationInfo',
        'vacuum1': [
            '/fleurOutput/startDensityCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/readDensityCharges/spinDependentCharge'
        ],
        'vacuum2': [
            '/fleurOutput/startDensityCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/readDensityCharges/spinDependentCharge'
        ],
        'value':
        ['/fleurOutput/startDensityCharges/totalCharge', '/fleurOutput/scfLoop/readDensityCharges/totalCharge'],
        'version': ['/fleurOutput/programVersion', '/fleurOutput/programVersion/gitInfo'],
        'weightScale':
        '/fleurOutput/numericalParameters/kPointList',
        'z1':
        '/fleurOutput/numericalParameters/volumes',
        'zone': ['/fleurOutput/startDateAndTime', '/fleurOutput/endDateAndTime']
    },
    'attrib_types': {
        'Delta': ['float'],
        'F_x': ['float'],
        'F_y': ['float'],
        'F_z': ['float'],
        'J': ['float'],
        'No': ['int'],
        'Q-vec': ['int'],
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
        'q': ['int'],
        'qvectors': ['int'],
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
    'group_tags': [
        'iteration', 'Forcetheorem_Loop_SSDISP', 'Forcetheorem_Loop_DMI', 'Forcetheorem_Loop_MAE',
        'Forcetheorem_Loop_JIJ'
    ],
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
            '/orbitalMagneticMomentsInMTSpheres/orbMagMoment', '/onSiteExchangeSplitting/excSplit',
            '/ldaUDensityMatrix/densityMatrixFor', '/totalForcesOnRepresentativeAtoms/forceTotal',
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
        'interstitial': ['/valenceDensity/spinDependentCharge', '/allElectronCharges/spinDependentCharge'],
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
        'mtSpheres': ['/valenceDensity/spinDependentCharge', '/allElectronCharges/spinDependentCharge'],
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
            '/allElectronCharges/spinDependentCharge', '/coreStates', '/ldaUDensityMatrix/densityMatrixFor',
            '/ldaUDensityMatrixConvergence/distance', '/densityConvergence/chargeDensity',
            '/densityConvergence/overallChargeDensity', '/densityConvergence/spinDensity'
        ],
        'spinDownCharge':
        ['/magneticMomentsInMTSpheres/magneticMoment', '/orbitalMagneticMomentsInMTSpheres/orbMagMoment'],
        'spinUpCharge':
        ['/magneticMomentsInMTSpheres/magneticMoment', '/orbitalMagneticMomentsInMTSpheres/orbMagMoment'],
        'total': [
            '/valenceDensity/mtCharges/mtCharge', '/allElectronCharges/mtCharges/mtCharge',
            '/valenceDensity/spinDependentCharge', '/allElectronCharges/spinDependentCharge'
        ],
        'uIndex':
        '/ldaUDensityMatrix/densityMatrixFor',
        'unit':
        '/onSiteExchangeSplitting/excSplit',
        'units': [
            '/energyParameters', '/bandgap', '/sumValenceSingleParticleEnergies', '/FermiEnergy',
            '/valenceDensity/totalCharge', '/allElectronCharges/totalCharge',
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
        'vacuum1': ['/valenceDensity/spinDependentCharge', '/allElectronCharges/spinDependentCharge'],
        'vacuum2': ['/valenceDensity/spinDependentCharge', '/allElectronCharges/spinDependentCharge'],
        'value': [
            '/energyParameters/atomicEP', '/energyParameters/heAtomicEP', '/energyParameters/loAtomicEP',
            '/energyParameters/heloAtomicEP', '/energyParameters/vacuumEP', '/bandgap',
            '/sumValenceSingleParticleEnergies', '/FermiEnergy', '/valenceDensity/totalCharge',
            '/allElectronCharges/totalCharge', '/totalEnergy/densityCoulombPotentialIntegral',
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
        'FermiEnergy': '/FermiEnergy',
        'FockExchangeEnergyCore': '/totalEnergy/FockExchangeEnergyCore',
        'FockExchangeEnergyValence': '/totalEnergy/FockExchangeEnergyValence',
        'MadelungTerm': '/totalEnergy/atomTypeDependentContributions/MadelungTerm',
        'allElectronCharges': '/allElectronCharges',
        'atomTypeDependentContributions': '/totalEnergy/atomTypeDependentContributions',
        'atomicEP': '/energyParameters/atomicEP',
        'bandgap': '/bandgap',
        'chargeDenXCDenIntegral': '/totalEnergy/chargeDenXCDenIntegral',
        'chargeDensity': '/densityConvergence/chargeDensity',
        'compositeTimer': '/timing/compositeTimer',
        'coreElectrons': '/totalEnergy/sumOfEigenvalues/coreElectrons',
        'coreStates': '/coreStates',
        'densityConvergence': '/densityConvergence',
        'densityCoulombPotentialIntegral': '/totalEnergy/densityCoulombPotentialIntegral',
        'densityEffectivePotentialIntegral': '/totalEnergy/densityEffectivePotentialIntegral',
        'densityMatrixFor': '/ldaUDensityMatrix/densityMatrixFor',
        'dftUCorrection': '/totalEnergy/dftUCorrection',
        'distance': '/ldaUDensityMatrixConvergence/distance',
        'eigenvalues': '/eigenvalues',
        'eigenvaluesAt': '/eigenvalues/eigenvaluesAt',
        'electronNucleiInteractionDifferentMTs':
        '/totalEnergy/atomTypeDependentContributions/electronNucleiInteractionDifferentMTs',
        'energyParameters': '/energyParameters',
        'excSplit': '/onSiteExchangeSplitting/excSplit',
        'extrapolationTo0K': '/totalEnergy/extrapolationTo0K',
        'forceTotal': '/totalForcesOnRepresentativeAtoms/forceTotal',
        'freeEnergy': '/totalEnergy/freeEnergy',
        'heAtomicEP': '/energyParameters/heAtomicEP',
        'heloAtomicEP': '/energyParameters/heloAtomicEP',
        'highJ': ['/valenceDensity/mtCharges/mtJcharge/highJ', '/allElectronCharges/mtCharges/mtJcharge/highJ'],
        'ldaUDensityMatrix': '/ldaUDensityMatrix',
        'ldaUDensityMatrixConvergence': '/ldaUDensityMatrixConvergence',
        'loAtomicEP': '/energyParameters/loAtomicEP',
        'lowJ': ['/valenceDensity/mtCharges/mtJcharge/lowJ', '/allElectronCharges/mtCharges/mtJcharge/lowJ'],
        'magneticMoment': '/magneticMomentsInMTSpheres/magneticMoment',
        'magneticMomentsInMTSpheres': '/magneticMomentsInMTSpheres',
        'mtCharge': ['/valenceDensity/mtCharges/mtCharge', '/allElectronCharges/mtCharges/mtCharge'],
        'mtCharges': ['/valenceDensity/mtCharges', '/allElectronCharges/mtCharges'],
        'mtJcharge': ['/valenceDensity/mtCharges/mtJcharge', '/allElectronCharges/mtCharges/mtJcharge'],
        'onSiteExchangeSplitting': '/onSiteExchangeSplitting',
        'orbMagMoment': '/orbitalMagneticMomentsInMTSpheres/orbMagMoment',
        'orbitalMagneticMomentsInMTSpheres': '/orbitalMagneticMomentsInMTSpheres',
        'overallChargeDensity': '/densityConvergence/overallChargeDensity',
        'spinDensity': '/densityConvergence/spinDensity',
        'spinDependentCharge': ['/valenceDensity/spinDependentCharge', '/allElectronCharges/spinDependentCharge'],
        'state': '/coreStates/state',
        'sumOfEigenvalues': '/totalEnergy/sumOfEigenvalues',
        'sumValenceSingleParticleEnergies': '/sumValenceSingleParticleEnergies',
        'timer': '/timing/timer',
        'timing': '/timing',
        'tkbTimesEntropy': '/totalEnergy/tkbTimesEntropy',
        'totalCharge': ['/valenceDensity/totalCharge', '/allElectronCharges/totalCharge'],
        'totalEnergy': '/totalEnergy',
        'totalForcesOnRepresentativeAtoms': '/totalForcesOnRepresentativeAtoms',
        'vacuumEP': '/energyParameters/vacuumEP',
        'valenceDensity': '/valenceDensity',
        'valenceElectrons': '/totalEnergy/sumOfEigenvalues/valenceElectrons'
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
    'tag_order': {
        'Forcetheorem_SSDISP': ['Entry'],
        'compositeTimer': ['compositeTimer', 'timer'],
        'coreStates': ['state'],
        'densityConvergence': ['chargeDensity', 'overallChargeDensity', 'spinDensity'],
        'eigenvalues': ['eigenvaluesAt'],
        'energyParameters': ['atomicEP', 'heAtomicEP', 'loAtomicEP', 'heloAtomicEP', 'vacuumEP'],
        'iteration': [
            'energyParameters', 'eigenvalues', 'bandgap', 'sumValenceSingleParticleEnergies', 'FermiEnergy',
            'valenceDensity', 'onSiteExchangeSplitting', 'coreStates', 'allElectronCharges',
            'magneticMomentsInMTSpheres', 'orbitalMagneticMomentsInMTSpheres', 'totalEnergy',
            'totalForcesOnRepresentativeAtoms', 'ldaUDensityMatrix', 'ldaUDensityMatrixConvergence',
            'densityConvergence', 'timing', 'Forcetheorem_Loop_SSDISP', 'Forcetheorem_Loop_DMI',
            'Forcetheorem_Loop_MAE', 'Forcetheorem_Loop_JIJ', 'Forcetheorem_SSDISP'
        ],
        'kPointList': ['kPoint'],
        'ldaUDensityMatrix': ['densityMatrixFor'],
        'ldaUDensityMatrixConvergence': ['distance'],
        'magneticMomentsInMTSpheres': ['magneticMoment'],
        'mtCharges': ['mtCharge', 'mtJcharge'],
        'mtJcharge': ['lowJ', 'highJ'],
        'numericalParameters': ['atomsInCell', 'basis', 'density', 'bands', 'volumes', 'kPointList'],
        'onSiteExchangeSplitting': ['excSplit'],
        'orbitalMagneticMomentsInMTSpheres': ['orbMagMoment'],
        'parallelSetup': ['openMP', 'mpi', 'mem'],
        'scfLoop': ['readDensityCharges', 'iteration'],
        'startDensityCharges': ['mtCharges', 'spinDependentCharge', 'totalCharge'],
        'timing': ['compositeTimer', 'timer'],
        'totalEnergy': [
            'sumOfEigenvalues', 'densityCoulombPotentialIntegral', 'densityEffectivePotentialIntegral',
            'chargeDenXCDenIntegral', 'FockExchangeEnergyValence', 'FockExchangeEnergyCore',
            'atomTypeDependentContributions', 'dftUCorrection', 'tkbTimesEntropy', 'freeEnergy', 'extrapolationTo0K'
        ],
        'totalForcesOnRepresentativeAtoms': ['forceTotal'],
        'volumes': ['mtVolume']
    },
    'tag_paths': {
        'Entry':
        '/fleurOutput/scfLoop/iteration/Forcetheorem_SSDISP/Entry',
        'Forcetheorem_Loop_DMI':
        '/fleurOutput/scfLoop/iteration/Forcetheorem_Loop_DMI',
        'Forcetheorem_Loop_JIJ':
        '/fleurOutput/scfLoop/iteration/Forcetheorem_Loop_JIJ',
        'Forcetheorem_Loop_MAE':
        '/fleurOutput/scfLoop/iteration/Forcetheorem_Loop_MAE',
        'Forcetheorem_Loop_SSDISP':
        '/fleurOutput/scfLoop/iteration/Forcetheorem_Loop_SSDISP',
        'Forcetheorem_SSDISP':
        '/fleurOutput/scfLoop/iteration/Forcetheorem_SSDISP',
        'additionalCompilerFlags':
        '/fleurOutput/programVersion/additionalCompilerFlags',
        'atomsInCell':
        '/fleurOutput/numericalParameters/atomsInCell',
        'bands':
        '/fleurOutput/numericalParameters/bands',
        'basis':
        '/fleurOutput/numericalParameters/basis',
        'compilationInfo':
        '/fleurOutput/programVersion/compilationInfo',
        'density':
        '/fleurOutput/numericalParameters/density',
        'endDateAndTime':
        '/fleurOutput/endDateAndTime',
        'fleurInput':
        '/fleurOutput/fleurInput',
        'fleurOutput':
        '/fleurOutput',
        'gitInfo':
        '/fleurOutput/programVersion/gitInfo',
        'highJ': [
            '/fleurOutput/startDensityCharges/mtCharges/mtJcharge/highJ',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtJcharge/highJ'
        ],
        'iteration':
        '/fleurOutput/scfLoop/iteration',
        'kPoint':
        '/fleurOutput/numericalParameters/kPointList/kPoint',
        'kPointList':
        '/fleurOutput/numericalParameters/kPointList',
        'lowJ': [
            '/fleurOutput/startDensityCharges/mtCharges/mtJcharge/lowJ',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtJcharge/lowJ'
        ],
        'mem':
        '/fleurOutput/parallelSetup/mem',
        'mpi':
        '/fleurOutput/parallelSetup/mpi',
        'mtCharge': [
            '/fleurOutput/startDensityCharges/mtCharges/mtCharge',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtCharge'
        ],
        'mtCharges':
        ['/fleurOutput/startDensityCharges/mtCharges', '/fleurOutput/scfLoop/readDensityCharges/mtCharges'],
        'mtJcharge': [
            '/fleurOutput/startDensityCharges/mtCharges/mtJcharge',
            '/fleurOutput/scfLoop/readDensityCharges/mtCharges/mtJcharge'
        ],
        'mtVolume':
        '/fleurOutput/numericalParameters/volumes/mtVolume',
        'numericalParameters':
        '/fleurOutput/numericalParameters',
        'openMP':
        '/fleurOutput/parallelSetup/openMP',
        'parallelSetup':
        '/fleurOutput/parallelSetup',
        'precision':
        '/fleurOutput/programVersion/precision',
        'programVersion':
        '/fleurOutput/programVersion',
        'readDensityCharges':
        '/fleurOutput/scfLoop/readDensityCharges',
        'scfLoop':
        '/fleurOutput/scfLoop',
        'spinDependentCharge': [
            '/fleurOutput/startDensityCharges/spinDependentCharge',
            '/fleurOutput/scfLoop/readDensityCharges/spinDependentCharge'
        ],
        'startDateAndTime':
        '/fleurOutput/startDateAndTime',
        'startDensityCharges':
        '/fleurOutput/startDensityCharges',
        'targetComputerArchitectures':
        '/fleurOutput/programVersion/targetComputerArchitectures',
        'targetStructureClass':
        '/fleurOutput/programVersion/targetStructureClass',
        'totalCharge':
        ['/fleurOutput/startDensityCharges/totalCharge', '/fleurOutput/scfLoop/readDensityCharges/totalCharge'],
        'volumes':
        '/fleurOutput/numericalParameters/volumes'
    },
    'tags_several': [
        'mtVolume', 'kPoint', 'iteration', 'Forcetheorem_Loop_SSDISP', 'Forcetheorem_Loop_DMI', 'Forcetheorem_Loop_MAE',
        'Forcetheorem_Loop_JIJ', 'Entry', 'coreStates', 'atomicEP', 'heAtomicEP', 'loAtomicEP', 'heloAtomicEP',
        'vacuumEP', 'eigenvaluesAt', 'mtCharges', 'spinDependentCharge', 'mtCharge', 'mtJcharge', 'state',
        'magneticMoment', 'orbMagMoment', 'forceTotal', 'densityMatrixFor', 'excSplit',
        'atomTypeDependentContributions', 'chargeDensity', 'distance', 'compositeTimer', 'timer'
    ]
}
