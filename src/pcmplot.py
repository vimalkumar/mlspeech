#!/usr/bin/python
import matplotlib.pyplot as plot
import wavedata

def PCMPlot(data):
  plot.plot(data)

if __name__ == "__main__":
  import wavedata
  import sys
  PCMPlot(wavedata.GetData(sys.argv[1]))
  plot.show()
