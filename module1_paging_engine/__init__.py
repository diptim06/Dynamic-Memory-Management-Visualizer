"""
Module 1: Paging Engine
Provides paging simulation with physical memory, page tables, and allocation strategies.
"""

from .paging_engine import PagingSimulator
from .allocator import AllocationStrategy

__all__ = ['PagingSimulator', 'AllocationStrategy']
