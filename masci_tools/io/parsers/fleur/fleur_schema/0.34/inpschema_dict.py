# -*- coding: utf-8 -*-
"""
This file contains information parsed from the FleurInputSchema.xsd
for version 0.34

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
__inp_version__ = '0.34'
schema_dict = {
    '_basic_types': {
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
        'fleurinputversion': ['string'],
        'name': ['string'],
        'value': ['float_expression', 'string'],
        'b_field': ['float_expression'],
        'zsigma': ['float_expression'],
        'sig_b_1': ['float_expression'],
        'sig_b_2': ['float_expression'],
        'plot_charge': ['switch'],
        'plot_rho': ['switch'],
        'autocomp': ['switch'],
        'dirichlet': ['switch'],
        'ev': ['switch'],
        'l_mtnocopot': ['switch'],
        'l_mperp': ['switch'],
        'l_constrained': ['switch'],
        'l_relaxsqa': ['switch'],
        'mag_mixing_scheme': ['int'],
        'mix_relaxweightoffd': ['float_expression'],
        'mix_constr': ['float_expression'],
        'l_sourcefree': ['switch'],
        'l_scalemag': ['switch'],
        'mag_scale': ['float_expression'],
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
        'l_core_confpot': ['switch'],
        'jspins': ['int'],
        'l_noco': ['switch'],
        'l_ss': ['switch'],
        'l_j': ['switch'],
        'swsp': ['switch'],
        'lflip': ['switch'],
        'l_onlymtstden': ['switch'],
        'fixed_moment': ['float_expression'],
        'scale': ['float_expression'],
        'dvac': ['float_expression'],
        'dtilda': ['float_expression'],
        'vacuum': ['int'],
        'spinup': ['float_expression'],
        'spindown': ['float_expression'],
        's': ['switch', 'int'],
        'p': ['switch', 'int'],
        'd': ['switch', 'int'],
        'f': ['switch', 'int'],
        'relativisticcorrections': ['switch'],
        'gcutm': ['float'],
        'bands': ['int'],
        'tolerance': ['float'],
        'lexp': ['int'],
        'ewaldlambda': ['int'],
        'fftcut': ['float'],
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
        'b_field_mt': ['float_expression'],
        'vca_charge': ['float_expression'],
        'element': ['string'],
        'atomicnumber': ['int'],
        'species': ['string'],
        'magfield': ['float'],
        'vcaaddcharge': ['float'],
        'label': ['string'],
        'wannier': ['switch'],
        'banddos': ['switch'],
        'alpha': ['float_expression', 'float'],
        'beta': ['float_expression', 'float'],
        'gamma': ['float_expression'],
        'l_magn': ['switch'],
        'm': ['float_expression', 'int'],
        'b_cons_x': ['float_expression'],
        'b_cons_y': ['float_expression'],
        'magmom': ['float_expression'],
        'flipspinphi': ['float_expression'],
        'flipspintheta': ['float_expression'],
        'flipspinscale': ['switch'],
        'radius': ['float_expression'],
        'gridpoints': ['int'],
        'logincrement': ['float_expression'],
        'lmax': ['int'],
        'lnonsphr': ['int'],
        'lmaxapw': ['int'],
        'l': ['int'],
        'u': ['float_expression'],
        'j': ['float_expression'],
        'phi': ['float_expression'],
        'theta': ['float_expression'],
        'l_amf': ['switch'],
        'init_occ': ['float', 'string'],
        'kkintgrcutoff': ['float', 'string'],
        'init_mom': ['float', 'string'],
        'key': ['string'],
        'l_sphavg': ['switch'],
        'nshells': ['int'],
        'calculate': ['switch'],
        'relaxxyz': ['string'],
        'type': ['string'],
        'n': ['int'],
        'ederiv': ['int'],
        'kmax': ['float_expression'],
        'gmax': ['float_expression'],
        'gmaxxc': ['float_expression'],
        'numbands': ['int', 'string'],
        'valenceelectrons': ['float_expression'],
        'mode': ['string'],
        'fermismearingenergy': ['float_expression'],
        'fermismearingtemp': ['float_expression'],
        'l_bloechl': ['switch'],
        'l_soc': ['switch'],
        'spav': ['switch'],
        'off': ['switch'],
        'soc66': ['switch'],
        'itmax': ['int'],
        'maxiterbroyd': ['int'],
        'imix': ['string'],
        'precondparam': ['float_expression'],
        'spinf': ['float_expression', 'float'],
        'mindistance': ['float_expression'],
        'maxtimetostartiter': ['float_expression'],
        'vacdos': ['switch'],
        'integ': ['switch'],
        'star': ['switch'],
        'nstars': ['int'],
        'locx1': ['float_expression'],
        'locy1': ['float_expression'],
        'locx2': ['float_expression'],
        'locy2': ['float_expression'],
        'nstm': ['int'],
        'tworkf': ['float_expression'],
        'iplot': ['int'],
        'polar': ['switch'],
        'format': ['int'],
        'cartesian': ['switch'],
        'twod': ['switch'],
        'grid': ['string'],
        'vec1': ['string'],
        'vec2': ['string'],
        'vec3': ['string'],
        'zero': ['string'],
        'file': ['string'],
        'onlymt': ['switch'],
        'typemt': ['int'],
        'vecfield': ['switch'],
        'numkpt': ['int'],
        'mineigenval': ['float_expression'],
        'maxeigenval': ['float_expression'],
        'nnne': ['int'],
        'pallst': ['switch'],
        'l_f': ['switch'],
        'f_level': ['int'],
        'forcealpha': ['float_expression'],
        'epsdisp': ['float_expression'],
        'epsforce': ['float_expression'],
        'forcemix': ['string'],
        'qfix': ['int'],
        'force_converged': ['float_expression'],
        'l_linmix': ['switch'],
        'mixparam': ['float'],
        'l_adjenpara': ['switch'],
        'itmaxhubbard1': ['int'],
        'minoccdistance': ['float'],
        'minmatdistance': ['float'],
        'n_occpm': ['int'],
        'dftspinpol': ['switch'],
        'fullmatch': ['switch'],
        'l_nonsphdc': ['switch'],
        'l_correctetot': ['switch'],
        'chargedensity': ['switch'],
        'potential': ['switch'],
        'remove4f': ['switch'],
        'l_resolvent': ['switch'],
        'mincalcdistance': ['float'],
        'outputsphavg': ['switch'],
        'intfullradial': ['switch'],
        'ne': ['int'],
        'ellow': ['float'],
        'elup': ['float'],
        'n1': ['int'],
        'n2': ['int'],
        'n3': ['int'],
        'nmatsub': ['int'],
        'sigma': ['float', 'float_expression'],
        'eb': ['float'],
        'et': ['float'],
        'analytical_cont': ['switch'],
        'l_fermi': ['switch'],
        'l_rdmft': ['switch'],
        'occeps': ['float'],
        'statesbelow': ['int'],
        'statesabove': ['int'],
        'functional': ['string'],
        'all_atoms': ['switch'],
        'orbcomp': ['switch'],
        'jdos': ['switch'],
        'minenergy': ['float_expression'],
        'maxenergy': ['float_expression'],
        'numberpoints': ['int'],
        'count': ['int'],
        'nx': ['int'],
        'ny': ['int'],
        'nz': ['int'],
        'nkq_pairs': ['int'],
        'listname': ['string'],
        'purpose': ['string'],
        'weight': ['float_expression'],
        'qx': ['int'],
        'qy': ['int'],
        'qz': ['int'],
        'gw': ['int'],
        'pot8': ['switch'],
        'eig66': ['switch'],
        'lpr': ['int'],
        'isec1': ['int'],
        'secvar': ['switch'],
        'warp_factor': ['float_expression'],
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
        'mcd': ['switch'],
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
        'energy': ['float_expression'],
        'thetaj': ['float_expression'],
        'unfoldband': ['switch'],
        'supercellx': ['int'],
        'supercelly': ['int'],
        'supercellz': ['int'],
        'l_potout': ['switch'],
        'l_eigout': ['switch'],
        'dos': ['switch'],
        'band': ['switch'],
        'slice': ['switch'],
        'corespec': ['switch'],
        'state': ['string']
    }),
    'inp_version':
    '0.34',
    'omitt_contained_tags': [
        'constants', 'atomSpecies', 'atomGroups', 'symmetryOperations', 'kPointLists', 'displacements',
        'relaxation-history', 'spinSpiralDispersion', 'qVectors'
    ],
    'other_attribs':
    CaseInsensitiveDict({
        'j': [
            '/fleurInput/atomGroups/atomGroup/ldaHIA/@J', '/fleurInput/atomGroups/atomGroup/ldaHIA/exc/@J',
            '/fleurInput/atomGroups/atomGroup/ldaU/@J', '/fleurInput/atomSpecies/species/ldaHIA/@J',
            '/fleurInput/atomSpecies/species/ldaHIA/exc/@J', '/fleurInput/atomSpecies/species/ldaU/@J'
        ],
        'm': [
            '/fleurInput/atomGroups/atomGroup/ldaHIA/cFCoeff/@m', '/fleurInput/atomGroups/atomGroup/nocoParams/@M',
            '/fleurInput/atomSpecies/species/ldaHIA/cFCoeff/@m', '/fleurInput/atomSpecies/species/nocoParams/@M'
        ],
        'twod': ['/fleurInput/output/plotting/plot/@TwoD'],
        'u': [
            '/fleurInput/atomGroups/atomGroup/ldaHIA/@U', '/fleurInput/atomGroups/atomGroup/ldaU/@U',
            '/fleurInput/atomSpecies/species/ldaHIA/@U', '/fleurInput/atomSpecies/species/ldaU/@U'
        ],
        'alpha': [
            '/fleurInput/atomGroups/atomGroup/absPos/@alpha', '/fleurInput/atomGroups/atomGroup/filmPos/@alpha',
            '/fleurInput/atomGroups/atomGroup/nocoParams/@alpha', '/fleurInput/atomGroups/atomGroup/relPos/@alpha',
            '/fleurInput/atomSpecies/species/nocoParams/@alpha',
            '/fleurInput/calculationSetup/greensFunction/contourSemicircle/@alpha'
        ],
        'analytical_cont': ['/fleurInput/calculationSetup/greensFunction/contourDOS/@analytical_cont'],
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
        'banddos': [
            '/fleurInput/atomGroups/atomGroup/absPos/@banddos', '/fleurInput/atomGroups/atomGroup/filmPos/@banddos',
            '/fleurInput/atomGroups/atomGroup/relPos/@banddos'
        ],
        'beta': [
            '/fleurInput/atomGroups/atomGroup/absPos/@beta', '/fleurInput/atomGroups/atomGroup/filmPos/@beta',
            '/fleurInput/atomGroups/atomGroup/nocoParams/@beta', '/fleurInput/atomGroups/atomGroup/relPos/@beta',
            '/fleurInput/atomSpecies/species/nocoParams/@beta'
        ],
        'calculate':
        ['/fleurInput/atomGroups/atomGroup/force/@calculate', '/fleurInput/atomSpecies/species/force/@calculate'],
        'cartesian': ['/fleurInput/output/plotting/plot/@cartesian'],
        'chargedensity': ['/fleurInput/atomGroups/atomGroup/cFCoeffs/@chargeDensity'],
        'count': ['/fleurInput/cell/bzIntegration/kPointLists/kPointList/@count'],
        'd': [
            '/fleurInput/atomGroups/atomGroup/energyParameters/@d',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/diagElements/@d',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements/d',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements/d',
            '/fleurInput/atomSpecies/species/energyParameters/@d',
            '/fleurInput/atomSpecies/species/greensfCalculation/diagElements/@d',
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements/d',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/d'
        ],
        'ederiv': ['/fleurInput/atomGroups/atomGroup/lo/@eDeriv', '/fleurInput/atomSpecies/species/lo/@eDeriv'],
        'eb': [
            '/fleurInput/calculationSetup/greensFunction/contourDOS/@eb',
            '/fleurInput/calculationSetup/greensFunction/contourRectangle/@eb',
            '/fleurInput/calculationSetup/greensFunction/contourSemicircle/@eb'
        ],
        'element': ['/fleurInput/atomSpecies/species/@element'],
        'energy': ['/fleurInput/relaxation/relaxation-history/step/@energy'],
        'et': [
            '/fleurInput/calculationSetup/greensFunction/contourDOS/@et',
            '/fleurInput/calculationSetup/greensFunction/contourSemicircle/@et'
        ],
        'f': [
            '/fleurInput/atomGroups/atomGroup/energyParameters/@f',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/diagElements/@f',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements/f',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements/f',
            '/fleurInput/atomSpecies/species/energyParameters/@f',
            '/fleurInput/atomSpecies/species/greensfCalculation/diagElements/@f',
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements/f',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/f'
        ],
        'file': ['/fleurInput/output/plotting/plot/@file'],
        'flipspinphi': [
            '/fleurInput/atomGroups/atomGroup/modInitDen/@flipSpinPhi',
            '/fleurInput/atomSpecies/species/modInitDen/@flipSpinPhi'
        ],
        'flipspinscale': [
            '/fleurInput/atomGroups/atomGroup/modInitDen/@flipSpinScale',
            '/fleurInput/atomSpecies/species/modInitDen/@flipSpinScale'
        ],
        'flipspintheta': [
            '/fleurInput/atomGroups/atomGroup/modInitDen/@flipSpinTheta',
            '/fleurInput/atomSpecies/species/modInitDen/@flipSpinTheta'
        ],
        'gamma': [
            '/fleurInput/atomGroups/atomGroup/absPos/@gamma', '/fleurInput/atomGroups/atomGroup/filmPos/@gamma',
            '/fleurInput/atomGroups/atomGroup/relPos/@gamma'
        ],
        'grid': ['/fleurInput/output/plotting/plot/@grid'],
        'gridpoints': [
            '/fleurInput/atomGroups/atomGroup/mtSphere/@gridPoints',
            '/fleurInput/atomSpecies/species/mtSphere/@gridPoints'
        ],
        'init_mom': [
            '/fleurInput/atomGroups/atomGroup/ldaHIA/exc/@init_mom',
            '/fleurInput/atomSpecies/species/ldaHIA/exc/@init_mom'
        ],
        'init_occ':
        ['/fleurInput/atomGroups/atomGroup/ldaHIA/@init_occ', '/fleurInput/atomSpecies/species/ldaHIA/@init_occ'],
        'key':
        ['/fleurInput/atomGroups/atomGroup/ldaHIA/addArg/@key', '/fleurInput/atomSpecies/species/ldaHIA/addArg/@key'],
        'kkintgrcutoff': [
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/@kkintgrCutoff',
            '/fleurInput/atomGroups/atomGroup/ldaHIA/@kkintgrCutoff',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/@kkintgrCutoff',
            '/fleurInput/atomSpecies/species/greensfCalculation/@kkintgrCutoff',
            '/fleurInput/atomSpecies/species/ldaHIA/@kkintgrCutoff',
            '/fleurInput/atomSpecies/species/torgueCalculation/@kkintgrCutoff'
        ],
        'l': [
            '/fleurInput/atomGroups/atomGroup/ldaHIA/@l', '/fleurInput/atomGroups/atomGroup/ldaHIA/cFCoeff/@l',
            '/fleurInput/atomGroups/atomGroup/ldaHIA/exc/@l', '/fleurInput/atomGroups/atomGroup/ldaU/@l',
            '/fleurInput/atomGroups/atomGroup/lo/@l', '/fleurInput/atomSpecies/species/ldaHIA/@l',
            '/fleurInput/atomSpecies/species/ldaHIA/cFCoeff/@l', '/fleurInput/atomSpecies/species/ldaHIA/exc/@l',
            '/fleurInput/atomSpecies/species/ldaU/@l', '/fleurInput/atomSpecies/species/lo/@l'
        ],
        'l_amf': [
            '/fleurInput/atomGroups/atomGroup/ldaHIA/@l_amf', '/fleurInput/atomGroups/atomGroup/ldaU/@l_amf',
            '/fleurInput/atomSpecies/species/ldaHIA/@l_amf', '/fleurInput/atomSpecies/species/ldaU/@l_amf'
        ],
        'l_constrained': [
            '/fleurInput/atomGroups/atomGroup/nocoParams/@l_constrained',
            '/fleurInput/atomSpecies/species/nocoParams/@l_constrained'
        ],
        'l_fermi': ['/fleurInput/calculationSetup/greensFunction/contourDOS/@l_fermi'],
        'l_magn':
        ['/fleurInput/atomGroups/atomGroup/nocoParams/@l_magn', '/fleurInput/atomSpecies/species/nocoParams/@l_magn'],
        'l_mtnocopot': [
            '/fleurInput/atomGroups/atomGroup/nocoParams/@l_mtNocoPot',
            '/fleurInput/atomSpecies/species/nocoParams/@l_mtNocoPot'
        ],
        'l_relaxsqa': [
            '/fleurInput/atomGroups/atomGroup/nocoParams/@l_relaxSQA',
            '/fleurInput/atomSpecies/species/nocoParams/@l_relaxSQA'
        ],
        'l_sphavg': [
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/@l_sphavg',
            '/fleurInput/atomSpecies/species/greensfCalculation/@l_sphavg'
        ],
        'label': [
            '/fleurInput/atomGroups/atomGroup/absPos/@label', '/fleurInput/atomGroups/atomGroup/filmPos/@label',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/@label',
            '/fleurInput/atomGroups/atomGroup/ldaHIA/@label', '/fleurInput/atomGroups/atomGroup/relPos/@label',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/@label',
            '/fleurInput/atomSpecies/species/greensfCalculation/@label',
            '/fleurInput/atomSpecies/species/ldaHIA/@label', '/fleurInput/atomSpecies/species/torgueCalculation/@label',
            '/fleurInput/calculationSetup/greensFunction/contourDOS/@label',
            '/fleurInput/calculationSetup/greensFunction/contourRectangle/@label',
            '/fleurInput/calculationSetup/greensFunction/contourSemicircle/@label',
            '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint/@label'
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
        'magfield': ['/fleurInput/atomGroups/atomGroup/@magField'],
        'magmom':
        ['/fleurInput/atomGroups/atomGroup/modInitDen/@magMom', '/fleurInput/atomSpecies/species/modInitDen/@magMom'],
        'n': [
            '/fleurInput/atomGroups/atomGroup/lo/@n', '/fleurInput/atomSpecies/species/lo/@n',
            '/fleurInput/calculationSetup/greensFunction/contourDOS/@n',
            '/fleurInput/calculationSetup/greensFunction/contourSemicircle/@n'
        ],
        'n1': ['/fleurInput/calculationSetup/greensFunction/contourRectangle/@n1'],
        'n2': ['/fleurInput/calculationSetup/greensFunction/contourRectangle/@n2'],
        'n3': ['/fleurInput/calculationSetup/greensFunction/contourRectangle/@n3'],
        'name': [
            '/fleurInput/atomSpecies/species/@name', '/fleurInput/cell/bzIntegration/kPointLists/kPointList/@name',
            '/fleurInput/constants/constant/@name'
        ],
        'nkq_pairs': ['/fleurInput/cell/bzIntegration/kPointLists/kPointList/@nkq_pairs'],
        'nmatsub': ['/fleurInput/calculationSetup/greensFunction/contourRectangle/@nmatsub'],
        'nshells': [
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/@nshells',
            '/fleurInput/atomSpecies/species/greensfCalculation/@nshells'
        ],
        'nx': ['/fleurInput/cell/bzIntegration/kPointLists/kPointList/@nx'],
        'ny': ['/fleurInput/cell/bzIntegration/kPointLists/kPointList/@ny'],
        'nz': ['/fleurInput/cell/bzIntegration/kPointLists/kPointList/@nz'],
        'onlymt': ['/fleurInput/output/plotting/plot/@onlyMT'],
        'p': [
            '/fleurInput/atomGroups/atomGroup/energyParameters/@p',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/diagElements/@p',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements/p',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements/p',
            '/fleurInput/atomSpecies/species/energyParameters/@p',
            '/fleurInput/atomSpecies/species/greensfCalculation/diagElements/@p',
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements/p',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/p'
        ],
        'phi': [
            '/fleurInput/atomGroups/atomGroup/ldaHIA/@phi', '/fleurInput/atomGroups/atomGroup/ldaU/@phi',
            '/fleurInput/atomSpecies/species/ldaHIA/@phi', '/fleurInput/atomSpecies/species/ldaU/@phi'
        ],
        'potential': ['/fleurInput/atomGroups/atomGroup/cFCoeffs/@potential'],
        'radius':
        ['/fleurInput/atomGroups/atomGroup/mtSphere/@radius', '/fleurInput/atomSpecies/species/mtSphere/@radius'],
        'relaxxyz':
        ['/fleurInput/atomGroups/atomGroup/force/@relaxXYZ', '/fleurInput/atomSpecies/species/force/@relaxXYZ'],
        'remove4f': ['/fleurInput/atomGroups/atomGroup/cFCoeffs/@remove4f'],
        's': [
            '/fleurInput/atomGroups/atomGroup/energyParameters/@s',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/diagElements/@s',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements/s',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements/s',
            '/fleurInput/atomSpecies/species/energyParameters/@s',
            '/fleurInput/atomSpecies/species/greensfCalculation/diagElements/@s',
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements/s',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/s'
        ],
        'select': ['/fleurInput/atomSpecies/species/prodBasis/@select'],
        'sigma': [
            '/fleurInput/calculationSetup/greensFunction/contourDOS/@sigma',
            '/fleurInput/calculationSetup/greensFunction/contourRectangle/@sigma'
        ],
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
        'theta': [
            '/fleurInput/atomGroups/atomGroup/ldaHIA/@theta', '/fleurInput/atomGroups/atomGroup/ldaU/@theta',
            '/fleurInput/atomSpecies/species/ldaHIA/@theta', '/fleurInput/atomSpecies/species/ldaU/@theta'
        ],
        'type': [
            '/fleurInput/atomGroups/atomGroup/lo/@type', '/fleurInput/atomSpecies/species/lo/@type',
            '/fleurInput/cell/bzIntegration/kPointLists/kPointList/@type'
        ],
        'typemt': ['/fleurInput/output/plotting/plot/@typeMT'],
        'vacuum': ['/fleurInput/cell/filmLattice/vacuumEnergyParameters/@vacuum'],
        'value': [
            '/fleurInput/atomGroups/atomGroup/ldaHIA/addArg/@value',
            '/fleurInput/atomGroups/atomGroup/ldaHIA/cFCoeff/@value',
            '/fleurInput/atomSpecies/species/ldaHIA/addArg/@value',
            '/fleurInput/atomSpecies/species/ldaHIA/cFCoeff/@value', '/fleurInput/constants/constant/@value'
        ],
        'vcaaddcharge': ['/fleurInput/atomGroups/atomGroup/@vcaAddCharge'],
        'vca_charge': ['/fleurInput/atomSpecies/species/special/@vca_charge'],
        'vec1': ['/fleurInput/output/plotting/plot/@vec1'],
        'vec2': ['/fleurInput/output/plotting/plot/@vec2'],
        'vec3': ['/fleurInput/output/plotting/plot/@vec3'],
        'vecfield': ['/fleurInput/output/plotting/plot/@vecField'],
        'wannier': [
            '/fleurInput/atomGroups/atomGroup/absPos/@wannier', '/fleurInput/atomGroups/atomGroup/filmPos/@wannier',
            '/fleurInput/atomGroups/atomGroup/relPos/@wannier'
        ],
        'weight': ['/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint/@weight'],
        'zero': ['/fleurInput/output/plotting/plot/@zero'],
        'abspos': ['/fleurInput/atomGroups/atomGroup/absPos'],
        'coreconfig': ['/fleurInput/atomSpecies/species/electronConfig/coreConfig'],
        'displace': ['/fleurInput/relaxation/displacements/displace'],
        'filmpos': ['/fleurInput/atomGroups/atomGroup/filmPos'],
        'kpoint': ['/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint'],
        'layer': ['/fleurInput/output/vacuumDOS/layer'],
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
        'shape': [{
            'type': ['string'],
            'length': 1
        }],
        'qss': [{
            'type': ['float_expression'],
            'length': 3
        }],
        'qsc': [{
            'type': ['float_expression'],
            'length': 3
        }],
        'a1': [{
            'type': ['float_expression'],
            'length': 1
        }],
        'a2': [{
            'type': ['float_expression'],
            'length': 1
        }],
        'c': [{
            'type': ['float_expression'],
            'length': 1
        }],
        'row-1': [{
            'type': ['float_expression'],
            'length': 2
        }, {
            'type': ['float_expression'],
            'length': 3
        }, {
            'type': ['float'],
            'length': 4
        }],
        'row-2': [{
            'type': ['float_expression'],
            'length': 2
        }, {
            'type': ['float_expression'],
            'length': 3
        }, {
            'type': ['float'],
            'length': 4
        }],
        'row-3': [{
            'type': ['float_expression'],
            'length': 3
        }, {
            'type': ['float'],
            'length': 4
        }],
        's': [{
            'type': ['switch'],
            'length': 4
        }],
        'p': [{
            'type': ['switch'],
            'length': 4
        }],
        'd': [{
            'type': ['switch'],
            'length': 4
        }],
        'f': [{
            'type': ['switch'],
            'length': 4
        }],
        'relpos': [{
            'type': ['float_expression'],
            'length': 3
        }],
        'abspos': [{
            'type': ['float_expression'],
            'length': 3
        }],
        'filmpos': [{
            'type': ['float_expression'],
            'length': 3
        }],
        'orbcomprot': [{
            'type': ['float'],
            'length': 3
        }],
        'layer': [{
            'type': ['string'],
            'length': 1
        }],
        'kpoint': [{
            'type': ['float_expression'],
            'length': 3
        }],
        'edgeindices': [{
            'type': ['int'],
            'length': 'unbounded'
        }],
        'joblist': [{
            'type': ['string'],
            'length': 'unbounded'
        }],
        'displace': [{
            'type': ['float'],
            'length': 3
        }],
        'posforce': [{
            'type': ['string'],
            'length': 1
        }],
        'q': [{
            'type': ['string'],
            'length': 1
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
            'complex':
            CaseInsensitiveFrozenSet([
                'atomGroups', 'atomSpecies', 'calculationSetup', 'cell', 'constants', 'forceTheorem', 'output',
                'relaxation'
            ]),
            'optional':
            CaseInsensitiveFrozenSet(['comment', 'constants', 'forceTheorem', 'output', 'relaxation']),
            'optional_attribs':
            CaseInsensitiveDict({}),
            'order': [
                'comment', 'constants', 'calculationSetup', 'cell', 'atomSpecies', 'atomGroups', 'output',
                'forceTheorem', 'relaxation'
            ],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet(['comment']),
            'text':
            CaseInsensitiveFrozenSet(['comment'])
        },
        '/fleurInput/atomGroups': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet(['atomGroup']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['atomGroup'],
            'several': CaseInsensitiveFrozenSet(['atomGroup']),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup': {
            'attribs':
            CaseInsensitiveFrozenSet(['magField', 'species', 'vcaAddCharge']),
            'complex':
            CaseInsensitiveFrozenSet(['greensfCalculation', 'ldaHIA', 'torgueCalculation']),
            'optional':
            CaseInsensitiveFrozenSet([
                'atomicCutoffs', 'cFCoeffs', 'energyParameters', 'force', 'greensfCalculation', 'ldaHIA', 'ldaU', 'lo',
                'modInitDen', 'mtSphere', 'nocoParams', 'orbcomprot', 'torgueCalculation'
            ]),
            'optional_attribs':
            CaseInsensitiveDict({
                'magfield': None,
                'vcaaddcharge': None
            }),
            'order': [
                'relPos', 'absPos', 'filmPos', 'mtSphere', 'atomicCutoffs', 'energyParameters', 'force', 'nocoParams',
                'modInitDen', 'ldaU', 'ldaHIA', 'greensfCalculation', 'torgueCalculation', 'lo', 'orbcomprot',
                'cFCoeffs'
            ],
            'several':
            CaseInsensitiveFrozenSet(['absPos', 'filmPos', 'greensfCalculation', 'ldaHIA', 'ldaU', 'lo', 'relPos']),
            'simple':
            CaseInsensitiveFrozenSet([
                'absPos', 'atomicCutoffs', 'cFCoeffs', 'energyParameters', 'filmPos', 'force', 'ldaU', 'lo',
                'modInitDen', 'mtSphere', 'nocoParams', 'orbcomprot', 'relPos'
            ]),
            'text':
            CaseInsensitiveFrozenSet(['absPos', 'filmPos', 'orbcomprot', 'relPos'])
        },
        '/fleurInput/atomGroups/atomGroup/absPos': {
            'attribs':
            CaseInsensitiveFrozenSet(['alpha', 'banddos', 'beta', 'gamma', 'label', 'wannier']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'label': ' ',
                'wannier': 'F',
                'banddos': None,
                'alpha': None,
                'beta': None,
                'gamma': None
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/atomicCutoffs': {
            'attribs': CaseInsensitiveFrozenSet(['lmax', 'lmaxAPW', 'lnonsphr']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'lmaxapw': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/cFCoeffs': {
            'attribs': CaseInsensitiveFrozenSet(['chargeDensity', 'potential', 'remove4f']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'remove4f': 'F'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/energyParameters': {
            'attribs': CaseInsensitiveFrozenSet(['d', 'f', 'p', 's']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/filmPos': {
            'attribs':
            CaseInsensitiveFrozenSet(['alpha', 'banddos', 'beta', 'gamma', 'label', 'wannier']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'label': ' ',
                'wannier': 'F',
                'banddos': None,
                'alpha': None,
                'beta': None,
                'gamma': None
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/force': {
            'attribs': CaseInsensitiveFrozenSet(['calculate', 'relaxXYZ']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'relaxxyz': 'TTT'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/greensfCalculation': {
            'attribs': CaseInsensitiveFrozenSet(['kkintgrCutoff', 'l_sphavg', 'label', 'nshells']),
            'complex': CaseInsensitiveFrozenSet(['matrixElements']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'nshells': '0',
                'kkintgrcutoff': 'calc',
                'label': 'default'
            }),
            'order': ['matrixElements', 'diagElements'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['diagElements']),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/greensfCalculation/diagElements': {
            'attribs': CaseInsensitiveFrozenSet(['d', 'f', 'p', 's']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['s', 'p', 'd', 'f'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['d', 'f', 'p', 's']),
            'text': CaseInsensitiveFrozenSet(['d', 'f', 'p', 's'])
        },
        '/fleurInput/atomGroups/atomGroup/ldaHIA': {
            'attribs':
            CaseInsensitiveFrozenSet(['J', 'U', 'init_occ', 'kkintgrCutoff', 'l', 'l_amf', 'label', 'phi', 'theta']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet(['addArg', 'cFCoeff', 'exc']),
            'optional_attribs':
            CaseInsensitiveDict({
                'phi': '0.0',
                'theta': '0.0',
                'init_occ': 'calc',
                'kkintgrcutoff': 'calc',
                'label': 'default'
            }),
            'order': ['exc', 'cFCoeff', 'addArg'],
            'several':
            CaseInsensitiveFrozenSet(['addArg', 'cFCoeff', 'exc']),
            'simple':
            CaseInsensitiveFrozenSet(['addArg', 'cFCoeff', 'exc']),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/ldaHIA/addArg': {
            'attribs': CaseInsensitiveFrozenSet(['key', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/ldaHIA/cFCoeff': {
            'attribs': CaseInsensitiveFrozenSet(['l', 'm', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/ldaHIA/exc': {
            'attribs': CaseInsensitiveFrozenSet(['J', 'init_mom', 'l']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'init_mom': 'calc'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/ldaU': {
            'attribs': CaseInsensitiveFrozenSet(['J', 'U', 'l', 'l_amf', 'phi', 'theta']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'phi': '0.0',
                'theta': '0.0'
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/lo': {
            'attribs': CaseInsensitiveFrozenSet(['eDeriv', 'l', 'n', 'type']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'ederiv': '0'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/modInitDen': {
            'attribs':
            CaseInsensitiveFrozenSet(['flipSpinPhi', 'flipSpinScale', 'flipSpinTheta', 'magMom']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'magmom': '0.0',
                'flipspinphi': '0.0',
                'flipspintheta': '0.0',
                'flipspinscale': 'F'
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/mtSphere': {
            'attribs': CaseInsensitiveFrozenSet(['gridPoints', 'logIncrement', 'radius']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/nocoParams': {
            'attribs':
            CaseInsensitiveFrozenSet(
                ['M', 'alpha', 'b_cons_x', 'b_cons_y', 'beta', 'l_constrained', 'l_magn', 'l_mtNocoPot', 'l_relaxSQA']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'l_constrained': None,
                'l_mtnocopot': None,
                'l_relaxsqa': None,
                'l_magn': 'F',
                'm': '0.0',
                'b_cons_x': None,
                'b_cons_y': None
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/relPos': {
            'attribs':
            CaseInsensitiveFrozenSet(['alpha', 'banddos', 'beta', 'gamma', 'label', 'wannier']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'label': ' ',
                'wannier': 'F',
                'banddos': None,
                'alpha': None,
                'beta': None,
                'gamma': None
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/torgueCalculation': {
            'attribs': CaseInsensitiveFrozenSet(['kkintgrCutoff', 'label']),
            'complex': CaseInsensitiveFrozenSet(['greensfElements']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'kkintgrcutoff': 'calc',
                'label': 'default'
            }),
            'order': ['greensfElements'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['s', 'p', 'd', 'f'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['d', 'f', 'p', 's']),
            'text': CaseInsensitiveFrozenSet(['d', 'f', 'p', 's'])
        },
        '/fleurInput/atomSpecies': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet(['species']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['species'],
            'several': CaseInsensitiveFrozenSet(['species']),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species': {
            'attribs':
            CaseInsensitiveFrozenSet(['atomicNumber', 'element', 'name']),
            'complex':
            CaseInsensitiveFrozenSet(['electronConfig', 'greensfCalculation', 'ldaHIA', 'torgueCalculation']),
            'optional':
            CaseInsensitiveFrozenSet([
                'energyParameters', 'force', 'greensfCalculation', 'ldaHIA', 'ldaU', 'lo', 'modInitDen', 'nocoParams',
                'prodBasis', 'special', 'torgueCalculation'
            ]),
            'optional_attribs':
            CaseInsensitiveDict({'element': None}),
            'order': [
                'mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'prodBasis', 'special', 'force',
                'nocoParams', 'modInitDen', 'ldaU', 'ldaHIA', 'greensfCalculation', 'torgueCalculation', 'lo'
            ],
            'several':
            CaseInsensitiveFrozenSet(['greensfCalculation', 'ldaHIA', 'ldaU', 'lo']),
            'simple':
            CaseInsensitiveFrozenSet([
                'atomicCutoffs', 'energyParameters', 'force', 'ldaU', 'lo', 'modInitDen', 'mtSphere', 'nocoParams',
                'prodBasis', 'special'
            ]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/atomicCutoffs': {
            'attribs': CaseInsensitiveFrozenSet(['lmax', 'lmaxAPW', 'lnonsphr']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'lmaxapw': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/electronConfig': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['stateOccupation', 'valenceConfig']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['coreConfig', 'valenceConfig', 'stateOccupation'],
            'several': CaseInsensitiveFrozenSet(['stateOccupation']),
            'simple': CaseInsensitiveFrozenSet(['coreConfig', 'stateOccupation', 'valenceConfig']),
            'text': CaseInsensitiveFrozenSet(['coreConfig', 'valenceConfig'])
        },
        '/fleurInput/atomSpecies/species/electronConfig/stateOccupation': {
            'attribs': CaseInsensitiveFrozenSet(['spinDown', 'spinUp', 'state']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/energyParameters': {
            'attribs': CaseInsensitiveFrozenSet(['d', 'f', 'p', 's']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/force': {
            'attribs': CaseInsensitiveFrozenSet(['calculate', 'relaxXYZ']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'relaxxyz': 'TTT'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/greensfCalculation': {
            'attribs': CaseInsensitiveFrozenSet(['kkintgrCutoff', 'l_sphavg', 'label', 'nshells']),
            'complex': CaseInsensitiveFrozenSet(['matrixElements']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'nshells': '0',
                'kkintgrcutoff': 'calc',
                'label': 'default'
            }),
            'order': ['matrixElements', 'diagElements'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['diagElements']),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/greensfCalculation/diagElements': {
            'attribs': CaseInsensitiveFrozenSet(['d', 'f', 'p', 's']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['s', 'p', 'd', 'f'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['d', 'f', 'p', 's']),
            'text': CaseInsensitiveFrozenSet(['d', 'f', 'p', 's'])
        },
        '/fleurInput/atomSpecies/species/ldaHIA': {
            'attribs':
            CaseInsensitiveFrozenSet(['J', 'U', 'init_occ', 'kkintgrCutoff', 'l', 'l_amf', 'label', 'phi', 'theta']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet(['addArg', 'cFCoeff', 'exc']),
            'optional_attribs':
            CaseInsensitiveDict({
                'phi': '0.0',
                'theta': '0.0',
                'init_occ': 'calc',
                'kkintgrcutoff': 'calc',
                'label': 'default'
            }),
            'order': ['exc', 'cFCoeff', 'addArg'],
            'several':
            CaseInsensitiveFrozenSet(['addArg', 'cFCoeff', 'exc']),
            'simple':
            CaseInsensitiveFrozenSet(['addArg', 'cFCoeff', 'exc']),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/ldaHIA/addArg': {
            'attribs': CaseInsensitiveFrozenSet(['key', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/ldaHIA/cFCoeff': {
            'attribs': CaseInsensitiveFrozenSet(['l', 'm', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/ldaHIA/exc': {
            'attribs': CaseInsensitiveFrozenSet(['J', 'init_mom', 'l']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'init_mom': 'calc'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/ldaU': {
            'attribs': CaseInsensitiveFrozenSet(['J', 'U', 'l', 'l_amf', 'phi', 'theta']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'phi': '0.0',
                'theta': '0.0'
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/lo': {
            'attribs': CaseInsensitiveFrozenSet(['eDeriv', 'l', 'n', 'type']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'ederiv': '0'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/modInitDen': {
            'attribs':
            CaseInsensitiveFrozenSet(['flipSpinPhi', 'flipSpinScale', 'flipSpinTheta', 'magMom']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'magmom': '0.0',
                'flipspinphi': '0.0',
                'flipspintheta': '0.0',
                'flipspinscale': 'F'
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/mtSphere': {
            'attribs': CaseInsensitiveFrozenSet(['gridPoints', 'logIncrement', 'radius']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/nocoParams': {
            'attribs':
            CaseInsensitiveFrozenSet(
                ['M', 'alpha', 'b_cons_x', 'b_cons_y', 'beta', 'l_constrained', 'l_magn', 'l_mtNocoPot', 'l_relaxSQA']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'l_constrained': None,
                'l_mtnocopot': None,
                'l_relaxsqa': None,
                'l_magn': 'F',
                'm': '0.0',
                'b_cons_x': None,
                'b_cons_y': None
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/prodBasis': {
            'attribs': CaseInsensitiveFrozenSet(['lcutm', 'lcutwf', 'select']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'select': '4 0 4 2'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/special': {
            'attribs':
            CaseInsensitiveFrozenSet(['b_field_mt', 'lda', 'socscale', 'vca_charge']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'lda': 'F',
                'socscale': '1.0',
                'b_field_mt': '0.0',
                'vca_charge': '0.0'
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/torgueCalculation': {
            'attribs': CaseInsensitiveFrozenSet(['kkintgrCutoff', 'label']),
            'complex': CaseInsensitiveFrozenSet(['greensfElements']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'kkintgrcutoff': 'calc',
                'label': 'default'
            }),
            'order': ['greensfElements'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['s', 'p', 'd', 'f'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['d', 'f', 'p', 's']),
            'text': CaseInsensitiveFrozenSet(['d', 'f', 'p', 's'])
        },
        '/fleurInput/calculationSetup': {
            'attribs':
            CaseInsensitiveFrozenSet([]),
            'complex':
            CaseInsensitiveFrozenSet(['fields', 'greensFunction', 'magnetism', 'xcFunctional']),
            'optional':
            CaseInsensitiveFrozenSet([
                'expertModes', 'fields', 'geometryOptimization', 'greensFunction', 'ldaHIA', 'ldaU', 'oneDParams',
                'prodBasis', 'rdmft', 'soc', 'spinSpiralQPointMesh'
            ]),
            'optional_attribs':
            CaseInsensitiveDict({}),
            'order': [
                'cutoffs', 'scfLoop', 'coreElectrons', 'xcFunctional', 'magnetism', 'prodBasis', 'soc', 'oneDParams',
                'expertModes', 'geometryOptimization', 'ldaU', 'ldaHIA', 'greensFunction', 'rdmft',
                'spinSpiralQPointMesh', 'fields'
            ],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([
                'coreElectrons', 'cutoffs', 'expertModes', 'geometryOptimization', 'ldaHIA', 'ldaU', 'oneDParams',
                'prodBasis', 'rdmft', 'scfLoop', 'soc', 'spinSpiralQPointMesh'
            ]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/coreElectrons': {
            'attribs':
            CaseInsensitiveFrozenSet(['coretail_lmax', 'ctail', 'frcor', 'kcrel', 'l_core_confpot']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'frcor': 'F',
                'kcrel': '0',
                'coretail_lmax': '0',
                'l_core_confpot': 'T'
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/cutoffs': {
            'attribs': CaseInsensitiveFrozenSet(['Gmax', 'GmaxXC', 'Kmax', 'numbands']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'gmaxxc': '0.0',
                'numbands': '0'
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/expertModes': {
            'attribs':
            CaseInsensitiveFrozenSet(['eig66', 'gw', 'isec1', 'lpr', 'pot8', 'secvar', 'warp_factor']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'gw': '0',
                'pot8': 'F',
                'eig66': 'F',
                'lpr': '0',
                'isec1': '99',
                'secvar': 'F',
                'warp_factor': '1.0'
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/fields': {
            'attribs':
            CaseInsensitiveFrozenSet(
                ['autocomp', 'b_field', 'dirichlet', 'eV', 'plot_charge', 'plot_rho', 'sig_b_1', 'sig_b_2', 'zsigma']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet(['shape']),
            'optional_attribs':
            CaseInsensitiveDict({
                'b_field': '0.0',
                'zsigma': '10.0',
                'sig_b_1': '0.0',
                'sig_b_2': '0.0',
                'plot_charge': 'F',
                'plot_rho': 'F',
                'autocomp': 'T',
                'dirichlet': 'F',
                'ev': 'F'
            }),
            'order': ['shape'],
            'several':
            CaseInsensitiveFrozenSet(['shape']),
            'simple':
            CaseInsensitiveFrozenSet(['shape']),
            'text':
            CaseInsensitiveFrozenSet(['shape'])
        },
        '/fleurInput/calculationSetup/geometryOptimization': {
            'attribs':
            CaseInsensitiveFrozenSet(
                ['epsdisp', 'epsforce', 'f_level', 'force_converged', 'forcealpha', 'forcemix', 'l_f', 'qfix']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'f_level': '0',
                'forcealpha': '0',
                'epsdisp': '0.001',
                'epsforce': '0.001',
                'forcemix': 'BFGS',
                'qfix': '0',
                'force_converged': '0.00001'
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/greensFunction': {
            'attribs':
            CaseInsensitiveFrozenSet(['intFullRadial', 'l_mperp', 'l_resolvent', 'minCalcDistance', 'outputSphavg']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'l_mperp': 'F',
                'l_resolvent': 'F',
                'mincalcdistance': '-1.0',
                'outputsphavg': 'F',
                'intfullradial': 'F'
            }),
            'order': ['realAxis', 'contourRectangle', 'contourSemicircle', 'contourDOS'],
            'several':
            CaseInsensitiveFrozenSet(['contourDOS', 'contourRectangle', 'contourSemicircle']),
            'simple':
            CaseInsensitiveFrozenSet(['contourDOS', 'contourRectangle', 'contourSemicircle', 'realAxis']),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/greensFunction/contourDOS': {
            'attribs': CaseInsensitiveFrozenSet(['analytical_cont', 'eb', 'et', 'l_fermi', 'label', 'n', 'sigma']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'label': 'default'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/greensFunction/contourRectangle': {
            'attribs': CaseInsensitiveFrozenSet(['eb', 'label', 'n1', 'n2', 'n3', 'nmatsub', 'sigma']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'label': 'default'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/greensFunction/contourSemicircle': {
            'attribs': CaseInsensitiveFrozenSet(['alpha', 'eb', 'et', 'label', 'n']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'label': 'default'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/greensFunction/realAxis': {
            'attribs': CaseInsensitiveFrozenSet(['ellow', 'elup', 'ne']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/ldaHIA': {
            'attribs':
            CaseInsensitiveFrozenSet([
                'beta', 'dftspinpol', 'fullMatch', 'itmaxHubbard1', 'l_correctEtot', 'l_nonsphDC', 'minmatDistance',
                'minoccDistance', 'n_occpm'
            ]),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'beta': '100.0',
                'minoccdistance': '0.01',
                'minmatdistance': '0.001',
                'n_occpm': '2',
                'dftspinpol': 'F',
                'fullmatch': 'T',
                'l_nonsphdc': 'T',
                'l_correctetot': 'T'
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/ldaU': {
            'attribs':
            CaseInsensitiveFrozenSet(['l_adjEnpara', 'l_linMix', 'mixParam', 'spinf']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'l_linmix': 'F',
                'mixparam': '0.05',
                'spinf': '1.00',
                'l_adjenpara': 'F'
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/magnetism': {
            'attribs':
            CaseInsensitiveFrozenSet(
                ['fixed_moment', 'jspins', 'l_J', 'l_noco', 'l_onlyMtStDen', 'l_ss', 'lflip', 'swsp']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet(['mtNocoParams', 'qsc', 'qss', 'sourceFreeMag']),
            'optional_attribs':
            CaseInsensitiveDict({
                'l_noco': 'F',
                'l_ss': 'F',
                'l_j': 'F',
                'swsp': 'F',
                'lflip': 'F',
                'l_onlymtstden': 'F',
                'fixed_moment': '0.0'
            }),
            'order': ['qss', 'qsc', 'mtNocoParams', 'sourceFreeMag'],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet(['mtNocoParams', 'qsc', 'qss', 'sourceFreeMag']),
            'text':
            CaseInsensitiveFrozenSet(['qsc', 'qss'])
        },
        '/fleurInput/calculationSetup/magnetism/mtNocoParams': {
            'attribs':
            CaseInsensitiveFrozenSet([
                'l_constrained', 'l_mperp', 'l_mtNocoPot', 'l_relaxSQA', 'mag_mixing_scheme', 'mix_RelaxWeightOffD',
                'mix_constr'
            ]),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'l_mtnocopot': 'F',
                'l_mperp': 'F',
                'l_constrained': 'F',
                'l_relaxsqa': 'F',
                'mag_mixing_scheme': '0',
                'mix_relaxweightoffd': '1.0',
                'mix_constr': '1.0'
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/magnetism/sourceFreeMag': {
            'attribs': CaseInsensitiveFrozenSet(['l_scaleMag', 'l_sourceFree', 'mag_scale']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'l_sourcefree': 'F',
                'l_scalemag': 'F',
                'mag_scale': '1.0'
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/oneDParams': {
            'attribs': CaseInsensitiveFrozenSet(['MM', 'chi', 'd1', 'invs1', 'm_cyl', 'rot', 'vM', 'zrfs1']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/prodBasis': {
            'attribs':
            CaseInsensitiveFrozenSet(['bands', 'ewaldlambda', 'fftcut', 'gcutm', 'lexp', 'tolerance']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'tolerance': '0.00001',
                'lexp': '16',
                'ewaldlambda': '3',
                'fftcut': '1.0'
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/rdmft': {
            'attribs': CaseInsensitiveFrozenSet(['functional', 'l_rdmft', 'occEps', 'statesAbove', 'statesBelow']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'occeps': '0.00001'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/scfLoop': {
            'attribs':
            CaseInsensitiveFrozenSet([
                'alpha', 'imix', 'itmax', 'maxIterBroyd', 'maxTimeToStartIter', 'minDistance', 'precondParam', 'spinf'
            ]),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'maxiterbroyd': '99',
                'precondparam': '0.0',
                'spinf': '2.0',
                'mindistance': '0.0',
                'maxtimetostartiter': None
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/soc': {
            'attribs': CaseInsensitiveFrozenSet(['l_soc', 'off', 'phi', 'soc66', 'spav', 'theta']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'spav': 'F',
                'off': 'F',
                'soc66': 'T'
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/spinSpiralQPointMesh': {
            'attribs': CaseInsensitiveFrozenSet(['qx', 'qy', 'qz']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/xcFunctional': {
            'attribs': CaseInsensitiveFrozenSet(['name', 'relativisticCorrections']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['LibXCID', 'LibXCName', 'ggaPrinting', 'xcParams']),
            'optional_attribs': CaseInsensitiveDict({'relativisticcorrections': 'F'}),
            'order': ['LibXCID', 'LibXCName', 'xcParams', 'ggaPrinting'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['LibXCID', 'LibXCName', 'ggaPrinting', 'xcParams']),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/xcFunctional/LibXCID': {
            'attribs': CaseInsensitiveFrozenSet(['correlation', 'etot_correlation', 'etot_exchange', 'exchange']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'etot_exchange': None,
                'etot_correlation': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/xcFunctional/LibXCName': {
            'attribs': CaseInsensitiveFrozenSet(['correlation', 'etot_correlation', 'etot_exchange', 'exchange']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'etot_exchange': None,
                'etot_correlation': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/xcFunctional/ggaPrinting': {
            'attribs': CaseInsensitiveFrozenSet(['idsprs0', 'idsprsi', 'idsprsl', 'idsprsv', 'iggachk']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/calculationSetup/xcFunctional/xcParams': {
            'attribs': CaseInsensitiveFrozenSet(['chng', 'idsprs', 'igrd', 'lwb', 'ndvgrd']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet(['bulkLattice', 'bzIntegration', 'filmLattice', 'symmetryOperations']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['bzIntegration', 'symmetryOperations', 'bulkLattice', 'filmLattice'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/bulkLattice': {
            'attribs': CaseInsensitiveFrozenSet(['scale']),
            'complex': CaseInsensitiveFrozenSet(['bravaisMatrix']),
            'optional': CaseInsensitiveFrozenSet(['a2']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['a1', 'a2', 'c', 'row-1', 'row-2', 'c', 'bravaisMatrix'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['a1', 'a2', 'c', 'row-1', 'row-2']),
            'text': CaseInsensitiveFrozenSet(['a1', 'a2', 'c', 'row-1', 'row-2'])
        },
        '/fleurInput/cell/bulkLattice/a1': {
            'attribs': CaseInsensitiveFrozenSet(['scale']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'scale': '1.0'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/bulkLattice/a2': {
            'attribs': CaseInsensitiveFrozenSet(['scale']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'scale': '1.0'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/bulkLattice/bravaisMatrix': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['row-1', 'row-2', 'row-3'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['row-1', 'row-2', 'row-3']),
            'text': CaseInsensitiveFrozenSet(['row-1', 'row-2', 'row-3'])
        },
        '/fleurInput/cell/bulkLattice/c': {
            'attribs': CaseInsensitiveFrozenSet(['scale']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'scale': '1.0'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/bzIntegration': {
            'attribs':
            CaseInsensitiveFrozenSet(
                ['fermiSmearingEnergy', 'fermiSmearingTemp', 'l_bloechl', 'mode', 'valenceElectrons']),
            'complex':
            CaseInsensitiveFrozenSet(['kPointLists']),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'valenceelectrons': None,
                'mode': 'hist',
                'fermismearingenergy': None,
                'fermismearingtemp': None,
                'l_bloechl': 'F'
            }),
            'order': ['kPointListSelection', 'kPointLists'],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet(['kPointListSelection']),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/bzIntegration/kPointListSelection': {
            'attribs': CaseInsensitiveFrozenSet(['listName']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/bzIntegration/kPointLists': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet(['kPointList']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['kPointList'],
            'several': CaseInsensitiveFrozenSet(['kPointList']),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/bzIntegration/kPointLists/kPointList': {
            'attribs':
            CaseInsensitiveFrozenSet(['count', 'name', 'nkq_pairs', 'nx', 'ny', 'nz', 'type']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'type': 'unspecified',
                'count': None,
                'nx': None,
                'ny': None,
                'nz': None,
                'nkq_pairs': None
            }),
            'order': ['kPoint'],
            'several':
            CaseInsensitiveFrozenSet(['kPoint']),
            'simple':
            CaseInsensitiveFrozenSet(['kPoint']),
            'text':
            CaseInsensitiveFrozenSet(['kPoint'])
        },
        '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint': {
            'attribs': CaseInsensitiveFrozenSet(['label', 'weight']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'label': ''}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/filmLattice': {
            'attribs': CaseInsensitiveFrozenSet(['dTilda', 'dVac', 'scale']),
            'complex': CaseInsensitiveFrozenSet(['bravaisMatrix']),
            'optional': CaseInsensitiveFrozenSet(['a2', 'vacuumEnergyParameters']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['a1', 'a2', 'row-1', 'row-2', 'bravaisMatrix', 'vacuumEnergyParameters'],
            'several': CaseInsensitiveFrozenSet(['vacuumEnergyParameters']),
            'simple': CaseInsensitiveFrozenSet(['a1', 'a2', 'row-1', 'row-2', 'vacuumEnergyParameters']),
            'text': CaseInsensitiveFrozenSet(['a1', 'a2', 'row-1', 'row-2'])
        },
        '/fleurInput/cell/filmLattice/a1': {
            'attribs': CaseInsensitiveFrozenSet(['scale']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'scale': '1.0'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/filmLattice/a2': {
            'attribs': CaseInsensitiveFrozenSet(['scale']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'scale': '1.0'}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/filmLattice/bravaisMatrix': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['row-1', 'row-2', 'row-3'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['row-1', 'row-2', 'row-3']),
            'text': CaseInsensitiveFrozenSet(['row-1', 'row-2', 'row-3'])
        },
        '/fleurInput/cell/filmLattice/vacuumEnergyParameters': {
            'attribs': CaseInsensitiveFrozenSet(['spinDown', 'spinUp', 'vacuum']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({'spindown': None}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/symmetryOperations': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet(['symOp']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['symOp'],
            'several': CaseInsensitiveFrozenSet(['symOp']),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/cell/symmetryOperations/symOp': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['row-1', 'row-2', 'row-3'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['row-1', 'row-2', 'row-3']),
            'text': CaseInsensitiveFrozenSet(['row-1', 'row-2', 'row-3'])
        },
        '/fleurInput/constants': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['constant']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['constant'],
            'several': CaseInsensitiveFrozenSet(['constant']),
            'simple': CaseInsensitiveFrozenSet(['constant']),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/constants/constant': {
            'attribs': CaseInsensitiveFrozenSet(['name', 'value']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/forceTheorem': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet(['DMI', 'Jij', 'spinSpiralDispersion']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['MAE', 'spinSpiralDispersion', 'DMI', 'Jij'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['MAE']),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/forceTheorem/DMI': {
            'attribs': CaseInsensitiveFrozenSet(['phi', 'theta']),
            'complex': CaseInsensitiveFrozenSet(['qVectors']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['qVectors'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/forceTheorem/DMI/qVectors': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['q'],
            'several': CaseInsensitiveFrozenSet(['q']),
            'simple': CaseInsensitiveFrozenSet(['q']),
            'text': CaseInsensitiveFrozenSet(['q'])
        },
        '/fleurInput/forceTheorem/Jij': {
            'attribs': CaseInsensitiveFrozenSet(['thetaj']),
            'complex': CaseInsensitiveFrozenSet(['qVectors']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['qVectors'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/forceTheorem/Jij/qVectors': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['q'],
            'several': CaseInsensitiveFrozenSet(['q']),
            'simple': CaseInsensitiveFrozenSet(['q']),
            'text': CaseInsensitiveFrozenSet(['q'])
        },
        '/fleurInput/forceTheorem/MAE': {
            'attribs': CaseInsensitiveFrozenSet(['phi', 'theta']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/forceTheorem/spinSpiralDispersion': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['q'],
            'several': CaseInsensitiveFrozenSet(['q']),
            'simple': CaseInsensitiveFrozenSet(['q']),
            'text': CaseInsensitiveFrozenSet(['q'])
        },
        '/fleurInput/output': {
            'attribs':
            CaseInsensitiveFrozenSet(['band', 'coreSpec', 'dos', 'eig66', 'slice', 'wannier']),
            'complex':
            CaseInsensitiveFrozenSet(['coreSpectrum', 'plotting', 'vacuumDOS', 'wannier']),
            'optional':
            CaseInsensitiveFrozenSet([
                'bandDOS', 'chargeDensitySlicing', 'checks', 'coreSpectrum', 'juPhon', 'magneticCircularDichroism',
                'plotting', 'specialOutput', 'unfoldingBand', 'vacuumDOS', 'wannier'
            ]),
            'optional_attribs':
            CaseInsensitiveDict({
                'dos': 'F',
                'band': 'F',
                'slice': 'F',
                'corespec': 'F',
                'wannier': 'F',
                'eig66': 'F'
            }),
            'order': [
                'checks', 'bandDOS', 'vacuumDOS', 'plotting', 'chargeDensitySlicing', 'specialOutput', 'coreSpectrum',
                'wannier', 'magneticCircularDichroism', 'unfoldingBand', 'juPhon'
            ],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([
                'bandDOS', 'chargeDensitySlicing', 'checks', 'juPhon', 'magneticCircularDichroism', 'specialOutput',
                'unfoldingBand'
            ]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output/bandDOS': {
            'attribs':
            CaseInsensitiveFrozenSet(
                ['all_atoms', 'jDOS', 'maxEnergy', 'minEnergy', 'numberPoints', 'orbcomp', 'sigma']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'all_atoms': 'T',
                'orbcomp': 'F',
                'jdos': 'F',
                'minenergy': '-0.5',
                'maxenergy': '0.5',
                'sigma': '0.01',
                'numberpoints': '1321'
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output/chargeDensitySlicing': {
            'attribs': CaseInsensitiveFrozenSet(['maxEigenval', 'minEigenval', 'nnne', 'numkpt', 'pallst']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output/checks': {
            'attribs': CaseInsensitiveFrozenSet(['cdinf', 'disp', 'vchk']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'vchk': 'F',
                'cdinf': 'F',
                'disp': 'F'
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output/coreSpectrum': {
            'attribs':
            CaseInsensitiveFrozenSet([
                'I_initial', 'alpha_Ex', 'atomType', 'beta_Ex', 'eKin', 'eMax', 'eMin', 'edgeType', 'lmax', 'nqphi',
                'nqr', 'numPoints', 'verbose'
            ]),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'verbose': 'F',
                'nqphi': '10',
                'nqr': '10',
                'alpha_ex': '0.024',
                'beta_ex': '0.05',
                'i_initial': '155'
            }),
            'order': ['edgeIndices'],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet(['edgeIndices']),
            'text':
            CaseInsensitiveFrozenSet(['edgeIndices'])
        },
        '/fleurInput/output/juPhon': {
            'attribs': CaseInsensitiveFrozenSet(['l_eigout', 'l_potout']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output/magneticCircularDichroism': {
            'attribs': CaseInsensitiveFrozenSet(['energyLo', 'energyUp', 'mcd']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output/plotting': {
            'attribs': CaseInsensitiveFrozenSet(['format', 'iplot', 'polar']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['plot']),
            'optional_attribs': CaseInsensitiveDict({
                'iplot': '0',
                'polar': 'F',
                'format': '1'
            }),
            'order': ['plot'],
            'several': CaseInsensitiveFrozenSet(['plot']),
            'simple': CaseInsensitiveFrozenSet(['plot']),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output/plotting/plot': {
            'attribs':
            CaseInsensitiveFrozenSet(
                ['TwoD', 'cartesian', 'file', 'grid', 'onlyMT', 'typeMT', 'vec1', 'vec2', 'vec3', 'vecField', 'zero']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet([]),
            'optional_attribs':
            CaseInsensitiveDict({
                'cartesian': 'F',
                'twod': 'T',
                'grid': '30 30 30',
                'vec1': '1.0 0.0 0.0',
                'vec2': '0.0 1.0 0.0',
                'vec3': '0.0 0.0 1.0',
                'zero': '0.0 0.0 0.0',
                'file': 'plot',
                'onlymt': 'F',
                'typemt': '0',
                'vecfield': 'F'
            }),
            'order': [],
            'several':
            CaseInsensitiveFrozenSet([]),
            'simple':
            CaseInsensitiveFrozenSet([]),
            'text':
            CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output/specialOutput': {
            'attribs': CaseInsensitiveFrozenSet(['bmt', 'eonly', 'form66']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'form66': 'F',
                'eonly': 'F',
                'bmt': 'F'
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output/unfoldingBand': {
            'attribs': CaseInsensitiveFrozenSet(['supercellX', 'supercellY', 'supercellZ', 'unfoldBand']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/output/vacuumDOS': {
            'attribs':
            CaseInsensitiveFrozenSet(
                ['integ', 'locx1', 'locx2', 'locy1', 'locy2', 'nstars', 'nstm', 'star', 'tworkf', 'vacdos']),
            'complex':
            CaseInsensitiveFrozenSet([]),
            'optional':
            CaseInsensitiveFrozenSet(['layer']),
            'optional_attribs':
            CaseInsensitiveDict({
                'integ': 'F',
                'star': 'F',
                'nstars': None,
                'locx1': '0.0',
                'locy1': '0.0',
                'locx2': '1.0',
                'locy2': '1.0',
                'nstm': '0',
                'tworkf': '0.0'
            }),
            'order': ['layer'],
            'several':
            CaseInsensitiveFrozenSet(['layer']),
            'simple':
            CaseInsensitiveFrozenSet(['layer']),
            'text':
            CaseInsensitiveFrozenSet(['layer'])
        },
        '/fleurInput/output/wannier': {
            'attribs': CaseInsensitiveFrozenSet(['atomList', 'bsComf', 'ms', 'sgwf', 'socgwf']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet(['bandSelection', 'jobList']),
            'optional_attribs': CaseInsensitiveDict({
                'ms': 'F',
                'sgwf': 'F',
                'socgwf': 'F',
                'bscomf': 'F',
                'atomlist': 'F'
            }),
            'order': ['bandSelection', 'jobList'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet(['bandSelection', 'jobList']),
            'text': CaseInsensitiveFrozenSet(['jobList'])
        },
        '/fleurInput/output/wannier/bandSelection': {
            'attribs': CaseInsensitiveFrozenSet(['maxSpinDown', 'maxSpinUp', 'minSpinDown', 'minSpinUp']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({
                'minspindown': None,
                'maxspindown': None
            }),
            'order': [],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/relaxation': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet(['displacements', 'relaxation-history']),
            'optional': CaseInsensitiveFrozenSet(['displacements', 'relaxation-history']),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['displacements', 'relaxation-history'],
            'several': CaseInsensitiveFrozenSet([]),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/relaxation/displacements': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['displace'],
            'several': CaseInsensitiveFrozenSet(['displace']),
            'simple': CaseInsensitiveFrozenSet(['displace']),
            'text': CaseInsensitiveFrozenSet(['displace'])
        },
        '/fleurInput/relaxation/relaxation-history': {
            'attribs': CaseInsensitiveFrozenSet([]),
            'complex': CaseInsensitiveFrozenSet(['step']),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['step'],
            'several': CaseInsensitiveFrozenSet(['step']),
            'simple': CaseInsensitiveFrozenSet([]),
            'text': CaseInsensitiveFrozenSet([])
        },
        '/fleurInput/relaxation/relaxation-history/step': {
            'attribs': CaseInsensitiveFrozenSet(['energy']),
            'complex': CaseInsensitiveFrozenSet([]),
            'optional': CaseInsensitiveFrozenSet([]),
            'optional_attribs': CaseInsensitiveDict({}),
            'order': ['posforce'],
            'several': CaseInsensitiveFrozenSet(['posforce']),
            'simple': CaseInsensitiveFrozenSet(['posforce']),
            'text': CaseInsensitiveFrozenSet(['posforce'])
        }
    },
    'tag_paths':
    CaseInsensitiveDict({
        'dmi':
        '/fleurInput/forceTheorem/DMI',
        'jij':
        '/fleurInput/forceTheorem/Jij',
        'libxcid':
        '/fleurInput/calculationSetup/xcFunctional/LibXCID',
        'libxcname':
        '/fleurInput/calculationSetup/xcFunctional/LibXCName',
        'mae':
        '/fleurInput/forceTheorem/MAE',
        'a1': ['/fleurInput/cell/bulkLattice/a1', '/fleurInput/cell/filmLattice/a1'],
        'a2': ['/fleurInput/cell/bulkLattice/a2', '/fleurInput/cell/filmLattice/a2'],
        'abspos':
        '/fleurInput/atomGroups/atomGroup/absPos',
        'addarg': ['/fleurInput/atomGroups/atomGroup/ldaHIA/addArg', '/fleurInput/atomSpecies/species/ldaHIA/addArg'],
        'atomgroup':
        '/fleurInput/atomGroups/atomGroup',
        'atomgroups':
        '/fleurInput/atomGroups',
        'atomspecies':
        '/fleurInput/atomSpecies',
        'atomiccutoffs':
        ['/fleurInput/atomGroups/atomGroup/atomicCutoffs', '/fleurInput/atomSpecies/species/atomicCutoffs'],
        'banddos':
        '/fleurInput/output/bandDOS',
        'bandselection':
        '/fleurInput/output/wannier/bandSelection',
        'bravaismatrix': ['/fleurInput/cell/bulkLattice/bravaisMatrix', '/fleurInput/cell/filmLattice/bravaisMatrix'],
        'bulklattice':
        '/fleurInput/cell/bulkLattice',
        'bzintegration':
        '/fleurInput/cell/bzIntegration',
        'c':
        '/fleurInput/cell/bulkLattice/c',
        'cfcoeff':
        ['/fleurInput/atomGroups/atomGroup/ldaHIA/cFCoeff', '/fleurInput/atomSpecies/species/ldaHIA/cFCoeff'],
        'cfcoeffs':
        '/fleurInput/atomGroups/atomGroup/cFCoeffs',
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
        'contourdos':
        '/fleurInput/calculationSetup/greensFunction/contourDOS',
        'contourrectangle':
        '/fleurInput/calculationSetup/greensFunction/contourRectangle',
        'contoursemicircle':
        '/fleurInput/calculationSetup/greensFunction/contourSemicircle',
        'coreconfig':
        '/fleurInput/atomSpecies/species/electronConfig/coreConfig',
        'coreelectrons':
        '/fleurInput/calculationSetup/coreElectrons',
        'corespectrum':
        '/fleurInput/output/coreSpectrum',
        'cutoffs':
        '/fleurInput/calculationSetup/cutoffs',
        'd': [
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements/d',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements/d',
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements/d',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/d'
        ],
        'diagelements': [
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/diagElements',
            '/fleurInput/atomSpecies/species/greensfCalculation/diagElements'
        ],
        'displace':
        '/fleurInput/relaxation/displacements/displace',
        'displacements':
        '/fleurInput/relaxation/displacements',
        'edgeindices':
        '/fleurInput/output/coreSpectrum/edgeIndices',
        'electronconfig':
        '/fleurInput/atomSpecies/species/electronConfig',
        'energyparameters':
        ['/fleurInput/atomGroups/atomGroup/energyParameters', '/fleurInput/atomSpecies/species/energyParameters'],
        'exc': ['/fleurInput/atomGroups/atomGroup/ldaHIA/exc', '/fleurInput/atomSpecies/species/ldaHIA/exc'],
        'expertmodes':
        '/fleurInput/calculationSetup/expertModes',
        'f': [
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements/f',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements/f',
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements/f',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/f'
        ],
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
        '/fleurInput/calculationSetup/xcFunctional/ggaPrinting',
        'greensfunction':
        '/fleurInput/calculationSetup/greensFunction',
        'greensfcalculation':
        ['/fleurInput/atomGroups/atomGroup/greensfCalculation', '/fleurInput/atomSpecies/species/greensfCalculation'],
        'greensfelements': [
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements'
        ],
        'joblist':
        '/fleurInput/output/wannier/jobList',
        'juphon':
        '/fleurInput/output/juPhon',
        'kpoint':
        '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint',
        'kpointlist':
        '/fleurInput/cell/bzIntegration/kPointLists/kPointList',
        'kpointlistselection':
        '/fleurInput/cell/bzIntegration/kPointListSelection',
        'kpointlists':
        '/fleurInput/cell/bzIntegration/kPointLists',
        'layer':
        '/fleurInput/output/vacuumDOS/layer',
        'ldahia': [
            '/fleurInput/atomGroups/atomGroup/ldaHIA', '/fleurInput/atomSpecies/species/ldaHIA',
            '/fleurInput/calculationSetup/ldaHIA'
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
        'matrixelements': [
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements',
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements'
        ],
        'modinitden': ['/fleurInput/atomGroups/atomGroup/modInitDen', '/fleurInput/atomSpecies/species/modInitDen'],
        'mtnocoparams':
        '/fleurInput/calculationSetup/magnetism/mtNocoParams',
        'mtsphere': ['/fleurInput/atomGroups/atomGroup/mtSphere', '/fleurInput/atomSpecies/species/mtSphere'],
        'nocoparams': ['/fleurInput/atomGroups/atomGroup/nocoParams', '/fleurInput/atomSpecies/species/nocoParams'],
        'onedparams':
        '/fleurInput/calculationSetup/oneDParams',
        'orbcomprot':
        '/fleurInput/atomGroups/atomGroup/orbcomprot',
        'output':
        '/fleurInput/output',
        'p': [
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements/p',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements/p',
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements/p',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/p'
        ],
        'plot':
        '/fleurInput/output/plotting/plot',
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
        '/fleurInput/calculationSetup/magnetism/qsc',
        'qss':
        '/fleurInput/calculationSetup/magnetism/qss',
        'rdmft':
        '/fleurInput/calculationSetup/rdmft',
        'realaxis':
        '/fleurInput/calculationSetup/greensFunction/realAxis',
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
        's': [
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements/s',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements/s',
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements/s',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/s'
        ],
        'scfloop':
        '/fleurInput/calculationSetup/scfLoop',
        'shape':
        '/fleurInput/calculationSetup/fields/shape',
        'soc':
        '/fleurInput/calculationSetup/soc',
        'sourcefreemag':
        '/fleurInput/calculationSetup/magnetism/sourceFreeMag',
        'special':
        '/fleurInput/atomSpecies/species/special',
        'specialoutput':
        '/fleurInput/output/specialOutput',
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
        'symmetryoperations':
        '/fleurInput/cell/symmetryOperations',
        'torguecalculation':
        ['/fleurInput/atomGroups/atomGroup/torgueCalculation', '/fleurInput/atomSpecies/species/torgueCalculation'],
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
        '/fleurInput/calculationSetup/xcFunctional',
        'xcparams':
        '/fleurInput/calculationSetup/xcFunctional/xcParams'
    }),
    'unique_attribs':
    CaseInsensitiveDict({
        'gmax': '/fleurInput/calculationSetup/cutoffs/@Gmax',
        'gmaxxc': '/fleurInput/calculationSetup/cutoffs/@GmaxXC',
        'i_initial': '/fleurInput/output/coreSpectrum/@I_initial',
        'kmax': '/fleurInput/calculationSetup/cutoffs/@Kmax',
        'mm': '/fleurInput/calculationSetup/oneDParams/@MM',
        'all_atoms': '/fleurInput/output/bandDOS/@all_atoms',
        'alpha': '/fleurInput/calculationSetup/scfLoop/@alpha',
        'alpha_ex': '/fleurInput/output/coreSpectrum/@alpha_Ex',
        'atomlist': '/fleurInput/output/wannier/@atomList',
        'atomtype': '/fleurInput/output/coreSpectrum/@atomType',
        'autocomp': '/fleurInput/calculationSetup/fields/@autocomp',
        'b_field': '/fleurInput/calculationSetup/fields/@b_field',
        'band': '/fleurInput/output/@band',
        'bands': '/fleurInput/calculationSetup/prodBasis/@bands',
        'beta': '/fleurInput/calculationSetup/ldaHIA/@beta',
        'beta_ex': '/fleurInput/output/coreSpectrum/@beta_Ex',
        'bmt': '/fleurInput/output/specialOutput/@bmt',
        'bscomf': '/fleurInput/output/wannier/@bsComf',
        'cdinf': '/fleurInput/output/checks/@cdinf',
        'chi': '/fleurInput/calculationSetup/oneDParams/@chi',
        'chng': '/fleurInput/calculationSetup/xcFunctional/xcParams/@chng',
        'corespec': '/fleurInput/output/@coreSpec',
        'coretail_lmax': '/fleurInput/calculationSetup/coreElectrons/@coretail_lmax',
        'ctail': '/fleurInput/calculationSetup/coreElectrons/@ctail',
        'd1': '/fleurInput/calculationSetup/oneDParams/@d1',
        'dtilda': '/fleurInput/cell/filmLattice/@dTilda',
        'dvac': '/fleurInput/cell/filmLattice/@dVac',
        'dftspinpol': '/fleurInput/calculationSetup/ldaHIA/@dftspinpol',
        'dirichlet': '/fleurInput/calculationSetup/fields/@dirichlet',
        'disp': '/fleurInput/output/checks/@disp',
        'dos': '/fleurInput/output/@dos',
        'ekin': '/fleurInput/output/coreSpectrum/@eKin',
        'emax': '/fleurInput/output/coreSpectrum/@eMax',
        'emin': '/fleurInput/output/coreSpectrum/@eMin',
        'ev': '/fleurInput/calculationSetup/fields/@eV',
        'edgetype': '/fleurInput/output/coreSpectrum/@edgeType',
        'ellow': '/fleurInput/calculationSetup/greensFunction/realAxis/@ellow',
        'elup': '/fleurInput/calculationSetup/greensFunction/realAxis/@elup',
        'energylo': '/fleurInput/output/magneticCircularDichroism/@energyLo',
        'energyup': '/fleurInput/output/magneticCircularDichroism/@energyUp',
        'eonly': '/fleurInput/output/specialOutput/@eonly',
        'epsdisp': '/fleurInput/calculationSetup/geometryOptimization/@epsdisp',
        'epsforce': '/fleurInput/calculationSetup/geometryOptimization/@epsforce',
        'ewaldlambda': '/fleurInput/calculationSetup/prodBasis/@ewaldlambda',
        'f_level': '/fleurInput/calculationSetup/geometryOptimization/@f_level',
        'fermismearingenergy': '/fleurInput/cell/bzIntegration/@fermiSmearingEnergy',
        'fermismearingtemp': '/fleurInput/cell/bzIntegration/@fermiSmearingTemp',
        'fftcut': '/fleurInput/calculationSetup/prodBasis/@fftcut',
        'fixed_moment': '/fleurInput/calculationSetup/magnetism/@fixed_moment',
        'fleurinputversion': '/fleurInput/@fleurInputVersion',
        'force_converged': '/fleurInput/calculationSetup/geometryOptimization/@force_converged',
        'forcealpha': '/fleurInput/calculationSetup/geometryOptimization/@forcealpha',
        'forcemix': '/fleurInput/calculationSetup/geometryOptimization/@forcemix',
        'form66': '/fleurInput/output/specialOutput/@form66',
        'format': '/fleurInput/output/plotting/@format',
        'frcor': '/fleurInput/calculationSetup/coreElectrons/@frcor',
        'fullmatch': '/fleurInput/calculationSetup/ldaHIA/@fullMatch',
        'functional': '/fleurInput/calculationSetup/rdmft/@functional',
        'gcutm': '/fleurInput/calculationSetup/prodBasis/@gcutm',
        'gw': '/fleurInput/calculationSetup/expertModes/@gw',
        'idsprs': '/fleurInput/calculationSetup/xcFunctional/xcParams/@idsprs',
        'idsprs0': '/fleurInput/calculationSetup/xcFunctional/ggaPrinting/@idsprs0',
        'idsprsi': '/fleurInput/calculationSetup/xcFunctional/ggaPrinting/@idsprsi',
        'idsprsl': '/fleurInput/calculationSetup/xcFunctional/ggaPrinting/@idsprsl',
        'idsprsv': '/fleurInput/calculationSetup/xcFunctional/ggaPrinting/@idsprsv',
        'iggachk': '/fleurInput/calculationSetup/xcFunctional/ggaPrinting/@iggachk',
        'igrd': '/fleurInput/calculationSetup/xcFunctional/xcParams/@igrd',
        'imix': '/fleurInput/calculationSetup/scfLoop/@imix',
        'intfullradial': '/fleurInput/calculationSetup/greensFunction/@intFullRadial',
        'integ': '/fleurInput/output/vacuumDOS/@integ',
        'invs1': '/fleurInput/calculationSetup/oneDParams/@invs1',
        'iplot': '/fleurInput/output/plotting/@iplot',
        'isec1': '/fleurInput/calculationSetup/expertModes/@isec1',
        'itmax': '/fleurInput/calculationSetup/scfLoop/@itmax',
        'itmaxhubbard1': '/fleurInput/calculationSetup/ldaHIA/@itmaxHubbard1',
        'jdos': '/fleurInput/output/bandDOS/@jDOS',
        'jspins': '/fleurInput/calculationSetup/magnetism/@jspins',
        'kcrel': '/fleurInput/calculationSetup/coreElectrons/@kcrel',
        'l_j': '/fleurInput/calculationSetup/magnetism/@l_J',
        'l_adjenpara': '/fleurInput/calculationSetup/ldaU/@l_adjEnpara',
        'l_bloechl': '/fleurInput/cell/bzIntegration/@l_bloechl',
        'l_constrained': '/fleurInput/calculationSetup/magnetism/mtNocoParams/@l_constrained',
        'l_core_confpot': '/fleurInput/calculationSetup/coreElectrons/@l_core_confpot',
        'l_correctetot': '/fleurInput/calculationSetup/ldaHIA/@l_correctEtot',
        'l_eigout': '/fleurInput/output/juPhon/@l_eigout',
        'l_f': '/fleurInput/calculationSetup/geometryOptimization/@l_f',
        'l_linmix': '/fleurInput/calculationSetup/ldaU/@l_linMix',
        'l_mtnocopot': '/fleurInput/calculationSetup/magnetism/mtNocoParams/@l_mtNocoPot',
        'l_noco': '/fleurInput/calculationSetup/magnetism/@l_noco',
        'l_nonsphdc': '/fleurInput/calculationSetup/ldaHIA/@l_nonsphDC',
        'l_onlymtstden': '/fleurInput/calculationSetup/magnetism/@l_onlyMtStDen',
        'l_potout': '/fleurInput/output/juPhon/@l_potout',
        'l_rdmft': '/fleurInput/calculationSetup/rdmft/@l_rdmft',
        'l_relaxsqa': '/fleurInput/calculationSetup/magnetism/mtNocoParams/@l_relaxSQA',
        'l_resolvent': '/fleurInput/calculationSetup/greensFunction/@l_resolvent',
        'l_scalemag': '/fleurInput/calculationSetup/magnetism/sourceFreeMag/@l_scaleMag',
        'l_soc': '/fleurInput/calculationSetup/soc/@l_soc',
        'l_sourcefree': '/fleurInput/calculationSetup/magnetism/sourceFreeMag/@l_sourceFree',
        'l_ss': '/fleurInput/calculationSetup/magnetism/@l_ss',
        'lexp': '/fleurInput/calculationSetup/prodBasis/@lexp',
        'lflip': '/fleurInput/calculationSetup/magnetism/@lflip',
        'listname': '/fleurInput/cell/bzIntegration/kPointListSelection/@listName',
        'lmax': '/fleurInput/output/coreSpectrum/@lmax',
        'locx1': '/fleurInput/output/vacuumDOS/@locx1',
        'locx2': '/fleurInput/output/vacuumDOS/@locx2',
        'locy1': '/fleurInput/output/vacuumDOS/@locy1',
        'locy2': '/fleurInput/output/vacuumDOS/@locy2',
        'lpr': '/fleurInput/calculationSetup/expertModes/@lpr',
        'lwb': '/fleurInput/calculationSetup/xcFunctional/xcParams/@lwb',
        'm_cyl': '/fleurInput/calculationSetup/oneDParams/@m_cyl',
        'mag_mixing_scheme': '/fleurInput/calculationSetup/magnetism/mtNocoParams/@mag_mixing_scheme',
        'mag_scale': '/fleurInput/calculationSetup/magnetism/sourceFreeMag/@mag_scale',
        'maxeigenval': '/fleurInput/output/chargeDensitySlicing/@maxEigenval',
        'maxenergy': '/fleurInput/output/bandDOS/@maxEnergy',
        'maxiterbroyd': '/fleurInput/calculationSetup/scfLoop/@maxIterBroyd',
        'maxspindown': '/fleurInput/output/wannier/bandSelection/@maxSpinDown',
        'maxspinup': '/fleurInput/output/wannier/bandSelection/@maxSpinUp',
        'maxtimetostartiter': '/fleurInput/calculationSetup/scfLoop/@maxTimeToStartIter',
        'mcd': '/fleurInput/output/magneticCircularDichroism/@mcd',
        'mincalcdistance': '/fleurInput/calculationSetup/greensFunction/@minCalcDistance',
        'mindistance': '/fleurInput/calculationSetup/scfLoop/@minDistance',
        'mineigenval': '/fleurInput/output/chargeDensitySlicing/@minEigenval',
        'minenergy': '/fleurInput/output/bandDOS/@minEnergy',
        'minspindown': '/fleurInput/output/wannier/bandSelection/@minSpinDown',
        'minspinup': '/fleurInput/output/wannier/bandSelection/@minSpinUp',
        'minmatdistance': '/fleurInput/calculationSetup/ldaHIA/@minmatDistance',
        'minoccdistance': '/fleurInput/calculationSetup/ldaHIA/@minoccDistance',
        'mixparam': '/fleurInput/calculationSetup/ldaU/@mixParam',
        'mix_relaxweightoffd': '/fleurInput/calculationSetup/magnetism/mtNocoParams/@mix_RelaxWeightOffD',
        'mix_constr': '/fleurInput/calculationSetup/magnetism/mtNocoParams/@mix_constr',
        'mode': '/fleurInput/cell/bzIntegration/@mode',
        'ms': '/fleurInput/output/wannier/@ms',
        'n_occpm': '/fleurInput/calculationSetup/ldaHIA/@n_occpm',
        'name': '/fleurInput/calculationSetup/xcFunctional/@name',
        'ndvgrd': '/fleurInput/calculationSetup/xcFunctional/xcParams/@ndvgrd',
        'ne': '/fleurInput/calculationSetup/greensFunction/realAxis/@ne',
        'nnne': '/fleurInput/output/chargeDensitySlicing/@nnne',
        'nqphi': '/fleurInput/output/coreSpectrum/@nqphi',
        'nqr': '/fleurInput/output/coreSpectrum/@nqr',
        'nstars': '/fleurInput/output/vacuumDOS/@nstars',
        'nstm': '/fleurInput/output/vacuumDOS/@nstm',
        'numpoints': '/fleurInput/output/coreSpectrum/@numPoints',
        'numbands': '/fleurInput/calculationSetup/cutoffs/@numbands',
        'numberpoints': '/fleurInput/output/bandDOS/@numberPoints',
        'numkpt': '/fleurInput/output/chargeDensitySlicing/@numkpt',
        'occeps': '/fleurInput/calculationSetup/rdmft/@occEps',
        'off': '/fleurInput/calculationSetup/soc/@off',
        'orbcomp': '/fleurInput/output/bandDOS/@orbcomp',
        'outputsphavg': '/fleurInput/calculationSetup/greensFunction/@outputSphavg',
        'pallst': '/fleurInput/output/chargeDensitySlicing/@pallst',
        'plot_charge': '/fleurInput/calculationSetup/fields/@plot_charge',
        'plot_rho': '/fleurInput/calculationSetup/fields/@plot_rho',
        'polar': '/fleurInput/output/plotting/@polar',
        'pot8': '/fleurInput/calculationSetup/expertModes/@pot8',
        'precondparam': '/fleurInput/calculationSetup/scfLoop/@precondParam',
        'qfix': '/fleurInput/calculationSetup/geometryOptimization/@qfix',
        'qx': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qx',
        'qy': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qy',
        'qz': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qz',
        'relativisticcorrections': '/fleurInput/calculationSetup/xcFunctional/@relativisticCorrections',
        'rot': '/fleurInput/calculationSetup/oneDParams/@rot',
        'secvar': '/fleurInput/calculationSetup/expertModes/@secvar',
        'sgwf': '/fleurInput/output/wannier/@sgwf',
        'sig_b_1': '/fleurInput/calculationSetup/fields/@sig_b_1',
        'sig_b_2': '/fleurInput/calculationSetup/fields/@sig_b_2',
        'sigma': '/fleurInput/output/bandDOS/@sigma',
        'slice': '/fleurInput/output/@slice',
        'soc66': '/fleurInput/calculationSetup/soc/@soc66',
        'socgwf': '/fleurInput/output/wannier/@socgwf',
        'spav': '/fleurInput/calculationSetup/soc/@spav',
        'star': '/fleurInput/output/vacuumDOS/@star',
        'statesabove': '/fleurInput/calculationSetup/rdmft/@statesAbove',
        'statesbelow': '/fleurInput/calculationSetup/rdmft/@statesBelow',
        'supercellx': '/fleurInput/output/unfoldingBand/@supercellX',
        'supercelly': '/fleurInput/output/unfoldingBand/@supercellY',
        'supercellz': '/fleurInput/output/unfoldingBand/@supercellZ',
        'swsp': '/fleurInput/calculationSetup/magnetism/@swsp',
        'thetaj': '/fleurInput/forceTheorem/Jij/@thetaj',
        'tolerance': '/fleurInput/calculationSetup/prodBasis/@tolerance',
        'tworkf': '/fleurInput/output/vacuumDOS/@tworkf',
        'unfoldband': '/fleurInput/output/unfoldingBand/@unfoldBand',
        'vm': '/fleurInput/calculationSetup/oneDParams/@vM',
        'vacdos': '/fleurInput/output/vacuumDOS/@vacdos',
        'valenceelectrons': '/fleurInput/cell/bzIntegration/@valenceElectrons',
        'vchk': '/fleurInput/output/checks/@vchk',
        'verbose': '/fleurInput/output/coreSpectrum/@verbose',
        'wannier': '/fleurInput/output/@wannier',
        'warp_factor': '/fleurInput/calculationSetup/expertModes/@warp_factor',
        'zrfs1': '/fleurInput/calculationSetup/oneDParams/@zrfs1',
        'zsigma': '/fleurInput/calculationSetup/fields/@zsigma',
        'c': '/fleurInput/cell/bulkLattice/c',
        'comment': '/fleurInput/comment',
        'edgeindices': '/fleurInput/output/coreSpectrum/edgeIndices',
        'joblist': '/fleurInput/output/wannier/jobList',
        'qsc': '/fleurInput/calculationSetup/magnetism/qsc',
        'qss': '/fleurInput/calculationSetup/magnetism/qss'
    }),
    'unique_path_attribs':
    CaseInsensitiveDict({
        'correlation': [
            '/fleurInput/calculationSetup/xcFunctional/LibXCID/@correlation',
            '/fleurInput/calculationSetup/xcFunctional/LibXCName/@correlation'
        ],
        'eig66': ['/fleurInput/calculationSetup/expertModes/@eig66', '/fleurInput/output/@eig66'],
        'etot_correlation': [
            '/fleurInput/calculationSetup/xcFunctional/LibXCID/@etot_correlation',
            '/fleurInput/calculationSetup/xcFunctional/LibXCName/@etot_correlation'
        ],
        'etot_exchange': [
            '/fleurInput/calculationSetup/xcFunctional/LibXCID/@etot_exchange',
            '/fleurInput/calculationSetup/xcFunctional/LibXCName/@etot_exchange'
        ],
        'exchange': [
            '/fleurInput/calculationSetup/xcFunctional/LibXCID/@exchange',
            '/fleurInput/calculationSetup/xcFunctional/LibXCName/@exchange'
        ],
        'l_mperp': [
            '/fleurInput/calculationSetup/greensFunction/@l_mperp',
            '/fleurInput/calculationSetup/magnetism/mtNocoParams/@l_mperp'
        ],
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
