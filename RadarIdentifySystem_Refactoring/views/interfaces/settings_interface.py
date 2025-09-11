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
from models.utils.signal_bus import mw_signalBus


class SettingsInterface(ScrollArea, LoggerMixin):
    """设置界面

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
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # 设置标签
        self.settingLabel = QLabel("设置", self)

        # 个性化
        self.personalGroup = SettingCardGroup("个性化", self.scrollWidget)
        self.micaCard = SwitchSettingCard(
            FIF.TRANSPARENT, 
            "云母效果", 
            "窗口界面的半透明效果", 
            _app_cfg.micaEnabled, 
            self.personalGroup
        )
        self.themeCard = OptionsSettingCard(
            _app_cfg.themeMode,
            FIF.BRUSH,
            "应用主题",
            "调整应用的外观",
            texts=["浅色", "深色", "跟随系统设置"],
            parent=self.personalGroup,
        )
        self.themeColorCard = CustomColorSettingCard(
            _app_cfg.themeColor, 
            FIF.PALETTE, 
            "主题色", 
            "调整应用的主题色", 
            self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            _app_cfg.dpiScale,
            FIF.ZOOM,
            "界面缩放",
            "调整界面的缩放比例",
            texts=["100%", "125%", "150%", "175%", "200%", "跟随系统设置"],
            parent=self.personalGroup,
        )

        # 关于
        self.aboutGroup = SettingCardGroup("关于", self.scrollWidget)
        self.helpCard = HyperlinkCard(
            HELP_URL,
            "打开帮助页面",
            FIF.HELP,
            "帮助",
            "发现新功能并了解使用技巧",
            self.aboutGroup,
        )
        self.aboutCard = PrimaryPushSettingCard(
            "检查更新",
            FIF.INFO,
            "关于",
            "© " + "版权所有" + f" {YEAR}, {AUTHOR}. " + "当前版本" + " " + VERSION,
            self.aboutGroup,
        )

        # 初始化对话框相关属性
        self._restart_dialog: Optional[MessageBox] = None
        
        # 设置UI
        self._setup_ui()

    def _setup_ui(self) -> None:
        """设置用户界面"""
        # 设置滚动区域属性
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("settingInterface")

        # 初始化样式
        self.scrollWidget.setObjectName("scrollWidget")
        self.settingLabel.setObjectName("settingLabel")
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.micaCard.setEnabled(isWin11())

        # 初始化布局
        self._initLayout()

    def _initLayout(self):
        self.settingLabel.move(36, 30)

        # 添加设置卡片到组
        self.personalGroup.addSettingCard(self.micaCard)
        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.zoomCard)

        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.aboutCard)

        # 添加设置卡片组到布局
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def showRestartTooltip(self):
        """唤起重启提示"""
        InfoBar.success("修改成功", "配置将在重启后生效", duration=1500, parent=self)
