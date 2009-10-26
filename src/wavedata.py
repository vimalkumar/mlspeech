#!/usr/bin/python
import numpy as np

def GetData(filename):
  return np.memmap(filename, dtype='h', mode='r', offset = 44)

def WriteHeader(filename, size):
  import struct
  samples = 600 * size
  bytes = samples * 2
  CK1_size = bytes + 36
  structure = "4sI4s4sIhhIIhh4sI"
  fn = open(filename, "w")
  fn.write(struct.pack(structure, 'RIFF', CK1_size, 'WAVE', 'fmt ', 16, 1, 1, 6000, 12000, 2, 16, 'data', bytes))
  fn.close()

  



def Read(original):
  import numpy as np
  input = np.memmap(original, dtype='h', mode='r', offset = 44)
  l = input.size
  print l
  input.resize(l/600, 600) 
  return input

def WriteBody(filename, content):
  fp = np.memmap(filename, dtype='h', mode='r+', offset = 44, shape=tuple([len(content), 600]))
  fp[:] = content
  del fp

def Write(filename, content):
  WriteHeader(filename, len(content))
  WriteBody(filename, content)


if "__main__" == __name__:
  import sys
  d = GetData(sys.argv[1])
  print "No of elements %d"%len(d)
