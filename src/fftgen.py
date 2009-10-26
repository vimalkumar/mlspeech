#!/usr/bin/python
import matplotlib.pyplot as plot
import numpy as np

def Norm(ft):
  su = sum(ft)/100
  return ft / su
#  return [ x/sum for x in ft ]

def FFTdata(data):
  ot = np.fft.fft(data)
  ft = np.abs(ot[:len(ot)/2])
  return Norm(ft)

def FFTGen(data):
  l = len(data)
  #with a sampling of 6k per second
  #we get 600 points per 0.1 second
  no_of_points  = l / 600
  print no_of_points
  points = [ FFTdata(data[600*x:600*(x+1)]) for x in range(no_of_points)]
  return points

def WriteFFT(data, filename, label):
  out = open(filename, "w")
  for k in data:
    print >> out, label + " " +  " ".join([ "%d:%f"%(x[0],x[1]) for x in zip(range(1, 601), k) ])

if __name__ == "__main__":
  import sys
  import wavedata
  WriteFFT(FFTGen(wavedata.GetData(sys.argv[1])), sys.argv[2], sys.argv[3])
