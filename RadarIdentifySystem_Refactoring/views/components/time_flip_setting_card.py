# coding:utf-8
from typing import Union
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QLabel, QButtonGroup, QVBoxLayout, QHBoxLayout

from qfluentwidgets import ComboBox, ExpandGroupSettingCard, RadioButton, qconfig, OptionsConfigItem, FluentIconBase

class TimeFlipSettingCard(ExpandGroupSettingCard):
    """
    
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
        self.discardRadioButton = RadioButton("丢弃", self.radioWidget)
        self.reserveRadioButton = RadioButton("保留", self.radioWidget)
        self.buttonGroup = QButtonGroup(self)
        self.reserveComboBox = ComboBox(self.radioWidget)

        self.__initWidget()

    def __initWidget(self):
        self.__initLayout()

        self.optionToText = {o: t for o, t in zip(self.reserveConfigItem.options[:2], self.texts)}
        for text, option in zip(self.texts, self.reserveConfigItem.options[:2]):
            self.reserveComboBox.addItem(text, userData=option)

        self.reserveComboBox.setCurrentText(self.optionToText[qconfig.get(self.reserveConfigItem)])
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

        self.choiceLabel.setText(self.buttonGroup.checkedButton().text())
        self.choiceLabel.adjustSize()

        self.choiceLabel.setObjectName("titleLabel")

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
        self.discardLayout.addStretch(1)

        self.reserveWidget = QWidget(self.radioWidget)
        self.reserveLayout = QHBoxLayout(self.reserveWidget)
        self.reserveLayout.setContentsMargins(0, 0, 0, 0)
        self.reserveLayout.addWidget(self.reserveRadioButton)
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

        if self.reserveRadioButton.isChecked():
            self.choiceLabel.setText(self.reserveComboBox.currentText())
        else:
            self.choiceLabel.setText(self.discardRadioButton.text())

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

    def setProcValue(self, value):
        """
        根据值选择对应的单选按钮
        
        Args:
            value: 处理方式的值（保留或丢弃）
        """
        qconfig.set(self.procConfigItem, value)

        if self.discardRadioButton.property(self.procConfigName) == value:
            self.discardRadioButton.setChecked(True)
            self.reserveComboBox.setEnabled(False)
            self.choiceLabel.setText(self.discardRadioButton.text())
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
            
            self.choiceLabel.setText(self.reserveComboBox.currentText())
            self.choiceLabel.adjustSize()

    def _onCurrentIndexChanged(self, index: int):
        """
        处理保留策略下拉框选择变化事件
        
        Args:
            index (int): 选中的索引
        """
        selected_value = self.reserveComboBox.itemData(index)
        qconfig.set(self.reserveConfigItem, selected_value)
        self.choiceLabel.setText(self.reserveComboBox.currentText())
        self.choiceLabel.adjustSize()
        
        # 保存用户的选择，用于后续恢复
        self._lastReserveChoice = selected_value
        
        self.reserveChanged.emit(self.reserveConfigItem)
        
    def setReserveValue(self, value):
        if value not in self.optionToText:
            return

        self.reserveComboBox.setCurrentText(self.optionToText[value])
        qconfig.set(self.reserveConfigItem, value)
