"""
Module 2: Segmentation and Virtual Memory
Provides segmentation simulation, virtual memory, and page replacement algorithms.
"""

from .segmentation_engine import SegmentationEngine
from .virtual_memory import VirtualMemoryManager, ReplacementAlgorithm
from .page_replacement import PageReplacementAlgorithm, FIFOReplacement, LRUReplacement, OptimalReplacement

__all__ = [
    'SegmentationEngine',
    'VirtualMemoryManager',
    'ReplacementAlgorithm',
    'PageReplacementAlgorithm',
    'FIFOReplacement',
    'LRUReplacement',
    'OptimalReplacement'
]
