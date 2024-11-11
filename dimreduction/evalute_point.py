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

args = options.get_args()
args.dataflow = 'searched'

eval_func = interface.get_eval_func(args)

shape = ['RESNET50_CONV3_4_2', {'N': 1, 'K': 128, 'C': 128, 'R': 3, 'S': 3, 'X': 28, 'Y': 28}, {'N': 1, 'K': 1, 'C': 1, 'R': 1, 'S': 1, 'X': 1, 'Y': 1}, 'CONV']
hw_point ={'num_simd_lane': 6, 'bit_width': 8, 'bandwidth': 191, 'l0_buf_size': 57344, 'l1_buf_size': 180224, 'subclusters': [214, 1]}
sw_point = {'K':[1,1,128],'C':[2,32,2],'N':[1,1,1],'X':[1,7,4],'Y':[1,28,1],'R':[1,3,1],'S':[3,1,1],'l0_spatial_dim':'Y','l1_spatial_dim':'K'}
cost = search_utils.run_maestro_tvm(args, eval_func, shape, hw_point, sw_point, 2)
print(cost)
