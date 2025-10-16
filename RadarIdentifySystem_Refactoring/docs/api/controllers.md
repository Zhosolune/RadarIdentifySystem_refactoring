# 控制器层 API（controllers）

控制器负责连接视图与模型，处理交互逻辑与配置刷新。

## 设置控制器（controllers/ui/settings_controller.py）

- `SettingsController`
  - 职责：
    - 管理设置界面与应用配置的同步
    - 实现“配置驱动”的主题刷新、DPI 缩放与日志级别变更
    - 连接全局信号总线（主题、DPI、日志级别等）
  - 常用方法与行为：
    - `bind_interface(settings_interface)` — 绑定设置界面并建立信号连接
    - 响应配置变化，触发界面刷新或重启提示
  - 使用示例：
    ```python
    from controllers.ui.settings_controller import SettingsController
    from views.interfaces.settings_interface import SettingsInterface
    
    controller = SettingsController()
    interface = SettingsInterface(parent)
    controller.bind_interface(interface)
    ```

---

> 注：随着更多控制器的增加（参数控制器、数据处理控制器等），本文件将扩展相应的接口说明与序列图。