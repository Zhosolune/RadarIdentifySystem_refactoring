from typing import Union
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QButtonGroup, QLabel, QWidget, QVBoxLayout

from qfluentwidgets import (
    FluentIcon as FIF,
    ExpandGroupSettingCard,
)
from views.components.option_with_icon import OptionsWithIcon
from models.utils.icons_manager import Icon

class OptionsWithIconCard(ExpandGroupSettingCard):
    """Expand group setting card"""

    # 默认垂直方向，样本竖向排列
    _dataDirection: str = "vertical"
    dataDirectionChanged = pyqtSignal(str)

    def __init__(self, icon: Union[str, QIcon, FIF], title: str, content: str = None, parent=None):
        super().__init__(icon, "数据方向", "样本脉冲排列的方向", parent)
        self.choiceLabel = QLabel(self)
        self.buttonGroup = QButtonGroup(self)

        self.choiceLabel.setObjectName("titleLabel")
        self.addWidget(self.choiceLabel)

        self._setup_ui()

    def _setup_ui(self):
        """
        初始化UI组件
        """

        # 第一组
        self.horizontalIcon = Icon.HORIZONTAL
        self.horizontalText = "水平方向"
        self.horizontalContent = "样本脉冲横向排列"

        # 第二组
        self.verticalIcon = Icon.VERTICAL
        self.verticalText = "垂直方向"
        self.verticalContent = "样本脉冲纵向排列"

        # 添加各组到设置卡中
        horizontalCard = OptionsWithIcon(self.horizontalIcon, self.horizontalText, self.horizontalContent, direction="horizontal")
        verticalCard = OptionsWithIcon(self.verticalIcon, self.verticalText, self.verticalContent, direction="vertical")

        # 添加单选按钮到互斥按钮组
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.addButton(horizontalCard.radioButton)
        self.buttonGroup.addButton(verticalCard.radioButton)

        # 默认选中垂直方向
        # TODO: 从配置中获取数据方向
        verticalCard.radioButton.setChecked(True)
        self.choiceLabel.setText(verticalCard.titleLabel.text())

        # 连接信号槽
        self.buttonGroup.buttonToggled.connect(self._on_data_direction_changed)

        w = QWidget()

        layout = QVBoxLayout(w)
        layout.setSpacing(19)
        layout.setContentsMargins(48, 18, 48, 18)
        layout.addWidget(horizontalCard)
        layout.addWidget(verticalCard)

        self.addGroupWidget(w)

    def _on_data_direction_changed(self, button):
        """
        处理数据方向切换信号槽

        Args:
            button (QRadioButton): 被点击的单选按钮
        """

        if button.isChecked():
            self._dataDirection = button.parent().direction
            self.dataDirectionChanged.emit(self._dataDirection)
            self.choiceLabel.setText(button.parent().titleLabel.text())

