cd ../
echo "tech-tga-dse-run-transformer-nvdla.sh"
echo "batch(5) 1"
date
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --feat-analysis 0,1,2,4 --algorithm=Spotlight &
sleep 5
date
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --feat-analysis 0,1,2,4 --algorithm=Spotlight &
sleep 5

date
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --feat-analysis 0,1,2,4 --algorithm=Spotlight &
sleep 5
date
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --feat-analysis 0,1,2,4 --algorithm=Spotlight &
sleep 5

date
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --feat-analysis 0,1,2,4 --algorithm=Spotlight &
wait


echo "batch(5) 2"
date
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --feat-analysis 0,1,2,4 --algorithm=Spotlight &
sleep 5
date
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --feat-analysis 0,1,2,4 --algorithm=Spotlight &
sleep 5

date
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --feat-analysis 0,1,2,4 --algorithm=Spotlight &
sleep 5
date
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --feat-analysis 0,1,2,4 --algorithm=Spotlight &
sleep 5

date
time ./run-ae.sh single --model TRANSFORMER --target Delay --technique NVDLA --scale Edge  --sw-trials 100   --sw-batch-size 1000 --dataflow fixed --enable-maestro-gemm 1 --feat-analysis 0,1,2,4 --algorithm=Spotlight &
wait


cd ./ablation
