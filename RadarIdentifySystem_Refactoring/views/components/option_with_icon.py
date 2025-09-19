from qfluentwidgets import (
    IconWidget, BodyLabel, CaptionLabel, RadioButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QEnterEvent, QMouseEvent
from models.utils.log_manager import LoggerMixin


class OptionsWithIcon(QWidget, LoggerMixin):
    """带图标的选项组件，支持悬浮和点击效果"""
    
    def __init__(self, icon, title, content, direction="vertical", parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.radioButton = RadioButton(self)
        self.direction = direction

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.iconWidget.setFixedSize(16, 16)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setSpacing(16)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.radioButton, 0, Qt.AlignmentFlag.AlignRight)
        
        # 设置鼠标跟踪以启用悬浮效果
        self.setMouseTracking(True)

    def enterEvent(self, event: QEnterEvent):
        """鼠标进入事件 - 触发RadioButton的悬浮效果"""
        super().enterEvent(event)
        # 模拟鼠标进入RadioButton
        enter_event = QEnterEvent(event.position(), event.globalPosition(), event.globalPosition())
        self.radioButton.enterEvent(enter_event)

    def leaveEvent(self, event):
        """鼠标离开事件 - 取消RadioButton的悬浮效果"""
        super().leaveEvent(event)
        # 模拟鼠标离开RadioButton
        self.radioButton.leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件 - 点击卡片等同于点击RadioButton"""
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            # 如果RadioButton未选中，则选中它
            if not self.radioButton.isChecked():
                self.radioButton.setChecked(True)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件"""
        super().mouseReleaseEvent(event)

