# coding:utf-8
"""
OptionsWithIcon组件悬浮和点击效果演示程序
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from views.components.options_with_icon_card import OptionsWithIconCard


class DemoWindow(QMainWindow):
    """演示窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OptionsWithIcon 悬浮和点击效果演示")
        self.setGeometry(100, 100, 600, 400)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 添加说明标签
        info_label = QLabel("演示说明：")
        info_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        layout.addWidget(info_label)
        
        instructions = QLabel(
            "1. 将鼠标悬浮在卡片上，可以看到RadioButton的悬浮动画效果\n"
            "2. 点击卡片任意位置，可以直接选中对应的RadioButton\n"
            "3. 观察控制台日志输出，了解事件处理过程"
        )
        instructions.setStyleSheet("font-size: 12px; color: #666; margin-bottom: 20px;")
        layout.addWidget(instructions)
        
        # 创建OptionsWithIconCard组件
        self.options_card = OptionsWithIconCard(
            icon=FIF.SETTING,
            title="数据方向设置",
            content="选择样本脉冲的排列方向"
        )
        
        # 连接信号
        self.options_card.dataDirectionChanged.connect(self.on_direction_changed)
        
        layout.addWidget(self.options_card)
        layout.addStretch()
        
        print("演示程序启动完成！")
        print("请尝试悬浮和点击卡片来体验交互效果。")
    
    def on_direction_changed(self, direction):
        """处理方向改变信号"""
        print(f"数据方向已改变为: {direction}")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    # 创建并显示窗口
    window = DemoWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == '__main__':
    main()