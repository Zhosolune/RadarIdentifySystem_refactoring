# coding: utf-8
from PyQt6.QtCore import QObject, pyqtSignal


class MainWindowSignalBus(QObject):
    """pyqtSignal bus"""

    micaEnableChanged = pyqtSignal(bool)





mw_signalBus = MainWindowSignalBus()
