from typing import Union, Optional
from qfluentwidgets import (
    IconWidget, BodyLabel, CaptionLabel, RadioButton, FluentIcon
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QEnterEvent, QMouseEvent, QIcon
from models.utils.log_manager import LoggerMixin


class OptionsWithIcon(QWidget, LoggerMixin):
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
    
    def __init__(
        self, 
        icon: Union[str, QIcon, FluentIcon], 
        title: str, 
        content: str, 
        direction: str = "vertical", 
        parent: Optional[QWidget] = None
    ) -> None:
        """
        初始化带图标的选项组件
        
        Args:
            icon: 图标，可以是字符串路径、QIcon对象或FluentIcon枚举
            title: 选项标题文本
            content: 选项描述内容文本
            direction: 方向标识符，默认为"vertical"，用于配置项识别
            parent: 父组件，默认为None
            
        Returns:
            None
        """
        super().__init__(parent)
        
        # 初始化UI组件
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.radioButton = RadioButton(self)
        self.direction = direction

        # 初始化布局管理器
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        # 设置图标大小为16x16像素
        self.iconWidget.setFixedSize(16, 16)
        
        # 设置描述文本颜色（浅色主题和深色主题）
        self.contentLabel.setTextColor("#606060", "#d2d2d2")

        # 配置水平布局：无边距，组件间距16像素
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setSpacing(16)

        # 添加图标到水平布局的最左侧
        self.hBoxLayout.addWidget(self.iconWidget)

        # 配置垂直布局
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # 将垂直布局添加到水平布局中
        self.hBoxLayout.addLayout(self.vBoxLayout)
        # 添加弹性空间，将单选按钮推到右侧
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.radioButton, 0, Qt.AlignmentFlag.AlignRight)
        
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
        enter_event = QEnterEvent(
            event.position(), 
            event.globalPosition(), 
            event.globalPosition()
        )
        self.radioButton.enterEvent(enter_event)

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
        self.radioButton.leaveEvent(event)

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
            if not self.radioButton.isChecked():
                self.radioButton.click()

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

