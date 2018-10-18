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


def read_shapefun(path='.'):
   """
   Read vertices of shapefunctions with 
   Zoom into shapefun of a single atom

   :author: Philipp Ruessmann

   :param path: path where voronoi output is found (optional, defaults to './')

   :returns pos: positions of the centers of the shapefunctions
   :returns out: dictionary of the vertices of the shapefunctions
   """
   path += '/'
   f = open(path+'vertices.dat')

   out = {}
   i_line = 1
   face, face_old = -1,-1
   for line in f:
	if 'representative' in line:
		atm = int(line.split()[-1])
		i_newat = 1
	elif 'Face' in line:
		i_newat = 0
		face = int(line.split()[-1])
		i_newface = 1
		tmp = []
	else:
		i_newface = 0
		tmp2 = line.split()
		if tmp2<>[]:
			tmp2 = [float(i) for i in tmp2]
			tmp.append(tmp2)
		atm_old, face_old = atm,face
		print i_line,atm,face
	if face_old<>face:
		out[atm,face] = tmp
	i_line += 1

   f.close()

   pos = loadtxt('positions.dat')

   return pos, out

