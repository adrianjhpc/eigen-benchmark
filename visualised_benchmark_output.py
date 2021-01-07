#!/usr/bin/python3
#===============================================================
# v1.0 - Initial version, Adrian Jackson
#===============================================================
#
#----------------------------------------------------------------------
# Copyright 2021 EPCC, The University of Edinburgh
#
# eigen-benchmark is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# eigen-benchmark is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with eigen-benchmark.  If not, see <http://www.gnu.org/licenses/>.
#----------------------------------------------------------------------
#

# This program parses the output for runs of the eigen benchmark to produce graphs of the runtime
# compared to the matrix size for the experiments undertaken.
#
# This is a very fragile program as it is closely tied to both the output of the benchmark
# and the output of batch scripts to run the program. In particular it expects the eigen
# benchmark to output lines like this:
#
# Matrix size: 2000000 iterations: 10 runtime: 0.149294 seconds
#
# As we manuallly parse these lines and expect the matrix size and runtime to be in the places
# in the sentence as above.
#
# We also expect the program to be run in a batch script that has output like this:
#
# Name: MKL
# Matrix size: 2000000 iterations: 10 runtime: 0.049684 seconds
# Matrix size: 3000000 iterations: 10 runtime: 0.055209 seconds
# Matrix size: 4000000 iterations: 10 runtime: 0.043492 seconds
# Matrix size: 5000000 iterations: 10 runtime: 0.094315 seconds
#
#
# That is to say, the first line is the name of the benchmark (i.e. what you want
# the legend label to be for the graph produced) and this is expected to be "Name: "
# followed the text you want in the legend. Subsequent lines are outputs of the individual
# benchmark runs, with an empty line separating separate benchmark sets. Extraneous lines
# in the output file processed by this program, or lines with differing formats, will likely
# cause this program to crash or work incorrectly.
# A more robust approach to this would be to use some self consistent output language for the
# benchmark data, such as XML or YAML.


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys


def readfile(filename):
    array = []
    temparray = None;
    f = open(filename, "r")
    for line in f:
        line = line.rstrip()
        if(line is "" or line is "\n" or line is "\r"):
            if not (temparray is None):
                array.append(temparray)
        elif "Name: " in line:
            temparray = []
            text = line.split(" ")
            concat_text  = " ".join(text[1:])
            temparray.append(concat_text)
        elif("Matrix" in line):
            words = line.split(" ")
            temparray.append([words[2],words[4],words[6]])
        else:
            print("else '" + line + "'")

    if not (temparray is None):
        array.append(temparray)

    return array
            

if(len(sys.argv) != 2):
    print("You need to provide the name of the file with the data in it to be processed")
    exit(0)

filename = sys.argv[1]

print("Processing " + filename)

data_array = readfile(filename)

fig = plt.figure()
ax = plt.axes()
    
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.Set2.colors)

x_points = None
first_run = True

for element in data_array:
    data_part = element[1:]
    if(first_run):
        x_points = np.array([item[0] for item in data_part], dtype=int)
        first_run = False
    runtimes = np.array([item[2] for item in data_part], dtype=float)
    plt.scatter(x_points, runtimes, label=element[0])

plt.ylabel('Runtime (seconds)')
plt.xlabel('Matrix size')
plt.xticks(rotation=90)

plt.legend(loc="upper left")

plt.tight_layout()

plt.savefig(filename+"_output.png",format="png")

