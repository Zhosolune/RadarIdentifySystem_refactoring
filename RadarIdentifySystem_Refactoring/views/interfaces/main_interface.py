from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSplitter
from PyQt6.QtCore import Qt
from typing import Optional

from views.modules.scroll_module.scroll_container import ScrollContainer
from views.modules.panel_module.parameter_panel import ParameterPanel
from views.modules.panel_module.slice_panel import SlicePanel
from views.modules.panel_module.cluster_panel import ClusterPanel


class MainInterface(QWidget):
    """主界面
    
    雷达信号分析的主界面，包含滚动窗口和三个控制面板。
    布局结构：
    - 左侧：滚动窗口（包含切片、聚类、合并、额外视图）
    - 右侧：参数面板、切片面板、聚类面板（垂直排列）
    """
    
    def __init__(self, text: str, parent: Optional[QWidget] = None) -> None:    
        """初始化主界面
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        
        # 创建子组件
        self.scroll_container = None
        self.parameter_panel = None
        self.slice_panel = None
        self.cluster_panel = None
        self.setObjectName(text.replace(" ", "-"))
        
        # 设置UI
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        """设置用户界面"""
        # 创建主布局
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 创建滚动容器
        self.scroll_container = ScrollContainer()
        
        # 创建面板容器
        panel_widget = QWidget()
        panel_layout = QVBoxLayout(panel_widget)
        panel_layout.setContentsMargins(10, 10, 10, 10)
        panel_layout.setSpacing(10)
        
        # 创建三个面板
        self.parameter_panel = ParameterPanel()
        self.slice_panel = SlicePanel()
        self.cluster_panel = ClusterPanel()
        
        # 添加面板到布局
        panel_layout.addWidget(self.parameter_panel, stretch=1)
        panel_layout.addWidget(self.slice_panel, stretch=1)
        panel_layout.addWidget(self.cluster_panel, stretch=1)
        
        # 添加组件到分割器
        splitter.addWidget(self.scroll_container)
        splitter.addWidget(panel_widget)
        
        # 设置分割器比例（左侧占3/4，右侧占1/4）
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        
        # 添加分割器到主布局
        main_layout.addWidget(splitter)
        
    def get_scroll_container(self) -> ScrollContainer:
        """获取滚动容器
        
        Returns:
            滚动容器实例
        """
        return self.scroll_container
        
    def get_parameter_panel(self) -> ParameterPanel:
        """获取参数面板
        
        Returns:
            参数面板实例
        """
        return self.parameter_panel
        
    def get_slice_panel(self) -> SlicePanel:
        """获取切片面板
        
        Returns:
            切片面板实例
        """
        return self.slice_panel
        
    def get_cluster_panel(self) -> ClusterPanel:
        """获取聚类面板
        
        Returns:
            聚类面板实例
        """
        return self.cluster_panel