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


from __future__ import print_function
from __future__ import absolute_import
from six.moves import range
def plot_shapefun(pos, out, mode):
  """
  Creates a simple matplotlib image to show the shapefunctions given it's positions in the unit cell, the atoms's vertices in `ut` and the plotting mode

  :author: Philipp Ruessmann

  :param pos: positions of the centers of the cells
  :param verts: array of vertices of the shapefunction (outlines of shapes)
  :param mode: 'all' or 'single' determines whether or not all shapes are combined in a single figure or plotted as individual figures

  :returns ax: return the axis in which the plot was done (useful to pass to 'change_zoom' and 'zoom_in' functions of this module
  """
  import matplotlib.pyplot as plt
  from mpl_toolkits.mplot3d import Axes3D
  from numpy import array, shape

  if mode=='all':
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

  Natm = len(pos)

  for j in range(1,Natm+1):
    if mode=='single':
      fig = plt.figure()
      ax = fig.add_subplot(111, projection='3d')
    for i in list(out.keys()):
      if i[0]==j:
        linecolor = 'r'
      if j in [2,3,6,7]:
        linecolor='b'
      d = array(out[i])
      if len(shape(pos))>1 and len(pos)>2 and mode=='all':
        dx, dy, dz = pos[j-1,0], pos[j-1,1], pos[j-1,2] 
      else:
        dx, dy, dz = 0, 0, 0
      ax.plot(d[:,0]+dx,d[:,1]+dy,d[:,2]+dz,linecolor)

  if mode=='all':
    xy_scale = 1
    scale = 1
    ax.set_xlim(-scale*xy_scale,scale*xy_scale)
    ax.set_ylim(-scale*xy_scale,scale*xy_scale)
    ax.set_zlim(-scale,scale)

  return ax


def change_zoom(ax, zoom_range, center=[0,0,0]):
  """
  Change the zoom of a 3d plot

  :author: Philipp Ruessmann

  :param ax: axis which is zoomed
  :param zoom_range: range to which the image is zoomed, total range from center-zoom_range to center+zoom_range
  :param center: center of the zoomed region (optional, defaults to origin)
  """
  ax.set_xlim(center[0]-zoom_range,center[0]+zoom_range)
  ax.set_ylim(center[1]-zoom_range,center[1]+zoom_range)
  ax.set_zlim(center[2]-zoom_range,center[2]+zoom_range)


def zoom_in(ax, atm, pos, zoom_range=10):
  """
  Zoom into shapefun of a single atom

  :author: Philipp Ruessmann

  :param ax: axis in which shapefun plot is found
  :param atm: atom index whose shapefunction is zoomed
  :param pos: array of positions of centers of the shapes (needed to shift center of zommed region to correct atom
  :param zoom_range: range of the zoomed region (optional, defaults to 10)
  """
  center = pos[atm-1]
  print('zoom in to atom', atm, ':', center)
  change_zoom(ax, zoom_range, center)

