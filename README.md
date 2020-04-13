# eigen-benchmark
This repository contains a simple benchmark of the Eigen library along with a bash script to compile it.

The bash script is setup to compile two different executables, on with standard configuration and the other using an optimised setup. It was created with Intel MKL in mind, i.e. enabling Eigen to be compiled with MKL to investigate the performance benefit that provides.

If you want to use this benchmark you probably will need to alter the compile script to configure the compiler and compiler flags you want to use and the location of the Eigen library you are benchmarking. 
