from __future__ import print_function
from __future__ import division
from matplotlib import cm

def FSqdos2D(p0='./', totonly=True, s=20, ls_ef= ':', lw_ef=1, color='', reload_data=False, clrbar=True, atoms=[], ax=None, nosave=False, noalat=False, cmap=cm.jet, noplot=False, return_data=False, pclrmesh=False, logscale=True):
    """ plotting routine for dos files """
    # import dependencies
    from numpy import loadtxt, load, save, sort, abs, log, sum, pi, linspace
    from matplotlib.pyplot import figure, plot, axvline, scatter, xlabel, ylabel, title, colorbar, axis, pcolormesh
    from matplotlib import cm
    from os import listdir
    from os.path import isdir
    from subprocess import check_output

    # read in data
    if p0[-1]!='/': p0+='/'

    ef = float(open(p0+'potential').readlines()[3].split()[1])
    if noalat:
       a0 = 1.
       alat = 1.
    else:
       alat = float(check_output('grep ALATBASIS '+p0+'inputcard', shell=True).decode('utf-8').split('=')[1].split()[0])
       a0 = 2*pi/alat/0.52918
    print(a0)

    if reload_data or 'saved_data_qdos.npy' not in sort(listdir(p0)):
       first=True
       print('reading qdos')
       j = 0 
       for i in sort(listdir(p0)):
           if 'qdos.' in i[:6] and not isdir(p0+i):
               j += 1
               iatom = int(i.replace('qdos.','').split('.')[0]) 
               if atoms==[] or iatom in atoms:
                 tmp = loadtxt(p0+i)
                 tmp[:,2:5] = tmp[:,2:5]*a0
                 print(i, iatom)
                 if first:
                     d = tmp
                     first=False
                 else:
                     d[:,5:]+=tmp[:,5:]
       if not nosave:
          save(p0+'saved_data_qdos', d)
    else:
       print('loading data')
       d = load(p0+'saved_data_qdos.npy')

    xlab = r'kx'
    ylab = r'ky'
    if a0!=1.:
         xlab = r'$k_x (\AA^{-1})$'
         ylab = r'$k_y (\AA^{-1})$'

    # plot dos
    data = abs(sum(d[:,5:], axis=1))
    if logscale: data = log(data)
    x, y = d[:,2], d[:,3]
    
    if not noplot:
      if ax==None:
         if pclrmesh:
            lx = len(set(x))
            ly = len(set(y))
            x = linspace(x.min(), x.max(), lx)
            y = linspace(y.min(), y.max(), ly)
            pcolormesh(x,y,data.reshape(lx,ly).T, cmap=cmap)
         else:
            scatter(x,y,c=data, s=s, lw=0, cmap=cmap)
         if clrbar:
            colorbar()
      else:
         ax.scatter(x,y,c=data, lw=0, cmap=cmap)
      
      # set axis labels
      if ax==None:
        xlabel(xlab)
        ylabel(ylab)
        axis('equal')

    if return_data:
       return x,y,data

