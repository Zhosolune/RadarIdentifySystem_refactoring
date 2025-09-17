# 信号总线使用规范文档

## 概述

本文档描述了雷达识别系统中信号总线（Signal Bus）的使用规范和最佳实践。信号总线是项目中用于实现组件间解耦通信的核心机制，遵循统一的架构模式和使用方式。

## 设计原则

1. **集中管理**：所有信号定义集中在信号总线类中
2. **职责分离**：不同功能模块使用独立的信号总线类
3. **解耦通信**：组件间通过信号总线进行通信，避免直接依赖
4. **架构一致性**：所有信号总线遵循相同的命名和使用模式
5. **单例模式**：每个信号总线类创建全局唯一实例

## 信号总线架构

### 文件结构

```
models/utils/signal_bus.py
├── MainWindowSignalBus        # 主窗口信号总线类
├── ParamsConfigSignalBus      # 参数配置信号总线类
├── [其他信号总线类]           # 未来扩展的信号总线类
├── mw_signalBus              # 主窗口信号总线实例
├── pc_signalBus              # 参数配置信号总线实例
└── [其他信号总线实例]         # 未来扩展的信号总线实例
```

### 信号总线类定义规范

```python
from PyQt6.QtCore import QObject, pyqtSignal

class [功能模块]SignalBus(QObject):
    """[功能模块]信号总线类
    
    用于管理应用程序中的[功能模块]类的全局信号，实现组件间的解耦通信。
    """

    # [功能模块]相关信号
    signal_name = pyqtSignal(参数类型)  # 信号描述
    
# 创建信号总线实例
[模块缩写]_signalBus = [功能模块]SignalBus()
```

## 现有信号总线

### 1. 主窗口信号总线 (MainWindowSignalBus)

**文件位置**: `models/utils/signal_bus.py`  
**实例名称**: `mw_signalBus`  
**用途**: 管理主窗口和应用程序级别的全局信号

#### 信号定义

```python
class MainWindowSignalBus(QObject):
    """主窗口信号总线类"""
    
    # 主窗口信号
    micaEnableChanged = pyqtSignal(bool)        # 云母效果开关变化
    switchToSampleCard = pyqtSignal(str, int)   # 切换到示例卡片
    
    # 设置信号
    settingInterfaceRestartSig = pyqtSignal()   # 设置界面重启信号
```

#### 使用示例

```python
# 导入信号总线
from models.utils.signal_bus import mw_signalBus

# 连接信号（在Controller层）
mw_signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)

# 发射信号（在View层或Controller层）
mw_signalBus.micaEnableChanged.emit(True)
```

### 2. 参数配置信号总线 (ParamsConfigSignalBus)

**文件位置**: `models/utils/signal_bus.py`  
**实例名称**: `pc_signalBus`  
**用途**: 管理参数配置系统的相关信号

#### 信号定义

```python
class ParamsConfigSignalBus(QObject):
    """参数配置信号总线类"""
    
    # 参数配置信号
    paramChanged = pyqtSignal(str, object)  # 参数变更信号 (param_name, new_value)
```

#### 使用示例

```python
# 导入信号总线
from models.utils.signal_bus import pc_signalBus

# 连接信号（在Controller层）
pc_signalBus.paramChanged.connect(self.on_param_changed)

# 发射信号（在Model层或Controller层）
pc_signalBus.paramChanged.emit("clustering.EPS", 0.5)
```

## 使用规范

### 1. 信号总线导入规范

```python
# ✅ 正确的导入方式
from models.utils.signal_bus import mw_signalBus, pc_signalBus

# ❌ 避免的导入方式
from models.utils.signal_bus import MainWindowSignalBus  # 不要导入类，导入实例
```

### 2. 信号连接规范

#### Controller层信号连接

```python
class SettingsController(QObject):
    def __init__(self, settings_interface: SettingsInterface):
        super().__init__()
        self._settings_interface = settings_interface
        self._connect_signals()
    
    def _connect_signals(self) -> None:
        """连接信号和槽函数"""
        # 连接UI组件信号到信号总线
        self._settings_interface.micaCard.checkedChanged.connect(
            mw_signalBus.micaEnableChanged
        )
        
        # 连接信号总线信号到处理函数
        mw_signalBus.micaEnableChanged.connect(self._on_mica_changed)
```

#### View层信号发射

```python
class MainWindow(MSFluentWindow):
    def _connectSignalToSlot(self) -> None:
        """连接窗口信号"""
        # 连接信号总线信号到窗口方法
        mw_signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
```

### 3. 信号命名规范

#### 信号名称规范

- **动作信号**: 使用动词 + 名词形式，如 `paramChanged`, `fileLoaded`
- **状态信号**: 使用形容词 + Changed形式，如 `micaEnableChanged`, `themeChanged`
- **请求信号**: 使用动词 + Requested形式，如 `restartRequested`, `saveRequested`

#### 参数规范

```python
# ✅ 推荐的信号参数设计
paramChanged = pyqtSignal(str, object)      # (参数名, 新值)
fileLoaded = pyqtSignal(str, bool)          # (文件路径, 是否成功)
themeChanged = pyqtSignal(str)              # (主题名称)

# ❌ 避免的信号参数设计
complexSignal = pyqtSignal(dict)            # 避免复杂对象，难以调试
voidSignal = pyqtSignal()                   # 尽量提供有用的参数信息
```

### 4. 架构层次使用规范

#### Model层
- **允许**: 发射数据变更相关信号
- **禁止**: 连接UI相关信号

```python
# ✅ Model层正确使用
class BaseParams(QObject):
    def _update_param(self, name: str, value: Any) -> None:
        setattr(self, name, value)
        pc_signalBus.paramChanged.emit(name, value)  # 发射数据变更信号
```

#### View层
- **允许**: 发射用户交互信号
- **允许**: 连接显示更新信号
- **禁止**: 直接处理业务逻辑

```python
# ✅ View层正确使用
class MainWindow(MSFluentWindow):
    def _connectSignalToSlot(self) -> None:
        # 连接信号总线信号到UI更新方法
        mw_signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
```

#### Controller层
- **允许**: 连接所有类型的信号
- **允许**: 发射控制流程信号
- **职责**: 协调Model和View之间的信号通信

```python
# ✅ Controller层正确使用
class SettingsController(QObject):
    def _connect_signals(self) -> None:
        # 连接View信号到信号总线
        self._view.micaCard.checkedChanged.connect(mw_signalBus.micaEnableChanged)
        
        # 连接信号总线信号到处理方法
        mw_signalBus.micaEnableChanged.connect(self._handle_mica_change)
```

## 扩展指南

### 添加新的信号总线

1. **在signal_bus.py中定义新的信号总线类**

```python
class [新功能]SignalBus(QObject):
    """[新功能]信号总线类
    
    用于管理应用程序中的[新功能]类的全局信号，实现组件间的解耦通信。
    """
    
    # [新功能]相关信号
    newSignal = pyqtSignal(参数类型)  # 信号描述

# 创建信号总线实例
[缩写]_signalBus = [新功能]SignalBus()
```

2. **在相关模块中导入和使用**

```python
from models.utils.signal_bus import [缩写]_signalBus

# 使用新的信号总线
[缩写]_signalBus.newSignal.connect(handler_function)
[缩写]_signalBus.newSignal.emit(data)
```

### 添加新信号到现有信号总线

1. **在对应的信号总线类中添加信号定义**

```python
class MainWindowSignalBus(QObject):
    # 现有信号...
    
    # 新增信号
    newFeatureSignal = pyqtSignal(参数类型)  # 新功能信号
```

2. **更新相关文档和使用示例**

## 调试和测试

### 信号连接调试

```python
# 使用Qt的信号调试功能
import os
os.environ['QT_LOGGING_RULES'] = 'qt.qml.connections.debug=true'

# 检查信号连接状态
def debug_signal_connections():
    print(f"micaEnableChanged连接数: {mw_signalBus.receivers(mw_signalBus.micaEnableChanged)}")
```

### 单元测试示例

```python
from unittest.mock import Mock, patch
import unittest

class TestSignalBus(unittest.TestCase):
    @patch('models.utils.signal_bus.mw_signalBus.micaEnableChanged')
    def test_mica_signal_emission(self, mock_signal):
        # 测试信号发射
        mw_signalBus.micaEnableChanged.emit(True)
        mock_signal.emit.assert_called_once_with(True)
```

## 最佳实践

### 1. 信号总线设计原则

- **单一职责**: 每个信号总线只管理特定功能域的信号
- **命名一致**: 遵循统一的命名规范
- **文档完整**: 为每个信号提供清晰的文档说明
- **参数明确**: 信号参数类型和含义要明确

### 2. 性能考虑

- **避免频繁信号**: 不要在循环中频繁发射信号
- **合理参数**: 避免传递大型对象作为信号参数
- **及时断开**: 在对象销毁时及时断开信号连接

### 3. 错误处理

```python
def safe_signal_connection(signal, slot):
    """安全的信号连接，包含错误处理"""
    try:
        signal.connect(slot)
    except Exception as e:
        logger.error(f"信号连接失败: {e}")
```

## 常见问题

### Q: 什么时候应该创建新的信号总线类？

A: 当新功能模块的信号与现有信号总线的职责不符时，应创建新的信号总线类。例如：数据处理模块、网络通信模块等。

### Q: 信号总线实例应该在哪里创建？

A: 所有信号总线实例都应该在`models/utils/signal_bus.py`文件中创建，确保全局唯一性。

### Q: 如何处理信号连接的循环依赖？

A: 通过Controller层进行信号路由，避免Model和View之间的直接信号连接。

### Q: 信号参数应该如何设计？

A: 优先使用基础数据类型（str, int, bool等），避免传递复杂对象。如需传递复杂数据，考虑使用数据ID或路径。

## 版本历史

- **v1.0** (2024年): 初始版本，定义基本的信号总线使用规范
- 包含MainWindowSignalBus和ParamsConfigSignalBus的使用指南

---

*文档版本：1.0*  
*创建日期：2024年*  
*最后更新：2024年*