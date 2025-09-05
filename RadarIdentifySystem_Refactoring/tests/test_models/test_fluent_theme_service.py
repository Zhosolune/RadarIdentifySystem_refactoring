import sys
import os
import unittest
from unittest.mock import patch, MagicMock, call
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QColor

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from models.theme.fluent_theme_service import FluentThemeService, get_theme_service, initialize_theme_service
from models.config.theme_config import ThemeMode


class TestFluentThemeService(unittest.TestCase):
    """Fluent主题服务测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 重置全局实例
        import models.theme.fluent_theme_service
        models.theme.fluent_theme_service._theme_service = None
        
    @patch('models.theme.fluent_theme_service.get_app_config')
    @patch('models.theme.fluent_theme_service.setTheme')
    @patch('models.theme.fluent_theme_service.setThemeColor')
    def test_service_initialization(self, mock_set_theme_color, mock_set_theme, mock_get_config):
        """测试服务初始化"""
        # 模拟配置
        mock_config = MagicMock()
        mock_config.themeMode.value = ThemeMode.AUTO
        mock_get_config.return_value = mock_config
        
        # 创建服务实例
        service = FluentThemeService()
        
        # 验证初始化
        self.assertEqual(service._primary_color, FluentThemeService.PRIMARY_COLOR)
        self.assertEqual(service._current_theme_mode, ThemeMode.AUTO)
        
        # 验证主题应用被调用
        mock_set_theme_color.assert_called_once()
        mock_set_theme.assert_called_once()
        
    @patch('models.theme.fluent_theme_service.get_app_config')
    @patch('models.theme.fluent_theme_service.setTheme')
    @patch('models.theme.fluent_theme_service.setThemeColor')
    def test_set_primary_color(self, mock_set_theme_color, mock_set_theme, mock_get_config):
        """测试设置主题色"""
        # 模拟配置
        mock_config = MagicMock()
        mock_config.themeMode.value = ThemeMode.AUTO
        mock_get_config.return_value = mock_config
        
        service = FluentThemeService()
        
        # 测试设置新的主题色
        new_color = "#ff0000"
        service.set_primary_color(new_color)
        
        # 验证颜色被设置
        self.assertEqual(service._primary_color, new_color)
        
        # 验证setThemeColor被调用
        self.assertTrue(mock_set_theme_color.called)
        
    @patch('models.theme.fluent_theme_service.get_app_config')
    @patch('models.theme.fluent_theme_service.setTheme')
    @patch('models.theme.fluent_theme_service.setThemeColor')
    def test_get_primary_color(self, mock_set_theme_color, mock_set_theme, mock_get_config):
        """测试获取主题色"""
        # 模拟配置
        mock_config = MagicMock()
        mock_config.themeMode.value = ThemeMode.AUTO
        mock_get_config.return_value = mock_config
        
        service = FluentThemeService()
        
        # 验证默认主题色
        self.assertEqual(service.get_primary_color(), FluentThemeService.PRIMARY_COLOR)
        
        # 设置新颜色并验证
        new_color = "#00ff00"
        service.set_primary_color(new_color)
        self.assertEqual(service.get_primary_color(), new_color)
        
    @patch('models.theme.fluent_theme_service.get_app_config')
    @patch('models.theme.fluent_theme_service.setTheme')
    @patch('models.theme.fluent_theme_service.setThemeColor')
    def test_set_theme_mode(self, mock_set_theme_color, mock_set_theme, mock_get_config):
        """测试设置主题模式"""
        # 模拟配置
        mock_config = MagicMock()
        mock_config.themeMode.value = ThemeMode.AUTO
        mock_get_config.return_value = mock_config
        
        service = FluentThemeService()
        
        # 测试设置不同主题模式
        service.set_theme_mode(ThemeMode.DARK)
        
        # 验证主题模式被设置
        self.assertEqual(service._current_theme_mode, ThemeMode.DARK)
        
        # 验证配置被更新
        self.assertEqual(mock_config.themeMode.value, ThemeMode.DARK)
        
        # 验证setTheme被调用
        self.assertTrue(mock_set_theme.called)
        
    @patch('models.theme.fluent_theme_service.get_app_config')
    @patch('models.theme.fluent_theme_service.setTheme')
    @patch('models.theme.fluent_theme_service.setThemeColor')
    def test_get_theme_mode(self, mock_set_theme_color, mock_set_theme, mock_get_config):
        """测试获取主题模式"""
        # 模拟配置
        mock_config = MagicMock()
        mock_config.themeMode.value = ThemeMode.LIGHT
        mock_get_config.return_value = mock_config
        
        service = FluentThemeService()
        
        # 验证获取主题模式
        self.assertEqual(service.get_theme_mode(), ThemeMode.LIGHT)
        
    @patch('models.theme.fluent_theme_service.get_app_config')
    @patch('models.theme.fluent_theme_service.setTheme')
    @patch('models.theme.fluent_theme_service.setThemeColor')
    def test_convenience_methods(self, mock_set_theme_color, mock_set_theme, mock_get_config):
        """测试便捷方法"""
        # 模拟配置
        mock_config = MagicMock()
        mock_config.themeMode.value = ThemeMode.AUTO
        mock_get_config.return_value = mock_config
        
        service = FluentThemeService()
        
        # 测试设置浅色主题
        service.set_light_theme()
        self.assertEqual(service._current_theme_mode, ThemeMode.LIGHT)
        
        # 测试设置深色主题
        service.set_dark_theme()
        self.assertEqual(service._current_theme_mode, ThemeMode.DARK)
        
        # 测试设置自动主题
        service.set_auto_theme()
        self.assertEqual(service._current_theme_mode, ThemeMode.AUTO)
        
    @patch('models.theme.fluent_theme_service.get_app_config')
    @patch('models.theme.fluent_theme_service.setTheme')
    @patch('models.theme.fluent_theme_service.setThemeColor')
    def test_reset_to_default(self, mock_set_theme_color, mock_set_theme, mock_get_config):
        """测试重置为默认设置"""
        # 模拟配置
        mock_config = MagicMock()
        mock_config.themeMode.value = ThemeMode.DARK
        mock_get_config.return_value = mock_config
        
        service = FluentThemeService()
        
        # 修改设置
        service.set_primary_color("#ff0000")
        service.set_theme_mode(ThemeMode.LIGHT)
        
        # 重置为默认
        service.reset_to_default()
        
        # 验证重置结果
        self.assertEqual(service._primary_color, FluentThemeService.PRIMARY_COLOR)
        self.assertEqual(service._current_theme_mode, ThemeMode.AUTO)
        
    @patch('models.theme.fluent_theme_service.get_app_config')
    @patch('models.theme.fluent_theme_service.setTheme')
    @patch('models.theme.fluent_theme_service.setThemeColor')
    def test_theme_changed_signal(self, mock_set_theme_color, mock_set_theme, mock_get_config):
        """测试主题变更信号"""
        # 模拟配置
        mock_config = MagicMock()
        mock_config.themeMode.value = ThemeMode.AUTO
        mock_get_config.return_value = mock_config
        
        service = FluentThemeService()
        
        # 连接信号
        signal_received = []
        service.themeChanged.connect(lambda theme: signal_received.append(theme))
        
        # 设置主题模式
        service.set_theme_mode(ThemeMode.DARK)
        
        # 验证信号被发射
        self.assertEqual(len(signal_received), 1)
        self.assertEqual(signal_received[0], ThemeMode.DARK)
        
    def test_get_theme_service_singleton(self):
        """测试获取主题服务单例"""
        # 第一次调用应该创建新实例
        service1 = get_theme_service()
        self.assertIsInstance(service1, FluentThemeService)
        
        # 第二次调用应该返回同一实例
        service2 = get_theme_service()
        self.assertIs(service1, service2)
        
    def test_initialize_theme_service(self):
        """测试初始化主题服务"""
        service = initialize_theme_service()
        self.assertIsInstance(service, FluentThemeService)
        
        # 验证返回的是单例实例
        service2 = get_theme_service()
        self.assertIs(service, service2)


if __name__ == '__main__':
    unittest.main()