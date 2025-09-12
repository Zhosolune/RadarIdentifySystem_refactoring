import sys
import os
import unittest

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.ui.dimensions import UIDimensions


class TestUIDimensions(unittest.TestCase):
    """UIDimensions类的单元测试
    
    测试全局尺寸设定类的各种功能和边界条件。
    """
    
    def test_constants_exist(self) -> None:
        """测试所有常量是否存在且为正整数"""
        constants = [
            'PADDING_SMALL', 'PADDING_MEDIUM', 'PADDING_LARGE',
            'SPACING_SMALL', 'SPACING_MEDIUM', 'SPACING_LARGE', 'SPACING_EXTRA_LARGE',
            'BORDER_WIDTH_THIN', 'BORDER_WIDTH_MEDIUM', 'BORDER_WIDTH_THICK',
            'SCROLL_AREA_MIN_WIDTH', 'SCROLL_AREA_MAX_WIDTH', 'SCROLL_AREA_MIN_HEIGHT',
            'PANEL_MIN_WIDTH', 'PANEL_MIN_HEIGHT', 'PANEL_HEADER_HEIGHT',
            'BUTTON_MIN_WIDTH', 'BUTTON_MIN_HEIGHT', 'BUTTON_ICON_SIZE',
            'INPUT_MIN_WIDTH', 'INPUT_HEIGHT',
            'WINDOW_MIN_WIDTH', 'WINDOW_MIN_HEIGHT', 'WINDOW_DEFAULT_WIDTH', 'WINDOW_DEFAULT_HEIGHT',
            'SPLITTER_WIDTH', 'TOOLBAR_HEIGHT', 'TOOLBAR_ICON_SIZE', 'STATUSBAR_HEIGHT'
        ]
        
        for constant in constants:
            with self.subTest(constant=constant):
                self.assertTrue(hasattr(UIDimensions, constant), f"常量 {constant} 不存在")
                value = getattr(UIDimensions, constant)
                self.assertIsInstance(value, int, f"常量 {constant} 不是整数")
                self.assertGreater(value, 0, f"常量 {constant} 不是正数")
    
    def test_get_right_panel_width_normal(self) -> None:
        """测试正常情况下的右侧面板宽度计算"""
        # 测试正常宽度
        width = UIDimensions.get_right_panel_width(total_width=1200, padding=40)
        expected = (1200 - 40) // 3  # 386
        self.assertEqual(width, expected)
        
        # 测试超过最大宽度的情况
        width = UIDimensions.get_right_panel_width(total_width=4000, padding=40)
        self.assertEqual(width, UIDimensions.SCROLL_AREA_MAX_WIDTH)
    
    def test_get_right_panel_width_edge_cases(self) -> None:
        """测试边界情况"""
        # 测试最小有效宽度
        width = UIDimensions.get_right_panel_width(total_width=41, padding=40)
        self.assertEqual(width, 0)  # (41-40)//3 = 0
        
        # 测试无效输入
        with self.assertRaises(ValueError):
            UIDimensions.get_right_panel_width(total_width=40, padding=40)
        
        with self.assertRaises(ValueError):
            UIDimensions.get_right_panel_width(total_width=30, padding=40)
    
    def test_get_responsive_padding(self) -> None:
        """测试响应式内边距"""
        # 小屏幕
        padding = UIDimensions.get_responsive_padding(container_width=500)
        self.assertEqual(padding, UIDimensions.PADDING_SMALL)
        
        # 中等屏幕
        padding = UIDimensions.get_responsive_padding(container_width=800)
        self.assertEqual(padding, UIDimensions.PADDING_MEDIUM)
        
        # 大屏幕
        padding = UIDimensions.get_responsive_padding(container_width=1200)
        self.assertEqual(padding, UIDimensions.PADDING_LARGE)
        
        # 边界值测试
        padding = UIDimensions.get_responsive_padding(container_width=600)
        self.assertEqual(padding, UIDimensions.PADDING_MEDIUM)
        
        padding = UIDimensions.get_responsive_padding(container_width=1000)
        self.assertEqual(padding, UIDimensions.PADDING_LARGE)
    
    def test_get_responsive_spacing(self) -> None:
        """测试响应式间距"""
        # 小屏幕
        spacing = UIDimensions.get_responsive_spacing(container_width=500)
        self.assertEqual(spacing, UIDimensions.SPACING_SMALL)
        
        # 中等屏幕
        spacing = UIDimensions.get_responsive_spacing(container_width=800)
        self.assertEqual(spacing, UIDimensions.SPACING_MEDIUM)
        
        # 大屏幕
        spacing = UIDimensions.get_responsive_spacing(container_width=1200)
        self.assertEqual(spacing, UIDimensions.SPACING_LARGE)
        
        # 边界值测试
        spacing = UIDimensions.get_responsive_spacing(container_width=600)
        self.assertEqual(spacing, UIDimensions.SPACING_MEDIUM)
        
        spacing = UIDimensions.get_responsive_spacing(container_width=1000)
        self.assertEqual(spacing, UIDimensions.SPACING_LARGE)
    
    def test_constants_relationships(self) -> None:
        """测试常量之间的逻辑关系"""
        # 内边距大小关系
        self.assertLess(UIDimensions.PADDING_SMALL, UIDimensions.PADDING_MEDIUM)
        self.assertLess(UIDimensions.PADDING_MEDIUM, UIDimensions.PADDING_LARGE)
        
        # 间距大小关系
        self.assertLess(UIDimensions.SPACING_SMALL, UIDimensions.SPACING_MEDIUM)
        self.assertLess(UIDimensions.SPACING_MEDIUM, UIDimensions.SPACING_LARGE)
        self.assertLess(UIDimensions.SPACING_LARGE, UIDimensions.SPACING_EXTRA_LARGE)
        
        # 边框宽度关系
        self.assertLess(UIDimensions.BORDER_WIDTH_THIN, UIDimensions.BORDER_WIDTH_MEDIUM)
        self.assertLess(UIDimensions.BORDER_WIDTH_MEDIUM, UIDimensions.BORDER_WIDTH_THICK)
        
        # 滚动区域尺寸关系
        self.assertLess(UIDimensions.SCROLL_AREA_MIN_WIDTH, UIDimensions.SCROLL_AREA_MAX_WIDTH)
        
        # 窗口尺寸关系
        self.assertLess(UIDimensions.WINDOW_MIN_WIDTH, UIDimensions.WINDOW_DEFAULT_WIDTH)
        self.assertLess(UIDimensions.WINDOW_MIN_HEIGHT, UIDimensions.WINDOW_DEFAULT_HEIGHT)


if __name__ == '__main__':
    unittest.main()