# Cut Norm Approximation #

## What is the cut norm approximation? ##
The code contained herein uses SDPA to calculate a semidefinite approximation to the cut norm and then applied a rounding technique of [1]. We use the so-called infinity-to-one norm to approximate the cut norm, which is given by the quadratic integer program contained in equation (1) in [1]. The semidefinite relaxation (SDR) is given in equation (2) of [1]. We then apply the algorithm in Section 5.1 of [1] to round the SDR to a feasible solution of equation (1).

As we want to use this as a norm: ||A-B||, two inputs are required. If you want the cut norm of just a single matrix, A, make B=0 the zero matrix.

## Installation ##
The following will allow you to install SDPA on a fresh install of Ubuntu (tested on Ubuntu 14.04.3 LTS).
```bash
#dependencies
sudo apt-get update
sudo apt-get install g++ patch
sudo apt-get install gfortran
sudo apt-get install liblapack-dev liblapack-doc-man liblapack-doc liblapack-pic liblapack3 liblapack-test liblapack3gf liblapacke liblapacke-dev
sudo apt-get install libatlas-base-dev

#SDPA
cd /Desktop
mkdir SDPA
cd SDPA
wget -O sdpa_7.3.8.tar.gz http://sourceforge.net/projects/sdpa/files/sdpa/sdpa_7.3.8.tar.gz/download
tar xvfz sdpa_7.3.8.tar.gz
cd sdpa-7.3.8
./configure
make
sudo cp sdpa /usr/local/bin

#numpy and scipy
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
```

The script(s) contained in ``src`` are written in python and should run upon installation.

## Usage ##
The script ``CutnormApprox.py`` is run via
```
python CutnormApprox.py -m <MaxEntropyMatrix.csv> -s <SampleAveMatrix.csv> -o <Output.txt> -e <ExecutableForSDPA>'
```

For example, using the included test data, upon running
```
python CutnormApprox.py -m ../test/A.csv -s ../test/B.csv -o ../test/out.txt
```

The file ``out.txt`` should match the included file ``/test/AB_out.txt``.

The script ``MaxEntMatrix.py`` is run via
```bash
python MaxEntMatrix.py -c <ColumnDegrees.csv> -r <RowDegrees.csv> -o <Output.csv> -e <ExecutableForSDPA>
```

The file ``ColumnDegrees.csv`` is a csv file with a single line representing the degrees of the columns.

The file ``RowDegrees.csv`` is a csv file with a single line representing the degrees of the rows.

The file ``Output.csv`` is a csv file containing the maximum entropy matrix Z from Barvinok 2009.

## Output format ##
The output format consists of three fields: the approximation value (``#Approximation``), the pertinent part of the output of SDPA (``#Ymat``) and the rounded variable values (``#ui's (rows)`` and ``#vj's (columns)``).

The ``uis`` and ``vjs`` correspond to the ``x_i`` and ``y_i`` in equation (1) of [1].

## SDPA details ##
The SDPA algorithm [2] is based on a Mehrotra-type predictor-corrector infeasible primal-dual interior-point method with the Helmberg, Kojima, Monteiro direction. The sparse input format is utilized, and input/output files can be found with extensions ``_SDPAinput.dat-s`` and ``_SDPAoutput.txt``.


## Citations ##
[1] Alon, N., and Naor, A. "Approximating the cut-norm via Grothendieck's inequality." SIAM Journal on Computing 35.4 (2006): 787-803.

[2]Fujisawa, K., et al. "SDPA (SemiDefinite Programming Algorithm) and SDPA-GMP User’s Manual—Version 7.1.1." Department of Mathematical and Computing Sciences, Tokyo Institute of Technology. Research Reports on Mathematical and Computing Sciences Series B: Operations Research (2008).