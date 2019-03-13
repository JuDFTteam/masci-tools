# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools    #
# For further information on the license, see the LICENSE.txt file            #
# For further information please visit http://www.flapw.de or                 #
#                                                                             #
###############################################################################

"""
Io routines for band structure files
"""
ry_to_ev = 13.6056917253
hartree_to_ev = ry_to_ev * 2.

def read_fleur_banddos_hdf(filepath):
    """
    Reads in the banddos.hdf file from the FLEUR code
    
    returns a dictionary containing all datasets with multidim numpy arrays 
    and also containing the attributes of the groups 
    
    :param filepath: path to the banddos.hdf file
    
    :return: xcoord, bands, xlabels, band_character, band_char_label, 
    kpoints, weights, rep_cell, cell, positions, atomicnumbers, special_point_pos 
    
    
    Expected file content:
    datasets
    [u'bravaisMatrix',
     u'numFoundEigenvals',
     u'specialPointIndices',
     u'lLikeCharge',
     u'positions',
     u'atomicNumbers',
     u'coordinates',
     u'weights',
     u'reciprocalCell',
     u'eigenvalues',
     u'specialPointLabels',
     u'equivAtomsGroup']
    
    attributes:
    {u'lastFermiEnergy': array([0.20852455]),
     u'maxL': array([3], dtype=int32),
     u'nAtoms': array([2], dtype=int32),
     u'nSpecialPoints': array([7], dtype=int32),
     u'nTypes': array([1], dtype=int32),
     u'neigd': array([19], dtype=int32),
     u'nkpt': array([100], dtype=int32),
     u'spins': array([1], dtype=int32),
     u'version': array([1], dtype=int32)}
    """
    import numpy as np
    from masci_tools.io.io_hdf5 import read_hdf
    
    xcoord, bands, xlabels, band_character, band_char_label = [],[],[],[],[]
    
    # read in file
    datasets, groups, group_attrs = read_hdf(filepath)
    
    # correct eigenvalues with Fermi energy
    fermien_htr = group_attrs.read(u'lastFermiEnergy', None)
    
    eig = datasets['eigenvalues']
    print(len(eig), len(eig[-1]), len(eig[-1][-1]))
    bands_tmp = [eig[0].transpose()]
    if len(eig)==2: # wo spins
        bands_tmp.append(eig[1].transpose())
    
    for i, spinband in enumerate(bands_tmp):
        bands_s = []
        for j, band in enumerate(spinband):
            bands_s.append((np.array(band) - fermien_htr)*hartree_to_ev)
        bands.append(bands_s)
    
    print(len(bands))
    # get special points
    nspecial_labels = group_attrs.read(u'nSpecialPoints', [0])[0]
    if nspecial_labels > 0:
        special_point_labels = list(datasets.read(u'specialPointLabels', []))
        special_point_pos = list(datasets.read(u'specialPointIndices', []))
        
        for i, special_label in enumerate(special_point_labels):
            label = special_label.rstrip()
            if label == u'g':
                label = u'Gamma'
            special_point_labels[i] = label
    else:
        special_point_pos = None
    
    # construct kpoint path
    kpoints = datasets.read('coordinates', None)
    if kpoints is None:
        return None
    
    rep_cell = datasets['reciprocalCell']
    repc = np.array(rep_cell)
    xc = 0.0 
    xcoord.append(xc)
    for i, kpt in enumerate(kpoints[1:]):
        if nspecial_labels > 0:
            if i+1 in special_point_pos:
                index = special_point_pos.index(i+1)
                xlabels.append([special_point_labels[index], xc])
        # get the right length for the path
        diff = np.matmul(repc,kpoints[i]) - np.matmul(repc,kpt)
        abst = np.sqrt(diff[0]**2+diff[1]**2+diff[2]**2)
        xc = xc + abst
        xcoord.append(xc)

    
    band_character = datasets['lLikeCharge'] # for each [kpoint (s,p,d,f), TODO, check because is optiona; output
    
    cell = datasets['bravaisMatrix']
    positions = datasets['positions']
    atomicnumbers = datasets['atomicNumbers']
    weights = datasets['weights']
    
    return xcoord, bands, xlabels, band_character, band_char_label, kpoints, weights, rep_cell, cell, positions, atomicnumbers, special_point_pos
    
