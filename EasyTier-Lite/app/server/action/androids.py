#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import util.et_util as et_util
import util.http_util as http_util
import util.github_util as github_util

et_min_version = "2.5.0"

def download():
    output_dir = f"/var/apps/EasyTier-Lite/shares/EasyTier-Lite"
    output_file = et_util.download_package(output_dir, 'android', None)
    http_util.http_response_file(output_file)

def download_url():
    url = github_util.get_download_url_proxy('https://github.com/EasyTier/EasyTier/releases/latest/download/app-universal-release.apk')
    http_util.http_response_ok(url)