#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志管理器
使用loguru提供日志记录功能，采用单例模式确保全局唯一性
"""

import sys
from pathlib import Path
from loguru import logger
from typing import Optional
import threading
from datetime import datetime


class LogManager:
    """日志管理器单例类
    
    使用单例模式确保整个应用程序中只有一个日志管理器实例。
    提供统一的日志配置和管理接口。
    
    Attributes:
        _instance: 单例实例
        _lock: 线程锁
        _initialized: 初始化标记
        _log_level: 当前日志级别
        _log_file: 日志文件路径
    """
    
    _instance: Optional['LogManager'] = None
    _lock: threading.Lock = threading.Lock()
    
    def __new__(cls) -> 'LogManager':
        """单例模式实现
        
        Returns:
            LogManager实例
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """初始化日志管理器
        
        只在第一次创建实例时执行初始化。
        """
        if not hasattr(self, '_initialized'):
            self._initialized = False
            self._log_level = "INFO"
            self._log_file: Optional[Path] = None
    
    def setup(self, log_level: str = "INFO", log_file: Optional[str] = None) -> None:
        """设置日志系统
        
        Args:
            log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: 日志文件路径，默认为项目根目录下的logs/app.log
            
        Raises:
            ValueError: 当日志级别无效时抛出
        """
        if self._initialized:
            logger.warning("日志系统已经初始化，跳过重复初始化")
            return
        
        # 验证日志级别
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if log_level.upper() not in valid_levels:
            raise ValueError(f"无效的日志级别: {log_level}，有效级别: {valid_levels}")
        
        self._log_level = log_level.upper()
        
        # 移除默认的handler
        logger.remove()
        
        # 设置日志格式
        console_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        )
        
        file_format = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
        
        # 添加控制台handler
        logger.add(
            sink=sys.stderr,
            format=console_format,
            level=self._log_level,
            colorize=True
        )
        
        # 设置日志文件路径
        if log_file is None:
            project_root = Path(__file__).parent.parent.parent
            log_dir = project_root / "logs"
            log_dir.mkdir(exist_ok=True)
            # 创建以当前时间命名的日志文件
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            self._log_file = log_dir / f"debug_{current_time}.log"
        else:
            self._log_file = Path(log_file)
            self._log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 添加普通日志文件handler
        logger.add(
            sink=self._log_file,
            format=file_format,
            level=self._log_level,
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            encoding="utf-8"
        )
        
        # 添加错误日志文件handler（也使用时间戳命名）
        # error_log_file = self._log_file.parent / f"error_{current_time}.log"
        # logger.add(
        #     sink=error_log_file,
        #     format=file_format,
        #     level="ERROR",
        #     rotation="10 MB",
        #     retention="30 days",
        #     compression="zip",
        #     encoding="utf-8"
        # )
        
        self._initialized = True
        logger.info(f"日志系统初始化完成，级别: {self._log_level}，文件: {self._log_file}")
    
    def get_logger(self, name: Optional[str] = None) -> logger:
        """获取logger实例
        
        Args:
            name: logger名称，默认为None
            
        Returns:
            配置好的logger实例
            
        Raises:
            RuntimeError: 当日志系统未初始化时抛出
        """
        if not self._initialized:
            raise RuntimeError("日志系统未初始化，请先调用setup()方法")
        
        if name:
            return logger.bind(name=name)
        return logger
    
    def set_level(self, level: str) -> None:
        """动态设置日志级别
        
        Args:
            level: 新的日志级别
            
        Raises:
            ValueError: 当日志级别无效时抛出
            RuntimeError: 当日志系统未初始化时抛出
        """
        if not self._initialized:
            raise RuntimeError("日志系统未初始化，请先调用setup()方法")
        
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if level.upper() not in valid_levels:
            raise ValueError(f"无效的日志级别: {level}，有效级别: {valid_levels}")
        
        old_level = self._log_level
        self._log_level = level.upper()
        
        # 重新配置所有handler的级别
        # 移除现有的handlers
        logger.remove()
        
        # 重新添加handlers with new level
        console_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        )
        
        file_format = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
        
        # 添加控制台handler
        logger.add(
            sink=sys.stderr,
            format=console_format,
            level=self._log_level,
            colorize=True
        )
        
        # 添加文件handler
        if self._log_file:
            logger.add(
                sink=self._log_file,
                format=file_format,
                level=self._log_level,
                rotation="10 MB",
                retention="7 days",
                compression="zip",
                encoding="utf-8"
            )
        
        logger.info(f"日志级别已从 {old_level} 更新为: {self._log_level}")
    
    @property
    def is_initialized(self) -> bool:
        """检查日志系统是否已初始化
        
        Returns:
            True表示已初始化，False表示未初始化
        """
        return self._initialized
    
    @property
    def log_level(self) -> str:
        """获取当前日志级别
        
        Returns:
            当前日志级别
        """
        return self._log_level
    
    @property
    def log_file(self) -> Optional[Path]:
        """获取日志文件路径
        
        Returns:
            日志文件路径
        """
        return self._log_file


# 全局日志管理器实例
_log_manager: Optional[LogManager] = None


def get_log_manager() -> LogManager:
    """获取全局日志管理器实例
    
    Returns:
        LogManager单例实例
    """
    global _log_manager
    if _log_manager is None:
        _log_manager = LogManager()
    return _log_manager


def setup_logger(log_level: str = "INFO", log_file: Optional[str] = None) -> None:
    """便捷的日志系统设置函数
    
    Args:
        log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 日志文件路径，默认为项目根目录下的logs/app.log
        
    Raises:
        ValueError: 当日志级别无效时抛出
    """
    manager = get_log_manager()
    manager.setup(log_level=log_level, log_file=log_file)


def get_logger(name: Optional[str] = None) -> logger:
    """便捷的获取logger函数
    
    Args:
        name: logger名称，默认为None
        
    Returns:
        配置好的logger实例
        
    Raises:
        RuntimeError: 当日志系统未初始化时抛出
    """
    manager = get_log_manager()
    return manager.get_logger(name=name)


class LoggerMixin:
    """日志混入类，为其他类提供日志功能"""

    @property
    def logger(self):
        """获取logger实例"""
        return logger.bind(name=self.__class__.__name__)

    def log_method_call(self, method_name: str, **kwargs):
        """记录方法调用"""
        args_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
        self.logger.debug(f"调用方法 {method_name}({args_str})")

    def log_error(self, error: Exception, context: str = ""):
        """记录错误信息"""
        error_msg = f"{context}: {str(error)}" if context else str(error)
        self.logger.error(error_msg)
        self.logger.exception("详细错误堆栈:")
