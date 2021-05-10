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


def dosplot(p0='./',
            totonly=True,
            color='',
            label='',
            marker='',
            lw=2,
            ms=5,
            ls='-',
            ls_ef=':',
            lw_ef=1,
            units='Ry',
            noefline=False,
            interpol=False,
            allatoms=False,
            onespin=False,
            atoms=[],
            lmdos=False,
            lm=[],
            nofig=False,
            scale=1.0,
            shift=0,
            normalized=False,
            xyswitch=False,
            efcolor='',
            return_data=False,
            xscale=1.,
            xshift=0.0,
            yshift=0.0,
            filled=False,
            spins=2):
    """ plotting routine for dos files """
    # import dependencies
    import numpy as np
    import matplotlib.pyplot as plt
    from os import listdir
    from os.path import isdir

    plt.ion()

    # deal with input of file handle instead of path (see plot_kkr of aiida_kkr)
    if not isinstance(p0, str):
        pathname_with_file = p0.name
        p0 = pathname_with_file.replace('/dos.atom1', '')

    # read in data
    if p0[-1] != '/':
        p0 += '/'
    #if 'rel' in units: ef = float(open(p0+'potential').readlines()[3].split()[1])
    ef = float(open(p0 + 'potential').readlines()[3].split()[1])
    first = True
    for i in np.sort(listdir(p0)):
        if (((i[:8] == 'dos.atom' and 'interpol' not in i) and not interpol) or
            (interpol and i[:17] == 'dos.interpol.atom')) or ('out_ldos.atom' in i and 'out_lmdos.atom' not in i and
                                                              not interpol) or ('out_ldos.interpol.atom' in i and
                                                                                'out_lmdos.interpol.atom' and
                                                                                interpol) and not isdir(p0 + i):
            if lmdos:
                i = i.replace('out_ldos.', 'out_lmdos.')
            if not onespin or 'spin' + str(spins) not in i:
                iatom = i.replace('dos.', '').replace('interpol.',
                                                      '').replace('atom',
                                                                  '').replace('out_l',
                                                                              '').replace('=',
                                                                                          '').replace('m',
                                                                                                      '').split('_')[0]
                if atoms == [] or int(iatom) in atoms:
                    tmp = np.loadtxt(p0 + i)
                    print(p0 + i)

                    # set units
                    if 'rel' in units:
                        tmp[:, 0] = tmp[:, 0] - ef
                    if 'eV' in units:
                        tmp[:, 0] = tmp[:, 0] * 13.6
                        tmp[:, 1:] = tmp[:, 1:] / 13.6

                    tmp[:, 0] = tmp[:, 0] * xscale + xshift
                    tmp[:, 1] = tmp[:, 1] + yshift

                    if allatoms:
                        sgn = 1
                        if 'spin2' in i:
                            sgn = -1
                        # plot dos
                        if totonly:
                            if color == '':
                                if first:
                                    if not nofig:
                                        plt.figure()
                                plt.plot(tmp[:, 0], sgn * tmp[:, 1], marker + ls, label=label + str(i), lw=lw, ms=ms)
                            else:
                                if not nofig:
                                    plt.figure()
                                if filled:
                                    plt.fill_between(tmp[:, 0], sgn * tmp[:, 1], color=color, label=label)
                                else:
                                    plt.plot(tmp[:, 0],
                                             sgn * tmp[:, 1],
                                             marker + ls,
                                             color=color,
                                             label=label,
                                             lw=lw,
                                             ms=ms)
                        else:
                            if not nofig and sgn == 1:
                                plt.figure()
                            if color == '':
                                if lm == []:
                                    if filled:
                                        plt.fill_between(tmp[:, 0], sgn * tmp[:, 1:])
                                    else:
                                        plt.plot(tmp[:, 0], sgn * tmp[:, 1:], marker + ls, lw=lw, ms=ms)
                                else:
                                    for ilm in lm:
                                        lmname = label + ' '
                                        if ilm == 1:
                                            lmname += 's'
                                        if ilm == 2:
                                            lmname += 'p_x'
                                        if ilm == 3:
                                            lmname += 'p_y'
                                        if ilm == 4:
                                            lmname += 'p_z'
                                        if ilm == 5:
                                            lmname += 'd_{x^2-y^2}'
                                        if ilm == 6:
                                            lmname += 'd_{xz}'
                                        if ilm == 7:
                                            lmname += 'd_{z^2}'
                                        if ilm == 8:
                                            lmname += 'd_{yz}'
                                        if ilm == 9:
                                            lmname += 'd_{xy}'
                                        if ilm == 10:
                                            lmname += 'f_{-3}'
                                        if ilm == 11:
                                            lmname += 'f_{-2}'
                                        if ilm == 12:
                                            lmname += 'f_{-1}'
                                        if ilm == 13:
                                            lmname += 'f_{0}'
                                        if ilm == 14:
                                            lmname += 'f_{1}'
                                        if ilm == 15:
                                            lmname += 'f_{2}'
                                        if ilm == 16:
                                            lmname += 'f_{3}'
                                        plt.plot(tmp[:, 0],
                                                 sgn * tmp[:, 1 + ilm],
                                                 marker + ls,
                                                 lw=lw,
                                                 ms=ms,
                                                 label=lmname)
                            else:
                                if lm == []:
                                    if filled:
                                        plt.fill_between(tmp[:, 0], sgn * tmp[:, 1:], color=color)
                                    else:
                                        plt.plot(tmp[:, 0], sgn * tmp[:, 1:], marker + ls, color=color, lw=lw, ms=ms)
                                else:
                                    for ilm in lm:
                                        lmname = label + ' '
                                        if ilm == 1:
                                            lmname += 's'
                                        if ilm == 2:
                                            lmname += 'p_x'
                                        if ilm == 3:
                                            lmname += 'p_y'
                                        if ilm == 4:
                                            lmname += 'p_z'
                                        if ilm == 5:
                                            lmname += 'd_{x^2-y^2}'
                                        if ilm == 6:
                                            lmname += 'd_{xz}'
                                        if ilm == 7:
                                            lmname += 'd_{z^2}'
                                        if ilm == 8:
                                            lmname += 'd_{yz}'
                                        if ilm == 9:
                                            lmname += 'd_{xy}'
                                        if ilm == 10:
                                            lmname += 'f_{-3}'
                                        if ilm == 11:
                                            lmname += 'f_{-2}'
                                        if ilm == 12:
                                            lmname += 'f_{-1}'
                                        if ilm == 13:
                                            lmname += 'f_{0}'
                                        if ilm == 14:
                                            lmname += 'f_{1}'
                                        if ilm == 15:
                                            lmname += 'f_{2}'
                                        if ilm == 16:
                                            lmname += 'f_{3}'
                                        plt.plot(tmp[:, 0],
                                                 sgn * tmp[:, 1 + ilm],
                                                 marker + ls,
                                                 lw=lw,
                                                 ms=ms,
                                                 label=lmname,
                                                 color=color)
                            plt.title(label + ' ' + i)

                    #sum data
                    if first:
                        d = tmp
                        d[:, 1:] = d[:, 1:] * scale
                        first = False
                    else:
                        d[:, 1:] += tmp[:, 1:] * scale

    # set units and axis labels
    if 'eV' in units:
        ef = ef * 13.6
    if 'rel' in units:
        ef = 0

    #if lmdos:
    #   if lm<>[]:
    #      d = d[:,[0,1]+list(np.array(lm)+1)]
    #   d[:,1] = np.sum(d[:,2:], axis=1)
    if lm != []:
        d = d[:, [0, 1] + list(np.array(lm) + 1)]
    d[:, 1] = np.sum(d[:, 2:], axis=1)

    if normalized:
        d[:, 1:] = d[:, 1:] / (d[:, 1:]).max()

    xlab = r'E (Ry)'
    ylab = r'DOS (states/Ry)'
    if units == 'eV':
        xlab = r'E (eV)'
        ylab = r'DOS (states/eV)'
    elif units == 'eV_rel':
        xlab = r'E-E_F (eV)'
        ylab = r'DOS (states/eV)'
    elif units == 'Ry_rel':
        xlab = r'E-E_F (Ry)'
        ylab = r'DOS (states/Ry)'

    # plot dos
    if not allatoms:
        if totonly:
            if color == '':
                if xyswitch:
                    plt.plot(d[:, 1], d[:, 0] + shift, marker + ls, label=label, lw=lw, ms=ms)
                else:
                    plt.plot(d[:, 0] + shift, d[:, 1], marker + ls, label=label, lw=lw, ms=ms)
            else:
                if xyswitch:
                    if filled:
                        plt.fill_between(d[:, 1], d[:, 0] + shift, color=color, label=label)
                    else:
                        plt.plot(d[:, 1], d[:, 0] + shift, marker + ls, color=color, label=label, lw=lw, ms=ms)
                else:
                    if filled:
                        plt.fill_between(d[:, 0] + shift, d[:, 1], color=color, label=label)
                    else:
                        plt.plot(d[:, 0] + shift, d[:, 1], marker + ls, color=color, label=label, lw=lw, ms=ms)

        else:
            if color == '':
                if xyswitch:
                    plt.plot(d[:, 1:], d[:, 0] + shift, marker + ls, lw=lw, ms=ms)
                else:
                    plt.plot(d[:, 0] + shift, d[:, 1:], marker + ls, lw=lw, ms=ms)
            else:
                if xyswitch:
                    if filled:
                        plt.fill_between(d[:, 1], d[:, 0] + shift, color=color)
                    else:
                        plt.plot(d[:, 1:], d[:, 0] + shift, marker + ls, color=color, lw=lw, ms=ms)
                else:
                    if filled:
                        plt.fill_between(d[:, 0] + shift, d[:, 1], color=color)
                    else:
                        plt.plot(d[:, 0] + shift, d[:, 1:], marker + ls, color=color, lw=lw, ms=ms)
            plt.title(label)

    # plot fermi level
    if not noefline:
        if color != '' and efcolor == '':
            efcolor = color
        if efcolor == '':
            if xyswitch:
                plt.axhline(ef, ls=ls_ef, lw=lw_ef, color='grey')
            else:
                plt.axvline(ef, ls=ls_ef, lw=lw_ef, color='grey')
        else:
            if xyswitch:
                plt.axhline(ef, color=efcolor, ls=ls_ef, lw=lw_ef)
            else:
                plt.axvline(ef, color=efcolor, ls=ls_ef, lw=lw_ef)

    # set axis labels
    if xyswitch:
        plt.ylabel(xlab)
        plt.xlabel(ylab)
    else:
        plt.xlabel(xlab)
        plt.ylabel(ylab)

    if return_data:
        return d, ef
