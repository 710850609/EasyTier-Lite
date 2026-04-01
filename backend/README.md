# EasyTier-Lite Backend (Go)

Go 语言实现的后端服务，替代原有的 Python 实现。

## 功能模块

- **配置管理** - TOML 配置文件读写
- **节点管理** - 调用 easytier-cli 获取节点列表
- **下载服务** - GitHub Release 下载代理
- **日志服务** - 日志查看接口

## 目录结构

```
backend/
├── main.go                      # 入口
├── go.mod                       # Go 模块
├── internal/
│   ├── handler/                 # HTTP 处理器
│   │   ├── config.go           # 配置相关
│   │   ├── node.go             # 节点相关
│   │   ├── log.go              # 日志相关
│   │   └── download.go         # 下载相关
│   ├── service/                 # 业务逻辑
│   │   ├── config.go           # 配置服务
│   │   └── download.go         # 下载服务
│   └── util/                    # 工具函数
│       └── command.go          # 命令执行
```

## 环境变量

- `ET_CONFIG_DIR` - 配置文件目录（默认：`./temp/config`）
- `ET_BIN_DIR` - EasyTier 二进制目录（默认：`./app/bin`）
- `PORT` - 服务端口（默认：`5666`）

## 运行

```bash
# 开发模式
go run main.go

# 构建
go build -o et-backend main.go

# 运行
./et-backend
```

## API 接口

- `GET /cgi/ThirdParty/EasyTier-Lite/api.cgi/configs/needSetting` - 检查是否需要配置
- `GET /cgi/ThirdParty/EasyTier-Lite/api.cgi/configs` - 获取配置
- `POST /cgi/ThirdParty/EasyTier-Lite/api.cgi/configs` - 保存配置
- `GET /cgi/ThirdParty/EasyTier-Lite/api.cgi/configs/publicPeers` - 获取公共节点
- `GET /cgi/ThirdParty/EasyTier-Lite/api.cgi/configs/download` - 下载配置
- `GET /cgi/ThirdParty/EasyTier-Lite/api.cgi/nodes` - 获取节点列表
- `GET /cgi/ThirdParty/EasyTier-Lite/api.cgi/logs` - 获取日志
- `GET /cgi/ThirdParty/EasyTier-Lite/api.cgi/download/windows` - Windows 下载链接
- `GET /cgi/ThirdParty/EasyTier-Lite/api.cgi/download/android` - Android 下载链接
