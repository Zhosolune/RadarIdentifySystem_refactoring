# coding: utf-8
from PyQt6.QtCore import QObject, pyqtSignal


class MainWindowSignalBus(QObject):
    """主窗口信号总线类
    
    用于管理应用程序中的主窗口类的全局信号，实现组件间的解耦通信。
    """

    # 主窗口信号
    micaEnableChanged = pyqtSignal(bool)
    switchToSampleCard = pyqtSignal(str, int)

    # 设置信号
    settingInterfaceRestartSig = pyqtSignal()



# 创建信号总线实例
mw_signalBus = MainWindowSignalBus()
