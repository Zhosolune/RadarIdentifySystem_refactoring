from typing import Union, Optional
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QButtonGroup, QLabel, QWidget

from qfluentwidgets import (
    RadioButton,
    FluentIcon as FIF,
    ExpandSettingCard,
    qconfig,
    OptionsConfigItem,
)
from views.base import OptionsWithIcon
from models.utils.icons_manager import Icon

class OptionsWithIconCard(ExpandSettingCard):
    """
    带图标选项的展开设置卡片组件
    
    这是一个继承自ExpandSettingCard的自定义组件，用于显示带图标的选项组。
    默认提供垂直和水平两个方向选项，支持配置项的读取和保存。
    当用户选择不同选项时，会发出optionChanged信号并自动保存到配置文件。
    
    Attributes:
        optionChanged (pyqtSignal): 选项改变时发出的信号，传递OptionsConfigItem对象
        optionLabel (QLabel): 显示当前选中选项标题的标签
        buttonGroup (QButtonGroup): 管理单选按钮互斥性的按钮组
        configItem (OptionsConfigItem): 关联的配置项对象
        configName (str): 配置项名称
        horizontalIcon: 水平方向选项的图标
        horizontalText (str): 水平方向选项的标题文本
        horizontalContent (str): 水平方向选项的描述文本
        horizontalOption (str): 水平方向选项的配置值
        verticalIcon: 垂直方向选项的图标
        verticalText (str): 垂直方向选项的标题文本
        verticalContent (str): 垂直方向选项的描述文本
        verticalOption (str): 垂直方向选项的配置值
        horizontalCard (OptionsWithIcon): 水平方向选项卡片组件
        verticalCard (OptionsWithIcon): 垂直方向选项卡片组件
    """

    # 默认垂直方向，样本竖向排列
    optionChanged = pyqtSignal(OptionsConfigItem)

    def __init__(
        self, 
        configItem: OptionsConfigItem, 
        icon: Union[str, QIcon, FIF], 
        title: str, 
        content: Optional[str] = None, 
        parent: Optional[QWidget] = None
    ) -> None:
        """
        初始化带图标选项的展开设置卡片
        
        Args:
        ---------
            configItem: 关联的配置项对象，用于读取和保存选项值
            icon: 卡片标题栏显示的图标，可以是字符串路径、QIcon对象或FluentIcon枚举
            title: 卡片标题文本
            content: 卡片描述内容文本，默认为None
            parent: 父组件，默认为None
            
        Returns:
        ---------
            None
        """
        super().__init__(icon, title, content, parent)
        
        # 初始化UI组件
        self.optionLabel = QLabel(self)
        self.buttonGroup = QButtonGroup(self)
        
        # 保存配置项相关信息
        self.configItem = configItem
        self.configName = configItem.name

        # 设置选项标签的样式名称
        self.optionLabel.setObjectName("titleLabel")
        self.addWidget(self.optionLabel)

        # 初始化UI界面
        self._setup_ui()

    def _setup_ui(self) -> None:
        """
        初始化UI组件和布局
        
        设置水平和垂直两个方向选项的图标、文本和配置值，
        创建对应的选项卡片组件，配置单选按钮组的互斥性，
        从配置文件读取当前值并设置界面状态，连接信号槽。
        
        Returns:
            None
        """

        # 第一组：水平方向选项配置
        self.horizontalIcon = Icon.HORIZONTAL
        self.horizontalText = "水平方向"
        self.horizontalContent = "样本脉冲横向排列"
        self.horizontalOption = "horizontal"

        # 第二组：垂直方向选项配置
        self.verticalIcon = Icon.VERTICAL
        self.verticalText = "垂直方向"
        self.verticalContent = "样本脉冲纵向排列"
        self.verticalOption = "vertical"

        # 创建水平方向选项卡片组件
        self.horizontalCard = OptionsWithIcon(
            icon=self.horizontalIcon, 
            title=self.horizontalText, 
            content=self.horizontalContent, 
            direction=self.horizontalOption
        )
        
        # 创建垂直方向选项卡片组件
        self.verticalCard = OptionsWithIcon(
            icon=self.verticalIcon, 
            title=self.verticalText, 
            content=self.verticalContent, 
            direction=self.verticalOption
        )

        # 添加单选按钮到互斥按钮组
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.addButton(self.horizontalCard.radioButton)
        self.buttonGroup.addButton(self.verticalCard.radioButton)

        # 为单选按钮设置配置属性，用于配置文件读取和保存
        self.horizontalCard.radioButton.setProperty(self.configName, self.horizontalOption)
        self.verticalCard.radioButton.setProperty(self.configName, self.verticalOption)

        # 调整视图大小以适应内容
        self._adjustViewSize()
        # 从配置文件读取当前值并设置界面状态
        self.setValue(qconfig.get(self.configItem))

        # 连接信号槽
        self.configItem.valueChanged.connect(self.setValue)
        self.buttonGroup.buttonClicked.connect(self._onButtonClicked)

        # 设置展开视图的布局参数
        self.viewLayout.setSpacing(19)
        self.viewLayout.setContentsMargins(48, 18, 48, 18)
        self.viewLayout.addWidget(self.horizontalCard)
        self.viewLayout.addWidget(self.verticalCard)

    def _onButtonClicked(self, button: RadioButton) -> None:
        """
        单选按钮点击事件处理器
        
        当用户点击某个选项的单选按钮时，检查是否为重复点击，
        如果不是重复点击，则获取按钮对应的配置值，保存到配置文件，
        更新选择标签显示的文本，并发出optionChanged信号。
        
        Args:
            button: 被点击的RadioButton对象
            
        Returns:
            None
        """
        # 检查是否为重复点击同一个选项
        if button.parent().titleLabel.text() == self.optionLabel.text():
            return

        # 获取按钮对应的配置值
        value = button.property(self.configName)
        # 保存配置值到配置文件
        qconfig.set(self.configItem, value)

        # 更新标签文本为当前选中选项
        self.optionLabel.setText(button.parent().titleLabel.text())
        self.optionLabel.adjustSize()
        # 发出选项改变信号
        self.optionChanged.emit(self.configItem)

    def setValue(self, value: str) -> None:
        """
        根据配置值设置选中的选项
        
        根据传入的配置值，找到对应的单选按钮并设置为选中状态，
        同时更新选择标签显示的文本。这个方法通常在初始化时
        或配置项值发生改变时被调用。
        
        Args:
            value: 配置值，应该是"horizontal"或"vertical"之一
            
        Returns:
            None
        """
        # 将配置值保存到配置文件
        qconfig.set(self.configItem, value)

        for button in self.buttonGroup.buttons():
            isChecked = button.property(self.configName) == value
            button.setChecked(isChecked)

            # 如果当前按钮被选中，更新标签文本
            if isChecked:
                self.optionLabel.setText(button.parent().titleLabel.text())
                self.optionLabel.adjustSize()

