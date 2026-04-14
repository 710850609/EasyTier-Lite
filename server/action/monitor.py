#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import util.common_util as cmd_util
import util.http_util as http_util
import json
import os


TRIM_APPNAME = os.getenv('TRIM_APPNAME', 'EasyTier-Lite')
TRIM_APPDEST = os.getenv('TRIM_APPDEST', f'/var/apps/{TRIM_APPNAME}/target')
TRIM_PKGVAR = os.getenv('TRIM_PKGVAR', f'/var/apps/{TRIM_APPNAME}/var')
TRIM_SHARE_DIR = os.getenv('TRIM_SHARE_DIR', f'/var/apps/{TRIM_APPNAME}/shares/{TRIM_APPNAME}')

ET_BIN_DIR = f"{TRIM_APPDEST}/bin"
ET_CONFIG_FILE = f'{TRIM_SHARE_DIR}/config.toml'
ET_CONFIG_INIT_FILE = f'{TRIM_PKGVAR}/.init'
ET_PEER_META_FILE = f'{TRIM_PKGVAR}/peer-txt-meta.json'

def list(*kwargs):
    """
    获取节点列表
    :param request_data: 请求数据（可选）
    """
    result = cmd_util.run_cmd(f'{ET_BIN_DIR}/easytier-cli --output json peer')
    peer_list = json.loads(result)
    http_util.http_response_ok(peer_list)
