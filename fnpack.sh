#!/bin/bash

# 定义函数用于显示用法信息
usage() {
    echo "Usage: $0 build --directory <directory>"
    exit 1
}

# 检查参数数量
if [ "$#" -ne 3 ]; then
    usage
fi

# 检查命令是否为 build
if [ "$1" != "build" ]; then
    usage
fi

# 检查参数是否为 --directory
if [ "$2" != "--directory" ]; then
    usage
fi

# 获取指定目录
directory=$3

# 检查指定目录是否存在
if [ ! -d "$directory" ]; then
    echo "Error: Directory '$directory' does not exist."
    exit 1
fi

build_dir="build_tmp"

rm -rf "$build_dir"
echo "copy files to build directory..."
cp -r "$directory" "$build_dir"  || exit 1

# 进入指定目录
cd "$build_dir" || exit 1
# 检查 app 文件夹是否存在
if [ ! -d "app" ]; then
    echo "Error: 'app' directory does not exist in '$directory'."
    exit 1
fi

# 第一步：压缩 app 文件夹为 app.tgz
echo "Compressing 'app' directory to 'app.tgz'..."
tar -czf app.tgz -C app .

# 检查压缩是否成功
if [ $? -ne 0 ]; then
    echo "Error: Failed to compress 'app' directory."
    exit 1
fi

# 第二步：计算 app.tgz 的 MD5 值并更新 manifest 文件
echo "Calculating MD5 checksum of 'app.tgz'..."
md5_value=$(md5sum app.tgz | awk '{print $1}')
echo "MD5 checksum: $md5_value"
# 检查 MD5 计算是否成功
if [ -z "$md5_value" ]; then
    echo "Error: Failed to calculate MD5 checksum."
    exit 1
fi

# 更新 manifest 文件
echo "Updating checksum in 'manifest' file..."
if [ ! -f "manifest" ]; then
    echo "Error: 'manifest' file does not exist in '$directory'."
    exit 1
fi
sed -i "s|^[[:space:]]*checksum[[:space:]]*=.*|checksum=${md5_value}|" 'manifest'
# 检查是否成功更新
if ! grep -q "^checksum=${md5_value}$" 'manifest'; then
    echo "Appending checksum to 'manifest' file..."
    # 确保追加时换行
    echo -e "\nchecksum=${md5_value}" >> 'manifest'
fi


# 检查写入是否成功
if [ $? -ne 0 ]; then
    echo "Error: Failed to update checksum in 'manifest' file."
    exit 1
fi

# 第三步：压缩指定目录下的所有数据（除 app 外）为 .fpk 文件
echo "remove app directory..."
rm -rf app
fpk_filename="${directory}.fpk"
echo "Compressing all data (excluding 'app') to '$fpk_filename'..."
tar -czf "../$fpk_filename" ./

# 检查压缩是否成功
if [ $? -ne 0 ]; then
    echo "Error: Failed to compress all data."
    exit 1
fi
cd ../

rm -rf "$build_dir"
echo "Packaging completed successfully."