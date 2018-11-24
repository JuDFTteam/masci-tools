import os
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from studenproject18ws.model.reader import Reader


class Plotter(object):

    def __init__(self, data):
        """

        :type data: Reader
        """
        self.data = data
        self._output_dir = ""

    def plot_to_files(self, output_dir):
        self._output_dir = output_dir

        self._plot_atoms_with_colors()

        Number_Bands_plotted = self.data.eigenvalues.shape[2]  # 5
        if (self.data.band_unfolding == True):
            self._plot_bands_with_weight(Number_Bands_plotted)

        self._plot_bands_with_weight(Number_Bands_plotted, weight=False)
        # plot_bands_with_weight(1)

        # llikecharge
        # %%

        color_scheme = ('green', 'red', 'blue', 'orange', 'black', 'cyan')

        fig = plt.figure()
        ax1 = fig.add_subplot(221)
        ax2 = fig.add_subplot(222)
        ax3 = fig.add_subplot(223)
        ax4 = fig.add_subplot(224)

        max_orbital = (self.data.llikecharge).shape[4]
        max_j = (self.data.llikecharge).shape[3]

        NN = self.data.eigenvalues.shape[2]
        for n in range(NN):
            for m in range(max_j):
                orbital = 0
                # prefactor of "s" should maybe be normalized to max(llikecharge_for_band_n(orbital, m, n)) or so...
                ax1.scatter(self.data.k_dist, self._E_i(n), marker='o', c=color_scheme[orbital],
                            s=4 * self._llikecharge_for_band_n(orbital, m, n), lw=0)
                orbital = 1
                ax2.scatter(self.data.k_dist, self._E_i(n), marker='o', c=color_scheme[orbital],
                            s=8 * self._llikecharge_for_band_n(orbital, m, n), lw=0)
                orbital = 2
                ax3.scatter(self.data.k_dist, self._E_i(n), marker='o', c=color_scheme[orbital],
                            s=16 * self._llikecharge_for_band_n(orbital, m, n), lw=0)
                orbital = 3
                ax4.scatter(self.data.k_dist, self._E_i(n), marker='o', c=color_scheme[orbital],
                            s=32 * self._llikecharge_for_band_n(orbital, m, n), lw=0)

            print("%i/%i" % (n, NN))

        plt.savefig(os.path.join(output_dir, self.data.filename + "_orbitals_compare.png"), dpi=2000)

    def _plot_atoms_no_color(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # Plot the values
        for i in range(len(self.data.atoms_coords[:].T[0])):
            ax.scatter(self.data.atoms_coords[:].T[0][i], self.data.atoms_coords[:].T[1][i],
                       self.data.atoms_coords[:].T[2][i], c="blue")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.savefig(os.path.join(self._output_dir, self.data.filename + "_3d_visualization_nocolor.png"), dpi=500)

    def _create_colorbar(self, N):
        colors = []
        m = int(N ** (1. / 3)) + 1
        for i in range(m):
            for j in range(m):
                for k in range(m):
                    colors += [(i * 1. / m, j * 1. / m, k * 1. / m)]
        return colors

    def _plot_atoms_with_colors(self):
        colorbar = self._create_colorbar(self.data.number_atom_groups)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for i in range(len(self.data.atoms_coords[:].T[0])):
            ax.scatter(self.data.atoms_coords[:].T[0][i], self.data.atoms_coords[:].T[1][i],
                       self.data.atoms_coords[:].T[2][i], c=colorbar[
                    self.data.atom_group[i]])

        plt.xlabel("x")
        plt.ylabel("y")
        plt.savefig(os.path.join(self._output_dir, self.data.filename + "_3d_visualization_color.png"), dpi=500)

    # Returns E(k) for the i-th Band

    def _E_i(self, i):
        return self.data.eigenvalues[0].T[i]

    # Returns weight for the i-th Band

    def _weight_for_band_i(self, i):
        return self.data.weights2[0].T[i]

    # Returns array of lenght len(kpts)
    # i: (0, 1, 2, 3) --> probalby belongs to the orbital number s,p, d,f
    # j: no idea what this is <----------------------------------------------------
    # n: n-th energy-band

    def _llikecharge_for_band_n(self, i, j, n):
        return (self.data.llikecharge[0][:].T[i][j][n])

    def _plot_bands_with_weight(self, Number_Bands_plotted, weight=True):
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        max_E = max(self._E_i(0))
        min_E = min(self._E_i(0))

        ax1.hlines(self.data.fermi_energy, 0, max(self.data.k_dist))

        for n in range(Number_Bands_plotted):
            # ax1.scatter(self.data.k_dist, self.E_i(n), marker='.', c='b', s=weight_for_band_i(n))
            if (weight == True):
                ax1.scatter(self.data.k_dist, self._E_i(n), marker='o', c='b', s=3 * self._weight_for_band_i(n), lw=0)
            else:
                ax1.scatter(self.data.k_dist, self._E_i(n), marker='o', c='b', s=0.1, lw=0)
            if (max_E < max(self._E_i(n))):
                max_E = max(self._E_i(n))
            if (min_E > min(self._E_i(n))):
                min_E = min(self._E_i(n))
            print("%i/%i" % (n, Number_Bands_plotted))

        # label of the special points is still missing...
        for i in range(len(self.data.special_points)):
            index = self.data.special_points[i]
            plt.vlines(self.data.k_dist[index - 1], min_E, max_E)

        plt.xlabel("k")
        plt.ylabel("E(k)")
        if (weight == True):
            plt.savefig(os.path.join(self._output_dir, self.data.filename + "_bandstructure_weight.png"), dpi=2000)
        else:
            plt.savefig(os.path.join(self._output_dir, self.data.filename + "_bandstructure_noweight.png"), dpi=2000)
