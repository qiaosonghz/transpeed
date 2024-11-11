
cd ../
echo "tech-tv-dse-run-transformer-nvdla.sh"
echo "batch(5) 1"
FeatAnalysis=$1
date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight --feat-analysis $FeatAnalysis   &
sleep 5                                                                                                                                                                                                                     
date                                                                                                                                                                                                                        
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight --feat-analysis $FeatAnalysis   &
sleep 5                                                                                                                                                                                                                     
                                                                                                                                                                                                                            
date                                                                                                                                                                                                                        
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight --feat-analysis $FeatAnalysis   &
sleep 5                                                                                                                                                                                                                     
date                                                                                                                                                                                                                        
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight --feat-analysis $FeatAnalysis   &
sleep 5                                                                                                                                                                                                                     
                                                                                                                                                                                                                            
date                                                                                                                                                                                                                        
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight --feat-analysis $FeatAnalysis   &
wait





date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight --feat-analysis $FeatAnalysis   &
sleep 5                                                                                                                                                                                                                     
date                                                                                                                                                                                                                        
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight --feat-analysis $FeatAnalysis   &
sleep 5                                                                                                                                                                                                                     
                                                                                                                                                                                                                            
date                                                                                                                                                                                                                        
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight --feat-analysis $FeatAnalysis   &
sleep 5                                                                                                                                                                                                                     
date                                                                                                                                                                                                                        
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight --feat-analysis $FeatAnalysis   &
sleep 5                                                                                                                                                                                                                     
 


cd ./ablation
