import argparse
import math

class DefaultArgs:
    model = None
    output_dir = './'
    output_filename = 'out.txt'

    simd_low = 2
    simd_high = 16
    simd_step = 2
    prec_low = 8
    prec_high = 8
    prec_step = 1
    bw_low = 64
    bw_high = 256
    bw_step = 2
    pe_low = 128
    pe_high = 300
    pe_step = 2
    buffer_low = 32
    buffer_high = 256
    buffer_step = 8
    max_area = 4.3841e+09
    max_power = 1.34877e+05
    max_invalid = 250000

    trials = 1
    hw_trials = 100
    sw_trials = 100

    target = 'edp'
    kernel = 'linear'
    hw_point = None
    sw_point = None

    sw_batch_size = 1000
    hw_batch_size = 1000
    sw_batch_trials = 10
    hw_batch_trials = 10 ##

    scalable_sw_bo = ''  # gpflow/gpytorch/gpy
    scalable_hw_bo = ''  # gpflow/gpytorch/gpy
    sw_inducing_num = 20
    hw_inducing_num = 20

    sw_adaptive_inducing = 0  # rate 0.25/0.4/..

    sw_adaptive_batch_size = 0  # rate 0.25/0.4/..

    sw_inducing_poilcy = 'kmean'  # policy kmean/ksmall/halton

    sw_init_lhs = 0  # Latin Hypercube Sampling (LHS) for mse
    hw_init_lhs = 0  # Latin Hypercube Sampling (LHS) for dse

    sw_warmup_ratio = 0.1
    hw_warmup_ratio = 0.1

    enable_pycuda = 0
    enable_maestro_gemm = 0
    layers = None
    exclude_feat = "raw"

def int_list(string):
    print(f'feat-analysis: int_list:{string}')
    if any(char.isdigit() for char in string):
        return [int(item) for item in string.split(',')]
    return []


def get_args():
    parser = argparse.ArgumentParser(description='spotlight-micro21.')
    parser.add_argument("--model", help="model name", type=str, default=DefaultArgs.model)
    parser.add_argument("--output-dir", help="output directory", type=str, default=DefaultArgs.output_dir)
    parser.add_argument("--output-filename", help="output filename", type=str, default=DefaultArgs.output_filename)
    parser.add_argument("--output-to-file", help="output to file", default=False, action="store_true")
    parser.add_argument("--dump-all", help="dump full cost dictionary", default=False, action="store_true")

    parser.add_argument("--simd-low", help="minimum number of SIMD lanes", type=int, default=DefaultArgs.simd_low)
    parser.add_argument("--simd-high", help="maxium number of SIMD lanes", type=int, default=DefaultArgs.simd_high)
    parser.add_argument("--simd-step", help="step size for SIMD lane values", type=int, default=DefaultArgs.simd_step)

    parser.add_argument("--prec-low", help="minimum bit precision", type=int, default=DefaultArgs.prec_low)
    parser.add_argument("--prec-high", help="maxium bit precision", type=int, default=DefaultArgs.prec_high)
    parser.add_argument("--prec-step", help="step size for bit precision", type=int, default=DefaultArgs.prec_step)

    parser.add_argument("--bw-low", help="minimum bandwidth", type=int, default=DefaultArgs.bw_low)
    parser.add_argument("--bw-high", help="maxium bandwidthnumber of SIMD lanes", type=int, default=DefaultArgs.bw_high)
    parser.add_argument("--bw-step", help="step size for bandwidth", type=int, default=DefaultArgs.bw_step)

    parser.add_argument("--pe-low", help="minimum number of PEs", type=int, default=DefaultArgs.pe_low)
    parser.add_argument("--pe-high", help="maxium number of PEs", type=int, default=DefaultArgs.pe_high)
    parser.add_argument("--pe-step", help="step size for PE values", type=int, default=DefaultArgs.pe_step)

    parser.add_argument("--levels-low", help="minimum number of levels of mem hierarchy", type=int, default=2)
    parser.add_argument("--levels-high", help="maxium number of levels of mem hierarchy", type=int, default=2)
    parser.add_argument("--levels-step", help="step size for levels of mem hierarchy", type=int, default=1)

    for i in range(1, 4):
        parser.add_argument("--l%d-low" % i, help="minimum total L%d size" % i, type=int, default=DefaultArgs.buffer_low)
        parser.add_argument("--l%d-high" % i, help="maximum total L%d size" % i, type=int, default=DefaultArgs.buffer_high)
        parser.add_argument("--l%d-step" % i, help="step size of L%d size" % i, type=int, default=DefaultArgs.buffer_step)

    parser.add_argument("--space-template", help="use template (edge, datacenter) to determine space", type=str, default='')

    parser.add_argument("--max-area", help="maximum area", type=float, default=DefaultArgs.max_area)
    parser.add_argument("--max-power", help="maximum power", type=float, default=DefaultArgs.max_power)

    parser.add_argument("--trials", help="number of hardware trials", type=int, default=DefaultArgs.trials)
    parser.add_argument("--hw-trials", help="number of hardware trials", type=int, default=DefaultArgs.hw_trials)
    parser.add_argument("--sw-trials", help="number of software trials", type=int, default=DefaultArgs.sw_trials)
    parser.add_argument("--scale-trials", help="scale number of hardware and software trials", default=False, action="store_true")
    parser.add_argument("--max-invalid", help="number of trials before giving up", type=int, default=DefaultArgs.max_invalid)
    parser.add_argument("--sw-progress-bar", help="whether to use progress bar for software samples", default=False, action="store_true")
    parser.add_argument("--hw-progress-bar", help="whether to use progress bar for hardware samples", default=False, action="store_true")
    parser.add_argument('--print-sw-samples', help="whether to print results for SW sample", default=False, action="store_true")

    parser.add_argument("--target", help="optimization target", type=str, default=DefaultArgs.target)
    parser.add_argument("--kernel", help="GP kernel", type=str, default=DefaultArgs.kernel)
    parser.add_argument("--sw-point", help="software config", type=str, default=DefaultArgs.sw_point)
    parser.add_argument("--hw-point", help="hardware config", type=str, default=DefaultArgs.hw_point)

    parser.add_argument("--sw-batch-size", help="number of random samples in software BO batch", type=int, default=DefaultArgs.sw_batch_size)
    parser.add_argument("--hw-batch-size", help="number of random samples in hardware BO batch", type=int, default=DefaultArgs.hw_batch_size)
    parser.add_argument("--sw-batch-trials", help="number of software samples in BO batch to evaluate", type=int, default=DefaultArgs.sw_batch_trials)
    parser.add_argument("--hw-batch-trials", help="number of hardware samples in BO batch to evaluate", type=int, default=DefaultArgs.hw_batch_trials)

    parser.add_argument("--sw-inducing-num", help="sw scalable bo inducing num", type=int, default=DefaultArgs.sw_inducing_num)
    parser.add_argument("--hw-inducing-num", help="hw scalable bo inducing num", type=int, default=DefaultArgs.hw_inducing_num)

    parser.add_argument("--sw-adaptive-inducing", help="sw scalable bo inducing num adaptive", type=float, default=DefaultArgs.sw_adaptive_inducing)

    parser.add_argument("--sw-adaptive-batch-size", help="enable sw adaptivte batch_size 0 or 1", type=int, default=DefaultArgs.sw_adaptive_batch_size)

    parser.add_argument("--sw-inducing-poilcy", help="sw scalable bo inducing num adaptive", type=str, default=DefaultArgs.sw_inducing_poilcy)

    parser.add_argument("--scalable-sw-bo", help="enable scalable bo for mse", type=str, default=DefaultArgs.scalable_sw_bo)
    parser.add_argument("--scalable-hw-bo", help="enable scalable bo for dse", type=str, default=DefaultArgs.scalable_hw_bo)

    parser.add_argument("--sw-init-lhs", help="enable lhs init for mse", type=int, default=DefaultArgs.sw_init_lhs)
    parser.add_argument("--hw-init-lhs", help="enable lhs init for dse", type=int, default=DefaultArgs.hw_init_lhs)

    parser.add_argument("--sw-warmup-ratio", help="warmup ratio for mse", type=float, default=DefaultArgs.sw_warmup_ratio)
    parser.add_argument("--hw-warmup-ratio", help="warmup ratio for dse", type=float, default=DefaultArgs.hw_warmup_ratio)

    parser.add_argument("--enable-pycuda", help="enable pycuda", type=int, default=DefaultArgs.enable_pycuda)

    parser.add_argument("--print-bo-analysis", dest="print_bo_analysis", help="whether to analyze BO features", default=False, action="store_true")

    parser.add_argument("--exhaustive-hw-start-idx", help="point at which to start HW space in exhaustive search", type=int, default=0)
    parser.add_argument("--exhaustive-hw-end-idx", help="point at which to end HW space in exhaustive search", type=int, default=0)
    parser.add_argument("--no-search-permutations", dest="search_permutations", help="enable MAESTRO to search permutations", default=True, action="store_false")
    parser.add_argument("--dataflow", help="type of dataflow to use", type=str, default="searched")

    parser.add_argument("--layers", help="comma separated list of layers", type=str, default=DefaultArgs.layers)
    parser.add_argument("--remove-duplicate-layers", dest="remove_duplicate_layers", help="ignore duplicate layers", default=False, action="store_true")
    parser.add_argument("--ignore-stride", dest="ignore_stride", help="ignore stride in layer shapes", default=False, action="store_true")

    parser.add_argument("--exclude-feat", help="comma separated list of features to ignore", type=str, default=DefaultArgs.exclude_feat)

    parser.add_argument("--enable-maestro-gemm", help="enable maestro gemm", type=int, default=False)

    parser.add_argument("--technique", help="which accelerator eyeriss/nvdla/spotlight/transpeed(enable-maestro-gemm)", type=str, default=False)
    parser.add_argument("--feat-analysis", help="which feats to exclude; 0 indicate none; otherwise indicate index to exclude", type=int_list, default=[])
    parser.add_argument("--algorithm", help="nothing", type=str, default='')

    args = parser.parse_args()

    if args.enable_maestro_gemm and args.layers == 'TRANSFORMER':
        args.layers = 'ALBERT'

    print(f'search-permutations:{args.search_permutations}, feat-analysis:{args.feat_analysis}')
    assert(args.model)
    assert(args.layers)

    if args.enable_pycuda == 1:
        # https://gpy.readthedocs.io/en/deploy/_modules/GPy/util/gpu_init.html?highlight=gpu
        gpu_initialized = False
        try:
            import pycuda.autoinit
            gpu_initialized = True
        except:
            pass

    if args.scale_trials:
        trial_scale = 1
        bo_time_per_layer = 2.71
        if 'grid' in args.model:
            trial_scale = 0.522
        elif 'random' in args.model:
            trial_scale = 1.91
        elif 'ga' in args.model:
            trial_scale = 1.68
        elif 'hebo' in args.model:
            trial_scale = bo_time_per_layer
        elif 'bo' in args.model:
            trial_scale = bo_time_per_layer

        trial_scale = bo_time_per_layer / trial_scale

        if 'hw' in args.model:
            trial_scale = math.sqrt(trial_scale)
            args.hw_trials = int(args.hw_trials * trial_scale)
        args.sw_trials = int(args.sw_trials * trial_scale)
        print(f'running {args.hw_trials} hw and {args.sw_trials} sw samples')

    if args.space_template != "":
        if args.space_template == "edge":
            args.pe_low = DefaultArgs.pe_low
            args.pe_high = DefaultArgs.pe_high
            args.pe_step = DefaultArgs.pe_step

            for i in range(1, 4):
                args.__dict__['l%d_low' % i] = DefaultArgs.buffer_low
                args.__dict__['l%d_high' % i] = DefaultArgs.buffer_high
                args.__dict__['l%d_step' % i] = DefaultArgs.buffer_step

            args.max_area = DefaultArgs.max_area
            args.max_power = DefaultArgs.max_power
            args.max_invalid = DefaultArgs.max_invalid

        elif args.space_template == 'datacenter':
            args.pe_low = 2048
            args.pe_high = 16384
            args.pe_step = 256

            for i in range(1, 4):
                args.__dict__['l%d_low' % i] = 8192
                args.__dict__['l%d_high' % i] = 32768
                args.__dict__['l%d_step' % i] = 2048

            args.max_area = 1.0e15
            args.max_power = 1.0e15
            args.max_invalid = 1000

    return args
