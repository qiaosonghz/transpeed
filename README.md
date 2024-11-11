## Setup
the following packages are required to be installed natively:
1. A C++ compiler that supports the C++17 standard
2. Boost libraries
3. Python 3.9 or later
4. Anaconda
5. SCons build system

Create an Anaconda environment and activate it.  Then build MAESTRO and its
wrapper.
```
conda env create -f environment.yml
```

## activate 
and its wrapper.  Spotlight should be run (see the following section) within the
Docker container as well.
```
conda activate transpeed
scons -j`nproc`
```

# Running TranSpeed

### MSE for ALBERT 
```
./run-ae.sh single --model TRANSFORMER --target EDP --technique Transpeed --scale Edge --hw-point "{'num_simd_lane':14,'bit_width':8,'bandwidth':186,'l0_buf_size':172032,'l1_buf_size':204800,'subclusters':[286,1]}" --sw-trials 200 --enable-maestro-gemm 1        --sw-batch-size 1000 
```

### DSE for ALBERT 
```
./run-ae.sh single --model TRANSFORMER --target EDP --technique Transpeed --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 
```













































































