
SiScLab 2018 Student Project **Analysis Tool for Materials Design**. Written in Python3.

Authors: [Johannes Wasmer](https://github.com/Irratzo), [Christian Partmann](https://github.com/ChristianPartmann), and [Praneeth Katta](https://github.com/PraneethKatta).

# Overview
This subfolder `studentproject18ws` is currently a largely independent side-project accompanying the main module `masci-tools`. It was created in a student project, and consists of three submodules:

  * preprocessor: a HDF reader interface, and one implementation for [Fleur](http://www.judft.de) band structure simulation output
  * visualization: a plotting interface, and one implementation for [Fleur](http://www.judft.de) bandstructure+DOS plots
  * frontends: a Desktop GUI and a Web Dashboard (Tk and Jupyter) for interactive Fleur bandDOS plots.

A more thorough description and example use cases can be found in the project [report](./doc/report.pdf) and [presentation](./doc/presentation.pdf). 

![](./readme/web_frontend.png)

# For Frontend Users

## General Remarks

These remarks apply to all frontends.

Though the Desktop and Web Frontend are functionally identical, there might be small differences in how the controls are used and how they are labeled.  

### File Input

The frontends currently expects band structure data in the HDF output format of
[Fleur](http://www.judft.de). The density of states data is expected to be in
the CSV output format of [Fleur](http://www.judft.de), one file per spin. If no
density of states files are supplied, the frontend will just draw a band
structure plot (BandPlot) and omit the adjoined density of states plot
(DOSPlot). Thus, in the following BandDOSPlot stands for both kinds of plot. The
Web Frontend will only show controls for data that is present in the input
(e.g., DOS and spin controls).

## Desktop Frontend

### Installation

A windows executable file (.exe) is made by packing all the required packages
into the file. Any modern PC running on windows can run the frontend without any
installation process and there is no prerequisite to execute this executable
file. PC need not have python or other packages installed.

For executables for other operating systems, please contact the developers.

### Usage

Desktop based front end GUI is easy to use. By just running the .exe file provided will open the software with the packages involved to run the software. There are three tabs/windows in the software. In the first tab, input data from the external files are chosen. 

Controls for all plots: 

  * Atom Groups: draw the BandDOSPlot only for the selected symmetry groups.
  * Character: select one or more band Characters (orbitals) 'S','P','D','F'.
  * Spin: select any one spin or both spins.
  * Marker size: Default marker size of 1.0 is selected. How ever, user have a
    choice to increase the marker size of the dots (eigenenergies) plotted in
    the BandPlot.
  * Ymin, Ymax: This control is used to limit the range energy range of the BandDOSPlot.
  * BandMin, BandMax: This control is used to limit the band range of the BandDOSPlot.
  * Update, SaveButton: Update the BandDOSplot to the newly selected data by user. Save the the plot as a PDF on disk.
  * Exponential weight: The unfolding exponent for supercell calculations (see [report](./doc/report.pdf)). Value 0.0 means no unfolding. If the calculation is done with a unit cell, this control has no effect.
  * Compare 2Characters: When a user wants to compare 2 characters, this button makes the BandPlot show the influence of each character to each eigenergy using a sequential (2** colormap. The control is disabled if other than two characters are selected.
  * Ignore Atom group: This button allows an option to ignore the atom groups.
  
Controls for the DOSPlot only:

  * Select groups: 
  * Interstitial: include the interstitial in the density of states
  * All characters: This button is used to get the data of all characters combined from the data file.



The above explains the input to be given by user in Tab 1. After Update button is clicked, a BandPlot or BandDOS plot can be observed in Tab 2 and 3D atomic plot can be seen in Tab 3. Atleast one Atom Group, one Character, one Spin have to be selected. Ymin should be lessthan Ymax and similarly BandMin should be lessthan BandMax.

## Web Frontend

### Access

The Web Frontend is a Jupyter Dashboard. It is in experimental state (no fileupload yet). You can try it out [here on Binder](https://mybinder.org/v2/gh/JuDFTteam/masci-tools/studentproject18ws?filepath=studentproject18w%2Ffrontend%2Fjupyter%2Fdemo%2Fbinder_demo.ipynb). You can run it locally (see developer section). If you have an [AiiDaLab account](https://aiidalab.materialscloud.org/hub/login): the dashboard is planned to be published as an app there.

### Usage

Using the Dashboard should be self-explanatory to the domain user. Some tips:

   * multi-selection boxes: use ctrl or shift to select multiple items. 
   * slider values can also be typed into the adjoining text box.   
   * should the app ever appear to get stuck, a reload/rerun will do the trick.

# For Developers

## Installation

Though `masci-tools` is availabe via PyPI, there is currently no plan to integrate `studentproject18ws`. If you want to use it in your code, clone the repo, use it in an IDE, or append the path to your `sys.path`:

``` python
import sys
if path_repo not in sys.path:
    sys.path.append(path_repo)
    
# now import works
from studentproject18w.hdf.reader import Reader
# ...
```

### Create project virtual environment

With conda (recommended):
- [Install Anaconda (3 recommended)](https://www.anaconda.com/download)
- Install the environment `masci-stupro` with the necessary and recommended dependencies:
```bash
conda create -f environment.yml
source activate masci-stupro
```
With virtualenv (untested):
```bash
virtualenv masci-stupro
source masci-stupro/bin/activate
pip install -r requirements_pip.txt # install requirements
```

## Programmatic use

In this example, a Fleur HDF file is preprocessed using the Recipe `FleurBands`. The resulting output `data` with the extracted and transformed HDF datasets and attached load methods (Extract-Transform-Load) is then passed to a plotter, alongside some DOS CSV files for a bandstructure plot using `matplotlib` as backend library.

``` python
import matplotlib.pyplot as plt
from studentproject18w.hdf.reader import Reader
from studentproject18w.hdf.recipes import Recipes
from studentproject18w.plot.matplot import BandDOSPlot

data = None
reader = Reader(filepath=filepath_hdf)
with reader as h5file:
    data = reader.read(recipe=Recipes.FleurBands)
    #
    # Note:
    # Inside the with statement (context manager),
    # all data attributes that are type h5py Dataset are available (in-file access)
    # When the statement is left,the HDF5 file gets closed and the datasets are closed.
    #
    # Use data outside the with-statement (in-memory access: all HDF5 datasets converted to numpy ndarrays):
    data.move_datasets_to_memory()

plotter = BandDOSPlot(plt, data, filepaths_dos)
(fig, ax_bands, ax_dos) = plter.setup_figure(fig_ratio=[12,6], fig_scale=1, fig_title="BandDOS")
data_selection = some_selection_process()
plotter.plot_bandDOS(*data_selection)
plt.show()
```

## Try out Web Frontend locally

The demo notebook with the Dashboard is `studentproject18w/frontend/jupyter/demo/demo.ipynb`.

### If using Jupyter Notebook
If using Windows, omit keyword `source`.
```bash
source activate masci-stupro
cd mypath/masci-tools/studentproject18ws/
jupyter-notebook .
# if Home is not set to this dir, try this instead:
# /home/you/anaconda3/envs/myenv/bin/python /home/you/anaconda3/envs/myenv/bin/jupyter-notebook .
```
### If using Jupyter Lab
Additional installation step needed:
```bash
source activate masci-stupro
jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-matplotlib ipyvolume
cd mypath/masci-tools/studentproject18ws/
jupyter-lab
```

## Frontend Deployment

### Desktop Frontend

To create executables for different operating systems, use
[PyInstaller](https://www.pyinstaller.org/). The target file is
`frontend/tkinter/gui.py`.


### Web Frontend

The Web Frontend is currently a single Jupyter Notebook. In order to publish it
as a usable standalone app, additional work has to be done.

  * (recommended: create `frontend/jupyter/Dashboard.py` widget and put code of [demo_back.ipynb](./frontend/jupyter/demo/demo_backend.ipynb) notebook inside it. Use [aiidalab-widgets-base > StructureUploadWidget](https://github.com/aiidalab/aiidalab-widgets-base/blob/master/aiidalab_widgets_base/structures.py) as a template. Create `frontend/jupyter/Dashboard.ipynb` notebook. Use [StructureUploadWidget Demo Notebook](https://github.com/aiidalab/aiidalab-widgets-base/blob/master/structures.ipynb) as a template.)
  * Add [fileupload](https://pypi.org/project/fileupload/) to widget (again, like in StructureUploadWidget. See [binder_fileupload_test.ipynb](./frontend/jupyter/demo/binder_fileupload_test.ipynb) notebook for a demo that works with binder.)
  * Now the Web Frontend should work on Binder.
  * For publishing the app on AiiDA Lab, the app has to be registered in the [aiidalab-registry](https://github.com/aiidalab/aiidalab-registry).
    * The project code is in Python3, but aiidalab requires Python2. So the code has to first be backported by hand using the `future** package. If this takes too long, maybe try the tool [3to2](https://pypi.org/project/3to2/).
    * Use the simplest app in the registry, [aiidalab-units](https://github.com/aiidalab/aiidalab-units) as a template. Adapt code.
    * Try it out first in the [Quantum Mobile Virtual Machine](https://www.materialscloud.org/work/quantum-mobile), which has aiidalab installed and configured. Else try it in a virtual environment with [aiidalab](https://pypi.org/project/aiidalab/) installed from PyPI.
    * Register the app.
    
Note: other publishing options besides Binder and AiiDALab are listed [here](https://github.com/markusschanta/awesome-jupyter). For instance, [Google Colaboratory](http://colab.research.google.com/) is a free Notebook hosting service that allows file upload.


## Exending the code

### Use Case: HDF with DOS data included

The Fleur output HDF format is expected to change and incorporate more data. In
turn, this project's code has to be extended as well. The procedure is outlined for a
an example use case: the incorporation of DOS data into the band structure HDF
(thus eliminating the need for separate DOS CSV files). The instructions show
how to extend the preprocessor, the visualization and frontend submodules to
that scenarion.

  * Add a new output type to `hdf/output_types`, say `FleurBandDOS`. Let it
    inherit from output type `FleurBands`. If you want an output type just for
    the DOS as well, add a type `FleurDOS` and let `FleurBandDOS` inherit it.
  * Add a new recipe to `hdf/recipes` e.g. `FleurBandDOS`. Copy unchanged things
    from recipe `FleurBands`.
  * If needed, add new transforms to `hdf/input_transforms`. Adhere to the
    transform function standard there. If there are mutual dependencies, add
    them to the list in the top of the file.
  * Add a DOS data selection method to the output type `FleurBands`. The
    `DOSPlot` in `plot/base` types will need those to plot the DOS plot. Simply
    adapt from the function in `dos/reader` for the DOS CSV files, adopt the
    identical signature.
  * In the `DOSPlot` types in submodule `plot`, add a switch to the constructor
    that can distinguish the three cases (bands, bands+CSV DOS, bands+HDF DOS).
    Use the switch in the `plotDOS` methods, and for the case bands+HDF DOS, call
    your new `FleurBandDOS` function.

### Extending the Visualization (Plots)

   * The inheritance scheme is based on Python `AbstractBaseClass`. It is
     helpful to note that unlike other languages, Python does not enforce
     implemented abstract methods to have the same method signature. However, it
     is recommended to keep 
