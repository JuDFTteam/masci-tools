# -*- coding: utf-8 -*-
"""
This file contains information parsed from the FleurInputSchema.xsd
for version 0.30

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
__inp_version__ = '0.30'
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
        'ForceMixEnum': {
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
    'attrib_types':
    CaseInsensitiveDict({
        'fleurinputversion': ['string'],
        'name': ['string'],
        'value': ['string'],
        'ellow': ['string'],
        'elup': ['string'],
        'b_field': ['string'],
        'zsigma': ['string'],
        'sig_b_1': ['string'],
        'sig_b_2': ['string'],
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
        'mix_b': ['string'],
        'thetaj': ['string'],
        'nsh': ['int'],
        'l_mtnocopot': ['switch'],
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
        'coretail_lmax': ['int'],
        'spgrp': ['string'],
        'invs': ['switch'],
        'zrfs': ['switch'],
        'filename': ['string'],
        'jspins': ['int'],
        'l_noco': ['switch'],
        'l_j': ['switch'],
        'swsp': ['switch'],
        'lflip': ['switch'],
        'fixed_moment': ['string'],
        'scale': ['string'],
        'latnam': ['string'],
        'dvac': ['string'],
        'dtilda': ['string'],
        'vacuum': ['int'],
        'spinup': ['string'],
        'spindown': ['string'],
        'relativisticcorrections': ['switch'],
        'gcutm': ['float'],
        'bands': ['int'],
        'tolerance': ['float'],
        'lexp': ['int'],
        'ewaldlambda': ['int'],
        'exchange': ['int', 'string'],
        'correlation': ['int', 'string'],
        'etot_exchange': ['int', 'string'],
        'etot_correlation': ['int', 'string'],
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
        'lcutm': ['int'],
        'lcutwf': ['int'],
        'select': ['string'],
        'lda': ['switch'],
        'socscale': ['float'],
        'b_field_mt': ['string'],
        'vca_charge': ['string'],
        'element': ['string'],
        'atomicnumber': ['int'],
        'corestates': ['int'],
        'magmom': ['string'],
        'flipspin': ['switch'],
        'magfield': ['float'],
        'vcaaddcharge': ['float'],
        'species': ['string'],
        'label': ['string'],
        'wannier': ['switch'],
        'orbcomp': ['switch'],
        'l_relax': ['switch'],
        'l_magn': ['switch'],
        'm': ['string'],
        'alpha': ['string'],
        'beta': ['string'],
        'b_cons_x': ['string'],
        'b_cons_y': ['string'],
        'radius': ['string'],
        'gridpoints': ['int'],
        'logincrement': ['string'],
        'lmax': ['int'],
        'lnonsphr': ['int'],
        'lmaxapw': ['int'],
        's': ['int'],
        'p': ['int'],
        'd': ['int'],
        'f': ['int'],
        'l': ['int'],
        'u': ['string'],
        'j': ['string'],
        'phi': ['string'],
        'theta': ['string'],
        'l_amf': ['switch'],
        'calculate': ['switch'],
        'relaxxyz': ['string'],
        'type': ['string'],
        'n': ['int'],
        'ederiv': ['int'],
        'kmax': ['string'],
        'gmax': ['string'],
        'gmaxxc': ['string'],
        'numbands': ['int', 'string'],
        'valenceelectrons': ['string'],
        'mode': ['string'],
        'fermismearingenergy': ['string'],
        'fermismearingtemp': ['string'],
        'l_soc': ['switch'],
        'spav': ['switch'],
        'off': ['switch'],
        'soc66': ['switch'],
        'itmax': ['int'],
        'maxiterbroyd': ['int'],
        'imix': ['string'],
        'precondparam': ['string'],
        'spinf': ['float', 'string'],
        'mindistance': ['string'],
        'maxtimetostartiter': ['string'],
        'layers': ['int'],
        'integ': ['switch'],
        'star': ['switch'],
        'nstars': ['int'],
        'locx1': ['string'],
        'locy1': ['string'],
        'locx2': ['string'],
        'locy2': ['string'],
        'nstm': ['int'],
        'tworkf': ['string'],
        'iplot': ['int'],
        'score': ['switch'],
        'plplot': ['switch'],
        'numkpt': ['int'],
        'mineigenval': ['string'],
        'maxeigenval': ['string'],
        'nnne': ['int'],
        'pallst': ['switch'],
        'l_f': ['switch'],
        'forcealpha': ['string'],
        'epsdisp': ['string'],
        'epsforce': ['string'],
        'forcemix': ['string'],
        'qfix': ['int'],
        'force_converged': ['string'],
        'l_linmix': ['switch'],
        'mixparam': ['float'],
        'l_rdmft': ['switch'],
        'occeps': ['float'],
        'statesbelow': ['int'],
        'statesabove': ['int'],
        'functional': ['string'],
        'ndir': ['int'],
        'minenergy': ['string'],
        'maxenergy': ['string'],
        'sigma': ['string'],
        'purpose': ['string'],
        'nx': ['int'],
        'ny': ['int'],
        'nz': ['int'],
        'gamma': ['switch'],
        'count': ['int'],
        'posscale': ['string'],
        'weightscale': ['string'],
        'denx': ['float'],
        'deny': ['float'],
        'denz': ['float'],
        'weight': ['string'],
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
        'ekin': ['float'],
        'atomtype': ['int'],
        'edgetype': ['string'],
        'emin': ['float'],
        'emax': ['float'],
        'numpoints': ['int'],
        'verbose': ['switch'],
        'nqphi': ['int'],
        'nqr': ['int'],
        'alpha_ex': ['float'],
        'beta_ex': ['float'],
        'i_initial': ['float'],
        'energylo': ['float'],
        'energyup': ['float'],
        'minspinup': ['int'],
        'maxspinup': ['int'],
        'minspindown': ['int'],
        'maxspindown': ['int'],
        'ms': ['switch'],
        'sgwf': ['switch'],
        'socgwf': ['switch'],
        'bscomf': ['switch'],
        'atomlist': ['switch'],
        'energy': ['string'],
        'unfoldband': ['switch'],
        'supercellx': ['int'],
        'supercelly': ['int'],
        'supercellz': ['int'],
        'dos': ['switch'],
        'band': ['switch'],
        'vacdos': ['switch'],
        'slice': ['switch'],
        'corespec': ['switch'],
        'mcd': ['switch'],
        'state': ['string']
    }),
    'inp_version':
    '0.30',
    'omitt_contained_tags': [
        'constants', 'atomSpecies', 'atomGroups', 'symmetryOperations', 'displacements', 'relaxation-history',
        'spinSpiralDispersion', 'qVectors'
    ],
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
        'b_field_mt': ['/fleurInput/atomSpecies/species/special/@b_field_mt'],
        'beta':
        ['/fleurInput/atomGroups/atomGroup/nocoParams/@beta', '/fleurInput/atomSpecies/species/nocoParams/@beta'],
        'calculate':
        ['/fleurInput/atomGroups/atomGroup/force/@calculate', '/fleurInput/atomSpecies/species/force/@calculate'],
        'corestates': ['/fleurInput/atomSpecies/species/@coreStates'],
        'count': [
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/@count',
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList/@count'
        ],
        'd':
        ['/fleurInput/atomGroups/atomGroup/energyParameters/@d', '/fleurInput/atomSpecies/species/energyParameters/@d'],
        'denx': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointDensity/@denX'],
        'deny': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointDensity/@denY'],
        'denz': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointDensity/@denZ'],
        'ederiv': ['/fleurInput/atomGroups/atomGroup/lo/@eDeriv', '/fleurInput/atomSpecies/species/lo/@eDeriv'],
        'element': ['/fleurInput/atomSpecies/species/@element'],
        'energy': ['/fleurInput/relaxation/relaxation-history/step/@energy'],
        'f':
        ['/fleurInput/atomGroups/atomGroup/energyParameters/@f', '/fleurInput/atomSpecies/species/energyParameters/@f'],
        'filename': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointListFile/@filename'],
        'flipspin': ['/fleurInput/atomSpecies/species/@flipSpin'],
        'gamma': [
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/@gamma',
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointDensity/@gamma',
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointMesh/@gamma'
        ],
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
        'label': [
            '/fleurInput/atomGroups/atomGroup/absPos/@label', '/fleurInput/atomGroups/atomGroup/filmPos/@label',
            '/fleurInput/atomGroups/atomGroup/relPos/@label'
        ],
        'lcutm': ['/fleurInput/atomSpecies/species/prodBasis/@lcutm'],
        'lcutwf': ['/fleurInput/atomSpecies/species/prodBasis/@lcutwf'],
        'lda': ['/fleurInput/atomSpecies/species/special/@lda'],
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
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/specialPoint/@name',
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint/@name',
            '/fleurInput/constants/constant/@name'
        ],
        'nx': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointMesh/@nx'],
        'ny': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointMesh/@ny'],
        'nz': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointMesh/@nz'],
        'orbcomp': [
            '/fleurInput/atomGroups/atomGroup/absPos/@orbcomp', '/fleurInput/atomGroups/atomGroup/filmPos/@orbcomp',
            '/fleurInput/atomGroups/atomGroup/relPos/@orbcomp'
        ],
        'p':
        ['/fleurInput/atomGroups/atomGroup/energyParameters/@p', '/fleurInput/atomSpecies/species/energyParameters/@p'],
        'phi': ['/fleurInput/atomGroups/atomGroup/ldaU/@phi', '/fleurInput/atomSpecies/species/ldaU/@phi'],
        'posscale': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList/@posScale'],
        'purpose': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/@purpose'],
        'radius':
        ['/fleurInput/atomGroups/atomGroup/mtSphere/@radius', '/fleurInput/atomSpecies/species/mtSphere/@radius'],
        'relaxxyz':
        ['/fleurInput/atomGroups/atomGroup/force/@relaxXYZ', '/fleurInput/atomSpecies/species/force/@relaxXYZ'],
        's':
        ['/fleurInput/atomGroups/atomGroup/energyParameters/@s', '/fleurInput/atomSpecies/species/energyParameters/@s'],
        'select': ['/fleurInput/atomSpecies/species/prodBasis/@select'],
        'socscale': ['/fleurInput/atomSpecies/species/special/@socscale'],
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
        'theta': ['/fleurInput/atomGroups/atomGroup/ldaU/@theta', '/fleurInput/atomSpecies/species/ldaU/@theta'],
        'type': ['/fleurInput/atomGroups/atomGroup/lo/@type', '/fleurInput/atomSpecies/species/lo/@type'],
        'vacuum': ['/fleurInput/cell/filmLattice/vacuumEnergyParameters/@vacuum'],
        'value': ['/fleurInput/constants/constant/@value'],
        'vcaaddcharge': [
            '/fleurInput/atomGroups/atomGroup/@vcaAddCharge', '/fleurInput/atomSpecies/species/@vcaAddCharge'
        ],
        'vca_charge': ['/fleurInput/atomSpecies/species/special/@vca_charge'],
        'wannier': [
            '/fleurInput/atomGroups/atomGroup/absPos/@wannier', '/fleurInput/atomGroups/atomGroup/filmPos/@wannier',
            '/fleurInput/atomGroups/atomGroup/relPos/@wannier'
        ],
        'weight': [
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList/kPoint/@weight',
            '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint/@weight'
        ],
        'weightscale': ['/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList/@weightScale'],
        'abspos': ['/fleurInput/atomGroups/atomGroup/absPos'],
        'coreconfig': ['/fleurInput/atomSpecies/species/electronConfig/coreConfig'],
        'displace': ['/fleurInput/relaxation/displacements/displace'],
        'filmpos': ['/fleurInput/atomGroups/atomGroup/filmPos'],
        'kpoint': [
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList/kPoint',
            '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint'
        ],
        'orbcomprot': ['/fleurInput/atomGroups/atomGroup/orbcomprot'],
        'posforce': ['/fleurInput/relaxation/relaxation-history/step/posforce'],
        'q': [
            '/fleurInput/forceTheorem/DMI/qVectors/q', '/fleurInput/forceTheorem/Jij/qVectors/q',
            '/fleurInput/forceTheorem/spinSpiralDispersion/q'
        ],
        'relpos': ['/fleurInput/atomGroups/atomGroup/relPos'],
        'row-1': ['/fleurInput/cell/symmetryOperations/symOp/row-1'],
        'row-2': ['/fleurInput/cell/symmetryOperations/symOp/row-2'],
        'row-3': ['/fleurInput/cell/symmetryOperations/symOp/row-3'],
        'shape': ['/fleurInput/calculationSetup/fields/shape'],
        'specialpoint': [
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/specialPoint',
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint'
        ],
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
            'optional_attribs': [],
            'order': [
                'comment', 'constants', 'calculationSetup', 'cell', 'xcFunctional', 'atomSpecies', 'atomGroups',
                'output', 'forceTheorem', 'relaxation'
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
            'attribs': ['l', 'U', 'J', 'phi', 'theta', 'l_amf'],
            'optional': [],
            'optional_attribs': ['phi', 'theta'],
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
            'attribs': ['l', 'U', 'J', 'phi', 'theta', 'l_amf'],
            'optional': [],
            'optional_attribs': ['phi', 'theta'],
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
            'attribs': ['lda', 'socscale', 'b_field_mt', 'vca_charge'],
            'optional': [],
            'optional_attribs': ['lda', 'socscale', 'b_field_mt', 'vca_charge'],
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
            'optional_attribs': [],
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
            'optional_attribs': ['valenceElectrons', 'mode', 'fermiSmearingEnergy', 'fermiSmearingTemp'],
            'order': ['kPointMesh', 'kPointCount', 'kPointList', 'kPointDensity', 'altKPointSet'],
            'several': ['altKPointSet'],
            'simple': ['kPointMesh', 'kPointDensity'],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet': {
            'attribs': ['purpose'],
            'optional': [],
            'optional_attribs': [],
            'order': ['kPointMesh', 'kPointCount', 'kPointList', 'kPointDensity', 'kPointListFile'],
            'several': [],
            'simple': ['kPointMesh', 'kPointDensity', 'kPointListFile'],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount': {
            'attribs': ['count', 'gamma'],
            'optional': ['specialPoint'],
            'optional_attribs': [],
            'order': ['specialPoint'],
            'several': ['specialPoint'],
            'simple': ['specialPoint'],
            'text': ['specialPoint']
        },
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/specialPoint': {
            'attribs': ['name'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointDensity': {
            'attribs': ['denX', 'denY', 'denZ', 'gamma'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList': {
            'attribs': ['posScale', 'weightScale', 'count'],
            'optional': [],
            'optional_attribs': ['count'],
            'order': ['kPoint'],
            'several': ['kPoint'],
            'simple': ['kPoint'],
            'text': ['kPoint']
        },
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList/kPoint': {
            'attribs': ['weight'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointListFile': {
            'attribs': ['filename'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointMesh': {
            'attribs': ['nx', 'ny', 'nz', 'gamma'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
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
        '/fleurInput/calculationSetup/fields': {
            'attribs':
            ['b_field', 'zsigma', 'sig_b_1', 'sig_b_2', 'plot_charge', 'plot_rho', 'autocomp', 'dirichlet', 'eV'],
            'optional': ['shape'],
            'optional_attribs':
            ['b_field', 'zsigma', 'sig_b_1', 'sig_b_2', 'plot_charge', 'plot_rho', 'autocomp', 'dirichlet', 'eV'],
            'order': ['shape'],
            'several': ['shape'],
            'simple': ['shape'],
            'text': ['shape']
        },
        '/fleurInput/calculationSetup/geometryOptimization': {
            'attribs': ['l_f', 'forcealpha', 'epsdisp', 'epsforce', 'forcemix', 'qfix', 'force_converged'],
            'optional': [],
            'optional_attribs': ['forcealpha', 'epsdisp', 'epsforce', 'forcemix', 'qfix', 'force_converged'],
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
            'attribs': ['jspins', 'l_noco', 'l_J', 'swsp', 'lflip', 'fixed_moment'],
            'optional': [],
            'optional_attribs': ['l_noco', 'l_J', 'swsp', 'lflip', 'fixed_moment'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/nocoParams': {
            'attribs': ['l_ss', 'l_mperp', 'l_constr', 'l_disp', 'sso_opt', 'mix_b', 'thetaJ', 'nsh', 'l_mtNocoPot'],
            'optional': ['qsc'],
            'optional_attribs': ['l_disp', 'thetaJ', 'nsh', 'l_mtNocoPot'],
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
        '/fleurInput/calculationSetup/rdmft': {
            'attribs': ['l_rdmft', 'occEps', 'statesBelow', 'statesAbove', 'functional'],
            'optional': [],
            'optional_attribs': ['occEps'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/scfLoop': {
            'attribs':
            ['itmax', 'maxIterBroyd', 'imix', 'alpha', 'precondParam', 'spinf', 'minDistance', 'maxTimeToStartIter'],
            'optional': [],
            'optional_attribs': ['maxIterBroyd', 'precondParam', 'spinf', 'minDistance', 'maxTimeToStartIter'],
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
            'attribs': [
                'eKin', 'atomType', 'lmax', 'edgeType', 'eMin', 'eMax', 'numPoints', 'verbose', 'nqphi', 'nqr',
                'alpha_Ex', 'beta_Ex', 'I_initial'
            ],
            'optional': [],
            'optional_attribs': ['verbose', 'nqphi', 'nqr', 'alpha_Ex', 'beta_Ex', 'I_initial'],
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
            'attribs': ['unfoldBand', 'supercellX', 'supercellY', 'supercellZ'],
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
        '/fleurInput/relaxation': {
            'attribs': [],
            'optional': ['displacements', 'relaxation-history'],
            'optional_attribs': [],
            'order': ['displacements', 'relaxation-history'],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/relaxation/displacements': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['displace'],
            'several': ['displace'],
            'simple': ['displace'],
            'text': ['displace']
        },
        '/fleurInput/relaxation/relaxation-history': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['step'],
            'several': ['step'],
            'simple': [],
            'text': []
        },
        '/fleurInput/relaxation/relaxation-history/step': {
            'attribs': ['energy'],
            'optional': [],
            'optional_attribs': [],
            'order': ['posforce'],
            'several': ['posforce'],
            'simple': ['posforce'],
            'text': ['posforce']
        },
        '/fleurInput/xcFunctional': {
            'attribs': ['name', 'relativisticCorrections'],
            'optional': ['LibXCID', 'LibXCName', 'xcParams', 'ggaPrinting'],
            'optional_attribs': ['relativisticCorrections'],
            'order': ['LibXCID', 'LibXCName', 'xcParams', 'ggaPrinting'],
            'several': [],
            'simple': ['LibXCID', 'LibXCName', 'xcParams', 'ggaPrinting'],
            'text': []
        },
        '/fleurInput/xcFunctional/LibXCID': {
            'attribs': ['exchange', 'correlation', 'etot_exchange', 'etot_correlation'],
            'optional': [],
            'optional_attribs': ['etot_exchange', 'etot_correlation'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/xcFunctional/LibXCName': {
            'attribs': ['exchange', 'correlation', 'etot_exchange', 'etot_correlation'],
            'optional': [],
            'optional_attribs': ['etot_exchange', 'etot_correlation'],
            'order': [],
            'several': [],
            'simple': [],
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
        'dmi':
        '/fleurInput/forceTheorem/DMI',
        'jij':
        '/fleurInput/forceTheorem/Jij',
        'libxcid':
        '/fleurInput/xcFunctional/LibXCID',
        'libxcname':
        '/fleurInput/xcFunctional/LibXCName',
        'mae':
        '/fleurInput/forceTheorem/MAE',
        'a1': ['/fleurInput/cell/bulkLattice/a1', '/fleurInput/cell/filmLattice/a1'],
        'a2': ['/fleurInput/cell/bulkLattice/a2', '/fleurInput/cell/filmLattice/a2'],
        'abspos':
        '/fleurInput/atomGroups/atomGroup/absPos',
        'altkpointset':
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet',
        'atomgroup':
        '/fleurInput/atomGroups/atomGroup',
        'atomgroups':
        '/fleurInput/atomGroups',
        'atomspecies':
        '/fleurInput/atomSpecies',
        'atomiccutoffs':
        ['/fleurInput/atomGroups/atomGroup/atomicCutoffs', '/fleurInput/atomSpecies/species/atomicCutoffs'],
        'bandselection':
        '/fleurInput/output/wannier/bandSelection',
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
        'corespectrum':
        '/fleurInput/output/coreSpectrum',
        'cutoffs':
        '/fleurInput/calculationSetup/cutoffs',
        'densityofstates':
        '/fleurInput/output/densityOfStates',
        'displace':
        '/fleurInput/relaxation/displacements/displace',
        'displacements':
        '/fleurInput/relaxation/displacements',
        'edgeindices':
        '/fleurInput/output/coreSpectrum/edgeIndices',
        'electronconfig':
        '/fleurInput/atomSpecies/species/electronConfig',
        'energyparameterlimits':
        '/fleurInput/calculationSetup/energyParameterLimits',
        'energyparameters':
        ['/fleurInput/atomGroups/atomGroup/energyParameters', '/fleurInput/atomSpecies/species/energyParameters'],
        'expertmodes':
        '/fleurInput/calculationSetup/expertModes',
        'fields':
        '/fleurInput/calculationSetup/fields',
        'filmlattice':
        '/fleurInput/cell/filmLattice',
        'filmpos':
        '/fleurInput/atomGroups/atomGroup/filmPos',
        'fleurinput':
        '/fleurInput',
        'force': ['/fleurInput/atomGroups/atomGroup/force', '/fleurInput/atomSpecies/species/force'],
        'forcetheorem':
        '/fleurInput/forceTheorem',
        'geometryoptimization':
        '/fleurInput/calculationSetup/geometryOptimization',
        'ggaprinting':
        '/fleurInput/xcFunctional/ggaPrinting',
        'joblist':
        '/fleurInput/output/wannier/jobList',
        'kpoint': [
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList/kPoint',
            '/fleurInput/calculationSetup/bzIntegration/kPointList/kPoint'
        ],
        'kpointcount': [
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount',
            '/fleurInput/calculationSetup/bzIntegration/kPointCount'
        ],
        'kpointdensity': [
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointDensity',
            '/fleurInput/calculationSetup/bzIntegration/kPointDensity'
        ],
        'kpointlist': [
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointList',
            '/fleurInput/calculationSetup/bzIntegration/kPointList'
        ],
        'kpointlistfile':
        '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointListFile',
        'kpointmesh': [
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointMesh',
            '/fleurInput/calculationSetup/bzIntegration/kPointMesh'
        ],
        'ldau': [
            '/fleurInput/atomGroups/atomGroup/ldaU', '/fleurInput/atomSpecies/species/ldaU',
            '/fleurInput/calculationSetup/ldaU'
        ],
        'lo': ['/fleurInput/atomGroups/atomGroup/lo', '/fleurInput/atomSpecies/species/lo'],
        'magneticcirculardichroism':
        '/fleurInput/output/magneticCircularDichroism',
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
        'posforce':
        '/fleurInput/relaxation/relaxation-history/step/posforce',
        'prodbasis': ['/fleurInput/atomSpecies/species/prodBasis', '/fleurInput/calculationSetup/prodBasis'],
        'q': [
            '/fleurInput/forceTheorem/DMI/qVectors/q', '/fleurInput/forceTheorem/Jij/qVectors/q',
            '/fleurInput/forceTheorem/spinSpiralDispersion/q'
        ],
        'qvectors': ['/fleurInput/forceTheorem/DMI/qVectors', '/fleurInput/forceTheorem/Jij/qVectors'],
        'qsc':
        '/fleurInput/calculationSetup/nocoParams/qsc',
        'qss':
        '/fleurInput/calculationSetup/nocoParams/qss',
        'rdmft':
        '/fleurInput/calculationSetup/rdmft',
        'relpos':
        '/fleurInput/atomGroups/atomGroup/relPos',
        'relaxation':
        '/fleurInput/relaxation',
        'relaxation-history':
        '/fleurInput/relaxation/relaxation-history',
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
        'shape':
        '/fleurInput/calculationSetup/fields/shape',
        'soc':
        '/fleurInput/calculationSetup/soc',
        'special':
        '/fleurInput/atomSpecies/species/special',
        'specialoutput':
        '/fleurInput/output/specialOutput',
        'specialpoint': [
            '/fleurInput/calculationSetup/bzIntegration/altKPointSet/kPointCount/specialPoint',
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/specialPoint'
        ],
        'species':
        '/fleurInput/atomSpecies/species',
        'spinspiraldispersion':
        '/fleurInput/forceTheorem/spinSpiralDispersion',
        'spinspiralqpointmesh':
        '/fleurInput/calculationSetup/spinSpiralQPointMesh',
        'stateoccupation':
        '/fleurInput/atomSpecies/species/electronConfig/stateOccupation',
        'step':
        '/fleurInput/relaxation/relaxation-history/step',
        'symop':
        '/fleurInput/cell/symmetryOperations/symOp',
        'symmetry':
        '/fleurInput/cell/symmetry',
        'symmetryfile':
        '/fleurInput/cell/symmetryFile',
        'symmetryoperations':
        '/fleurInput/cell/symmetryOperations',
        'unfoldingband':
        '/fleurInput/output/unfoldingBand',
        'vacuumdos':
        '/fleurInput/output/vacuumDOS',
        'vacuumenergyparameters':
        '/fleurInput/cell/filmLattice/vacuumEnergyParameters',
        'valenceconfig':
        '/fleurInput/atomSpecies/species/electronConfig/valenceConfig',
        'wannier':
        '/fleurInput/output/wannier',
        'xcfunctional':
        '/fleurInput/xcFunctional',
        'xcparams':
        '/fleurInput/xcFunctional/xcParams'
    }),
    'unique_attribs':
    CaseInsensitiveDict({
        'gmax': '/fleurInput/calculationSetup/cutoffs/@Gmax',
        'gmaxxc': '/fleurInput/calculationSetup/cutoffs/@GmaxXC',
        'i_initial': '/fleurInput/output/coreSpectrum/@I_initial',
        'kmax': '/fleurInput/calculationSetup/cutoffs/@Kmax',
        'mm': '/fleurInput/calculationSetup/oneDParams/@MM',
        'alpha': '/fleurInput/calculationSetup/scfLoop/@alpha',
        'alpha_ex': '/fleurInput/output/coreSpectrum/@alpha_Ex',
        'atomlist': '/fleurInput/output/wannier/@atomList',
        'atomtype': '/fleurInput/output/coreSpectrum/@atomType',
        'autocomp': '/fleurInput/calculationSetup/fields/@autocomp',
        'b_field': '/fleurInput/calculationSetup/fields/@b_field',
        'band': '/fleurInput/output/@band',
        'bands': '/fleurInput/calculationSetup/prodBasis/@bands',
        'beta_ex': '/fleurInput/output/coreSpectrum/@beta_Ex',
        'bmt': '/fleurInput/output/specialOutput/@bmt',
        'bscomf': '/fleurInput/output/wannier/@bsComf',
        'cdinf': '/fleurInput/output/checks/@cdinf',
        'chi': '/fleurInput/calculationSetup/oneDParams/@chi',
        'chng': '/fleurInput/xcFunctional/xcParams/@chng',
        'corespec': '/fleurInput/output/@coreSpec',
        'coretail_lmax': '/fleurInput/calculationSetup/coreElectrons/@coretail_lmax',
        'ctail': '/fleurInput/calculationSetup/coreElectrons/@ctail',
        'd1': '/fleurInput/calculationSetup/oneDParams/@d1',
        'dtilda': '/fleurInput/cell/filmLattice/@dTilda',
        'dvac': '/fleurInput/cell/filmLattice/@dVac',
        'denx': '/fleurInput/calculationSetup/bzIntegration/kPointDensity/@denX',
        'deny': '/fleurInput/calculationSetup/bzIntegration/kPointDensity/@denY',
        'denz': '/fleurInput/calculationSetup/bzIntegration/kPointDensity/@denZ',
        'dirichlet': '/fleurInput/calculationSetup/fields/@dirichlet',
        'disp': '/fleurInput/output/checks/@disp',
        'dos': '/fleurInput/output/@dos',
        'ekin': '/fleurInput/output/coreSpectrum/@eKin',
        'emax': '/fleurInput/output/coreSpectrum/@eMax',
        'emin': '/fleurInput/output/coreSpectrum/@eMin',
        'ev': '/fleurInput/calculationSetup/fields/@eV',
        'edgetype': '/fleurInput/output/coreSpectrum/@edgeType',
        'eig66': '/fleurInput/calculationSetup/expertModes/@eig66',
        'ellow': '/fleurInput/calculationSetup/energyParameterLimits/@ellow',
        'elup': '/fleurInput/calculationSetup/energyParameterLimits/@elup',
        'energylo': '/fleurInput/output/magneticCircularDichroism/@energyLo',
        'energyup': '/fleurInput/output/magneticCircularDichroism/@energyUp',
        'eonly': '/fleurInput/output/specialOutput/@eonly',
        'epsdisp': '/fleurInput/calculationSetup/geometryOptimization/@epsdisp',
        'epsforce': '/fleurInput/calculationSetup/geometryOptimization/@epsforce',
        'ewaldlambda': '/fleurInput/calculationSetup/prodBasis/@ewaldlambda',
        'fermismearingenergy': '/fleurInput/calculationSetup/bzIntegration/@fermiSmearingEnergy',
        'fermismearingtemp': '/fleurInput/calculationSetup/bzIntegration/@fermiSmearingTemp',
        'filename': '/fleurInput/cell/symmetryFile/@filename',
        'fixed_moment': '/fleurInput/calculationSetup/magnetism/@fixed_moment',
        'fleurinputversion': '/fleurInput/@fleurInputVersion',
        'force_converged': '/fleurInput/calculationSetup/geometryOptimization/@force_converged',
        'forcealpha': '/fleurInput/calculationSetup/geometryOptimization/@forcealpha',
        'forcemix': '/fleurInput/calculationSetup/geometryOptimization/@forcemix',
        'form66': '/fleurInput/output/specialOutput/@form66',
        'frcor': '/fleurInput/calculationSetup/coreElectrons/@frcor',
        'functional': '/fleurInput/calculationSetup/rdmft/@functional',
        'gcutm': '/fleurInput/calculationSetup/prodBasis/@gcutm',
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
        'l_linmix': '/fleurInput/calculationSetup/ldaU/@l_linMix',
        'l_mperp': '/fleurInput/calculationSetup/nocoParams/@l_mperp',
        'l_mtnocopot': '/fleurInput/calculationSetup/nocoParams/@l_mtNocoPot',
        'l_noco': '/fleurInput/calculationSetup/magnetism/@l_noco',
        'l_rdmft': '/fleurInput/calculationSetup/rdmft/@l_rdmft',
        'l_soc': '/fleurInput/calculationSetup/soc/@l_soc',
        'l_ss': '/fleurInput/calculationSetup/nocoParams/@l_ss',
        'layers': '/fleurInput/output/vacuumDOS/@layers',
        'lexp': '/fleurInput/calculationSetup/prodBasis/@lexp',
        'lflip': '/fleurInput/calculationSetup/magnetism/@lflip',
        'lmax': '/fleurInput/output/coreSpectrum/@lmax',
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
        'maxspindown': '/fleurInput/output/wannier/bandSelection/@maxSpinDown',
        'maxspinup': '/fleurInput/output/wannier/bandSelection/@maxSpinUp',
        'maxtimetostartiter': '/fleurInput/calculationSetup/scfLoop/@maxTimeToStartIter',
        'mcd': '/fleurInput/output/@mcd',
        'mindistance': '/fleurInput/calculationSetup/scfLoop/@minDistance',
        'mineigenval': '/fleurInput/output/chargeDensitySlicing/@minEigenval',
        'minenergy': '/fleurInput/output/densityOfStates/@minEnergy',
        'minspindown': '/fleurInput/output/wannier/bandSelection/@minSpinDown',
        'minspinup': '/fleurInput/output/wannier/bandSelection/@minSpinUp',
        'mixparam': '/fleurInput/calculationSetup/ldaU/@mixParam',
        'mix_b': '/fleurInput/calculationSetup/nocoParams/@mix_b',
        'mode': '/fleurInput/calculationSetup/bzIntegration/@mode',
        'ms': '/fleurInput/output/wannier/@ms',
        'name': '/fleurInput/xcFunctional/@name',
        'ndir': '/fleurInput/output/densityOfStates/@ndir',
        'ndvgrd': '/fleurInput/xcFunctional/xcParams/@ndvgrd',
        'nnne': '/fleurInput/output/chargeDensitySlicing/@nnne',
        'nqphi': '/fleurInput/output/coreSpectrum/@nqphi',
        'nqr': '/fleurInput/output/coreSpectrum/@nqr',
        'nsh': '/fleurInput/calculationSetup/nocoParams/@nsh',
        'nstars': '/fleurInput/output/vacuumDOS/@nstars',
        'nstm': '/fleurInput/output/vacuumDOS/@nstm',
        'numpoints': '/fleurInput/output/coreSpectrum/@numPoints',
        'numbands': '/fleurInput/calculationSetup/cutoffs/@numbands',
        'numkpt': '/fleurInput/output/chargeDensitySlicing/@numkpt',
        'nx': '/fleurInput/calculationSetup/bzIntegration/kPointMesh/@nx',
        'ny': '/fleurInput/calculationSetup/bzIntegration/kPointMesh/@ny',
        'nz': '/fleurInput/calculationSetup/bzIntegration/kPointMesh/@nz',
        'occeps': '/fleurInput/calculationSetup/rdmft/@occEps',
        'off': '/fleurInput/calculationSetup/soc/@off',
        'pallst': '/fleurInput/output/chargeDensitySlicing/@pallst',
        'plot_charge': '/fleurInput/calculationSetup/fields/@plot_charge',
        'plot_rho': '/fleurInput/calculationSetup/fields/@plot_rho',
        'plplot': '/fleurInput/output/plotting/@plplot',
        'posscale': '/fleurInput/calculationSetup/bzIntegration/kPointList/@posScale',
        'pot8': '/fleurInput/calculationSetup/expertModes/@pot8',
        'precondparam': '/fleurInput/calculationSetup/scfLoop/@precondParam',
        'qfix': '/fleurInput/calculationSetup/geometryOptimization/@qfix',
        'qx': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qx',
        'qy': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qy',
        'qz': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qz',
        'relativisticcorrections': '/fleurInput/xcFunctional/@relativisticCorrections',
        'rot': '/fleurInput/calculationSetup/oneDParams/@rot',
        'score': '/fleurInput/output/plotting/@score',
        'secvar': '/fleurInput/calculationSetup/expertModes/@secvar',
        'sgwf': '/fleurInput/output/wannier/@sgwf',
        'sig_b_1': '/fleurInput/calculationSetup/fields/@sig_b_1',
        'sig_b_2': '/fleurInput/calculationSetup/fields/@sig_b_2',
        'sigma': '/fleurInput/output/densityOfStates/@sigma',
        'slice': '/fleurInput/output/@slice',
        'soc66': '/fleurInput/calculationSetup/soc/@soc66',
        'socgwf': '/fleurInput/output/wannier/@socgwf',
        'spav': '/fleurInput/calculationSetup/soc/@spav',
        'spgrp': '/fleurInput/cell/symmetry/@spgrp',
        'sso_opt': '/fleurInput/calculationSetup/nocoParams/@sso_opt',
        'star': '/fleurInput/output/vacuumDOS/@star',
        'statesabove': '/fleurInput/calculationSetup/rdmft/@statesAbove',
        'statesbelow': '/fleurInput/calculationSetup/rdmft/@statesBelow',
        'supercellx': '/fleurInput/output/unfoldingBand/@supercellX',
        'supercelly': '/fleurInput/output/unfoldingBand/@supercellY',
        'supercellz': '/fleurInput/output/unfoldingBand/@supercellZ',
        'swsp': '/fleurInput/calculationSetup/magnetism/@swsp',
        'tolerance': '/fleurInput/calculationSetup/prodBasis/@tolerance',
        'tworkf': '/fleurInput/output/vacuumDOS/@tworkf',
        'unfoldband': '/fleurInput/output/unfoldingBand/@unfoldBand',
        'vm': '/fleurInput/calculationSetup/oneDParams/@vM',
        'vacdos': '/fleurInput/output/@vacdos',
        'valenceelectrons': '/fleurInput/calculationSetup/bzIntegration/@valenceElectrons',
        'vchk': '/fleurInput/output/checks/@vchk',
        'verbose': '/fleurInput/output/coreSpectrum/@verbose',
        'wannier': '/fleurInput/output/@wannier',
        'weightscale': '/fleurInput/calculationSetup/bzIntegration/kPointList/@weightScale',
        'zrfs': '/fleurInput/cell/symmetry/@zrfs',
        'zrfs1': '/fleurInput/calculationSetup/oneDParams/@zrfs1',
        'zsigma': '/fleurInput/calculationSetup/fields/@zsigma',
        'c': '/fleurInput/cell/bulkLattice/c',
        'comment': '/fleurInput/comment',
        'edgeindices': '/fleurInput/output/coreSpectrum/edgeIndices',
        'joblist': '/fleurInput/output/wannier/jobList',
        'qsc': '/fleurInput/calculationSetup/nocoParams/qsc',
        'qss': '/fleurInput/calculationSetup/nocoParams/qss'
    }),
    'unique_path_attribs':
    CaseInsensitiveDict({
        'correlation':
        ['/fleurInput/xcFunctional/LibXCID/@correlation', '/fleurInput/xcFunctional/LibXCName/@correlation'],
        'count': [
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/@count',
            '/fleurInput/calculationSetup/bzIntegration/kPointList/@count'
        ],
        'etot_correlation':
        ['/fleurInput/xcFunctional/LibXCID/@etot_correlation', '/fleurInput/xcFunctional/LibXCName/@etot_correlation'],
        'etot_exchange':
        ['/fleurInput/xcFunctional/LibXCID/@etot_exchange', '/fleurInput/xcFunctional/LibXCName/@etot_exchange'],
        'exchange': ['/fleurInput/xcFunctional/LibXCID/@exchange', '/fleurInput/xcFunctional/LibXCName/@exchange'],
        'gamma': [
            '/fleurInput/calculationSetup/bzIntegration/kPointCount/@gamma',
            '/fleurInput/calculationSetup/bzIntegration/kPointDensity/@gamma',
            '/fleurInput/calculationSetup/bzIntegration/kPointMesh/@gamma'
        ],
        'latnam': ['/fleurInput/cell/bulkLattice/@latnam', '/fleurInput/cell/filmLattice/@latnam'],
        'phi': [
            '/fleurInput/calculationSetup/soc/@phi', '/fleurInput/forceTheorem/DMI/@phi',
            '/fleurInput/forceTheorem/MAE/@phi'
        ],
        'scale': [
            '/fleurInput/cell/bulkLattice/@scale', '/fleurInput/cell/bulkLattice/a1/@scale',
            '/fleurInput/cell/bulkLattice/a2/@scale', '/fleurInput/cell/bulkLattice/c/@scale',
            '/fleurInput/cell/filmLattice/@scale', '/fleurInput/cell/filmLattice/a1/@scale',
            '/fleurInput/cell/filmLattice/a2/@scale'
        ],
        'spinf': ['/fleurInput/calculationSetup/ldaU/@spinf', '/fleurInput/calculationSetup/scfLoop/@spinf'],
        'theta': [
            '/fleurInput/calculationSetup/soc/@theta', '/fleurInput/forceTheorem/DMI/@theta',
            '/fleurInput/forceTheorem/MAE/@theta'
        ],
        'thetaj': ['/fleurInput/calculationSetup/nocoParams/@thetaJ', '/fleurInput/forceTheorem/Jij/@thetaj'],
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
