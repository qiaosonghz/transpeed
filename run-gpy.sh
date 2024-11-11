echo "run-ae.sh --sw-trials 200 --scalable-sw-bo gpy --sw-inducing-num 32"
date && time ./run-ae.sh single --model ALL --target EDP --technique Spotlight --scale Edge --hw-point "{'num_simd_lane':14,'bit_width':8,'bandwidth':186,'l0_buf_size':172032,'l1_buf_size':204800,'subclusters':[286,1]}" --sw-trials 200 --scalable-sw-bo gpy --sw-inducing-num 32 && date
sleep 60

echo "run-ae.sh --sw-trials 200 --scalable-sw-bo gpy --sw-inducing-num 32"
date && time ./run-ae.sh single --model ALL --target EDP --technique Spotlight --scale Edge --hw-point "{'num_simd_lane':14,'bit_width':8,'bandwidth':186,'l0_buf_size':172032,'l1_buf_size':204800,'subclusters':[286,1]}" --sw-trials 200 --scalable-sw-bo gpy --sw-inducing-num 32 && date
sleep 60


echo "run-ae.sh --sw-trials 400 --scalable-sw-bo gpy --sw-inducing-num 32"
date && time ./run-ae.sh single --model ALL --target EDP --technique Spotlight --scale Edge --hw-point "{'num_simd_lane':14,'bit_width':8,'bandwidth':186,'l0_buf_size':172032,'l1_buf_size':204800,'subclusters':[286,1]}" --sw-trials 400 --scalable-sw-bo gpy --sw-inducing-num 32 && date
sleep 60

echo "run-ae.sh --sw-trials 400 --scalable-sw-bo gpy --sw-inducing-num 32"
date && time ./run-ae.sh single --model ALL --target EDP --technique Spotlight --scale Edge --hw-point "{'num_simd_lane':14,'bit_width':8,'bandwidth':186,'l0_buf_size':172032,'l1_buf_size':204800,'subclusters':[286,1]}" --sw-trials 400 --scalable-sw-bo gpy --sw-inducing-num 32 && date
sleep 60

echo "run-ae.sh --sw-trials 400 --scalable-sw-bo gpy --sw-inducing-num 100"
date && time ./run-ae.sh single --model ALL --target EDP --technique Spotlight --scale Edge --hw-point "{'num_simd_lane':14,'bit_width':8,'bandwidth':186,'l0_buf_size':172032,'l1_buf_size':204800,'subclusters':[286,1]}" --sw-trials 400 --scalable-sw-bo gpy --sw-inducing-num 100 && date
sleep 60

echo "run-ae.sh --sw-trials 400 --scalable-sw-bo gpy --sw-inducing-num 100"
date && time ./run-ae.sh single --model ALL --target EDP --technique Spotlight --scale Edge --hw-point "{'num_simd_lane':14,'bit_width':8,'bandwidth':186,'l0_buf_size':172032,'l1_buf_size':204800,'subclusters':[286,1]}" --sw-trials 400 --scalable-sw-bo gpy --sw-inducing-num 100 && date
sleep 60
