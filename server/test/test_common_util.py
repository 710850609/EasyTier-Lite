#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
import json

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from server.util.common_util import run_cmd


class TestCommonUtil(unittest.TestCase):
    """测试 common_util 模块"""
    
    def setUp(self):
        """测试前准备"""
        # 设置 easytier-cli 路径
        self.et_bin_dir = os.environ.get('ET_BIN_DIR', '/var/apps/EasyTier-Lite/target/bin')
        self.cli_path = os.path.join(self.et_bin_dir, 'easytier-cli')
        
    # def test_run_cmd_basic(self):
    #     """测试基本命令执行"""
    #     # 测试 echo 命令
    #     result = run_cmd('echo', 'hello world')
    #     self.assertEqual(result, 'hello world')
        
    #     # 测试 shell 模式
    #     result = run_cmd('echo "hello shell"', shell=True)
    #     self.assertEqual(result, 'hello shell')
    
    # def test_run_cmd_with_timeout(self):
    #     """测试命令超时"""
    #     # 测试超时命令（应该会超时）
    #     with self.assertRaises(Exception):
    #         run_cmd('sleep', '10')  # 超过默认超时时间
    
    # def test_run_cmd_error(self):
    #     """测试错误命令"""
    #     # 测试不存在的命令
    #     with self.assertRaises(Exception):
    #         run_cmd('nonexistent_command')
            
    #     # 测试返回非零的命令
    #     with self.assertRaises(Exception):
    #         run_cmd('false')
    
    # def test_easytier_cli_peer_command(self):
    #     """测试 easytier-cli peer 命令"""
    #     # 检查 easytier-cli 是否存在
    #     if not os.path.exists(self.cli_path):
    #         self.skipTest(f"easytier-cli not found at {self.cli_path}")
        
    #     try:
    #         # 测试获取 peer 列表
    #         result = run_cmd(self.cli_path, 'peer')
            
    #         # 检查返回结果
    #         self.assertIsInstance(result, str)
    #         self.assertGreater(len(result), 0)
            
    #         # 如果返回的是 JSON，尝试解析
    #         if result.strip().startswith('{'):
    #             try:
    #                 peer_data = json.loads(result)
    #                 self.assertIsInstance(peer_data, (dict, list))
    #             except json.JSONDecodeError:
    #                 # 不是 JSON 格式也没关系
    #                 pass
                    
    #     except Exception as e:
    #         # 如果 easytier 服务未运行，跳过测试
    #         if "connection refused" in str(e).lower() or "no such file" in str(e).lower():
    #             self.skipTest("easytier service not running")
    #         else:
    #             raise
    
    def test_easytier_cli_peer_json_output(self):
        """测试 easytier-cli peer --output json 命令"""
        if not os.path.exists(self.cli_path):
            self.skipTest(f"easytier-cli not found at {self.cli_path}")
        
        try:
            # 测试 JSON 格式输出
            result = run_cmd(self.cli_path, '--output', 'json', 'peer')
            
            # 检查返回结果
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)
            
            # 尝试解析 JSON
            try:
                peer_data = json.loads(result)
                print(f"{peer_data}")
                self.assertIsInstance(peer_data, (dict, list))
                
                # 如果是列表，检查基本结构
                if isinstance(peer_data, list):
                    for peer in peer_data:
                        self.assertIsInstance(peer, dict)
                        # 检查常见字段
                        if 'id' in peer:
                            self.assertIsInstance(peer['id'], str)
                        if 'name' in peer:
                            self.assertIsInstance(peer['name'], str)
                            
            except json.JSONDecodeError as e:
                self.fail(f"Invalid JSON response: {result}. Error: {e}")
                
        except Exception as e:
            if "connection refused" in str(e).lower() or "no such file" in str(e).lower():
                self.skipTest("easytier service not running")
            else:
                raise
    
    def test_run_cmd_with_environment(self):
        """测试带环境变量的命令执行"""
        # 测试环境变量传递
        result = run_cmd('echo', '$TEST_VAR', env={'TEST_VAR': 'test_value'})
        self.assertEqual(result, 'test_value')
    
    def test_run_cmd_list_command(self):
        """测试列表形式的命令"""
        # 测试列表形式的命令
        result = run_cmd(['echo', 'hello', 'from', 'list'])
        self.assertEqual(result, 'hello from list')
    
    def test_run_cmd_empty_output(self):
        """测试空输出命令"""
        # 测试空输出
        result = run_cmd('true')
        self.assertEqual(result, '')


class TestCommonUtilIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_easytier_cli_integration(self):
        """集成测试：完整的 easytier-cli 工作流"""
        et_bin_dir = os.environ.get('ET_BIN_DIR', '/var/apps/EasyTier-Lite/target/bin')
        cli_path = os.path.join(et_bin_dir, 'easytier-cli')
        
        if not os.path.exists(cli_path):
            self.skipTest(f"easytier-cli not found at {cli_path}")
        
        try:
            # 测试多个命令组合
            commands = [
                ['peer'],
                ['--output', 'json', 'peer'],
                ['version'],
                ['--help']
            ]
            
            for cmd_args in commands:
                try:
                    result = run_cmd(cli_path, *cmd_args)
                    self.assertIsInstance(result, str)
                    # 不检查具体内容，只要不抛出异常即可
                except Exception as e:
                    # 某些命令可能失败是正常的（如服务未启动）
                    if "connection refused" not in str(e).lower():
                        raise
                        
        except Exception as e:
            if "connection refused" in str(e).lower():
                self.skipTest("easytier service not running")
            else:
                raise


def run_tests():
    """运行测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试用例
    suite.addTests(loader.loadTestsFromTestCase(TestCommonUtil))
    # suite.addTests(loader.loadTestsFromTestCase(TestCommonUtilIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # 设置环境变量（如果需要）
    if 'ET_BIN_DIR' not in os.environ:
        # 尝试在常见位置查找 easytier-cli
        possible_paths = [
            '/var/apps/EasyTier-Lite/target/bin',
            '/mnt/f/git-space/fpk-EasyTier-Lite/EasyTier-Lite/app/bin',
            '/usr/bin',
            os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'bin')
        ]
        
        for path in possible_paths:
            cli_path = os.path.join(path, 'easytier-cli')
            if os.path.exists(cli_path):
                os.environ['ET_BIN_DIR'] = path
                break
    
    # 运行测试
    success = run_tests()
    sys.exit(0 if success else 1)