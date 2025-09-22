import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from qfluentwidgets import RangeConfigItem, RangeValidator, FluentIcon
from views.components.options_group_setting_card import (
    OptionsGroupWidget, 
    OptionsGroupSettingCard
)


class SmartExchangeDemo(QMainWindow):
    """智能交换机制演示窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("智能交换机制演示")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建测试用的配置项
        self.config1 = RangeConfigItem("Demo", "radar1", 1, RangeValidator(0, 4))
        self.config2 = RangeConfigItem("Demo", "radar2", 2, RangeValidator(0, 4))
        self.config3 = RangeConfigItem("Demo", "radar3", 0, RangeValidator(0, 4))
        
        # 创建选项组件
        self.widget1 = OptionsGroupWidget(self.config1, "雷达1编号")
        self.widget2 = OptionsGroupWidget(self.config2, "雷达2编号")
        self.widget3 = OptionsGroupWidget(self.config3, "雷达3编号")
        
        # 创建设置卡片
        self.setting_card = OptionsGroupSettingCard(
            icon=FluentIcon.SETTING,
            title="智能交换演示",
            content="点击任意编号按钮，体验智能交换和清空机制",
            optionsGroupWidgets=[self.widget1, self.widget2, self.widget3]
        )
        
        layout.addWidget(self.setting_card)
        
        # 连接信号以显示反馈信息
        self.setting_card.optionExchanged.connect(self.on_option_exchanged)
        self.setting_card.optionCleared.connect(self.on_option_cleared)
        
    def on_option_exchanged(self, source_name: str, target_name: str, new_value: int, old_value: int):
        """处理编号交换事件"""
        print(f"智能交换: {source_name} 获得编号 {new_value}，{target_name} 获得编号 {old_value}")
        
    def on_option_cleared(self, cleared_name: str, cleared_value: int):
        """处理编号清空事件"""
        print(f"编号清空: {cleared_name} 的编号 {cleared_value} 已被清空")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 创建演示窗口
    demo = SmartExchangeDemo()
    demo.show()
    
    print("智能交换机制演示说明：")
    print("1. 雷达1初始编号为1，雷达2初始编号为2，雷达3初始编号为0（未选择）")
    print("2. 智能交换：当选择已被占用的编号时，如果当前组件有编号，则与占用该编号的组件交换")
    print("3. 智能清空：当选择已被占用的编号时，如果当前组件没有编号，则清空占用该编号的组件")
    print("4. 所有按钮始终可点击，不会被禁用")
    print("5. 操作时会显示视觉反馈通知")
    print("\n测试建议：")
    print("- 点击雷达1的编号2按钮，观察与雷达2的交换")
    print("- 点击雷达3的编号1按钮，观察雷达1被清空")
    print("- 尝试各种组合，体验智能交换机制")
    
    sys.exit(app.exec())