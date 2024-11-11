import numpy as np
import time

class Parameter:
    def __init__(self, name, range):
        self.name = name
        self.range = range
    def __repr__(self):
        return '%s %s' % (self.name, str(self.range))

class Point:
    def __init__(self, params=dict(), userdata = None):
        self.param_labels = list()
        self.param_values = list()
        for label, value in params.items():
            self.add(label, value)
        self.userdata = userdata

    def add(self, label, value):
        self.param_labels.append(label)
        self.param_values.append(value)

    def set(self, label, value):
        try:
            idx = self.param_labels.index(label)
            self.param_values[idx] = value
        except ValueError:
            self.add(label, value)

    def get(self, label):
        try:
            idx = self.param_labels.index(label)
            return self.param_values[idx]
        except ValueError:
            return None

    def set_by_idx(self, idx, lable, value):
        try:
            assert(lable == self.param_labels[idx])
            self.param_values[idx] = value
        except ValueError:
            pass

    def get_by_idx(self, idx, param_label):
        try:
            assert(param_label == self.param_labels[idx])
            return self.param_values[idx]
        except ValueError:
            return None

    def getLabels(self):
        return self.param_labels

    def setUserData(self, userData):
        self.userdata = userData

    def __repr__(self):
        ret = str(dict(zip(self.param_labels, self.param_values)))
        if self.userdata:
            ret = ret + ',userdata:' + str(self.userdata)
        return ret.replace(' ', '')

class Space:
    def __init__(self, params, num_levels, space_name='default', enable_maestro_gemm=0):
        self.params = params
        self.num_levels = num_levels
        self.build_meta()
        self.space_name = space_name
        self.enable_maestro_gemm = enable_maestro_gemm

    def build_meta(self):
        self.param_length = [len(x.range) for x in self.params]
        self.cumulative_length = np.flip(np.multiply.accumulate(np.flip(self.param_length)))
        self.size = self.cumulative_length[0]
        self.cumulative_length = self.cumulative_length[1:]

    def build_point(self, index):
        point = Point()
        for i in range(len(self.params) - 1):
            point.add(self.params[i].name, self.params[i].range[int(index / self.cumulative_length[i])])
            index %= self.cumulative_length[i]

            if (self.enable_maestro_gemm == 0) and (i == (len(self.params) - self.num_levels - 1)):
                # K C N X Y R S
                if self.space_name.find('MatMul') >= 0: # # R = Y
                    point.add('R', point.get_by_idx(4, 'Y'))

                if self.space_name.find('FC') >= 0 or self.space_name.find('FF') >= 0: # S = X
                    point.add('S', point.get_by_idx(3, 'X'))

        point.add(self.params[-1].name, self.params[-1].range[index % len(self.params[-1].range)])
        return point

    def build_point_lhs(self, indexs):
        point = Point()
        for i in range(len(self.params)):
            value = self.params[i].range[int(indexs[i] * len(self.params[i].range))]
            point.add(self.params[i].name, value)
        return point

    def getParam(self, param_name):
        return self.params[param_name]

    def __repr__(self):
        return 'params:%s num_levels:%s' % (self.params, str(self.num_levels))

def get_all_combinations(n, V, ret, curr):
    if n == 0:
        return
    if n == 1:
        ret.append(curr + [int(V)])
    possible_values = [v for v in range(int(V), 0, -1) if V % v == 0]
    for pv in possible_values:
        get_all_combinations(n-1, V/pv, ret, curr+[pv])
    return ret

def get_all_combinations_v2(n, V, ret, curr):
    if n == 0:
        return
    if n == 1:
        ret.append(curr + [int(V)])
    possible_values = [v for v in range(2, int(V)+1) if V % v == 0]
    for pv in possible_values:
        get_all_combinations_v2(n-1, V/pv, ret, curr+[pv])
    return ret

def get_all_summation(n, V, step, ret, curr):
    if n == 0:
        return
    if n == 1:
        ret.append(curr + [int(V)])
    possible_values = [v for v in range(step, V, step) if v < V]
    for pv in possible_values:
        get_all_summation(n-1, V-pv, step, ret, curr+[pv])
    return ret

def create_hardware_space(args, num_element_type=3):
    # TODO: now randomly choose number of levels, not sure if this is the right thing to do
    # num_levels = np.random.randint(args.levels_low, args.levels_high+1)
    num_levels = 2

    params = list()
    # print('Creating hardware resources...')
    params.append(Parameter('num_simd_lane', list(range(args.simd_low, args.simd_high+1, args.simd_step))))
    params.append(Parameter('bit_width', list(range(args.prec_low, args.prec_high+1, args.prec_step))))
    params.append(Parameter('bandwidth', list(range(args.bw_low, args.bw_high+1, args.bw_step))))

    arg_dict = vars(args)
    for num_level in range(num_levels):
        step = arg_dict['l{}_step'.format(num_level+1)]
        low = arg_dict['l{}_low'.format(num_level+1)]
        high = arg_dict['l{}_high'.format(num_level+1)]
        buf_range = [1024 * v for v in range(low, high+1, step)]
        params.append(Parameter('l{}_buf_size'.format(num_level), buf_range))

    # subcluster
    step = args.pe_step
    pe_range = range(args.pe_low, args.pe_high+1, step)
    subcluster_range = []
    for num_pe in pe_range:
        subcluster = get_all_combinations_v2(num_levels, num_pe, [], [])
        print(f'create_hardware_space len(subcluster):{len(subcluster)}')
        subcluster_range += list(subcluster)
    params.append(Parameter('subclusters', subcluster_range))

    return Space(params, num_levels)

def create_software_space(args, shape, num_levels, shape_name=''):
    print(f'create_software_space shape:{shape}, shape_name:{shape_name}, num_levels:{num_levels}')
    params = []
    # tile sizes
    params.append(Parameter('K', list(get_all_combinations(num_levels+1, shape['K'], [], []))))
    params.append(Parameter('C', list(get_all_combinations(num_levels+1, shape['C'], [], []))))
    if args.dataflow == 'searched': # default spotlight
        params.append(Parameter('N', list(get_all_combinations(num_levels+1, shape['N'], [], []))))
        params.append(Parameter('X', list(get_all_combinations(num_levels+1, shape['X'], [], []))))
        params.append(Parameter('Y', list(get_all_combinations(num_levels+1, shape['Y'], [], []))))


        start = time.time()
        if (shape['R'] < 8):
        # if shape_name.index('MatMul') >= 0 or (shape['R'] < 8):  #:  # two case: 1. conv  small odd number 2. matmul map_R equals map_S, just give one perm
        # if shape_name.startswith('TRANSFORMER_SD_MatMul')  or (shape['R'] < 8):  #:  # two case: 1. conv  small odd number 2. matmul map_R equals map_S, just give one perm
            params.append(Parameter('R', list([[shape['R'], 1, 1]])))
            print(f'create_software_space params append, elapse:{time.time() - start}')
        elif shape_name.find('MatMul') > 0:
            pass # R = Y
            # params.append(Parameter('R', list([[shape['R'], 1, 1]])))
            # print(f'create_software_space params append, elapse:{time.time() - start}')
        else:
            params.append(Parameter('R', list(get_all_combinations(num_levels + 1, shape['R'], [], []))))

        if shape['S'] < 8:
            params.append(Parameter('S', list([[shape['S'], 1, 1]])))
        elif shape_name.find('FC') > 0 or shape_name.find('FF') > 0:
            pass # S = X
            # params.append(Parameter('R', list([[shape['R'], 1, 1]])))
            # print(f'create_software_space params append, elapse:{time.time() - start}')
        else:
            params.append(Parameter('S', list(get_all_combinations(num_levels+1, shape['S'], [], []))))

        # spatial_dim
        for num_level in range(num_levels):
            if shape_name.find('MatMul') > 0:
                params.append(Parameter('l{}_spatial_dim'.format(num_level), ['K', 'X', 'Y', 'R']))
            elif shape_name.find('FC') > 0 or shape_name.find('FF') > 0:
                params.append(Parameter('l{}_spatial_dim'.format(num_level), ['K', 'N', 'S', 'X']))
            else:
                params.append(Parameter('l{}_spatial_dim'.format(num_level), ['K', 'C', 'X', 'Y', 'R', 'S']))
    elif args.dataflow == 'fixed':
        params.append(Parameter('dataflow', ['eye', 'dla', 'shi']))

    return Space(params, num_levels, shape_name, args.enable_maestro_gemm)

def create_software_space_gemm(args, shape, num_levels, shape_name=''):
    print(f'create_software_space shape:{shape}, shape_name:{shape_name}, num_levels:{num_levels}')
    params = []
    # tile sizes
    params.append(Parameter('M', list(get_all_combinations(num_levels + 1, shape['M'], [], []))))
    params.append(Parameter('K', list(get_all_combinations(num_levels + 1, shape['K'], [], []))))
    params.append(Parameter('N', list(get_all_combinations(num_levels + 1, shape['N'], [], []))))
    if args.dataflow == 'searched': # default spotlight
        # spatial_dim
        for num_level in range(num_levels):
            params.append(Parameter('l{}_spatial_dim'.format(num_level), ['M', 'K', 'N']))

    elif args.dataflow == 'fixed':
        if 'eye' in args.hw_point:
            params.append(Parameter('dataflow', ['eye']))
            params.append(Parameter('l{}_spatial_dim'.format(0), ['M']))
            params.append(Parameter('l{}_spatial_dim'.format(1), ['K']))
        elif 'dla' in args.hw_point:
            params.append(Parameter('dataflow', ['dla']))
            params.append(Parameter('l{}_spatial_dim'.format(0), ['N']))
            params.append(Parameter('l{}_spatial_dim'.format(1), ['K']))
        else:
            params.append(Parameter('dataflow', ['eye', 'dla', 'shi']))

    return Space(params, num_levels, shape_name, args.enable_maestro_gemm)


def to_design_space(space):
    '''
    params: [
        num_simd_lane[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], bit_width[8],
        bandwidth[64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, ..., 254, 255, 256],
        l0_buf_size[32768, 40960, 49152, 57344, 65536, 73728, 81920, 90112, 98304, 106496, 114688, ..., 253952, 262144],
        l1_buf_size[32768, 40960, 49152, 57344, 65536, 73728, 81920, 90112, 98304, 106496, 114688, 253952, 262144],
        subclusters[[2, 64], [4, 32], [8, 16], [16, 8], ...],
        num_levels:2


    :param space:
    :return:
    '''
    design_space = DesignSpace().parse([
        {'name': 'x0', 'type': 'num', 'lb': -5, 'ub': 10},
        {'name': 'x1', 'type': 'num', 'lb': 0, 'ub': 15}
    ])
