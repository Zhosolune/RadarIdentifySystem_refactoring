import os
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

YEAR = datetime.datetime.now().year
AUTHOR = "ZhoSolune"
VERSION = "1.0.0"
COPYRIGHT = f"© {YEAR} {AUTHOR}"
HELP_URL = ""

class Config(QConfig):
    """应用程序配置类

    管理应用程序的所有需要使用ConfigItem的配置项。
    """

    # 文件
    # musicFolders = ConfigItem("Folders", "LocalMusic", [], FolderListValidator())
    # downloadFolder = ConfigItem("Folders", "Download", "app/download", FolderValidator())

    # 主窗口
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())
    dpiScale = OptionsConfigItem("MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]))
    logLevel = OptionsConfigItem("MainWindow", "logLevel", "INFO", OptionsValidator(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]))

    # 导入设置
    importFileFormat = OptionsConfigItem("Import", "FileFormat", "Excel", OptionsValidator(["CSV", "Excel", "TXT", "MAT"]))
    dataDirection = OptionsConfigItem("Import", "DataDirection", "列", OptionsValidator(["行", "列"]))

    def __init__(self):
        """初始化应用程序配置"""
        super().__init__()


# 全局配置实例
cfg = Config()
# 默认主题：跟随系统
cfg.themeMode.value = Theme.AUTO
# 导入配置文件
# 获取项目根目录的绝对路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
qconfig.load(os.path.join(project_root, "app/config/app_config/config.json"), cfg)
