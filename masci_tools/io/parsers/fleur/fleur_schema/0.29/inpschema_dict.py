# -*- coding: utf-8 -*-
__inp_version__ = '0.29'
schema_dict = {
    'attrib_types': {
        'Gmax': ['string'],
        'GmaxXC': ['string'],
        'I_initial': ['float'],
        'J': ['string'],
        'Kmax': ['string'],
        'M': ['string'],
        'MM': ['int'],
        'U': ['string'],
        'alpha': ['string'],
        'alpha_Ex': ['float'],
        'atomList': ['switch'],
        'atomType': ['int'],
        'atomicNumber': ['int'],
        'autocomp': ['switch'],
        'b_cons_x': ['string'],
        'b_cons_y': ['string'],
        'b_field': ['string'],
        'b_field_mt': ['string'],
        'band': ['switch'],
        'bands': ['int'],
        'beta': ['string'],
        'beta_Ex': ['float'],
        'bmt': ['switch'],
        'bsComf': ['switch'],
        'calculate': ['switch'],
        'cdinf': ['switch'],
        'chi': ['int'],
        'chng': ['float'],
        'coreSpec': ['switch'],
        'coreStates': ['int'],
        'coretail_lmax': ['int'],
        'correlation': ['int', 'string'],
        'count': ['int'],
        'ctail': ['switch'],
        'd': ['int'],
        'd1': ['switch'],
        'dTilda': ['string'],
        'dVac': ['string'],
        'denX': ['float'],
        'denY': ['float'],
        'denZ': ['float'],
        'dirichlet': ['switch'],
        'disp': ['switch'],
        'dos': ['switch'],
        'eDeriv': ['int'],
        'eKin': ['float'],
        'eMax': ['float'],
        'eMin': ['float'],
        'eV': ['switch'],
        'edgeType': ['string'],
        'eig66': ['switch'],
        'element': ['string'],
        'ellow': ['string'],
        'elup': ['string'],
        'energy': ['string'],
        'energyLo': ['float'],
        'energyUp': ['float'],
        'eonly': ['switch'],
        'epsdisp': ['string'],
        'epsforce': ['string'],
        'ewaldlambda': ['int'],
        'exchange': ['int', 'string'],
        'f': ['int'],
        'fermiSmearingEnergy': ['string'],
        'fermiSmearingTemp': ['string'],
        'filename': ['string'],
        'fixed_moment': ['string'],
        'fleurInputVersion': ['string'],
        'flipSpin': ['switch'],
        'force_converged': ['string'],
        'forcealpha': ['string'],
        'forcemix': ['int'],
        'form66': ['switch'],
        'frcor': ['switch'],
        'functional': ['string'],
        'gamma': ['switch'],
        'gcutm': ['float'],
        'gridPoints': ['int'],
        'gw': ['int'],
        'idsprs': ['int'],
        'idsprs0': ['int'],
        'idsprsi': ['int'],
        'idsprsl': ['int'],
        'idsprsv': ['float'],
        'iggachk': ['int'],
        'igrd': ['int'],
        'imix': ['string'],
        'integ': ['switch'],
        'invs': ['switch'],
        'invs1': ['switch'],
        'iplot': ['switch'],
        'isec1': ['int'],
        'itmax': ['int'],
        'jspins': ['int'],
        'kcrel': ['int'],
        'l': ['int'],
        'l_J': ['switch'],
        'l_amf': ['switch'],
        'l_constr': ['switch'],
        'l_disp': ['switch'],
        'l_f': ['switch'],
        'l_linMix': ['switch'],
        'l_magn': ['switch'],
        'l_mperp': ['switch'],
        'l_mtNocoPot': ['switch'],
        'l_noco': ['switch'],
        'l_rdmft': ['switch'],
        'l_relax': ['switch'],
        'l_soc': ['switch'],
        'l_ss': ['switch'],
        'label': ['string'],
        'latnam': ['string'],
        'layers': ['int'],
        'lcutm': ['int'],
        'lcutwf': ['int'],
        'lda': ['switch'],
        'lexp': ['int'],
        'lflip': ['switch'],
        'lmax': ['int'],
        'lmaxAPW': ['int'],
        'lnonsphr': ['int'],
        'locx1': ['string'],
        'locx2': ['string'],
        'locy1': ['string'],
        'locy2': ['string'],
        'logIncrement': ['string'],
        'lpr': ['int'],
        'lwb': ['switch'],
        'm_cyl': ['int'],
        'magField': ['float'],
        'magMom': ['string'],
        'maxEigenval': ['string'],
        'maxEnergy': ['string'],
        'maxIterBroyd': ['int'],
        'maxSpinDown': ['int'],
        'maxSpinUp': ['int'],
        'maxTimeToStartIter': ['string'],
        'mcd': ['switch'],
        'minDistance': ['string'],
        'minEigenval': ['string'],
        'minEnergy': ['string'],
        'minSpinDown': ['int'],
        'minSpinUp': ['int'],
        'mixParam': ['float'],
        'mix_b': ['string'],
        'mode': ['string'],
        'ms': ['switch'],
        'n': ['int'],
        'name': ['string'],
        'ndir': ['int'],
        'ndvgrd': ['int'],
        'nnne': ['int'],
        'nqphi': ['int'],
        'nqr': ['int'],
        'nsh': ['int'],
        'nstars': ['int'],
        'nstm': ['int'],
        'numPoints': ['int'],
        'numbands': ['int', 'string'],
        'numkpt': ['int'],
        'nx': ['int'],
        'ny': ['int'],
        'nz': ['int'],
        'occEps': ['float'],
        'off': ['switch'],
        'orbcomp': ['switch'],
        'p': ['int'],
        'pallst': ['switch'],
        'phi': ['string'],
        'plot_charge': ['switch'],
        'plot_rho': ['switch'],
        'plplot': ['switch'],
        'posScale': ['string'],
        'pot8': ['switch'],
        'preconditioning_param': ['string'],
        'purpose': ['string'],
        'qfix': ['int'],
        'qx': ['int'],
        'qy': ['int'],
        'qz': ['int'],
        'radius': ['string'],
        'relativisticCorrections': ['switch'],
        'relaxXYZ': ['string'],
        'rot': ['int'],
        's': ['int'],
        'scale': ['string'],
        'score': ['switch'],
        'secvar': ['switch'],
        'select': ['string'],
        'sgwf': ['switch'],
        'sig_b_1': ['string'],
        'sig_b_2': ['string'],
        'sigma': ['string'],
        'slice': ['switch'],
        'soc66': ['switch'],
        'socgwf': ['switch'],
        'socscale': ['float'],
        'spav': ['switch'],
        'species': ['string'],
        'spgrp': ['string'],
        'spinDown': ['string'],
        'spinUp': ['string'],
        'spinf': ['float', 'string'],
        'sso_opt': ['string'],
        'star': ['switch'],
        'state': ['string'],
        'statesAbove': ['int'],
        'statesBelow': ['int'],
        'supercellX': ['int'],
        'supercellY': ['int'],
        'supercellZ': ['int'],
        'swsp': ['switch'],
        'theta': ['string'],
        'thetaJ': ['string'],
        'thetaj': ['string'],
        'tolerance': ['float'],
        'tworkf': ['string'],
        'type': ['string'],
        'unfoldband': ['switch'],
        'vM': ['int'],
        'vacdos': ['switch'],
        'vacuum': ['int'],
        'valenceElectrons': ['string'],
        'value': ['string'],
        'vcaAddCharge': ['float'],
        'vca_charge': ['string'],
        'vchk': ['switch'],
        'verbose': ['switch'],
        'wannier': ['switch'],
        'weight': ['string'],
        'weightScale': ['string'],
        'zrfs': ['switch'],
        'zrfs1': ['switch'],
        'zsigma': ['string']
    },
    'basic_types': {
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
    'omitt_contained_tags': [
        'constants', 'atomSpecies', 'atomGroups', 'symmetryOperations', 'displacements', 'relaxation-history',
        'spinSpiralDispersion', 'qVectors'
    ],
    'other_attribs': {
        'J': ['/fleurInput/atomSpecies/species/ldaU', '/fleurInput/atomGroups/atomGroup/ldaU'],
        'M': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'U': ['/fleurInput/atomSpecies/species/ldaU', '/fleurInput/atomGroups/atomGroup/ldaU'],
        'absPos': ['/fleurInput/atomGroups/atomGroup/absPos'],
        'alpha': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'atomicNumber': ['/fleurInput/atomSpecies/species'],
        'b_cons_x': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'b_cons_y': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'b_field_mt': ['/fleurInput/atomSpecies/species/special'],
        'beta': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'calculate': ['/fleurInput/atomSpecies/species/force', '/fleurInput/atomGroups/atomGroup/force'],
        'coreConfig': ['/fleurInput/atomSpecies/species/electronConfig/coreConfig'],
        'coreStates': ['/fleurInput/atomSpecies/species'],
        'count': [
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount',
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList'
        ],
        'd': ['/fleurInput/atomSpecies/species/energyParameters', '/fleurInput/atomGroups/atomGroup/energyParameters'],
        'denX': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointDensity'],
        'denY': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointDensity'],
        'denZ': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointDensity'],
        'displace': ['/fleurInput/relaxation/displacements/displace'],
        'eDeriv': ['/fleurInput/atomSpecies/species/lo', '/fleurInput/atomGroups/atomGroup/lo'],
        'element': ['/fleurInput/atomSpecies/species'],
        'energy': ['/fleurInput/relaxation/relaxation-history/step'],
        'f': ['/fleurInput/atomSpecies/species/energyParameters', '/fleurInput/atomGroups/atomGroup/energyParameters'],
        'filename': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointListFile'],
        'filmPos': ['/fleurInput/atomGroups/atomGroup/filmPos'],
        'flipSpin': ['/fleurInput/atomSpecies/species'],
        'gamma': [
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointMesh',
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount',
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointDensity'
        ],
        'gridPoints': ['/fleurInput/atomSpecies/species/mtSphere', '/fleurInput/atomGroups/atomGroup/mtSphere'],
        'kPoint': [
            '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint',
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList/kPoint'
        ],
        'l': [
            '/fleurInput/atomSpecies/species/ldaU', '/fleurInput/atomGroups/atomGroup/ldaU',
            '/fleurInput/atomSpecies/species/lo', '/fleurInput/atomGroups/atomGroup/lo'
        ],
        'l_amf': ['/fleurInput/atomSpecies/species/ldaU', '/fleurInput/atomGroups/atomGroup/ldaU'],
        'l_magn': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'l_relax': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'label': [
            '/fleurInput/atomGroups/atomGroup/relPos', '/fleurInput/atomGroups/atomGroup/absPos',
            '/fleurInput/atomGroups/atomGroup/filmPos'
        ],
        'lcutm': ['/fleurInput/atomSpecies/species/prodBasis'],
        'lcutwf': ['/fleurInput/atomSpecies/species/prodBasis'],
        'lda': ['/fleurInput/atomSpecies/species/special'],
        'lmax': ['/fleurInput/atomSpecies/species/atomicCutoffs', '/fleurInput/atomGroups/atomGroup/atomicCutoffs'],
        'lmaxAPW': ['/fleurInput/atomSpecies/species/atomicCutoffs', '/fleurInput/atomGroups/atomGroup/atomicCutoffs'],
        'lnonsphr': ['/fleurInput/atomSpecies/species/atomicCutoffs', '/fleurInput/atomGroups/atomGroup/atomicCutoffs'],
        'logIncrement': ['/fleurInput/atomSpecies/species/mtSphere', '/fleurInput/atomGroups/atomGroup/mtSphere'],
        'magField': ['/fleurInput/atomSpecies/species', '/fleurInput/atomGroups/atomGroup'],
        'magMom': ['/fleurInput/atomSpecies/species'],
        'n': ['/fleurInput/atomSpecies/species/lo', '/fleurInput/atomGroups/atomGroup/lo'],
        'name': [
            '/fleurInput/constants/constant', '/fleurInput/atomSpecies/species',
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint',
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/specialPoint'
        ],
        'nx': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointMesh'],
        'ny': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointMesh'],
        'nz': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointMesh'],
        'orbcomp': [
            '/fleurInput/atomGroups/atomGroup/relPos', '/fleurInput/atomGroups/atomGroup/absPos',
            '/fleurInput/atomGroups/atomGroup/filmPos'
        ],
        'orbcomprot': ['/fleurInput/atomGroups/atomGroup/orbcomprot'],
        'p': ['/fleurInput/atomSpecies/species/energyParameters', '/fleurInput/atomGroups/atomGroup/energyParameters'],
        'posScale': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList'],
        'posforce': ['/fleurInput/relaxation/relaxation-history/step/posforce'],
        'purpose': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet'],
        'q': [
            '/fleurInput/forceTheorem/spinSpiralDispersion/q', '/fleurInput/forceTheorem/DMI/qVectors/q',
            '/fleurInput/forceTheorem/Jij/qVectors/q'
        ],
        'radius': ['/fleurInput/atomSpecies/species/mtSphere', '/fleurInput/atomGroups/atomGroup/mtSphere'],
        'relPos': ['/fleurInput/atomGroups/atomGroup/relPos'],
        'relaxXYZ': ['/fleurInput/atomSpecies/species/force', '/fleurInput/atomGroups/atomGroup/force'],
        'row-1': ['/fleurInput/cell/symmetryOperations/symOp/row-1'],
        'row-2': ['/fleurInput/cell/symmetryOperations/symOp/row-2'],
        'row-3': ['/fleurInput/cell/symmetryOperations/symOp/row-3'],
        's': ['/fleurInput/atomSpecies/species/energyParameters', '/fleurInput/atomGroups/atomGroup/energyParameters'],
        'select': ['/fleurInput/atomSpecies/species/prodBasis'],
        'shape': ['/fleurInput/calculationSetup/fields/shape'],
        'socscale': ['/fleurInput/atomSpecies/species/special'],
        'specialPoint': [
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint',
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/specialPoint'
        ],
        'species': ['/fleurInput/atomGroups/atomGroup'],
        'spinDown': [
            '/fleurInput/cell/filmLattice/vacuumEnergyParameters',
            '/fleurInput/atomSpecies/species/electronConfig/stateOccupation'
        ],
        'spinUp': [
            '/fleurInput/cell/filmLattice/vacuumEnergyParameters',
            '/fleurInput/atomSpecies/species/electronConfig/stateOccupation'
        ],
        'state': ['/fleurInput/atomSpecies/species/electronConfig/stateOccupation'],
        'type': ['/fleurInput/atomSpecies/species/lo', '/fleurInput/atomGroups/atomGroup/lo'],
        'vacuum': ['/fleurInput/cell/filmLattice/vacuumEnergyParameters'],
        'valenceConfig': ['/fleurInput/atomSpecies/species/electronConfig/valenceConfig'],
        'value': ['/fleurInput/constants/constant'],
        'vcaAddCharge': ['/fleurInput/atomSpecies/species', '/fleurInput/atomGroups/atomGroup'],
        'vca_charge': ['/fleurInput/atomSpecies/species/special'],
        'wannier': [
            '/fleurInput/atomGroups/atomGroup/relPos', '/fleurInput/atomGroups/atomGroup/absPos',
            '/fleurInput/atomGroups/atomGroup/filmPos'
        ],
        'weight': [
            '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint',
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList/kPoint'
        ],
        'weightScale': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList']
    },
    'settable_attribs': {
        'Gmax': '/fleurInput/calculationSetup/cutoffs',
        'GmaxXC': '/fleurInput/calculationSetup/cutoffs',
        'I_initial': '/fleurInput/output/coreSpectrum',
        'Kmax': '/fleurInput/calculationSetup/cutoffs',
        'MM': '/fleurInput/calculationSetup/oneDParams',
        'alpha': '/fleurInput/calculationSetup/scfLoop',
        'alpha_Ex': '/fleurInput/output/coreSpectrum',
        'atomList': '/fleurInput/output/wannier',
        'atomType': '/fleurInput/output/coreSpectrum',
        'autocomp': '/fleurInput/calculationSetup/fields',
        'b_field': '/fleurInput/calculationSetup/fields',
        'band': '/fleurInput/output',
        'bands': '/fleurInput/calculationSetup/prodBasis',
        'beta_Ex': '/fleurInput/output/coreSpectrum',
        'bmt': '/fleurInput/output/specialOutput',
        'bsComf': '/fleurInput/output/wannier',
        'c': '/fleurInput/cell/bulkLattice/c',
        'cdinf': '/fleurInput/output/checks',
        'chi': '/fleurInput/calculationSetup/oneDParams',
        'chng': '/fleurInput/xcFunctional/xcParams',
        'comment': '/fleurInput/comment',
        'coreSpec': '/fleurInput/output',
        'coretail_lmax': '/fleurInput/calculationSetup/coreElectrons',
        'ctail': '/fleurInput/calculationSetup/coreElectrons',
        'd1': '/fleurInput/calculationSetup/oneDParams',
        'dTilda': '/fleurInput/cell/filmLattice',
        'dVac': '/fleurInput/cell/filmLattice',
        'denX': '/fleurInput/calculationSetup/bzIntegration/kPointDensity',
        'denY': '/fleurInput/calculationSetup/bzIntegration/kPointDensity',
        'denZ': '/fleurInput/calculationSetup/bzIntegration/kPointDensity',
        'dirichlet': '/fleurInput/calculationSetup/fields',
        'disp': '/fleurInput/output/checks',
        'dos': '/fleurInput/output',
        'eKin': '/fleurInput/output/coreSpectrum',
        'eMax': '/fleurInput/output/coreSpectrum',
        'eMin': '/fleurInput/output/coreSpectrum',
        'eV': '/fleurInput/calculationSetup/fields',
        'edgeIndices': '/fleurInput/output/coreSpectrum/edgeIndices',
        'edgeType': '/fleurInput/output/coreSpectrum',
        'eig66': '/fleurInput/calculationSetup/expertModes',
        'ellow': '/fleurInput/calculationSetup/energyParameterLimits',
        'elup': '/fleurInput/calculationSetup/energyParameterLimits',
        'energyLo': '/fleurInput/output/magneticCircularDichroism',
        'energyUp': '/fleurInput/output/magneticCircularDichroism',
        'eonly': '/fleurInput/output/specialOutput',
        'epsdisp': '/fleurInput/calculationSetup/geometryOptimization',
        'epsforce': '/fleurInput/calculationSetup/geometryOptimization',
        'ewaldlambda': '/fleurInput/calculationSetup/prodBasis',
        'fermiSmearingEnergy': '/fleurInput/calculationSetup/bzIntegration',
        'fermiSmearingTemp': '/fleurInput/calculationSetup/bzIntegration',
        'filename': '/fleurInput/cell/symmetryFile',
        'fixed_moment': '/fleurInput/calculationSetup/magnetism',
        'fleurInputVersion': '/fleurInput',
        'force_converged': '/fleurInput/calculationSetup/geometryOptimization',
        'forcealpha': '/fleurInput/calculationSetup/geometryOptimization',
        'forcemix': '/fleurInput/calculationSetup/geometryOptimization',
        'form66': '/fleurInput/output/specialOutput',
        'frcor': '/fleurInput/calculationSetup/coreElectrons',
        'functional': '/fleurInput/calculationSetup/rdmft',
        'gcutm': '/fleurInput/calculationSetup/prodBasis',
        'gw': '/fleurInput/calculationSetup/expertModes',
        'idsprs': '/fleurInput/xcFunctional/xcParams',
        'idsprs0': '/fleurInput/xcFunctional/ggaPrinting',
        'idsprsi': '/fleurInput/xcFunctional/ggaPrinting',
        'idsprsl': '/fleurInput/xcFunctional/ggaPrinting',
        'idsprsv': '/fleurInput/xcFunctional/ggaPrinting',
        'iggachk': '/fleurInput/xcFunctional/ggaPrinting',
        'igrd': '/fleurInput/xcFunctional/xcParams',
        'imix': '/fleurInput/calculationSetup/scfLoop',
        'integ': '/fleurInput/output/vacuumDOS',
        'invs': '/fleurInput/cell/symmetry',
        'invs1': '/fleurInput/calculationSetup/oneDParams',
        'iplot': '/fleurInput/output/plotting',
        'isec1': '/fleurInput/calculationSetup/expertModes',
        'itmax': '/fleurInput/calculationSetup/scfLoop',
        'jobList': '/fleurInput/output/wannier/jobList',
        'jspins': '/fleurInput/calculationSetup/magnetism',
        'kcrel': '/fleurInput/calculationSetup/coreElectrons',
        'l_J': '/fleurInput/calculationSetup/magnetism',
        'l_constr': '/fleurInput/calculationSetup/nocoParams',
        'l_disp': '/fleurInput/calculationSetup/nocoParams',
        'l_f': '/fleurInput/calculationSetup/geometryOptimization',
        'l_linMix': '/fleurInput/calculationSetup/ldaU',
        'l_mperp': '/fleurInput/calculationSetup/nocoParams',
        'l_mtNocoPot': '/fleurInput/calculationSetup/nocoParams',
        'l_noco': '/fleurInput/calculationSetup/magnetism',
        'l_rdmft': '/fleurInput/calculationSetup/rdmft',
        'l_soc': '/fleurInput/calculationSetup/soc',
        'l_ss': '/fleurInput/calculationSetup/nocoParams',
        'layers': '/fleurInput/output/vacuumDOS',
        'lexp': '/fleurInput/calculationSetup/prodBasis',
        'lflip': '/fleurInput/calculationSetup/magnetism',
        'lmax': '/fleurInput/output/coreSpectrum',
        'locx1': '/fleurInput/output/vacuumDOS',
        'locx2': '/fleurInput/output/vacuumDOS',
        'locy1': '/fleurInput/output/vacuumDOS',
        'locy2': '/fleurInput/output/vacuumDOS',
        'lpr': '/fleurInput/calculationSetup/expertModes',
        'lwb': '/fleurInput/xcFunctional/xcParams',
        'm_cyl': '/fleurInput/calculationSetup/oneDParams',
        'maxEigenval': '/fleurInput/output/chargeDensitySlicing',
        'maxEnergy': '/fleurInput/output/densityOfStates',
        'maxIterBroyd': '/fleurInput/calculationSetup/scfLoop',
        'maxSpinDown': '/fleurInput/output/wannier/bandSelection',
        'maxSpinUp': '/fleurInput/output/wannier/bandSelection',
        'maxTimeToStartIter': '/fleurInput/calculationSetup/scfLoop',
        'mcd': '/fleurInput/output',
        'minDistance': '/fleurInput/calculationSetup/scfLoop',
        'minEigenval': '/fleurInput/output/chargeDensitySlicing',
        'minEnergy': '/fleurInput/output/densityOfStates',
        'minSpinDown': '/fleurInput/output/wannier/bandSelection',
        'minSpinUp': '/fleurInput/output/wannier/bandSelection',
        'mixParam': '/fleurInput/calculationSetup/ldaU',
        'mix_b': '/fleurInput/calculationSetup/nocoParams',
        'mode': '/fleurInput/calculationSetup/bzIntegration',
        'ms': '/fleurInput/output/wannier',
        'name': '/fleurInput/xcFunctional',
        'ndir': '/fleurInput/output/densityOfStates',
        'ndvgrd': '/fleurInput/xcFunctional/xcParams',
        'nnne': '/fleurInput/output/chargeDensitySlicing',
        'nqphi': '/fleurInput/output/coreSpectrum',
        'nqr': '/fleurInput/output/coreSpectrum',
        'nsh': '/fleurInput/calculationSetup/nocoParams',
        'nstars': '/fleurInput/output/vacuumDOS',
        'nstm': '/fleurInput/output/vacuumDOS',
        'numPoints': '/fleurInput/output/coreSpectrum',
        'numbands': '/fleurInput/calculationSetup/cutoffs',
        'numkpt': '/fleurInput/output/chargeDensitySlicing',
        'nx': '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
        'ny': '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
        'nz': '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
        'occEps': '/fleurInput/calculationSetup/rdmft',
        'off': '/fleurInput/calculationSetup/soc',
        'pallst': '/fleurInput/output/chargeDensitySlicing',
        'plot_charge': '/fleurInput/calculationSetup/fields',
        'plot_rho': '/fleurInput/calculationSetup/fields',
        'plplot': '/fleurInput/output/plotting',
        'posScale': '/fleurInput/calculationSetup/bzIntegration/kPointList',
        'pot8': '/fleurInput/calculationSetup/expertModes',
        'preconditioning_param': '/fleurInput/calculationSetup/scfLoop',
        'qfix': '/fleurInput/calculationSetup/geometryOptimization',
        'qsc': '/fleurInput/calculationSetup/nocoParams/qsc',
        'qss': '/fleurInput/calculationSetup/nocoParams/qss',
        'qx': '/fleurInput/calculationSetup/spinSpiralQPointMesh',
        'qy': '/fleurInput/calculationSetup/spinSpiralQPointMesh',
        'qz': '/fleurInput/calculationSetup/spinSpiralQPointMesh',
        'relativisticCorrections': '/fleurInput/xcFunctional',
        'rot': '/fleurInput/calculationSetup/oneDParams',
        'score': '/fleurInput/output/plotting',
        'secvar': '/fleurInput/calculationSetup/expertModes',
        'sgwf': '/fleurInput/output/wannier',
        'sig_b_1': '/fleurInput/calculationSetup/fields',
        'sig_b_2': '/fleurInput/calculationSetup/fields',
        'sigma': '/fleurInput/output/densityOfStates',
        'slice': '/fleurInput/output',
        'soc66': '/fleurInput/calculationSetup/soc',
        'socgwf': '/fleurInput/output/wannier',
        'spav': '/fleurInput/calculationSetup/soc',
        'spgrp': '/fleurInput/cell/symmetry',
        'sso_opt': '/fleurInput/calculationSetup/nocoParams',
        'star': '/fleurInput/output/vacuumDOS',
        'statesAbove': '/fleurInput/calculationSetup/rdmft',
        'statesBelow': '/fleurInput/calculationSetup/rdmft',
        'supercellX': '/fleurInput/output/unfoldingBand',
        'supercellY': '/fleurInput/output/unfoldingBand',
        'supercellZ': '/fleurInput/output/unfoldingBand',
        'swsp': '/fleurInput/calculationSetup/magnetism',
        'thetaJ': '/fleurInput/calculationSetup/nocoParams',
        'thetaj': '/fleurInput/forceTheorem/Jij',
        'tolerance': '/fleurInput/calculationSetup/prodBasis',
        'tworkf': '/fleurInput/output/vacuumDOS',
        'unfoldband': '/fleurInput/output/unfoldingBand',
        'vM': '/fleurInput/calculationSetup/oneDParams',
        'vacdos': '/fleurInput/output',
        'valenceElectrons': '/fleurInput/calculationSetup/bzIntegration',
        'vchk': '/fleurInput/output/checks',
        'verbose': '/fleurInput/output/coreSpectrum',
        'wannier': '/fleurInput/output',
        'weightScale': '/fleurInput/calculationSetup/bzIntegration/kPointList',
        'zrfs': '/fleurInput/cell/symmetry',
        'zrfs1': '/fleurInput/calculationSetup/oneDParams',
        'zsigma': '/fleurInput/calculationSetup/fields'
    },
    'settable_contains_attribs': {
        'a1': ['/fleurInput/cell/bulkLattice/a1', '/fleurInput/cell/filmLattice/a1'],
        'a2': ['/fleurInput/cell/bulkLattice/a2', '/fleurInput/cell/filmLattice/a2'],
        'correlation': ['/fleurInput/xcFunctional/LibXCID', '/fleurInput/xcFunctional/LibXCName'],
        'count': [
            '/fleurInput/calculationSetup/bzIntegration/kPointCount',
            '/fleurInput/calculationSetup/bzIntegration/kPointList'
        ],
        'exchange': ['/fleurInput/xcFunctional/LibXCID', '/fleurInput/xcFunctional/LibXCName'],
        'gamma': [
            '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
            '/fleurInput/calculationSetup/bzIntegration/kPointCount',
            '/fleurInput/calculationSetup/bzIntegration/kPointDensity'
        ],
        'latnam': ['/fleurInput/cell/bulkLattice', '/fleurInput/cell/filmLattice'],
        'phi': ['/fleurInput/calculationSetup/soc', '/fleurInput/forceTheorem/MAE', '/fleurInput/forceTheorem/DMI'],
        'row-1': [
            '/fleurInput/cell/bulkLattice/row-1', '/fleurInput/cell/filmLattice/row-1',
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-1', '/fleurInput/cell/filmLattice/bravaisMatrix/row-1'
        ],
        'row-2': [
            '/fleurInput/cell/bulkLattice/row-2', '/fleurInput/cell/filmLattice/row-2',
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-2', '/fleurInput/cell/filmLattice/bravaisMatrix/row-2'
        ],
        'row-3':
        ['/fleurInput/cell/bulkLattice/bravaisMatrix/row-3', '/fleurInput/cell/filmLattice/bravaisMatrix/row-3'],
        'scale': [
            '/fleurInput/cell/bulkLattice', '/fleurInput/cell/filmLattice', '/fleurInput/cell/bulkLattice/a1',
            '/fleurInput/cell/filmLattice/a1', '/fleurInput/cell/bulkLattice/a2', '/fleurInput/cell/filmLattice/a2',
            '/fleurInput/cell/bulkLattice/c'
        ],
        'spinf': ['/fleurInput/calculationSetup/scfLoop', '/fleurInput/calculationSetup/ldaU'],
        'theta': ['/fleurInput/calculationSetup/soc', '/fleurInput/forceTheorem/MAE', '/fleurInput/forceTheorem/DMI']
    },
    'simple_elements': {
        'a1': [{
            'length': 1,
            'type': ['string']
        }],
        'a2': [{
            'length': 1,
            'type': ['string']
        }],
        'absPos': [{
            'length': 3,
            'type': ['string']
        }],
        'c': [{
            'length': 1,
            'type': ['string']
        }],
        'comment': [{
            'length': 1,
            'type': ['string']
        }],
        'coreConfig': [{
            'length': 'unbounded',
            'type': ['string']
        }],
        'displace': [{
            'length': 3,
            'type': ['float']
        }],
        'edgeIndices': [{
            'length': 'unbounded',
            'type': ['int']
        }],
        'filmPos': [{
            'length': 3,
            'type': ['string']
        }],
        'jobList': [{
            'length': 'unbounded',
            'type': ['string']
        }],
        'kPoint': [{
            'length': 3,
            'type': ['float']
        }],
        'orbcomprot': [{
            'length': 3,
            'type': ['float']
        }],
        'posforce': [{
            'length': 1,
            'type': ['string']
        }],
        'q': [{
            'length': 1,
            'type': ['string']
        }],
        'qsc': [{
            'length': 3,
            'type': ['float']
        }],
        'qss': [{
            'length': 3,
            'type': ['float']
        }],
        'relPos': [{
            'length': 3,
            'type': ['string']
        }],
        'row-1': [{
            'length': 2,
            'type': ['string']
        }, {
            'length': 3,
            'type': ['string']
        }, {
            'length': 4,
            'type': ['float']
        }],
        'row-2': [{
            'length': 2,
            'type': ['string']
        }, {
            'length': 3,
            'type': ['string']
        }, {
            'length': 4,
            'type': ['float']
        }],
        'row-3': [{
            'length': 3,
            'type': ['string']
        }, {
            'length': 4,
            'type': ['float']
        }],
        'shape': [{
            'length': 1,
            'type': ['string']
        }],
        'specialPoint': [{
            'length': 3,
            'type': ['string']
        }],
        'valenceConfig': [{
            'length': 'unbounded',
            'type': ['string']
        }]
    },
    'tag_info': {
        '/fleurInput': {
            'attribs': ['fleurInputVersion'],
            'optional': ['comment', 'constants', 'output', 'forceTheorem', 'relaxation'],
            'order': [
                'comment', 'constants', 'calculationSetup', 'cell', 'xcFunctional', 'atomSpecies', 'atomGroups',
                'output', 'forceTheorem', 'relaxation'
            ],
            'several': [],
            'simple': ['comment', 'calculationSetup', 'output', 'relaxation'],
            'text': ['comment']
        },
        '/fleurInput/atomGroups': {
            'attribs': [],
            'optional': [],
            'order': ['atomGroup'],
            'several': ['atomGroup'],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup': {
            'attribs': ['species', 'magField', 'vcaAddCharge'],
            'optional':
            ['mtSphere', 'atomicCutoffs', 'energyParameters', 'force', 'nocoParams', 'ldaU', 'lo', 'orbcomprot'],
            'order': [
                'relPos', 'absPos', 'filmPos', 'mtSphere', 'atomicCutoffs', 'energyParameters', 'force', 'nocoParams',
                'ldaU', 'lo', 'orbcomprot'
            ],
            'several': ['relPos', 'absPos', 'filmPos', 'ldaU', 'lo'],
            'simple': [
                'relPos', 'absPos', 'filmPos', 'mtSphere', 'atomicCutoffs', 'energyParameters', 'force', 'nocoParams',
                'ldaU', 'lo', 'orbcomprot'
            ],
            'text': ['relPos', 'absPos', 'filmPos', 'orbcomprot']
        },
        '/fleurInput/atomGroups/atomGroup/absPos': {
            'attribs': ['label', 'wannier', 'orbcomp'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/atomicCutoffs': {
            'attribs': ['lmax', 'lnonsphr', 'lmaxAPW'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/energyParameters': {
            'attribs': ['s', 'p', 'd', 'f'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/filmPos': {
            'attribs': ['label', 'wannier', 'orbcomp'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/force': {
            'attribs': ['calculate', 'relaxXYZ'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/ldaU': {
            'attribs': ['l', 'U', 'J', 'l_amf'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/lo': {
            'attribs': ['type', 'l', 'n', 'eDeriv'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/mtSphere': {
            'attribs': ['radius', 'gridPoints', 'logIncrement'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/nocoParams': {
            'attribs': ['l_relax', 'l_magn', 'M', 'alpha', 'beta', 'b_cons_x', 'b_cons_y'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/relPos': {
            'attribs': ['label', 'wannier', 'orbcomp'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies': {
            'attribs': [],
            'optional': [],
            'order': ['species'],
            'several': ['species'],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species': {
            'attribs':
            ['name', 'element', 'atomicNumber', 'coreStates', 'magMom', 'flipSpin', 'magField', 'vcaAddCharge'],
            'optional':
            ['energyParameters', 'prodBasis', 'special', 'force', 'electronConfig', 'nocoParams', 'ldaU', 'lo'],
            'order': [
                'mtSphere', 'atomicCutoffs', 'energyParameters', 'prodBasis', 'special', 'force', 'electronConfig',
                'nocoParams', 'ldaU', 'lo'
            ],
            'several': ['ldaU', 'lo'],
            'simple': [
                'mtSphere', 'atomicCutoffs', 'energyParameters', 'prodBasis', 'special', 'force', 'nocoParams', 'ldaU',
                'lo'
            ],
            'text': []
        },
        '/fleurInput/atomSpecies/species/atomicCutoffs': {
            'attribs': ['lmax', 'lnonsphr', 'lmaxAPW'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/electronConfig': {
            'attribs': [],
            'optional': ['valenceConfig', 'stateOccupation'],
            'order': ['coreConfig', 'valenceConfig', 'stateOccupation'],
            'several': ['stateOccupation'],
            'simple': ['coreConfig', 'valenceConfig', 'stateOccupation'],
            'text': ['coreConfig', 'valenceConfig']
        },
        '/fleurInput/atomSpecies/species/electronConfig/stateOccupation': {
            'attribs': ['state', 'spinUp', 'spinDown'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/energyParameters': {
            'attribs': ['s', 'p', 'd', 'f'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/force': {
            'attribs': ['calculate', 'relaxXYZ'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/ldaU': {
            'attribs': ['l', 'U', 'J', 'l_amf'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/lo': {
            'attribs': ['type', 'l', 'n', 'eDeriv'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/mtSphere': {
            'attribs': ['radius', 'gridPoints', 'logIncrement'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/nocoParams': {
            'attribs': ['l_relax', 'l_magn', 'M', 'alpha', 'beta', 'b_cons_x', 'b_cons_y'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/prodBasis': {
            'attribs': ['lcutm', 'lcutwf', 'select'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/special': {
            'attribs': ['lda', 'socscale', 'b_field_mt', 'vca_charge'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup': {
            'attribs': [],
            'optional': [
                'prodBasis', 'soc', 'nocoParams', 'oneDParams', 'expertModes', 'geometryOptimization', 'ldaU', 'rdmft',
                'spinSpiralQPointMesh', 'fields', 'energyParameterLimits'
            ],
            'order': [
                'cutoffs', 'scfLoop', 'coreElectrons', 'magnetism', 'bzIntegration', 'prodBasis', 'soc', 'nocoParams',
                'oneDParams', 'expertModes', 'geometryOptimization', 'ldaU', 'rdmft', 'spinSpiralQPointMesh', 'fields',
                'energyParameterLimits'
            ],
            'several': [],
            'simple': [
                'cutoffs', 'scfLoop', 'coreElectrons', 'magnetism', 'prodBasis', 'soc', 'oneDParams', 'expertModes',
                'geometryOptimization', 'ldaU', 'rdmft', 'spinSpiralQPointMesh', 'energyParameterLimits'
            ],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration': {
            'attribs': ['valenceElectrons', 'mode', 'fermiSmearingEnergy', 'fermiSmearingTemp'],
            'optional': ['altKPointSet'],
            'order': ['kPointMesh', 'kPointCount', 'kPointList', 'kPointDensity', 'altKPointSet'],
            'several': ['altKPointSet'],
            'simple': ['kPointMesh', 'kPointDensity'],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet': {
            'attribs': ['purpose'],
            'optional': [],
            'order': ['kPointMesh', 'kPointCount', 'kPointList', 'kPointDensity', 'kPointListFile'],
            'several': [],
            'simple': ['kPointMesh', 'kPointDensity', 'kPointListFile'],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount': {
            'attribs': ['count', 'gamma'],
            'optional': ['specialPoint'],
            'order': ['specialPoint'],
            'several': ['specialPoint'],
            'simple': ['specialPoint'],
            'text': ['specialPoint']
        },
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/specialPoint': {
            'attribs': ['name'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointDensity': {
            'attribs': ['denX', 'denY', 'denZ', 'gamma'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList': {
            'attribs': ['posScale', 'weightScale', 'count'],
            'optional': [],
            'order': ['kPoint'],
            'several': ['kPoint'],
            'simple': ['kPoint'],
            'text': ['kPoint']
        },
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList/kPoint': {
            'attribs': ['weight'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointListFile': {
            'attribs': ['filename'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointMesh': {
            'attribs': ['nx', 'ny', 'nz', 'gamma'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointCount': {
            'attribs': ['count', 'gamma'],
            'optional': ['specialPoint'],
            'order': ['specialPoint'],
            'several': ['specialPoint'],
            'simple': ['specialPoint'],
            'text': ['specialPoint']
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint': {
            'attribs': ['name'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointDensity': {
            'attribs': ['denX', 'denY', 'denZ', 'gamma'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointList': {
            'attribs': ['posScale', 'weightScale', 'count'],
            'optional': [],
            'order': ['kPoint'],
            'several': ['kPoint'],
            'simple': ['kPoint'],
            'text': ['kPoint']
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint': {
            'attribs': ['weight'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointMesh': {
            'attribs': ['nx', 'ny', 'nz', 'gamma'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/coreElectrons': {
            'attribs': ['ctail', 'frcor', 'kcrel', 'coretail_lmax'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/cutoffs': {
            'attribs': ['Kmax', 'Gmax', 'GmaxXC', 'numbands'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/energyParameterLimits': {
            'attribs': ['ellow', 'elup'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/expertModes': {
            'attribs': ['gw', 'pot8', 'eig66', 'lpr', 'isec1', 'secvar'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/fields': {
            'attribs':
            ['b_field', 'zsigma', 'sig_b_1', 'sig_b_2', 'plot_charge', 'plot_rho', 'autocomp', 'dirichlet', 'eV'],
            'optional': ['shape'],
            'order': ['shape'],
            'several': ['shape'],
            'simple': ['shape'],
            'text': ['shape']
        },
        '/fleurInput/calculationSetup/geometryOptimization': {
            'attribs': ['l_f', 'forcealpha', 'epsdisp', 'epsforce', 'forcemix', 'qfix', 'force_converged'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/ldaU': {
            'attribs': ['l_linMix', 'mixParam', 'spinf'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/magnetism': {
            'attribs': ['jspins', 'l_noco', 'l_J', 'swsp', 'lflip', 'fixed_moment'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/nocoParams': {
            'attribs': ['l_ss', 'l_mperp', 'l_constr', 'l_disp', 'sso_opt', 'mix_b', 'thetaJ', 'nsh', 'l_mtNocoPot'],
            'optional': ['qsc'],
            'order': ['qss', 'qsc'],
            'several': [],
            'simple': ['qss', 'qsc'],
            'text': ['qss', 'qsc']
        },
        '/fleurInput/calculationSetup/oneDParams': {
            'attribs': ['d1', 'MM', 'vM', 'm_cyl', 'chi', 'rot', 'invs1', 'zrfs1'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/prodBasis': {
            'attribs': ['gcutm', 'bands', 'tolerance', 'lexp', 'ewaldlambda'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/rdmft': {
            'attribs': ['l_rdmft', 'occEps', 'statesBelow', 'statesAbove', 'functional'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/scfLoop': {
            'attribs': [
                'itmax', 'maxIterBroyd', 'imix', 'alpha', 'preconditioning_param', 'spinf', 'minDistance',
                'maxTimeToStartIter'
            ],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/soc': {
            'attribs': ['theta', 'phi', 'l_soc', 'spav', 'off', 'soc66'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/spinSpiralQPointMesh': {
            'attribs': ['qx', 'qy', 'qz'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell': {
            'attribs': [],
            'optional': [],
            'order': ['symmetry', 'symmetryFile', 'symmetryOperations', 'bulkLattice', 'filmLattice'],
            'several': [],
            'simple': ['symmetry', 'symmetryFile'],
            'text': []
        },
        '/fleurInput/cell/bulkLattice': {
            'attribs': ['scale', 'latnam'],
            'optional': ['a2'],
            'order': ['a1', 'a2', 'c', 'row-1', 'row-2', 'c', 'bravaisMatrix'],
            'several': [],
            'simple': ['a1', 'a2', 'c', 'row-1', 'row-2', 'c'],
            'text': ['a1', 'a2', 'c', 'row-1', 'row-2', 'c']
        },
        '/fleurInput/cell/bulkLattice/a1': {
            'attribs': ['scale'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/bulkLattice/a2': {
            'attribs': ['scale'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/bulkLattice/bravaisMatrix': {
            'attribs': [],
            'optional': [],
            'order': ['row-1', 'row-2', 'row-3'],
            'several': [],
            'simple': ['row-1', 'row-2', 'row-3'],
            'text': ['row-1', 'row-2', 'row-3']
        },
        '/fleurInput/cell/bulkLattice/c': {
            'attribs': ['scale'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/filmLattice': {
            'attribs': ['scale', 'latnam', 'dVac', 'dTilda'],
            'optional': ['a2', 'vacuumEnergyParameters'],
            'order': ['a1', 'a2', 'row-1', 'row-2', 'bravaisMatrix', 'vacuumEnergyParameters'],
            'several': ['vacuumEnergyParameters'],
            'simple': ['a1', 'a2', 'row-1', 'row-2', 'vacuumEnergyParameters'],
            'text': ['a1', 'a2', 'row-1', 'row-2']
        },
        '/fleurInput/cell/filmLattice/a1': {
            'attribs': ['scale'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/filmLattice/a2': {
            'attribs': ['scale'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/filmLattice/bravaisMatrix': {
            'attribs': [],
            'optional': [],
            'order': ['row-1', 'row-2', 'row-3'],
            'several': [],
            'simple': ['row-1', 'row-2', 'row-3'],
            'text': ['row-1', 'row-2', 'row-3']
        },
        '/fleurInput/cell/filmLattice/vacuumEnergyParameters': {
            'attribs': ['vacuum', 'spinUp', 'spinDown'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/symmetry': {
            'attribs': ['spgrp', 'invs', 'zrfs'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/symmetryFile': {
            'attribs': ['filename'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/symmetryOperations': {
            'attribs': [],
            'optional': [],
            'order': ['symOp'],
            'several': ['symOp'],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/symmetryOperations/symOp': {
            'attribs': [],
            'optional': [],
            'order': ['row-1', 'row-2', 'row-3'],
            'several': [],
            'simple': ['row-1', 'row-2', 'row-3'],
            'text': ['row-1', 'row-2', 'row-3']
        },
        '/fleurInput/constants': {
            'attribs': [],
            'optional': ['constant'],
            'order': ['constant'],
            'several': ['constant'],
            'simple': ['constant'],
            'text': []
        },
        '/fleurInput/constants/constant': {
            'attribs': ['name', 'value'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/forceTheorem': {
            'attribs': [],
            'optional': [],
            'order': ['MAE', 'spinSpiralDispersion', 'DMI', 'Jij'],
            'several': [],
            'simple': ['MAE', 'DMI', 'Jij'],
            'text': []
        },
        '/fleurInput/forceTheorem/DMI': {
            'attribs': ['theta', 'phi'],
            'optional': [],
            'order': ['qVectors'],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/forceTheorem/DMI/qVectors': {
            'attribs': [],
            'optional': [],
            'order': ['q'],
            'several': ['q'],
            'simple': ['q'],
            'text': ['q']
        },
        '/fleurInput/forceTheorem/Jij': {
            'attribs': ['thetaj'],
            'optional': [],
            'order': ['qVectors'],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/forceTheorem/Jij/qVectors': {
            'attribs': [],
            'optional': [],
            'order': ['q'],
            'several': ['q'],
            'simple': ['q'],
            'text': ['q']
        },
        '/fleurInput/forceTheorem/MAE': {
            'attribs': ['theta', 'phi'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/forceTheorem/spinSpiralDispersion': {
            'attribs': [],
            'optional': [],
            'order': ['q'],
            'several': ['q'],
            'simple': ['q'],
            'text': ['q']
        },
        '/fleurInput/output': {
            'attribs': ['dos', 'band', 'vacdos', 'slice', 'coreSpec', 'wannier', 'mcd'],
            'optional': [
                'checks', 'densityOfStates', 'vacuumDOS', 'plotting', 'chargeDensitySlicing', 'specialOutput',
                'coreSpectrum', 'wannier', 'magneticCircularDichroism', 'unfoldingBand'
            ],
            'order': [
                'checks', 'densityOfStates', 'vacuumDOS', 'plotting', 'chargeDensitySlicing', 'specialOutput',
                'coreSpectrum', 'wannier', 'magneticCircularDichroism', 'unfoldingBand'
            ],
            'several': [],
            'simple': [
                'checks', 'densityOfStates', 'vacuumDOS', 'plotting', 'chargeDensitySlicing', 'specialOutput',
                'wannier', 'magneticCircularDichroism', 'unfoldingBand'
            ],
            'text': []
        },
        '/fleurInput/output/chargeDensitySlicing': {
            'attribs': ['numkpt', 'minEigenval', 'maxEigenval', 'nnne', 'pallst'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/checks': {
            'attribs': ['vchk', 'cdinf', 'disp'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/coreSpectrum': {
            'attribs': [
                'eKin', 'atomType', 'lmax', 'edgeType', 'eMin', 'eMax', 'numPoints', 'verbose', 'nqphi', 'nqr',
                'alpha_Ex', 'beta_Ex', 'I_initial'
            ],
            'optional': [],
            'order': ['edgeIndices'],
            'several': [],
            'simple': ['edgeIndices'],
            'text': ['edgeIndices']
        },
        '/fleurInput/output/densityOfStates': {
            'attribs': ['ndir', 'minEnergy', 'maxEnergy', 'sigma'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/magneticCircularDichroism': {
            'attribs': ['energyLo', 'energyUp'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/plotting': {
            'attribs': ['iplot', 'score', 'plplot'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/specialOutput': {
            'attribs': ['form66', 'eonly', 'bmt'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/unfoldingBand': {
            'attribs': ['unfoldband', 'supercellX', 'supercellY', 'supercellZ'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/vacuumDOS': {
            'attribs': ['layers', 'integ', 'star', 'nstars', 'locx1', 'locy1', 'locx2', 'locy2', 'nstm', 'tworkf'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/wannier': {
            'attribs': ['ms', 'sgwf', 'socgwf', 'bsComf', 'atomList'],
            'optional': ['bandSelection', 'jobList'],
            'order': ['bandSelection', 'jobList'],
            'several': [],
            'simple': ['bandSelection', 'jobList'],
            'text': ['jobList']
        },
        '/fleurInput/output/wannier/bandSelection': {
            'attribs': ['minSpinUp', 'maxSpinUp', 'minSpinDown', 'maxSpinDown'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/relaxation': {
            'attribs': [],
            'optional': ['displacements', 'relaxation-history'],
            'order': ['displacements', 'relaxation-history'],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/relaxation/displacements': {
            'attribs': [],
            'optional': [],
            'order': ['displace'],
            'several': ['displace'],
            'simple': ['displace'],
            'text': ['displace']
        },
        '/fleurInput/relaxation/relaxation-history': {
            'attribs': [],
            'optional': [],
            'order': ['step'],
            'several': ['step'],
            'simple': [],
            'text': []
        },
        '/fleurInput/relaxation/relaxation-history/step': {
            'attribs': ['energy'],
            'optional': [],
            'order': ['posforce'],
            'several': ['posforce'],
            'simple': ['posforce'],
            'text': ['posforce']
        },
        '/fleurInput/xcFunctional': {
            'attribs': ['name', 'relativisticCorrections'],
            'optional': ['LibXCID', 'LibXCName', 'xcParams', 'ggaPrinting'],
            'order': ['LibXCID', 'LibXCName', 'xcParams', 'ggaPrinting'],
            'several': [],
            'simple': ['LibXCID', 'LibXCName', 'xcParams', 'ggaPrinting'],
            'text': []
        },
        '/fleurInput/xcFunctional/LibXCID': {
            'attribs': ['exchange', 'correlation'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/xcFunctional/LibXCName': {
            'attribs': ['exchange', 'correlation'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/xcFunctional/ggaPrinting': {
            'attribs': ['iggachk', 'idsprs0', 'idsprsl', 'idsprsi', 'idsprsv'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/xcFunctional/xcParams': {
            'attribs': ['igrd', 'lwb', 'ndvgrd', 'idsprs', 'chng'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        }
    },
    'tag_paths': {
        'DMI':
        '/fleurInput/forceTheorem/DMI',
        'Jij':
        '/fleurInput/forceTheorem/Jij',
        'LibXCID':
        '/fleurInput/xcFunctional/LibXCID',
        'LibXCName':
        '/fleurInput/xcFunctional/LibXCName',
        'MAE':
        '/fleurInput/forceTheorem/MAE',
        'a1': ['/fleurInput/cell/bulkLattice/a1', '/fleurInput/cell/filmLattice/a1'],
        'a2': ['/fleurInput/cell/bulkLattice/a2', '/fleurInput/cell/filmLattice/a2'],
        'absPos':
        '/fleurInput/atomGroups/atomGroup/absPos',
        'altKPointSet':
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet',
        'atomGroup':
        '/fleurInput/atomGroups/atomGroup',
        'atomGroups':
        '/fleurInput/atomGroups',
        'atomSpecies':
        '/fleurInput/atomSpecies',
        'atomicCutoffs':
        ['/fleurInput/atomSpecies/species/atomicCutoffs', '/fleurInput/atomGroups/atomGroup/atomicCutoffs'],
        'bandSelection':
        '/fleurInput/output/wannier/bandSelection',
        'bravaisMatrix': ['/fleurInput/cell/bulkLattice/bravaisMatrix', '/fleurInput/cell/filmLattice/bravaisMatrix'],
        'bulkLattice':
        '/fleurInput/cell/bulkLattice',
        'bzIntegration':
        '/fleurInput/calculationSetup/bzIntegration',
        'c':
        '/fleurInput/cell/bulkLattice/c',
        'calculationSetup':
        '/fleurInput/calculationSetup',
        'cell':
        '/fleurInput/cell',
        'chargeDensitySlicing':
        '/fleurInput/output/chargeDensitySlicing',
        'checks':
        '/fleurInput/output/checks',
        'comment':
        '/fleurInput/comment',
        'constant':
        '/fleurInput/constants/constant',
        'constants':
        '/fleurInput/constants',
        'coreConfig':
        '/fleurInput/atomSpecies/species/electronConfig/coreConfig',
        'coreElectrons':
        '/fleurInput/calculationSetup/coreElectrons',
        'coreSpectrum':
        '/fleurInput/output/coreSpectrum',
        'cutoffs':
        '/fleurInput/calculationSetup/cutoffs',
        'densityOfStates':
        '/fleurInput/output/densityOfStates',
        'displace':
        '/fleurInput/relaxation/displacements/displace',
        'displacements':
        '/fleurInput/relaxation/displacements',
        'edgeIndices':
        '/fleurInput/output/coreSpectrum/edgeIndices',
        'electronConfig':
        '/fleurInput/atomSpecies/species/electronConfig',
        'energyParameterLimits':
        '/fleurInput/calculationSetup/energyParameterLimits',
        'energyParameters':
        ['/fleurInput/atomSpecies/species/energyParameters', '/fleurInput/atomGroups/atomGroup/energyParameters'],
        'expertModes':
        '/fleurInput/calculationSetup/expertModes',
        'fields':
        '/fleurInput/calculationSetup/fields',
        'filmLattice':
        '/fleurInput/cell/filmLattice',
        'filmPos':
        '/fleurInput/atomGroups/atomGroup/filmPos',
        'fleurInput':
        '/fleurInput',
        'force': ['/fleurInput/atomSpecies/species/force', '/fleurInput/atomGroups/atomGroup/force'],
        'forceTheorem':
        '/fleurInput/forceTheorem',
        'geometryOptimization':
        '/fleurInput/calculationSetup/geometryOptimization',
        'ggaPrinting':
        '/fleurInput/xcFunctional/ggaPrinting',
        'jobList':
        '/fleurInput/output/wannier/jobList',
        'kPoint': [
            '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint',
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList/kPoint'
        ],
        'kPointCount': [
            '/fleurInput/calculationSetup/bzIntegration/kPointCount',
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount'
        ],
        'kPointDensity': [
            '/fleurInput/calculationSetup/bzIntegration/kPointDensity',
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointDensity'
        ],
        'kPointList': [
            '/fleurInput/calculationSetup/bzIntegration/kPointList',
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList'
        ],
        'kPointListFile':
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointListFile',
        'kPointMesh': [
            '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointMesh'
        ],
        'ldaU': [
            '/fleurInput/calculationSetup/ldaU', '/fleurInput/atomSpecies/species/ldaU',
            '/fleurInput/atomGroups/atomGroup/ldaU'
        ],
        'lo': ['/fleurInput/atomSpecies/species/lo', '/fleurInput/atomGroups/atomGroup/lo'],
        'magneticCircularDichroism':
        '/fleurInput/output/magneticCircularDichroism',
        'magnetism':
        '/fleurInput/calculationSetup/magnetism',
        'mtSphere': ['/fleurInput/atomSpecies/species/mtSphere', '/fleurInput/atomGroups/atomGroup/mtSphere'],
        'nocoParams': [
            '/fleurInput/calculationSetup/nocoParams', '/fleurInput/atomSpecies/species/nocoParams',
            '/fleurInput/atomGroups/atomGroup/nocoParams'
        ],
        'oneDParams':
        '/fleurInput/calculationSetup/oneDParams',
        'orbcomprot':
        '/fleurInput/atomGroups/atomGroup/orbcomprot',
        'output':
        '/fleurInput/output',
        'plotting':
        '/fleurInput/output/plotting',
        'posforce':
        '/fleurInput/relaxation/relaxation-history/step/posforce',
        'prodBasis': ['/fleurInput/calculationSetup/prodBasis', '/fleurInput/atomSpecies/species/prodBasis'],
        'q': [
            '/fleurInput/forceTheorem/spinSpiralDispersion/q', '/fleurInput/forceTheorem/DMI/qVectors/q',
            '/fleurInput/forceTheorem/Jij/qVectors/q'
        ],
        'qVectors': ['/fleurInput/forceTheorem/DMI/qVectors', '/fleurInput/forceTheorem/Jij/qVectors'],
        'qsc':
        '/fleurInput/calculationSetup/nocoParams/qsc',
        'qss':
        '/fleurInput/calculationSetup/nocoParams/qss',
        'rdmft':
        '/fleurInput/calculationSetup/rdmft',
        'relPos':
        '/fleurInput/atomGroups/atomGroup/relPos',
        'relaxation':
        '/fleurInput/relaxation',
        'relaxation-history':
        '/fleurInput/relaxation/relaxation-history',
        'row-1': [
            '/fleurInput/cell/bulkLattice/row-1', '/fleurInput/cell/filmLattice/row-1',
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-1', '/fleurInput/cell/filmLattice/bravaisMatrix/row-1',
            '/fleurInput/cell/symmetryOperations/symOp/row-1'
        ],
        'row-2': [
            '/fleurInput/cell/bulkLattice/row-2', '/fleurInput/cell/filmLattice/row-2',
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-2', '/fleurInput/cell/filmLattice/bravaisMatrix/row-2',
            '/fleurInput/cell/symmetryOperations/symOp/row-2'
        ],
        'row-3': [
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-3', '/fleurInput/cell/filmLattice/bravaisMatrix/row-3',
            '/fleurInput/cell/symmetryOperations/symOp/row-3'
        ],
        'scfLoop':
        '/fleurInput/calculationSetup/scfLoop',
        'shape':
        '/fleurInput/calculationSetup/fields/shape',
        'soc':
        '/fleurInput/calculationSetup/soc',
        'special':
        '/fleurInput/atomSpecies/species/special',
        'specialOutput':
        '/fleurInput/output/specialOutput',
        'specialPoint': [
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint',
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/specialPoint'
        ],
        'species':
        '/fleurInput/atomSpecies/species',
        'spinSpiralDispersion':
        '/fleurInput/forceTheorem/spinSpiralDispersion',
        'spinSpiralQPointMesh':
        '/fleurInput/calculationSetup/spinSpiralQPointMesh',
        'stateOccupation':
        '/fleurInput/atomSpecies/species/electronConfig/stateOccupation',
        'step':
        '/fleurInput/relaxation/relaxation-history/step',
        'symOp':
        '/fleurInput/cell/symmetryOperations/symOp',
        'symmetry':
        '/fleurInput/cell/symmetry',
        'symmetryFile':
        '/fleurInput/cell/symmetryFile',
        'symmetryOperations':
        '/fleurInput/cell/symmetryOperations',
        'unfoldingBand':
        '/fleurInput/output/unfoldingBand',
        'vacuumDOS':
        '/fleurInput/output/vacuumDOS',
        'vacuumEnergyParameters':
        '/fleurInput/cell/filmLattice/vacuumEnergyParameters',
        'valenceConfig':
        '/fleurInput/atomSpecies/species/electronConfig/valenceConfig',
        'wannier':
        '/fleurInput/output/wannier',
        'xcFunctional':
        '/fleurInput/xcFunctional',
        'xcParams':
        '/fleurInput/xcFunctional/xcParams'
    }
}
