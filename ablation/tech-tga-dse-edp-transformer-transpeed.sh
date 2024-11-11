cd ../
echo "tech-tga-dse-edp-transformer-transpeed.sh"
echo "batch(5) 1"
date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                 
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                 
                                                                                                                        
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                 
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                 
                                                                                                                        
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
wait                                                                                                                    
                                                                                                                        
                                                                                                                        
echo "batch(5) 2"                                                                                                       
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                 
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                 
                                                                                                                        
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                 
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                 
                                                                                                                        
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique Spotlight-GA --scale Edge  --algorithm Spotlight-GA --dataflow searched --enable-maestro-gemm 1  &
wait


cd ./ablation
