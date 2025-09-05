import sys
import os
import unittest
from unittest.mock import patch, MagicMock, Mock
from PyQt6.QtCore import QObject

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from controllers.theme_controller import ThemeController, get_theme_controller, initialize_theme_controller
from models.config.theme_config import ThemeMode


class TestThemeController(unittest.TestCase):
    """主题控制器测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 重置全局实例
        import controllers.theme_controller
        controllers.theme_controller._theme_controller = None
        
    @patch('controllers.theme_controller.get_theme_service')
    @patch('controllers.theme_controller.get_app_config')
    def test_controller_initialization(self, mock_get_config, mock_get_service):
        """测试控制器初始化"""
        # 模拟服务和配置
        mock_service = MagicMock()
        mock_config = MagicMock()
        mock_get_service.return_value = mock_service
        mock_get_config.return_value = mock_config
        
        # 创建控制器实例
        controller = ThemeController()
        
        # 验证初始化
        self.assertEqual(controller._theme_service, mock_service)
        self.assertEqual(controller._config, mock_config)
        
        # 验证信号连接
        mock_service.themeChanged.connect.assert_called_once()
        
    @patch('controllers.theme_controller.get_theme_service')
    @patch('controllers.theme_controller.get_app_config')
    def test_on_theme_changed(self, mock_get_config, mock_get_service):
        """测试主题变更事件处理"""
        # 模拟服务和配置
        mock_service = MagicMock()
        mock_config = MagicMock()
        mock_get_service.return_value = mock_service
        mock_get_config.return_value = mock_config
        
        controller = ThemeController()
        
        # 连接信号以测试
        signal_received = []
        controller.themeApplied.connect(lambda theme: signal_received.append(theme))
        
        # 触发主题变更
        controller._on_theme_changed(ThemeMode.DARK)
        
        # 验证信号被发射
        self.assertEqual(len(signal_received), 1)
        self.assertEqual(signal_received[0], ThemeMode.DARK)
        
    @patch('controllers.theme_controller.get_theme_service')
    @patch('controllers.theme_controller.get_app_config')
    def test_connect_theme_card(self, mock_get_config, mock_get_service):
        """测试连接主题设置卡"""
        # 模拟服务和配置
        mock_service = MagicMock()
        mock_service.get_theme_mode.return_value = ThemeMode.AUTO
        mock_config = MagicMock()
        mock_get_service.return_value = mock_service
        mock_get_config.return_value = mock_config
        
        controller = ThemeController()
        
        # 模拟主题设置卡
        mock_theme_card = MagicMock()
        
        # 连接主题设置卡
        controller.connect_theme_card(mock_theme_card)
        
        # 验证信号连接
        mock_theme_card.optionChanged.connect.assert_called_once()
        
        # 验证设置卡值被同步
        mock_theme_card.setValue.assert_called_once_with("跟随系统")
        
    @patch('controllers.theme_controller.get_theme_service')
    @patch('controllers.theme_controller.get_app_config')
    def test_on_theme_option_changed(self, mock_get_config, mock_get_service):
        """测试主题选项变更事件处理"""
        # 模拟服务和配置
        mock_service = MagicMock()
        mock_config = MagicMock()
        mock_get_service.return_value = mock_service
        mock_get_config.return_value = mock_config
        
        controller = ThemeController()
        
        # 测试不同选项文本
        test_cases = [
            ("浅色", ThemeMode.LIGHT),
            ("深色", ThemeMode.DARK),
            ("跟随系统", ThemeMode.AUTO)
        ]
        
        for option_text, expected_theme in test_cases:
            with self.subTest(option_text=option_text):
                # 重置mock
                mock_service.reset_mock()
                
                # 触发选项变更
                controller._on_theme_option_changed(option_text)
                
                # 验证主题服务被调用
                mock_service.set_theme_mode.assert_called_once_with(expected_theme)
                
    @patch('controllers.theme_controller.get_theme_service')
    @patch('controllers.theme_controller.get_app_config')
    def test_on_theme_option_changed_invalid(self, mock_get_config, mock_get_service):
        """测试无效主题选项变更事件处理"""
        # 模拟服务和配置
        mock_service = MagicMock()
        mock_config = MagicMock()
        mock_get_service.return_value = mock_service
        mock_get_config.return_value = mock_config
        
        controller = ThemeController()
        
        # 测试无效选项文本
        controller._on_theme_option_changed("无效选项")
        
        # 验证主题服务未被调用
        mock_service.set_theme_mode.assert_not_called()
        
    @patch('controllers.theme_controller.get_theme_service')
    @patch('controllers.theme_controller.get_app_config')
    def test_sync_theme_to_card(self, mock_get_config, mock_get_service):
        """测试同步主题状态到设置卡"""
        # 模拟服务和配置
        mock_service = MagicMock()
        mock_config = MagicMock()
        mock_get_service.return_value = mock_service
        mock_get_config.return_value = mock_config
        
        controller = ThemeController()
        
        # 模拟主题设置卡
        mock_theme_card = MagicMock()
        
        # 测试不同主题模式的同步
        test_cases = [
            (ThemeMode.LIGHT, "浅色"),
            (ThemeMode.DARK, "深色"),
            (ThemeMode.AUTO, "跟随系统")
        ]
        
        for theme_mode, expected_text in test_cases:
            with self.subTest(theme_mode=theme_mode):
                # 设置当前主题模式
                mock_service.get_theme_mode.return_value = theme_mode
                
                # 重置mock
                mock_theme_card.reset_mock()
                
                # 同步主题到设置卡
                controller._sync_theme_to_card(mock_theme_card)
                
                # 验证设置卡值被设置
                mock_theme_card.setValue.assert_called_once_with(expected_text)
                
    @patch('controllers.theme_controller.get_theme_service')
    @patch('controllers.theme_controller.get_app_config')
    def test_apply_theme(self, mock_get_config, mock_get_service):
        """测试应用主题"""
        # 模拟服务和配置
        mock_service = MagicMock()
        mock_config = MagicMock()
        mock_get_service.return_value = mock_service
        mock_get_config.return_value = mock_config
        
        controller = ThemeController()
        
        # 应用主题
        controller.apply_theme(ThemeMode.DARK)
        
        # 验证主题服务被调用
        mock_service.set_theme_mode.assert_called_once_with(ThemeMode.DARK)
        
    @patch('controllers.theme_controller.get_theme_service')
    @patch('controllers.theme_controller.get_app_config')
    @patch('builtins.print')
    def test_apply_theme_exception(self, mock_print, mock_get_config, mock_get_service):
        """测试应用主题异常处理"""
        # 模拟服务和配置
        mock_service = MagicMock()
        mock_service.set_theme_mode.side_effect = Exception("测试异常")
        mock_config = MagicMock()
        mock_get_service.return_value = mock_service
        mock_get_config.return_value = mock_config
        
        controller = ThemeController()
        
        # 应用主题（应该捕获异常）
        controller.apply_theme(ThemeMode.DARK)
        
        # 验证异常被打印
        mock_print.assert_called_once_with("应用主题失败: 测试异常")
        
    @patch('controllers.theme_controller.get_theme_service')
    @patch('controllers.theme_controller.get_app_config')
    def test_get_current_theme(self, mock_get_config, mock_get_service):
        """测试获取当前主题"""
        # 模拟服务和配置
        mock_service = MagicMock()
        mock_service.get_theme_mode.return_value = ThemeMode.LIGHT
        mock_config = MagicMock()
        mock_get_service.return_value = mock_service
        mock_get_config.return_value = mock_config
        
        controller = ThemeController()
        
        # 获取当前主题
        current_theme = controller.get_current_theme()
        
        # 验证结果
        self.assertEqual(current_theme, ThemeMode.LIGHT)
        mock_service.get_theme_mode.assert_called_once()
        
    @patch('controllers.theme_controller.get_theme_service')
    @patch('controllers.theme_controller.get_app_config')
    def test_reset_theme(self, mock_get_config, mock_get_service):
        """测试重置主题"""
        # 模拟服务和配置
        mock_service = MagicMock()
        mock_config = MagicMock()
        mock_get_service.return_value = mock_service
        mock_get_config.return_value = mock_config
        
        controller = ThemeController()
        
        # 重置主题
        controller.reset_theme()
        
        # 验证主题服务被调用
        mock_service.reset_to_default.assert_called_once()
        
    def test_get_theme_controller_singleton(self):
        """测试获取主题控制器单例"""
        # 第一次调用应该创建新实例
        controller1 = get_theme_controller()
        self.assertIsInstance(controller1, ThemeController)
        
        # 第二次调用应该返回同一实例
        controller2 = get_theme_controller()
        self.assertIs(controller1, controller2)
        
    def test_initialize_theme_controller(self):
        """测试初始化主题控制器"""
        controller = initialize_theme_controller()
        self.assertIsInstance(controller, ThemeController)
        
        # 验证返回的是单例实例
        controller2 = get_theme_controller()
        self.assertIs(controller, controller2)


if __name__ == '__main__':
    unittest.main()