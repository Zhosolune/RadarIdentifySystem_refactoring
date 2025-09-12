"""UIDimensions使用示例

展示如何在界面开发中使用全局尺寸设定类，避免硬编码尺寸值。
"""

import sys
import os

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt6.QtCore import Qt
from qfluentwidgets import ScrollArea, PushButton, LineEdit
from models.ui.dimensions import UIDimensions


class ExampleWidget(QWidget):
    """使用UIDimensions的示例界面
    
    展示如何使用全局尺寸设定类来创建一致的界面布局。
    """
    
    def __init__(self) -> None:
        super().__init__()
        self._setup_ui()
        self._setup_styles()
    
    def _setup_ui(self) -> None:
        """设置用户界面"""
        # 设置窗口基本属性
        self.setWindowTitle("UIDimensions 使用示例")
        self.resize(UIDimensions.WINDOW_DEFAULT_WIDTH, UIDimensions.WINDOW_DEFAULT_HEIGHT)
        self.setMinimumSize(UIDimensions.WINDOW_MIN_WIDTH, UIDimensions.WINDOW_MIN_HEIGHT)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(
            UIDimensions.PADDING_LARGE,
            UIDimensions.PADDING_LARGE,
            UIDimensions.PADDING_LARGE,
            UIDimensions.PADDING_LARGE
        )
        main_layout.setSpacing(UIDimensions.SPACING_LARGE)
        
        # 创建标题
        title_label = QLabel("UIDimensions 全局尺寸管理示例")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 创建输入区域
        input_layout = self._create_input_section()
        main_layout.addLayout(input_layout)
        
        # 创建按钮区域
        button_layout = self._create_button_section()
        main_layout.addLayout(button_layout)
        
        # 创建滚动区域示例
        scroll_area = self._create_scroll_area_example()
        main_layout.addWidget(scroll_area)
    
    def _create_input_section(self) -> QHBoxLayout:
        """创建输入区域
        
        Returns:
            包含输入控件的水平布局
        """
        layout = QHBoxLayout()
        layout.setSpacing(UIDimensions.SPACING_MEDIUM)
        
        # 标签
        label = QLabel("输入示例:")
        layout.addWidget(label)
        
        # 输入框
        line_edit = LineEdit()
        line_edit.setMinimumWidth(UIDimensions.INPUT_MIN_WIDTH)
        line_edit.setFixedHeight(UIDimensions.INPUT_HEIGHT)
        line_edit.setPlaceholderText("请输入内容...")
        layout.addWidget(line_edit)
        
        layout.addStretch()  # 添加弹性空间
        
        return layout
    
    def _create_button_section(self) -> QHBoxLayout:
        """创建按钮区域
        
        Returns:
            包含按钮的水平布局
        """
        layout = QHBoxLayout()
        layout.setSpacing(UIDimensions.SPACING_MEDIUM)
        
        # 创建不同大小的按钮
        buttons = [
            ("小按钮", UIDimensions.BUTTON_MIN_WIDTH),
            ("中等按钮", UIDimensions.BUTTON_MIN_WIDTH * 1.5),
            ("大按钮", UIDimensions.BUTTON_MIN_WIDTH * 2)
        ]
        
        for text, width in buttons:
            button = PushButton(text)
            button.setMinimumWidth(int(width))
            button.setMinimumHeight(UIDimensions.BUTTON_MIN_HEIGHT)
            layout.addWidget(button)
        
        layout.addStretch()  # 添加弹性空间
        
        return layout
    
    def _create_scroll_area_example(self) -> ScrollArea:
        """创建滚动区域示例
        
        Returns:
            配置好的滚动区域
        """
        scroll_area = ScrollArea()
        scroll_area.setMinimumHeight(UIDimensions.SCROLL_AREA_MIN_HEIGHT)
        
        # 创建滚动内容
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(
            UIDimensions.PADDING_MEDIUM,
            UIDimensions.PADDING_MEDIUM,
            UIDimensions.PADDING_MEDIUM,
            UIDimensions.PADDING_MEDIUM
        )
        content_layout.setSpacing(UIDimensions.SPACING_SMALL)
        
        # 添加示例内容
        for i in range(20):
            label = QLabel(f"滚动内容项 {i + 1}")
            content_layout.addWidget(label)
        
        scroll_area.setWidget(content_widget)
        
        return scroll_area
    
    def _setup_styles(self) -> None:
        """设置样式"""
        # 使用UIDimensions中的边框宽度设置样式
        border_style = f"""
            QWidget {{
                border: {UIDimensions.BORDER_WIDTH_THIN}px solid #CCCCCC;
                border-radius: 4px;
            }}
        """
        
        # 可以根据需要应用样式
        # self.setStyleSheet(border_style)
    
    def resizeEvent(self, event) -> None:
        """窗口大小改变事件
        
        演示如何使用响应式尺寸方法。
        
        Args:
            event: 大小改变事件
        """
        super().resizeEvent(event)
        
        # 获取响应式内边距和间距
        responsive_padding = UIDimensions.get_responsive_padding(self.width())
        responsive_spacing = UIDimensions.get_responsive_spacing(self.width())
        
        # 可以根据响应式值调整布局
        # 这里只是演示，实际使用时可以动态调整布局参数
        print(f"窗口宽度: {self.width()}, 响应式内边距: {responsive_padding}, 响应式间距: {responsive_spacing}")


def main() -> None:
    """主函数
    
    创建并运行示例应用程序。
    """
    app = QApplication(sys.argv)
    
    # 创建示例窗口
    window = ExampleWidget()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == '__main__':
    main()