#!/bin/bash

COMPILER=icpc
FLAGS="-std=c++11 -Wall -O3 -g"
INCLUDE="-I/lustre/home/sc004/adrianjc/puri-psi-dev-build/external/include/eigen3"
LIBS="-lpthread -lm"
$COMPILER $FLAGS $INCLUDE -o benchmark benchmark.cc $LIBS

OPT_FLAGS="-std=c++11 -Wall -O3 -g -DEIGEN_USE_MKL_ALL"
OPT_INCLUDE="-I/lustre/home/sc004/adrianjc/puri-psi-dev-build/external/include/eigen3 -I${MKLROOT}/include"
OPT_LIBS="-L${MKLROOT}/lib/intel64 -Wl,--start-group ${MKLROOT}/lib/intel64/libmkl_scalapack_lp64.a ${MKLROOT}/lib/intel64/libmkl_blacs_intelmpi_lp64.a ${MKLROOT}/lib/intel64/libmkl_intel_lp64.a ${MKLROOT}/lib/intel64/libmkl_core.a ${MKLROOT}/lib/intel64/libmkl_sequential.a -Wl,--end-group -lpthread -lm"

$COMPILER $OPT_FLAGS $OPT_INCLUDE -o benchmark_opt benchmark.cc $OPT_LIBS
