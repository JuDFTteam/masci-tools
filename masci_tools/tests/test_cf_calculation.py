# -*- coding: utf-8 -*-
"""
Tests of the crystal field calculations
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pytest


def test_CFCalculation_txt_files():
    """
    Test of the CFCalculation reading the data from txt files
    """
    from masci_tools.tools.cf_calculation import CFCalculation, CFCoefficient

    #Make sure new script produces the same result as old one
    expected_results = [
        CFCoefficient(l=2,
                      m=0,
                      spin_up=-419.7891726292168,
                      spin_down=-414.7152560307904,
                      unit='K',
                      convention='Stevens'),
        CFCoefficient(l=4,
                      m=0,
                      spin_up=-35.92607948104669,
                      spin_down=-26.384951772020756,
                      unit='K',
                      convention='Stevens'),
        CFCoefficient(l=6, m=0, spin_up=6.522900740505054, spin_down=5.488104692050172, unit='K', convention='Stevens')
    ]

    cf = CFCalculation(reference_radius='cdn')
    cf.readPot('files/cf_calculation/VKS.2.0.dat',
               'files/cf_calculation/VKS.4.0.dat',
               'files/cf_calculation/VKS.6.0.dat',
               lm=[(2, 0), (4, 0), (6, 0)])
    cf.readCDN('files/cf_calculation/Nd.dat', header=3)
    cf.cdn['RMT'] = 3.138049652
    results = cf.performIntegration()

    assert results == expected_results


def test_CFCalculation_hdf_files():
    """
    Test of the CFCalculation using the hdf file produced by fleur
    """
    from masci_tools.tools.cf_calculation import CFCalculation, CFCoefficient

    expected_results = [
        CFCoefficient(l=2, m=0, spin_up=-571.68845386399, spin_down=-558.2336974657351, unit='K', convention='Stevens'),
        CFCoefficient(l=4,
                      m=0,
                      spin_up=-34.982539807305045,
                      spin_down=-21.850435868549834,
                      unit='K',
                      convention='Stevens'),
        CFCoefficient(l=6, m=0, spin_up=3.8503494779930776, spin_down=2.168215129491561, unit='K',
                      convention='Stevens'),
        CFCoefficient(l=6,
                      m=-6,
                      spin_up=110.50156137060345,
                      spin_down=85.58558990378205,
                      unit='K',
                      convention='Stevens'),
        CFCoefficient(l=6, m=6, spin_up=110.50156137060345, spin_down=85.58558990378205, unit='K', convention='Stevens')
    ]

    cf = CFCalculation()
    cf.readPot('files/cf_calculation/CFdata.hdf')
    cf.readCDN('files/cf_calculation/CFdata.hdf')
    results = cf.performIntegration()

    assert results == expected_results


def test_CFCalculation_hdf_files_wybourne_convention():
    """
    Test of the CFCalculation using the hdf file produced by fleur
    """
    from masci_tools.tools.cf_calculation import CFCalculation, CFCoefficient

    expected_results = [
        CFCoefficient(l=2,
                      m=0,
                      spin_up=(-1143.37690772798 + 0j),
                      spin_down=(-1116.4673949314702 + 0j),
                      unit='K',
                      convention='Wybourne'),
        CFCoefficient(l=4,
                      m=0,
                      spin_up=(-279.86031845844036 + 0j),
                      spin_down=(-174.80348694839867 + 0j),
                      unit='K',
                      convention='Wybourne'),
        CFCoefficient(l=6,
                      m=0,
                      spin_up=(61.60559164788924 + 0j),
                      spin_down=(34.69144207186498 + 0j),
                      unit='K',
                      convention='Wybourne'),
        CFCoefficient(l=6,
                      m=-6,
                      spin_up=(116.32750335918315 + 4.696327749935313e-06j),
                      spin_down=(90.09789430612014 + 3.6373963939901583e-06j),
                      unit='K',
                      convention='Wybourne'),
        CFCoefficient(l=6,
                      m=6,
                      spin_up=(116.32750335918315 - 4.696327749935313e-06j),
                      spin_down=(90.09789430612014 - 3.6373963939901583e-06j),
                      unit='K',
                      convention='Wybourne')
    ]

    cf = CFCalculation()
    cf.readPot('files/cf_calculation/CFdata.hdf')
    cf.readCDN('files/cf_calculation/CFdata.hdf')
    results = cf.performIntegration(convert=False)

    print(results)
    assert results == expected_results


@pytest.mark.mpl_image_compare(baseline_dir='files/cf_calculation/', filename='cf_calculation.png')
def test_plot_crystal_field_calculation():
    """
    Test of the plot illustrating the potential and charge density going into the calculation
    """
    from masci_tools.tools.cf_calculation import CFCalculation, plot_crystal_field_calculation

    cf = CFCalculation()
    cf.readPot('files/cf_calculation/CFdata.hdf')
    cf.readCDN('files/cf_calculation/CFdata.hdf')

    plt.gcf().clear()

    plot_crystal_field_calculation(cf, show=False)

    return plt.gcf()


@pytest.mark.mpl_image_compare(baseline_dir='files/cf_calculation/', filename='cf_potential.png')
def test_plot_crystal_field_potential():
    """
    Test of the plot illustraing the resulting crystal field potential
    """
    from masci_tools.tools.cf_calculation import CFCoefficient, plot_crystal_field_potential

    coeffs = [
        CFCoefficient(l=2,
                      m=0,
                      spin_up=(-1143.37690772798 + 0j),
                      spin_down=(-1116.4673949314702 + 0j),
                      unit='K',
                      convention='Wybourne'),
        CFCoefficient(l=4,
                      m=0,
                      spin_up=(-279.86031845844036 + 0j),
                      spin_down=(-174.80348694839867 + 0j),
                      unit='K',
                      convention='Wybourne'),
        CFCoefficient(l=6,
                      m=0,
                      spin_up=(61.60559164788924 + 0j),
                      spin_down=(34.69144207186498 + 0j),
                      unit='K',
                      convention='Wybourne'),
        CFCoefficient(l=6,
                      m=-6,
                      spin_up=(116.32750335918315 + 4.696327749935313e-06j),
                      spin_down=(90.09789430612014 + 3.6373963939901583e-06j),
                      unit='K',
                      convention='Wybourne'),
        CFCoefficient(l=6,
                      m=6,
                      spin_up=(116.32750335918315 - 4.696327749935313e-06j),
                      spin_down=(90.09789430612014 - 3.6373963939901583e-06j),
                      unit='K',
                      convention='Wybourne')
    ]

    plt.gcf().clear()
    plot_crystal_field_potential(coeffs, show=False)

    return plt.gcf()
