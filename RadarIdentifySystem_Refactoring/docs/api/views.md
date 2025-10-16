# 视图层 API（views）

视图层负责界面呈现与交互布局，不直接处理业务逻辑，通过信号与控制器协作。

## 主窗口与导航

- `views/main_window.py`
  - `MainWindow`: 基于 `MSFluentWindow` 的主窗口
    - 子页面：
      - `MainInterface` — 主工作台
      - `RadarAnalysisInterface` — 雷达分析
      - `ModelManagementInterface` — 模型管理
      - `SettingsInterface` — 设置
      - `ParamsConfigInterface` — 参数配置
    - 关键职责：创建子界面、注入控制器、连接信号、设置窗口图标与居中显示

## 子界面（views/interfaces）

- `main_interface.py`
  - 布局：左右滚动区，统一边距/间距（依赖 `UIDimensions`）

- `settings_interface.py`
  - 分组：基本设置、个性化、关于
  - 特性：标签相对定位（居中滚动区域对齐）、重启提示、主题/DPI/日志级别联动

- `params_config_interface.py`
  - 分组：导入设置、切片设置、绘图设置
  - 特性：标签相对定位、滚动区域居中与最大宽度限制、与设置卡片协作

- `radar_analysis_interface.py` / `model_management_interface.py`
  - 当前以占位视图为主，用于后续功能扩展

## 模块化面板（views/modules）

- `panel_module/*_panel.py`
  - `slice_panel`, `cluster_panel`, `parameter_panel`
  - 职责：各自领域的数据/参数变更的占位与信号定义（部分 TODO）

- `scroll_module/*`
  - `scroll_container.py`: 支持锚点吸附的滚动容器，鼠标滚轮滚动与动画吸附
  - `view_panel/*_view.py`: `slice_view`, `cluster_view`, `merge_view` — 5×1图像占位网格（部分 TODO：数据更新/清空逻辑）
  - `merge_control_panel/merge_control_panel.py`: 合并控制面板（TODO：启用/禁用与参数获取）

---

> 注：视图层仅负责界面与信号，具体业务逻辑由控制器与模型层实现。带有 TODO 的模块为功能占位，后续实现将补充详细 API。