#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
In this module are plot routines collected to create default plots out of certain
AiiDA ouput nodes from certain workflows with matplot lib. 

Comment: This makes plot_methods shorter to use for a Fleur, AiiDA user.
Be aware that requirements are the aiida-fleur plugin and aiida-fleur-basewf
Since we have a dependence to AiiDA here, it might be better to make a seperate repo, 
if this evolves.
"""
# TODO but allow to optional parse information for saving and title,
#  (that user can put pks or structure formulas in there)

__copyright__ = (u"Copyright (c), 2016-2017, Forschungszentrum Jülich GmbH, "
                 "IAS-1/PGI-1, Germany. All rights reserved.")
__license__ = "MIT license, see LICENSE.txt file"
__version__ = "0.27"
__contributors__ = "Jens Broeder"

import re
import os
import numpy as np
import matplotlib.pyplot as pp
from plot_methods import *
from aiida import load_dbenv, is_dbenv_loaded
if not is_dbenv_loaded():
    load_dbenv()
from aiida.orm import Code, DataFactory
from aiida.orm import load_node
from aiida.orm.calculation.work import WorkCalculation
from aiida.orm import Node
from pprint import pprint

RemoteData = DataFactory('remote')
StructureData = DataFactory('structure')
ParameterData = DataFactory('parameter')
FleurInpData = DataFactory('fleur.fleurinp')



###########################
## general plot routine  ##
###########################

def plot_fleur(node, show_dict = False):
    """
    This methods takes any AiiDa node and starts the standard visualisation for
    if it finds one
    """
    if isinstance(node, int):#pk
        node = load_node(node)
    
    if isinstance(node, str): #uuid
        node = load_node(node) #try
    
    if isinstance(node, Node):
        if isinstance(node, WorkCalculation):
            #print('workcalc')
            output_dict = node.get_outputs_dict()
            keys = output_dict.keys()
            #print keys
            for key in keys:
                if 'output_' in key:
                    if 'wc' in key:
                        node = output_dict.get(key)# we only visualize last output node
        if isinstance(node, ParameterData):
            #print('parameter')
            p_dict = node.get_dict()
            workflow_name = p_dict.get('workflow_name', None)
            
            if workflow_name == 'fleur_scf_wc':
                plot_fleur_scf_wc(node)
            elif workflow_name == 'fleur_eos_wc':
                plot_fleur_eos_wc(node)
            elif workflow_name == 'fleur_dos_wc':
                plot_fleur_dos_wc(node)
            elif workflow_name == 'fleur_band_wc':
                plot_fleur_band_wc(node)
            else:
                pprint(p_dict)
                show_dict = False # do not print twice
            if show_dict:
                pprint(p_dict)
        else:
            print('I do not know how to visualize this node: {}, type {}'.format(node, type(node)))
    else:
        print('The node provided: {}, type {} is not an AiiDA object'.format(node, type(node)))
    # check if AiiDa node
    #check what type of node
    # if workfunction, get certain output node
    #if parameterData, output node check if workflow name tag
    # if routine known plot,
    #else say I do not know

###########################
## general plot routine  ##
###########################

def plot_fleur_scf_wc(node):
    """
    This methods takes an AiiDA output parameter node from a scf workchain and
    plots number of iteration over distance and total energy
    """
    from aiida.tools.codespecific.fleur.plot_methods import plot_convergence_results

    #scf_wf = load_node(6513)
    output_d = node.get_dict()
    Total_energy = output_d.get('total_energy_all')
    distance_all = output_d.get('distance_charge_all')
    iteration_total = output_d.get('iterations_total')
    iteration = []
    for i in range(1, len(Total_energy)+1):
        iteration.append(iteration_total - len(Total_energy) + i)
    plot_convergence_results(distance_all, Total_energy, iteration)

def plot_fleur_dos_wc(node):
    """
    This methods takes an AiiDA output parameter node from a density of states
    workchain and plots a simple density of states
    """
    from aiida.tools.codespecific.fleur.plot_methods import plot_dos
    
    output_d = node.get_dict()
    path_to_dosfile = output_d.get('dosfile', None)
    print path_to_dosfile
    if path_to_dosfile:
        plot_dos(path_to_dosfile, only_total=False)
    else:
        print('Could not retrieve dos file path from output node')
        
def plot_fleur_eos_wc(node):
    """
    This methods takes an AiiDA output parameter node from a density of states
    workchain and plots a simple density of states
    """
    from aiida.tools.codespecific.fleur.plot_methods import plot_lattice_constant
    
    outpara = node.get_dict()
    Total_energy = outpara.get('total_energy')
    scaling = outpara.get('scaling')
    fit = outpara.get('fitresults')
    fit = outpara.get('fit')
    
    def parabola(x, a, b, c):
        return a*x**2 + b*x + c
    
    fit_y = []
    #fit_y = [parabola(scale2, fit[0], fit[1], fit[2]) for scale2 in scaling]
    plot_lattice_constant(Total_energy, scaling)#, fit_y)

def plot_fleur_band_wc(node):
    """
    This methods takes an AiiDA output parameter node from a band structure
    workchain and plots a simple band structure
    """
    from aiida.tools.codespecific.fleur.plot_methods import plot_bands
    
    output_d = node.get_dict()
    path_to_bands_file = output_d.get('bandfile', None)
    print(path_to_bands_file)
    kpath = output_d.get('kpath', {})#r"$\Gamma$": 0.00000, r"$H$" : 1.04590, 
    #    r"$N$" : 1.78546, r"$P$": 2.30841, r"$\Gamma1$" : 3.21419, r"$N1$" : 3.95375} )
    
    if path_to_bands_file:
        plot_bands(path_to_bands_file, kpath)
    else:
        print('Could not retrieve dos file path from output node')    

def plot_fleur_relax_wc(node):
    """
    This methods takes an AiiDA output parameter node from a relaxation
    workchain and plots some information about atom movements and forces
    """
    pass
    #from aiida.tools.codespecific.fleur.plot_methods import plot_relaxation_results
    
    #plot_relaxation_results
