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
    assert gf.energy_dependence(spin=1).dtype == float

    assert gf.energy_dependence(m=0, mp=0, spin=1).shape == (128,)  #(nz,2*l+1,2*l+1)
    assert gf.energy_dependence(m=0, mp=0, spin=1).dtype == float

    assert gf.energy_dependence(spin=1, both_contours=True).shape == (128, 5, 5, 2)  #(nz,2*l+1,2*l+1,2)
    assert gf.energy_dependence(spin=1, both_contours=True).dtype == complex

    assert isinstance(gf.trace_energy_dependence(spin=1), np.ndarray)
    assert gf.trace_energy_dependence(spin=1).shape == (128,)
    assert gf.trace_energy_dependence(spin=1).dtype == float


def test_greensfunction_radial(test_file):
    """
    Basic test of greensfunction
    """

    gf = GreensFunction.fromFile(test_file('fleur/greensf/greensf_radial.hdf'), l=2)

    elem = gf.element._replace(atomDiff=gf.element.atomDiff.tolist())
    assert elem == GreensfElement(l=2,
                                  lp=2,
                                  atomType=1,
                                  atomTypep=1,
                                  sphavg=False,
                                  onsite=True,
                                  kresolved=False,
                                  contour=1,
                                  nLO=1,
                                  atomDiff=[0., 0., 0.])

    assert not gf.mperp
    assert not gf.sphavg

    assert isinstance(gf.energy_dependence(spin=1), np.ndarray)
    assert gf.energy_dependence(spin=1).shape == (128, 5, 5)  #(nz,2*l+1,2*l+1)
    assert gf.energy_dependence(spin=1).dtype == float

    assert gf.energy_dependence(m=0, mp=0, spin=1).shape == (128,)  #(nz,2*l+1,2*l+1)
    assert gf.energy_dependence(m=0, mp=0, spin=1).dtype == float

    assert gf.energy_dependence(spin=1, both_contours=True).shape == (128, 5, 5, 2)  #(nz,2*l+1,2*l+1,2)
    assert gf.energy_dependence(spin=1, both_contours=True).dtype == complex

    assert isinstance(gf.trace_energy_dependence(spin=1), np.ndarray)
    assert gf.trace_energy_dependence(spin=1).shape == (128,)
    assert gf.trace_energy_dependence(spin=1).dtype == float


def test_list_elements(test_file):
    """
    Test of the listElements function
    """
    from masci_tools.tools.greensfunction import listElements

    elem = listElements(test_file('fleur/greensf/greensf_radial.hdf'))

    elem = [e._replace(atomDiff=e.atomDiff.tolist()) for e in elem]
    assert elem == [
        GreensfElement(l=1,
                       lp=1,
                       atomType=1,
                       atomTypep=1,
                       sphavg=False,
                       onsite=True,
                       kresolved=False,
                       contour=1,
                       nLO=2,
                       atomDiff=[0., 0., 0.]),
        GreensfElement(l=2,
                       lp=2,
                       atomType=1,
                       atomTypep=1,
                       sphavg=False,
                       onsite=True,
                       kresolved=False,
                       contour=1,
                       nLO=1,
                       atomDiff=[0., 0., 0.])
    ]


def test_print_elements(test_file, capsys):
    """
    Test of the listElements function
    """
    from masci_tools.tools.greensfunction import printElements, listElements

    elem = listElements(test_file('fleur/greensf/greensf_radial.hdf'))
    printElements(elem)

    out = capsys.readouterr().out
    assert out != ''
    assert '1      |      1|      1|      1|      1|   False|    True|         1|[ 0.00, 0.00, 0.00]|' in out
    assert '2      |      2|      2|      1|      1|   False|    True|         1|[ 0.00, 0.00, 0.00]|' in out
