# coding: utf-8
import os
from enum import Enum
from tkinter import HORIZONTAL

from qfluentwidgets import FluentIconBase, getIconColor, Theme


class Icon(FluentIconBase, Enum):

    PARAMS_CONFIG = "ParamsConfig"
    IMPORT_FILE = "ImportFile"
    DATA_DIRECTION = "DataDirection"
    HORIZONTAL = "Horizontal"
    VERTICAL = "Vertical"
    IGNORE_FIRST_LINE = "IgnoreFirstLine"

    def path(self, theme=Theme.AUTO):
        # 获取项目根目录的绝对路径
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(project_root, "resources", "icons", f"{self.value}_{getIconColor(theme)}.svg")
