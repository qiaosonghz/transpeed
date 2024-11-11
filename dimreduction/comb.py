def get_combination_by_id(arrays, id):
    combination = []
    for i in range(len(arrays)):
        index = id % len(arrays[i])  # 取余数得到当前数组的索引
        combination.append(arrays[i][index])
        id //= len(arrays[i])  # 更新id，准备处理下一个数组
    return combination

def list_combinations_with_ids(arrays):
    num_arrays = len(arrays)
    total_combinations = 1
    for arr in arrays:
        total_combinations *= len(arr)

    combinations_with_ids = []
    for i in range(total_combinations):
        combination = get_combination_by_id(arrays, i)
        combinations_with_ids.append((i, combination))

    return combinations_with_ids

# 示例用法
arrays = [[1, 2], [3, 4], [5, 6]]
combinations_with_ids = list_combinations_with_ids(arrays)

for combo_id, combination in combinations_with_ids:
    print(f"ID {combo_id}: {combination}")

