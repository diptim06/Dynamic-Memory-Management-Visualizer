"""
Logger Module
Provides logging functionality for the application.
"""

import logging
import sys
from typing import Optional


_logger: Optional[logging.Logger] = None


def setup_logger(name: str = "MemoryVisualizer", level: int = logging.INFO) -> logging.Logger:
    """
    Setup and configure the application logger.
    
    Args:
        name: Logger name
        level: Logging level (default: INFO)
        
    Returns:
        Configured logger instance
    """
    global _logger
    
    if _logger is not None:
        return _logger
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    _logger = logger
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get the logger instance.
    
    Args:
        name: Optional logger name (uses default if None)
        
    Returns:
        Logger instance
    """
    if _logger is None:
        return setup_logger(name or "MemoryVisualizer")
    return _logger
