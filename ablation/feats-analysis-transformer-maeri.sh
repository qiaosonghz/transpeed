cd ../
echo "dse-run-transformer-maeri.sh" $1
echo "batch(5) 1"
FeatAnalysis=$1
date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique MAERI --scale Edge  --sw-trials 50   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis=$FeatAnalysis &
sleep 60
date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique MAERI --scale Edge  --sw-trials 50   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis=$FeatAnalysis &
sleep 60

date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique MAERI --scale Edge  --sw-trials 50   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis=$FeatAnalysis &
sleep 60
date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique MAERI --scale Edge  --sw-trials 50   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis=$FeatAnalysis &
sleep 60

date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique MAERI --scale Edge  --sw-trials 50   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis=$FeatAnalysis &
wait

echo "batch(5) 2"
date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique MAERI --scale Edge  --sw-trials 50   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis=$FeatAnalysis &
sleep 60
date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique MAERI --scale Edge  --sw-trials 50   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis=$FeatAnalysis &
sleep 60

date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique MAERI --scale Edge  --sw-trials 50   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis=$FeatAnalysis &
sleep 60
date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique MAERI --scale Edge  --sw-trials 50   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 --feat-analysis=$FeatAnalysis &
sleep 60

date
time ./run-ae.sh single --model TRANSFORMER --target EDP --technique MAERI --scale Edge  --sw-trials 50   --sw-batch-size 1000 --dataflow searched --enable-maestro-gemm 1 &
wait


cd ./ablation
