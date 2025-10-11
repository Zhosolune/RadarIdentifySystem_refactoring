from typing import Optional
from qfluentwidgets import BodyLabel, CaptionLabel
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtGui import QEnterEvent, QMouseEvent
from models.utils.log_manager import LoggerMixin


class SubTitle(QWidget, LoggerMixin):
    """
    带图标的选项组件，支持悬浮和点击效果

    这是一个自定义的选项卡片组件，包含图标、标题、描述文本和单选按钮。
    支持鼠标悬浮效果和点击整个卡片来选中选项的功能。

    Attributes:
        iconWidget (IconWidget): 显示图标的组件
        titleLabel (BodyLabel): 显示标题的标签
        contentLabel (CaptionLabel): 显示描述内容的标签
        radioButton (RadioButton): 单选按钮组件
        direction (str): 方向标识符，用于配置项识别
        hBoxLayout (QHBoxLayout): 水平布局管理器
        vBoxLayout (QVBoxLayout): 垂直布局管理器
    """

    def __init__(self, title: str, subtitle: str, baseButton: QWidget, parent: Optional[QWidget] = None) -> QWidget:
        """
        初始化带图标的选项组件

        Args:
            title: 选项标题文本
            subtitle: 选项描述内容文本
            baseButton: 基组件，用于传递事件，大多为单选按钮
            parent: 父组件，默认为None

        Returns:
            None
        """
        super().__init__(parent)

        # 初始化UI组件
        self.titleLabel = BodyLabel(title, self)
        self.subtitleLabel = CaptionLabel(subtitle, self)
        self.subtitleLabel.setTextColor("#606060", "#d2d2d2")  # 设置描述文本颜色（浅色主题和深色主题）
        self.subtitleLabel.pixelFontSize = 11
        self.baseButton = baseButton

        # 初始化布局管理器
        self.vBoxLayout = QVBoxLayout(self)

        # 配置垂直布局
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.addWidget(self.subtitleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # 启用鼠标跟踪以支持悬浮效果
        self.setMouseTracking(True)

    def enterEvent(self, event: QEnterEvent) -> None:
        """
        鼠标进入事件处理器 - 触发RadioButton的悬浮效果

        当鼠标进入整个卡片区域时，模拟鼠标进入RadioButton，
        使RadioButton显示悬浮状态的视觉效果。

        Args:
            event: 鼠标进入事件对象，包含鼠标位置信息

        Returns:
            None
        """
        super().enterEvent(event)
        # 创建新的鼠标进入事件并传递给RadioButton
        enter_event = QEnterEvent(event.position(), event.globalPosition(), event.globalPosition())
        self.baseButton.enterEvent(enter_event)

    def leaveEvent(self, event) -> None:
        """
        鼠标离开事件处理器 - 取消RadioButton的悬浮效果

        当鼠标离开整个卡片区域时，模拟鼠标离开RadioButton，
        使RadioButton恢复正常状态的视觉效果。

        Args:
            event: 鼠标离开事件对象

        Returns:
            None
        """
        super().leaveEvent(event)
        # 将鼠标离开事件传递给RadioButton
        self.baseButton.leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        鼠标按下事件处理器 - 点击卡片等同于点击RadioButton

        当用户点击卡片的任意区域时，如果RadioButton未被选中，
        则自动选中该RadioButton，提供更好的用户体验。

        Args:
            event: 鼠标按下事件对象，包含按键信息和位置信息

        Returns:
            None
        """
        super().mousePressEvent(event)
        # 只处理鼠标左键点击
        if event.button() == Qt.MouseButton.LeftButton:
            # 如果RadioButton当前未选中，则模拟点击选中它
            if not self.baseButton.isChecked():
                self.baseButton.click()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        鼠标释放事件处理器

        处理鼠标按键释放事件，目前仅调用父类方法保持事件传递链完整。

        Args:
            event: 鼠标释放事件对象，包含按键信息和位置信息

        Returns:
            None
        """
        super().mouseReleaseEvent(event)
