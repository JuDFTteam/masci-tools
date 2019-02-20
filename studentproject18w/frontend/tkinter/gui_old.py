# from tkinter import Tk, Label, Button, Entry, StringVar, DISABLED, NORMAL, END, W, E
from tkinter import *
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

from studentproject18w.hdf.reader import Reader
from studentproject18w.hdf.recipes import Recipes
from studentproject18w.plot.matplot import BandDOSPlot

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
import os

from mpl_toolkits.mplot3d import axes3d, Axes3D
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
import logging


class SiscLab:
    def __init__(self, master):
        self.master = master
        master.title("SiscLab-WS Project-8")

        tabControl = ttk.Notebook(root)  # Create Tab Control
        tabControl.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')

        self.tabframe1 = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(self.tabframe1, text='Entering the Variables')  # Add the tab
        self.tab1 = ttk.LabelFrame(self.tabframe1, text="Entering the Variables")
        self.tab1.grid(row=0, column=0, padx=8, pady=10)

        self.tabframe2 = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(self.tabframe2, text='Band-DOS plot')  # Add the tab
        self.tab2 = ttk.LabelFrame(self.tabframe2, text="Band plot")
        self.tab2.grid(row=0, column=0, padx=8, pady=10)

        self.tabframe3 = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(self.tabframe3, text='3D atomic group plot')  # Add the tab
        self.tab3 = ttk.LabelFrame(self.tabframe3, text="3D atomic group plot")
        self.tab3.grid(row=0, column=0, padx=8, pady=10)

        self.NumAtomGroups = IntVar()
        self.NumAtomGroups.set(1)
        self.FileMessage = Label(self.tab1, text="Enter the hdf file name")
        self.FileName = Entry(self.tab1, validate="key")

        self.FileDOS1Message = Label(self.tab1, text="Enter the DOS Spin 0 file name")
        self.FileNameDOS1 = Entry(self.tab1, validate="key")

        self.FileDOS2Message = Label(self.tab1, text="Enter the DOS Spin 1 file name")
        self.FileNameDOS2 = Entry(self.tab1, validate="key")

        self.data = []
        self.OpenButton = Button(self.tab1, text="open", command=self.OpenTheFile)

        self.LabelAtom = Label(self.tab1, text="Choose a atom group")
        self.menubar = Menu(self.tab1)
        self.choices = IntVar()
        self.choices.set([i for i in range(1, self.NumAtomGroups.get() + 1)])
        self.AtomGroupSelection = Listbox(self.tab1, listvariable=self.choices, selectmode=MULTIPLE, width=9, height=4,
                                          exportselection=0)

        self.LabelBand = Label(self.tab1, text="Choose a Character group")
        self.menubar1 = Menu(self.tab1)
        self.choices1 = StringVar()
        self.choices1.set("S P D F")
        self.BandSelection = Listbox(self.tab1, listvariable=self.choices1, selectmode=MULTIPLE, width=3, height=4,
                                     exportselection=0)

        self.ExpoLabel = Label(self.tab1, text='Exponential')
        self.ExponentialWeight = Scale(self.tab1, from_=0.0, to_=4.0, resolution=0.1, orient=HORIZONTAL)
        self.MarkerLabel = Label(self.tab1, text='Marker')

        self.UpdateButton = Button(self.tab1, text='Update', command=self.Update)
        self.SaveButton = Button(self.tab1, text='Save as PDF', command=self.SavePDF)

        self.Compare = BooleanVar()
        self.Compare.set(False)
        self.CompareButton = Checkbutton(self.tab1, text='Compare 2 characters', onvalue=True, variable=self.Compare)
        self.MarkerSizeSlider = Scale(self.tab1, from_=1.0, to_=10.0, resolution=0.1, orient=HORIZONTAL)
        self.ignore_atoms_per_group = BooleanVar()
        self.ignore_atoms_per_group.set(False)
        self.ignore_atoms = Checkbutton(self.tab1, text='Ignore Atom Groups', onvalue=True,
                                        variable=self.ignore_atoms_per_group)

        self.menubar2 = Menu(self.tab1)
        self.choices2 = IntVar()
        self.choices2.set("0 1")
        self.spinlist = Listbox(self.tab1, listvariable=self.choices2, selectmode=MULTIPLE, width=5, height=4,
                                exportselection=0)
        self.LabelSpin = Label(self.tab1, text="Choose a Spin group")

        self.select_groups = BooleanVar()
        self.select_groups.set(False)
        self.select_groupsButton = Checkbutton(self.tab1, text='select_groups', onvalue=True,
                                               variable=self.select_groups)

        self.interstitial = BooleanVar()
        self.interstitial.set(False)
        self.interstitialButton = Checkbutton(self.tab1, text='interstitial', onvalue=True, variable=self.interstitial)

        self.all_characters = BooleanVar()
        self.all_characters.set(False)
        self.all_charactersButton = Checkbutton(self.tab1, text='all_characters', onvalue=True,
                                                variable=self.all_characters)

        self.eigenmin = 0
        self.eigenmax = 0
        self.Eigenweightlb = Scale(self.tab1, from_=self.eigenmin, to_=self.eigenmax, orient=HORIZONTAL)
        self.Eigenweightlb.grid(row=12, column=0, columnspan=4)
        self.Eigenweightub = tk.Scale(self.tab1, from_=self.eigenmin, to_=self.eigenmax, orient=HORIZONTAL)
        self.Eigenweightub.grid(row=15, column=0, columnspan=4)
        self.BandminLabel = Label(self.tab1, text='Band min')
        self.BandmaxLabel = Label(self.tab1, text='Band max')

        self.ymin, self.ymax = 0.0, 0.0
        self.yaxismin = tk.Scale(self.tab1, from_=self.ymin, to_=self.ymax, resolution=0.1, orient=HORIZONTAL)
        self.yaxismin.grid(row=12, column=5, columnspan=4)
        self.yaxismax = tk.Scale(self.tab1, from_=self.ymin, to_=self.ymax, resolution=0.1, orient=HORIZONTAL)
        self.yaxismax.grid(row=15, column=5, columnspan=4)
        self.YminLabel = Label(self.tab1, text='Y min')
        self.YmaxLabel = Label(self.tab1, text='Y max')
        fig_scale = 0.5
        fig_ratio = [10, 6]
        self.fig1, self.ax_bands = plt.subplots(1, figsize=[fig_scale * el for el in fig_ratio])
        self.fig2 = plt.figure()
        self.fig2.suptitle(f"Atom Group")
        self.ax2 = Axes3D(self.fig2)
        self.fig1.suptitle(f"BandStructure of {self.FileName.get()}")
        '''
        tk.Frame(self.tab2)
        self.canvas = FigureCanvasTkAgg(self.fig1, master=self.tab2)
        self.canvas.draw()
        self.tkwidget = self.canvas.get_tk_widget()
        self.fig2 = Figure(figsize=(4, 4), dpi=70)
        self.fig2.suptitle(f"Atom Group")
        tk.Frame(self.tab3)
        self.canvas1 = FigureCanvasTkAgg(self.fig2, master=self.tab3)
        self.canvas1.draw()
        self.tkwidget1 = self.canvas1.get_tk_widget()
        #self.fig2 = Figure(figsize=(4, 4), dpi=70)
        self.fig2.suptitle(f"Atom Group")
        self.f2=tk.Frame(self.tab3)
        self.f2.pack(padx=15, pady=15)
        self.canvas1 = FigureCanvasTkAgg(self.fig2, master=self.f2)
        self.canvas1.get_tk_widget().pack(side='top', fill='both')
        self.canvas1._tkcanvas.pack(side='top', fill='both', expand=1)
        self.ax2 = Axes3D(self.fig2)
        self.toolbar = NavigationToolbar2Tk(self.canvas1, self.f2)
        self.toolbar.update()
        self.toolbar.pack()
        '''

        self.FileMessage.grid(row=0, column=0)
        self.FileName.grid(row=0, column=1, columnspan=5)
        self.FileDOS1Message.grid(row=1, column=0)
        self.FileNameDOS1.grid(row=1, column=1, columnspan=5)
        self.FileDOS2Message.grid(row=2, column=0)
        self.FileNameDOS2.grid(row=2, column=1, columnspan=5)
        self.OpenButton.grid(row=1, column=8)
        self.AtomGroupSelection.grid(row=3, column=1, rowspan=4, columnspan=4)
        self.LabelAtom.grid(row=3, column=0)
        self.LabelBand.grid(row=3, column=6)
        self.BandSelection.grid(row=3, column=7, rowspan=4)
        self.ExponentialWeight.grid(row=9, column=0, columnspan=4)
        self.ExpoLabel.grid(row=8, column=0, columnspan=4)
        self.MarkerLabel.grid(row=8, column=5, columnspan=4)
        self.MarkerSizeSlider.grid(row=9, column=5, columnspan=4)
        self.BandminLabel.grid(row=11, column=0, columnspan=4)
        self.BandmaxLabel.grid(row=14, column=0, columnspan=4)
        self.YminLabel.grid(row=11, column=5, columnspan=4)
        self.YmaxLabel.grid(row=14, column=5, columnspan=4)
        self.spinlist.grid(row=3, column=10, rowspan=4)
        self.LabelSpin.grid(row=3, column=9)
        self.UpdateButton.grid(row=20, column=15)
        self.SaveButton.grid(row=21, column=15)
        self.CompareButton.grid(row=10, column=10, columnspan=2, sticky="W")
        self.ignore_atoms.grid(row=11, column=10, columnspan=2, sticky="W")
        self.select_groupsButton.grid(row=12, column=10, sticky="W")
        self.interstitialButton.grid(row=13, column=10, sticky="W")
        self.all_charactersButton.grid(row=14, column=10, sticky="W")

    def atomgroupselection(self):
        self.AtomgroupBoolean = []
        for i in range(self.NumAtomGroups.get()):
            self.AtomgroupBoolean.append(False)
        self.n = [i for i in self.AtomGroupSelection.curselection()]
        for i in self.n:
            self.AtomgroupBoolean[int(i) - 1] = True
        return

    def bandselection(self):
        self.Band = [False, False, False, False]
        band = [self.BandSelection.get(i) for i in self.BandSelection.curselection()]
        if 'S' in band:
            self.Band[0] = True
        if 'P' in band:
            self.Band[1] = True
        if 'D' in band:
            self.Band[2] = True
        if 'F' in band:
            self.Band[3] = True

    def OpenTheFile(self):
        self.filepath = ['data', 'input', self.FileName.get()]
        self.filepath = os.path.join(*self.filepath)
        self.extractor = Reader(filepath=self.filepath)
        with self.extractor as h5file:
            self.data = self.extractor.read(recipe=Recipes.FleurBands)
            self.data.move_datasets_to_memory()
        self.filepath_dos = []
        if self.FileNameDOS1.get():
            self.filepath_dos.append(['data', 'input', self.FileNameDOS1.get()])
        if self.FileNameDOS2.get():
            self.filepath_dos.append(['data', 'input', self.FileNameDOS2.get()])
        self.filepath_dos = [os.path.join(*fpd) for fpd in self.filepath_dos]
        self.bandplotter = BandDOSPlot(plt, self.data, self.filepath_dos)
        self.plter = BandDOSPlot(plt, self.data, self.filepath_dos)
        fig_scale = 0.9
        fig_ratio = [10, 6]
        self.fig1, self.ax_bands, self.ax_dos = self.plter.setup_figure(fig_ratio, fig_scale)

        self.NumAtomGroups.set(self.data.num_groups)
        self.labels = self.plter.icdv.group_labels
        # self.choices.set([i for i in range(1, self.NumAtomGroups.get() + 1)])
        self.choices.set([i for i in self.labels])
        self.AtomGroupSelection.grid_remove()
        self.AtomGroupSelection = Listbox(self.tab1, listvariable=self.choices, selectmode=MULTIPLE, width=9, height=4,
                                          exportselection=0)  # , yscrollcommand=scrollbar)
        self.AtomGroupSelection.grid(row=3, column=1, rowspan=4, columnspan=4)

        self.def_bands = [band for band in range(self.data.eigenvalues.shape[2])]
        self.eigenmin = self.def_bands[0] + 1
        self.eigenmax = self.def_bands[-1] + 1

        self.Eigenweightlb.grid_remove()
        self.Eigenweightub.grid_remove()
        self.Eigenweightlb = Scale(self.tab1, from_=self.eigenmin, to_=self.eigenmax, orient=HORIZONTAL)
        self.Eigenweightlb.grid(row=12, column=0, columnspan=4)
        self.Eigenweightub = Scale(self.tab1, from_=self.eigenmin, to_=self.eigenmax, orient=HORIZONTAL)
        self.Eigenweightub.grid(row=15, column=0, columnspan=4)

        self.yaxismin.grid_remove()
        self.yaxismax.grid_remove()
        self.ymin, self.ymax = self.bandplotter.get_data_ylim()
        self.yaxismin = tk.Scale(self.tab1, from_=self.ymin, to_=self.ymax, resolution=0.1, orient=HORIZONTAL)
        self.yaxismin.grid(row=12, column=5, columnspan=4)
        self.yaxismax = tk.Scale(self.tab1, from_=self.ymin, to_=self.ymax, resolution=0.1, orient=HORIZONTAL)
        self.yaxismax.grid(row=15, column=5, columnspan=4)
        # opening the file which is in self.entry

        return

    def drawSphere(self, xCenter, yCenter, zCenter, c):
        # draw sphere
        r = 1
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        # shift and scale sphere
        x = r * x + xCenter
        y = r * y + yCenter
        z = r * z + zCenter
        self.ax2.plot_surface(x, y, z, rstride=4, cstride=4, color=c, linewidth=0)

    def PlotAtomGroups(self):
        self.ax2.clear()
        x, y, z = self.data.atoms_position.T
        # self.n = [self.AtomGroupSelection.get(i) for i in self.AtomGroupSelection.curselection()]
        self.n = [i + 1 for i in self.AtomGroupSelection.curselection()]
        self.legend = [self.labels[i] for i in self.AtomGroupSelection.curselection()]
        color = iter(cm.rainbow(np.linspace(0, 1, len(self.n))))
        for group in self.n:
            selected_atoms_in_group = np.where(self.data.atoms_group == group)
            c = next(color)
            for i in selected_atoms_in_group:
                for j in i:
                    self.drawSphere(x[j], y[j], z[j], c)
                    # self.ax2.legend(self.legend)

    def Update(self):
        self.ax_bands.clear()
        self.ax2.clear()
        # self.fig1.clear()
        self.ylim = [self.yaxismin.get(), self.yaxismax.get()]
        self.ax_bands.set_ylim(self.yaxismin.get(), self.yaxismax.get())
        self.spin = [i for i in self.spinlist.curselection()]
        self.spinboolean = [False, False]
        self.spinboolean = [True for i in self.spinlist.curselection()]

        self.atomgroupselection()
        self.bandselection()
        self.mask_groups = self.AtomgroupBoolean
        self.mask_characters = self.Band
        self.mask_bands = [el in range(self.Eigenweightlb.get() - 1, self.Eigenweightub.get()) for el in self.def_bands]
        self.unfolding_weight_exponent = self.ExponentialWeight.get()
        self.isCharacterPlot = False
        if self.Compare.get():
            if (self.Band.count(True) == 2):
                self.isCharacterPlot = True

        self.marker_size = self.MarkerSizeSlider.get()

        # atom group plot
        self.PlotAtomGroups()
        plt.suptitle(f"BandStructure of { self.FileName.get()}")
        self.dos_fix_xlim = True
        print(self.marker_size)
        self.plter.plot_bandDOS2(self.mask_bands, self.mask_characters, self.mask_groups, self.spin,
                                 self.unfolding_weight_exponent, self.isCharacterPlot,
                                 self.ignore_atoms_per_group.get(), self.marker_size,
                                 self.select_groups.get(), self.interstitial.get(), self.all_characters.get(),
                                 self.ax_bands,
                                 self.dos_fix_xlim, self.ylim)
        print(self.marker_size)
        self.f1 = tk.Frame(self.tab2)
        self.f1.grid(row=0, column=0)
        self.canvas = FigureCanvasTkAgg(self.fig1, master=self.f1)
        self.canvas.draw()
        self.tkwidget = self.canvas.get_tk_widget()
        self.tkwidget.grid(row=0, column=0)
        self.toolbarFrame1 = Frame(master=self.f1)
        self.toolbarFrame1.grid(row=5, column=0)
        self.toolbar1 = NavigationToolbar2Tk(self.canvas, self.toolbarFrame1)
        self.toolbar1.update()
        print(self.marker_size)
        self.f2 = tk.Frame(self.tab3)
        self.f2.grid(row=0, column=0)
        self.canvas1 = FigureCanvasTkAgg(self.fig2, master=self.f2)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid()  # side='top', fill='both'
        self.canvas1._tkcanvas.grid(sticky=N + S + W + E)  # side='top', fill='both', expand=1

        self.toolbarFrame = Frame(master=self.f2)
        self.toolbarFrame.grid(row=5, column=0)
        self.toolbar = NavigationToolbar2Tk(self.canvas1, self.toolbarFrame)
        # self.toolbar = NavigationToolbar2Tk(self.canvas1, self.f2)
        self.toolbar.update()
        # self.toolbar.grid()
        print(self.marker_size)
        return

    def SavePDF(self):
        self.pp = PdfPages('main.pdf')
        self.pp.savefig(self.fig1)
        self.pp.savefig(self.fig2)
        self.pp.close()


if __name__ == "__main__":
    root = Tk()
    gui = SiscLab(root)
    root.mainloop()
