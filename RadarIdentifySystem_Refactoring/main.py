#!/usr/bin/env python3
"""
雷达信号识别系统 - 重构版本启动脚本

解决Python模块路径问题，启动主应用程序
"""

import os
import sys
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from models.utils.log_manager import setup_logger
from models.config.app_config import _app_cfg
from views.main_window import MainWindow

# 将项目根目录添加到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """主函数"""
    # 初始化日志系统
    log_level = _app_cfg.get(_app_cfg.logLevel)
    setup_logger(log_level=log_level)

    # 在创建QApplication之前设置高DPI支持
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    # 根据配置设置DPI缩放
    dpi_scale = _app_cfg.get(_app_cfg.dpiScale)
    if dpi_scale != "Auto":
        # 使用手动设置的缩放比例
        os.environ["QT_SCALE_FACTOR"] = str(dpi_scale)
    else:
        # Auto模式下清除环境变量，让Qt使用系统DPI设置
        if "QT_SCALE_FACTOR" in os.environ:
            del os.environ["QT_SCALE_FACTOR"]
                
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
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