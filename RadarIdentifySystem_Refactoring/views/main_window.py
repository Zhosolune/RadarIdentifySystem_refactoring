from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication
from typing import Optional

from qfluentwidgets import MSFluentWindow, NavigationItemPosition, FluentIcon, SplashScreen
from views.interfaces.main_interface import MainInterface
from views.interfaces.radar_analysis_interface import RadarAnalysisInterface
from views.interfaces.model_management_interface import ModelManagementInterface
from views.interfaces.params_config_interface import ParamsConfigInterface
from views.interfaces.settings_interface import SettingsInterface
from controllers.ui.settings_controller import SettingsController
from models.utils.log_manager import LoggerMixin
from models.utils.icons_manager import Icon
from models.utils.signal_bus import mw_signalBus
from models.config.app_config import _app_cfg


class MainWindow(MSFluentWindow, LoggerMixin):
    """主窗口
    
    使用MSFluentWindow作为主窗口，集成四个导航界面：
    1. 雷达分析（主界面）
    2. 模型管理
    3. 参数配置
    4. 设置
    """
    
    def __init__(self, parent: Optional[object] = None):
        """初始化主窗口
        
        Args:
            parent: 父对象
        Returns:
            None
        """
        super().__init__(parent)
        self._init_window()

        # 创建子界面
        self.main_interface = None
        self.radar_analysis_interface = None
        self.model_management_interface = None
        self.settings_interface = None
        self.params_config_interface = None
        
        # 创建控制器
        self.settings_controller = None

        # 连接信号
        self._connectSignalToSlot()
        
        # 初始化界面
        self._init_navigation()
        self.splashScreen.finish()

    def _init_window(self) -> None:
        """初始化窗口

        Returns:
            None
        """
        self.setWindowTitle("雷达信号识别系统")
        self.resize(1200, 800)

        self.setMicaEffectEnabled(_app_cfg.get(_app_cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        # 设置窗口图标
        self.setWindowIcon(FluentIcon.HOME.icon())
        # 设置窗口居中
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
            
    def _init_navigation(self) -> None:
        """初始化导航
        
        Returns:
            None
        """
        # 创建子界面实例（设置子页面唯一路由）
        self.main_interface: MainInterface = MainInterface(self)  # MainInterface
        self.radar_analysis_interface: RadarAnalysisInterface = RadarAnalysisInterface(self)  # RadarAnalysisInterface
        self.model_management_interface: ModelManagementInterface = ModelManagementInterface(self)  # ModelManagementInterface
        self.settings_interface: SettingsInterface = SettingsInterface(self)  # SettingsInterface
        self.params_config_interface: ParamsConfigInterface = ParamsConfigInterface(self)  # ParamsConfigInterface
        
        # 创建并配置设置控制器
        self.settings_controller: SettingsController = SettingsController(parent=self)
        self.settings_controller.set_settings_interface(settings_interface=self.settings_interface)
        self.logger.info("设置控制器已初始化并连接到设置界面")
        
        # 添加导航项
        self.addSubInterface(
            interface=self.main_interface, 
            icon=FluentIcon.HOME, 
            text="雷达分析", 
            position=NavigationItemPosition.TOP
        )
        
        self.addSubInterface(
            interface=self.radar_analysis_interface, 
            icon=FluentIcon.SEARCH, 
            text="信号分析", 
            position=NavigationItemPosition.TOP
        )
        
        self.addSubInterface(
            interface=self.model_management_interface, 
            icon=FluentIcon.FOLDER, 
            text="模型管理", 
            position=NavigationItemPosition.TOP
        )
        
        self.addSubInterface(
            interface=self.params_config_interface,
            icon=Icon.PARAMS_CONFIG, 
            text="参数配置", 
            position=NavigationItemPosition.BOTTOM
        )

        self.addSubInterface(
            interface=self.settings_interface, 
            icon=FluentIcon.SETTING, 
            text="设置", 
            position=NavigationItemPosition.BOTTOM
        )


    def _connectSignalToSlot(self) -> None:
        """连接窗口信号

        Returns:
            None
        """

        mw_signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
             
    def get_main_interface(self) -> MainInterface:
        """获取主界面实例
        
        Returns:
            主界面实例
        """
        return self.main_interface
        
    def get_radar_analysis_interface(self) -> RadarAnalysisInterface:
        """获取雷达分析界面实例
        
        Returns:
            雷达分析界面实例
        """
        return self.radar_analysis_interface
        
    def get_model_management_interface(self) -> ModelManagementInterface:
        """获取模型管理界面实例
        
        Returns:
            模型管理界面实例
        """
        return self.model_management_interface
        
    def get_settings_interface(self) -> SettingsInterface:
        """获取设置界面实例
        
        Returns:
            设置界面实例
        """
        return self.settings_interface
