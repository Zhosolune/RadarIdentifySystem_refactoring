# coding: utf-8
from enum import Enum
import os
from qfluentwidgets import StyleSheetBase, Theme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    MAIN_INTERFACE = "main_interface"
    SETTING_INTERFACE = "setting_interface"
    PARAMS_CONFIG_INTERFACE = "params_config_interface"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        # 获取项目根目录的绝对路径
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(project_root, "resources", "qss", theme.value.lower(), f"{self.value}.qss")
