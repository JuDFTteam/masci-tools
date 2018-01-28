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
            #print(arg)
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
            output_dict = node.get_outputs_dict()
            keys = output_dict.keys()
            for key in keys:
                if 'output_' in key:
                    if 'wc' in key or 'wf' in key:
                        if 'para' in key: # currently only parameter nodes 
                            # TODO more general...: get all output node, plotmethod has to deal with them...
                            node = output_dict.get(key)# we only visualize last output node
        if isinstance(node, ParameterData):
            p_dict = node.get_dict()
            workflow_name = p_dict.get('workflow_name', None)
            try:
                plotf = functions_dict[workflow_name]
            except KeyError:
                print('Sorry, I do not know how to visualize this workflow: {}, node {}. Please implement me in plot_fleur_aiida!'.format(workflow_name, node))            
                if show_dict:
                    pprint(p_dict)
                return
            plotf(node)
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
    
    node_labels = []
    for node in nodelist:
        # first find out what we have then how to visualize
        if isinstance(node, int):#pk
            node = load_node(node)
        if isinstance(node, str): #uuid
            node = load_node(node) #try
            
        if isinstance(node, Node):
            node_labels.append(node.label)
            if isinstance(node, WorkCalculation):
                output_dict = node.get_outputs_dict()
                keys = output_dict.keys()
                for key in keys:
                    if 'output_' in key:
                        if 'wc' in key or 'wf' in key:
                            node = output_dict.get(key)# we only visualize last output node
            if isinstance(node, ParameterData):
                p_dict = node.get_dict()
                workflow_name = p_dict.get('workflow_name', None)
                cur_list = all_nodes.get(workflow_name, [])
                cur_list.append(node)  
                all_nodes[workflow_name] = cur_list
            else:
                print('I do not know how to visualize this node: {}, type {} from the nodelist {}'.format(node, type(node), nodelist))
        else:
            print('The node provided: {} of type {} in the nodelist {} is not an AiiDA object'.format(node, type(node), nodelist))    
  
    #print(all_nodes)
    for node_key, nodelist in all_nodes.iteritems():
        try:
            plotf = functions_dict[node_key]
        except KeyError:
            print('Sorry, I do not know how to visualize these nodes (multiplot): {} {}'.format(node_key, nodelist))            
            continue
        plot_res = plotf(nodelist, labels=node_labels)



###########################
## general plot routine  ##
###########################

def plot_fleur_scf_wc(nodes, labels=[]):
    """
    This methods takes an AiiDA output parameter node or a list from a scf workchain and
    plots number of iteration over distance and total energy
    """
    from plot_methods import plot_convergence_results, plot_convergence_results_m
    
    if isinstance(nodes, list):
        if len(nodes) >= 2:
            #return # TODO
            pass
        else:
            nodes=[nodes[0]]
    #scf_wf = load_node(6513)

    iterations = []
    distance_all_n = []
    total_energy_n =[]
    
    for node in nodes:
        iteration = []
        output_d = node.get_dict()
        total_energy = output_d.get('total_energy_all')
        distance_all = output_d.get('distance_charge_all')
        iteration_total = output_d.get('iterations_total')        
        for i in range(1, len(total_energy)+1):
            iteration.append(iteration_total - len(total_energy) + i)
        iterations.append(iteration)
        distance_all_n.append(distance_all)
        total_energy_n.append(total_energy)
    #plot_convergence_results(distance_all, total_energy, iteration)
    if labels:
        plot_convergence_results_m(distance_all_n, total_energy_n, iterations, plot_labels=labels)        
    else:
        plot_convergence_results_m(distance_all_n, total_energy_n, iterations)

def plot_fleur_dos_wc(node, labels=[]):
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
        
def plot_fleur_eos_wc(node, labels=[]):
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
    
    #def parabola(x, a, b, c):
    #    return a*x**2 + b*x + c
    
    #fit_y = []
    #fit_y = [parabola(scale2, fit[0], fit[1], fit[2]) for scale2 in scaling]
    plot_lattice_constant(Total_energy, scaling)#, fit_y)

def plot_fleur_band_wc(node, labels=[]):
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

def plot_fleur_relax_wc(node, labels=[]):
    """
    This methods takes an AiiDA output parameter node from a relaxation
    workchain and plots some information about atom movements and forces
    """
    pass
    #from plot_methods import plot_relaxation_results
    
    #plot_relaxation_results

def plot_fleur_corehole_wc(nodes, labels=[]):
    """
    This methods takes AiiDA output parameter nodes from a corehole
    workchain and plots some information about Binding energies
    """    
    pass

def plot_fleur_initial_cls_wc(nodes, labels=[]):
    """
    This methods takes AiiDA output parameter nodes from a initial_cls 
    workchain and plots some information about corelevel shifts.
    (Spectra)
    """     
    
    
    pass

def plot_spectra(wc_nodes, title='', factors=[], energy_range=[100, 120], fwhm_g=0.6, fwhm_l=0.1, energy_grid=0.2, peakfunction='voigt', linetyp_spec='o-', warn_ref=False, **kwargs):
    """
    This function takes a list of workflow/result nodes/pks/uuids an plots the combined spectrum in a certain energy range.
    It has all kwargs of plot_corelevel_spectra, which is used below.
    
    It checks what nodes are present, extracts the results from them and the number of atoms with that result. 
    For older result node versions it gets parses the out.xml file again.
    It converts the core-level shifts to Bindingenergies with all the given experimental Bindingenergies ('exp_bindingenergies') from the NIST database.
    Then it plots the data with 'plot_corelevel_spectra'
    Comment: For now only inital shift nodes, TODO: Final state Binding energies
    
    :param wc_nodes: 
    :prints : Warnings a
    :return corelevelshifts: it returns the results it plots
    # TODO if several compounds are plottet together all references energies have to be extracted, not only the last ones...
    """
    from aiida.orm import DataFactory, Node, load_node
    from aiida.orm.calculation.work import WorkCalculation
    from aiida_fleur.tools.element_econfig_list import exp_bindingenergies
    from aiida_fleur.tools.extract_corelevels import extract_corelevels
    from plot_methods import plot_corelevel_spectra
    from aiida_fleur.tools.extract_corelevels import clshifts_to_be
    from aiida_fleur.workflows.initial_cls import fleur_initial_cls_wc
    from aiida_fleur.workflows.initial_cls import extract_results
    from aiida_fleur.tools.extract_corelevels import clshifts_to_be
    from aiida_fleur.tools.element_econfig_list import exp_bindingenergies, atomic_numbers
    from aiida_fleur.tools.element_econfig_list import get_coreconfig, get_spin_econfig, convert_fleur_config_to_econfig
    from aiida_fleur.tools.ParameterData_util import dict_merger
    from pprint import pprint
    
    ParameterData = DataFactory('parameter')
    htr_to_ev = 27.21138602
    # TODO: How to group certain contributions?
    # TODO: allow also scf_ouput nodes, parse them ... you cannot get shifts
    # TODO: how to add Elementals? only with 
    
    # TODO: Check what kind of nodes given
    # If initital -> calculate binding energies from experiments, if no reference found, skip, but warn..
    # If final use absolute results, currently only initial state
    
    # get Be from corelevel shifts
    # multiply atomtypes with number of electrons and given factors (for mixtures, or wirkungsquerschnitte)
    wc_node = None
    
    if not isinstance(wc_nodes, list):
        wc_nodes = [wc_nodes]
    bindingenergies_all = {}
    natomtypes_dict_all = {}
    bindingenergies_ref_all = {}
    compound_info = []
    for ncount, node in enumerate(wc_nodes): # each node is the wc_node or result node/uuid/pk for a compound
        if isinstance(node, int):#pk
            node = load_node(node)
        if isinstance(node, str): #uuid
            node = load_node(node) #try
        if not isinstance(node, Node):
            print('WARNING: node: {} is not a node, or could not load..., I skip this one'.format(node))
            continue
            
        if isinstance(node, WorkCalculation):
            wc_node = node
            node = node.get_outputs_dict()['output_inital_cls_wc_para']
            # try if fail continue, print warning
        if not isinstance(node, ParameterData):
            print('the node {} is not a result node of an initial_cls workchain'.format(node))
            continue
        else:
            inputsnodes = node.get_inputs_dict()
            wc_node = inputsnodes.get('output_inital_cls_wc_para', None)
            if not wc_node:
                break
        
        # check version of workflow if older then 0.2.0 we have to parse the files...        
        wres_dict = node.get_dict()
        wc_version = wres_dict.get('workflow_version','0.0.0')
        cls_units = wres_dict.get('corelevelshifts_units', 'htr')
        if cls_units == 'htr' or cls_units == 'Htr':
            convert_to_eV = True
        version = int(wc_version.replace('.',''))
        if not wres_dict.get('succesfull', False):
            print('WARNING: outputnode {}, states that workchain was not successfull, check the results!'.format(node))
        
        if version <= 20:
            # Some atomtype information is not saved yet, therefore we have to parse the files with the newest parser version
            # to get theses. However the corelevel shifts we will always retrieve from the output node..
            outputs = wc_node.get_outputs()
            for output in outputs:# we assume the first scf we find is the 
                if isinstance(output, WorkCalculation):
                    outdict = output.get_outputs_dict()
                    outscf_para = outdict.get('output_scf_wc_para', None)
                    if outscf_para:
                        total_energy, fermi_energies, bandgaps, all_atomtypes, all_corelevels, log = extract_results([output])
                        break # we only use the first one (main compound per default) # TODO always the case? 
        else: # use only information from output nodes/Database, do not use any files
            all_atomtypes = wres_dict.get('atomtypes', {})         
        
        coreshifts = wres_dict.get('corelevelshifts', {})
        #pprint(all_atomtypes)
        
        compound_label = all_atomtypes.keys()[0]
        compound_info.append(compound_label)
        print('Material: {}'.format(compound_label))
        # Now we need to convert/build the right format for plot_corelevel_spectra        
        # For each atomtype in compound, get full coresetup, number of atoms
        # the multiplication by the number of electrons is done in the plot routine
        # write the corelevel names in the dictionary
        natomtypes_dict = {}
        coreshifts_new = {}
        coreconfig_full_list = {}
        #compound_info_dict = {}
        
        for atomtype in all_atomtypes.values()[0]:
            elem = atomtype.get('element')
            coreconfig_short = atomtype.get('coreconfig')
            if not coreconfig_short:# we assume the default...
                coreconfig_short = get_coreconfig(elem)
                print('WARNING: no coreconfig parsed from out.xml, using default coreconfig...')
            coreconfig_full = get_spin_econfig(convert_fleur_config_to_econfig(coreconfig_short))
            natoms = atomtype.get('natoms')
            natomtypes_dict[elem] = natomtypes_dict.get(elem, [])
            multiplier = factors[ncount:ncount+1]
            if multiplier:
                multiplier = multiplier[0]
            else:
                multiplier = 1
            natomtypes_dict[elem].append(natoms*multiplier)
            coreconfig_full_list[elem] = coreconfig_full_list.get(elem, [])
            coreconfig_full_list[elem].append(coreconfig_full.split())
        
        for element, ecorelevels in coreshifts.iteritems():
            #Check if number right
            #if not len(ecorelevels) == natomtype_element
            # continue Warning
            coreconfig_full_list_elm = coreconfig_full_list[element]
            coreshifts_new_element = coreshifts_new.get(element, {})
            for j,atomtype_cls in enumerate(ecorelevels):
                type_coreconfig = coreconfig_full_list_elm[j]
                if not len(atomtype_cls) == len(type_coreconfig):
                    print('WARNING: Number of corelevels found {} is not equal to number of '
                          'corelevels in coreconfig {}... node {}. The coreconfig is {}, atomtypes: {}'
                          ''.format(len(atomtype_cls), len(type_coreconfig), node, type_coreconfig, atomtype_cls))
                    
                for i,corelevel in enumerate(atomtype_cls):
                    coreshifts_new_element[type_coreconfig[i]] = coreshifts_new_element.get(type_coreconfig[i], [])
                    if convert_to_eV: # we move von negative BE to Postive BE, that is the -1
                        coreshifts_new_element[type_coreconfig[i]].append(corelevel*htr_to_ev*-1)   
                    else:
                        coreshifts_new_element[type_coreconfig[i]].append(corelevel*-1)  
            #compound_info_dict[element] = [0, len(ecorelevels)]
            
            coreshifts_new[element] = coreshifts_new_element
        # Convert the corelevelshifts with experimental references to absolut Bindingenergies 
        symbols = coreshifts.keys()
        bindingenergies_ref = {}
        for symbol in symbols:
            koordinationnumber = atomic_numbers[symbol]
            bindingenergies_ref[symbol] = exp_bindingenergies.get(koordinationnumber, {})['binding_energy']
        #pprint(bindingenergies_ref)
        bindingenergies = clshifts_to_be(coreshifts_new, bindingenergies_ref, warn=warn_ref)        
        
        # merge the contribution of the compound into a total dictionary with all compounds and apply factors. 
        # optional mark the experiemntal references
        bindingenergies_all = dict_merger(bindingenergies_all, bindingenergies)
        natomtypes_dict_all = dict_merger(natomtypes_dict_all, natomtypes_dict)
        bindingenergies_ref_all = dict_merger(bindingenergies_ref_all, bindingenergies_ref)
        #compound_info[compound_label] = compound_info_dict#len(natomtypes_dict)
        # compound info : { 'Be': [BeTi, BeTi, Be12Ti, Be12Ti, Be12Ti], 'Ti' : [BeTi, Be12Ti]}
        # might work, because of dict merger
    #pprint(compound_info)
    #pprint(natomtypes_dict_all)
    pprint(bindingenergies_all)
    # plot the results        
    [xdata_spec, ydata_spec, ydata_single_all , xdata_all, ydata_all, xdatalabel] = plot_corelevel_spectra(bindingenergies_all, natomtypes_dict_all, exp_references=bindingenergies_ref_all, #compound_info=compound_info, 
                           energy_range=energy_range, title=title, fwhm_g=fwhm_g, fwhm_l=fwhm_l, 
                           energy_grid=energy_grid, peakfunction=peakfunction, linetyp_spec=linetyp_spec, **kwargs)

    bindingenergies_ref_all_compressed = clear_dict_empty_lists(bindingenergies_ref_all)
        
    return natomtypes_dict_all, bindingenergies_all, bindingenergies_ref_all_compressed, xdata_spec, ydata_spec, ydata_single_all , xdata_all, ydata_all, compound_info, xdatalabel


functions_dict = {
        'fleur_scf_wc' : plot_fleur_scf_wc,
        'fleur_eos_wc' : plot_fleur_eos_wc,
        'fleur_dos_wc' : plot_fleur_dos_wc,
        'fleur_band_wc' : plot_fleur_band_wc,
        'fleur_corehole_wc' : plot_fleur_corehole_wc,
        'fleur_initial_cls_wc' : plot_fleur_initial_cls_wc

    }
    
def clear_dict_empty_lists(to_clear_dict):
    '''
    Removes entries from a nested dictionary which are empty lists.
    
    param to_clear_dict dict: python dictionary which should be 'compressed'
    return new_dict dict: compressed python dict version of to_clear_dict
    
    Hints: rekursive
    '''
    new_dict = {}
    if not to_clear_dict:
        return new_dict

    if not isinstance(to_clear_dict, dict):
        return to_clear_dict

    for key, value in to_clear_dict.iteritems():
        if value:
            new_value = clear_dict_empty_lists(value)
            if new_value:
                new_dict[key] = new_value
    return new_dict