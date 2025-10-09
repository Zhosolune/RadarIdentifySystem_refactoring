from typing import Optional, Union, List, Set
from qfluentwidgets import BodyLabel, RangeConfigItem, PillPushButton, qconfig, FluentIconBase, ExpandSettingCard
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QButtonGroup
from PyQt6.QtGui import QIcon
from models.utils.log_manager import LoggerMixin

class OptionsGroupWidget(QWidget, LoggerMixin):
    """
    选项组组件，支持智能交换机制

    这是一个自定义的选项组件，包含标题标签和多个选项按钮。
    支持智能交换机制：当选择已被其他组件占用的编号时，会自动与占用该编号的组件交换，
    或清空占用该编号的组件（如果当前组件未选择任何编号）。

    Signals:
        optionChanged (int, object): 选项值改变时发出，传递新值和当前组件实例

    Attributes:
        configItem (RangeConfigItem): 配置项，定义选项的范围和当前值
        configName (str): 配置项名称
        titleLabel (BodyLabel): 显示标题的标签
        buttonGroup (QButtonGroup): 管理所有选项按钮的按钮组
        optionCurent (int): 当前选择的选项值（已弃用，使用configItem.value）
        hBoxLayout (QHBoxLayout): 水平布局管理器
        parent_card (Optional[OptionsGroupSettingCard]): 父级设置卡片，用于智能交换功能
    """
    optionChanged = pyqtSignal(int, object)  # 传递选择的值和当前组件实例

    def __init__(self, configItem: RangeConfigItem, title: str, parent: Optional[QWidget] = None) -> None:
        """
        初始化带图标的选项组件

        Args:
            configItem: 配置项，包含选项范围信息
            title: 选项标题文本
            parent: 父组件，默认为None

        Returns:
            None

        Raises:
            ValueError: 当配置项范围无效时抛出异常
        """
        super().__init__(parent)

        # 初始化UI组件
        self.configItem = configItem
        self.configName = configItem.name
        self.titleLabel = BodyLabel(title, self)
        self.buttonGroup = QButtonGroup(self)
        self.optionCurent = -1
        self.parent_card: Optional['OptionsGroupSettingCard'] = None

        # 初始化布局管理器
        self.hBoxLayout = QHBoxLayout(self)

        # 配置水平布局：无边距，组件间距16像素
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setSpacing(16)

        # 添加文本到水平布局的最左侧
        self.hBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addStretch(1)

        # 添加配置按钮
        for option in range(*configItem.range):
            button = PillPushButton(str(option))
            self.buttonGroup.addButton(button)
            self.hBoxLayout.addWidget(button)
            button.setProperty(self.configName, option)

        self.setValue(qconfig.get(self.configItem))

        self.buttonGroup.buttonClicked.connect(self._onButtonClicked)
        configItem.valueChanged.connect(self.setValue)

    def setParentCard(self, parent_card: 'OptionsGroupSettingCard') -> None:
        """
        设置父级设置卡片，用于编号互斥功能

        Args:
            parent_card: 父级设置卡片实例

        Returns:
            None
        """
        self.parent_card = parent_card

    def _onButtonClicked(self, button: PillPushButton) -> None:
        """
        处理按钮点击事件，支持智能交换机制

        Args:
            button: 被点击的按钮

        Returns:
            None
        """
        value = int(button.property(self.configName))
        
        # 检查是否与当前值相同
        if value == self.configItem.value:
            return

        # 设置新值
        old_value = self.configItem.value
        qconfig.set(self.configItem, value)

        # 通知父级卡片处理智能交换
        if self.parent_card:
            self.parent_card._onOptionChanged(value, old_value, self)

        self.optionChanged.emit(value, self)

    def setValue(self, value: int) -> None:
        """
        设置选项值

        Args:
            value: 要设置的值

        Returns:
            None
        """
        qconfig.set(self.configItem, value)

        for button in self.buttonGroup.buttons():
            isChecked = button.property(self.configName) == value
            button.setChecked(isChecked)

class OptionsGroupSettingCard(ExpandSettingCard, LoggerMixin):
    """
    选项组设置卡片，支持编号互斥和智能交换机制
    
    这是一个扩展设置卡片，包含多个选项组件，确保不同组件不能选择相同的编号。
    
    Attributes:
        optionsGroupWidgets (List[OptionsGroupWidget]): 选项组件列表
        _occupied_values (Set[int]): 已被占用的编号集合
    """

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title: str, content: Optional[str] = None, 
                 optionsGroupWidgets: Optional[List[OptionsGroupWidget]] = None, parent: Optional[QWidget] = None) -> None:
        """
        初始化选项组设置卡片

        Args:
            icon: 卡片图标
            title: 卡片标题
            content: 卡片内容描述，默认为None
            optionsGroupWidgets: 选项组件列表，默认为None
            parent: 父组件，默认为None

        Returns:
            None
        """
        super().__init__(icon, title, content, parent)

        # 初始化选项组件列表和占用值集合
        self.optionsGroupWidgets: List[OptionsGroupWidget] = optionsGroupWidgets or []
        self.occupied_values: Set[int] = set()

        # 创建选项组
        self.viewLayout.setSpacing(19)
        self.viewLayout.setContentsMargins(48, 18, 48, 18)
        
        for optionsGroup in self.optionsGroupWidgets:
            # 设置父级卡片引用
            optionsGroup.setParentCard(self)
            self.viewLayout.addWidget(optionsGroup)
            
            # 初始化占用值集合
            current_value = optionsGroup.configItem.value
            if current_value is not None and current_value >= 0:
                self.occupied_values.add(current_value)

    def _onOptionChanged(self, new_value: int, old_value: int, source_widget: 'OptionsGroupWidget') -> None:
        """
        处理选项变更事件，实现智能交换机制

        Args:
            new_value: 新选择的编号
            old_value: 之前的编号
            source_widget: 触发变更的组件

        Returns:
            None
        """
        self.logger.info(f"维度索引设置: {source_widget.configName} 被设置为 {new_value}")
        
        # 查找是否有其他组件使用了新选择的编号
        conflicted_widget = None
        for widget in self.optionsGroupWidgets:
            if widget != source_widget and widget.configItem.value == new_value:
                conflicted_widget = widget
                break

        if conflicted_widget:
            # 智能交换机制：如果有其他组件使用新编号，则交换
            self.logger.info(f"维度索引交换: {conflicted_widget.configName} 被交换为 {old_value}")
            qconfig.set(conflicted_widget.configItem, old_value)
