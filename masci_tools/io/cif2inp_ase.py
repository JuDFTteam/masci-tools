#!/usr/bin/python3
import sys
import ase.io
import numpy as np
cifFilename=sys.argv[1]
structure=ase.io.read(cifFilename)

structureFormula=structure.get_chemical_formula()
inpFilename='inp_'+structureFormula

Binv =  np.linalg.inv(structure.cell)
frac_coordinates = structure.arrays['positions'].dot(Binv)

with open(inpFilename,"w+") as f:
    natoms=len(structure.arrays['numbers'])
    f.write(structureFormula+"\r\n")
    f.write("&input film=F /\r\n")
    for i in range(3):
        f.write(' '.join(map("{:.4f}".format,structure.cell[i]))+"\r\n")
    f.write("1.8897    !lattice const scaled as(1.0*bohr)\r\n1.0000 1.0000 1.0000    !scaling\r\n\r\n")
    f.write(str(natoms)+"\r\n")
    for i in range(natoms):
        f.write(str(structure.arrays['numbers'][i])+" "
                +" ".join(map("{:.6f}".format, frac_coordinates[i]))+"\r\n")
    f.write("\r\n")
        
