#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import urllib.parse
import mimetypes

# 静态文件根目录
BASE_PATH = "/var/apps/EasyTier-Lite/target/ui"

# 从 REQUEST_URI 里拿到 index.cgi 后面的路径
REQUEST_URI = os.environ.get("REQUEST_URI", "")
URI_NO_QUERY = REQUEST_URI.split("?", 1)[0]
REL_PATH = "/"

if "index.cgi" in URI_NO_QUERY:
    REL_PATH = URI_NO_QUERY.split("index.cgi", 1)[1]

if REL_PATH == "" or REL_PATH == "/":
    REL_PATH = "/index.html"

TARGET_FILE = BASE_PATH + REL_PATH

# 防御：禁止 .. 越级访问
if ".." in TARGET_FILE:
    print("Status: 400 Bad Request")
    print("Content-Type: text/plain; charset=utf-8")
    print("")
    print("Bad Request")
    sys.exit(0)

# 判断文件是否存在
if not os.path.isfile(TARGET_FILE):
    print("Status: 404 Not Found")
    print("Content-Type: text/plain; charset=utf-8")
    print("")
    print(f"404 Not Found: {REL_PATH}")
    sys.exit(0)

# 根据扩展名判断 MIME
ext = TARGET_FILE.split(".")[-1].lower()
mime_map = {
    "html": "text/html; charset=utf-8",
    "css": "text/css; charset=utf-8",
    "js": "application/javascript; charset=utf-8",
    "json": "application/json; charset=utf-8",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "svg": "image/svg+xml",
    "woff": "font/woff",
    "woff2": "font/woff2",
}

mime = mime_map.get(ext, "application/octet-stream")

# 输出 HTTP 头部（统一使用二进制模式）
header = f"Content-Type: {mime}\r\n\r\n"
sys.stdout.buffer.write(header.encode('utf-8'))

# 输出文件内容（统一使用二进制模式）
with open(TARGET_FILE, "rb") as f:
    sys.stdout.buffer.write(f.read())
