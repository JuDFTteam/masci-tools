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
dispersionplot function for plotting KKR bandstructures (i.e. qdos) files
"""

import numpy as np


def load_data(p0='./',
              reload_data=False,
              nosave=False,
              atoms=None,
              ratios=False,
              atoms2=None,
              atoms3=None,
              ef=None,
              verbose=False):
    """load the qdos data"""
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
            with open(p0 + 'potential', encoding='utf-8') as _f:
                ef = float(_f.readlines()[3].split()[1])
        else:
            ef = 0
    alat = float(
        check_output('grep ALATBASIS ' + p0 + 'inputcard', shell=True).decode('utf-8').split('=')[1].split()[0])
    a0 = 2 * np.pi / alat / 0.52918

    d2, d3 = None, None
    if reload_data or 'saved_data_dispersion.npy' not in np.sort(listdir(p0)):
        first = True
        first2 = True
        first3 = True
        if verbose:
            print('reading qdos')
        j = 0
        for i in np.sort(listdir(p0)):
            if 'qdos.' in i[:5] and not isdir(p0 + i):
                iatom = i.replace('qdos.', '').split('.')[0]
                if atoms is None or int(iatom) in atoms:
                    j += 1
                    if verbose:
                        print(j, p0, i)
                    tmp = np.loadtxt(p0 + i)
                    tmp[:, 2:5] = tmp[:, 2:5]
                    if first:
                        d = tmp
                        first = False
                    else:
                        d[:, 5:] += tmp[:, 5:]
                if ratios and (atoms2 is None or int(iatom) in atoms2):
                    j += 1
                    if verbose:
                        print(j, p0, i, 'atoms2=', atoms2)
                    tmp = np.loadtxt(p0 + i)
                    tmp[:, 2:5] = tmp[:, 2:5]
                    if first2:
                        d2 = tmp
                        first2 = False
                    else:
                        d2[:, 5:] += tmp[:, 5:]  # pylint: disable=unsupported-assignment-operation
                if (atoms3 is None or int(iatom) in atoms3) and ratios:
                    j += 1
                    if verbose:
                        print(j, p0, i, 'atoms3=', atoms3)
                    tmp = np.loadtxt(p0 + i)
                    tmp[:, 2:5] = tmp[:, 2:5]
                    if first3:
                        d3 = tmp
                        first3 = False
                    else:
                        d3[:, 5:] += tmp[:, 5:]  # pylint: disable=unsupported-assignment-operation
        if not nosave:
            if verbose:
                print('saving data')
            np.save(p0 + 'saved_data_dispersion', d)
    else:
        if verbose:
            print('loading data')
        d = np.load(p0 + 'saved_data_dispersion.npy')

    return a0, d, d2, d3, ef


def dispersionplot(  # pylint: disable=inconsistent-return-statements
        p0='./',
        data_all=None,  # alternative way, skips loading data with the load_data function
        totonly=True,
        s=20,
        ls_ef=':',
        lw_ef=1,
        units='eV_rel',
        noefline=False,
        color='',
        reload_data=False,
        clrbar=True,
        logscale=True,
        nosave=False,
        atoms=None,
        ratios=False,
        atoms2=None,
        noscale=False,
        newfig=False,
        cmap=None,
        alpha=1.0,
        qcomponent=-2,
        clims=None,
        xscale=1.,
        raster=True,
        atoms3=None,
        alpha_reverse=False,
        return_data=False,
        xshift=0.,
        yshift=0.,
        plotmode='pcolor',
        ptitle=None,
        ef=None,
        as_e_dimension=None,
        scale_alpha_data=False,
        shading='gouraud',
        verbose=False):
    """ plotting routine for qdos files - dispersion (E vs. q) """
    # import dependencies
    from numpy import log, abs, sum, sort, pi, shape, array  # pylint: disable=redefined-builtin
    from matplotlib.pyplot import figure, plot, axvline, scatter, axhline, xlabel, ylabel, title, colorbar, pcolormesh, cm, xlim, ylim, clim
    from os import listdir, getcwd
    from os.path import getctime
    from time import ctime
    from numpy import linspace
    from matplotlib.colors import ListedColormap

    if data_all is None:
        # load data from files
        a0, d, d2, d3, ef = load_data(p0=p0,
                                      reload_data=reload_data,
                                      nosave=nosave,
                                      atoms=atoms,
                                      ratios=ratios,
                                      atoms2=atoms2,
                                      atoms3=atoms3,
                                      ef=ef,
                                      verbose=verbose)
    else:
        # simply unpack the data_all input
        a0, d, d2, d3, ef = data_all

    if verbose:
        print('loaded/unpacked data')

    if cmap is None:
        cmap = cm.viridis

    if newfig:
        if verbose:
            print('open new figure')
        figure()

    if noscale:
        a0 = 1.

    d[:, 2:5] = d[:, 2:5] * a0
    if ratios:
        d2[:, 2:5] = d2[:, 2:5] * a0
        d3[:, 2:5] = d3[:, 2:5] * a0

    # set units and axis labels
    if 'eV' in units:
        d[:, 0] = d[:, 0] * 13.6
        d[:, 5:] = d[:, 5:] / 13.6
        ef = ef * 13.6
    if 'rel' in units:
        d[:, 0] = d[:, 0] - ef
        ef = 0
    if ratios:
        if 'eV' in units:
            d2[:, 5:] = d2[:, 5:] / 13.6
            d3[:, 5:] = d3[:, 5:] / 13.6

    ylab = r'E (Ry)'
    xlab = r'k'
    if units == 'eV':
        ylab = r'E (eV)'
    elif units == 'eV_rel':
        ylab = r'E-E_F (eV)'
    elif units == 'Ry_rel':
        ylab = r'E-E_F (Ry)'

    # plot dos
    if totonly:
        data = abs(sum(d[:, 5:], axis=1))
    else:
        data = abs(d[:, 5:])
    if logscale:
        data = log(data)
    x, y = xscale * sum(d[:, 2:5], axis=1), d[:, 0]
    if qcomponent == -2:
        el = len(set(d[:, 0]))  # pylint disable=unnecessary-comprehension
        if el == 1 and as_e_dimension is not None:
            y = d[:, 2 + as_e_dimension]
            el = len(set(y))
            ylab = r'k (1/Ang.)'
        x = array([list(range(len(d) // el)) for j in range(el)])
    elif qcomponent != -1:
        x = xscale * d[:, 2:5][:, qcomponent]

    if xshift != 0:
        x += xshift

    if ratios:
        data = abs(sum(d[:, 5:], axis=1))
        data2 = abs(sum(d2[:, 5:], axis=1))
        data = (data - data2) / (data + data2)

    if yshift != 0:
        y += yshift

    if scale_alpha_data:
        dtmp = data.copy()
        dtmp = linspace(dtmp.min(), dtmp.max(), 1000)
        colors = cmap(dtmp)
        dtmp = dtmp - dtmp.min()
        dtmp = dtmp / dtmp.max()
        colors[:, -1] = alpha * (dtmp)
        cmap = ListedColormap(colors)
        alpha = 1.
    if ratios and atoms3 is not None:
        colors = cmap(data / data.max())
        colors[:, -1] = abs(sum(d3[:, 5:], axis=1)) / abs(sum(d3[:, 5:], axis=1)).max()
        if alpha_reverse:
            colors[:, -1] = 1 - colors[:, -1]
    if ratios:
        if plotmode == 'scatter':
            scatter(x, y, s=s, lw=0, c=colors, cmap=cmap, rasterized=raster)
        else:
            lx = len(set(x.reshape(-1)))
            ly = len(set(y.reshape(-1)))
            pcolormesh(
                x.reshape(ly, lx),
                y.reshape(ly, lx),
                data.reshape(ly, lx),
                cmap=cmap,
                rasterized=raster,
                edgecolor='face',
                linewidths=0.0001,
                shading=shading,
            )
    else:
        if plotmode == 'scatter':
            scatter(x, y, c=data, s=s, lw=0, cmap=cmap, alpha=alpha, rasterized=raster)
        else:
            lx = len(set(x.reshape(-1)))
            ly = len(set(y.reshape(-1)))
            pcolormesh(
                x.reshape(ly, lx),
                y.reshape(ly, lx),
                data.reshape(ly, lx),
                cmap=cmap,
                rasterized=raster,
                edgecolor='face',
                linewidths=0.0001,
                shading=shading,
            )
    if clims is not None:
        clim(clims[0], clims[1])
    if clrbar:
        colorbar()

    # plot fermi level
    if not noefline:
        if color == '':
            axhline(ef, ls=ls_ef, lw=lw_ef, color='grey')
        else:
            axhline(ef, color=color, ls=ls_ef, lw=lw_ef)

    # set axis labels
    xlabel(xlab)
    ylabel(ylab)

    # set x and y limits
    xlim(x.min(), x.max())
    ylim(y.min(), y.max())

    # print path to title
    if totonly and ptitle is None:
        title(getcwd())
    else:
        title(ptitle)

    if return_data:
        data = abs(sum(d[:, 5:], axis=1))

        if ratios:
            data2 = abs(sum(d2[:, 5:], axis=1))
            data3 = abs(sum(d3[:, 5:], axis=1))
            return x, y, data, data2, data3

        return x, y, data
