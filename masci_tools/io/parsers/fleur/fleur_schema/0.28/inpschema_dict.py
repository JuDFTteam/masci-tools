# -*- coding: utf-8 -*-
__inp_version__ = '0.28'
schema_dict = {
    'attrib_types': {
        'Gmax': ['string'],
        'GmaxXC': ['string'],
        'J': ['string'],
        'Kmax': ['string'],
        'M': ['string'],
        'MM': ['int'],
        'U': ['string'],
        'alpha': ['string'],
        'atomList': ['switch'],
        'atomType': ['int'],
        'atomicNumber': ['int'],
        'autocomp': ['switch'],
        'b_cons_x': ['string'],
        'b_cons_y': ['string'],
        'band': ['switch'],
        'bands': ['int'],
        'beta': ['string'],
        'bmt': ['switch'],
        'bsComf': ['switch'],
        'calculate': ['switch'],
        'cdinf': ['switch'],
        'chi': ['int'],
        'chng': ['float'],
        'coreSpec': ['switch'],
        'coreStates': ['int'],
        'coretail_lmax': ['int'],
        'correlation': ['int'],
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
        'energyLo': ['float'],
        'energyUp': ['float'],
        'eonly': ['switch'],
        'epsdisp': ['string'],
        'epsforce': ['string'],
        'ewaldlambda': ['int'],
        'exchange': ['int'],
        'f': ['int'],
        'fermiSmearingEnergy': ['string'],
        'fermiSmearingTemp': ['string'],
        'filename': ['string'],
        'fleurInputVersion': ['string'],
        'flipSpin': ['switch'],
        'form66': ['switch'],
        'frcor': ['switch'],
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
        'l_noco': ['switch'],
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
        'nsh': ['int'],
        'nstars': ['int'],
        'nstm': ['int'],
        'numPoints': ['int'],
        'numbands': ['int', 'string'],
        'numkpt': ['int'],
        'nx': ['int'],
        'ny': ['int'],
        'nz': ['int'],
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
        'qfix': ['switch'],
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
        'supercellX': ['int'],
        'supercellY': ['int'],
        'supercellZ': ['int'],
        'swsp': ['switch'],
        'theta': ['string'],
        'thetaJ': ['string'],
        'thetad': ['string'],
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
        'vchk': ['switch'],
        'verbose': ['switch'],
        'wannier': ['switch'],
        'weight': ['string'],
        'weightScale': ['string'],
        'xa': ['string'],
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
    'omitt_contained_tags':
    ['constants', 'atomSpecies', 'atomGroups', 'symmetryOperations', 'spinSpiralDispersion', 'qVectors'],
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
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint'
        ],
        'orbcomp': [
            '/fleurInput/atomGroups/atomGroup/relPos', '/fleurInput/atomGroups/atomGroup/absPos',
            '/fleurInput/atomGroups/atomGroup/filmPos'
        ],
        'orbcomprot': ['/fleurInput/atomGroups/atomGroup/orbcomprot'],
        'p': ['/fleurInput/atomSpecies/species/energyParameters', '/fleurInput/atomGroups/atomGroup/energyParameters'],
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
        'socscale': ['/fleurInput/atomSpecies/species/special'],
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
        'wannier': [
            '/fleurInput/atomGroups/atomGroup/relPos', '/fleurInput/atomGroups/atomGroup/absPos',
            '/fleurInput/atomGroups/atomGroup/filmPos'
        ],
        'weight': ['/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint']
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
            'optional': ['comment', 'constants', 'output', 'forceTheorem'],
            'order': [
                'comment', 'constants', 'calculationSetup', 'cell', 'xcFunctional', 'atomSpecies', 'atomGroups',
                'output', 'forceTheorem'
            ],
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
            'attribs': ['lda', 'socscale'],
            'optional': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup': {
            'attribs': [],
            'optional': [
                'prodBasis', 'soc', 'nocoParams', 'oneDParams', 'expertModes', 'geometryOptimization', 'ldaU',
                'spinSpiralQPointMesh', 'eField', 'energyParameterLimits'
            ],
            'order': [
                'cutoffs', 'scfLoop', 'coreElectrons', 'magnetism', 'bzIntegration', 'prodBasis', 'soc', 'nocoParams',
                'oneDParams', 'expertModes', 'geometryOptimization', 'ldaU', 'spinSpiralQPointMesh', 'eField',
                'energyParameterLimits'
            ],
            'several': [],
            'simple': [
                'cutoffs', 'scfLoop', 'coreElectrons', 'magnetism', 'prodBasis', 'soc', 'oneDParams', 'expertModes',
                'geometryOptimization', 'ldaU', 'spinSpiralQPointMesh', 'eField', 'energyParameterLimits'
            ],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration': {
            'attribs': ['valenceElectrons', 'mode', 'fermiSmearingEnergy', 'fermiSmearingTemp'],
            'optional': [],
            'order': ['kPointMesh', 'kPointCount', 'kPointList', 'kPointDensity'],
            'several': [],
            'simple': ['kPointMesh', 'kPointDensity'],
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
        '/fleurInput/calculationSetup/ldaU': {
            'attribs': ['l_linMix', 'mixParam', 'spinf'],
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
        '/fleurInput/calculationSetup/prodBasis': {
            'attribs': ['gcutm', 'bands', 'tolerance', 'lexp', 'ewaldlambda'],
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
            'attribs': ['eKin', 'atomType', 'lmax', 'edgeType', 'eMin', 'eMax', 'numPoints', 'verbose'],
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
        '/fleurInput/xcFunctional': {
            'attribs': ['name', 'relativisticCorrections'],
            'optional': ['libXC', 'xcParams', 'ggaPrinting'],
            'order': ['libXC', 'xcParams', 'ggaPrinting'],
            'several': [],
            'simple': ['libXC', 'xcParams', 'ggaPrinting'],
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
        '/fleurInput/xcFunctional/libXC': {
            'attribs': ['exchange', 'correlation'],
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
        'MAE':
        '/fleurInput/forceTheorem/MAE',
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
        'eField':
        '/fleurInput/calculationSetup/eField',
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
        'kPoint':
        '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint',
        'kPointCount':
        '/fleurInput/calculationSetup/bzIntegration/kPointCount',
        'kPointDensity':
        '/fleurInput/calculationSetup/bzIntegration/kPointDensity',
        'kPointList':
        '/fleurInput/calculationSetup/bzIntegration/kPointList',
        'kPointMesh':
        '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
        'ldaU': [
            '/fleurInput/calculationSetup/ldaU', '/fleurInput/atomSpecies/species/ldaU',
            '/fleurInput/atomGroups/atomGroup/ldaU'
        ],
        'libXC':
        '/fleurInput/xcFunctional/libXC',
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
        'special':
        '/fleurInput/atomSpecies/species/special',
        'specialOutput':
        '/fleurInput/output/specialOutput',
        'specialPoint':
        '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint',
        'species':
        '/fleurInput/atomSpecies/species',
        'spinSpiralDispersion':
        '/fleurInput/forceTheorem/spinSpiralDispersion',
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
    },
    'unique_attribs': {
        'Gmax': '/fleurInput/calculationSetup/cutoffs',
        'GmaxXC': '/fleurInput/calculationSetup/cutoffs',
        'Kmax': '/fleurInput/calculationSetup/cutoffs',
        'MM': '/fleurInput/calculationSetup/oneDParams',
        'alpha': '/fleurInput/calculationSetup/scfLoop',
        'atomList': '/fleurInput/output/wannier',
        'atomType': '/fleurInput/output/coreSpectrum',
        'autocomp': '/fleurInput/calculationSetup/eField',
        'band': '/fleurInput/output',
        'bands': '/fleurInput/calculationSetup/prodBasis',
        'bmt': '/fleurInput/output/specialOutput',
        'bsComf': '/fleurInput/output/wannier',
        'c': '/fleurInput/cell/bulkLattice/c',
        'cdinf': '/fleurInput/output/checks',
        'chi': '/fleurInput/calculationSetup/oneDParams',
        'chng': '/fleurInput/xcFunctional/xcParams',
        'comment': '/fleurInput/comment',
        'coreSpec': '/fleurInput/output',
        'coretail_lmax': '/fleurInput/calculationSetup/coreElectrons',
        'correlation': '/fleurInput/xcFunctional/libXC',
        'ctail': '/fleurInput/calculationSetup/coreElectrons',
        'd1': '/fleurInput/calculationSetup/oneDParams',
        'dTilda': '/fleurInput/cell/filmLattice',
        'dVac': '/fleurInput/cell/filmLattice',
        'denX': '/fleurInput/calculationSetup/bzIntegration/kPointDensity',
        'denY': '/fleurInput/calculationSetup/bzIntegration/kPointDensity',
        'denZ': '/fleurInput/calculationSetup/bzIntegration/kPointDensity',
        'dirichlet': '/fleurInput/calculationSetup/eField',
        'disp': '/fleurInput/output/checks',
        'dos': '/fleurInput/output',
        'eKin': '/fleurInput/output/coreSpectrum',
        'eMax': '/fleurInput/output/coreSpectrum',
        'eMin': '/fleurInput/output/coreSpectrum',
        'eV': '/fleurInput/calculationSetup/eField',
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
        'exchange': '/fleurInput/xcFunctional/libXC',
        'fermiSmearingEnergy': '/fleurInput/calculationSetup/bzIntegration',
        'fermiSmearingTemp': '/fleurInput/calculationSetup/bzIntegration',
        'filename': '/fleurInput/cell/symmetryFile',
        'fleurInputVersion': '/fleurInput',
        'form66': '/fleurInput/output/specialOutput',
        'frcor': '/fleurInput/calculationSetup/coreElectrons',
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
        'l_noco': '/fleurInput/calculationSetup/magnetism',
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
        'nsh': '/fleurInput/calculationSetup/nocoParams',
        'nstars': '/fleurInput/output/vacuumDOS',
        'nstm': '/fleurInput/output/vacuumDOS',
        'numPoints': '/fleurInput/output/coreSpectrum',
        'numbands': '/fleurInput/calculationSetup/cutoffs',
        'numkpt': '/fleurInput/output/chargeDensitySlicing',
        'nx': '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
        'ny': '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
        'nz': '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
        'off': '/fleurInput/calculationSetup/soc',
        'pallst': '/fleurInput/output/chargeDensitySlicing',
        'plot_charge': '/fleurInput/calculationSetup/eField',
        'plot_rho': '/fleurInput/calculationSetup/eField',
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
        'sig_b_1': '/fleurInput/calculationSetup/eField',
        'sig_b_2': '/fleurInput/calculationSetup/eField',
        'sigma': '/fleurInput/output/densityOfStates',
        'slice': '/fleurInput/output',
        'soc66': '/fleurInput/calculationSetup/soc',
        'socgwf': '/fleurInput/output/wannier',
        'spav': '/fleurInput/calculationSetup/soc',
        'spgrp': '/fleurInput/cell/symmetry',
        'sso_opt': '/fleurInput/calculationSetup/nocoParams',
        'star': '/fleurInput/output/vacuumDOS',
        'supercellX': '/fleurInput/output/unfoldingBand',
        'supercellY': '/fleurInput/output/unfoldingBand',
        'supercellZ': '/fleurInput/output/unfoldingBand',
        'swsp': '/fleurInput/calculationSetup/magnetism',
        'thetaJ': '/fleurInput/calculationSetup/nocoParams',
        'thetad': '/fleurInput/calculationSetup/geometryOptimization',
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
        'xa': '/fleurInput/calculationSetup/geometryOptimization',
        'zrfs': '/fleurInput/cell/symmetry',
        'zrfs1': '/fleurInput/calculationSetup/oneDParams',
        'zsigma': '/fleurInput/calculationSetup/eField'
    },
    'unique_path_attribs': {
        'a1': ['/fleurInput/cell/bulkLattice/a1', '/fleurInput/cell/filmLattice/a1'],
        'a2': ['/fleurInput/cell/bulkLattice/a2', '/fleurInput/cell/filmLattice/a2'],
        'count': [
            '/fleurInput/calculationSetup/bzIntegration/kPointCount',
            '/fleurInput/calculationSetup/bzIntegration/kPointList'
        ],
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
    }
}
