#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import util.http_util as http_util
import logging
import tomlkit


def download():    
    tmp_file = copy()
    logging.info(f"{tmp_file}")
    http_util.http_response_file(tmp_file, filename="et-fnos.toml")

def copy(): 
    src_file = '/var/apps/EasyTier-Lite/shares/EasyTier-Lite/config.toml'
    tmp_file = '/tmp/EasyTier-Lite/config-copy.toml'
    with open(src_file, "r", encoding="utf-8") as f:
        doc = tomlkit.parse(f.read())
    # 情况IP
    doc["ipv4"] = ""
    # 设置启用DHCP
    doc["dhcp"] = True

    with open(tmp_file, "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(doc))
    return tmp_file