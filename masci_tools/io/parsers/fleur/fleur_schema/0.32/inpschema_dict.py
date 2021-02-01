# -*- coding: utf-8 -*-
"""
This file contains information parsed from the FleurInputSchema.xsd
for version 0.32

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
__inp_version__ = '0.32'
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
        'FleurBool4DVecType': {
            'base_types': ['switch'],
            'length': 4
        },
        'FleurBoolVecType': {
            'base_types': ['switch'],
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
            'base_types': ['string'],
            'length': 3
        },
        'LatticeParameterType': {
            'base_types': ['string'],
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
            'base_types': ['string'],
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
        'TetType': {
            'base_types': ['int'],
            'length': 4
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
    'attrib_types': {
        'Gmax': ['string'],
        'GmaxXC': ['string'],
        'I_initial': ['float'],
        'J': ['string'],
        'Kmax': ['string'],
        'M': ['string'],
        'MM': ['int'],
        'TwoD': ['switch'],
        'U': ['string'],
        'all_atoms': ['switch'],
        'alpha': ['float', 'string'],
        'alpha_Ex': ['float'],
        'analytical_cont': ['switch'],
        'atomList': ['switch'],
        'atomType': ['int'],
        'atomicNumber': ['int'],
        'autocomp': ['switch'],
        'b_cons_x': ['string'],
        'b_cons_y': ['string'],
        'b_field': ['string'],
        'b_field_mt': ['string'],
        'band': ['switch'],
        'banddos': ['switch'],
        'bands': ['int'],
        'beta': ['float', 'string'],
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
        'dTilda': ['string'],
        'dVac': ['string'],
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
        'ellow': ['float', 'string'],
        'elup': ['float', 'string'],
        'energy': ['string'],
        'energyLo': ['float'],
        'energyUp': ['float'],
        'eonly': ['switch'],
        'epsdisp': ['string'],
        'epsforce': ['string'],
        'et': ['float'],
        'etot_correlation': ['int', 'string'],
        'etot_exchange': ['int', 'string'],
        'ewaldlambda': ['int'],
        'exchange': ['int', 'string'],
        'f': ['switch', 'int'],
        'fermiSmearingEnergy': ['string'],
        'fermiSmearingTemp': ['string'],
        'file': ['string'],
        'fixed_moment': ['string'],
        'fleurInputVersion': ['string'],
        'flipSpinPhi': ['string'],
        'flipSpinScale': ['switch'],
        'flipSpinTheta': ['string'],
        'force_converged': ['string'],
        'forcealpha': ['string'],
        'forcemix': ['string'],
        'form66': ['switch'],
        'format': ['int'],
        'frcor': ['switch'],
        'fullMatch': ['switch'],
        'functional': ['string'],
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
        'jDOS': ['switch'],
        'jspins': ['int'],
        'kcrel': ['int'],
        'key': ['string'],
        'kkintgrCutoff': ['float', 'string'],
        'l': ['int'],
        'l_J': ['switch'],
        'l_RelaxAlpha': ['switch'],
        'l_RelaxBeta': ['switch'],
        'l_RelaxMT': ['switch'],
        'l_adjEnpara': ['switch'],
        'l_amf': ['switch'],
        'l_bloechl': ['switch'],
        'l_constr': ['switch'],
        'l_correctEtot': ['switch'],
        'l_disp': ['switch'],
        'l_f': ['switch'],
        'l_fermi': ['switch'],
        'l_linMix': ['switch'],
        'l_magn': ['switch'],
        'l_mperp': ['switch'],
        'l_mtNocoPot': ['switch'],
        'l_noco': ['switch'],
        'l_nonsphDC': ['switch'],
        'l_onlyMtStDen': ['switch'],
        'l_rdmft': ['switch'],
        'l_relax': ['switch'],
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
        'mag_scale': ['string'],
        'maxEigenval': ['string'],
        'maxEnergy': ['string'],
        'maxIterBroyd': ['int'],
        'maxSpinDown': ['int'],
        'maxSpinUp': ['int'],
        'maxTimeToStartIter': ['string'],
        'mcd': ['switch'],
        'minCalcDistance': ['float'],
        'minDistance': ['string'],
        'minEigenval': ['string'],
        'minEnergy': ['string'],
        'minSpinDown': ['int'],
        'minSpinUp': ['int'],
        'minmatDistance': ['float'],
        'minoccDistance': ['float'],
        'mixParam': ['float'],
        'mix_RelaxWeightOffD': ['string'],
        'mix_b': ['string'],
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
        'nmatsub': ['int'],
        'nnne': ['int'],
        'nqphi': ['int'],
        'nqr': ['int'],
        'nsh': ['int'],
        'nshells': ['int'],
        'nstars': ['int'],
        'nstm': ['int'],
        'ntet': ['int'],
        'ntria': ['int'],
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
        'phi': ['string'],
        'plot_charge': ['switch'],
        'plot_rho': ['switch'],
        'polar': ['switch'],
        'pot8': ['switch'],
        'potential': ['switch'],
        'precondParam': ['string'],
        'purpose': ['string'],
        'qfix': ['int'],
        'qx': ['int'],
        'qy': ['int'],
        'qz': ['int'],
        'radius': ['string'],
        'relativisticCorrections': ['switch'],
        'relaxXYZ': ['string'],
        'remove4f': ['switch'],
        'rot': ['int'],
        's': ['switch', 'int'],
        'scale': ['string'],
        'secvar': ['switch'],
        'select': ['string'],
        'sgwf': ['switch'],
        'sig_b_1': ['string'],
        'sig_b_2': ['string'],
        'sigma': ['float', 'string'],
        'slice': ['switch'],
        'soc66': ['switch'],
        'socgwf': ['switch'],
        'socscale': ['float'],
        'spav': ['switch'],
        'species': ['string'],
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
        'typeMT': ['int'],
        'unfoldBand': ['switch'],
        'vM': ['int'],
        'vacdos': ['switch'],
        'vacuum': ['int'],
        'valenceElectrons': ['string'],
        'value': ['string'],
        'vcaAddCharge': ['float'],
        'vca_charge': ['string'],
        'vchk': ['switch'],
        'vec1': ['string'],
        'vec2': ['string'],
        'vec3': ['string'],
        'vecField': ['switch'],
        'verbose': ['switch'],
        'vol': ['string'],
        'wannier': ['switch'],
        'warp_factor': ['string'],
        'weight': ['string'],
        'zero': ['string'],
        'zrfs1': ['switch'],
        'zsigma': ['string']
    },
    'inp_version':
    '0.32',
    'omitt_contained_tags': [
        'constants', 'atomSpecies', 'atomGroups', 'symmetryOperations', 'kPointLists', 'displacements',
        'relaxation-history', 'spinSpiralDispersion', 'qVectors'
    ],
    'other_attribs': {
        'abspos': ['/fleurInput/atomGroups/atomGroup/absPos'],
        'alpha': [
            '/fleurInput/atomGroups/atomGroup/nocoParams/@alpha', '/fleurInput/atomSpecies/species/nocoParams/@alpha',
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
        'beta':
        ['/fleurInput/atomGroups/atomGroup/nocoParams/@beta', '/fleurInput/atomSpecies/species/nocoParams/@beta'],
        'calculate':
        ['/fleurInput/atomGroups/atomGroup/force/@calculate', '/fleurInput/atomSpecies/species/force/@calculate'],
        'cartesian': ['/fleurInput/output/plotting/plot/@cartesian'],
        'chargedensity': ['/fleurInput/atomGroups/atomGroup/cFCoeffs/@chargeDensity'],
        'coreconfig': ['/fleurInput/atomSpecies/species/electronConfig/coreConfig'],
        'count': ['/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/@count'],
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
        'displace': ['/fleurInput/relaxation/displacements/displace'],
        'eb': [
            '/fleurInput/calculationSetup/greensFunction/contourDOS/@eb',
            '/fleurInput/calculationSetup/greensFunction/contourRectangle/@eb',
            '/fleurInput/calculationSetup/greensFunction/contourSemicircle/@eb'
        ],
        'ederiv': ['/fleurInput/atomGroups/atomGroup/lo/@eDeriv', '/fleurInput/atomSpecies/species/lo/@eDeriv'],
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
        'filmpos': ['/fleurInput/atomGroups/atomGroup/filmPos'],
        'flipspinphi': ['/fleurInput/atomSpecies/species/@flipSpinPhi'],
        'flipspinscale': ['/fleurInput/atomSpecies/species/@flipSpinScale'],
        'flipspintheta': ['/fleurInput/atomSpecies/species/@flipSpinTheta'],
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
        'j': [
            '/fleurInput/atomGroups/atomGroup/ldaHIA/@J', '/fleurInput/atomGroups/atomGroup/ldaHIA/exc/@J',
            '/fleurInput/atomGroups/atomGroup/ldaU/@J', '/fleurInput/atomSpecies/species/ldaHIA/@J',
            '/fleurInput/atomSpecies/species/ldaHIA/exc/@J', '/fleurInput/atomSpecies/species/ldaU/@J'
        ],
        'jdos': [
            '/fleurInput/atomGroups/atomGroup/absPos/@jDOS', '/fleurInput/atomGroups/atomGroup/filmPos/@jDOS',
            '/fleurInput/atomGroups/atomGroup/relPos/@jDOS'
        ],
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
        'kpoint': ['/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/kPoint'],
        'l': [
            '/fleurInput/atomGroups/atomGroup/ldaHIA/@l', '/fleurInput/atomGroups/atomGroup/ldaHIA/exc/@l',
            '/fleurInput/atomGroups/atomGroup/ldaU/@l', '/fleurInput/atomGroups/atomGroup/lo/@l',
            '/fleurInput/atomSpecies/species/ldaHIA/@l', '/fleurInput/atomSpecies/species/ldaHIA/exc/@l',
            '/fleurInput/atomSpecies/species/ldaU/@l', '/fleurInput/atomSpecies/species/lo/@l'
        ],
        'l_amf': [
            '/fleurInput/atomGroups/atomGroup/ldaHIA/@l_amf', '/fleurInput/atomGroups/atomGroup/ldaU/@l_amf',
            '/fleurInput/atomSpecies/species/ldaHIA/@l_amf', '/fleurInput/atomSpecies/species/ldaU/@l_amf'
        ],
        'l_fermi': ['/fleurInput/calculationSetup/greensFunction/contourDOS/@l_fermi'],
        'l_magn':
        ['/fleurInput/atomGroups/atomGroup/nocoParams/@l_magn', '/fleurInput/atomSpecies/species/nocoParams/@l_magn'],
        'l_relax':
        ['/fleurInput/atomGroups/atomGroup/nocoParams/@l_relax', '/fleurInput/atomSpecies/species/nocoParams/@l_relax'],
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
            '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/kPoint/@label',
            '/fleurInput/calculationSetup/greensFunction/contourDOS/@label',
            '/fleurInput/calculationSetup/greensFunction/contourRectangle/@label',
            '/fleurInput/calculationSetup/greensFunction/contourSemicircle/@label'
        ],
        'layer': ['/fleurInput/output/vacuumDOS/layer'],
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
        'm': ['/fleurInput/atomGroups/atomGroup/nocoParams/@M', '/fleurInput/atomSpecies/species/nocoParams/@M'],
        'magfield': ['/fleurInput/atomGroups/atomGroup/@magField'],
        'magmom': ['/fleurInput/atomSpecies/species/@magMom'],
        'n': [
            '/fleurInput/atomGroups/atomGroup/lo/@n', '/fleurInput/atomSpecies/species/lo/@n',
            '/fleurInput/calculationSetup/greensFunction/contourDOS/@n',
            '/fleurInput/calculationSetup/greensFunction/contourSemicircle/@n'
        ],
        'n1': ['/fleurInput/calculationSetup/greensFunction/contourRectangle/@n1'],
        'n2': ['/fleurInput/calculationSetup/greensFunction/contourRectangle/@n2'],
        'n3': ['/fleurInput/calculationSetup/greensFunction/contourRectangle/@n3'],
        'name': [
            '/fleurInput/atomSpecies/species/@name',
            '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/@name',
            '/fleurInput/constants/constant/@name'
        ],
        'nmatsub': ['/fleurInput/calculationSetup/greensFunction/contourRectangle/@nmatsub'],
        'nshells': [
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/@nshells',
            '/fleurInput/atomSpecies/species/greensfCalculation/@nshells'
        ],
        'ntet': ['/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/tetraeder/@ntet'],
        'ntria': ['/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/triangles/@ntria'],
        'nx': ['/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/@nx'],
        'ny': ['/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/@ny'],
        'nz': ['/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/@nz'],
        'onlymt': ['/fleurInput/output/plotting/plot/@onlyMT'],
        'orbcomp': [
            '/fleurInput/atomGroups/atomGroup/absPos/@orbcomp', '/fleurInput/atomGroups/atomGroup/filmPos/@orbcomp',
            '/fleurInput/atomGroups/atomGroup/relPos/@orbcomp'
        ],
        'orbcomprot': ['/fleurInput/atomGroups/atomGroup/orbcomprot'],
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
        'posforce': ['/fleurInput/relaxation/relaxation-history/step/posforce'],
        'potential': ['/fleurInput/atomGroups/atomGroup/cFCoeffs/@potential'],
        'q': [
            '/fleurInput/forceTheorem/DMI/qVectors/q', '/fleurInput/forceTheorem/Jij/qVectors/q',
            '/fleurInput/forceTheorem/spinSpiralDispersion/q'
        ],
        'radius':
        ['/fleurInput/atomGroups/atomGroup/mtSphere/@radius', '/fleurInput/atomSpecies/species/mtSphere/@radius'],
        'relaxxyz':
        ['/fleurInput/atomGroups/atomGroup/force/@relaxXYZ', '/fleurInput/atomSpecies/species/force/@relaxXYZ'],
        'relpos': ['/fleurInput/atomGroups/atomGroup/relPos'],
        'remove4f': ['/fleurInput/atomGroups/atomGroup/cFCoeffs/@remove4f'],
        'row-1': ['/fleurInput/calculationSetup/symmetryOperations/symOp/row-1'],
        'row-2': ['/fleurInput/calculationSetup/symmetryOperations/symOp/row-2'],
        'row-3': ['/fleurInput/calculationSetup/symmetryOperations/symOp/row-3'],
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
        'shape': ['/fleurInput/calculationSetup/fields/shape'],
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
        'tet': ['/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/tetraeder/tet'],
        'theta': [
            '/fleurInput/atomGroups/atomGroup/ldaHIA/@theta', '/fleurInput/atomGroups/atomGroup/ldaU/@theta',
            '/fleurInput/atomSpecies/species/ldaHIA/@theta', '/fleurInput/atomSpecies/species/ldaU/@theta'
        ],
        'tria': ['/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/triangles/tria'],
        'twod': ['/fleurInput/output/plotting/plot/@TwoD'],
        'type': [
            '/fleurInput/atomGroups/atomGroup/lo/@type', '/fleurInput/atomSpecies/species/lo/@type',
            '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/@type'
        ],
        'typemt': ['/fleurInput/output/plotting/plot/@typeMT'],
        'u': [
            '/fleurInput/atomGroups/atomGroup/ldaHIA/@U', '/fleurInput/atomGroups/atomGroup/ldaU/@U',
            '/fleurInput/atomSpecies/species/ldaHIA/@U', '/fleurInput/atomSpecies/species/ldaU/@U'
        ],
        'vacuum': ['/fleurInput/cell/filmLattice/vacuumEnergyParameters/@vacuum'],
        'valenceconfig': ['/fleurInput/atomSpecies/species/electronConfig/valenceConfig'],
        'value': [
            '/fleurInput/atomGroups/atomGroup/ldaHIA/addArg/@value',
            '/fleurInput/atomSpecies/species/ldaHIA/addArg/@value', '/fleurInput/constants/constant/@value'
        ],
        'vca_charge': ['/fleurInput/atomSpecies/species/special/@vca_charge'],
        'vcaaddcharge': ['/fleurInput/atomGroups/atomGroup/@vcaAddCharge'],
        'vec1': ['/fleurInput/output/plotting/plot/@vec1'],
        'vec2': ['/fleurInput/output/plotting/plot/@vec2'],
        'vec3': ['/fleurInput/output/plotting/plot/@vec3'],
        'vecfield': ['/fleurInput/output/plotting/plot/@vecField'],
        'vol': [
            '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/tetraeder/tet/@vol',
            '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/triangles/tria/@vol'
        ],
        'wannier': [
            '/fleurInput/atomGroups/atomGroup/absPos/@wannier', '/fleurInput/atomGroups/atomGroup/filmPos/@wannier',
            '/fleurInput/atomGroups/atomGroup/relPos/@wannier'
        ],
        'weight': ['/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/kPoint/@weight'],
        'zero': ['/fleurInput/output/plotting/plot/@zero']
    },
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
            'type': ['string']
        }],
        'jobList': [{
            'length': 'unbounded',
            'type': ['string']
        }],
        'kPoint': [{
            'length': 3,
            'type': ['string']
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
        's': [{
            'length': 4,
            'type': ['switch']
        }],
        'shape': [{
            'length': 1,
            'type': ['string']
        }],
        'tet': [{
            'length': 4,
            'type': ['int']
        }],
        'tria': [{
            'length': 3,
            'type': ['int']
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
            'optional': [
                'mtSphere', 'atomicCutoffs', 'energyParameters', 'force', 'nocoParams', 'ldaU', 'ldaHIA',
                'greensfCalculation', 'torgueCalculation', 'lo', 'orbcomprot', 'cFCoeffs'
            ],
            'optional_attribs': ['magField', 'vcaAddCharge'],
            'order': [
                'relPos', 'absPos', 'filmPos', 'mtSphere', 'atomicCutoffs', 'energyParameters', 'force', 'nocoParams',
                'ldaU', 'ldaHIA', 'greensfCalculation', 'torgueCalculation', 'lo', 'orbcomprot', 'cFCoeffs'
            ],
            'several': ['relPos', 'absPos', 'filmPos', 'ldaU', 'ldaHIA', 'greensfCalculation', 'lo'],
            'simple': [
                'relPos', 'absPos', 'filmPos', 'mtSphere', 'atomicCutoffs', 'energyParameters', 'force', 'nocoParams',
                'ldaU', 'lo', 'orbcomprot', 'cFCoeffs'
            ],
            'text': ['relPos', 'absPos', 'filmPos', 'orbcomprot']
        },
        '/fleurInput/atomGroups/atomGroup/absPos': {
            'attribs': ['label', 'wannier', 'orbcomp', 'jDOS', 'banddos'],
            'optional': [],
            'optional_attribs': ['label', 'wannier', 'orbcomp', 'jDOS', 'banddos'],
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
            'attribs': ['label', 'wannier', 'orbcomp', 'jDOS', 'banddos'],
            'optional': [],
            'optional_attribs': ['label', 'wannier', 'orbcomp', 'jDOS', 'banddos'],
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
            'optional': ['exc', 'addArg'],
            'optional_attribs': ['phi', 'theta', 'init_occ', 'kkintgrCutoff', 'label'],
            'order': ['exc', 'addArg'],
            'several': ['exc', 'addArg'],
            'simple': ['exc', 'addArg'],
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
            'optional_attribs': ['l_magn', 'M', 'b_cons_x', 'b_cons_y'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/atomGroups/atomGroup/relPos': {
            'attribs': ['label', 'wannier', 'orbcomp', 'jDOS', 'banddos'],
            'optional': [],
            'optional_attribs': ['label', 'wannier', 'orbcomp', 'jDOS', 'banddos'],
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
            'attribs': ['name', 'element', 'atomicNumber', 'magMom', 'flipSpinPhi', 'flipSpinTheta', 'flipSpinScale'],
            'optional': [
                'energyParameters', 'prodBasis', 'special', 'force', 'nocoParams', 'ldaU', 'ldaHIA',
                'greensfCalculation', 'torgueCalculation', 'lo'
            ],
            'optional_attribs': ['magMom', 'flipSpinPhi', 'flipSpinTheta', 'flipSpinScale'],
            'order': [
                'mtSphere', 'atomicCutoffs', 'electronConfig', 'energyParameters', 'prodBasis', 'special', 'force',
                'nocoParams', 'ldaU', 'ldaHIA', 'greensfCalculation', 'torgueCalculation', 'lo'
            ],
            'several': ['ldaU', 'ldaHIA', 'greensfCalculation', 'lo'],
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
            'optional': ['exc', 'addArg'],
            'optional_attribs': ['phi', 'theta', 'init_occ', 'kkintgrCutoff', 'label'],
            'order': ['exc', 'addArg'],
            'several': ['exc', 'addArg'],
            'simple': ['exc', 'addArg'],
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
            'optional_attribs': ['l_magn', 'M', 'b_cons_x', 'b_cons_y'],
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
                'prodBasis', 'soc', 'nocoParams', 'oneDParams', 'expertModes', 'geometryOptimization', 'ldaU', 'ldaHIA',
                'greensFunction', 'rdmft', 'spinSpiralQPointMesh', 'fields', 'energyParameterLimits'
            ],
            'optional_attribs': [],
            'order': [
                'cutoffs', 'scfLoop', 'coreElectrons', 'magnetism', 'bzIntegration', 'symmetryOperations', 'prodBasis',
                'soc', 'nocoParams', 'oneDParams', 'expertModes', 'geometryOptimization', 'ldaU', 'ldaHIA',
                'greensFunction', 'rdmft', 'spinSpiralQPointMesh', 'fields', 'energyParameterLimits'
            ],
            'several': [],
            'simple': [
                'cutoffs', 'scfLoop', 'coreElectrons', 'magnetism', 'prodBasis', 'soc', 'oneDParams', 'expertModes',
                'geometryOptimization', 'ldaU', 'ldaHIA', 'rdmft', 'spinSpiralQPointMesh', 'energyParameterLimits'
            ],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration': {
            'attribs': ['valenceElectrons', 'mode', 'fermiSmearingEnergy', 'fermiSmearingTemp', 'l_bloechl'],
            'optional': [],
            'optional_attribs': ['valenceElectrons', 'mode', 'fermiSmearingEnergy', 'fermiSmearingTemp', 'l_bloechl'],
            'order': ['kPointListSelection', 'kPointLists'],
            'several': [],
            'simple': ['kPointListSelection'],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointListSelection': {
            'attribs': ['listName'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointLists': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['kPointList'],
            'several': ['kPointList'],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList': {
            'attribs': ['name', 'type', 'count', 'nx', 'ny', 'nz'],
            'optional': ['tetraeder', 'triangles'],
            'optional_attribs': ['type', 'count', 'nx', 'ny', 'nz'],
            'order': ['kPoint', 'tetraeder', 'triangles'],
            'several': ['kPoint'],
            'simple': ['kPoint'],
            'text': ['kPoint']
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/kPoint': {
            'attribs': ['weight', 'label'],
            'optional': [],
            'optional_attribs': ['label'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/tetraeder': {
            'attribs': ['ntet'],
            'optional': [],
            'optional_attribs': ['ntet'],
            'order': ['tet'],
            'several': ['tet'],
            'simple': ['tet'],
            'text': ['tet']
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/tetraeder/tet': {
            'attribs': ['vol'],
            'optional': [],
            'optional_attribs': [],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/triangles': {
            'attribs': ['ntria'],
            'optional': [],
            'optional_attribs': ['ntria'],
            'order': ['tria'],
            'several': ['tria'],
            'simple': ['tria'],
            'text': ['tria']
        },
        '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/triangles/tria': {
            'attribs': ['vol'],
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
            'attribs': ['l_f', 'forcealpha', 'epsdisp', 'epsforce', 'forcemix', 'qfix', 'force_converged'],
            'optional': [],
            'optional_attribs': ['forcealpha', 'epsdisp', 'epsforce', 'forcemix', 'qfix', 'force_converged'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/greensFunction': {
            'attribs': ['l_mperp', 'l_resolvent', 'minCalcDistance', 'outputSphavg', 'intFullRadial'],
            'optional': [],
            'optional_attribs': ['l_resolvent', 'minCalcDistance', 'outputSphavg', 'intFullRadial'],
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
                'itmax', 'beta', 'minoccDistance', 'minmatDistance', 'n_occpm', 'dftspinpol', 'fullMatch', 'l_nonsphDC',
                'l_correctEtot'
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
            'attribs': ['jspins', 'l_noco', 'l_J', 'swsp', 'lflip', 'l_onlyMtStDen', 'fixed_moment'],
            'optional': [],
            'optional_attribs': ['l_noco', 'l_J', 'swsp', 'lflip', 'l_onlyMtStDen', 'fixed_moment'],
            'order': [],
            'several': [],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/nocoParams': {
            'attribs': [
                'l_ss', 'l_mperp', 'l_constr', 'l_disp', 'sso_opt', 'mix_b', 'thetaJ', 'nsh', 'l_mtNocoPot',
                'l_sourceFree', 'l_scaleMag', 'mag_scale', 'l_RelaxMT', 'l_RelaxAlpha', 'l_RelaxBeta',
                'mix_RelaxWeightOffD'
            ],
            'optional': ['qsc'],
            'optional_attribs': [
                'l_disp', 'thetaJ', 'nsh', 'l_mtNocoPot', 'l_sourceFree', 'l_scaleMag', 'mag_scale', 'l_RelaxMT',
                'l_RelaxAlpha', 'l_RelaxBeta', 'mix_RelaxWeightOffD'
            ],
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
        '/fleurInput/calculationSetup/symmetryOperations': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['symOp'],
            'several': ['symOp'],
            'simple': [],
            'text': []
        },
        '/fleurInput/calculationSetup/symmetryOperations/symOp': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['row-1', 'row-2', 'row-3'],
            'several': [],
            'simple': ['row-1', 'row-2', 'row-3'],
            'text': ['row-1', 'row-2', 'row-3']
        },
        '/fleurInput/cell': {
            'attribs': [],
            'optional': [],
            'optional_attribs': [],
            'order': ['bulkLattice', 'filmLattice'],
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
            'attribs': ['dos', 'band', 'slice', 'coreSpec', 'wannier', 'eig66'],
            'optional': [
                'checks', 'bandDOS', 'vacuumDOS', 'plotting', 'chargeDensitySlicing', 'specialOutput', 'coreSpectrum',
                'wannier', 'magneticCircularDichroism', 'unfoldingBand'
            ],
            'optional_attribs': ['dos', 'band', 'slice', 'coreSpec', 'wannier', 'eig66'],
            'order': [
                'checks', 'bandDOS', 'vacuumDOS', 'plotting', 'chargeDensitySlicing', 'specialOutput', 'coreSpectrum',
                'wannier', 'magneticCircularDichroism', 'unfoldingBand'
            ],
            'several': [],
            'simple': [
                'checks', 'bandDOS', 'chargeDensitySlicing', 'specialOutput', 'magneticCircularDichroism',
                'unfoldingBand'
            ],
            'text': []
        },
        '/fleurInput/output/bandDOS': {
            'attribs': ['all_atoms', 'minEnergy', 'maxEnergy', 'sigma', 'numberPoints'],
            'optional': [],
            'optional_attribs': ['all_atoms', 'minEnergy', 'maxEnergy', 'sigma', 'numberPoints'],
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
    'tag_paths': {
        'a1': ['/fleurInput/cell/bulkLattice/a1', '/fleurInput/cell/filmLattice/a1'],
        'a2': ['/fleurInput/cell/bulkLattice/a2', '/fleurInput/cell/filmLattice/a2'],
        'abspos':
        '/fleurInput/atomGroups/atomGroup/absPos',
        'addarg': ['/fleurInput/atomGroups/atomGroup/ldaHIA/addArg', '/fleurInput/atomSpecies/species/ldaHIA/addArg'],
        'atomgroup':
        '/fleurInput/atomGroups/atomGroup',
        'atomgroups':
        '/fleurInput/atomGroups',
        'atomiccutoffs':
        ['/fleurInput/atomGroups/atomGroup/atomicCutoffs', '/fleurInput/atomSpecies/species/atomicCutoffs'],
        'atomspecies':
        '/fleurInput/atomSpecies',
        'banddos':
        '/fleurInput/output/bandDOS',
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
        'cfcoeffs':
        '/fleurInput/atomGroups/atomGroup/cFCoeffs',
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
        'dmi':
        '/fleurInput/forceTheorem/DMI',
        'edgeindices':
        '/fleurInput/output/coreSpectrum/edgeIndices',
        'electronconfig':
        '/fleurInput/atomSpecies/species/electronConfig',
        'energyparameterlimits':
        '/fleurInput/calculationSetup/energyParameterLimits',
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
        '/fleurInput/xcFunctional/ggaPrinting',
        'greensfcalculation':
        ['/fleurInput/atomGroups/atomGroup/greensfCalculation', '/fleurInput/atomSpecies/species/greensfCalculation'],
        'greensfelements': [
            '/fleurInput/atomGroups/atomGroup/torgueCalculation/greensfElements',
            '/fleurInput/atomSpecies/species/torgueCalculation/greensfElements'
        ],
        'greensfunction':
        '/fleurInput/calculationSetup/greensFunction',
        'jij':
        '/fleurInput/forceTheorem/Jij',
        'joblist':
        '/fleurInput/output/wannier/jobList',
        'kpoint':
        '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/kPoint',
        'kpointlist':
        '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList',
        'kpointlists':
        '/fleurInput/calculationSetup/bzIntegration/kPointLists',
        'kpointlistselection':
        '/fleurInput/calculationSetup/bzIntegration/kPointListSelection',
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
        'libxcid':
        '/fleurInput/xcFunctional/LibXCID',
        'libxcname':
        '/fleurInput/xcFunctional/LibXCName',
        'lo': ['/fleurInput/atomGroups/atomGroup/lo', '/fleurInput/atomSpecies/species/lo'],
        'mae':
        '/fleurInput/forceTheorem/MAE',
        'magneticcirculardichroism':
        '/fleurInput/output/magneticCircularDichroism',
        'magnetism':
        '/fleurInput/calculationSetup/magnetism',
        'matrixelements': [
            '/fleurInput/atomGroups/atomGroup/greensfCalculation/matrixElements',
            '/fleurInput/atomSpecies/species/greensfCalculation/matrixElements'
        ],
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
        'qsc':
        '/fleurInput/calculationSetup/nocoParams/qsc',
        'qss':
        '/fleurInput/calculationSetup/nocoParams/qss',
        'qvectors': ['/fleurInput/forceTheorem/DMI/qVectors', '/fleurInput/forceTheorem/Jij/qVectors'],
        'rdmft':
        '/fleurInput/calculationSetup/rdmft',
        'realaxis':
        '/fleurInput/calculationSetup/greensFunction/realAxis',
        'relaxation':
        '/fleurInput/relaxation',
        'relaxation-history':
        '/fleurInput/relaxation/relaxation-history',
        'relpos':
        '/fleurInput/atomGroups/atomGroup/relPos',
        'row-1': [
            '/fleurInput/calculationSetup/symmetryOperations/symOp/row-1',
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-1', '/fleurInput/cell/bulkLattice/row-1',
            '/fleurInput/cell/filmLattice/bravaisMatrix/row-1', '/fleurInput/cell/filmLattice/row-1'
        ],
        'row-2': [
            '/fleurInput/calculationSetup/symmetryOperations/symOp/row-2',
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-2', '/fleurInput/cell/bulkLattice/row-2',
            '/fleurInput/cell/filmLattice/bravaisMatrix/row-2', '/fleurInput/cell/filmLattice/row-2'
        ],
        'row-3': [
            '/fleurInput/calculationSetup/symmetryOperations/symOp/row-3',
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-3', '/fleurInput/cell/filmLattice/bravaisMatrix/row-3'
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
        'symmetryoperations':
        '/fleurInput/calculationSetup/symmetryOperations',
        'symop':
        '/fleurInput/calculationSetup/symmetryOperations/symOp',
        'tet':
        '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/tetraeder/tet',
        'tetraeder':
        '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/tetraeder',
        'torguecalculation':
        ['/fleurInput/atomGroups/atomGroup/torgueCalculation', '/fleurInput/atomSpecies/species/torgueCalculation'],
        'tria':
        '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/triangles/tria',
        'triangles':
        '/fleurInput/calculationSetup/bzIntegration/kPointLists/kPointList/triangles',
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
    },
    'unique_attribs': {
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
        'c': '/fleurInput/cell/bulkLattice/c',
        'cdinf': '/fleurInput/output/checks/@cdinf',
        'chi': '/fleurInput/calculationSetup/oneDParams/@chi',
        'chng': '/fleurInput/xcFunctional/xcParams/@chng',
        'comment': '/fleurInput/comment',
        'corespec': '/fleurInput/output/@coreSpec',
        'coretail_lmax': '/fleurInput/calculationSetup/coreElectrons/@coretail_lmax',
        'ctail': '/fleurInput/calculationSetup/coreElectrons/@ctail',
        'd1': '/fleurInput/calculationSetup/oneDParams/@d1',
        'dftspinpol': '/fleurInput/calculationSetup/ldaHIA/@dftspinpol',
        'dirichlet': '/fleurInput/calculationSetup/fields/@dirichlet',
        'disp': '/fleurInput/output/checks/@disp',
        'dos': '/fleurInput/output/@dos',
        'dtilda': '/fleurInput/cell/filmLattice/@dTilda',
        'dvac': '/fleurInput/cell/filmLattice/@dVac',
        'edgeindices': '/fleurInput/output/coreSpectrum/edgeIndices',
        'edgetype': '/fleurInput/output/coreSpectrum/@edgeType',
        'ekin': '/fleurInput/output/coreSpectrum/@eKin',
        'emax': '/fleurInput/output/coreSpectrum/@eMax',
        'emin': '/fleurInput/output/coreSpectrum/@eMin',
        'energylo': '/fleurInput/output/magneticCircularDichroism/@energyLo',
        'energyup': '/fleurInput/output/magneticCircularDichroism/@energyUp',
        'eonly': '/fleurInput/output/specialOutput/@eonly',
        'epsdisp': '/fleurInput/calculationSetup/geometryOptimization/@epsdisp',
        'epsforce': '/fleurInput/calculationSetup/geometryOptimization/@epsforce',
        'ev': '/fleurInput/calculationSetup/fields/@eV',
        'ewaldlambda': '/fleurInput/calculationSetup/prodBasis/@ewaldlambda',
        'fermismearingenergy': '/fleurInput/calculationSetup/bzIntegration/@fermiSmearingEnergy',
        'fermismearingtemp': '/fleurInput/calculationSetup/bzIntegration/@fermiSmearingTemp',
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
        'gmax': '/fleurInput/calculationSetup/cutoffs/@Gmax',
        'gmaxxc': '/fleurInput/calculationSetup/cutoffs/@GmaxXC',
        'gw': '/fleurInput/calculationSetup/expertModes/@gw',
        'i_initial': '/fleurInput/output/coreSpectrum/@I_initial',
        'idsprs': '/fleurInput/xcFunctional/xcParams/@idsprs',
        'idsprs0': '/fleurInput/xcFunctional/ggaPrinting/@idsprs0',
        'idsprsi': '/fleurInput/xcFunctional/ggaPrinting/@idsprsi',
        'idsprsl': '/fleurInput/xcFunctional/ggaPrinting/@idsprsl',
        'idsprsv': '/fleurInput/xcFunctional/ggaPrinting/@idsprsv',
        'iggachk': '/fleurInput/xcFunctional/ggaPrinting/@iggachk',
        'igrd': '/fleurInput/xcFunctional/xcParams/@igrd',
        'imix': '/fleurInput/calculationSetup/scfLoop/@imix',
        'integ': '/fleurInput/output/vacuumDOS/@integ',
        'intfullradial': '/fleurInput/calculationSetup/greensFunction/@intFullRadial',
        'invs1': '/fleurInput/calculationSetup/oneDParams/@invs1',
        'iplot': '/fleurInput/output/plotting/@iplot',
        'isec1': '/fleurInput/calculationSetup/expertModes/@isec1',
        'joblist': '/fleurInput/output/wannier/jobList',
        'jspins': '/fleurInput/calculationSetup/magnetism/@jspins',
        'kcrel': '/fleurInput/calculationSetup/coreElectrons/@kcrel',
        'kmax': '/fleurInput/calculationSetup/cutoffs/@Kmax',
        'l_adjenpara': '/fleurInput/calculationSetup/ldaU/@l_adjEnpara',
        'l_bloechl': '/fleurInput/calculationSetup/bzIntegration/@l_bloechl',
        'l_constr': '/fleurInput/calculationSetup/nocoParams/@l_constr',
        'l_correctetot': '/fleurInput/calculationSetup/ldaHIA/@l_correctEtot',
        'l_disp': '/fleurInput/calculationSetup/nocoParams/@l_disp',
        'l_f': '/fleurInput/calculationSetup/geometryOptimization/@l_f',
        'l_j': '/fleurInput/calculationSetup/magnetism/@l_J',
        'l_linmix': '/fleurInput/calculationSetup/ldaU/@l_linMix',
        'l_mtnocopot': '/fleurInput/calculationSetup/nocoParams/@l_mtNocoPot',
        'l_noco': '/fleurInput/calculationSetup/magnetism/@l_noco',
        'l_nonsphdc': '/fleurInput/calculationSetup/ldaHIA/@l_nonsphDC',
        'l_onlymtstden': '/fleurInput/calculationSetup/magnetism/@l_onlyMtStDen',
        'l_rdmft': '/fleurInput/calculationSetup/rdmft/@l_rdmft',
        'l_relaxalpha': '/fleurInput/calculationSetup/nocoParams/@l_RelaxAlpha',
        'l_relaxbeta': '/fleurInput/calculationSetup/nocoParams/@l_RelaxBeta',
        'l_relaxmt': '/fleurInput/calculationSetup/nocoParams/@l_RelaxMT',
        'l_resolvent': '/fleurInput/calculationSetup/greensFunction/@l_resolvent',
        'l_scalemag': '/fleurInput/calculationSetup/nocoParams/@l_scaleMag',
        'l_soc': '/fleurInput/calculationSetup/soc/@l_soc',
        'l_sourcefree': '/fleurInput/calculationSetup/nocoParams/@l_sourceFree',
        'l_ss': '/fleurInput/calculationSetup/nocoParams/@l_ss',
        'lexp': '/fleurInput/calculationSetup/prodBasis/@lexp',
        'lflip': '/fleurInput/calculationSetup/magnetism/@lflip',
        'listname': '/fleurInput/calculationSetup/bzIntegration/kPointListSelection/@listName',
        'lmax': '/fleurInput/output/coreSpectrum/@lmax',
        'locx1': '/fleurInput/output/vacuumDOS/@locx1',
        'locx2': '/fleurInput/output/vacuumDOS/@locx2',
        'locy1': '/fleurInput/output/vacuumDOS/@locy1',
        'locy2': '/fleurInput/output/vacuumDOS/@locy2',
        'lpr': '/fleurInput/calculationSetup/expertModes/@lpr',
        'lwb': '/fleurInput/xcFunctional/xcParams/@lwb',
        'm_cyl': '/fleurInput/calculationSetup/oneDParams/@m_cyl',
        'mag_scale': '/fleurInput/calculationSetup/nocoParams/@mag_scale',
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
        'minmatdistance': '/fleurInput/calculationSetup/ldaHIA/@minmatDistance',
        'minoccdistance': '/fleurInput/calculationSetup/ldaHIA/@minoccDistance',
        'minspindown': '/fleurInput/output/wannier/bandSelection/@minSpinDown',
        'minspinup': '/fleurInput/output/wannier/bandSelection/@minSpinUp',
        'mix_b': '/fleurInput/calculationSetup/nocoParams/@mix_b',
        'mix_relaxweightoffd': '/fleurInput/calculationSetup/nocoParams/@mix_RelaxWeightOffD',
        'mixparam': '/fleurInput/calculationSetup/ldaU/@mixParam',
        'mm': '/fleurInput/calculationSetup/oneDParams/@MM',
        'mode': '/fleurInput/calculationSetup/bzIntegration/@mode',
        'ms': '/fleurInput/output/wannier/@ms',
        'n_occpm': '/fleurInput/calculationSetup/ldaHIA/@n_occpm',
        'name': '/fleurInput/xcFunctional/@name',
        'ndvgrd': '/fleurInput/xcFunctional/xcParams/@ndvgrd',
        'ne': '/fleurInput/calculationSetup/greensFunction/realAxis/@ne',
        'nnne': '/fleurInput/output/chargeDensitySlicing/@nnne',
        'nqphi': '/fleurInput/output/coreSpectrum/@nqphi',
        'nqr': '/fleurInput/output/coreSpectrum/@nqr',
        'nsh': '/fleurInput/calculationSetup/nocoParams/@nsh',
        'nstars': '/fleurInput/output/vacuumDOS/@nstars',
        'nstm': '/fleurInput/output/vacuumDOS/@nstm',
        'numbands': '/fleurInput/calculationSetup/cutoffs/@numbands',
        'numberpoints': '/fleurInput/output/bandDOS/@numberPoints',
        'numkpt': '/fleurInput/output/chargeDensitySlicing/@numkpt',
        'numpoints': '/fleurInput/output/coreSpectrum/@numPoints',
        'occeps': '/fleurInput/calculationSetup/rdmft/@occEps',
        'off': '/fleurInput/calculationSetup/soc/@off',
        'outputsphavg': '/fleurInput/calculationSetup/greensFunction/@outputSphavg',
        'pallst': '/fleurInput/output/chargeDensitySlicing/@pallst',
        'plot_charge': '/fleurInput/calculationSetup/fields/@plot_charge',
        'plot_rho': '/fleurInput/calculationSetup/fields/@plot_rho',
        'polar': '/fleurInput/output/plotting/@polar',
        'pot8': '/fleurInput/calculationSetup/expertModes/@pot8',
        'precondparam': '/fleurInput/calculationSetup/scfLoop/@precondParam',
        'qfix': '/fleurInput/calculationSetup/geometryOptimization/@qfix',
        'qsc': '/fleurInput/calculationSetup/nocoParams/qsc',
        'qss': '/fleurInput/calculationSetup/nocoParams/qss',
        'qx': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qx',
        'qy': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qy',
        'qz': '/fleurInput/calculationSetup/spinSpiralQPointMesh/@qz',
        'relativisticcorrections': '/fleurInput/xcFunctional/@relativisticCorrections',
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
        'vacdos': '/fleurInput/output/vacuumDOS/@vacdos',
        'valenceelectrons': '/fleurInput/calculationSetup/bzIntegration/@valenceElectrons',
        'vchk': '/fleurInput/output/checks/@vchk',
        'verbose': '/fleurInput/output/coreSpectrum/@verbose',
        'vm': '/fleurInput/calculationSetup/oneDParams/@vM',
        'wannier': '/fleurInput/output/@wannier',
        'warp_factor': '/fleurInput/calculationSetup/expertModes/@warp_factor',
        'zrfs1': '/fleurInput/calculationSetup/oneDParams/@zrfs1',
        'zsigma': '/fleurInput/calculationSetup/fields/@zsigma'
    },
    'unique_path_attribs': {
        'a1': ['/fleurInput/cell/bulkLattice/a1', '/fleurInput/cell/filmLattice/a1'],
        'a2': ['/fleurInput/cell/bulkLattice/a2', '/fleurInput/cell/filmLattice/a2'],
        'correlation':
        ['/fleurInput/xcFunctional/LibXCID/@correlation', '/fleurInput/xcFunctional/LibXCName/@correlation'],
        'eig66': ['/fleurInput/calculationSetup/expertModes/@eig66', '/fleurInput/output/@eig66'],
        'ellow': [
            '/fleurInput/calculationSetup/energyParameterLimits/@ellow',
            '/fleurInput/calculationSetup/greensFunction/realAxis/@ellow'
        ],
        'elup': [
            '/fleurInput/calculationSetup/energyParameterLimits/@elup',
            '/fleurInput/calculationSetup/greensFunction/realAxis/@elup'
        ],
        'etot_correlation':
        ['/fleurInput/xcFunctional/LibXCID/@etot_correlation', '/fleurInput/xcFunctional/LibXCName/@etot_correlation'],
        'etot_exchange':
        ['/fleurInput/xcFunctional/LibXCID/@etot_exchange', '/fleurInput/xcFunctional/LibXCName/@etot_exchange'],
        'exchange': ['/fleurInput/xcFunctional/LibXCID/@exchange', '/fleurInput/xcFunctional/LibXCName/@exchange'],
        'itmax': ['/fleurInput/calculationSetup/ldaHIA/@itmax', '/fleurInput/calculationSetup/scfLoop/@itmax'],
        'l_mperp':
        ['/fleurInput/calculationSetup/greensFunction/@l_mperp', '/fleurInput/calculationSetup/nocoParams/@l_mperp'],
        'phi': [
            '/fleurInput/calculationSetup/soc/@phi', '/fleurInput/forceTheorem/DMI/@phi',
            '/fleurInput/forceTheorem/MAE/@phi'
        ],
        'row-1': [
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-1', '/fleurInput/cell/bulkLattice/row-1',
            '/fleurInput/cell/filmLattice/bravaisMatrix/row-1', '/fleurInput/cell/filmLattice/row-1'
        ],
        'row-2': [
            '/fleurInput/cell/bulkLattice/bravaisMatrix/row-2', '/fleurInput/cell/bulkLattice/row-2',
            '/fleurInput/cell/filmLattice/bravaisMatrix/row-2', '/fleurInput/cell/filmLattice/row-2'
        ],
        'row-3':
        ['/fleurInput/cell/bulkLattice/bravaisMatrix/row-3', '/fleurInput/cell/filmLattice/bravaisMatrix/row-3'],
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
        'thetaj': ['/fleurInput/calculationSetup/nocoParams/@thetaJ', '/fleurInput/forceTheorem/Jij/@thetaj']
    }
}
