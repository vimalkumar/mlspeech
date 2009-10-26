#!/usr/bin/python

import random
def RandPick(list, no, train, test):
  selected =   [ no > random.random() for x in range(len(list))]
  tr = [ x[0] for x in zip(list, range(len(list))) if selected[x[1]]]
  te  = [ x[0] for x in zip(list, range(len(list))) if not selected[x[1]]]
  print "Training " + str(len(tr))
  print "Testing " + str(len(te))

  train_file = open(train, "w")
  train_file.write("\n".join(tr))
  train_file.write('\n')
  train_file.close()
  
  test_file = open(test, "w")
  test_file.write("\n".join(te))
  test_file.write('\n')
  test_file.close()
 
if __name__ == "__main__":
  import sys
  list = open(sys.argv[1]).read().strip().split('\n')
  print len(list)
  RandPick(list, float(sys.argv[2]), sys.argv[3], sys.argv[4])
