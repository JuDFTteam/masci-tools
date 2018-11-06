#!/usr/bin/env ipython

# by David Bauer 2012
# edited by Philipp Ruessmann 2014
# added averaging of spin up/down by Philipp Sep. 2015

from numpy import *
from sys import argv,exit

mode='pot'
if len(argv)==2:
  if argv[1]=='shape' or argv[1]=='shapefun':
    mode='shape'

if mode=='pot':
  data = open('potential').readlines()
elif mode=='shape':
  data = open('shapefun').readlines()


def iatom2shape():
  atominfolines = open('inputcard').readlines()
  print len(atominfolines)
  starti = -1
  for i in range(len(atominfolines)):
    if 'ATOMINFO' in atominfolines[i]:
      starti=i
  icount=2
  listatom=[]
  while (not ('---' in atominfolines[starti+icount])):
    print
    listatom.append(int(atominfolines[starti+icount].split()[8]))
    icount = icount +1
  return listatom

def iatom2shape_2016():
  inputcard = open('inputcard').readlines()
  try:
     natyp = [ int(line.split('=')[1].split()[0]) for line in inputcard if 'NAEZ' in line][0]
     print 'natyp v1:', natyp
  except:
     natyp = [ int(line.split('=')[1].split()[0]) for line in inputcard if 'NATYP' in line][0]
     print 'natyp v2:', natyp
  try:
     ntc_iline = [iline for iline in range(len(inputcard)) if '<SHAPE>' in inputcard[iline]][0]
     ntc_line_start = inputcard[ntc_iline].find('<SHAPE>')
  except:
     ntc_iline = [iline for iline in range(len(inputcard)) if 'NTC' in inputcard[iline]][0]
     ntc_line_start = inputcard[ntc_iline].find('NTC')
  listatom=[]
  for iatom in range(natyp):
    line = inputcard[ntc_iline+iatom+1]
    ntc  =  int(line[ntc_line_start:].split()[0])
    listatom.append(ntc)
  return listatom

def check_potstart(str1,shape_ver='new'):
  if mode=='pot':
    #check1='POTENTIAL' in str1
    check1='exc:' in str1
  elif mode=='shape':
    if shape_ver=='new':
        check1='Shape number' in str1
    else:
        check1= (len(str1)==11)
  else:
    print 'mode error'
    exit()
  return check1


def read_pot_values(lstart, lstop):
  tmpdat = data[lstart:lstop]
  #print shape(tmpdat)
  #first find start of potential values
  il, lpotstart = 0, -1
  for i in range(25):
    tmplen = len(tmpdat[i])
    #print tmplen
    if tmplen==81 and lpotstart==-1:
      lpotstart = il
    il += 1
  #now lpotstart contains position where values begin
  #next step is to read in values which can later be modified
  potential = []
  potentialheader = tmpdat[:lpotstart]
  lm = 0
  for il in range(lpotstart,len(tmpdat)):
    s = tmpdat[il]
    s = s.replace('D','E')
    snew = []
    if il==lpotstart:
      dl = len(s)/4
      print dl
      print len(s)
    snew.append(s[:dl])
    if len(s)>21:
      snew.append(s[dl:2*dl])
    if len(s)>41:
      snew.append(s[2*dl:3*dl])
    if len(s)>61:
      snew.append(s[3*dl:-1])
    print snew
    potential.append(snew)
  #now array potential contains potential values as float numbers
  return potentialheader,potential

def pot2newdata(header, pot):
  """ convert potential data back to string file format """
  out = header
  for i in pot:
    if len(i)==1:
      out.append(i[0])
    else:
      tmps = ''
      for ii in i:
        tmps+=ii.replace('E','D').replace('e','D')
      tmps += '\n'
      out.append(tmps)
  return out

def calc_coulomb_spin_pot(pot1, pot2):
  """ calculate spin mixing and coulomb part of potential """
  # first do consistency checks
  if len(pot1)<>len(pot2):
    exit('ERROR: potential1 and potential2 inconsistent in calc_coulomb_spin_pot')
  # now calculate coulomb part and spin part and save them in vc and vs
  vc, vs = [],[]
  for i in range(len(pot1)):
    if len(pot1)<>len(pot2):
      exit('ERROR: potential1 and potential2 inconsistent in calc_coulomb_spin_pot')
    tmp1, tmp2 = pot1[i], pot2[i]
    tmpvc, tmpvs = [],[]
    if len(tmp1[0])>=20:
      for ii in range(len(tmp1)):
        tmpvc.append( '%20.13e'%((float(tmp1[ii])+float(tmp2[ii]))/2.) )
        tmpvs.append( '%20.13e'%((float(tmp1[ii])-float(tmp2[ii]))/2.) )
    else:
      tmpvc.append( tmp1[0] )
      tmpvs.append( tmp1[0] )
    vc.append(tmpvc)
    vs.append(tmpvs)
  # now vc and vs contain spin and coulomb part of potential
  return vc,vs


def combine_potentials(pot1, pot2, alpha):
  """ combine potentials: pot_out = pot1 + alpha*pot2 """
  # first do consistency checks
  if len(pot1)<>len(pot2):
    exit('ERROR: potential1 and potential2 inconsistent in combine_potentials')
  # now calculate coulomb part and spin part and save them in vc and vs
  potout = []
  for i in range(len(pot1)):
    if len(pot1)<>len(pot2):
      exit('ERROR: potential1 and potential2 inconsistent in combine_potentials')
    tmp1, tmp2 = pot1[i], pot2[i]
    tmppot = []
    if len(tmp1[0])>=20:
      for ii in range(len(tmp1)):
        tmppot.append( '%20.13e'%(float(tmp1[ii])+alpha*float(tmp2[ii])) )
    else:
      tmppot.append( tmp1[0] )
    potout.append(tmppot)
  return potout


def combine_header(head1, head2, alpha):
  print len(head1),len(head2),alpha
  # combine core energies
  headnew1 = head1[:7]
  ne = int(head1[6].split()[0])
  ne2 = int(head2[6].split()[0])
  if ne<>ne2:
    exit('ERROR: number of core levels inconsistent')
  for i in range(ne):
    tmp1 = head1[7+i].replace('D','E').split()
    tmp2 = head2[7+i].replace('D','E').split()
    tmp = ('%5i%20.11e\n'%(int(tmp1[0]), ((float(tmp1[1])+float(tmp2[1]))/2. + alpha*((float(tmp1[1])-float(tmp2[1]))/2.)) )).replace('e','D')
    headnew1.append( tmp )
  print 'rest length',len(head1[7+ne:])
  for i in range(len(head1[7+ne:])):
    headnew1.append(head1[7+ne:][i])
  print ne
  return headnew1



index1=[];index2=[]
for i in range(len(data)):
  if check_potstart(data[i]):
    index1.append(i)
    if len(index1)>1: index2.append(i-1)
index2.append(i)

# read shapefun if old style is used
if mode=='shape' and len(index1)<1:
        index1=[];index2=[]
        for i in range(len(data)):
          if check_potstart(data[i],shape_ver='old'):
            index1.append(i)
            if len(index1)>1: index2.append(i-1)
        index2.append(i)

print index1
print index2

print 'Potential file read'
print 'found %i potentials in file'%len(index1)
print ''

tempsave=-1
order=range(len(index1))
while 1:
#while 0:
  for i in range(len(order)):
    #print '%3i'%i,data[index1[order[i]]][:-1]
    if 'GENERAL POTENTIAL' in data[index1[order[i]]][:-1]:
       print '%3i'%i,data[index1[order[i]]][:-1],data[index1[order[i]]+1][:-1]
    else:
       print '%3i'%i,data[index1[order[i]]][:-1]
  print '  ***************************'
  print '  *  ( 0) Stop and Save         *'
  print '  *  ( 1) Delete                *'
  print '  *  ( 2) Copy                  *'
  print '  *  ( 3) Cut                   *'
  print '  *  ( 4) Paste                 *'
  print '  *  ( 5) Copy  [multiline]     *'
  print '  *  ( 6) Cut   [multiline]     *'
  print '  *  ( 7) Del   [multiline]     *'
  print '  *  ( 8) Paste [multiple]      *'
  print '  *  ( 9) swap lines            *'
  print '  *  (10) read scoef nonmag host*'
  print '  *  (11) flip magnetic moments *'
  print '  *  (12) Input new list        *'
  print '  *  (13) Nspin=1 -> 2  :       *'
  print '  *  (14) read scoef mag host   *'
  print '  *  (15) average spin up/down  *'
  print '  *  (16) scale up mag. moment  *'
  print '  ***************************'

  mode1=int(raw_input('Input: '))
  print mode1
  if mode1==0: break
  if mode1==1:
    row1=int(raw_input('Row number:'))
    del order[row1]
  if mode1==2:
    row1=int(raw_input('Row number:'))
    tempsave=order[row1]
  if mode1==3:
    row1=int(raw_input('Row number:'))
    tempsave=order[row1]
    del order[row1]
  if mode1==4:
    if type(tempsave)==type(1):
      if tempsave!=-1:
        row1=int(raw_input('Paste before number:'))
        order.insert(row1,tempsave)
      else:
        print 'nothing in temp, copy first'
        raw_input('Continue')
    else:
      row1=int(raw_input('Paste before number:'))
      print row1
      print tempsave
      for i in reversed(range(len(tempsave))):
        order.insert(row1,tempsave[i])
  if mode1==5:
    row1=int(raw_input('Row number [start]:'))
    row2=int(raw_input('Row number [stop] :'))
    tempsave=range(row1,row2+1)
  if mode1==6:
    row1=int(raw_input('Row number [start]:'))
    row2=int(raw_input('Row number [stop] :'))
    tempsave=range(row1,row2+1)
    for i in range(len(tempsave)):
      del order[row1]
  if mode1==7:
    row1=int(raw_input('Row number [start]:'))
    row2=int(raw_input('Row number [stop] :'))
    for i in range(row1,row2+1):
      del order[row1]
  if mode1==8:
    if type(tempsave)==type(1):
      if tempsave!=-1:
        row1=int(raw_input('Paste before number:'))
        row2=int(raw_input('How many times?:'))
        for i in range(row2):
          order.insert(row1,tempsave)
      else:
        print 'nothing in temp, copy first'
        raw_input('Continue')
    else:
      row1=int(raw_input('Paste before number:'))
      row2=int(raw_input('How many times?:'))
      for i in range(row2):
        for i in reversed(range(len(tempsave))):
          order.insert(row1,tempsave[i])
  if mode1==9:
        row1=int(raw_input('Swap line: '))
        row2=int(raw_input('with line: '))
        ordertemp=order[row1]
        order[row1]=order[row2]
        order[row2]=ordertemp
  if mode1==10:
        nspintemp = int(raw_input('Double potential (1=no,2=yes) '))
        natomtemp = int(open('scoef').readlines()[0])
        filedata=open('scoef').readlines()[1:natomtemp+1]
        listnew=[]
        if mode=='shape':
          shapeorder = iatom2shape_2016()
          print shapeorder
        for line in filedata:
          if (len(line.split())>1):
            if mode=='pot':
              listnew.append(int(line.split()[3])-1)
              if (nspintemp==2): listnew.append(int(line.split()[3])-1)
            elif mode=='shape':
              listnew.append(shapeorder[int(line.split()[3])-1]-1)
        print 'new order list'
        print listnew
        print len(listnew)
        order = listnew
  if mode1==11:
        npot=len(order)
        if npot%2!=0:
          print'number of potentials is odd';exit()
        print range(0,len(order),2)
        for i in range(0,len(order),2):
          ordertemp=order[i]
          order[i]=order[i+1]
          order[i+1]=ordertemp
  if mode1==12:
        listnew=raw_input('New list :').split()
        makeorder= lambda x: int(x)-1
        order=map(makeorder,listnew)
  if mode1==13:
        ordernew=[]
        for item in order:
          ordernew.append(item)
          ordernew.append(item)
        order=ordernew
  if mode1==14:
        filedata=open('scoef').readlines()[1:]
        listnew=[]
        if mode=='shape':
          shapeorder = iatom2shape_2016()
          print shapeorder
        for line in filedata:
          if (len(line.split())>1):
            if mode=='pot':
              listnew.append( (int(line.split()[3])-1)*2 )
              listnew.append( (int(line.split()[3])-1)*2+1 )
            elif mode=='shape':
              listnew.append(shapeorder[int(line.split()[3])-1]-1)
        print 'new order list'
        print listnew
        print len(listnew)
        order = listnew
  if mode1==15:
        print 'mode 15 chosen'
        if len(order)%2<>0:
          exit('ERROR: odd number of potentials')
        for i in range(len(order)/2):
          print i
          head1, pot1 = read_pot_values(index1[2*i+0],index2[2*i+0])
          head2, pot2 = read_pot_values(index1[2*i+1],index2[2*i+1])
          if head1[1:7]<>head2[1:7]:
            print head1, head2
            exit('ERROR: potential header for spin up and down do not match!!!')
          vc, vs = calc_coulomb_spin_pot(pot1, pot2)
          head1[0] = head1[0].replace('up','averaged')
          head1[0] = head1[0].replace('UP','averaged')
          head1[0] = head1[0].replace('down','averaged')
          head1[0] = head1[0].replace('DOWN','averaged')
          headnew1 = combine_header(head1, head2, 0)
          headnew2 = combine_header(head1, head2, 0)
          print len(headnew1),len(head1),len(head2)
          newdat1 = pot2newdata(headnew1,vc)
          newdat2 = pot2newdata(headnew2,vc)
          print len(headnew1),len(head1),len(head2), len(newdat1), len(newdat2), len(vc), len(vs)
          print i, index1, index2
          data[index1[2*i]:index2[2*i]] = newdat1
          data[index1[2*i+1]:index2[2*i+1]] = newdat2
  if mode1==16:
        if len(order)%2<>0:
          exit('ERROR: odd number of potentials')
        print 'scale magnetic moment up: newpot_1/2 = (v_1+v_2)/2 +/- alpha*(v_1-v_2)/2'
        alpha = float(raw_input('alpha: '))
        for i in range(len(order)/2):
          print i
          head1, pot1 = read_pot_values(index1[2*i+0],index2[2*i+0])
          head2, pot2 = read_pot_values(index1[2*i+1],index2[2*i+1])
          if head1[1:7]<>head2[1:7]:
            print head1, head2
            exit('ERROR: potential header for spin up and down do not match!!!')
          vc, vs = calc_coulomb_spin_pot(pot1, pot2)
          pot_new1 = combine_potentials(vc,vs, alpha)
          pot_new2 = combine_potentials(vc,vs,-alpha)
          headnew1 = combine_header(head1, head2, alpha)
          headnew2 = combine_header(head2, head1, alpha)
          print len(headnew1),len(head1),len(head2)
          newdat1 = pot2newdata(headnew1,pot_new1)
          newdat2 = pot2newdata(headnew2,pot_new2)
          print len(headnew1),len(head1),len(head2), len(newdat1), len(newdat2), len(vc), len(vs)
          print i, index1, index2
          data[index1[2*i]:index2[2*i]] = newdat1
          data[index1[2*i+1]:index2[2*i+1]] = newdat2



datanew=[]
for i in range(len(order)):
  for ii in range(index1[order[i]], index2[order[i]]+1  ):
    datanew.append(data[ii])
if mode=='pot':
  open('potential_new','w').writelines(datanew)
elif mode=='shape':
  # add header to shapefun_new
  tmp = datanew
  datanew = []
  datanew.append('   %i\n' %(len(order)))
  datanew.append('  1.000000000000E+00\n')
  datanew += tmp
  open('shapefun_new','w').writelines(datanew)
else:
  print 'error';exit()

