
SiScLab 2018 Student Project **Analysis Tool for Materials Design**

Authors: [Johannes Wasmer](https://github.com/Irratzo), [Christian Partmann](https://github.com/ChristianPartmann), and [Praneeth Katta](https://github.com/PraneethKatta).

# Overview
This subfolder `studentproject18ws` is currently a largely independent side-project accompanying the main module `masci-tools`. It was created in a student project, and consists of three submodules:
  * preprocessor: a HDF reader interface, and one implementation for Fleur band structure simulation output
  * visualization: a plotting interface, and one implementation for Fleur bandstructure+DOS plots
  * frontends: a Desktop GUI and a Web Dashboard (Tk and Jupyter) for interactive Fleur bandDOS plots.

A more thorough description and example use cases can be found in the project [report](./readme/web_frontend.png) and [presentation](./readme/web_frontend.png). 

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

## To-do list for publishing the Web Frontend

  * bla



