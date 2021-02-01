# -*- coding: utf-8 -*-
"""
This file contains information parsed from the FleurInputSchema.xsd
for version 0.27

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
__inp_version__ = '0.27'
schema_dict = {
    '_basic_types': {
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
    'inp_version':
    '0.27',
    'omitt_contained_tags': ['constants', 'atomSpecies', 'atomGroups', 'symmetryOperations'],
    'other_attribs':
    CaseInsensitiveDict({
        'corestates': ['/fleurInput/atomSpecies/species/@coreStates'],
        'radius':
        ['/fleurInput/atomGroups/atomGroup/mtSphere/@radius', '/fleurInput/atomSpecies/species/mtSphere/@radius'],
        'flipspin': ['/fleurInput/atomSpecies/species/@flipSpin'],
        'l_amf': ['/fleurInput/atomGroups/atomGroup/ldaU/@l_amf', '/fleurInput/atomSpecies/species/ldaU/@l_amf'],
        'l_magn':
        ['/fleurInput/atomGroups/atomGroup/nocoParams/@l_magn', '/fleurInput/atomSpecies/species/nocoParams/@l_magn'],
        'logincrement': [
            '/fleurInput/atomGroups/atomGroup/mtSphere/@logIncrement',
            '/fleurInput/atomSpecies/species/mtSphere/@logIncrement'
        ],
        'orbcomp': ['/fleurInput/atomGroups/atomGroup/@orbcomp'],
        'species': ['/fleurInput/atomGroups/atomGroup/@species'],
        'value': ['/fleurInput/constants/constant/@value'],
        'f':
        ['/fleurInput/atomGroups/atomGroup/energyParameters/@f', '/fleurInput/atomSpecies/species/energyParameters/@f'],
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
        'state': ['/fleurInput/atomSpecies/species/electronConfig/stateOccupation/@state'],
        'd':
        ['/fleurInput/atomGroups/atomGroup/energyParameters/@d', '/fleurInput/atomSpecies/species/energyParameters/@d'],
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
        'coreconfig': ['/fleurInput/atomSpecies/species/electronConfig/coreConfig'],
        'valenceconfig': ['/fleurInput/atomSpecies/species/electronConfig/valenceConfig']
    }),
    'root_tag':
    'fleurInput',
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
            'optional_attribs': [],
            'order':
            ['comment', 'constants', 'calculationSetup', 'cell', 'xcFunctional', 'atomSpecies', 'atomGroups', 'output'],
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
            'attribs': ['species', 'orbcomp', 'magField', 'vcaAddCharge'],
            'optional':
            ['mtSphere', 'atomicCutoffs', 'energyParameters', 'force', 'nocoParams', 'ldaU', 'lo', 'orbcomprot'],
            'optional_attribs': ['orbcomp', 'magField', 'vcaAddCharge'],
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
            'optional_attribs': [],
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
            'optional': ['energyParameters', 'force', 'electronConfig', 'nocoParams', 'ldaU', 'lo'],
            'optional_attribs': ['magMom', 'flipSpin', 'magField', 'vcaAddCharge'],
            'order':
            ['mtSphere', 'atomicCutoffs', 'energyParameters', 'force', 'electronConfig', 'nocoParams', 'ldaU', 'lo'],
            'several': ['ldaU', 'lo'],
            'simple': ['mtSphere', 'atomicCutoffs', 'energyParameters', 'force', 'nocoParams', 'ldaU', 'lo'],
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
            'optional_attribs': [],
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
            'optional_attribs': [],
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
            'optional_attribs': ['valenceElectrons', 'mode', 'fermiSmearingEnergy', 'fermiSmearingTemp'],
            'order': ['kPointMesh', 'kPointCount', 'kPointList'],
            'several': [],
            'simple': ['kPointMesh'],
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
            'attribs': ['ctail', 'frcor', 'kcrel'],
            'optional': [],
            'optional_attribs': ['frcor', 'kcrel'],
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
            'optional_attribs': [],
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
        '/fleurInput/calculationSetup/scfLoop': {
            'attribs': ['itmax', 'maxIterBroyd', 'imix', 'alpha', 'spinf', 'minDistance', 'maxTimeToStartIter'],
            'optional': [],
            'optional_attribs': ['maxIterBroyd', 'spinf', 'minDistance', 'maxTimeToStartIter'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/soc': {
            'attribs': ['theta', 'phi', 'l_soc', 'spav', 'off', 'soc66'],
            'optional': [],
            'optional_attribs': [],
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
        '/fleurInput/cell/bulkLattice/bravaisMatrix': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['row-1', 'row-2', 'row-3'],
            'several': [],
            'simple': ['row-1', 'row-2', 'row-3'],
            'text': ['row-1', 'row-2', 'row-3']
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
        '/fleurInput/output': {
            'attribs': ['dos', 'band', 'vacdos', 'slice'],
            'optional': ['checks', 'densityOfStates', 'vacuumDOS', 'plotting', 'chargeDensitySlicing', 'specialOutput'],
            'optional_attribs': ['dos', 'band', 'vacdos', 'slice'],
            'order': ['checks', 'densityOfStates', 'vacuumDOS', 'plotting', 'chargeDensitySlicing', 'specialOutput'],
            'several': [],
            'simple': ['checks', 'densityOfStates', 'vacuumDOS', 'plotting', 'chargeDensitySlicing', 'specialOutput'],
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
        '/fleurInput/output/densityOfStates': {
            'attribs': ['ndir', 'minEnergy', 'maxEnergy', 'sigma'],
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
        '/fleurInput/output/vacuumDOS': {
            'attribs': ['layers', 'integ', 'star', 'nstars', 'locx1', 'locy1', 'locx2', 'locy2', 'nstm', 'tworkf'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/xcFunctional': {
            'attribs': ['name', 'relativisticCorrections'],
            'optional': ['xcParams', 'ggaPrinting'],
            'optional_attribs': ['relativisticCorrections'],
            'order': ['xcParams', 'ggaPrinting'],
            'several': [],
            'simple': ['xcParams', 'ggaPrinting'],
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
        'qss':
        '/fleurInput/calculationSetup/nocoParams/qss',
        'c':
        '/fleurInput/cell/bulkLattice/c',
        'constants':
        '/fleurInput/constants',
        'force': ['/fleurInput/atomGroups/atomGroup/force', '/fleurInput/atomSpecies/species/force'],
        'kpointmesh':
        '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
        'qsc':
        '/fleurInput/calculationSetup/nocoParams/qsc',
        'bravaismatrix': ['/fleurInput/cell/bulkLattice/bravaisMatrix', '/fleurInput/cell/filmLattice/bravaisMatrix'],
        'plotting':
        '/fleurInput/output/plotting',
        'output':
        '/fleurInput/output',
        'ggaprinting':
        '/fleurInput/xcFunctional/ggaPrinting',
        'symop':
        '/fleurInput/cell/symmetryOperations/symOp',
        'orbcomprot':
        '/fleurInput/atomGroups/atomGroup/orbcomprot',
        'chargedensityslicing':
        '/fleurInput/output/chargeDensitySlicing',
        'coreelectrons':
        '/fleurInput/calculationSetup/coreElectrons',
        'vacuumenergyparameters':
        '/fleurInput/cell/filmLattice/vacuumEnergyParameters',
        'atomspecies':
        '/fleurInput/atomSpecies',
        'scfloop':
        '/fleurInput/calculationSetup/scfLoop',
        'soc':
        '/fleurInput/calculationSetup/soc',
        'atomgroups':
        '/fleurInput/atomGroups',
        'kpointcount':
        '/fleurInput/calculationSetup/bzIntegration/kPointCount',
        'densityofstates':
        '/fleurInput/output/densityOfStates',
        'row-2': [
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-2', '/fleurInput/cell/bulkLattice/row-2',
            '/fleurInput/cell/filmLattice/bravaisMatrix/row-2', '/fleurInput/cell/filmLattice/row-2',
            '/fleurInput/cell/symmetryOperations/symOp/row-2'
        ],
        'energyparameterlimits':
        '/fleurInput/calculationSetup/energyParameterLimits',
        'coreconfig':
        '/fleurInput/atomSpecies/species/electronConfig/coreConfig',
        'atomgroup':
        '/fleurInput/atomGroups/atomGroup',
        'row-1': [
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-1', '/fleurInput/cell/bulkLattice/row-1',
            '/fleurInput/cell/filmLattice/bravaisMatrix/row-1', '/fleurInput/cell/filmLattice/row-1',
            '/fleurInput/cell/symmetryOperations/symOp/row-1'
        ],
        'ldau': ['/fleurInput/atomGroups/atomGroup/ldaU', '/fleurInput/atomSpecies/species/ldaU'],
        'stateoccupation':
        '/fleurInput/atomSpecies/species/electronConfig/stateOccupation',
        'specialpoint':
        '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint',
        'fleurinput':
        '/fleurInput',
        'nocoparams': [
            '/fleurInput/atomGroups/atomGroup/nocoParams', '/fleurInput/atomSpecies/species/nocoParams',
            '/fleurInput/calculationSetup/nocoParams'
        ],
        'bzintegration':
        '/fleurInput/calculationSetup/bzIntegration',
        'filmlattice':
        '/fleurInput/cell/filmLattice',
        'vacuumdos':
        '/fleurInput/output/vacuumDOS',
        'kpoint':
        '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint',
        'atomiccutoffs':
        ['/fleurInput/atomGroups/atomGroup/atomicCutoffs', '/fleurInput/atomSpecies/species/atomicCutoffs'],
        'calculationsetup':
        '/fleurInput/calculationSetup',
        'spinspiralqpointmesh':
        '/fleurInput/calculationSetup/spinSpiralQPointMesh',
        'a1': ['/fleurInput/cell/bulkLattice/a1', '/fleurInput/cell/filmLattice/a1'],
        'bulklattice':
        '/fleurInput/cell/bulkLattice',
        'species':
        '/fleurInput/atomSpecies/species',
        'onedparams':
        '/fleurInput/calculationSetup/oneDParams',
        'xcparams':
        '/fleurInput/xcFunctional/xcParams',
        'valenceconfig':
        '/fleurInput/atomSpecies/species/electronConfig/valenceConfig',
        'efield':
        '/fleurInput/calculationSetup/eField',
        'kpointlist':
        '/fleurInput/calculationSetup/bzIntegration/kPointList',
        'electronconfig':
        '/fleurInput/atomSpecies/species/electronConfig',
        'lo': ['/fleurInput/atomGroups/atomGroup/lo', '/fleurInput/atomSpecies/species/lo'],
        'cutoffs':
        '/fleurInput/calculationSetup/cutoffs',
        'symmetry':
        '/fleurInput/cell/symmetry',
        'relpos':
        '/fleurInput/atomGroups/atomGroup/relPos',
        'row-3': [
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-3', '/fleurInput/cell/filmLattice/bravaisMatrix/row-3',
            '/fleurInput/cell/symmetryOperations/symOp/row-3'
        ],
        'symmetryoperations':
        '/fleurInput/cell/symmetryOperations',
        'xcfunctional':
        '/fleurInput/xcFunctional',
        'cell':
        '/fleurInput/cell',
        'magnetism':
        '/fleurInput/calculationSetup/magnetism',
        'constant':
        '/fleurInput/constants/constant',
        'expertmodes':
        '/fleurInput/calculationSetup/expertModes',
        'a2': ['/fleurInput/cell/bulkLattice/a2', '/fleurInput/cell/filmLattice/a2'],
        'energyparameters':
        ['/fleurInput/atomGroups/atomGroup/energyParameters', '/fleurInput/atomSpecies/species/energyParameters'],
        'comment':
        '/fleurInput/comment',
        'checks':
        '/fleurInput/output/checks',
        'mtsphere': ['/fleurInput/atomGroups/atomGroup/mtSphere', '/fleurInput/atomSpecies/species/mtSphere'],
        'specialoutput':
        '/fleurInput/output/specialOutput',
        'symmetryfile':
        '/fleurInput/cell/symmetryFile',
        'geometryoptimization':
        '/fleurInput/calculationSetup/geometryOptimization'
    }),
    'unique_attribs':
    CaseInsensitiveDict({
        'eig66': '/fleurInput/calculationSetup/expertModes/@eig66',
        'ellow': '/fleurInput/calculationSetup/energyParameterLimits/@ellow',
        'iggachk': '/fleurInput/xcFunctional/ggaPrinting/@iggachk',
        'plplot': '/fleurInput/output/plotting/@plplot',
        'dirichlet': '/fleurInput/calculationSetup/eField/@dirichlet',
        'locy2': '/fleurInput/output/vacuumDOS/@locy2',
        'isec1': '/fleurInput/calculationSetup/expertModes/@isec1',
        'plot_rho': '/fleurInput/calculationSetup/eField/@plot_rho',
        'nx': '/fleurInput/calculationSetup/bzIntegration/kPointMesh/@nx',
        'idsprsv': '/fleurInput/xcFunctional/ggaPrinting/@idsprsv',
        'igrd': '/fleurInput/xcFunctional/xcParams/@igrd',
        'weightscale': '/fleurInput/calculationSetup/bzIntegration/kPointList/@weightScale',
        'cdinf': '/fleurInput/output/checks/@cdinf',
        'star': '/fleurInput/output/vacuumDOS/@star',
        'invs1': '/fleurInput/calculationSetup/oneDParams/@invs1',
        'plot_charge': '/fleurInput/calculationSetup/eField/@plot_charge',
        'pot8': '/fleurInput/calculationSetup/expertModes/@pot8',
        'd1': '/fleurInput/calculationSetup/oneDParams/@d1',
        'maxtimetostartiter': '/fleurInput/calculationSetup/scfLoop/@maxTimeToStartIter',
        'qz': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qz',
        'epsdisp': '/fleurInput/calculationSetup/geometryOptimization/@epsdisp',
        'kcrel': '/fleurInput/calculationSetup/coreElectrons/@kcrel',
        'thetad': '/fleurInput/calculationSetup/geometryOptimization/@thetad',
        'spgrp': '/fleurInput/cell/symmetry/@spgrp',
        'idsprs0': '/fleurInput/xcFunctional/ggaPrinting/@idsprs0',
        'ndvgrd': '/fleurInput/xcFunctional/xcParams/@ndvgrd',
        'vm': '/fleurInput/calculationSetup/oneDParams/@vM',
        'slice': '/fleurInput/output/@slice',
        'l_disp': '/fleurInput/calculationSetup/nocoParams/@l_disp',
        'jspins': '/fleurInput/calculationSetup/magnetism/@jspins',
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
        'theta': '/fleurInput/calculationSetup/soc/@theta',
        'l_soc': '/fleurInput/calculationSetup/soc/@l_soc',
        'fermismearingenergy': '/fleurInput/calculationSetup/bzIntegration/@fermiSmearingEnergy',
        'zrfs1': '/fleurInput/calculationSetup/oneDParams/@zrfs1',
        'l_j': '/fleurInput/calculationSetup/magnetism/@l_J',
        'swsp': '/fleurInput/calculationSetup/magnetism/@swsp',
        'nz': '/fleurInput/calculationSetup/bzIntegration/kPointMesh/@nz',
        'vchk': '/fleurInput/output/checks/@vchk',
        'm_cyl': '/fleurInput/calculationSetup/oneDParams/@m_cyl',
        'gmax': '/fleurInput/calculationSetup/cutoffs/@Gmax',
        'locx1': '/fleurInput/output/vacuumDOS/@locx1',
        'ev': '/fleurInput/calculationSetup/eField/@eV',
        'form66': '/fleurInput/output/specialOutput/@form66',
        'imix': '/fleurInput/calculationSetup/scfLoop/@imix',
        'nstars': '/fleurInput/output/vacuumDOS/@nstars',
        'name': '/fleurInput/xcFunctional/@name',
        'mix_b': '/fleurInput/calculationSetup/nocoParams/@mix_b',
        'itmax': '/fleurInput/calculationSetup/scfLoop/@itmax',
        'dos': '/fleurInput/output/@dos',
        'minenergy': '/fleurInput/output/densityOfStates/@minEnergy',
        'locx2': '/fleurInput/output/vacuumDOS/@locx2',
        'ny': '/fleurInput/calculationSetup/bzIntegration/kPointMesh/@ny',
        'dvac': '/fleurInput/cell/filmLattice/@dVac',
        'soc66': '/fleurInput/calculationSetup/soc/@soc66',
        'alpha': '/fleurInput/calculationSetup/scfLoop/@alpha',
        'valenceelectrons': '/fleurInput/calculationSetup/bzIntegration/@valenceElectrons',
        'qx': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qx',
        'l_noco': '/fleurInput/calculationSetup/magnetism/@l_noco',
        'disp': '/fleurInput/output/checks/@disp',
        'sigma': '/fleurInput/output/densityOfStates/@sigma',
        'locy1': '/fleurInput/output/vacuumDOS/@locy1',
        'thetaj': '/fleurInput/calculationSetup/nocoParams/@thetaJ',
        'spav': '/fleurInput/calculationSetup/soc/@spav',
        'chi': '/fleurInput/calculationSetup/oneDParams/@chi',
        'chng': '/fleurInput/xcFunctional/xcParams/@chng',
        'lwb': '/fleurInput/xcFunctional/xcParams/@lwb',
        'epsforce': '/fleurInput/calculationSetup/geometryOptimization/@epsforce',
        'invs': '/fleurInput/cell/symmetry/@invs',
        'idsprs': '/fleurInput/xcFunctional/xcParams/@idsprs',
        'filename': '/fleurInput/cell/symmetryFile/@filename',
        'idsprsi': '/fleurInput/xcFunctional/ggaPrinting/@idsprsi',
        'eonly': '/fleurInput/output/specialOutput/@eonly',
        'mm': '/fleurInput/calculationSetup/oneDParams/@MM',
        'score': '/fleurInput/output/plotting/@score',
        'sig_b_1': '/fleurInput/calculationSetup/eField/@sig_b_1',
        'l_mperp': '/fleurInput/calculationSetup/nocoParams/@l_mperp',
        'layers': '/fleurInput/output/vacuumDOS/@layers',
        'l_f': '/fleurInput/calculationSetup/geometryOptimization/@l_f',
        'spinf': '/fleurInput/calculationSetup/scfLoop/@spinf',
        'iplot': '/fleurInput/output/plotting/@iplot',
        'lpr': '/fleurInput/calculationSetup/expertModes/@lpr',
        'ndir': '/fleurInput/output/densityOfStates/@ndir',
        'xa': '/fleurInput/calculationSetup/geometryOptimization/@xa',
        'numkpt': '/fleurInput/output/chargeDensitySlicing/@numkpt',
        'relativisticcorrections': '/fleurInput/xcFunctional/@relativisticCorrections',
        'lflip': '/fleurInput/calculationSetup/magnetism/@lflip',
        'mineigenval': '/fleurInput/output/chargeDensitySlicing/@minEigenval',
        'nnne': '/fleurInput/output/chargeDensitySlicing/@nnne',
        'zsigma': '/fleurInput/calculationSetup/eField/@zsigma',
        'fermismearingtemp': '/fleurInput/calculationSetup/bzIntegration/@fermiSmearingTemp',
        'dtilda': '/fleurInput/cell/filmLattice/@dTilda',
        'mindistance': '/fleurInput/calculationSetup/scfLoop/@minDistance',
        'nstm': '/fleurInput/output/vacuumDOS/@nstm',
        'maxeigenval': '/fleurInput/output/chargeDensitySlicing/@maxEigenval',
        'maxenergy': '/fleurInput/output/densityOfStates/@maxEnergy',
        'secvar': '/fleurInput/calculationSetup/expertModes/@secvar',
        'frcor': '/fleurInput/calculationSetup/coreElectrons/@frcor',
        'phi': '/fleurInput/calculationSetup/soc/@phi',
        'tworkf': '/fleurInput/output/vacuumDOS/@tworkf',
        'elup': '/fleurInput/calculationSetup/energyParameterLimits/@elup',
        'ctail': '/fleurInput/calculationSetup/coreElectrons/@ctail',
        'fleurinputversion': '/fleurInput/@fleurInputVersion',
        'nsh': '/fleurInput/calculationSetup/nocoParams/@nsh',
        'band': '/fleurInput/output/@band',
        'zrfs': '/fleurInput/cell/symmetry/@zrfs',
        'gmaxxc': '/fleurInput/calculationSetup/cutoffs/@GmaxXC',
        'l_constr': '/fleurInput/calculationSetup/nocoParams/@l_constr',
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
        'c': '/fleurInput/cell/bulkLattice/c'
    }),
    'unique_path_attribs':
    CaseInsensitiveDict({
        'latnam': ['/fleurInput/cell/bulkLattice/@latnam', '/fleurInput/cell/filmLattice/@latnam'],
        'scale': ['/fleurInput/cell/bulkLattice/@scale', '/fleurInput/cell/filmLattice/@scale'],
        'gamma': [
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/@gamma',
            '/fleurInput/calculationSetup/bzIntegration/kPointMesh/@gamma'
        ],
        'count': [
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/@count',
            '/fleurInput/calculationSetup/bzIntegration/kPointList/@count'
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
