#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import util.http_util as http_util
import logging
import tomlkit
import os

TRIM_APPNAME = os.getenv('TRIM_APPNAME', 'EasyTier-Lite')
TRIM_APPDEST = os.getenv('TRIM_APPDEST', f'/var/apps/{TRIM_APPNAME}/target')
TRIM_PKGVAR = os.getenv('TRIM_PKGVAR', f'/var/apps/{TRIM_APPNAME}/var')
TRIM_SHARE_DIR = os.getenv('TRIM_SHARE_DIR', f'/var/apps/{TRIM_APPNAME}/shares/{TRIM_APPNAME}')

ET_CONFIG_FILE = f'{TRIM_SHARE_DIR}/config.toml'
ET_CONFIG_INIT_FILE = f'{TRIM_PKGVAR}/.init'

GITHUB_PROXY = "https://ghfast.top"

def version(*kwargs):
    version = cmd_util.run_cmd(f'{ET_BIN_DIR}/easytier-core --version')
    http_util.http_response_ok(version)

def install(data, *kwargs):
    version = data['version']
    if not version:
        http_util.http_response_error('版本不能为空')
    http_util.http_response_ok(f'安装{version}版本成功')
