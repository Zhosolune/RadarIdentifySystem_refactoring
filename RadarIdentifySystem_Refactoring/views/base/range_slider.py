# coding:utf-8
from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QRectF, QPropertyAnimation, pyqtProperty
from PyQt6.QtGui import QColor, QPainter, QMouseEvent
from PyQt6.QtWidgets import QWidget

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from qfluentwidgets.common.style_sheet import themeColor, isDarkTheme


class ColorUtils:
    @staticmethod
    def fallbackThemeColor(color: QColor):
        return color if color.isValid() else themeColor()


    @staticmethod
    def autoFallbackThemeColor(light: QColor, dark: QColor):
        color = dark if isDarkTheme() else light
        return ColorUtils.fallbackThemeColor(color)


class RangeSliderHandle(QWidget):
    """双向滑块的句柄组件"""

    pressed = pyqtSignal()
    released = pyqtSignal()

    def __init__(self, parent: QWidget, handle_type: str = "min"):
        """
        初始化句柄
        
        Parameters
        ----------
        parent : QWidget
            父组件
        handle_type : str
            句柄类型，"min" 或 "max"
        """
        super().__init__(parent=parent)
        self.setFixedSize(22, 22)
        self._radius = 5
        self.handle_type = handle_type
        self.lightHandleColor = QColor()
        self.darkHandleColor = QColor()
        self.radiusAni = QPropertyAnimation(self, b'radius', self)
        self.radiusAni.setDuration(100)

    @pyqtProperty(int)
    def radius(self) -> int:
        """获取句柄半径"""
        return self._radius

    @radius.setter
    def radius(self, r: int) -> None:
        """设置句柄半径"""
        self._radius = r
        self.update()

    def setHandleColor(self, light: QColor, dark: QColor) -> None:
        """
        设置句柄颜色
        
        Parameters
        ----------
        light : QColor
            浅色主题颜色
        dark : QColor
            深色主题颜色
        """
        self.lightHandleColor = QColor(light)
        self.darkHandleColor = QColor(dark)
        self.update()

    def enterEvent(self, e) -> None:
        """鼠标进入事件"""
        self._startAni(6)

    def leaveEvent(self, e) -> None:
        """鼠标离开事件"""
        self._startAni(5)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        """鼠标按下事件"""
        self._startAni(4)
        self.pressed.emit()

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        """鼠标释放事件"""
        self._startAni(6)
        self.released.emit()

    def _startAni(self, radius: int) -> None:
        """启动半径动画"""
        self.radiusAni.stop()
        self.radiusAni.setStartValue(self.radius)
        self.radiusAni.setEndValue(radius)
        self.radiusAni.start()

    def paintEvent(self, e) -> None:
        """绘制句柄"""
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        # 绘制外圆
        isDark = isDarkTheme()
        painter.setPen(QColor(0, 0, 0, 90 if isDark else 25))
        painter.setBrush(QColor(69, 69, 69) if isDark else Qt.GlobalColor.white)
        painter.drawEllipse(self.rect().adjusted(1, 1, -1, -1))

        # 绘制内圆
        painter.setBrush(ColorUtils.autoFallbackThemeColor(self.lightHandleColor, self.darkHandleColor))
        painter.drawEllipse(QPoint(11, 11), self.radius, self.radius)


class RangeSlider(QWidget):
    """
    双向滑块组件
    
    支持范围选择，包含最小值和最大值两个句柄
    """

    # 信号定义
    rangeChanged = pyqtSignal(int, int)  # (min_value, max_value)
    minValueChanged = pyqtSignal(int)
    maxValueChanged = pyqtSignal(int)
    sliderPressed = pyqtSignal()
    sliderReleased = pyqtSignal()

    def __init__(self, parent: QWidget = None):
        """
        初始化双向滑块
        
        Parameters
        ----------
        parent : QWidget
            父组件
        """
        super().__init__(parent)
        
        # 数值范围
        self._minimum = 0
        self._maximum = 100
        self._min_value = 20
        self._max_value = 80
        self._step = 1  # 分度值，默认为1
        
        # 句柄组件
        self.min_handle = RangeSliderHandle(self, "min")
        self.max_handle = RangeSliderHandle(self, "max")
        
        # 拖拽状态
        self._dragging_handle = None
        self._drag_start_pos = QPoint()
        self._drag_start_value = 0
        
        # 样式颜色
        self.lightGrooveColor = QColor()
        self.darkGrooveColor = QColor()
        
        # 初始化
        self._postInit()

    def _postInit(self) -> None:
        """后初始化设置"""
        self.setMinimumHeight(22)
        self.setMinimumWidth(200)
        
        # 连接信号
        self.min_handle.pressed.connect(self._onMinHandlePressed)
        self.min_handle.released.connect(self._onHandleReleased)
        self.max_handle.pressed.connect(self._onMaxHandlePressed)
        self.max_handle.released.connect(self._onHandleReleased)
        
        # 调整句柄位置
        self._adjustHandlePositions()

    def setThemeColor(self, light: QColor, dark: QColor) -> None:
        """
        设置主题颜色
        
        Parameters
        ----------
        light : QColor
            浅色主题颜色
        dark : QColor
            深色主题颜色
        """
        self.lightGrooveColor = QColor(light)
        self.darkGrooveColor = QColor(dark)
        self.min_handle.setHandleColor(light, dark)
        self.max_handle.setHandleColor(light, dark)
        self.update()

    def setRange(self, minimum: int, maximum: int) -> None:
        """
        设置滑块范围
        
        Parameters
        ----------
        minimum : int
            最小值
        maximum : int
            最大值
        """
        if minimum >= maximum:
            return
            
        self._minimum = minimum
        self._maximum = maximum
        
        # 确保当前值在有效范围内
        self._min_value = max(minimum, min(self._min_value, maximum))
        self._max_value = max(minimum, min(self._max_value, maximum))
        
        # 确保最小值不大于最大值
        if self._min_value > self._max_value:
            self._min_value = self._max_value
            
        self._adjustHandlePositions()
        self.update()

    def setMinValue(self, value: int) -> None:
        """
        设置最小值
        
        Parameters
        ----------
        value : int
            最小值
        """
        value = max(self._minimum, min(value, self._maximum))
        # 对齐到分度值
        value = self._alignToStep(value)
        
        if value > self._max_value:
            value = self._max_value
            
        if self._min_value != value:
            self._min_value = value
            self._adjustHandlePositions()
            self.minValueChanged.emit(value)
            self.rangeChanged.emit(self._min_value, self._max_value)
            self.update()

    def setMaxValue(self, value: int) -> None:
        """
        设置最大值
        
        Parameters
        ----------
        value : int
            最大值
        """
        value = max(self._minimum, min(value, self._maximum))
        # 对齐到分度值
        value = self._alignToStep(value)
        
        if value < self._min_value:
            value = self._min_value
            
        if self._max_value != value:
            self._max_value = value
            self._adjustHandlePositions()
            self.maxValueChanged.emit(value)
            self.rangeChanged.emit(self._min_value, self._max_value)
            self.update()

    def setValues(self, min_value: int, max_value: int) -> None:
        """
        同时设置最小值和最大值
        
        Parameters
        ----------
        min_value : int
            最小值
        max_value : int
            最大值
        """
        min_value = max(self._minimum, min(min_value, self._maximum))
        max_value = max(self._minimum, min(max_value, self._maximum))
        
        # 对齐到分度值
        min_value = self._alignToStep(min_value)
        max_value = self._alignToStep(max_value)
        
        if min_value > max_value:
            min_value, max_value = max_value, min_value
            
        changed = False
        if self._min_value != min_value:
            self._min_value = min_value
            self.minValueChanged.emit(min_value)
            changed = True
            
        if self._max_value != max_value:
            self._max_value = max_value
            self.maxValueChanged.emit(max_value)
            changed = True
            
        if changed:
            self._adjustHandlePositions()
            self.rangeChanged.emit(self._min_value, self._max_value)
            self.update()

    def minimum(self) -> int:
        """获取最小范围值"""
        return self._minimum

    def maximum(self) -> int:
        """获取最大范围值"""
        return self._maximum

    def minValue(self) -> int:
        """获取当前最小值"""
        return self._min_value

    def maxValue(self) -> int:
        """获取当前最大值"""
        return self._max_value

    def values(self) -> tuple:
        """获取当前值范围"""
        return (self._min_value, self._max_value)

    def step(self) -> int:
        """获取分度值"""
        return self._step

    def setStep(self, step: int) -> None:
        """
        设置分度值
        
        Parameters
        ----------
        step : int
            分度值，必须大于0
        """
        if step <= 0:
            return
        self._step = step
        
        # 重新对齐当前值到分度值
        self._min_value = self._alignToStep(self._min_value)
        self._max_value = self._alignToStep(self._max_value)
        
        self._adjustHandlePositions()
        self.rangeChanged.emit(self._min_value, self._max_value)
        self.update()

    def _alignToStep(self, value: int) -> int:
        """
        将数值对齐到分度值
        
        Parameters
        ----------
        value : int
            原始数值
            
        Returns
        -------
        int
            对齐后的数值
        """
        if self._step <= 1:
            return value
            
        # 计算相对于最小值的偏移
        offset = value - self._minimum
        # 对齐到最近的分度值
        aligned_offset = round(offset / self._step) * self._step
        aligned_value = self._minimum + aligned_offset
        
        # 确保在有效范围内
        return max(self._minimum, min(aligned_value, self._maximum))

    @property
    def grooveLength(self) -> int:
        """获取滑槽长度"""
        return self.width() - self.min_handle.width()

    def _adjustHandlePositions(self) -> None:
        """调整句柄位置"""
        if self._maximum <= self._minimum:
            return
            
        total_range = self._maximum - self._minimum
        groove_length = self.grooveLength
        
        # 计算最小值句柄位置
        min_ratio = (self._min_value - self._minimum) / total_range
        min_pos = int(min_ratio * groove_length)
        self.min_handle.move(min_pos, 0)
        
        # 计算最大值句柄位置
        max_ratio = (self._max_value - self._minimum) / total_range
        max_pos = int(max_ratio * groove_length)
        self.max_handle.move(max_pos, 0)

    def _posToValue(self, pos: int) -> int:
        """
        将位置转换为数值
        
        Parameters
        ----------
        pos : int
            位置
            
        Returns
        -------
        int
            对应的数值（已对齐到分度值）
        """
        handle_radius = self.min_handle.width() / 2
        groove_length = max(self.grooveLength, 1)
        ratio = (pos - handle_radius) / groove_length
        value = int(ratio * (self._maximum - self._minimum) + self._minimum)
        
        # 限制在有效范围内
        value = max(self._minimum, min(value, self._maximum))
        
        # 对齐到分度值
        return self._alignToStep(value)

    def _getHandleAtPos(self, pos: QPoint) -> RangeSliderHandle:
        """
        获取指定位置的句柄
        
        Parameters
        ----------
        pos : QPoint
            位置
            
        Returns
        -------
        RangeSliderHandle
            句柄对象，如果没有则返回None
        """
        # 检查最大值句柄（优先级更高，因为通常在右侧）
        if self.max_handle.geometry().contains(pos):
            return self.max_handle
        elif self.min_handle.geometry().contains(pos):
            return self.min_handle
        return None

    def _onMinHandlePressed(self) -> None:
        """最小值句柄按下事件"""
        self._dragging_handle = self.min_handle
        self.sliderPressed.emit()

    def _onMaxHandlePressed(self) -> None:
        """最大值句柄按下事件"""
        self._dragging_handle = self.max_handle
        self.sliderPressed.emit()

    def _onHandleReleased(self) -> None:
        """句柄释放事件"""
        self._dragging_handle = None
        self.sliderReleased.emit()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        """鼠标按下事件"""
        if e.button() != Qt.MouseButton.LeftButton:
            return
            
        # 检查是否点击在句柄上
        handle = self._getHandleAtPos(e.pos())
        if handle:
            self._dragging_handle = handle
            self._drag_start_pos = e.pos()
            if handle == self.min_handle:
                self._drag_start_value = self._min_value
                self._onMinHandlePressed()
            else:
                self._drag_start_value = self._max_value
                self._onMaxHandlePressed()
        else:
            # 点击在滑槽上，移动最近的句柄
            click_value = self._posToValue(e.pos().x())
            min_distance = abs(click_value - self._min_value)
            max_distance = abs(click_value - self._max_value)
            
            if min_distance <= max_distance:
                self.setMinValue(click_value)
            else:
                self.setMaxValue(click_value)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        """鼠标移动事件"""
        if self._dragging_handle is None:
            return
            
        new_value = self._posToValue(e.pos().x())
        
        if self._dragging_handle == self.min_handle:
            self.setMinValue(new_value)
        else:
            self.setMaxValue(new_value)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        """鼠标释放事件"""
        if self._dragging_handle:
            self._onHandleReleased()

    def paintEvent(self, e) -> None:
        """绘制滑块"""
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        
        self._drawGroove(painter)

    def _drawGroove(self, painter: QPainter) -> None:
        """绘制滑槽"""
        w, r = self.width(), self.min_handle.width() / 2
        
        # 绘制背景滑槽
        painter.setBrush(QColor(255, 255, 255, 115) if isDarkTheme() else QColor(0, 0, 0, 100))
        painter.drawRoundedRect(QRectF(r, r-2, w-r*2, 4), 2, 2)

        if self._maximum <= self._minimum:
            return

        # 绘制选中范围
        painter.setBrush(ColorUtils.autoFallbackThemeColor(self.lightGrooveColor, self.darkGrooveColor))
        
        total_range = self._maximum - self._minimum
        groove_width = w - r*2
        
        # 计算选中区域的起始和结束位置
        start_ratio = (self._min_value - self._minimum) / total_range
        end_ratio = (self._max_value - self._minimum) / total_range
        
        start_x = r + start_ratio * groove_width
        end_x = r + end_ratio * groove_width
        
        painter.drawRoundedRect(QRectF(start_x, r-2, end_x - start_x, 4), 2, 2)

    def resizeEvent(self, e) -> None:
        """窗口大小改变事件"""
        self._adjustHandlePositions()
        super().resizeEvent(e)