import sys

sys.path.append("..")
sys.path.append("./")
sys.path.append("./src")
sys.path.append("../src")

from src import space
from src import options
from src import layers
from clickhouse_driver import Client

import re
import json
import subprocess

def parse_and_update(client, data_line):
    if len(data_line) < 5:
            return
    # print(data_line)
    layer_match = re.search(r'(\d+)\s+opt_layer', data_line)
    layer_number = layer_match.group(1)

    # 使用正则表达式提取字段
    pattern = r'(\w+)\s+([\d.e+-]+)\s+'
    fields = re.findall(pattern, data_line)

    # 创建一个字典来存储字段
    data_dict = {}
    for i in range(0, len(fields), 1):
        key = fields[i][0]
        value = fields[i][1]
        data_dict[key] = value

    data_dict['opt_layer']=layer_number

    point_match = re.search(r'point\s+(.*?)\s+feats', data_line)
    if point_match:
        point_data_str = point_match.group(1)
    else:
        raise ValueError("point field not found")

    # 使用 json.loads() 解析 point 字段
    point_data = json.loads(point_data_str.replace("'", "\""))
    # 将点数据解析为字典

    # query = f"alter table default.modellayer_tile_space update edp ={float(data_dict['edp'])} " \
    #         f" where  (model_layer = '{index2ch[data_dict['opt_layer']]}') AND (tile_k = {point_data['K']}) AND (tile_c = {point_data['C']}) AND (tile_n = {point_data['N']}) " \
    #         f" AND (tile_x = {point_data['X']}) AND (tile_y = {point_data['Y']}) AND (tile_r = {point_data['R']}) AND (tile_s = {point_data['S']})" \

            # f" settings mutations_sync=1"

    query = f"select tile_index, l1_occupy, l2_occupy from default.modellayer_tile_space " \
            f" where  (model_layer = '{index2ch[data_dict['opt_layer']]}') AND (tile_k = {point_data['K']}) AND (tile_c = {point_data['C']}) AND (tile_n = {point_data['N']}) " \
            f" AND (tile_x = {point_data['X']}) AND (tile_y = {point_data['Y']}) AND (tile_r = {point_data['R']}) AND (tile_s = {point_data['S']})"
    result = client.execute(query)

    tile_index = result[0][0]
    l1_occupy = result[0][1]
    l2_occupy = result[0][2]


    insert_query = f"INSERT INTO default.modellayer_tile_space (model_layer, tile_index, tile_k, tile_c, tile_n, tile_x, tile_y, tile_r, tile_s, l1_occupy, l2_occupy, edp, delay) " \
    f"VALUES ('{index2ch[data_dict['opt_layer']]}', {tile_index},{point_data['K']}, {point_data['C']}, {point_data['N']} " \
    f" , {point_data['X']}, {point_data['Y']} , {point_data['R']} , {point_data['S']}, {l1_occupy}, {l2_occupy}, {float(data_dict['edp'])}, {data_dict['delay']})"

    print(insert_query)
    client.execute(insert_query)

files=['/root/hourz/spotlight_dev/results/Edge/Spotlight/EDP/ALL/out.txt202308090600', \
'/root/hourz/spotlight_dev/results/Edge/Spotlight/EDP/ALL/out.txt202308090601', \
'/root/hourz/spotlight_dev/results/Edge/Spotlight/EDP/ALL/out.txt202308080222', \
'/root/hourz/spotlight_dev/results/Edge/Spotlight/EDP/ALL/out.txt202308090602', \
'/root/hourz/spotlight_dev/results/Edge/Spotlight/EDP/ALL/out.txt202308090604', \
'/root/hourz/spotlight_dev/results/Edge/Spotlight/EDP/ALL/out.txt202308090558', \
'/root/hourz/spotlight_dev/results/Edge/Spotlight/EDP/ALL/out.txt202308090559', \
'/root/hourz/spotlight_dev/results/Edge/Spotlight/EDP/ALL/out.txt202308090251']


cat_process = subprocess.Popen(['cat'] + files, stdout=subprocess.PIPE, text=True)
grep_process = subprocess.Popen(['grep', 'opt_layer'], stdin= cat_process.stdout, stdout=subprocess.PIPE, text=True)
# output_lines = grep_process.communicate()[0].decode('utf-8')
output_lines = grep_process.stdout
# print(output_lines)
# 获取shell命令的返回结果
# result = subprocess.run(['cat',  ' '.join(files) + ' | grep opt_layer'], capture_output=True, text=True)
# result = subprocess.run(['/usr/bin/grep', ' opt_layer ' + ' '.join(files)], capture_output=True, text=True)
# output_lines = result.stdout.splitlines()  # 获取输出结果，并去除首尾空白字符

index2ch = {'0': 'VGG16_CONV01', '1': 'VGG16_CONV02', '2': 'VGG16_CONV03', '3': 'VGG16_CONV04', '4': 'VGG16_CONV05', '5': 'VGG16_CONV06', '6': 'VGG16_CONV07', '7': 'VGG16_CONV08', '8': 'VGG16_CONV09', '9': 'VGG16_CONV10', '10': 'VGG16_CONV11', '11': 'VGG16_CONV12', '12': 'VGG16_CONV13', '13': 'RESNET50_CONV1', '14': 'RESNET50_CONV2_1_1', '15': 'RESNET50_CONV2_1_2', '16': 'RESNET50_CONV2_1_3', '17': 'RESNET50_CONV2_1_Residual', '18': 'RESNET50_CONV2_2_1', '19': 'RESNET50_CONV2_2_2', '20': 'RESNET50_CONV2_2_3', '21': 'RESNET50_CONV2_2_Residual', '22': 'RESNET50_CONV2_3_1', '23': 'RESNET50_CONV2_3_2', '24': 'RESNET50_CONV2_3_3', '25': 'RESNET50_CONV2_3_Residual', '26': 'RESNET50_CONV3_1_1', '27': 'RESNET50_CONV3_1_2', '28': 'RESNET50_CONV3_1_3', '29': 'RESNET50_CONV3_1_Residual', '30': 'RESNET50_CONV3_2_1', '31': 'RESNET50_CONV3_2_2', '32': 'RESNET50_CONV3_2_3', '33': 'RESNET50_CONV3_3_1', '34': 'RESNET50_CONV3_3_2', '35': 'RESNET50_CONV3_3_3', '36': 'RESNET50_CONV3_3_Residual', '37': 'RESNET50_CONV3_4_1', '38': 'RESNET50_CONV3_4_2', '39': 'RESNET50_CONV3_4_3', '40': 'RESNET50_CONV3_4_Residual', '41': 'RESNET50_CONV4_1_1', '42': 'RESNET50_CONV4_1_2', '43': 'RESNET50_CONV4_1_3', '44': 'RESNET50_CONV4_1_Residual', '45': 'RESNET50_CONV4_2_1', '46': 'RESNET50_CONV4_2_2', '47': 'RESNET50_CONV4_2_3', '48': 'RESNET50_CONV4_2_Residual', '49': 'RESNET50_CONV4_3_1', '50': 'RESNET50_CONV4_3_2', '51': 'RESNET50_CONV4_3_3', '52': 'RESNET50_CONV4_3_Residual', '53': 'RESNET50_CONV4_4_1', '54': 'RESNET50_CONV4_4_2', '55': 'RESNET50_CONV4_4_3', '56': 'RESNET50_CONV4_4_Residual', '57': 'RESNET50_CONV4_5_1', '58': 'RESNET50_CONV4_5_2', '59': 'RESNET50_CONV4_5_3', '60': 'RESNET50_CONV4_5_Residual', '61': 'RESNET50_CONV4_6_1', '62': 'RESNET50_CONV4_6_2', '63': 'RESNET50_CONV4_6_3', '64': 'RESNET50_CONV4_6_Residual', '65': 'RESNET50_CONV5_1_1', '66': 'RESNET50_CONV5_1_2', '67': 'RESNET50_CONV5_1_3', '68': 'RESNET50_CONV5_1_Residual', '69': 'RESNET50_CONV5_2_1', '70': 'RESNET50_CONV5_2_2', '71': 'RESNET50_CONV5_2_3', '72': 'RESNET50_CONV5_2_Residual', '73': 'RESNET50_CONV5_3_1', '74': 'RESNET50_CONV5_3_2', '75': 'RESNET50_CONV5_3_3', '76': 'RESNET50_CONV5_3_Residual', '77': 'RESNET50_FC1000', '78': 'MOBILENET_CONV1', '79': 'MOBILENET_Bottleneck1_1_1', '80': 'MOBILENET_Bottleneck1_1_2', '81': 'MOBILENET_Bottleneck1_1_3', '82': 'MOBILENET_Bottleneck1_1_Residual', '83': 'MOBILENET_Bottleneck2_1_1', '84': 'MOBILENET_Bottleneck2_1_2', '85': 'MOBILENET_Bottleneck2_1_3', '86': 'MOBILENET_Bottleneck2_2_1', '87': 'MOBILENET_Bottleneck2_2_2', '88': 'MOBILENET_Bottleneck2_2_3', '89': 'MOBILENET_Bottleneck3_1_1', '90': 'MOBILENET_Bottleneck3_1_2', '91': 'MOBILENET_Bottleneck3_1_3', '92': 'MOBILENET_Bottleneck3_2_1', '93': 'MOBILENET_Bottleneck3_2_2', '94': 'MOBILENET_Bottleneck3_2_3', '95': 'MOBILENET_Bottleneck3_2_Residual', '96': 'MOBILENET_Bottleneck3_3_1', '97': 'MOBILENET_Bottleneck3_3_2', '98': 'MOBILENET_Bottleneck3_3_3', '99': 'MOBILENET_Bottleneck4_1_1', '100': 'MOBILENET_Bottleneck4_1_2', '101': 'MOBILENET_Bottleneck4_1_3', '102': 'MOBILENET_Bottleneck4_2_1', '103': 'MOBILENET_Bottleneck4_2_2', '104': 'MOBILENET_Bottleneck4_2_3', '105': 'MOBILENET_Bottleneck4_2_Residual', '106': 'MOBILENET_Bottleneck4_3_1', '107': 'MOBILENET_Bottleneck4_3_2', '108': 'MOBILENET_Bottleneck4_3_3', '109': 'MOBILENET_Bottleneck4_3_Residual', '110': 'MOBILENET_Bottleneck4_4_1', '111': 'MOBILENET_Bottleneck4_4_2', '112': 'MOBILENET_Bottleneck4_4_3', '113': 'MOBILENET_Bottleneck5_1_1', '114': 'MOBILENET_Bottleneck5_1_2', '115': 'MOBILENET_Bottleneck5_1_3', '116': 'MOBILENET_Bottleneck5_2_1', '117': 'MOBILENET_Bottleneck5_2_2', '118': 'MOBILENET_Bottleneck5_2_3', '119': 'MOBILENET_Bottleneck6_1_1', '120': 'MOBILENET_Bottleneck6_1_2', '121': 'MOBILENET_Bottleneck6_2_1', '122': 'MOBILENET_Bottleneck6_2_2', '123': 'MOBILENET_Bottleneck6_2_3', '124': 'MOBILENET_Bottleneck6_2_Residual', '125': 'MOBILENET_Bottleneck6_3_1', '126': 'MOBILENET_Bottleneck6_3_2', '127': 'MOBILENET_Bottleneck6_3_3', '128': 'MOBILENET_Bottleneck7_1_1', '129': 'MOBILENET_Bottleneck7_1_2', '130': 'MOBILENET_Bottleneck7_1_3', '131': 'MOBILENET_CONV2D_2', '132': 'MOBILENET_CONV2D_3', '133': 'MNASNET_Conv2d-1', '134': 'MNASNET_Conv2d-2', '135': 'MNASNET_Conv2d-3', '136': 'MNASNET_Conv2d-4', '137': 'MNASNET_Conv2d-5', '138': 'MNASNET_Conv2d-6', '139': 'MNASNET_Conv2d-7', '140': 'MNASNET_Conv2d-8', '141': 'MNASNET_Conv2d-9', '142': 'MNASNET_Conv2d-10', '143': 'MNASNET_Conv2d-11', '144': 'MNASNET_Conv2d-12', '145': 'MNASNET_Conv2d-13', '146': 'MNASNET_Conv2d-14', '147': 'MNASNET_Conv2d-15', '148': 'MNASNET_Conv2d-16', '149': 'MNASNET_Conv2d-17', '150': 'MNASNET_Conv2d-18', '151': 'MNASNET_Conv2d-19', '152': 'MNASNET_Conv2d-20', '153': 'MNASNET_Conv2d-21', '154': 'MNASNET_Conv2d-22', '155': 'MNASNET_Conv2d-23', '156': 'MNASNET_Conv2d-24', '157': 'MNASNET_Conv2d-25', '158': 'MNASNET_Conv2d-26', '159': 'MNASNET_Conv2d-27', '160': 'MNASNET_Conv2d-28', '161': 'MNASNET_Conv2d-29', '162': 'MNASNET_Conv2d-30', '163': 'MNASNET_Conv2d-31', '164': 'MNASNET_Conv2d-32', '165': 'MNASNET_Conv2d-33', '166': 'MNASNET_Conv2d-34', '167': 'MNASNET_Conv2d-35', '168': 'MNASNET_Conv2d-36', '169': 'MNASNET_Conv2d-37', '170': 'MNASNET_Conv2d-38', '171': 'MNASNET_Conv2d-39', '172': 'MNASNET_Conv2d-40', '173': 'MNASNET_Conv2d-41', '174': 'MNASNET_Conv2d-42', '175': 'MNASNET_Conv2d-43', '176': 'MNASNET_Conv2d-44', '177': 'MNASNET_Conv2d-45', '178': 'MNASNET_Conv2d-46', '179': 'MNASNET_Conv2d-47', '180': 'MNASNET_Conv2d-48', '181': 'MNASNET_Conv2d-49', '182': 'MNASNET_Conv2d-50', '183': 'MNASNET_Conv2d-51', '184': 'MNASNET_Conv2d-52', '185': 'MNASNET_Linear-53', '186': 'TRANSFORMER_MH_FC_DimReduce_VKQ_0', '187': 'TRANSFORMER_SD_MatMul_QK_00', '188': 'TRANSFORMER_SD_MatMul_V_00', '189': 'TRANSFORMER_SD_MatMul_QK_01', '190': 'TRANSFORMER_SD_MatMul_V_01', '191': 'TRANSFORMER_SD_MatMul_QK_02', '192': 'TRANSFORMER_SD_MatMul_V_02', '193': 'TRANSFORMER_SD_MatMul_QK_03', '194': 'TRANSFORMER_SD_MatMul_V_03', '195': 'TRANSFORMER_SD_MatMul_QK_04', '196': 'TRANSFORMER_SD_MatMul_V_04', '197': 'TRANSFORMER_SD_MatMul_QK_05', '198': 'TRANSFORMER_SD_MatMul_V_05', '199': 'TRANSFORMER_MH_FC_DimRecast_0', '200': 'TRANSFORMER_FF_A_0', '201': 'TRANSFORMER_FF_B_0', '202': 'TRANSFORMER_FinalLinear'}


# 连接到ClickHouse数据库
client = Client('localhost')

# 逐行解析, 将数据写入ClickHouse表

# data_line = "       202 opt_layer target 7.0312e+12 edp 7.0312e+12 energy 2.8984e+06 delay 2.4259e+06 throughput 1.3832e+01 area 1.2242e+08 power 4.321380e+03 point {'K':[2,128,2],'C':[1,1,1],'N':[4,32,1],'X':[64,8,1],'Y':[1,1,1],'R':[1,1,1],'S':[64,8,1],'l0_spatial_dim':'X','l1_spatial_dim':'S'} feats [16, 0.0, 1, 262144, 933, 4.484375] t 298.94610388204455 sec"
# parse_and_update(client, data_line)
for data_line in output_lines:
    # print(data_line)
    parse_and_update(client, data_line)

client.disconnect()


