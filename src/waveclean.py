#!/usr/bin/python

import numpy as np
def WaveClean(indata):
  print indata
  s = np.abs(indata).sum(axis = 1, dtype=np.int64)
  print s
  todel = [ i for i, x in enumerate(s) if x < 3000000]
  print len(s)
  print len(todel)
  cp = np.delete(indata, todel, axis = 0)
  print todel
  print cp.shape
  return cp

if "__main__" == __name__:
  import sys
  import wavedata
  fname = sys.argv[1]
  raw_data = wavedata.Read(fname)
  wavedata.Write(sys.argv[2], WaveClean(raw_data))
