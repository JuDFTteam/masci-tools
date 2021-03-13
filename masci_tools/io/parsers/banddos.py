#!/usr/bin/env python3
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
Parser for the FLEUR (MaX_R5) `banddos.hdf`  file
"""

import numpy as np
import h5py

def hdfList(obj, sep="\t"):
    """
    Iterate through groups in a HDF5 file and prints...
    ...the groups and datasets names and datasets attributes
    """
    if type(obj) in [h5py._hl.group.Group, h5py._hl.files.File]:
        for key in obj.keys():
            print(sep, '-', key, ':', obj[key])
            hdfList(obj[key], sep=sep+'\t')
    elif type(obj) == h5py._hl.dataset.Dataset:
        for key in obj.attrs.keys():
            print(sep+'\t', '-', key, ':', obj.attrs[key])


def h5dump(path, group='/'):
    """
    group: you can give a specific group, defaults to the root group
    """
    with h5py.File(path, 'r') as f:
        hdfList(f[group])



def kpath(kcoord,reciprocalCell):
    """
    Construct k-point path from the k point coordinate array 
    """
    nkpt = kcoord.shape[0]
    kpts = np.zeros(nkpt)
    kpts[0] = np.linalg.norm(reciprocalCell.dot(kcoord[0]))
    for i in range(1, nkpt):
        kpts[i] = kpts[i - 1] + \
            np.linalg.norm(reciprocalCell.dot(
                kcoord[i]) - reciprocalCell.dot(kcoord[i - 1]))
    return kpts


def writeBand(inpFile, outFile1, outFile2):
    eV = 27.211386
    f = h5py.File(inpFile, 'r')
    atomicGroup = np.array(f.get('atoms/equivAtomsGroup'))
    kpts = kpath(np.array(f.get('Local/BS/kpts')),
                 np.array(f.get('cell/reciprocalCell')))
    eigVal = np.array(f.get('Local/BS/eigenvalues'))
    INT = np.array(f.get('Local/BS/INT'))

    MT = []
    for i in np.array(f.get('atoms/equivAtomsGroup')):
        tmp = []
        for j in ['s', 'p', 'd', 'f']:
            tmp.append(np.array(f.get(f'Local/BS/MT:{i}{j}')))
        MT.append(np.array(tmp).sum(axis=0))
    MT = np.array(MT)

    (jspin, nband, eigen), nkpt = eigVal.shape, len(kpts)
    for s in range(jspin):
        if s == 0:
            with open(outFile1, 'w') as f1:
                f1.write('#spin,k,E(ev),INT,{}\n'.format(
                    ','.join(map(str, [f'MT:{i}' for i in atomicGroup]))))
                for i in range(nband):
                    for j in range(nkpt):
                        f1.write('{},{:.5f},{:.5f},{:.5f},{}\n'.format(
                            s, kpts[j], eV*eigVal[s, j, i], INT[s, j, i], ','.join(map(str, ['{:.5f}'.format(MT[k, s, j, i]) for k in range(len(atomicGroup))]))))
        else:
            with open(outFile2, 'w') as f2:
                f2.write('#spin,k,E(ev),INT,{}\n'.format(
                    ','.join(map(str, [f'MT:{i}' for i in atomicGroup]))))
                for i in range(nband):
                    for j in range(nkpt):
                        f2.write('{},{:.5f},{:.5f},{:.5f},{}\n'.format(
                            s, kpts[j], eV*eigVal[s, j, i], INT[s, j, i], ','.join(map(str, ['{:.5f}'.format(MT[k, s, j, i]) for k in range(len(atomicGroup))]))))

    with open('bandinfo.txt', 'w') as f3:
        specialPointLabels = np.array(
            f.get('kpts/specialPointLabels')).astype(str)
        specialPointIndices = np.array(f.get('kpts/specialPointIndices'))
        for i, val in enumerate(specialPointIndices):
            f3.write(f'{val},{kpts[val-1]:.5f},{specialPointLabels[i]}\n')


if __name__ == '__main__':
    pass
    # writeBand('banddos.hdf','band1.csv','band2.csv')