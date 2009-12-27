#!/usr/bin/python
from scikits.talkbox.features.mfcc import *


def MelGen(data):
  ceps = mfcc(data)[0]
  print "data len:%d, num cep samples cpes len:%d"%(len(data),len(ceps))
  return ceps

def WriteMel(data, filename, label):
  out = open(filename, "w")
  for k in data:
    print >> out, label + " " +  " ".join([ "%d:%f"%(x[0],x[1]) for x in zip(range(1, len(k)+1), k) ])

if __name__ == "__main__":
  import sys
  import wavedata
  WriteMel(MelGen(wavedata.GetData(sys.argv[1])), sys.argv[2], sys.argv[3])
