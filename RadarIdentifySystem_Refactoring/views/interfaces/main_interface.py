from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from qfluentwidgets import ScrollArea
from typing import Optional
from models.theme.style_sheet import StyleSheet
from models.utils.log_manager import LoggerMixin
from models.ui.dimensions import UIDimensions


class MainInterface(QWidget, LoggerMixin):
    """主界面
    
    雷达信号分析的主界面，包含左右两个滚动区域。
    布局结构：
    - 左侧：水平滚动区域
    - 右侧：垂直滚动区域（宽度为界面宽度减40px后的1/3，最大500px）
    """
    
    def __init__(self, text: str, parent: Optional[QWidget] = None) -> None:    
        """初始化主界面
        
        Args:
            text: 界面文本（保持兼容性）
            parent: 父控件
        """
        super().__init__(parent)
        self.setObjectName("MainInterface")
        
        # 创建子组件
        self.left_scroll_area = None
        self.right_scroll_area = None
        StyleSheet.MAIN_INTERFACE.apply(self)
        
        # 设置UI
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        """设置用户界面"""
        # 创建主布局，设置内边距：10px
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(
            UIDimensions.PADDING_MEDIUM, 
            UIDimensions.PADDING_MEDIUM, 
            UIDimensions.PADDING_MEDIUM, 
            UIDimensions.PADDING_MEDIUM
        )
        main_layout.setSpacing(UIDimensions.SPACING_MEDIUM)  # 左右滚动区域间隔
        
        # 创建左侧水平滚动区域
        self.left_scroll_area = ScrollArea()
        self.left_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.left_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        border_style = f"ScrollArea {{ border: {UIDimensions.BORDER_WIDTH_THIN}px solid #CCCCCC; }}"
        self.left_scroll_area.setStyleSheet(border_style)
        
        # 创建右侧垂直滚动区域
        self.right_scroll_area = ScrollArea()
        self.right_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.right_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.right_scroll_area.setStyleSheet(border_style)
        
        # 添加滚动区域到主布局
        main_layout.addWidget(self.left_scroll_area, stretch=2)  # 左侧占更大比例
        main_layout.addWidget(self.right_scroll_area, stretch=1)  # 右侧占较小比例
        
    def resizeEvent(self, event) -> None:
        """重写窗口大小变化事件，动态调整右侧滚动区域宽度
        
        Args:
            event: 窗口大小变化事件
        """
        super().resizeEvent(event)
        
        # 计算右侧滚动区域宽度
        padding_and_spacing = UIDimensions.PADDING_MEDIUM * 2 + UIDimensions.SPACING_MEDIUM * 2
        right_width = UIDimensions.get_right_panel_width(
            total_width=self.width(), 
            padding=padding_and_spacing
        )
        
        # 设置右侧滚动区域的最大宽度
        self.right_scroll_area.setMaximumWidth(right_width)
        
    def get_left_scroll_area(self) -> ScrollArea:
        """获取左侧滚动区域
        
        Returns:
            左侧滚动区域实例
        """
        return self.left_scroll_area
        
    def get_right_scroll_area(self) -> ScrollArea:
        """获取右侧滚动区域
        
        Returns:
            右侧滚动区域实例
        """
        return self.right_scroll_area