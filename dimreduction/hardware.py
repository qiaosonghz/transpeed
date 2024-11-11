# -*- coding: utf-8 -*-

import argparse
import math
import copy
import random
import time

import numpy as np
import sys
sys.path.append("..")
sys.path.append("./src")
sys.path.append("../src")

from src import options
from src import interface
from src import layers
from src import space
from src import bo
from src import search_utils

# 根据 point，遍历固定其它维度，展开某一维度
def generate_dim_space(sw_space, sw_point):
    sw_dims_points = {}
    for param in sw_space.params:
        if param.name not in ['N', 'K', 'C', 'R', 'S', 'Y', 'X']:
            continue

        sw_points = []
        for dim_point in param.range:
            sw_point.set(param.name, dim_point)
            # print(f'generate_dim_space:{sw_point}')
            sw_points.append(copy.deepcopy(sw_point))
        sw_dims_points[param.name] = sw_points

    return sw_dims_points

# ./run-ae.sh single --model RESNET --target EDP --technique Spotlight --scale Edge
args = options.get_args()
args.dataflow = 'searched'

# get model layers
shapes = layers.get_shapes(args.layers, args.ignore_stride, True, args.remove_duplicate_layers)
#random_shapes = random.sample(shapes, int(len(shapes)/8))
random_shapes = shapes
print(f'random_shapes:{random_shapes}')


# get pe cluster shape
subcluster_range = []
num_levels = 2
num_pe = (args.pe_low + args.pe_high)/2
subcluster_range += list(space.get_all_combinations_v2(num_levels, num_pe, [], []))

# evalute function
eval_func = interface.get_eval_func(args)

# dict_shape_dim_size_edps = dict()

dict_dimsize_edps = dict()
dict_subcluster_edps = dict()
# 遍历硬件配置
for subcluster in subcluster_range:
    hw_point = {'num_simd_lane': 6, 'bit_width': 8, 'bandwidth': 191, 'l0_buf_size': 57344, 'l1_buf_size': 180224,
                'subclusters': subcluster}
    # 遍历模型的形状
    for shape in random_shapes:
        sw_space = space.create_software_space(args, shape[1], num_levels)
        print(f'hw_point:{hw_point},sw_space:{sw_space}')

        sw_points, feats = bo.generate_sw_batch(sw_space, hw_point, 1, [], args.dataflow)

        # random_points = random.sample(sw_points, int(len(sw_points) / 8))
        # 根据 point，遍历固定其它维度，展开某一维度
        sw_dims_points = generate_dim_space(sw_space, sw_points[0])
        for sw_dim, sw_points in sw_dims_points.items():
            print(f'dims_sw_points sw_dim:{sw_dim}, sw_points:{sw_points}')

            tiles = []
            edps =[]
            ## 按照K/Y/.../ 其中某一维度展开的point
            for sw_point in sw_points:
                print(f'sw_point_dim sw_dim:{sw_dim},dim:{sw_point.get(sw_dim)},sw_point:{sw_point}')
                assert(len(sw_point.get(sw_dim)) >0)
                cost = search_utils.run_maestro_tvm(args, eval_func, shape, hw_point, sw_point, num_levels)

                edp = np.iinfo(np.int64).max
                if cost is not None:
                    print(f'notnone cost:{cost},sw_dim:{sw_dim},sw_point:{sw_point}')
                    edp = cost['OverallEnergy'] * cost['ExactRunTime']
                    delay = cost['ExactRunTime']

                # else :
                #     print(f'none cost:{cost},sw_dim:{sw_dim},sw_point:{sw_point}')
                #     retry = 0
                #     while retry < 1:
                #         cost = search_utils.run_maestro_tvm(args, eval_func, shape, hw_point, sw_point, num_levels)
                #         time.sleep(0.1)
                #         if cost is not None:
                #             edp = cost['OverallEnergy'] * cost['ExactRunTime']
                #             delay = cost['ExactRunTime']
                #             print(f'retry ok:{retry},cost:{cost}')
                #             break
                #         retry = retry + 1

                edps.append(edp)

            print(f'(len_edp):{len(edps)},np.product_tiles:{np.product(sw_point.get(sw_dim))},sw_points:{sw_points}')
            # norm_edps = np.array((10 * edps/ min(edps)).astype(int))

            # 将edps转换为NumPy数组
            edps = np.array(edps)

            # 计算norm_edps
            min_edps = np.min(edps)
            norm_edps =  (edps / min_edps)
            norm_edps = norm_edps.astype(int)

            prev_edps = dict_dimsize_edps.get('sw_dim' + str(np.product(sw_point.get(sw_dim))))
            if prev_edps != None:
                norm_edps = norm_edps + prev_edps
            dict_dimsize_edps[sw_dim + str(np.product(sw_point.get(sw_dim)))] = norm_edps

            # num = dict_dimsize_num_edps.get(sw_dim + str(np.product(tiles)))
            # if num == None:
            #     num = 1
            # else:
            #     num += 1
            # dict_dimsize_num_edps[sw_dim + str(np.product(tiles))] = num
            #print(f'sw_point_dim sw_dim:{sw_dim}:,enum_len:{len(tiles)},value:{tiles},cost_edp:{edps}')

print(f'dict_dimsizeedps:{dict_dimsize_edps}')
print(f'dict_dimsize_num_edps:{dict_dimsize_num_edps}')
#print(f'subcluster_range len:{len(subcluster_range)}')