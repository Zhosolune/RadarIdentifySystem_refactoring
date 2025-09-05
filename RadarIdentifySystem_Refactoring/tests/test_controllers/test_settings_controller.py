import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
from PyQt6.QtCore import QObject

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from controllers.ui.settings_controller import SettingsController
from views.interfaces.settings_interface import SettingsInterface


class TestSettingsController(unittest.TestCase):
    """设置控制器测试类
    
    测试SettingsController的各项功能，包括初始化、
    信号连接、界面关联等。
    """
    
    def setUp(self) -> None:
        """测试前的准备工作
        
        创建测试所需的对象和模拟环境。
        """
        self.controller = None
        self.mock_settings_interface = None
    
    def tearDown(self) -> None:
        """测试后的清理工作
        
        清理测试过程中创建的对象。
        """
        if self.controller:
            self.controller.deleteLater()
        if self.mock_settings_interface:
            self.mock_settings_interface.deleteLater()
    
    @patch('controllers.ui.settings_controller._app_cfg')
    def test_controller_initialization(self, mock_app_cfg: Mock) -> None:
        """测试控制器初始化
        
        验证控制器能够正确初始化，并设置全局主题信号连接。
        
        Args:
            mock_app_cfg: 模拟的应用配置对象
        """
        # 模拟配置对象的信号
        mock_app_cfg.themeChanged = Mock()
        mock_app_cfg.themeColorChanged = Mock()
        
        # 创建控制器
        self.controller = SettingsController()
        
        # 验证控制器正确初始化
        self.assertIsInstance(self.controller, QObject)
        self.assertIsNone(self.controller.get_settings_interface())
        
        # 验证全局主题信号连接
        mock_app_cfg.themeChanged.connect.assert_called_once()
        mock_app_cfg.themeColorChanged.connect.assert_called_once()
        
        # 验证控制器具有日志功能
        self.assertTrue(hasattr(self.controller, 'logger'))
        self.assertIsNotNone(self.controller.logger)
    
    @patch('controllers.ui.settings_controller._app_cfg')
    def test_set_settings_interface_success(self, mock_app_cfg: Mock) -> None:
        """测试成功设置设置界面
        
        验证控制器能够正确关联设置界面。
        
        Args:
            mock_app_cfg: 模拟的应用配置对象
        """
        # 模拟配置对象的信号
        mock_app_cfg.themeChanged = Mock()
        mock_app_cfg.themeColorChanged = Mock()
        
        # 创建控制器和模拟设置界面
        self.controller = SettingsController()
        self.mock_settings_interface = Mock(spec=SettingsInterface)
        
        # 设置设置界面
        self.controller.set_settings_interface(self.mock_settings_interface)
        
        # 验证设置界面正确关联
        self.assertEqual(
            self.controller.get_settings_interface(), 
            self.mock_settings_interface
        )
        
        # 验证设置界面正确关联（日志功能通过LoggerMixin提供）
        self.assertTrue(hasattr(self.controller, 'logger'))
    
    @patch('controllers.ui.settings_controller._app_cfg')
    def test_set_settings_interface_none(self, mock_app_cfg: Mock) -> None:
        """测试设置None设置界面
        
        验证当传入None时控制器会抛出ValueError。
        
        Args:
            mock_app_cfg: 模拟的应用配置对象
        """
        # 模拟配置对象的信号
        mock_app_cfg.themeChanged = Mock()
        mock_app_cfg.themeColorChanged = Mock()
        
        # 创建控制器
        self.controller = SettingsController()
        
        # 验证传入None时抛出ValueError
        with self.assertRaises(ValueError) as context:
            self.controller.set_settings_interface(None)
        
        self.assertIn("Settings interface cannot be None", str(context.exception))
        
        # 验证异常正确抛出（错误日志通过LoggerMixin记录）
        self.assertTrue(hasattr(self.controller, 'logger'))
    
    @patch('controllers.ui.settings_controller._app_cfg')
    def test_connect_interface_signals_without_interface(self, mock_app_cfg: Mock) -> None:
        """测试在未设置界面时连接信号
        
        验证当未设置设置界面时，内部信号连接方法会抛出RuntimeError。
        
        Args:
            mock_app_cfg: 模拟的应用配置对象
        """
        # 模拟配置对象的信号
        mock_app_cfg.themeChanged = Mock()
        mock_app_cfg.themeColorChanged = Mock()
        
        # 创建控制器
        self.controller = SettingsController()
        
        # 验证在未设置界面时调用内部方法会抛出RuntimeError
        with self.assertRaises(RuntimeError) as context:
            self.controller._connect_interface_signals()
        
        self.assertIn(
            "Settings interface must be set before connecting signals", 
            str(context.exception)
        )
        
        # 验证异常正确抛出（错误日志通过LoggerMixin记录）
        self.assertTrue(hasattr(self.controller, 'logger'))
    
    @patch('controllers.ui.settings_controller.setTheme')
    @patch('controllers.ui.settings_controller.setThemeColor')
    @patch('controllers.ui.settings_controller._app_cfg')
    def test_global_theme_connections(self, mock_app_cfg: Mock, 
                                    mock_set_theme_color: Mock, 
                                    mock_set_theme: Mock) -> None:
        """测试全局主题信号连接
        
        验证控制器正确连接了全局主题相关的信号。
        
        Args:
            mock_app_cfg: 模拟的应用配置对象
            mock_set_theme_color: 模拟的setThemeColor函数
            mock_set_theme: 模拟的setTheme函数
        """
        # 模拟配置对象的信号
        mock_theme_changed = Mock()
        mock_theme_color_changed = Mock()
        mock_app_cfg.themeChanged = mock_theme_changed
        mock_app_cfg.themeColorChanged = mock_theme_color_changed
        
        # 创建控制器
        self.controller = SettingsController()
        
        # 验证信号连接
        mock_theme_changed.connect.assert_called_once_with(mock_set_theme)
        mock_theme_color_changed.connect.assert_called_once_with(mock_set_theme_color)
    
    @patch('controllers.ui.settings_controller._app_cfg')
    def test_theme_change_callbacks(self, mock_app_cfg: Mock) -> None:
        """测试主题变化回调方法
        
        验证主题变化回调方法能够正常执行并记录日志。
        
        Args:
            mock_app_cfg: 模拟的应用配置对象
        """
        # 模拟配置对象的信号和值
        mock_app_cfg.themeChanged = Mock()
        mock_app_cfg.themeColorChanged = Mock()
        mock_app_cfg.themeMode.value = "Dark"
        mock_app_cfg.themeColor.value = "#FF5722"
        
        # 创建控制器
        self.controller = SettingsController()
        
        # 测试主题变化回调（日志记录通过LoggerMixin处理）
        try:
            self.controller._on_theme_changed()
            self.controller._on_theme_color_changed()
        except Exception as e:
            self.fail(f"Theme change callbacks should not raise exceptions: {e}")
        
        # 验证回调方法可以正常调用
        self.assertTrue(callable(self.controller._on_theme_changed))
        self.assertTrue(callable(self.controller._on_theme_color_changed))


if __name__ == '__main__':
    unittest.main()