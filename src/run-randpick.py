#!/usr/bin/python

from common import *

def All(folder, ratio, files):
  setup_tmp_folder(folder)
  for f in files:
    label = infer_label_from_file_name(f) 
    sample_file = tmp_file_prefix(f) + ".labeled"
    create_labeled_samples(f,folder,sample_file,label)
    # Split the samples to training & test files depending on the ratio given
    execute("randpick.py %s/%s %s %s/%s %s/%s"%(folder, sample_file, ratio,folder, train_fname(f),folder,test_fname(f)))
  train_and_test(folder)

if __name__ == "__main__":
  import sys
  usage = "[-n]? TmpFolder TestTrainSplitRatio WavFiles+"
  argv = process_args(sys.argv,3,[],usage)
  All(argv[1],argv[2],argv[3:])
