from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
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
        # self.__connectSignalToSlot()

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
    
    def show_restart_confirmation_dialog(self, countdown_seconds: int = 3) -> None:
        """显示重启确认对话框
        
        Args:
            countdown_seconds: 倒计时秒数，默认为3秒
            
        Returns:
            None
            
        Raises:
            None
        """
        if self._restart_dialog is not None:
            self._restart_dialog.close()
        
        self._restart_dialog = MessageBox(
            title="重启确认",
            content=f"DPI设置已更改，需要重启应用生效。\n\n{countdown_seconds}秒后自动关闭",
            parent=self
        )
        
        # 设置对话框按钮
        self._restart_dialog.yesButton.setText("立即重启")
        self._restart_dialog.cancelButton.setText("取消")
        
        # 连接按钮信号
        self._restart_dialog.yesButton.clicked.connect(self._on_restart_confirmed)
        self._restart_dialog.cancelButton.clicked.connect(self._on_restart_cancelled)
        
        self._restart_dialog.show()
        self.logger.debug("重启确认对话框已显示")
    
    def update_countdown_display(self, countdown_seconds: int) -> None:
        """更新倒计时显示
        
        Args:
            countdown_seconds: 剩余倒计时秒数
            
        Returns:
            None
            
        Raises:
            None
        """
        if self._restart_dialog is not None:
            self._restart_dialog.contentLabel.setText(
                f"DPI设置已更改，需要重启应用生效。\n\n{countdown_seconds}秒后自动关闭"
            )
    
    def close_restart_dialog(self) -> None:
        """关闭重启确认对话框
        
        Returns:
            None
            
        Raises:
            None
        """
        if self._restart_dialog is not None:
            self._restart_dialog.close()
            self._restart_dialog = None
            self.logger.debug("重启确认对话框已关闭")
    
    def _on_restart_confirmed(self) -> None:
        """用户确认重启的回调处理
        
        当用户点击"立即重启"按钮时触发。
        
        Returns:
            None
            
        Raises:
            None
        """
        self.logger.info("用户确认重启应用")
        self.close_restart_dialog()
        # 发射确认重启信号到信号总线
        mw_signalBus.restartConfirmed.emit()
    
    def _on_restart_cancelled(self) -> None:
        """用户取消重启的回调处理
        
        当用户点击"取消"按钮时触发。
        
        Returns:
            None
            
        Raises:
            None
        """
        self.logger.info("用户取消重启应用")
        self.close_restart_dialog()
        # 发射取消重启信号到信号总线
        mw_signalBus.restartCancelled.emit()
