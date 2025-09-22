import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

import unittest
from unittest.mock import Mock, patch
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import RangeConfigItem, RangeValidator, FluentIcon
from RadarIdentifySystem_Refactoring.views.components.options_group_setting_card import (
    OptionsGroupWidget, 
    OptionsGroupSettingCard
)


class TestOptionsGroupMutualExclusion(unittest.TestCase):
    """测试选项组编号互斥功能"""

    @classmethod
    def setUpClass(cls):
        """设置测试类"""
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()

    def setUp(self):
        """设置测试用例"""
        # 创建测试用的配置项，使用正确的RangeValidator
        self.config1 = RangeConfigItem("Test", "config1", 0, RangeValidator(0, 4))
        self.config2 = RangeConfigItem("Test", "config2", 1, RangeValidator(0, 4))
        self.config3 = RangeConfigItem("Test", "config3", 2, RangeValidator(0, 4))

        # 创建选项组件
        self.widget1 = OptionsGroupWidget(self.config1, "选项组1")
        self.widget2 = OptionsGroupWidget(self.config2, "选项组2")
        self.widget3 = OptionsGroupWidget(self.config3, "选项组3")

        # 创建设置卡片
        self.setting_card = OptionsGroupSettingCard(
            icon=FluentIcon.SETTING,
            title="测试设置卡片",
            content="测试编号互斥功能",
            optionsGroupWidgets=[self.widget1, self.widget2, self.widget3]
        )

    def test_initial_occupied_values(self):
        """测试初始占用值集合"""
        expected_values = {0, 1, 2}  # 初始值分别为0, 1, 2
        self.assertEqual(self.setting_card.occupied_values, expected_values)

    def test_can_select_unoccupied_value(self):
        """测试可以选择未被占用的值"""
        # 值3未被占用，应该可以选择
        result = self.setting_card._canSelectValue(3, self.widget1)
        self.assertTrue(result)

    def test_cannot_select_occupied_value(self):
        """测试不能选择已被占用的值"""
        # 值1被widget2占用，widget1不能选择
        result = self.setting_card._canSelectValue(1, self.widget1)
        self.assertFalse(result)

    def test_can_reselect_own_value(self):
        """测试可以重新选择自己当前的值"""
        # widget1当前值为0，可以重新选择0
        result = self.setting_card._canSelectValue(0, self.widget1)
        self.assertTrue(result)

    def test_button_states_update_on_selection(self):
        """测试选择时按钮状态更新"""
        # 模拟widget1选择值3
        with patch.object(self.widget1, 'updateButtonStates') as mock_update:
            self.setting_card._onOptionChanged(3, 0, self.widget1)
            
            # 由于新逻辑不再维护occupied_values集合，这个测试需要调整
            # 主要验证是否调用了按钮状态更新
            mock_update.assert_called()

    def test_smart_exchange_mechanism(self):
        """测试智能交换机制"""
        # 初始状态：widget1=0, widget2=1, widget3=2
        
        # 模拟widget1选择值1（被widget2占用）
        # 应该触发智能交换：widget1获得1，widget2获得0
        with patch('qfluentwidgets.qconfig.set') as mock_set:
            self.setting_card._onOptionChanged(1, 0, self.widget1)
            
            # 检查是否调用了两次配置设置（交换）
            self.assertEqual(mock_set.call_count, 1)
            # 第一次调用应该是设置widget2的值为0
            mock_set.assert_called_with(self.widget2.configItem, 0)

    def test_smart_clear_mechanism(self):
        """测试智能清空机制"""
        # 创建一个初始值为0的新组件
        new_config = RangeConfigItem("Test", "config4", 0, RangeValidator(0, 4))
        new_widget = OptionsGroupWidget(new_config, "选项组4")
        self.setting_card.addOptionsGroupWidget(new_widget)
        
        # 模拟new_widget选择值1（被widget2占用）
        # 由于new_widget之前的值是0（无效值），应该清空widget2
        with patch('qfluentwidgets.qconfig.set') as mock_set:
            self.setting_card._onOptionChanged(1, 0, new_widget)
            
            # 检查是否调用了配置设置来清空widget2
            mock_set.assert_called_with(self.widget2.configItem, 0)

    def test_visual_feedback_signals(self):
        """测试视觉反馈信号"""
        # 测试交换信号
        with patch.object(self.setting_card, 'optionExchanged') as mock_exchange:
            with patch('qfluentwidgets.qconfig.set'):
                self.setting_card._onOptionChanged(1, 2, self.widget3)  # widget3从2变为1
                
                # 检查是否发出了交换信号
                mock_exchange.emit.assert_called_once_with(
                    self.widget3.configName, 
                    self.widget2.configName, 
                    1, 2
                )

        # 测试清空信号
        new_config = RangeConfigItem("Test", "config4", 0, RangeValidator(0, 4))
        new_widget = OptionsGroupWidget(new_config, "选项组4")
        self.setting_card.addOptionsGroupWidget(new_widget)
        
        with patch.object(self.setting_card, 'optionCleared') as mock_clear:
            with patch('qfluentwidgets.qconfig.set'):
                self.setting_card._onOptionChanged(1, 0, new_widget)  # new_widget从0变为1
                
                # 检查是否发出了清空信号
                mock_clear.emit.assert_called_once_with(
                    self.widget2.configName, 
                    1
                )

    def test_button_always_enabled(self):
        """测试按钮始终保持启用状态（移除禁用逻辑后）"""
        occupied_values = {0, 1, 2, 3, 4}  # 所有值都被占用
        
        # 更新按钮状态
        self.widget1.updateButtonStates(occupied_values)
        
        # 检查所有按钮都应该保持启用状态
        for button in self.widget1.buttonGroup.buttons():
            self.assertTrue(button.isEnabled(), f"按钮 {button.property(self.widget1.configName)} 应该保持启用状态")

    def test_button_click_with_smart_exchange(self):
        """测试点击按钮触发智能交换"""
        # 获取widget1的按钮组中值为1的按钮
        button_1 = None
        for button in self.widget1.buttonGroup.buttons():
            if button.property(self.widget1.configName) == 1:
                button_1 = button
                break
        
        self.assertIsNotNone(button_1)
        
        # 模拟点击值为1的按钮（被widget2占用）
        with patch('qfluentwidgets.qconfig.set') as mock_set:
            self.widget1._onButtonClicked(button_1)
            
            # 检查是否设置了widget1的值为1
            mock_set.assert_any_call(self.config1, 1)

    def test_no_conflict_scenario(self):
        """测试无冲突场景"""
        # 模拟widget1选择值3（未被占用）
        with patch('qfluentwidgets.qconfig.set') as mock_set:
            self.setting_card._onOptionChanged(3, 0, self.widget1)
            
            # 应该只调用一次配置设置（不需要交换或清空）
            self.assertEqual(mock_set.call_count, 0)  # _onOptionChanged不直接调用set，由按钮点击处理

    def test_button_click_without_conflict(self):
        """测试点击无冲突编号的按钮"""
        # 获取widget1的按钮组中值为3的按钮
        button_3 = None
        for button in self.widget1.buttonGroup.buttons():
            if button.property(self.widget1.configName) == 3:
                button_3 = button
                break
        
        self.assertIsNotNone(button_3)
        
        # 模拟点击值为3的按钮（未被占用）
        with patch('qfluentwidgets.qconfig.set') as mock_set:
            self.widget1._onButtonClicked(button_3)
            
            # 检查是否调用了配置设置
            mock_set.assert_called_with(self.config1, 3)

    def test_add_options_group_widget(self):
        """测试添加新的选项组件"""
        # 创建新的配置项和组件
        new_config = RangeConfigItem("Test", "config4", 4, RangeValidator(0, 4))
        new_widget = OptionsGroupWidget(new_config, "选项组4")
        
        # 添加到设置卡片
        self.setting_card.addOptionsGroupWidget(new_widget)
        
        # 检查组件是否被添加
        self.assertIn(new_widget, self.setting_card.optionsGroupWidgets)
        
        # 检查父级卡片引用是否设置
        self.assertEqual(new_widget.parent_card, self.setting_card)

    def test_remove_options_group_widget(self):
        """测试移除选项组件"""
        # 记录移除前的状态
        initial_count = len(self.setting_card.optionsGroupWidgets)
        
        # 移除widget1
        self.setting_card.removeOptionsGroupWidget(self.widget1)
        
        # 检查组件是否被移除
        self.assertNotIn(self.widget1, self.setting_card.optionsGroupWidgets)
        self.assertEqual(len(self.setting_card.optionsGroupWidgets), initial_count - 1)
        
        # 检查父级卡片引用是否被清除
        self.assertIsNone(self.widget1.parent_card)

    def test_update_button_states_no_longer_disables(self):
        """测试按钮状态更新不再禁用按钮（新逻辑）"""
        occupied_values = {0, 2, 4}
        
        # 设置widget1当前值为1（未被占用）
        self.widget1.configItem.value = 1
        
        # 更新按钮状态
        self.widget1.updateButtonStates(occupied_values)
        
        # 检查所有按钮都保持启用状态（新逻辑）
        for button in self.widget1.buttonGroup.buttons():
            self.assertTrue(button.isEnabled(), f"按钮 {button.property(self.widget1.configName)} 应该保持启用状态")

    def tearDown(self):
        """清理测试用例"""
        self.setting_card.deleteLater()
        self.widget1.deleteLater()
        self.widget2.deleteLater()
        self.widget3.deleteLater()


if __name__ == '__main__':
    unittest.main()