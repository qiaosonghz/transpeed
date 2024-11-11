cd ../
echo "tech-transp-dse-delay-transformer-transpeed.sh"
echo "batch(5) 1"
date
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-HEBO --scale Edge  --algorithm Spotlight-HEBO --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis , &
sleep 5                                                                                                              
date                                                                                                                 
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-HEBO --scale Edge  --algorithm Spotlight-HEBO --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis , &
sleep 5                                                                                                              
                                                                                                                     
date                                                                                                                 
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-HEBO --scale Edge  --algorithm Spotlight-HEBO --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis , &
sleep 5                                                                                                              
date                                                                                                                 
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-HEBO --scale Edge  --algorithm Spotlight-HEBO --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis , &
sleep 5                                                                                                              
                                                                                                                     
date                                                                                                                 
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-HEBO --scale Edge  --algorithm Spotlight-HEBO --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis , &
wait                                                                                                                 
                                                                                                                     
                                                                                                                     
echo "batch(5) 2"                                                                                                    
date                                                                                                                 
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-HEBO --scale Edge  --algorithm Spotlight-HEBO --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis , &
sleep 5                                                                                                              
date                                                                                                                 
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-HEBO --scale Edge  --algorithm Spotlight-HEBO --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis , &
sleep 5                                                                                                              
                                                                                                                     
date                                                                                                                 
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-HEBO --scale Edge  --algorithm Spotlight-HEBO --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis , &
sleep 5                                                                                                              
date                                                                                                                 
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-HEBO --scale Edge  --algorithm Spotlight-HEBO --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis , &
sleep 5                                                                                                              
                                                                                                                     
date                                                                                                                 
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-HEBO --scale Edge  --algorithm Spotlight-HEBO --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis , &
wait


cd ./ablation
