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
Here I collect all functions needed to parse the output of a KKR calculation.
These functions do not need aiida and are therefore separated from the actual
parser file where parse_kkr_outputfile is called
"""
import numpy as np
from numpy import ndarray, array, loadtxt, shape
from masci_tools.io.common_functions import (search_string, get_version_info, angles_to_vec,
                                             get_corestates_from_potential, get_highest_core_state, convert_to_pystd,
                                             get_outfile_txt)
from masci_tools.io.common_functions import get_Ry2eV
import traceback

__copyright__ = ('Copyright (c), 2017, Forschungszentrum Jülich GmbH,'
                 'IAS-1/PGI-1, Germany. All rights reserved.')
__license__ = 'MIT license, see LICENSE.txt file'
__contributors__ = 'Philipp Rüßmann'
__version__ = '1.8.1'

####################################################################################


def parse_array_float(outfile, searchstring, splitinfo, replacepair=None, debug=False):
    """
    Search for keyword `searchstring` in `outfile` and extract array of results

    .. note:
        `splitinfo` can be of the form [1, 'X', 1] or [2, 'X', 1, 0] where
        splitinfo[0] can only be 1 or 2 (determines the mode),
        splitinfo[1] is the string at which the line is split,
        splitinfo[2] is the index which is used,
        splitinfo[3] (only for splitinfo[0]==2) is the part that is taken after applying split() a second time (split at whitespace).

    .. note:
        If `replacepair` is not None the substring replacepair[0] is replaced by replacepair[1] before processing further

    Returns: array of results

    """
    tmptxt = get_outfile_txt(outfile)
    itmp = 0
    res = []
    while itmp >= 0:
        itmp = search_string(searchstring, tmptxt)
        if debug:
            print(('in parse_array_float (itmp, searchstring, outfile):', itmp, searchstring, outfile))
        if itmp >= 0:
            tmpval = tmptxt.pop(itmp)
            if replacepair is not None:
                tmpval = tmpval.replace(replacepair[0], replacepair[1])
            if splitinfo[0] == 1:
                tmpval = float(tmpval.split(splitinfo[1])[splitinfo[2]])
            elif splitinfo[0] == 2:
                tmpval = float(tmpval.split(splitinfo[1])[splitinfo[2]].split()[splitinfo[3]])
            else:
                raise ValueError('splitinfo[0] has to be either 1 or 2')
            res.append(tmpval)
    res = array(res)
    return res


def get_rms(outfile, outfile2, debug=False):
    """
    Get rms error per atom (both values for charge and spin) and total (i.e. average) value
    """
    if debug:
        print((outfile, outfile2))
    rms_charge = parse_array_float(outfile, 'average rms-error', [2, '=', 1, 0], ['D', 'E'], debug=debug)
    if debug:
        print(rms_charge)
    rms_spin = parse_array_float(
        outfile, 'v+ - v-', [1, '=', 1],
        ['D', 'E'])  # this should be in the line after 'average rms-error' but is only present if NSPIN==2
    if debug:
        print(rms_spin)
    rms_charge_atoms = parse_array_float(outfile2, 'rms-error for atom', [2, '=', 1, 0], ['D', 'E'])
    if debug:
        print(rms_charge_atoms)
    rms_spin_atoms = parse_array_float(outfile2, 'rms-error for atom', [2, '=', 1, 0],
                                       ['D', 'E'])  # only present for NSPIN==2
    if debug:
        print(rms_spin_atoms)
    niter = len(rms_charge)  # number of iterations
    if debug:
        print(niter)
    natoms = int(len(rms_charge_atoms) //
                 niter)  # number of atoms in system, needed to take only atom resolved rms of last iteration
    if debug:
        print(natoms)
    return rms_charge, rms_spin, rms_charge_atoms[-natoms:], rms_spin_atoms[-natoms:]


def get_noco_rms(outfile, debug=False):
    """
    Get average noco rms error
    """
    if debug:
        print(outfile)
    try:
        rms_noco = parse_array_float(outfile, 'Total RMS(angles)', [1, ':', 1], debug=debug)
    except:  # pylint: disable=bare-except
        rms_noco = []
        if debug:
            traceback.print_exc()
    return rms_noco


def get_neutr(outfile):
    res = parse_array_float(outfile, 'charge neutrality in unit cell', [1, '=', 1])
    return res


def get_magtot(outfile):
    res = parse_array_float(outfile, 'TOTAL mag. moment in unit cell', [1, '=', 1])
    return res


def get_EF(outfile):
    res = parse_array_float(outfile, 'E FERMI', [2, 'FERMI', 1, 0])
    return res


def get_DOS_EF(outfile):
    res = parse_array_float(outfile, 'DOS(E_F)', [1, '=', 1])
    return res


def get_Etot(outfile):
    res = parse_array_float(outfile, 'TOTAL ENERGY in ryd.', [1, ':', 1])
    return res


def find_warnings(outfile):
    tmptxt = get_outfile_txt(outfile)
    tmptxt_caps = [txt.upper() for txt in tmptxt]
    itmp = 0
    res = []
    while itmp >= 0:
        itmp = search_string('WARNING', tmptxt_caps)
        if itmp >= 0:
            tmpval = tmptxt_caps.pop(itmp)
            tmpval = tmptxt.pop(itmp)
            res.append(tmpval.strip())
    return array(res)


def extract_timings(outfile):
    tmptxt = get_outfile_txt(outfile)
    itmp = 0
    res = []
    search_keys = [
        'main0',
        'main1a - tbref',
        'main1a  ',  # two spaces to differentiate from following key
        'main1b - calctref13',
        'main1b  ',  # two spaces!
        'main1c - serial part',
        'main1c  ',  # two spaces!
        'main2',
        'Time in Iteration'
    ]
    while itmp >= 0:
        tmpvals = []
        for isearch in search_keys:
            itmp = search_string(isearch, tmptxt)
            if itmp >= 0:
                tmpval = [isearch, float(tmptxt.pop(itmp).split()[-1])]
                tmpvals.append(tmpval)
        if len(tmpvals) > 0:
            res.append(tmpvals)
    res = res[0]
    return dict(res)


def get_charges_per_atom(outfile_000):
    res1 = parse_array_float(outfile_000, 'charge in wigner seitz', [1, '=', 1])
    # these two are not in output of DOS calculation (and are then ignored)
    res2 = parse_array_float(outfile_000, 'nuclear charge', [2, 'nuclear charge', 1, 0])
    try:
        res3 = parse_array_float(outfile_000, 'core charge', [1, '=', 1])
    except IndexError:
        res3 = parse_array_float(outfile_000, 'core charge', [1, ':', 1])
    return res1, res2, res3


def get_single_particle_energies(outfile_000):
    """
    extracts single particle energies from outfile_000 (output.000.txt)
    returns the valence contribution of the single particle energies
    """
    tmptxt = get_outfile_txt(outfile_000)
    itmp = 0
    res = []
    while itmp >= 0:
        itmp = search_string('band energy per atom', tmptxt)
        if itmp >= 0:
            tmpval = float(tmptxt.pop(itmp).split()[-1])
            res.append(tmpval)
    return array(res)


def get_econt_info(outfile_0init):
    tmptxt = get_outfile_txt(outfile_0init)

    itmp = search_string('E min', tmptxt)
    emin = float(tmptxt[itmp].split('min')[1].split('=')[1].split()[0])

    itmp = search_string('Temperature', tmptxt)
    tempr = float(tmptxt[itmp].split('Temperature')[1].split('=')[1].split()[0])

    itmp = search_string('Number of energy points', tmptxt)
    Nepts = int(tmptxt[itmp].split(':')[1].split()[0])

    doscalc = search_string('Density-of-States calculation', tmptxt)
    semi_circ = search_string('integration on semi-circle contour', tmptxt)

    # dummy values
    N1, N2, N3, Npol = None, None, None, None
    Nsemi_circ, im_e_min = None, None

    # for DOS contour
    if doscalc == -1:
        # scf contour
        if semi_circ == -1:
            # npol
            itmp = search_string('poles =', tmptxt)
            Npol = int(tmptxt[itmp].split('=')[1].split()[0])
            # npt1, npt2, npt3
            itmp = search_string('contour:', tmptxt)
            tmp = tmptxt[itmp].replace(',', '').replace('=', '= ').split(':')[1].split()
            N1 = int(tmp[2])
            N2 = int(tmp[5])
            N3 = int(tmp[8])
        else:
            # semi-circular contour
            Nsemi_circ = Nepts
            itmp = search_string('smallest imaginary part ', tmptxt)
            im_e_min = tmptxt[itmp].split('=')[1].split()[0]
    else:
        # DOS contour
        Npol, N1, N2, N3 = 0, 0, Nepts, 0

    return emin, tempr, Nepts, Npol, N1, N2, N3, Nsemi_circ, im_e_min


def get_core_states(potfile):
    ncore, energies, lmoments = get_corestates_from_potential(potfile=potfile)
    emax, lmax, descr_max = [], [], []
    for ipot, nc in enumerate(ncore):
        if nc > 0:
            lvalmax, energy_max, descr = get_highest_core_state(nc, energies[ipot], lmoments[ipot])
        else:
            lvalmax, energy_max, descr = None, None, 'no core states'
        emax.append(energy_max)
        lmax.append(lvalmax)
        descr_max.append(descr)
    return array(ncore), array(emax), array(lmax), array(descr_max)


def get_alatinfo(outfile_0init):
    tmptxt = get_outfile_txt(outfile_0init)
    itmp = search_string('Lattice constants :', tmptxt)
    alat = float(tmptxt[itmp].split(':')[1].split('=')[1].split()[0])
    twopialat = float(tmptxt[itmp].split(':')[1].split('=')[2].split()[0])
    return alat, twopialat


def get_scfinfo(outfile_0init, outfile_000, outfile):
    tmptxt = get_outfile_txt(outfile_000)

    itmp = search_string('ITERATION :', tmptxt)
    tmpval = tmptxt[itmp].split(':')[1].split()
    niter = int(tmpval[0])
    nitermax = int(tmpval[3])

    tmptxt = get_outfile_txt(outfile)
    itmp1 = search_string('SCF ITERATION CONVERGED', tmptxt)
    itmp2 = search_string('NUMBER OF SCF STEPS EXHAUSTED', tmptxt)
    converged = itmp1 >= 0
    nmax_reached = itmp2 >= 0

    tmptxt = get_outfile_txt(outfile_0init)
    itmp = search_string('STRMIX        FCM       QBOUND', tmptxt)
    tmpval = tmptxt[itmp + 1].split()
    strmix = float(tmpval[0])
    fcm = float(tmpval[1])
    qbound = float(tmpval[2])
    tmpval = tmptxt[itmp + 4].split()
    brymix = float(tmpval[0])
    itmp = search_string('IMIX    IGF    ICC', tmptxt)
    imix = int(tmptxt[itmp + 1].split()[0])
    idtbry = int(tmptxt[itmp + 4].split()[0])

    mixinfo = [imix, strmix, qbound, fcm, idtbry, brymix]

    return niter, nitermax, converged, nmax_reached, mixinfo


def get_kmeshinfo(outfile_0init, outfile_000):
    """
    Extract kmesh info from output.0.txt and output.000.txt
    """
    # first get info from output.0.txt
    tmptxt = get_outfile_txt(outfile_0init)
    nkmesh = []
    itmp = search_string('number of different k-meshes', tmptxt)
    nkmesh.append(int(tmptxt[itmp].split(':')[1].split()[0]))
    itmp = search_string('NofKs', tmptxt)
    nofks, nkx, nky, nkz = [], [], [], []
    if itmp >= 0:
        for ik in range(nkmesh[0]):
            tmpval = tmptxt[itmp + 2 + ik].split()
            nofks.append(int(tmpval[1]))
            nkx.append(int(tmpval[2]))
            nky.append(int(tmpval[3]))
            nkz.append(int(tmpval[4]))

    tmpdict = {'number_of_kpts': nofks, 'n_kx': nkx, 'n_ky': nky, 'n_kz': nkz}
    nkmesh.append(tmpdict)

    #next get kmesh_ie from output.000.txt
    tmptxt = get_outfile_txt(outfile_000)
    kmesh_ie = []
    itmp = 0
    while itmp >= 0:
        itmp = search_string('KMESH =', tmptxt)
        if itmp >= 0:
            tmpval = int(tmptxt.pop(itmp).split()[-1])
            kmesh_ie.append(tmpval)

    return nkmesh, kmesh_ie


def get_symmetries(outfile_0init):
    tmptxt = get_outfile_txt(outfile_0init)
    try:
        itmp = search_string('symmetries found for this lattice:', tmptxt)
        nsym = int(tmptxt[itmp].split(':')[1].split()[0])
    except IndexError:
        itmp = search_string('< FINDGROUP > : Finding symmetry operations', tmptxt)
        tmptxt2 = tmptxt[itmp:]
        itmp = search_string('found for this lattice:', tmptxt2)
        nsym = int(tmptxt2[itmp].split(':')[1].split()[0])
    itmp = search_string('symmetries will be used', tmptxt)
    nsym_used = int(tmptxt[itmp].split()[3])
    itmp = search_string('<SYMTAUMAT>', tmptxt)
    tmpdict = {}
    for isym in range(nsym_used):
        tmpval = tmptxt[itmp + 5 + isym].replace('0-',
                                                 '0 -').replace('1-',
                                                                '1 -').split()  # bugfix for -120 degree euler angle
        desc = tmpval[1]
        inversion = int(tmpval[2])
        euler = [float(tmpval[3]), float(tmpval[4]), float(tmpval[5])]
        unitary = int(tmpval[6].replace('T', '1').replace('F', '0'))
        tmpdict[desc] = {'has_inversion': inversion, 'is_unitary': unitary, 'euler_angles': euler}
    desc = tmpdict
    return nsym, nsym_used, desc


def get_ewald(outfile_0init):
    tmptxt = get_outfile_txt(outfile_0init)
    itmp = search_string('setting bulk Madelung coefficients', tmptxt)
    if itmp >= 0:
        info = '3D'
    else:
        info = '2D'
    if info == '3D':
        itmp = search_string('< LATTICE3D >', tmptxt)
        tmpval = tmptxt[itmp + 7].split()[2:]
        rsum = float(tmpval[2]), int(tmpval[0]), int(tmpval[1])
        tmpval = tmptxt[itmp + 8].split()[2:]
        gsum = float(tmpval[2]), int(tmpval[0]), int(tmpval[1])
    else:
        itmp = search_string('< LATTICE2D >', tmptxt)
        tmpval = tmptxt[itmp + 13].split()[2:]
        rsum = float(tmpval[2]), int(tmpval[0]), int(tmpval[1])
        tmpval = tmptxt[itmp + 14].split()[2:]
        gsum = float(tmpval[2]), int(tmpval[0]), int(tmpval[1])
    return rsum, gsum, info


def get_nspin(outfile_0init):
    """
    extract NSPIN value from output.0.txt
    """
    tmptxt = get_outfile_txt(outfile_0init)
    itmp = search_string('NSPIN', tmptxt)
    nspin = int(tmptxt[itmp + 1].split()[0])
    return nspin


def get_natom(outfile_0init):
    """
    extract NATYP value from output.0.txt
    """
    tmptxt = get_outfile_txt(outfile_0init)
    itmp = search_string('NATYP', tmptxt)
    natom = int(tmptxt[itmp + 1].split()[0])
    return natom


def use_newsosol(outfile_0init):
    """
    extract NEWSOSOL info from output.0.txt
    """
    tmptxt = get_outfile_txt(outfile_0init)
    newsosol = False
    # old style (RUNOPT output)
    itmp = search_string('NEWSOSOL', tmptxt)
    if itmp >= 0 and 'NEWSOSOL' in tmptxt[itmp].upper():
        newsosol = True
    itmp = search_string('<use_Chebychev_solver>=', tmptxt)
    # new style: check for output of runoptions
    if itmp >= 0:
        if tmptxt[itmp].split()[1][:1].upper() == 'T':
            newsosol = True
        if tmptxt[itmp].split()[1][:1].upper() == 'F':
            newsosol = False
    return newsosol


def use_BdG(outfile_0init):
    """
    extract BdG run info from output.0.txt
    """
    tmptxt = get_outfile_txt(outfile_0init)
    val_use_BdG = False
    itmp = search_string('<use_BdG>=', tmptxt)
    if itmp >= 0:
        if tmptxt[itmp].split()[1][:1].upper() == 'T':
            val_use_BdG = True
        if tmptxt[itmp].split()[1][:1].upper() == 'F':
            val_use_BdG = False
    return val_use_BdG


def get_spinmom_per_atom(outfile, natom, nonco_out_file=None):
    """
    Extract spin moment information from outfile and nonco_angles_out (if given)
    """
    tmptxt = get_outfile_txt(outfile)
    itmp = 0
    result = []
    while itmp >= 0:
        itmp = search_string('m_spin', tmptxt)
        if itmp >= 0:
            tmpline = tmptxt.pop(itmp)
            tmparray = []
            for iatom in range(natom):
                tmpline = tmptxt.pop(itmp)
                tmparray.append(float(tmpline.split()[3]))
            result.append(tmparray)

    # if the file is there, i.e. NEWSOSOL is used, then extract also direction of spins (angles theta and phi)
    if nonco_out_file is not None and result:
        angles = loadtxt(nonco_out_file, usecols=[0, 1])  # make sure only theta and phi are read in
        if len(shape(angles)) == 1:
            angles = array([angles])
        vec = angles_to_vec(result[-1], angles[:, 0] / 180. * np.pi, angles[:, 1] / 180. * np.pi)
    else:
        vec, angles = [], []

    return array(result), vec, angles


def get_orbmom(outfile, natom):
    """
    read orbmom info from outfile and return array (iteration, atom)=orbmom
    """
    tmptxt = get_outfile_txt(outfile)
    itmp = 0
    result = []
    while itmp >= 0:
        itmp = search_string('m_spin', tmptxt)
        if itmp >= 0:
            tmpline = tmptxt.pop(itmp)
            tmparray = []
            for iatom in range(natom):
                tmpline = tmptxt.pop(itmp)
                tmparray.append(float(tmpline.split()[4]))
            result.append(tmparray)

    return array(result)  #, vec, angles


def get_lattice_vectors(outfile_0init):
    """
    read direct and reciprocal lattice vectors in internal units (useful for qdos generation)
    """
    tmptxt = get_outfile_txt(outfile_0init)
    vecs, rvecs = [], []
    tmpvecs = []
    for search_txt in ['a_1: ', 'a_2: ', 'a_3: ', 'b_1: ', 'b_2: ', 'b_3: ']:
        itmp = search_string(search_txt, tmptxt)
        if itmp >= 0:
            tmpvec = tmptxt[itmp].split(':')[1].split()
            tmpvecs.append([float(tmpvec[0]), float(tmpvec[1]), float(tmpvec[1])])
        if search_txt in ['a_3: ', 'b_3: '] and itmp < 0:
            # reset vecs for 2D case
            tmpvecs[0] = tmpvecs[0][:2]
            tmpvecs[1] = tmpvecs[1][:2]
        if search_txt == 'a_3: ':
            vecs = tmpvecs
            tmpvecs = []
        elif search_txt == 'b_3: ':
            rvecs = tmpvecs
    return vecs, rvecs


def parse_kkr_outputfile(out_dict,
                         outfile,
                         outfile_0init,
                         outfile_000,
                         timing_file,
                         potfile_out,
                         nonco_out_file,
                         outfile_2='output.2.txt',
                         skip_readin=False,
                         debug=False):
    """
    Parser method for the kkr outfile. It returns a dictionary with results
    """
    # scaling factors etc. defined globally
    doscalc = False

    # collection of parsing error messages
    msg_list = []

    try:
        code_version, compile_options, serial_number = get_version_info(outfile)
        tmp_dict = {}
        tmp_dict['code_version'] = code_version
        tmp_dict['compile_options'] = compile_options
        tmp_dict['calculation_serial_number'] = serial_number
        out_dict['code_info_group'] = tmp_dict
    except:  # pylint: disable=bare-except
        msg = 'Error parsing output of KKR: Version Info'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        nspin = get_nspin(outfile_0init)
        natom = get_natom(outfile_0init)
        newsosol = use_newsosol(outfile_0init)
        out_dict['nspin'] = nspin
        out_dict['number_of_atoms_in_unit_cell'] = natom
        out_dict['use_newsosol'] = newsosol
    except:  # pylint: disable=bare-except
        msg = 'Error parsing output of KKR: nspin/natom'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        # extract some BdG infos
        out_dict['use_BdG'] = use_BdG(outfile_0init)
    except:  # pylint: disable=bare-except
        msg = 'Error parsing output of KKR: BdG'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        result = find_warnings(outfile)
        tmp_dict = {}
        tmp_dict['number_of_warnings'] = len(result)
        tmp_dict['warnings_list'] = result
        out_dict['warnings_group'] = tmp_dict
    except:  # pylint: disable=bare-except
        msg = 'Error parsing output of KKR: search for warnings'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        result = extract_timings(timing_file)
        out_dict['timings_group'] = result
        out_dict['timings_unit'] = 'seconds'
    except:  # pylint: disable=bare-except
        msg = 'Error parsing output of KKR: timings'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        emin, tempr, Nepts, Npol, N1, N2, N3, Nsemi_circ, im_e_min = get_econt_info(outfile_0init)
        tmp_dict = {}
        tmp_dict['emin'] = emin
        tmp_dict['emin_unit'] = 'Rydberg'
        tmp_dict['number_of_energy_points'] = Nepts
        if Nsemi_circ is None:
            # normal scf or DOS contour
            tmp_dict['temperature'] = tempr
            tmp_dict['temperature_unit'] = 'Kelvin'
            tmp_dict['npol'] = Npol
            tmp_dict['n1'] = N1
            tmp_dict['n2'] = N2
            tmp_dict['n3'] = N3
        else:
            # semi-circle contour
            tmp_dict['im_e_min'] = im_e_min
            tmp_dict['im_e_min_unit'] = 'Ry'
        # now fill energy contour group
        out_dict['energy_contour_group'] = tmp_dict
        if Npol == 0:
            doscalc = True
    except:  # pylint: disable=bare-except
        msg = 'Error parsing output of KKR: energy contour'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        alat, twopioveralat = get_alatinfo(outfile_0init)
        out_dict['alat_internal'] = alat
        out_dict['two_pi_over_alat_internal'] = twopioveralat
        out_dict['alat_internal_unit'] = 'a_Bohr'
        out_dict['two_pi_over_alat_internal_unit'] = '1/a_Bohr'
    except:  # pylint: disable=bare-except
        msg = 'Error parsing output of KKR: alat, 2*pi/alat'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        nkmesh, kmesh_ie = get_kmeshinfo(outfile_0init, outfile_000)
        tmp_dict = {}
        tmp_dict['number_different_kmeshes'] = nkmesh[0]
        tmp_dict['number_kpoints_per_kmesh'] = nkmesh[1]
        tmp_dict['kmesh_energypoint'] = kmesh_ie
        out_dict['kmesh_group'] = tmp_dict
    except:  # pylint: disable=bare-except
        msg = 'Error parsing output of KKR: kmesh'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        nsym, nsym_used, desc = get_symmetries(outfile_0init)
        tmp_dict = {}
        tmp_dict['number_of_lattice_symmetries'] = nsym
        tmp_dict['number_of_used_symmetries'] = nsym_used
        tmp_dict['symmetry_description'] = desc
        out_dict['symmetries_group'] = tmp_dict
    except:  # pylint: disable=bare-except
        msg = 'Error parsing output of KKR: symmetries'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    if not doscalc:  # in case of dos calculation no ewald summation is done
        try:
            rsum, gsum, info = get_ewald(outfile_0init)
            tmp_dict = {}
            tmp_dict['ewald_summation_mode'] = info
            tmp_dict['rsum_cutoff'] = rsum[0]
            tmp_dict['rsum_number_of_vectors'] = rsum[1]
            tmp_dict['rsum_number_of_shells'] = rsum[2]
            tmp_dict['rsum_cutoff_unit'] = 'a_Bohr'
            tmp_dict['gsum_cutoff'] = gsum[0]
            tmp_dict['gsum_number_of_vectors'] = gsum[1]
            tmp_dict['gsum_number_of_shells'] = gsum[2]
            tmp_dict['gsum_cutoff_unit'] = '1/a_Bohr'
            out_dict['ewald_sum_group'] = tmp_dict
        except:  # pylint: disable=bare-except
            msg = 'Error parsing output of KKR: ewald summation for madelung poterntial'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

    try:
        bv, recbv = get_lattice_vectors(outfile_0init)
        out_dict['direct_bravais_matrix'] = bv
        out_dict['reciprocal_bravais_matrix'] = recbv
        out_dict['direct_bravais_matrix_unit'] = 'alat'
        out_dict['reciprocal_bravais_matrix_unit'] = '2*pi / alat'
    except:  # pylint: disable=bare-except
        msg = 'Error parsing output of KKR: lattice vectors (direct/reciprocal)'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    # this is skipped for qdos run for example
    if not skip_readin and not doscalc:
        try:
            ncore, emax, lmax, descr_max = get_core_states(potfile_out)
            tmp_dict = {}
            tmp_dict['number_of_core_states_per_atom'] = ncore
            tmp_dict['energy_highest_lying_core_state_per_atom'] = emax
            tmp_dict['energy_highest_lying_core_state_per_atom_unit'] = 'Rydberg'
            tmp_dict['descr_highest_lying_core_state_per_atom'] = descr_max
            out_dict['core_states_group'] = tmp_dict
        except:  # pylint: disable=bare-except
            msg = 'Error parsing output of KKR: core_states'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        tmp_dict = {}  # used to group convergence info (rms, rms per atom, charge neutrality)
        # also initialize convegence_group where all info stored for all iterations is kept
        out_dict['convergence_group'] = tmp_dict
        try:
            rms_charge, rms_spin, result_atoms_last_charge, result_atoms_last_spin = get_rms(outfile,
                                                                                             outfile_000,
                                                                                             debug=debug)
            tmp_dict['rms'] = rms_charge[-1]
            tmp_dict['rms_all_iterations'] = rms_charge
            tmp_dict['rms_per_atom'] = result_atoms_last_charge
            if len(rms_spin) > 0:
                tmp_dict['rms_spin'] = rms_spin[-1]
            else:
                tmp_dict['rms_spin'] = None
            tmp_dict['rms_spin_all_iterations'] = rms_spin
            tmp_dict['rms_spin_per_atom'] = result_atoms_last_spin
            tmp_dict['rms_unit'] = 'unitless'
            out_dict['convergence_group'] = tmp_dict
        except:  # pylint: disable=bare-except
            msg = 'Error parsing output of KKR: rms-error'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            result = get_neutr(outfile)
            tmp_dict['charge_neutrality'] = result[-1]
            out_dict['convergence_group']['charge_neutrality_all_iterations'] = result
            tmp_dict['charge_neutrality_unit'] = 'electrons'
            out_dict['convergence_group'] = tmp_dict
        except:  # pylint: disable=bare-except
            msg = 'Error parsing output of KKR: charge neutrality'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        tmp_dict = {}  # used to group magnetism info (spin and orbital moments)
        try:
            result = get_magtot(outfile)
            if len(result) > 0:
                tmp_dict['total_spin_moment'] = result[-1]
                out_dict['convergence_group']['total_spin_moment_all_iterations'] = result
                tmp_dict['total_spin_moment_unit'] = 'mu_Bohr'
                out_dict['magnetism_group'] = tmp_dict
        except:  # pylint: disable=bare-except
            msg = 'Error parsing output of KKR: total magnetic moment'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            if nspin > 1:
                if not newsosol:
                    #reset automatically to None to turn off reading of nonco angles file
                    nonco_out_file = None

                result, vec, angles = get_spinmom_per_atom(outfile, natom, nonco_out_file)
                if len(result) > 0:
                    tmp_dict['spin_moment_per_atom'] = result[-1, :]
                    if newsosol:
                        tmp_dict['spin_moment_vector_per_atom'] = vec[:]
                        tmp_dict['spin_moment_angles_per_atom'] = angles[:]
                        tmp_dict['spin_moment_angles_per_atom_unit'] = 'degree'
                    out_dict['convergence_group']['spin_moment_per_atom_all_iterations'] = result[:, :]
                    tmp_dict['spin_moment_unit'] = 'mu_Bohr'
                    out_dict['magnetism_group'] = tmp_dict
        except:  # pylint: disable=bare-except
            msg = 'Error parsing output of KKR: spin moment per atom'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        # add orbital moments to magnetis group in parser output
        try:
            if nspin > 1 and newsosol:
                #TODO orbital moment full vectors
                # so far the KKR code writes only the component of the orbital moment
                # parallel to the spin moment, thus vec and angles are returned empty
                # by construction. This might change in the future
                #result, vec, angles = get_orbmom(outfile, natom, nonco_angles_orbmom)
                # so for now return only result= array containing all iterations, all atoms, orbital moment parallel to spin quantization axis
                result = get_orbmom(outfile, natom)
                if len(result) > 0:
                    tmp_dict['total_orbital_moment'] = sum(result[-1, :])
                    tmp_dict['orbital_moment_per_atom'] = result[-1, :]
                    #tmp_dict['orbital_moment_vector_per_atom'] = vec[-1,:]
                    #tmp_dict['orbital_moment_angles_per_atom'] = angles[-1,:]
                    out_dict['convergence_group']['orbital_moment_per_atom_all_iterations'] = result[:, :]
                    tmp_dict['orbital_moment_unit'] = 'mu_Bohr'
                    #tmp_dict['orbital_moment_angles_per_atom_unit'] = 'degree'
                    out_dict['magnetism_group'] = tmp_dict
        except:  # pylint: disable=bare-except
            msg = 'Error parsing output of KKR: orbital moment'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        # get RMS info for nonco angles
        try:
            if nspin > 1 and newsosol:
                result = get_noco_rms(outfile, debug)
                if len(result) > 0:
                    out_dict['convergence_group']['noco_angles_rms_all_iterations'] = result[:]
                    out_dict['convergence_group']['noco_angles_rms_all_iterations_unit'] = 'degrees'
        except:  # pylint: disable=bare-except
            msg = 'Error parsing output of KKR: noco angles rms value'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            result = get_EF(outfile)
            out_dict['fermi_energy'] = result[-1]
            out_dict['fermi_energy_units'] = 'Ry'
            out_dict['convergence_group']['fermi_energy_all_iterations'] = result
            out_dict['convergence_group']['fermi_energy_all_iterations_units'] = 'Ry'
        except:  # pylint: disable=bare-except
            msg = 'Error parsing output of KKR: EF'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            result = get_DOS_EF(outfile)
            out_dict['dos_at_fermi_energy'] = result[-1]
            out_dict['convergence_group']['dos_at_fermi_energy_all_iterations'] = result
        except:  # pylint: disable=bare-except
            msg = 'Error parsing output of KKR: DOS@EF'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            result = get_Etot(outfile)
            out_dict['energy'] = result[-1] * get_Ry2eV()
            out_dict['energy_unit'] = 'eV'
            out_dict['total_energy_Ry'] = result[-1]
            out_dict['total_energy_Ry_unit'] = 'Rydberg'
            out_dict['convergence_group']['total_energy_Ry_all_iterations'] = result
        except:  # pylint: disable=bare-except
            msg = 'Error parsing output of KKR: total energy'
            msg_list.append(msg)
        if debug:
            traceback.print_exc()

        try:
            result = get_single_particle_energies(outfile_000)
            out_dict['single_particle_energies'] = result * get_Ry2eV()
            out_dict['single_particle_energies_unit'] = 'eV'
        except:  # pylint: disable=bare-except
            msg = 'Error parsing output of KKR: single particle energies'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            result_WS, result_tot, result_C = get_charges_per_atom(outfile_000)
            niter = len(out_dict['convergence_group']['rms_all_iterations'])
            natyp = int(len(result_tot) // niter)
            out_dict['total_charge_per_atom'] = result_tot[-natyp:]
            out_dict['charge_core_states_per_atom'] = result_C[-natyp:]
            # this check deals with the DOS case where output is slightly different
            if len(result_WS) == len(result_C):
                out_dict['charge_valence_states_per_atom'] = result_WS[-natyp:] - result_C[-natyp:]
            out_dict['total_charge_per_atom_unit'] = 'electron charge'
            out_dict['charge_core_states_per_atom_unit'] = 'electron charge'
            out_dict['charge_valence_states_per_atom_unit'] = 'electron charge'
        except:  # pylint: disable=bare-except
            msg = 'Error parsing output of KKR: charges'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            try:
                niter, nitermax, converged, nmax_reached, mixinfo = get_scfinfo(outfile_0init, outfile_000, outfile)
            except IndexError:
                niter, nitermax, converged, nmax_reached, mixinfo = get_scfinfo(outfile_0init, outfile_2, outfile)
            out_dict['convergence_group']['number_of_iterations'] = niter
            out_dict['convergence_group']['number_of_iterations_max'] = nitermax
            out_dict['convergence_group']['calculation_converged'] = converged
            out_dict['convergence_group']['nsteps_exhausted'] = nmax_reached
            out_dict['convergence_group']['imix'] = mixinfo[0]
            out_dict['convergence_group']['strmix'] = mixinfo[1]
            out_dict['convergence_group']['qbound'] = mixinfo[2]
            out_dict['convergence_group']['fcm'] = mixinfo[3]
            out_dict['convergence_group']['idtbry'] = mixinfo[4]
            out_dict['convergence_group']['brymix'] = mixinfo[5]
        except:  # pylint: disable=bare-except
            msg = 'Error parsing output of KKR: scfinfo'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

    #convert numpy arrays to standard python lists
    out_dict = convert_to_pystd(out_dict)

    # return output with error messages if there are any
    return len(msg_list) == 0, msg_list, out_dict


def check_error_category(err_cat, err_msg, out_dict):
    """
    Check if parser error of the non-critical category (err_cat != 1) are
    actually consistent and may be discarded.

    :param err_cat: the error-category of the error message to be investigated
    :param err_msg: the error-message
    :param out_dict: the dict of results obtained from the parser function

    :returns: True/False if message is an error or warning
    """
    # check special cases:
    # 1. nonco_angle_file not present, but newsosol==False anyways
    if 'NONCO_ANGLES_OUT' in err_msg:
        return out_dict.get('use_newsosol', True)

    # default behavior
    return err_cat == 1
