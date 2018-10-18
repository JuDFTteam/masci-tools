#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), 2018 Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
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

Plotting utility to visualize the output of the voronoi code.

Reads files 'vertices.dat' to extract the vertices of the shapefunctions and 'positions.dat' (done in 'read_shapefun' function)

Then creates a simple matplotlib image to show the shapefunctions using the 'plot_shapefun' function.
"""

from numpy import array
import sys
from masci_tools.io.kkr_read_shapfun_info import read_shapefun
from masci_tools.vis.kkr_plot_shapfun import plot_shapefun


mode = 'all'      # 'single' or 'all'
if mode not in ['all','single']:
	print 'ERROR: illegal mode chosen. Only all or single can be used'
	sys.exit()

pos, vertices = read_shapefun('.')

ax = plot_shapefun(pos, vertices, mode)



