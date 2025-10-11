# coding:utf-8
from typing import Union
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QLabel, QButtonGroup, QVBoxLayout, QHBoxLayout

from qfluentwidgets import ComboBox, ExpandGroupSettingCard, RadioButton, qconfig, OptionsConfigItem, FluentIconBase
from views.base import SubTitle

class TimeFlipSettingCard(ExpandGroupSettingCard):
    """
    时间翻转设置卡片组件
    
    该组件用于配置雷达数据处理中的时间翻转处理策略，提供两种处理方式：
    1. 丢弃：丢弃出现到达时间重置情况的所有切片
    2. 保留：保留数据并选择拼合策略（重叠或顺序）
    
    组件特性：
    - 支持单选按钮切换处理方式
    - 保留模式下提供下拉框选择拼合策略
    - 自动保存和恢复用户的保留策略选择
    - 实时更新配置项并发射相应信号
    
    Signals:
        procChanged (OptionsConfigItem): 处理方式改变时发射
        reserveChanged (OptionsConfigItem): 保留策略改变时发射
    
    Attributes:
        procConfigItem (OptionsConfigItem): 处理方式配置项
        reserveConfigItem (OptionsConfigItem): 保留策略配置项
        _lastReserveChoice: 用户最后一次选择的保留策略，用于切换时恢复
    """

    procChanged = pyqtSignal(OptionsConfigItem)
    reserveChanged = pyqtSignal(OptionsConfigItem)

    def __init__(
        self, 
        configItem1: OptionsConfigItem, 
        configItem2: OptionsConfigItem, 
        icon: Union[str, QIcon, FluentIconBase], 
        title: str, 
        content=None, 
        texts: list[str] = None,
        parent=None
    ):
        """
        初始化时间翻转设置卡片
        
        Args:
            configItem1 (OptionsConfigItem): 处理方式配置项，包含"丢弃"和"保留"选项
            configItem2 (OptionsConfigItem): 保留策略配置项，包含拼合策略选项
            icon (Union[str, QIcon, FluentIconBase]): 卡片图标
            title (str): 卡片标题
            content (str, optional): 卡片内容描述. Defaults to None.
            texts (list[str], optional): 保留策略选项的显示文本. Defaults to None，使用["重叠", "顺序"]
            parent (QWidget, optional): 父组件. Defaults to None.
            
        Raises:
            ValueError: 当配置项选项数量不符合要求时抛出异常
            
        Note:
            - configItem1应包含两个选项：[丢弃选项, 保留选项]
            - configItem2应包含保留策略选项，至少包含两个选项
            - texts参数用于自定义保留策略选项的显示文本
        """
        super().__init__(icon, title, content, parent=parent)
        self.procConfigItem = configItem1
        self.reserveConfigItem = configItem2
        self.procConfigName = configItem1.name
        self.texts = texts

        self.choiceLabel = QLabel(self)
        self.discardOption = self.procConfigItem.options[0]
        self.reserveOption = self.procConfigItem.options[1]
        self._lastReserveChoice = None

        self.radioWidget = QWidget(self.view)
        self.radioLayout = QVBoxLayout(self.radioWidget)
        self.discardRadioButton = RadioButton(self.radioWidget)
        self.reserveRadioButton = RadioButton(self.radioWidget)
        self.discardSubTitle = SubTitle("丢弃", "出现到达时间重置情况的所有切片，它们的数据将会被丢弃", self.discardRadioButton)
        self.reserveSubTitle = SubTitle("保留", "首尾拼合：将重置的TOA推移T1-T2，这会导致重置处的DTOA为0；序列相接：将重置的TOA推移T1，这会导致重置处的DTOA为T2。\n其中T1、T2分别为为重置处前、后的TOA。", self.reserveRadioButton)
        self.buttonGroup = QButtonGroup(self)
        self.reserveComboBox = ComboBox(self.radioWidget)

        self.__initWidget()

    def __initWidget(self) -> None:
        """
        初始化组件的UI控件
        
        该方法负责创建和配置所有UI控件，包括：
        1. 创建单选按钮组用于选择处理方式（丢弃/保留）
        2. 创建下拉框用于选择保留策略（重叠/顺序）
        3. 创建标签用于显示当前选择状态
        4. 设置控件的初始状态和值
        5. 连接信号和槽函数
        
        Note:
            - 根据配置项的当前值设置控件的初始状态
            - 如果保留策略不是"none"，则保存到_lastReserveChoice中
            - 连接单选按钮的clicked和toggled信号到相应的处理函数
            - 连接下拉框的currentIndexChanged信号到处理函数
        """
    def __initWidget(self):
        self.__initLayout()

        self.optionToText = {o: t for o, t in zip(self.reserveConfigItem.options[:2], self.texts)}
        for text, option in zip(self.texts, self.reserveConfigItem.options[:2]):
            self.reserveComboBox.addItem(text, userData=option)

        reserveText = (
            self.optionToText[qconfig.get(self.reserveConfigItem)] 
            if qconfig.get(self.reserveConfigItem) != "none" 
            else self.reserveConfigItem.options[0]
        )
        self.reserveComboBox.setCurrentText(reserveText)
        self.reserveComboBox.currentIndexChanged.connect(self._onCurrentIndexChanged)
        self.reserveConfigItem.valueChanged.connect(self.setReserveValue)

        # 初始化时保存当前的保留策略选择
        current_reserve_value = qconfig.get(self.reserveConfigItem)
        if current_reserve_value != "none":
            self._lastReserveChoice = current_reserve_value

        self.discardRadioButton.setProperty(self.procConfigName, self.discardOption)
        self.reserveRadioButton.setProperty(self.procConfigName, self.reserveOption)
        self.setProcValue(qconfig.get(self.procConfigItem))
        self.buttonGroup.buttonClicked.connect(self._onRadioButtonClicked)
        self.buttonGroup.buttonToggled.connect(self._onRadioButtonToggled)
        self.procConfigItem.valueChanged.connect(self.setProcValue)

        self.choiceLabel.setObjectName("titleLabel")

    def __initLayout(self) -> None:
        """
        初始化组件的布局结构
        
        该方法负责设置组件的布局和样式：
        1. 创建水平布局容器
        2. 添加单选按钮到布局中，设置适当的间距
        3. 添加下拉框和标签到布局中
        4. 设置布局的边距和对齐方式
        5. 将布局添加到卡片的视图区域
        
        布局结构：
        [单选按钮1] [单选按钮2] [下拉框] [状态标签]
        
        Note:
            - 使用水平布局确保控件在同一行显示
            - 设置适当的控件间距以保证良好的视觉效果
            - 确保布局在不同窗口大小下都能正常显示
        """
    def __initLayout(self):
        self.addWidget(self.choiceLabel)

        self.radioLayout.setSpacing(19)
        self.radioLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.radioLayout.setContentsMargins(48, 18, 0, 18)
        self.buttonGroup.addButton(self.discardRadioButton)
        self.buttonGroup.addButton(self.reserveRadioButton)

        self.discardWidget = QWidget(self.radioWidget)
        self.discardLayout = QHBoxLayout(self.discardWidget)
        self.discardLayout.setContentsMargins(0, 0, 0, 0)
        self.discardLayout.addWidget(self.discardRadioButton)
        self.discardLayout.addWidget(self.discardSubTitle)
        self.discardLayout.addStretch(1)

        self.reserveWidget = QWidget(self.radioWidget)
        self.reserveLayout = QHBoxLayout(self.reserveWidget)
        self.reserveLayout.setContentsMargins(0, 0, 0, 0)
        self.reserveLayout.addWidget(self.reserveRadioButton)
        self.reserveLayout.addWidget(self.reserveSubTitle)
        self.reserveLayout.addStretch(1)
        self.reserveLayout.addWidget(self.reserveComboBox, 0, Qt.AlignmentFlag.AlignRight)
        self.reserveLayout.addSpacing(16)

        self.radioLayout.addWidget(self.discardWidget)
        self.radioLayout.addWidget(self.reserveWidget)
        self.radioLayout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)

        self.viewLayout.setSpacing(0)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.addGroupWidget(self.radioWidget)

    def _onRadioButtonClicked(self, button: RadioButton):
        """
        处理单选按钮点击事件，更新选择标签和配置项

        Args:
            button: 被点击的单选按钮

        Returns:
            None
        """

        if button == self.reserveRadioButton and self.reserveRadioButton.isChecked():
            self.choiceLabel.setText("保留：" + self.reserveComboBox.currentText())
        elif button == self.discardRadioButton and self.discardRadioButton.isChecked():
            self.choiceLabel.setText(self.discardSubTitle.titleLabel.text())

    def _onRadioButtonToggled(self, button: RadioButton):
        """
        处理单选按钮切换事件，更新选择标签和配置项

        Args:
            button: 被切换的单选按钮

        Returns:
            None
        """
        if not button.isChecked():
            return

        value = button.property(self.procConfigName)
        qconfig.set(self.procConfigItem, value)

        self.procChanged.emit(self.procConfigItem)

    def setProcValue(self, value: str) -> None:
        """
        设置处理方式的值并更新UI显示
        
        该方法用于程序化地设置处理方式，支持在"丢弃"和"保留"之间切换。
        当切换到"保留"模式时，会自动恢复用户之前选择的保留策略。
        
        Args:
            value (str): 处理方式的值，应该是procConfigItem.options中的有效选项
            
        Note:
            - 当切换到"保留"模式时，如果_lastReserveChoice不为None，会恢复之前的选择
            - 当切换到"丢弃"模式时，reserveConfigItem会被设置为"none"
            - 会更新单选按钮的选中状态和下拉框的显示
            - 会发射procChanged信号通知其他组件
            
        Example:
            >>> card.setProcValue("discard")   # 切换到丢弃模式
            >>> card.setProcValue("reserve")   # 切换到保留模式，恢复之前的策略
        """

        qconfig.set(self.procConfigItem, value)

        if self.discardRadioButton.property(self.procConfigName) == value:
            self.discardRadioButton.setChecked(True)
            self.reserveComboBox.setEnabled(False)
            self.choiceLabel.setText(self.discardSubTitle.titleLabel.text())
            self.choiceLabel.adjustSize()
            qconfig.set(self.reserveConfigItem, "none")
        elif self.reserveRadioButton.property(self.procConfigName) == value:
            self.reserveRadioButton.setChecked(True)
            self.reserveComboBox.setEnabled(True)
            
            # 恢复用户之前的保留策略选择
            if self._lastReserveChoice is not None:
                # 使用用户之前的选择
                restore_value = self._lastReserveChoice
                qconfig.set(self.reserveConfigItem, restore_value)
                # 更新ComboBox显示
                self.reserveComboBox.setCurrentText(self.optionToText[restore_value])
            else:
                # 如果没有之前的选择，使用当前ComboBox的值
                current_value = self.reserveComboBox.itemData(self.reserveComboBox.currentIndex())
                qconfig.set(self.reserveConfigItem, current_value)
                self._lastReserveChoice = current_value
            
            self.choiceLabel.setText("保留：" + self.reserveComboBox.currentText())
            self.choiceLabel.adjustSize()

    def _onCurrentIndexChanged(self, index: int):
        """
        处理保留策略下拉框选择变化事件
        
        Args:
            index (int): 选中的索引
        """
        selected_value = self.reserveComboBox.itemData(index)
        qconfig.set(self.reserveConfigItem, selected_value)
        self.choiceLabel.setText("保留：" + self.reserveComboBox.currentText())
        self.choiceLabel.adjustSize()
        
        # 保存用户的选择，用于后续恢复
        self._lastReserveChoice = selected_value
        
        self.reserveChanged.emit(self.reserveConfigItem)
        
    def setReserveValue(self, value: str) -> None:
        """
        设置保留策略的值并更新UI显示
        
        该方法用于程序化地设置保留策略的值，通常在配置加载或外部调用时使用。
        
        Args:
            value (str): 保留策略的值，应该是reserveConfigItem.options中的有效选项
            
        Note:
            - 该方法会更新下拉框的当前选择
            - 会触发配置项的更新（通过qconfig.set）
            - 会发射reserveChanged信号通知其他组件
            - 如果value不在有效选项中，下拉框会保持当前状态
            
        Example:
            >>> card.setReserveValue("overlapping")  # 设置为重叠策略
            >>> card.setReserveValue("sequential")   # 设置为顺序策略
        """
        if value not in self.optionToText:
            return

        self.reserveComboBox.setCurrentText(self.optionToText[value])
        qconfig.set(self.reserveConfigItem, value)
