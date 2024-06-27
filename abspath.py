#!/usr/bin/env python3

# creates a copy of fusesoc.conf with absolute paths for easier handling outside of the installation folder
import os

inpath = "fusesoc.conf"
dir_path = os.path.dirname(os.path.realpath(inpath))
os.chdir(dir_path)

with open("fusesoc.conf",'r') as infile:
    with open ("fusesoc_abs.conf", 'w') as outfile:
        for line in infile:
            if line.startswith(('location')):
                path = line.split(" = ")
                outfile.write("location = " + os.path.realpath(path[1]))
            else:
                outfile.write(line);
        print(os.path.abspath(outfile.name))
        outfile.close()

