# -*- coding: utf-8 -*-
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
Everything that is needed to parse the output of a voronoi calculation.
"""
from masci_tools.io.common_functions import (get_corestates_from_potential, get_highest_core_state, search_string,
                                             get_version_info, get_ef_from_potfile, open_general, convert_to_pystd)
from masci_tools.io.parsers.kkrparser_functions import get_core_states
from masci_tools.util.constants import RY_TO_EV
import numpy as np
import io
import sys
import traceback

__copyright__ = (u'Copyright (c), 2018, Forschungszentrum Jülich GmbH,' 'IAS-1/PGI-1, Germany. All rights reserved.')
__license__ = 'MIT license, see LICENSE.txt file'
__contributors__ = (u'Philipp Rüßmann')
__version__ = 1.4

####################################################################################


def get_valence_min(outfile='out_voronoi'):
    """Construct minimum of energy contour (between valence band bottom and core states)"""
    f = open_general(outfile)
    with f:  # make sure the file is properly closed
        txt = f.readlines()
        searchstr = 'All other states are above'
        valence_minimum = np.array([float(line.split(':')[1].split()[0]) for line in txt if searchstr in line])
    return valence_minimum


def check_voronoi_output(potfile, outfile, delta_emin_safety=0.1):
    """Read output from voronoi code and create guess of energy contour"""
    #analyse core levels, minimum of valence band and their difference
    ncore, ecore, lcore = get_corestates_from_potential(potfile=potfile)
    e_val_min = get_valence_min(outfile=outfile)

    #print a table that summarizes the result
    e_core_max = np.zeros(len(ncore))
    print('pot    Highest core-level     low. val. state    diff')
    for ipot in range(len(ncore)):
        if ncore[ipot] > 0:
            lval, emax, descr = get_highest_core_state(ncore[ipot], ecore[ipot], lcore[ipot])
            e_core_max[ipot] = emax
            print('%3i     %2s %10.6f            %6.2f         %6.2f' %
                  (ipot + 1, descr, emax, e_val_min[ipot], e_val_min[ipot] - emax))
        else:
            print('%3i     << no core states >>' % (ipot + 1))
            # set to some large negative number for check to not give false positive in case of empty cells
            e_core_max[ipot] = -1000

    #get hint for energy integration:
    emin_guess = e_val_min.min() - delta_emin_safety  # in Ry

    return emin_guess, e_core_max.max()


def parse_voronoi_output(out_dict, outfile, potfile, atominfo, radii, inputfile, debug=False):
    """
    Parse output of voronoi calculation and return (success, error_messages_list, out_dict)
    """
    # for collection of error messages:
    msg_list = []

    try:
        code_version, compile_options, serial_number = get_version_info(outfile)
        tmp_dict = {}
        tmp_dict['code_version'] = code_version
        tmp_dict['compile_options'] = compile_options
        tmp_dict['calculation_serial_number'] = serial_number
        out_dict['code_info_group'] = tmp_dict
    except:
        msg = 'Error parsing output of voronoi: Version Info'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        emin, e_core_max = check_voronoi_output(potfile, outfile)
        out_dict['emin'] = emin
        out_dict['emin_units'] = 'Ry'
        diff_emin_ef = emin - get_ef_from_potfile(potfile)
        out_dict['emin_minus_efermi_Ry'] = diff_emin_ef
        out_dict['emin_minus_efermi'] = diff_emin_ef * RY_TO_EV
        out_dict['emin_minus_efermi_Ry_units'] = 'Ry'
        out_dict['emin_minus_efermi_units'] = 'eV'
    except:
        msg = "Error parsing output of voronoi: 'EMIN'"
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    # parse
    try:
        ncore, emax, lmax, descr_max = get_core_states(potfile)
        tmp_dict = {}
        tmp_dict['number_of_core_states_per_atom'] = ncore
        tmp_dict['energy_highest_lying_core_state_per_atom'] = emax
        tmp_dict['energy_highest_lying_core_state_per_atom_unit'] = 'Rydberg'
        tmp_dict['descr_highest_lying_core_state_per_atom'] = descr_max
        out_dict['core_states_group'] = tmp_dict
    except:
        msg = 'Error parsing output of voronoi: core_states'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        Ncls, natom, results = get_cls_info(outfile)
        clsinfo = []
        tmpdict_all = {}
        for icls in range(natom):
            tmpdict = {}
            tmpdict['iatom'] = results[icls][0]
            tmpdict['refpot'] = results[icls][1]
            tmpdict['rmt_ref'] = results[icls][2]
            tmpdict['tb_cluster_id'] = results[icls][3]
            tmpdict['sites'] = results[icls][4]
            clsinfo.append(tmpdict)
        tmpdict_all['cluster_info_atoms'] = clsinfo
        tmpdict_all['number_of_clusters'] = Ncls
        out_dict['cluster_info_group'] = tmpdict_all
    except:
        msg = 'Error parsing output of voronoi: Cluster Info'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        out_dict['start_from_jellium_potentials'] = startpot_jellium(outfile)
    except:
        msg = 'Error parsing output of voronoi: Jellium startpot'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        natyp, naez, shapes = get_shape_array(outfile, atominfo)
        out_dict['shapes'] = shapes
    except:
        msg = 'Error parsing output of voronoi: SHAPE Info'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        Vtot, results = get_volumes(outfile)
        tmp_dict = {}
        tmp_dict['volume_total'] = Vtot
        tmpdict_all = []
        for icls in range(naez):
            tmpdict = {}
            tmpdict['iatom'] = results[icls][0]
            tmpdict['v_atom'] = results[icls][1]
            tmpdict_all.append(tmpdict)
        tmp_dict['volume_atoms'] = tmpdict_all
        tmp_dict['volume_unit'] = 'alat^3'
        out_dict['volumes_group'] = tmp_dict
    except:
        msg = 'Error parsing output of voronoi: Volume Info'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        results = get_radii(naez, radii)
        tmpdict_all = []
        for icls in range(naez):
            tmpdict = {}
            tmpdict['iatom'] = results[icls][0]
            tmpdict['rmt0'] = results[icls][1]
            tmpdict['rout'] = results[icls][2]
            tmpdict['dist_nn'] = results[icls][4]
            tmpdict['rmt0_over_rout'] = results[icls][3]
            tmpdict['rout_over_dist_nn'] = results[icls][5]
            tmpdict_all.append(tmpdict)
        tmpdict_all.append({'radii_units': 'alat'})
        out_dict['radii_atoms_group'] = tmpdict_all
    except:
        msg = 'Error parsing output of voronoi: radii.dat Info'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        results = get_fpradius(naez, atominfo)
        out_dict['fpradius_atoms'] = results
        out_dict['fpradius_atoms_unit'] = 'alat'
    except:
        msg = 'Error parsing output of voronoi: full potential radius'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        result = get_alat(inputfile)
        out_dict['alat'] = result
        out_dict['alat_unit'] = 'a_Bohr'
    except:
        msg = 'Error parsing output of voronoi: alat'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    try:
        result = get_radial_meshpoints(potfile)
        out_dict['radial_meshpoints'] = result
    except:
        msg = 'Error parsing output of voronoi: radial meshpoints'
        msg_list.append(msg)
        if debug:
            traceback.print_exc()

    # some consistency checks comparing lists with natyp/naez numbers
    #TODO implement checks

    #convert numpy arrays to standard python lists
    out_dict = convert_to_pystd(out_dict)

    # return output with error messages if there are any
    if len(msg_list) > 0:
        return False, msg_list, out_dict
    else:
        return True, [], out_dict


def startpot_jellium(outfile):
    f = open_general(outfile)
    with f:  # make sure the file is properly closed
        tmptxt = f.readlines()
    itmp = search_string('JELLSTART POTENTIALS', tmptxt)
    if itmp == -1:
        return False
    else:
        return True


def get_volumes(outfile):
    f = open_general(outfile)
    with f:  # make sure the file is properly closed
        tmptxt = f.readlines()

    itmp = search_string('Total volume (alat^3)', tmptxt)
    if itmp >= 0:
        Vtot = float(tmptxt.pop(itmp).split()[-1])

    itmp = 0
    results = []
    while itmp >= 0:
        itmp = search_string(' Volume(alat^3)  :', tmptxt)
        if itmp >= 0:
            tmpstr = tmptxt.pop(itmp)
            tmpstr = tmpstr.split()
            tmpstr = [int(tmpstr[2]), float(tmpstr[5])]
            results.append(tmpstr)
    return Vtot, results


def get_cls_info(outfile):
    f = open_general(outfile)
    with f:  # make sure the file is properly closed
        tmptxt = f.readlines()
        f.close()
        itmp = 0
        Ncls = 0
        Natom = 0
        cls_all = []
        results = []
        while itmp >= 0:
            itmp = search_string('CLSGEN_TB: Atom', tmptxt)
            if itmp >= 0:
                tmpstr = tmptxt.pop(itmp)
                tmpstr = tmpstr.split()
                tmp = [int(tmpstr[2]), int(tmpstr[4]), float(tmpstr[6]), int(tmpstr[8]), int(tmpstr[10])]
                results.append(tmp)
                if int(tmpstr[8]) not in cls_all:
                    Ncls += 1
                    cls_all.append(int(tmpstr[8]))
                Natom += 1
    return Ncls, Natom, results


def get_shape_array(outfile, atominfo):
    f = open_general(outfile)
    with f:  # make sure the file is properly closed
        txt = f.readlines()
    #naez/natyp number of items either one number (=ishape without cpa or two =[iatom, ishape] with CPA)
    # read in naez and/or natyp and then find ishape array (1..natyp[=naez without CPA])
    itmp = search_string('NAEZ= ', txt)
    if itmp >= 0:
        tmp = txt[itmp]
        ipos = tmp.find('NAEZ=')
        naez = int(tmp[ipos + 5:].split()[0])
    else:
        naez = -1
    itmp = search_string('NATYP= ', txt)
    if itmp >= 0:
        tmp = txt[itmp]
        ipos = tmp.find('NATYP=')
        natyp = int(tmp[ipos + 6:].split()[0])
    else:
        natyp = -1

    # consistency check
    if naez == -1 and natyp > 0:
        naez = natyp
    elif natyp == -1 and naez > 0:
        natyp = naez
    elif natyp == -1 and naez == -1:
        raise ValueError('Neither NAEZ nor NATYP found in %s' % outfile)

    # read shape index from atominfo file
    f = open_general(atominfo)
    with f:  # make sure the file is properly closed
        tmptxt = f.readlines()

    itmp = search_string('<SHAPE>', tmptxt) + 1
    ishape = []
    for iatom in range(natyp):
        txt = tmptxt[itmp + iatom]
        if natyp > naez:  #CPA option
            ishape.append(int(txt.split()[1]))
        else:
            ishape.append(int(txt.split()[0]))

    return natyp, naez, ishape


def get_radii(naez, radii):
    f = open_general(radii)
    with f:  # make sure the file is properly closed
        txt = f.readlines()
    results = []
    for iatom in range(naez):
        # IAT    Rmt0           Rout            Ratio(%)   dist(NN)      Rout/dist(NN) (%)
        # 1   0.5000001547   0.7071070000       70.71   1.0000003094       70.71
        tmpline = txt[3 + iatom].split()
        tmpline = [
            int(tmpline[0]),
            float(tmpline[1]),
            float(tmpline[2]),
            float(tmpline[3]),
            float(tmpline[4]),
            float(tmpline[5])
        ]
        results.append(tmpline)
    return results


def get_fpradius(naez, atominfo):
    f = open_general(atominfo)
    with f:  # make sure the file is properly closed
        txt = f.readlines()
    itmp = search_string('<FPRADIUS>', txt) + 1
    results = []
    for iatom in range(naez):
        #ZAT   LMXC  KFG   <CLS> <REFPOT> <NTC>  FAC  <IRNS> <RMTREF>   <FPRADIUS>
        # 0.00 1 3 3 0 0      1      1      1    1.     199   2.3166000   0.4696902
        tmpline = float(txt[itmp + iatom].split()[-1])
        results.append(tmpline)
    return results


def get_alat(inpfile):
    f = open_general(inpfile)
    with f:  # make sure the file is properly closed
        txt = f.readlines()
    itmp = search_string('ALATBASIS', txt)
    result = float(txt[itmp].split('ALATBASIS')[1].split('=')[1].split()[0])
    return result


def get_radial_meshpoints(potfile):
    f = open_general(potfile)
    with f:  # make sure the file is properly closed
        txt = f.readlines()
    itmp = 0
    result = []
    while itmp >= 0:
        itmp = search_string('exc:', txt)
        if itmp >= 0:
            txt.pop(itmp)  # remove header line
            tmp = txt.pop(itmp + 3)  # extract meshpoints
            result.append(float(tmp))
    return result
