#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os


BASE_URI = "/cgi/ThirdParty/EasyTier-Lite"
PARENT_PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# CGI 文件真实路径
CGI_INDEX = os.path.join(PARENT_PROJECT_PATH, 'EasyTier-Lite', 'app', 'ui', 'index.cgi')
CGI_API = os.path.join(PARENT_PROJECT_PATH, 'EasyTier-Lite', 'app', 'ui', 'api.cgi')
BACKEND_PATH = os.path.join(PARENT_PROJECT_PATH, 'server')
LOG_FILE = os.path.join(PARENT_PROJECT_PATH, 'server.log')

ET_BIN_DIR = os.getenv('ET_BIN_DIR', )
ET_CONFIG_FILE = os.getenv('ET_CONFIG_FILE', )
ET_CONFIG_FILE = os.getenv('ET_CONFIG_FILE', )

os.path.join(PARENT_PROJECT_PATH, 'EasyTier-Lite', 'app', 'bin')