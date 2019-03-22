#!/usr/bin/env python

# by Philipp Ruessmann July 2016

from __future__ import print_function
from __future__ import division
from builtins import str
from builtins import range
from numpy import array, sum, sqrt, log, abs, loadtxt, zeros_like, shape
from matplotlib.pyplot import plot, figure, subplot, show, ion, title, suptitle, legend, gca, ioff, axvline, gcf
import subprocess, sys, os, time


print()
print("  ########  start script rms_tracker  ########")
print("  please give input path and some options:")
print("  available options are: 0 = rms")
print("                         1 = total energy")
print("                         2 = charge neutrality")
print("                         3 = total moment")
print()
print("  if last given option is -1 then no refreshing is done and plots are only generated once")
print()
print("  after the options there is the possibility to give the 'nodos' option which prevents the plotting of the dos if 'dos.atom*' files are there")
print()
print("  input might look like this:")
print("    for self refreshing plot of rms charge neutrality and moment: ./rms_tracker.py ./path/ 0 2 3")
print("    for non refreshing plot of rms and total energy without dos plot: ./rms_tracker.py ./path/ 0 1 -1 nodos")
print()
print("  default values: ./rms_tracker.py ./path/ 0 1 2 3")


if len(sys.argv)>1:
	allpaths = sys.argv[1]
        # create list of paths from input
        allpath = []
        for path0 in allpaths.split(','):
           outfile_found = False
           for file in ['out', 'out_kkr']:
              if file in os.listdir(path0):
                 outfile_found = True
                 outfile = file
           if outfile_found:
              if path0=='.' or path0=='./':
                 path0 = os.getcwd()
    	      if path0[-1]!='/':
	         path0 += '/'
              allpath.append(path0)
           else:
              print("WARNING: file 'out' not found in",path0)
        if allpath==[]:
           print("no file 'out' found")
           sys.exit()

        if len(sys.argv)>2:
           nopt = len(sys.argv[2:])
           opt = sys.argv[2:]
           if len(opt[-1])<=2:
              dos='dos.atom1' in os.listdir(path0)
           else:
              dos=False
              nopt = nopt-1
              opt = opt[:-1]
           opt = [int(i) for i in opt]
           print(opt)
           if opt[-1]==-1:
              refresh = False
              nopt = nopt-1
              opt = opt[:-1]
           else:
              refresh = True
        else:
           nopt = 4
           opt = [0,1,2,3]
           refresh = True
           if len(sys.argv[-1])<=2:
              dos='dos.atom1' in os.listdir(path0)
           else:
              dos=False
           
else:
	print('Please give input path')
	sys.exit()

# consistency check and names
names = []
for i in opt:
   if i not in [0,1,2,3]:
      print('Found non existing option:',i)
      sys.exit()
   else:
      if i==0:
          names.append('rms error')
      elif i==1:
          names.append('total energy')
      elif i==2:
          names.append('neutrality')
      elif i==3:
          names.append('total moment')

# print input
print()
print("  your input options:", opt, "; refresh=", refresh,"; DOS=",dos)
print("  path(s):",allpath)
print()




def read_rms_data(path0):
   global opt, nopt
   ### rms
   try:
      f = subprocess.check_output('grep aver '+path0+outfile,shell=True).decode('utf-8').split('\n')
      rms = array([float((i.split()[-1]).replace('D','e').replace('\n','')) for i in f if i!=''])
   except:
      rms = []
   
   ### charge neutrality
   try:
      f = subprocess.check_output('grep neutr '+path0+outfile,shell=True).decode('utf-8').split('\n')
      neut = array([float((i.split()[-1]).replace('D','e').replace('\n','')) for i in f if i!=''])
   except:
      neut = []
   # check if neutrality info is available (not there in case of impurity code output)
   if len(neut)<len(rms) and 2 in opt:
        nopt = nopt-1
        j = 0
        for i in range(nopt+1):
           if opt[i]==2: j=i
        print('removing option', opt.pop(j), names.pop(j))

   ### read total energy
   try:
      f = subprocess.check_output("grep 'TOTAL ENERGY' "+path0+outfile,shell=True).decode('utf-8').split('\n')
      etot = array([float((i.split()[-1]).replace('D','e').replace('\n','')) for i in f if i!=''])
   except:
      etot = []
   
   ### moment 
   try:
      f = subprocess.check_output("grep 'L m' "+path0+outfile,shell=True).decode('utf-8').split('\n')
      mom = array([float((i.split()[-1]).replace('D','e').replace('\n','')) for i in f if i!=''])
   except:
      mom = []
   # check if moment info is available
   if len(mom)<len(rms) and 3 in opt:
        nopt = nopt-1
        for i in range(nopt+1):
           if opt[i]==3: j=i
        print('removing option', opt.pop(j), names.pop(j))
   else:
      try:
         f = subprocess.check_output("grep 'ITERATION ' "+path0+outfile,shell=True).decode('utf-8').split('\n')
         tmp = array([float((i.split()[1]).replace('D','e').replace('\n','')) for i in f if 'SCF' not in i and i!=''])
      except:
         tmp=[]
      if tmp!=[] and 'out_magneticmoments' in os.listdir(path0):
         it = int(tmp[-1])
         tmp = loadtxt(path0+'out_magneticmoments')
         ncls = len(tmp)//it
         tmp = tmp[::ncls,:3]
         tmpmomx = tmp[:,0]
         tmpmomy = tmp[:,1]
         tmpmomz = tmp[:,2]
         tmpmom = mom
         mom = array([tmpmom, tmpmomx,tmpmomy,tmpmomz])
      else:
         inp = open(path0+'inputcard').readlines()
         natyp = -1
         for iline in range(len(inp)):
            if 'NATYP' in inp[iline]:
               natyp = iline
         if natyp==-1:
            for iline in range(len(inp)):
               if 'NAEZ' in inp[iline]:
                  natyp = iline
            natyp = int(inp[natyp].split('NAEZ=')[1])
         else:
            natyp = int(inp[natyp].split('NATYP=')[1])
         try:
            tmp2 = subprocess.check_output("grep 'm_spin' "+path0+outfile+" -A"+str(natyp), shell=True).decode('utf-8').replace('TOT','').split('\n')
            if tmp2!='':
              tmp2 = tmp2#[-natyp-1:]
              tmp2 = array([float(i.split()[2]) for i in tmp2 if i!='' and 'dn' not in i and i!='--'])
              tmp2 = tmp2.reshape(-1,natyp)
              mom = array([mom]+[tmp2[:,i] for i in range(len(tmp2[0]))])
         except:
           tmpmom, tmpmomx, tmpmomy, tmpmomz = mom,mom,mom,mom
           mom = array([tmpmom, tmpmomx,tmpmomy,tmpmomz])
  
   return rms,neut,mom,etot


# turn interactive mode on (needed for figures to appear immediately in while loop)
ion()

rms = [[] for i in range(len(allpath))]
neut = [[] for i in range(len(allpath))]
etot = [[] for i in range(len(allpath))]
mom = [[] for i in range(len(allpath))]
istart = [True for i in range(len(allpath))]

while(True):
   for ipath0 in range(len(allpath)):
      path0 = allpath[ipath0]
      l0 = len(rms[ipath0])
      rms[ipath0],neut[ipath0],mom[ipath0],etot[ipath0] = read_rms_data(path0)
 
      if len(rms[ipath0])>l0:
         ### fig 1 for plots of values from option
         figure(ipath0)
         figure(ipath0).clf()

         # give path name to figure
         gcf().canvas.set_window_title(allpath[ipath0])
 
         for i in range(nopt):
            # choose data according to option
            if opt[i]==0:
                data = rms[ipath0] 
            elif opt[i]==1:
                data = etot[ipath0] 
            elif opt[i]==2:
                data = neut[ipath0]
            elif opt[i]==3:
                data = mom[ipath0] 
 
            # choose appropriate subplot according to number of options
            if nopt==1:
               subplot(1,2,1+i)
            elif nopt==2:
               subplot(2,2,1+i)
            elif nopt==3:
               subplot(2,3,1+i)
            elif nopt==4:
               subplot(2,4,1+i)
 
            # plot data in linear scale
            title(names[i])
            if opt[i]==3:
               clrs = ['b','g','r','y','m','c','k']
               for j in range(len(data)-1,-1,-1):
                  plot(data[j],'x--') #+clrs[j])
            else:
               plot(data,'x--')
 
            # substract reference for Etot and mom
            if len(data)>1 and opt[i] in [1,3]:
               if opt[i]==3 and len(data[0])>1:
                  datanew = zeros_like(data)[:,:-1]
                  for j in range(len(data[:,0])):
                     datanew[j,:] = (data[j,:]-data[j,-1])[:-1]
                  data = datanew
               else:
                  data = (data-data[-1])[:-1]
 
            #  plot log scale if data is not always 0 
            if (abs(data).any()>0):
               if nopt==1:
                  subplot(1,2,1+i+nopt)
               elif nopt==2:
                  subplot(2,2,1+i+nopt)
               elif nopt==3:
                  subplot(2,3,1+i+nopt)
               elif nopt==4:
                  subplot(2,4,1+i+nopt)
               if opt[i] in [1,3]:
                  name = 'change in '+names[i]
               else:
                  name = names[i]+', log scale'
               title(name)
               if opt[i]==3:
                  for j in range(len(data)-1,-1,-1):
                     plot(abs(data[j]),'x--') #+clrs[j])
               else:
                  plot(abs(data),'x--')
               gca().set_yscale('log')
            try:
               t_iter=subprocess.check_output('grep Iter '+path0+'out_timing.000.txt', shell=True).decode('utf-8').split('\n')[-2].split()[-1]
               t_iter = '%5.2f min'%(float(t_iter)/60)
            except:
               t_iter='no time info for last iteration'
            suptitle(time.ctime()+', time in last iteration: '+t_iter)

     
         ### fig 2 for DOS plots
         if dos:
            figure(ipath0+1000)
            figure(ipath0+1000).clf()
            j = 0
            for i in os.listdir(path0):
               if len(i)>8 and 'dos.atom'==i[:8]:
                  tmpi = int(i.replace('dos.atom',''))
                  if j<=tmpi:
                     j = tmpi
            
            if len(rms[ipath0])>1 and not istart[ipath0]:
                subplot(1,2,2)
                title('previous iteration')
                for i in range(len(d_old)):
                   d = d_old[i]
                   lab = i
                   plot(d[:,0],sum(d[:,1:], axis=1), '-', label=lab)
                legend() 
                ef = float(open(path0+'potential').readlines()[3].split()[1])
                axvline(ef)
                subplot(1,2,1)
            else:
                subplot(1,1,1)
            title('current iteration')
            d_old = []
            for i in range(j):
                d = loadtxt((path0+'dos.atom%i'%(i+1)))
                lab = i
                plot(d[:,0],sum(d[:,1:], axis=1), '-', label=lab)
                d_old.append(d)
                istart[ipath0] = False
            legend() 
            ef = float(open(path0+'potential').readlines()[3].split()[1])
            axvline(ef)
            suptitle(time.ctime())
 
      figure(ipath0).canvas.draw()
      figure(ipath0).canvas.flush_events()
     
      if dos:
         figure(ipath0+1000).canvas.draw()
         figure(ipath0+1000).canvas.flush_events()
 
      dobreak=False
      if refresh:
         time.sleep(2)
      else:
         # turn off interactive mode and exit while loop
         if path0==allpath[-1]:
            dobreak=True
   if dobreak:
      break

ioff()
show()
