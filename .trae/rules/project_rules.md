# 核心行为规范

- 时时刻刻牢记遵守MVC架构原则，避免单文件杂糅不同职责，保持代码的清晰和可维护性
- PyQt6-Fluent-Widgets在命令中被简化成“PFW”，你识别到PFW时应当理解我是在说PyQt6-Fluent-Widgets库
- 功能重构不允许篡改原项目的功能
- 原项目目录为E:\myProjects_Trae\RadarIdentifySystem_trae\RadarIdentifySystem
- 重构后项目目录为E:\myProjects_Trae\RadarIdentifySystem_trae\RadarIdentifySystem_Refactoring

# 代码编写规范

- Python导入使用绝对路径导入，不使用相对路径导入
- 除了明确说明，否则一律使用PyQt6-Fluent-Widgets库编写UI代码
- 编写代码时，要编写适宜的日志输出，以便于调试和维护，使用软件自己的日志类：from models.utils.log_manager import LoggerMixin
    - 要根据具体任务的日志重要程度选择使用不同的日志级别，例如：
        - 调试信息：DEBUG
        - 一般信息：INFO
        - 警告信息：WARNING
        - 错误信息：ERROR
        - 严重错误：CRITICAL
- 当你编写UI相关的代码文件时，一定要使用MCP服务的context7工具查询PyQt6-Fluent-Widgets官方文档，以获取正确的接口、用法和最佳实践
- 测试文件使用“sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))”的方式将项目根目录添加到Python路径，其中“../..”根据实际目录层级确定

# 文件操作规范

- 你必须对完成的每一个模块进行单元测试，测试文件的代码按照类别存放在RadarIdentifySystem_Refactoring/tests目录下，若该目录不存在，则创建它
