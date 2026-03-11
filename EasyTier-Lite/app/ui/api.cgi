#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json

def run_cmd(command, *args, shell=False):
    """
    执行命令并返回 JSON 格式结果
    
    Args:
        command: 命令（字符串或列表）
        *args: 命令参数（当 command 为字符串时）
        shell: 是否使用 shell 执行
    
    Returns:
        JSON 字符串: {"code": 状态码, "stdout": 标准输出, "stderr": 错误输出, "success": 是否成功}
    """
    try:
        # 构建命令列表
        if shell:
            # shell 模式：合并为字符串
            if args:
                full_command = f"{command} {' '.join(args)}"
            else:
                full_command = command
            cmd = full_command
        else:
            # 非 shell 模式：使用列表
            if args:
                cmd = [command] + list(args)
            else:
                cmd = command if isinstance(command, list) else command.split()
        
        # 执行命令
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )
        if result.returncode == 0:
            output = {
                "code": 0,
                "data": result.stdout.strip() if result.stdout else ""
            }
        else:
            output = {
                "code": result.returncode,
                "data": result.stderr.strip() if result.stderr else ""
            }
        
    except subprocess.TimeoutExpired:
        output = {
            "code": -1,
            "data": "Command execution timeout"
        }
    except Exception as e:
        output = {
            "code": -1,
            "data": str(e)
        }
    return output

def http_response(status_code, data):
    """发送HTTP响应"""
    print(f"Status: {status_code}")
    print("Content-Type: application/json; charset=utf-8")
    print("")
    print(json.dumps(data, ensure_ascii=False))
    sys.exit(0)

def get_peer():
    result = run_cmd('/var/apps/EasyTier-Lite/target/bin/easytier-cli --output json peer')
    if result['code'] == 0:
        result['data'] = json.loads(result['data'])
    http_response(200, result)

if __name__ == '__main__':
    get_peer()
    
