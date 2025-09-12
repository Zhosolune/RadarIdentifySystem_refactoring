from typing import Final


class UIDimensions:
    """全局UI尺寸设定类
    
    统一管理界面中使用的各种尺寸参数，避免在各个页面文件中重复定义相同的尺寸值。
    所有尺寸值以像素(px)为单位。
    """
    
    # 内边距相关
    PADDING_SMALL: Final[int] = 5      # 小内边距
    PADDING_MEDIUM: Final[int] = 10    # 中等内边距
    PADDING_LARGE: Final[int] = 20     # 大内边距
    
    # 间距相关
    SPACING_SMALL: Final[int] = 5      # 小间距
    SPACING_MEDIUM: Final[int] = 10    # 中等间距
    SPACING_LARGE: Final[int] = 15     # 大间距
    SPACING_EXTRA_LARGE: Final[int] = 20  # 超大间距
    
    # 边框相关
    BORDER_WIDTH_THIN: Final[int] = 1  # 细边框
    BORDER_WIDTH_MEDIUM: Final[int] = 2  # 中等边框
    BORDER_WIDTH_THICK: Final[int] = 3   # 粗边框
    
    # 滚动区域相关
    SCROLL_AREA_MAX_WIDTH_PANEL: Final[int] = 600  # 滚动区域最大宽度（主界面）
    SCROLL_AREA_MAX_WIDTH_SETTING: Final[int] = 1200  # 滚动区域最大宽度（设置界面）
    
    # 面板相关
    PANEL_MIN_WIDTH: Final[int] = 250     # 面板最小宽度
    PANEL_MIN_HEIGHT: Final[int] = 200    # 面板最小高度
    PANEL_HEADER_HEIGHT: Final[int] = 40  # 面板标题栏高度
    
    # 按钮相关
    BUTTON_MIN_WIDTH: Final[int] = 80     # 按钮最小宽度
    BUTTON_MIN_HEIGHT: Final[int] = 32    # 按钮最小高度
    BUTTON_ICON_SIZE: Final[int] = 16     # 按钮图标大小
    
    # 输入框相关
    INPUT_MIN_WIDTH: Final[int] = 120     # 输入框最小宽度
    INPUT_HEIGHT: Final[int] = 32         # 输入框高度
    
    # 窗口相关
    WINDOW_MIN_WIDTH: Final[int] = 800    # 窗口最小宽度
    WINDOW_MIN_HEIGHT: Final[int] = 600   # 窗口最小高度
    WINDOW_DEFAULT_WIDTH: Final[int] = 1200  # 窗口默认宽度
    WINDOW_DEFAULT_HEIGHT: Final[int] = 800  # 窗口默认高度
    
    # 分割器相关
    SPLITTER_WIDTH: Final[int] = 4        # 分割器宽度
    
    # 工具栏相关
    TOOLBAR_HEIGHT: Final[int] = 40       # 工具栏高度
    TOOLBAR_ICON_SIZE: Final[int] = 24    # 工具栏图标大小
    
    # 状态栏相关
    STATUSBAR_HEIGHT: Final[int] = 25     # 状态栏高度
    
    @classmethod
    def get_right_panel_width(cls, total_width: int, padding: int = 40) -> int:
        """计算右侧面板宽度
        
        根据总宽度计算右侧面板的合适宽度，遵循三分之一原则且不超过最大值。
        
        Args:
            total_width: 总宽度
            padding: 需要减去的内边距和间距总和，默认40px
            
        Returns:
            计算后的右侧面板宽度
            
        Raises:
            ValueError: 当total_width小于等于padding时抛出
        """
        if total_width <= padding:
            raise ValueError(f"总宽度({total_width})必须大于内边距({padding})")
            
        available_width = total_width - padding
        calculated_width = available_width // 3
        return min(calculated_width, cls.SCROLL_AREA_MAX_WIDTH_PANEL)
    
    @classmethod
    def get_responsive_padding(cls, container_width: int) -> int:
        """根据容器宽度获取响应式内边距
        
        Args:
            container_width: 容器宽度
            
        Returns:
            响应式内边距值
        """
        if container_width < 600:
            return cls.PADDING_SMALL
        elif container_width < 1000:
            return cls.PADDING_MEDIUM
        else:
            return cls.PADDING_LARGE
    
    @classmethod
    def get_responsive_spacing(cls, container_width: int) -> int:
        """根据容器宽度获取响应式间距
        
        Args:
            container_width: 容器宽度
            
        Returns:
            响应式间距值
        """
        if container_width < 600:
            return cls.SPACING_SMALL
        elif container_width < 1000:
            return cls.SPACING_MEDIUM
        else:
            return cls.SPACING_LARGE