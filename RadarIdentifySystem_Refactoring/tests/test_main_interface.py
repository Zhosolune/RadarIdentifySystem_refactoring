import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from qfluentwidgets import setTheme, Theme
from views.interfaces.main_interface import MainInterface


class TestMainWindow(QMainWindow):
    """测试主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("主界面测试")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建主界面
        self.main_interface = MainInterface("测试")
        
        # 在左侧滚动区域添加测试内容
        left_content = QLabel("左侧水平滚动区域\n这里可以放置需要水平滚动的内容")
        left_content.setStyleSheet("QLabel { padding: 20px; background-color: #f0f0f0; }")
        self.main_interface.get_left_scroll_area().setWidget(left_content)
        
        # 在右侧滚动区域添加测试内容
        right_content = QLabel("右侧垂直滚动区域\n\n" + "\n".join([f"第{i}行内容" for i in range(1, 21)]))
        right_content.setStyleSheet("QLabel { padding: 20px; background-color: #e0e0e0; }")
        self.main_interface.get_right_scroll_area().setWidget(right_content)
        
        self.setCentralWidget(self.main_interface)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置主题
    setTheme(Theme.LIGHT)
    
    window = TestMainWindow()
    window.show()
    
    sys.exit(app.exec())