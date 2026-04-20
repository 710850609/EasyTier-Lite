#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import logging
from pathlib import Path
import json

# 配置日志
# Windows 控制台编码处理
if sys.platform == 'win32':
    import io
    # 强制 stdout/stderr 使用 utf-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def setup_env():
    global BASE_URI, BACKEND_PATH, FRONTEND_PATH, LOG_FILE, ET_BIN_DIR, LOG_DIR, CONFIG_DIR, DATA_DIR, CGI_INDEX, CGI_API, PACKAGE_PATH
    BASE_URI = "/cgi/ThirdParty/EasyTier-Lite/index.cgi"
    # 是否在 PyInstaller 打包环境中
    WORK_DIR = None
    if getattr(sys, 'frozen', False):
        print("打包模式运行...")
        # _MEIPASS 是 PyInstaller 解压资源的临时目录
        WORK_DIR = str(Path(os.path.dirname(sys.executable)).absolute())
        Path(WORK_DIR).mkdir(parents=True, exist_ok=True)
        FRONTEND_PATH = os.path.abspath(os.path.join(sys._MEIPASS, 'frontend'))
        BACKEND_PATH = WORK_DIR
        CGI_INDEX = os.path.abspath(os.path.join(sys._MEIPASS, 'htt_cgi', 'index.htt_cgi'))
        CGI_API = os.path.abspath(os.path.join(sys._MEIPASS, 'htt_cgi', 'api.htt_cgi'))
        PACKAGE_PATH = str(sys._MEIPASS)
    else:
        print("本地模式运行...")
        project_root_path = Path(__file__).absolute().parent.parent.parent
        WORK_DIR = str(project_root_path.joinpath('temp').joinpath('EasyTier-Lite').absolute())
        Path(WORK_DIR).mkdir(parents=True, exist_ok=True)
        FRONTEND_PATH = str(project_root_path.joinpath('frontend').joinpath('dist'))
        BACKEND_PATH = str(Path(__file__).absolute().parent)
        CGI_INDEX = os.path.abspath(os.path.join(BACKEND_PATH, 'htt_cgi', 'index.htt_cgi'))
        CGI_API = os.path.abspath(os.path.join(BACKEND_PATH, 'htt_cgi', 'api.htt_cgi'))
        PACKAGE_PATH = ''

    LOG_FILE = os.path.join(WORK_DIR, 'logs', 'server.log')
    ET_BIN_DIR = os.path.join(WORK_DIR, 'core')
    LOG_DIR = os.path.join(WORK_DIR, 'logs')
    CONFIG_DIR = os.path.join(WORK_DIR, 'config')
    DATA_DIR = os.path.join(WORK_DIR, 'data')

    Path(ET_BIN_DIR).mkdir(parents=True, exist_ok=True)
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    Path(CONFIG_DIR).mkdir(parents=True, exist_ok=True)
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    pass

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),  # 输出到文件
            logging.StreamHandler(sys.stdout)  # 输出到控制台
        ]
    )

    logging.info(f"BASE_URI: {BASE_URI}")
    logging.info(f"BACKEND_PATH: {BACKEND_PATH}")
    logging.info(f"FRONTEND_PATH: {FRONTEND_PATH}")
    logging.info(f"LOG_FILE: {LOG_FILE}")
    logging.info(f"CONFIG_DIR: {CONFIG_DIR}")
    logging.info(f"DATA_DIR: {DATA_DIR}")
    logging.info(f"CGI_API: {CGI_API}")


# def get_project_path() -> Path:
#     """获取项目路径，兼容源码执行和 PyInstaller 打包"""
#     # 1. 优先使用环境变量
#     if 'DATA_DIR' in os.environ:
#         return Path(os.environ['DATA_DIR']).absolute()
#
#     # 2. 检测是否在 PyInstaller 打包环境中
#     if getattr(sys, 'frozen', False):
#         # PyInstaller 打包后使用可执行文件所在目录
#         return Path(os.path.dirname(sys.executable)).absolute()
#
#     # 3. 源码执行，从当前文件位置推算
#     return Path(__file__).parent.absolute()

# def get_frontend_path() -> str:
#     """获取资源路径，兼容源码执行和 PyInstaller 打包"""
#     if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
#         # _MEIPASS 是 PyInstaller 解压资源的临时目录
#         return os.path.abspath(os.path.join(sys._MEIPASS, 'frontend'))
#     else:
#         # 源码执行，从当前文件位置推算
#         return str(get_project_path().absolute().parent.parent.joinpath('frontend').joinpath('dist'))

# project_path = get_project_path()
# print(f"project_path: {project_path}")

# 虚拟 base URI
# BASE_URI = "/htt_cgi/ThirdParty/EasyTier-Lite"
# BACKEND_PATH = str(project_path)
# print(f"BACKEND_PATH: {BACKEND_PATH}")
# FRONTEND_PATH = get_frontend_path()
# WORK_DIR = project_path.parent.parent.joinpath('temp').joinpath('EasyTier-Lite').absolute()
# if getattr(sys, 'frozen', False):
#     WORK_DIR = project_path.absolute()
#
# Path(WORK_DIR).mkdir(parents=True, exist_ok=True)
#
# LOG_FILE = os.path.join(WORK_DIR, 'logs', 'server.log')
# ET_BIN_DIR = os.path.join(WORK_DIR, 'core')
# LOG_DIR = os.path.join(WORK_DIR, 'logs')
# CONFIG_DIR = os.path.join(WORK_DIR, 'config')
# DATA_DIR = os.path.join(WORK_DIR, 'data')

# CGI 文件真实路径
# CGI_INDEX = os.path.abspath(os.path.join(BACKEND_PATH, 'htt_cgi', 'index.htt_cgi'))
# CGI_API = os.path.abspath(os.path.join(BACKEND_PATH, 'htt_cgi', 'api.htt_cgi'))
#
#
# Path(ET_BIN_DIR).mkdir(parents=True, exist_ok=True)
# Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
# Path(CONFIG_DIR).mkdir(parents=True, exist_ok=True)
# Path(DATA_DIR).mkdir(parents=True, exist_ok=True)





class CGIProxyHandler(BaseHTTPRequestHandler):
    """处理 HTTP 请求并转发给 CGI 脚本"""
    
    def do_GET(self):
        """处理 GET 请求"""
        self.handle_request()
    
    def do_POST(self):
        """处理 POST 请求"""
        self.handle_request()
    
    def handle_request(self):
        """处理请求的核心逻辑"""
        try:
            # 解析请求路径
            parsed_path = urllib.parse.urlparse(self.path)
            path = parsed_path.path
            
            # 检查是否以 BASE_URI 开头
            # if not path.startswith(BASE_URI):
            #     self.send_error(404, f"Path must start with {BASE_URI}")
            #     return
            
            # 提取 BASE_URI 之后的路径作为 PATH_INFO
            path_info = path[len(BASE_URI):]
            if not path_info or path_info == "/":
                path_info = "/"
            
            # 构建完整的 REQUEST_URI
            request_uri = path
            if parsed_path.query:
                request_uri = f"{path}?{parsed_path.query}"
            
            # logging.debug(f"Request: path={path}, path_info={path_info}, query={parsed_path.query}")
            
            # 根据路径决定调用哪个 CGI
            # 如果 path_info 以 /index.htt_cgi 开头，使用 index.htt_cgi
            if path_info.startswith("/index.htt_cgi"):
                cgi_script = CGI_INDEX
                # 保持原有的 path_info 不变，让 index.htt_cgi 自己解析
                cgi_path_info = path_info
            # 如果 path_info 以 /api.htt_cgi 开头，使用 api.htt_cgi
            elif path_info.startswith("/api.htt_cgi"):
                cgi_script = CGI_API
                # 保持原有的 path_info 不变，让 api.htt_cgi 自己解析
                cgi_path_info = path_info
            else:
                # 默认当作 index.htt_cgi 处理（兼容根路径访问）
                cgi_script = CGI_INDEX
                cgi_path_info = path_info
            
            # logging.debug(f"Routing to: {cgi_script}, cgi_path_info={cgi_path_info}")
            self.run_cgi(cgi_script, cgi_path_info, parsed_path.query, request_uri)
                
        except Exception as e:
            logging.error(f"Request handling error: {e}", exc_info=True)
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def run_cgi(self, cgi_script, path_info, query_string, request_uri):
        """执行 CGI 脚本并返回结果"""
        try:
            # 检查 CGI 文件是否存在
            # if not os.path.isfile(cgi_script):
            #     self.send_error(404, f"CGI script not found: {cgi_script}")
            #     return
            
            # 检查是否可执行
            # if not os.access(cgi_script, os.X_OK):
            #     try:
            #         os.chmod(cgi_script, 0o755)
            #     except Exception as e:
            #         logging.warning(f"Failed to chmod {cgi_script}: {e}")
            
            # 获取请求体（POST 请求）
            stdin_data = None
            content_length = self.headers.get('Content-Length')
            if self.command == 'POST' and content_length:
                try:
                    content_length = int(content_length)
                    if content_length > 0:
                        stdin_data = self.rfile.read(content_length)
                except ValueError:
                    pass
            
            # 构建环境变量
            env = os.environ.copy()
            env.update({
                'PACKAGE_PATH': PACKAGE_PATH,
                'BACKEND_PATH': BACKEND_PATH,
                'FRONTEND_PATH': FRONTEND_PATH,
                'LOG_DIR': LOG_DIR,
                'LOG_FILE': LOG_FILE,
                'CONFIG_DIR': CONFIG_DIR,
                'DATA_DIR': DATA_DIR,
                'ET_BIN_DIR': ET_BIN_DIR,

                'REQUEST_METHOD': self.command,
                'SCRIPT_NAME': cgi_script,
                'SCRIPT_FILENAME': cgi_script,
                'PATH_INFO': path_info,
                'QUERY_STRING': query_string,
                'REQUEST_URI': request_uri,
                'SERVER_PROTOCOL': self.request_version,
                'SERVER_NAME': self.headers.get('Host', 'localhost').split(':')[0],
                'SERVER_PORT': str(self.server.server_port),
                'CONTENT_TYPE': self.headers.get('Content-Type', ''),
                'CONTENT_LENGTH': str(content_length) if content_length else '',
                'HTTP_HOST': self.headers.get('Host', ''),
                'HTTP_USER_AGENT': self.headers.get('User-Agent', ''),
                'HTTP_ACCEPT': self.headers.get('Accept', ''),
                'HTTP_ACCEPT_ENCODING': self.headers.get('Accept-Encoding', ''),
                'HTTP_ACCEPT_LANGUAGE': self.headers.get('Accept-Language', ''),
                'HTTP_COOKIE': self.headers.get('Cookie', ''),
                'HTTP_REFERER': self.headers.get('Referer', ''),
                'HTTP_X_FORWARDED_FOR': self.headers.get('X-Forwarded-For', ''),
                'HTTP_X_REAL_IP': self.headers.get('X-Real-IP', ''),
            })
            
            # 添加所有以 HTTP_ 开头的自定义头
            for header, value in self.headers.items():
                header_key = f"HTTP_{header.upper().replace('-', '_')}"
                if header_key not in env:
                    env[header_key] = value

            import htt_cgi.cgi as my_cgi
            for item in env.items():
                os.environ[item[0]] = item[1]
                # os.environ.setdefault(item[0], item[1])


            resp = my_cgi.http_handle(base_uri=BASE_URI, body_data=stdin_data, cgi_module=False)
            self.send_response(resp.status_code)
            if resp.file:
                ext = resp.file.split(".")[-1].lower()
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
                self.send_header('Content-type', mime)
                disposition = resp.get_file_disposition()
                if disposition:
                    self.send_header('Content-Disposition', disposition)
            else:
                self.send_header('Content-Type', 'application/json; charset=utf-8')

            self.end_headers()
            # 发送内容
            if resp.file:
                with open(resp.file, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(json.dumps(resp.json, ensure_ascii=False, indent=2).encode())

        except Exception as e:
            logging.error(f"CGI execution error: {e}", exc_info=True)
            self.send_error(500, f"CGI execution error: {str(e)}")
    
    def send_cgi_output(self, output):
        """解析并发送 CGI 输出"""
        try:
            # 查找头部和内容的分隔符
            header_end = output.find(b'\r\n\r\n')
            if header_end == -1:
                header_end = output.find(b'\n\n')
            
            if header_end != -1:
                headers_part = output[:header_end]
                content = output[header_end + 2:]  # 跳过空行
                
                # 解析头部
                headers = headers_part.decode('utf-8', errors='ignore').splitlines()
                status_code = 200
                content_type_sent = False
                
                for line in headers:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 检查状态行
                    if line.lower().startswith('status:'):
                        try:
                            parts = line.split(':', 1)
                            status_part = parts[1].strip()
                            status_code = int(status_part.split()[0])
                        except (ValueError, IndexError):
                            pass
                    # 检查 Content-Type
                    elif line.lower().startswith('content-type'):
                        content_type_sent = True
                        # 先发送状态码，再发送头部
                        self.send_response(status_code)
                        header_name = line.split(':', 1)[0].strip()
                        header_value = line.split(':', 1)[1].strip()
                        # 确保 header 值是 latin-1 编码
                        header_value = header_value.encode('utf-8').decode('latin-1', 'replace')
                        self.send_header(header_name, header_value)
                    elif ':' in line:
                        if not content_type_sent:
                            self.send_response(status_code)
                            content_type_sent = True
                        header_name = line.split(':', 1)[0].strip()
                        header_value = line.split(':', 1)[1].strip()
                        # 确保 header 值是 latin-1 编码
                        header_value = header_value.encode('utf-8').decode('latin-1', 'replace')
                        self.send_header(header_name, header_value)
                
                # 如果没有找到任何头部，发送默认响应
                if not content_type_sent:
                    self.send_response(status_code)
                    self.send_header('Content-Type', 'text/plain; charset=utf-8')
                
                self.end_headers()
                
                # 发送内容
                self.wfile.write(content)
            else:
                # 没有找到头部，直接输出内容
                self.send_response(200)
                self.end_headers()
                self.wfile.write(output)
                
        except Exception as e:
            logging.error(f"Error sending CGI output: {e}", exc_info=True)
            # 如果解析失败，直接输出原始内容
            try:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(output)
            except:
                self.send_error(500, "Failed to process CGI output")
    
    def log_message(self, format, *args):
        """重写日志方法"""
        logging.debug(f"{self.address_string()} - {format % args}")

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """支持多线程的 HTTP 服务器"""
    daemon_threads = True
    allow_reuse_address = True

def start_server(host='127.0.0.1', port=8080):
    """启动 HTTP 服务器"""
    logging.info(f"HTTP服务启动中....")
    server = ThreadedHTTPServer((host, port), CGIProxyHandler)
    logging.info(f"HTTP服务已启动： http://{host}:{port}")
    # 验证 CGI 文件是否存在
    if not os.path.exists(CGI_INDEX):
        logging.warning(f"index.htt_cgi not found: {CGI_INDEX}")
    else:
        logging.info(f"index.htt_cgi found: {CGI_INDEX}")
    
    if not os.path.exists(CGI_API):
        logging.warning(f"api.htt_cgi not found: {CGI_API}")
    else:
        logging.info(f"api.htt_cgi found: {CGI_API}")
    
    logging.info(f"Starting HTTP server on {host}:{port}")
    logging.info(f"Virtual base URI: {BASE_URI}")
    logging.info(f"Requests will be proxied to CGI scripts based on path")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
        server.shutdown()

def run(host='127.0.0.1', port=5666):
    setup_env()
    start_server(host, port)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='CGI Proxy HTTP Server')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5666, help='Port to bind to (default: 5666)')
    args = parser.parse_args()
    # print(f"http://{args.host}:{args.port}/")
    run(args.host, args.port)