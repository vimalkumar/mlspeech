
import os,subprocess,sys

# Classification Labels
OBJ_TO_LABEL={
    "a":1, 
    "e":2,
    "i":3,
    "o":4,
    "u":5
}

LABEL_TO_OBJ = dict([(OBJ_TO_LABEL[obj],obj) 
                     for obj in OBJ_TO_LABEL.keys()])

def get_label(obj):
    return OBJ_TO_LABEL[obj]

def from_label(label):
    return LABEL_TO_OBJ[label]

# This infers the label from file name 
# Files names for label obj "a" can be:  a.wav, a.mpg, song-a.wav, -a.wav
def infer_label_from_file_name(file_name):
    file_name = os.path.basename(file_name)
    file_noext, ext = os.path.splitext(file_name)
    return get_label(file_noext.split("-")[-1:][0])

#**** Common functionality for shell based execution ****
def dummy_execute(command):
    print command

def execute(command):
    python_path=os.path.pathsep.join(sys.path)
    shell_path=os.environ.get("PATH")
    full_path=python_path + os.path.pathsep + shell_path
    subprocess.call(command, env = {"PATH":full_path}, shell=True)

def process_args(argv,min_args,mandatory_opts,usage):
    import sys
    cmd = argv[0]
    if argv[1] == "-n":
        argv = argv[1:]
        execute = dummy_execute        
    if len(argv) < min_args or not set(mandatory_opts).issubset(argv):
        print "usage: %s %s"%(cmd,usage)
        sys.exit(1) 
    return argv

# To be used to generate identifiyable unique temp files for each sample input file
#"./a/b/c/d.wav" returns home-vimal-prog-ai-ml-git-mlspeech-data-vimal-a-b-c-d.wav
def tmp_file_prefix(orig_file):
    return "-".join(os.path.splitdrive(os.path.abspath(orig_file))[1].split(os.path.sep)[1:])

def setup_tmp_folder(folder):
    execute("rm -rf %s"%(folder))
    execute("mkdir -p %s"%folder)

def train_fname(orig_file):
    return tmp_file_prefix(orig_file) + ".train"

def test_fname(orig_file):
    return tmp_file_prefix(orig_file) + ".test"

def create_labeled_samples(wavefile,folder,sample_file,label):
    execute("fftgen.py %s %s/%s %d"%(wavefile, folder,sample_file, label))

# Main training and testing script
# Input
#    Assuming the following extensions for the files in the folder
#      training files: *.train
#      test files: *.test
# Output:
#      test result: all.out, accuracy is printed in stdout
#      svm movel: all.model
def train_and_test(folder):
  execute("cat %s/*.train > %s/all.train.nonscaled"%(folder, folder))
  execute("cat %s/*.test > %s/all.test.nonscaled"%(folder, folder))
  execute("svm-scale %s/all.train.nonscaled > %s/all.train"%(folder,folder))
  execute("svm-scale %s/all.test.nonscaled > %s/all.test"%(folder,folder))
  execute("svm-train %s/all.train %s/all.model"%(folder, folder))
  execute("svm-predict %s/all.test %s/all.model %s/all.out"%(folder, folder, folder))


