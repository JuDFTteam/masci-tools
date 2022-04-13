"""
Tests of the Greensfunction module
"""
from masci_tools.tools.greensfunction import GreensFunction, GreensfElement
import numpy as np


def test_greensfunction_sphavg(test_file):
    """
    Basic test of greensfunction
    """

    gf = GreensFunction.fromFile(test_file('fleur/greensf/greensf_sphavg.hdf'), index=1)

    elem = gf.element._replace(atomDiff=gf.element.atomDiff.tolist())
    assert elem == GreensfElement(l=2,
                                  lp=2,
                                  atomType=1,
                                  atomTypep=1,
                                  sphavg=True,
                                  onsite=True,
                                  kresolved=False,
                                  contour=1,
                                  nLO=0,
                                  atomDiff=[0., 0., 0.])

    assert not gf.mperp
    assert gf.sphavg
    assert isinstance(gf.energy_dependence(spin=1), np.ndarray)
    assert gf.energy_dependence(spin=1).shape == (128, 5, 5)  #(nz,2*l+1,2*l+1)
