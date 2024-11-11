
cd ../
echo "tech-transp-dse-edp-transformer-transpeed.sh"
echo "batch(5) 1"
FeatAnalysis=$1
date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight --scale Edge --algorithm Spotlight  --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis $FeatAnalysis  &
sleep 2                                                                                                           
date                                                                                                              
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight --scale Edge --algorithm Spotlight  --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis $FeatAnalysis  &
sleep 2                                                                                                           
                                                                                                                  
date                                                                                                              
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight --scale Edge --algorithm Spotlight  --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis $FeatAnalysis  &
sleep 2                                                                                                           
date                                                                                                              
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight --scale Edge --algorithm Spotlight  --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis $FeatAnalysis  &
sleep 2                                                                                                           
                                                                                                                  
date                                                                                                              
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight --scale Edge --algorithm Spotlight  --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis $FeatAnalysis  &
wait                                                                                                              
                                                                                                                  
                                                                                                                  
echo "batch(5) 2"                                                                                                
date                                                                                                             
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight --scale Edge --algorithm Spotlight  --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis $FeatAnalysis   &
sleep 5                                                                                                          
date                                                                                                             
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight --scale Edge --algorithm Spotlight  --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis $FeatAnalysis   &
sleep 5                                                                                                          
                                                                                                                 
date                                                                                                             
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight --scale Edge --algorithm Spotlight  --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis $FeatAnalysis   &
sleep 5                                                                                                          
date                                                                                                             
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight --scale Edge --algorithm Spotlight  --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis $FeatAnalysis   &
sleep 5                                                                                                          
                                                                                                                 
date                                                                                                             
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight --scale Edge --algorithm Spotlight  --sw-trials 100   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis $FeatAnalysis   &
wait



cd ./ablation
