#!/bin/bash

# 检查jq是否安装
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed. Please install jq first." >&2
    exit 1
fi

# API地址
API_URL="https://api.ilingku.com/int/v1/image.360"

# 存储图片URL的数组
urls=()

# 遍历所有图片参数
for image_path in "$@"; do
    # 使用curl上传图片
    response=$(curl -s -X POST -d "url=$image_path" "$API_URL")

    # 解析响应JSON
    code=$(echo "$response" | jq -r '.code')
    msg=$(echo "$response" | jq -r '.msg')
    url=$(echo "$response" | jq -r '.url')

    # 检查上传结果
    if [ "$code" != "200" ]; then
        echo "Upload failed for $image_path: $msg" >&2
        exit 1
    fi

    # 收集成功URL
    urls+=("$url")
done

# 所有请求成功后输出成功信息
echo "Upload Success"

# 输出所有图片URL（Typora会读取这些URL）
for url in "${urls[@]}"; do
    echo "$url"
done