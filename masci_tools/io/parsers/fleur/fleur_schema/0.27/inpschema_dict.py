# -*- coding: utf-8 -*-
__inp_version__ = '0.27'
schema_dict = {
    'attrib_types': {
        'Gmax': ['float'],
        'GmaxXC': ['float'],
        'J': ['float'],
        'Kmax': ['float'],
        'M': ['float'],
        'MM': ['int'],
        'U': ['float'],
        'alpha': ['float'],
        'atomicNumber': ['int'],
        'autocomp': ['switch'],
        'b_cons_x': ['float'],
        'b_cons_y': ['float'],
        'band': ['switch'],
        'beta': ['float'],
        'bmt': ['switch'],
        'calculate': ['switch'],
        'cdinf': ['switch'],
        'chi': ['int'],
        'chng': ['float'],
        'coreStates': ['int'],
        'count': ['int'],
        'ctail': ['switch'],
        'd': ['int'],
        'd1': ['switch'],
        'dTilda': ['float'],
        'dVac': ['float'],
        'dirichlet': ['switch'],
        'disp': ['switch'],
        'dos': ['switch'],
        'eDeriv': ['int'],
        'eV': ['switch'],
        'eig66': ['switch'],
        'element': ['string'],
        'ellow': ['float'],
        'elup': ['float'],
        'eonly': ['switch'],
        'epsdisp': ['float'],
        'epsforce': ['float'],
        'f': ['int'],
        'fermiSmearingEnergy': ['float'],
        'fermiSmearingTemp': ['float'],
        'filename': ['string'],
        'fleurInputVersion': ['string'],
        'flipSpin': ['switch'],
        'form66': ['switch'],
        'frcor': ['switch'],
        'gamma': ['switch'],
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
        'l_magn': ['switch'],
        'l_mperp': ['switch'],
        'l_noco': ['switch'],
        'l_relax': ['switch'],
        'l_soc': ['switch'],
        'l_ss': ['switch'],
        'latnam': ['string'],
        'layers': ['int'],
        'lflip': ['switch'],
        'lmax': ['int'],
        'lmaxAPW': ['int'],
        'lnonsphr': ['int'],
        'locx1': ['float'],
        'locx2': ['float'],
        'locy1': ['float'],
        'locy2': ['float'],
        'logIncrement': ['float'],
        'lpr': ['int'],
        'lwb': ['switch'],
        'm_cyl': ['int'],
        'magField': ['float'],
        'magMom': ['float'],
        'maxEigenval': ['float'],
        'maxEnergy': ['float'],
        'maxIterBroyd': ['int'],
        'maxTimeToStartIter': ['float'],
        'minDistance': ['float'],
        'minEigenval': ['float'],
        'minEnergy': ['float'],
        'mix_b': ['float'],
        'mode': ['string'],
        'n': ['int'],
        'name': ['string'],
        'ndir': ['int'],
        'ndvgrd': ['int'],
        'nnne': ['int'],
        'nsh': ['int'],
        'nstars': ['int'],
        'nstm': ['int'],
        'numbands': ['int', 'string'],
        'numkpt': ['int'],
        'nx': ['int'],
        'ny': ['int'],
        'nz': ['int'],
        'off': ['switch'],
        'orbcomp': ['switch'],
        'p': ['int'],
        'pallst': ['switch'],
        'phi': ['float'],
        'plot_charge': ['switch'],
        'plot_rho': ['switch'],
        'plplot': ['switch'],
        'posScale': ['float'],
        'pot8': ['switch'],
        'qfix': ['switch'],
        'qx': ['int'],
        'qy': ['int'],
        'qz': ['int'],
        'radius': ['float'],
        'relativisticCorrections': ['switch'],
        'relaxXYZ': ['string'],
        'rot': ['int'],
        's': ['int'],
        'scale': ['float'],
        'score': ['switch'],
        'secvar': ['switch'],
        'sig_b_1': ['float'],
        'sig_b_2': ['float'],
        'sigma': ['float'],
        'slice': ['switch'],
        'soc66': ['switch'],
        'spav': ['switch'],
        'species': ['string'],
        'spgrp': ['string'],
        'spinDown': ['float'],
        'spinUp': ['float'],
        'spinf': ['float'],
        'sso_opt': ['string'],
        'star': ['switch'],
        'state': ['string'],
        'swsp': ['switch'],
        'theta': ['float'],
        'thetaJ': ['float'],
        'thetad': ['float'],
        'tworkf': ['float'],
        'type': ['string'],
        'vM': ['int'],
        'vacdos': ['switch'],
        'vacuum': ['int'],
        'valenceElectrons': ['float'],
        'value': ['string'],
        'vcaAddCharge': ['float'],
        'vchk': ['switch'],
        'weight': ['float'],
        'weightScale': ['float'],
        'xa': ['float'],
        'zrfs': ['switch'],
        'zrfs1': ['switch'],
        'zsigma': ['float']
    },
    'basic_types': {
        'BZIntegrationModeEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'CoreConfigEnum': {
            'base_types': ['string'],
            'length': 1
        },
        'CoreStateListType': {
            'base_types': ['string'],
            'length': 'unbounded'
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
        'KPointType': {
            'base_types': ['float'],
            'length': 3
        },
        'LatnamEnum': {
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
        'SpecialPointType': {
            'base_types': ['float'],
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
        }
    },
    'omitt_contained_tags': ['constants', 'atomSpecies', 'atomGroups', 'symmetryOperations'],
    'other_attribs': {
        'J': ['/fleurInput/atomSpecies/species/ldaU', '/fleurInput/atomGroups/atomGroup/ldaU'],
        'M': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'U': ['/fleurInput/atomSpecies/species/ldaU', '/fleurInput/atomGroups/atomGroup/ldaU'],
        'absPos': ['/fleurInput/atomGroups/atomGroup/absPos'],
        'alpha': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'atomicNumber': ['/fleurInput/atomSpecies/species'],
        'b_cons_x': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'b_cons_y': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'beta': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'calculate': ['/fleurInput/atomSpecies/species/force', '/fleurInput/atomGroups/atomGroup/force'],
        'coreConfig': ['/fleurInput/atomSpecies/species/electronConfig/coreConfig'],
        'coreStates': ['/fleurInput/atomSpecies/species'],
        'd': ['/fleurInput/atomSpecies/species/energyParameters', '/fleurInput/atomGroups/atomGroup/energyParameters'],
        'eDeriv': ['/fleurInput/atomSpecies/species/lo', '/fleurInput/atomGroups/atomGroup/lo'],
        'element': ['/fleurInput/atomSpecies/species'],
        'f': ['/fleurInput/atomSpecies/species/energyParameters', '/fleurInput/atomGroups/atomGroup/energyParameters'],
        'filmPos': ['/fleurInput/atomGroups/atomGroup/filmPos'],
        'flipSpin': ['/fleurInput/atomSpecies/species'],
        'gridPoints': ['/fleurInput/atomSpecies/species/mtSphere', '/fleurInput/atomGroups/atomGroup/mtSphere'],
        'kPoint': ['/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint'],
        'l': [
            '/fleurInput/atomSpecies/species/ldaU', '/fleurInput/atomGroups/atomGroup/ldaU',
            '/fleurInput/atomSpecies/species/lo', '/fleurInput/atomGroups/atomGroup/lo'
        ],
        'l_amf': ['/fleurInput/atomSpecies/species/ldaU', '/fleurInput/atomGroups/atomGroup/ldaU'],
        'l_magn': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'l_relax': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'lmax': ['/fleurInput/atomSpecies/species/atomicCutoffs', '/fleurInput/atomGroups/atomGroup/atomicCutoffs'],
        'lmaxAPW': ['/fleurInput/atomSpecies/species/atomicCutoffs', '/fleurInput/atomGroups/atomGroup/atomicCutoffs'],
        'lnonsphr': ['/fleurInput/atomSpecies/species/atomicCutoffs', '/fleurInput/atomGroups/atomGroup/atomicCutoffs'],
        'logIncrement': ['/fleurInput/atomSpecies/species/mtSphere', '/fleurInput/atomGroups/atomGroup/mtSphere'],
        'magField': ['/fleurInput/atomSpecies/species', '/fleurInput/atomGroups/atomGroup'],
        'magMom': ['/fleurInput/atomSpecies/species'],
        'n': ['/fleurInput/atomSpecies/species/lo', '/fleurInput/atomGroups/atomGroup/lo'],
        'name': [
            '/fleurInput/constants/constant', '/fleurInput/atomSpecies/species',
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint'
        ],
        'orbcomp': ['/fleurInput/atomGroups/atomGroup'],
        'orbcomprot': ['/fleurInput/atomGroups/atomGroup/orbcomprot'],
        'p': ['/fleurInput/atomSpecies/species/energyParameters', '/fleurInput/atomGroups/atomGroup/energyParameters'],
        'radius': ['/fleurInput/atomSpecies/species/mtSphere', '/fleurInput/atomGroups/atomGroup/mtSphere'],
        'relPos': ['/fleurInput/atomGroups/atomGroup/relPos'],
        'relaxXYZ': ['/fleurInput/atomSpecies/species/force', '/fleurInput/atomGroups/atomGroup/force'],
        'row-1': ['/fleurInput/cell/symmetryOperations/symOp/row-1'],
        'row-2': ['/fleurInput/cell/symmetryOperations/symOp/row-2'],
        'row-3': ['/fleurInput/cell/symmetryOperations/symOp/row-3'],
        's': ['/fleurInput/atomSpecies/species/energyParameters', '/fleurInput/atomGroups/atomGroup/energyParameters'],
        'specialPoint': ['/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint'],
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
        'weight': ['/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint']
    },
    'settable_attribs': {
        'Gmax': '/fleurInput/calculationSetup/cutoffs',
        'GmaxXC': '/fleurInput/calculationSetup/cutoffs',
        'Kmax': '/fleurInput/calculationSetup/cutoffs',
        'MM': '/fleurInput/calculationSetup/oneDParams',
        'alpha': '/fleurInput/calculationSetup/scfLoop',
        'autocomp': '/fleurInput/calculationSetup/eField',
        'band': '/fleurInput/output',
        'bmt': '/fleurInput/output/specialOutput',
        'c': '/fleurInput/cell/bulkLattice/c',
        'cdinf': '/fleurInput/output/checks',
        'chi': '/fleurInput/calculationSetup/oneDParams',
        'chng': '/fleurInput/xcFunctional/xcParams',
        'comment': '/fleurInput/comment',
        'ctail': '/fleurInput/calculationSetup/coreElectrons',
        'd1': '/fleurInput/calculationSetup/oneDParams',
        'dTilda': '/fleurInput/cell/filmLattice',
        'dVac': '/fleurInput/cell/filmLattice',
        'dirichlet': '/fleurInput/calculationSetup/eField',
        'disp': '/fleurInput/output/checks',
        'dos': '/fleurInput/output',
        'eV': '/fleurInput/calculationSetup/eField',
        'eig66': '/fleurInput/calculationSetup/expertModes',
        'ellow': '/fleurInput/calculationSetup/energyParameterLimits',
        'elup': '/fleurInput/calculationSetup/energyParameterLimits',
        'eonly': '/fleurInput/output/specialOutput',
        'epsdisp': '/fleurInput/calculationSetup/geometryOptimization',
        'epsforce': '/fleurInput/calculationSetup/geometryOptimization',
        'fermiSmearingEnergy': '/fleurInput/calculationSetup/bzIntegration',
        'fermiSmearingTemp': '/fleurInput/calculationSetup/bzIntegration',
        'filename': '/fleurInput/cell/symmetryFile',
        'fleurInputVersion': '/fleurInput',
        'form66': '/fleurInput/output/specialOutput',
        'frcor': '/fleurInput/calculationSetup/coreElectrons',
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
        'jspins': '/fleurInput/calculationSetup/magnetism',
        'kcrel': '/fleurInput/calculationSetup/coreElectrons',
        'l_J': '/fleurInput/calculationSetup/magnetism',
        'l_constr': '/fleurInput/calculationSetup/nocoParams',
        'l_disp': '/fleurInput/calculationSetup/nocoParams',
        'l_f': '/fleurInput/calculationSetup/geometryOptimization',
        'l_mperp': '/fleurInput/calculationSetup/nocoParams',
        'l_noco': '/fleurInput/calculationSetup/magnetism',
        'l_soc': '/fleurInput/calculationSetup/soc',
        'l_ss': '/fleurInput/calculationSetup/nocoParams',
        'layers': '/fleurInput/output/vacuumDOS',
        'lflip': '/fleurInput/calculationSetup/magnetism',
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
        'maxTimeToStartIter': '/fleurInput/calculationSetup/scfLoop',
        'minDistance': '/fleurInput/calculationSetup/scfLoop',
        'minEigenval': '/fleurInput/output/chargeDensitySlicing',
        'minEnergy': '/fleurInput/output/densityOfStates',
        'mix_b': '/fleurInput/calculationSetup/nocoParams',
        'mode': '/fleurInput/calculationSetup/bzIntegration',
        'name': '/fleurInput/xcFunctional',
        'ndir': '/fleurInput/output/densityOfStates',
        'ndvgrd': '/fleurInput/xcFunctional/xcParams',
        'nnne': '/fleurInput/output/chargeDensitySlicing',
        'nsh': '/fleurInput/calculationSetup/nocoParams',
        'nstars': '/fleurInput/output/vacuumDOS',
        'nstm': '/fleurInput/output/vacuumDOS',
        'numbands': '/fleurInput/calculationSetup/cutoffs',
        'numkpt': '/fleurInput/output/chargeDensitySlicing',
        'nx': '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
        'ny': '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
        'nz': '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
        'off': '/fleurInput/calculationSetup/soc',
        'pallst': '/fleurInput/output/chargeDensitySlicing',
        'phi': '/fleurInput/calculationSetup/soc',
        'plot_charge': '/fleurInput/calculationSetup/eField',
        'plot_rho': '/fleurInput/calculationSetup/eField',
        'plplot': '/fleurInput/output/plotting',
        'posScale': '/fleurInput/calculationSetup/bzIntegration/kPointList',
        'pot8': '/fleurInput/calculationSetup/expertModes',
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
        'sig_b_1': '/fleurInput/calculationSetup/eField',
        'sig_b_2': '/fleurInput/calculationSetup/eField',
        'sigma': '/fleurInput/output/densityOfStates',
        'slice': '/fleurInput/output',
        'soc66': '/fleurInput/calculationSetup/soc',
        'spav': '/fleurInput/calculationSetup/soc',
        'spgrp': '/fleurInput/cell/symmetry',
        'spinf': '/fleurInput/calculationSetup/scfLoop',
        'sso_opt': '/fleurInput/calculationSetup/nocoParams',
        'star': '/fleurInput/output/vacuumDOS',
        'swsp': '/fleurInput/calculationSetup/magnetism',
        'theta': '/fleurInput/calculationSetup/soc',
        'thetaJ': '/fleurInput/calculationSetup/nocoParams',
        'thetad': '/fleurInput/calculationSetup/geometryOptimization',
        'tworkf': '/fleurInput/output/vacuumDOS',
        'vM': '/fleurInput/calculationSetup/oneDParams',
        'vacdos': '/fleurInput/output',
        'valenceElectrons': '/fleurInput/calculationSetup/bzIntegration',
        'vchk': '/fleurInput/output/checks',
        'weightScale': '/fleurInput/calculationSetup/bzIntegration/kPointList',
        'xa': '/fleurInput/calculationSetup/geometryOptimization',
        'zrfs': '/fleurInput/cell/symmetry',
        'zrfs1': '/fleurInput/calculationSetup/oneDParams',
        'zsigma': '/fleurInput/calculationSetup/eField'
    },
    'settable_contains_attribs': {
        'a1': ['/fleurInput/cell/bulkLattice/a1', '/fleurInput/cell/filmLattice/a1'],
        'a2': ['/fleurInput/cell/bulkLattice/a2', '/fleurInput/cell/filmLattice/a2'],
        'count': [
            '/fleurInput/calculationSetup/bzIntegration/kPointCount',
            '/fleurInput/calculationSetup/bzIntegration/kPointList'
        ],
        'gamma': [
            '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
            '/fleurInput/calculationSetup/bzIntegration/kPointCount'
        ],
        'latnam': ['/fleurInput/cell/bulkLattice', '/fleurInput/cell/filmLattice'],
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
        'scale': ['/fleurInput/cell/bulkLattice', '/fleurInput/cell/filmLattice']
    },
    'simple_elements': {
        'a1': [{
            'length': 1,
            'type': ['float']
        }],
        'a2': [{
            'length': 1,
            'type': ['float']
        }],
        'absPos': [{
            'length': 3,
            'type': ['string']
        }],
        'c': [{
            'length': 1,
            'type': ['float']
        }],
        'comment': [{
            'length': 1,
            'type': ['string']
        }],
        'coreConfig': [{
            'length': 'unbounded',
            'type': ['string']
        }],
        'filmPos': [{
            'length': 3,
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
        'specialPoint': [{
            'length': 3,
            'type': ['float']
        }],
        'valenceConfig': [{
            'length': 'unbounded',
            'type': ['string']
        }]
    },
    'tag_info': {
        '/fleurInput': {
            'attribs': ['fleurInputVersion'],
            'optional': ['comment', 'constants', 'output'],
            'order':
            ['comment', 'constants', 'calculationSetup', 'cell', 'xcFunctional', 'atomSpecies', 'atomGroups', 'output'],
            'several': [],
            'simple': ['comment', 'calculationSetup', 'output'],
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
            'attribs': ['species', 'orbcomp', 'magField', 'vcaAddCharge'],
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
            'optional': ['energyParameters', 'force', 'electronConfig', 'nocoParams', 'ldaU', 'lo'],
            'order':
            ['mtSphere', 'atomicCutoffs', 'energyParameters', 'force', 'electronConfig', 'nocoParams', 'ldaU', 'lo'],
            'several': ['ldaU', 'lo'],
            'simple': ['mtSphere', 'atomicCutoffs', 'energyParameters', 'force', 'nocoParams', 'ldaU', 'lo'],
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
        '/fleurInput/calculationSetup': {
            'attribs': [],
            'optional': [
                'soc', 'nocoParams', 'oneDParams', 'expertModes', 'geometryOptimization', 'spinSpiralQPointMesh',
                'eField', 'energyParameterLimits'
            ],
            'order': [
                'cutoffs', 'scfLoop', 'coreElectrons', 'magnetism', 'bzIntegration', 'soc', 'nocoParams', 'oneDParams',
                'expertModes', 'geometryOptimization', 'spinSpiralQPointMesh', 'eField', 'energyParameterLimits'
            ],
            'several': [],
            'simple': [
                'cutoffs', 'scfLoop', 'coreElectrons', 'magnetism', 'soc', 'oneDParams', 'expertModes',
                'geometryOptimization', 'spinSpiralQPointMesh', 'eField', 'energyParameterLimits'
            ],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration': {
            'attribs': ['valenceElectrons', 'mode', 'fermiSmearingEnergy', 'fermiSmearingTemp'],
            'optional': [],
            'order': ['kPointMesh', 'kPointCount', 'kPointList'],
            'several': [],
            'simple': ['kPointMesh'],
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
            'attribs': ['ctail', 'frcor', 'kcrel'],
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
        '/fleurInput/calculationSetup/eField': {
            'attribs': ['zsigma', 'sig_b_1', 'sig_b_2', 'plot_charge', 'plot_rho', 'autocomp', 'dirichlet', 'eV'],
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
        '/fleurInput/calculationSetup/geometryOptimization': {
            'attribs': ['l_f', 'xa', 'thetad', 'epsdisp', 'epsforce', 'qfix'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/magnetism': {
            'attribs': ['jspins', 'l_noco', 'l_J', 'swsp', 'lflip'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/nocoParams': {
            'attribs': ['l_ss', 'l_mperp', 'l_constr', 'l_disp', 'sso_opt', 'mix_b', 'thetaJ', 'nsh'],
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
        '/fleurInput/calculationSetup/scfLoop': {
            'attribs': ['itmax', 'maxIterBroyd', 'imix', 'alpha', 'spinf', 'minDistance', 'maxTimeToStartIter'],
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
        '/fleurInput/cell/bulkLattice/bravaisMatrix': {
            'attribs': [],
            'optional': [],
            'order': ['row-1', 'row-2', 'row-3'],
            'several': [],
            'simple': ['row-1', 'row-2', 'row-3'],
            'text': ['row-1', 'row-2', 'row-3']
        },
        '/fleurInput/cell/filmLattice': {
            'attribs': ['scale', 'latnam', 'dVac', 'dTilda'],
            'optional': ['a2', 'vacuumEnergyParameters'],
            'order': ['a1', 'a2', 'row-1', 'row-2', 'bravaisMatrix', 'vacuumEnergyParameters'],
            'several': ['vacuumEnergyParameters'],
            'simple': ['a1', 'a2', 'row-1', 'row-2', 'vacuumEnergyParameters'],
            'text': ['a1', 'a2', 'row-1', 'row-2']
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
        '/fleurInput/output': {
            'attribs': ['dos', 'band', 'vacdos', 'slice'],
            'optional': ['checks', 'densityOfStates', 'vacuumDOS', 'plotting', 'chargeDensitySlicing', 'specialOutput'],
            'order': ['checks', 'densityOfStates', 'vacuumDOS', 'plotting', 'chargeDensitySlicing', 'specialOutput'],
            'several': [],
            'simple': ['checks', 'densityOfStates', 'vacuumDOS', 'plotting', 'chargeDensitySlicing', 'specialOutput'],
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
        '/fleurInput/output/densityOfStates': {
            'attribs': ['ndir', 'minEnergy', 'maxEnergy', 'sigma'],
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
        '/fleurInput/output/vacuumDOS': {
            'attribs': ['layers', 'integ', 'star', 'nstars', 'locx1', 'locy1', 'locx2', 'locy2', 'nstm', 'tworkf'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/xcFunctional': {
            'attribs': ['name', 'relativisticCorrections'],
            'optional': ['xcParams', 'ggaPrinting'],
            'order': ['xcParams', 'ggaPrinting'],
            'several': [],
            'simple': ['xcParams', 'ggaPrinting'],
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
        'a1': ['/fleurInput/cell/bulkLattice/a1', '/fleurInput/cell/filmLattice/a1'],
        'a2': ['/fleurInput/cell/bulkLattice/a2', '/fleurInput/cell/filmLattice/a2'],
        'absPos':
        '/fleurInput/atomGroups/atomGroup/absPos',
        'atomGroup':
        '/fleurInput/atomGroups/atomGroup',
        'atomGroups':
        '/fleurInput/atomGroups',
        'atomSpecies':
        '/fleurInput/atomSpecies',
        'atomicCutoffs':
        ['/fleurInput/atomSpecies/species/atomicCutoffs', '/fleurInput/atomGroups/atomGroup/atomicCutoffs'],
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
        'cutoffs':
        '/fleurInput/calculationSetup/cutoffs',
        'densityOfStates':
        '/fleurInput/output/densityOfStates',
        'eField':
        '/fleurInput/calculationSetup/eField',
        'electronConfig':
        '/fleurInput/atomSpecies/species/electronConfig',
        'energyParameterLimits':
        '/fleurInput/calculationSetup/energyParameterLimits',
        'energyParameters':
        ['/fleurInput/atomSpecies/species/energyParameters', '/fleurInput/atomGroups/atomGroup/energyParameters'],
        'expertModes':
        '/fleurInput/calculationSetup/expertModes',
        'filmLattice':
        '/fleurInput/cell/filmLattice',
        'filmPos':
        '/fleurInput/atomGroups/atomGroup/filmPos',
        'fleurInput':
        '/fleurInput',
        'force': ['/fleurInput/atomSpecies/species/force', '/fleurInput/atomGroups/atomGroup/force'],
        'geometryOptimization':
        '/fleurInput/calculationSetup/geometryOptimization',
        'ggaPrinting':
        '/fleurInput/xcFunctional/ggaPrinting',
        'kPoint':
        '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint',
        'kPointCount':
        '/fleurInput/calculationSetup/bzIntegration/kPointCount',
        'kPointList':
        '/fleurInput/calculationSetup/bzIntegration/kPointList',
        'kPointMesh':
        '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
        'ldaU': ['/fleurInput/atomSpecies/species/ldaU', '/fleurInput/atomGroups/atomGroup/ldaU'],
        'lo': ['/fleurInput/atomSpecies/species/lo', '/fleurInput/atomGroups/atomGroup/lo'],
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
        'qsc':
        '/fleurInput/calculationSetup/nocoParams/qsc',
        'qss':
        '/fleurInput/calculationSetup/nocoParams/qss',
        'relPos':
        '/fleurInput/atomGroups/atomGroup/relPos',
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
        'soc':
        '/fleurInput/calculationSetup/soc',
        'specialOutput':
        '/fleurInput/output/specialOutput',
        'specialPoint':
        '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint',
        'species':
        '/fleurInput/atomSpecies/species',
        'spinSpiralQPointMesh':
        '/fleurInput/calculationSetup/spinSpiralQPointMesh',
        'stateOccupation':
        '/fleurInput/atomSpecies/species/electronConfig/stateOccupation',
        'symOp':
        '/fleurInput/cell/symmetryOperations/symOp',
        'symmetry':
        '/fleurInput/cell/symmetry',
        'symmetryFile':
        '/fleurInput/cell/symmetryFile',
        'symmetryOperations':
        '/fleurInput/cell/symmetryOperations',
        'vacuumDOS':
        '/fleurInput/output/vacuumDOS',
        'vacuumEnergyParameters':
        '/fleurInput/cell/filmLattice/vacuumEnergyParameters',
        'valenceConfig':
        '/fleurInput/atomSpecies/species/electronConfig/valenceConfig',
        'xcFunctional':
        '/fleurInput/xcFunctional',
        'xcParams':
        '/fleurInput/xcFunctional/xcParams'
    }
}
