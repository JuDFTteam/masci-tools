
SiScLab 2018 Student Project **Analysis Tool for Materials Design**. Written in Python3.

Authors: [Johannes Wasmer](https://github.com/Irratzo), [Christian Partmann](https://github.com/ChristianPartmann), and [Praneeth Katta](https://github.com/PraneethKatta).

# Overview
This subfolder `studentproject18ws` is currently a largely independent side-project accompanying the main module `masci-tools`. It was created in a student project, and consists of three submodules:

  * preprocessor: a HDF reader interface, and one implementation for Fleur band structure simulation output
  * visualization: a plotting interface, and one implementation for Fleur bandstructure+DOS plots
  * frontends: a Desktop GUI and a Web Dashboard (Tk and Jupyter) for interactive Fleur bandDOS plots.

A more thorough description and example use cases can be found in the project [report](./doc/report.pdf) and [presentation](./doc/presentation.pdf). 

![](./readme/web_frontend.png)

# For Frontend Users
The Desktop GUI executable can be received from the developers on request. Otherwise, it can be built using [PyInstaller](https://www.pyinstaller.org/) from this repo.

The Web Frontend is a Jupyter Dashboard. It is in experimental phase (no fileupload yet). You can try it out [here on Binder](https://mybinder.org/v2/gh/JuDFTteam/masci-tools/studentproject18ws?filepath=studentproject18w%2Ffrontend%2Fjupyter%2Fdemo%2Fbinder_demo.ipynb). You can run it locally (see developer section). If you have an [AiiDaLab account](https://aiidalab.materialscloud.org/hub/login): the dashboard is planned to be published as an app there.

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
``**


## To-do list for publishing the Web Frontend

  * (recommended: create `frontend/jupyter/Dashboard.py` widget and put code of [demo_back.ipynb](./frontend/jupyter/demo/demo_backend.ipynb) notebook inside it. Use [aiidalab-widgets-base > StructureUploadWidget](https://github.com/aiidalab/aiidalab-widgets-base/blob/master/aiidalab_widgets_base/structures.py) as a template. Create `frontend/jupyter/Dashboard.ipynb` notebook. Use [StructureUploadWidget Demo Notebook](https://github.com/aiidalab/aiidalab-widgets-base/blob/master/structures.ipynb) as a template.)
  * Add [fileupload](https://pypi.org/project/fileupload/) to widget (again, like in StructureUploadWidget. See [binder_fileupload_test.ipynb](./frontend/jupyter/demo/binder_fileupload_test.ipynb) notebook for a demo that works with binder.)
  * Now the Web Frontend should work on Binder.
  * For publishing the app on AiiDA Lab, the app has to be registered in the [aiidalab-registry](https://github.com/aiidalab/aiidalab-registry).
    * The project code is in Python3, but aiidalab requires Python2. So the code has to first be backported by hand using the `future` package. If this takes too long, maybe try the tool [3to2](https://pypi.org/project/3to2/).
    * Use the simplest app in the registry, [aiidalab-units](https://github.com/aiidalab/aiidalab-units) as a template. Adapt code.
    * Try it out first in the [Quantum Mobile Virtual Machine](https://www.materialscloud.org/work/quantum-mobile), which has aiidalab installed and configured. Else try it in a virtual environment with [aiidalab](https://pypi.org/project/aiidalab/) installed from PyPI.
    * Register the app.
    
Note: other publishing options besides Binder and AiiDALab are listed [here](https://github.com/markusschanta/awesome-jupyter). For instance, [Google Colaboratory](http://colab.research.google.com/) is a free Notebook hosting service that allows file upload.



