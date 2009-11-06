#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

def smooth(n):
  return [ n[0] + n[1] ] + [ n[x-1] + n[x] + n[x +1] for x in range(1,len(n)-1) ] + [ n[-2] + n[-1] ]


def WaveClean(indata, mindp, maxdp):
  print indata
  s = np.abs(indata).sum(axis = 1, dtype=np.int64)
  n, bins, patches =  plt.hist(s, 100)
  print n
  print bins
  sm = smooth(n)
  print len(n), len(sm), len(bins)
  plt.plot(bins[:-1], sm)

  cs = np.cumsum(n)
  size = cs[-1]
  print "size : ", size
  print "left : ", size * mindp
  print "right : ", size * maxdp


  leftindex = np.searchsorted(cs, size * mindp)
  print leftindex
  rightindex = np.searchsorted(cs, size * maxdp)
  print rightindex
  ind = np.argmin(sm[leftindex:rightindex])
  ind = ind + leftindex
  print "cutting at ", ind, bins[ind]

  plt.plot([bins[ind]]*50, range(50))
  plt.plot([bins[leftindex]]*50, range(50))
  plt.plot([bins[rightindex]]*50, range(50))

  plt.show()
  select = s >= bins[ind]
  delete = ~select
  return indata[select,:], indata[delete,:]

if "__main__" == __name__:
  import sys
  import wavedata
  fname = sys.argv[1]
  raw_data = wavedata.Read(fname)
  mindp = 0.05
  maxdp = 0.30
  if len(sys.argv) > 3:
    mindp = float(sys.argv[3])

  if len(sys.argv) > 4:
    maxdp = float(sys.argv[4])

  clean, dirty = WaveClean(raw_data, mindp, maxdp)
  wavedata.Write(sys.argv[2], clean)
  wavedata.Write(sys.argv[2]+ ".rest", dirty)
