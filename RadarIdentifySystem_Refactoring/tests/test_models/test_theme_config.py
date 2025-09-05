import sys
import os
import unittest
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from models.config.theme_config import ThemeMode, AppConfig, get_app_config, initialize_app_config
from qfluentwidgets import Theme


class TestThemeMode(unittest.TestCase):
    """主题模式枚举测试类"""
    
    def test_theme_mode_values(self):
        """测试主题模式值"""
        expected_values = ["Light", "Dark", "Auto"]
        actual_values = ThemeMode.values()
        self.assertEqual(actual_values, expected_values)
        
    def test_to_fluent_theme(self):
        """测试转换为Fluent主题枚举"""
        # 测试各种主题模式的转换
        self.assertEqual(ThemeMode.LIGHT.to_fluent_theme(), Theme.LIGHT)
        self.assertEqual(ThemeMode.DARK.to_fluent_theme(), Theme.DARK)
        self.assertEqual(ThemeMode.AUTO.to_fluent_theme(), Theme.AUTO)
        
    def test_from_fluent_theme(self):
        """测试从Fluent主题枚举转换"""
        # 测试各种Fluent主题的转换
        self.assertEqual(ThemeMode.from_fluent_theme(Theme.LIGHT), ThemeMode.LIGHT)
        self.assertEqual(ThemeMode.from_fluent_theme(Theme.DARK), ThemeMode.DARK)
        self.assertEqual(ThemeMode.from_fluent_theme(Theme.AUTO), ThemeMode.AUTO)
        
    def test_theme_mode_enum_consistency(self):
        """测试主题模式枚举的一致性"""
        # 测试双向转换的一致性
        for theme_mode in ThemeMode:
            fluent_theme = theme_mode.to_fluent_theme()
            converted_back = ThemeMode.from_fluent_theme(fluent_theme)
            self.assertEqual(theme_mode, converted_back)


class TestAppConfig(unittest.TestCase):
    """应用程序配置测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test_config.json")
        
    def tearDown(self):
        """测试后清理"""
        # 清理临时目录
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            
    def test_app_config_creation(self):
        """测试应用程序配置创建"""
        config = AppConfig()
        
        # 验证配置项存在
        self.assertTrue(hasattr(config, 'themeMode'))
        
        # 验证默认值
        self.assertEqual(config.themeMode.value, ThemeMode.AUTO)
        
    def test_theme_mode_config_item(self):
        """测试主题模式配置项"""
        config = AppConfig()
        
        # 测试设置不同的主题模式
        config.themeMode.value = ThemeMode.LIGHT
        self.assertEqual(config.themeMode.value, ThemeMode.LIGHT)
        
        config.themeMode.value = ThemeMode.DARK
        self.assertEqual(config.themeMode.value, ThemeMode.DARK)
        
        config.themeMode.value = ThemeMode.AUTO
        self.assertEqual(config.themeMode.value, ThemeMode.AUTO)
        
    def test_config_validation(self):
        """测试配置验证"""
        config = AppConfig()
        
        # 测试有效值
        for theme_mode in ThemeMode:
            config.themeMode.value = theme_mode
            self.assertEqual(config.themeMode.value, theme_mode)
            
    @patch('models.config.theme_config._app_config', None)
    def test_get_app_config_singleton(self):
        """测试获取应用程序配置单例"""
        # 第一次调用应该创建新实例
        config1 = get_app_config()
        self.assertIsInstance(config1, AppConfig)
        
        # 第二次调用应该返回同一实例
        config2 = get_app_config()
        self.assertIs(config1, config2)
        
    @patch('qfluentwidgets.qconfig.load')
    def test_initialize_app_config(self, mock_load):
        """测试初始化应用程序配置"""
        # 测试默认配置文件路径
        initialize_app_config()
        mock_load.assert_called_once()
        
        # 测试自定义配置文件路径
        mock_load.reset_mock()
        custom_path = "custom/config.json"
        initialize_app_config(custom_path)
        mock_load.assert_called_once_with(custom_path, get_app_config())


if __name__ == '__main__':
    unittest.main()