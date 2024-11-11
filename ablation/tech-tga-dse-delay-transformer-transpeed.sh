cd ../
echo "tech-tga-dse-delay-transformer-transpeed.sh"
echo "batch(5) 1"
date
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                   
date                                                                                                                      
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                   
                                                                                                                          
date                                                                                                                      
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                   
date                                                                                                                      
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                   
                                                                                                                          
date                                                                                                                      
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
wait                                                                                                                      
                                                                                                                          
                                                                                                                          
echo "batch(5) 2"                                                                                                         
date                                                                                                                      
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                   
date                                                                                                                      
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                   
                                                                                                                          
date                                                                                                                      
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                   
date                                                                                                                      
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                   
                                                                                                                          
date                                                                                                                      
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
wait


cd ./ablation
