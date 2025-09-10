# coding: utf-8
from PyQt6.QtCore import QObject, pyqtSignal


class MainWindowSignalBus(QObject):
    """信号总线类
    
    用于管理应用程序中的主窗口类的全局信号，实现组件间的解耦通信。
    """

    # 主窗口信号
    micaEnableChanged = pyqtSignal(bool)
    switchToSampleCard = pyqtSignal(str, int)

    # 设置信号
    settingInterfaceRestartSig = pyqtSignal()
    
    # 重启相关信号
    restartRequested = pyqtSignal(str)  # 重启请求信号，携带重启原因
    restartConfirmed = pyqtSignal()  # 用户确认重启信号
    restartCancelled = pyqtSignal()  # 重启取消信号
    countdownTick = pyqtSignal(int)  # 倒计时信号，携带剩余秒数


# 创建信号总线实例
mw_signalBus = MainWindowSignalBus()
