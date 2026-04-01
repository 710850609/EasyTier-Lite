#!/bin/bash

# EasyTier-Lite Backend 构建脚本
# 支持交叉编译为 Linux 可执行文件

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 默认参数
VERSION=${VERSION:-"1.0.0"}
BUILD_TIME=$(date '+%Y-%m-%d %H:%M:%S')
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

# 输出目录
OUTPUT_DIR="./dist"

# 打印信息
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示帮助
show_help() {
    cat << EOF
EasyTier-Lite Backend 构建脚本

用法: ./build.sh [选项]

选项:
    -h, --help          显示帮助信息
    -a, --arch ARCH     目标架构 (amd64, arm64, arm) [默认: amd64]
    -o, --os OS         目标系统 (linux, windows, darwin) [默认: linux]
    -v, --version VER   设置版本号 [默认: 1.0.0]
    -c, --clean         清理构建目录
    -a, --all           构建所有平台

示例:
    ./build.sh                          # 构建 Linux amd64
    ./build.sh -a arm64                 # 构建 Linux arm64
    ./build.sh -o windows -a amd64      # 构建 Windows amd64
    ./build.sh --all                    # 构建所有平台
EOF
}

# 清理构建目录
clean() {
    info "清理构建目录..."
    rm -rf "$OUTPUT_DIR"
    mkdir -p "$OUTPUT_DIR"
}

# 构建函数
build() {
    local os=$1
    local arch=$2
    
    # 设置输出文件名
    local output_name="et-backend-${os}-${arch}"
    if [ "$os" = "windows" ]; then
        output_name="${output_name}.exe"
    fi
    
    info "构建 ${os}/${arch}..."
    
    # 设置环境变量
    export GOOS=$os
    export GOARCH=$arch
    export CGO_ENABLED=0
    
    # 构建参数
    local ldflags="-s -w \
        -X 'main.Version=${VERSION}' \
        -X 'main.BuildTime=${BUILD_TIME}' \
        -X 'main.GitCommit=${GIT_COMMIT}'"
    
    # 执行构建
    go build -ldflags "$ldflags" -o "${OUTPUT_DIR}/${output_name}" main.go
    
    if [ $? -eq 0 ]; then
        info "构建成功: ${OUTPUT_DIR}/${output_name}"
        # 显示文件大小
        ls -lh "${OUTPUT_DIR}/${output_name}" | awk '{print "  大小:", $5}'
    else
        error "构建失败: ${os}/${arch}"
        return 1
    fi
}

# 构建所有平台
build_all() {
    info "开始构建所有平台..."
    
    # Linux
    build linux amd64
    build linux arm64
    build linux arm
    
    # Windows
    build windows amd64
    build windows arm64
    
    # macOS
    build darwin amd64
    build darwin arm64
    
    info "所有平台构建完成!"
}

# 主函数
main() {
    # 默认参数
    TARGET_OS="linux"
    TARGET_ARCH="amd64"
    BUILD_ALL=false
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -a|--arch)
                TARGET_ARCH="$2"
                shift 2
                ;;
            -o|--os)
                TARGET_OS="$2"
                shift 2
                ;;
            -v|--version)
                VERSION="$2"
                shift 2
                ;;
            -c|--clean)
                clean
                exit 0
                ;;
            --all)
                BUILD_ALL=true
                shift
                ;;
            *)
                error "未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 检查 Go 环境
    if ! command -v go &> /dev/null; then
        error "未找到 Go，请先安装 Go"
        exit 1
    fi
    
    info "Go 版本: $(go version)"
    info "版本号: $VERSION"
    info "构建时间: $BUILD_TIME"
    info "Git Commit: $GIT_COMMIT"
    
    # 创建输出目录
    mkdir -p "$OUTPUT_DIR"
    
    # 下载依赖
    info "下载依赖..."
    go mod tidy
    
    # 执行构建
    if [ "$BUILD_ALL" = true ]; then
        build_all
    else
        build "$TARGET_OS" "$TARGET_ARCH"
    fi
    
    info "构建完成! 输出目录: $OUTPUT_DIR"
    ls -lh "$OUTPUT_DIR"
}

# 执行主函数
main "$@"
