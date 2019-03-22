from __future__ import print_function
from __future__ import division
from builtins import range
from matplotlib import cm

def dispersionplot(p0='./', totonly=True, s=20, ls_ef= ':', lw_ef=1, units='eV_rel', noefline=False, 
                   color='', reload_data=False, clrbar=True, logscale=True, nosave=False, atoms=[], 
                   ratios=False, atoms2=[], noscale=False, newfig=False, cmap=None, alpha=1.0, 
                   qcomponent=-2, clims=[], xscale=1., raster=True, atoms3=[], alpha_reverse=False, 
                   return_data=False, xshift=0, yshift=0, plotmode='pcolor', ptitle=None):
    """ plotting routine for qdos files - dispersion (E vs. q) """
    # import dependencies
    from numpy import loadtxt, load, save, log, abs, sum, sort, pi, shape, array
    from matplotlib.pyplot import figure, plot, axvline, scatter, axhline, xlabel, ylabel, title, colorbar, pcolormesh, cm
    from os import listdir, getcwd
    from os.path import isdir, getctime
    from time import ctime
    from subprocess import check_output

    if cmap==None:
       cmap = cm.viridis
    if newfig: figure()

    # read in data
    if p0[-1]!='/': p0+='/'
    ef = float(open(p0+'potential').readlines()[3].split()[1])
    alat = float(check_output('grep ALATBASIS '+p0+'inputcard', shell=True).decode('utf-8').split('=')[1].split()[0])
    a0 = 2*pi/alat/0.52918
    if noscale: a0 = 1.
    if reload_data or 'saved_data_dispersion.npy' not in sort(listdir(p0)):
       first=True
       first2=True
       first3=True
       print('reading qdos')
       j = 0
       for i in sort(listdir(p0)):
           if 'qdos.' in i[:5] and not isdir(p0+i):
               iatom = i.replace('qdos.','').split('.')[0]
               if atoms==[] or int(iatom) in atoms:
                  j += 1
                  print(j,p0,i)
                  tmp = loadtxt(p0+i)
                  tmp[:,2:5] = tmp[:,2:5]
                  if first:
                      d = tmp
                      first=False
                  else:
                      d[:,5:]+=tmp[:,5:]
               if ratios and (atoms2==[] or int(iatom)):
                  j += 1
                  print(j,p0,i, 'atoms2')
                  tmp = loadtxt(p0+i)
                  tmp[:,2:5] = tmp[:,2:5]
                  if first2:
                      d2 = tmp
                      first2=False
                  else:
                      d2[:,5:]+=tmp[:,5:]
               if (atoms3==[] or int(iatom) in atoms3) and ratios:
                  j += 1
                  print(j,p0,i, 'atoms3')
                  tmp = loadtxt(p0+i)
                  tmp[:,2:5] = tmp[:,2:5]
                  if first3:
                      d3 = tmp
                      first3=False
                  else:
                      d3[:,5:]+=tmp[:,5:]
       if not nosave: save(p0+'saved_data_dispersion', d)
    else:
       print('loading data')#,'qdos files created on:',ctime(getctime('qdos.01.1.dat')), '.npy file created on:', ctime(getctime('saved_data_dispersion.npy'))
       d = load(p0+'saved_data_dispersion.npy')

    d[:,2:5] = d[:,2:5]*a0
    if ratios: d2[:,2:5] = d2[:,2:5]*a0
    if ratios: d3[:,2:5] = d3[:,2:5]*a0

    # set units and axis labels
    if 'eV' in units:
       d[:,0] = d[:,0]*13.6
       d[:,5:] = d[:,5:]/13.6
       ef = ef*13.6
    if 'rel' in units:
       d[:,0] = d[:,0]-ef
       ef = 0
    if ratios:
      if 'eV' in units:
       d2[:,0] = d2[:,0]*13.6
       d2[:,5:] = d2[:,5:]/13.6
       ef = ef*13.6
      if 'rel' in units:
       d2[:,0] = d2[:,0]-ef
       ef = 0

    ylab = r'E (Ry)'
    xlab = r'k'
    if units=='eV':
       ylab = r'E (eV)'
    elif units=='eV_rel':
       ylab = r'E-E_F (eV)'
    elif units=='Ry_rel':
       ylab = r'E-E_F (Ry)'

    # plot dos
    if totonly:
       data = abs(sum(d[:,5:], axis=1))
    else:
       data = abs(d[:,5:])
    if logscale: data = log(data)
    x, y = xscale*sum(d[:,2:5], axis=1), d[:,0]
    if qcomponent==-2:
       el = len(set(d[:,0]))
       x = array([[i for i in range(len(d)//el)] for j in range(el)])
    elif qcomponent!=-1:
       x = xscale*d[:,2:5][:,qcomponent]

    if xshift != 0:
       x += xshift

    if ratios:
       data = abs(sum(d[:,5:], axis=1))
       data2 = abs(sum(d2[:,5:], axis=1))
       data = (data-data2)/(data+data2)

    if yshift != 0:
       y += yshift
    
    colors = cmap(data/data.max())
    if ratios and atoms3!=[]:
       colors[:,-1] = abs(sum(d3[:,5:], axis=1))/abs(sum(d3[:,5:], axis=1)).max()
       if alpha_reverse:
          colors[:,-1] = 1 - colors[:,-1]
    if ratios:
       if plotmode=='scatter':
           scatter(x,y,s=s, lw=0, c=colors, cmap=cmap, rasterized=raster)
       else:
           lx = len(set(x.reshape(-1)))
           ly = len(set(y.reshape(-1)))
           pcolormesh(data.reshape(ly,lx), cmap=cmap, rasterized=raster)
    else:
       if plotmode=='scatter':
           scatter(x,y,c=data, s=s, lw=0, cmap=cmap, alpha=alpha, rasterized=raster)
       else:
           lx = len(set(x.reshape(-1)))
           ly = len(set(y.reshape(-1)))
           pcolormesh(x.reshape(ly,lx), y.reshape(ly,lx), data.reshape(ly,lx), cmap=cmap, alpha=alpha, rasterized=raster)
    if clims!=[]: clim(clims[0], clims[1])
    if clrbar: colorbar()

    # plot fermi level
    if not noefline:
       if color=='':
          axhline(ef, ls=ls_ef, lw=lw_ef, color='grey')
       else:
          axhline(ef, color=color, ls=ls_ef, lw=lw_ef)
    
    # set axis labels
    xlabel(xlab)
    ylabel(ylab)

    # print path to title
    if totonly and ptitle is None:
       title(getcwd())
    else:
       title(ptitle)

    if return_data:
       data = abs(sum(d[:,5:], axis=1))
       data2 = abs(sum(d2[:,5:], axis=1))
       data3 = abs(sum(d3[:,5:], axis=1))
       return x, y, data, data2, data3


