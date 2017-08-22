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

def plot_fleur(*args, **kwargs):
    """
    This methods takes any amount of AiiDA node and starts 
    the standard visualisation either as single or together visualisation.
    (if they are provided as list)
    i.e plot_fleur(123, [124,125], uuid, save=False)    
    
    Some general parameters of plot methods can be given as
    keyword arguments.
    param: save showed the plots be saved automaticaly
    
    """
    
    '''
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
    '''
    from plot_methods import set_plot_defaults

    save = False
    show_dict = False
    for key, val in kwargs.iteritems():    
        if key=='save':
           save=val
        if key=='show_dict':
            show_dict = val
    #    # the rest we ignore for know
    #Just call set plot defaults
    set_plot_defaults(**kwargs)   
     
    for arg in args:
        if isinstance(arg, list):
            # try plot together
            plot_fleur_mn(arg, save=save)                           
        else:
            print(arg)
            # plot alone
            plot_fleur_sn(arg, show_dict=show_dict, save=save)
            

def plot_fleur_sn(node, show_dict=False, save=False):
    """
    This methods takes any single AiiDA node and starts the standard visualisation for
    if it finds one
    """
    #show_dic = show_dic
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
            try:
                plotf = functions_dict[workflow_name]
            except KeyError:
                pass            
                if show_dict:
                    pprint(p_dict)
                return
            plotf(node)
            '''
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
            '''
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


def plot_fleur_mn(nodelist, save=False):
    """
    This methods takes any amount of AiiDA node as a list and starts 
    the standard visualisation for it, if it finds one.
    
    Some nodes types it tries to display together if it knows how to.
    and if they are given as a list.
    
    param: save showed the plots be saved automaticaly
    
    """
    ###
    # Things to plot together
    all_nodes = {}
    ###    
    
    if not isinstance(nodelist, list):
        print('The nodelist provided: {}, type {} is not a list. I abort'.format(nodelist, type(nodelist)))
        return None
    
    
    for node in nodelist:
        # first find out what we have then how to visualize
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
                cur_list = all_nodes.get(workflow_name, [])
                cur_list.append(node)                
                '''                
                if workflow_name == 'fleur_scf_wc':
                    cur_list = all_nodes.get(workflow_name, [])
                    cur_list.append(node)                    
                    #plot_fleur_scf_wc(node)
                elif workflow_name == 'fleur_eos_wc':
                    cur_list = all_nodes.get(workflow_name, [])
                    cur_list.append(node)                    
                    #plot_fleur_eos_wc(node)
                elif workflow_name == 'fleur_dos_wc':
                    cur_list = all_nodes.get(workflow_name, [])
                    cur_list.append(node)                  
                    #plot_fleur_dos_wc(node)
                elif workflow_name == 'fleur_band_wc':
                    cur_list = all_nodes.get(workflow_name, [])
                    cur_list.append(node)                    
                    #plot_fleur_band_wc(node)
                else:
                    pprint(p_dict)
                    show_dict = False # do not print twice
                
                if show_dict:
                    pprint(p_dict)
                '''
            else:
                print('I do not know how to visualize this node: {}, type {} from the nodelist {}'.format(node, type(node), nodelist))
        else:
            print('The node provided: {} of type {} in the nodelist {} is not an AiiDA object'.format(node, type(node), nodelist))    
  
    print(all_nodes)
    for node_key, nodelist in all_nodes.iteritems():
        try:
            plotf = functions_dict[node_key]
        except KeyError:
            pass
            continue
        plot_res = plotf(nodelist)



###########################
## general plot routine  ##
###########################

def plot_fleur_scf_wc(node):
    """
    This methods takes an AiiDA output parameter node or a list from a scf workchain and
    plots number of iteration over distance and total energy
    """
    from plot_methods import plot_convergence_results, plot_convergence_results_m
    
    if isinstance(node, list):
        if len(node) >= 2:
            return # TODO
        else:
            node=node[0]
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
    from plot_methods import plot_dos

    if isinstance(node, list):
        if len(node) > 2:
            return # TODO
        else:
            node=node[0]
    
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
    from plot_methods import plot_lattice_constant

    if isinstance(node, list):
        if len(node) > 2:
            return # TODO
        else:
            node=node[0]

    
    outpara = node.get_dict()
    Total_energy = outpara.get('total_energy')
    scaling = outpara.get('scaling')
    #fit = outpara.get('fitresults')
    #fit = outpara.get('fit')
    
    def parabola(x, a, b, c):
        return a*x**2 + b*x + c
    
    #fit_y = []
    #fit_y = [parabola(scale2, fit[0], fit[1], fit[2]) for scale2 in scaling]
    plot_lattice_constant(Total_energy, scaling)#, fit_y)

def plot_fleur_band_wc(node):
    """
    This methods takes an AiiDA output parameter node from a band structure
    workchain and plots a simple band structure
    """
    from plot_methods import plot_bands

    if isinstance(node, list):
        if len(node) > 2:
            return # TODO
        else:
            node=node[0]
    
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
    #from plot_methods import plot_relaxation_results
    
    #plot_relaxation_results


functions_dict = {
        'fleur_scf_wc' : plot_fleur_scf_wc,
        'fleur_eos_wc' : plot_fleur_eos_wc,
        'fleur_dos_wc' : plot_fleur_dos_wc,
        'fleur_band_wc' : plot_fleur_band_wc,

    }