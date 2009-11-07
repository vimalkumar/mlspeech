#!/usr/bin/python
import os

def system(x):
  os.system("echo '" + x + "'")

def ConvertWavtoOut(wavefile, folder, label, ratio):
  system("fftgen.py %s %s/%d.out %d"%(wavefile, folder, label, label))
  system("randpick.py %s/%d.out %f %s/%d.train %s/%d.test"%(folder, label, ratio, folder, label, folder, label))

def All(folder, ratio, files):
  system("mkdir -p %s"%folder)
  for f in range(len(files)):
    ConvertWavtoOut(files[f], folder, f + 1, float(ratio))

  system("rm %s/all.train %s/all.test %s/all.model %s/all.out"%(folder, folder, folder, folder))
  system("cat %s/*.train > %s/all.train.nonscaled"%(folder, folder))
  system("cat %s/*.test > %s/all.test.nonscaled"%(folder, folder))
  system("svm-scale %s/all.train.nonscaled > %s/all.train"%(folder,folder))
  system("svm-scale %s/all.test.nonscaled > %s/all.test"%(folder,folder))
  system("svm-train %s/all.train %s/all.model"%(folder, folder))
  system("svm-predict %s/all.test %s/all.model %s/all.out"%(folder, folder, folder))

#usage run.py [-n for dry run] scratchfolder ratiofortrain:test listoffiles
if __name__ == "__main__":
  import sys
  if sys.argv[1] == "-n":
    sys.argv = sys.argv[1:]
  else:
    system = os.system

  All(sys.argv[1], sys.argv[2], sys.argv[3:])
