import numpy as np
import sys
from array import array


# 从标准输入读取字典数据
input_data = input("")


# data = {'TRANSFORMER_MH_FC_DimReduce_VKQ_0': ['2', '10', '100'],'TRANSFORMER_SD_MatMul_QK_00': ['3', '11', '200'],'TRANSFORMER_SD_MatMul_V_00': ['4', '12', '300']}

# 将输入的字符串解析为字典
data={}
try:
    data = eval(input_data)  # 使用eval()来解析JSON格式的输入，注意：请谨慎使用eval()。
except Exception as e:
    pass



# 初始化一个空列表，用于存储转换后的 NumPy 数组
arrays = []

# 遍历字典中的每个键值对
for key, value in data.items():
    # 将字符数组转换为浮点数数组
    float_array = np.array([float(val) for val in value])
    # 添加到列表中
    arrays.append(float_array)


# 堆叠所有数组为一个张量（垂直堆叠）
tensor = np.vstack(arrays)

# 对张量按列求和，得到一个包含每列和的一维数组
column_sum = np.sum(tensor, axis=0)

# 打印结果
print(column_sum.tolist())
#print(array('f', column_sum))
