# 组件 API（components & base）

组件层提供可复用的 UI 控件与设置卡片，统一交互与样式。

## 设置卡片（views/components）

- `options_group_setting_card.py`
  - `OptionsGroupSettingCard`
    - 概要：带互斥编号与“智能交换”机制的选项卡片
    - 信号：`optionChanged(int, object)` — 选项值变更（值、当前卡片实例）
    - 用法：
      ```python
      card = OptionsGroupSettingCard(title="编号选择", content="选择唯一编号")
      card.optionChanged.connect(lambda v, c: print(v))
      ```

- `icon_options_setting_card.py`
  - `IconOptionsSettingCard`
    - 概要：带图标的方向选项卡片（水平/垂直），与配置项联动
    - 行为：点击更新配置、标签文本与发出选项改变信号

- `time_flip_setting_card.py`
  - `TimeFlipSettingCard`
    - 概要：时间处理策略卡片，支持“保留/丢弃”与“重叠/顺序”等策略
    - 关键方法：`setProcValue(str)`, `setReserveValue(str)` — 设置处理与保留策略

## 基础控件（views/base）

- `step_slider.py`
  - `StepSlider`
    - 概要：支持分度对齐的滑块控件
    - 关键：`setStep(int)`，所有滑动与取值对齐到步长

- `range_slider.py`
  - `RangeSlider`
    - 概要：双向范围选择滑块，支持分度值与动画句柄
    - 信号：`rangeChanged(int, int)` — 最小值与最大值变更

- 其它：`subtitle_widget.py`, `icon_option_widget.py`, `test_radiobutton.py` 等提供统一的样式与交互体验。

## 交互容器（views/modules/scroll_module）

- `scroll_container.py`
  - 概要：四面板横向滚动容器，支持锚点吸附与滚轮平滑滚动
  - 核心：锚点计算、动画吸附、滚轮事件处理

---

> 注：组件 API 以当前实现与测试用例为依据，后续完善将补充更细粒度的属性说明与事件序列。