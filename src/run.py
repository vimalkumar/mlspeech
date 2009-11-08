#!/usr/bin/python

from common import *

def All(folder, train_files,test_files):
  setup_tmp_folder(folder)
  for f in train_files:
    label = infer_label_from_file_name(f) 
    create_labeled_samples(f,folder,train_fname(f),label)

  for f in test_files:
    label = infer_label_from_file_name(f) 
    create_labeled_samples(f,folder,test_fname(f),label)

  train_and_test(folder)


if __name__ == "__main__":
  import sys

  # Parse options
  usage = "[-n]? tmpfolder --train wavfiles+ --test wavfiles+"
  argv = process_args(sys.argv,5,["--train","--test"],usage) 
  train_idx = argv.index("--train")
  test_idx = argv.index("--test")  
  folder = argv[1]
  train_files = argv[train_idx+1:test_idx]
  test_files = argv[test_idx+1:]

  All(folder,train_files,test_files)
