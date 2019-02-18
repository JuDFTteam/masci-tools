This is work in progress.

# Installation
## With conda (recommended)
- [Install Anaconda (3 recommended)](https://www.anaconda.com/download)
- Install the environment `masci-stupro` with the necessary and recommended dependencies:
```bash
conda create -f environment.yml
```
## With pip (untested)
```bash
git clone <repo>
cd <repo>/studentproject18ws
pip install venv # to create your environment
source venv/bin/activate # to enter the virtual environment
pip install -r requirements_pip.txt # to install the requirements in the current environment
```

# Try out experimental Frontends
## Web - Jupyter
Try it out on [Binder](https://mybinder.org/v2/gh/JuDFTteam/masci-tools/studentproject18ws)!

Under `studentproject18ws/frontend/jupyter/demo`, there is a demo notebook.
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
### Note on committing Jupyter Notebooks
If changes to a notebook shall be committed, best clear all output cells before.
## Desktop - Tkinter
The only guaranteed way right now to get the Desktop GUI running, is by using the `masci-tools` folder to create a 
project in an IDE (e.g. PyCharm), and then run the file `studentproject18ws/frontend/tkinter/gui.py`.





