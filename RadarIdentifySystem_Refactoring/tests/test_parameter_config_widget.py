import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from views.components.parameter_config_widget import ParameterConfigWidget


class TestWindow(QMainWindow):
    """测试窗口类
    
    用于测试ParameterConfigWidget组件的各种功能
    """
    
    def __init__(self):
        """初始化测试窗口"""
        super().__init__()
        self.setWindowTitle("参数配置框组件测试")
        self.setGeometry(100, 100, 600, 400)
        
        # 创建中央组件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建水平布局的参数配置框
        self.horizontal_config = ParameterConfigWidget()
        self.horizontal_config.set_label_text("频率")
        self.horizontal_config.set_unit_text("Hz")
        self.horizontal_config.set_placeholder_text("请输入频率值")
        self.horizontal_config.set_clear_button_enabled(True)
        self.horizontal_config.set_label_width(60)
        self.horizontal_config.set_widget_width(300)
        self.horizontal_config.set_widget_height(20)
        layout.addWidget(self.horizontal_config)
        
        # 创建垂直布局的参数配置框
        self.vertical_config = ParameterConfigWidget()
        self.vertical_config.set_vertical_layout()
        self.vertical_config.set_label_text("幅度")
        self.vertical_config.set_unit_text("dB")
        self.vertical_config.set_placeholder_text("请输入幅度值")
        self.vertical_config.set_input_text("20")
        self.vertical_config.set_clear_button_enabled(True)
        self.vertical_config.set_widget_height(80)  # 设置高度测试自适应
        # 测试样式设置
        self.vertical_config.set_label_style(
            "BodyLabel { color: #0078d4; font-weight: bold; }",
            "BodyLabel { color: #60cdff; font-weight: bold; }"
        )
        layout.addWidget(self.vertical_config)
        
        # 创建另一个水平布局的参数配置框（设置固定宽度）
        self.horizontal_config2 = ParameterConfigWidget()
        self.horizontal_config2.set_label_text("带宽")
        self.horizontal_config2.set_unit_text("MHz")
        self.horizontal_config2.set_placeholder_text("请输入带宽值")
        self.horizontal_config2.set_widget_width(300)
        self.horizontal_config2.set_label_width(40)
        self.horizontal_config2.set_input_width(200)
        self.horizontal_config2.set_unit_label_width(60)
        self.horizontal_config2.set_clear_button_enabled(True)
        layout.addWidget(self.horizontal_config2)
        
        # 创建按钮来测试功能
        button_layout = QVBoxLayout()
        
        # 切换布局按钮
        self.toggle_layout_btn = QPushButton("切换第一个组件为垂直布局")
        self.toggle_layout_btn.clicked.connect(self.toggle_layout)
        button_layout.addWidget(self.toggle_layout_btn)
        
        # 获取输入值按钮
        self.get_values_btn = QPushButton("获取所有输入值")
        self.get_values_btn.clicked.connect(self.get_all_values)
        button_layout.addWidget(self.get_values_btn)
        
        # 清空输入按钮
        self.clear_inputs_btn = QPushButton("清空所有输入")
        self.clear_inputs_btn.clicked.connect(self.clear_all_inputs)
        button_layout.addWidget(self.clear_inputs_btn)
        
        # 禁用/启用输入按钮
        self.toggle_enabled_btn = QPushButton("禁用/启用第二个组件输入")
        self.toggle_enabled_btn.clicked.connect(self.toggle_input_enabled)
        button_layout.addWidget(self.toggle_enabled_btn)
        
        # 测试高度调整按钮
        self.test_height_btn = QPushButton("测试组件高度调整")
        self.test_height_btn.clicked.connect(self.test_height_adjustment)
        button_layout.addWidget(self.test_height_btn)
        
        # 测试样式设置按钮
        self.test_style_btn = QPushButton("测试样式设置")
        self.test_style_btn.clicked.connect(self.test_style_setting)
        button_layout.addWidget(self.test_style_btn)
        
        layout.addLayout(button_layout)
        
        # 添加弹性空间
        layout.addStretch()
        
        # 记录当前状态
        self.is_horizontal = True
        self.input_enabled = True
    
    def toggle_layout(self) -> None:
        """切换第一个组件的布局方式"""
        if self.is_horizontal:
            self.horizontal_config.set_vertical_layout()
            self.toggle_layout_btn.setText("切换第一个组件为水平布局")
            self.is_horizontal = False
        else:
            self.horizontal_config.set_horizontal_layout()
            self.toggle_layout_btn.setText("切换第一个组件为垂直布局")
            self.is_horizontal = True
    
    def get_all_values(self) -> None:
        """获取所有组件的输入值并打印"""
        values = {
            "频率": self.horizontal_config.get_input_text(),
            "幅度": self.vertical_config.get_input_text(),
            "带宽": self.horizontal_config2.get_input_text()
        }
        
        print("当前输入值：")
        for param, value in values.items():
            print(f"  {param}: {value}")
    
    def clear_all_inputs(self) -> None:
        """清空所有组件的输入"""
        self.horizontal_config.clear_input()
        self.vertical_config.clear_input()
        self.horizontal_config2.clear_input()
        print("已清空所有输入")
    
    def toggle_input_enabled(self) -> None:
        """切换第二个组件的输入启用状态"""
        self.input_enabled = not self.input_enabled
        self.vertical_config.set_input_enabled(self.input_enabled)
        status = "启用" if self.input_enabled else "禁用"
        print(f"第二个组件输入已{status}")
    
    def test_height_adjustment(self) -> None:
        """测试组件高度调整功能"""
        import random
        # 随机设置不同的高度
        heights = [40, 60, 80, 100, 120]
        new_height = random.choice(heights)
        
        self.horizontal_config.set_widget_height(new_height)
        self.vertical_config.set_widget_height(new_height)
        
        print(f"已将组件高度调整为: {new_height}px")
        print("输入框高度已自动适应")
    
    def test_style_setting(self) -> None:
        """测试样式设置功能"""
        # 为第三个组件设置不同的样式
        self.horizontal_config2.set_labels_style(
            "BodyLabel { color: #d13438; font-size: 14px; }",
            "BodyLabel { color: #ff6b6b; font-size: 14px; }"
        )
        
        self.horizontal_config2.set_input_style(
            "LineEdit { border: 2px solid #d13438; border-radius: 6px; }",
            "LineEdit { border: 2px solid #ff6b6b; border-radius: 6px; }"
        )
        
        print("已为第三个组件设置红色主题样式")


def main():
    """主函数
    
    创建应用程序并显示测试窗口
    """
    app = QApplication(sys.argv)
    
    # 创建并显示测试窗口
    window = TestWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()