#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志管理器测试
测试LogManager的单例模式和基本功能
"""

import sys
import os
# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

import tempfile
from pathlib import Path
from models.utils.log_manager import LogManager, get_log_manager, setup_logger, get_logger

def test_singleton_pattern():
    """测试单例模式
    
    验证LogManager确实是单例模式，多次创建返回同一个实例。
    """
    print("\n=== 测试单例模式 ===")
    
    # 创建多个实例
    manager1 = LogManager()
    manager2 = LogManager()
    manager3 = get_log_manager()
    
    # 验证是否为同一个实例
    print(f"manager1 id: {id(manager1)}")
    print(f"manager2 id: {id(manager2)}")
    print(f"manager3 id: {id(manager3)}")
    
    assert manager1 is manager2, "单例模式失败：manager1 和 manager2 不是同一个实例"
    assert manager2 is manager3, "单例模式失败：manager2 和 manager3 不是同一个实例"
    
    print("✓ 单例模式测试通过")


def test_log_setup_and_logging():
    """测试日志设置和记录功能
    
    测试日志系统的初始化、不同级别的日志记录和文件输出。
    """
    print("\n=== 测试日志设置和记录 ===")
    
    # 获取当前管理器状态
    manager = get_log_manager()
    
    if manager.is_initialized:
        print("日志系统已初始化，测试现有配置...")
        
        # 获取logger并测试不同级别的日志
        logger = get_logger("test_module")
        
        logger.debug("这是一条调试信息")
        logger.info("这是一条信息")
        logger.warning("这是一条警告")
        logger.error("这是一条错误")
        logger.critical("这是一条严重错误")
        
        # 验证日志文件是否存在（如果已配置）
        if manager.log_file and manager.log_file.exists():
            print(f"✓ 日志文件存在: {manager.log_file}")
            
            # 验证错误日志文件
            error_log_file = manager.log_file.parent / "error.log"
            if error_log_file.exists():
                print(f"✓ 错误日志文件存在: {error_log_file}")
        
        print("✓ 日志记录功能测试通过")
    else:
        # 如果未初始化，进行完整的初始化测试
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"
            
            # 设置日志系统
            setup_logger(log_level="DEBUG", log_file=str(log_file))
            
            # 获取logger并测试不同级别的日志
            logger = get_logger("test_module")
            
            logger.debug("这是一条调试信息")
            logger.info("这是一条信息")
            logger.warning("这是一条警告")
            logger.error("这是一条错误")
            logger.critical("这是一条严重错误")
            
            # 验证日志文件是否创建
            assert log_file.exists(), f"日志文件未创建: {log_file}"
            
            # 验证错误日志文件是否创建
            error_log_file = log_file.parent / "error.log"
            assert error_log_file.exists(), f"错误日志文件未创建: {error_log_file}"
            
            # 读取日志文件内容
            log_content = log_file.read_text(encoding='utf-8')
            print(f"日志文件内容预览:\n{log_content[:200]}...")
            
            # 验证日志内容包含预期的信息
            assert "这是一条调试信息" in log_content, "日志文件中未找到调试信息"
            assert "这是一条信息" in log_content, "日志文件中未找到普通信息"
            assert "这是一条警告" in log_content, "日志文件中未找到警告信息"
            
            print("✓ 日志设置和记录测试通过")


def test_log_level_validation():
    """测试日志级别验证
    
    测试无效日志级别的处理和动态级别设置。
    """
    print("\n=== 测试日志级别验证 ===")
    
    manager = get_log_manager()
    
    # 测试无效日志级别
    try:
        manager.set_level("INVALID_LEVEL")
        assert False, "应该抛出ValueError异常"
    except ValueError as e:
        print(f"✓ 正确捕获无效日志级别异常: {e}")
    
    # 测试有效日志级别设置
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    for level in valid_levels:
        manager.set_level(level)
        assert manager.log_level == level, f"日志级别设置失败: 期望{level}，实际{manager.log_level}"
        print(f"✓ 日志级别 {level} 设置成功")


def test_manager_properties():
    """测试管理器属性
    
    测试LogManager的各种属性访问。
    """
    print("\n=== 测试管理器属性 ===")
    
    manager = get_log_manager()
    
    # 测试初始化状态
    print(f"初始化状态: {manager.is_initialized}")
    print(f"当前日志级别: {manager.log_level}")
    print(f"日志文件路径: {manager.log_file}")
    
    assert isinstance(manager.is_initialized, bool), "is_initialized应该返回布尔值"
    assert isinstance(manager.log_level, str), "log_level应该返回字符串"
    
    print("✓ 管理器属性测试通过")


def test_repeated_initialization():
    """测试重复初始化
    
    验证重复调用setup方法不会导致问题。
    """
    print("\n=== 测试重复初始化 ===")
    
    manager = get_log_manager()
    
    # 多次调用setup
    with tempfile.TemporaryDirectory() as temp_dir:
        log_file = Path(temp_dir) / "repeat_test.log"
        
        setup_logger(log_level="INFO", log_file=str(log_file))
        setup_logger(log_level="DEBUG", log_file=str(log_file))  # 第二次调用
        setup_logger(log_level="WARNING", log_file=str(log_file))  # 第三次调用
        
        # 验证管理器状态
        assert manager.is_initialized, "管理器应该保持初始化状态"
        
        print("✓ 重复初始化测试通过")


def main():
    """主测试函数
    
    运行所有测试用例。
    """
    print("开始日志管理器测试...")
    
    try:
        test_singleton_pattern()
        test_log_setup_and_logging()
        test_log_level_validation()
        test_manager_properties()
        test_repeated_initialization()
        
        print("\n🎉 所有测试通过！")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)