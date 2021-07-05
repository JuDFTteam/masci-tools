
from masci_tools.util.constants import PERIODIC_TABLE_ELEMENTS, BOHR_A
from masci_tools.util.xml.converters import convert_to_fortran_bool
from masci_tools.io.common_functions import abs_to_rel_f, abs_to_rel, convert_to_fortran_string

# Inpgen file structure, order is important
POSSIBLE_NAMELISTS = [
        'title', 'input', 'lattice', 'gen', 'shift', 'factor', 'qss', 'soc', 'atom', 'comp', 'exco', 'film', 'kpt',
        'end'
    ]
POSSIBLE_PARAMS = {
        'input': ['film', 'cartesian', 'cal_symm', 'checkinp', 'symor', 'oldfleur'],
        'lattice': ['latsys', 'a0', 'a', 'b', 'c', 'alpha', 'beta', 'gamma'],
        'atom': ['id', 'z', 'rmt', 'dx', 'jri', 'lmax', 'lnonsph', 'ncst', 'econfig', 'bmu', 'lo', 'element', 'name'],
        'comp': ['jspins', 'frcor', 'ctail', 'kcrel', 'gmax', 'gmaxxc', 'kmax'],
        'exco': ['xctyp', 'relxc'],
        'film': ['dvac', 'dtild'],
        'soc': ['theta', 'phi'],
        'qss': ['x', 'y', 'z'],
        'kpt': ['nkpt', 'kpts', 'div1', 'div2', 'div3', 'tkb', 'tria'],
        'title': {}
    }


def write_inpgen_file(cell, atoms_dict_list, kind_list, path='inpgen.in', pbc=(True, True, True), input_params=None, settings=None):
    """Write an input file for the fleur inputgenerator 'inpgen' from given inputs

    Args:
        cell (tuple length 3): the bravais matrix of the structure, in Angstrom
        atoms_dict_list (list): list of a dict containing the keys absolute 'position' in Angstrom and 'kind_name', i.e:
                  [{'position': (0.0, 0.0, -1.0545708047819), 'kind_name': 'Fe123'},
                   {'position': (1.4026317387183, 1.9836207751336, 0.0), 'kind_name': 'Pt'},
                   {'position': (0.0, 0.0, 1.4026318234924), 'kind_name': 'Pt'}]
        kind_list (list): a list of kind information containing the keys symbols, weights, mass, name i.e.
                  [{'symbols': ('Fe',), 'weights': (1.0,), 'mass': 55.845, 'name': 'Fe123'},
                   {'symbols': ('Pt',), 'weights': (1.0,), 'mass': 195.084, 'name': 'Pt'}]
        path (str, optional): Path where the file should be written to. Defaults to 'inpgen.in'.
        pbc (tuple length 3, optional): Periodic boundary conditions of the structure. Defaults to (True, True, True).
        input_params (dict, optional): Dict containing further namelist which should be written to the file. Defaults to None.
        settings (dict, optional): Dict, allowing some settings about how the file is written. Defaults to None.

    Raises:
        ValueError: raised if some input is wrong or inconsistent.

    Returns:
        [list]: A report, list of strings, things which where logged within the process

    Comments: This was extracted out of aiida-fleur for more general use, 
    the datastructures stayed very close to what aiida provides (to_raw()), it may not
    yet be convenient for all usecases. I.e data so far has to be given in Angstrom and will be converted to fleur units.
    # This could be made optional
    """

    # Get the connection between coordination number and element symbol
    _atomic_numbers = {data['symbol']: num for num, data in PERIODIC_TABLE_ELEMENTS.items()}

    _settings_keys = [
        'additional_retrieve_list', 'remove_from_retrieve_list', 'cmdline', 'significant_figures_cell',
        'significant_figures_positions'
    ]

    _blocked_keywords = []

    # TODO different kpt mods? (use kpointNode)? aiida-fleur FleurinpdData can do it.
    _use_kpoints = False

    # If two lattices are given, via the input &lattice
    # and a structure of some form
    # currently is not allow the use of &lattice
    _use_aiida_structure = True

    # Default title
    _inp_title = 'A Fleur input generator calculation with aiida'
    bulk = True
    film = False
    report = []

    # convert these 'booleans' to the inpgen format.
    replacer_values_bool = [True, False, 'True', 'False', 't', 'T', 'F', 'f']

    # some keywords require a string " around them in the input file.
    string_replace = ['econfig', 'lo', 'element', 'name', 'xctyp']

    # of some keys only the values are written to the file, specify them here.
    val_only_namelist = ['soc', 'qss']

    # Scaling comes from the Structure
    # but we have to convert from Angstrom to a.u (bohr radii)
    scaling_factors = [1.0, 1.0, 1.0]
    scaling_lat = 1.  # /bohr_to_ang = 0.52917720859
    scaling_pos = 1. / BOHR_A  # Angstrom to atomic
    own_lattice = False  # not _use_aiida_structure

    ##########################################
    ############# INPUT CHECK ################
    ##########################################
    # first check existence of structure and if 1D, 2D, 3D

    if False in pbc:
        bulk = False
        film = True
    
    # check existence of parameters (optional)
    if input_params is None:
        input_params = {}
    
    # we write always out rel coordinates, because thats the way FLEUR uses
    # them best. we have to convert them from abs, because thats how they
    # are stored in a Structure node. cartesian=F is default
    if 'input' in input_params:
        input_params['input']['cartesian'] = False
        if film:
            input_params['input']['film'] = True
    else:
        if bulk:
            input_params['input'] = {'cartesian': False}
        elif film:
            input_params['input'] = {'cartesian': False, 'film': True}

    namelists_toprint = POSSIBLE_NAMELISTS

    if 'title' in list(input_params.keys()):
        _inp_title = input_params.pop('title')

    # TODO validate type of values of the input parameter keys ?
    # check input_parameters
    for namelist, paramdic in input_params.items():
        if 'atom' in namelist:  # this namelist can be specified more often
            # special atom namelist needs to be set for writing,
            #  but insert it in the right spot!
            index = namelists_toprint.index('atom') + 1
            namelists_toprint.insert(index, namelist)
            namelist = 'atom'
        if namelist not in POSSIBLE_NAMELISTS:
            raise ValueError("The namelist '{0}' is not supported by the fleur"
                                       " inputgenerator. Check on the fleur website or add '{0}'"
                                       'to _possible_namelists.'.format(namelist))
        for para in paramdic.keys():
            if para not in POSSIBLE_PARAMS[namelist]:
                raise ValueError("The property '{}' is not supported by the "
                                           "namelist '{}'. "
                                           'Check the fleur website, or if it really is,'
                                           ' update _possible_params. '.format(para, namelist))
            if para in string_replace:
                # TODO check if its in the parameter dict
                paramdic[para] = convert_to_fortran_string(paramdic[para])
            # things that are in string replace can never be a bool
            # Otherwise input where someone given the title 'F' would fail...
            elif paramdic[para] in replacer_values_bool:
                # because 1/1.0 == True, and 0/0.0 == False
                # maybe change in convert_to_fortran that no error occurs
                if isinstance(paramdic[para], (int, float)):
                    if isinstance(paramdic[para], bool):
                        paramdic[para] = convert_to_fortran_bool(paramdic[para])
                else:
                    paramdic[para] = convert_to_fortran_bool(paramdic[para])
        # in fleur it is possible to give a lattice namelist
        if 'lattice' in list(input_params.keys()):
            own_lattice = True
            if cell is not None:  # two structures given?
                # which one should be prepared? TODO: log warning or even error
                if _use_aiida_structure:
                    input_params.pop('lattice', {})
                    own_lattice = False

    # check existence of settings (optional)
    if settings is None:
        settings_dict = {}
    else:
        settings_dict = settings

    # check for for allowed keys, ignore unknown keys but warn.
    for key in settings_dict.keys():
        if key not in _settings_keys:
            report.append('Settings dict key %s for Fleur calculation'
                             'not recognized, only %s are allowed.', key, str(_settings_keys))

    ##############################
    # END OF INITIAL INPUT CHECK #
    ##############################

    #######################################################
    ######### PREPARE PARAMETERS FOR INPUT FILE ###########
    #######################################################

    #### STRUCTURE_PARAMETERS ####
    scaling_factor_card = ''
    cell_parameters_card = ''
    # We allow to set the significant figures format, because sometimes
    # inpgen has numerical problems which are not there with less precise formatting
    sf_c = str(settings_dict.get('significant_figures_cell', 9))
    sf_p = str(settings_dict.get('significant_figure_positions', 10))
    if not own_lattice:
        for vector in cell:
            scaled = [a * scaling_pos for a in vector]  # scaling_pos=1./bohr_to_ang
            reg_string = '{0:18.' + sf_c + 'f} {1:18.' + sf_c + 'f} {2:18.' + sf_c + 'f}\n'
            cell_parameters_card += (reg_string.format(scaled[0], scaled[1], scaled[2]))
        reg_string = '{0:18.' + sf_c + 'f} {1:18.' + sf_c + 'f} {2:18.' + sf_c + 'f}\n'
        scaling_factor_card += (reg_string.format(scaling_factors[0], scaling_factors[1], scaling_factors[2]))

    #### ATOMIC_POSITIONS ####
    atomic_positions_card_list = ['']
    atomic_positions_card_listtmp = ['']
    if not own_lattice:
        natoms = len(atoms_dict_list)
        # for FLEUR true, general not, because you could put several
        # atoms on a site
        # TODO this feature might change in Fleur, do different. that in inpgen kind gets a name, which will also be the name in fleur inp.xml.
        # now user has to make kind_name = atom id.
        for site in atoms_dict_list:
            kind_name = site['kind_name']
            for kin in kind_list:
                if kin['name'] == kind_name:
                    kind = kin
            if kind.get('has_vacancies', False):
                # then we do not at atoms with weights smaller one
                if kind.get('weights', [1])[0] <1.0:                    
                    natoms = natoms -1
                    # Log message?
                    continue
            # We assume atoms therefore I just get the first one... test that only one atom at site?
            site_symbol = kind['symbols'][0]
            atomic_number = _atomic_numbers[site_symbol]
            atomic_number_name = atomic_number
            # per default we use relative coordinates in Fleur
            # we have to scale back to atomic units from angstrom
            pos = site['position']
            if bulk:
                vector_rel = abs_to_rel(pos, cell)
            elif film:
                vector_rel = abs_to_rel_f(pos, cell, pbc)
                vector_rel[2] = vector_rel[2] * scaling_pos
            if site_symbol != kind_name:  # This is an important fact, if user renames it becomes a new atomtype or species!
                try:
                    # Kind names can be more then numbers now, this might need to be reworked
                    head = kind_name.rstrip('0123456789')
                    kind_namet = int(kind_name[len(head):])
                    #if int(kind_name[len(head)]) > 4:
                    #    raise InputValidationError('New specie name/label should start with a digit smaller than 4')
                except ValueError:
                    report.append(
                        'Warning: Kind name {} will be ignored by the FleurinputgenCalculation and not set a charge number.'
                        .format(kind_name))
                else:
                    atomic_number_name = '{}.{}'.format(atomic_number, kind_namet)
                # append a label to the detached atom
                reg_string = '    {0:7} {1:18.' + sf_p + 'f} {2:18.' + sf_p + 'f} {3:18.' + sf_p + 'f} {4}\n'
                atomic_positions_card_listtmp.append(
                    reg_string.format(atomic_number_name, vector_rel[0], vector_rel[1], vector_rel[2], kind_namet))
            else:
                reg_string = '    {0:7} {1:18.' + sf_p + 'f} {2:18.' + sf_p + 'f} {3:18.' + sf_p + 'f}\n'
                atomic_positions_card_listtmp.append(
                    reg_string.format(atomic_number_name, vector_rel[0], vector_rel[1], vector_rel[2]))
        # TODO check format
        # we write it later, since we do not know what natoms is before the loop...
        atomic_positions_card_list.append('    {0:3}\n'.format(natoms))
        for card in atomic_positions_card_listtmp:
            atomic_positions_card_list.append(card)
    else:
        # TODO with own lattice atomic positions have to come from somewhere
        # else.... User input?
        raise ValueError('fleur lattice needs also the atom '
                                   ' position as input,'
                                   ' not implemented yet, sorry!')
    atomic_positions_card = ''.join(atomic_positions_card_list)
    del atomic_positions_card_list  # Free memory

    #### Kpts ####
    # TODO: kpts
    # kpoints_card = ""#.join(kpoints_card_list)
    #del kpoints_card_list


    #######################################
    #### WRITE ALL CARDS IN INPUT FILE ####

    with open(path, 'w') as infile:
        # first write title
        infile.write('{0}\n'.format(_inp_title))
        # then write &input namelist
        infile.write('&{0}'.format('input'))
        # namelist content; set to {} if not present, so that we leave an
        # empty namelist
        namelist = input_params.pop('input', {})
        for k, val in sorted(namelist.items()):
            infile.write(get_input_data_text(k, val, False, mapping=None))
        infile.write('/\n')

        # Write lattice information now
        infile.write(cell_parameters_card)
        infile.write('{0:18.10f}\n'.format(scaling_lat))
        infile.write(scaling_factor_card)
        infile.write('\n')

        # Write Atomic positons
        infile.write(atomic_positions_card)

        # Write namelists after atomic positions
        for namels_name in namelists_toprint:
            namelist = input_params.pop(namels_name, {})
            if namelist:
                if 'atom' in namels_name:
                    namels_name = 'atom'
                infile.write('&{0}\n'.format(namels_name))
                if namels_name in val_only_namelist:
                    make_reversed = False
                    if namels_name == 'soc':
                        make_reversed = True
                    for k, val in sorted(namelist.items(), reverse=make_reversed):
                        infile.write(get_input_data_text(k, val, True, mapping=None))
                else:
                    for k, val in sorted(namelist.items()):
                        infile.write(get_input_data_text(k, val, False, mapping=None))
                infile.write('/\n')
        # infile.write(kpoints_card)

    if input_params:
        raise ValueError('input_params leftover: The following namelists are specified'
                                   ' in input_params, but are '
                                   'not valid namelists for the current type of calculation: '
                                   '{}'.format(','.join(list(input_params.keys()))))

    return report


def get_input_data_text(key, val, value_only, mapping=None):
    """
    Given a key and a value, return a string (possibly multiline for arrays)
    with the text to be added to the input file.

    :param key: the flag name
    :param val: the flag value. If it is an array, a line for each element
            is produced, with variable indexing starting from 1.
            Each value is formatted using the conv_to_fortran function.
    :param mapping: Optional parameter, must be provided if val is a dictionary.
            It maps each key of the 'val' dictionary to the corresponding
            list index. For instance, if ``key='magn'``,
            ``val = {'Fe': 0.1, 'O': 0.2}`` and ``mapping = {'Fe': 2, 'O': 1}``,
            this function will return the two lines ``magn(1) = 0.2`` and
            ``magn(2) = 0.1``. This parameter is ignored if 'val'
            is not a dictionary.
    """
    # I don't try to do iterator=iter(val) and catch TypeError because
    # it would also match strings
    # I check first the dictionary, because it would also match
    # hasattr(__iter__)
    if isinstance(val, dict):
        if mapping is None:
            raise ValueError("If 'val' is a dictionary, you must provide also "
                             "the 'mapping' parameter")

        # At difference with the case of a list, at the beginning
        # list_of_strings
        # is a list of 2-tuples where the first element is the idx, and the
        # second is the actual line. This is used at the end to
        # resort everything.
        list_of_strings = []
        for elemk, itemval in val.items():
            try:
                idx = mapping[elemk]
            except KeyError:
                raise ValueError("Unable to find the key '{}' in the mapping "
                                 "dictionary".format(elemk))

            list_of_strings.append((
                idx, "  {0}({2})={1} ".format(key, conv_to_fortran(itemval), idx)))
                #changed {0}({2}) = {1}\n".format

        # I first have to resort, then to remove the index from the first
        # column, finally to join the strings
        list_of_strings = zip(*sorted(list_of_strings))[1]
        return "".join(list_of_strings)
    elif not isinstance(val, str) and hasattr(val, '__iter__'):
        if value_only:
            list_of_strings = [
                "  ({1}){0} ".format(conv_to_fortran(itemval), idx+1)
                for idx, itemval in enumerate(val)]
        else:
            # a list/array/tuple of values
            list_of_strings = [
                "  {0}({2})={1} ".format(key, conv_to_fortran(itemval),
                                         idx+1)
                for idx, itemval in enumerate(val)]
        return "".join(list_of_strings)
    else:
        # single value
        #return "  {0}={1} ".format(key, conv_to_fortran(val))
        if value_only:
            return " {0} ".format(val)
        else:
            return "  {0}={1} ".format(key, val)

def conv_to_fortran(val, quote_strings=True):
    """
    :param val: the value to be read and converted to a Fortran-friendly string.
    """
    # Note that bool should come before integer, because a boolean matches also
    # isinstance(...,int)
    import numpy
    import numbers

    if isinstance(val, (bool, numpy.bool_)):
        if val:
            val_str = '.true.'
        else:
            val_str = '.false.'
    elif isinstance(val, numbers.Integral):
        val_str = '{:d}'.format(val)
    elif isinstance(val, numbers.Real):
        val_str = ('{:18.10e}'.format(val)).replace('e', 'd')
    elif isinstance(val, str):
        if quote_strings:
            val_str = "'{!s}'".format(val)
        else:
            val_str = '{!s}'.format(val)
    else:
        raise ValueError("Invalid value '{}' of type '{}' passed, accepts only booleans, ints, "
                         'floats and strings'.format(val, type(val)))

    return val_str

'''
def conv_to_fortran(val, quote_strings=True):
    """
    :param val: the value to be read and converted to a Fortran-friendly string.
    """
    # Note that bool should come before integer, because a boolean matches also
    # isinstance(...,int)
    if isinstance(val, (bool, np.bool_)):
        if val:
            val_str = '.true.'
        else:
            val_str = '.false.'
    elif isinstance(val, int):
        val_str = "{:d}".format(val)
    elif isinstance(val, float):
        val_str = ("{:18.10e}".format(val)).replace('e', 'd')
    elif isinstance(val, str):
        if quote_strings:
            val_str = "'{!s}'".format(val)
        else:
            val_str = "{!s}".format(val)
    else:
        raise ValueError("Invalid value '{}' of type '{}' passed, accepts only bools, ints, floats and strings".format(val, type(val)))

    return val_str
'''

def read_inpgen_file(filepath):
    """
    Method which reads in an inpgen input file and parses the structure and name lists information.

    TODO: implement me
    :param filepath (str, path): path to the file to read
    """
    pbc = (True, True, True)
    input_params = {}
    namelists_raw = {}
    kind_list = []
    atoms_dict_list = []
    cell = []
    lattice_information = []

    with open(filepath, 'r') as inpfile:
        contents = inpfile.read()
            
    content_lines = contents.split('\n')
    # The first line is the title
    if not content_lines[0].startswith('&'):
        input_params['title'] = content_lines[0]
    
    content_lines = content_lines[1:]
    if '&lattice' in contents:
        cell = None


    # each line starting with a & is a name list, we can not assume the line will end with a \
    # since this is not fully required
    name_list_start = False
    for i, line in enumerate(content_lines):
        if line.startswith('&'):
            if not name_list_start:
                name_list_start = True
                namelist_name = line.split('&')[1].split()[0]
                namelist_raw = line.split(f'&{namelist_name}')[1]
            else:
                name_list_start = False
        else:
            if name_list_start:
                namelist_raw += line
            else:
                lattice_information.append(line)
        if line.endswith('/'):
            name_list_start = False
            j = 0
            while namelist_name in namelists_raw.keys():
                namelist_name = namelist_name + f'{j}'
            namelists_raw[namelist_name] = namelist_raw
    
    print(lattice_information)
    print(namelists_raw)
    # TODO:
    # parse(namelists_raw)
    # parse(lattice_information, cell)
    # if cell is none the first 5 are the lattice, and scalings
    # everything else it atom information

    for key, val in namelists_raw.items():
        parsed_name_dict = {}
        dict(val)
        for param in val.split():
            if param == '/':
                continue
            pval = param.rstrip('/')
            pval = pval.strip()
            pval = pval.split("=")
            # works for all namelist except gen and sym
            if 'atom' in key:
                keyt = 'atom'
            else:
                keyt = key
            print(pval)
            if pval[0] not in POSSIBLE_PARAMS[keyt]:
                raise ValueError(f'Value {pval[0]} is not allowed as inpgen input of namelist {keyt}.')
            parsed_name_dict[pval[0]] = pval[1]
        input_params[key] = parsed_name_dict
    return cell, atoms_dict_list, kind_list, pbc, input_params