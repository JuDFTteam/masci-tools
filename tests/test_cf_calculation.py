"""
Tests of the crystal field calculations
"""
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pytest


def test_CFCalculation_txt_files_deprecated(test_file):
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
    with pytest.deprecated_call():
        cf.readPot(test_file('cf_calculation/VKS.2.0.dat'),
                   test_file('cf_calculation/VKS.4.0.dat'),
                   test_file('cf_calculation/VKS.6.0.dat'),
                   lm=[(2, 0), (4, 0), (6, 0)])
    with pytest.deprecated_call():
        cf.readCDN(test_file('cf_calculation/Nd.dat'), header=3)
    cf.cdn['RMT'] = 3.138049652
    with pytest.deprecated_call():
        results = cf.performIntegration()

    assert results == expected_results


def test_CFCalculation_hdf_files(test_file):
    """
    Test of the CFCalculation using the hdf file produced by fleur
    """
    from masci_tools.tools.cf_calculation import CFCalculation, CFCoefficient

    expected_results = [
        CFCoefficient(l=2,
                      m=0,
                      spin_up=-114.39275809609971,
                      spin_down=-90.09580885564438,
                      unit='K',
                      convention='Stevens'),
        CFCoefficient(l=4,
                      m=0,
                      spin_up=-21.39894218147612,
                      spin_down=-37.31408959854193,
                      unit='K',
                      convention='Stevens'),
        CFCoefficient(l=6, m=0, spin_up=3.492132631169345, spin_down=3.0713512716362596, unit='K',
                      convention='Stevens'),
        CFCoefficient(l=6,
                      m=-6,
                      spin_up=114.10925799683953,
                      spin_down=90.17800570239386,
                      unit='K',
                      convention='Stevens'),
        CFCoefficient(l=6, m=6, spin_up=114.10925799683953, spin_down=90.17800570239386, unit='K', convention='Stevens')
    ]

    cf = CFCalculation()
    cf.read_potential(test_file('cf_calculation/CFdata.hdf'))
    cf.read_charge_density(test_file('cf_calculation/CFdata.hdf'))
    results = cf.get_coefficients()

    assert results == expected_results


def test_CFCalculation_hdf_files_deprecated(test_file):
    """
    Test of the CFCalculation using the hdf file produced by fleur
    """
    from masci_tools.tools.cf_calculation import CFCalculation, CFCoefficient

    expected_results = [
        CFCoefficient(l=2,
                      m=0,
                      spin_up=-114.39275809609971,
                      spin_down=-90.09580885564438,
                      unit='K',
                      convention='Stevens'),
        CFCoefficient(l=4,
                      m=0,
                      spin_up=-21.39894218147612,
                      spin_down=-37.31408959854193,
                      unit='K',
                      convention='Stevens'),
        CFCoefficient(l=6, m=0, spin_up=3.492132631169345, spin_down=3.0713512716362596, unit='K',
                      convention='Stevens'),
        CFCoefficient(l=6,
                      m=-6,
                      spin_up=114.10925799683953,
                      spin_down=90.17800570239386,
                      unit='K',
                      convention='Stevens'),
        CFCoefficient(l=6, m=6, spin_up=114.10925799683953, spin_down=90.17800570239386, unit='K', convention='Stevens')
    ]

    cf = CFCalculation()
    with pytest.deprecated_call():
        cf.readPot(test_file('cf_calculation/CFdata.hdf'))
        cf.readCDN(test_file('cf_calculation/CFdata.hdf'))
        results = cf.performIntegration()

    assert results == expected_results


def test_CFCalculation_hdf_files_wybourne_convention(test_file):
    """
    Test of the CFCalculation using the hdf file produced by fleur
    """
    from masci_tools.tools.cf_calculation import CFCalculation, CFCoefficient

    expected_results = [
        CFCoefficient(l=2,
                      m=0,
                      spin_up=(-228.78551619219942 + 0j),
                      spin_down=(-180.19161771128876 + 0j),
                      unit='K',
                      convention='Wybourne'),
        CFCoefficient(l=4,
                      m=0,
                      spin_up=(-171.19153745180895 + 0j),
                      spin_down=(-298.51271678833547 + 0j),
                      unit='K',
                      convention='Wybourne'),
        CFCoefficient(l=6,
                      m=0,
                      spin_up=(55.87412209870952 + 0j),
                      spin_down=(49.141620346180154 + 0j),
                      unit='K',
                      convention='Wybourne'),
        CFCoefficient(l=6,
                      m=-6,
                      spin_up=(120.12540753539542 + 2.1944180858399073e-08j),
                      spin_down=(94.9324347199708 + 1.7341997497152095e-08j),
                      unit='K',
                      convention='Wybourne'),
        CFCoefficient(l=6,
                      m=6,
                      spin_up=(120.12540753539542 - 2.1944180858399073e-08j),
                      spin_down=(94.9324347199708 - 1.7341997497152095e-08j),
                      unit='K',
                      convention='Wybourne')
    ]

    cf = CFCalculation()
    cf.read_potential(test_file('cf_calculation/CFdata.hdf'))
    cf.read_charge_density(test_file('cf_calculation/CFdata.hdf'))
    results = cf.get_coefficients(convention='Wybourne')

    assert results == expected_results


def test_CFCalculation_hdf_files_wybourne_convention_deprecated(test_file):
    """
    Test of the CFCalculation using the hdf file produced by fleur
    """
    from masci_tools.tools.cf_calculation import CFCalculation, CFCoefficient

    expected_results = [
        CFCoefficient(l=2,
                      m=0,
                      spin_up=(-228.78551619219942 + 0j),
                      spin_down=(-180.19161771128876 + 0j),
                      unit='K',
                      convention='Wybourne'),
        CFCoefficient(l=4,
                      m=0,
                      spin_up=(-171.19153745180895 + 0j),
                      spin_down=(-298.51271678833547 + 0j),
                      unit='K',
                      convention='Wybourne'),
        CFCoefficient(l=6,
                      m=0,
                      spin_up=(55.87412209870952 + 0j),
                      spin_down=(49.141620346180154 + 0j),
                      unit='K',
                      convention='Wybourne'),
        CFCoefficient(l=6,
                      m=-6,
                      spin_up=(120.12540753539542 + 2.1944180858399073e-08j),
                      spin_down=(94.9324347199708 + 1.7341997497152095e-08j),
                      unit='K',
                      convention='Wybourne'),
        CFCoefficient(l=6,
                      m=6,
                      spin_up=(120.12540753539542 - 2.1944180858399073e-08j),
                      spin_down=(94.9324347199708 - 1.7341997497152095e-08j),
                      unit='K',
                      convention='Wybourne')
    ]

    with pytest.deprecated_call():
        cf = CFCalculation()
        cf.readPot(test_file('cf_calculation/CFdata.hdf'))
        cf.readCDN(test_file('cf_calculation/CFdata.hdf'))
        results = cf.performIntegration(convert=False)

    assert results == expected_results


@pytest.mark.mpl_image_compare(baseline_dir='files/cf_calculation/', filename='cf_calculation.png')
def test_plot_crystal_field_calculation(test_file):
    """
    Test of the plot illustrating the potential and charge density going into the calculation
    """
    from masci_tools.tools.cf_calculation import CFCalculation, plot_crystal_field_calculation

    cf = CFCalculation()
    cf.read_potential(test_file('cf_calculation/CFdata.hdf'))
    cf.read_charge_density(test_file('cf_calculation/CFdata.hdf'))

    plt.gcf().clear()

    plot_crystal_field_calculation(cf, show=False)

    return plt.gcf()


@pytest.mark.mpl_image_compare(baseline_dir='files/cf_calculation/', filename='cf_calculation_only_potential.png')
def test_plot_crystal_field_calculation_only_potential(test_file):
    """
    Test of the plot illustrating the potential and charge density going into the calculation
    """
    from masci_tools.tools.cf_calculation import CFCalculation, plot_crystal_field_calculation

    cf = CFCalculation()
    cf.read_potential(test_file('cf_calculation/CFdata.hdf'))
    cf.read_charge_density(test_file('cf_calculation/CFdata.hdf'))

    plt.gcf().clear()

    plot_crystal_field_calculation(cf, show=False, density=False)

    return plt.gcf()


@pytest.mark.mpl_image_compare(baseline_dir='files/cf_calculation/', filename='cf_calculation_only_density.png')
def test_plot_crystal_field_calculation_only_density(test_file):
    """
    Test of the plot illustrating the potential and charge density going into the calculation
    """
    from masci_tools.tools.cf_calculation import CFCalculation, plot_crystal_field_calculation

    cf = CFCalculation()
    cf.read_potential(test_file('cf_calculation/CFdata.hdf'))
    cf.read_charge_density(test_file('cf_calculation/CFdata.hdf'))

    plt.gcf().clear()

    plot_crystal_field_calculation(cf, show=False, potential=False)

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
