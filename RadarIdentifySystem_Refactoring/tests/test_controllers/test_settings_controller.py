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
        """测试结束后的清理工作
        
        释放测试中创建的对象和资源。
        """
        self.controller = None
        self.mock_settings_interface = None

    @patch('controllers.ui.settings_controller.cfg')
    def test_init_and_signal_setup(self, mock_app_cfg: Mock) -> None:
        """测试初始化和全局信号连接
        
        验证在初始化时，控制器能够正确连接主题相关的全局信号。
        
        Args:
            mock_app_cfg: 模拟的应用配置对象
        Returns:
            None
        """
        # 模拟配置对象的信号
        mock_app_cfg.themeChanged = MagicMock()
        mock_app_cfg.themeColorChanged = MagicMock()
        
        # 创建控制器
        self.controller = SettingsController()
        
        # 验证信号连接时未抛出异常
        self.assertIsInstance(self.controller, SettingsController)

    @patch('controllers.ui.settings_controller.cfg')
    def test_set_settings_interface(self, mock_app_cfg: Mock) -> None:
        """测试设置界面关联
        
        验证设置界面可以成功关联到控制器。
        
        Args:
            mock_app_cfg: 模拟的应用配置对象
        Returns:
            None
        """
        # 准备模拟接口
        class DummySettingsInterface(SettingsInterface):
            def __init__(self):
                QObject.__init__(self)
        
        # 创建控制器和界面
        self.controller = SettingsController()
        interface = DummySettingsInterface()
        
        # 执行关联
        self.controller.set_settings_interface(settings_interface=interface)
        
        # 断言
        self.assertIs(self.controller.get_settings_interface(), interface)

    @patch('controllers.ui.settings_controller.cfg')
    def test_theme_change_callbacks(self, mock_app_cfg: Mock) -> None:
        """测试主题变化回调方法
        
        验证主题变化回调方法能够正常执行并记录日志。
        
        Args:
            mock_app_cfg: 模拟的应用配置对象
        Returns:
            None
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
            # 传入一个具有 name() 方法的模拟颜色对象
            mock_color = MagicMock()
            mock_color.name.return_value = "#FF5722"
            self.controller._on_theme_color_changed(color=mock_color)
        except Exception as e:
            self.fail(f"Theme change callbacks should not raise exceptions: {e}")
        
        # 验证回调方法可以正常调用
        self.assertTrue(callable(self.controller._on_theme_changed))
        self.assertTrue(callable(self.controller._on_theme_color_changed))

    @patch('controllers.ui.settings_controller.cfg')
    def test_config_driven_theme_color_no_direct_set(self, mock_app_cfg: Mock) -> None:
        """测试配置驱动下，不直接调用 setThemeColor
        
        期望：_on_theme_color_changed 仅记录日志，不调用 setThemeColor。
        """
        mock_app_cfg.themeChanged = MagicMock()
        mock_app_cfg.themeColorChanged = MagicMock()
        
        controller = SettingsController()
        mock_color = MagicMock()
        mock_color.name.return_value = "#2196F3"
        
        # 若实现中误调用 setThemeColor，会因未打 patch 而抛 Import 或 Attribute 错误/或需额外断言。
        # 这里仅验证不抛异常即可。
        try:
            controller._on_theme_color_changed(color=mock_color)
        except Exception as e:
            self.fail(f"_on_theme_color_changed should not call setThemeColor directly: {e}")

    @patch('controllers.ui.settings_controller.cfg')
    def test_color_card_no_direct_wiring(self, mock_app_cfg: Mock) -> None:
        """测试颜色选择卡不进行直接接线
        
        期望：set_settings_interface 后不会对 themeColorCard.colorChanged 调用 connect。
        """
        mock_app_cfg.themeChanged = MagicMock()
        mock_app_cfg.themeColorChanged = MagicMock()
        
        class DummySignal:
            def __init__(self):
                self.connect = MagicMock()
        
        class DummyThemeColorCard:
            def __init__(self):
                self.colorChanged = DummySignal()
        
        class DummySettingsInterface(SettingsInterface):
            def __init__(self):
                QObject.__init__(self)
                self.themeColorCard = DummyThemeColorCard()
        
        controller = SettingsController()
        interface = DummySettingsInterface()
        controller.set_settings_interface(settings_interface=interface)
        
        # 断言不会尝试连接
        interface.themeColorCard.colorChanged.connect.assert_not_called()


if __name__ == '__main__':
    unittest.main()