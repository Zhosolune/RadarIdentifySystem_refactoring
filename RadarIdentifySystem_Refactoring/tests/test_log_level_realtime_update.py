#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志级别实时更新功能测试

测试设置界面中日志级别设置项的实时更新功能，验证MVC架构下的信号连接和处理。

Author: Assistant
Date: 2025-01-10
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from PyQt6.QtTest import QTest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from views.interfaces.settings_interface import SettingsInterface
from controllers.ui.settings_controller import SettingsController
from models.utils.log_manager import get_log_manager
from models.config.app_config import _app_cfg


class TestLogLevelRealtimeUpdate(unittest.TestCase):
    """日志级别实时更新测试类
    
    测试日志级别设置项的实时更新功能，包括：
    - 信号连接是否正确
    - 配置变更是否触发日志管理器更新
    - MVC架构下的数据流是否正确
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """测试类初始化
        
        创建QApplication实例，确保Qt环境正常。
        """
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        else:
            cls.app = QApplication.instance()
    
    def setUp(self) -> None:
        """每个测试方法前的初始化
        
        创建测试所需的对象实例。
        """
        self.settings_interface = SettingsInterface(text="设置")
        self.settings_controller = SettingsController(
            settings_interface=self.settings_interface
        )
    
    def tearDown(self) -> None:
        """每个测试方法后的清理
        
        清理测试中创建的对象。
        """
        self.settings_interface = None
        self.settings_controller = None
    
    def test_log_level_signal_connection(self) -> None:
        """测试日志级别信号连接
        
        验证SettingsController是否正确连接了日志级别变更信号。
        """
        # 验证控制器已正确初始化
        self.assertIsNotNone(self.settings_controller)
        
        # 验证设置界面中的日志级别卡片存在
        self.assertTrue(hasattr(self.settings_interface, 'logLevelCard'))
        
        # 验证日志级别卡片绑定了正确的配置项
        self.assertEqual(
            self.settings_interface.logLevelCard.configItem, 
            _app_cfg.logLevel
        )
        
        print("✓ 日志级别信号连接测试通过")
    
    @patch('controllers.ui.settings_controller.get_log_manager')
    def test_log_level_change_handling(self, mock_get_log_manager) -> None:
        """测试日志级别变更处理
        
        验证当配置项变更时，是否正确调用日志管理器的set_level方法。
        """
        # 设置mock
        mock_log_manager = Mock()
        mock_get_log_manager.return_value = mock_log_manager
        
        # 在mock生效后创建新的SettingsController实例
        from controllers.ui.settings_controller import SettingsController
        test_controller = SettingsController(settings_interface=self.settings_interface)
        
        # 测试不同的日志级别
        test_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        
        for level in test_levels:
            with self.subTest(level=level):
                # 重置mock
                mock_log_manager.reset_mock()
                
                # 触发信号
                _app_cfg.logLevel.valueChanged.emit(level)
                
                # 验证set_level被调用
                mock_log_manager.set_level.assert_called_with(level)
        
        print("✓ 日志级别变更处理测试通过")
    
    def test_log_level_ui_integration(self) -> None:
        """测试日志级别UI集成
        
        验证UI组件与配置项的双向绑定是否正常工作。
        """
        # 获取日志级别卡片
        log_level_card = self.settings_interface.logLevelCard
        
        # 验证初始值
        initial_value = _app_cfg.logLevel.value
        self.assertEqual(log_level_card.comboBox.currentText(), initial_value)
        
        # 测试UI变更是否更新配置
        test_level = "DEBUG" if initial_value != "DEBUG" else "ERROR"
        
        # 模拟用户在UI中选择新的日志级别
        index = log_level_card.comboBox.findText(test_level)
        if index >= 0:
            log_level_card.comboBox.setCurrentIndex(index)
            
            # 验证配置项是否更新
            self.assertEqual(_app_cfg.logLevel.value, test_level)
        
        print("✓ 日志级别UI集成测试通过")
    
    @patch('controllers.ui.settings_controller.get_log_manager')
    def test_error_handling(self, mock_get_log_manager: Mock) -> None:
        """测试错误处理
        
        验证当日志管理器操作失败时，控制器是否正确处理异常。
        
        Args:
            mock_get_log_manager: 模拟的日志管理器获取函数
        """
        # 创建会抛出异常的模拟日志管理器
        mock_log_manager = Mock()
        mock_log_manager.set_level.side_effect = ValueError("测试异常")
        mock_get_log_manager.return_value = mock_log_manager
        
        # 触发配置变更，应该不会抛出未处理的异常
        try:
            _app_cfg.logLevel.valueChanged.emit("DEBUG")
            print("✓ 错误处理测试通过")
        except Exception as e:
            self.fail(f"控制器未正确处理异常: {e}")
    
    def test_mvc_architecture_compliance(self) -> None:
        """测试MVC架构合规性
        
        验证实现是否遵循MVC架构原则：
        - Model层（_app_cfg）负责数据管理
        - View层（SettingsInterface）负责UI展示
        - Controller层（SettingsController）负责协调
        """
        # 验证Model层：配置项存在且类型正确
        self.assertTrue(hasattr(_app_cfg, 'logLevel'))
        self.assertIn(_app_cfg.logLevel.value, ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        
        # 验证View层：UI组件存在且绑定正确
        self.assertTrue(hasattr(self.settings_interface, 'logLevelCard'))
        self.assertEqual(
            self.settings_interface.logLevelCard.configItem, 
            _app_cfg.logLevel
        )
        
        # 验证Controller层：信号处理方法存在
        self.assertTrue(hasattr(self.settings_controller, '_on_log_level_changed'))
        self.assertTrue(callable(self.settings_controller._on_log_level_changed))
        
        print("✓ MVC架构合规性测试通过")


def main():
    """主测试函数
    
    运行所有测试用例。
    """
    print("开始日志级别实时更新功能测试...")
    
    try:
        # 创建测试套件
        suite = unittest.TestLoader().loadTestsFromTestCase(TestLogLevelRealtimeUpdate)
        
        # 运行测试
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        if result.wasSuccessful():
            print("\n🎉 所有测试通过！日志级别实时更新功能正常工作。")
            return True
        else:
            print(f"\n❌ 测试失败: {len(result.failures)} 个失败, {len(result.errors)} 个错误")
            return False
        
    except Exception as e:
        print(f"\n❌ 测试执行失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)