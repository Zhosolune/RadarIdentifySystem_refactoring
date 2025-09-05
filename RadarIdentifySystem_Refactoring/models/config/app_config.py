import sys
import datetime

from qfluentwidgets import (
    qconfig,
    QConfig,
    ConfigItem,
    OptionsConfigItem,
    BoolValidator,
    OptionsValidator,
    Theme,
)


def isWin11():
    """检查是否为Windows 11系统
    
    Returns:
        bool: 如果是Windows 11系统则返回True，否则返回False
    """
    return sys.platform == "win32" and sys.getwindowsversion().build >= 22000

class AppConfig(QConfig):
    """应用程序配置类
    
    管理应用程序的所有配置项，包括主题设置、语言设置等。
    """

    # 文件
    # musicFolders = ConfigItem("Folders", "LocalMusic", [], FolderListValidator())
    # downloadFolder = ConfigItem("Folders", "Download", "app/download", FolderValidator())

    # 主窗口
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())
    dpiScale = OptionsConfigItem("MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)

    def __init__(self):
        """初始化应用程序配置"""
        super().__init__()

YEAR = datetime.datetime.now().year
AUTHOR = "ZhoSolune"
VERSION = "1.0.0"
COPYRIGHT = f"© {YEAR} {AUTHOR}"
HELP_URL = ""


# 全局配置实例
_app_cfg = AppConfig()
# 默认主题：跟随系统
_app_cfg.themeMode.value = Theme.AUTO
# 导入配置文件
qconfig.load("/RadarIdentifySystem_Refactoring/app/config/config.json", _app_cfg)