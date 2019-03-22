#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), 2018 Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.    #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools    #
# For further information on the license, see the LICENSE.txt file            #
#                                                                             #
###############################################################################

"""
:author: Philipp Ruessmann
:date: 2018-11-26

Plotting utility to visualize the output of the voronoi code.

Reads files 'vertices.dat' to extract the vertices of the shapefunctions and 'positions.dat' (done in 'read_shapefun' function)
Then creates a simple matplotlib image to show the shapefunctions using the 'plot_shapefun' function.
"""
from __future__ import print_function

from numpy import array, shape
from sys import argv
from masci_tools.io.kkr_read_shapefun_info import read_shapefun
from masci_tools.vis.kkr_plot_shapefun import plot_shapefun#, change_zoom, zoom_in
from matplotlib.pyplot import show


mode = 'all'      # 'single' or 'all'

if len(argv)>1:
  mode = argv[1]

if mode not in ['all','single']:
  print('ERROR: illegal mode chosen. Only all or single can be used')
  sys.exit()

pos, vertices = read_shapefun('.')
ax = plot_shapefun(pos, vertices, mode)

# this can be used to 
#if mode=='all':
  #change_zoom(ax, 1.5, center=[0,0,0])
  #zoom_in(ax, 3, pos, zoom_range=1)

show()


