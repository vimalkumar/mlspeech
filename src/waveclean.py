#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
def WaveClean(indata):
  print indata
  s = np.abs(indata).sum(axis = 1, dtype=np.int64)
  n, bins, patches =  plt.hist(s, 100)
  print n
  print bins

  plt.show()
  select = s >= 500000
  delete = ~select
  return indata[select,:], indata[delete,:]

if "__main__" == __name__:
  import sys
  import wavedata
  fname = sys.argv[1]
  raw_data = wavedata.Read(fname)
  clean, dirty = WaveClean(raw_data)
  wavedata.Write(sys.argv[2], clean)
  wavedata.Write(sys.argv[2]+ ".rest", dirty)
