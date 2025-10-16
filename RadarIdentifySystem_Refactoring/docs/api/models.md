# 模型层 API（models）

模型层负责应用配置、数据结构、服务与工具。以下为当前实现中的关键模块与接口摘要。

## 配置（models/config）

- `app_config.py`
  - `AppConfig`: 基于 `QConfig` 的应用配置集合
    - `mainWindow.micaEnable: bool` — 是否启用 Mica 效果
    - `mainWindow.dpiScale: float` — DPI 缩放比例（默认 1.0）
    - `mainWindow.logLevel: str` — 日志级别（`DEBUG/INFO/WARNING/ERROR/CRITICAL`）
    - `import.*` — 数据导入参数（文件格式、方向、列索引等）
  - 用法示例：
    ```python
    from models.config.app_config import app_config
    scale = app_config.mainWindow.dpiScale.value
    app_config.mainWindow.logLevel.value = "INFO"
    ```

- `app/config/config.json`
  - 应用初始化配置（默认值），优先级低于用户配置。

## 工具（models/utils）

- `log_manager.py`
  - `LogManager`: 单例日志管理
    - `get_logger(name: str) -> Logger` — 获取模块日志器
    - 示例：
      ```python
      from models.utils.log_manager import LogManager
      logger = LogManager.get_logger("radar")
      logger.info("系统启动")
      ```

- `signal_bus.py`
  - `MainWindowSignalBus`: 主窗口全局信号总线（单例）
    - 典型信号：`micaEnableChanged(bool)`, `switchToSampleCard()`, 主题/DPI/日志级别变更等
    - 示例：
      ```python
      from models.utils.signal_bus import signal_bus
      signal_bus.micaEnableChanged.emit(True)
      ```

## UI 规范（models/ui）

- `dimensions.py`
  - `UIDimensions`: 应用统一尺寸规范（窗口尺寸、内边距、间距、滚动区域宽度计算）
  - 示例：
    ```python
    from models.ui.dimensions import UIDimensions
    width = UIDimensions.calc_right_panel_width(1200)
    ```

## 数据与服务（models/data, models/services, models/processors）

- 当前主要以占位与结构化目录为主，后续将补充雷达数据的处理流程、特征提取、训练/推理服务接口。

---

> 注：以上接口基于现有实现与测试用例总结，具体字段与方法以代码为准。随着功能完善，将持续补充更详细的类型与异常说明。