# coding:utf-8
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QWidget

from qfluentwidgets import Slider
from models.base import singledispatchmethod


class StepSlider(Slider):
    """
    带步长功能的滑块组件
    
    继承自Slider，添加了步长设置功能，使滑块每次移动都按照指定的步长对齐
    
    Constructors
    ------------
    * StepSlider(`parent`: QWidget = None)
    * StepSlider(`orient`: Qt.Orientation, `parent`: QWidget = None)
    """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        """
        初始化带步长功能的滑块
        
        Parameters
        ----------
        parent : QWidget
            父组件
        """
        super().__init__(parent)
        self._step = 1  # 默认步长为1
        self._postStepInit()

    @__init__.register
    def _(self, orientation: Qt.Orientation, parent: QWidget = None):
        """
        初始化带步长功能的滑块
        
        Parameters
        ----------
        orientation : Qt.Orientation
            滑块方向
        parent : QWidget
            父组件
        """
        super().__init__(orientation, parent)
        self._step = 1  # 默认步长为1
        self._postStepInit()

    def _postStepInit(self) -> None:
        """
        步长功能的后初始化
        """
        # 确保初始值对齐到步长
        self.setValue(self._alignToStep(self.value()))

    def step(self) -> int:
        """
        获取当前步长
        
        Returns
        -------
        int
            当前步长值
        """
        return self._step

    def setStep(self, step: int) -> None:
        """
        设置步长
        
        Parameters
        ----------
        step : int
            步长值，必须大于0
        """
        if step <= 0:
            return
        
        self._step = step
        
        # 重新对齐当前值到新的步长
        aligned_value = self._alignToStep(self.value())
        if aligned_value != self.value():
            self.setValue(aligned_value)

    def _alignToStep(self, value: int) -> int:
        """
        将数值对齐到步长
        
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
        offset = value - self.minimum()
        # 对齐到最近的步长
        aligned_offset = round(offset / self._step) * self._step
        aligned_value = self.minimum() + aligned_offset
        
        # 确保在有效范围内
        return max(self.minimum(), min(aligned_value, self.maximum()))

    def _posToValue(self, pos: QPoint) -> int:
        """
        将鼠标位置转换为对应的数值（带步长对齐）
        
        Parameters
        ----------
        pos : QPoint
            鼠标位置
            
        Returns
        -------
        int
            对齐到步长的数值
        """
        # 调用父类方法获取原始值
        raw_value = super()._posToValue(pos)
        
        # 对齐到步长
        return self._alignToStep(raw_value)

    def setValue(self, value: int) -> None:
        """
        设置滑块值（自动对齐到步长）
        
        Parameters
        ----------
        value : int
            要设置的值
        """
        aligned_value = self._alignToStep(value)
        super().setValue(aligned_value)