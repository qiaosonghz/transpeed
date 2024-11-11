import sys
sys.path.append("..")
sys.path.append("./")
sys.path.append("./src")
sys.path.append("../src")

from src import space
from src import options
from src import bo
from pyDOE2 import lhs

import numpy as np

def lhs_sample(space, sample_num):
    # 定义特征的维度
    num_dimensions = len(space.params)

    # 生成拉丁超立方采样点
    lhs_samples = lhs(num_dimensions, sample_num, criterion="center")
    points = []
    for sample in lhs_samples:
        point = space.build_point_lhs(sample)
        points.append(point)
        print(point)

    return points

args = options.DefaultArgs()
# options.get_args()
args.dataflow = 'searched'
# args.model = 'test'
# args.layers = 'resnet'
layer = eval("{'N': 1, 'K': 512, 'C': 512, 'R': 3, 'S': 3, 'X': 14, 'Y': 14}")
space = space.create_software_space(args, layer, 2)

points = lhs_sample(space, 30)
# print(points)

# l1occpys=[]
# l2occpys=[]
# for point in points:
#     l1occpy = 1
#     l2occpy = 1
#     for i in range(len(point.param_values)-2):
#         l1occpy = l1occpy * point.param_values[i][0]
#         l2occpy = l2occpy * point.param_values[i][1]
#     l2occpy = l2occpy * l1occpy
#     l1occpys.append(l1occpy)
#     l2occpys.append(l2occpy)
#     print(f'point:{point},l1occpy:{l1occpy},l2occpy:{l2occpy}')
#     print('')


# res = bo.check_smem(eval("{'K': [64, 1, 1], 'C': [1, 3, 1], 'N': [1, 1, 1], 'X': [7, 32, 1], 'Y': [1, 8, 28], 'R': [1, 1, 3], 'S': [3, 1, 1],'l0_spatial_dim': 'X', 'l1_spatial_dim': 'Y'}"),
# res = bo.check_smem(eval("{'K':[8,2,4],'C':[1,1,3],'N':[1,1,1],'X':[7,32,1],'Y':[1,56,4],'R':[1,3,1],'S':[3,1,1],'l0_spatial_dim': 'X', 'l1_spatial_dim': 'Y'}"),
res = bo.check_smem(eval("{'K':[32,1,2],'C':[3,1,1],'N':[1,1,1],'X':[1,32,7],'Y':[1,224,1],'R':[1,1,3],'S':[1,1,3],'l0_spatial_dim':'X','l1_spatial_dim':'X'}"),
                  172032, 204800)
print(res)
print(res[0]/res[1])
print(res[2]/res[3])