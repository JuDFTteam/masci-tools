#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools for the impurity caluclation plugin and its workflows
"""
#use print('message') instead of print 'message' in python 2.7 as well:
from __future__ import print_function
# redefine raw_input for python 3/2.7 compatilbility
from sys import version_info
if version_info[0] >= 3:
    def raw_input(msg):
        return input(msg)
         
__copyright__ = (u"Copyright (c), 2018, Forschungszentrum Jülich GmbH,"
                 "IAS-1/PGI-1, Germany. All rights reserved.")
__license__ = "MIT license, see LICENSE.txt file"
__version__ = "0.3"
__contributors__ = u"Philipp Rüßmann"


class modify_potential():
    """
    Class for old modify potential script, ported from modify_potential script, initially by D. Bauer
    """
    
    def _check_potstart(self, str1, mode='pot', shape_ver='new'):
        if mode=='shape':
            if shape_ver=='new':
                check1='Shape number' in str1
            else:
                check1= (len(str1)==11)
        else:
            check1='exc:' in str1
        return check1
        
    def _read_input(self, filepath):
        #print(filepath)
        with open(filepath) as file:
            data = file.readlines()
        
        if 'shapefun' in filepath:
            mode = 'shape'
        else:
            mode = 'pot'
        
        #print(mode, len(data))
            
        # read file
        index1=[];index2=[]
        for i in range(len(data)):
          if self._check_potstart(data[i], mode=mode):
            index1.append(i)
            if len(index1)>1: index2.append(i-1)
        index2.append(i)
        
        # read shapefun if old style is used
        if mode=='shape' and len(index1)<1:
            index1=[];index2=[]
            for i in range(len(data)):
                if self._check_potstart(data[i], mode=mode, shape_ver='old'):
                    index1.append(i)
                if len(index1)>1: index2.append(i-1)
                index2.append(i)
           
        """
        print(index1)
        print(index2)
        
        print('Potential file read')
        print('found %i potentials in file'%len(index1))
        print('')
        """
        
        return index1, index2, data

    def shapefun_from_scoef(self, scoefpath, shapefun_path, atom2shapes, shapefun_new):
        """
        Read shapefun and create impurity shapefun using scoef info and shapes array
        
        :param scoefpath: absolute path to scoef file
        :param shapefun_path: absolute path to input shapefun file
        :param shapes: shapes array for mapping between atom index and shapefunction index
        :param shapefun_new: absolute path to output shapefun file to which the new shapefunction will be written
        """
        index1, index2, data = self._read_input(shapefun_path)
        
        order=range(len(index1))
               
        natomtemp = int(open(scoefpath).readlines()[0])
        filedata=open(scoefpath).readlines()[1:natomtemp+1]
        listnew=[]
        for line in filedata:
            if (len(line.split())>1):
                listnew.append(atom2shapes[int(line.split()[3])-1]-1)
        order = listnew
        
        datanew=[]
        for i in range(len(order)):
          for ii in range(index1[order[i]], index2[order[i]]+1  ):
            datanew.append(data[ii])
            
        # add header to shapefun_new
        tmp = datanew
        datanew = []
        datanew.append('   %i\n' %(len(order)))
        datanew.append('  1.000000000000E+00\n')
        datanew += tmp
        open(shapefun_new,'w').writelines(datanew)
        
    def neworder_potential(self, potfile_in, potfile_out, neworder, potfile_2=None, replace_from_pot2=None):
        """
        Read potential file and new potential using a list describing the order of the new potential.
        If a second potential is given as input together with an index list, then the corresponding of 
        the output potential are overwritten with positions from the second input potential.
        
        :param potfile_in: absolute path to input potential
        :type potfile_in: str
        :param potfile_out: absolute path to output potential
        :type potfile_out: str
        :param neworder: list after which output potential is constructed from input potential
        :type neworder: list
        :param potfile_2: optional, absolute path to second potential file if 
            positions in new list of potentials shall be replaced by positions of 
            second potential, requires *replace_from_pot* to be given as well
        :type potfile_2: str
        :param replace_from_pot: optional, list containing tuples of (position 
            in newlist that is to be replaced, position in pot2 with which position 
            is replaced)
        :type replace_from_pot: list
        
        :usage:
            1. modify_potential().neworder_potential(<path_to_input_pot>, <path_to_output_pot>, [])
        """
        from numpy import array, shape
        
        index1, index2, data = self._read_input(potfile_in)
        
        if potfile_2 is not None:
            index12, index22, data2 = self._read_input(potfile_2)
            # check if also replace_from_pot2 is given correctly
            if replace_from_pot2 is None:
                raise ValueError('replace_from_pot2 not given')
            else:
                replace_from_pot2 = array(replace_from_pot2)
                if shape(replace_from_pot2)[1]!=2:
                    raise ValueError('replace_from_pot2 needs to be a 2D array!')
        else:
            if replace_from_pot2 is not None:
                raise ValueError('replace_from_pot2 given but potfile_2 not given')
        
        # set order in which potential file is written
        # ensure that numbers are integers:
        order = [int(i) for i in neworder]
                
        datanew=[]
        for i in range(len(order)):
            # check if new position is replaced with position from old pot
            if replace_from_pot2 is not None and i in replace_from_pot2[:,0]:
                    replace_index = replace_from_pot2[replace_from_pot2[:,0]==i][0][1]
                    for ii in range(index12[replace_index], index22[replace_index]+1 ):
                        datanew.append(data2[ii])
            else: # otherwise take new potntial according to input list
                    for ii in range(index1[order[i]], index2[order[i]]+1 ):
                        datanew.append(data[ii])
        
        # write out new potential
        open(potfile_out,'w').writelines(datanew)
        
        
        
        
class kkrimp_parser_functions():
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
        from aiida_kkr.tools.common_functions import search_string
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
        from aiida_kkr.tools.common_functions import search_string
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
        from aiida_kkr.tools.common_functions import search_string
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
        from aiida_kkr.tools.common_functions import search_string
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
        from aiida_kkr.tools.common_functions import search_string
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
        from aiida_kkr.tools.common_functions import search_string
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
        from aiida_kkr.tools.common_functions import search_string
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
        from aiida_kkr.tools.kkrparser_functions import get_rms, find_warnings, get_charges_per_atom, get_core_states
        from aiida_kkr.tools.common_functions import get_version_info, get_Ry2eV
        
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
            natyp = int(len(result_tot)/niter)
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
        for key in out_dict.keys():
            if type(out_dict[key])==ndarray:
                out_dict[key] = list(out_dict[key])
            elif type(out_dict[key])==dict:
                for subkey in out_dict[key].keys():
                    if type(out_dict[key][subkey])==ndarray:
                        out_dict[key][subkey] = (out_dict[key][subkey]).tolist()
                        
                        
        # return output with error messages if there are any
        if len(msg_list)>0:
            return False, msg_list, out_dict
        else:
            return True, [], out_dict


####################################################################################
# for create scoef functions
import numpy as np

def get_structure_data(structure):
    """
    Function to take data from AiiDA's StructureData type and store it into a single numpy array of the following form:
    a = [[x-Position 1st atom, y-Position 1st atom, z-Position 1st atom, index 1st atom, charge 1st atom, 0.],
         [x-Position 2nd atom, y-Position 2nd atom, z-Position 2nd atom, index 2nd atom, charge 1st atom, 0.],
         [..., ..., ..., ..., ..., ...],
         ...
         ]
    
    :param structure: input structure of the type StructureData
    
    :return: numpy array a[# of atoms in the unit cell][5] containing the structure related data (positions in units
             of the unit cell length)
    
    :note:   
    """
    
    #import packages
    from aiida.common.constants import elements as PeriodicTableElements
    from aiida_kkr.tools.common_functions import get_Ang2aBohr, get_alat_from_bravais
    import numpy as np
    
    #list of globally used constants
    a_to_bohr = get_Ang2aBohr()
    
    #get the connection between coordination number and element symbol
    _atomic_numbers = {data['symbol']:num for num,
                data in PeriodicTableElements.iteritems()}    
    

    #convert units from Å to Bohr (KKR needs Bohr)
    bravais = np.array(structure.cell)*a_to_bohr
    alat = get_alat_from_bravais(bravais, is3D=structure.pbc[2])
    #bravais = bravais/alat  
    
    #initialize the array that will be returned later (it will be a (# of atoms in the cell) x 6-matrix)
    a = np.zeros((len(structure.sites),6))
    k = 0 #running index for filling up the array with data correctly
    charges = [] #will be needed to return the charge number for the different atoms later  

    #loop to fill up the a-array with positions, index, charge and a 0. for every atom in the cell
    sites = structure.sites 
    n = len(structure.sites) + 1 #needed to do the indexing of atoms
    m = len(structure.sites) #needed to do the indexing of atoms
    for site in sites:
        for j in range(3):
            a[k][j] = site.position[j]*a_to_bohr/alat          
        sitekind = structure.get_kind(site.kind_name)
        naez = n - m
        m = m - 1
        #convert the element symbol from StructureData to the charge number
        for ikind in range(len(sitekind.symbols)):
            site_symbol = sitekind.symbols[ikind]
            charges.append(_atomic_numbers[site_symbol])  
        i = len(charges) - 1
        a[k][3] = int(naez)
        a[k][4] = float(charges[i])
        k = k + 1
        
    return a        

def select_reference(structure_array, i):
    """
    Function that references all of the atoms in the cell to one particular atom i in the cell and calculates 
    the distance from the different atoms to atom i. New numpy array will have the form:
    x = [[x-Position 1st atom, y-Position 1st atom, z-Position 1st atom, index 1st atom, charge 1st atom, 
            distance 1st atom to atom i],
         [x-Position 2nd atom, y-Position 2nd atom, z-Position 2nd atom, index 2nd atom, charge 1st atom, 
            distance 1st atom to atom i],
         [..., ..., ..., ..., ..., ...],
         ...
         ]
    
    :param structure_array: input array of the cell containing all the atoms (obtained from get_structure_data)
    :param i: index of the atom which should be the new reference
    
    :return: new structure array with the origin at the selected atom i (for KKRimp: impurity atom)
    
    :note: the first atom in the structure_array is labelled with 0, the second with 1, ...
    """
    
    #import packages
    import numpy as np
    
    #initialize new array for data centered around atom i
    x = np.zeros((len(structure_array),6))
    
    #take the positions of atom i as new origin
    x_ref = np.array([structure_array[i][0], structure_array[i][1], structure_array[i][2], 0, 0, 0])
    
    #calculate the positions and distances for all atoms in the cell with respect to the chosen atom i
    for k in range(len(structure_array)):
        x[k][5] = get_distance(structure_array, i, k)
        for j in range(5):
            x[k][j] = structure_array[k][j] - x_ref[j]
      
    return x

def get_distance(structure_array, i, j):
    """
    Calculates and returns the distances between to atoms i and j in the given structure_array
    
    :param structure_array: input numpy array of the cell containing all the atoms ((# of atoms) x 6-matrix)
    :params i, j: indices of the atoms for which the distance should be calculated (indices again start at 0)
    
    :return: distance between atoms i and j in units of alat
    
    :note:
    """
    
    #import math package for square root calculation
    import math
    
    #calculate x-, y-, z-components of distance of i and j 
    del_x = structure_array[i][0] - structure_array[j][0]
    del_y = structure_array[i][1] - structure_array[j][1]
    del_z = structure_array[i][2] - structure_array[j][2]
    
    #return absolute value of the distance of atom i and j
    return math.sqrt(del_x*del_x + del_y*del_y + del_z*del_z)

def rotate_onto_z(structure, structure_array, vector):
    """
    Rotates all positions of a structure array of orientation 'orient' onto the z-axis. Needed to implement the
    cylindrical cutoff shape.
    
    :param structure: input structure of the type StructureData
    :param structure_array: input structure array, obtained by select_reference for the referenced system.
    :param vector: reference vector that has to be mapped onto the z-axis. 
                   
    :return: rotated system, now the 'orient'-axis is aligned with the z-axis
    """    
    
    from aiida_kkr.tools.common_functions import vec_to_angles
    import math
    import numpy as np
    
    #get angles, from vector
    angles = vec_to_angles(vector)
    theta = angles[1]
    phi = angles[2]
    
    #initialize needed arrays
    x_res = np.delete(structure_array, np.s_[3:6], 1)
    x_temp_1 = np.delete(structure_array, np.s_[3:6], 1)
    x_temp_2 = np.delete(structure_array, np.s_[3:6], 1)
    
    #define rotation matrices
    #========================
    #rotation around z-axis with angle phi
    R_z = np.array([[math.cos(-phi), -math.sin(-phi), 0.],
                    [math.sin(-phi), math.cos(-phi), 0.],
                    [0., 0., 1]])
    #rotation around y-axis with angle theta
    R_y = np.array([[math.cos(-theta), 0, math.sin(-theta)],
                    [0., 1., 0.],
                    [-math.sin(-theta), 0., math.cos(-theta)]])

    #first rotate around z-axis
    for i in range(len(structure_array)):
        x_temp_1[i] = np.dot(R_z, x_res[i])
        x_temp_2[i] = np.dot(R_y, x_temp_1[i])
    
    return x_temp_2

def find_neighbors(structure, structure_array, i, radius, clust_shape='spherical', h=0., vector=[0., 0., 1.]):
    """
    Applies periodic boundary conditions and obtains the distances between the selected atom i in the cell and 
    all other atoms that lie within a cutoff radius r_cut. Afterwards an numpy array with all those atoms including 
    atom i (x_res) will be returned.
    
    :param structure: input parameter of the StructureData type containing the three bravais lattice cell vectors
    :param structure_array: input numpy structure array containing all the structure related data
    :param i: centered atom at which the origin lies (same one as in select_reference)
    :param radius: Specifies the radius of the cylinder or of the sphere, depending on clust_shape. 
                   Input in units of the lattice constant. 
    :param clust_shape: specifies the shape of the cluster that is used to determine the neighbors for the 'scoef' file.
                        Default value is 'spherical'. Other possible forms are 'cylindrical' ('h' and 'orient' 
                        needed), ... .
    :param h: needed for a cylindrical cluster shape. Specifies the height of the cylinder. Default=0. 
              Input in units of the lattice constant.
    :param vector: needed for a cylindrical cluster shape. Specifies the orientation vector of the cylinder. Default:
                   z-direction.
                  
    :return: array with all the atoms within the cutoff (x_res)
    
    :ToDo: - dynamical box construction (r_cut determines which values n1, n2, n3 have)
           - different cluster forms (spherical, cylinder, ...), add default parameters, better solution for 'orient'
    """
    
    #import packages
    from aiida_kkr.tools.common_functions import get_Ang2aBohr, get_alat_from_bravais
    import numpy as np
    import math
    
    #list of globally used constants
    a_to_bohr = get_Ang2aBohr()
    
    #conversion into units of the lattice constant
    bravais = np.array(structure.cell)*a_to_bohr
    alat = get_alat_from_bravais(bravais, is3D=structure.pbc[2])
    
    #obtain cutoff distance from radius and h
    dist_cut = max(radius, h)
    
    #initialize arrays and reference the system 
    x = select_reference(structure_array, i)
    center = x[i]
    x_temp = np.array([x[i]]) 
    
    #calculate needed amount of boxes in all three directions
    #========================================================
    #spherical approach (same distance in all three directions)
    if clust_shape == 'spherical':
        box_1 = int(radius/(structure.cell_lengths[0]*a_to_bohr/alat) + 1)
        box_2 = int(radius/(structure.cell_lengths[1]*a_to_bohr/alat) + 1)
        box_3 = int(radius/(structure.cell_lengths[2]*a_to_bohr/alat) + 1)
    #cylindrical shape (different distances for the different directions)
    elif clust_shape == 'cylindrical':
        maxval = max(h/2., radius)
        box_1 = int(maxval/(structure.cell_lengths[0]*a_to_bohr/alat) + 1)
        box_2 = int(maxval/(structure.cell_lengths[1]*a_to_bohr/alat) + 1)
        box_3 = int(maxval/(structure.cell_lengths[2]*a_to_bohr/alat) + 1)  
    #================================================================================================================
  
    #create array of all the atoms in an expanded system
    box = max(box_1, box_2, box_3)
    for j in range(len(x)):
        for n in range(-box, box + 1):
            for m in range(-box, box + 1):
                for l in range(-box, box + 1):
                    x_temp = np.append(x_temp, [[x[j][0] + (n*structure.cell[0][0] + m*structure.cell[1][0] + 
                                                     l*structure.cell[2][0])*a_to_bohr/alat, 
                                                 x[j][1] + (n*structure.cell[0][1] + m*structure.cell[1][1] + 
                                                     l*structure.cell[2][1])*a_to_bohr/alat,
                                                 x[j][2] + (n*structure.cell[0][2] + m*structure.cell[1][2] + 
                                                     l*structure.cell[2][2])*a_to_bohr/alat, 
                                                 x[j][3], x[j][4], 0.]], axis = 0)
      
    #x_temp now contains all the atoms and their positions regardless if they are bigger or smaller than the cutoff
    x_new = x_temp
    
    #calculate the distances between all the atoms and the center atom i
    for j in range(len(x_temp)):
        x_new[j][5] = get_distance(x_temp, 0, j)
    
    #initialize result array
    x_res = np.array([x[i]])
    
    #only take atoms into account whose distance to atom i is smaller than the cutoff radius
    #dist_cut = dist_cut
    if clust_shape == 'spherical':
        for j in range(len(x_temp)):
            if x_new[j][5] <= dist_cut and x_new[j][5] > 0.:
                x_res = np.append(x_res, [[x_temp[j][0], 
                                             x_temp[j][1], 
                                             x_temp[j][2], 
                                             x_temp[j][3], x_temp[j][4], x_new[j][5]]], axis=0)
    elif clust_shape == 'cylindrical':
        for j in range(len(x_temp)):
            #rotate system into help system that is aligned with the z-axis
            x_help = rotate_onto_z(structure, x_temp, vector)
        
            #calculate in plane distance and vertical distance
            vert_dist = np.absolute(x_help[j][2])
            inplane_dist = math.sqrt(x_help[j][0]**2 + x_help[j][1]**2)
            #print(vert_dist, inplane_dist)
            if vert_dist <= h/2. and inplane_dist <= radius and x_new[j][5] > 0.:
                x_res = np.append(x_res, [[x_temp[j][0], 
                                             x_temp[j][1], 
                                             x_temp[j][2], 
                                             x_temp[j][3], x_temp[j][4], x_new[j][5]]], axis=0)
     
    #return an unordered array of all the atoms which are within the cutoff distance with respect to atom i
    return x_res

def write_scoef(x_res, path):
    """
    Sorts the data from find_neighbors with respect to the distance to the selected atom and writes the data
    correctly formatted into the file 'scoef'. Additionally the total number of atoms in the list is written out
    in the first line of the file.
    
    :param x_res: array of atoms within the cutoff radius obtained by find_neighbors (unsorted)
    
    :output: returns scoef file with the total number of atoms in the first line, then with the formatted positions,
             indices, charges and distances in the subsequent lines.
    """
    
    #sort the data from x_res with respect to distance to the centered atom
    m = x_res[:,-1].argsort()
    x_res = x_res[m]
    
    #write data of x_res into the 'scoef'-file
    file = open(path, 'w')
    file.write(str("{0:4d}".format(len(x_res))))
    file.write("\n")
    for i in range(len(x_res)):
        file.write(str("{0:26.19e}".format(x_res[i][0])))
        file.write(" ")
        file.write(str("{0:26.19e}".format(x_res[i][1])))
        file.write(" ")
        file.write(str("{0:26.19e}".format(x_res[i][2])))
        file.write(" ")
        file.write(str("{0:4d}".format(int(x_res[i][3]))))
        file.write(" ")
        file.write(str("{0:4.1f}".format(x_res[i][4])))
        file.write(" ")
        file.write(str("{0:26.19e}".format(x_res[i][5])))
        file.write("\n")
    file.close()

def make_scoef(structure, radius, path, h=-1., vector=[0., 0., 1.], i=0):
    """
    Creates the 'scoef' file for a certain structure. Needed to conduct an impurity KKR calculation.
    
    :param structure: input structure of the StructureData type.
    :param radius: input cutoff radius in units of the lattice constant.
    :param h: height of the cutoff cylinder (negative for spherical cluster shape). For negative values, clust_shape 
              will be automatically assumed as 'spherical'. If there will be given a h > 0, the clust_shape 
              will be 'cylindrical'.
    :param vector: orientation vector of the cylinder (just for clust_shape='cylindrical'). 
    :param i: atom index around which the cluster should be centered. Default: 0 (first atom in the structure).
    """
    
    #shape of the cluster is specified
    if h < 0.:
        clust_shape = 'spherical'
    else:
        clust_shape = 'cylindrical'
    
    #store data from StructureData type in an numpy array
    structure_array = get_structure_data(structure)
    
    #creates an array with all the atoms within a certain cluster shape and size with respect to atom i
    c = find_neighbors(structure, structure_array, i, radius, clust_shape, h, vector)  
    
    #writes out the 'scoef'-file
    write_scoef(c, path)
    return c
    
