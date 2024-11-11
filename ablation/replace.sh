#!/bin/bash

# 定义文件列表
#files=(
#    "tech-tga-dse-delay-transformer-transpeed.sh"
#    "tech-transp-dse-delay-transformer-transpeed.sh"
#    "tech-tr-dse-delay-transformer-transpeed.sh"
#    "tech-tv-dse-delay-transformer-transpeed.sh"
#    "tech-tga-dse-edp-transformer-transpeed.sh"
#    "tech-transp-dse-edp-transformer-transpeed.sh"
#    "tech-tr-dse-edp-transformer-transpeed.sh"
#    "tech-tv-dse-edp-transformer-transpeed.sh"
#)

files=(tech-tga-dse-edp-transformer-nvdla.sh  tech-transp-dse-edp-transformer-nvdla.sh  tech-tr-dse-edp-transformer-nvdla.sh  tech-tv-dse-edp-transformer-nvdla.sh)
# 遍历文件列表
for file in "${files[@]}"; do
    # 使用sed进行替换
    #sed -i 's/-dataflow fixed/-dataflow searched/g' "$file"
    sed -i 's/--sw-trials 100/--sw-trials 50/g' "$file"
    echo $file
done

echo "Content replacement completed."

