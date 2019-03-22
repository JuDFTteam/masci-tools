#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#use print('message') instead of print 'message' in python 2.7 as well:
from __future__ import print_function
from __future__ import division

from builtins import range
from builtins import object
"""
Tools for the impurity caluclation plugin and its workflows
"""
         
__copyright__ = (u"Copyright (c), 2018, Forschungszentrum Jülich GmbH,"
                 "IAS-1/PGI-1, Germany. All rights reserved.")
__license__ = "MIT license, see LICENSE.txt file"
__version__ = "0.3"
__contributors__ = (u"Philipp Rüßmann", 
                    u"Fabian Bertoldo")


class kkrimp_parser_functions(object):
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
        from masci_tools.io.common_functions import search_string
        from numpy import array
        f = open(out_log)
        tmptxt = f.readlines()
        f.close()
        econt = {}
        itmp = search_string('[read_energy] number of energy points', tmptxt)
        if itmp>=0: econt['Nepts'] = int(tmptxt.pop(itmp).split()[-1])
        itmp = search_string('energies and weights are:', tmptxt)
        if itmp>=0:
            tmp = []
            for ie in range(econt['Nepts']):
                tmpline = tmptxt[itmp+4+ie].split()[1:]
                tmp.append([float(tmpline[0]), float(tmpline[1]), float(tmpline[2]), float(tmpline[3])])
            tmp = array(tmp)
            econt['epts'] = tmp[:,:2]
            econt['weights'] = tmp[:,2:]
            econt['emin'] = tmp[0,0]
        return econt
    
    
    def _get_scfinfo(self, file):
        """
        extract scf infos (nunmber of iterations, max number of iterations, mixing info) from file
        :param file:
        :returns: niter (int), nitermax (int), converged (bool), nmax_reached (bool), mixinfo (dict)
        :note: mixinfo contains information on mixing scheme and mixing factor used in the calculation
        """
        from masci_tools.io.common_functions import search_string
        f = open(file)
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
        if nitermax==niter: nmax_reached = True
        if rms<qbound: converged = True
        # return values
        return niter, nitermax, converged, nmax_reached, mixinfo
    
    
    def _get_newsosol(self, file):
        """
        Check if spin orbit coupling solver is used
        :param file: absolute path to out_log.000.txt of KKRimp calculation
        :returns: True(False) if SOC solver is (not) used
        """
        from masci_tools.io.common_functions import search_string
        f = open(file)
        tmptxt = f.readlines()
        f.close()
        itmp = search_string('Spin orbit coupling used?', tmptxt)
        itmp = int(tmptxt.pop(itmp).split()[-1])
        if itmp==1:
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
        from masci_tools.io.common_functions import search_string
        f = open(file)
        tmptxt = f.readlines()
        f.close()
        itmp = search_string('NATOM is', tmptxt)
        natom = int(tmptxt.pop(itmp).split()[-1])
        return natom
    
    
    def _get_magtot(self, file):
        """
        Extract total magnetic moment ofall atoms in imp. cluster
        :param file: file that is parsed to find magnetic moments
        :returns: list of total magnetic moments of all atoms
        """
        #TODO implement
        return []
    
    
    def _extract_timings(self, outfile):
        """
        Extract timings for the different parts in the KKRimp code
        :param outfile: timing file of the KKRimp run
        :returns: res (dict) timings in seconds, averaged over iterations
        """
        from masci_tools.io.common_functions import search_string
        f = open(outfile)
        tmptxt = f.readlines()
        f.close()
        search_keys = ['time until scf starts', 
                       'vpot->tmat',
                       'gref->gmat',
                       'gonsite->density', 
                       'energyloop', 
                       'Iteration number', 
                       'Total running time']
                       
        res = {}
        for isearch in search_keys:
            tmpval = []
            itmp = 0
            while itmp>=0:
                itmp = search_string(isearch, tmptxt)
                if itmp>=0:
                    tmpval.append(float(tmptxt.pop(itmp).split()[-1]))
            if len(tmpval)>0:
                res[isearch] = tmpval
        # average over iterations
        niter = len(res.get(search_keys[-2], []))
        if niter>0:
            for key in search_keys[1:6]:
                res[key] = sum(res[key])/niter
            for key in [search_keys[0], search_keys[-1]]:
                res[key] = res[key][0]
        return res
        
        
    def _get_nspin(self, file):
        """
        Extract nspin from file
        :param file: file that is parsed
        :returns: 1 if calculation is paramagnetic, 2 otherwise
        """
        from masci_tools.io.common_functions import search_string
        f = open(file)
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
        :returns: spinmom_at (list), spin moments for all atoms
        """
        #TODO implement
        return spinmom_at
    
    
    def _get_orbmom_per_atom(self, file, natom):
        """
        Extract orbital moment for all atoms
        :param file: file that is parsed
        :param natom: number of atoms in impurity cluster
        :returns: orbmom_at (list), orbital moments for all atoms
        """
        #TODO implement
        return orbmom_at
        
        
    def _get_EF_potfile(self, potfile):
        """
        Extract EF value from potential file
        :param potfile: file that is parsed
        :returns: EF (float), value of the Fermi energy in Ry
        """
        f = open(potfile)
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
        from masci_tools.io.common_functions import search_string
        f = open(file)
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
        from numpy import loadtxt
        esp = loadtxt(file1)
        etot = loadtxt(file2)
        esp_at = esp[-natom:,1]
        etot_at = etot[-natom:,1]
        return esp_at, etot_at

    
    ### end helper functions ###

    
    def parse_kkrimp_outputfile(self, out_dict, file_dict):
        """
        Main parser function for kkrimp, read information from files in file_dict and fills out_dict
        :param out_dict: dictionary that is filled with parsed output of the KKRimp calculation
        :param file_dict: dictionary of files that are parsed
        :returns: success (bool), msg_list(list of error/warning messages of parser), out_dict (filled dict of parsed output)
        :note: file_dict should contain the following keys
            * 'outfile', the std_out of the KKRimp calculation
            * 'out_log', the out_log.000.txt file
            * 'out_pot', the output potential
            * 'out_enersp_at', the out_energysp_per_atom_eV file
            * 'out_enertot_at', the out_energytotal_per_atom_eV file
            * 'out_timing', the timing file
            * 'kkrflex_llyfac', the file for the Lloyd factor
            * 'kkrflex_angles', the nonco_angles file for the KKRimp calculation
            * 'out_spinmoms', the output spin moments file
            * 'out_orbmoms', the output orbital moments file
        """
        from masci_tools.io.parsers.kkrparser_functions import get_rms, find_warnings, get_charges_per_atom, get_core_states
        from masci_tools.io.common_functions import get_version_info, get_Ry2eV
        
        Ry2eV = get_Ry2eV()
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
            msg = "Error parsing output of KKRimp: Version Info"
            msg_list.append(msg)
        
        tmp_dict = {} # used to group convergence info (rms, rms per atom, charge neutrality)
        # also initialize convegence_group where all info stored for all iterations is kept
        out_dict['convergence_group'] = tmp_dict
        try:
            result, result_atoms_last = get_rms(files['outfile'], files['out_log'])
            tmp_dict['rms'] = result[-1]
            tmp_dict['rms_all_iterations'] = result
            tmp_dict['rms_per_atom'] = result_atoms_last
            tmp_dict['rms_unit'] = 'unitless'
            out_dict['convergence_group'] = tmp_dict
        except:
            msg = "Error parsing output of KKRimp: rms-error"
            msg_list.append(msg)
            
        tmp_dict = {} # used to group magnetism info (spin and orbital moments)
        try:
            result = self._get_magtot(files['out_log'])
            if len(result)>0:
                tmp_dict['total_spin_moment'] = result[-1]
                out_dict['convergence_group']['total_spin_moment_all_iterations'] = result
                tmp_dict['total_spin_moment_unit'] = 'mu_Bohr'
                out_dict['magnetism_group'] = tmp_dict
        except:
            msg = "Error parsing output of KKRimp: total magnetic moment"
            msg_list.append(msg)
            
        try:
            nspin = self._get_nspin(files['out_log'])
            natom = self._get_natom(files['out_log'])
            newsosol = self._get_newsosol(files['out_log'])
            out_dict['nspin'] = nspin
            out_dict['number_of_atoms_in_unit_cell'] = natom
            out_dict['use_newsosol'] = newsosol
        except:
            msg = "Error parsing output of KKRimp: nspin/natom"
            msg_list.append(msg)
        
        try:
            if nspin>1:
                #result, vec, angles = get_spinmom_per_atom(outfile, natom, nonco_out_file)
                spinmom_atom, spinmom_atom_vec_all_iter,  = self._get_spinmom_per_atom(files['out_spinmom'], natom)
                if len(result)>0:
                    tmp_dict['spin_moment_per_atom'] = result[-1,:]
                    if newsosol:
                        tmp_dict['spin_moment_vector_per_atom'] = vec[:]
                        tmp_dict['spin_moment_angles_per_atom'] = angles[:]
                        tmp_dict['spin_moment_angles_per_atom_unit'] = 'degree'
                    out_dict['convergence_group']['spin_moment_per_atom_all_iterations'] = result[:,:]
                    tmp_dict['spin_moment_unit'] = 'mu_Bohr'
                    out_dict['magnetism_group'] = tmp_dict
        except:
            msg = "Error parsing output of KKRimp: spin moment per atom"
            msg_list.append(msg)
        
        # add orbital moments to magnetis group in parser output
        try:
            if nspin>1 and newsosol:
                orbmom_atom = self._get_orbmom_per_atom(files['out_orbmom'], natom)
                if len(result)>0:
                    tmp_dict['total_orbital_moment'] = sum(result[-1,:])
                    tmp_dict['orbital_moment_per_atom'] = result[-1,:]
                    out_dict['convergence_group']['orbital_moment_per_atom_all_iterations'] = result[:,:]
                    tmp_dict['orbital_moment_unit'] = 'mu_Bohr'
                    out_dict['magnetism_group'] = tmp_dict
        except:
            msg = "Error parsing output of KKRimp: orbital moment"
            msg_list.append(msg)
    
        try:
            result = self._get_EF_potfile(files['out_pot'])
            out_dict['fermi_energy'] = result
            out_dict['fermi_energy_units'] = 'Ry'
        except:
            msg = "Error parsing output of KKRimp: EF"
            msg_list.append(msg)
    
        try:
            result = self._get_Etot(files['out_log'])
            print(result)
            out_dict['energy'] = result[-1]*Ry2eV
            out_dict['energy_unit'] = 'eV'
            out_dict['total_energy_Ry'] = result[-1]
            out_dict['total_energy_Ry_unit'] = 'Rydberg'
            out_dict['convergence_group']['total_energy_Ry_all_iterations'] = result
        except:
            msg = "Error parsing output of KKRimp: total energy"
            msg_list.append(msg)
    
        try:
            result = find_warnings(files['outfile'])
            tmp_dict = {}
            tmp_dict['number_of_warnings'] = len(result)
            tmp_dict['warnings_list'] = result
            out_dict['warnings_group'] = tmp_dict
        except:
            msg = "Error parsing output of KKRimp: search for warnings"
            msg_list.append(msg)
    
        try:
            result = self._extract_timings(files['out_timing'])
            out_dict['timings_group'] = result
            out_dict['timings_unit'] = 'seconds'
        except:
            msg = "Error parsing output of KKRimp: timings"
            msg_list.append(msg)
        
        try:
            esp_at, etot_at = self._get_energies_atom(files['out_enersp_at'], files['out_enertot_at'], natom)
            out_dict['single_particle_energies'] = esp_at*Ry2eV
            out_dict['single_particle_energies_unit'] = 'eV'
            out_dict['total_energies_atom'] = etot_at*Ry2eV
            out_dict['total_energies_atom_unit'] = 'eV'
        except:
            msg = "Error parsing output of KKRimp: single particle energies"
            msg_list.append(msg)
        
        try:
            result_WS, result_tot, result_C = get_charges_per_atom(files['out_log'])
            niter = len(out_dict['convergence_group']['rms_all_iterations'])
            natyp = int(len(result_tot)//niter)
            out_dict['total_charge_per_atom'] = result_WS[-natyp:]
            out_dict['charge_core_states_per_atom'] = result_C[-natyp:]
            # this check deals with the DOS case where output is slightly different
            if len(result_WS) == len(result_C):
                out_dict['charge_valence_states_per_atom'] = result_WS[-natyp:]-result_C[-natyp:]
            out_dict['total_charge_per_atom_unit'] = 'electron charge'
            out_dict['charge_core_states_per_atom_unit'] = 'electron charge'
            out_dict['charge_valence_states_per_atom_unit'] = 'electron charge'
        except:
            msg = "Error parsing output of KKRimp: charges"
            msg_list.append(msg)
        
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
            msg = "Error parsing output of KKRimp: energy contour"
            msg_list.append(msg)
        
        try:
            ncore, emax, lmax, descr_max = get_core_states(files['out_pot'])
            tmp_dict = {}
            tmp_dict['number_of_core_states_per_atom'] = ncore
            tmp_dict['energy_highest_lying_core_state_per_atom'] = emax
            tmp_dict['energy_highest_lying_core_state_per_atom_unit'] = 'Rydberg'
            tmp_dict['descr_highest_lying_core_state_per_atom'] = descr_max
            out_dict['core_states_group'] = tmp_dict
        except:
            msg = "Error parsing output of KKRimp: core_states"
            msg_list.append(msg)
            
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
            msg = "Error parsing output of KKRimp: scfinfo"
            msg_list.append(msg)            
            
        #convert arrays to lists
        from numpy import ndarray
        for key in list(out_dict.keys()):
            if type(out_dict[key])==ndarray:
                out_dict[key] = list(out_dict[key])
            elif type(out_dict[key])==dict:
                for subkey in list(out_dict[key].keys()):
                    if type(out_dict[key][subkey])==ndarray:
                        out_dict[key][subkey] = (out_dict[key][subkey]).tolist()
                        
                        
        # return output with error messages if there are any
        if len(msg_list)>0:
            return False, msg_list, out_dict
        else:
            return True, [], out_dict

