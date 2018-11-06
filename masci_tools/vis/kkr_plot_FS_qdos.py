from matplotlib import cm



def dosplot(p0='./', totonly=True, color='', label='', marker='', lw=2, ms=5, ls='-', ls_ef= ':', lw_ef=1, units='Ry', noefline=False, interpol=False, allatoms=False, onespin=False, atoms=[], lmdos=False, lm=[], nofig=False, scale=1.0, shift=0, normalized=False, xyswitch=False, efcolor='', return_data=False, xscale=1., xshift = 0.0, yshift = 0.0, filled=False, spins=2):
    """ plotting routine for dos files """
    # import dependencies
    from numpy import loadtxt, sort, array, sum
    from matplotlib.pyplot import figure, plot, axvline, xlabel, ylabel, ion, title, figure, fill_between, axhline
    from os import listdir
    from os.path import isdir

    ion()

    # read in data
    if p0[-1]<>'/': p0+='/'
    #if 'rel' in units: ef = float(open(p0+'potential').readlines()[3].split()[1])
    ef = float(open(p0+'potential').readlines()[3].split()[1])
    first=True
    for i in sort(listdir(p0)):
        if (((i[:8]=='dos.atom' and 'interpol' not in i) and not interpol) or (interpol and i[:17]=='dos.interpol.atom')) or ('out_ldos.atom' in i and 'out_lmdos.atom' not in i and not interpol) or ('out_ldos.interpol.atom' in i and 'out_lmdos.interpol.atom' and interpol) and not isdir(p0+i):
          if lmdos:
             i = i.replace('out_ldos.','out_lmdos.')
          if not onespin or 'spin'+str(spins) not in i:
            iatom = i.replace('dos.','').replace('interpol.','').replace('atom','').replace('out_l','').replace('=','').replace('m','').split('_')[0]
            if atoms==[] or int(iatom) in atoms:
              tmp = loadtxt(p0+i)
              print p0+i

              # set units
              if 'rel' in units:
                tmp[:,0] = tmp[:,0]-ef
              if 'eV' in units:
                tmp[:,0] = tmp[:,0]*13.6
                tmp[:,1:] = tmp[:,1:]/13.6

              tmp[:,0] = tmp[:,0]*xscale+xshift
              tmp[:,1] = tmp[:,1] + yshift

              if allatoms:
                 sgn = 1
                 if 'spin2' in i: sgn=-1
                 # plot dos
                 if totonly:
                    if color=='':
                       if first:
                          if not nofig: figure()
                       plot(tmp[:,0],sgn*tmp[:,1], marker+ls, label=label+str(i), lw=lw, ms=ms)
                    else:
                       if not nofig: figure()
                       if filled:
                          fill_between(tmp[:,0],sgn*tmp[:,1], color=color, label=label)
                       else:
                          plot(tmp[:,0],sgn*tmp[:,1], marker+ls, color=color, label=label, lw=lw, ms=ms)
                 else:
                    if not nofig and sgn==1: figure()
                    if color=='':
                       if lm==[]:
                          if filled:
                             fill_between(tmp[:,0],sgn*tmp[:,1:])
                          else:
                             plot(tmp[:,0],sgn*tmp[:,1:], marker+ls, lw=lw, ms=ms)
                       else:
                          for ilm in lm:
                             lmname=label+' '
                             if ilm==1: lmname+='s'
                             if ilm==2: lmname+='p_x'
                             if ilm==3: lmname+='p_y'
                             if ilm==4: lmname+='p_z'
                             if ilm==5: lmname+='d_{x^2-y^2}'
                             if ilm==6: lmname+='d_{xz}'
                             if ilm==7: lmname+='d_{z^2}'
                             if ilm==8: lmname+='d_{yz}'
                             if ilm==9: lmname+='d_{xy}'
                             if ilm==10: lmname+='f_{-3}'
                             if ilm==11: lmname+='f_{-2}'
                             if ilm==12: lmname+='f_{-1}'
                             if ilm==13: lmname+='f_{0}'
                             if ilm==14: lmname+='f_{1}'
                             if ilm==15: lmname+='f_{2}'
                             if ilm==16: lmname+='f_{3}'
                             plot(tmp[:,0],sgn*tmp[:,1+ilm], marker+ls, lw=lw, ms=ms, label=lmname)
                    else:
                       if lm==[]:
                          if filled:
                             fill_between(tmp[:,0],sgn*tmp[:,1:], color=color)
                          else:
                             plot(tmp[:,0],sgn*tmp[:,1:], marker+ls, color=color, lw=lw, ms=ms)
                       else:
                          for ilm in lm:
                             lmname=label+' '
                             if ilm==1: lmname+='s'
                             if ilm==2: lmname+='p_x'
                             if ilm==3: lmname+='p_y'
                             if ilm==4: lmname+='p_z'
                             if ilm==5: lmname+='d_{x^2-y^2}'
                             if ilm==6: lmname+='d_{xz}'
                             if ilm==7: lmname+='d_{z^2}'
                             if ilm==8: lmname+='d_{yz}'
                             if ilm==9: lmname+='d_{xy}'
                             if ilm==10: lmname+='f_{-3}'
                             if ilm==11: lmname+='f_{-2}'
                             if ilm==12: lmname+='f_{-1}'
                             if ilm==13: lmname+='f_{0}'
                             if ilm==14: lmname+='f_{1}'
                             if ilm==15: lmname+='f_{2}'
                             if ilm==16: lmname+='f_{3}'
                             plot(tmp[:,0],sgn*tmp[:,1+ilm], marker+ls, lw=lw, ms=ms, label=lmname, color=color)
                    title(label+' '+i)

              #sum data
              if first:
                  d = tmp
                  d[:,1:]=d[:,1:]*scale
                  first=False
              else:
                  d[:,1:]+=tmp[:,1:]*scale

    # set units and axis labels
    if 'eV' in units:
       ef = ef*13.6
    if 'rel' in units:
       ef = 0

    #if lmdos:
    #   if lm<>[]:
    #      d = d[:,[0,1]+list(array(lm)+1)]
    #   d[:,1] = sum(d[:,2:], axis=1)
    if lm<>[]:
       d = d[:,[0,1]+list(array(lm)+1)]
    d[:,1] = sum(d[:,2:], axis=1)


    if normalized:
      d[:,1:] = d[:,1:]/(d[:,1:]).max()

    xlab = r'E (Ry)'
    ylab = r'DOS (states/Ry)'
    if units=='eV':
       xlab = r'E (eV)'
       ylab = r'DOS (states/eV)'
    elif units=='eV_rel':
       xlab = r'E-E_F (eV)'
       ylab = r'DOS (states/eV)'
    elif units=='Ry_rel':
       xlab = r'E-E_F (Ry)'
       ylab = r'DOS (states/Ry)'

    # plot dos
    if not allatoms:
      if totonly:
        if color=='':
          if xyswitch:
           plot(d[:,1],d[:,0]+shift, marker+ls, label=label, lw=lw, ms=ms)
          else:
           plot(d[:,0]+shift,d[:,1], marker+ls, label=label, lw=lw, ms=ms)
        else:
         if xyswitch:
           if filled:
              fill_between(d[:,1],d[:,0]+shift, color=color, label=label)
           else:
              plot(d[:,1],d[:,0]+shift, marker+ls, color=color, label=label, lw=lw, ms=ms)
         else:
           if filled:
              fill_between(d[:,0]+shift,d[:,1], color=color, label=label)
           else:
              plot(d[:,0]+shift,d[:,1], marker+ls, color=color, label=label, lw=lw, ms=ms)

      else:
        if color=='':
         if xyswitch:
           plot(d[:,1:],d[:,0]+shift, marker+ls, lw=lw, ms=ms)
         else:
           plot(d[:,0]+shift,d[:,1:], marker+ls, lw=lw, ms=ms)
        else:
         if xyswitch:
           if filled:
              fill_between(d[:,1], d[:,0]+shift, color=color)
           else:
              plot(d[:,1:],d[:,0]+shift, marker+ls, color=color, lw=lw, ms=ms)
         else:
           if filled:
              fill_between(d[:,0]+shift, d[:,1], color=color)
           else:
              plot(d[:,0]+shift,d[:,1:], marker+ls, color=color, lw=lw, ms=ms)
        title(label)

    # plot fermi level
    if not noefline:
       if color<>'' and efcolor=='': efcolor=color
       if efcolor=='':
         if xyswitch:
          axhline(ef, ls=ls_ef, lw=lw_ef, color='grey')
         else:
          axvline(ef, ls=ls_ef, lw=lw_ef, color='grey')
       else:
         if xyswitch:
          axhline(ef, color=efcolor, ls=ls_ef, lw=lw_ef)
         else:
          axvline(ef, color=efcolor, ls=ls_ef, lw=lw_ef)

    
    # set axis labels
    if xyswitch:
      ylabel(xlab)
      xlabel(ylab)
    else:
      xlabel(xlab)
      ylabel(ylab)

    if return_data:
        return d,ef


#######################################################################################################


def dispersionplot(p0='./', totonly=True, s=20, ls_ef= ':', lw_ef=1, units='Ry', noefline=False, color='', reload_data=False, clrbar=True, logscale=True, nosave=False, atoms=[], ratios=False, atoms2=[], noscale=False, newfig=False, cmap=None, alpha=1.0, qcomponent=-1, clims=[], xscale=1., raster=True, atoms3=[], alpha_reverse=False, return_data=False, xshift=0, yshift=0):
    """ plotting routine for dos files """
    # import dependencies
    from numpy import loadtxt, load, save, log, abs, sum, sort, pi, shape
    from matplotlib.pyplot import figure, plot, axvline, scatter, axhline, xlabel, ylabel, ion, title, colorbar, pcolormesh, cm
    from os import listdir, getcwd
    from os.path import isdir, getctime
    from time import ctime
    from subprocess import check_output

    if cmap==None:
       cmap = cm.viridis
    if newfig: figure()

    ion()

    # read in data
    if p0[-1]<>'/': p0+='/'
    ef = float(open(p0+'potential').readlines()[3].split()[1])
    alat = float(check_output('grep ALATBASIS inputcard', shell=True).split('=')[1].split()[0])
    a0 = 2*pi/alat/0.52918
    if noscale: a0 = 1.
    if reload_data or 'saved_data_dispersion.npy' not in sort(listdir(p0)):
       first=True
       first2=True
       first3=True
       print 'reading qdos'
       j = 0
       for i in sort(listdir(p0)):
           if 'qdos.' in i[:5] and not isdir(p0+i):
               iatom = i.replace('qdos.','').split('.')[0]
               if atoms==[] or int(iatom) in atoms:
                  j += 1
                  print j,p0,i
                  tmp = loadtxt(p0+i)
                  tmp[:,2:5] = tmp[:,2:5]
                  if first:
                      d = tmp
                      first=False
                  else:
                      d[:,5:]+=tmp[:,5:]
               if ratios and (atoms2==[] or int(iatom)):
                  j += 1
                  print j,p0,i, 'atoms2'
                  tmp = loadtxt(p0+i)
                  tmp[:,2:5] = tmp[:,2:5]
                  if first2:
                      d2 = tmp
                      first2=False
                  else:
                      d2[:,5:]+=tmp[:,5:]
               if (atoms3==[] or int(iatom) in atoms3) and ratios:
                  j += 1
                  print j,p0,i, 'atoms3'
                  tmp = loadtxt(p0+i)
                  tmp[:,2:5] = tmp[:,2:5]
                  if first3:
                      d3 = tmp
                      first3=False
                  else:
                      d3[:,5:]+=tmp[:,5:]
       if not nosave: save(p0+'saved_data_dispersion', d)
    else:
       print 'loading data'#,'qdos files created on:',ctime(getctime('qdos.01.1.dat')), '.npy file created on:', ctime(getctime('saved_data_dispersion.npy'))
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
       x = [[i for i in range(len(d)/el)] for j in range(el)]
    elif qcomponent<>-1:
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
    if ratios and atoms3<>[]:
       colors[:,-1] = abs(sum(d3[:,5:], axis=1))/abs(sum(d3[:,5:], axis=1)).max()
       if alpha_reverse:
          colors[:,-1] = 1 - colors[:,-1]
    if ratios:
       scatter(x,y,s=s, lw=0, c=colors, cmap=cmap, rasterized=raster)
    else:
       scatter(x,y,c=data, s=s, lw=0, cmap=cmap, alpha=alpha, rasterized=raster)
    if clims<>[]: clim(clims[0], clims[1])
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
    if totonly:
       title(getcwd())

    if return_data:
       data = abs(sum(d[:,5:], axis=1))
       data2 = abs(sum(d2[:,5:], axis=1))
       data3 = abs(sum(d3[:,5:], axis=1))
       return x, y, data, data2, data3




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
    if p0[-1]<>'/': p0+='/'

    ef = float(open(p0+'potential').readlines()[3].split()[1])
    if noalat:
       a0 = 1.
       alat = 1.
    else:
       alat = float(check_output('grep ALATBASIS inputcard', shell=True).split('=')[1].split()[0])
       a0 = 2*pi/alat/0.52918
    print a0

    if reload_data or 'saved_data_qdos.npy' not in sort(listdir(p0)):
       first=True
       print 'reading qdos'
       j = 0 
       for i in sort(listdir(p0)):
           if 'qdos.' in i[:6] and not isdir(p0+i):
               j += 1
               iatom = int(i.replace('qdos.','').split('.')[0]) 
               if atoms==[] or iatom in atoms:
                 tmp = loadtxt(p0+i)
                 tmp[:,2:5] = tmp[:,2:5]*a0
                 print i, iatom
                 if first:
                     d = tmp
                     first=False
                 else:
                     d[:,5:]+=tmp[:,5:]
       if not nosave:
          save(p0+'saved_data_qdos', d)
    else:
       print 'loading data'
       d = load(p0+'saved_data_qdos.npy')

    xlab = r'kx'
    ylab = r'ky'
    if a0<>1.:
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

