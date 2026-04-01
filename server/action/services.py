#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import util.http_util as http_util
import util.process_util as process_util
import os
import logging

ET_CONFIG_DIR = os.getenv('ET_CONFIG_DIR', '/var/apps/EasyTier-Lite/shares/EasyTier-Lite')
ET_CONFIG_FILE = os.path.join(ET_CONFIG_DIR, 'config.toml')
ET_BIN_DIR = os.environ.get('ET_BIN_DIR', '/var/apps/EasyTier-Lite/target/bin')
ET_PID_FILE = os.getenv('ET_PID_FILE', '/var/apps/EasyTier-Lite/var/app.pid')
START_CMD = f"{ET_BIN_DIR}/easytier-core --config-file {ET_CONFIG_FILE}"

# 延迟初始化：使用单例模式
_pm = None

def _get_process_manager():
    """获取 ProcessManager 实例（延迟初始化）"""
    global _pm
    logging.info(f"START_CMD: {START_CMD}")
    logging.info(f"ET_PID_FILE: {ET_PID_FILE}")
    if _pm is None:
        _pm = process_util.ProcessManager(START_CMD, ET_PID_FILE)
    return _pm

def status(*kwargs):
    pm = _get_process_manager()
    running = pm.status()
    http_util.http_response_ok({'running': running})

def stop(*kwargs):
    pm = _get_process_manager()
    pm.stop()
    http_util.http_response_ok({})

def start(*kwargs):
    pm = _get_process_manager()
    pm.start()
    http_util.http_response_ok({})

def restart(*kwargs):
    pm = _get_process_manager()
    if (pm.status()):
        pm.stop()
    pm.start()
    http_util.http_response_ok({})