from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
from qfluentwidgets import (
    OptionsSettingCard,
    ExpandLayout,
    ScrollArea,
    SettingCardGroup,
    SwitchSettingCard,
    CustomColorSettingCard,
    HyperlinkCard,
    PrimaryPushSettingCard,
    MessageBox,
    InfoBar,
)
from qfluentwidgets import FluentIcon as FIF
from typing import Optional
from models.config.app_config import _app_cfg, AUTHOR, YEAR, HELP_URL, VERSION, isWin11
from models.theme.style_sheet import StyleSheet
from models.utils.log_manager import LoggerMixin


class ParamsConfigInterface(ScrollArea, LoggerMixin):
    """参数配置界面

    用于系统设置的界面，包含主题设置等功能。
    """

    # 注意：重启相关信号已移至信号总线 (models.utils.signal_bus.mw_signalBus)

    def __init__(self, text: str, parent: Optional[QWidget] = None):
        """初始化设置界面

        Args:
            text: 界面标识文本
            parent: 父控件
        """
        super().__init__(parent=parent)
        self.setObjectName("ParamsConfigInterface")
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        StyleSheet.PARAMS_CONFIG_INTERFACE.apply(self)

