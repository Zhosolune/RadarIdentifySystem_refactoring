from typing import Union
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QButtonGroup, QLabel, QWidget, QHBoxLayout

from qfluentwidgets import (
    FluentIcon as FIF,
    ExpandGroupSettingCard,
)
from views.components.item_card import AppCard

class ExpandGroupSettingCard1(ExpandGroupSettingCard):
    """Expand group setting card"""

    def __init__(self, icon: Union[str, QIcon, FIF], title: str, content: str = None, parent=None):
        super().__init__(icon, "数据方向", "样本脉冲排列的方向", parent)
        self.choiceLabel = QLabel(self)
        self.buttonGroup = QButtonGroup(self)

        self.choiceLabel.setObjectName("titleLabel")
        self.addWidget(self.choiceLabel)

        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.setSpacing(0)

        self._setup_ui()

    def _setup_ui(self):

        # 第一组
        self.horizontalIcon = FIF.ACCEPT
        self.horizontalIcon = "水平方向"
        self.horizontalContent = "样本脉冲横向排列"

        # 第二组
        self.verticalIcon = FIF.ACCEPT
        self.verticalText = "垂直方向"
        self.verticalContent = "样本脉冲纵向排列"

        # 添加各组到设置卡中
        self.add(self.horizontalIcon, self.horizontalText, self.horizontalContent)
        self.add(self.verticalIcon, self.verticalText, self.verticalContent)

    def add(self, icon: Union[str, QIcon, FIF], title: str, content: str = None):
        w = AppCard(icon, title, content)
        w.setFixedHeight(60)
        # layout.setContentsMargins(48, 12, 48, 12)

        # 添加组件到设置卡
        self.addGroupWidget(w)



