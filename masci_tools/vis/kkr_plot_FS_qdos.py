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
from matplotlib import cm


def FSqdos2D(p0='./',
             totonly=True,
             s=20,
             ls_ef=':',
             lw_ef=1,
             color='',
             reload_data=False,
             clrbar=True,
             atoms=[],
             ax=None,
             nosave=False,
             noalat=False,
             cmap=cm.jet,
             noplot=False,
             return_data=False,
             pclrmesh=False,
             logscale=True,
             ef=None):
    """ plotting routine for dos files """
    # import dependencies
    import numpy as np
    import matplotlib.pyplot as plt
    from os import listdir
    from os.path import isdir
    from subprocess import check_output

    # deal with input of file handle instead of path (see plot_kkr of aiida_kkr)
    if not isinstance(p0, str):
        pathname_with_file = p0.name
        p0 = pathname_with_file.replace('/qdos.01.1.dat', '')  #dos.atom1

    # read in data
    if p0[-1] != '/':
        p0 += '/'

    # read EF if not given as input
    if ef is None:
        if 'potential' in listdir(p0):
            ef = float(open(p0 + 'potential').readlines()[3].split()[1])
        else:
            ef = 0

    if noalat:
        a0 = 1.
        alat = 1.
    else:
        alat = float(
            check_output('grep ALATBASIS ' + p0 + 'inputcard', shell=True).decode('utf-8').split('=')[1].split()[0])
        a0 = 2 * np.pi / alat / 0.52918

    if reload_data or 'saved_data_qdos.npy' not in np.sort(listdir(p0)):
        first = True
        print('reading qdos')
        j = 0
        for i in np.sort(listdir(p0)):
            if 'qdos.' in i[:6] and not isdir(p0 + i):
                j += 1
                iatom = int(i.replace('qdos.', '').split('.')[0])
                if atoms == [] or iatom in atoms:
                    tmp = np.loadtxt(p0 + i)
                    tmp[:, 2:5] = tmp[:, 2:5] * a0
                    print(i, iatom)
                    if first:
                        d = tmp
                        first = False
                    else:
                        d[:, 5:] += tmp[:, 5:]
        if not nosave:
            np.save(p0 + 'saved_data_qdos', d)
    else:
        d = np.load(p0 + 'saved_data_qdos.npy')

    xlab = r'kx'
    ylab = r'ky'
    if a0 != 1.:
        xlab = r'$k_x (\AA^{-1})$'
        ylab = r'$k_y (\AA^{-1})$'

    # plot dos
    data = np.abs(np.sum(d[:, 5:], axis=1))
    if logscale:
        data = np.log(data)
    x, y = d[:, 2], d[:, 3]

    if not noplot:
        if ax is None:
            if pclrmesh:
                lx = len(set(x))
                ly = len(set(y))
                x = np.linspace(x.min(), x.max(), lx)
                y = np.linspace(y.min(), y.max(), ly)
                plt.pcolormesh(x, y, data.reshape(lx, ly).T, cmap=cmap)
            else:
                plt.scatter(x, y, c=data, s=s, lw=0, cmap=cmap)
            if clrbar:
                plt.colorbar()
        else:
            ax.scatter(x, y, c=data, lw=0, cmap=cmap)

        # set axis labels
        if ax is None:
            plt.xlabel(xlab)
            plt.ylabel(ylab)
            plt.axis('equal')

    if return_data:
        return x, y, data
