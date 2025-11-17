"""Error handling and recovery utilities for the MSR605 application."""

import time
import functools
from typing import Any, Callable, Optional, Type, TypeVar, cast
import serial
import logging
from pathlib import Path

from .logging_config import log_exception, logger

# Type variable for generic function typing
F = TypeVar('F', bound=Callable[..., Any])

class MSRError(Exception):
    """Base exception class for MSR605 related errors."""
    
    def __init__(self, message: str, error_code: Optional[int] = None, **kwargs):
        """Initialize the exception.
        
        Args:
            message: Error message
            error_code: Optional error code
            **kwargs: Additional context information
        """
        self.message = message
        self.error_code = error_code
        self.context = kwargs
        super().__init__(self.message)


class CardReadError(MSRError):
    """Raised when there is an error reading from the card."""
    pass


class CardWriteError(MSRError):
    """Raised when there is an error writing to the card."""
    pass


class DeviceConnectionError(MSRError):
    """Raised when there is an error connecting to the device."""
    pass


class ValidationError(MSRError):
    """Raised when there is a validation error."""
    pass


class RecoveryStrategy:
    """Base class for recovery strategies."""
    
    def __init__(self, max_retries: int = 3, backoff_factor: float = 0.5):
        """Initialize the recovery strategy.
        
        Args:
            max_retries: Maximum number of retry attempts
            backoff_factor: Factor for exponential backoff between retries
        """
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    def should_retry(self, attempt: int, exception: Exception) -> bool:
        """Determine if a retry should be attempted.
        
        Args:
            attempt: Current attempt number (1-based)
            exception: The exception that was raised
            
        Returns:
            bool: True if a retry should be attempted, False otherwise
        """
        return attempt <= self.max_retries
    
    def get_delay(self, attempt: int) -> float:
        """Get the delay before the next retry.
        
        Args:
            attempt: Current attempt number (1-based)
            
        Returns:
            float: Delay in seconds
        """
        return self.backoff_factor * (2 ** (attempt - 1))
    
    def before_retry(self, attempt: int, exception: Exception) -> None:
        """Perform any actions before a retry.
        
        Args:
            attempt: Current attempt number (1-based)
            exception: The exception that was raised
        """
        logger.warning(
            f"Retry {attempt}/{self.max_retries} after error: {str(exception)}",
            extra={
                'retry_attempt': attempt,
                'max_retries': self.max_retries,
                'exception': str(exception),
                'exception_type': exception.__class__.__name__
            }
        )
        time.sleep(self.get_delay(attempt))


class RetryOnException(RecoveryStrategy):
    """Retry strategy that retries on specific exceptions."""
    
    def __init__(self, exceptions: tuple[Type[Exception], ...], **kwargs):
        """Initialize the retry strategy.
        
        Args:
            exceptions: Tuple of exception types to retry on
            **kwargs: Additional arguments for the base class
        """
        super().__init__(**kwargs)
        self.exceptions = exceptions
    
    def should_retry(self, attempt: int, exception: Exception) -> bool:
        return (
            attempt <= self.max_retries and
            any(isinstance(exception, exc) for exc in self.exceptions)
        )


def retry(retry_strategy: Optional[RecoveryStrategy] = None, **retry_kwargs):
    """Decorator to retry a function on failure.
    
    Args:
        retry_strategy: Recovery strategy to use
        **retry_kwargs: Arguments to pass to the default recovery strategy
    """
    if retry_strategy is None:
        retry_strategy = RecoveryStrategy(**retry_kwargs)
    
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(1, retry_strategy.max_retries + 2):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if not retry_strategy.should_retry(attempt, e):
                        break
                    
                    # Log the retry
                    retry_strategy.before_retry(attempt, e)
            
            # If we get here, all retries failed
            log_exception(
                logger,
                last_exception,
                {
                    'function': func.__name__,
                    'max_retries': retry_strategy.max_retries,
                    'attempts': attempt
                }
            )
            raise last_exception
            
        return cast(F, wrapper)
    return decorator


def handle_serial_errors(func: F) -> F:
    """Decorator to handle common serial port errors."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except serial.SerialException as e:
            error_msg = f"Serial communication error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise DeviceConnectionError(error_msg) from e
        except serial.SerialTimeoutException as e:
            error_msg = "Serial communication timeout"
            logger.error(error_msg, exc_info=True)
            raise DeviceConnectionError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise
    return cast(F, wrapper)


def recover_from_failure(
    func: Optional[Callable] = None,
    recovery_func: Optional[Callable] = None,
    recovery_args: Optional[tuple] = None,
    recovery_kwargs: Optional[dict] = None,
    exceptions: tuple[Type[Exception], ...] = (Exception,),
    log_errors: bool = True
):
    """Decorator to recover from failures by calling a recovery function.
    
    Args:
        func: The function to decorate
        recovery_func: Function to call on failure
        recovery_args: Positional arguments to pass to recovery_func
        recovery_kwargs: Keyword arguments to pass to recovery_func
        exceptions: Tuple of exception types to catch
        log_errors: Whether to log errors
    """
    if recovery_args is None:
        recovery_args = ()
    if recovery_kwargs is None:
        recovery_kwargs = {}
    
    def decorator(f: F) -> F:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except exceptions as e:
                if log_errors:
                    log_exception(logger, e, {
                        'function': f.__name__,
                        'recovery_function': recovery_func.__name__ if recovery_func else None
                    })
                
                if recovery_func is not None:
                    try:
                        recovery_func(*recovery_args, **recovery_kwargs)
                    except Exception as recovery_error:
                        if log_errors:
                            log_exception(
                                logger, 
                                recovery_error,
                                {'context': 'Error in recovery function'}
                            )
                raise
        
        return cast(F, wrapper)
    
    if func is not None:
        return decorator(func)
    return decorator


class ErrorContext:
    """Context manager for error handling with additional context."""
    
    def __init__(self, context: Optional[dict] = None, logger: Optional[logging.Logger] = None):
        """Initialize the context manager.
        
        Args:
            context: Additional context information
            logger: Logger instance to use
        """
        self.context = context or {}
        self.logger = logger or logging.getLogger(__name__)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            log_exception(self.logger, exc_val, self.context)
        return False  # Don't suppress the exception
    
    def add_context(self, **kwargs):
        """Add context information."""
        self.context.update(kwargs)
        return self


# Example usage:
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Example of using the retry decorator
    @retry(max_retries=3, backoff_factor=0.5)
    def risky_operation():
        if datetime.now().second % 3 == 0:
            raise ValueError("Something went wrong!")
        return "Success!"
    
    # Example of using the error context
    def process_file(file_path):
        with ErrorContext({"file_path": file_path}):
            with open(file_path) as f:
                return f.read()
    
    # Example of using recover_from_failure
    def recover():
        print("Recovering from failure...")
    
    @recover_from_failure(recovery_func=recover, exceptions=(FileNotFoundError,))
    def read_file(file_path):
        with open(file_path) as f:
            return f.read()
