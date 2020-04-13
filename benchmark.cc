/*===============================================================
 * v1.0 - Initial version, Adrian Jackson
 *===============================================================
 *
 *----------------------------------------------------------------------
 * Copyright 2020 EPCC, The University of Edinburgh
 *
 * eigen-benchmark is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * eigen-benchmark is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with cpuid.  If not, see <http://www.gnu.org/licenses/>.
 *----------------------------------------------------------------------
 */

#include <cstdio>
#include <iostream>
#include <sys/time.h>
#include <algorithm>
#include <vector>
#include <Eigen/Dense>

using namespace std;

double Compare_Times(timeval, timeval);
double Run_Eigen(int, int, Eigen::MatrixXd &A, Eigen::MatrixXd &B, int);

int main(){
    const int N = 1000000;
    const int iterations = 10;

    for(int M=2; M <= 16; M++){ 
        Eigen::MatrixXd A(N,M);
        Eigen::MatrixXd B(N,1);

        for(size_t i=0; i < A.size(); i++){
            A(i) = rand()/(1.0 + RAND_MAX);
        }

        // Perturb B
        for(size_t i=0; i < B.size(); i++) {
            B(i) += -1.0 + 2*rand()/(1.0+RAND_MAX);
        }       

        cout << "Matrix size: " << M*N << " iterations: " << iterations << " runtime: " << Run_Eigen(N, M, A, B, iterations) << " seconds" << endl;
    }

    return 0;
}

double Compare_Times(timeval t1, timeval t2){
    double t;

    t = (t2.tv_sec - t1.tv_sec) * 1000.0;      // sec to ms
    t += (t2.tv_usec - t1.tv_usec) / 1000.0;   // us to ms
    t = t / 1000.0; // ms to s
    return t;
}

double Run_Eigen(int N, int M, Eigen::MatrixXd &A, Eigen::MatrixXd &B, int iterations){
  Eigen::MatrixXd _A(N,M);
  Eigen::MatrixXd _B(N,1);
  Eigen::MatrixXd X(M,1);
  timeval t1, t2;
  double d;

  for(int i=0; i < N; i++) {
    _B(i,0) = B(i);
    for(int j=0; j < M; j++) {
      _A(i,j) = A(i,j);
    }
  }
  
  gettimeofday(&t1, NULL);
  for(int i=0; i < iterations; i++) {
    X = (_A.transpose()*_A).inverse()*(_A.transpose()*_B);
  }
  gettimeofday(&t2, NULL);
  
  d = Compare_Times(t1, t2);
  
  return d;
}
