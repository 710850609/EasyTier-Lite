#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import util.http_util as http_util
import logging
import tomlkit
import os

ET_CONFIG_FILE = '/var/apps/EasyTier-Lite/shares/EasyTier-Lite/config.toml'

def need_setting():
    init_file = '/va/sdf/sd/f.txt'
    need_config = not Path(init_file).exists()
    http_util.http_response_ok({"needConfig": need_config})

def public_peers():
    peers = [
        'https://raw.githubusercontent.com/710850609/fpk-EasyTier-Lite/refs/heads/main/peers/peer-1.txt',
        'https://raw.githubusercontent.com/710850609/fpk-EasyTier-Lite/refs/heads/main/peers/peer-2.txt',
        'https://raw.githubusercontent.com/710850609/fpk-EasyTier-Lite/refs/heads/main/peers/peer-3.txt',
        'https://raw.githubusercontent.com/710850609/fpk-EasyTier-Lite/refs/heads/main/peers/peer-4.txt',
        'https://raw.githubusercontent.com/710850609/fpk-EasyTier-Lite/refs/heads/main/peers/peer-5.txt',
    ]
    http_util.http_response_ok(peers)

def download():    
    tmp_file = copy()
    logging.info(f"{tmp_file}")
    http_util.http_response_file(tmp_file, filename="et-fnos.toml")

def copy(): 
    tmp_file = '/tmp/EasyTier-Lite/config-copy.toml'
    
    # 确保目录存在
    os.makedirs(os.path.dirname(tmp_file), exist_ok=True)
    
    with open(ET_CONFIG_FILE, "r", encoding="utf-8") as f:
        doc = tomlkit.parse(f.read())
    # 情况IP
    doc["ipv4"] = ""
    # 设置启用DHCP
    doc["dhcp"] = True

    with open(tmp_file, "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(doc))
    return tmp_file
