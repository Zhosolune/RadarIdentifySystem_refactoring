from PyQt6.QtWidgets import QWidget, QHBoxLayout, QScrollArea, QVBoxLayout
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QTimer
from PyQt6.QtGui import QResizeEvent, QWheelEvent
from typing import Optional, List
import logging


class ScrollContainer(QWidget):
    """横向滚动容器
    
    用于容纳四个子视图的横向滚动容器，支持1:1:1:1的等比例布局。
    支持动画滚动到指定位置。
    """
    
    # 滚动完成信号
    scrollFinished = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        """初始化横向滚动容器

        Args:
            parent: 父控件
        """
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)

        # 初始化属性
        self.scroll_enabled = False  # 滚动功能默认禁用
        self.animation: Optional[QPropertyAnimation] = None

        # 锚点相关属性
        self.anchor_points: List[int] = []  # 锚点位置列表
        self.anchor_threshold = 50  # 锚点吸附阈值（像素）
        self.snap_timer: Optional[QTimer] = None  # 延迟吸附定时器

        # 存储子控件引用
        self.slice_widget: Optional[QWidget] = None
        self.cluster_widget: Optional[QWidget] = None
        self.merge_widget: Optional[QWidget] = None
        self.extra_widget: Optional[QWidget] = None
        
        # 设置UI
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        """设置用户界面"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        
        # 设置滚动区域样式
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        # 创建内容容器
        self.content_widget = QWidget()
        self.content_layout = QHBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(10)
        
        # 设置滚动区域的内容
        self.scroll_area.setWidget(self.content_widget)
        
        # 添加到主布局
        main_layout.addWidget(self.scroll_area)

    def add_widgets(self, slice_widget: QWidget, cluster_widget: QWidget, 
                   merge_widget: QWidget, extra_widget: QWidget) -> None:
        """添加四个子控件到容器中
        
        Args:
            slice_widget: 切片视图控件
            cluster_widget: 聚类视图控件
            merge_widget: 合并视图控件
            extra_widget: 额外视图控件
        """
        # 清除现有控件
        self._clear_layout()
        
        # 存储控件引用
        self.slice_widget = slice_widget
        self.cluster_widget = cluster_widget
        self.merge_widget = merge_widget
        self.extra_widget = extra_widget
        
        # 添加控件到布局
        self.content_layout.addWidget(slice_widget)
        self.content_layout.addWidget(cluster_widget)
        self.content_layout.addWidget(merge_widget)
        self.content_layout.addWidget(extra_widget)
        
        # 更新控件尺寸
        self._update_widget_sizes()
        
    def _clear_layout(self) -> None:
        """清除布局中的所有控件"""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
                
    def _update_widget_sizes(self) -> None:
        """更新控件尺寸，保持1:1:1:1的比例"""
        if not all([self.slice_widget, self.cluster_widget, 
                   self.merge_widget, self.extra_widget]):
            return
            
        # 计算可用宽度
        available_width = self.width() - 30  # 30px间距（3个10px间距）
        
        # 按1:1:1:1比例分配宽度
        unit_width = available_width // 4
        
        # 设置控件宽度
        self.slice_widget.setFixedWidth(unit_width)
        self.cluster_widget.setFixedWidth(unit_width)
        self.merge_widget.setFixedWidth(unit_width)
        self.extra_widget.setFixedWidth(unit_width)
        
        # 更新内容容器的总宽度
        total_width = unit_width * 4 + 30  # 加上间距
        self.content_widget.setFixedWidth(total_width)
        
        # 更新锚点位置
        self._update_anchor_points()
        
    def _update_anchor_points(self) -> None:
        """更新锚点位置列表"""
        self.anchor_points.clear()
        
        if not all([self.slice_widget, self.cluster_widget, 
                   self.merge_widget, self.extra_widget]):
            return
            
        # 第一个锚点：初始位置（显示slice和cluster）
        self.anchor_points.append(0)
        
        # 第二个锚点：显示cluster和merge
        anchor1 = self.slice_widget.width() + 10  # slice宽度 + 间距
        self.anchor_points.append(anchor1)
        
        # 第三个锚点：显示merge和extra
        anchor2 = anchor1 + self.cluster_widget.width() + 10  # 加上cluster宽度和间距
        self.anchor_points.append(anchor2)

    def _find_nearest_anchor(self, position: int) -> int | None:
        """查找最近的锚点
        
        Args:
            position: 当前滚动位置
            
        Returns:
            最近的锚点位置，如果没有在阈值范围内的锚点则返回None
        """
        if not self.anchor_points:
            return None
            
        nearest_anchor = None
        min_distance = float('inf')
        
        for anchor in self.anchor_points:
            distance = abs(position - anchor)
            if distance < self.anchor_threshold and distance < min_distance:
                min_distance = distance
                nearest_anchor = anchor
                
        return nearest_anchor
        
    def _snap_to_anchor(self, anchor_position: int, duration: int = 300) -> None:
        """吸附到指定锚点
        
        Args:
            anchor_position: 锚点位置
            duration: 动画持续时间（毫秒）
        """
        if self.animation:
            self.animation.stop()
            
        self.animation = QPropertyAnimation(self.scroll_area.horizontalScrollBar(), b"value")
        self.animation.setDuration(duration)
        self.animation.setStartValue(self.scroll_area.horizontalScrollBar().value())
        self.animation.setEndValue(anchor_position)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
        
    def enable_scroll(self, enabled: bool = True) -> None:
        """启用或禁用滚动功能
        
        Args:
            enabled: 是否启用滚动
        """
        self.scroll_enabled = enabled
        
        # 始终隐藏滚动条，通过鼠标滚轮进行滚动
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        if not enabled:
            # 禁用滚动时，回到初始位置
            self.scroll_area.horizontalScrollBar().setValue(0)
            
    def scroll_to_position(self, position: int, duration: int = 800) -> None:
        """滚动到指定位置
        
        Args:
            position: 目标位置
            duration: 动画持续时间（毫秒）
        """
        if not self.scroll_enabled:
            return
            
        # 创建滚动动画
        if self.animation:
            self.animation.stop()
            
        self.animation = QPropertyAnimation(self.scroll_area.horizontalScrollBar(), b"value")
        self.animation.setDuration(duration)
        self.animation.setStartValue(self.scroll_area.horizontalScrollBar().value())
        self.animation.setEndValue(position)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.finished.connect(self.scrollFinished.emit)
        self.animation.start()
        
    def scroll_to_view(self, view_index: int, duration: int = 800) -> None:
        """滚动到指定视图
        
        Args:
            view_index: 视图索引（0-3）
            duration: 动画持续时间（毫秒）
        """
        if not self.scroll_enabled or view_index < 0 or view_index >= len(self.anchor_points):
            return
            
        target_position = self.anchor_points[view_index]
        self.scroll_to_position(target_position, duration)
        
    def get_current_view_index(self) -> int:
        """获取当前视图索引
        
        Returns:
            当前视图索引（0-3）
        """
        if not self.scroll_enabled:
            return 0
            
        current_pos = self.scroll_area.horizontalScrollBar().value()
        
        # 找到最近的锚点
        nearest_index = 0
        min_distance = float('inf')
        
        for i, anchor in enumerate(self.anchor_points):
            distance = abs(current_pos - anchor)
            if distance < min_distance:
                min_distance = distance
                nearest_index = i
                
        return nearest_index
    
    def wheelEvent(self, event: QWheelEvent) -> None:
        """处理鼠标滚轮事件

        Args:
            event: 滚轮事件
        """
        if not self.scroll_enabled:
            return
            
        # 停止当前的吸附动画
        if self.animation and self.animation.state() == QPropertyAnimation.State.Running:
            self.animation.stop()
            
        # 获取滚轮滚动的角度
        angle_delta = event.angleDelta().y()
        
        # 计算滚动步长（每次滚动90像素）
        scroll_step = 90
        
        # 获取当前滚动位置
        current_value = self.scroll_area.horizontalScrollBar().value()
        
        # 计算新的滚动位置
        if angle_delta > 0:  # 向上滚动，向左移动
            new_value = max(0, current_value - scroll_step)
        else:  # 向下滚动，向右移动
            max_value = self.scroll_area.horizontalScrollBar().maximum()
            new_value = min(max_value, current_value + scroll_step)
        
        # 设置新的滚动位置
        self.scroll_area.horizontalScrollBar().setValue(new_value)
        
        # 重置吸附定时器
        self._reset_snap_timer()
        
        # 接受事件，防止传递给父控件
        event.accept()
        
    def _reset_snap_timer(self) -> None:
        """重置锚点吸附定时器"""
        if self.snap_timer:
            self.snap_timer.stop()
            
        self.snap_timer = QTimer()
        self.snap_timer.setSingleShot(True)
        self.snap_timer.timeout.connect(self._check_and_snap_to_anchor)
        self.snap_timer.start(500)  # 500毫秒后检查是否需要吸附
        
    def _check_and_snap_to_anchor(self) -> None:
        """检查当前位置并吸附到最近的锚点"""
        current_position = self.scroll_area.horizontalScrollBar().value()
        nearest_anchor = self._find_nearest_anchor(current_position)

        if nearest_anchor is not None:
            self._snap_to_anchor(nearest_anchor)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """窗口大小改变事件

        Args:
            event: 大小改变事件
        """
        super().resizeEvent(event)
        self._update_widget_sizes()