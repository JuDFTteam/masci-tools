# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools.   #
# For further information on the license, see the LICENSE.txt file.           #
# For further information please visit http://judft.de/.                      #
#                                                                             #
###############################################################################
"""
Tools for the impurity caluclation plugin and its workflows
"""
from sys import version_info
if version_info[0] >= 3:

    def raw_input(msg):
        return eval(eval(input(msg)))


__copyright__ = (u'Copyright (c), 2018, Forschungszentrum Jülich GmbH,' 'IAS-1/PGI-1, Germany. All rights reserved.')
__license__ = 'MIT license, see LICENSE.txt file'
__version__ = '0.3'
__contributors__ = u'Philipp Rüßmann'


class modify_potential(object):
    """
    Class for old modify potential script, ported from modify_potential script, initially by D. Bauer
    """

    def _check_potstart(self, str1, mode='pot', shape_ver='new'):
        if mode == 'shape':
            if shape_ver == 'new':
                check1 = 'Shape number' in str1
            else:
                check1 = (len(str1) == 11)
        else:
            check1 = 'exc:' in str1
        return check1

    def _read_input(self, filepath):
        #print(filepath)
        with open(filepath) as file:
            data = file.readlines()

        if 'shapefun' in filepath:
            mode = 'shape'
        else:
            mode = 'pot'

        #print(mode, len(data))

        # read file
        index1 = []
        index2 = []
        for i in range(len(data)):
            if self._check_potstart(data[i], mode=mode):
                index1.append(i)
                if len(index1) > 1:
                    index2.append(i - 1)
        index2.append(i)

        # read shapefun if old style is used
        if mode == 'shape' and len(index1) < 1:
            index1 = []
            index2 = []
            for i in range(len(data)):
                if self._check_potstart(data[i], mode=mode, shape_ver='old'):
                    index1.append(i)
                if len(index1) > 1:
                    index2.append(i - 1)
                index2.append(i)
        """
        print(index1)
        print(index2)

        print('Potential file read')
        print('found %i potentials in file'%len(index1))
        print('')
        """

        return index1, index2, data

    def shapefun_from_scoef(self, scoefpath, shapefun_path, atom2shapes, shapefun_new):
        """
        Read shapefun and create impurity shapefun using scoef info and shapes array

        :param scoefpath: absolute path to scoef file
        :param shapefun_path: absolute path to input shapefun file
        :param shapes: shapes array for mapping between atom index and shapefunction index
        :param shapefun_new: absolute path to output shapefun file to which the new shapefunction will be written
        """
        index1, index2, data = self._read_input(shapefun_path)

        order = list(range(len(index1)))

        natomtemp = int(open(scoefpath).readlines()[0])
        filedata = open(scoefpath).readlines()[1:natomtemp + 1]
        listnew = []
        for line in filedata:
            if len(line.split()) > 1:
                listnew.append(atom2shapes[int(line.split()[3]) - 1] - 1)
        order = listnew

        datanew = []
        for i in range(len(order)):
            for ii in range(index1[order[i]], index2[order[i]] + 1):
                datanew.append(data[ii])

        # add header to shapefun_new
        tmp = datanew
        datanew = []
        datanew.append('   %i\n' % (len(order)))
        datanew.append('  1.000000000000E+00\n')
        datanew += tmp
        with open(shapefun_new, 'w') as f:
            f.writelines(datanew)

    def neworder_potential(self, potfile_in, potfile_out, neworder, potfile_2=None, replace_from_pot2=None):
        """
        Read potential file and new potential using a list describing the order of the new potential.
        If a second potential is given as input together with an index list, then the corresponding of
        the output potential are overwritten with positions from the second input potential.

        :param potfile_in: absolute path to input potential
        :type potfile_in: str
        :param potfile_out: absolute path to output potential
        :type potfile_out: str
        :param neworder: list after which output potential is constructed from input potential
        :type neworder: list
        :param potfile_2: optional, absolute path to second potential file if
            positions in new list of potentials shall be replaced by positions of
            second potential, requires *replace_from_pot* to be given as well
        :type potfile_2: str
        :param replace_from_pot: optional, list containing tuples of (position
            in newlist that is to be replaced, position in pot2 with which position
            is replaced)
        :type replace_from_pot: list

        :usage:
            1. modify_potential().neworder_potential(<path_to_input_pot>, <path_to_output_pot>, [])
        """
        from numpy import array, shape

        index1, index2, data = self._read_input(potfile_in)

        if potfile_2 is not None:
            index12, index22, data2 = self._read_input(potfile_2)
            # check if also replace_from_pot2 is given correctly
            if replace_from_pot2 is None:
                raise ValueError('replace_from_pot2 not given')
            else:
                replace_from_pot2 = array(replace_from_pot2)
                if shape(replace_from_pot2)[1] != 2:
                    raise ValueError('replace_from_pot2 needs to be a 2D array!')
        else:
            if replace_from_pot2 is not None:
                raise ValueError('replace_from_pot2 given but potfile_2 not given')

        # set order in which potential file is written
        # ensure that numbers are integers:
        order = [int(i) for i in neworder]

        datanew = []
        for i in range(len(order)):
            # check if new position is replaced with position from old pot
            if replace_from_pot2 is not None and i in replace_from_pot2[:, 0]:
                replace_index = replace_from_pot2[replace_from_pot2[:, 0] == i][0][1]
                for ii in range(index12[replace_index], index22[replace_index] + 1):
                    datanew.append(data2[ii])
            else:  # otherwise take new potntial according to input list
                for ii in range(index1[order[i]], index2[order[i]] + 1):
                    datanew.append(data[ii])

        # write out new potential
        with open(potfile_out, 'w') as f:
            f.writelines(datanew)
