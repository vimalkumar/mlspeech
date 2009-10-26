#!/usr/bin/python
import matplotlib.pyplot as plot
import numpy as np

def FFTdata(data):
  print len(data)
  ot = np.fft.fft(data)
  ft = np.abs(ot[:len(ot)/2])
  print len(ft)
  return ft

def FFTPlot(data):
  d = FFTdata(data)
  lenth = len(d)
  plot.plot(np.r_[0:3000:(lenth*1j)], d)
  plot.show()

if __name__ == "__main__":
  import sys
  import wavedata
  FFTPlot(wavedata.GetData(sys.argv[1]))
