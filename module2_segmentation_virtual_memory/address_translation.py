"""
Address Translation Module
Provides utilities for address translation in different memory management schemes.
"""

from typing import Optional, Tuple


def logical_to_physical_paging(
    logical_address: int,
    page_size: int,
    page_table: dict,
    frame_size: int
) -> Optional[Tuple[int, int, bool]]:
    """
    Translate logical address to physical address using paging.
    
    Args:
        logical_address: Logical memory address
        page_size: Size of each page in bytes
        page_table: Dictionary mapping page_id -> frame_id
        frame_size: Size of each frame in bytes
        
    Returns:
        Tuple of (physical_address, offset, page_fault) or None if invalid
        page_fault is True if page is not in memory
    """
    page_id = logical_address // page_size
    offset = logical_address % page_size
    
    if page_id not in page_table:
        return None  # Invalid page
    
    frame_id = page_table[page_id]
    
    if frame_id is None:
        # Page not in memory - page fault
        return (None, offset, True)
    
    physical_address = (frame_id * frame_size) + offset
    return (physical_address, offset, False)


def logical_to_physical_segmentation(
    segment_id: int,
    offset: int,
    segment_table: dict
) -> Optional[Tuple[int, bool, str]]:
    """
    Translate logical address (segment, offset) to physical address using segmentation.
    
    Args:
        segment_id: Segment identifier
        offset: Offset within segment
        segment_table: Dictionary mapping segment_id -> (base, limit)
        
    Returns:
        Tuple of (physical_address, valid, error_message) or None if segment not found
    """
    if segment_id not in segment_table:
        return None
    
    base, limit = segment_table[segment_id]
    
    if offset < 0 or offset >= limit:
        return (None, False, f"Offset {offset} out of bounds (limit: {limit})")
    
    physical_address = base + offset
    return (physical_address, True, "")


def split_address(address: int, page_size: int) -> Tuple[int, int]:
    """
    Split an address into page number and offset.
    
    Args:
        address: Memory address
        page_size: Size of each page
        
    Returns:
        Tuple of (page_number, offset)
    """
    page_number = address // page_size
    offset = address % page_size
    return (page_number, offset)


def combine_address(page_number: int, offset: int, page_size: int) -> int:
    """
    Combine page number and offset into a full address.
    
    Args:
        page_number: Page number
        offset: Offset within page
        page_size: Size of each page
        
    Returns:
        Full memory address
    """
    return (page_number * page_size) + offset
