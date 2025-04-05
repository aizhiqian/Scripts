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

# 判断是否为URL的函数
is_url() {
    local regex='^(http|https)://'
    [[ $1 =~ $regex ]]
    return $?
}

# 遍历所有图片参数
for image_path in "$@"; do
    # 判断是本地文件还是远程URL
    if is_url "$image_path"; then
        # 使用url参数上传远程图片链接
        response=$(curl -s -X POST -d "url=$image_path" "$API_URL")
    else
        # 检查本地文件是否存在
        if [ ! -f "$image_path" ]; then
            echo "Error: File not found: $image_path" >&2
            exit 1
        fi

        # 使用file参数上传本地文件
        response=$(curl -s -X POST -F "file=@$image_path" "$API_URL")
    fi

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
echo "Upload Success:"

# 输出所有图片URL（Typora会读取这些URL）
for url in "${urls[@]}"; do
    echo "$url"
done
