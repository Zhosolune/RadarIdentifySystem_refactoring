"""设置界面标签定位演示程序

演示设置标签的相对定位功能，展示标签位置如何随窗口大小变化而自动调整。
"""

import sys
import os

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from views.interfaces.settings_interface import SettingsInterface
from models.ui.dimensions import UIDimensions


class SettingsLabelPositioningDemo(QMainWindow):
    """设置界面标签定位演示窗口
    
    展示设置标签的相对定位功能，包含窗口大小调整按钮。
    """
    
    def __init__(self) -> None:
        """初始化演示窗口"""
        super().__init__()
        self._setup_ui()
        self._setup_connections()
    
    def _setup_ui(self) -> None:
        """设置用户界面"""
        # 设置窗口基本属性
        self.setWindowTitle("设置界面标签定位演示")
        self.resize(UIDimensions.WINDOW_DEFAULT_WIDTH, UIDimensions.WINDOW_DEFAULT_HEIGHT)
        self.setMinimumSize(UIDimensions.WINDOW_MIN_WIDTH, UIDimensions.WINDOW_MIN_HEIGHT)
        
        # 创建中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 创建说明标签
        info_label = QLabel("演示说明：")
        info_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        main_layout.addWidget(info_label)
        
        description_label = QLabel(
            "• 观察'设置'标签的位置变化\n"
            "• 标签位置会根据窗口大小自动调整\n"
            "• 标签始终与滚动区域的左边距保持一致\n"
            "• 当窗口最大化时，标签不会固定在左上角"
        )
        description_label.setStyleSheet("margin-bottom: 10px;")
        main_layout.addWidget(description_label)
        
        # 创建控制按钮区域
        button_layout = QHBoxLayout()
        
        self.small_size_btn = QPushButton("小窗口 (800x600)")
        self.medium_size_btn = QPushButton("中等窗口 (1200x800)")
        self.large_size_btn = QPushButton("大窗口 (1600x1000)")
        self.max_btn = QPushButton("最大化窗口")
        
        button_layout.addWidget(self.small_size_btn)
        button_layout.addWidget(self.medium_size_btn)
        button_layout.addWidget(self.large_size_btn)
        button_layout.addWidget(self.max_btn)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        # 创建设置界面
        self.settings_interface = SettingsInterface("demo")
        main_layout.addWidget(self.settings_interface)
        
        # 添加位置信息标签
        self.position_info_label = QLabel()
        self.position_info_label.setStyleSheet("font-family: monospace; background-color: #f0f0f0; padding: 5px;")
        main_layout.addWidget(self.position_info_label)
        
        # 更新位置信息
        self._update_position_info()
    
    def _setup_connections(self) -> None:
        """设置信号连接"""
        self.small_size_btn.clicked.connect(lambda: self._resize_window(800, 600))
        self.medium_size_btn.clicked.connect(lambda: self._resize_window(1200, 800))
        self.large_size_btn.clicked.connect(lambda: self._resize_window(1600, 1000))
        self.max_btn.clicked.connect(self.showMaximized)
    
    def _resize_window(self, width: int, height: int) -> None:
        """调整窗口大小
        
        Args:
            width: 目标宽度
            height: 目标高度
        """
        if self.isMaximized():
            self.showNormal()
        self.resize(width, height)
        self._update_position_info()
    
    def _update_position_info(self) -> None:
        """更新位置信息显示"""
        # 获取当前标签位置
        label_pos = self.settings_interface.settingLabel.pos()
        window_size = self.size()
        
        # 计算滚动区域宽度
        scroll_area_width = min(window_size.width(), UIDimensions.SCROLL_AREA_MAX_WIDTH_SETTING)
        
        # 更新信息显示
        info_text = (
            f"窗口大小: {window_size.width()} x {window_size.height()} | "
            f"滚动区域宽度: {scroll_area_width} | "
            f"标签位置: ({label_pos.x()}, {label_pos.y()})"
        )
        self.position_info_label.setText(info_text)
    
    def resizeEvent(self, event) -> None:
        """窗口大小变化事件
        
        Args:
            event: 大小变化事件
        """
        super().resizeEvent(event)
        # 延迟更新位置信息，确保设置界面已经处理了resize事件
        self._update_position_info()
    
    def showEvent(self, event) -> None:
        """窗口显示事件
        
        Args:
            event: 显示事件
        """
        super().showEvent(event)
        self._update_position_info()


def main() -> None:
    """主函数
    
    创建并运行演示应用程序。
    """
    app = QApplication(sys.argv)
    
    # 创建演示窗口
    demo_window = SettingsLabelPositioningDemo()
    demo_window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == '__main__':
    main()