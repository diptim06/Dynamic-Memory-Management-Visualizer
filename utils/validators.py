"""
Validators Module
Provides validation functions for user inputs and data.
"""

from typing import Optional, Tuple


def validate_positive_int(value: int, name: str = "Value", min_value: int = 1) -> Tuple[bool, Optional[str]]:
    """
    Validate that a value is a positive integer.
    
    Args:
        value: Value to validate
        name: Name of the value (for error messages)
        min_value: Minimum allowed value
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(value, int):
        return (False, f"{name} must be an integer")
    
    if value < min_value:
        return (False, f"{name} must be at least {min_value}")
    
    return (True, None)


def validate_address(address: int, max_address: Optional[int] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate a memory address.
    
    Args:
        address: Memory address to validate
        max_address: Maximum allowed address (optional)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(address, int):
        return (False, "Address must be an integer")
    
    if address < 0:
        return (False, "Address cannot be negative")
    
    if max_address is not None and address >= max_address:
        return (False, f"Address {address} exceeds maximum {max_address}")
    
    return (True, None)


def validate_process_id(process_id: int) -> Tuple[bool, Optional[str]]:
    """
    Validate a process ID.
    
    Args:
        process_id: Process identifier
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(process_id, int):
        return (False, "Process ID must be an integer")
    
    if process_id < 0:
        return (False, "Process ID cannot be negative")
    
    return (True, None)


def validate_page_id(page_id: int) -> Tuple[bool, Optional[str]]:
    """
    Validate a page ID.
    
    Args:
        page_id: Page identifier
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(page_id, int):
        return (False, "Page ID must be an integer")
    
    if page_id < 0:
        return (False, "Page ID cannot be negative")
    
    return (True, None)


def validate_segment_id(segment_id: int) -> Tuple[bool, Optional[str]]:
    """
    Validate a segment ID.
    
    Args:
        segment_id: Segment identifier
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(segment_id, int):
        return (False, "Segment ID must be an integer")
    
    if segment_id < 0:
        return (False, "Segment ID cannot be negative")
    
    return (True, None)
