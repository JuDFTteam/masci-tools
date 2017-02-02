#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
In this module are plot routines collected to create default plots out of certain
ouput nodes from certain workflows with matplot lib. 

Comment: Do not use any aiida methods, otherwise the methods in here can become 
tricky to use inside a virtual environment. Make the user extract thing out of 
aiida objects before hand or write something on top. Since usually parameter nodes,
or files are ploted, parse a dict or filepath.
"""
# TODO but allow to optional parse information for saving and title,
#  (that user can put pks or structure formulas in there)

__copyright__ = (u"Copyright (c), 2016, Forschungszentrum Jülich GmbH, "
                 "IAS-1/PGI-1, Germany. All rights reserved.")
__license__ = "MIT license, see LICENSE.txt file"
__version__ = "0.27"
__contributors__ = "Jens Broeder"

import re
import os
import numpy as np
import matplotlib.pyplot as pp

############
# GLOBAL MODULE VARIABLES setting properties
# maintain this and set method for them
# convention they are the property ending with '_g'

# figure properties
title_fontsize_g = 16
figsize_g = (8, 6)
dpi_g = 80
facecolor_g = 'w'
edgecolor_g = 'k'

# axis properties
alpha_g = 1
axis_linewidth_g = 1.5
# plot properties
linewidth_g = 2.0
markersize_g = 4.0

# x, y label
labelfonstsize_g = 15

# ticks
ticklabelsize_g = 14
tick_params_g = {'size' : 4.0, 'width' : 1.0, 'labelsize' : ticklabelsize_g, 'length' : 5}

# legend properties

# save all plots?
save_plots_g = False# True
save_format_g = 'pdf'
tightlayout_g = False
##############


def set_plot_defaults(title_fontsize = 16,
                      linewidth = 2.0,
                      markersize = 4.0,
                      labelfonstsize = 15,
                      ticklabelsize = 14,
                      tick_params = {'size' : 4.0, 'width' : 1.0,
                                     'labelsize' : ticklabelsize_g,
                                     'length' : 5},
                      save_plots = False, #True,
                      save_format = 'pdf'):
    """
    Try to use this to set some global default values.
    
    Set some evironment variable with or global variables.
    """
    global linewidth_g, markersize_g, labelfonstsize_g
    global ticklabelsize_g, tick_params_g, save_plots_g, save_format_g

    # plot properties
    linewidth_g = linewidth
    markersize_g = markersize
    # x, y label
    labelfonstsize_g = labelfonstsize
    # ticks
    ticklabelsize_g = ticklabelsize
    tick_params_g.update(tick_params)

    # save all plots?
    save_plots_g = save_plots
    save_format_g = save_format
    #print markersize_g



###########################
## general plot routines ##
###########################


def single_scatterplot(ydata, xdata, xlabel, ylabel, title, plotlabel ='scatterplot', linetyp='o-', limits=[None, None], saveas ='scatterplot', color = 'k'):
    """
    Create a standard scatter plot (this should be flexible enough) to do all the
    basic plots.
    """

    fig = pp.figure(num=None, figsize=figsize_g, dpi=dpi_g, facecolor=facecolor_g, edgecolor=edgecolor_g)
    ax = fig.add_subplot(111)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(axis_linewidth_g)
    ax.set_title(title, fontsize=title_fontsize_g, alpha=alpha_g, ha='center')
    ax.set_xlabel(xlabel, fontsize=labelfonstsize_g)
    ax.set_ylabel(ylabel, fontsize=labelfonstsize_g)
    ax.yaxis.set_tick_params(size = tick_params_g.get('size', 4.0),
                             width = tick_params_g.get('width', 1.0),
                             labelsize = tick_params_g.get('labelsize', 14),
                             length = tick_params_g.get('length', 5))
    ax.xaxis.set_tick_params(size = tick_params_g.get('size', 4.0),
                             width = tick_params_g.get('width', 1.0),
                             labelsize = tick_params_g.get('labelsize', 14),
                             length = tick_params_g.get('length', 5))
    ax.yaxis.get_major_formatter().set_powerlimits((0, 3))
    ax.yaxis.get_major_formatter().set_useOffset(False)
    p1 = pp.plot(xdata, ydata, linetyp, label = plotlabel, color = color,
                 linewidth = linewidth_g, markersize = markersize_g)
    if limits:
        if limits[0]:
            xmin = limits[0][0]
            xmax = limits[0][1]
            pp.xlim(xmin, xmax)
        if limits[1]:
            ymin = limits[1][0]
            ymax = limits[1][1]
            pp.ylim(ymin, ymax)

    if save_plots_g:
        savefilename = '{}.{}'.format(saveas, save_format_g)
        print 'save plot to: {}'.format(savefilename)
        pp.savefig(savefilename, format=save_format_g, transparent=True)
    else:
        pp.show()


def multiple_scatterplots(ydata, xdata, xlabel, ylabel, title, plot_labels, linetyp='o-', legend=True, saveas ='mscatterplot', limits=[None, None]):
    """
    Create a standard scatter plot (this should be flexible enough) to do all the
    basic plots.
    """
    nplots = len(ydata)
    if not (nplots==len(xdata)): # todo check dimention not len, without moving to special datatype.
        print 'ydata and xdata must have the same dimension'
        return

    # TODO allow plotlabels to have different dimension
    pl =[]

    fig = pp.figure(num=None, figsize=figsize_g, dpi=dpi_g, facecolor=facecolor_g, edgecolor=edgecolor_g)
    ax = fig.add_subplot(111)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(axis_linewidth_g)
    ax.set_title(title, fontsize=title_fontsize_g, alpha=alpha_g, ha='center')
    ax.set_xlabel(xlabel, fontsize=labelfonstsize_g)
    ax.set_ylabel(ylabel, fontsize=labelfonstsize_g)
    ax.yaxis.set_tick_params(size = tick_params_g.get('size', 4.0),
                             width = tick_params_g.get('width', 1.0),
                             labelsize = tick_params_g.get('labelsize', 14),
                             length = tick_params_g.get('length', 5))
    ax.xaxis.set_tick_params(size = tick_params_g.get('size', 4.0),
                             width = tick_params_g.get('width', 1.0),
                             labelsize = tick_params_g.get('labelsize', 14),
                             length = tick_params_g.get('length', 5))
    ax.yaxis.get_major_formatter().set_powerlimits((0, 3))
    ax.yaxis.get_major_formatter().set_useOffset(False)

    for i, data in enumerate(ydata):
        p1 = pp.plot(xdata[i], data, linetyp, label = plot_labels[i],
                     linewidth = linewidth_g, markersize = markersize_g)

    if limits:
        if limits[0]:
            xmin = limits[0][0]
            xmax = limits[0][1]
            pp.xlim(xmin, xmax)
        if limits[1]:
            ymin = limits[1][0]
            ymax = limits[1][1]
            pp.ylim(ymin, ymax)
    #TODO legend
    if legend:
        pass
    if save_plots_g:
        savefilename = '{}.{}'.format(saveas, save_format_g)
        print 'save plot to: {}'.format(savefilename)
        pp.savefig(savefilename, format=save_format_g, transparent=True)
    else:
        pp.show()


def default_histogram():
    """
    Create a standard looking histogram
    """
    pass


def multiaxis_scatterplot():
    """
    Create a scatter plot with multiple axes
    """
    pass

def surface_plot():
    """
    Create a standard 3D surface plot
    """
    pass

###########################
## special plot routines ##
###########################

def plot_convergence_results(distance, total_energy, iteration, saveas1='t_energy_convergence', saveas2='distance_convergence'):
    """
    Plot the total energy versus the scf iteration
    and plot the distance of the density versus iterations.
    """
    xlabel = r'Iteration'
    ylabel1 = r'Total energy [eV]'
    ylabel2 = r'Distance [me/bohr^3]'
    title1 = r'Total energy over scf-Iterations'
    title2 = r'Distance over scf-Iterations'

    single_scatterplot(total_energy, iteration, xlabel, ylabel1, title1, plotlabel='total energy', saveas=saveas1)
    single_scatterplot(distance, iteration, xlabel, ylabel2, title2, plotlabel='distance', saveas=saveas2)



def plot_lattice_constant(Total_energy, scaling, fit_y, relative = True, ref_const = None, multi = False, plotlables = [r'simulation data', r'fit results'], title = r'Total Energy vs lattice constant', saveas = 'Lattice_constant'):
    """
    Plot a lattice constant versus Total energy
    Plot also the fit.
    On the x axis is the scaling, it
    
    params: Total_energy, list with floats, or list of lists of floats
    params: scaling, list with floats, or list of lists of floats
    params: fit_y, list with floats, evaluated fit, or list of lists of floats
    params: relative = True, (optional), scaling factor given, or lattice constants given?
    params: ref_const = None, (optional), float, or list of floats, lattice constant for scaling 1.0
    params: multi = False, (optional), bool, multiple plots?
    params: plotlables, list of strings, for lableling of the plots.
    params: title

    """
    # TODO: make box which shows fit results. (fit resuls have to be past)
    # TODO: multiple plots in one

    #print markersize_g
    if relative:
        if ref_const:
            xlabel = r'Relative Lattice Constant [a/{}$\AA$]'.format(ref_const)
        else:
            xlabel = r'Relative Lattice Constant'
    else:
        xlabel = r'Lattice Constant [$\AA$]'

    fig = pp.figure(num=None, figsize=figsize_g, dpi=dpi_g, facecolor=facecolor_g, edgecolor=edgecolor_g)
    ax = fig.add_subplot(111)
    ax.set_title(title, fontsize=title_fontsize_g, alpha=alpha_g, ha='center')
    ax.set_xlabel(xlabel, fontsize=labelfonstsize_g)
    ax.set_ylabel(r'Total energy [eV]', fontsize=labelfonstsize_g)
    ax.yaxis.set_tick_params(size = tick_params_g.get('size', 4.0),
                             width = tick_params_g.get('width', 1.0),
                             labelsize = tick_params_g.get('labelsize', 14),
                             length = tick_params_g.get('length', 5))
    ax.xaxis.set_tick_params(size = tick_params_g.get('size', 4.0),
                             width = tick_params_g.get('width', 1.0),
                             labelsize = tick_params_g.get('labelsize', 14),
                             length = tick_params_g.get('length', 5))
    ax.yaxis.get_major_formatter().set_powerlimits((0, 3))
    ax.yaxis.get_major_formatter().set_useOffset(False)
    if multi:
        # TODO test if dim of total_e = dim of scaling, dim plot lables...
        # or parse on scaling?
        for i, scale in enumerate(scaling):
            print i
            p1 = pp.plot(scale, Total_energy[i], 'o-', label = plotlables[2*i],
                         linewidth = linewidth_g, markersize = markersize_g)
            p2 = pp.plot(scale, fit_y[i], 's-', label = plotlables[2*i+1],
                         linewidth = linewidth_g, markersize = markersize_g)
    else:
        p1 = pp.plot(scaling, Total_energy, 'o-', label = plotlables[0],
                      linewidth = linewidth_g, markersize = markersize_g)

        p2 = pp.plot(scaling, fit_y, r'-', label = plotlables[1],
                     linewidth = linewidth_g, markersize = markersize_g)
    
    pp.legend(bbox_to_anchor=(0.85, 1), loc=2, borderaxespad=0., fancybox=True)
    pp.legend(loc='best', borderaxespad=0., fancybox=True) #, framealpha=0.5) #loc='upper right')
    #lg = pp.legend(bbox_to_anchor=(0.76, 0.400), loc=2, borderaxespad=0., borderpad=1, fancybox=True, title =r'K-pts in $\bf{k_{x,y,z}}$',fontsize=14)#loc='best', fancybox=True) #, framealpha=0.5) #loc='upper right')
    #lg.get_frame().set_linewidth(2.0)
    #lg.get_title().set_fontsize('16') #legend 'Title' fontsize

    print save_plots_g
    if save_plots_g:
        # TODO override or not, better title?
        savefilename = '{}.{}'.format(saveas, save_format_g)
        print 'save plot to: {}'.format(savefilename)
        pp.savefig(savefilename, format=save_format_g, transparent=True)
    else:
        pp.show()





def plot_relatxation_results():
    """
    Plot from the result node of a relaxation workflow, 
    All forces of every atom type versus relaxation cycle.
    Average force of all atom types versus relaxation cycle.
    Absolut relaxation in Angstroem of every atom type.
    Relative realxation of every atom type to a reference structure.
    (if none given use the structure from first relaxation cycle as reference)
    """
    pass


def plot_dos(path_to_dosfile, only_total=False, saveas=r'dos_plot', title=r'Density of states', linetyp='-', legend=True, limits=[None, None]):
    """
    Plot the total density of states from a FLEUR DOS.1 file
    
    params:
    """
    doses = []
    energies = []
    #dosmt_total = np.zeros(nData, "d")
    #totaldos = np.zeros(nData, "d")

    #read data from file
    datafile = 'DOS.1'
    data = np.loadtxt(datafile,skiprows = 0)

    energy = data[..., 0]
    totaldos = data[:, 1]
    interstitialdos = data[:, 2]
    dosmt_total = totaldos-interstitialdos

    doses = [totaldos, interstitialdos, dosmt_total]
    energies = [energy, energy, energy]
    xlabel = r'E - E$_F$ [eV]'
    ylabel = r'DOS [eV$^{-1}$]'

    if only_total:
        single_scatterplot(totaldos, energy, xlabel, ylabel, title, plotlabel='total dos', linetyp=linetyp, limits=limits, saveas=saveas)
    else:
        multiple_scatterplots(doses, energies, xlabel, ylabel, title, plot_labels=['Total', 'Interstitial', 'Muffin-Tin'], linetyp=linetyp, legend=legend, limits=limits, saveas=saveas)


def plot_dos_total_atom_resolved():
    """
    Plot the density of states from a FLEUR DOS.1 file
    
    params:
    """
    pass

def plot_dos_total_l_resolved():
    """
    Plot the density of states from a FLEUR DOS.1 file
    
    params:
    """
    pass

def plot_dos_atom_resolved():
    """
    Plot the density of states from a FLEUR DOS.1 file
    
    params:
    """
    pass


def plot_spin_dos():
    """
    Plot a spin density of states from FLEUR DOS.1, DOS.2 files together in one
    plot.
    
    params:
    """
    pass


def plot_bands(path_to_bands_file, kpath, title='Bandstructure', plotlabel ='bands', linetyp='o', limits=[None, None], saveas ='bandstructure', color = 'k'):
    """
    Plot a band structure from a bands.1 file from FLEUR
    params: kpath: dict: {r"$\Gamma$": 0.00000, r"$H$" : 1.04590, r"$N$" : 1.78546, r"$P$": 2.30841, r"$\Gamma$" : 3.21419, r"$N$" 3.95375 }

    """
    xpos = kpath.values()
    xNames = kpath.keys()
    data = np.loadtxt(path_to_bands_file,skiprows = 0)
    xdata = data[..., 0]
    ydata = data[..., 1]
    xmin = min(xdata)-0.01
    xmax = max(xdata)+0.01
    ymin = 0
    ymax = max(ydata)
    xlabel = ''
    ylabel = r'$E - E_F$ [eV]'
    fig = pp.figure(num=None, figsize=figsize_g, dpi=dpi_g, facecolor=facecolor_g, edgecolor=edgecolor_g)
    ax = fig.add_subplot(111)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(axis_linewidth_g)

    pp.xticks(xpos,xNames)
    ax.set_title(title, fontsize=title_fontsize_g, alpha=alpha_g, ha='center')
    ax.set_xlabel(xlabel, fontsize=labelfonstsize_g)
    ax.set_ylabel(ylabel, fontsize=labelfonstsize_g)
    ax.yaxis.set_tick_params(size = tick_params_g.get('size', 4.0),
                             width = tick_params_g.get('width', 1.0),
                             labelsize = tick_params_g.get('labelsize', 14),
                             length = tick_params_g.get('length', 5))
    ax.xaxis.set_tick_params(size = tick_params_g.get('size', 4.0),
                             width = tick_params_g.get('width', 1.0),
                             labelsize = tick_params_g.get('labelsize', 14),
                             length = tick_params_g.get('length', 5))
    ax.yaxis.get_major_formatter().set_powerlimits((0, 3))
    ax.yaxis.get_major_formatter().set_useOffset(False)
    p1 = pp.plot(xdata, ydata, linetyp, label = plotlabel, color = color,
                 linewidth = linewidth_g, markersize = markersize_g)

    if limits:
        if limits[0]:
            xmin = limits[0][0]
            xmax = limits[0][1]
            pp.xlim(xmin, xmax)
        if limits[1]:
            ymin = limits[1][0]
            ymax = limits[1][1]
            pp.ylim(ymin, ymax)
    for i in xpos:
        pp.axvline(x=i, ymin=ymin, ymax = ymax, linewidth=1, color='k')

    if save_plots_g:
        savefilename = '{}.{}'.format(saveas, save_format_g)
        print 'save plot to: {}'.format(savefilename)
        pp.savefig(savefilename, format=save_format_g, transparent=True)
    else:
        pp.show()

def plot_certain_bands():
    """
    Plot only certain bands from a bands.1 file from FLEUR
    """
    pass


def plot_bands_and_dos():
    """
    PLot a Bandstructure with a density of states on the right side.
    """
    pass



