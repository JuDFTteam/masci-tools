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
Tools for the impurity caluclation plugin and its workflows
"""
from numpy import array, ndarray, loadtxt
from masci_tools.io.common_functions import search_string, open_general, get_version_info, convert_to_pystd
from masci_tools.io.parsers.kkrparser_functions import get_rms, find_warnings, get_charges_per_atom, get_core_states
import traceback
from masci_tools.util.constants import RY_TO_EV

__copyright__ = (u'Copyright (c), 2018, Forschungszentrum Jülich GmbH,' 'IAS-1/PGI-1, Germany. All rights reserved.')
__license__ = 'MIT license, see LICENSE.txt file'
__version__ = '0.7'
__contributors__ = (u'Philipp Rüßmann', u'Fabian Bertoldo')

####################################################################################


class KkrimpParserFunctions(object):
    """
    Class of parser functions for KKRimp calculation

    :usage: success, msg_list, out_dict = parse_kkrimp_outputfile().parse_kkrimp_outputfile(out_dict, files)
    """

    ### some helper functions ###

    def _get_econt_info(self, out_log):
        """
        extract energy contour information from out_log file
        :param out_log: file that is parsed
        :retuns: econt (dict), dictionary containing the energy contour info
        :note: econt contains the following keys
            * 'emin', bottom of energy contour
            * 'Nepts', number of points in energy contour
            * 'epts', list of complex valued energy points
            * 'weights', list of complex valued weights for energy integration
        """
        f = open_general(out_log)
        tmptxt = f.readlines()
        f.close()
        econt = {}
        itmp = search_string('[read_energy] number of energy points', tmptxt)
        if itmp >= 0:
            econt['Nepts'] = int(tmptxt.pop(itmp).split()[-1])
        itmp = search_string('energies and weights are:', tmptxt)
        if itmp >= 0:
            tmp = []
            for ie in range(econt['Nepts']):
                tmpline = tmptxt[itmp + 4 + ie].split()[1:]
                tmp.append([float(tmpline[0]), float(tmpline[1]), float(tmpline[2]), float(tmpline[3])])
            tmp = array(tmp)
            econt['epts'] = tmp[:, :2]
            econt['weights'] = tmp[:, 2:]
            econt['emin'] = tmp[0, 0]
        return econt

    def _get_scfinfo(self, file):
        """
        extract scf infos (nunmber of iterations, max number of iterations, mixing info) from file
        :param file:
        :returns: niter (int), nitermax (int), converged (bool), nmax_reached (bool), mixinfo (dict)
        :note: mixinfo contains information on mixing scheme and mixing factor used in the calculation
        """
        f = open_general(file)
        tmptxt = f.readlines()
        f.close()
        # get rms and number of iterations
        itmp, niter, rms = 0, -1, -1
        while itmp >= 0:
            itmp = search_string('average rms-error', tmptxt)
            if itmp >= 0:
                tmp = tmptxt.pop(itmp).replace('D', 'E').split()
                niter = int(tmp[1])
                rms = float(tmp[-1])
        # get max number of scf steps
        itmp = search_string('SCFSTEPS', tmptxt)
        if itmp >= 0:
            nitermax = int(tmptxt.pop(itmp).split()[-1])
        # get qbound
        itmp = search_string('QBOUND', tmptxt)
        if itmp >= 0:
            qbound = float(tmptxt.pop(itmp).split()[-1])
        # get imix
        itmp = search_string('IMIX', tmptxt)
        if itmp >= 0:
            imix = int(tmptxt.pop(itmp).split()[-1])
        # get mixfac
        itmp = search_string('MIXFAC', tmptxt)
        if itmp >= 0:
            mixfac = float(tmptxt.pop(itmp).split()[-1])
        # get fcm
        itmp = search_string('FCM', tmptxt)
        if itmp >= 0:
            fcm = float(tmptxt.pop(itmp).split()[-1])
        # set mixinfo
        mixinfo = [imix, mixfac, qbound, fcm]
        # set converged and nmax_reached logicals
        converged, nmax_reached = False, False
        if nitermax == niter:
            nmax_reached = True
        if rms < qbound:
            converged = True
        # return values
        return niter, nitermax, converged, nmax_reached, mixinfo

    def _get_newsosol(self, file):
        """
        Check if spin orbit coupling solver is used
        :param file: absolute path to out_log.000.txt of KKRimp calculation
        :returns: True(False) if SOC solver is (not) used
        """
        f = open_general(file)
        tmptxt = f.readlines()
        f.close()
        itmp = search_string('Spin orbit coupling used?', tmptxt)
        itmp = int(tmptxt.pop(itmp).split()[-1])
        if itmp == 1:
            newsosol = True
        else:
            newsosol = False
        return newsosol

    def _get_natom(self, file):
        """
        Extract number of atoms in impurity cluster
        :param file: file that is parsed to find number of atoms
        :returns: natom (int), number of atoms in impurity cluster
        """
        f = open_general(file)
        tmptxt = f.readlines()
        f.close()
        itmp = search_string('NATOM is', tmptxt)
        natom = int(tmptxt.pop(itmp).split()[-1])
        return natom

    def _get_magtot(self, file, natom, debug=False):
        """
        Extract total magnetic moment of all atoms in imp. cluster,
        magnetic moment for each atom in the cluster and magn. moment
        for all atoms and all iterations of the calculation
        :param file: file that is parsed to find magnetic moments
        :param natom: number of atoms in the cluster
        :returns: magn. moment for all atoms in the cluster for the last iteration (saved in z-comp. of 3d vector)
                  magn. moment for all atoms in the cluster for all iterations (saved in z-comp. of 3d vector)
                  total magnetic moments of all atoms for last iteration
        """
        import numpy as np

        f = open_general(file)
        tmptxt = f.readlines()
        f.close()
        itmp = 0
        spinmom_all = []
        while itmp >= 0:
            itmp = search_string('spin magnetic moment =', tmptxt)
            if itmp >= 0:
                spinmom_all.append(float(tmptxt.pop(itmp).split()[-1]))
        # if no spin
        spinmom = spinmom_all[len(spinmom_all) - natom:]
        if len(spinmom) > 0:  # this means we found something
            spinmom_vec = np.array([[0, 0, spinmom[0]]])
            spinmom_vec_all = np.array([[0, 0, spinmom_all[0]]])
            for i in range(1, natom):
                spinmom_vec = np.append(spinmom_vec, [[0, 0, spinmom[i]]], axis=0)
            for i in range(1, len(spinmom_all)):
                spinmom_vec_all = np.append(spinmom_vec_all, [[0, 0, spinmom_all[i]]], axis=0)
            magtot = sum(spinmom)
        else:
            # otherwise return empty lists
            spinmom_vec, spinmom_vec_all, magtot = [], [], []

        return spinmom_vec, spinmom_vec_all, magtot

    def _extract_timings(self, outfile):
        """
        Extract timings for the different parts in the KKRimp code
        :param outfile: timing file of the KKRimp run
        :returns: res (dict) timings in seconds, averaged over iterations
        """
        f = open_general(outfile)
        tmptxt = f.readlines()
        f.close()
        search_keys = [
            'time until scf starts', 'vpot->tmat', 'gref->gmat', 'gonsite->density', 'energyloop', 'Iteration number',
            'Total running time'
        ]

        res = {}
        for isearch in search_keys:
            tmpval = []
            itmp = 0
            while itmp >= 0:
                itmp = search_string(isearch, tmptxt)
                if itmp >= 0:
                    tmpval.append(float(tmptxt.pop(itmp).split()[-1]))
            if len(tmpval) > 0:
                res[isearch] = tmpval
        # average over iterations
        niter = len(res.get(search_keys[-2], []))
        if niter > 0:
            for key in search_keys[1:6]:
                if key in list(res.keys()):
                    res[key] = sum(res[key]) / niter
            for key in [search_keys[0], search_keys[-1]]:
                if key in list(res.keys()):
                    res[key] = res[key][0]
        return res

    def _get_nspin(self, file):
        """
        Extract nspin from file
        :param file: file that is parsed
        :returns: 1 if calculation is paramagnetic, 2 otherwise
        """
        f = open_general(file)
        tmptxt = f.readlines()
        f.close()
        itmp = search_string('NSPIN', tmptxt)
        nspin = int(tmptxt.pop(itmp).split()[-1])
        return nspin

    def _get_spinmom_per_atom(self, file, natom):
        """
        Extract spin moment for all atoms
        :param file: file that is parsed
        :param natom: number of atoms in impurity cluster
        :returns: spinmom_at (array of spin moments for all atoms and the last iteration),
                  spinmom_at_all (array of spin moments for all atoms and iterations),
                  spinmom_at_tot (total spinmoment for the last iteration)
        """
        import numpy as np
        from math import sqrt

        f = open_general(file)
        lines = f.readlines()
        startline = len(lines) - natom
        spinmom_at = np.array([lines[startline].split()])
        spinmom_at_all = np.array([lines[1].split()])
        for i in range(1, natom):
            spinmom_at = np.append(spinmom_at, [lines[startline + i].split()], axis=0)
        for j in range(2, len(lines)):
            spinmom_at_all = np.append(spinmom_at_all, [lines[j].split()], axis=0)
        spinmom_at_tot = 0
        for i in range(0, natom):
            spinmom_at_tot += sqrt(float(spinmom_at[i][0])**2 + float(spinmom_at[i][1])**2 + float(spinmom_at[i][2])**2)
        # make sure the values are converted from string to float
        spinmom_at = np.array(spinmom_at, dtype=float)
        spinmom_at_all = np.array(spinmom_at_all, dtype=float)

        return spinmom_at, spinmom_at_all, spinmom_at_tot

    def _get_orbmom_per_atom(self, file, natom):
        """
        Extract orbital moment for all atoms (orbmom_at: all atoms in last iteration,
        orbmom_at_all: all atoms in all iterations). For each atom there are six values:
        first -> x-component real part, second -> x-component imaginary part,
        third -> y-component real part, ... sixth -> z-component imaginary part.
        :param file: file that is parsed
        :param natom: number of atoms in impurity cluster
        :returns: orbmom_at (list), orbital moments for all atoms
        """
        import numpy as np

        f = open_general(file)
        lines = f.readlines()
        startline = len(lines) - natom

        orbmom_at = []
        for i in range(natom):
            tmp = lines[startline + i].split()
            orbmom_at.append([tmp[1], tmp[3], tmp[5]])  # [1,3,5] needed since full complex number is written
        orbmom_at = np.array(orbmom_at, dtype=float)  # convert to float array

        # do the same for all iterations
        orbmom_at_all = []
        for i in range(1, len(lines)):
            tmp = lines[i].split()
            orbmom_at_all.append([tmp[1], tmp[3], tmp[5]])

        orbmom_at_all = np.array(orbmom_at_all, dtype=float)  # convert to float array

        return orbmom_at, orbmom_at_all

    def _get_EF_potfile(self, potfile):
        """
        Extract EF value from potential file
        :param potfile: file that is parsed
        :returns: EF (float), value of the Fermi energy in Ry
        """
        f = open_general(potfile)
        tmptxt = f.readlines()
        f.close()
        EF = float(tmptxt[3].split()[1])
        return EF

    def _get_Etot(self, file):
        """
        Extract total energy file
        :param file: file that is parsed
        :returns: Etot (list), values of the total energy in Ry for all iterations
        """
        f = open_general(file)
        tmptxt = f.readlines()
        f.close()
        itmp = 0
        Etot = []
        while itmp >= 0:
            itmp = search_string('TOTAL ENERGY', tmptxt)
            if itmp >= 0:
                Etot.append(float(tmptxt.pop(itmp).split()[-1]))
        return Etot

    def _get_energies_atom(self, file1, file2, natom):
        """
        Extract single particle and total energies in Ry for all atoms from file 1 and file 2
        :param file1: file containing all single particle energies
        :param file2: file containing all total energies
        :returns: esp_at (list), etot_at (list)
        """
        esp = loadtxt(file1)
        etot = loadtxt(file2)
        esp_at = esp[-natom:, 1]
        etot_at = etot[-natom:, 1]
        return esp_at, etot_at

    ### end helper functions ###

    def parse_kkrimp_outputfile(self, out_dict, file_dict, debug=False):
        """
        Main parser function for kkrimp, read information from files in file_dict and fills out_dict
        :param out_dict: dictionary that is filled with parsed output of the KKRimp calculation
        :param file_dict: dictionary of files that are parsed
        :returns: success (bool), msg_list(list of error/warning messages of parser), out_dict (filled dict of parsed output)
        :note: file_dict should contain the following keys

               - 'outfile', the std_out of the KKRimp calculation
               - 'out_log', the out_log.000.txt file
               - 'out_pot', the output potential
               - 'out_enersp_at', the out_energysp_per_atom_eV file
               - 'out_enertot_at', the out_energytotal_per_atom_eV file
               - 'out_timing', the timing file
               - 'kkrflex_llyfac', the file for the Lloyd factor
               - 'kkrflex_angles', the nonco_angles file for the KKRimp calculation
               - 'out_spinmoms', the output spin moments file
               - 'out_orbmoms', the output orbital moments file

        """

        msg_list = []
        files = file_dict

        try:
            code_version, compile_options, serial_number = get_version_info(files['out_log'])
            tmp_dict = {}
            tmp_dict['code_version'] = code_version
            tmp_dict['compile_options'] = compile_options
            tmp_dict['calculation_serial_number'] = serial_number
            out_dict['code_info_group'] = tmp_dict
        except:
            msg = 'Error parsing output of KKRimp: Version Info'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        tmp_dict = {}  # used to group convergence info (rms, rms per atom, charge neutrality)
        # also initialize convegence_group where all info stored for all iterations is kept
        out_dict['convergence_group'] = tmp_dict
        try:
            rms_charge, rms_spin, result_atoms_last_charge, result_atoms_last_spin = get_rms(files['outfile'],
                                                                                             files['out_log'],
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
        except:
            msg = 'Error parsing output of KKRimp: rms-error'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            nspin = self._get_nspin(files['out_log'])
            natom = self._get_natom(files['out_log'])
            newsosol = self._get_newsosol(files['out_log'])
            out_dict['nspin'] = nspin
            out_dict['number_of_atoms_in_unit_cell'] = natom
            out_dict['use_newsosol'] = newsosol
        except:
            msg = 'Error parsing output of KKRimp: nspin/natom'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        tmp_dict = {}  # used to group magnetism info (spin and orbital moments)
        try:
            result = self._get_magtot(files['out_log'], natom, debug=debug)
            if len(result) > 0:
                tmp_dict['total_spin_moment'] = result[-1]
                out_dict['convergence_group']['total_spin_moment_all_iterations'] = result
                tmp_dict['total_spin_moment_unit'] = 'mu_Bohr'
                out_dict['magnetism_group'] = tmp_dict
        except:
            msg = 'Error parsing output of KKRimp: total magnetic moment'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            if nspin > 1 and newsosol:
                #result, vec, angles = get_spinmom_per_atom(outfile, natom, nonco_out_file)
                spinmom_atom, spinmom_atom_vec_all_iter, spin_tot_abs = self._get_spinmom_per_atom(
                    files['out_spinmoms'], natom)
                if len(result) > 0:
                    tmp_dict['total_abs_spin_moment'] = spin_tot_abs
                    tmp_dict['spin_moment_per_atom'] = spinmom_atom
                    out_dict['convergence_group']['spin_moment_per_atom_all_iterations'] = spinmom_atom_vec_all_iter
                    tmp_dict['spin_moment_unit'] = 'mu_Bohr'
                    out_dict['magnetism_group'] = tmp_dict
        except:
            msg = 'Error parsing output of KKRimp: spin moment per atom'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        # add orbital moments to magnetis group in parser output
        try:
            if nspin > 1 and newsosol:
                orbmom_atom, orbmom_atom_all_iter = self._get_orbmom_per_atom(files['out_orbmoms'], natom)
                if len(result) > 0:
                    tmp_dict['total_orbital_moment'] = sum(orbmom_atom)
                    tmp_dict['orbital_moment_per_atom'] = orbmom_atom
                    out_dict['convergence_group']['orbital_moment_per_atom_all_iterations'] = orbmom_atom_all_iter
                    tmp_dict['orbital_moment_unit'] = 'mu_Bohr'
                    out_dict['magnetism_group'] = tmp_dict
        except:
            msg = 'Error parsing output of KKRimp: orbital moment'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            result = self._get_EF_potfile(files['out_pot'])
            out_dict['fermi_energy'] = result
            out_dict['fermi_energy_units'] = 'Ry'
        except:
            msg = 'Error parsing output of KKRimp: EF'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            result = self._get_Etot(files['out_log'])
            out_dict['energy'] = result[-1] * RY_TO_EV
            out_dict['energy_unit'] = 'eV'
            out_dict['total_energy_Ry'] = result[-1]
            out_dict['total_energy_Ry_unit'] = 'Rydberg'
            out_dict['convergence_group']['total_energy_Ry_all_iterations'] = result
        except:
            msg = 'Error parsing output of KKRimp: total energy'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            result = find_warnings(files['outfile'])
            tmp_dict = {}
            tmp_dict['number_of_warnings'] = len(result)
            tmp_dict['warnings_list'] = result
            out_dict['warnings_group'] = tmp_dict
        except:
            msg = 'Error parsing output of KKRimp: search for warnings'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            result = self._extract_timings(files['out_timing'])
            out_dict['timings_group'] = result
            out_dict['timings_unit'] = 'seconds'
        except:
            msg = 'Error parsing output of KKRimp: timings'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            esp_at, etot_at = self._get_energies_atom(files['out_enersp_at'], files['out_enertot_at'], natom)
            out_dict['single_particle_energies'] = esp_at * RY_TO_EV
            out_dict['single_particle_energies_unit'] = 'eV'
            out_dict['total_energies_atom'] = etot_at * RY_TO_EV
            out_dict['total_energies_atom_unit'] = 'eV'
        except:
            msg = 'Error parsing output of KKRimp: single particle energies'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            result_WS, result_tot, result_C = get_charges_per_atom(files['out_log'])
            niter = len(out_dict['convergence_group']['rms_all_iterations'])
            natyp = int(len(result_tot) / niter)
            out_dict['total_charge_per_atom'] = result_WS[-natyp:]
            out_dict['charge_core_states_per_atom'] = result_C[-natyp:]
            # this check deals with the DOS case where output is slightly different
            if len(result_WS) == len(result_C):
                out_dict['charge_valence_states_per_atom'] = result_WS[-natyp:] - result_C[-natyp:]
            out_dict['total_charge_per_atom_unit'] = 'electron charge'
            out_dict['charge_core_states_per_atom_unit'] = 'electron charge'
            out_dict['charge_valence_states_per_atom_unit'] = 'electron charge'
        except:
            msg = 'Error parsing output of KKRimp: charges'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            econt = self._get_econt_info(files['out_log'])
            tmp_dict = {}
            tmp_dict['emin'] = econt.get('emin')
            tmp_dict['emin_unit'] = 'Rydberg'
            tmp_dict['number_of_energy_points'] = econt.get('Nepts')
            tmp_dict['epoints_contour'] = econt.get('epts')
            tmp_dict['epoints_contour_unit'] = 'Rydberg'
            tmp_dict['epoints_weights'] = econt.get('weights')
            out_dict['energy_contour_group'] = tmp_dict
        except:
            msg = 'Error parsing output of KKRimp: energy contour'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            ncore, emax, lmax, descr_max = get_core_states(files['out_pot'])
            tmp_dict = {}
            tmp_dict['number_of_core_states_per_atom'] = ncore
            tmp_dict['energy_highest_lying_core_state_per_atom'] = emax
            tmp_dict['energy_highest_lying_core_state_per_atom_unit'] = 'Rydberg'
            tmp_dict['descr_highest_lying_core_state_per_atom'] = descr_max
            out_dict['core_states_group'] = tmp_dict
        except:
            msg = 'Error parsing output of KKRimp: core_states'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        try:
            niter, nitermax, converged, nmax_reached, mixinfo = self._get_scfinfo(files['out_log'])
            out_dict['convergence_group']['number_of_iterations'] = niter
            out_dict['convergence_group']['number_of_iterations_max'] = nitermax
            out_dict['convergence_group']['calculation_converged'] = converged
            out_dict['convergence_group']['nsteps_exhausted'] = nmax_reached
            out_dict['convergence_group']['imix'] = mixinfo[0]
            out_dict['convergence_group']['strmix'] = mixinfo[1]
            out_dict['convergence_group']['qbound'] = mixinfo[2]
            out_dict['convergence_group']['fcm'] = mixinfo[3]
            out_dict['convergence_group']['brymix'] = mixinfo[1]
        except:
            msg = 'Error parsing output of KKRimp: scfinfo'
            msg_list.append(msg)
            if debug:
                traceback.print_exc()

        #convert numpy arrays to standard python lists
        out_dict = convert_to_pystd(out_dict)

        # return output with error messages if there are any
        if len(msg_list) > 0:
            return False, msg_list, out_dict
        else:
            return True, [], out_dict
