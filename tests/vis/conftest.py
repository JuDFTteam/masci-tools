"""
Fixtures for testing visualzation functions
"""
import pytest
import numpy as np

@pytest.fixture
def convergence_plot_data():
    """
    Fixture returning sample data for convergence plots
    """

    def _convergence_plot_data(n):
        """
        Return n sets of distance and energy convergence data
        """
        if n == 1:

            energies = [
                -69269.46134019217, -69269.42108466873, -69269.35509388152, -69269.62486438647, -69269.51102655893,
                -69269.48862754989, -69269.48874847183, -69269.48459145911, -69269.47327003669, -69269.47248623992,
                -69269.47244891679, -69269.47645687914, -69269.47922946361, -69269.4793222245, -69269.47901836311,
                -69269.47895198638, -69269.47886053707, -69269.47875692157, -69269.47890881824, -69269.47887586526
            ]

            distances = [
                11.6508412231, 10.5637525546, 7.1938351319, 2.6117836621, 2.4735288205, 2.9455389405, 1.8364080301,
                1.4740568937, 1.8542068593, 0.9186745766, 0.900191025, 0.5290019787, 0.0979035892, 0.1098240811, 0.0717916768,
                0.0258508395, 0.0300810883, 0.0067904499, 0.0085097364, 0.0073435947
            ]

            iteration = range(len(distances))

        else:
            np.random.seed(19680801)
            number_iterations = np.random.randint(n, high=50, size=15)
            iteration = [np.array(range(iters)) for iters in number_iterations]

            noise_arr = [0.1 * np.random.randn(iters) + 1.0 for iters in number_iterations]

            distance_decay = np.random.rand(n)
            distance_offset = 100 * np.random.rand(n)

            energy_decay = np.random.rand(n)
            energy_offset = 20000 + 500 * np.random.rand(n)
            energy_offset2 = 1000 * np.random.rand(n)

            distances = [
                noise * offset * np.exp(-decay * iters)
                for iters, noise, decay, offset in zip(iteration, noise_arr, distance_decay, distance_offset)
            ]
            energies = [
                noise * offset2 * np.exp(-decay * iters) + offset for iters, noise, decay, offset, offset2 in zip(
                    iteration, noise_arr, energy_decay, energy_offset, energy_offset2)
            ]

        return iteration, distances, energies
    
    return _convergence_plot_data

@pytest.fixture
def lattice_constant_data():
    """
    FIcture returning smaple data for EOS plots
    """
    def _lattice_plot_data(n):
        
        np.random.seed(19680801)
        
        if n==1:

            scaling = np.linspace(0.95, 1.04, 10)
            energy = -500.0 + 500 * (0.99 - scaling)**2

            noise = 0.5 * (np.random.rand(10) - 0.5)

            return scaling, energy+noise, energy

        energy_offset = np.random.rand(n)
        energy_offset = -500.0 + energy_offset

        energy_scaling = np.random.rand(n) * 50
        energy_groundstate = np.random.rand(n)
        energy_groundstate = 1.0 + (energy_groundstate - 0.5) * 0.05

        scaling = np.linspace(0.95, 1.04, 10)
        energy_fit = [
            offset + const * (ground - scaling)**2
            for offset, const, ground in zip(energy_offset, energy_scaling, energy_groundstate)
        ]
        energy_noise = [energy + (np.random.rand(10) - 0.5) * 0.05 for energy in energy_fit]
        scaling = [scaling] * n

        return scaling, energy_noise, energy_fit
    
    return _lattice_plot_data