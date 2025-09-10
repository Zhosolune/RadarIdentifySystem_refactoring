#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DPI配置测试脚本
用于验证DPI设置的配置映射是否正确
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from models.config.app_config import _app_cfg

def test_dpi_config():
    """
    测试DPI配置的设置和获取
    
    Returns:
        bool: 测试是否通过
    """
    print("=== DPI配置测试 ===")
    
    # 测试默认值
    current_dpi = _app_cfg.get(_app_cfg.dpiScale)
    print(f"当前DPI设置: {current_dpi}")
    
    # 测试所有可用选项
    available_options = _app_cfg.dpiScale.validator.values if hasattr(_app_cfg.dpiScale.validator, 'values') else ["100%", "125%", "150%", "175%", "200%", "Auto"]
    print(f"可用DPI选项: {available_options}")
    
    # 测试设置不同的DPI值
    test_values = ["100%", "125%", "150%", "175%", "200%", "Auto"]
    
    for test_value in test_values:
        try:
            # 设置DPI值
            _app_cfg.set(_app_cfg.dpiScale, test_value)
            # 获取设置的值
            retrieved_value = _app_cfg.get(_app_cfg.dpiScale)
            
            if retrieved_value == test_value:
                print(f"✓ {test_value} -> {retrieved_value} (成功)")
            else:
                print(f"✗ {test_value} -> {retrieved_value} (失败)")
                return False
                
        except Exception as e:
            print(f"✗ 设置 {test_value} 时出错: {e}")
            return False
    
    # 测试百分比转换逻辑
    print("\n=== 百分比转换测试 ===")
    test_conversions = {
        "100%": 1.0,
        "125%": 1.25,
        "150%": 1.5,
        "175%": 1.75,
        "200%": 2.0
    }
    
    for percent_str, expected_value in test_conversions.items():
        if percent_str.endswith('%'):
            scale_value = float(percent_str[:-1]) / 100.0
        else:
            scale_value = float(percent_str)
            
        if abs(scale_value - expected_value) < 0.001:
            print(f"✓ {percent_str} -> {scale_value} (预期: {expected_value})")
        else:
            print(f"✗ {percent_str} -> {scale_value} (预期: {expected_value})")
            return False
    
    print("\n=== 所有测试通过 ===")
    return True

if __name__ == "__main__":
    success = test_dpi_config()
    sys.exit(0 if success else 1)