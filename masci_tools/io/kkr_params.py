###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools.   #
# For further information on the license, see the LICENSE.txt file.           #
# For further information please visit http://judft.de/.                      #
#                                                                             #
###############################################################################
"""
In this module you find the kkrparams class that helps defining the KKR input parameters
Also some defaults for the parameters are defined.
"""
import json
import pathlib
from masci_tools.io.common_functions import open_general

# path of this file
_DIR = pathlib.Path(__file__).parent.resolve()

__copyright__ = ('Copyright (c), 2017, Forschungszentrum Jülich GmbH,'
                 'IAS-1/PGI-1, Germany. All rights reserved.')
__license__ = 'MIT license, see LICENSE.txt file'
__version__ = '1.9.0'
__contributors__ = 'Philipp Rüßmann'

# This defines the default parameters for KKR used in the aiida plugin:
__kkr_default_params__ = {
    'LMAX': 3,  # lmax-cutoff
    'INS': 1,  # use shape corrections (full potential)
    'KSHAPE': 2,  # basically the same information as INS (KSHAPE=2*INS should always hold!)
    'NSPIN': 2,  # spin-polarized calculation (but by default not automatically initialized with external field)
    'RMAX': 10.,  # Madelung sum real-space cutoff
    'GMAX': 100.,  # Madelung sum reciprocal-space cutoff
    'RCLUSTZ': 2.3  # size of screening cluster (in alat units)
}

# prevent kkrparams to add brackets around these keywords automatically
# case insensitive (converted to upper case)
__forbid_brackets__ = ['USE_INPUT_ALAT']


class kkrparams:
    """
    Class for creating and handling the parameter input for a KKR calculation
    Optional keyword arguments are passed to init and stored in values dictionary.

    Example usage: params = kkrparams(LMAX=3, BRAVAIS=array([[1,0,0], [0,1,0], [0,0,1]]))

    Alternatively values can be set afterwards either individually with
        params.set_value('LMAX', 3)
    or multiple keys at once with
        params.set_multiple_values(EMIN=-0.5, EMAX=1)

    Other useful functions

    - print the description of a keyword: params.get_description([key]) where [key] is a string for a keyword in params.values
    - print a list of mandatory keywords: params.get_all_mandatory()
    - print a list of keywords that are set including their value: params.get_set_values()

    .. note:
        KKR-units (e.g. atomic units with energy in Ry, length in a_Bohr) are assumed
        except for the keys'<RBLEFT>', '<RBRIGHT>', 'ZPERIODL', and 'ZPERIODR' which should be given in Ang. units!
    """

    def __init__(self, **kwargs):
        """
        Initialize class instance with containing the attribute values that also have
        a format, mandatory flags (defaults for KKRcode, changed for example via params_type='voronoi' keyword) and a description.
        """

        # keywords for KKRhost and voronoi (all allowed keys for inputcard)
        with open(_DIR.joinpath('data_kkrparams/detauls_kkrhost.json'), encoding='utf8') as _f:
            self._DEFAULT_KEYWORDS_KKR = json.load(_f)

        # keywords for KKRimp (all allowed settings for config file)
        with open(_DIR.joinpath('data_kkrparams/detauls_kkrimp.json'), encoding='utf8') as _f:
            self._DEFAULT_KEYS_KKRIMP = json.load(_f)

        # make keys upper case (needed internally to equality comparison)
        self._DEFAULT_KEYWORDS_KKR = {k.upper(): v for k, v in self._DEFAULT_KEYWORDS_KKR.items()}
        self._DEFAULT_KEYS_KKRIMP = {k.upper(): v for k, v in self._DEFAULT_KEYS_KKRIMP.items()}

        if 'params_type' in kwargs:
            self.__params_type = kwargs.pop('params_type')
        else:
            #parameter are set for kkr or voronoi code? (changes mandatory flags)
            self.__params_type = 'kkr'  #default value, also possible: 'voronoi', 'kkrimp'
        valid_types = ['kkr', 'voronoi', 'kkrimp']
        if self.__params_type not in valid_types:
            raise ValueError(f'params_type can only be one of {valid_types} but got {self.__params_type}')

        # initialize keywords dict
        if self.__params_type == 'kkrimp':
            keyw = self._create_keywords_dict_kkrimp(**kwargs)
        else:
            keyw = self._create_keywords_dict(**kwargs)

        #values of keywords:
        self.values = {}
        #formatting info
        self.__format = {}
        #mandatory flag
        self._mandatory = {}
        # description of each key
        self.__description = {}
        self.__listargs = None
        self.__special_formatting = None

        for key, val in keyw.items():
            self.values[key] = val[0]
            self.__format[key] = val[1]
            self._mandatory[key] = val[2]
            self.__description[key] = val[3]

        # update mandatory set for voronoi, kkrimp cases
        self._update_mandatory()

    @classmethod
    def get_KKRcalc_parameter_defaults(cls, silent=False):
        """
        set defaults (defined in header of this file) and returns dict, kkrparams_version
        """
        p = cls()
        for key, val in __kkr_default_params__.items():
            p.set_value(key, val, silent=silent)
        return dict(p.get_set_values()), __version__

    def get_dict(self, group=None, subgroup=None):
        """
        Returns values dictionary.

        Prints values belonging to a certain group only if the 'group' argument
        is one of the following: 'lattice', 'chemistry', 'accuracy',
        'external fields', 'scf cycle', 'other'

        Additionally the subgroups argument allows to print only a subset of
        all keys in a certain group. The following subgroups are available.

        - in 'lattice' group  '2D mode', 'shape functions'
        - in 'chemistry' group 'Atom types', 'Exchange-correlation', 'CPA mode', '2D mode'
        - in 'accuracy' group  'Valence energy contour', 'Semicore energy contour',
          'CPA mode', 'Screening clusters', 'Radial solver',
          'Ewald summation', 'LLoyd'

        """
        out_dict = self.values

        #check for grouping
        group_searchstrings = {
            'lattice': 'Description of lattice',
            'chemistry': 'Chemistry',
            'external fields': 'External fields:',
            'accuracy': 'Accuracy',
            'scf cycle': 'Self-consistency control:',
            'other': ['Running and test options', 'Name of potential and shapefun file']
        }
        subgroups_all = {
            'lattice': ['2D mode', 'shape functions'],
            'chemistry': ['Atom types', 'Exchange-correlation', 'CPA mode', '2D mode'],
            'accuracy': [
                'Valence energy contour', 'Semicore energy contour', 'CPA mode', 'Screening clusters', 'Radial solver',
                'Ewald summation', 'LLoyd'
            ]
        }
        if group in ['lattice', 'chemistry', 'accuracy', 'external fields', 'scf cycle', 'other']:
            print(f'Returning only values belonging to group {group}')
            tmp_dict = {}
            for key in out_dict:
                desc = self.__description[key]
                key_in_group = False
                if group_searchstrings[group] != 'other':
                    if group_searchstrings[group] in desc:
                        key_in_group = True
                else:
                    if group_searchstrings[group][0] in desc or group_searchstrings[group][1] in desc:
                        key_in_group = True
                if key_in_group:
                    tmp_dict[key] = self.values[key]

            #check for subgrouping and overwrite tmp_dict accordingly
            if group in ['lattice', 'chemistry', 'accuracy']:
                if subgroup in subgroups_all[group]:
                    print(f'Restrict keys additionally to subgroup {subgroup}')
                    tmp_dict2 = {}
                    for key in tmp_dict:
                        desc = self.__description[key]
                        key_in_group = False
                        if subgroup in desc:
                            key_in_group = True
                            if key_in_group:
                                tmp_dict2[key] = self.values[key]
                    tmp_dict = tmp_dict2

            # overwrite out_dict with tmp_dict
            out_dict = tmp_dict

        return out_dict

    def _get_type_from_string(self, fmtstr):
        """Helper function of get_type"""
        if 'f' in fmtstr or 'e' in fmtstr:
            keytype = float
        elif 'i' in fmtstr:
            keytype = int
        elif 'l' in fmtstr:
            keytype = bool
        elif 's' in fmtstr:
            keytype = str
        else:
            print('Error: type of keyvalue not found:', fmtstr)
            raise TypeError(f'Type not found for format string: {fmtstr}')
        return keytype

    def get_type(self, key):
        """Extract expected type of 'key' from format info"""
        try:
            fmtstr = self.__format[key]
        except KeyError:
            fmtstr = None
        if fmtstr is not None:
            # simple format or complex pattern
            simplefmt = True
            if fmtstr.count('%') > 1:
                simplefmt = False
            if simplefmt:
                keytype = self._get_type_from_string(fmtstr)
            else:
                fmtlist = fmtstr.replace('\n', '').replace(' ', '').split('%')[1:]
                keytype = []
                for fmtstr in fmtlist:
                    keytype.append(self._get_type_from_string(fmtstr))
            return keytype
        return None

    def _check_valuetype(self, key):
        """Consistency check if type of value matches expected type from format info"""

        # this is the type which is expected
        cmptypes = self.get_type(key)

        # check if entry is numpy array and change to list automatically:
        try:
            tmpval = self.values[key].flatten().tolist()
        except:  # pylint: disable=bare-except
            tmpval = self.values[key]
        tmptype = type(tmpval)

        # get type of value
        if tmptype == list:
            valtype = []
            for index, val in enumerate(tmpval):
                if cmptypes == str:
                    tmpval[index] = str(val)  # for pytho2/3 compatibility
                valtype.append(type(val))
        else:
            if cmptypes == str:
                tmpval = str(tmpval)  # for pytho2/3 compatibility
                tmptype = type(tmpval)
            valtype = tmptype
        #print(key, valtype, self.get_type(key))

        # check if type matches format info
        success = True
        if cmptypes is not None:
            #print(key, type(valtype), valtype, cmptypes)
            changed_type_automatically = False
            if valtype == int and cmptypes == float:
                changed_type_automatically = True
                self.values[key] = float(self.values[key])
            elif isinstance(valtype, list):
                for index, current_type in enumerate(valtype):
                    if current_type == int and cmptypes == float:
                        changed_type_automatically = True
                        self.values[key][index] = float(self.values[key][index])
            elif valtype != cmptypes and tmpval is not None:
                success = False
                print('Error: type of value does not match expected type for ', key, self.values[key], cmptypes,
                      type(self.values[key]), valtype)
                raise TypeError(
                    'type of value does not match expected type for key={}; value={}; expected type={}; got type={}'.
                    format(key, self.values[key], cmptypes, type(self.values[key])))

            if changed_type_automatically:
                print(
                    'Warning: filling value of "%s" with integer but expects float. Converting automatically and continue'
                    % key)

        return success

    def get_value(self, key):
        """Gets value of keyword 'key'"""
        if key not in self.values:
            print(f'Error key ({key}) not found in values dict! {self.values}')
            raise KeyError

        # deal with special cases of runopt and testopt (lists of codewords)
        if key in ['RUNOPT', 'TESTOPT'] and self.values[key] is None:
            return []
        return self.values[key]

    def set_value(self, key, value, silent=False):
        """Sets value of keyword 'key'"""
        if value is None:
            if not silent:
                print('Warning setting value None is not permitted!')
                print(f'Use remove_value function instead! Ignore keyword {key}')
        else:
            key = key.upper()  # make case insensitive
            if self.__params_type == 'kkrimp' and key == 'XC':
                value = self.change_XC_val_kkrimp(value)
            self.values[key] = value
            self._check_valuetype(key)

    def remove_value(self, key):
        """Removes value of keyword 'key', i.e. resets to None"""
        self.values[key] = None

    def set_multiple_values(self, **kwargs):
        """Set multiple values (in example value1 and value2 of keywords 'key1' and 'key2') given as key1=value1, key2=value2"""
        for key, val in kwargs.items():
            key2 = self._add_brackets_to_key(key, self.values)
            #print('setting', key2, kwargs[key])
            self.set_value(key2, val)

    def get_set_values(self):
        """Return a list of all keys/values that are set (i.e. not None)"""
        set_values = [[key, val] for key, val in self.values.items() if val is not None]
        if not set_values:
            print('No values set')
        return set_values

    def get_all_mandatory(self):
        """Return a list of mandatory keys"""
        self._update_mandatory()
        return [key for key in self.values if self.is_mandatory(key)]

    def is_mandatory(self, key):
        """Returns mandatory flag (True/False) for keyword 'key'"""
        return self._mandatory[key]

    def get_description(self, key=None, search=None):  # pylint: disable=inconsistent-return-statements
        """
        Returns description of keyword 'key'
        If 'key' is None, print all descriptions of all available keywords
        If 'search' is not None, print all keys+descriptions where the search string is found
        """
        if key is not None:
            return self.__description[key]
        for key2 in self.values:
            if search is None or search.lower() in key2.lower() or search.lower() in self.__description[key2].lower():
                print(f'{key2:25}', self.__description[key2])

    def _create_keywords_dict(self, **kwargs):
        """
        Creates KKR inputcard keywords dictionary and fills entry if value is given in **kwargs

        entries of keyword dictionary are: 'keyword', [value, format, keyword_mandatory, description]

        where

        - 'value' can be a single entry or a list of entries
        - 'format' contains formatting info
        - 'keyword_mandatory' is a logical stating if keyword needs to be defined to run a calculation
        - 'description' is a string containing human redable info about the keyword
        """

        default_keywords = self._DEFAULT_KEYWORDS_KKR

        for key, val in kwargs.items():
            key2 = self._add_brackets_to_key(key, default_keywords)
            if self.__params_type == 'kkrimp':
                if key == 'KEXCORE':
                    key2 = 'XC'
                if key == 'R_LOG':
                    key2 = 'RADIUS_LOGPANELS'
                if key == 'STRMIX':
                    key2 = 'MIXFAC'
                if key == 'RUNOPT':
                    key2 = 'RUNFLAG'
                if key == 'TESTOPT':
                    key2 = 'TESTFLAG'
                if key == 'NSTEPS':
                    key2 = 'SCFSTEPS'
            # workaround to fix inconsistency of XC input between host and impurity code
            if self.__params_type == 'kkrimp' and key2 == 'XC':
                kwargs[key] = self.change_XC_val_kkrimp(val)
            # enforce upper case for key2
            key2 = key2.upper()

            default_keywords[key2][0] = val

        return default_keywords

    def _update_mandatory(self):
        """Check if mandatory flags need to be updated if certain keywords are set"""
        # initialize all mandatory flags to False and update list afterwards
        for key in self.values:
            self._mandatory[key] = False

        runopts = []
        if self.values.get('RUNOPT', None) is not None:
            for runopt in self.values['RUNOPT']:
                runopts.append(runopt.strip())

        #For a KKR calculation these keywords are always mandatory:
        mandatory_list = ['ALATBASIS', 'BRAVAIS', 'NAEZ', '<RBASIS>', 'NSPIN', 'LMAX', 'RMAX', 'GMAX', '<ZATOM>']

        if self.values.get('NPOL', None) is not None and self.values['NPOL'] != 0:
            mandatory_list += ['EMIN']
        #Mandatory in 2D
        if self.values.get('INTERFACE', None):
            mandatory_list += ['<NLBASIS>', '<RBLEFT>', 'ZPERIODL', '<NRBASIS>', '<RBRIGHT>', 'ZPERIODR']
        #Mandatory in LDA+U
        if 'NAT_LDAU' in self.values and 'LDAU' in runopts:
            mandatory_list += ['NAT_LDAU', 'LDAU_PARA']
        #Mandatory in CPA
        if self.values.get('NATYP', None) is not None and self.values['NATYP'] > self.values['NAEZ']:
            mandatory_list += ['NATYP', '<SITE>', '<CPA-CONC>']
        #Mandatory in SEMICORE
        if 'EBOTSEMI' in self.values and 'SEMICORE' in runopts:
            mandatory_list += ['EBOTSEMI', 'EMUSEMI', 'TKSEMI', 'NPOLSEMI', 'N1SEMI', 'N2SEMI', 'N3SEMI', 'FSEMICORE']
        if self.values['INS'] == 1 and 'WRITEALL' not in runopts:
            mandatory_list += ['<SHAPE>']

        for key in mandatory_list:
            self._mandatory[key] = True

        # overwrite if mandatory list needs to be changed (determined from value of self.__params_type):
        if self.__params_type == 'voronoi':
            self._update_mandatory_voronoi()
        if self.__params_type == 'kkrimp':
            self._update_mandatory_kkrimp()

    def _check_mandatory(self):
        """Check if all mandatory keywords are set"""
        self._update_mandatory()
        for key, value in self.values.items():
            if self.is_mandatory(key) and value is None:
                print('Error not all mandatory keys are set!')
                set_of_mandatory = set(self.get_all_mandatory())
                set_of_keys = {key[0] for key in self.get_set_values()}
                print(set_of_mandatory - set_of_keys, 'missing')
                raise ValueError(f'Missing mandatory key(s): {set_of_mandatory - set_of_keys}')

    def _check_array_consistency(self):
        """Check all keys in __listargs if they match their specification (mostly 1D array, except for special cases e.g. <RBASIS>)"""
        from numpy import array, ndarray

        vec3_entries = ['<RBASIS>', '<RBLEFT>', '<RBRIGHT>', 'ZPERIODL', 'ZPERIODR']

        #success = [True]
        for key, listarg in self.__listargs.items():
            if self.values[key] is not None:
                tmpsuccess = True
                if self.verbose:
                    print('checking', key, self.values[key], self.__listargs[key])  # pylint: disable=unnecessary-dict-index-lookup
                if not isinstance(self.values[key], (list, ndarray)):
                    self.values[key] = array([self.values[key]])
                if isinstance(listarg, tuple):
                    cmpdims = listarg
                else:
                    cmpdims = (listarg,)
                if key in vec3_entries:
                    cmpdims = (listarg, 3)
                    # automatically convert if naez==1 and only 1D array is given
                    if listarg == 1 and len(array(self.values[key]).shape) == 1 and key not in ['ZPERIODL', 'ZPERIODR']:
                        print(f'Warning: expected 2D array for {key} but got 1D array, converting automatically')
                        self.values[key] = array([self.values[key]])
                tmpdims = array(self.values[key]).shape
                if tmpdims[0] != cmpdims[0]:
                    tmpsuccess = False
                if len(tmpdims) == 2 and tmpdims[1] != cmpdims[1]:
                    tmpsuccess = False
                #success.append(tmpsuccess)

                if not tmpsuccess:
                    print('check consistency:', key, self.values[key], cmpdims, tmpdims, tmpsuccess)
                    raise TypeError(f'Error: array input not consistent for key {key}')

    def _check_input_consistency(self, set_lists_only=False, verbose=False):
        """Check consistency of input, to be done before wrinting to inputcard"""
        from numpy import array

        self.verbose = verbose  # pylint: disable=attribute-defined-outside-init

        # first check if all mandatory values are there
        if not set_lists_only:
            self._check_mandatory()

        # lists of array arguments
        if self.__params_type != 'kkrimp':
            keywords = self.values
            naez = keywords['NAEZ']
            if keywords['NATYP'] is not None:
                natyp = keywords['NATYP']
            else:
                natyp = keywords['NAEZ']
            if keywords['<NLBASIS>'] is not None:
                nlbasis = keywords['<NLBASIS>']
            else:
                nlbasis = 1
            if keywords['<NRBASIS>'] is not None:
                nrbasis = keywords['<NRBASIS>']
            else:
                nrbasis = 1
            lmax = keywords['LMAX']
            num_triplet = keywords['<BDG_NUM_TRIPLET_CHANNELS>']

            #yapf: disable
            listargs = dict([
                ['BZDIVIDE', 3], ['ZPERIODL', 3], ['ZPERIODR', 3], ['LDAU_PARA', 5],
                ['CPAINFO', 2], ['<DELTAE>', 2], ['FILES', 2], ['DECIFILES', 2]
            ])
            if naez is not None:
                for key in ['<RBASIS>',  '<RMTCORE>',  '<MTWAU>',  '<MTWAL>']:
                    listargs[key] = naez
            if natyp is not None:
                for key in ['<SHAPE>', '<ZATOM>', '<SOCSCL>', '<SITE>', '<CPA-CONC>', 'XINIPOL', '<RMTREF>', '<FPRADIUS>', '<AT_SCALE_BDG>', '<PHASE_BDG>']:
                    listargs[key] = natyp
            if nlbasis is not None:
                for key in ['<RBLEFT>', '<KAOEZL>', '<RMTREFL>', '<RBLEFT>', '<LFMTWAU>', '<LFMTWAL>']:
                    listargs[key] = nlbasis
            if nrbasis is not None:
                for key in ['<RBRIGHT>', '<KAOEZR>', '<RMTREFR>', '<RBRIGHT>', '<RTMTWAU>', '<RTMTWAL>']:
                    listargs[key] = nrbasis
            if lmax is not None:
                listargs['<LM_SCALE_BDG>'] = (lmax + 1)**2
            if num_triplet is not None:
                listargs['<BDG_TRIPLET_LAMBDAS>'] = (num_triplet, 4)
                listargs['<BDG_TRIPLET_DVEC>'] = (num_triplet, 3)
                listargs['<BDG_TRIPLET_DELTA0>'] = num_triplet
            #yapf: enable

            # deal with special stuff for voronoi:
            if self.__params_type == 'voronoi':
                listargs['<RMTCORE>'] = naez
                self.update_to_voronoi()
            special_formatting = ['BRAVAIS', 'RUNOPT', 'TESTOPT', 'FILES', 'DECIFILES', 'JIJSITEI', 'JIJSITEJ']
        else:
            special_formatting = ['RUNFLAG', 'TESTFLAG']
            listargs = dict([['HFIELD', 2]])

        self.__special_formatting = special_formatting
        self.__listargs = listargs
        print('listargs:', listargs)
        print('special_formatting:', special_formatting)

        # ruturn after setting __special_formatting and __listargs lists
        if set_lists_only:
            return

        # check for consistency of array arguments
        self._check_array_consistency()

        if self.__params_type != 'kkrimp':
            # some special checks
            bulkmode = False
            set_values = [key[0] for key in self.get_set_values()]
            if 'INTERFACE' not in set_values or self.values['INTERFACE']:
                bulkmode = True

            bravais = array(self.values['BRAVAIS'])
            if bulkmode and sum(bravais[2]**2) == 0:
                print("Error: 'BRAVAIS' matches 2D calculation but 'INTERFACE' is not set to True!")
                raise ValueError

            # check if KSHAPE and INS are consistent and add missing values automatically
            # WARNING: KSHAPE should be 2*INS !!!
            if 'INS' not in set_values and 'KSHAPE' in set_values:
                self.set_value('INS', self.get_value('KSHAPE') // 2)
                print(f"setting INS automatically with KSHAPE value ({self.get_value('KSHAPE') // 2})")
            elif 'INS' in set_values and 'KSHAPE' not in set_values:
                self.set_value('KSHAPE', self.get_value('INS') * 2)
                print(f"setting KSHAPE automatically with INS value ({self.get_value('INS') * 2})")
            elif 'INS' in set_values and 'KSHAPE' in set_values:
                ins = self.get_value('INS')
                kshape = self.get_value('KSHAPE')
                if (ins != 0 and kshape == 0) or (ins == 0 and kshape != 0):
                    print(
                        "Error: values of 'INS' and 'KSHAPE' are both found but are inconsistent (should be 0/0 or 1/2)"
                    )
                    raise ValueError('INS,KSHAPE mismatch')

    def fill_keywords_to_inputfile(self, is_voro_calc=False, output='inputcard', no_check=False, verbose=False):
        """
        Fill new inputcard with keywords/values
        automatically check for input consistency (can be disabled by the no_check input)
        if is_voro_calc==True change mandatory list to match voronoi code, default is KKRcode
        """
        from numpy import array

        # first check input consistency
        if is_voro_calc:
            self.__params_type = 'voronoi'

        # check for inconsistencies in input before writing file
        self._check_input_consistency(set_lists_only=no_check, verbose=verbose)

        #rename for easy reference
        keywords = self.values
        keyfmts = self.__format

        if self.__params_type != 'kkrimp':
            sorted_keylist = [  #run/testopts
                'RUNOPT',
                'TESTOPT',
                #lattice:
                'ALATBASIS',
                'BRAVAIS',
                'NAEZ',
                'CARTESIAN',
                '<RBASIS>',
                'INTERFACE',
                '<NLBASIS>',
                '<RBLEFT>',
                'ZPERIODL',
                '<NRBASIS>',
                '<RBRIGHT>',
                'ZPERIODR',
                'KSHAPE',
                '<SHAPE>',
                # chemistry
                'NSPIN',
                'KVREL',
                'KEXCOR',
                'LAMBDA_XC',
                'NAT_LDAU',
                'LDAU_PARA',
                'KREADLDAU',
                '<ZATOM>',
                '<SOCSCL>',
                'NATYP',
                '<SITE>',
                '<CPA-CONC>',
                '<KAOEZL>',
                '<KAOEZR>',
                # external fields
                'LINIPOL',
                'HFIELD',
                'XINIPOL',
                'VCONST',
                # accuracy
                'LMAX',
                'BZDIVIDE',
                'EMIN',
                'EMAX',
                'TEMPR',
                'NPT1',
                'NPT2',
                'NPT3',
                'NPOL',
                'EBOTSEMI',
                'EMUSEMI',
                'TKSEMI',
                'NPOLSEMI',
                'N1SEMI',
                'N2SEMI',
                'N3SEMI',
                'FSEMICORE',
                'CPAINFO',
                'RCLUSTZ',
                'RCLUSTXY',
                '<RMTREF>',
                'NLEFTHOS',
                '<RMTREFL>',
                'NRIGHTHO',
                '<RMTREFR>',
                'INS',
                'ICST',
                'R_LOG',
                'NPAN_LOG',
                'NPAN_EQ',
                'NCHEB',
                '<FPRADIUS>',
                'RMAX',
                'GMAX',
                '<LLOYD>',
                '<DELTAE>',
                '<TOLRDIF>',
                # scf cycle
                'NSTEPS',
                'IMIX',
                'STRMIX',
                'ITDBRY',
                'FCM',
                'BRYMIX',
                'QBOUND',
                #file names
                'FILES',
                'DECIFILES'
            ]
        else:
            sorted_keylist = [
                'RUNFLAG', 'TESTFLAG', 'INS', 'KVREL', 'NSPIN', 'SCFSTEPS', 'IMIX', 'ITDBRY', 'MIXFAC', 'BRYMIX',
                'QBOUND', 'XC', 'ICST', 'SPINORBIT', 'NCOLL', 'NPAN_LOGPANELFAC', 'RADIUS_LOGPANELS', 'RADIUS_MIN',
                'NPAN_LOG', 'NPAN_EQ', 'NCHEB', 'HFIELD', 'CALCORBITALMOMENT', 'CALCFORCE', 'CALCJIJMAT'
            ]

        #add everything that was forgotten in sorted_keylist above
        for key in list(keywords.keys()):
            if key not in sorted_keylist:
                sorted_keylist += [key]

        # set accuracy of float writeouts
        # ensure high enough precision in inputcard writeout, limit to 12 places everything else is overkill
        for key in list(keyfmts.keys()):
            keyfmts[key] = keyfmts[key].replace('%f', '%21.12f')

        # write all set keys to file
        tmpl = ''
        for key in sorted_keylist:
            if keywords[key] is not None:
                if verbose:
                    print('writing', key, keywords[key])
                # go through different formatting options (first normal case then special cases)
                if key not in self.__listargs and key not in self.__special_formatting:
                    tmpfmt = keyfmts[key].replace('%l', '%s')
                    try:
                        if self.__params_type == 'kkrimp' and key == 'XC':
                            # workaround to fix inconsistency of XC input between host and impurity code
                            keywords[key] = self.change_XC_val_kkrimp(keywords[key])
                        repltxt = tmpfmt % (keywords[key])
                    except:  # pylint: disable=bare-except
                        #print(key, tmpfmt, keywords[key])
                        repltxt = ''
                        for index, fmt in enumerate(tmpfmt):
                            repltxt += ' ' + fmt % (keywords[key][index])
                    tmpl += f'{key}= {repltxt}\n'
                elif key == 'BRAVAIS':
                    self.values[key] = array(self.values[key])
                    tmpl += ('BRAVAIS\n' + keyfmts[key] +
                             '\n') % (self.values[key][0, 0], self.values[key][0, 1], self.values[key][0, 2],
                                      self.values[key][1, 0], self.values[key][1, 1], self.values[key][1, 2],
                                      self.values[key][2, 0], self.values[key][2, 1], self.values[key][2, 2])
                elif key == 'RUNOPT':
                    runops = keywords[key]
                    tmpl += 'RUNOPT\n'
                    for op in runops:
                        nblanks = 8 - len(op)
                        if nblanks < 0:
                            print(f'WARNING for replacement of RUNOPTION {op}: too long?')
                            print(f'RUNOPT {op} is ignored and was not set!')
                        else:
                            op = op + ' ' * nblanks
                        tmpl += op
                    tmpl += '\n'
                elif key == 'TESTOPT':
                    testops = keywords[key]
                    tmpl += 'TESTOPT\n'
                    for index, op in enumerate(testops):
                        nblanks = 8 - len(op)
                        if nblanks < 0:
                            print(f'WARNING for replacement of TESTOPTION {op}: too long?')
                            print(f'TESTOPT {op} is ignored and was not set!')
                        else:
                            op = op + ' ' * nblanks
                        tmpl += op
                        if index == 8:
                            tmpl += '\n'
                    tmpl += '\n'
                elif key == 'XINIPOL':
                    tmpl += f'{key}='
                    for ival in range(len(self.values[key])):
                        tmpl += f' {keyfmts[key]}' % self.values[key][ival]
                    tmpl += '\n'
                elif key == 'FILES':
                    files_changed = 0
                    if self.values[key][0] == '':
                        self.values[key][0] = 'potential'
                    else:
                        files_changed += 1
                    if self.values[key][1] == '':
                        self.values[key][1] = 'shapefun'
                    else:
                        files_changed += 1
                    if files_changed > 0 or 'DECIFILES' in self.values:  # force writing FILES line if DECIFILES should be set
                        if files_changed > 0:
                            print(
                                'Warning: Changing file name of potential file to "%s" and of shapefunction file to "%s"'
                                % (self.values[key][0], self.values[key][1]))
                        tmpl += 'FILES\n'
                        tmpl += '\n'
                        tmpl += f'{self.values[key][0]}\n'
                        tmpl += '\n'
                        tmpl += f'{self.values[key][1]}\n'
                        tmpl += 'scoef\n'
                elif key == 'DECIFILES':
                    tmpl += 'DECIFILES\n'
                    tmpl += f'{self.values[key][0]}\n'
                    tmpl += f'{self.values[key][1]}\n'
                elif key in ['JIJSITEI', 'JIJSITEJ']:
                    tmpl += f'{key}= '
                    jijsite = self.values[key]
                    tmpl += '%i ' % jijsite[0]
                    for isite in range(jijsite[0]):
                        tmpl += '%i ' % jijsite[1 + isite]
                    tmpl += '\n'
                elif self.__params_type == 'kkrimp' and key == 'RUNFLAG' or key == 'TESTFLAG':
                    # for kkrimp
                    ops = keywords[key]
                    tmpl += f'{key}='
                    if ops:
                        tmpl += ' ' + ' '.join(map(str, ops))
                    tmpl += '\n'
                elif key in self.__listargs:
                    if verbose:
                        print('key is in listargs', key)

                    # keys that have array values
                    if key in ['<RBASIS>', '<RBLEFT>',
                               '<RBRIGHT>']:  # RBASIS needs special formatting since three numbers are filled per line
                        tmpl += f'{key}\n'
                        for ival in range(self.__listargs[key]):
                            tmpl += (keyfmts[key] + '\n') % (self.values[key][ival][0], self.values[key][ival][1],
                                                             self.values[key][ival][2])
                    elif key in ['<BDG_TRIPLET_LAMBDAS>']:  # 4 values per line
                        tmpl += f'{key}\n'
                        for ival in range(self.__listargs[key][0]):
                            tmpl += ('  ' + keyfmts[key] +
                                     '\n') % (self.values[key][ival][0], self.values[key][ival][1],
                                              self.values[key][ival][2], self.values[key][ival][3])
                    elif key in ['<BDG_TRIPLET_DVEC>']:  # 3 values per line
                        tmpl += f'{key}\n'
                        for ival in range(self.__listargs[key][0]):
                            tmpl += ('  ' + keyfmts[key] + '\n') % (
                                self.values[key][ival][0], self.values[key][ival][1], self.values[key][ival][2])
                    elif key in ['CPAINFO', '<DELTAE>']:
                        tmpl += f'{key}= '
                        tmpl += (keyfmts[key] + '\n') % (self.values[key][0], self.values[key][1])
                    elif key in ['BZDIVIDE', 'ZPERIODL', 'ZPERIODR']:
                        tmpl += f'{key}= '
                        tmpl += (keyfmts[key] + '\n') % (self.values[key][0], self.values[key][1], self.values[key][2])
                    elif key in ['LDAU_PARA']:
                        tmpl += f'{key}= '
                        tmpl += (keyfmts[key] + '\n') % (self.values[key][0], self.values[key][1], self.values[key][2],
                                                         self.values[key][3], self.values[key][4])
                    elif self.__params_type == 'kkrimp' and key in ['HFIELD']:  # for kkrimp
                        tmpl += f'{key}= '
                        tmpl += (keyfmts[key] + '\n') % (self.values[key][0], self.values[key][1])
                    else:
                        #print(key, self.__listargs[key], len(self.values[key]))
                        tmpl += f'{key}\n'
                        for ival in range(self.__listargs[key]):
                            tmpl += (keyfmts[key] + '\n') % (self.values[key][ival])
                else:
                    print(f'Error trying to write keyword {key} but writing failed!')
                    raise ValueError

                # to make inputcard more readable insert some blank lines after certain keys
                if self.__params_type == 'kkrimp':
                    breaklines = ['TESTFLAG', 'NSPIN', 'QBOUND', 'NCHEB', 'HFIELD']
                else:
                    breaklines = [
                        'TESTOPT', 'CARTESIAN', '<RBASIS>', 'ZPERIODL', 'ZPERIODR', '<SHAPE>', 'KREADLDAU', '<ZATOM>',
                        '<SOCSCL>', '<CPA-CONC>', '<KAOEZR>', 'VCONST', 'BZDIVIDE', 'FSEMICORE', 'CPAINFO', 'RCLUSTXY',
                        '<RMTREF>', '<RMTREFR>', 'ICST', '<FPRADIUS>', 'GMAX', '<TOLRDIF>', 'QBOUND'
                    ]
                if key in breaklines:
                    tmpl += '\n'

        # finally write to file
        with open_general(output, 'w') as f:
            f.write(tmpl)

    def read_keywords_from_inputcard(self, inputcard='inputcard', verbose=False):
        """
        Read list of keywords from inputcard and extract values to keywords dict

        :example usage: p = kkrparams(); p.read_keywords_from_inputcard('inputcard')
        :note: converts '<RBLEFT>', '<RBRIGHT>', 'ZPERIODL', and 'ZPERIODR' automatically to Ang. units!
        """
        from numpy import shape, array
        from masci_tools.io.common_functions import get_aBohr2Ang

        debug = False
        if verbose:
            print(f'start reading {inputcard}')
            debug = True

        with open_general(inputcard, 'r') as f:
            txt = f.readlines()
        keywords = self.values
        keyfmts = self.__format

        #TODO loop over known keywords and fill with values found in inputcard
        # first read array dimensions
        read_first = ['NAEZ', 'NATYP', '<NLBASIS>', '<NRBASIS>', 'LMAX']
        read_already = []
        for key in read_first:
            valtxt = self._find_value(key, txt, debug=debug)
            if valtxt is None:  # try to read key without '<', '>'
                valtxt = self._find_value(key.replace('<', '').replace('>', ''), txt, debug=debug)
            # now set value in kkrparams
            if valtxt is not None:
                value = self.get_type(key)(valtxt)
                self.set_value(key, value)
                read_already.append(key)

        # then set self.__special_formatting and self.__listargs in _check_input_consistency
        # needs NAEZ, NATYP, NLBASIS, NRBASIS to be set to get array dimensions correct
        self._check_input_consistency(set_lists_only=True, verbose=verbose)

        # try to read keywords from inputcard and fill self.values
        for key in keywords:
            if key not in read_already:
                item, num = 1, 1  # starting column and number of columns that are read in

                if keyfmts[key].count('%') > 1:
                    num = keyfmts[key].count('%')

                if key not in self.__special_formatting:
                    # determine if more than one line is read in
                    if key in self.__listargs and key not in ['ZPERIODL', 'ZPERIODR', 'BZDIVIDE']:
                        itmp = self.__listargs[key]
                        if itmp is None:
                            itmp = 0
                        lines = list(range(1, itmp + 1))
                    else:
                        lines = [1]
                else:  # special formatting keys
                    if key == 'RUNOPT':
                        lines = [1]
                        num = 8
                        keyfmts[key] = '%s%s%s%s%s%s%s%s'
                    elif key == 'TESTOPT':
                        lines = [1, 2]
                        num = 8
                        keyfmts[key] = '%s%s%s%s%s%s%s%s'
                    elif key == 'BRAVAIS':
                        lines = [1, 2, 3]
                        num = 3
                        keyfmts[key] = '%f %f %f'
                    elif key == 'BZDIVIDE':
                        lines = [1]
                        num = 3
                        keyfmts[key] = '%f'
                    elif key == 'FILES':
                        lines = [2, 4]
                        num = 1
                        keyfmts[key] = '%s'
                    elif key == 'DECIFILES':
                        lines = [1, 2]
                        num = 1
                        keyfmts[key] = '%s'
                # read in all lines for this key
                values = []
                for iline in lines:
                    valtxt = self._find_value(key, txt, iline, item, num, debug=debug)
                    if valtxt is not None:
                        # first deal with run and testopts (needs to spearate keys)
                        if key in ('RUNOPT', 'TESTOPT'):
                            valtxt = self.split_kkr_options(valtxt)
                        # then continue with valtxt
                        if isinstance(valtxt, list):
                            tmp = []
                            for index, value in enumerate(valtxt):
                                tmptype = self.get_type(key)[index]
                                if tmptype == float and ('d' in value or 'D' in value):
                                    valtxt[index] = value.replace('d', 'e').replace('D', 'e')
                                tmp.append(tmptype(value))
                        else:
                            tmptype = self.get_type(key)
                            if tmptype == float and ('d' in valtxt or 'D' in valtxt):
                                valtxt = valtxt.replace('d', 'e').replace('D', 'e')
                            if tmptype == bool:
                                if valtxt.upper() in ['F', 'FALSE', '.FALSE.', 'NO', '0']:
                                    valtxt = ''  # only empty string evaluates to False!!!
                                else:
                                    valtxt = 'True'
                            tmp = tmptype(valtxt)
                        values.append(tmp)
                if len(values) == 1:
                    values = values[0]

                if key == 'TESTOPT':  # flatten list
                    if shape(values)[0] == 2 and isinstance(values[0], list):
                        tmp = []
                        for itmp in values:
                            for ii in itmp:
                                tmp.append(ii)
                        values = tmp

                # finally set values in kkrparams object
                if values != []:
                    self.set_value(key, values)

        # finally check if some input of the old style was given and read it in
        natyp = self.get_value('NATYP')
        if natyp is None:
            if debug:
                print('set NATYP=NAEZ')
            natyp = self.get_value('NAEZ')

        # look for old RBASIS input style
        if self.get_value('<RBASIS>') is None:
            if debug:
                print('look for RBASIS instead of <RBASIS>')
            rbasis = []
            for iatom in range(natyp):
                rbasis.append([float(i) for i in self._find_value('RBASIS', txt, 1 + iatom, 1, 3, debug=debug)])
            self.set_value('<RBASIS>', rbasis)

        # look for old atominfo input style
        atominfo_c = self._find_value('ATOMINFOC', txt, 2, debug=debug)
        if atominfo_c is None:
            atominfo_c = False
        else:
            atominfo_c = True
        atominfo = self._find_value('ATOMINFO', txt, 2, debug=debug)
        if atominfo is None:
            atominfo = False
        else:
            atominfo = True
        tmp = []
        if atominfo_c:
            if debug:
                print('read ATOMINFOC')
            for iatom in range(natyp):
                tmp.append(self._find_value('ATOMINFOC', txt, 2 + iatom, 1, 14, debug=debug))
        elif atominfo:
            if debug:
                print('read ATOMINFO')
            for iatom in range(natyp):
                tmp.append(self._find_value('ATOMINFO', txt, 2 + iatom, 1, 12, debug=debug))
        if atominfo_c or atominfo:
            tmp = array(tmp)
            cls_list = [int(i) for i in tmp[:, 6]]
            self.set_multiple_values(ZATOM=[float(i) for i in tmp[:, 0]],
                                     SHAPE=[int(i) for i in tmp[:, 8]],
                                     RMTREF=[float(i) for i in tmp[:, 11]])
            if atominfo_c:
                self.set_value('SITE', [int(i) for i in tmp[:, 12]])
                self.set_value('<CPA-CONC>', [float(i) for i in tmp[:, 13]])
        else:
            cls_list = list(range(1, natyp + 1))

        # look for old left/right basis input style
        if self.get_value('INTERFACE'):
            leftbasis = self._find_value('LEFTBASIS', txt, debug=debug)
            if leftbasis is None:
                leftbasis = False
            else:
                leftbasis = True
                nlbasis = self.get_value('<NLBASIS>')
            rightbasis = self._find_value('RIGHBASIS', txt, debug=debug)  # RIGHBASIS is no typo!!
            if rightbasis is None:
                rightbasis = False
            else:
                rightbasis = True
                nrbasis = self.get_value('<NRBASIS>')
            if leftbasis:
                tmp = []
                for iatom in range(nlbasis):
                    tmp.append(self._find_value('LEFTBASIS', txt, 1 + iatom, 1, 5, debug=debug))
                tmp = array(tmp)
                self.set_multiple_values(RBLEFT=[[float(i[j]) for j in range(3)] for i in tmp[:, 0:3]],
                                         KAOEZL=[int(i) for i in tmp[:, 3]])
                tmp2 = []
                for icls in tmp[:, 3]:
                    rmtref = self.get_value('<RMTREF>')[cls_list.index(int(icls))]
                    tmp2.append(rmtref)
                self.set_value('<RMTREFL>', tmp2)
            if rightbasis:
                tmp = []
                for iatom in range(nrbasis):
                    tmp.append(self._find_value('RIGHBASIS', txt, 1 + iatom, 1, 5, debug=debug))
                tmp = array(tmp)
                self.set_multiple_values(RBRIGHT=[[float(i[j]) for j in range(3)] for i in tmp[:, 0:3]],
                                         KAOEZR=[int(i) for i in tmp[:, 3]])
                tmp2 = []
                for icls in tmp[:, 3]:
                    rmtref = self.get_value('<RMTREF>')[cls_list.index(int(icls))]
                    tmp2.append(rmtref)
                self.set_value('<RMTREFR>', tmp2)

        # convert RBLEFT etc. from alat units to Ang. units (this is assumed in generate_inputcard)
        rbl = self.get_value('<RBLEFT>')
        rbr = self.get_value('<RBRIGHT>')
        zper_l = self.get_value('ZPERIODL')
        zper_r = self.get_value('ZPERIODR')
        alat2ang = self.get_value('ALATBASIS')
        if alat2ang is not None:
            alat2ang *= get_aBohr2Ang()
        if rbl is not None:
            self.set_value('<RBLEFT>', array(rbl) * alat2ang)
        if rbr is not None:
            self.set_value('<RBRIGHT>', array(rbr) * alat2ang)
        if zper_l is not None:
            self.set_value('ZPERIODL', array(zper_l) * alat2ang)
        if zper_r is not None:
            self.set_value('ZPERIODR', array(zper_r) * alat2ang)

        if debug:
            print(f'extracted parameters: {self.get_set_values()}')

    def _find_value(self, charkey, txt, line=1, item=1, num=1, debug=False):
        """
        Search charkey in txt and return value string

        parameter, input :: charkey         string that is search in txt
        parameter, input :: txt             text that is searched (output of readlines)
        parameter, input, optional :: line  index in which line to start reading after key was found
        parameter, input, optional :: item  index which column is read
        parameter, input, optional :: num   number of column that are read

        returns :: valtxt                   string or list of strings depending on num setting
        """
        if debug:
            print(f'find_value: {charkey}')
        try:
            iline = [ii for ii in range(len(txt)) if charkey in txt[ii]][0]
        except IndexError:
            iline = None
        if iline is not None:
            txtline = txt[iline]
            chkeq = charkey + '='
            if chkeq in txtline:
                valtxt = txtline.split(chkeq)[1].split()[item - 1:item - 1 + num]
            else:
                nextline = txt[iline + line]
                startpos = txtline.index(charkey)
                valtxt = nextline[startpos:].split()[item - 1:item - 1 + num]
            if debug:
                print(f'find_value found {valtxt}')
            if num == 1:
                return valtxt[0]
            return valtxt
        return None

    # redefine _update_mandatory for voronoi code
    def _update_mandatory_voronoi(self):
        """Change mandatory flags to match requirements of voronoi code"""
        # initialize all mandatory flags to False and update list afterwards
        for key in list(self.values.keys()):
            self._mandatory[key] = False

        runopts = []
        if self.values['RUNOPT'] is not None:
            for runopt in self.values['RUNOPT']:
                runopts.append(runopt.strip())

        #For a KKR calculation these keywords are always mandatory:
        mandatory_list = ['ALATBASIS', 'BRAVAIS', 'NAEZ', '<RBASIS>', 'NSPIN', 'LMAX', 'RCLUSTZ', '<ZATOM>']

        #Mandatory in 2D
        if self.values['INTERFACE']:
            mandatory_list += ['<NLBASIS>', '<RBLEFT>', 'ZPERIODL', '<NRBASIS>', '<RBRIGHT>', 'ZPERIODR']
        #Mandatory in CPA
        if self.values['NATYP'] is not None and self.values['NATYP'] > self.values['NAEZ']:
            mandatory_list += ['NATYP', '<SITE>', '<CPA-CONC>']

        for key in mandatory_list:
            self._mandatory[key] = True

    # redefine _update_mandatory for kkrim code
    def _update_mandatory_kkrimp(self):
        """Change mandatory flags to match requirements of kkrimp code"""
        # initialize all mandatory flags to False and update list afterwards
        for key in list(self.values.keys()):
            self._mandatory[key] = False

        runopts = []
        if self.values.get('RUNOPT', None) is not None:
            for runopt in self.values['RUNOPT']:
                runopts.append(runopt.strip())

        #For a KKR calculation these keywords are always mandatory:
        mandatory_list = []

        for key in mandatory_list:
            self._mandatory[key] = True

    def get_missing_keys(self, use_aiida=False):
        """Find list of mandatory keys that are not yet set"""
        setlist = list(dict(self.get_set_values()).keys())
        manlist = self.get_all_mandatory()
        missing = []
        autoset_list = ['BRAVAIS', '<RBASIS>', '<ZATOM>', 'ALATBASIS', 'NAEZ', '<SHAPE>', 'EMIN', 'RCLUSTZ']
        if self.__params_type == 'voronoi':
            autoset_list = ['BRAVAIS', '<RBASIS>', '<ZATOM>', 'ALATBASIS', 'NAEZ']
        for key in manlist:
            if key not in setlist:
                if not use_aiida:
                    missing.append(key)
                else:
                    if key not in autoset_list:
                        missing.append(key)
        return missing

    def update_to_voronoi(self):
        """
        Update parameter settings to match voronoi specification.
        Sets self.__params_type and calls _update_mandatory_voronoi()
        """
        self.__params_type = 'voronoi'
        self._update_mandatory_voronoi()

    def update_to_kkrimp(self):
        """
        Update parameter settings to match kkrimp specification.
        Sets self.__params_type and calls _update_mandatory_kkrimp()
        """
        self.__params_type = 'kkrimp'
        self._update_mandatory_kkrimp()

    def _create_keywords_dict_kkrimp(self, **kwargs):
        """
        Like create_keywords_dict but for changed keys of impurity code
        """

        default_keywords = self._DEFAULT_KEYS_KKRIMP

        for key, val in kwargs.items():
            key2 = self._add_brackets_to_key(key, default_keywords)
            default_keywords[key2][0] = val

        return default_keywords

    @staticmethod
    def split_kkr_options(valtxt):
        """
        Split keywords after fixed length of 8
        :param valtxt: list of strings or single string
        :returns: List of keywords of maximal length 8
        """
        if not isinstance(valtxt, list):
            valtxt = [valtxt]
        valtxt_tmp = []
        for itmp in valtxt:
            if len(itmp) > 8:
                Nsplitoff = int(len(itmp) // 8)
                for ii in range(Nsplitoff):
                    itmp_splitoff = itmp[ii * 8:(ii + 1) * 8]
                    valtxt_tmp.append(itmp_splitoff)
                itmp_splitoff = itmp[Nsplitoff * 8:]
                valtxt_tmp.append(itmp_splitoff)
            else:
                valtxt_tmp.append(itmp)
        valtxt = valtxt_tmp
        return valtxt

    def items(self):
        """make kkrparams.items() work"""
        return list(self.get_dict().items())

    def change_XC_val_kkrimp(self, val):
        """Convert integer value of KKRhost KEXCOR input to KKRimp XC string input."""
        if isinstance(val, int):
            if val == 0:
                val = 'LDA-MJW'
            if val == 1:
                val = 'LDA-vBH'
            if val == 2:
                val = 'LDA-VWN'
            if val == 3:
                val = 'GGA-PW91'
            if val == 4:
                val = 'GGA-PBE'
            if val == 5:
                val = 'GGA-PBEsol'
        return val

    def _add_brackets_to_key(self, key, key_dict):
        """Put '<' and '>' around the key expect for special keys defined in `__forbid_brackets__` list."""

        if self.__params_type == 'kkrimp':
            # skip this for the parameters for KKRimp
            return key

        key2 = key
        if key.upper() not in key_dict and key.upper() not in __forbid_brackets__:
            key2 = '<' + key + '>'

        return key2
