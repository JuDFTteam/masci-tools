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

from builtins import range
__version__ = 0.1


def read_shapefun(path='.'):
  """
  Read vertices of shapefunctions with 
  Zoom into shapefun of a single atom

  :author: Philipp Ruessmann

  :param path: path where voronoi output is found (optional, defaults to './')

  :returns pos: positions of the centers of the shapefunctions
  :returns out: dictionary of the vertices of the shapefunctions
  """
  from masci_tools.io.common_functions import search_string
  from numpy import array

  path += '/'

  # first read vertices file
  with open(path+'vertices.dat') as f:
    out = {}
    face, face_old = -1,-1
    for line in f:
      if '# serial:' in line[:9]:
        # skip line with serial number
        pass
      else:
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
          if tmp2!=[]:
            tmp2 = [float(i) for i in tmp2]
            tmp.append(tmp2)
          atm_old, face_old = atm,face
        if face_old!=face:
          out[atm,face] = tmp

  # then read positions from inputcard
  with open(path+'inputcard') as file:
    inp = file.readlines()
    # convert to uppercase
    for iline in range(len(inp)):
      inp[iline] = inp[iline].upper()
    # search number of atoms in inputcard
    iline = search_string('NAEZ', inp)
    if iline<0:
      iline = search_string('NATYP', inp)
      if iline==-1:
        raise ValueError("Error reading NAEZ or NATYP from inputcard.")
    naez = int(inp.pop(iline).split('=')[1].split()[0])

    # read rbasis positions
    iline = search_string('RBASIS', inp)
    if iline>=0:
      pos = []
      for iatom in range(naez):
        pos.append(inp.pop(iline+1))
      # finally convert to float arrays
      pos = array([[float(j) for j in i.split()[:3]] for i in pos])
    else:
      raise ValueError("Error reading RBASIS from inputcard.")

  return pos, out

