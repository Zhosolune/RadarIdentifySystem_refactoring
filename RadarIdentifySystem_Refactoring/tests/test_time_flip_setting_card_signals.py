# coding:utf-8
"""
TimeFlipSettingCard组件信号发射功能测试

这个测试程序创建一个可视化界面，用于测试TimeFlipSettingCard组件的信号发射功能。
包含以下测试功能：
1. procChanged信号测试 - 测试单选按钮切换时的信号发射
2. reserveChanged信号测试 - 测试下拉框选项改变时的信号发射
3. 实时显示信号触发情况和参数值
4. 提供清除日志和重置配置的功能
"""

import sys
import os
from datetime import datetime
from typing import Optional

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QFrame
from PyQt6.QtGui import QFont

from qfluentwidgets import (
    FluentIcon as FIF, 
    OptionsConfigItem, 
    OptionsValidator, 
    qconfig,
    PushButton,
    BodyLabel,
    CaptionLabel,
    ScrollArea,
    CardWidget
)

from views.components.time_flip_setting_card import TimeFlipSettingCard
from models.utils.log_manager import LoggerMixin


class SignalMonitor(QWidget, LoggerMixin):
    """
    信号监控器组件
    
    用于显示和记录TimeFlipSettingCard组件发射的信号信息，
    包括信号类型、触发时间、配置项名称和值等详细信息。
    """
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        初始化信号监控器
        
        Args:
            parent: 父组件，默认为None
            
        Returns:
            None
        """
        super().__init__(parent)
        self.setupUI()
        
    def setupUI(self) -> None:
        """
        设置监控器界面
        
        Returns:
            None
        """
        layout = QVBoxLayout(self)
        
        # 标题
        title = BodyLabel("信号监控器", self)
        title.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # 信号日志显示区域
        self.logTextEdit = QTextEdit(self)
        self.logTextEdit.setReadOnly(True)
        self.logTextEdit.setMaximumHeight(200)
        self.logTextEdit.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #d0d0d0;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 10pt;
            }
        """)
        layout.addWidget(self.logTextEdit)
        
        # 控制按钮
        buttonLayout = QHBoxLayout()
        
        self.clearButton = PushButton("清除日志", self)
        self.clearButton.clicked.connect(self.clearLog)
        buttonLayout.addWidget(self.clearButton)
        
        buttonLayout.addStretch()
        layout.addLayout(buttonLayout)
        
        # 添加初始日志
        self.addLog("信号监控器已启动，等待信号...")
        
    def addLog(self, message: str) -> None:
        """
        添加日志信息
        
        Args:
            message: 日志消息内容
            
        Returns:
            None
        """
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] {message}"
        self.logTextEdit.append(log_entry)
        
        # 自动滚动到底部
        cursor = self.logTextEdit.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.logTextEdit.setTextCursor(cursor)
        
    def clearLog(self) -> None:
        """
        清除所有日志
        
        Returns:
            None
        """
        self.logTextEdit.clear()
        self.addLog("日志已清除")


class TimeFlipSettingCardTestWindow(QWidget, LoggerMixin):
    """
    TimeFlipSettingCard组件信号测试主窗口
    
    提供完整的测试界面，包含TimeFlipSettingCard组件实例、
    信号监控器、配置状态显示和测试控制功能。
    """
    
    def __init__(self) -> None:
        """
        初始化测试窗口
        
        Returns:
            None
        """
        super().__init__()
        self.setupConfig()
        self.setupUI()
        self.connectSignals()
        self.logger.info("TimeFlipSettingCard信号测试窗口已初始化")
        
    def setupConfig(self) -> None:
        """
        设置测试用的配置项
        
        Returns:
            None
        """
        # 创建测试用的配置项
        self.procConfigItem = OptionsConfigItem(
            "Test", 
            "timeFlipProc", 
            "discard", 
            OptionsValidator(["discard", "reserve"])
        )
        
        self.reserveConfigItem = OptionsConfigItem(
            "Test", 
            "timeFlipReserve", 
            "overlapping", 
            OptionsValidator(["overlapping", "sequential", "none"])
        )
        
        # 下拉框选项文本
        self.reserveTexts = ["重叠处理", "顺序处理"]
        
    def setupUI(self) -> None:
        """
        设置测试窗口界面
        
        Returns:
            None
        """
        self.setWindowTitle("TimeFlipSettingCard 信号测试")
        self.setMinimumSize(800, 700)
        self.resize(800, 700)
        
        # 主布局
        mainLayout = QVBoxLayout(self)
        mainLayout.setSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        
        # 创建滚动区域
        scrollArea = ScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # 滚动内容容器
        scrollContent = QWidget()
        scrollLayout = QVBoxLayout(scrollContent)
        scrollLayout.setSpacing(20)
        scrollLayout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        titleLabel = BodyLabel("TimeFlipSettingCard 组件信号发射测试", self)
        titleLabel.setFont(QFont("Microsoft YaHei", 16, QFont.Weight.Bold))
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scrollLayout.addWidget(titleLabel)
        
        # 说明文本
        descLabel = CaptionLabel(
            "这个测试界面用于验证TimeFlipSettingCard组件的信号发射功能。\n"
            "请操作下方的组件，观察信号监控器中的日志输出。", 
            self
        )
        descLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descLabel.setWordWrap(True)
        scrollLayout.addWidget(descLabel)
        
        # 分隔线
        line1 = QFrame(self)
        line1.setFrameShape(QFrame.Shape.HLine)
        line1.setFrameShadow(QFrame.Shadow.Sunken)
        scrollLayout.addWidget(line1)
        
        # 测试组件区域
        componentCard = CardWidget(self)
        componentLayout = QVBoxLayout(componentCard)
        componentLayout.setContentsMargins(20, 20, 20, 20)
        
        componentTitle = BodyLabel("测试组件", self)
        componentTitle.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        componentLayout.addWidget(componentTitle)
        
        # 创建TimeFlipSettingCard组件
        self.timeFlipCard = TimeFlipSettingCard(
            configItem1=self.procConfigItem,
            configItem2=self.reserveConfigItem,
            icon=FIF.SETTING,
            title="时间翻转处理",
            content="设置时间翻转数据的处理方式",
            texts=self.reserveTexts,
            parent=componentCard
        )
        componentLayout.addWidget(self.timeFlipCard)
        
        scrollLayout.addWidget(componentCard)
        
        # 分隔线
        line2 = QFrame(self)
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        scrollLayout.addWidget(line2)
        
        # 信号监控器
        self.signalMonitor = SignalMonitor(self)
        scrollLayout.addWidget(self.signalMonitor)
        
        # 分隔线
        line3 = QFrame(self)
        line3.setFrameShape(QFrame.Shape.HLine)
        line3.setFrameShadow(QFrame.Shadow.Sunken)
        scrollLayout.addWidget(line3)
        
        # 配置状态显示
        statusCard = CardWidget(self)
        statusLayout = QVBoxLayout(statusCard)
        statusLayout.setContentsMargins(20, 15, 20, 15)
        
        statusTitle = BodyLabel("当前配置状态", self)
        statusTitle.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        statusLayout.addWidget(statusTitle)
        
        self.statusLabel = CaptionLabel("", self)
        self.statusLabel.setWordWrap(True)
        statusLayout.addWidget(self.statusLabel)
        
        scrollLayout.addWidget(statusCard)
        
        # 控制按钮区域
        buttonLayout = QHBoxLayout()
        
        self.resetButton = PushButton("重置配置", self)
        self.resetButton.clicked.connect(self.resetConfig)
        buttonLayout.addWidget(self.resetButton)
        
        buttonLayout.addStretch()
        
        self.exitButton = PushButton("退出测试", self)
        self.exitButton.clicked.connect(self.close)
        buttonLayout.addWidget(self.exitButton)
        
        scrollLayout.addLayout(buttonLayout)
        
        # 设置滚动区域的内容
        scrollArea.setWidget(scrollContent)
        mainLayout.addWidget(scrollArea)
        
        # 更新状态显示
        self.updateStatusDisplay()
        
    def connectSignals(self) -> None:
        """
        连接信号槽
        
        Returns:
            None
        """
        # 连接TimeFlipSettingCard的信号
        self.timeFlipCard.procChanged.connect(self.onProcChanged)
        self.timeFlipCard.reserveChanged.connect(self.onReserveChanged)
        
        # 连接配置项的值变化信号
        self.procConfigItem.valueChanged.connect(self.onConfigValueChanged)
        self.reserveConfigItem.valueChanged.connect(self.onConfigValueChanged)
        
    def onProcChanged(self, configItem) -> None:
        """
        处理procChanged信号
        
        Args:
            configItem: 发生变化的配置项
            
        Returns:
            None
        """
        value = qconfig.get(configItem)
        message = f"🔄 procChanged信号触发 - 配置项: {configItem.name}, 新值: {value}"
        self.signalMonitor.addLog(message)
        self.logger.info(f"procChanged信号: {configItem.name} = {value}")
        
        # 延迟更新状态显示，确保配置已更新
        QTimer.singleShot(50, self.updateStatusDisplay)
        
    def onReserveChanged(self, configItem) -> None:
        """
        处理reserveChanged信号
        
        Args:
            configItem: 发生变化的配置项
            
        Returns:
            None
        """
        value = qconfig.get(configItem)
        # 获取对应的显示文本
        text_map = {
            "overlapping": "重叠处理",
            "sequential": "顺序处理",
            "none": "不处理"
        }
        display_text = text_map.get(value, value)
        
        message = f"📋 reserveChanged信号触发 - 配置项: {configItem.name}, 新值: {value} ({display_text})"
        self.signalMonitor.addLog(message)
        self.logger.info(f"reserveChanged信号: {configItem.name} = {value}")
        
        # 延迟更新状态显示，确保配置已更新
        QTimer.singleShot(50, self.updateStatusDisplay)
        
    def onConfigValueChanged(self, value) -> None:
        """
        处理配置项值变化
        
        Args:
            value: 新的配置值
            
        Returns:
            None
        """
        # 这个方法用于监听配置项的直接变化
        QTimer.singleShot(100, self.updateStatusDisplay)
        
    def updateStatusDisplay(self) -> None:
        """
        更新配置状态显示
        
        Returns:
            None
        """
        proc_value = qconfig.get(self.procConfigItem)
        reserve_value = qconfig.get(self.reserveConfigItem)
        
        # 获取显示文本
        proc_text = "丢弃" if proc_value == "discard" else "保留"
        reserve_text = "重叠处理" if reserve_value == "overlapping" else "不处理" if reserve_value == "none" else "顺序处理"
        
        status_text = (
            f"处理方式: {proc_text} ({proc_value})\n"
            f"保留方式: {reserve_text} ({reserve_value})"
        )
        
        self.statusLabel.setText(status_text)
        
    def resetConfig(self) -> None:
        """
        重置配置到默认值
        
        Returns:
            None
        """
        # 重置配置项到默认值
        qconfig.set(self.procConfigItem, "discard")
        qconfig.set(self.reserveConfigItem, "overlapping")
        
        self.signalMonitor.addLog("🔄 配置已重置到默认值")
        self.logger.info("配置已重置")
        
        # 更新状态显示
        self.updateStatusDisplay()


def main():
    """
    主函数，启动测试应用程序
    
    Returns:
        None
    """
    app = QApplication(sys.argv)
    
    # 设置应用程序属性
    app.setApplicationName("TimeFlipSettingCard信号测试")
    app.setApplicationVersion("1.0.0")
    
    # 创建并显示测试窗口
    window = TimeFlipSettingCardTestWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()