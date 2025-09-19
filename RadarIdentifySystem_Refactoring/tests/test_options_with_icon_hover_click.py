# coding:utf-8
"""
测试OptionsWithIcon组件的悬浮和点击效果
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

import unittest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QEnterEvent, QMouseEvent
from PyQt6.QtTest import QTest

from qfluentwidgets import FluentIcon as FIF
from views.components.option_with_icon import OptionsWithIcon


class TestOptionsWithIconHoverClick(unittest.TestCase):
    """测试OptionsWithIcon组件的悬浮和点击效果"""

    @classmethod
    def setUpClass(cls):
        """设置测试类"""
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()

    def setUp(self):
        """设置每个测试"""
        self.widget = OptionsWithIcon(
            icon=FIF.ACCEPT,
            title="测试选项",
            content="这是一个测试选项",
            direction="horizontal"
        )

    def test_mouse_tracking_enabled(self):
        """测试鼠标跟踪是否启用"""
        self.assertTrue(self.widget.hasMouseTracking())

    def test_enter_event_triggers_radio_button_hover(self):
        """测试鼠标进入事件是否触发RadioButton的悬浮效果"""
        # 模拟鼠标进入事件
        with patch.object(self.widget.radioButton, 'enterEvent') as mock_enter:
            from PyQt6.QtCore import QPointF
            enter_event = QEnterEvent(
                QPointF(self.widget.rect().center()),
                QPointF(self.widget.mapToGlobal(self.widget.rect().center())),
                QPointF(self.widget.mapToGlobal(self.widget.rect().center()))
            )
            self.widget.enterEvent(enter_event)
            mock_enter.assert_called_once()

    def test_leave_event_triggers_radio_button_leave(self):
        """测试鼠标离开事件是否触发RadioButton的离开效果"""
        # 模拟鼠标离开事件
        with patch.object(self.widget.radioButton, 'leaveEvent') as mock_leave:
            from PyQt6.QtCore import QPointF
            leave_event = QEnterEvent(
                QPointF(self.widget.rect().center()),
                QPointF(self.widget.mapToGlobal(self.widget.rect().center())),
                QPointF(self.widget.mapToGlobal(self.widget.rect().center()))
            )
            self.widget.leaveEvent(leave_event)
            mock_leave.assert_called_once()

    def test_mouse_click_selects_radio_button(self):
        """测试点击卡片是否选中RadioButton"""
        # 确保RadioButton初始未选中
        self.widget.radioButton.setChecked(False)
        self.assertFalse(self.widget.radioButton.isChecked())

        # 模拟鼠标点击
        from PyQt6.QtCore import QPointF
        mouse_press_event = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            QPointF(self.widget.rect().center()),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier
        )
        self.widget.mousePressEvent(mouse_press_event)

        # 验证RadioButton被选中
        self.assertTrue(self.widget.radioButton.isChecked())

    def test_mouse_click_on_already_selected_radio_button(self):
        """测试点击已选中的RadioButton卡片"""
        # 设置RadioButton为选中状态
        self.widget.radioButton.setChecked(True)
        self.assertTrue(self.widget.radioButton.isChecked())

        # 模拟鼠标点击
        from PyQt6.QtCore import QPointF
        mouse_press_event = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            QPointF(self.widget.rect().center()),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier
        )
        self.widget.mousePressEvent(mouse_press_event)

        # 验证RadioButton仍然选中
        self.assertTrue(self.widget.radioButton.isChecked())

    def test_right_click_does_not_select(self):
        """测试右键点击不会选中RadioButton"""
        # 确保RadioButton初始未选中
        self.widget.radioButton.setChecked(False)
        self.assertFalse(self.widget.radioButton.isChecked())

        # 模拟右键点击
        from PyQt6.QtCore import QPointF
        mouse_press_event = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            QPointF(self.widget.rect().center()),
            Qt.MouseButton.RightButton,
            Qt.MouseButton.RightButton,
            Qt.KeyboardModifier.NoModifier
        )
        self.widget.mousePressEvent(mouse_press_event)

        # 验证RadioButton仍未选中
        self.assertFalse(self.widget.radioButton.isChecked())

    def test_mouse_release_event(self):
        """测试鼠标释放事件"""
        # 模拟鼠标释放事件
        from PyQt6.QtCore import QPointF
        mouse_release_event = QMouseEvent(
            QMouseEvent.Type.MouseButtonRelease,
            QPointF(self.widget.rect().center()),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier
        )
        
        # 这个测试主要确保事件处理不会抛出异常
        try:
            self.widget.mouseReleaseEvent(mouse_release_event)
        except Exception as e:
            self.fail(f"mouseReleaseEvent raised an exception: {e}")

    def tearDown(self):
        """清理每个测试"""
        self.widget.deleteLater()


if __name__ == '__main__':
    unittest.main()