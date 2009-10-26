#!/usr/bin/python
import struct
import sys
from collections import namedtuple

structure = "4sI4s4sIhhIIhh4sI"
content = open(sys.argv[1]).read(struct.calcsize(structure))
desc_structure = namedtuple('Waveformat', \
    "CK1 CK1_size FMT \
    CK1a CK1a_size FM_a_1_uncompressed \
    CHANNELS SAMPLERATE BYTERATE ALIGN \
    BITS_per_SAMPLE CK1b CK1b_size")
out_content =  desc_structure._make(struct.unpack(structure, content))
print out_content
