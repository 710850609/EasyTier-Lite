#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import json
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger():
    # logging.basicConfig(
    #     level=logging.DEBUG,  # 设置日志级别
    #     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 日志格式
    #     datefmt='%Y-%m-%d %H:%M:%S',  # 日期格式
    #     filename=os.environ.get('LOG_FILE', '/var/apps/EasyTier-Lite/var/http_dispatcher.log'),  # 输出到文件
    #     filemode='a'  # 'a'追加，'w'覆盖
    # )
    # 1. 获取 root logger（不传参数时就是根日志记录器）
    log_dir = '/var/apps/EasyTier-Lite/var/logs'
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    root_logger = logging.getLogger()
    # 2. 设置日志级别（可选，默认为 WARNING，需要调低才能看到 INFO 及以上）
    root_logger.setLevel(logging.INFO)
    # 3. 创建 RotatingFileHandler
    handler = RotatingFileHandler(
        filename=f'{log_dir}/app.log',
        maxBytes=20 * 1024 * 1024,  # 5 MB
        backupCount=5,  # 保留5个备份
        encoding='utf-8'
    )
    # 4. 设置格式并添加 handler
    formatter = logging.Formatter(fmt = '%(asctime)s - %(levelname)s - %(message)s', datefmt = "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    root_logger.handlers.clear()  # 清除所有已有 handler
    root_logger.addHandler(handler)

def setup_env():
    # # 激活server虚拟环境
    backend_path = os.environ.get('BACKEND_PATH', os.path.join(os.path.dirname(__file__), '..', 'backend'))
    backend_path = os.path.abspath(backend_path)
    venv_path = os.path.join(backend_path, '.venv')
    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    site_packages = os.path.join(venv_path, 'lib', python_version, 'site-packages')
    if os.path.exists(site_packages):
        sys.path.insert(0, site_packages)
        bin_path = os.path.join(venv_path, 'bin')
        if os.path.exists(bin_path):
            os.environ['PATH'] = bin_path + ':' + os.environ.get('PATH', '')
    else:
        logging.error(f"找不到python依赖: {site_packages}")

    # 添加backend目录到Python路径
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)

def dispatcher():
    from http_dispatcher import  dispatcher
    os.environ['FRONTEND_PATH'] = f'/var/apps/EasyTier-Lite/target/frontend'
    dispatcher.http_handle(base_uri='/cgi/ThirdParty/EasyTier-Lite/index.cgi', cgi_module=True)

if __name__ == '__main__':
    try:
        setup_logger()
        setup_env()
        dispatcher()
    except Exception as e:
        logging.error(f"CGI服务异常",  exc_info=True)
        print(f"Status: 500")
        print("Content-Type: application/json; charset=utf-8")
        print("")
        print(json.dumps(e, ensure_ascii=False))