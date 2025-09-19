from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QResizeEvent
from qfluentwidgets import (
    OptionsSettingCard,
    ComboBoxSettingCard,
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
from models.config.app_config import cfg, AUTHOR, YEAR, HELP_URL, VERSION, isWin11
from models.theme.style_sheet import StyleSheet
from models.utils.log_manager import LoggerMixin
from models.ui.dimensions import UIDimensions


class SettingsInterface(ScrollArea, LoggerMixin):
    """设置界面

    用于系统设置的界面，包含主题设置等功能。
    """

    def __init__(self, text: str, parent: Optional[QWidget] = None):
        """初始化设置界面

        Args:
            text: 界面标识文本
            parent: 父控件
        """
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.scrollWidget.setMaximumWidth(UIDimensions.SCROLL_AREA_MAX_WIDTH_SETTING)
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # 设置标签
        self.settingLabel = QLabel("设置", self)

        # 基本设置
        self.basicGroup = SettingCardGroup("基本设置", self.scrollWidget)
        self.logLevelCard = ComboBoxSettingCard(
            cfg.logLevel,
            FIF.DOCUMENT,
            "日志级别",
            "调整应用的日志记录级别，DEBUG级别最低。选择的级别越高，过滤掉的日志输出越多。",
            texts=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            parent=self.basicGroup,
        )

        # 个性化
        self.personalGroup = SettingCardGroup("个性化", self.scrollWidget)
        self.micaCard = SwitchSettingCard(
            FIF.TRANSPARENT, 
            "云母效果", 
            "窗口界面的半透明效果", 
            cfg.micaEnabled, 
            self.personalGroup
        )
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            "应用主题",
            "调整应用的外观",
            texts=["浅色", "深色", "跟随系统设置"],
            parent=self.personalGroup,
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor, 
            FIF.PALETTE, 
            "主题色", 
            "调整应用的主题色", 
            self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
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
        self.setObjectName("SettingsInterface")
        
        # 设置滚动区域居中对齐
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # 初始化样式
        self.scrollWidget.setObjectName("scrollWidget")
        self.settingLabel.setObjectName("settingLabel")
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.micaCard.setEnabled(isWin11())

        # 初始化布局
        self._initLayout()

    def _initLayout(self) -> None:
        """初始化布局
        
        设置标签位置和卡片组布局。
        """
        # 初始化标签位置（相对定位）
        self._updateLabelPosition()

        # 添加设置卡片到组
        self.basicGroup.addSettingCard(self.logLevelCard)
        
        self.personalGroup.addSettingCard(self.micaCard)
        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.zoomCard)

        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.aboutCard)

        # 添加设置卡片组到布局
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.basicGroup)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def _updateLabelPosition(self) -> None:
        """更新设置标签位置
        
        根据滚动区域的宽度动态调整标签位置，使其始终与滚动区域保持一致的对齐方式。
        """
        # 获取当前窗口宽度
        window_width = self.width() if self.width() > 0 else UIDimensions.WINDOW_DEFAULT_WIDTH
        
        # 计算滚动区域的实际宽度（考虑最大宽度限制）
        scroll_area_width = min(window_width, UIDimensions.SCROLL_AREA_MAX_WIDTH_SETTING)
        
        # 计算标签的水平位置（与滚动区域左边距保持一致）
        # 滚动区域居中对齐，所以标签也应该相对于居中位置计算
        center_offset = (window_width - scroll_area_width) // 2
        label_x = max(center_offset + 36, 36)  # 确保最小边距为36px
        
        # 设置标签位置
        self.settingLabel.move(label_x, 30)
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        """窗口大小变化事件处理
        
        当窗口大小变化时，自动调整设置标签的位置。
        
        Args:
            event: 窗口大小变化事件
        """
        super().resizeEvent(event)
        # 更新标签位置以适应新的窗口大小
        self._updateLabelPosition()

    def showRestartTooltip(self) -> None:
        """唤起重启提示"""
        InfoBar.success("修改成功", "配置将在重启后生效", duration=1500, parent=self)
