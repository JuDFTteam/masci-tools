#from tkinter import Tk, Label, Button, Entry, StringVar, DISABLED, NORMAL, END, W, E
from tkinter import *
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
#matlplotlib.use("TkAgg")
from studenproject18ws.hdf.reader import Reader
from studenproject18ws.hdf.recipes import Recipes
from studenproject18ws.plot.plot import Bandplot_matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
import os
import logging
class SiscLab:
    def __init__(self, master):
        self.master = master
        master.title("SiscLab")

        # variables needed to declare
        self.variables = 0

        tabControl = ttk.Notebook(root)  # Create Tab Control
        tabControl.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')

        self.tabframe1 = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(self.tabframe1, text='Entering the Variables')  # Add the tab
        self.tab1 = ttk.LabelFrame(self.tabframe1, text = "Entering the Variables")
        self.tab1.grid(row = 0,column=0,padx =8,pady=10)

        self.tabframe2 = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(self.tabframe2, text='Band plot')  # Add the tab
        self.tab2 = ttk.LabelFrame(self.tabframe2, text="Band plot")
        self.tab2.grid(row=0, column=0, padx=8, pady=10)

        self.tabframe3 = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(self.tabframe3, text='3D atomic group plot')  # Add the tab
        self.tab3 = ttk.LabelFrame(self.tabframe3, text="3D atomic group plot")
        self.tab3.grid(row=0, column=0, padx=8, pady=10)

        self.tabframe4 = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(self.tabframe4, text='DOS Plot')  # Add the tab
        self.tab4 = ttk.LabelFrame(self.tabframe4, text="DOS plot")
        self.tab4.grid(row=0, column=0, padx=8, pady=10)

        self.message1 = "Enter the file name"
        self.label_text = StringVar()
        self.label_text.set(self.message1)
        self.NumAtomGroups = IntVar()
        self.NumAtomGroups.set(2)
        #self.NumAtomGroups = 2
        self.FileMessage = Label(self.tab1, textvariable=self.label_text)
        self.FileName = Entry(self.tab1, validate="key")
        self.data=[]
        self.OpenButton = Button(self.tab1, text="open", command=self.OpenTheFile)

        self.LabelAtom = Label(self.tab1, text="Choose a atom group")
        self.menubar = Menu(self.tab1)
        self.choices = IntVar()
        self.choices.set([i for i in range(1, self.NumAtomGroups.get()+1)])
        self.AtomGroupSelection = Listbox(self.tab1, listvariable=self.choices, selectmode=MULTIPLE, width=5, height=4,exportselection=0)

        self.menubar1 = Menu(self.tab1)
        self.choices1 = StringVar()
        self.choices1.set("S P D F")
        self.BandSelection =Listbox(self.tab1, listvariable= self.choices1, selectmode=MULTIPLE, width=3, height=4,exportselection=0)

        self.Unfolding = BooleanVar()
        self.Unfolding.set(False)
        self.UnfoldingButton = Checkbutton(self.tab1,text="Unfold Band Structure", onvalue = True, variable = self.Unfolding)

        self.ExpoLabel = Label(self.tab1, text = 'Exponential')
        self.ExponentialWeight = tk.Scale(self.tab1,from_=0, to_=4)
        self.MarkerLabel = Label(self.tab1, text='Marker')
        #self.MarkerSize = Entry(self.tab1, validate="key")
        self.UpdateButton = Button(self.tab1, text='Update', command=self.Update)
        self.SaveButton = Button(self.tab1, text='Save as PDF', command = self.SavePDF)

        #self.Eigenweight = tk.Scale(self.tab1, from_=self.ymin, to_=self.ymax)
        self.Compare = BooleanVar()
        self.Compare.set(False)
        self.CompareButton = Checkbutton(self.tab1,text='Compare 2 characters',onvalue = True,variable = self.Compare)
        self.MarkerSizeSlider = Scale(self.tab1, from_=1,to_=10)
        self.ignore_atoms_per_group = BooleanVar()
        self.ignore_atoms_per_group.set(False)
        self.ignore_atoms = Checkbutton(self.tab1,text='Ignore Atom Groups',onvalue = True,variable = self.ignore_atoms_per_group)

        self.menubar2 = Menu(self.tab1)
        self.choices2 = IntVar()
        self.choices2.set("0 1")
        self.spinlist = Listbox(self.tab1, listvariable=self.choices2, selectmode=MULTIPLE, width=5, height=4,exportselection=0)

        self.select_groups = BooleanVar()
        self.select_groups.set(False)
        self.select_groupsButton = Checkbutton(self.tab1, text='select_groups', onvalue=True, variable=self.select_groups)

        self.interstitial = BooleanVar()
        self.interstitial.set(False)
        self.interstitialButton = Checkbutton(self.tab1, text='interstitial', onvalue=True, variable=self.interstitial)

        self.all_characters = BooleanVar()
        self.all_characters.set(False)
        self.all_charactersButton = Checkbutton(self.tab1, text='all_characters', onvalue=True, variable=self.all_characters)

        self.fig1 = Figure(figsize=(4, 4), dpi=70)
        self.fig1.suptitle(f"BandStructure of {self.FileName.get()}")
        tk.Frame(self.tab2)
        self.canvas = FigureCanvasTkAgg(self.fig1, master=self.tab2)
        self.canvas.draw()
        self.tkwidget = self.canvas.get_tk_widget()

        self.fig2 = Figure(figsize=(4, 4), dpi=70)
        self.fig2.suptitle(f"Atom Group")
        tk.Frame(self.tab3)
        # calling function to get figure as object
        self.canvas1 = FigureCanvasTkAgg(self.fig2, master=self.tab3)
        self.canvas1.draw()
        # get widget then pack
        self.tkwidget1 = self.canvas1.get_tk_widget()
        # self.tkwidget.pack()

        self.fig3 = Figure(figsize=(4, 4), dpi=70)
        self.fig3.suptitle(f"DOS")
        tk.Frame(self.tab4)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.tab4)
        self.canvas2.draw()
        self.tkwidget2 = self.canvas1.get_tk_widget()

        self.FileMessage.grid(row=0, column=0)
        self.FileName.grid(row=1, column=0, columnspan=5)
        self.OpenButton.grid(row=1,column=5)
        self.AtomGroupSelection.grid(row=2,column=2)
        self.LabelAtom.grid(row=2, column=0)
        self.BandSelection.grid(row=3,column=0)
        self.tkwidget.grid(row=2,rowspan =5,columnspan=5)
        self.UnfoldingButton.grid(row=3,column =2)
        self.ExponentialWeight.grid(row= 3,column=6)
        self.ExpoLabel.grid(row=3,column =5)
        self.MarkerLabel.grid(row=4,column =0)
        #self.MarkerSize.grid(row=4,column =2)
        #self.tkwidget.grid(row=6,column =2)
        self.UpdateButton.grid()
        self.SaveButton.grid()
        #self.Eigenweight.grid(row=6,column=5)
        self.CompareButton.grid()
        self.MarkerSizeSlider.grid(row=4,column =2)
        self.ignore_atoms.grid()
        self.spinlist.grid()
        self.select_groupsButton.grid()
        self.interstitialButton.grid()
        self.all_charactersButton.grid()
    def atomgroupselection(self):
        self.AtomgroupBoolean = []
        for i in range(self.NumAtomGroups.get()):
            self.AtomgroupBoolean.append(False)
        n = [self.AtomGroupSelection.get(i) for i in self.AtomGroupSelection.curselection()]
        for i in n:
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
            self.data = self.extractor.read(recipe=Recipes.Bands)
            self.data.move_datasets_to_memory()
        self.bandplotter = Bandplot_matplotlib(self.data)
        self.NumAtomGroups.set(self.data.num_groups)
        '''
        self.AtomGroup.set('all')  # set the default option
        self.AtomGroupSelection = OptionMenu(root, self.AtomGroup, *self.choices)
        '''
        self.choices.set([i for i in range(1, self.NumAtomGroups.get() + 1)])
        self.AtomGroupSelection = Listbox(self.tab1, listvariable=self.choices, selectmode=MULTIPLE, width=5, height=4,exportselection=0)#, yscrollcommand=scrollbar)
        self.AtomGroupSelection.grid(row=2, column=2)
        #print(type(self.NumAtomGroups))
        self.def_bands = [band for band in range(self.data.eigenvalues.shape[2])]
        self.eigenmin = self.def_bands[0] +1
        self.eigenmax = self.def_bands[-1] +1
        self.Eigenweightlb = tk.Scale(self.tab1, from_=self.eigenmin, to_=self.eigenmax)
        self.Eigenweightlb.grid(row=6, column=5)
        self.Eigenweightub = tk.Scale(self.tab1, from_=self.eigenmin, to_=self.eigenmax)
        self.Eigenweightub.grid(row=6, column=7)
        self.ymin,self.ymax = self.bandplotter.get_band_data_ylim()
        self.yaxismin = tk.Scale(self.tab1, from_=self.ymin, to_=self.ymax)
        self.yaxismin.grid(row =6,column = 10)
        self.yaxismax = tk.Scale(self.tab1, from_=self.ymin, to_=self.ymax)
        self.yaxismax.grid(row = 6, column=12)
        # opening the file which is in self.entry
        fig_scale = 0.5
        fig_ratio = [10, 6]
        # self.fig.clf()
        self.fig1, self.ax1 = plt.subplots(1, figsize=[fig_scale * el for el in fig_ratio])

        self.fig2 = plt.figure()

        self.fig3, self.ax3 = plt.subplots(1, figsize=[fig_scale * el for el in fig_ratio])
        return
    def Update(self):
        self.ax1.clear()
        #self.fig1.clear()
        self.ax1.set_ylim(self.yaxismin.get(),self.yaxismax.get())
        self.spin = [i for i in self.spinlist.curselection()]
        self.spinboolean = [False, False]
        self.spinboolean = [True for i in self.spinlist.curselection()]

        self.atomgroupselection()
        self.bandselection()
        self.mask_groups = self.AtomgroupBoolean
        self.mask_characters = self.Band
        self.mask_bands = [el in range(self.Eigenweightlb.get()-1, self.Eigenweightub.get()) for el in self.def_bands] #This is from eigen energy which can be slided
        #get the band from the data.bands


        self.unfolding_weight_exponent = self.ExponentialWeight.get()
        self.isCharacterPlot = False
        if self.Compare:
            if (self.Band.count(True)+self.AtomgroupBoolean.count(True)+self.spinboolean.count(True) == 4):
                self.isCharacterPlot = True

        self.marker_size = self.MarkerSizeSlider.get()
        #spin is a list
        plt.suptitle(f"BandStructure of { self.FileName.get()}")
        print(self.mask_bands)
        print(self.mask_characters)
        print(self.mask_groups)
        print(self.unfolding_weight_exponent, self.isCharacterPlot, self.ax1,
                                    self.ignore_atoms_per_group.get(), self.marker_size)
        self.bandplotter.plot_bands(self.mask_bands, self.mask_characters, self.mask_groups, self.spin,
                                    float(self.unfolding_weight_exponent), self.isCharacterPlot, self.ax1,
                                    self.ignore_atoms_per_group.get(), float(self.marker_size))

        #self.fig1= ax.scatter(k_r, E_r, marker='o', c='b', s=2 * W_r, lw=0)
        self.canvas = FigureCanvasTkAgg(self.fig1, master=self.tab2)
        self.canvas.draw()
        # get widget then pack
        self.tkwidget = self.canvas.get_tk_widget()
        self.tkwidget.grid(row=6, column=2)
        self.fix_xlim=True
        '''
        fig_scale =0.65
        figsize=[fig_scale * el for el in fig_ratio]
        fug3=plt.fugure()
        gs_dos = gridspec.Gridspec(1,2)
        ax_dos =fig3.add_subplot(gs_dos[0,1])
        gs = gridspec.Gridspec(1,2)
        ax3 =fig3.add_subplot(gs[0,0],sharey=ax_dos)
        gs.update(wspace=0,left=0.1,right=1.4)
        gss_dos.update(left=0.6,right=0.9,wspace=0)
        plt.setp(ax_dos.get_ytiklabels(),visible=False)
        
        self.bandplotter.plot_dos(self.filepath_dos, self.mask_groups, self.mask_characters,
                 self.select_groups, self.interstitial, self.all_characters,
                 self.ax3, self.fix_xlim)
                 
        self.canvas2 = FigureCanvasTkAgg(self.fig3, master=self.tab2)
        self.canvas2.draw()
        # get widget then pack
        self.tkwidget2 = self.canvas.get_tk_widget()
        self.tkwidget2.grid(row=6, column=2)
        '''
        # rgneoinite
        return

    def SavePDF(self):
        self.pp = PdfPages('main.pdf')
        self.pp.savefig(self.fig1)
        self.pp.close()
if __name__ == "__main__":
    root= Tk()
    gui = SiscLab(root)
    root.mainloop()