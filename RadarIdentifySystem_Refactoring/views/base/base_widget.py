from PyQt6.QtWidgets import QWidget
from typing import Optional, Any


class BaseWidget(QWidget):
    """控件基类
    
    为项目中的自定义控件提供通用的基础功能和接口规范。
    所有自定义控件都应该继承此基类以保持一致性。
    
    Attributes:
        _initialized: 标记控件是否已完成初始化
    """
    
    def __init__(self, parent: Optional[QWidget] = None):
        """初始化基础控件
        
        Args:
            parent: 父控件，默认为None
        """
        super().__init__(parent)
        self._initialized = False
        self._setup_ui()
        self._connect_signals()
        self._initialized = True
    
    def _setup_ui(self) -> None:
        """设置用户界面
        
        子类应重写此方法来创建和配置UI组件。
        此方法在__init__中被调用。
        """
        pass
    
    def _connect_signals(self) -> None:
        """连接信号和槽
        
        子类应重写此方法来连接信号和槽函数。
        此方法在_setup_ui之后被调用。
        """
        pass
    
    def set_enabled_state(self, enabled: bool) -> None:
        """设置控件启用状态
        
        Args:
            enabled: True为启用，False为禁用
        """
        self.setEnabled(enabled)
    
    def set_visible_state(self, visible: bool) -> None:
        """设置控件可见状态
        
        Args:
            visible: True为可见，False为隐藏
        """
        self.setVisible(visible)
    
    def get_widget_data(self) -> Any:
        """获取控件数据
        
        子类应重写此方法来返回控件的当前数据。
        
        Returns:
            控件的当前数据，具体类型由子类定义
        """
        return None
    
    def set_widget_data(self, data: Any) -> None:
        """设置控件数据
        
        子类应重写此方法来设置控件的数据。
        
        Args:
            data: 要设置的数据，具体类型由子类定义
        """
        pass
    
    def reset_widget(self) -> None:
        """重置控件到初始状态
        
        子类应重写此方法来实现控件的重置逻辑。
        """
        pass
    
    def validate_data(self) -> bool:
        """验证控件数据
        
        子类应重写此方法来实现数据验证逻辑。
        
        Returns:
            True表示数据有效，False表示数据无效
        """
        return True
    
    @property
    def is_initialized(self) -> bool:
        """检查控件是否已初始化
        
        Returns:
            True表示已初始化，False表示未初始化
        """
        return self._initialized