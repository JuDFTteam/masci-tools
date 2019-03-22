#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Here commonly used functions that do not need aiida-stuff (i.e. can be tested 
without a database) are collected.
"""
from __future__ import print_function
from __future__ import division

from builtins import range
__copyright__ = (u"Copyright (c), 2018, Forschungszentrum Jülich GmbH,"
                 "IAS-1/PGI-1, Germany. All rights reserved.")
__license__ = "MIT license, see LICENSE.txt file"
__contributors__ = (u"Philipp Rüßmann")
__version__ = 1.0

####################################################################################

#helper functions used in calculation, parser etc.
def get_alat_from_bravais(bravais, is3D=True):
    from numpy import sqrt, sum
    bravais_tmp = bravais
    if not is3D:
        #take only in-plane lattice to find maximum as alat
        bravais_tmp = bravais[:2,:2]
    return sqrt(sum(bravais_tmp**2, axis=1)).max()
    
def get_Ang2aBohr():
    return 1.8897261254578281
    
def get_aBohr2Ang():
    return 1/get_Ang2aBohr()

def get_Ry2eV():
    return 13.605693009
    
def search_string(searchkey, txt):
    iline = 0
    for line in txt:
        if searchkey in line:
            return iline
        iline+=1
    return -1


def angles_to_vec(magnitude, theta, phi):
    """
    convert (magnitude, theta, phi) to (x,y,z)
    
    theta/phi need to be in radians!
    
    Input can be single number, list of numpy.ndarray data
    Returns x,y,z vector 
    """
    from numpy import ndarray, array, cos, sin
    
    # correct data type if necessary
    if type(magnitude) == list:
        magnitude = array(magnitude)
    if type(theta) == list:
        theta = array(theta)
    if type(phi) == list:
        phi = array(phi)
    single_value_input = False
    if type(magnitude) != ndarray:
        magnitude = array([magnitude])
        single_value_input = True
    if type(theta) != ndarray:
        theta = array([theta])
        single_value_input = True
    if type(phi) != ndarray:
        phi = array([phi])
        single_value_input = True
        
    vec = []
    for ivec in range(len(magnitude)):
        r_inplane = magnitude[ivec]*sin(theta[ivec])
        x = r_inplane*cos(phi[ivec])
        y = r_inplane*sin(phi[ivec])
        z = cos(theta[ivec])*magnitude[ivec]
        vec.append([x,y,z])
    vec = array(vec)   
    
    if single_value_input:
        vec = vec[0]
        
    return vec


def vec_to_angles(vec):
    """
    converts vector (x,y,z) to (magnitude, theta, phi)
    """
    from numpy import array, arctan2, sqrt, shape
    magnitude, theta, phi = [], [], []
    if len(vec)==3 and len(shape(vec))<2:
        vec = array([vec])
        multiple_entries = False
    else:
        multiple_entries = True
        
    for ivec in range(len(vec)):
        phi.append(arctan2(vec[ivec, 1], vec[ivec, 0]))
        r_inplane = sqrt(vec[ivec, 0]**2+vec[ivec, 1]**2)
        theta.append(arctan2(r_inplane, vec[ivec, 2]))
        magnitude.append(sqrt(r_inplane**2+vec[ivec, 2]**2))
    if multiple_entries:
        magnitude, theta, phi = array(magnitude), array(theta), array(phi)
    else:
        magnitude, theta, phi = magnitude[0], theta[0], phi[0]
    return magnitude, theta, phi
    


def get_version_info(outfile):
    f = open(outfile)
    tmptxt = f.readlines()
    f.close()
    itmp = search_string('Code version:', tmptxt)
    if itmp==-1: # try to find serial number from header of file
        itmp = search_string('# serial:', tmptxt)
        code_version = tmptxt[itmp].split(':')[1].split('_')[1].strip()
        compile_options = tmptxt[itmp].split(':')[1].split('_')[2].strip()
        serial_number = tmptxt[itmp].split(':')[1].split('_')[3].strip()
    else:
        code_version = tmptxt.pop(itmp).split(':')[1].strip()
        itmp = search_string('Compile options:', tmptxt)
        compile_options = tmptxt.pop(itmp).split(':')[1].strip()
        itmp = search_string('serial number for files:', tmptxt)
        serial_number = tmptxt.pop(itmp).split(':')[1].strip()
    return code_version, compile_options, serial_number


def get_corestates_from_potential(potfile='potential'):
    """Read core states from potential file"""
    from numpy import zeros
    txt = open(potfile).readlines()

    #get start of each potential part
    istarts = [iline for iline in range(len(txt)) if 'POTENTIAL' in txt[iline]]
    print(istarts)

    n_core_states = [] #number of core states per potential
    e_core_states = [] #energies of core states
    l_core_states = [] #angular momentum index, i.e. 0=s, 1=p etc...
    for ipot in range(len(istarts)):
        line = txt[istarts[ipot]+6]
        n = int(line.split()[0])
        print(ipot, n)
        n_core_states.append(n)
        elevels = zeros(n) #temp array for energies
        langmom = zeros(n, dtype=int) #temp array for angular momentum index
        for icore in range(n):
            line = txt[istarts[ipot]+7+icore].split()
            langmom[icore] = int(line[0])
            elevels[icore] = float(line[1].replace('D', 'E'))
        e_core_states.append(elevels)
        l_core_states.append(langmom)

    return n_core_states, e_core_states, l_core_states


def get_highest_core_state(nstates, energies, lmoments):
    """Find highest lying core state from list of core states, needed to find and check energy contour"""
    idx = energies.argmax()
    lval = lmoments[idx]
    nquant = sum(lmoments == lval) + lval
    level_descr = '%i%s'%(nquant, 'spdfgh'[lval])

    return lval, energies[idx], level_descr


def interpolate_dos(dospath, return_original=False, ):
    """
    interpolation function copied from complexdos3 fortran code
    
    Principle of DOS here: Two-point contour integration
    for DOS in the middle of the two points. The input DOS
    and energy must be complex. Parameter deltae should be
    of the order of magnitude of eim::
        
              <-2*deltae->   _
                   /\        |     DOS=(n(1)+n(2))/2 + (n(1)-n(2))*eim/deltae
                  /  \       |
                (1)  (2)   2*i*eim=2*i*pi*Kb*Tk
                /      \     |
               /        \    |
        ------------------------ (Real E axis)
    
    :param input: dospath, path where 'complex.dos' file can be found
    
    :returns: E_Fermi, numpy array of interpolated dos 
    
    :note: output units are in Ry!
    """
    from numpy import array, real, imag
    
    f = open(dospath+'/complex.dos', 'r')
    text = f.readline() # dummy readin of header, may be replaced later
    npot = int(f.readline().split()[0])
    iemax = int(f.readline().split()[0])
    lmax = int(f.readline().split()[0])
    
    dosnew_all_atoms = []
    dos_all_atoms = []
    
    for i1 in range(npot):
        #print('Reading potential',i1)
        # Read header (not used)
        for iheader in range(3):
            text = f.readline()
        
        # extract EF
        ef = float(f.readline().split()[7])
        
        # some more dummy lines
        for iheader in range(5,9+1):
            text = f.readline()
        
        # now header is done. start reading DOS
        # Read dos: (total dos stored at DOS(LMAX+1,IE))
        dos_l_cmplx = []
        for ie in range(iemax):
            tmpline = f.readline().replace('(','').replace(')','').replace(',','').split()
            ez = float(tmpline[0])+1j*float(tmpline[1])
            dostmp_complex = [[tmpline[len(tmpline)-2], tmpline[len(tmpline)-1]]]
            dostmp_complex += [[tmpline[iline], tmpline[iline+1]] for iline in range(2,len(tmpline)-2,2)]
            dostmp = [ez]+[float(ds[0])+1j*float(ds[1]) for ds in dostmp_complex]
            dos_l_cmplx.append(dostmp)
        dos_l_cmplx = array(dos_l_cmplx)
        dos_l = imag(dos_l_cmplx.copy())
        dos_l[:,0] = real(dos_l_cmplx.copy()[:,0])
        dos_all_atoms.append(dos_l)
        
        # Compute and write out corrected dos at new (middle) energy points:
        dosnew = []
        ez = dos_l_cmplx[:,0]
        for ie in range(1, iemax-1):
            deltae = real(ez[ie+1] - ez[ie])
            eim = imag(ez[ie])
            enew = real(ez[ie]) # Real quantity
        
            tmpdos = [enew]
            for ll in range(1,lmax+3):
                t = (dos_l_cmplx[ie-1, ll]-dos_l_cmplx[ie+1, ll])*0.5*(0.0+eim*1j)/deltae
                #print ie+1, ll,  dos_l_cmplx[ie, ll], deltae, eim, t, shape(dos_l_cmplx[ie]), lmax
                #tmpdos.append(dos_l_cmplx[ie, ll] + 0.5*(dos_l_cmplx[ie-1, ll]-dos_l_cmplx[ie+1, ll])*(0.+1j*eim)/deltae)
                tmpdos.append(dos_l_cmplx[ie, ll]+t)
            tmpdos = array(tmpdos)
            # build imaginary part (factor -1/2pi is already included)
            tmpdos = array([real(tmpdos[0])]+[imag(ds) for ds in tmpdos[1:]])
            dosnew.append(tmpdos)
        
        # save to big array with all atoms
        dosnew_all_atoms.append(dosnew)
        
        if i1 != npot:
            text = f.readline() # dummy line
            
    dosnew_all_atoms = array(dosnew_all_atoms)
    dos_all_atoms = array(dos_all_atoms)
    
    # close complex.dos file
    f.close()
    
    if return_original:
        return ef, dos_all_atoms, dosnew_all_atoms
    else:
        return ef, dosnew_all_atoms
    
def get_ef_from_potfile(potfile):
    """
    extract fermi energy from potfile
    """
    f = open(potfile)
    txt = f.readlines()
    f.close()
    ef = float(txt[3].split()[1])
    return ef
  
