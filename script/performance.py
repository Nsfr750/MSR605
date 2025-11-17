"""performance.py

This module provides performance optimization utilities for the MSR605 application,
including caching, batching, and other performance-enhancing techniques.
"""

import time
import functools
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, cast
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import threading
import queue
import hashlib
import json
from pathlib import Path

# Type variable for generic function typing
F = TypeVar('F', bound=Callable[..., Any])

@dataclass
class CacheEntry:
    """Represents a cache entry with expiration."""
    value: Any
    expires_at: float

class LRUCache:
    """A simple LRU (Least Recently Used) cache implementation."""
    
    def __init__(self, max_size: int = 1000, ttl: Optional[float] = None):
        """Initialize the cache.
        
        Args:
            max_size: Maximum number of items to store in the cache
            ttl: Time-to-live in seconds for cache entries (None for no expiration)
        """
        self.max_size = max_size
        self.ttl = ttl
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = threading.RLock()
    
    def get(self, key: str) -> Any:
        """Get a value from the cache."""
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return None
                
            # Check if entry has expired
            if self.ttl is not None and entry.expires_at < time.time():
                del self._cache[key]
                return None
                
            # Move to end (most recently used)
            value = entry.value
            del self._cache[key]
            self._cache[key] = entry
            return value
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Set a value in the cache."""
        with self._lock:
            expires_at = time.time() + (ttl if ttl is not None else (self.ttl or float('inf')))
            
            # If key exists, remove it first
            if key in self._cache:
                del self._cache[key]
            # If cache is full, remove the least recently used item
            elif len(self._cache) >= self.max_size:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
                
            self._cache[key] = CacheEntry(value=value, expires_at=expires_at)
    
    def clear(self) -> None:
        """Clear the cache."""
        with self._lock:
            self._cache.clear()
    
    def cleanup(self) -> None:
        """Remove expired entries from the cache."""
        if self.ttl is None:
            return
            
        with self._lock:
            now = time.time()
            expired_keys = [k for k, v in self._cache.items() if v.expires_at < now]
            for key in expired_keys:
                del self._cache[key]


def cache_result(max_size: int = 1000, ttl: Optional[float] = None) -> Callable[[F], F]:
    """Decorator to cache function results.
    
    Args:
        max_size: Maximum number of items to store in the cache
        ttl: Time-to-live in seconds for cache entries (None for no expiration)
    """
    def decorator(func: F) -> F:
        cache = LRUCache(max_size=max_size, ttl=ttl)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a cache key from function name and arguments
            key_parts = [func.__name__] + list(args) + [f"{k}={v}" for k, v in sorted(kwargs.items())]
            key = hashlib.md5(json.dumps(key_parts, sort_keys=True).encode()).hexdigest()
            
            # Try to get from cache
            result = cache.get(key)
            if result is not None:
                return result
                
            # Call the function and cache the result
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
            
        return cast(F, wrapper)
    return decorator


class BatchProcessor:
    """Processes operations in batches for better performance."""
    
    def __init__(self, batch_size: int = 10, max_delay: float = 0.1):
        """Initialize the batch processor.
        
        Args:
            batch_size: Maximum number of operations per batch
            max_delay: Maximum time to wait before processing a batch (seconds)
        """
        self.batch_size = batch_size
        self.max_delay = max_delay
        self._queue = queue.Queue()
        self._current_batch = []
        self._timer = None
        self._lock = threading.Lock()
        self._running = True
        self._worker_thread = threading.Thread(target=self._process_batches, daemon=True)
        self._worker_thread.start()
    
    def add_operation(self, operation: Any) -> None:
        """Add an operation to the batch."""
        with self._lock:
            self._current_batch.append(operation)
            
            # If we've reached the batch size, process immediately
            if len(self._current_batch) >= self.batch_size:
                self._process_batch()
            # Otherwise, start/restart the timer
            else:
                if self._timer is not None:
                    self._timer.cancel()
                self._timer = threading.Timer(self.max_delay, self._process_batch)
                self._timer.daemon = True
                self._timer.start()
    
    def _process_batch(self) -> None:
        """Process the current batch of operations."""
        with self._lock:
            if not self._current_batch:
                return
                
            batch = self._current_batch
            self._current_batch = []
            self._timer = None
            
            # Add to the processing queue
            self._queue.put(batch)
    
    def _process_batches(self) -> None:
        """Background thread that processes batches."""
        while self._running or not self._queue.empty():
            try:
                batch = self._queue.get(timeout=0.1)
                if batch is None:  # Shutdown signal
                    break
                    
                # Process the batch (this would be overridden by subclasses)
                self.process_batch(batch)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error processing batch: {e}")
    
    def process_batch(self, batch: List[Any]) -> None:
        """Process a batch of operations. Subclasses should override this."""
        raise NotImplementedError("Subclasses must implement process_batch")
    
    def shutdown(self) -> None:
        """Shut down the batch processor."""
        self._running = False
        self._queue.put(None)  # Signal the worker thread to exit
        self._worker_thread.join()


class CardOperationBatcher(BatchProcessor):
    """Specialized batch processor for card operations."""
    
    def __init__(self, card_reader, batch_size: int = 5, max_delay: float = 0.2):
        """Initialize the card operation batcher.
        
        Args:
            card_reader: The CardReader instance to use for operations
            batch_size: Maximum number of operations per batch
            max_delay: Maximum time to wait before processing a batch (seconds)
        """
        super().__init__(batch_size=batch_size, max_delay=max_delay)
        self.card_reader = card_reader
    
    def process_batch(self, batch: List[Dict]) -> None:
        """Process a batch of card operations."""
        for operation in batch:
            try:
                op_type = operation.get('type')
                if op_type == 'read':
                    self.card_reader.read_card(
                        detect_format=operation.get('detect_format', True),
                        validate=operation.get('validate', True)
                    )
                elif op_type == 'write':
                    self.card_reader.write_card(
                        tracks=operation['tracks'],
                        format_override=operation.get('format')
                    )
                # Add more operation types as needed
                    
            except Exception as e:
                print(f"Error processing operation {operation}: {e}")


def measure_execution_time(func: F) -> F:
    """Decorator to measure and log function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            end_time = time.perf_counter()
            duration = (end_time - start_time) * 1000  # Convert to milliseconds
            print(f"{func.__name__} executed in {duration:.2f}ms")
    return cast(F, wrapper)


def memoize(max_size: int = 1000, ttl: Optional[float] = None) -> Callable[[F], F]:
    """A more advanced memoization decorator with max size and TTL."""
    cache = LRUCache(max_size=max_size, ttl=ttl)
    
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a cache key from function name and arguments
            key_parts = [func.__name__] + list(args) + [f"{k}={v}" for k, v in sorted(kwargs.items())]
            key = hashlib.md5(json.dumps(key_parts, sort_keys=True).encode()).hexdigest()
            
            # Try to get from cache
            result = cache.get(key)
            if result is not None:
                return result
                
            # Call the function and cache the result
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
            
        # Add cache management methods to the wrapper
        wrapper.cache_clear = cache.clear
        wrapper.cache_cleanup = cache.cleanup
        
        return cast(F, wrapper)
    return decorator
