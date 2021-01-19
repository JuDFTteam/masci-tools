# -*- coding: utf-8 -*-
"""
This file contains information parsed from the FleurInputSchema.xsd
for version 0.34

The keys contain the following information:

    - 'inp_version': Version string of the input schema represented in this file
    - 'tag_paths': simple xpath expressions to all valid tag names
                   Multiple paths or ambiguous tag names are parsed as a list
    - 'basic_types': Parsed definitions of all simple Types with their respective
                     base type (int, float, ...) and evtl. length restrictions
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
__inp_version__ = '0.34'
schema_dict = {
    'attrib_types': {
        'Gmax': ['float_expression'],
        'GmaxXC': ['float_expression'],
        'I_initial': ['float'],
        'J': ['float_expression'],
        'Kmax': ['float_expression'],
        'M': ['float_expression'],
        'MM': ['int'],
        'TwoD': ['switch'],
        'U': ['float_expression'],
        'all_atoms': ['switch'],
        'alpha': ['float_expression', 'float'],
        'alpha_Ex': ['float'],
        'analytical_cont': ['switch'],
        'atomList': ['switch'],
        'atomType': ['int'],
        'atomicNumber': ['int'],
        'autocomp': ['switch'],
        'b_cons_x': ['float_expression'],
        'b_cons_y': ['float_expression'],
        'b_field': ['float_expression'],
        'b_field_mt': ['float_expression'],
        'band': ['switch'],
        'banddos': ['switch'],
        'bands': ['int'],
        'beta': ['float_expression', 'float'],
        'beta_Ex': ['float'],
        'bmt': ['switch'],
        'bsComf': ['switch'],
        'calculate': ['switch'],
        'cartesian': ['switch'],
        'cdinf': ['switch'],
        'chargeDensity': ['switch'],
        'chi': ['int'],
        'chng': ['float'],
        'coreSpec': ['switch'],
        'coretail_lmax': ['int'],
        'correlation': ['int', 'string'],
        'count': ['int'],
        'ctail': ['switch'],
        'd': ['switch', 'int'],
        'd1': ['switch'],
        'dTilda': ['float_expression'],
        'dVac': ['float_expression'],
        'dftspinpol': ['switch'],
        'dirichlet': ['switch'],
        'disp': ['switch'],
        'dos': ['switch'],
        'eDeriv': ['int'],
        'eKin': ['float'],
        'eMax': ['float'],
        'eMin': ['float'],
        'eV': ['switch'],
        'eb': ['float'],
        'edgeType': ['string'],
        'eig66': ['switch'],
        'element': ['string'],
        'ellow': ['float'],
        'elup': ['float'],
        'energy': ['float_expression'],
        'energyLo': ['float'],
        'energyUp': ['float'],
        'eonly': ['switch'],
        'epsdisp': ['float_expression'],
        'epsforce': ['float_expression'],
        'et': ['float'],
        'etot_correlation': ['int', 'string'],
        'etot_exchange': ['int', 'string'],
        'ewaldlambda': ['int'],
        'exchange': ['int', 'string'],
        'f': ['switch', 'int'],
        'f_level': ['int'],
        'fermiSmearingEnergy': ['float_expression'],
        'fermiSmearingTemp': ['float_expression'],
        'fftcut': ['float'],
        'file': ['string'],
        'fixed_moment': ['float_expression'],
        'fleurInputVersion': ['string'],
        'flipSpinPhi': ['float_expression'],
        'flipSpinScale': ['switch'],
        'flipSpinTheta': ['float_expression'],
        'force_converged': ['float_expression'],
        'forcealpha': ['float_expression'],
        'forcemix': ['string'],
        'form66': ['switch'],
        'format': ['int'],
        'frcor': ['switch'],
        'fullMatch': ['switch'],
        'functional': ['string'],
        'gamma': ['float_expression'],
        'gcutm': ['float'],
        'grid': ['string'],
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
        'init_mom': ['float', 'string'],
        'init_occ': ['float', 'string'],
        'intFullRadial': ['switch'],
        'integ': ['switch'],
        'invs1': ['switch'],
        'iplot': ['int'],
        'isec1': ['int'],
        'itmax': ['int'],
        'itmaxHubbard1': ['int'],
        'jDOS': ['switch'],
        'jspins': ['int'],
        'kcrel': ['int'],
        'key': ['string'],
        'kkintgrCutoff': ['float', 'string'],
        'l': ['int'],
        'l_J': ['switch'],
        'l_adjEnpara': ['switch'],
        'l_amf': ['switch'],
        'l_bloechl': ['switch'],
        'l_constrained': ['switch'],
        'l_core_confpot': ['switch'],
        'l_correctEtot': ['switch'],
        'l_eigout': ['switch'],
        'l_f': ['switch'],
        'l_fermi': ['switch'],
        'l_linMix': ['switch'],
        'l_magn': ['switch'],
        'l_mperp': ['switch'],
        'l_mtNocoPot': ['switch'],
        'l_noco': ['switch'],
        'l_nonsphDC': ['switch'],
        'l_onlyMtStDen': ['switch'],
        'l_potout': ['switch'],
        'l_rdmft': ['switch'],
        'l_relaxSQA': ['switch'],
        'l_resolvent': ['switch'],
        'l_scaleMag': ['switch'],
        'l_soc': ['switch'],
        'l_sourceFree': ['switch'],
        'l_sphavg': ['switch'],
        'l_ss': ['switch'],
        'label': ['string'],
        'lcutm': ['int'],
        'lcutwf': ['int'],
        'lda': ['switch'],
        'lexp': ['int'],
        'lflip': ['switch'],
        'listName': ['string'],
        'lmax': ['int'],
        'lmaxAPW': ['int'],
        'lnonsphr': ['int'],
        'locx1': ['float_expression'],
        'locx2': ['float_expression'],
        'locy1': ['float_expression'],
        'locy2': ['float_expression'],
        'logIncrement': ['float_expression'],
        'lpr': ['int'],
        'lwb': ['switch'],
        'm': ['int'],
        'm_cyl': ['int'],
        'magField': ['float'],
        'magMom': ['float_expression'],
        'mag_mixing_scheme': ['int'],
        'mag_scale': ['float_expression'],
        'maxEigenval': ['float_expression'],
        'maxEnergy': ['float_expression'],
        'maxIterBroyd': ['int'],
        'maxSpinDown': ['int'],
        'maxSpinUp': ['int'],
        'maxTimeToStartIter': ['float_expression'],
        'mcd': ['switch'],
        'minCalcDistance': ['float'],
        'minDistance': ['float_expression'],
        'minEigenval': ['float_expression'],
        'minEnergy': ['float_expression'],
        'minSpinDown': ['int'],
        'minSpinUp': ['int'],
        'minmatDistance': ['float'],
        'minoccDistance': ['float'],
        'mixParam': ['float'],
        'mix_RelaxWeightOffD': ['float_expression'],
        'mix_constr': ['float_expression'],
        'mode': ['string'],
        'ms': ['switch'],
        'n': ['int'],
        'n1': ['int'],
        'n2': ['int'],
        'n3': ['int'],
        'n_occpm': ['int'],
        'name': ['string'],
        'ndvgrd': ['int'],
        'ne': ['int'],
        'nkq_pairs': ['int'],
        'nmatsub': ['int'],
        'nnne': ['int'],
        'nqphi': ['int'],
        'nqr': ['int'],
        'nshells': ['int'],
        'nstars': ['int'],
        'nstm': ['int'],
        'numPoints': ['int'],
        'numbands': ['int', 'string'],
        'numberPoints': ['int'],
        'numkpt': ['int'],
        'nx': ['int'],
        'ny': ['int'],
        'nz': ['int'],
        'occEps': ['float'],
        'off': ['switch'],
        'onlyMT': ['switch'],
        'orbcomp': ['switch'],
        'outputSphavg': ['switch'],
        'p': ['switch', 'int'],
        'pallst': ['switch'],
        'phi': ['float_expression'],
        'plot_charge': ['switch'],
        'plot_rho': ['switch'],
        'polar': ['switch'],
        'pot8': ['switch'],
        'potential': ['switch'],
        'precondParam': ['float_expression'],
        'purpose': ['string'],
        'qfix': ['int'],
        'qx': ['int'],
        'qy': ['int'],
        'qz': ['int'],
        'radius': ['float_expression'],
        'relativisticCorrections': ['switch'],
        'relaxXYZ': ['string'],
        'remove4f': ['switch'],
        'rot': ['int'],
        's': ['switch', 'int'],
        'scale': ['float_expression'],
        'secvar': ['switch'],
        'select': ['string'],
        'sgwf': ['switch'],
        'sig_b_1': ['float_expression'],
        'sig_b_2': ['float_expression'],
        'sigma': ['float', 'float_expression'],
        'slice': ['switch'],
        'soc66': ['switch'],
        'socgwf': ['switch'],
        'socscale': ['float'],
        'spav': ['switch'],
        'species': ['string'],
        'spinDown': ['float_expression'],
        'spinUp': ['float_expression'],
        'spinf': ['float_expression', 'float'],
        'star': ['switch'],
        'state': ['string'],
        'statesAbove': ['int'],
        'statesBelow': ['int'],
        'supercellX': ['int'],
        'supercellY': ['int'],
        'supercellZ': ['int'],
        'swsp': ['switch'],
        'theta': ['float_expression'],
        'thetaj': ['float_expression'],
        'tolerance': ['float'],
        'tworkf': ['float_expression'],
        'type': ['string'],
        'typeMT': ['int'],
        'unfoldBand': ['switch'],
        'vM': ['int'],
        'vacdos': ['switch'],
        'vacuum': ['int'],
        'valenceElectrons': ['float_expression'],
        'value': ['float_expression', 'string'],
        'vcaAddCharge': ['float'],
        'vca_charge': ['float_expression'],
        'vchk': ['switch'],
        'vec1': ['string'],
        'vec2': ['string'],
        'vec3': ['string'],
        'vecField': ['switch'],
        'verbose': ['switch'],
        'wannier': ['switch'],
        'warp_factor': ['float_expression'],
        'weight': ['float_expression'],
        'zero': ['string'],
        'zrfs1': ['switch'],
        'zsigma': ['float_expression']
    },
    'basic_types': {
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
    'inp_version':
    '0.34',
    'omitt_contained_tags': [
        'constants', 'atomSpecies', 'atomGroups', 'symmetryOperations', 'kPointLists', 'displacements',
        'relaxation-history', 'spinSpiralDispersion', 'qVectors'
    ],
    'other_attribs': {
        'J': [
            '/fleurInput/atomSpecies/species/ldaU', '/fleurInput/atomGroups/atomGroup/ldaU',
            '/fleurInput/atomSpecies/species/ldaHIA', '/fleurInput/atomGroups/atomGroup/ldaHIA',
            '/fleurInput/atomSpecies/species/ldaHIA/exc', '/fleurInput/atomGroups/atomGroup/ldaHIA/exc'
        ],
        'M': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'TwoD': ['/fleurInput/output/plotting/plot'],
        'U': [
            '/fleurInput/atomSpecies/species/ldaU', '/fleurInput/atomGroups/atomGroup/ldaU',
            '/fleurInput/atomSpecies/species/ldaHIA', '/fleurInput/atomGroups/atomGroup/ldaHIA'
        ],
        'absPos': ['/fleurInput/atomGroups/atomGroup/absPos'],
        'alpha': [
            '/fleurInput/atomGroups/atomGroup/relPos', '/fleurInput/atomGroups/atomGroup/absPos',
            '/fleurInput/atomGroups/atomGroup/filmPos', '/fleurInput/atomSpecies/species/nocoParams',
            '/fleurInput/atomGroups/atomGroup/nocoParams',
            '/fleurInput/calculationSetup/greensFunction/contourSemicircle'
        ],
        'analytical_cont': ['/fleurInput/calculationSetup/greensFunction/contourDOS'],
        'atomicNumber': ['/fleurInput/atomSpecies/species'],
        'b_cons_x': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'b_cons_y': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'b_field_mt': ['/fleurInput/atomSpecies/species/special'],
        'banddos': [
            '/fleurInput/atomGroups/atomGroup/relPos', '/fleurInput/atomGroups/atomGroup/absPos',
            '/fleurInput/atomGroups/atomGroup/filmPos'
        ],
        'beta': [
            '/fleurInput/atomGroups/atomGroup/relPos', '/fleurInput/atomGroups/atomGroup/absPos',
            '/fleurInput/atomGroups/atomGroup/filmPos', '/fleurInput/atomSpecies/species/nocoParams',
            '/fleurInput/atomGroups/atomGroup/nocoParams'
        ],
        'calculate': ['/fleurInput/atomSpecies/species/force', '/fleurInput/atomGroups/atomGroup/force'],
        'cartesian': ['/fleurInput/output/plotting/plot'],
        'chargeDensity': ['/fleurInput/atomGroups/atomGroup/cFCoeffs'],
        'coreConfig': ['/fleurInput/atomSpecies/species/electronConfig/coreConfig'],
        'count': ['/fleurInput/cell/bzIntegration/kPointLists/kPointList'],
        'd': [
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements/d',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements/d',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/d',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements/d'
        ],
        'displace': ['/fleurInput/relaxation/displacements/displace'],
        'eDeriv': ['/fleurInput/atomSpecies/species/lo', '/fleurInput/atomGroups/atomGroup/lo'],
        'eb': [
            '/fleurInput/calculationSetup/greensFunction/contourRectangle',
            '/fleurInput/calculationSetup/greensFunction/contourSemicircle',
            '/fleurInput/calculationSetup/greensFunction/contourDOS'
        ],
        'element': ['/fleurInput/atomSpecies/species'],
        'energy': ['/fleurInput/relaxation/relaxation-history/step'],
        'et': [
            '/fleurInput/calculationSetup/greensFunction/contourSemicircle',
            '/fleurInput/calculationSetup/greensFunction/contourDOS'
        ],
        'f': [
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements/f',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements/f',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/f',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements/f'
        ],
        'file': ['/fleurInput/output/plotting/plot'],
        'filmPos': ['/fleurInput/atomGroups/atomGroup/filmPos'],
        'flipSpinPhi': ['/fleurInput/atomSpecies/species/modInitDen', '/fleurInput/atomGroups/atomGroup/modInitDen'],
        'flipSpinScale': ['/fleurInput/atomSpecies/species/modInitDen', '/fleurInput/atomGroups/atomGroup/modInitDen'],
        'flipSpinTheta': ['/fleurInput/atomSpecies/species/modInitDen', '/fleurInput/atomGroups/atomGroup/modInitDen'],
        'gamma': [
            '/fleurInput/atomGroups/atomGroup/relPos', '/fleurInput/atomGroups/atomGroup/absPos',
            '/fleurInput/atomGroups/atomGroup/filmPos'
        ],
        'grid': ['/fleurInput/output/plotting/plot'],
        'gridPoints': ['/fleurInput/atomSpecies/species/mtSphere', '/fleurInput/atomGroups/atomGroup/mtSphere'],
        'init_mom': ['/fleurInput/atomSpecies/species/ldaHIA/exc', '/fleurInput/atomGroups/atomGroup/ldaHIA/exc'],
        'init_occ': ['/fleurInput/atomSpecies/species/ldaHIA', '/fleurInput/atomGroups/atomGroup/ldaHIA'],
        'kPoint': ['/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint'],
        'key': ['/fleurInput/atomSpecies/species/ldaHIA/addArg', '/fleurInput/atomGroups/atomGroup/ldaHIA/addArg'],
        'kkintgrCutoff': [
            '/fleurInput/atomSpecies/species/ldaHIA', '/fleurInput/atomGroups/atomGroup/ldaHIA',
            '/fleurInput/atomSpecies/species/greensfCalculation', '/fleurInput/atomGroups/atomGroup/greensfCalculation',
            '/fleurInput/atomSpecies/species/torgueCalculation', '/fleurInput/atomGroups/atomGroup/torgueCalculation'
        ],
        'l': [
            '/fleurInput/atomSpecies/species/ldaU', '/fleurInput/atomGroups/atomGroup/ldaU',
            '/fleurInput/atomSpecies/species/ldaHIA', '/fleurInput/atomGroups/atomGroup/ldaHIA',
            '/fleurInput/atomSpecies/species/ldaHIA/exc', '/fleurInput/atomGroups/atomGroup/ldaHIA/exc',
            '/fleurInput/atomSpecies/species/ldaHIA/cFCoeff', '/fleurInput/atomGroups/atomGroup/ldaHIA/cFCoeff',
            '/fleurInput/atomSpecies/species/lo', '/fleurInput/atomGroups/atomGroup/lo'
        ],
        'l_amf': [
            '/fleurInput/atomSpecies/species/ldaU', '/fleurInput/atomGroups/atomGroup/ldaU',
            '/fleurInput/atomSpecies/species/ldaHIA', '/fleurInput/atomGroups/atomGroup/ldaHIA'
        ],
        'l_constrained': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'l_fermi': ['/fleurInput/calculationSetup/greensFunction/contourDOS'],
        'l_magn': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'l_mtNocoPot': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'l_relaxSQA': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'l_sphavg':
        ['/fleurInput/atomSpecies/species/greensfCalculation', '/fleurInput/atomGroups/atomGroup/greensfCalculation'],
        'label': [
            '/fleurInput/atomGroups/atomGroup/relPos', '/fleurInput/atomGroups/atomGroup/absPos',
            '/fleurInput/atomGroups/atomGroup/filmPos', '/fleurInput/atomSpecies/species/ldaHIA',
            '/fleurInput/atomGroups/atomGroup/ldaHIA', '/fleurInput/atomSpecies/species/greensfCalculation',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation', '/fleurInput/atomSpecies/species/torgueCalculation',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation',
            '/fleurInput/calculationSetup/greensFunction/contourRectangle',
            '/fleurInput/calculationSetup/greensFunction/contourSemicircle',
            '/fleurInput/calculationSetup/greensFunction/contourDOS',
            '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint'
        ],
        'layer': ['/fleurInput/output/vacuumDOS/layer'],
        'lcutm': ['/fleurInput/atomSpecies/species/prodBasis'],
        'lcutwf': ['/fleurInput/atomSpecies/species/prodBasis'],
        'lda': ['/fleurInput/atomSpecies/species/special'],
        'lmax': ['/fleurInput/atomSpecies/species/atomicCutoffs', '/fleurInput/atomGroups/atomGroup/atomicCutoffs'],
        'lmaxAPW': ['/fleurInput/atomSpecies/species/atomicCutoffs', '/fleurInput/atomGroups/atomGroup/atomicCutoffs'],
        'lnonsphr': ['/fleurInput/atomSpecies/species/atomicCutoffs', '/fleurInput/atomGroups/atomGroup/atomicCutoffs'],
        'logIncrement': ['/fleurInput/atomSpecies/species/mtSphere', '/fleurInput/atomGroups/atomGroup/mtSphere'],
        'm': ['/fleurInput/atomSpecies/species/ldaHIA/cFCoeff', '/fleurInput/atomGroups/atomGroup/ldaHIA/cFCoeff'],
        'magField': ['/fleurInput/atomGroups/atomGroup'],
        'magMom': ['/fleurInput/atomSpecies/species/modInitDen', '/fleurInput/atomGroups/atomGroup/modInitDen'],
        'n': [
            '/fleurInput/atomSpecies/species/lo', '/fleurInput/atomGroups/atomGroup/lo',
            '/fleurInput/calculationSetup/greensFunction/contourSemicircle',
            '/fleurInput/calculationSetup/greensFunction/contourDOS'
        ],
        'n1': ['/fleurInput/calculationSetup/greensFunction/contourRectangle'],
        'n2': ['/fleurInput/calculationSetup/greensFunction/contourRectangle'],
        'n3': ['/fleurInput/calculationSetup/greensFunction/contourRectangle'],
        'name': [
            '/fleurInput/constants/constant', '/fleurInput/atomSpecies/species',
            '/fleurInput/cell/bzIntegration/kPointLists/kPointList'
        ],
        'nkq_pairs': ['/fleurInput/cell/bzIntegration/kPointLists/kPointList'],
        'nmatsub': ['/fleurInput/calculationSetup/greensFunction/contourRectangle'],
        'nshells':
        ['/fleurInput/atomSpecies/species/greensfCalculation', '/fleurInput/atomGroups/atomGroup/greensfCalculation'],
        'nx': ['/fleurInput/cell/bzIntegration/kPointLists/kPointList'],
        'ny': ['/fleurInput/cell/bzIntegration/kPointLists/kPointList'],
        'nz': ['/fleurInput/cell/bzIntegration/kPointLists/kPointList'],
        'onlyMT': ['/fleurInput/output/plotting/plot'],
        'orbcomprot': ['/fleurInput/atomGroups/atomGroup/orbcomprot'],
        'p': [
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements/p',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements/p',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/p',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements/p'
        ],
        'phi': [
            '/fleurInput/atomSpecies/species/ldaU', '/fleurInput/atomGroups/atomGroup/ldaU',
            '/fleurInput/atomSpecies/species/ldaHIA', '/fleurInput/atomGroups/atomGroup/ldaHIA'
        ],
        'posforce': ['/fleurInput/relaxation/relaxation-history/step/posforce'],
        'potential': ['/fleurInput/atomGroups/atomGroup/cFCoeffs'],
        'q': [
            '/fleurInput/forceTheorem/spinSpiralDispersion/q', '/fleurInput/forceTheorem/DMI/qVectors/q',
            '/fleurInput/forceTheorem/Jij/qVectors/q'
        ],
        'radius': ['/fleurInput/atomSpecies/species/mtSphere', '/fleurInput/atomGroups/atomGroup/mtSphere'],
        'relPos': ['/fleurInput/atomGroups/atomGroup/relPos'],
        'relaxXYZ': ['/fleurInput/atomSpecies/species/force', '/fleurInput/atomGroups/atomGroup/force'],
        'remove4f': ['/fleurInput/atomGroups/atomGroup/cFCoeffs'],
        'row-1': ['/fleurInput/cell/symmetryOperations/symOp/row-1'],
        'row-2': ['/fleurInput/cell/symmetryOperations/symOp/row-2'],
        'row-3': ['/fleurInput/cell/symmetryOperations/symOp/row-3'],
        's': [
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements/s',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements/s',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/s',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements/s'
        ],
        'select': ['/fleurInput/atomSpecies/species/prodBasis'],
        'shape': ['/fleurInput/calculationSetup/fields/shape'],
        'sigma': [
            '/fleurInput/calculationSetup/greensFunction/contourRectangle',
            '/fleurInput/calculationSetup/greensFunction/contourDOS'
        ],
        'socscale': ['/fleurInput/atomSpecies/species/special'],
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
        'theta': [
            '/fleurInput/atomSpecies/species/ldaU', '/fleurInput/atomGroups/atomGroup/ldaU',
            '/fleurInput/atomSpecies/species/ldaHIA', '/fleurInput/atomGroups/atomGroup/ldaHIA'
        ],
        'type': [
            '/fleurInput/atomSpecies/species/lo', '/fleurInput/atomGroups/atomGroup/lo',
            '/fleurInput/cell/bzIntegration/kPointLists/kPointList'
        ],
        'typeMT': ['/fleurInput/output/plotting/plot'],
        'vacuum': ['/fleurInput/cell/filmLattice/vacuumEnergyParameters'],
        'valenceConfig': ['/fleurInput/atomSpecies/species/electronConfig/valenceConfig'],
        'value': [
            '/fleurInput/constants/constant', '/fleurInput/atomSpecies/species/ldaHIA/cFCoeff',
            '/fleurInput/atomGroups/atomGroup/ldaHIA/cFCoeff', '/fleurInput/atomSpecies/species/ldaHIA/addArg',
            '/fleurInput/atomGroups/atomGroup/ldaHIA/addArg'
        ],
        'vcaAddCharge': ['/fleurInput/atomGroups/atomGroup'],
        'vca_charge': ['/fleurInput/atomSpecies/species/special'],
        'vec1': ['/fleurInput/output/plotting/plot'],
        'vec2': ['/fleurInput/output/plotting/plot'],
        'vec3': ['/fleurInput/output/plotting/plot'],
        'vecField': ['/fleurInput/output/plotting/plot'],
        'wannier': [
            '/fleurInput/atomGroups/atomGroup/relPos', '/fleurInput/atomGroups/atomGroup/absPos',
            '/fleurInput/atomGroups/atomGroup/filmPos'
        ],
        'weight': ['/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint'],
        'zero': ['/fleurInput/output/plotting/plot']
    },
    'root_tag':
    'fleurInput',
    'simple_elements': {
        'a1': [{
            'length': 1,
            'type': ['float_expression']
        }],
        'a2': [{
            'length': 1,
            'type': ['float_expression']
        }],
        'absPos': [{
            'length': 3,
            'type': ['float_expression']
        }],
        'c': [{
            'length': 1,
            'type': ['float_expression']
        }],
        'comment': [{
            'length': 1,
            'type': ['string']
        }],
        'coreConfig': [{
            'length': 'unbounded',
            'type': ['string']
        }],
        'd': [{
            'length': 4,
            'type': ['switch']
        }],
        'displace': [{
            'length': 3,
            'type': ['float']
        }],
        'edgeIndices': [{
            'length': 'unbounded',
            'type': ['int']
        }],
        'f': [{
            'length': 4,
            'type': ['switch']
        }],
        'filmPos': [{
            'length': 3,
            'type': ['float_expression']
        }],
        'jobList': [{
            'length': 'unbounded',
            'type': ['string']
        }],
        'kPoint': [{
            'length': 3,
            'type': ['float_expression']
        }],
        'layer': [{
            'length': 1,
            'type': ['string']
        }],
        'orbcomprot': [{
            'length': 3,
            'type': ['float']
        }],
        'p': [{
            'length': 4,
            'type': ['switch']
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
            'type': ['float_expression']
        }],
        'qss': [{
            'length': 3,
            'type': ['float_expression']
        }],
        'relPos': [{
            'length': 3,
            'type': ['float_expression']
        }],
        'row-1': [{
            'length': 2,
            'type': ['float_expression']
        }, {
            'length': 3,
            'type': ['float_expression']
        }, {
            'length': 4,
            'type': ['float']
        }],
        'row-2': [{
            'length': 2,
            'type': ['float_expression']
        }, {
            'length': 3,
            'type': ['float_expression']
        }, {
            'length': 4,
            'type': ['float']
        }],
        'row-3': [{
            'length': 3,
            'type': ['float_expression']
        }, {
            'length': 4,
            'type': ['float']
        }],
        's': [{
            'length': 4,
            'type': ['switch']
        }],
        'shape': [{
            'length': 1,
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
                'comment', 'constants', 'calculationSetup', 'cell', 'atomSpecies', 'atomGroups', 'output',
                'forceTheorem', 'relaxation'
            ],
            'several': [],
            'simple': ['comment', 'calculationSetup', 'output', 'relaxation'],
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
            'optional': [
                'mtSphere', 'atomicCutoffs', 'energyParameters', 'force', 'nocoParams', 'modInitDen', 'ldaU', 'ldaHIA',
                'greensfCalculation', 'torgueCalculation', 'lo', 'orbcomprot', 'cFCoeffs'
            ],
            'optional_attribs': ['magField', 'vcaAddCharge'],
            'order': [
                'relPos', 'absPos', 'filmPos', 'mtSphere', 'atomicCutoffs', 'energyParameters', 'force', 'nocoParams',
                'modInitDen', 'ldaU', 'ldaHIA', 'greensfCalculation', 'torgueCalculation', 'lo', 'orbcomprot',
                'cFCoeffs'
            ],
            'several': ['relPos', 'absPos', 'filmPos', 'ldaU', 'ldaHIA', 'greensfCalculation', 'lo'],
            'simple': [
                'relPos', 'absPos', 'filmPos', 'mtSphere', 'atomicCutoffs', 'energyParameters', 'force', 'nocoParams',
                'modInitDen', 'ldaU', 'lo', 'orbcomprot', 'cFCoeffs'
            ],
            'text': ['relPos', 'absPos', 'filmPos', 'orbcomprot']
        },
        '/fleurInput/atomGroups/atomGroup/absPos': {
            'attribs': ['label', 'wannier', 'banddos', 'alpha', 'beta', 'gamma'],
            'optional': [],
            'optional_attribs': ['label', 'wannier', 'banddos', 'alpha', 'beta', 'gamma'],
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
        '/fleurInput/atomGroups/atomGroup/cFCoeffs': {
            'attribs': ['chargeDensity', 'potential', 'remove4f'],
            'optional': [],
            'optional_attribs': ['remove4f'],
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
            'attribs': ['label', 'wannier', 'banddos', 'alpha', 'beta', 'gamma'],
            'optional': [],
            'optional_attribs': ['label', 'wannier', 'banddos', 'alpha', 'beta', 'gamma'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/force': {
            'attribs': ['calculate', 'relaxXYZ'],
            'optional': [],
            'optional_attribs': ['relaxXYZ'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/greensfCalculation': {
            'attribs': ['l_sphavg', 'nshells', 'kkintgrCutoff', 'label'],
            'optional': [],
            'optional_attribs': ['nshells', 'kkintgrCutoff', 'label'],
            'order': ['matrixElements', 'diagElements'],
            'several': [],
            'simple': ['diagElements'],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/greensfCalculation/diagElements': {
            'attribs': ['s', 'p', 'd', 'f'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['s', 'p', 'd', 'f'],
            'several': [],
            'simple': ['s', 'p', 'd', 'f'],
            'text': ['s', 'p', 'd', 'f']
        },
        '/fleurInput/atomGroups/atomGroup/ldaHIA': {
            'attribs': ['l', 'U', 'J', 'phi', 'theta', 'l_amf', 'init_occ', 'kkintgrCutoff', 'label'],
            'optional': ['exc', 'cFCoeff', 'addArg'],
            'optional_attribs': ['phi', 'theta', 'init_occ', 'kkintgrCutoff', 'label'],
            'order': ['exc', 'cFCoeff', 'addArg'],
            'several': ['exc', 'cFCoeff', 'addArg'],
            'simple': ['exc', 'cFCoeff', 'addArg'],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/ldaHIA/addArg': {
            'attribs': ['key', 'value'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/ldaHIA/cFCoeff': {
            'attribs': ['l', 'm', 'value'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/ldaHIA/exc': {
            'attribs': ['l', 'J', 'init_mom'],
            'optional': [],
            'optional_attribs': ['init_mom'],
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
        '/fleurInput/atomGroups/atomGroup/modInitDen': {
            'attribs': ['magMom', 'flipSpinPhi', 'flipSpinTheta', 'flipSpinScale'],
            'optional': [],
            'optional_attribs': ['magMom', 'flipSpinPhi', 'flipSpinTheta', 'flipSpinScale'],
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
            'attribs':
            ['l_constrained', 'l_mtNocoPot', 'l_relaxSQA', 'l_magn', 'M', 'alpha', 'beta', 'b_cons_x', 'b_cons_y'],
            'optional': [],
            'optional_attribs': ['l_constrained', 'l_mtNocoPot', 'l_relaxSQA', 'l_magn', 'M', 'b_cons_x', 'b_cons_y'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/relPos': {
            'attribs': ['label', 'wannier', 'banddos', 'alpha', 'beta', 'gamma'],
            'optional': [],
            'optional_attribs': ['label', 'wannier', 'banddos', 'alpha', 'beta', 'gamma'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/torgueCalculation': {
            'attribs': ['kkintgrCutoff', 'label'],
            'optional': [],
            'optional_attribs': ['kkintgrCutoff', 'label'],
            'order': ['greensfElements'],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['s', 'p', 'd', 'f'],
            'several': [],
            'simple': ['s', 'p', 'd', 'f'],
            'text': ['s', 'p', 'd', 'f']
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
            'attribs': ['name', 'element', 'atomicNumber'],
            'optional': [
                'energyParameters', 'prodBasis', 'special', 'force', 'nocoParams', 'modInitDen', 'ldaU', 'ldaHIA',
                'greensfCalculation', 'torgueCalculation', 'lo'
            ],
            'optional_attribs': ['element'],
            'order': [
                'mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'prodBasis', 'special', 'force',
                'nocoParams', 'modInitDen', 'ldaU', 'ldaHIA', 'greensfCalculation', 'torgueCalculation', 'lo'
            ],
            'several': ['ldaU', 'ldaHIA', 'greensfCalculation', 'lo'],
            'simple': [
                'mtSphere', 'atomicCutoffs', 'energyParameters', 'prodBasis', 'special', 'force', 'nocoParams',
                'modInitDen', 'ldaU', 'lo'
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
            'optional_attribs': ['relaxXYZ'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/greensfCalculation': {
            'attribs': ['l_sphavg', 'nshells', 'kkintgrCutoff', 'label'],
            'optional': [],
            'optional_attribs': ['nshells', 'kkintgrCutoff', 'label'],
            'order': ['matrixElements', 'diagElements'],
            'several': [],
            'simple': ['diagElements'],
            'text': []
        },
        '/fleurInput/atomSpecies/species/greensfCalculation/diagElements': {
            'attribs': ['s', 'p', 'd', 'f'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['s', 'p', 'd', 'f'],
            'several': [],
            'simple': ['s', 'p', 'd', 'f'],
            'text': ['s', 'p', 'd', 'f']
        },
        '/fleurInput/atomSpecies/species/ldaHIA': {
            'attribs': ['l', 'U', 'J', 'phi', 'theta', 'l_amf', 'init_occ', 'kkintgrCutoff', 'label'],
            'optional': ['exc', 'cFCoeff', 'addArg'],
            'optional_attribs': ['phi', 'theta', 'init_occ', 'kkintgrCutoff', 'label'],
            'order': ['exc', 'cFCoeff', 'addArg'],
            'several': ['exc', 'cFCoeff', 'addArg'],
            'simple': ['exc', 'cFCoeff', 'addArg'],
            'text': []
        },
        '/fleurInput/atomSpecies/species/ldaHIA/addArg': {
            'attribs': ['key', 'value'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/ldaHIA/cFCoeff': {
            'attribs': ['l', 'm', 'value'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/ldaHIA/exc': {
            'attribs': ['l', 'J', 'init_mom'],
            'optional': [],
            'optional_attribs': ['init_mom'],
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
        '/fleurInput/atomSpecies/species/modInitDen': {
            'attribs': ['magMom', 'flipSpinPhi', 'flipSpinTheta', 'flipSpinScale'],
            'optional': [],
            'optional_attribs': ['magMom', 'flipSpinPhi', 'flipSpinTheta', 'flipSpinScale'],
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
            'attribs':
            ['l_constrained', 'l_mtNocoPot', 'l_relaxSQA', 'l_magn', 'M', 'alpha', 'beta', 'b_cons_x', 'b_cons_y'],
            'optional': [],
            'optional_attribs': ['l_constrained', 'l_mtNocoPot', 'l_relaxSQA', 'l_magn', 'M', 'b_cons_x', 'b_cons_y'],
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
        '/fleurInput/atomSpecies/species/torgueCalculation': {
            'attribs': ['kkintgrCutoff', 'label'],
            'optional': [],
            'optional_attribs': ['kkintgrCutoff', 'label'],
            'order': ['greensfElements'],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['s', 'p', 'd', 'f'],
            'several': [],
            'simple': ['s', 'p', 'd', 'f'],
            'text': ['s', 'p', 'd', 'f']
        },
        '/fleurInput/calculationSetup': {
            'attribs': [],
            'optional': [
                'prodBasis', 'soc', 'oneDParams', 'expertModes', 'geometryOptimization', 'ldaU', 'ldaHIA',
                'greensFunction', 'rdmft', 'spinSpiralQPointMesh', 'fields'
            ],
            'optional_attribs': [],
            'order': [
                'cutoffs', 'scfLoop', 'coreElectrons', 'xcFunctional', 'magnetism', 'prodBasis', 'soc', 'oneDParams',
                'expertModes', 'geometryOptimization', 'ldaU', 'ldaHIA', 'greensFunction', 'rdmft',
                'spinSpiralQPointMesh', 'fields'
            ],
            'several': [],
            'simple': [
                'cutoffs', 'scfLoop', 'coreElectrons', 'magnetism', 'prodBasis', 'soc', 'oneDParams', 'expertModes',
                'geometryOptimization', 'ldaU', 'ldaHIA', 'rdmft', 'spinSpiralQPointMesh'
            ],
            'text': []
        },
        '/fleurInput/calculationSetup/coreElectrons': {
            'attribs': ['ctail', 'frcor', 'kcrel', 'coretail_lmax', 'l_core_confpot'],
            'optional': [],
            'optional_attribs': ['frcor', 'kcrel', 'coretail_lmax', 'l_core_confpot'],
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
        '/fleurInput/calculationSetup/expertModes': {
            'attribs': ['gw', 'pot8', 'eig66', 'lpr', 'isec1', 'secvar', 'warp_factor'],
            'optional': [],
            'optional_attribs': ['gw', 'pot8', 'eig66', 'lpr', 'isec1', 'secvar', 'warp_factor'],
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
            'attribs': ['l_f', 'f_level', 'forcealpha', 'epsdisp', 'epsforce', 'forcemix', 'qfix', 'force_converged'],
            'optional': [],
            'optional_attribs': ['f_level', 'forcealpha', 'epsdisp', 'epsforce', 'forcemix', 'qfix', 'force_converged'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/greensFunction': {
            'attribs': ['l_mperp', 'l_resolvent', 'minCalcDistance', 'outputSphavg', 'intFullRadial'],
            'optional': [],
            'optional_attribs': ['l_mperp', 'l_resolvent', 'minCalcDistance', 'outputSphavg', 'intFullRadial'],
            'order': ['realAxis', 'contourRectangle', 'contourSemicircle', 'contourDOS'],
            'several': ['contourRectangle', 'contourSemicircle', 'contourDOS'],
            'simple': ['realAxis', 'contourRectangle', 'contourSemicircle', 'contourDOS'],
            'text': []
        },
        '/fleurInput/calculationSetup/greensFunction/contourDOS': {
            'attribs': ['n', 'sigma', 'eb', 'et', 'analytical_cont', 'l_fermi', 'label'],
            'optional': [],
            'optional_attribs': ['label'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/greensFunction/contourRectangle': {
            'attribs': ['n1', 'n2', 'n3', 'nmatsub', 'sigma', 'eb', 'label'],
            'optional': [],
            'optional_attribs': ['label'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/greensFunction/contourSemicircle': {
            'attribs': ['n', 'eb', 'et', 'alpha', 'label'],
            'optional': [],
            'optional_attribs': ['label'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/greensFunction/realAxis': {
            'attribs': ['ne', 'ellow', 'elup'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/ldaHIA': {
            'attribs': [
                'itmaxHubbard1', 'beta', 'minoccDistance', 'minmatDistance', 'n_occpm', 'dftspinpol', 'fullMatch',
                'l_nonsphDC', 'l_correctEtot'
            ],
            'optional': [],
            'optional_attribs': [
                'beta', 'minoccDistance', 'minmatDistance', 'n_occpm', 'dftspinpol', 'fullMatch', 'l_nonsphDC',
                'l_correctEtot'
            ],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/ldaU': {
            'attribs': ['l_linMix', 'mixParam', 'spinf', 'l_adjEnpara'],
            'optional': [],
            'optional_attribs': ['l_linMix', 'mixParam', 'spinf', 'l_adjEnpara'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/magnetism': {
            'attribs': ['jspins', 'l_noco', 'l_ss', 'l_J', 'swsp', 'lflip', 'l_onlyMtStDen', 'fixed_moment'],
            'optional': ['qss', 'qsc', 'mtNocoParams', 'sourceFreeMag'],
            'optional_attribs': ['l_noco', 'l_ss', 'l_J', 'swsp', 'lflip', 'l_onlyMtStDen', 'fixed_moment'],
            'order': ['qss', 'qsc', 'mtNocoParams', 'sourceFreeMag'],
            'several': [],
            'simple': ['qss', 'qsc', 'mtNocoParams', 'sourceFreeMag'],
            'text': ['qss', 'qsc']
        },
        '/fleurInput/calculationSetup/magnetism/mtNocoParams': {
            'attribs': [
                'l_mtNocoPot', 'l_mperp', 'l_constrained', 'l_relaxSQA', 'mag_mixing_scheme', 'mix_RelaxWeightOffD',
                'mix_constr'
            ],
            'optional': [],
            'optional_attribs': [
                'l_mtNocoPot', 'l_mperp', 'l_constrained', 'l_relaxSQA', 'mag_mixing_scheme', 'mix_RelaxWeightOffD',
                'mix_constr'
            ],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/magnetism/sourceFreeMag': {
            'attribs': ['l_sourceFree', 'l_scaleMag', 'mag_scale'],
            'optional': [],
            'optional_attribs': ['l_sourceFree', 'l_scaleMag', 'mag_scale'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
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
            'attribs': ['gcutm', 'bands', 'tolerance', 'lexp', 'ewaldlambda', 'fftcut'],
            'optional': [],
            'optional_attribs': ['tolerance', 'lexp', 'ewaldlambda', 'fftcut'],
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
            'optional_attribs': ['spav', 'off', 'soc66'],
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
        '/fleurInput/calculationSetup/xcFunctional': {
            'attribs': ['name', 'relativisticCorrections'],
            'optional': ['LibXCID', 'LibXCName', 'xcParams', 'ggaPrinting'],
            'optional_attribs': ['relativisticCorrections'],
            'order': ['LibXCID', 'LibXCName', 'xcParams', 'ggaPrinting'],
            'several': [],
            'simple': ['LibXCID', 'LibXCName', 'xcParams', 'ggaPrinting'],
            'text': []
        },
        '/fleurInput/calculationSetup/xcFunctional/LibXCID': {
            'attribs': ['exchange', 'correlation', 'etot_exchange', 'etot_correlation'],
            'optional': [],
            'optional_attribs': ['etot_exchange', 'etot_correlation'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/xcFunctional/LibXCName': {
            'attribs': ['exchange', 'correlation', 'etot_exchange', 'etot_correlation'],
            'optional': [],
            'optional_attribs': ['etot_exchange', 'etot_correlation'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/xcFunctional/ggaPrinting': {
            'attribs': ['iggachk', 'idsprs0', 'idsprsl', 'idsprsi', 'idsprsv'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/xcFunctional/xcParams': {
            'attribs': ['igrd', 'lwb', 'ndvgrd', 'idsprs', 'chng'],
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
            'order': ['bzIntegration', 'symmetryOperations', 'bulkLattice', 'filmLattice'],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/bulkLattice': {
            'attribs': ['scale'],
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
        '/fleurInput/cell/bzIntegration': {
            'attribs': ['valenceElectrons', 'mode', 'fermiSmearingEnergy', 'fermiSmearingTemp', 'l_bloechl'],
            'optional': [],
            'optional_attribs': ['valenceElectrons', 'mode', 'fermiSmearingEnergy', 'fermiSmearingTemp', 'l_bloechl'],
            'order': ['kPointListSelection', 'kPointLists'],
            'several': [],
            'simple': ['kPointListSelection'],
            'text': []
        },
        '/fleurInput/cell/bzIntegration/kPointListSelection': {
            'attribs': ['listName'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/bzIntegration/kPointLists': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['kPointList'],
            'several': ['kPointList'],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/bzIntegration/kPointLists/kPointList': {
            'attribs': ['name', 'type', 'count', 'nx', 'ny', 'nz', 'nkq_pairs'],
            'optional': [],
            'optional_attribs': ['type', 'count', 'nx', 'ny', 'nz', 'nkq_pairs'],
            'order': ['kPoint'],
            'several': ['kPoint'],
            'simple': ['kPoint'],
            'text': ['kPoint']
        },
        '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint': {
            'attribs': ['weight', 'label'],
            'optional': [],
            'optional_attribs': ['label'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/cell/filmLattice': {
            'attribs': ['scale', 'dVac', 'dTilda'],
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
            'simple': ['MAE', 'DMI', 'Jij'],
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
            'attribs': ['dos', 'band', 'slice', 'coreSpec', 'wannier', 'eig66'],
            'optional': [
                'checks', 'bandDOS', 'vacuumDOS', 'plotting', 'chargeDensitySlicing', 'specialOutput', 'coreSpectrum',
                'wannier', 'magneticCircularDichroism', 'unfoldingBand', 'juPhon'
            ],
            'optional_attribs': ['dos', 'band', 'slice', 'coreSpec', 'wannier', 'eig66'],
            'order': [
                'checks', 'bandDOS', 'vacuumDOS', 'plotting', 'chargeDensitySlicing', 'specialOutput', 'coreSpectrum',
                'wannier', 'magneticCircularDichroism', 'unfoldingBand', 'juPhon'
            ],
            'several': [],
            'simple': [
                'checks', 'bandDOS', 'chargeDensitySlicing', 'specialOutput', 'wannier', 'magneticCircularDichroism',
                'unfoldingBand', 'juPhon'
            ],
            'text': []
        },
        '/fleurInput/output/bandDOS': {
            'attribs': ['all_atoms', 'orbcomp', 'jDOS', 'minEnergy', 'maxEnergy', 'sigma', 'numberPoints'],
            'optional': [],
            'optional_attribs': ['all_atoms', 'orbcomp', 'jDOS', 'minEnergy', 'maxEnergy', 'sigma', 'numberPoints'],
            'order': [],
            'several': [],
            'simple': [],
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
        '/fleurInput/output/juPhon': {
            'attribs': ['l_potout', 'l_eigout'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/magneticCircularDichroism': {
            'attribs': ['mcd', 'energyLo', 'energyUp'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/output/plotting': {
            'attribs': ['iplot', 'polar', 'format'],
            'optional': ['plot'],
            'optional_attribs': ['iplot', 'polar', 'format'],
            'order': ['plot'],
            'several': ['plot'],
            'simple': ['plot'],
            'text': []
        },
        '/fleurInput/output/plotting/plot': {
            'attribs':
            ['cartesian', 'TwoD', 'grid', 'vec1', 'vec2', 'vec3', 'zero', 'file', 'onlyMT', 'typeMT', 'vecField'],
            'optional': [],
            'optional_attribs':
            ['cartesian', 'TwoD', 'grid', 'vec1', 'vec2', 'vec3', 'zero', 'file', 'onlyMT', 'typeMT', 'vecField'],
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
            'attribs': ['vacdos', 'integ', 'star', 'nstars', 'locx1', 'locy1', 'locx2', 'locy2', 'nstm', 'tworkf'],
            'optional': ['layer'],
            'optional_attribs': ['integ', 'star', 'nstars', 'locx1', 'locy1', 'locx2', 'locy2', 'nstm', 'tworkf'],
            'order': ['layer'],
            'several': ['layer'],
            'simple': ['layer'],
            'text': ['layer']
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
        }
    },
    'tag_paths': {
        'DMI':
        '/fleurInput/forceTheorem/DMI',
        'Jij':
        '/fleurInput/forceTheorem/Jij',
        'LibXCID':
        '/fleurInput/calculationSetup/xcFunctional/LibXCID',
        'LibXCName':
        '/fleurInput/calculationSetup/xcFunctional/LibXCName',
        'MAE':
        '/fleurInput/forceTheorem/MAE',
        'a1': ['/fleurInput/cell/bulkLattice/a1', '/fleurInput/cell/filmLattice/a1'],
        'a2': ['/fleurInput/cell/bulkLattice/a2', '/fleurInput/cell/filmLattice/a2'],
        'absPos':
        '/fleurInput/atomGroups/atomGroup/absPos',
        'addArg': ['/fleurInput/atomSpecies/species/ldaHIA/addArg', '/fleurInput/atomGroups/atomGroup/ldaHIA/addArg'],
        'atomGroup':
        '/fleurInput/atomGroups/atomGroup',
        'atomGroups':
        '/fleurInput/atomGroups',
        'atomSpecies':
        '/fleurInput/atomSpecies',
        'atomicCutoffs':
        ['/fleurInput/atomSpecies/species/atomicCutoffs', '/fleurInput/atomGroups/atomGroup/atomicCutoffs'],
        'bandDOS':
        '/fleurInput/output/bandDOS',
        'bandSelection':
        '/fleurInput/output/wannier/bandSelection',
        'bravaisMatrix': ['/fleurInput/cell/bulkLattice/bravaisMatrix', '/fleurInput/cell/filmLattice/bravaisMatrix'],
        'bulkLattice':
        '/fleurInput/cell/bulkLattice',
        'bzIntegration':
        '/fleurInput/cell/bzIntegration',
        'c':
        '/fleurInput/cell/bulkLattice/c',
        'cFCoeff':
        ['/fleurInput/atomSpecies/species/ldaHIA/cFCoeff', '/fleurInput/atomGroups/atomGroup/ldaHIA/cFCoeff'],
        'cFCoeffs':
        '/fleurInput/atomGroups/atomGroup/cFCoeffs',
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
        'contourDOS':
        '/fleurInput/calculationSetup/greensFunction/contourDOS',
        'contourRectangle':
        '/fleurInput/calculationSetup/greensFunction/contourRectangle',
        'contourSemicircle':
        '/fleurInput/calculationSetup/greensFunction/contourSemicircle',
        'coreConfig':
        '/fleurInput/atomSpecies/species/electronConfig/coreConfig',
        'coreElectrons':
        '/fleurInput/calculationSetup/coreElectrons',
        'coreSpectrum':
        '/fleurInput/output/coreSpectrum',
        'cutoffs':
        '/fleurInput/calculationSetup/cutoffs',
        'd': [
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements/d',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements/d',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/d',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements/d'
        ],
        'diagElements': [
            '/fleurInput/atomSpecies/species/greensfCalculation/diagElements',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/diagElements'
        ],
        'displace':
        '/fleurInput/relaxation/displacements/displace',
        'displacements':
        '/fleurInput/relaxation/displacements',
        'edgeIndices':
        '/fleurInput/output/coreSpectrum/edgeIndices',
        'electronConfig':
        '/fleurInput/atomSpecies/species/electronConfig',
        'energyParameters':
        ['/fleurInput/atomSpecies/species/energyParameters', '/fleurInput/atomGroups/atomGroup/energyParameters'],
        'exc': ['/fleurInput/atomSpecies/species/ldaHIA/exc', '/fleurInput/atomGroups/atomGroup/ldaHIA/exc'],
        'expertModes':
        '/fleurInput/calculationSetup/expertModes',
        'f': [
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements/f',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements/f',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/f',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements/f'
        ],
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
        '/fleurInput/calculationSetup/xcFunctional/ggaPrinting',
        'greensFunction':
        '/fleurInput/calculationSetup/greensFunction',
        'greensfCalculation':
        ['/fleurInput/atomSpecies/species/greensfCalculation', '/fleurInput/atomGroups/atomGroup/greensfCalculation'],
        'greensfElements': [
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements'
        ],
        'jobList':
        '/fleurInput/output/wannier/jobList',
        'juPhon':
        '/fleurInput/output/juPhon',
        'kPoint':
        '/fleurInput/cell/bzIntegration/kPointLists/kPointList/kPoint',
        'kPointList':
        '/fleurInput/cell/bzIntegration/kPointLists/kPointList',
        'kPointListSelection':
        '/fleurInput/cell/bzIntegration/kPointListSelection',
        'kPointLists':
        '/fleurInput/cell/bzIntegration/kPointLists',
        'layer':
        '/fleurInput/output/vacuumDOS/layer',
        'ldaHIA': [
            '/fleurInput/calculationSetup/ldaHIA', '/fleurInput/atomSpecies/species/ldaHIA',
            '/fleurInput/atomGroups/atomGroup/ldaHIA'
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
        'matrixElements': [
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements'
        ],
        'modInitDen': ['/fleurInput/atomSpecies/species/modInitDen', '/fleurInput/atomGroups/atomGroup/modInitDen'],
        'mtNocoParams':
        '/fleurInput/calculationSetup/magnetism/mtNocoParams',
        'mtSphere': ['/fleurInput/atomSpecies/species/mtSphere', '/fleurInput/atomGroups/atomGroup/mtSphere'],
        'nocoParams': ['/fleurInput/atomSpecies/species/nocoParams', '/fleurInput/atomGroups/atomGroup/nocoParams'],
        'oneDParams':
        '/fleurInput/calculationSetup/oneDParams',
        'orbcomprot':
        '/fleurInput/atomGroups/atomGroup/orbcomprot',
        'output':
        '/fleurInput/output',
        'p': [
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements/p',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements/p',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/p',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements/p'
        ],
        'plot':
        '/fleurInput/output/plotting/plot',
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
        '/fleurInput/calculationSetup/magnetism/qsc',
        'qss':
        '/fleurInput/calculationSetup/magnetism/qss',
        'rdmft':
        '/fleurInput/calculationSetup/rdmft',
        'realAxis':
        '/fleurInput/calculationSetup/greensFunction/realAxis',
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
        's': [
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements/s',
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements/s',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements/s',
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements/s'
        ],
        'scfLoop':
        '/fleurInput/calculationSetup/scfLoop',
        'shape':
        '/fleurInput/calculationSetup/fields/shape',
        'soc':
        '/fleurInput/calculationSetup/soc',
        'sourceFreeMag':
        '/fleurInput/calculationSetup/magnetism/sourceFreeMag',
        'special':
        '/fleurInput/atomSpecies/species/special',
        'specialOutput':
        '/fleurInput/output/specialOutput',
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
        'symmetryOperations':
        '/fleurInput/cell/symmetryOperations',
        'torgueCalculation':
        ['/fleurInput/atomSpecies/species/torgueCalculation', '/fleurInput/atomGroups/atomGroup/torgueCalculation'],
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
        '/fleurInput/calculationSetup/xcFunctional',
        'xcParams':
        '/fleurInput/calculationSetup/xcFunctional/xcParams'
    },
    'unique_attribs': {
        'Gmax': '/fleurInput/calculationSetup/cutoffs',
        'GmaxXC': '/fleurInput/calculationSetup/cutoffs',
        'I_initial': '/fleurInput/output/coreSpectrum',
        'Kmax': '/fleurInput/calculationSetup/cutoffs',
        'MM': '/fleurInput/calculationSetup/oneDParams',
        'all_atoms': '/fleurInput/output/bandDOS',
        'alpha': '/fleurInput/calculationSetup/scfLoop',
        'alpha_Ex': '/fleurInput/output/coreSpectrum',
        'atomList': '/fleurInput/output/wannier',
        'atomType': '/fleurInput/output/coreSpectrum',
        'autocomp': '/fleurInput/calculationSetup/fields',
        'b_field': '/fleurInput/calculationSetup/fields',
        'band': '/fleurInput/output',
        'bands': '/fleurInput/calculationSetup/prodBasis',
        'beta': '/fleurInput/calculationSetup/ldaHIA',
        'beta_Ex': '/fleurInput/output/coreSpectrum',
        'bmt': '/fleurInput/output/specialOutput',
        'bsComf': '/fleurInput/output/wannier',
        'c': '/fleurInput/cell/bulkLattice/c',
        'cdinf': '/fleurInput/output/checks',
        'chi': '/fleurInput/calculationSetup/oneDParams',
        'chng': '/fleurInput/calculationSetup/xcFunctional/xcParams',
        'comment': '/fleurInput/comment',
        'coreSpec': '/fleurInput/output',
        'coretail_lmax': '/fleurInput/calculationSetup/coreElectrons',
        'ctail': '/fleurInput/calculationSetup/coreElectrons',
        'd1': '/fleurInput/calculationSetup/oneDParams',
        'dTilda': '/fleurInput/cell/filmLattice',
        'dVac': '/fleurInput/cell/filmLattice',
        'dftspinpol': '/fleurInput/calculationSetup/ldaHIA',
        'dirichlet': '/fleurInput/calculationSetup/fields',
        'disp': '/fleurInput/output/checks',
        'dos': '/fleurInput/output',
        'eKin': '/fleurInput/output/coreSpectrum',
        'eMax': '/fleurInput/output/coreSpectrum',
        'eMin': '/fleurInput/output/coreSpectrum',
        'eV': '/fleurInput/calculationSetup/fields',
        'edgeIndices': '/fleurInput/output/coreSpectrum/edgeIndices',
        'edgeType': '/fleurInput/output/coreSpectrum',
        'ellow': '/fleurInput/calculationSetup/greensFunction/realAxis',
        'elup': '/fleurInput/calculationSetup/greensFunction/realAxis',
        'energyLo': '/fleurInput/output/magneticCircularDichroism',
        'energyUp': '/fleurInput/output/magneticCircularDichroism',
        'eonly': '/fleurInput/output/specialOutput',
        'epsdisp': '/fleurInput/calculationSetup/geometryOptimization',
        'epsforce': '/fleurInput/calculationSetup/geometryOptimization',
        'ewaldlambda': '/fleurInput/calculationSetup/prodBasis',
        'f_level': '/fleurInput/calculationSetup/geometryOptimization',
        'fermiSmearingEnergy': '/fleurInput/cell/bzIntegration',
        'fermiSmearingTemp': '/fleurInput/cell/bzIntegration',
        'fftcut': '/fleurInput/calculationSetup/prodBasis',
        'fixed_moment': '/fleurInput/calculationSetup/magnetism',
        'fleurInputVersion': '/fleurInput',
        'force_converged': '/fleurInput/calculationSetup/geometryOptimization',
        'forcealpha': '/fleurInput/calculationSetup/geometryOptimization',
        'forcemix': '/fleurInput/calculationSetup/geometryOptimization',
        'form66': '/fleurInput/output/specialOutput',
        'format': '/fleurInput/output/plotting',
        'frcor': '/fleurInput/calculationSetup/coreElectrons',
        'fullMatch': '/fleurInput/calculationSetup/ldaHIA',
        'functional': '/fleurInput/calculationSetup/rdmft',
        'gcutm': '/fleurInput/calculationSetup/prodBasis',
        'gw': '/fleurInput/calculationSetup/expertModes',
        'idsprs': '/fleurInput/calculationSetup/xcFunctional/xcParams',
        'idsprs0': '/fleurInput/calculationSetup/xcFunctional/ggaPrinting',
        'idsprsi': '/fleurInput/calculationSetup/xcFunctional/ggaPrinting',
        'idsprsl': '/fleurInput/calculationSetup/xcFunctional/ggaPrinting',
        'idsprsv': '/fleurInput/calculationSetup/xcFunctional/ggaPrinting',
        'iggachk': '/fleurInput/calculationSetup/xcFunctional/ggaPrinting',
        'igrd': '/fleurInput/calculationSetup/xcFunctional/xcParams',
        'imix': '/fleurInput/calculationSetup/scfLoop',
        'intFullRadial': '/fleurInput/calculationSetup/greensFunction',
        'integ': '/fleurInput/output/vacuumDOS',
        'invs1': '/fleurInput/calculationSetup/oneDParams',
        'iplot': '/fleurInput/output/plotting',
        'isec1': '/fleurInput/calculationSetup/expertModes',
        'itmax': '/fleurInput/calculationSetup/scfLoop',
        'itmaxHubbard1': '/fleurInput/calculationSetup/ldaHIA',
        'jDOS': '/fleurInput/output/bandDOS',
        'jobList': '/fleurInput/output/wannier/jobList',
        'jspins': '/fleurInput/calculationSetup/magnetism',
        'kcrel': '/fleurInput/calculationSetup/coreElectrons',
        'l_J': '/fleurInput/calculationSetup/magnetism',
        'l_adjEnpara': '/fleurInput/calculationSetup/ldaU',
        'l_bloechl': '/fleurInput/cell/bzIntegration',
        'l_constrained': '/fleurInput/calculationSetup/magnetism/mtNocoParams',
        'l_core_confpot': '/fleurInput/calculationSetup/coreElectrons',
        'l_correctEtot': '/fleurInput/calculationSetup/ldaHIA',
        'l_eigout': '/fleurInput/output/juPhon',
        'l_f': '/fleurInput/calculationSetup/geometryOptimization',
        'l_linMix': '/fleurInput/calculationSetup/ldaU',
        'l_mtNocoPot': '/fleurInput/calculationSetup/magnetism/mtNocoParams',
        'l_noco': '/fleurInput/calculationSetup/magnetism',
        'l_nonsphDC': '/fleurInput/calculationSetup/ldaHIA',
        'l_onlyMtStDen': '/fleurInput/calculationSetup/magnetism',
        'l_potout': '/fleurInput/output/juPhon',
        'l_rdmft': '/fleurInput/calculationSetup/rdmft',
        'l_relaxSQA': '/fleurInput/calculationSetup/magnetism/mtNocoParams',
        'l_resolvent': '/fleurInput/calculationSetup/greensFunction',
        'l_scaleMag': '/fleurInput/calculationSetup/magnetism/sourceFreeMag',
        'l_soc': '/fleurInput/calculationSetup/soc',
        'l_sourceFree': '/fleurInput/calculationSetup/magnetism/sourceFreeMag',
        'l_ss': '/fleurInput/calculationSetup/magnetism',
        'lexp': '/fleurInput/calculationSetup/prodBasis',
        'lflip': '/fleurInput/calculationSetup/magnetism',
        'listName': '/fleurInput/cell/bzIntegration/kPointListSelection',
        'lmax': '/fleurInput/output/coreSpectrum',
        'locx1': '/fleurInput/output/vacuumDOS',
        'locx2': '/fleurInput/output/vacuumDOS',
        'locy1': '/fleurInput/output/vacuumDOS',
        'locy2': '/fleurInput/output/vacuumDOS',
        'lpr': '/fleurInput/calculationSetup/expertModes',
        'lwb': '/fleurInput/calculationSetup/xcFunctional/xcParams',
        'm_cyl': '/fleurInput/calculationSetup/oneDParams',
        'mag_mixing_scheme': '/fleurInput/calculationSetup/magnetism/mtNocoParams',
        'mag_scale': '/fleurInput/calculationSetup/magnetism/sourceFreeMag',
        'maxEigenval': '/fleurInput/output/chargeDensitySlicing',
        'maxEnergy': '/fleurInput/output/bandDOS',
        'maxIterBroyd': '/fleurInput/calculationSetup/scfLoop',
        'maxSpinDown': '/fleurInput/output/wannier/bandSelection',
        'maxSpinUp': '/fleurInput/output/wannier/bandSelection',
        'maxTimeToStartIter': '/fleurInput/calculationSetup/scfLoop',
        'mcd': '/fleurInput/output/magneticCircularDichroism',
        'minCalcDistance': '/fleurInput/calculationSetup/greensFunction',
        'minDistance': '/fleurInput/calculationSetup/scfLoop',
        'minEigenval': '/fleurInput/output/chargeDensitySlicing',
        'minEnergy': '/fleurInput/output/bandDOS',
        'minSpinDown': '/fleurInput/output/wannier/bandSelection',
        'minSpinUp': '/fleurInput/output/wannier/bandSelection',
        'minmatDistance': '/fleurInput/calculationSetup/ldaHIA',
        'minoccDistance': '/fleurInput/calculationSetup/ldaHIA',
        'mixParam': '/fleurInput/calculationSetup/ldaU',
        'mix_RelaxWeightOffD': '/fleurInput/calculationSetup/magnetism/mtNocoParams',
        'mix_constr': '/fleurInput/calculationSetup/magnetism/mtNocoParams',
        'mode': '/fleurInput/cell/bzIntegration',
        'ms': '/fleurInput/output/wannier',
        'n_occpm': '/fleurInput/calculationSetup/ldaHIA',
        'name': '/fleurInput/calculationSetup/xcFunctional',
        'ndvgrd': '/fleurInput/calculationSetup/xcFunctional/xcParams',
        'ne': '/fleurInput/calculationSetup/greensFunction/realAxis',
        'nnne': '/fleurInput/output/chargeDensitySlicing',
        'nqphi': '/fleurInput/output/coreSpectrum',
        'nqr': '/fleurInput/output/coreSpectrum',
        'nstars': '/fleurInput/output/vacuumDOS',
        'nstm': '/fleurInput/output/vacuumDOS',
        'numPoints': '/fleurInput/output/coreSpectrum',
        'numbands': '/fleurInput/calculationSetup/cutoffs',
        'numberPoints': '/fleurInput/output/bandDOS',
        'numkpt': '/fleurInput/output/chargeDensitySlicing',
        'occEps': '/fleurInput/calculationSetup/rdmft',
        'off': '/fleurInput/calculationSetup/soc',
        'orbcomp': '/fleurInput/output/bandDOS',
        'outputSphavg': '/fleurInput/calculationSetup/greensFunction',
        'pallst': '/fleurInput/output/chargeDensitySlicing',
        'plot_charge': '/fleurInput/calculationSetup/fields',
        'plot_rho': '/fleurInput/calculationSetup/fields',
        'polar': '/fleurInput/output/plotting',
        'pot8': '/fleurInput/calculationSetup/expertModes',
        'precondParam': '/fleurInput/calculationSetup/scfLoop',
        'qfix': '/fleurInput/calculationSetup/geometryOptimization',
        'qsc': '/fleurInput/calculationSetup/magnetism/qsc',
        'qss': '/fleurInput/calculationSetup/magnetism/qss',
        'qx': '/fleurInput/calculationSetup/spinSpiralQPointMesh',
        'qy': '/fleurInput/calculationSetup/spinSpiralQPointMesh',
        'qz': '/fleurInput/calculationSetup/spinSpiralQPointMesh',
        'relativisticCorrections': '/fleurInput/calculationSetup/xcFunctional',
        'rot': '/fleurInput/calculationSetup/oneDParams',
        'secvar': '/fleurInput/calculationSetup/expertModes',
        'sgwf': '/fleurInput/output/wannier',
        'sig_b_1': '/fleurInput/calculationSetup/fields',
        'sig_b_2': '/fleurInput/calculationSetup/fields',
        'sigma': '/fleurInput/output/bandDOS',
        'slice': '/fleurInput/output',
        'soc66': '/fleurInput/calculationSetup/soc',
        'socgwf': '/fleurInput/output/wannier',
        'spav': '/fleurInput/calculationSetup/soc',
        'star': '/fleurInput/output/vacuumDOS',
        'statesAbove': '/fleurInput/calculationSetup/rdmft',
        'statesBelow': '/fleurInput/calculationSetup/rdmft',
        'supercellX': '/fleurInput/output/unfoldingBand',
        'supercellY': '/fleurInput/output/unfoldingBand',
        'supercellZ': '/fleurInput/output/unfoldingBand',
        'swsp': '/fleurInput/calculationSetup/magnetism',
        'thetaj': '/fleurInput/forceTheorem/Jij',
        'tolerance': '/fleurInput/calculationSetup/prodBasis',
        'tworkf': '/fleurInput/output/vacuumDOS',
        'unfoldBand': '/fleurInput/output/unfoldingBand',
        'vM': '/fleurInput/calculationSetup/oneDParams',
        'vacdos': '/fleurInput/output/vacuumDOS',
        'valenceElectrons': '/fleurInput/cell/bzIntegration',
        'vchk': '/fleurInput/output/checks',
        'verbose': '/fleurInput/output/coreSpectrum',
        'wannier': '/fleurInput/output',
        'warp_factor': '/fleurInput/calculationSetup/expertModes',
        'zrfs1': '/fleurInput/calculationSetup/oneDParams',
        'zsigma': '/fleurInput/calculationSetup/fields'
    },
    'unique_path_attribs': {
        'a1': ['/fleurInput/cell/bulkLattice/a1', '/fleurInput/cell/filmLattice/a1'],
        'a2': ['/fleurInput/cell/bulkLattice/a2', '/fleurInput/cell/filmLattice/a2'],
        'correlation':
        ['/fleurInput/calculationSetup/xcFunctional/LibXCID', '/fleurInput/calculationSetup/xcFunctional/LibXCName'],
        'eig66': ['/fleurInput/calculationSetup/expertModes', '/fleurInput/output'],
        'etot_correlation':
        ['/fleurInput/calculationSetup/xcFunctional/LibXCID', '/fleurInput/calculationSetup/xcFunctional/LibXCName'],
        'etot_exchange':
        ['/fleurInput/calculationSetup/xcFunctional/LibXCID', '/fleurInput/calculationSetup/xcFunctional/LibXCName'],
        'exchange':
        ['/fleurInput/calculationSetup/xcFunctional/LibXCID', '/fleurInput/calculationSetup/xcFunctional/LibXCName'],
        'l_mperp':
        ['/fleurInput/calculationSetup/magnetism/mtNocoParams', '/fleurInput/calculationSetup/greensFunction'],
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
