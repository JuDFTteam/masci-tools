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
legend_g = False

# save all plots?
save_plots_g = False# True
save_format_g = 'png'#'pdf'
tightlayout_g = False
##############


def set_plot_defaults(title_fontsize = 16,
                      linewidth = 2.0,
                      markersize = 4.0,
                      labelfonstsize = 15,
                      ticklabelsize = 14,
                      axis_linewidth = 2.0,
                      tick_params = {'size' : 4.0, 'width' : 1.0,
                                     'labelsize' : ticklabelsize_g,
                                     'length' : 5},
                      figsize = (8, 6),
                      save_plots = False, #True,
                      save_format = 'pdf', legend=True, **kwargs):
    """
    Try to use this to set some global default values.
    
    Set some evironment variable with or global variables.
    """
    global linewidth_g, markersize_g, labelfonstsize_g, title_fontsize_g, axis_linewidth_g
    global ticklabelsize_g, tick_params_g, save_plots_g, save_format_g, legend_g, figsize_g
    
    title_fontsize_g = title_fontsize
    # plot properties
    linewidth_g = linewidth
    markersize_g = markersize
    axis_linewidth_g = axis_linewidth
    # x, y label
    labelfonstsize_g = labelfonstsize
    # ticks
    ticklabelsize_g = ticklabelsize
    tick_params_g.update(tick_params)

    # save all plots?
    save_plots_g = save_plots
    save_format_g = save_format
    #print markersize_g
    
    legend_g = legend
    figsize_g = figsize


###########################
## general plot routines ##
###########################


def single_scatterplot(ydata, xdata, xlabel, ylabel, title, plotlabel ='scatterplot', 
                       linetyp='o-', limits=[None, None], saveas ='scatterplot', 
                       color = 'k', scale = [None, None]):
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
    #ax.yaxis.get_major_formatter().set_powerlimits((0, 3))
    #ax.yaxis.get_major_formatter().set_useOffset(False)
    #ax.xaxis.set_major_formatter(DateFormatter("%b %y"))
    p1 = pp.plot(xdata, ydata, linetyp, label = plotlabel, color = color,
                 linewidth = linewidth_g, markersize = markersize_g)
    if scale:
        if scale[0]:
            ax.set_xscale(scale[0])
        elif scale[1]:
            ax.set_yscale(scale[1])
        else:
            pass
        
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


def multiple_scatterplots(ydata, xdata, xlabel, ylabel, title, plot_labels, 
                          linetyp='o-', legend=legend_g, 
                          legend_option = {},
                          saveas ='mscatterplot', limits=[None, None], scale = [None, None]):
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
    if scale:
        if scale[0]:
            ax.set_xscale(scale[0])
        elif scale[1]:
            ax.set_yscale(scale[1])
        else:
            pass
    
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
        print legend
        #{anchor, title, fontsize, linewith, borderaxespad}
        # defaults 'anchor' : (0.75, 0.97), 'title' : 'Legend', 'fontsize' : 17, 'linewith' : 1.5, 'borderaxespad' : }, 
        legends_defaults = {'bbox_to_anchor' : (0.70, 0.97), 'fontsize' : 12, 'linewidth' : 1.5, 'borderaxespad' : 0 , 'loc' : 2, 'fancybox' : True} #'title' : 'Legend',
        loptions = legends_defaults.copy()
        loptions.update(legend_option)
        linewidth = loptions.pop('linewidth', 1.5)
        #title_font_size = loptions.pop('title_font_size', 15)
        leg = pp.legend(**loptions)#bbox_to_anchor=loptions['anchor'],loc=loptions['loc'], title=legend_title, borderaxespad=0., fancybox=True)
        leg.get_frame().set_linewidth(linewidth)
        #leg.get_title().set_fontsize(title_font_size) #legend 'Title' fontsize
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
    ylabel1 = r'Total energy difference [Htr]'
    ylabel2 = r'Distance [me/bohr^3]'
    title1 = r'Total energy difference over scf-Iterations'
    #title2 = r'Distance over scf-Iterations'
    title2 = r'Convergence (log)'
    # since we make a log plot of the total_energy make sure to plot the absolute total energy
    total_energy_abs_diff = []
    for en0, en1 in zip(total_energy[:-1], total_energy[1:]):
        total_energy_abs_diff.append(abs(en1-en0))
    #saveas3 ='t_energy_convergence2'
    
    single_scatterplot(total_energy_abs_diff, iteration[1:], xlabel, ylabel1, title1, plotlabel='delta total energy', saveas=saveas1, scale=[None, 'log'])
    #single_scatterplot(total_energy, iteration, xlabel, ylabel1, title1, plotlabel='total energy', saveas=saveas3)
    single_scatterplot(distance, iteration, xlabel, ylabel2, title2, plotlabel='distance', saveas=saveas2, scale=[None, 'log'])

def plot_convergence_results_m(distances, total_energies, iterations, plot_labels=[], saveas1='t_energy_convergence', saveas2='distance_convergence'):
    """
    Plot the total energy versus the scf iteration
    and plot the distance of the density versus iterations.
    """
    xlabel = r'Iteration'
    ylabel1 = r'Total energy difference [Htr]'
    ylabel2 = r'Distance [me/bohr^3]'
    title1 = r'Total energy difference over scf-Iterations'
    #title2 = r'Distance over scf-Iterations'
    title2 = r'Convergence (log)'
    
    iterations1 = []
    plot_labels1 = []
    plot_labels2 = []

    # since we make a log plot of the total_energy make sure to plot the absolute total energy
    total_energy_abs_diffs = []    
    for i, total_energy in enumerate(total_energies): 
        iterations1.append(iterations[i][1:])
        total_energy_abs_diff = []
        for en0, en1 in zip(total_energy[:-1], total_energy[1:]):
            total_energy_abs_diff.append(abs(en1-en0))
        total_energy_abs_diffs.append(total_energy_abs_diff)
        plot_labels1.append('delta total energy {}'.format(i))
        plot_labels2.append('distance {}'.format(i))
    #saveas3 ='t_energy_convergence2'
    if plot_labels:
        plot_labels1 = plot_labels
        plot_labels2 = plot_labels
    multiple_scatterplots(total_energy_abs_diffs, iterations1, xlabel, ylabel1, title1, plot_labels1, saveas=saveas1, scale=[None, 'log'])
    multiple_scatterplots(distances, iterations, xlabel, ylabel2, title2, plot_labels2, saveas=saveas2, scale=[None, 'log'])


def plot_lattice_constant(Total_energy, scaling, fit_y=None, relative=True, ref_const=None, multi=False, plotlables = [r'simulation data', r'fit results'], title = r'Equation of states', saveas = 'Lattice_constant'):
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
            xlabel = r'Relative Volume [a/{}$\AA$]'.format(ref_const)
        else:
            xlabel = r'Relative Volume'
    else:
        xlabel = r'Volume [$\AA$]'

    fig = pp.figure(num=None, figsize=figsize_g, dpi=dpi_g, facecolor=facecolor_g, edgecolor=edgecolor_g)
    ax = fig.add_subplot(111)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(axis_linewidth_g)
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
            #print i
            p1 = pp.plot(scale, Total_energy[i], 'o-', label = plotlables[2*i],
                         linewidth = linewidth_g, markersize = markersize_g)
            if fit_y:
                p2 = pp.plot(scale, fit_y[i], 's-', label = plotlables[2*i+1],
                             linewidth = linewidth_g, markersize = markersize_g)
    else:
        p1 = pp.plot(scaling, Total_energy, 'o-', label = plotlables[0],
                      linewidth = linewidth_g, markersize = markersize_g)
        if fit_y:
            p2 = pp.plot(scaling, fit_y, r'-', label = plotlables[1],
                         linewidth = linewidth_g, markersize = markersize_g)
    if legend_g:
        pp.legend(bbox_to_anchor=(0.85, 1), loc=2, borderaxespad=0., fancybox=True)
        pp.legend(loc='best', borderaxespad=0., fancybox=True) #, framealpha=0.5) #loc='upper right')
        #lg = pp.legend(bbox_to_anchor=(0.76, 0.400), loc=2, borderaxespad=0., borderpad=1, fancybox=True, title =r'K-pts in $\bf{k_{x,y,z}}$',fontsize=14)#loc='best', fancybox=True) #, framealpha=0.5) #loc='upper right')
        #lg.get_frame().set_linewidth(2.0)
        #lg.get_title().set_fontsize('16') #legend 'Title' fontsize

    #print save_plots_g
    if save_plots_g:
        # TODO override or not, better title?
        savefilename = '{}.{}'.format(saveas, save_format_g)
        print 'save plot to: {}'.format(savefilename)
        pp.savefig(savefilename, format=save_format_g, transparent=True)
    else:
        pp.show()





def plot_relaxation_results():
    """
    Plot from the result node of a relaxation workflow, 
    All forces of every atom type versus relaxation cycle.
    Average force of all atom types versus relaxation cycle.
    Absolut relaxation in Angstroem of every atom type.
    Relative realxation of every atom type to a reference structure.
    (if none given use the structure from first relaxation cycle as reference)
    """
    pass


def plot_dos(path_to_dosfile, only_total=False, saveas=r'dos_plot', title=r'Density of states', linetyp='-', legend=legend_g, limits=[None, None]):
    """
    Plot the total density of states from a FLEUR DOS.1 file
    
    params:
    """
    doses = []
    energies = []
    #dosmt_total = np.zeros(nData, "d")
    #totaldos = np.zeros(nData, "d")

    #read data from file
    datafile = path_to_dosfile#'DOS.1'
    data = np.loadtxt(datafile,skiprows = 0)

    energy = data[..., 0]
    totaldos = data[:, 1]
    interstitialdos = data[:, 2]
    dosmt_total = totaldos-interstitialdos

    doses = [totaldos, interstitialdos, dosmt_total]
    energies = [energy, energy, energy]
    #xlabel = r'E - E$_F$ [eV]'
    xlabel = r'Energy [eV]'
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

    pp.xticks(xpos, xNames)
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


def plot_corelevels(coreleveldict, compound=''):
    """
    Ploting function to visualize corelevels and corelevel shifts
    """

    for elem, corelevel_dict in coreleveldict.iteritems():
        # one plot for each element
        plot_one_element_corelv(corelevel_dict, elem, compound=compound)
        
def plot_one_element_corelv(corelevel_dict, element, compound=''):
    """
    This routine creates a plot which visualizes all the binding energies of one 
    element (and currenlty one corelevel) for different atomtypes.
    
    i.e
    
    corelevels = {'W' : {'4f7/2' : [123, 123.3, 123.4 ,123.1], 
                     '4f5/2' : [103, 103.3, 103.4, 103.1]}, 
              'Be' : {'1s': [118, 118.2, 118.4, 118.1, 118.3]}}
    """
    corelevels_names = []
    xdata_all = []
    ydata_all = []
        
    for corelevel, corelevel_list in corelevel_dict.iteritems():
        #print corelevel
        n_atom = len(corelevel_list)
        x_axis = list(range(0,n_atom,1))
        y_axis = corelevel_list
        xdata_all.append(x_axis)
        ydata_all.append(y_axis)
        corelevels_names.append(corelevel)
    
    elem = element        
    xdata = xdata_all[0]
    ydata = ydata_all[0]
    xlabel = '{} atomtype'.format(elem)
    ylabel = 'energy in eV'
    title = 'Element: {} from {} cl {}'.format(elem, title, corelevels_names)
    #plotlabel ='corelevel shifts'
    #linetyp='o-'
    xmin = xdata[0] - 0.5
    xmax = xdata[-1] + 0.5
    ymin = min(ydata)-1
    ymax = max(ydata)+1
    #limits=[(xmin, xmax), (ymin, ymax)], 
    saveas ='scatterplot'
    #color = 'k'
    scale = [None, None]
    font = {'family': 'serif',
            'color':  'darkred',
            'weight': 'normal',
            'size': 16,
            }
    
    
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

    for j,y in enumerate(ydata_all):
        for i,x in enumerate(xdata):
            lenx = xmax-xmin
            length = 0.5/lenx
            offset = 0.5/lenx
            xminline = x/lenx + offset - length/2
            xmaxline = x/lenx + offset + length/2
            pp.axhline(y=y[i], xmin=xminline, xmax=xmaxline, linewidth=2, color='k')
            text = r'{}'.format(y[i])
            pp.text(x-0.25, y[i]+0.3, text, fontdict=font)
        
        
    if scale:
        if scale[0]:
            ax.set_xscale(scale[0])
        elif scale[1]:
            ax.set_yscale(scale[1])
        else:
            pass

    pp.xlim(xmin, xmax)
    pp.ylim(ymin, ymax)
    if save_plots_g:
        savefilename = '{}.{}'.format(saveas, save_format_g)
        print 'save plot to: {}'.format(savefilename)
        pp.savefig(savefilename, format=save_format_g, transparent=True)
    else:
        pp.show()            


def plot_corelevel_spectra(coreleveldict, natom_typesdict, exp_references={}, show_single=True, show_ref=True, energy_range=[None, None], title = '', fwhm_g=0.6, fwhm_l=0.1, energy_grid=0.2, peakfunction='voigt', linetyp_spec='o-'):
    #show_compound=True, , compound_info={} compound_info dict: dict that can be used to specify what component should be shown together     compound_info = {'Be12Ti' : {'Be' : 4, 'Ti' : 1}, 'BeTi' : {'Be' : 1, 'Ti' : 1}}


    """
    Ploting function of corelevel in the form of a spectrum.
    
    Convention: Binding energies are positiv!
    
    Args:
        coreleveldict: dict of corelevels with a list of corelevel energy of atomstypes 
        # (The given corelevel accounts for a weight (number of electrons for full occupied corelevel) in the plot.)
        natom_typesdict: dict with number of atom types for each entry
    Kwargs:
        exp_references: dict with experimental refereces, will be ploted as vertical lines
        show_single (bool): plot all single peaks. 
        title (string): something for labeling
        fwhm (float): full width half maximum of peaks (gaus, lorentz or voigt_profile)
        energy_grid (float): energy resolution
        linetyp_spec : linetype for spectrum
        peakfunction (string): what the peakfunction should be {'voigt', 'pseudo-voigt', 'lorentz', 'gaus'}
    example:
    
    coreleveldict = {u'Be': {'1s1/2' : [-1.0220669053033051, -0.3185614920138805, 
                                        -0.7924091040092139]}}
    n_atom_types_Be12Ti = {'Be' : [4,4,4]}
    """
    xdata_all = []
    ydata_all = []
    ydata_spec = []
    xdata_spec = []
    energy_grid = energy_grid # eV
    #count = 0
    #compound_info_new = compound_info
    
    for elem, corelevel_dict in coreleveldict.iteritems():
        natom = natom_typesdict.get(elem, 0)
        #elem_count = 0
        for corelevel_name, corelevel_list in corelevel_dict.iteritems():
            # get number of electron if fully occ:
            nelectrons = 1
            if 's' in corelevel_name:
                nelectrons = 2
            else:
                max_state_occ_spin = {'1/2' : 2, '3/2' : 4, '5/2' : 6, '7/2' : 8}
                # check if spin in name
                for key, val in max_state_occ_spin.iteritems():
                    if key in corelevel_name:
                        nelectrons = val
            for i,corelevel in enumerate(corelevel_list):
                xdata_all.append(corelevel)
                ydata_all.append(natom[i]*nelectrons)
                #count = count + 1
                #elem_count = elem_count + 1
            '''
            not working yet bad design
            if compound_info:
                for compound, element_dict in compound_info.iteritems():
                    for elemt, number in element_dict.iteritems():
                        print number
                        if elemt == elem:
                            # we need to set the index that we find it later, group it
                            if isinstance(number, list):
                                continue
                            compound_info_new[compound][elemt] = [count-elem_count, count-elem_count+number]
             '''

    xmin = min(xdata_all) - 2 #0.5
    xmax = max(xdata_all)+ 2   #0.5
    if energy_range[0]:
        xmin = energy_range[0]
    if energy_range[1]:
        xmax = energy_range[1]
    # xdata_spec = np.array(np.arange(xmax,xmin, -energy_grid))
    xdata_spec = np.array(np.arange(xmin, xmax, energy_grid))
    ydata_spec = np.zeros(len(xdata_spec), dtype=float)
    ydata_single_all = []
    
    for i,xpoint in enumerate(xdata_all):
        if peakfunction== 'gaus':
            data_f = np.array(gaussian(xdata_spec, fwhm_g, xpoint))#, 1.0))
        elif peakfunction== 'voigt':
            data_f = np.array(voigt_profile(xdata_spec, fwhm_g, fwhm_l, xpoint))# different fwhn for g und l       
        elif peakfunction== 'pseudo-voigt':
            data_f = np.array(pseudo_voigt_profile(xdata_spec, fwhm_g, fwhm_l, xpoint))
        elif peakfunction== 'lorentz':
            data_f = np.array(lorentzian(xdata_spec, fwhm_l, xpoint))
        else:
            print('given peakfunction type not known')
            data_f = []
            return

        #gaus_f = lorentzian(xdata_spec, xpoint, 0.6, 100.0)
        ydata_spec = ydata_spec + ydata_all[i]*data_f
        ydata_single_all.append(ydata_all[i]*data_f)
    
    '''
    # TODO this is bad... a redesign might be good, maybe input change...
    ydata_compound = []
    if show_compound and compound_info:
        compound_plot_label = []
        for name, element_dict in compound_info_new.iteritems():
            for elem, value in element_dict.iteritems():
                compound_plot_label.append(name)
                sumdata = np.zeros(len(xdata_spec), dtype=float)
                for data in ydata_single_all[value[0]:value[1]]:
                    sumdata = sumdata + data
                ydata_compound.append(sumdata)
    '''            
    xdata = xdata_all
    ydata = ydata_all
    ymax2 = max(ydata_spec)+1


    #print len(xdata), len(ydata)
    xlabel = 'Binding energy [eV]'
    ylabel = 'Intensity [arb] (natoms*nelectrons)'
    title = title#'Spectrum of {}'.format(compound)
    plotlabel ='corelevel shifts'
    linetyp = 'o'
    linetyp1 = linetyp_spec#'-'
    linewidth_g1 = 2


    ymin = -0.3
    ymax = max(ydata)+1


    limits=[(xmin, xmax), (ymin, ymax)], 
    saveas ='XPS_theo_{}_{}'.format(fwhm_g, title)
    saveas1 ='XPS_theo_2_{}_{}'.format(fwhm_g, title)
    color = 'k'
    scale = [None, None]
    font = {'family': 'serif',
            'color':  'darkred',
            'weight': 'normal',
            'size': 16,
            }
    
    ##### PLOT 1, plot raw datapoints
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
    p1 = pp.plot(xdata_all, ydata_all, linetyp, label = plotlabel, color = color,
                 linewidth = linewidth_g, markersize = markersize_g)
    
    if show_ref and exp_references:
        for elm,ref_list_dict in exp_references.iteritems():
            for state,ref_list in ref_list_dict.iteritems():
                for ref in ref_list:                
                    pp.axvline(ymin=0, ymax=0.1, x=ref, linewidth=2, color='k')
    '''
    for j,y in enumerate(ydata_all):
        for i,x in enumerate(xdata):
            lenx = xmax-xmin
            length = 0.5/lenx
            offset = 0.5/lenx
            xminline = x/lenx + offset - length/2
            xmaxline = x/lenx + offset + length/2
            plt.axhline(y=y[i], xmin=xminline, xmax=xmaxline, linewidth=2, color='k')
            text = r'{}'.format(y[i])
            plt.text(x-0.25, y[i]+0.3, text, fontdict=font)
    '''    
        
    if scale:
        if scale[0]:
            ax.set_xscale(scale[0])
        elif scale[1]:
            ax.set_yscale(scale[1])
        else:
            pass
        
    pp.ylim(ymin, ymax)
    #flip x axes
    pp.xlim(xmax, xmin)
    
    if save_plots_g:
        savefilename = '{}.{}'.format(saveas, save_format_g)
        print 'save plot to: {}'.format(savefilename)
        pp.savefig(savefilename, format=save_format_g, transparent=True)
    else:
        pp.show()
    
    
    ##### PLOT 2, plot spectra, voigts around datapoints
    
    fig1 = pp.figure(num=None, figsize=figsize_g, dpi=dpi_g, facecolor=facecolor_g, edgecolor=edgecolor_g)
    ax1 = fig1.add_subplot(111)
    for axis in ['top','bottom','left','right']:
        ax1.spines[axis].set_linewidth(axis_linewidth_g)
    ax1.set_title(title, fontsize=title_fontsize_g, alpha=alpha_g, ha='center')
    ax1.set_xlabel(xlabel, fontsize=labelfonstsize_g)
    ax1.set_ylabel(ylabel, fontsize=labelfonstsize_g)
    ax1.yaxis.set_tick_params(size = tick_params_g.get('size', 4.0),
                             width = tick_params_g.get('width', 1.0),
                             labelsize = tick_params_g.get('labelsize', 14),
                             length = tick_params_g.get('length', 5))
    ax1.xaxis.set_tick_params(size = tick_params_g.get('size', 4.0),
                             width = tick_params_g.get('width', 1.0),
                             labelsize = tick_params_g.get('labelsize', 14),
                             length = tick_params_g.get('length', 5))
    ax1.yaxis.get_major_formatter().set_powerlimits((0, 3))
    ax1.yaxis.get_major_formatter().set_useOffset(False)
    
    p11 = pp.plot(xdata_spec, ydata_spec, linetyp1, label=plotlabel, color=color,
                 linewidth=linewidth_g1, markersize=markersize_g)
                 
    if show_single:
        for single_peek in ydata_single_all:
            pp.plot(xdata_spec, single_peek, '-', label=plotlabel, #color = color,
                 linewidth=linewidth_g1, markersize = markersize_g)
                 
    if show_ref and exp_references:
        for elm,ref_list_dict in exp_references.iteritems():
            for state,ref_list in ref_list_dict.iteritems():
                for ref in ref_list:                
                    pp.axvline(ymin=0, ymax=0.1, x=ref, linewidth=2, color='k')
    '''
    if show_compound and compound_info:   
        for i,compound_data in enumerate(ydata_compound):
            plotlabel = compound_plot_label[i]
            pp.plot(xdata_spec, compound_data, '-', label=plotlabel, color = color,
                 linewidth=linewidth_g1, markersize = markersize_g) 
    '''
    if scale:
        if scale[0]:
            ax1.set_xscale(scale[0])
        elif scale[1]:
            ax1.set_yscale(scale[1])
        else:
            pass
        
    pp.ylim(ymin, ymax2)
    #flip x axes
    pp.xlim(xmax, xmin)

    if save_plots_g:
        savefilename = '{}.{}'.format(saveas1, save_format_g)
        print 'save plot to: {}'.format(savefilename)
        pp.savefig(savefilename, format=save_format_g, transparent=True)
    else:
        pp.show()            

'''
def plot_corelevel_spectra(coreleveldict, natom_typesdict, compound = ''):
    """
    Ploting function of corelevel in the form of a spectrum
    """
    xdata_all = []
    ydata_all = []
    ydata_spec = []
    xdata_spec = []
    
    for elem, corelevel_dict in coreleveldict.iteritems():
        natom = natom_typesdict.get(elem, 0)
        print natom
        for corelevel_name, corelevel_list in corelevel_dict.iteritems():
            for i,corelevel in enumerate(corelevel_list):
                xdata_all.append(corelevel)
                ydata_all.append(natom[i])
              
    xmin = min(xdata_all) - 2#0.5
    xmax = max(xdata_all)+ 2#0.5
    
    xdata_spec = np.array(np.arange(xmin,xmax, 0.1))
    ydata_spec = np.zeros(len(xdata_spec), dtype=float)                
    for i,xpoint in enumerate(xdata_all):
        gaus_f = gaussian(xdata_spec, xpoint, 0.6, 1.0)
        #gaus_f = lorentzian(xdata_spec, xpoint, 0.6, 100.0)
        ydata_spec = ydata_spec + ydata_all[i]*gaus_f
        
    xdata = xdata_all
    ydata = ydata_all
    ymax2 = max(ydata_spec)+1

    xlabel = 'Binding energy [eV]'
    ylabel = 'Intensity [arb] (natoms)'
    title = 'Spectrum of {}'.format(compound)
    plotlabel ='corelevel shifts'
    linetyp = 'o'
    linetyp1 = '-'
    linewidth_g1 = 1



    ymin = -0.3
    ymax = max(ydata)+1


    #limits=[(xmin, xmax), (ymin, ymax)], 
    saveas ='scatterplot'
    color = 'k'
    scale = [None, None]
    
    
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
    p1 = pp.plot(xdata_all, ydata_all, linetyp, label = plotlabel, color = color,
                 linewidth = linewidth_g, markersize = markersize_g)
  
        
    if scale:
        if scale[0]:
            ax.set_xscale(scale[0])
        elif scale[1]:
            ax.set_yscale(scale[1])
        else:
            pass
        
    pp.xlim(xmin, xmax)
    pp.ylim(ymin, ymax)
    if save_plots_g:
        savefilename = '{}.{}'.format(saveas, save_format_g)
        print 'save plot to: {}'.format(savefilename)
        pp.savefig(savefilename, format=save_format_g, transparent=True)
    else:
        pp.show()
    
    
    
    fig1 = pp.figure(num=None, figsize=figsize_g, dpi=dpi_g, facecolor=facecolor_g, edgecolor=edgecolor_g)
    ax1 = fig1.add_subplot(111)
    for axis in ['top','bottom','left','right']:
        ax1.spines[axis].set_linewidth(axis_linewidth_g)
    ax1.set_title(title, fontsize=title_fontsize_g, alpha=alpha_g, ha='center')
    ax1.set_xlabel(xlabel, fontsize=labelfonstsize_g)
    ax1.set_ylabel(ylabel, fontsize=labelfonstsize_g)
    ax1.yaxis.set_tick_params(size = tick_params_g.get('size', 4.0),
                             width = tick_params_g.get('width', 1.0),
                             labelsize = tick_params_g.get('labelsize', 14),
                             length = tick_params_g.get('length', 5))
    ax1.xaxis.set_tick_params(size = tick_params_g.get('size', 4.0),
                             width = tick_params_g.get('width', 1.0),
                             labelsize = tick_params_g.get('labelsize', 14),
                             length = tick_params_g.get('length', 5))
    ax1.yaxis.get_major_formatter().set_powerlimits((0, 3))
    ax1.yaxis.get_major_formatter().set_useOffset(False)
    
    p11 = pp.plot(xdata_spec, ydata_spec, linetyp1, label = plotlabel, color = color,
                 linewidth = linewidth_g1, markersize = markersize_g)  
    if scale:
        if scale[0]:
            ax1.set_xscale(scale[0])
        elif scale[1]:
            ax1.set_yscale(scale[1])
        else:
            pass
        
    pp.xlim(xmin, xmax)
    pp.ylim(ymin, ymax2)
    if save_plots_g:
        savefilename = '{}.{}'.format(saveas, save_format_g)
        print 'save plot to: {}'.format(savefilename)
        pp.savefig(savefilename, format=save_format_g, transparent=True)
    else:
        pp.show()            


def gaussian(x,E,F,m):
    """
    Gives back a gaussian
    E is mean energy
    x are the values
    F is the area, derivation ?
    m is ?
    """
    gaus = []
    for point in x:
        gp = np.exp(-2*np.log(2)*(1-m/100.)*((point-E)/F)**2)
        #print(gp)
        gaus.append(gp)
    return np.array(gaus)

def lorentzian(x,E,F,m):
    """
    Gives back a loretzian
    E is mean energy
    x are the values
    F is the area, derivation, FWTH?
    m is ?
    """
    lorentz = []
    for point in x:
        lp = 1./(1+4*(m/100.)*((point-E)/F)**2)
        lorentz.append(lp)
    return np.array(lorentz)
'''
'''

def gaussian(x,E,F,m):
    """
    Gives back a gaussian
    E is mean energy
    x are the values
    F is the area, derivation ?
    m is ?
    """
    gaus = []
    for i in range(len(x)):
        gp = np.exp(-2*np.log(2)*(1-m/100.)*((x[i]-E)/F)**2)
        #print(gp)
        gaus.append(gp)
    #return np.array(gaus)
    return gaus

def lorentzian(x,E,F,m):
    """
    Gives back a loretzian
    E is mean energy
    x are the values
    F is the area, derivation, FWTH?
    m is ?
    """
    lorentz = []
    for i in range(len(x)):
        lp = 1./(1+4*(m/100.)*((x[i]-E)/F)**2)
        lorentz.append(lp)
    #return np.array(lorentz)
    return lorentz

def pseudo_voigt_profile(x,E,F,m,mu):
    """
    Linear combination of gaussian and loretzian instead of convolution
    """
    # TODO currently the varialble in gaus and lorentz might not be the same..
    pseudo_voigt = []
    if not (mu <=1):
        print('mu has to be smaller than 1.')
        return []
    gaus = gaussian(x,E,F,m)
    lorentz = lorentzian(x,E,F,m)
    pseudo_voigt = mu * gaus  + (1-mu)*lorentz
    return np.array(pseudo_voigt)

def voigt_profile(x,E,F,m):
    """
    Diskrete Convolution of a gaussian and loretzian.
    v(t) = sum of (g(x)*l(x-t))
    # Still buggy
    """
    voigt = []
    x2 = x
    #lor = np.array(lorentzian(x,E,F,m))
    #gaus = np.array(gaussian(x,E,F,m))
    for point in x:
        v_t = 0#
        for point2 in x2:
            point2a = [point2]
            #print point2
            point2_ta =  [point - point2]
            print point2_ta
            v_t = v_t + gaussian(point2a,E,F,m)[0]*lorentzian(point2_ta,E,F,m)[0]
        voigt.append(v_t)
    print(voigt)
    return np.array(voigt)
'''  
    

def gaussian(x, fwhm, mu):
    """ 
    Returns Gaussian line shape at x with FWHM fwhm and mean mu 
    
    """
    
    #hwhm = fwhm/2.0
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    #return np.sqrt(np.log(2) / np.pi) / hwhm\
    #                         * np.exp(-((x-mu) / hwhm)**2 * np.log(2))
    return np.exp(-(x-mu)**2 / (2*(sigma**2))) / (np.sqrt(2 * np.pi) * sigma)

def lorentzian(x, fwhm, mu):
    """ 
    Returns a Lorentzian line shape at x with FWHM fwhm and mean mu 
    """
    hwhm = fwhm/2.0
    return hwhm / np.pi / ((x-mu)**2 + hwhm**2)

def voigt_profile(x, fwhm_g, fwhm_l, mu):
    """
    Return the Voigt line shape at x with Lorentzian component FWHM fwhm_l
    and Gaussian component FWHM fwhm_g and mean mu. 
    There is no closed form for the Voigt profile, 
    but it is related to the real part of the Faddeeva function (wofz),
    which is used here.

    """
    from scipy.special import wofz

    hwhm_l = fwhm_l/2.0
    sigma = fwhm_g / (2 * np.sqrt(2 * np.log(2)))
    # complex 1j
    return np.real(wofz(((x-mu) + 1j*hwhm_l)/sigma/np.sqrt(2))) / sigma\
                                                           /np.sqrt(2*np.pi)

def pseudo_voigt_profile(x, fwhm_g, fwhm_l, mu, mix=0.5):
    """
    Linear combination of gaussian and loretzian instead of convolution
    Args:
       x: array of floats
       fwhm_g: FWHM of gaussian
       fwhm_l: FWHM of Lorentzian
       mu: Mean
       mix: ratio of gaus to lorentz, mix* gaus, (1-mix)*Lorentz
    """
    #pseudo_voigt = []
    if not (mix <=1):
        print('mix has to be smaller than 1.')
        return []
    gaus = gaussian(x, fwhm_g, mu)
    lorentz = lorentzian(x, fwhm_l, mu)
    return mix * gaus  + (1-mix)*lorentz