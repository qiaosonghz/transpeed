
cd ../
echo "tech-tv-dse-run-transformer-nvdla.sh"
echo "batch(5) 1"
date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight-V &
sleep 5
date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight-V &
sleep 5

date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight-V &
sleep 5
date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight-V &
sleep 5

date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight-V &
wait


echo "batch(5) 2"
date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight-V &
sleep 5
date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight-V &
sleep 5

date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight-V &
sleep 5
date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight-V &
sleep 5

date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --algorithm Spotlight-V &
wait



cd ./ablation