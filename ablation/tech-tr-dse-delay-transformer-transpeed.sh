
cd ../
echo "tech-tr-dse-delay-transformer-transpeed.sh"
echo "batch(5) 1"
date
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-R --scale Edge  --algorithm Spotlight-R --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                 
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-R --scale Edge  --algorithm Spotlight-R --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                 
                                                                                                                        
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-R --scale Edge  --algorithm Spotlight-R --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                 
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-R --scale Edge  --algorithm Spotlight-R --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                 
                                                                                                                        
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-R --scale Edge  --algorithm Spotlight-R --dataflow searched --enable-maestro-gemm 1  &
wait                                                                                                                    
                                                                                                                        
                                                                                                                        
echo "batch(5) 2"                                                                                                       
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-R --scale Edge  --algorithm Spotlight-R --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                 
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-R --scale Edge  --algorithm Spotlight-R --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                 
                                                                                                                        
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-R --scale Edge  --algorithm Spotlight-R --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                 
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-R --scale Edge  --algorithm Spotlight-R --dataflow searched --enable-maestro-gemm 1  &
sleep 5                                                                                                                 
                                                                                                                        
date                                                                                                                    
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique Spotlight-R --scale Edge  --algorithm Spotlight-R --dataflow searched --enable-maestro-gemm 1  &
wait



cd ./ablation
