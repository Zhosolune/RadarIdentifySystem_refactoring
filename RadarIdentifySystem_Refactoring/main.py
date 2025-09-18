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
    """主函数：初始化应用程序并启动主窗口
    
    Returns:
        int: 应用程序退出代码
        
    Raises:
        ImportError: 当缺少必要的依赖包时
        Exception: 当应用程序启动失败时
    """
    try:
        # 初始化日志系统
        setup_logger(log_level=_app_cfg.logLevel.value)
        
        # 设置高DPI支持
        if hasattr(Qt.ApplicationAttribute, 'AA_EnableHighDpiScaling'):
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        if hasattr(Qt.ApplicationAttribute, 'AA_UseHighDpiPixmaps'):
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        # 设置DPI缩放
        if _app_cfg.dpiScale.value != "Auto":
            os.environ["QT_SCALE_FACTOR"] = str(_app_cfg.dpiScale.value)
        else:
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
        
    except ImportError as e:
        from models.utils.log_manager import get_log_manager
        logger = get_log_manager().get_logger()
        logger.error(f"导入错误: {e}")
        logger.error("请确保已安装PyQt6和PyQt6-Fluent-Widgets")
        logger.error("运行: pip install PyQt6 PyQt6-Fluent-Widgets")
        return 1
    except Exception as e:
        from models.utils.log_manager import get_log_manager
        logger = get_log_manager().get_logger()
        logger.critical(f"启动错误: {e}")
        return 1
    
if __name__ == "__main__":
    sys.exit(main())