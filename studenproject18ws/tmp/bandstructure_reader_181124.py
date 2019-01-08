#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 17:00:10 2018

@author: christianpartmann
"""

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import pyplot as plt
import h5py
from collections import Counter

bohr_constant = 0.52

filepath = '../data/input/'
#filename = 'banddos_4x4'
filename = 'banddos'
#filename = 'banddos_Co'
f = h5py.File(filepath+filename+str('.hdf'), 'r')


Eigenvalues = f["/eigenvalues/eigenvalues"]
llikecharge =  f["/eigenvalues/lLikeCharge"]
# 3d coordinates of the path along which E_n(kx, ky, kz) is sampled
kpts_int = f["/kpts/coordinates"]
# index of the high symmetry points
special_points = f["/kpts/specialPointIndices"]
special_points_label = f["/kpts/specialPointLabels"]
# fermi_energy of the system
fermi_energy = f["/general"].attrs['lastFermiEnergy'][0]

# useless quantities
weights1 = f["/kpts/weights"]
jsym = f["/eigenvalues/jsym"][0]
ksym = f["/eigenvalues/ksym"][0]
numFoundEigenvals = f["/eigenvalues/numFoundEigenvals"]

# unfloding True/False
band_unfolding = f["/general"].attrs['bandUnfolding'][0]

# weight for each E_n(k)
if(band_unfolding == True):
    weights2 = f["/bandUnfolding/weights"]


rec_cell = f["/cell/reciprocalCell"][:]
bravais = f["/cell/bravaisMatrix"][:]*bohr_constant

atoms_coords_int = f["/atoms/positions"]
atom_group = f["/atoms/equivAtomsGroup"]

def internal_to_pyhsical_x(x_int, bravais):
# x_ext_ik = A_ij * x_int_jk --> should be correct maybe up to transposition 
    return np.dot(x_int, bravais)

def internal_to_pyhsical_k(kpt_int, rec_cell):
    return np.dot(kpt_int, rec_cell)

# convert to physical dimensions
atoms_coords = internal_to_pyhsical_x(atoms_coords_int, bravais)
kpts = internal_to_pyhsical_k(kpts_int, rec_cell)
Number_atom_groups = max(atom_group[:])
#%%
# =============================================================================
# Visualization of the realspace lattice:
# =============================================================================
def create_colorbar(N):
    colors = []
    m = int(N**(1./3))+1
    for i in range(m):
        for j in range(m):
            for k in range(m):
                colors += [(i*1./m, j*1./m, k*1./m)]
    return colors

def plot_atoms_with_colors():
    colorbar = create_colorbar(Number_atom_groups)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(atoms_coords[:].T[0])):
        x = atoms_coords[:].T[0][i]
        y = atoms_coords[:].T[1][i]
        z = atoms_coords[:].T[2][i]
        ax.scatter(x, y, z, c=colorbar[atom_group[i]])

    plt.xlabel("x")
    plt.ylabel("y")
    # plt.savefig("../data/output/"+filename+"_3d_visualization_color.png", dpi = 500)
    plt.show()


plot_atoms_with_colors()

#%%
# =============================================================================
# Visualize the Energy-Eigenvalues including weights, character...   
# =============================================================================

# get k spacing along the path in the Brillouin Zone
def create_k_spacing():
    kx = kpts[:].T[0]
    ky = kpts[:].T[1]
    kz = kpts[:].T[2]
    k_dist = np.zeros(len(kx))
    k_dist[0] = 0
    
    for i in range(1, len(kx)):
        k_dist[i] = k_dist[i-1] + np.sqrt((kx[i]-kx[i-1])**2 +(ky[i]-ky[i-1])**2 +(kz[i]-kz[i-1])**2)
    return k_dist

k_dist = create_k_spacing()

# get the k values of the high symmetry points
def get_k_special_pt():
    k_special_pt = np.zeros(len(special_points[:]))
    for i in range(len(special_points[:])):
        k_special_pt[i] = k_dist[special_points[i]-1]
    return k_special_pt

k_special_pt = get_k_special_pt()

# Returns E(k) for the i-th Band
def E_i(i, spin = 0):
    return Eigenvalues[spin].T[i]


# returns reduced weights:
# - sums over selected characters {s, p, d, f}
# - sums over weighted (selected) atomgroups 
# - returns array for (k, n)

# needs to be changed, very ugly...
atoms_per_group_dict = Counter(atom_group)
atom_group_keys = atoms_per_group_dict.keys()
atoms_per_group = np.zeros(max(atom_group_keys))
for i in range(max(atom_group_keys)):
    atoms_per_group[i] = atoms_per_group_dict[i]
    
all_characters = [0, 1, 2, 3]
all_groups = range(max(atom_group_keys))
all_bands = range(Eigenvalues.shape[2])

def weights(characters, groups, spin):
    weights_reduced = np.zeros((Eigenvalues.shape[2], len(kpts)))
    weights_norm = np.zeros((Eigenvalues.shape[2], len(kpts)))
    
    # this can surely be improved with matrix product method and sum
    # second loop for normalization is even partially redundant...
    for group in groups:
        for character in characters:
            weights_reduced += atoms_per_group_dict[group] * llikecharge[spin][:].T[character][group][:]
            
    for group in range(max(atom_group_keys)):
        for character in range(4):
            weights_norm += atoms_per_group[group] * llikecharge[spin][:].T[character][group][:]
    
    return weights_reduced/weights_norm


# combines reduced l-like weights and unfolding weights
# returns array for (k, n)
def combined_weight(characters, groups, spin, unfolding_weight):
    if(unfolding_weight == True):
        return weights(characters, groups, spin) * weights2[spin].T[:]
    else:
        return weights(characters, groups, spin)


def new_plotfunction_weights(bands, characters, groups, spin, unfolding_weight):
    
    weight_k_n = combined_weight(characters, groups, spin, unfolding_weight)
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    
    for n in bands:
        weight_k_n[n]
        ax1.scatter(k_dist, E_i(n, spin), marker='o', c='b', s = 2 * weight_k_n[n], lw=0)
    
    plt.xticks(k_special_pt, special_points_label)
    
    """
    for i in range(len(special_points)):
        index = special_points[i]
        plt.vlines(k_dist[index-1], -0.2, 0.4)
    """
    plt.xlim(0, max(k_dist))

new_plotfunction_weights(all_bands, all_characters, all_groups, spin = 0, unfolding_weight = band_unfolding)

#new_plotfunction_weights(all_bands, all_characters, all_groups, spin = 1, unfolding_weight = band_unfolding)
#plt.savefig("Output/newplot_weights.png", dpi=2000)


#%%
#range(max(atom_group_keys))

"""
def plot_bands_with_weight(Number_Bands_plotted, weight = True):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    max_E = max(E_i(0))
    min_E = min(E_i(0))
    
    ax1.hlines(fermi_energy, 0, max(k_dist))
    
    for n in range(Number_Bands_plotted):
        #ax1.scatter(k_dist, E_i(n), marker='.', c='b', s=weight_for_band_i(n))
        if(weight == True):
            ax1.scatter(k_dist, E_i(n), marker='o', c='b', s=3*weight_for_band_i(n), lw=0)
        else:
            ax1.scatter(k_dist, E_i(n), marker='o', c='b', s=0.1, lw=0)
        if(max_E < max(E_i(n))):
            max_E = max(E_i(n))
        if(min_E > min(E_i(n))):
            min_E = min(E_i(n))
        print("%i/%i"%(n, Number_Bands_plotted))
    
    # label of the special points is still missing...
    for i in range(len(special_points)):
        index = special_points[i]
        plt.vlines(k_dist[index-1], min_E, max_E)
        
    plt.xlabel("k")
    plt.ylabel("E(k)")
    if(weight == True):
        plt.savefig("output/"+filename+"_bandstructure_weight.png", dpi=2000)
    else:
        plt.savefig("output/"+filename+"_bandstructure_noweight.png", dpi=2000)    
"""


#k_dist = create_k_spacing()
#Number_Bands_plotted = Eigenvalues.shape[2] #5
#if(band_unfolding == True):
#    plot_bands_with_weight(Number_Bands_plotted)

#plot_bands_with_weight(Number_Bands_plotted, weight = False)
#plot_bands_with_weight(1)
    


#llikecharge
#%%


#color_scheme = ('green', 'red', 'blue', 'orange', 'black', 'cyan')

"""
# Returns array of lenght len(kpts)
# 
# i: (0, 1, 2, 3) --> probalby belongs to the orbital number s,p, d,f
# j:
# n: n-th energy-band
def llikecharge_for_band_i(i, j, n):
    return (llikecharge[0][:].T[i][j][n])
"""
"""
fig = plt.figure()
ax2 = fig.add_subplot(111)
max_orbital = (llikecharge).shape[4]
max_j = (llikecharge).shape[3]

for orbital in range(4):
    for n in range(30):
        for m in range(max_j):
            ax2.scatter(k_dist, E_i(n), marker='o', c=color_scheme[orbital], s=10*llikecharge_for_band_n(orbital, m, n), lw=0)
        
    print("%i/%i"%(orbital, 3))

           plt.savefig("output/"+filename+"_orbitals.png", dpi=2000)   
"""
#%%

"""
fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

max_orbital = (llikecharge).shape[4]
max_j = (llikecharge).shape[3]

NN = Eigenvalues.shape[2]
for n in range(NN):
    for m in range(max_j):
        orbital = 0
        # prefactor of "s" should maybe be normalized to max(llikecharge_for_band_n(orbital, m, n)) or so...
        ax1.scatter(k_dist, E_i(n), marker='o', c=color_scheme[orbital], s=4*llikecharge_for_band_n(orbital, m, n), lw=0)
        orbital = 1
        ax2.scatter(k_dist, E_i(n), marker='o', c=color_scheme[orbital], s=8*llikecharge_for_band_n(orbital, m, n), lw=0)
        orbital = 2
        ax3.scatter(k_dist, E_i(n), marker='o', c=color_scheme[orbital], s=16*llikecharge_for_band_n(orbital, m, n), lw=0)
        orbital = 3
        ax4.scatter(k_dist, E_i(n), marker='o', c=color_scheme[orbital], s=32*llikecharge_for_band_n(orbital, m, n), lw=0)
        
    print("%i/%i"%(n, NN))

plt.savefig("output/"+filename+"_orbitals_compare.png", dpi=2000)
"""

"""   
# Returns array of lenght len(kpts)
# c: (0, 1, 2, 3) --> probalby belongs to the orbital number s,p, d,f
# g: atom groups
# n: n-th energy-band
def llikecharge_for_band_n(c, g, n, spin = 0):
    return (llikecharge[spin][:].T[c][g][n])
"""
"""
# Returns unfolding weight (n,k)
def unfold_weighti(unfolding_weight = True, spin = 0):
    if(unfolding_weight == True):
        return weights2[spin].T
    else:
        return 1
"""