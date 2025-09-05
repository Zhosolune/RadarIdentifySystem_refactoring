#!/usr/bin/env python3
"""
雷达信号识别系统 - 重构版本启动脚本

解决Python模块路径问题，启动主应用程序
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator
from views.main_window import MainWindow

# 将项目根目录添加到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# try:

def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("雷达信号识别系统")
    app.setApplicationVersion("2.0.0")

    # 安装翻译器
    translator = FluentTranslator()
    app.installTranslator(translator)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    return app.exec()
    
if __name__ == "__main__":
    sys.exit(main())
        
# except ImportError as e:
#     print(f"导入错误: {e}")
#     print("请确保已安装PyQt6和PyQt6-Fluent-Widgets")
#     print("运行: pip install PyQt6 PyQt6-Fluent-Widgets")
#     sys.exit(1)
# except Exception as e:
#     print(f"启动错误: {e}")
#     sys.exit(1)