"""
Advanced logging configuration and utilities for Project Browser application.
Features colored console output, structured logging, and enhanced error handling.
"""

import os
import sys
import json
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Union
from enum import Enum


class LogLevel(Enum):
    """Custom log levels for better categorization."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    SUCCESS = 25  # Between INFO and WARNING
    TRACE = 5     # Below DEBUG


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output with different colors per log level."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'SUCCESS': '\033[32;1m',  # Bright Green
        'TRACE': '\033[37m',      # White
        'RESET': '\033[0m'        # Reset color
    }
    
    def __init__(self, fmt: str = None, datefmt: str = None, use_colors: bool = True):
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors
    
    def format(self, record: logging.LogRecord) -> str:
        # Add custom level names
        if record.levelno == LogLevel.SUCCESS.value:
            record.levelname = 'SUCCESS'
        elif record.levelno == LogLevel.TRACE.value:
            record.levelname = 'TRACE'
        
        # Format the message
        message = super().format(record)
        
        # Apply colors if enabled and supported
        if self.use_colors and self._supports_color():
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            reset_color = self.COLORS['RESET']
            return f"{color}{message}{reset_color}"
        
        return message
    
    def _supports_color(self) -> bool:
        """Check if the terminal supports color output."""
        return (
            hasattr(sys.stdout, 'isatty') and sys.stdout.isatty() and
            os.environ.get('TERM') != 'dumb' and
            not os.environ.get('NO_COLOR')
        )


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def __init__(self, fmt: str = None, datefmt: str = None):
        super().__init__(fmt, datefmt)
        self.datefmt = datefmt or '%Y-%m-%d %H:%M:%S'
    
    def format(self, record: logging.LogRecord) -> str:
        # Create structured log entry
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).strftime(self.datefmt),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        # Add custom fields
        if hasattr(record, 'extra') and record.extra:
            log_entry.update(record.extra)
        
        return json.dumps(log_entry, ensure_ascii=False, default=str)


class MSR605Logger:
    """Advanced logger for MSR605 application with enhanced features."""
    
    def __init__(self, name: str = 'MSR605', log_level: int = logging.INFO):
        self.name = name
        self.log_level = log_level
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.logger.propagate = False
        
        # Register custom log levels
        self._register_custom_levels()
        
        # Configuration
        self.config = {
            'logs_dir': Path('logs'),
            'max_file_size': 10 * 1024 * 1024,  # 10MB
            'backup_count': 30,
            'console_colors': True,
            'json_logging': False,
            'include_caller_info': True
        }
    
    def _register_custom_levels(self):
        """Register custom log levels."""
        if not hasattr(logging, 'SUCCESS'):
            logging.addLevelName(LogLevel.SUCCESS.value, 'SUCCESS')
            logging.SUCCESS = LogLevel.SUCCESS.value
        
        if not hasattr(logging, 'TRACE'):
            logging.addLevelName(LogLevel.TRACE.value, 'TRACE')
            logging.TRACE = LogLevel.TRACE.value
    
    def setup_handlers(self, **kwargs):
        """Setup all log handlers with configuration options."""
        # Update config with provided kwargs
        self.config.update(kwargs)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create logs directory
        self.config['logs_dir'].mkdir(exist_ok=True)
        
        # Setup file handlers
        self._setup_file_handlers()
        
        # Setup console handler
        self._setup_console_handler()
    
    def _setup_file_handlers(self):
        """Setup file handlers for different log types."""
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Main log file (daily rotation)
        main_log_file = self.config['logs_dir'] / f'MSR605_{current_date}.log'
        main_handler = self._create_file_handler(
            main_log_file,
            'main',
            TimedRotatingFileHandler,
            when='midnight',
            interval=1,
            backupCount=self.config['backup_count']
        )
        
        # Error log file (size-based rotation)
        error_log_file = self.config['logs_dir'] / f'MSR605_errors_{current_date}.log'
        error_handler = self._create_file_handler(
            error_log_file,
            'error',
            RotatingFileHandler,
            maxBytes=self.config['max_file_size'],
            backupCount=10
        )
        error_handler.setLevel(logging.ERROR)
        
        # JSON log file if enabled
        if self.config['json_logging']:
            json_log_file = self.config['logs_dir'] / f'MSR605_json_{current_date}.log'
            json_handler = self._create_file_handler(
                json_log_file,
                'json',
                TimedRotatingFileHandler,
                when='midnight',
                interval=1,
                backupCount=self.config['backup_count']
            )
            json_handler.setFormatter(JSONFormatter(datefmt='%Y-%m-%d %H:%M:%S'))
            self.logger.addHandler(json_handler)
    
    def _create_file_handler(self, log_file: Path, handler_type: str, handler_class, **kwargs):
        """Create a file handler with error handling."""
        try:
            handler = handler_class(log_file, encoding='utf-8', **kwargs)
            
            if handler_type == 'json':
                formatter = JSONFormatter(datefmt='%Y-%m-%d %H:%M:%S')
            else:
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
            
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            return handler
            
        except Exception as e:
            print(f"Failed to create {handler_type} file handler: {e}", file=sys.stderr)
            return None
    
    def _setup_console_handler(self):
        """Setup console handler with colored output."""
        try:
            console_handler = logging.StreamHandler(sys.stdout)
            
            if self.config['include_caller_info']:
                console_formatter = ColoredFormatter(
                    '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    datefmt='%H:%M:%S',
                    use_colors=self.config['console_colors']
                )
            else:
                console_formatter = ColoredFormatter(
                    '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S',
                    use_colors=self.config['console_colors']
                )
            
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
            
        except Exception as e:
            print(f"Failed to create console handler: {e}", file=sys.stderr)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self._log_with_extra(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self._log_with_extra(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self._log_with_extra(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self._log_with_extra(logging.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self._log_with_extra(logging.CRITICAL, message, **kwargs)
    
    def success(self, message: str, **kwargs):
        """Log success message."""
        self._log_with_extra(LogLevel.SUCCESS.value, message, **kwargs)
    
    def trace(self, message: str, **kwargs):
        """Log trace message."""
        self._log_with_extra(LogLevel.TRACE.value, message, **kwargs)
    
    def exception(self, message: str, **kwargs):
        """Log exception with traceback."""
        self._log_with_extra(logging.ERROR, message, exc_info=True, **kwargs)
    
    def _log_with_extra(self, level: int, message: str, **kwargs):
        """Log message with extra context."""
        extra = kwargs.pop('extra', {})
        exc_info = kwargs.pop('exc_info', False)
        
        if extra:
            # Create a custom LogRecord with extra fields
            record = self.logger.makeRecord(
                self.logger.name, level, 
                kwargs.get('pathname', ''), kwargs.get('lineno', 0),
                message, (), None, None, extra
            )
            record.extra = extra
            self.logger.handle(record)
        else:
            self.logger.log(level, message, exc_info=exc_info, extra=extra)
    
    def set_level(self, level: Union[int, str]):
        """Set logging level."""
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(level)
        self.log_level = level
    
    def get_logger(self) -> logging.Logger:
        """Get the underlying logger instance."""
        return self.logger


class LoggerManager:
    """Singleton manager for logger instances."""
    
    _instances = {}
    
    @classmethod
    def get_logger(cls, name: str = 'MSR605', **kwargs) -> MSR605Logger:
        """Get or create a logger instance."""
        if name not in cls._instances:
            cls._instances[name] = MSR605Logger(name)
            cls._instances[name].setup_handlers(**kwargs)
        return cls._instances[name]
    
    @classmethod
    def configure_all(cls, **kwargs):
        """Configure all logger instances."""
        for logger in cls._instances.values():
            logger.setup_handlers(**kwargs)


# Convenience functions for backward compatibility
def setup_logger(name: str = 'MSR605', log_level: int = logging.INFO, **kwargs) -> MSR605Logger:
    """Setup and return a configured logger instance."""
    return LoggerManager.get_logger(name, log_level=log_level, **kwargs)


def get_logger(name: str = None) -> MSR605Logger:
    """Get a logger instance."""
    if name:
        return LoggerManager.get_logger(f'MSR605.{name}')
    return LoggerManager.get_logger('MSR605')


# Create default logger instance
logger = setup_logger()


# Add custom methods to the logger for convenience
def add_custom_methods(logger_instance: MSR605Logger):
    """Add custom methods to logger instance."""
    def log_performance(self, operation: str, duration: float, **kwargs):
        """Log performance metrics."""
        self.info(f"Performance: {operation} took {duration:.3f}s", 
                 extra={'operation': operation, 'duration': duration, **kwargs})
    
    def log_user_action(self, action: str, user: str = None, **kwargs):
        """Log user actions."""
        self.info(f"User action: {action}", 
                 extra={'action': action, 'user': user or 'unknown', **kwargs})
    
    def log_api_call(self, method: str, endpoint: str, status_code: int = None, **kwargs):
        """Log API calls."""
        self.info(f"API {method} {endpoint}", 
                 extra={'method': method, 'endpoint': endpoint, 'status_code': status_code, **kwargs})
    
    # Bind methods to instance
    import types
    logger_instance.log_performance = types.MethodType(log_performance, logger_instance)
    logger_instance.log_user_action = types.MethodType(log_user_action, logger_instance)
    logger_instance.log_api_call = types.MethodType(log_api_call, logger_instance)


# Add custom methods to default logger
add_custom_methods(logger)
