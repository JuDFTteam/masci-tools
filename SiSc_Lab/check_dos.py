#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 17:27:59 2019

@author: christianpartmann
"""

import numpy as np
from matplotlib import pyplot as plt

num_groups = 2
skip = 5
a = np.genfromtxt("Data/DOS_Co.1").T



E = a[0]
totdos = a[1]
interst = a[2]
vac1 = a[3]
vac2 = a[4]

tot_per_atomg = a[skip:skip+num_groups]



plt.figure()
plt.plot(sum(a[skip:skip+num_groups]), E)



plt.plot(totdos-interst, E)

