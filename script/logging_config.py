"""Logging configuration for the MSR605 application."""

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import json
import traceback
from datetime import datetime

# Log directory setup
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
JSON_LOG_FORMAT = """{
    "timestamp": "%(asctime)s",
    "name": "%(name)s",
    "level": "%(levelname)s",
    "message": "%(message)s",
    "module": "%(module)s",
    "function": "%(funcName)s",
    "line": %(lineno)d,
    "thread": "%(threadName)s",
    "process": "%(processName)s"
}"""

class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs logs in JSON format."""
    
    def format(self, record):
        log_record = {
            'timestamp': self.formatTime(record, self.datefmt),
            'name': record.name,
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'thread': record.threadName,
            'process': record.processName,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)
            
        # Add any extra attributes
        for key, value in record.__dict__.items():
            if key not in ('args', 'asctime', 'created', 'exc_info', 'exc_text', 
                          'filename', 'funcName', 'id', 'levelname', 'levelno', 
                          'lineno', 'module', 'msecs', 'message', 'msg', 'name', 
                          'pathname', 'process', 'processName', 'relativeCreated',
                          'stack_info', 'thread', 'threadName'):
                log_record[key] = value
                
        return json.dumps(log_record, ensure_ascii=False)


def configure_logger(
    name: str = 'msr605',
    level: int = logging.INFO,
    log_to_console: bool = True,
    log_to_file: bool = True,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    json_format: bool = False
) -> logging.Logger:
    """Configure and return a logger with the specified settings.
    
    Args:
        name: Logger name
        level: Logging level (e.g., logging.INFO, logging.DEBUG)
        log_to_console: Whether to log to console
        log_to_file: Whether to log to file
        max_file_size: Maximum log file size in bytes
        backup_count: Number of backup log files to keep
        json_format: Whether to use JSON format for logs
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Create formatter
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(LOG_FORMAT)
    
    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_to_file:
        log_file = LOG_DIR / f"{name}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def log_exception(logger: logging.Logger, exception: Exception, context: Optional[Dict[str, Any]] = None) -> None:
    """Log an exception with context information.
    
    Args:
        logger: Logger instance
        exception: The exception that was raised
        context: Additional context information
    """
    exc_info = (type(exception), exception, exception.__traceback__)
    exc_traceback = ''.join(traceback.format_exception(*exc_info))
    
    log_data = {
        'exception': str(exception),
        'exception_type': exception.__class__.__name__,
        'traceback': exc_traceback,
        'context': context or {}
    }
    
    logger.error("Exception occurred", extra=log_data)


def log_operation(logger: logging.Logger, operation: str, **kwargs) -> None:
    """Log an operation with its parameters and result.
    
    Args:
        logger: Logger instance
        operation: Name of the operation
        **kwargs: Operation parameters and result
    """
    logger.info(f"Operation: {operation}", extra={'operation': operation, **kwargs})


# Default logger instance
logger = configure_logger('msr605', logging.INFO)
