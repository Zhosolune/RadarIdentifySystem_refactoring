from PyQt6.QtWidgets import QWidget, QHBoxLayout, QGridLayout
from qfluentwidgets import BodyLabel, LineEdit, setCustomStyleSheet
from typing import Optional


class ParamsConfigWidget(QWidget):
    """参数配置框组件
    
    提供水平和垂直两种布局方式的参数配置框，包含参数标签、输入框和单位标签。
    
    Attributes:
        _label: 参数标签组件
        _input: 输入框组件
        _unit_label: 单位标签组件
        _layout: 布局管理器
    """
    
    def __init__(self, parent: Optional[QWidget] = None):
        """初始化参数配置框组件
        
        Args:
            parent: 父组件，默认为None
        """
        super().__init__(parent)
        
        # 初始化组件
        self._label = BodyLabel("参数")
        self._input = LineEdit()
        self._unit_label = BodyLabel("单位")
        
        # 默认使用水平布局
        self._layout = None
        self._is_horizontal = True  # 记录当前布局类型
        self._setup_horizontal_layout()
    
    def _setup_horizontal_layout(self) -> None:
        """设置水平布局
        
        布局方式：参数标签、输入框、单位标签为一行三列
        """
        if self._is_horizontal and self._layout is not None:
            return  # 已经是水平布局，无需重复设置
            
        self._clear_layout()
        
        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        
        # 添加组件到水平布局
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._input)
        self._layout.addWidget(self._unit_label)
        
        self.setLayout(self._layout)
        self._is_horizontal = True
    
    def _setup_vertical_layout(self) -> None:
        """设置垂直布局
        
        布局方式：第一行参数标签，第二行输入框、单位标签（2行2列）
        """
        if not self._is_horizontal and self._layout is not None:
            return  # 已经是垂直布局，无需重复设置
            
        self._clear_layout()
        
        self._layout = QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(8)
        
        # 第一行：参数标签（跨两列）
        self._layout.addWidget(self._label, 0, 0, 1, 2)
        
        # 第二行：输入框和单位标签
        self._layout.addWidget(self._input, 1, 0)
        self._layout.addWidget(self._unit_label, 1, 1)
        
        self.setLayout(self._layout)
        self._is_horizontal = False
    
    def _clear_layout(self) -> None:
        """清除当前布局
        
        安全地删除当前布局并重新设置组件的父级
        """
        current_layout = self.layout()
        if current_layout:
            # 移除所有组件从布局中，但保持它们的父级关系
            while current_layout.count():
                child = current_layout.takeAt(0)
                if child.widget():
                    child.widget().setParent(self)
            
            # 创建一个临时的空widget来"接管"布局
            temp_widget = QWidget()
            temp_widget.setLayout(current_layout)
            temp_widget.deleteLater()
            
            # 重置内部布局引用
            self._layout = None
    
    def set_horizontal_layout(self) -> None:
        """设置为水平布局
        
        参数标签、输入框、单位标签为一行三列
        """
        self._setup_horizontal_layout()
    
    def set_vertical_layout(self) -> None:
        """设置为垂直布局
        
        第一行参数标签，第二行输入框、单位标签
        """
        self._setup_vertical_layout()
    
    def set_label_text(self, text: str) -> None:
        """设置参数标签文字
        
        Args:
            text: 标签文字内容
        """
        self._label.setText(text)
    
    def set_unit_text(self, text: str) -> None:
        """设置单位标签文字
        
        Args:
            text: 单位文字内容
        """
        self._unit_label.setText(text)
    
    def set_placeholder_text(self, text: str) -> None:
        """设置输入框默认文字（占位符）
        
        Args:
            text: 占位符文字内容
        """
        self._input.setPlaceholderText(text)
    
    def set_input_text(self, text: str) -> None:
        """设置输入框文字
        
        Args:
            text: 输入框文字内容
        """
        self._input.setText(text)
    
    def get_input_text(self) -> str:
        """获取输入框文字
        
        Returns:
            输入框中的文字内容
        """
        return self._input.text()
    
    def set_widget_width(self, width: int) -> None:
        """设置整个组件的宽度
        
        Args:
            width: 组件宽度（像素）
        """
        self.setFixedWidth(width)
    
    def set_widget_height(self, height: int) -> None:
        """设置整个组件的高度
        
        Args:
            height: 组件高度（像素）
        """
        self.setFixedHeight(height)
        # 自动调整输入框高度以适应组件高度
        self._adjust_input_height(height)
    
    def set_widget_size(self, width: int, height: int) -> None:
        """设置整个组件的尺寸
        
        Args:
            width: 组件宽度（像素）
            height: 组件高度（像素）
        """
        self.setFixedSize(width, height)
        # 自动调整输入框高度以适应组件高度
        self._adjust_input_height(height)
    
    def set_label_width(self, width: int) -> None:
        """设置参数标签的宽度
        
        Args:
            width: 标签宽度（像素）
        """
        self._label.setFixedWidth(width)
    
    def set_input_width(self, width: int) -> None:
        """设置输入框的宽度
        
        Args:
            width: 输入框宽度（像素）
        """
        self._input.setFixedWidth(width)
    
    def set_unit_label_width(self, width: int) -> None:
        """设置单位标签的宽度
        
        Args:
            width: 单位标签宽度（像素）
        """
        self._unit_label.setFixedWidth(width)
    
    def get_label_widget(self) -> BodyLabel:
        """获取参数标签组件
        
        Returns:
            参数标签组件实例
        """
        return self._label
    
    def get_input_widget(self) -> LineEdit:
        """获取输入框组件
        
        Returns:
            输入框组件实例
        """
        return self._input
    
    def get_unit_label_widget(self) -> BodyLabel:
        """获取单位标签组件
        
        Returns:
            单位标签组件实例
        """
        return self._unit_label
    
    def set_input_enabled(self, enabled: bool) -> None:
        """设置输入框是否可编辑
        
        Args:
            enabled: True为可编辑，False为只读
        """
        self._input.setEnabled(enabled)
    
    def clear_input(self) -> None:
        """清空输入框内容"""
        self._input.clear()
    
    def set_clear_button_enabled(self, enabled: bool) -> None:
        """设置输入框清除按钮是否可见
        
        Args:
            enabled: True为显示清除按钮，False为隐藏
        """
        self._input.setClearButtonEnabled(enabled)
    
    def _adjust_input_height(self, widget_height: int) -> None:
        """根据组件高度自动调整输入框高度
        
        Args:
            widget_height: 组件总高度
        """
        if self._is_horizontal:
            # 水平布局：输入框高度约为组件高度的80%，但不小于30px
            input_height = max(30, int(widget_height * 0.8))
        else:
            # 垂直布局：输入框高度约为组件高度的40%，但不小于30px
            input_height = max(30, int(widget_height * 0.4))
        
        self._input.setFixedHeight(input_height)
    
    def set_input_height(self, height: int) -> None:
        """手动设置输入框高度
        
        Args:
            height: 输入框高度（像素）
        """
        self._input.setFixedHeight(height)
    
    def set_label_style(self, light_qss: str, dark_qss: str) -> None:
        """设置参数标签样式
        
        Args:
            light_qss: 浅色主题样式表
            dark_qss: 深色主题样式表
        """
        setCustomStyleSheet(self._label, light_qss, dark_qss)
    
    def set_unit_label_style(self, light_qss: str, dark_qss: str) -> None:
        """设置单位标签样式
        
        Args:
            light_qss: 浅色主题样式表
            dark_qss: 深色主题样式表
        """
        setCustomStyleSheet(self._unit_label, light_qss, dark_qss)
    
    def set_labels_style(self, light_qss: str, dark_qss: str) -> None:
        """同时设置参数标签和单位标签样式
        
        Args:
            light_qss: 浅色主题样式表
            dark_qss: 深色主题样式表
        """
        setCustomStyleSheet(self._label, light_qss, dark_qss)
        setCustomStyleSheet(self._unit_label, light_qss, dark_qss)
    
    def set_input_style(self, light_qss: str, dark_qss: str) -> None:
        """设置输入框样式
        
        Args:
            light_qss: 浅色主题样式表
            dark_qss: 深色主题样式表
        """
        setCustomStyleSheet(self._input, light_qss, dark_qss)