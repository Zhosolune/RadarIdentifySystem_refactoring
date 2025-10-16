# RadarIdentifySystem 项目总览

本项目采用 MVC 架构改造后的雷达识别系统，强调配置驱动、信号总线解耦与高质量的 UI 组件化。

- 项目入口：`main.py`
- 架构分层：`models/`（模型层）、`views/`（视图层）、`controllers/`（控制器层）
- 全局资源：`resources/`（图标、图片、主题样式）
- 文档：`docs/`（设计与 API 文档）
- 测试：`tests/`（单元与集成测试）

## 快速开始

- 安装依赖：`pip install -r RadarIdentifySystem_Refactoring/requirements.txt`
- 运行应用：`python RadarIdentifySystem_Refactoring/main.py`

## 文档结构

```
docs/
├── api/
│   ├── models.md      # 模型层API
│   ├── views.md       # 视图层API
│   ├── controllers.md # 控制器层API
│   └── components.md  # 组件API
├── params_config_design.md
└── signal_bus_usage_guide.md
```

## 关键特性

- 配置统一管理（`AppConfig` + `QConfig`）
- 全局信号总线（`MainWindowSignalBus`）实现模块间解耦
- 组件化的设置卡片与交互控件
- 统一日志管理（`LogManager`，基于 `loguru`）
- UI 尺寸与响应式规范（`UIDimensions`）

## API 文档

详见 `docs/api/*.md`，包含各分层与组件的接口说明与使用示例。