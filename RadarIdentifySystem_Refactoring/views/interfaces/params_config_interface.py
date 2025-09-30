from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QResizeEvent
from qfluentwidgets import (
    OptionsSettingCard,
    ComboBoxSettingCard,
    ExpandLayout,
    ScrollArea,
    SettingCardGroup,
    SwitchSettingCard,
    CustomColorSettingCard,
    HyperlinkCard,
    PrimaryPushSettingCard,
    MessageBox,
    InfoBar,
    ExpandGroupSettingCard,
)
from qfluentwidgets import FluentIcon as FIF
from typing import Optional
from models.theme.style_sheet import StyleSheet
from models.ui.dimensions import UIDimensions
from models.utils.log_manager import LoggerMixin
from models.utils.icons_manager import Icon
from models.config.app_config import cfg
from views.components import OptionsWithIconCard, OptionsGroupWidget, OptionsGroupSettingCard

class ParamsConfigInterface(ScrollArea, LoggerMixin):
    """参数配置界面

    用于系统设置的界面，包含主题设置等功能。
    """

    def __init__(self, text: str, parent: Optional[QWidget] = None):
        """初始化参数配置界面

        Args:
            text: 界面标识文本
            parent: 父控件
        """
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.scrollWidget.setMaximumWidth(UIDimensions.SCROLL_AREA_MAX_WIDTH_SETTING)
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # 设置标签
        self.settingLabel = QLabel("参数配置", self)

        # 导入设置
        self.importGroup = SettingCardGroup("导入设置", self.scrollWidget)
        self.importFileFormatCard = ComboBoxSettingCard(
            cfg.importFileFormat, 
            Icon.IMPORT_FILE, 
            "文件格式", 
            "选择将要导入文件的格式", 
            texts=["CSV", "Excel", "TXT", "MAT"], 
            parent=self.importGroup
        )
        self.dataDirectionCard = OptionsWithIconCard(
            cfg.dataDirection,
            Icon.DATA_DIRECTION, 
            "数据方向", 
            "选择数据的方向", 
            parent=self.importGroup
        )
        self.ignoreFirstLineCard = SwitchSettingCard(
            Icon.IGNORE_FIRST_LINE, 
            "忽略首行", 
            "如果文件的第一行/列是表头等信息，可以选择在导入数据时忽略第一行/列", 
            cfg.ignoreFirstLine, 
            parent=self.importGroup
        )
        self._setup_switch(self.ignoreFirstLineCard)
        self.dimIndexSettingCard = None
        self.dimIndexSettingCard = OptionsGroupSettingCard(
            FIF.IOT,
            "维度索引",
            "选择脉冲数据的各个维度在文件中的索引，以动态匹配不同的数据包格式。（索引从0开始）",
            [
                OptionsGroupWidget(cfg.dimCFIndex, "CF索引", parent=self.dimIndexSettingCard),
                OptionsGroupWidget(cfg.dimPWIndex, "PW索引", parent=self.dimIndexSettingCard),
                OptionsGroupWidget(cfg.dimPAIndex, "PA索引", parent=self.dimIndexSettingCard),
                OptionsGroupWidget(cfg.dimDOAIndex, "DOA索引", parent=self.dimIndexSettingCard),
                OptionsGroupWidget(cfg.dimTOAIndex, "TOA索引", parent=self.dimIndexSettingCard),
            ],
            parent=self.importGroup,
        )

        # 切片设置
        self.sliceGroup = SettingCardGroup("切片设置", self.scrollWidget)
        


        # 绘图设置
        self.plotGroup = SettingCardGroup("绘图设置", self.scrollWidget)
        





        # 设置UI
        self._setup_ui()

    def _setup_ui(self) -> None:
        """设置用户界面"""
        # 设置滚动区域属性
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("ParamsConfigInterface")

        # 设置滚动区域居中对齐
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # 初始化样式
        self.scrollWidget.setObjectName("scrollWidget")
        self.settingLabel.setObjectName("paramsConfigLabel")
        StyleSheet.PARAMS_CONFIG_INTERFACE.apply(self)

        # 初始化布局
        self._initLayout()

    def _initLayout(self) -> None:
        """初始化布局

        设置标签位置和卡片组布局。
        """
        # 初始化标签位置（相对定位）
        self._updateLabelPosition()

        # 添加设置卡片到组
        self.importGroup.addSettingCard(self.importFileFormatCard)
        self.importGroup.addSettingCard(self.dataDirectionCard)
        self.importGroup.addSettingCard(self.ignoreFirstLineCard)
        self.importGroup.addSettingCard(self.dimIndexSettingCard)

        # 添加卡片组到布局
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.importGroup)
        self.expandLayout.addWidget(self.sliceGroup)
        self.expandLayout.addWidget(self.plotGroup)



    def _updateLabelPosition(self) -> None:
        """更新设置标签位置

        根据滚动区域的宽度动态调整标签位置，使其始终与滚动区域保持一致的对齐方式。
        """
        # 获取当前窗口宽度
        window_width = self.width() if self.width() > 0 else UIDimensions.WINDOW_DEFAULT_WIDTH

        # 计算滚动区域的实际宽度（考虑最大宽度限制）
        scroll_area_width = min(window_width, UIDimensions.SCROLL_AREA_MAX_WIDTH_SETTING)

        # 计算标签的水平位置（与滚动区域左边距保持一致）
        # 滚动区域居中对齐，所以标签也应该相对于居中位置计算
        center_offset = (window_width - scroll_area_width) // 2
        label_x = max(center_offset + 36, 36)  # 确保最小边距为36px

        # 设置标签位置
        self.settingLabel.move(label_x, 30)

    def _setup_switch(self, switch_card: SwitchSettingCard) -> None:
        """设置开关卡片

        修改默认开关组件的中文文本。

        Args:
            switch_card: 开关卡片实例
        """
        switch_card.switchButton.setText(
            "是" if switch_card.isChecked() else "否")
        switch_card.switchButton.checkedChanged.connect(
            lambda isChecked: switch_card.switchButton.setText(
                "是" if isChecked else "否"))

    def resizeEvent(self, event: QResizeEvent) -> None:
        """窗口大小变化事件处理

        当窗口大小变化时，自动调整设置标签的位置。

        Args:
            event: 窗口大小变化事件
        """
        super().resizeEvent(event)
        # 更新标签位置以适应新的窗口大小
        self._updateLabelPosition()

