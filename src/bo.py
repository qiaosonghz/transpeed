import numpy as np
import sklearn.gaussian_process as gp
import sklearn.preprocessing as pp

import space
import search_utils
import sys
import time
import traceback
from pyDOE2 import lhs

class BO:
    def __init__(self, args, warmup_iters=10, exploration_ratio=0.1, op_type='sw'):
        if args.kernel == 'linear':
            self.kernel = gp.kernels.DotProduct() + gp.kernels.WhiteKernel()
        elif args.kernel == 'matern':
            self.kernel = gp.kernels.Matern() + gp.kernels.WhiteKernel()
        elif args.kernel == 'rbf':
            self.kernel = gp.kernels.RBF() + gp.kernels.WhiteKernel()
        self.model = gp.GaussianProcessRegressor(kernel=self.kernel)
        self.train_x = []
        self.train_y = []
        self.scale_x = pp.StandardScaler()
        self.scale_y = pp.StandardScaler()
        self.warmup = True
        self.warmup_iters = warmup_iters
        self.standarization = True
        self.exploration_ratio = exploration_ratio
        if op_type == 'sw':
            A = [0, 1, 2, 3]
            self.feat_analysis = [item for item in A if item in args.feat_analysis]
        else:
            self.feat_analysis = []

    def update(self, xs, ys):
        print(f'BO update feat_analysis ', self.feat_analysis)
        if len(self.feat_analysis) > 0:
            real_xs = np.delete(xs, self.feat_analysis, axis=1)
            self.train_x = np.copy(real_xs)
        else:
            self.train_x = np.copy(xs)
        print(f'BO update train_x', self.train_x)
        self.train_y = [[y] for y in ys]
        self.warmup = len(self.train_x) <= self.warmup_iters

    def fit(self):
        if not self.warmup:
            if self.standarization:

                train_x_std = self.scale_x.fit_transform(self.train_x)
                train_y_std = self.scale_y.fit_transform(self.train_y)
                self.predictor = self.model.fit(train_x_std, train_y_std)
            else:
                self.predictor = self.model.fit(self.train_x, self.train_y)

    def predict(self, batch_x, return_std=True):
        if len(self.feat_analysis) > 0:
            real_batch_x = np.delete(batch_x, self.feat_analysis, axis=1)
        else:
            real_batch_x = batch_x
        traceback.print_stack(file=sys.stdout)
        if self.standarization:
            batch_x_std = self.scale_x.transform(real_batch_x)
            return self.predictor.predict(batch_x_std, return_std=return_std)
        else:
            return self.predictor.predict(real_batch_x, return_std=return_std)
    # 初次进入，走self.warmup 流程，直接返回
    def run(self, batch_x):
        if self.warmup or np.random.random() < self.exploration_ratio:
            return list(range(len(batch_x)))
        start = time.time()
        preds, std = self.predict(batch_x=batch_x)
        sort_index = np.argsort(preds - 1.0 * std) # 很明确，LCB
        end = time.time()
        # print(f'bo run elapse:{end - start}')
        print(f'bo run elapse:{end - start}, preds:{preds},std:{std},sort_index:{sort_index}')
        return sort_index

# batch_size 1000
def generate_hw_batch(hw_space, batch_size):
    hw_points = list()
    hw_feats = list()
    print(f'generate_hw_batch batch_size:{batch_size},hw_space.size:{hw_space.size}')
    for _ in range(batch_size):
        space_idx = np.random.randint(hw_space.size)
        hw_point = hw_space.build_point(space_idx)
        hw_feat = search_utils.get_hw_point_feats(hw_point, hw_space.num_levels)
        print(f'generate_hw_batch hw_point:{hw_point},hw_feat:{hw_feat}')
        hw_points.append(hw_point)
        hw_feats.append(hw_feat)
    return hw_points, hw_feats

def filter_by_smem(sw_point, l0_buf_size, l1_buf_size):
    l1occupy = 1

    for i in range(len(sw_point.param_values)-2):
        if sw_point.param_labels[i] == 'N':
            tile_n = sw_point.param_values[i]
        if sw_point.param_labels[i] == 'C':
            tile_c = sw_point.param_values[i]
        if sw_point.param_labels[i] == 'K':
            tile_k = sw_point.param_values[i]
        if sw_point.param_labels[i] == 'Y':
            tile_y = sw_point.param_values[i]
        if sw_point.param_labels[i] == 'X':
            tile_x = sw_point.param_values[i]
        if sw_point.param_labels[i] == 'R':
            tile_r = sw_point.param_values[i]
        if sw_point.param_labels[i] == 'S':
            tile_s = sw_point.param_values[i]

    if tile_x[0] < tile_r[0] or tile_y[0] < tile_s[0]:
        return True

    # l1occupy = tile_k[0] * tile_c[0] * tile_r[0] * tile_s[0] * tile_k[1] * tile_c[1] * tile_r[1] * tile_s[1] + \
    #     tile_c[0] * tile_n[0] * tile_x[0] * tile_y[0] * tile_c[1] * tile_n[1] * tile_x[1] * tile_y[1] + \
    #     tile_k[0] * (tile_x[0]) * (tile_y[0]) * tile_k[1] * tile_x[1] * tile_y[1]

    l1occupy = tile_k[0] * tile_c[0] * tile_r[0] * tile_s[0] * tile_k[1] * tile_c[1] * tile_r[1] * tile_s[1] + \
        tile_c[0] * tile_n[0] * tile_x[0] * tile_y[0] * tile_c[1] * tile_n[1] * tile_x[1] * tile_y[1] + \
        tile_k[0] * (tile_x[0]) * (tile_y[0]) * tile_k[1] * tile_x[1] * tile_y[1]

    if l1occupy > l1_buf_size or l1occupy < l1_buf_size * 0.4:
        return True
    return False

def check_smem(sw_point_str, l0_buf_size, l1_buf_size):
    sw_point = space.Point(sw_point_str)
    l0occpy = 1
    l1occpy = 1
    for i in range(len(sw_point.param_values)-2):
        l0occpy = l0occpy * sw_point.param_values[i][0]
        l1occpy = l1occpy * sw_point.param_values[i][1]
    l1occpy = l1occpy * l0occpy

    return l0occpy,l0_buf_size, l1occpy, l1_buf_size

# batch_size 1000
def generate_sw_batch(sw_space, hw_point, batch_size, excluded_feats, dataflow, enable_maestro_gemm=0):
    l0_buf_size = hw_point.get('l0_buf_size')
    l1_buf_size = hw_point.get('l1_buf_size')

    sw_points = list()
    sw_feats = list()
    print(f'generate_sw_batch batch_size:{batch_size},sw_space.size:{sw_space.size}')
    for _ in range(batch_size):
        space_idx = np.random.randint(sw_space.size)
        sw_point = sw_space.build_point(space_idx)
        #if filter_by_smem(sw_point, l0_buf_size, l1_buf_size):
        #    continue
        if enable_maestro_gemm == 1:
            sw_feat = search_utils.get_sw_point_feats_gemm(hw_point, sw_point, sw_space.num_levels, excluded_feats, dataflow)
        else:
            sw_feat = search_utils.get_sw_point_feats(hw_point, sw_point, sw_space.num_levels, excluded_feats, dataflow)
        sw_points.append(sw_point)
        sw_feats.append(sw_feat)

    if len(sw_points) < 20:
        for _ in range(batch_size - len(sw_points)):
            space_idx = np.random.randint(sw_space.size)
            sw_point = sw_space.build_point(space_idx)
            if enable_maestro_gemm == 1:
                sw_feat = search_utils.get_sw_point_feats_gemm(
                    hw_point, sw_point, sw_space.num_levels, excluded_feats,dataflow)
            else:
                sw_feat = search_utils.get_sw_point_feats(
                    hw_point, sw_point, sw_space.num_levels, excluded_feats,dataflow)
            sw_points.append(sw_point)
            sw_feats.append(sw_feat)
    print(f'generate_sw_batch filtered_batch_size:{len(sw_points)}')
    return sw_points, sw_feats

def generate_sw_lhs_batch(sw_space, hw_point, sample_num, excluded_feats, dataflow, args):
    sw_points = list()
    sw_feats = list()
    print(f'generate_sw_lhs_batch sample_num:{sample_num},sw_space.size:{sw_space.size}')

    num_dimensions = len(sw_space.params)
    # 生成拉丁超立方采样点
    lhs_samples = lhs(num_dimensions, sample_num, criterion="center")
    for sample in lhs_samples:
        sw_point = sw_space.build_point_lhs(sample)
        print(f'generate_sw_lhs_batch sw_point:{sw_point}')
        if args.enable_maestro_gemm:
            sw_feat = search_utils.get_sw_point_feats_gemm(hw_point, sw_point, sw_space.num_levels, excluded_feats, dataflow)
        else:
            sw_feat = search_utils.get_sw_point_feats(hw_point, sw_point, sw_space.num_levels, excluded_feats, dataflow)
        sw_points.append(sw_point)
        sw_feats.append(sw_feat)
    return sw_points, sw_feats
