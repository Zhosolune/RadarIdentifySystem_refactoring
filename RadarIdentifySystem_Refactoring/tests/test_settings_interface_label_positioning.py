import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QResizeEvent
from views.interfaces.settings_interface import SettingsInterface
from models.ui.dimensions import UIDimensions


class TestSettingsInterfaceLabelPositioning(unittest.TestCase):
    """设置界面标签定位功能的单元测试
    
    测试设置标签的相对定位功能，确保标签位置与滚动区域宽度保持一致。
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """设置测试类"""
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()
    
    def setUp(self) -> None:
        """设置每个测试用例"""
        self.settings_interface = SettingsInterface("test")
        
    def tearDown(self) -> None:
        """清理每个测试用例"""
        if hasattr(self, 'settings_interface'):
            self.settings_interface.close()
            self.settings_interface.deleteLater()
    
    def test_initial_label_position(self) -> None:
        """测试初始标签位置"""
        # 设置一个默认窗口大小
        self.settings_interface.resize(UIDimensions.WINDOW_DEFAULT_WIDTH, UIDimensions.WINDOW_DEFAULT_HEIGHT)
        
        # 获取标签位置
        label_pos = self.settings_interface.settingLabel.pos()
        
        # 验证标签不在固定的(36, 30)位置（原来的绝对定位）
        # 新的相对定位应该根据窗口宽度计算位置
        self.assertIsNotNone(label_pos)
        self.assertEqual(label_pos.y(), 30)  # Y坐标应该保持不变
        
        # X坐标应该大于等于36（最小边距）
        self.assertGreaterEqual(label_pos.x(), 36)
    
    def test_label_position_with_different_window_sizes(self) -> None:
        """测试不同窗口大小下的标签位置"""
        test_cases = [
            (800, 600),   # 小窗口
            (1200, 800),  # 默认窗口
            (1600, 1000), # 大窗口
            (2000, 1200), # 超大窗口
        ]
        
        for width, height in test_cases:
            with self.subTest(window_size=(width, height)):
                # 设置窗口大小
                self.settings_interface.resize(width, height)
                
                # 手动触发标签位置更新
                self.settings_interface._updateLabelPosition()
                
                # 获取标签位置
                label_pos = self.settings_interface.settingLabel.pos()
                
                # 计算期望的标签位置
                scroll_area_width = min(width, UIDimensions.SCROLL_AREA_MAX_WIDTH_SETTING)
                center_offset = (width - scroll_area_width) // 2
                expected_x = max(center_offset + 36, 36)
                
                # 验证标签位置
                self.assertEqual(label_pos.x(), expected_x, 
                               f"窗口大小 {width}x{height} 时标签X位置不正确")
                self.assertEqual(label_pos.y(), 30, 
                               f"窗口大小 {width}x{height} 时标签Y位置不正确")
    
    def test_resize_event_updates_label_position(self) -> None:
        """测试窗口大小变化事件是否正确更新标签位置"""
        # 初始窗口大小
        initial_width, initial_height = 1000, 700
        self.settings_interface.resize(initial_width, initial_height)
        
        # 获取初始标签位置
        initial_pos = self.settings_interface.settingLabel.pos()
        
        # 改变窗口大小
        new_width, new_height = 1500, 900
        self.settings_interface.resize(new_width, new_height)
        
        # 手动触发resize事件
        resize_event = QResizeEvent(QSize(new_width, new_height), QSize(initial_width, initial_height))
        self.settings_interface.resizeEvent(resize_event)
        
        # 获取新的标签位置
        new_pos = self.settings_interface.settingLabel.pos()
        
        # 验证标签位置已更新
        self.assertNotEqual(initial_pos.x(), new_pos.x(), "标签X位置应该随窗口大小变化而更新")
        self.assertEqual(initial_pos.y(), new_pos.y(), "标签Y位置应该保持不变")
    
    def test_minimum_label_position(self) -> None:
        """测试标签位置的最小值限制"""
        # 设置一个很小的窗口
        small_width = 200
        self.settings_interface.resize(small_width, 400)
        self.settings_interface._updateLabelPosition()
        
        # 获取标签位置
        label_pos = self.settings_interface.settingLabel.pos()
        
        # 验证标签X位置不小于最小边距36px
        self.assertGreaterEqual(label_pos.x(), 36, "标签X位置不应小于最小边距36px")
    
    def test_label_position_with_max_scroll_width(self) -> None:
        """测试当窗口宽度超过滚动区域最大宽度时的标签位置"""
        # 设置一个超大窗口，超过滚动区域最大宽度
        large_width = UIDimensions.SCROLL_AREA_MAX_WIDTH_SETTING + 500
        self.settings_interface.resize(large_width, 800)
        self.settings_interface._updateLabelPosition()
        
        # 获取标签位置
        label_pos = self.settings_interface.settingLabel.pos()
        
        # 计算期望位置
        center_offset = (large_width - UIDimensions.SCROLL_AREA_MAX_WIDTH_SETTING) // 2
        expected_x = center_offset + 36
        
        # 验证标签位置
        self.assertEqual(label_pos.x(), expected_x, 
                        "当窗口宽度超过滚动区域最大宽度时，标签位置计算不正确")
    
    @patch('views.interfaces.settings_interface.SettingsInterface.logger')
    def test_debug_logging(self, mock_logger: MagicMock) -> None:
        """测试调试日志输出"""
        # 触发标签位置更新
        self.settings_interface.resize(1200, 800)
        self.settings_interface._updateLabelPosition()
        
        # 验证日志方法被调用
        mock_logger.debug.assert_called()
        
        # 验证日志内容包含位置信息
        call_args = mock_logger.debug.call_args[0][0]
        self.assertIn("更新设置标签位置", call_args)
        self.assertIn("窗口宽度", call_args)
        self.assertIn("滚动区域宽度", call_args)


if __name__ == '__main__':
    unittest.main()