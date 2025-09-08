from typing import Optional
from functools import wraps
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QColor
from qfluentwidgets import setTheme, setThemeColor
from models.config.app_config import _app_cfg
from views.interfaces.settings_interface import SettingsInterface
from models.utils.log_manager import LoggerMixin


class SettingsController(QObject, LoggerMixin):
    """设置界面控制器
    
    负责协调设置界面视图与配置模型之间的交互。
    现采用“配置驱动”的主题刷新策略：
    - 直接监听 _app_cfg.themeChanged / themeColorChanged；
    - 仅在回调里记录日志，不再显式调用 setThemeColor；
    - SettingsInterface 的注入保持为可选（用于未来扩展/其他设置项的信号接线），但主题色不依赖它。
    """
    
    def __init__(self, parent: Optional[QObject] = None) -> None:
        """初始化设置控制器
        
        Args:
            parent (Optional[QObject]): 父对象，用于Qt对象树管理
        
        Returns:
            None
        
        Raises:
            None
        """
        super().__init__(parent=parent)
        self._settings_interface: Optional[SettingsInterface] = None
        
        self.logger.info("正在初始化设置控制器")
        self._setup_theme_connections()
        self.logger.info("设置控制器初始化成功")
    
    def _setup_theme_connections(self) -> None:
        """设置全局主题信号连接
        
        - 连接 _app_cfg.themeChanged -> setTheme（由 PFW 生效整个主题明/暗）；
        - 连接 _app_cfg.themeChanged -> _on_theme_changed（日志/业务扩展点）；
        
        Returns:
            None
        """
        self.logger.debug("正在设置全局主题信号连接")
        _app_cfg.themeChanged.connect(setTheme)
        _app_cfg.themeChanged.connect(self._on_theme_changed)
        self.logger.info("全局主题信号连接已建立")

    def set_settings_interface(self, settings_interface: SettingsInterface) -> None:
        """设置关联的设置界面实例

        Args:
            settings_interface (SettingsInterface): 设置界面实例

        Returns:
            None

        Raises:
            ValueError: 当传入的设置界面为 None 时
        """
        if settings_interface is None:
            self.logger.error("尝试设置空的设置界面")
            raise ValueError("Settings interface cannot be None")

        self._settings_interface = settings_interface
        self.logger.debug("设置界面已注入")
        self._connect_interface_signals()
        self.logger.info("设置界面信号连接完成")
        
    def _connect_interface_signals(self) -> None:
        """连接设置界面中与主题无关或后续可扩展的信号

        - 连接 _settings_interface.themeColorCard -> setThemeColor（由 PFW 生效整个主题色）；
        - 连接 _settings_interface.themeColorCard -> _on_theme_color_changed（仅记录日志）。

        Returns:
            None

        Raises:
            RuntimeError: 当设置界面未设置时抛出
        """
        if self._settings_interface is None:
            self.logger.error("尝试在未设置设置界面的情况下连接信号")
            raise RuntimeError("设置界面在连接信号前必须先被创建")

        if hasattr(self._settings_interface, "themeColorCard") and hasattr(self._settings_interface.themeColorCard, "colorChanged"):
            self._settings_interface.themeColorCard.colorChanged.connect(setThemeColor)
            self._settings_interface.themeColorCard.colorChanged.connect(self._on_theme_color_changed)
        else:
            self.logger.debug("未找到 themeColorCard 或其 colorChanged 信号；当前为配置驱动，跳过接线")

    def _on_theme_changed(self) -> None:
        """主题明/暗变化时的回调处理
        
        用于记录日志或承载后续额外业务逻辑。
        
        Returns:
            None
        """
        current_theme = _app_cfg.themeMode.value
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
