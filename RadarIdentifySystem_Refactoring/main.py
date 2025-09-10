#!/usr/bin/env python3
"""
雷达信号识别系统 - 重构版本启动脚本

解决Python模块路径问题，启动主应用程序
"""

import os
import sys
import subprocess
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from models.config.app_config import _app_cfg
from models.utils.signal_bus import mw_signalBus
from views.main_window import MainWindow

# 将项目根目录添加到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def restart_application():
    """重启应用程序
    
    无缝重启当前应用程序实例。
    
    Returns:
        None
    
    Raises:
        None
    """
    try:
        # 获取当前Python解释器和脚本路径
        python_exe = sys.executable
        script_path = sys.argv[0]
        
        # 启动新的应用程序实例
        subprocess.Popen([python_exe, script_path] + sys.argv[1:])
        
        # 退出当前实例
        QApplication.quit()
    except Exception as e:
        print(f"重启应用程序时发生错误: {e}")

def main():
    """主函数"""
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
    
    # 连接重启信号
    mw_signalBus.restartConfirmed.connect(restart_application)
    
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