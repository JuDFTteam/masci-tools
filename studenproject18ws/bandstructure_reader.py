#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 17:00:10 2018

SiScLab 2018 Project 8
Week1, Task 1: Plot band structure from Fleur HDF5 files.

@author: christianpartmann
"""

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import pyplot as plt
import h5py

filename = 'banddos_4x4'
#filename = 'banddos' #.hdf'

f = h5py.File(filename+str('.hdf'), 'r')

# E_n sampled at discrete k values stored in "kpts"
Eigenvalues = f["/eigenvalues/eigenvalues"]

# something related to the projection on s,p,d,f,... orbitals...
llikecharge =  f["/eigenvalues/lLikeCharge"]

# 3d coordinates of the path along which E_n(kx, ky, kz) is sampled
kpts = f["/kpts/coordinates"]

# index of the high symmetry points
special_points = f["/kpts/specialPointIndices"]

# what is this weight good for? <----------------------------------------------
weights1 = f["/kpts/weights"]

# weight for each E_n(k)
weights2 = f["/bandUnfolding/weights"]

fermi_energy = f["/general"]


#%%
# =============================================================================
# Visualization of the realspace lattice:
#   - without distinction between atom groups
#   - with distinction between atom groups
# =============================================================================

atoms_coords = f["/atoms/positions"]
atom_group = f["/atoms/equivAtomsGroup"]
Number_atom_groups = max(atom_group[:])

def plot_atoms_no_color():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Plot the values
    for i in range(len(atoms_coords[:].T[0])):
        ax.scatter(atoms_coords[:].T[0][i], atoms_coords[:].T[1][i], atoms_coords[:].T[2][i], c="blue")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig("output/"+filename+"_3d_visualization_nocolor.png", dpi = 500)

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
        ax.scatter(atoms_coords[:].T[0][i], atoms_coords[:].T[1][i], atoms_coords[:].T[2][i], c=colorbar[atom_group[i]])

    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig("output/"+filename+"_3d_visualization_color.png", dpi = 500)

plot_atoms_with_colors()

#%%
# =============================================================================
# Visualize the Energy-Eigenvalues including weights, character...   
# =============================================================================

def create_k_spacing():
    kx = kpts[:].T[0]
    ky = kpts[:].T[1]
    kz = kpts[:].T[2]
    k_dist = np.zeros(len(kx))
    # trivial...
    k_dist[0] = 0

    for i in range(1, len(kx)):
        k_dist[i] = k_dist[i-1] + np.sqrt((kx[i]-kx[i-1])**2 +(ky[i]-ky[i-1])**2 +(kz[i]-kz[i-1])**2)
    
    return k_dist

# Returns E(k) for the i-th Band
def E_i(i):
    return Eigenvalues[0].T[i]

# Returns weight for the i-th Band
def weight_for_band_i(i):
    return weights2[0].T[i]

# Returns array of lenght len(kpts)
# i: (0, 1, 2, 3) --> probalby belongs to the orbital number s,p, d,f
# j: no idea what this is <----------------------------------------------------
# n: n-th energy-band
def llikecharge_for_band_n(i, j, n):
    return (llikecharge[0][:].T[i][j][n])


def plot_bands_with_weight(Number_Bands_plotted):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    max_E = max(E_i(0))
    min_E = min(E_i(0))
    
    for n in range(Number_Bands_plotted):
        #ax1.scatter(k_dist, E_i(n), marker='.', c='b', s=weight_for_band_i(n))
        ax1.scatter(k_dist, E_i(n), marker='o', c='b', s=3*weight_for_band_i(n), lw=0)
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
    plt.savefig("output/"+filename+"_bandstructure_weight.png", dpi=2000)


k_dist = create_k_spacing()
Number_Bands_plotted = Eigenvalues.shape[2] #5
plot_bands_with_weight(Number_Bands_plotted)
#plot_bands_with_weight(1)
    


#llikecharge
#%%


color_scheme = ('green', 'red', 'blue', 'orange', 'black', 'cyan')

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

