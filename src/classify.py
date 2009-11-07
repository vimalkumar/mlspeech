#!/usr/bin/python


from wavedata import *
def Classify(wave, result, max):
  res = open(result).read().strip().split('\n')
  print len(res)
  print len(wave)
  return [ [ wave[x] for x in range(len(wave)) if res[x] == str(k) ] for k in range(1, max) ]

def WriteClassify(wave):
  import numpy as np
  for x in range(len(wave)):
    y = x + 1
    Write("%d.wav"%y, wave[x])

# classify.py wavefile svm-predict-output-file
if __name__ == "__main__":
  import sys
  wave = Read(sys.argv[1])
  WriteClassify(Classify(wave, sys.argv[2], 5))

