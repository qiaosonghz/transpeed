import time

import numpy as np
import numpy as np
from pyDOE import lhs
import torch

from hebo.design_space.design_space import DesignSpace
from hebo.optimizers.hebo import HEBO
from hebo.optimizers.bo import BO
from optimizer import Optimizer
from optimizer import CoBOOptimizer
import search_utils
import space
import pandas as pd

class HEBOOptimizer(CoBOOptimizer):
    def __init__(self, args, eval_f, shapes, n_hw, n_sw, out_file, compute_feats=True):
        super().__init__(args, eval_f, shapes, n_hw, n_sw, out_file, compute_feats)

    def updateByHwResult(self, hw_results):
        print(f'HEBOOptimizer updateByHwResult,len:{len(hw_results.points)}')
        if hw_results:
            bo_points = self.hw_real2bo(hw_results.points)
            self.hw_bo.update(bo_points, hw_results.values)


    def init_hw_batch(self, hw_dataspace):
        start_time = time.time()

        # 生成 Latin Hypercube Sampling
        lhs_samples = lhs(hw_dataspace.num_paras, samples=20)
        # lower_bound = hw_dataspace.opt_lb
        lower_bound= np.array([hw_dataspace.paras[p].lb for p in hw_dataspace.numeric_names])

        # upper_bound = hw_dataspace.opt_ub
        upper_bound= np.array([hw_dataspace.paras[p].ub for p in hw_dataspace.numeric_names])
        # 根据实际问题进行采样范围的缩放和平移
        # 例如，如果要在 [0, 1] 范围内采样，则无需进行缩放和平移
        # 如果要在特定范围内采样，可以进行以下操作：
        lhs_samples = lower_bound + lhs_samples * (upper_bound - lower_bound)
        # lhs_samples = lower_bound.numpy() + lhs_samples * (upper_bound - lower_bound).numpy()
        # int_tensor = lhs_samples.round().to(torch.int32)
        int_tensor = lhs_samples.astype(int)

        int_tensor[:, 0] = ceil_even(int_tensor[:, 0])
        int_tensor[:, 2] = ceil_even(int_tensor[:, 2])
        int_tensor[:, 6] = ceil_even(int_tensor[:, 6])
        int_tensor[:, 3] = np.ceil(int_tensor[:, 3] / 8) * 8
        int_tensor[:, 4] = np.ceil(int_tensor[:, 4] / 8) * 8


        df_bo_points = pd.DataFrame(int_tensor, columns=hw_dataspace.para_names)
        print(f'init_hw_batch elapse:{time.time() - start_time},lower_bound:{lower_bound},upper_bound:{upper_bound},lhs_samples:{lhs_samples},int_tensor:{int_tensor},df_bo_points:{df_bo_points}, hw_points:{self.hw_points}')

        self.hw_points = self.hw_bo2real(df_bo_points)
        self.hw_idx = 0
        self.hw_valid_count = 0

        print(f'init_hw_batch2 elapse:{time.time()-start_time}, int_tensor:{int_tensor},df_bo_points:{df_bo_points}, hw_points:{self.hw_points}')

    def gen_hw_batch(self, hw_space, hw_results):
        start_time = time.time()
        if hw_results:
            self.updateByHwResult(hw_results)

        bo_points = self.hw_bo.suggest()
        self.hw_points = self.hw_bo2real(bo_points)
        self.hw_idx = 0
        self.hw_valid_count = 0

        print(f'gen_hw_batch elapse:{time.time()-start_time}, hw_points:{self.hw_points}')

    def increment_hw_opt(self, success):
        self.hw_idx += 1
        if success:
            self.hw_valid_count += 1

    def get_hw_point(self, hw_space, hw_results):
        if self.hw_idx >= self.args.hw_batch_trials:
            self.gen_hw_batch(hw_space, hw_results)
        return self.hw_points[self.hw_idx]

    def reset_hw_state(self, hw_space):
        self.hw_design_space, self.hw_bo2real_dict = parse_hw_designspace(hw_space)
        # self.hw_real2bo_dict = {tuple(value): key for key, value in self.hw_bo2real_dict.items()}

        self.hw_batch_trials = self.args.hw_batch_trials
        self.hw_bo = HexBO(self.args, self.hw_design_space, self.hw_batch_trials)
        self.hw_points = list()
        self.hw_valid_count = 0
        self.gen_hw_batch(hw_space, None)
        # self.init_hw_batch(self.hw_design_space)

    def hw_bo2real(self, dataframe:pd.DataFrame):
        points = []
        # 遍历访问DataFrame的每一行
        for index, row in dataframe.iterrows():
            point = space.Point()

            # 访问每一列的值
            for column_name in dataframe.columns:
                if column_name == 'subclusters':
                    point.add(column_name, self.hw_bo2real_dict[row['penum']][row[column_name]])
                    point.setUserData(row[column_name])
                elif column_name == 'penum':
                    pass
                else:
                    point.add(column_name, row[column_name])

            points.append(point)

        print(f'hw_bo2real, df:{dataframe}, points:{points}')
        return points

    def hw_real2bo(self, points:[]):
        df = pd.DataFrame()

        for point in points:
            # filtered_label = list(filter(lambda label: label != 'penum', point.getLabels()))

            data = [point.userdata if 'subclusters' in label else point.get(label)for label in point.getLabels()]
            data.append(np.product(point.get('subclusters')))
            labels = point.getLabels() + ['penum']
            print(f'hw_real2bo point:{point}, data:{data},labels:{labels}')

            df = df.append(pd.Series(data, index=labels), ignore_index=True)
        print(f'hw_real2bo df:{df}')
        return df

class HexBO:
    def __init__(self, args, design_space, batch_trials, warmup_iters=10, exploration_ratio=0.1):
        # self.exploration_ratio = exploration_ratio
        self.batch_trials = batch_trials
        self.bo = HEBO(design_space, rand_sample=self.batch_trials)
        self.train_x = []
        self.train_y = []
        self.warmup = True
        self.warmup_iters = self.batch_trials
        self.standarization = True

    def update(self, xs, ys):
        self.train_x = np.copy(xs)
        self.train_y = np.reshape(ys, (-1, 1)) #[[y] for y in ys]
        self.warmup = len(self.train_x) <= self.warmup_iters
        print(f'HexBo update xs:{xs},y:{np.reshape(ys, (-1, 1))}')
        self.bo.observe(xs, np.reshape(ys, (-1, 1)))

    def suggest(self):
        return self.bo.suggest(self.batch_trials)

def ceil_even(x):
    return np.ceil(x / 2) * 2


def generate_hw_batch(hw_space, batch_size):
    hw_points = list()
    hw_feats = list()
    for _ in range(batch_size):
        space_idx = np.random.randint(hw_space.size)
        hw_point = hw_space.build_point(space_idx)
        hw_feat = search_utils.get_hw_point_feats(hw_point, hw_space.num_levels)
        hw_points.append(hw_point)
        hw_feats.append(hw_feat)
    return hw_points, hw_feats


'''
input:
[
    {"name": "num_simd_lane", "values": [2, 3, 4, 5, 6, 7, 8, 9]},
    {"name": "bit_width", "values": [8]},
    {"name": "bandwidth", "values": [64, 65, 66, 67, 68, 69, 70, 71]},
    {"name": "l0_buf_size", "values": [32768, 40960, 49152, 57344, 65536, 73728, 81920, 90112, 98304, 106496, 114688, 122880, 131072, 139264, 147456, 155648, 163840, 172032, 180224, 188416, 196608, 204800, 212992, 221184, 229376, 237568, 245760, 253952, 262144]},
    {"name": "l1_buf_size", "values": [32768, 40960, 49152, 57344, 65536, 73728, 81920, 90112, 98304, 106496, 114688, 122880, 131072, 139264, 147456, 155648, 163840, 172032, 180224, 188416, 196608, 204800, 212992, 221184, 229376, 237568, 245760, 253952, 262144]},
    {"name": "subclusters", "values": [[2, 64], [4, 32], [8, 16], [16, 8], [32, 4], [64, 2], [128, 1], [3, 43], [43, 3], [129, 1], [2, 65], [5, 26], [10, 13], [13, 10], [26, 5], [65, 2], [130, 1], [131, 1], [2, 66], [3, 44], [4, 33], [6, 22], [11, 12], [12, 11], [22, 6], [33, 4], [44, 3], [66, 2], [132, 1], [7, 19], [19, 7], [133, 1], [2, 67], [67, 2], [134, 1], [3, 45], [5, 27], [9, 15], [15, 9], [27, 5], [45, 3], [135, 1]]}
]

output:
[{'name': 'num_simd_lane', 'type': 'step_int', 'lb': 2, 'ub': 9, 'step': 1}, 
{'name': 'bit_width', 'type': 'step_int', 'lb': 8, 'ub': 8, 'step': 0}, 
{'name': 'bandwidth', 'type': 'step_int', 'lb': 64, 'ub': 71, 'step': 1}, 
{'name': 'l0_buf_size', 'type': 'step_int', 'lb': 32768, 'ub': 262144, 'step': 8192}, 
{'name': 'l1_buf_size', 'type': 'step_int', 'lb': 32768, 'ub': 262144, 'step': 8192},
{'name': 'penum', 'type': 'step_int', 'lb': 128, 'ub': 300, 'step': 2}, 
{'name': 'subclusters', 'type': 'cat', 'categories': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]}]

{
128:{1:[2, 64], 2:[2,64],3:[4,32],4:[4,32]..., 19:[128:1]},
130:{1:[1, 130], 2:[1,30]..},
}
'''

def parse_hw_designspace(hw_space):
    cat_to_subcluster = {}
    # subcluster_to_cat = {}
    space = []
    for param in hw_space.params:
        param_name = param.name
        param_values = param.range

        if param_name == 'subclusters':
            groupby_penum = {}
            for param_value in param_values:
                penum = np.product(param_value)
                arr = groupby_penum.get(penum)
                if arr is None:
                    groupby_penum[penum] = [param_value]
                else:
                    arr.append(param_value)

            max_length = max(len(subcluster) for subcluster in groupby_penum.values())
            for penum, value in groupby_penum.items():
                # cat_s = np.array(list(range(1,len(value) + 1)))
                # mapping = {cat_s[i]: value[i] for i in range(len(cat_s))}
                # cat_to_subcluster[penum] = mapping

                scs = [value[i % len(value)] for i in range(max_length)]
                scs.sort()

                cat_s = np.array(list(range(1, max_length + 1)))
                mapping = {cat_s[i]: scs[i] for i in range(len(cat_s))}
                cat_to_subcluster[penum] = mapping
            # {'name' : 'activation', 'type' : 'cat', 'categories' : ['relu', 'tanh','sigmoid']},


            parsed_param = {
                "name": param_name,
                # "type": "cat",
                # "categories": list(np.array(list(range(1, max_length + 1))))
                "type": "step_int",
                "lb": 1,
                "ub": max_length,
                "step": 1
            }
            space.append(parsed_param)

            pe_low = min(groupby_penum.keys())
            pe_high = max(groupby_penum.keys())
            # pe_step = int((pe_high - pe_low)/len(groupby_penum.keys())) if len(groupby_penum.keys()) > 1 else 1
            pe_step = 2

            penum_param = {
                "name": 'penum',
                "type": "step_int",
                "lb": pe_low,
                "ub": pe_high,
                "step": pe_step
            }
            space.append(penum_param)

        else :
            param_lb = min(param_values)
            param_ub = max(param_values)
            param_step = param_values[1] - param_values[0] if len(param_values) > 1 else 1

            parsed_param = {
                "name": param_name,
                "type": "step_int",
                "lb": param_lb,
                "ub": param_ub,
                "step": param_step
            }
            space.append(parsed_param)
        print(f'parse_hw_designspace hwspace:{hw_space},space:{space},cat_to_subcluster:{cat_to_subcluster}')
    return DesignSpace().parse(space), cat_to_subcluster
