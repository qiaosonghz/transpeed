import sys

sys.path.append("..")
sys.path.append("./")
sys.path.append("./src")
sys.path.append("../src")

from src import space
from src import options
from src import layers
from clickhouse_driver import Client

def get_combination_by_id(arrays, id):
    combination = []
    for i in range(len(arrays)):
        index = id % len(arrays[i])  # 取余数得到当前数组的索引
        combination.append(arrays[i][index])
        id //= len(arrays[i])  # 更新id，准备处理下一个数组
    return combination

def get_combination_by_id2(maps, id):
    combination = {}
    for key, value in maps.items():
        index = id % len(value)  # 取余数得到当前数组的索引
        combination[key] = value[index]
        id //= len(value)  # 更新id，准备处理下一个数组
    # print(combination)
    return combination

def list_combinations_with_name_ids(maps):
    num_map = len(maps)
    total_combinations = 1
    for value  in maps.values():
        total_combinations *= len(value)

    combinations_with_ids = []
    for i in range(total_combinations):
        combination = get_combination_by_id2(maps, i)
        combinations_with_ids.append((i, combination))
        if (i % 10000) ==0 :
            print(f'list_combinations_with_ids i:{i}')

    return combinations_with_ids

def list_combinations_with_ids(arrays):
    num_arrays = len(arrays)
    total_combinations = 1
    for arr in arrays:
        total_combinations *= len(arr)

    combinations_with_ids = []
    for i in range(total_combinations):
        combination = get_combination_by_id(arrays, i)
        combinations_with_ids.append((i, combination))
        if (i % 10000) ==0 :
            print(f'list_combinations_with_ids i:{i}')

    return combinations_with_ids

def list_combinations(arrays):
    num_arrays = len(arrays)
    total_combinations = 1
    for arr in arrays:
        total_combinations *= len(arr)

    combinations = []
    for i in range(total_combinations):
        combination = get_combination_by_id(arrays, i)
        combinations.append(combination)

    return combinations


def insert_to_clickhouse(client, model_layer, combinations_with_ids):
    # data_to_insert = []
    # for i in range(8192):
    #     data_to_insert.append({
    #         'model_layer': model_layer,
    #         'tile_index': i,
    #         'tile_k': [4, 5, 6],
    #         'tile_c': [7, 8, 9],
    #         'tile_n': [1, 2, 3],
    #         'tile_x': [19, 20, 21],
    #         'tile_y': [16, 17, 18],
    #         'tile_r': [10, 11, 12],
    #         'tile_s': [13, 14, 15],
    #         'l1_occupy': 100,
    #         'l2_occupy': 200,
    #     })

    # 批量插入数据
    batch_size = 8192
    for i in range(0, len(combinations_with_ids), batch_size):
        batch = combinations_with_ids[i:i + batch_size]
        insert_query = f"INSERT INTO modellayer_tile_space (model_layer, tile_index, tile_n, tile_k, tile_c, tile_r, tile_s, tile_y, tile_x, l1_occupy, l2_occupy) VALUES"

        for data in batch:
            insert_query += f" ('{model_layer}', {data[0]}, {data[1]['N']}, {data[1]['K']}, {data[1]['C']}, {data[1]['R']}, {data[1]['S']}, {data[1]['Y']}, {data[1]['X']}, 0, 0),"

        # 移除最后一个逗号
        insert_query = insert_query.rstrip(',')

        client.execute(insert_query)


# 示例用法
arrays = [[1, 2], [3, 4], [5, 6]]
combinations_with_ids = list_combinations_with_ids(arrays)
print(combinations_with_ids)
# sys.exit(0)

# 连接到ClickHouse数据库
client = Client(host='localhost', port=9000, user='default', password='', database='default')
args = options.DefaultArgs()
# options.get_args()
args.dataflow = 'searched'


# model_layers = "VGG16,RESNET,MOBILENET,MNASNET,TRANSFORMER"
# model_layers = "VGG16"
model_layers = "VGG16,RESNET,MOBILENET,MNASNET,TRANSFORMER"
idx_2_modellayer = {}
shapes = layers.get_shapes(model_layers, False, True, False)
for i, shape in enumerate(shapes):
    sw_space = space.create_software_space(args, shape[1], 2)
    print(f'i:{i}, shape:{shape[0]},size:{sw_space.size}')
    # print(sw_space.params.keys())
    idx_2_modellayer[str(i)]=shape[0]
    continue
    maps = {}
    for param in sw_space.params:
        if len(param.name) == 1:
            maps[param.name] = param.range
    # sw_range_space = [ item.range for item in sw_space.params[0:len(sw_space.params) - 2]]
    # print(sw_range_space)
    combinations = list_combinations_with_name_ids(maps)
    insert_to_clickhouse(client, shape[0], combinations)

print(idx_2_modellayer)
# 关闭连接
client.disconnect()
