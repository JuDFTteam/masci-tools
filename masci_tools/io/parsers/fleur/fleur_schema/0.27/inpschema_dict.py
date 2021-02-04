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
from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict, CaseInsensitiveFrozenSet
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
    'attrib_types':
    CaseInsensitiveDict({
        'fleurinputversion': ['string'],
        'name': ['string'],
        'value': ['string'],
        'ellow': ['float'],
        'elup': ['float'],
        'zsigma': ['float'],
        'sig_b_1': ['float'],
        'sig_b_2': ['float'],
        'plot_charge': ['switch'],
        'plot_rho': ['switch'],
        'autocomp': ['switch'],
        'dirichlet': ['switch'],
        'ev': ['switch'],
        'l_ss': ['switch'],
        'l_mperp': ['switch'],
        'l_constr': ['switch'],
        'l_disp': ['switch'],
        'sso_opt': ['string'],
        'mix_b': ['float'],
        'thetaj': ['float'],
        'nsh': ['int'],
        'd1': ['switch'],
        'mm': ['int'],
        'vm': ['int'],
        'm_cyl': ['int'],
        'chi': ['int'],
        'rot': ['int'],
        'invs1': ['switch'],
        'zrfs1': ['switch'],
        'ctail': ['switch'],
        'frcor': ['switch'],
        'kcrel': ['int'],
        'spgrp': ['string'],
        'invs': ['switch'],
        'zrfs': ['switch'],
        'filename': ['string'],
        'jspins': ['int'],
        'l_noco': ['switch'],
        'l_j': ['switch'],
        'swsp': ['switch'],
        'lflip': ['switch'],
        'scale': ['float'],
        'latnam': ['string'],
        'dvac': ['float'],
        'dtilda': ['float'],
        'vacuum': ['int'],
        'spinup': ['float'],
        'spindown': ['float'],
        'relativisticcorrections': ['switch'],
        'igrd': ['int'],
        'lwb': ['switch'],
        'ndvgrd': ['int'],
        'idsprs': ['int'],
        'chng': ['float'],
        'iggachk': ['int'],
        'idsprs0': ['int'],
        'idsprsl': ['int'],
        'idsprsi': ['int'],
        'idsprsv': ['float'],
        'element': ['string'],
        'atomicnumber': ['int'],
        'corestates': ['int'],
        'magmom': ['float'],
        'flipspin': ['switch'],
        'magfield': ['float'],
        'vcaaddcharge': ['float'],
        'species': ['string'],
        'orbcomp': ['switch'],
        'l_relax': ['switch'],
        'l_magn': ['switch'],
        'm': ['float'],
        'alpha': ['float'],
        'beta': ['float'],
        'b_cons_x': ['float'],
        'b_cons_y': ['float'],
        'radius': ['float'],
        'gridpoints': ['int'],
        'logincrement': ['float'],
        'lmax': ['int'],
        'lnonsphr': ['int'],
        'lmaxapw': ['int'],
        's': ['int'],
        'p': ['int'],
        'd': ['int'],
        'f': ['int'],
        'l': ['int'],
        'u': ['float'],
        'j': ['float'],
        'l_amf': ['switch'],
        'calculate': ['switch'],
        'relaxxyz': ['string'],
        'type': ['string'],
        'n': ['int'],
        'ederiv': ['int'],
        'kmax': ['float'],
        'gmax': ['float'],
        'gmaxxc': ['float'],
        'numbands': ['int', 'string'],
        'valenceelectrons': ['float'],
        'mode': ['string'],
        'fermismearingenergy': ['float'],
        'fermismearingtemp': ['float'],
        'theta': ['float'],
        'phi': ['float'],
        'l_soc': ['switch'],
        'spav': ['switch'],
        'off': ['switch'],
        'soc66': ['switch'],
        'itmax': ['int'],
        'maxiterbroyd': ['int'],
        'imix': ['string'],
        'spinf': ['float'],
        'mindistance': ['float'],
        'maxtimetostartiter': ['float'],
        'layers': ['int'],
        'integ': ['switch'],
        'star': ['switch'],
        'nstars': ['int'],
        'locx1': ['float'],
        'locy1': ['float'],
        'locx2': ['float'],
        'locy2': ['float'],
        'nstm': ['int'],
        'tworkf': ['float'],
        'iplot': ['switch'],
        'score': ['switch'],
        'plplot': ['switch'],
        'numkpt': ['int'],
        'mineigenval': ['float'],
        'maxeigenval': ['float'],
        'nnne': ['int'],
        'pallst': ['switch'],
        'l_f': ['switch'],
        'xa': ['float'],
        'thetad': ['float'],
        'epsdisp': ['float'],
        'epsforce': ['float'],
        'qfix': ['switch'],
        'ndir': ['int'],
        'minenergy': ['float'],
        'maxenergy': ['float'],
        'sigma': ['float'],
        'nx': ['int'],
        'ny': ['int'],
        'nz': ['int'],
        'gamma': ['switch'],
        'count': ['int'],
        'posscale': ['float'],
        'weightscale': ['float'],
        'weight': ['float'],
        'qx': ['int'],
        'qy': ['int'],
        'qz': ['int'],
        'gw': ['int'],
        'pot8': ['switch'],
        'eig66': ['switch'],
        'lpr': ['int'],
        'isec1': ['int'],
        'secvar': ['switch'],
        'vchk': ['switch'],
        'cdinf': ['switch'],
        'disp': ['switch'],
        'form66': ['switch'],
        'eonly': ['switch'],
        'bmt': ['switch'],
        'dos': ['switch'],
        'band': ['switch'],
        'vacdos': ['switch'],
        'slice': ['switch'],
        'state': ['string']
    }),
    'inp_version':
    '0.27',
    'omitt_contained_tags': ['constants', 'atomSpecies', 'atomGroups', 'symmetryOperations'],
    'other_attribs':
    CaseInsensitiveDict({
        'j': ['/fleurInput/atomGroups/atomGroup/ldaU/@J', '/fleurInput/atomSpecies/species/ldaU/@J'],
        'm': ['/fleurInput/atomGroups/atomGroup/nocoParams/@M', '/fleurInput/atomSpecies/species/nocoParams/@M'],
        'u': ['/fleurInput/atomGroups/atomGroup/ldaU/@U', '/fleurInput/atomSpecies/species/ldaU/@U'],
        'alpha':
        ['/fleurInput/atomGroups/atomGroup/nocoParams/@alpha', '/fleurInput/atomSpecies/species/nocoParams/@alpha'],
        'atomicnumber': ['/fleurInput/atomSpecies/species/@atomicNumber'],
        'b_cons_x': [
            '/fleurInput/atomGroups/atomGroup/nocoParams/@b_cons_x',
            '/fleurInput/atomSpecies/species/nocoParams/@b_cons_x'
        ],
        'b_cons_y': [
            '/fleurInput/atomGroups/atomGroup/nocoParams/@b_cons_y',
            '/fleurInput/atomSpecies/species/nocoParams/@b_cons_y'
        ],
        'beta':
        ['/fleurInput/atomGroups/atomGroup/nocoParams/@beta', '/fleurInput/atomSpecies/species/nocoParams/@beta'],
        'calculate':
        ['/fleurInput/atomGroups/atomGroup/force/@calculate', '/fleurInput/atomSpecies/species/force/@calculate'],
        'corestates': ['/fleurInput/atomSpecies/species/@coreStates'],
        'd':
        ['/fleurInput/atomGroups/atomGroup/energyParameters/@d', '/fleurInput/atomSpecies/species/energyParameters/@d'],
        'ederiv': ['/fleurInput/atomGroups/atomGroup/lo/@eDeriv', '/fleurInput/atomSpecies/species/lo/@eDeriv'],
        'element': ['/fleurInput/atomSpecies/species/@element'],
        'f':
        ['/fleurInput/atomGroups/atomGroup/energyParameters/@f', '/fleurInput/atomSpecies/species/energyParameters/@f'],
        'flipspin': ['/fleurInput/atomSpecies/species/@flipSpin'],
        'gridpoints': [
            '/fleurInput/atomGroups/atomGroup/mtSphere/@gridPoints',
            '/fleurInput/atomSpecies/species/mtSphere/@gridPoints'
        ],
        'l': [
            '/fleurInput/atomGroups/atomGroup/ldaU/@l', '/fleurInput/atomGroups/atomGroup/lo/@l',
            '/fleurInput/atomSpecies/species/ldaU/@l', '/fleurInput/atomSpecies/species/lo/@l'
        ],
        'l_amf': ['/fleurInput/atomGroups/atomGroup/ldaU/@l_amf', '/fleurInput/atomSpecies/species/ldaU/@l_amf'],
        'l_magn':
        ['/fleurInput/atomGroups/atomGroup/nocoParams/@l_magn', '/fleurInput/atomSpecies/species/nocoParams/@l_magn'],
        'l_relax':
        ['/fleurInput/atomGroups/atomGroup/nocoParams/@l_relax', '/fleurInput/atomSpecies/species/nocoParams/@l_relax'],
        'lmax':
        ['/fleurInput/atomGroups/atomGroup/atomicCutoffs/@lmax', '/fleurInput/atomSpecies/species/atomicCutoffs/@lmax'],
        'lmaxapw': [
            '/fleurInput/atomGroups/atomGroup/atomicCutoffs/@lmaxAPW',
            '/fleurInput/atomSpecies/species/atomicCutoffs/@lmaxAPW'
        ],
        'lnonsphr': [
            '/fleurInput/atomGroups/atomGroup/atomicCutoffs/@lnonsphr',
            '/fleurInput/atomSpecies/species/atomicCutoffs/@lnonsphr'
        ],
        'logincrement': [
            '/fleurInput/atomGroups/atomGroup/mtSphere/@logIncrement',
            '/fleurInput/atomSpecies/species/mtSphere/@logIncrement'
        ],
        'magfield': ['/fleurInput/atomGroups/atomGroup/@magField', '/fleurInput/atomSpecies/species/@magField'],
        'magmom': ['/fleurInput/atomSpecies/species/@magMom'],
        'n': ['/fleurInput/atomGroups/atomGroup/lo/@n', '/fleurInput/atomSpecies/species/lo/@n'],
        'name': [
            '/fleurInput/atomSpecies/species/@name',
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint/@name',
            '/fleurInput/constants/constant/@name'
        ],
        'orbcomp': ['/fleurInput/atomGroups/atomGroup/@orbcomp'],
        'p':
        ['/fleurInput/atomGroups/atomGroup/energyParameters/@p', '/fleurInput/atomSpecies/species/energyParameters/@p'],
        'radius':
        ['/fleurInput/atomGroups/atomGroup/mtSphere/@radius', '/fleurInput/atomSpecies/species/mtSphere/@radius'],
        'relaxxyz':
        ['/fleurInput/atomGroups/atomGroup/force/@relaxXYZ', '/fleurInput/atomSpecies/species/force/@relaxXYZ'],
        's':
        ['/fleurInput/atomGroups/atomGroup/energyParameters/@s', '/fleurInput/atomSpecies/species/energyParameters/@s'],
        'species': ['/fleurInput/atomGroups/atomGroup/@species'],
        'spindown': [
            '/fleurInput/atomSpecies/species/electronConfig/stateOccupation/@spinDown',
            '/fleurInput/cell/filmLattice/vacuumEnergyParameters/@spinDown'
        ],
        'spinup': [
            '/fleurInput/atomSpecies/species/electronConfig/stateOccupation/@spinUp',
            '/fleurInput/cell/filmLattice/vacuumEnergyParameters/@spinUp'
        ],
        'state': ['/fleurInput/atomSpecies/species/electronConfig/stateOccupation/@state'],
        'type': ['/fleurInput/atomGroups/atomGroup/lo/@type', '/fleurInput/atomSpecies/species/lo/@type'],
        'vacuum': ['/fleurInput/cell/filmLattice/vacuumEnergyParameters/@vacuum'],
        'value': ['/fleurInput/constants/constant/@value'],
        'vcaaddcharge': [
            '/fleurInput/atomGroups/atomGroup/@vcaAddCharge', '/fleurInput/atomSpecies/species/@vcaAddCharge'
        ],
        'weight': ['/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint/@weight'],
        'abspos': ['/fleurInput/atomGroups/atomGroup/absPos'],
        'coreconfig': ['/fleurInput/atomSpecies/species/electronConfig/coreConfig'],
        'filmpos': ['/fleurInput/atomGroups/atomGroup/filmPos'],
        'kpoint': ['/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint'],
        'orbcomprot': ['/fleurInput/atomGroups/atomGroup/orbcomprot'],
        'relpos': ['/fleurInput/atomGroups/atomGroup/relPos'],
        'row-1': ['/fleurInput/cell/symmetryOperations/symOp/row-1'],
        'row-2': ['/fleurInput/cell/symmetryOperations/symOp/row-2'],
        'row-3': ['/fleurInput/cell/symmetryOperations/symOp/row-3'],
        'specialpoint': ['/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint'],
        'valenceconfig': ['/fleurInput/atomSpecies/species/electronConfig/valenceConfig']
    }),
    'root_tag':
    'fleurInput',
    'simple_elements':
    CaseInsensitiveDict({
        'comment': [{
            'type': ['string'],
            'length': 1
        }],
        'qss': [{
            'type': ['float'],
            'length': 3
        }],
        'qsc': [{
            'type': ['float'],
            'length': 3
        }],
        'a1': [{
            'type': ['float'],
            'length': 1
        }],
        'a2': [{
            'type': ['float'],
            'length': 1
        }],
        'c': [{
            'type': ['float'],
            'length': 1
        }],
        'row-1': [{
            'type': ['string'],
            'length': 2
        }, {
            'type': ['string'],
            'length': 3
        }, {
            'type': ['float'],
            'length': 4
        }],
        'row-2': [{
            'type': ['string'],
            'length': 2
        }, {
            'type': ['string'],
            'length': 3
        }, {
            'type': ['float'],
            'length': 4
        }],
        'row-3': [{
            'type': ['string'],
            'length': 3
        }, {
            'type': ['float'],
            'length': 4
        }],
        'relpos': [{
            'type': ['string'],
            'length': 3
        }],
        'abspos': [{
            'type': ['string'],
            'length': 3
        }],
        'filmpos': [{
            'type': ['string'],
            'length': 3
        }],
        'orbcomprot': [{
            'type': ['float'],
            'length': 3
        }],
        'specialpoint': [{
            'type': ['float'],
            'length': 3
        }],
        'kpoint': [{
            'type': ['float'],
            'length': 3
        }],
        'coreconfig': [{
            'type': ['string'],
            'length': 'unbounded'
        }],
        'valenceconfig': [{
            'type': ['string'],
            'length': 'unbounded'
        }]
    }),
    'tag_info': {
        '/fleurInput': {
            'attribs':
            CaseInsensitiveFrozenSet(['fleurInputVersion']),
            'optional':
            CaseInsensitiveFrozenSet(['comment', 'constants', 'output']),
            'optional_attribs':
            CaseInsensitiveFrozenSet([]),
            'order':
            CaseInsensitiveFrozenSet([
                'atomGroups', 'atomSpecies', 'calculationSetup', 'cell', 'comment', 'constants', 'output',
                'xcFunctional'
            ]),
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet(['comment']),
            'text':
            CaseInsensitiveFrozenSet(['comment'])
        },
        '/fleurInput/atomGroups': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet(['atomGroup']),
            'several': CaseInsensitiveFrozenSet(['atomGroup']),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup': {
            'attribs':
            CaseInsensitiveFrozenSet(['magField', 'orbcomp', 'species', 'vcaAddCharge']),
            'optional':
            CaseInsensitiveFrozenSet(
                ['atomicCutoffs', 'energyParameters', 'force', 'ldaU', 'lo', 'mtSphere', 'nocoParams', 'orbcomprot']),
            'optional_attribs':
            CaseInsensitiveFrozenSet(['magField', 'orbcomp', 'vcaAddCharge']),
            'order':
            CaseInsensitiveFrozenSet([
                'absPos', 'atomicCutoffs', 'energyParameters', 'filmPos', 'force', 'ldaU', 'lo', 'mtSphere',
                'nocoParams', 'orbcomprot', 'relPos'
            ]),
            'several':
            CaseInsensitiveFrozenSet(['absPos', 'filmPos', 'ldaU', 'lo', 'relPos']),
            'simple':
            CaseInsensitiveFrozenSet([
                'absPos', 'atomicCutoffs', 'energyParameters', 'filmPos', 'force', 'ldaU', 'lo', 'mtSphere',
                'nocoParams', 'orbcomprot', 'relPos'
            ]),
            'text':
            CaseInsensitiveFrozenSet(['absPos', 'filmPos', 'orbcomprot', 'relPos'])
        },
        '/fleurInput/atomGroups/atomGroup/atomicCutoffs': {
            'attribs': CaseInsensitiveFrozenSet(['lmax', 'lmaxAPW', 'lnonsphr']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet(['lmaxAPW']),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/energyParameters': {
            'attribs': CaseInsensitiveFrozenSet(['d', 'f', 'p', 's']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/force': {
            'attribs': CaseInsensitiveFrozenSet(['calculate', 'relaxXYZ']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/ldaU': {
            'attribs': CaseInsensitiveFrozenSet(['J', 'U', 'l', 'l_amf']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/lo': {
            'attribs': CaseInsensitiveFrozenSet(['eDeriv', 'l', 'n', 'type']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet(['eDeriv']),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/mtSphere': {
            'attribs': CaseInsensitiveFrozenSet(['gridPoints', 'logIncrement', 'radius']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/nocoParams': {
            'attribs': CaseInsensitiveFrozenSet(['M', 'alpha', 'b_cons_x', 'b_cons_y', 'beta', 'l_magn', 'l_relax']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet(['species']),
            'several': CaseInsensitiveFrozenSet(['species']),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species': {
            'attribs':
            CaseInsensitiveFrozenSet(
                ['atomicNumber', 'coreStates', 'element', 'flipSpin', 'magField', 'magMom', 'name', 'vcaAddCharge']),
            'optional':
            CaseInsensitiveFrozenSet(['electronConfig', 'energyParameters', 'force', 'ldaU', 'lo', 'nocoParams']),
            'optional_attribs':
            CaseInsensitiveFrozenSet(['flipSpin', 'magField', 'magMom', 'vcaAddCharge']),
            'order':
            CaseInsensitiveFrozenSet([
                'atomicCutoffs', 'electronConfig', 'energyParameters', 'force', 'ldaU', 'lo', 'mtSphere', 'nocoParams'
            ]),
            'several':
            CaseInsensitiveFrozenSet(['ldaU', 'lo']),
            'simple':
            CaseInsensitiveFrozenSet(
                ['atomicCutoffs', 'energyParameters', 'force', 'ldaU', 'lo', 'mtSphere', 'nocoParams']),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/atomicCutoffs': {
            'attribs': CaseInsensitiveFrozenSet(['lmax', 'lmaxAPW', 'lnonsphr']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet(['lmaxAPW']),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/electronConfig': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['stateOccupation', 'valenceConfig']),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet(['coreConfig', 'stateOccupation', 'valenceConfig']),
            'several': CaseInsensitiveFrozenSet(['stateOccupation']),
            'simple': CaseInsensitiveFrozenSet(['coreConfig', 'stateOccupation', 'valenceConfig']),
            'text': CaseInsensitiveFrozenSet(['coreConfig', 'valenceConfig'])
        },
        '/fleurInput/atomSpecies/species/electronConfig/stateOccupation': {
            'attribs': CaseInsensitiveFrozenSet(['spinDown', 'spinUp', 'state']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/energyParameters': {
            'attribs': CaseInsensitiveFrozenSet(['d', 'f', 'p', 's']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/force': {
            'attribs': CaseInsensitiveFrozenSet(['calculate', 'relaxXYZ']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/ldaU': {
            'attribs': CaseInsensitiveFrozenSet(['J', 'U', 'l', 'l_amf']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/lo': {
            'attribs': CaseInsensitiveFrozenSet(['eDeriv', 'l', 'n', 'type']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet(['eDeriv']),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/mtSphere': {
            'attribs': CaseInsensitiveFrozenSet(['gridPoints', 'logIncrement', 'radius']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/nocoParams': {
            'attribs': CaseInsensitiveFrozenSet(['M', 'alpha', 'b_cons_x', 'b_cons_y', 'beta', 'l_magn', 'l_relax']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup': {
            'attribs':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([
                'eField', 'energyParameterLimits', 'expertModes', 'geometryOptimization', 'nocoParams', 'oneDParams',
                'soc', 'spinSpiralQPointMesh'
            ]),
            'optional_attribs':
            CaseInsensitiveFrozenSet([]),
            'order':
            CaseInsensitiveFrozenSet([
                'bzIntegration', 'coreElectrons', 'cutoffs', 'eField', 'energyParameterLimits', 'expertModes',
                'geometryOptimization', 'magnetism', 'nocoParams', 'oneDParams', 'scfLoop', 'soc',
                'spinSpiralQPointMesh'
            ]),
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([
                'coreElectrons', 'cutoffs', 'eField', 'energyParameterLimits', 'expertModes', 'geometryOptimization',
                'magnetism', 'oneDParams', 'scfLoop', 'soc', 'spinSpiralQPointMesh'
            ]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/bzIntegration': {
            'attribs':
            CaseInsensitiveFrozenSet(['fermiSmearingEnergy', 'fermiSmearingTemp', 'mode', 'valenceElectrons']),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveFrozenSet(['fermiSmearingEnergy', 'fermiSmearingTemp', 'mode', 'valenceElectrons']),
            'order':
            CaseInsensitiveFrozenSet(['kPointCount', 'kPointList', 'kPointMesh']),
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet(['kPointMesh']),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointCount': {
            'attribs': CaseInsensitiveFrozenSet(['count', 'gamma']),
            'optional': CaseInsensitiveFrozenSet(['specialPoint']),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet(['specialPoint']),
            'several': CaseInsensitiveFrozenSet(['specialPoint']),
            'simple': CaseInsensitiveFrozenSet(['specialPoint']),
            'text': CaseInsensitiveFrozenSet(['specialPoint'])
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint': {
            'attribs': CaseInsensitiveFrozenSet(['name']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointList': {
            'attribs': CaseInsensitiveFrozenSet(['count', 'posScale', 'weightScale']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet(['count']),
            'order': CaseInsensitiveFrozenSet(['kPoint']),
            'several': CaseInsensitiveFrozenSet(['kPoint']),
            'simple': CaseInsensitiveFrozenSet(['kPoint']),
            'text': CaseInsensitiveFrozenSet(['kPoint'])
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint': {
            'attribs': CaseInsensitiveFrozenSet(['weight']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointMesh': {
            'attribs': CaseInsensitiveFrozenSet(['gamma', 'nx', 'ny', 'nz']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/coreElectrons': {
            'attribs': CaseInsensitiveFrozenSet(['ctail', 'frcor', 'kcrel']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet(['frcor', 'kcrel']),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/cutoffs': {
            'attribs': CaseInsensitiveFrozenSet(['Gmax', 'GmaxXC', 'Kmax', 'numbands']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet(['GmaxXC', 'numbands']),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/eField': {
            'attribs':
            CaseInsensitiveFrozenSet(
                ['autocomp', 'dirichlet', 'eV', 'plot_charge', 'plot_rho', 'sig_b_1', 'sig_b_2', 'zsigma']),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveFrozenSet(
                ['autocomp', 'dirichlet', 'eV', 'plot_charge', 'plot_rho', 'sig_b_1', 'sig_b_2', 'zsigma']),
            'order':
            CaseInsensitiveFrozenSet([]),
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/energyParameterLimits': {
            'attribs': CaseInsensitiveFrozenSet(['ellow', 'elup']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/expertModes': {
            'attribs': CaseInsensitiveFrozenSet(['eig66', 'gw', 'isec1', 'lpr', 'pot8', 'secvar']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet(['eig66', 'gw', 'isec1', 'lpr', 'pot8', 'secvar']),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/geometryOptimization': {
            'attribs': CaseInsensitiveFrozenSet(['epsdisp', 'epsforce', 'l_f', 'qfix', 'thetad', 'xa']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet(['qfix']),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/magnetism': {
            'attribs': CaseInsensitiveFrozenSet(['jspins', 'l_J', 'l_noco', 'lflip', 'swsp']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet(['l_J', 'l_noco', 'lflip', 'swsp']),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/nocoParams': {
            'attribs':
            CaseInsensitiveFrozenSet(['l_constr', 'l_disp', 'l_mperp', 'l_ss', 'mix_b', 'nsh', 'sso_opt', 'thetaJ']),
            'optional':
            CaseInsensitiveFrozenSet(['qsc']),
            'optional_attribs':
            CaseInsensitiveFrozenSet([]),
            'order':
            CaseInsensitiveFrozenSet(['qsc', 'qss']),
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet(['qsc', 'qss']),
            'text':
            CaseInsensitiveFrozenSet(['qsc', 'qss'])
        },
        '/fleurInput/calculationSetup/oneDParams': {
            'attribs': CaseInsensitiveFrozenSet(['MM', 'chi', 'd1', 'invs1', 'm_cyl', 'rot', 'vM', 'zrfs1']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/scfLoop': {
            'attribs':
            CaseInsensitiveFrozenSet(
                ['alpha', 'imix', 'itmax', 'maxIterBroyd', 'maxTimeToStartIter', 'minDistance', 'spinf']),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveFrozenSet(['maxIterBroyd', 'maxTimeToStartIter', 'minDistance', 'spinf']),
            'order':
            CaseInsensitiveFrozenSet([]),
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/soc': {
            'attribs': CaseInsensitiveFrozenSet(['l_soc', 'off', 'phi', 'soc66', 'spav', 'theta']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/spinSpiralQPointMesh': {
            'attribs': CaseInsensitiveFrozenSet(['qx', 'qy', 'qz']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell': {
            'attribs':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveFrozenSet([]),
            'order':
            CaseInsensitiveFrozenSet(['bulkLattice', 'filmLattice', 'symmetry', 'symmetryFile', 'symmetryOperations']),
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet(['symmetry', 'symmetryFile']),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/bulkLattice': {
            'attribs': CaseInsensitiveFrozenSet(['latnam', 'scale']),
            'optional': CaseInsensitiveFrozenSet(['a2']),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet(['a1', 'a2', 'bravaisMatrix', 'c', 'row-1', 'row-2']),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['a1', 'a2', 'c', 'row-1', 'row-2']),
            'text': CaseInsensitiveFrozenSet(['a1', 'a2', 'c', 'row-1', 'row-2'])
        },
        '/fleurInput/cell/bulkLattice/bravaisMatrix': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet(['row-1', 'row-2', 'row-3']),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['row-1', 'row-2', 'row-3']),
            'text': CaseInsensitiveFrozenSet(['row-1', 'row-2', 'row-3'])
        },
        '/fleurInput/cell/filmLattice': {
            'attribs': CaseInsensitiveFrozenSet(['dTilda', 'dVac', 'latnam', 'scale']),
            'optional': CaseInsensitiveFrozenSet(['a2', 'vacuumEnergyParameters']),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet(['a1', 'a2', 'bravaisMatrix', 'row-1', 'row-2',
                                               'vacuumEnergyParameters']),
            'several': CaseInsensitiveFrozenSet(['vacuumEnergyParameters']),
            'simple': CaseInsensitiveFrozenSet(['a1', 'a2', 'row-1', 'row-2', 'vacuumEnergyParameters']),
            'text': CaseInsensitiveFrozenSet(['a1', 'a2', 'row-1', 'row-2'])
        },
        '/fleurInput/cell/filmLattice/bravaisMatrix': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet(['row-1', 'row-2', 'row-3']),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['row-1', 'row-2', 'row-3']),
            'text': CaseInsensitiveFrozenSet(['row-1', 'row-2', 'row-3'])
        },
        '/fleurInput/cell/filmLattice/vacuumEnergyParameters': {
            'attribs': CaseInsensitiveFrozenSet(['spinDown', 'spinUp', 'vacuum']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet(['spinDown']),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/symmetry': {
            'attribs': CaseInsensitiveFrozenSet(['invs', 'spgrp', 'zrfs']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/symmetryFile': {
            'attribs': CaseInsensitiveFrozenSet(['filename']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/symmetryOperations': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet(['symOp']),
            'several': CaseInsensitiveFrozenSet(['symOp']),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/symmetryOperations/symOp': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet(['row-1', 'row-2', 'row-3']),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['row-1', 'row-2', 'row-3']),
            'text': CaseInsensitiveFrozenSet(['row-1', 'row-2', 'row-3'])
        },
        '/fleurInput/constants': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['constant']),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet(['constant']),
            'several': CaseInsensitiveFrozenSet(['constant']),
            'simple': CaseInsensitiveFrozenSet(['constant']),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/constants/constant': {
            'attribs': CaseInsensitiveFrozenSet(['name', 'value']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output': {
            'attribs':
            CaseInsensitiveFrozenSet(['band', 'dos', 'slice', 'vacdos']),
            'optional':
            CaseInsensitiveFrozenSet(
                ['chargeDensitySlicing', 'checks', 'densityOfStates', 'plotting', 'specialOutput', 'vacuumDOS']),
            'optional_attribs':
            CaseInsensitiveFrozenSet(['band', 'dos', 'slice', 'vacdos']),
            'order':
            CaseInsensitiveFrozenSet(
                ['chargeDensitySlicing', 'checks', 'densityOfStates', 'plotting', 'specialOutput', 'vacuumDOS']),
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet(
                ['chargeDensitySlicing', 'checks', 'densityOfStates', 'plotting', 'specialOutput', 'vacuumDOS']),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output/chargeDensitySlicing': {
            'attribs': CaseInsensitiveFrozenSet(['maxEigenval', 'minEigenval', 'nnne', 'numkpt', 'pallst']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output/checks': {
            'attribs': CaseInsensitiveFrozenSet(['cdinf', 'disp', 'vchk']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet(['cdinf', 'disp', 'vchk']),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output/densityOfStates': {
            'attribs': CaseInsensitiveFrozenSet(['maxEnergy', 'minEnergy', 'ndir', 'sigma']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output/plotting': {
            'attribs': CaseInsensitiveFrozenSet(['iplot', 'plplot', 'score']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet(['iplot', 'plplot', 'score']),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output/specialOutput': {
            'attribs': CaseInsensitiveFrozenSet(['bmt', 'eonly', 'form66']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet(['bmt', 'eonly', 'form66']),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output/vacuumDOS': {
            'attribs':
            CaseInsensitiveFrozenSet(
                ['integ', 'layers', 'locx1', 'locx2', 'locy1', 'locy2', 'nstars', 'nstm', 'star', 'tworkf']),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveFrozenSet([]),
            'order':
            CaseInsensitiveFrozenSet([]),
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/xcFunctional': {
            'attribs': CaseInsensitiveFrozenSet(['name', 'relativisticCorrections']),
            'optional': CaseInsensitiveFrozenSet(['ggaPrinting', 'xcParams']),
            'optional_attribs': CaseInsensitiveFrozenSet(['relativisticCorrections']),
            'order': CaseInsensitiveFrozenSet(['ggaPrinting', 'xcParams']),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['ggaPrinting', 'xcParams']),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/xcFunctional/ggaPrinting': {
            'attribs': CaseInsensitiveFrozenSet(['idsprs0', 'idsprsi', 'idsprsl', 'idsprsv', 'iggachk']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/xcFunctional/xcParams': {
            'attribs': CaseInsensitiveFrozenSet(['chng', 'idsprs', 'igrd', 'lwb', 'ndvgrd']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveFrozenSet([]),
            'order': CaseInsensitiveFrozenSet([]),
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        }
    },
    'tag_paths':
    CaseInsensitiveDict({
        'a1': ['/fleurInput/cell/bulkLattice/a1', '/fleurInput/cell/filmLattice/a1'],
        'a2': ['/fleurInput/cell/bulkLattice/a2', '/fleurInput/cell/filmLattice/a2'],
        'abspos':
        '/fleurInput/atomGroups/atomGroup/absPos',
        'atomgroup':
        '/fleurInput/atomGroups/atomGroup',
        'atomgroups':
        '/fleurInput/atomGroups',
        'atomspecies':
        '/fleurInput/atomSpecies',
        'atomiccutoffs':
        ['/fleurInput/atomGroups/atomGroup/atomicCutoffs', '/fleurInput/atomSpecies/species/atomicCutoffs'],
        'bravaismatrix': ['/fleurInput/cell/bulkLattice/bravaisMatrix', '/fleurInput/cell/filmLattice/bravaisMatrix'],
        'bulklattice':
        '/fleurInput/cell/bulkLattice',
        'bzintegration':
        '/fleurInput/calculationSetup/bzIntegration',
        'c':
        '/fleurInput/cell/bulkLattice/c',
        'calculationsetup':
        '/fleurInput/calculationSetup',
        'cell':
        '/fleurInput/cell',
        'chargedensityslicing':
        '/fleurInput/output/chargeDensitySlicing',
        'checks':
        '/fleurInput/output/checks',
        'comment':
        '/fleurInput/comment',
        'constant':
        '/fleurInput/constants/constant',
        'constants':
        '/fleurInput/constants',
        'coreconfig':
        '/fleurInput/atomSpecies/species/electronConfig/coreConfig',
        'coreelectrons':
        '/fleurInput/calculationSetup/coreElectrons',
        'cutoffs':
        '/fleurInput/calculationSetup/cutoffs',
        'densityofstates':
        '/fleurInput/output/densityOfStates',
        'efield':
        '/fleurInput/calculationSetup/eField',
        'electronconfig':
        '/fleurInput/atomSpecies/species/electronConfig',
        'energyparameterlimits':
        '/fleurInput/calculationSetup/energyParameterLimits',
        'energyparameters':
        ['/fleurInput/atomGroups/atomGroup/energyParameters', '/fleurInput/atomSpecies/species/energyParameters'],
        'expertmodes':
        '/fleurInput/calculationSetup/expertModes',
        'filmlattice':
        '/fleurInput/cell/filmLattice',
        'filmpos':
        '/fleurInput/atomGroups/atomGroup/filmPos',
        'fleurinput':
        '/fleurInput',
        'force': ['/fleurInput/atomGroups/atomGroup/force', '/fleurInput/atomSpecies/species/force'],
        'geometryoptimization':
        '/fleurInput/calculationSetup/geometryOptimization',
        'ggaprinting':
        '/fleurInput/xcFunctional/ggaPrinting',
        'kpoint':
        '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint',
        'kpointcount':
        '/fleurInput/calculationSetup/bzIntegration/kPointCount',
        'kpointlist':
        '/fleurInput/calculationSetup/bzIntegration/kPointList',
        'kpointmesh':
        '/fleurInput/calculationSetup/bzIntegration/kPointMesh',
        'ldau': ['/fleurInput/atomGroups/atomGroup/ldaU', '/fleurInput/atomSpecies/species/ldaU'],
        'lo': ['/fleurInput/atomGroups/atomGroup/lo', '/fleurInput/atomSpecies/species/lo'],
        'magnetism':
        '/fleurInput/calculationSetup/magnetism',
        'mtsphere': ['/fleurInput/atomGroups/atomGroup/mtSphere', '/fleurInput/atomSpecies/species/mtSphere'],
        'nocoparams': [
            '/fleurInput/atomGroups/atomGroup/nocoParams', '/fleurInput/atomSpecies/species/nocoParams',
            '/fleurInput/calculationSetup/nocoParams'
        ],
        'onedparams':
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
        'relpos':
        '/fleurInput/atomGroups/atomGroup/relPos',
        'row-1': [
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-1', '/fleurInput/cell/bulkLattice/row-1',
            '/fleurInput/cell/filmLattice/bravaisMatrix/row-1', '/fleurInput/cell/filmLattice/row-1',
            '/fleurInput/cell/symmetryOperations/symOp/row-1'
        ],
        'row-2': [
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-2', '/fleurInput/cell/bulkLattice/row-2',
            '/fleurInput/cell/filmLattice/bravaisMatrix/row-2', '/fleurInput/cell/filmLattice/row-2',
            '/fleurInput/cell/symmetryOperations/symOp/row-2'
        ],
        'row-3': [
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-3', '/fleurInput/cell/filmLattice/bravaisMatrix/row-3',
            '/fleurInput/cell/symmetryOperations/symOp/row-3'
        ],
        'scfloop':
        '/fleurInput/calculationSetup/scfLoop',
        'soc':
        '/fleurInput/calculationSetup/soc',
        'specialoutput':
        '/fleurInput/output/specialOutput',
        'specialpoint':
        '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint',
        'species':
        '/fleurInput/atomSpecies/species',
        'spinspiralqpointmesh':
        '/fleurInput/calculationSetup/spinSpiralQPointMesh',
        'stateoccupation':
        '/fleurInput/atomSpecies/species/electronConfig/stateOccupation',
        'symop':
        '/fleurInput/cell/symmetryOperations/symOp',
        'symmetry':
        '/fleurInput/cell/symmetry',
        'symmetryfile':
        '/fleurInput/cell/symmetryFile',
        'symmetryoperations':
        '/fleurInput/cell/symmetryOperations',
        'vacuumdos':
        '/fleurInput/output/vacuumDOS',
        'vacuumenergyparameters':
        '/fleurInput/cell/filmLattice/vacuumEnergyParameters',
        'valenceconfig':
        '/fleurInput/atomSpecies/species/electronConfig/valenceConfig',
        'xcfunctional':
        '/fleurInput/xcFunctional',
        'xcparams':
        '/fleurInput/xcFunctional/xcParams'
    }),
    'unique_attribs':
    CaseInsensitiveDict({
        'gmax': '/fleurInput/calculationSetup/cutoffs/@Gmax',
        'gmaxxc': '/fleurInput/calculationSetup/cutoffs/@GmaxXC',
        'kmax': '/fleurInput/calculationSetup/cutoffs/@Kmax',
        'mm': '/fleurInput/calculationSetup/oneDParams/@MM',
        'alpha': '/fleurInput/calculationSetup/scfLoop/@alpha',
        'autocomp': '/fleurInput/calculationSetup/eField/@autocomp',
        'band': '/fleurInput/output/@band',
        'bmt': '/fleurInput/output/specialOutput/@bmt',
        'cdinf': '/fleurInput/output/checks/@cdinf',
        'chi': '/fleurInput/calculationSetup/oneDParams/@chi',
        'chng': '/fleurInput/xcFunctional/xcParams/@chng',
        'ctail': '/fleurInput/calculationSetup/coreElectrons/@ctail',
        'd1': '/fleurInput/calculationSetup/oneDParams/@d1',
        'dtilda': '/fleurInput/cell/filmLattice/@dTilda',
        'dvac': '/fleurInput/cell/filmLattice/@dVac',
        'dirichlet': '/fleurInput/calculationSetup/eField/@dirichlet',
        'disp': '/fleurInput/output/checks/@disp',
        'dos': '/fleurInput/output/@dos',
        'ev': '/fleurInput/calculationSetup/eField/@eV',
        'eig66': '/fleurInput/calculationSetup/expertModes/@eig66',
        'ellow': '/fleurInput/calculationSetup/energyParameterLimits/@ellow',
        'elup': '/fleurInput/calculationSetup/energyParameterLimits/@elup',
        'eonly': '/fleurInput/output/specialOutput/@eonly',
        'epsdisp': '/fleurInput/calculationSetup/geometryOptimization/@epsdisp',
        'epsforce': '/fleurInput/calculationSetup/geometryOptimization/@epsforce',
        'fermismearingenergy': '/fleurInput/calculationSetup/bzIntegration/@fermiSmearingEnergy',
        'fermismearingtemp': '/fleurInput/calculationSetup/bzIntegration/@fermiSmearingTemp',
        'filename': '/fleurInput/cell/symmetryFile/@filename',
        'fleurinputversion': '/fleurInput/@fleurInputVersion',
        'form66': '/fleurInput/output/specialOutput/@form66',
        'frcor': '/fleurInput/calculationSetup/coreElectrons/@frcor',
        'gw': '/fleurInput/calculationSetup/expertModes/@gw',
        'idsprs': '/fleurInput/xcFunctional/xcParams/@idsprs',
        'idsprs0': '/fleurInput/xcFunctional/ggaPrinting/@idsprs0',
        'idsprsi': '/fleurInput/xcFunctional/ggaPrinting/@idsprsi',
        'idsprsl': '/fleurInput/xcFunctional/ggaPrinting/@idsprsl',
        'idsprsv': '/fleurInput/xcFunctional/ggaPrinting/@idsprsv',
        'iggachk': '/fleurInput/xcFunctional/ggaPrinting/@iggachk',
        'igrd': '/fleurInput/xcFunctional/xcParams/@igrd',
        'imix': '/fleurInput/calculationSetup/scfLoop/@imix',
        'integ': '/fleurInput/output/vacuumDOS/@integ',
        'invs': '/fleurInput/cell/symmetry/@invs',
        'invs1': '/fleurInput/calculationSetup/oneDParams/@invs1',
        'iplot': '/fleurInput/output/plotting/@iplot',
        'isec1': '/fleurInput/calculationSetup/expertModes/@isec1',
        'itmax': '/fleurInput/calculationSetup/scfLoop/@itmax',
        'jspins': '/fleurInput/calculationSetup/magnetism/@jspins',
        'kcrel': '/fleurInput/calculationSetup/coreElectrons/@kcrel',
        'l_j': '/fleurInput/calculationSetup/magnetism/@l_J',
        'l_constr': '/fleurInput/calculationSetup/nocoParams/@l_constr',
        'l_disp': '/fleurInput/calculationSetup/nocoParams/@l_disp',
        'l_f': '/fleurInput/calculationSetup/geometryOptimization/@l_f',
        'l_mperp': '/fleurInput/calculationSetup/nocoParams/@l_mperp',
        'l_noco': '/fleurInput/calculationSetup/magnetism/@l_noco',
        'l_soc': '/fleurInput/calculationSetup/soc/@l_soc',
        'l_ss': '/fleurInput/calculationSetup/nocoParams/@l_ss',
        'layers': '/fleurInput/output/vacuumDOS/@layers',
        'lflip': '/fleurInput/calculationSetup/magnetism/@lflip',
        'locx1': '/fleurInput/output/vacuumDOS/@locx1',
        'locx2': '/fleurInput/output/vacuumDOS/@locx2',
        'locy1': '/fleurInput/output/vacuumDOS/@locy1',
        'locy2': '/fleurInput/output/vacuumDOS/@locy2',
        'lpr': '/fleurInput/calculationSetup/expertModes/@lpr',
        'lwb': '/fleurInput/xcFunctional/xcParams/@lwb',
        'm_cyl': '/fleurInput/calculationSetup/oneDParams/@m_cyl',
        'maxeigenval': '/fleurInput/output/chargeDensitySlicing/@maxEigenval',
        'maxenergy': '/fleurInput/output/densityOfStates/@maxEnergy',
        'maxiterbroyd': '/fleurInput/calculationSetup/scfLoop/@maxIterBroyd',
        'maxtimetostartiter': '/fleurInput/calculationSetup/scfLoop/@maxTimeToStartIter',
        'mindistance': '/fleurInput/calculationSetup/scfLoop/@minDistance',
        'mineigenval': '/fleurInput/output/chargeDensitySlicing/@minEigenval',
        'minenergy': '/fleurInput/output/densityOfStates/@minEnergy',
        'mix_b': '/fleurInput/calculationSetup/nocoParams/@mix_b',
        'mode': '/fleurInput/calculationSetup/bzIntegration/@mode',
        'name': '/fleurInput/xcFunctional/@name',
        'ndir': '/fleurInput/output/densityOfStates/@ndir',
        'ndvgrd': '/fleurInput/xcFunctional/xcParams/@ndvgrd',
        'nnne': '/fleurInput/output/chargeDensitySlicing/@nnne',
        'nsh': '/fleurInput/calculationSetup/nocoParams/@nsh',
        'nstars': '/fleurInput/output/vacuumDOS/@nstars',
        'nstm': '/fleurInput/output/vacuumDOS/@nstm',
        'numbands': '/fleurInput/calculationSetup/cutoffs/@numbands',
        'numkpt': '/fleurInput/output/chargeDensitySlicing/@numkpt',
        'nx': '/fleurInput/calculationSetup/bzIntegration/kPointMesh/@nx',
        'ny': '/fleurInput/calculationSetup/bzIntegration/kPointMesh/@ny',
        'nz': '/fleurInput/calculationSetup/bzIntegration/kPointMesh/@nz',
        'off': '/fleurInput/calculationSetup/soc/@off',
        'pallst': '/fleurInput/output/chargeDensitySlicing/@pallst',
        'phi': '/fleurInput/calculationSetup/soc/@phi',
        'plot_charge': '/fleurInput/calculationSetup/eField/@plot_charge',
        'plot_rho': '/fleurInput/calculationSetup/eField/@plot_rho',
        'plplot': '/fleurInput/output/plotting/@plplot',
        'posscale': '/fleurInput/calculationSetup/bzIntegration/kPointList/@posScale',
        'pot8': '/fleurInput/calculationSetup/expertModes/@pot8',
        'qfix': '/fleurInput/calculationSetup/geometryOptimization/@qfix',
        'qx': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qx',
        'qy': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qy',
        'qz': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qz',
        'relativisticcorrections': '/fleurInput/xcFunctional/@relativisticCorrections',
        'rot': '/fleurInput/calculationSetup/oneDParams/@rot',
        'score': '/fleurInput/output/plotting/@score',
        'secvar': '/fleurInput/calculationSetup/expertModes/@secvar',
        'sig_b_1': '/fleurInput/calculationSetup/eField/@sig_b_1',
        'sig_b_2': '/fleurInput/calculationSetup/eField/@sig_b_2',
        'sigma': '/fleurInput/output/densityOfStates/@sigma',
        'slice': '/fleurInput/output/@slice',
        'soc66': '/fleurInput/calculationSetup/soc/@soc66',
        'spav': '/fleurInput/calculationSetup/soc/@spav',
        'spgrp': '/fleurInput/cell/symmetry/@spgrp',
        'spinf': '/fleurInput/calculationSetup/scfLoop/@spinf',
        'sso_opt': '/fleurInput/calculationSetup/nocoParams/@sso_opt',
        'star': '/fleurInput/output/vacuumDOS/@star',
        'swsp': '/fleurInput/calculationSetup/magnetism/@swsp',
        'theta': '/fleurInput/calculationSetup/soc/@theta',
        'thetaj': '/fleurInput/calculationSetup/nocoParams/@thetaJ',
        'thetad': '/fleurInput/calculationSetup/geometryOptimization/@thetad',
        'tworkf': '/fleurInput/output/vacuumDOS/@tworkf',
        'vm': '/fleurInput/calculationSetup/oneDParams/@vM',
        'vacdos': '/fleurInput/output/@vacdos',
        'valenceelectrons': '/fleurInput/calculationSetup/bzIntegration/@valenceElectrons',
        'vchk': '/fleurInput/output/checks/@vchk',
        'weightscale': '/fleurInput/calculationSetup/bzIntegration/kPointList/@weightScale',
        'xa': '/fleurInput/calculationSetup/geometryOptimization/@xa',
        'zrfs': '/fleurInput/cell/symmetry/@zrfs',
        'zrfs1': '/fleurInput/calculationSetup/oneDParams/@zrfs1',
        'zsigma': '/fleurInput/calculationSetup/eField/@zsigma',
        'c': '/fleurInput/cell/bulkLattice/c',
        'comment': '/fleurInput/comment',
        'qsc': '/fleurInput/calculationSetup/nocoParams/qsc',
        'qss': '/fleurInput/calculationSetup/nocoParams/qss'
    }),
    'unique_path_attribs':
    CaseInsensitiveDict({
        'count': [
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/@count',
            '/fleurInput/calculationSetup/bzIntegration/kPointList/@count'
        ],
        'gamma': [
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/@gamma',
            '/fleurInput/calculationSetup/bzIntegration/kPointMesh/@gamma'
        ],
        'latnam': ['/fleurInput/cell/bulkLattice/@latnam', '/fleurInput/cell/filmLattice/@latnam'],
        'scale': ['/fleurInput/cell/bulkLattice/@scale', '/fleurInput/cell/filmLattice/@scale'],
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
