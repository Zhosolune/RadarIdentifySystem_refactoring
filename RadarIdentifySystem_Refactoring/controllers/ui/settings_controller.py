from typing import Optional
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QColor
from qfluentwidgets import setTheme, setThemeColor
from views.interfaces.settings_interface import SettingsInterface
from models.utils.log_manager import LoggerMixin, get_log_manager
from models.config.app_config import cfg
from models.utils.signal_bus import mw_signalBus


class SettingsController(QObject, LoggerMixin):
    """设置界面控制器
    
    负责协调设置界面视图与配置模型之间的交互。
    现采用“配置驱动”的主题刷新策略：
    - 直接监听 cfg.themeChanged / themeColorChanged；
    - 仅在回调里记录日志，不再显式调用 setThemeColor；
    - 通过构造函数直接注入 SettingsInterface，确保控制器创建时就是完整可用的状态。
    """
    
    def __init__(self, settings_interface: SettingsInterface, parent: Optional[QObject] = None) -> None:
        """初始化设置控制器
        
        Args:
            settings_interface (SettingsInterface): 设置界面实例
            parent (Optional[QObject]): 父对象，用于Qt对象树管理
        
        Returns:
            None
        
        Raises:
            ValueError: 当传入的设置界面为 None 时
        """
        super().__init__(parent=parent)
            
        self._settings_interface: SettingsInterface = settings_interface
        
        self.logger.debug("正在初始化设置控制器")
        self._setup_app_connections()
        self._connect_interface_signals()
        self.logger.info("设置控制器初始化成功，界面信号已连接")
    
    def _setup_app_connections(self) -> None:
        """设置全局信号连接
        
        - 连接 cfg.themeChanged -> setTheme（由 PFW 生效整个主题明/暗）；
        - 连接 cfg.themeChanged -> _on_theme_changed（日志/业务扩展点）；
        - 连接 cfg.dpiScale.valueChanged -> _on_dpi_scale_changed（DPI变化处理）；
        - 连接 cfg.logLevel.valueChanged -> _on_log_level_changed（日志级别变化处理）；
        
        Returns:
            None
        """
        self.logger.debug("正在设置全局主题信号连接")
        cfg.themeChanged.connect(setTheme)
        cfg.themeChanged.connect(self._on_theme_changed)
        cfg.dpiScale.valueChanged.connect(self._on_dpi_scale_changed)
        cfg.logLevel.valueChanged.connect(self._on_log_level_changed)
        self.logger.debug("全局主题、DPI和日志级别信号连接已建立")

    def _connect_interface_signals(self) -> None:
        """连接设置界面中与主题无关或后续可扩展的信号

        - 连接 _settings_interface.themeColorCard -> setThemeColor（由 PFW 生效整个主题色）；
        - 连接 _settings_interface.themeColorCard -> _on_theme_color_changed（仅记录日志）。
        - 连接 _settings_interface.micaCard -> mw_signalBus.micaEnableChanged（是否开启云母效果）。

        Returns:
            None

        Raises:
            None
        """
        try:
            # 连接主题色变化信号
            self._settings_interface.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c))
            self._settings_interface.themeColorCard.colorChanged.connect(self._on_theme_color_changed)
            self.logger.debug("主题色卡片信号连接成功")
        except AttributeError as e:
            self.logger.debug(f"未找到 themeColorCard 或其 colorChanged 信号: {e}")
        
        try:
            # 连接云母效果开关信号
            self._settings_interface.micaCard.checkedChanged.connect(mw_signalBus.micaEnableChanged)
            self.logger.debug("云母效果卡片信号连接成功")
        except AttributeError as e:
            self.logger.debug(f"未找到 micaCard 或其 checkedChanged 信号: {e}")

    def _on_theme_changed(self) -> None:
        """主题明/暗变化时的回调处理
        
        用于记录日志或承载后续额外业务逻辑。
        
        Returns:
            None
        """
        current_theme = cfg.themeMode.value
        self.logger.info(f"主题已切换为: {current_theme}")

    def _on_theme_color_changed(self, color: QColor) -> None:
        """主题色变化时的回调处理
        
        Args:
            color (QColor): 新的主题色值（QColor 或兼容类型）
        
        Returns:
            None
        
        Raises:
            None
        """
        color_name = color.name() if hasattr(color, 'name') else str(color)
        self.logger.info(f"主题色已变更为: {color_name}")
    
    def _on_dpi_scale_changed(self, value) -> None:
        """DPI缩放变化时的回调处理
        
        当DPI缩放设置变更时触发，显示带倒计时的重启确认对话框。
        
        Args:
            value: 新的DPI缩放值
        
        Returns:
            None
        
        Raises:
            None
        """
        self.logger.info(f"DPI缩放已变更为: {value}，准备显示重启确认对话框")
        self._settings_interface.showRestartTooltip()
    
    def _on_log_level_changed(self, value: str) -> None:
        """日志级别变化时的回调处理
        
        当日志级别设置变更时触发，动态更新日志管理器的级别。
        
        Args:
            value: 新的日志级别值
        
        Returns:
            None
        
        Raises:
            None
        """
        try:
            log_manager = get_log_manager()
            log_manager.set_level(value)
            self.logger.info(f"日志级别已动态更新为: {value}")
        except Exception as e:
            self.logger.error(f"更新日志级别失败: {e}")
    
