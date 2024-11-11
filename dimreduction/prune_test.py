import sys

sys.path.append("..")
sys.path.append("./")
sys.path.append("./src")
sys.path.append("../src")

from src import space
from src import options
from src import layers
from src import search_utils

args = options.DefaultArgs()
args.dataflow = 'searched'

hw_point = space.Point(eval("{'num_simd_lane':14,'bit_width':8,'bandwidth':186,'l0_buf_size':172032,'l1_buf_size':204800,'subclusters':[286,1]}"))
sw_point = space.Point(eval("{'K':[64,1,1],'C':[3,1,1],'N':[1,1,1],'X':[14,1,16],'Y':[1,224,1],'R':[1,1,3],'S':[3,1,1],'l0_spatial_dim':'Y','l1_spatial_dim':'X'}"))
mae_point = search_utils.convert_point_to_maestro(args, hw_point, sw_point, 2)
print(mae_point)

'''

(14, 8, 186, 'searched', [L1
buf_size: 204800
num_subcluster: 1
tile_sizes: {'N': 1, 'K': 64, 'C': 3, 'X': 14, 'Y': 224, 'R': 1, 'S': 3}
spatial_dim: X
, L0
buf_size: 172032
num_subcluster: 286
tile_sizes: {'N': 1, 'K': 64, 'C': 3, 'X': 14, 'Y': 1, 'R': 1, 'S': 3}
spatial_dim: Y
])

------------------------------------------------------------------------------------------------------------------------------------------------------

SELECT
    ((((tile_k[1]) * (tile_c[1])) * (tile_r[1])) * (tile_s[1])) + ((((tile_c[1]) * (tile_n[1])) * (tile_x[1])) * (tile_y[1])) AS l1_occupy,
    l1_occupy / 172032 AS l1_rate,
    ((((((((tile_k[1]) * (tile_c[1])) * (tile_r[1])) * (tile_s[1])) * (tile_k[2])) * (tile_c[2])) * (tile_r[2])) * (tile_s[2])) + ((((((((tile_c[1]) * (tile_n[1])) * (tile_x[1])) * (tile_y[1])) * (tile_c[2])) * (tile_n[2])) * (tile_x[2])) * (tile_y[2])) AS l2_occupy,
    l2_occupy / 204800 AS l2_rate
FROM default.modellayer_tile_space
WHERE (model_layer = 'VGG16_CONV01') AND (tile_index = 0)

Query id: 45ef2884-76b8-4091-8e99-ec56c210d3fa

┌─l1_occupy─┬────────────l1_rate─┬─l2_occupy─┬───l2_rate─┐
│    152256 │ 0.8850446428571429 │    152256 │ 0.7434375 │
└───────────┴────────────────────┴───────────┴───────────┘


SELECT
    ((((tile_k[1]) * (tile_c[1])) * (tile_r[1])) * (tile_s[1])) + ((((tile_c[1]) * (tile_n[1])) * (tile_x[1])) * (tile_y[1])) AS l1_occupy,
    l1_occupy / 172032 AS l1_rate,
    ((((((((tile_k[1]) * (tile_c[1])) * (tile_r[1])) * (tile_s[1])) * (tile_k[2])) * (tile_c[2])) * (tile_r[2])) * (tile_s[2])) + ((((((((tile_c[1]) * (tile_n[1])) * (tile_x[1])) * (tile_y[1])) * (tile_c[2])) * (tile_n[2])) * (tile_x[2])) * (tile_y[2])) AS l2_occupy,
    l2_occupy / 204800 AS l2_rate
FROM default.modellayer_tile_space
WHERE (model_layer = 'VGG16_CONV01') AND (tile_index = 938364)


┌─l1_occupy─┬───────────────l1_rate─┬─l2_occupy─┬─l2_rate─┐
│       618 │ 0.0035923549107142855 │      9984 │ 0.04875 │
└───────────┴───────────────────────┴───────────┴─────────┘
'''