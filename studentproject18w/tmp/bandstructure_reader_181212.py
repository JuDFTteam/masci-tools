#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 21:17:10 2018

@author: christianpartmann
"""

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import pyplot as plt
import h5py
import time
import os

bohr_constant = 0.52
times = []
times += [time.time()]

# filename = 'banddos_4x4.hdf'
filename = 'banddos.hdf'
# filename = 'banddos_Co.hdf'

filepath = ['..', 'data', 'input', filename]
filepath = os.path.join(*filepath)

f = h5py.File(filepath, 'r')

evs = np.array(f["/eigenvalues/eigenvalues"])
llc =  np.array(f["/eigenvalues/lLikeCharge"])
#unfold_weight = np.array(f["/bandUnfolding/weights"])

special_points = f["/kpts/specialPointIndices"]
special_points_label = f["/kpts/specialPointLabels"]
band_unfolding = f["/general"].attrs['bandUnfolding'][0]
fermi_energy = f["/general"].attrs['lastFermiEnergy'][0]
atom_group = f["/atoms/equivAtomsGroup"]

(NUM_SPIN, NUM_K, NUM_E, NUM_GROUPS, NUM_CHAR) = llc.shape

# ugly, but doesn't matter for total runtime
# check if rec_cell or rec_cell.T is correct!!!!!!!!!!!
#
# JW: this is identical, no change. 'k_distances' is now 'k'
def k_phys(f):
    kpts_int = f["/kpts/coordinates"]
    rec_cell = f["/cell/reciprocalCell"][:]
    phys_k = np.dot(kpts_int, rec_cell)

    kx = phys_k[:].T[0]
    ky = phys_k[:].T[1]
    kz = phys_k[:].T[2]
    k_dist = np.zeros(len(kx))
    k_dist[0] = 0
    for i in range(1, len(kx)):
        k_dist[i] = k_dist[i-1] + np.sqrt((kx[i]-kx[i-1])**2 +(ky[i]-ky[i-1])**2 +(kz[i]-kz[i-1])**2)
    return k_dist

def create_spin_filter(which_spin, NUM_SPIN = NUM_SPIN):
    SPIN_FILTER = np.zeros(NUM_SPIN).astype(bool)
    SPIN_FILTER[which_spin] = True
    return SPIN_FILTER

def create_character_filter(which_characters):
    CHARACTER_FILTER = np.zeros(4).astype(bool)
    CHARACTER_FILTER[which_characters] = True
    return CHARACTER_FILTER

def create_group_filter(which_groups = range(NUM_GROUPS)):
    GROUP_FILTER = np.zeros(NUM_GROUPS).astype(bool)
    GROUP_FILTER[which_groups] = True
    return GROUP_FILTER

def create_band_filter(which_bands = range(NUM_E)):
    BAND_FILTER = np.zeros(NUM_E).astype(bool)
    BAND_FILTER[which_bands] = True
    return BAND_FILTER

k = k_phys(f)


times += [time.time()]

# JW: this is identical, now change
def get_k_special_pt(ind_special_points, k):
    k_special_pt = np.zeros(len(special_points[:]))
    for i in range(len(special_points[:])):
        k_special_pt[i] = k[special_points[i]-1]
    return k_special_pt

k_special_pt = get_k_special_pt(special_points, k)

# this is the expensive funkction!
# reads all data, selects relevant parts and reduces along groups and characters
# generic form: pass lists of booleans...
def get_data(f, llc, SPIN_FILTER, CHARACTER_FILTER, GROUP_FILTER, BAND_FILTER, UNFOLD_WEIGHT=band_unfolding):
    ATOMS_PER_GROUP = np.zeros(NUM_GROUPS)
    for i in range(NUM_GROUPS):
        ATOMS_PER_GROUP[i] = np.count_nonzero(np.array(atom_group)==i)
    
    # filter arrays in bands and spin:
    llc = llc[SPIN_FILTER, :, :, :, :]
    llc = llc[:, :, BAND_FILTER, :, :]
    # reduce the arrays in Character, Spin, Group
    #llc_red = llc[SPIN_FILTER, :, :, :, :]
    llc_red = llc[:, :, :, GROUP_FILTER, :]
    llc_red = llc_red[:, :, :, :, CHARACTER_FILTER]
    #llc_red = llc_red[:, :, BAND_FILTER, :, :]
    ATOMS_PER_GROUP_red = ATOMS_PER_GROUP[GROUP_FILTER]
    
    # compute normalized weights with tensor product
    llc_redG = np.tensordot(llc_red, ATOMS_PER_GROUP_red, axes=([3],[0]))
    llc_redGC = np.sum(llc_redG, axis = 3)
    llc_norm_temp = np.tensordot(llc, ATOMS_PER_GROUP, axes=([3],[0]))
    llc_norm = np.sum(llc_norm_temp, axis = 3)
    llc_normalized = llc_redGC/llc_norm
    
    # consider unfolding weight
    if(UNFOLD_WEIGHT == True):
        unfold_weight = np.array(f["/bandUnfolding/weights"])
        unfold_weight = unfold_weight[SPIN_FILTER, :, :]
        unfold_weight = unfold_weight[:, :, BAND_FILTER]
        llc_normalized = llc_normalized * unfold_weight
    
    return llc_normalized

def reshape_data(f, llc, evs, k, spin, CHARACTER_FILTER, GROUP_FILTER, BAND_FILTER, UNFOLD_WEIGHT=band_unfolding):
    SPIN_FILTER = create_spin_filter(spin)
    total_weight = get_data(f, llc, SPIN_FILTER, CHARACTER_FILTER, GROUP_FILTER, BAND_FILTER, UNFOLD_WEIGHT)
    # only select the requested spin and bands
    evs = evs[spin, :, BAND_FILTER]

    # to speed up scatter plot, unfold data in one dimension
    (Nk, Ne) = evs.T.shape

    evs_resh = np.reshape(evs, Nk*Ne)
    weight_resh = np.reshape(total_weight[0].T, Nk*Ne)
    k_resh = np.tile(k, Ne)
    return (k_resh, evs_resh, weight_resh)


times += [time.time()]

spin = 0
SPIN_FILTER = create_spin_filter(spin)
CHARACTER_FILTER = create_character_filter([0,1,2,3])
GROUP_FILTER = create_group_filter()
UNFOLD_WEIGHT = band_unfolding
BAND_FILTER = create_band_filter()

# JW: llc, evs come frome file, no change.
# JW: k is k_distances, no change.
# JW: characters, groups, spin now replaced with these masks (all boolean lists)
#     so instead of all_characters = [0,1,2,3] for spdf before, we now have [True,True,True,True]
#     for group_filter we had all_groups = eg [0,1,2,3,4] before, now [True,...,True]
#     for BAND_FILTER we had all_bands = eg [0,...,48] before, now [True,...,True]
#      UNFOLD_WEIGHT = bandUnfolding = boolean as before from file, no change
(k_r, E_r, W_r) = reshape_data(f, llc, evs, k, spin, CHARACTER_FILTER, GROUP_FILTER, BAND_FILTER, UNFOLD_WEIGHT)
times += [time.time()]

fig = plt.figure()
ax1 = fig.add_subplot(111)

#just plot points with minimal size of t
speed_up = True
if(speed_up == True):
    t = 1e-4
    k_r = k_r[W_r>t]
    E_r = E_r[W_r>t]
    W_r = W_r[W_r>t]

ax1.scatter(k_r, E_r, marker='o', c='b', s = 2 * W_r, lw=0)


label = []
for i in range(len(special_points_label)):
    label += str(special_points_label[i])[2]
plt.xticks(k_special_pt, label)
plt.xlabel("k")
plt.ylabel("E(k)")


# plt.savefig("testfigure.png", dpi=250)
plt.show()

times += [time.time()]
times = np.array(times)-times[0]
print(times)
#[3.08742310e-02]



#%%
"""

aaa = time.time()
kk = k_phys(f)
bbb = time.time()
kpts_int = f["/kpts/coordinates"]
rec_cell = f["/cell/reciprocalCell"][:]
phys_k = np.dot(kpts_int, rec_cell)

shiftp = phys_k[1:, :]
shiftm = phys_k[:-1, :]
k_dist = np.append(np.array([0]), np.sum((phys_k[1:, :]-phys_k[:-1, :])**2, axis = 1))
#for i in range(1, len(k_dist)):
#    k_dist[i] = k_dist[i-1] + k_dist[i]

ccc = time.time()

print(bbb-aaa)
print(ccc-bbb)
"""

"""
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
for n in range(NUM_E):
        ax2.scatter(k, evs[0, :, n], marker='o', c='b', s = 2 * llc_redGC[0, :, n], lw=0)
"""  

"""
SPIN_FILTER = np.array([True])
CHARACTER_FILTER = np.array([True, False, False, False])
GROUP_FILTER = np.ones(NUM_GROUPS).astype(bool) #np.array([])
GROUP_FILTER[1] = False
"""