"""
Plotting routines for fleur density of states with and without hdf
"""
import warnings

def fleur_plot_dos(path_to_dosfile, path_to_dosfile_dn=None, hdf_group='Local',**kwargs):
   """
   Plot the density of states either from a `banddos.hdf` or text output
   """
   from masci_tools.io.io_hdf5 import read_hdf
   from masci_tools.vis.plot_methods import plot_dos, plot_spinpol_dos
   from masci_tools.util.constants import HTR_TO_EV

   if path_to_dosfile.endswith('.hdf'):
      if path_to_dosfile_dn is not None:
         warnings.warn('path_to_dosfile_dn is ignored for hdf files')
      data, attrs = read_hdf(path_to_dosfile)

      dos_data = data[hdf_group].get('DOS')

      if dos_data is None:
         raise ValueError(f"DOS entry is missing in {hdf_group} for file '{path_to_dosfile}'." 
                           ' Are you sure this is a DOS calculation?')

      energy_grid = dos_data.pop('energyGrid') * HTR_TO_EV

      if dos_data[list(dos_data.keys())[0]].shape[0] == 1:
         spin_pol = False
         dos_data_up = [data[0,...]/HTR_TO_EV for data in dos_data.values()]
      else:
         spin_pol = True
         dos_data_up = [data[0,...]/HTR_TO_EV for data in dos_data.values()]
         dos_data_dn = [data[1,...]/HTR_TO_EV for data in dos_data.values()]

      plot_label = list(dos_data.keys())

   else:
      #TODO: txt input
      raise NotImplementedError

   if spin_pol:
      plot_spinpol_dos(dos_data_up, dos_data_dn, energy_grid, plot_label=plot_label, **kwargs)
   else:
      plot_dos(dos_data_up, energy_grid, plot_label=plot_label, **kwargs)









