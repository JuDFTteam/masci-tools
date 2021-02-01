# -*- coding: utf-8 -*-
"""
This file contains information parsed from the FleurInputSchema.xsd
for version 0.28

The keys contain the following information:

    - 'inp_version': Version string of the input schema represented in this file
    - 'tag_paths': simple xpath expressions to all valid tag names
                   Multiple paths or ambiguous tag names are parsed as a list
    - '_basic_types': Parsed definitions of all simple Types with their respective
                      base type (int, float, ...) and evtl. length restrictions
                     (Only used in the schema construction itself)
    - 'attrib_types': All possible base types for all valid attributes. If multiple are
                      possible a list, with 'string' always last (if possible)
    - 'simple_elements': All elements with simple types and their type definition
                         with the additional attributes
    - 'unique_attribs': All attributes and their paths, which occur only once and
                        have a unique path
    - 'unique_path_attribs': All attributes and their paths, which have a unique path
                             but occur in multiple places
    - 'other_attribs': All attributes and their paths, which are not in 'unique_attribs' or
                       'unique_path_attribs'
    - 'omitt_contained_tags': All tags, which only contain a list of one other tag
    - 'tag_info': For each tag (path), the valid attributes and tags (optional, several,
                  order, simple, text)
"""
from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict
__inp_version__ = '0.28'
schema_dict = {
    '_basic_types': {
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
    'inp_version':
    '0.28',
    'omitt_contained_tags':
    ['constants', 'atomSpecies', 'atomGroups', 'symmetryOperations', 'spinSpiralDispersion', 'qVectors'],
    'other_attribs':
    CaseInsensitiveDict({
        'corestates': ['/fleurInput/atomSpecies/species/@coreStates'],
        'radius':
        ['/fleurInput/atomGroups/atomGroup/mtSphere/@radius', '/fleurInput/atomSpecies/species/mtSphere/@radius'],
        'wannier': [
            '/fleurInput/atomGroups/atomGroup/absPos/@wannier', '/fleurInput/atomGroups/atomGroup/filmPos/@wannier',
            '/fleurInput/atomGroups/atomGroup/relPos/@wannier'
        ],
        'flipspin': ['/fleurInput/atomSpecies/species/@flipSpin'],
        'lda': ['/fleurInput/atomSpecies/species/special/@lda'],
        'l_amf': ['/fleurInput/atomGroups/atomGroup/ldaU/@l_amf', '/fleurInput/atomSpecies/species/ldaU/@l_amf'],
        'l_magn':
        ['/fleurInput/atomGroups/atomGroup/nocoParams/@l_magn', '/fleurInput/atomSpecies/species/nocoParams/@l_magn'],
        'logincrement': [
            '/fleurInput/atomGroups/atomGroup/mtSphere/@logIncrement',
            '/fleurInput/atomSpecies/species/mtSphere/@logIncrement'
        ],
        'orbcomp': [
            '/fleurInput/atomGroups/atomGroup/absPos/@orbcomp', '/fleurInput/atomGroups/atomGroup/filmPos/@orbcomp',
            '/fleurInput/atomGroups/atomGroup/relPos/@orbcomp'
        ],
        'species': ['/fleurInput/atomGroups/atomGroup/@species'],
        'value': ['/fleurInput/constants/constant/@value'],
        'f':
        ['/fleurInput/atomGroups/atomGroup/energyParameters/@f', '/fleurInput/atomSpecies/species/energyParameters/@f'],
        'socscale': ['/fleurInput/atomSpecies/species/special/@socscale'],
        'b_cons_y': [
            '/fleurInput/atomGroups/atomGroup/nocoParams/@b_cons_y',
            '/fleurInput/atomSpecies/species/nocoParams/@b_cons_y'
        ],
        'spindown': [
            '/fleurInput/atomSpecies/species/electronConfig/stateOccupation/@spinDown',
            '/fleurInput/cell/filmLattice/vacuumEnergyParameters/@spinDown'
        ],
        'vcaaddcharge':
        ['/fleurInput/atomGroups/atomGroup/@vcaAddCharge', '/fleurInput/atomSpecies/species/@vcaAddCharge'],
        'lmaxapw': [
            '/fleurInput/atomGroups/atomGroup/atomicCutoffs/@lmaxAPW',
            '/fleurInput/atomSpecies/species/atomicCutoffs/@lmaxAPW'
        ],
        'u': ['/fleurInput/atomGroups/atomGroup/ldaU/@U', '/fleurInput/atomSpecies/species/ldaU/@U'],
        'spinup': [
            '/fleurInput/atomSpecies/species/electronConfig/stateOccupation/@spinUp',
            '/fleurInput/cell/filmLattice/vacuumEnergyParameters/@spinUp'
        ],
        'select': ['/fleurInput/atomSpecies/species/prodBasis/@select'],
        'b_cons_x': [
            '/fleurInput/atomGroups/atomGroup/nocoParams/@b_cons_x',
            '/fleurInput/atomSpecies/species/nocoParams/@b_cons_x'
        ],
        'calculate':
        ['/fleurInput/atomGroups/atomGroup/force/@calculate', '/fleurInput/atomSpecies/species/force/@calculate'],
        'l_relax':
        ['/fleurInput/atomGroups/atomGroup/nocoParams/@l_relax', '/fleurInput/atomSpecies/species/nocoParams/@l_relax'],
        'beta':
        ['/fleurInput/atomGroups/atomGroup/nocoParams/@beta', '/fleurInput/atomSpecies/species/nocoParams/@beta'],
        'p':
        ['/fleurInput/atomGroups/atomGroup/energyParameters/@p', '/fleurInput/atomSpecies/species/energyParameters/@p'],
        'magfield': ['/fleurInput/atomGroups/atomGroup/@magField', '/fleurInput/atomSpecies/species/@magField'],
        'relaxxyz':
        ['/fleurInput/atomGroups/atomGroup/force/@relaxXYZ', '/fleurInput/atomSpecies/species/force/@relaxXYZ'],
        's':
        ['/fleurInput/atomGroups/atomGroup/energyParameters/@s', '/fleurInput/atomSpecies/species/energyParameters/@s'],
        'type': ['/fleurInput/atomGroups/atomGroup/lo/@type', '/fleurInput/atomSpecies/species/lo/@type'],
        'name': [
            '/fleurInput/atomSpecies/species/@name',
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint/@name',
            '/fleurInput/constants/constant/@name'
        ],
        'element': ['/fleurInput/atomSpecies/species/@element'],
        'alpha':
        ['/fleurInput/atomGroups/atomGroup/nocoParams/@alpha', '/fleurInput/atomSpecies/species/nocoParams/@alpha'],
        'm': ['/fleurInput/atomGroups/atomGroup/nocoParams/@M', '/fleurInput/atomSpecies/species/nocoParams/@M'],
        'j': ['/fleurInput/atomGroups/atomGroup/ldaU/@J', '/fleurInput/atomSpecies/species/ldaU/@J'],
        'atomicnumber': ['/fleurInput/atomSpecies/species/@atomicNumber'],
        'magmom': ['/fleurInput/atomSpecies/species/@magMom'],
        'weight': ['/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint/@weight'],
        'vacuum': ['/fleurInput/cell/filmLattice/vacuumEnergyParameters/@vacuum'],
        'gridpoints': [
            '/fleurInput/atomGroups/atomGroup/mtSphere/@gridPoints',
            '/fleurInput/atomSpecies/species/mtSphere/@gridPoints'
        ],
        'l': [
            '/fleurInput/atomGroups/atomGroup/ldaU/@l', '/fleurInput/atomGroups/atomGroup/lo/@l',
            '/fleurInput/atomSpecies/species/ldaU/@l', '/fleurInput/atomSpecies/species/lo/@l'
        ],
        'lnonsphr': [
            '/fleurInput/atomGroups/atomGroup/atomicCutoffs/@lnonsphr',
            '/fleurInput/atomSpecies/species/atomicCutoffs/@lnonsphr'
        ],
        'ederiv': ['/fleurInput/atomGroups/atomGroup/lo/@eDeriv', '/fleurInput/atomSpecies/species/lo/@eDeriv'],
        'label': [
            '/fleurInput/atomGroups/atomGroup/absPos/@label', '/fleurInput/atomGroups/atomGroup/filmPos/@label',
            '/fleurInput/atomGroups/atomGroup/relPos/@label'
        ],
        'state': ['/fleurInput/atomSpecies/species/electronConfig/stateOccupation/@state'],
        'd':
        ['/fleurInput/atomGroups/atomGroup/energyParameters/@d', '/fleurInput/atomSpecies/species/energyParameters/@d'],
        'lcutm': ['/fleurInput/atomSpecies/species/prodBasis/@lcutm'],
        'lcutwf': ['/fleurInput/atomSpecies/species/prodBasis/@lcutwf'],
        'lmax':
        ['/fleurInput/atomGroups/atomGroup/atomicCutoffs/@lmax', '/fleurInput/atomSpecies/species/atomicCutoffs/@lmax'],
        'n': ['/fleurInput/atomGroups/atomGroup/lo/@n', '/fleurInput/atomSpecies/species/lo/@n'],
        'row-1': ['/fleurInput/cell/symmetryOperations/symOp/row-1'],
        'row-2': ['/fleurInput/cell/symmetryOperations/symOp/row-2'],
        'row-3': ['/fleurInput/cell/symmetryOperations/symOp/row-3'],
        'relpos': ['/fleurInput/atomGroups/atomGroup/relPos'],
        'abspos': ['/fleurInput/atomGroups/atomGroup/absPos'],
        'filmpos': ['/fleurInput/atomGroups/atomGroup/filmPos'],
        'orbcomprot': ['/fleurInput/atomGroups/atomGroup/orbcomprot'],
        'specialpoint': ['/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint'],
        'kpoint': ['/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint'],
        'q': [
            '/fleurInput/forceTheorem/DMI/qVectors/q', '/fleurInput/forceTheorem/Jij/qVectors/q',
            '/fleurInput/forceTheorem/spinSpiralDispersion/q'
        ],
        'coreconfig': ['/fleurInput/atomSpecies/species/electronConfig/coreConfig'],
        'valenceconfig': ['/fleurInput/atomSpecies/species/electronConfig/valenceConfig']
    }),
    'root_tag':
    'fleurInput',
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
            'optional_attribs': [],
            'order': [
                'comment', 'constants', 'calculationSetup', 'cell', 'xcFunctional', 'atomSpecies', 'atomGroups',
                'output', 'forceTheorem'
            ],
            'several': [],
            'simple': ['comment'],
            'text': ['comment']
        },
        '/fleurInput/atomGroups': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['atomGroup'],
            'several': ['atomGroup'],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup': {
            'attribs': ['species', 'magField', 'vcaAddCharge'],
            'optional':
            ['mtSphere', 'atomicCutoffs', 'energyParameters', 'force', 'nocoParams', 'ldaU', 'lo', 'orbcomprot'],
            'optional_attribs': ['magField', 'vcaAddCharge'],
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
            'optional_attribs': ['label', 'wannier', 'orbcomp'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/atomicCutoffs': {
            'attribs': ['lmax', 'lnonsphr', 'lmaxAPW'],
            'optional': [],
            'optional_attribs': ['lmaxAPW'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/energyParameters': {
            'attribs': ['s', 'p', 'd', 'f'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/filmPos': {
            'attribs': ['label', 'wannier', 'orbcomp'],
            'optional': [],
            'optional_attribs': ['label', 'wannier', 'orbcomp'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/force': {
            'attribs': ['calculate', 'relaxXYZ'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/ldaU': {
            'attribs': ['l', 'U', 'J', 'l_amf'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/lo': {
            'attribs': ['type', 'l', 'n', 'eDeriv'],
            'optional': [],
            'optional_attribs': ['eDeriv'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/mtSphere': {
            'attribs': ['radius', 'gridPoints', 'logIncrement'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/nocoParams': {
            'attribs': ['l_relax', 'l_magn', 'M', 'alpha', 'beta', 'b_cons_x', 'b_cons_y'],
            'optional': [],
            'optional_attribs': ['l_magn', 'M'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/relPos': {
            'attribs': ['label', 'wannier', 'orbcomp'],
            'optional': [],
            'optional_attribs': ['label', 'wannier', 'orbcomp'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
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
            'optional_attribs': ['magMom', 'flipSpin', 'magField', 'vcaAddCharge'],
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
            'optional_attribs': ['lmaxAPW'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/electronConfig': {
            'attribs': [],
            'optional': ['valenceConfig', 'stateOccupation'],
            'optional_attribs': [],
            'order': ['coreConfig', 'valenceConfig', 'stateOccupation'],
            'several': ['stateOccupation'],
            'simple': ['coreConfig', 'valenceConfig', 'stateOccupation'],
            'text': ['coreConfig', 'valenceConfig']
        },
        '/fleurInput/atomSpecies/species/electronConfig/stateOccupation': {
            'attribs': ['state', 'spinUp', 'spinDown'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/energyParameters': {
            'attribs': ['s', 'p', 'd', 'f'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/force': {
            'attribs': ['calculate', 'relaxXYZ'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/ldaU': {
            'attribs': ['l', 'U', 'J', 'l_amf'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/lo': {
            'attribs': ['type', 'l', 'n', 'eDeriv'],
            'optional': [],
            'optional_attribs': ['eDeriv'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/mtSphere': {
            'attribs': ['radius', 'gridPoints', 'logIncrement'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/nocoParams': {
            'attribs': ['l_relax', 'l_magn', 'M', 'alpha', 'beta', 'b_cons_x', 'b_cons_y'],
            'optional': [],
            'optional_attribs': ['l_magn', 'M'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/prodBasis': {
            'attribs': ['lcutm', 'lcutwf', 'select'],
            'optional': [],
            'optional_attribs': ['select'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/special': {
            'attribs': ['lda', 'socscale'],
            'optional': [],
            'optional_attribs': ['lda', 'socscale'],
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
            'optional_attribs': [],
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
            'optional_attribs': ['valenceElectrons', 'mode', 'fermiSmearingEnergy', 'fermiSmearingTemp'],
            'order': ['kPointMesh', 'kPointCount', 'kPointList', 'kPointDensity'],
            'several': [],
            'simple': ['kPointMesh', 'kPointDensity'],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointCount': {
            'attribs': ['count', 'gamma'],
            'optional': ['specialPoint'],
            'optional_attribs': [],
            'order': ['specialPoint'],
            'several': ['specialPoint'],
            'simple': ['specialPoint'],
            'text': ['specialPoint']
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint': {
            'attribs': ['name'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointDensity': {
            'attribs': ['denX', 'denY', 'denZ', 'gamma'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointList': {
            'attribs': ['posScale', 'weightScale', 'count'],
            'optional': [],
            'optional_attribs': ['count'],
            'order': ['kPoint'],
            'several': ['kPoint'],
            'simple': ['kPoint'],
            'text': ['kPoint']
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint': {
            'attribs': ['weight'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointMesh': {
            'attribs': ['nx', 'ny', 'nz', 'gamma'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/coreElectrons': {
            'attribs': ['ctail', 'frcor', 'kcrel', 'coretail_lmax'],
            'optional': [],
            'optional_attribs': ['frcor', 'kcrel', 'coretail_lmax'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/cutoffs': {
            'attribs': ['Kmax', 'Gmax', 'GmaxXC', 'numbands'],
            'optional': [],
            'optional_attribs': ['GmaxXC', 'numbands'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/eField': {
            'attribs': ['zsigma', 'sig_b_1', 'sig_b_2', 'plot_charge', 'plot_rho', 'autocomp', 'dirichlet', 'eV'],
            'optional': [],
            'optional_attribs':
            ['zsigma', 'sig_b_1', 'sig_b_2', 'plot_charge', 'plot_rho', 'autocomp', 'dirichlet', 'eV'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/energyParameterLimits': {
            'attribs': ['ellow', 'elup'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/expertModes': {
            'attribs': ['gw', 'pot8', 'eig66', 'lpr', 'isec1', 'secvar'],
            'optional': [],
            'optional_attribs': ['gw', 'pot8', 'eig66', 'lpr', 'isec1', 'secvar'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/geometryOptimization': {
            'attribs': ['l_f', 'xa', 'thetad', 'epsdisp', 'epsforce', 'qfix'],
            'optional': [],
            'optional_attribs': ['qfix'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/ldaU': {
            'attribs': ['l_linMix', 'mixParam', 'spinf'],
            'optional': [],
            'optional_attribs': ['l_linMix', 'mixParam', 'spinf'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/magnetism': {
            'attribs': ['jspins', 'l_noco', 'l_J', 'swsp', 'lflip'],
            'optional': [],
            'optional_attribs': ['l_noco', 'l_J', 'swsp', 'lflip'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/nocoParams': {
            'attribs': ['l_ss', 'l_mperp', 'l_constr', 'l_disp', 'sso_opt', 'mix_b', 'thetaJ', 'nsh'],
            'optional': ['qsc'],
            'optional_attribs': ['l_disp', 'thetaJ', 'nsh'],
            'order': ['qss', 'qsc'],
            'several': [],
            'simple': ['qss', 'qsc'],
            'text': ['qss', 'qsc']
        },
        '/fleurInput/calculationSetup/oneDParams': {
            'attribs': ['d1', 'MM', 'vM', 'm_cyl', 'chi', 'rot', 'invs1', 'zrfs1'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/prodBasis': {
            'attribs': ['gcutm', 'bands', 'tolerance', 'lexp', 'ewaldlambda'],
            'optional': [],
            'optional_attribs': ['tolerance', 'lexp', 'ewaldlambda'],
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
            'optional_attribs': ['maxIterBroyd', 'preconditioning_param', 'spinf', 'minDistance', 'maxTimeToStartIter'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/soc': {
            'attribs': ['theta', 'phi', 'l_soc', 'spav', 'off', 'soc66'],
            'optional': [],
            'optional_attribs': ['off', 'soc66'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/spinSpiralQPointMesh': {
            'attribs': ['qx', 'qy', 'qz'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['symmetry', 'symmetryFile', 'symmetryOperations', 'bulkLattice', 'filmLattice'],
            'several': [],
            'simple': ['symmetry', 'symmetryFile'],
            'text': []
        },
        '/fleurInput/cell/bulkLattice': {
            'attribs': ['scale', 'latnam'],
            'optional': ['a2'],
            'optional_attribs': [],
            'order': ['a1', 'a2', 'c', 'row-1', 'row-2', 'c', 'bravaisMatrix'],
            'several': [],
            'simple': ['a1', 'a2', 'c', 'row-1', 'row-2', 'c'],
            'text': ['a1', 'a2', 'c', 'row-1', 'row-2', 'c']
        },
        '/fleurInput/cell/bulkLattice/a1': {
            'attribs': ['scale'],
            'optional': [],
            'optional_attribs': ['scale'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/bulkLattice/a2': {
            'attribs': ['scale'],
            'optional': [],
            'optional_attribs': ['scale'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/bulkLattice/bravaisMatrix': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['row-1', 'row-2', 'row-3'],
            'several': [],
            'simple': ['row-1', 'row-2', 'row-3'],
            'text': ['row-1', 'row-2', 'row-3']
        },
        '/fleurInput/cell/bulkLattice/c': {
            'attribs': ['scale'],
            'optional': [],
            'optional_attribs': ['scale'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/filmLattice': {
            'attribs': ['scale', 'latnam', 'dVac', 'dTilda'],
            'optional': ['a2', 'vacuumEnergyParameters'],
            'optional_attribs': [],
            'order': ['a1', 'a2', 'row-1', 'row-2', 'bravaisMatrix', 'vacuumEnergyParameters'],
            'several': ['vacuumEnergyParameters'],
            'simple': ['a1', 'a2', 'row-1', 'row-2', 'vacuumEnergyParameters'],
            'text': ['a1', 'a2', 'row-1', 'row-2']
        },
        '/fleurInput/cell/filmLattice/a1': {
            'attribs': ['scale'],
            'optional': [],
            'optional_attribs': ['scale'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/filmLattice/a2': {
            'attribs': ['scale'],
            'optional': [],
            'optional_attribs': ['scale'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/filmLattice/bravaisMatrix': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['row-1', 'row-2', 'row-3'],
            'several': [],
            'simple': ['row-1', 'row-2', 'row-3'],
            'text': ['row-1', 'row-2', 'row-3']
        },
        '/fleurInput/cell/filmLattice/vacuumEnergyParameters': {
            'attribs': ['vacuum', 'spinUp', 'spinDown'],
            'optional': [],
            'optional_attribs': ['spinDown'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/symmetry': {
            'attribs': ['spgrp', 'invs', 'zrfs'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/symmetryFile': {
            'attribs': ['filename'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/symmetryOperations': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['symOp'],
            'several': ['symOp'],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/symmetryOperations/symOp': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['row-1', 'row-2', 'row-3'],
            'several': [],
            'simple': ['row-1', 'row-2', 'row-3'],
            'text': ['row-1', 'row-2', 'row-3']
        },
        '/fleurInput/constants': {
            'attribs': [],
            'optional': ['constant'],
            'optional_attribs': [],
            'order': ['constant'],
            'several': ['constant'],
            'simple': ['constant'],
            'text': []
        },
        '/fleurInput/constants/constant': {
            'attribs': ['name', 'value'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/forceTheorem': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['MAE', 'spinSpiralDispersion', 'DMI', 'Jij'],
            'several': [],
            'simple': ['MAE'],
            'text': []
        },
        '/fleurInput/forceTheorem/DMI': {
            'attribs': ['theta', 'phi'],
            'optional': [],
            'optional_attribs': [],
            'order': ['qVectors'],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/forceTheorem/DMI/qVectors': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['q'],
            'several': ['q'],
            'simple': ['q'],
            'text': ['q']
        },
        '/fleurInput/forceTheorem/Jij': {
            'attribs': ['thetaj'],
            'optional': [],
            'optional_attribs': [],
            'order': ['qVectors'],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/forceTheorem/Jij/qVectors': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['q'],
            'several': ['q'],
            'simple': ['q'],
            'text': ['q']
        },
        '/fleurInput/forceTheorem/MAE': {
            'attribs': ['theta', 'phi'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/forceTheorem/spinSpiralDispersion': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
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
            'optional_attribs': ['dos', 'band', 'vacdos', 'slice', 'coreSpec', 'wannier', 'mcd'],
            'order': [
                'checks', 'densityOfStates', 'vacuumDOS', 'plotting', 'chargeDensitySlicing', 'specialOutput',
                'coreSpectrum', 'wannier', 'magneticCircularDichroism', 'unfoldingBand'
            ],
            'several': [],
            'simple': [
                'checks', 'densityOfStates', 'vacuumDOS', 'plotting', 'chargeDensitySlicing', 'specialOutput',
                'magneticCircularDichroism', 'unfoldingBand'
            ],
            'text': []
        },
        '/fleurInput/output/chargeDensitySlicing': {
            'attribs': ['numkpt', 'minEigenval', 'maxEigenval', 'nnne', 'pallst'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/checks': {
            'attribs': ['vchk', 'cdinf', 'disp'],
            'optional': [],
            'optional_attribs': ['vchk', 'cdinf', 'disp'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/coreSpectrum': {
            'attribs': ['eKin', 'atomType', 'lmax', 'edgeType', 'eMin', 'eMax', 'numPoints', 'verbose'],
            'optional': [],
            'optional_attribs': ['verbose'],
            'order': ['edgeIndices'],
            'several': [],
            'simple': ['edgeIndices'],
            'text': ['edgeIndices']
        },
        '/fleurInput/output/densityOfStates': {
            'attribs': ['ndir', 'minEnergy', 'maxEnergy', 'sigma'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/magneticCircularDichroism': {
            'attribs': ['energyLo', 'energyUp'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/plotting': {
            'attribs': ['iplot', 'score', 'plplot'],
            'optional': [],
            'optional_attribs': ['iplot', 'score', 'plplot'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/specialOutput': {
            'attribs': ['form66', 'eonly', 'bmt'],
            'optional': [],
            'optional_attribs': ['form66', 'eonly', 'bmt'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/unfoldingBand': {
            'attribs': ['unfoldband', 'supercellX', 'supercellY', 'supercellZ'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/vacuumDOS': {
            'attribs': ['layers', 'integ', 'star', 'nstars', 'locx1', 'locy1', 'locx2', 'locy2', 'nstm', 'tworkf'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/wannier': {
            'attribs': ['ms', 'sgwf', 'socgwf', 'bsComf', 'atomList'],
            'optional': ['bandSelection', 'jobList'],
            'optional_attribs': ['ms', 'sgwf', 'socgwf', 'bsComf', 'atomList'],
            'order': ['bandSelection', 'jobList'],
            'several': [],
            'simple': ['bandSelection', 'jobList'],
            'text': ['jobList']
        },
        '/fleurInput/output/wannier/bandSelection': {
            'attribs': ['minSpinUp', 'maxSpinUp', 'minSpinDown', 'maxSpinDown'],
            'optional': [],
            'optional_attribs': ['minSpinDown', 'maxSpinDown'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/xcFunctional': {
            'attribs': ['name', 'relativisticCorrections'],
            'optional': ['libXC', 'xcParams', 'ggaPrinting'],
            'optional_attribs': ['relativisticCorrections'],
            'order': ['libXC', 'xcParams', 'ggaPrinting'],
            'several': [],
            'simple': ['libXC', 'xcParams', 'ggaPrinting'],
            'text': []
        },
        '/fleurInput/xcFunctional/ggaPrinting': {
            'attribs': ['iggachk', 'idsprs0', 'idsprsl', 'idsprsi', 'idsprsv'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/xcFunctional/libXC': {
            'attribs': ['exchange', 'correlation'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/xcFunctional/xcParams': {
            'attribs': ['igrd', 'lwb', 'ndvgrd', 'idsprs', 'chng'],
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
        'filmpos':
        '/fleurInput/atomGroups/atomGroup/filmPos',
        'abspos':
        '/fleurInput/atomGroups/atomGroup/absPos',
        'constants':
        '/fleurInput/constants',
        'force': ['/fleurInput/atomGroups/atomGroup/force', '/fleurInput/atomSpecies/species/force'],
        'wannier':
        '/fleurInput/output/wannier',
        'plotting':
        '/fleurInput/output/plotting',
        'symop':
        '/fleurInput/cell/symmetryOperations/symOp',
        'orbcomprot':
        '/fleurInput/atomGroups/atomGroup/orbcomprot',
        'chargedensityslicing':
        '/fleurInput/output/chargeDensitySlicing',
        'densityofstates':
        '/fleurInput/output/densityOfStates',
        'coreconfig':
        '/fleurInput/atomSpecies/species/electronConfig/coreConfig',
        'row-1': [
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-1', '/fleurInput/cell/bulkLattice/row-1',
            '/fleurInput/cell/filmLattice/bravaisMatrix/row-1', '/fleurInput/cell/filmLattice/row-1',
            '/fleurInput/cell/symmetryOperations/symOp/row-1'
        ],
        'ldau': [
            '/fleurInput/atomGroups/atomGroup/ldaU', '/fleurInput/atomSpecies/species/ldaU',
            '/fleurInput/calculationSetup/ldaU'
        ],
        'specialpoint':
        '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint',
        'filmlattice':
        '/fleurInput/cell/filmLattice',
        'unfoldingband':
        '/fleurInput/output/unfoldingBand',
        'species':
        '/fleurInput/atomSpecies/species',
        'qvectors': ['/fleurInput/forceTheorem/DMI/qVectors', '/fleurInput/forceTheorem/Jij/qVectors'],
        'q': [
            '/fleurInput/forceTheorem/DMI/qVectors/q', '/fleurInput/forceTheorem/Jij/qVectors/q',
            '/fleurInput/forceTheorem/spinSpiralDispersion/q'
        ],
        'efield':
        '/fleurInput/calculationSetup/eField',
        'electronconfig':
        '/fleurInput/atomSpecies/species/electronConfig',
        'symmetry':
        '/fleurInput/cell/symmetry',
        'row-3': [
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-3', '/fleurInput/cell/filmLattice/bravaisMatrix/row-3',
            '/fleurInput/cell/symmetryOperations/symOp/row-3'
        ],
        'symmetryoperations':
        '/fleurInput/cell/symmetryOperations',
        'forcetheorem':
        '/fleurInput/forceTheorem',
        'xcfunctional':
        '/fleurInput/xcFunctional',
        'cell':
        '/fleurInput/cell',
        'constant':
        '/fleurInput/constants/constant',
        'checks':
        '/fleurInput/output/checks',
        'special':
        '/fleurInput/atomSpecies/species/special',
        'mtsphere': ['/fleurInput/atomGroups/atomGroup/mtSphere', '/fleurInput/atomSpecies/species/mtSphere'],
        'kpointdensity':
        '/fleurInput/calculationSetup/bzIntegration/kPointDensity',
        'bravaismatrix': ['/fleurInput/cell/bulkLattice/bravaisMatrix', '/fleurInput/cell/filmLattice/bravaisMatrix'],
        'output':
        '/fleurInput/output',
        'ggaprinting':
        '/fleurInput/xcFunctional/ggaPrinting',
        'spinspiraldispersion':
        '/fleurInput/forceTheorem/spinSpiralDispersion',
        'vacuumenergyparameters':
        '/fleurInput/cell/filmLattice/vacuumEnergyParameters',
        'scfloop':
        '/fleurInput/calculationSetup/scfLoop',
        'geometryoptimization':
        '/fleurInput/calculationSetup/geometryOptimization',
        'bzintegration':
        '/fleurInput/calculationSetup/bzIntegration',
        'calculationsetup':
        '/fleurInput/calculationSetup',
        'a1': ['/fleurInput/cell/bulkLattice/a1', '/fleurInput/cell/filmLattice/a1'],
        'corespectrum':
        '/fleurInput/output/coreSpectrum',
        'onedparams':
        '/fleurInput/calculationSetup/oneDParams',
        'jij':
        '/fleurInput/forceTheorem/Jij',
        'energyparameters':
        ['/fleurInput/atomGroups/atomGroup/energyParameters', '/fleurInput/atomSpecies/species/energyParameters'],
        'expertmodes':
        '/fleurInput/calculationSetup/expertModes',
        'a2': ['/fleurInput/cell/bulkLattice/a2', '/fleurInput/cell/filmLattice/a2'],
        'specialoutput':
        '/fleurInput/output/specialOutput',
        'kpointmesh':
        '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
        'edgeindices':
        '/fleurInput/output/coreSpectrum/edgeIndices',
        'stateoccupation':
        '/fleurInput/atomSpecies/species/electronConfig/stateOccupation',
        'fleurinput':
        '/fleurInput',
        'spinspiralqpointmesh':
        '/fleurInput/calculationSetup/spinSpiralQPointMesh',
        'xcparams':
        '/fleurInput/xcFunctional/xcParams',
        'valenceconfig':
        '/fleurInput/atomSpecies/species/electronConfig/valenceConfig',
        'kpointlist':
        '/fleurInput/calculationSetup/bzIntegration/kPointList',
        'lo': ['/fleurInput/atomGroups/atomGroup/lo', '/fleurInput/atomSpecies/species/lo'],
        'joblist':
        '/fleurInput/output/wannier/jobList',
        'mae':
        '/fleurInput/forceTheorem/MAE',
        'comment':
        '/fleurInput/comment',
        'qss':
        '/fleurInput/calculationSetup/nocoParams/qss',
        'c':
        '/fleurInput/cell/bulkLattice/c',
        'qsc':
        '/fleurInput/calculationSetup/nocoParams/qsc',
        'coreelectrons':
        '/fleurInput/calculationSetup/coreElectrons',
        'atomspecies':
        '/fleurInput/atomSpecies',
        'soc':
        '/fleurInput/calculationSetup/soc',
        'atomgroups':
        '/fleurInput/atomGroups',
        'kpointcount':
        '/fleurInput/calculationSetup/bzIntegration/kPointCount',
        'row-2': [
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-2', '/fleurInput/cell/bulkLattice/row-2',
            '/fleurInput/cell/filmLattice/bravaisMatrix/row-2', '/fleurInput/cell/filmLattice/row-2',
            '/fleurInput/cell/symmetryOperations/symOp/row-2'
        ],
        'energyparameterlimits':
        '/fleurInput/calculationSetup/energyParameterLimits',
        'atomgroup':
        '/fleurInput/atomGroups/atomGroup',
        'libxc':
        '/fleurInput/xcFunctional/libXC',
        'vacuumdos':
        '/fleurInput/output/vacuumDOS',
        'nocoparams': [
            '/fleurInput/atomGroups/atomGroup/nocoParams', '/fleurInput/atomSpecies/species/nocoParams',
            '/fleurInput/calculationSetup/nocoParams'
        ],
        'bandselection':
        '/fleurInput/output/wannier/bandSelection',
        'kpoint':
        '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint',
        'atomiccutoffs':
        ['/fleurInput/atomGroups/atomGroup/atomicCutoffs', '/fleurInput/atomSpecies/species/atomicCutoffs'],
        'dmi':
        '/fleurInput/forceTheorem/DMI',
        'prodbasis': ['/fleurInput/atomSpecies/species/prodBasis', '/fleurInput/calculationSetup/prodBasis'],
        'cutoffs':
        '/fleurInput/calculationSetup/cutoffs',
        'relpos':
        '/fleurInput/atomGroups/atomGroup/relPos',
        'magnetism':
        '/fleurInput/calculationSetup/magnetism',
        'magneticcirculardichroism':
        '/fleurInput/output/magneticCircularDichroism',
        'symmetryfile':
        '/fleurInput/cell/symmetryFile',
        'bulklattice':
        '/fleurInput/cell/bulkLattice'
    }),
    'unique_attribs':
    CaseInsensitiveDict({
        'eig66': '/fleurInput/calculationSetup/expertModes/@eig66',
        'ellow': '/fleurInput/calculationSetup/energyParameterLimits/@ellow',
        'iggachk': '/fleurInput/xcFunctional/ggaPrinting/@iggachk',
        'wannier': '/fleurInput/output/@wannier',
        'plplot': '/fleurInput/output/plotting/@plplot',
        'socgwf': '/fleurInput/output/wannier/@socgwf',
        'dirichlet': '/fleurInput/calculationSetup/eField/@dirichlet',
        'correlation': '/fleurInput/xcFunctional/libXC/@correlation',
        'locy2': '/fleurInput/output/vacuumDOS/@locy2',
        'mixparam': '/fleurInput/calculationSetup/ldaU/@mixParam',
        'isec1': '/fleurInput/calculationSetup/expertModes/@isec1',
        'plot_rho': '/fleurInput/calculationSetup/eField/@plot_rho',
        'nx': '/fleurInput/calculationSetup/bzIntegration/kPointMesh/@nx',
        'idsprsv': '/fleurInput/xcFunctional/ggaPrinting/@idsprsv',
        'corespec': '/fleurInput/output/@coreSpec',
        'igrd': '/fleurInput/xcFunctional/xcParams/@igrd',
        'weightscale': '/fleurInput/calculationSetup/bzIntegration/kPointList/@weightScale',
        'cdinf': '/fleurInput/output/checks/@cdinf',
        'star': '/fleurInput/output/vacuumDOS/@star',
        'bscomf': '/fleurInput/output/wannier/@bsComf',
        'maxspinup': '/fleurInput/output/wannier/bandSelection/@maxSpinUp',
        'invs1': '/fleurInput/calculationSetup/oneDParams/@invs1',
        'plot_charge': '/fleurInput/calculationSetup/eField/@plot_charge',
        'pot8': '/fleurInput/calculationSetup/expertModes/@pot8',
        'minspindown': '/fleurInput/output/wannier/bandSelection/@minSpinDown',
        'maxspindown': '/fleurInput/output/wannier/bandSelection/@maxSpinDown',
        'gcutm': '/fleurInput/calculationSetup/prodBasis/@gcutm',
        'd1': '/fleurInput/calculationSetup/oneDParams/@d1',
        'numpoints': '/fleurInput/output/coreSpectrum/@numPoints',
        'maxtimetostartiter': '/fleurInput/calculationSetup/scfLoop/@maxTimeToStartIter',
        'emax': '/fleurInput/output/coreSpectrum/@eMax',
        'qz': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qz',
        'epsdisp': '/fleurInput/calculationSetup/geometryOptimization/@epsdisp',
        'kcrel': '/fleurInput/calculationSetup/coreElectrons/@kcrel',
        'thetad': '/fleurInput/calculationSetup/geometryOptimization/@thetad',
        'spgrp': '/fleurInput/cell/symmetry/@spgrp',
        'idsprs0': '/fleurInput/xcFunctional/ggaPrinting/@idsprs0',
        'ndvgrd': '/fleurInput/xcFunctional/xcParams/@ndvgrd',
        'coretail_lmax': '/fleurInput/calculationSetup/coreElectrons/@coretail_lmax',
        'unfoldband': '/fleurInput/output/unfoldingBand/@unfoldband',
        'vm': '/fleurInput/calculationSetup/oneDParams/@vM',
        'slice': '/fleurInput/output/@slice',
        'l_disp': '/fleurInput/calculationSetup/nocoParams/@l_disp',
        'supercellz': '/fleurInput/output/unfoldingBand/@supercellZ',
        'minspinup': '/fleurInput/output/wannier/bandSelection/@minSpinUp',
        'jspins': '/fleurInput/calculationSetup/magnetism/@jspins',
        'supercellx': '/fleurInput/output/unfoldingBand/@supercellX',
        'qy': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qy',
        'mode': '/fleurInput/calculationSetup/bzIntegration/@mode',
        'rot': '/fleurInput/calculationSetup/oneDParams/@rot',
        'posscale': '/fleurInput/calculationSetup/bzIntegration/kPointList/@posScale',
        'sso_opt': '/fleurInput/calculationSetup/nocoParams/@sso_opt',
        'vacdos': '/fleurInput/output/@vacdos',
        'maxiterbroyd': '/fleurInput/calculationSetup/scfLoop/@maxIterBroyd',
        'integ': '/fleurInput/output/vacuumDOS/@integ',
        'gw': '/fleurInput/calculationSetup/expertModes/@gw',
        'qfix': '/fleurInput/calculationSetup/geometryOptimization/@qfix',
        'idsprsl': '/fleurInput/xcFunctional/ggaPrinting/@idsprsl',
        'l_soc': '/fleurInput/calculationSetup/soc/@l_soc',
        'fermismearingenergy': '/fleurInput/calculationSetup/bzIntegration/@fermiSmearingEnergy',
        'zrfs1': '/fleurInput/calculationSetup/oneDParams/@zrfs1',
        'l_j': '/fleurInput/calculationSetup/magnetism/@l_J',
        'swsp': '/fleurInput/calculationSetup/magnetism/@swsp',
        'nz': '/fleurInput/calculationSetup/bzIntegration/kPointMesh/@nz',
        'vchk': '/fleurInput/output/checks/@vchk',
        'm_cyl': '/fleurInput/calculationSetup/oneDParams/@m_cyl',
        'lexp': '/fleurInput/calculationSetup/prodBasis/@lexp',
        'atomtype': '/fleurInput/output/coreSpectrum/@atomType',
        'exchange': '/fleurInput/xcFunctional/libXC/@exchange',
        'l_linmix': '/fleurInput/calculationSetup/ldaU/@l_linMix',
        'gmax': '/fleurInput/calculationSetup/cutoffs/@Gmax',
        'locx1': '/fleurInput/output/vacuumDOS/@locx1',
        'ev': '/fleurInput/calculationSetup/eField/@eV',
        'form66': '/fleurInput/output/specialOutput/@form66',
        'imix': '/fleurInput/calculationSetup/scfLoop/@imix',
        'nstars': '/fleurInput/output/vacuumDOS/@nstars',
        'mcd': '/fleurInput/output/@mcd',
        'name': '/fleurInput/xcFunctional/@name',
        'mix_b': '/fleurInput/calculationSetup/nocoParams/@mix_b',
        'itmax': '/fleurInput/calculationSetup/scfLoop/@itmax',
        'dos': '/fleurInput/output/@dos',
        'minenergy': '/fleurInput/output/densityOfStates/@minEnergy',
        'locx2': '/fleurInput/output/vacuumDOS/@locx2',
        'ny': '/fleurInput/calculationSetup/bzIntegration/kPointMesh/@ny',
        'ekin': '/fleurInput/output/coreSpectrum/@eKin',
        'dvac': '/fleurInput/cell/filmLattice/@dVac',
        'soc66': '/fleurInput/calculationSetup/soc/@soc66',
        'denx': '/fleurInput/calculationSetup/bzIntegration/kPointDensity/@denX',
        'alpha': '/fleurInput/calculationSetup/scfLoop/@alpha',
        'valenceelectrons': '/fleurInput/calculationSetup/bzIntegration/@valenceElectrons',
        'qx': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qx',
        'l_noco': '/fleurInput/calculationSetup/magnetism/@l_noco',
        'disp': '/fleurInput/output/checks/@disp',
        'sigma': '/fleurInput/output/densityOfStates/@sigma',
        'locy1': '/fleurInput/output/vacuumDOS/@locy1',
        'spav': '/fleurInput/calculationSetup/soc/@spav',
        'energylo': '/fleurInput/output/magneticCircularDichroism/@energyLo',
        'chi': '/fleurInput/calculationSetup/oneDParams/@chi',
        'edgetype': '/fleurInput/output/coreSpectrum/@edgeType',
        'chng': '/fleurInput/xcFunctional/xcParams/@chng',
        'lwb': '/fleurInput/xcFunctional/xcParams/@lwb',
        'epsforce': '/fleurInput/calculationSetup/geometryOptimization/@epsforce',
        'invs': '/fleurInput/cell/symmetry/@invs',
        'idsprs': '/fleurInput/xcFunctional/xcParams/@idsprs',
        'filename': '/fleurInput/cell/symmetryFile/@filename',
        'idsprsi': '/fleurInput/xcFunctional/ggaPrinting/@idsprsi',
        'eonly': '/fleurInput/output/specialOutput/@eonly',
        'preconditioning_param': '/fleurInput/calculationSetup/scfLoop/@preconditioning_param',
        'verbose': '/fleurInput/output/coreSpectrum/@verbose',
        'mm': '/fleurInput/calculationSetup/oneDParams/@MM',
        'score': '/fleurInput/output/plotting/@score',
        'tolerance': '/fleurInput/calculationSetup/prodBasis/@tolerance',
        'sig_b_1': '/fleurInput/calculationSetup/eField/@sig_b_1',
        'l_mperp': '/fleurInput/calculationSetup/nocoParams/@l_mperp',
        'layers': '/fleurInput/output/vacuumDOS/@layers',
        'l_f': '/fleurInput/calculationSetup/geometryOptimization/@l_f',
        'iplot': '/fleurInput/output/plotting/@iplot',
        'energyup': '/fleurInput/output/magneticCircularDichroism/@energyUp',
        'lpr': '/fleurInput/calculationSetup/expertModes/@lpr',
        'ndir': '/fleurInput/output/densityOfStates/@ndir',
        'emin': '/fleurInput/output/coreSpectrum/@eMin',
        'xa': '/fleurInput/calculationSetup/geometryOptimization/@xa',
        'numkpt': '/fleurInput/output/chargeDensitySlicing/@numkpt',
        'relativisticcorrections': '/fleurInput/xcFunctional/@relativisticCorrections',
        'ewaldlambda': '/fleurInput/calculationSetup/prodBasis/@ewaldlambda',
        'lflip': '/fleurInput/calculationSetup/magnetism/@lflip',
        'mineigenval': '/fleurInput/output/chargeDensitySlicing/@minEigenval',
        'nnne': '/fleurInput/output/chargeDensitySlicing/@nnne',
        'zsigma': '/fleurInput/calculationSetup/eField/@zsigma',
        'deny': '/fleurInput/calculationSetup/bzIntegration/kPointDensity/@denY',
        'fermismearingtemp': '/fleurInput/calculationSetup/bzIntegration/@fermiSmearingTemp',
        'dtilda': '/fleurInput/cell/filmLattice/@dTilda',
        'mindistance': '/fleurInput/calculationSetup/scfLoop/@minDistance',
        'nstm': '/fleurInput/output/vacuumDOS/@nstm',
        'maxeigenval': '/fleurInput/output/chargeDensitySlicing/@maxEigenval',
        'maxenergy': '/fleurInput/output/densityOfStates/@maxEnergy',
        'ms': '/fleurInput/output/wannier/@ms',
        'supercelly': '/fleurInput/output/unfoldingBand/@supercellY',
        'secvar': '/fleurInput/calculationSetup/expertModes/@secvar',
        'frcor': '/fleurInput/calculationSetup/coreElectrons/@frcor',
        'tworkf': '/fleurInput/output/vacuumDOS/@tworkf',
        'elup': '/fleurInput/calculationSetup/energyParameterLimits/@elup',
        'bands': '/fleurInput/calculationSetup/prodBasis/@bands',
        'ctail': '/fleurInput/calculationSetup/coreElectrons/@ctail',
        'atomlist': '/fleurInput/output/wannier/@atomList',
        'sgwf': '/fleurInput/output/wannier/@sgwf',
        'fleurinputversion': '/fleurInput/@fleurInputVersion',
        'nsh': '/fleurInput/calculationSetup/nocoParams/@nsh',
        'band': '/fleurInput/output/@band',
        'denz': '/fleurInput/calculationSetup/bzIntegration/kPointDensity/@denZ',
        'zrfs': '/fleurInput/cell/symmetry/@zrfs',
        'gmaxxc': '/fleurInput/calculationSetup/cutoffs/@GmaxXC',
        'l_constr': '/fleurInput/calculationSetup/nocoParams/@l_constr',
        'lmax': '/fleurInput/output/coreSpectrum/@lmax',
        'off': '/fleurInput/calculationSetup/soc/@off',
        'autocomp': '/fleurInput/calculationSetup/eField/@autocomp',
        'l_ss': '/fleurInput/calculationSetup/nocoParams/@l_ss',
        'bmt': '/fleurInput/output/specialOutput/@bmt',
        'numbands': '/fleurInput/calculationSetup/cutoffs/@numbands',
        'sig_b_2': '/fleurInput/calculationSetup/eField/@sig_b_2',
        'pallst': '/fleurInput/output/chargeDensitySlicing/@pallst',
        'kmax': '/fleurInput/calculationSetup/cutoffs/@Kmax',
        'comment': '/fleurInput/comment',
        'qss': '/fleurInput/calculationSetup/nocoParams/qss',
        'qsc': '/fleurInput/calculationSetup/nocoParams/qsc',
        'c': '/fleurInput/cell/bulkLattice/c',
        'edgeindices': '/fleurInput/output/coreSpectrum/edgeIndices',
        'joblist': '/fleurInput/output/wannier/jobList'
    }),
    'unique_path_attribs':
    CaseInsensitiveDict({
        'latnam': ['/fleurInput/cell/bulkLattice/@latnam', '/fleurInput/cell/filmLattice/@latnam'],
        'theta': [
            '/fleurInput/calculationSetup/soc/@theta', '/fleurInput/forceTheorem/DMI/@theta',
            '/fleurInput/forceTheorem/MAE/@theta'
        ],
        'scale': [
            '/fleurInput/cell/bulkLattice/@scale', '/fleurInput/cell/bulkLattice/a1/@scale',
            '/fleurInput/cell/bulkLattice/a2/@scale', '/fleurInput/cell/bulkLattice/c/@scale',
            '/fleurInput/cell/filmLattice/@scale', '/fleurInput/cell/filmLattice/a1/@scale',
            '/fleurInput/cell/filmLattice/a2/@scale'
        ],
        'gamma': [
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/@gamma',
            '/fleurInput/calculationSetup/bzIntegration/kPointDensity/@gamma',
            '/fleurInput/calculationSetup/bzIntegration/kPointMesh/@gamma'
        ],
        'thetaj': ['/fleurInput/calculationSetup/nocoParams/@thetaJ', '/fleurInput/forceTheorem/Jij/@thetaj'],
        'count': [
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/@count',
            '/fleurInput/calculationSetup/bzIntegration/kPointList/@count'
        ],
        'spinf': ['/fleurInput/calculationSetup/ldaU/@spinf', '/fleurInput/calculationSetup/scfLoop/@spinf'],
        'phi': [
            '/fleurInput/calculationSetup/soc/@phi', '/fleurInput/forceTheorem/DMI/@phi',
            '/fleurInput/forceTheorem/MAE/@phi'
        ],
        'a1': ['/fleurInput/cell/bulkLattice/a1', '/fleurInput/cell/filmLattice/a1'],
        'a2': ['/fleurInput/cell/bulkLattice/a2', '/fleurInput/cell/filmLattice/a2'],
        'row-1': [
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-1', '/fleurInput/cell/bulkLattice/row-1',
            '/fleurInput/cell/filmLattice/bravaisMatrix/row-1', '/fleurInput/cell/filmLattice/row-1'
        ],
        'row-2': [
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-2', '/fleurInput/cell/bulkLattice/row-2',
            '/fleurInput/cell/filmLattice/bravaisMatrix/row-2', '/fleurInput/cell/filmLattice/row-2'
        ],
        'row-3':
        ['/fleurInput/cell/bulkLattice/bravaisMatrix/row-3', '/fleurInput/cell/filmLattice/bravaisMatrix/row-3']
    })
}
