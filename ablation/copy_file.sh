#!/bin/bash

# 定义源文件列表
files=(
    "tech-tga-dse-delay-transformer-nvdla.sh"
    "tech-transp-dse-delay-transformer-nvdla.sh"
    "tech-tr-dse-delay-transformer-nvdla.sh"
    "tech-tv-dse-delay-transformer-nvdla.sh"
    "tech-tga-dse-edp-transformer-nvdla.sh"
    "tech-transp-dse-edp-transformer-nvdla.sh"
    "tech-tr-dse-edp-transformer-nvdla.sh"
    "tech-tv-dse-edp-transformer-nvdla.sh"
)

# 循环遍历文件
for file in "${files[@]}"; do
    # 创建新的文件名，替换nvdla为transpeed
    new_file=${file/nvdla/transpeed}

    # 使用cp命令复制文件
    cp "$file" "$new_file"
done

echo "Files copied and renamed successfully."

