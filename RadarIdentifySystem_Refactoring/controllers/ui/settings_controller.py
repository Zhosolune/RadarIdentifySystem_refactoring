from typing import Optional
from PyQt6.QtCore import QObject
from qfluentwidgets import setTheme, setThemeColor
from models.config.app_config import _app_cfg
from views.interfaces.settings_interface import SettingsInterface
from models.utils.log_manager import LoggerMixin


class SettingsController(QObject, LoggerMixin):
    """设置界面控制器
    
    负责协调设置界面视图与配置模型之间的交互，
    处理主题相关的信号连接和业务逻辑。
    """
    
    def __init__(self, parent: Optional[QObject] = None):
        """初始化设置控制器
        
        Args:
            parent: 父对象，用于Qt对象树管理
        """
        super().__init__(parent=parent)
        self._settings_interface: Optional[SettingsInterface] = None
        
        self.logger.info("正在初始化设置控制器")
        self._setup_global_theme_connections()
        self.logger.info("设置控制器初始化成功")
    
    def set_settings_interface(self, settings_interface: SettingsInterface) -> None:
        """设置关联的设置界面
        
        Args:
            settings_interface: 设置界面实例
            
        Raises:
            ValueError: 当传入的设置界面为None时抛出
        """
        if settings_interface is None:
            self.logger.error("尝试设置空的设置界面")
            raise ValueError("Settings interface cannot be None")
            
        self.logger.info("正在为控制器设置设置界面")
        self._settings_interface = settings_interface
        self._connect_interface_signals()
        self.logger.info("设置界面连接成功")
    
    def _setup_global_theme_connections(self) -> None:
        """设置全局主题信号连接
        
        将应用配置的主题变化信号连接到全局主题应用函数，
        确保主题变化能够全局生效。这些连接只需要在应用启动时设置一次。
        """
        self.logger.debug("正在设置全局主题信号连接")
        
        # 连接全局主题变化信号
        _app_cfg.themeChanged.connect(setTheme)
        self.logger.debug("已连接主题变化信号到主题设置函数")
        
        # 连接全局主题色变化信号  
        _app_cfg.themeColorChanged.connect(setThemeColor)
        self.logger.debug("已连接主题色变化信号到主题色设置函数")
        
        self.logger.info("全局主题信号连接已建立")
    
    def _connect_interface_signals(self) -> None:
        """连接设置界面的信号
        
        将设置界面中各个设置卡的信号连接到相应的处理方法。
        注意：由于OptionsSettingCard和CustomColorSettingCard已经通过
        构造函数绑定了ConfigItem，它们的值变化会自动更新配置，
        这里主要处理需要额外业务逻辑的场景。
        
        Raises:
            RuntimeError: 当设置界面未设置时抛出
        """
        if self._settings_interface is None:
            self.logger.error("尝试在未设置设置界面的情况下连接信号")
            raise RuntimeError("设置界面在连接信号前必须先被创建")
        
        self.logger.debug("正在连接设置界面信号")
        
        # 主题卡片的选项变化已经通过ConfigItem自动处理
        # 这里可以添加额外的业务逻辑，比如日志记录、验证等
        
        # 主题色卡片的颜色变化也已经通过ConfigItem自动处理
        # 由于CustomColorSettingCard绑定了_app_cfg.themeColor，
        # 颜色变化会自动触发themeColorChanged信号，
        # 进而通过我们在_setup_global_theme_connections中设置的连接
        # 调用setThemeColor函数
        
        # 如果需要在主题变化时执行额外逻辑，可以连接到配置信号：
        _app_cfg.themeChanged.connect(self._on_theme_changed)
        _app_cfg.themeColorChanged.connect(self._on_theme_color_changed)
        
        self.logger.info("设置界面信号连接成功")
    
    def _on_theme_changed(self) -> None:
        """主题变化时的回调处理
        
        当应用主题发生变化时执行的额外业务逻辑，
        比如日志记录、状态同步等。
        """
        current_theme = _app_cfg.themeMode.value
        self.logger.info(f"主题已切换为: {current_theme}")
        
        # 这里可以添加主题变化时的额外处理逻辑
        # 例如：通知其他组件、保存用户偏好等
    
    def _on_theme_color_changed(self) -> None:
        """主题色变化时的回调处理
        
        当应用主题色发生变化时执行的额外业务逻辑，
        比如日志记录、状态同步等。
        """
        current_color = _app_cfg.themeColor.value
        self.logger.info(f"主题色已切换为: {current_color}")
        
        # 这里可以添加主题色变化时的额外处理逻辑
        # 例如：通知其他组件、保存用户偏好等
    
    def get_settings_interface(self) -> Optional[SettingsInterface]:
        """获取关联的设置界面
        
        Returns:
            关联的设置界面实例，如果未设置则返回None
        """
        return self._settings_interface