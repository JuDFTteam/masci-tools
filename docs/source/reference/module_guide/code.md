# Visualisation and Plotting

## Fleur specific Plotting

```{eval-rst}
.. automodule:: masci_tools.vis.fleur
   :members:
```

## KKR specific Plotting

```{eval-rst}
.. automodule:: masci_tools.vis.kkr_plot_FS_qdos
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.vis.kkr_plot_bandstruc_qdos
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.vis.kkr_plot_dos
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.vis.kkr_plot_shapefun
   :members:
```

## General Plotting

```{eval-rst}
.. automodule:: masci_tools.vis.parameters
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.vis.data
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.vis.helpers
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.vis.common
   :members:
```

### Matplotlib

```{eval-rst}
.. automodule:: masci_tools.vis.matplotlib_plotter
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.vis.plot_methods
   :members:
```

### Bokeh

```{eval-rst}
.. automodule:: masci_tools.vis.bokeh_plotter
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.vis.bokeh_plots
   :members:
```

# Calculation tools

```{eval-rst}
.. automodule:: masci_tools.tools.cf_calculation
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.tools.greensfunction
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.tools.greensf_calculations
   :members:
```

# IO helper functions and file parsers

## KKR related IO

```{eval-rst}
.. automodule:: masci_tools.io.kkr_params
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.io.kkr_read_shapefun_info
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.io.parsers.kkrparser_functions
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.io.parsers.voroparser_functions
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.io.parsers.kkrimp_parser_functions
   :members:
```

## Fleur related IO

### Input/Output Parser

```{eval-rst}
.. automodule:: masci_tools.io.parsers.fleur
   :members:
```

### Inputgenerator related IO

```{eval-rst}
.. automodule:: masci_tools.io.fleur_inpgen
   :members:
```

### Functions for modifying the input file

```{eval-rst}
.. automodule:: masci_tools.io.fleurxmlmodifier
   :members:
```

### Functions/Classes for loading/validating fleur XML files

```{eval-rst}
.. automodule:: masci_tools.io.parsers.fleur_schema.schema_dict
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.io.fleur_xml
   :members:
   :private-members: _EvalContext
```

### Helper functions for the `n_mmp_mat` file

```{eval-rst}
.. automodule:: masci_tools.io.io_nmmpmat
   :members:

```

## General HDF5 parser

```{eval-rst}
.. automodule:: masci_tools.io.parsers.hdf5.reader
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.io.parsers.hdf5.recipes
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.io.parsers.hdf5.transforms
   :members:

```

## Definition of default parsing tasks for fleur out.xml

```{eval-rst}
.. automodule:: masci_tools.io.parsers.fleur.default_parse_tasks
   :members:
```

```{eval-rst}
.. automodule:: masci_tools.io.parsers.fleur.task_migrations
   :members:

```

# Commandline interface (CLI)

(masci-tools-cmdline)=

```{eval-rst}
.. click:: masci_tools.cmdline.commands.root:cli
    :prog: masci_tools
    :show-nested:
```
