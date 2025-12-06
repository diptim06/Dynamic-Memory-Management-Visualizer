"""
Page Replacement Algorithms Module
Implements FIFO, LRU, and Optimal page replacement algorithms.
"""

from typing import Dict, List, Optional, Deque
from enum import Enum
from collections import deque
from abc import ABC, abstractmethod


class ReplacementAlgorithm(Enum):
    """Types of page replacement algorithms."""
    FIFO = "FIFO"
    LRU = "LRU"
    OPTIMAL = "OPTIMAL"


class PageReplacementAlgorithm(ABC):
    """Abstract base class for page replacement algorithms."""
    
    def __init__(self, num_frames: int):
        """
        Initialize the replacement algorithm.
        
        Args:
            num_frames: Number of frames in physical memory
        """
        self.num_frames = num_frames
        self.frames: List[Optional[int]] = [None] * num_frames
        self.page_faults = 0
        self.page_hits = 0
    
    @abstractmethod
    def access_page(self, page_id: int, future_references: Optional[List[int]] = None) -> Dict:
        """
        Access a page, handling page replacement if needed.
        
        Args:
            page_id: Page to access
            future_references: Future page references (for Optimal algorithm)
            
        Returns:
            Dictionary with access result information
        """
        pass
    
    def is_page_loaded(self, page_id: int) -> bool:
        """
        Check if a page is currently loaded in memory.
        
        Args:
            page_id: Page identifier
            
        Returns:
            True if page is loaded, False otherwise
        """
        return page_id in self.frames
    
    def get_free_frame_index(self) -> Optional[int]:
        """
        Find a free frame slot.
        
        Returns:
            Frame index if available, None otherwise
        """
        for i, page in enumerate(self.frames):
            if page is None:
                return i
        return None
    
    def get_statistics(self) -> Dict:
        """
        Get algorithm statistics.
        
        Returns:
            Dictionary with statistics
        """
        total_accesses = self.page_faults + self.page_hits
        fault_rate = (
            self.page_faults / total_accesses
            if total_accesses > 0 else 0
        )
        hit_rate = (
            self.page_hits / total_accesses
            if total_accesses > 0 else 0
        )
        
        return {
            "page_faults": self.page_faults,
            "page_hits": self.page_hits,
            "total_accesses": total_accesses,
            "fault_rate": fault_rate,
            "hit_rate": hit_rate,
            "loaded_pages": [p for p in self.frames if p is not None]
        }
    
    def reset(self) -> None:
        """Reset algorithm state."""
        self.frames = [None] * self.num_frames
        self.page_faults = 0
        self.page_hits = 0


class FIFOReplacement(PageReplacementAlgorithm):
    """
    First-In-First-Out (FIFO) Page Replacement Algorithm.
    Replaces the page that has been in memory the longest.
    """
    
    def __init__(self, num_frames: int):
        """
        Initialize FIFO replacement algorithm.
        
        Args:
            num_frames: Number of frames in physical memory
        """
        super().__init__(num_frames)
        self.queue: Deque[int] = deque()  # Queue to track page insertion order
    
    def access_page(self, page_id: int, future_references: Optional[List[int]] = None) -> Dict:
        """
        Access a page using FIFO replacement.
        
        Args:
            page_id: Page to access
            future_references: Not used in FIFO (ignored)
            
        Returns:
            Dictionary with access result
        """
        result = {
            "page_id": page_id,
            "page_fault": False,
            "replaced_page": None,
            "frame_index": None,
            "algorithm": "FIFO"
        }
        
        # Check if page is already loaded
        if self.is_page_loaded(page_id):
            self.page_hits += 1
            result["page_fault"] = False
            # Find frame index
            for i, page in enumerate(self.frames):
                if page == page_id:
                    result["frame_index"] = i
                    break
            return result
        
        # Page fault occurred
        self.page_faults += 1
        result["page_fault"] = True
        
        # Find free frame
        free_index = self.get_free_frame_index()
        
        if free_index is not None:
            # Load page into free frame
            self.frames[free_index] = page_id
            self.queue.append(page_id)
            result["frame_index"] = free_index
        else:
            # Replace oldest page (FIFO)
            if self.queue:
                oldest_page = self.queue.popleft()
                # Find and replace the oldest page
                for i, page in enumerate(self.frames):
                    if page == oldest_page:
                        self.frames[i] = page_id
                        self.queue.append(page_id)
                        result["replaced_page"] = oldest_page
                        result["frame_index"] = i
                        break
        
        return result
    
    def reset(self) -> None:
        """Reset FIFO algorithm state."""
        super().reset()
        self.queue.clear()


class LRUReplacement(PageReplacementAlgorithm):
    """
    Least Recently Used (LRU) Page Replacement Algorithm.
    Replaces the page that has not been used for the longest time.
    """
    
    def __init__(self, num_frames: int):
        """
        Initialize LRU replacement algorithm.
        
        Args:
            num_frames: Number of frames in physical memory
        """
        super().__init__(num_frames)
        self.access_order: List[int] = []  # Track access order (most recent last)
    
    def access_page(self, page_id: int, future_references: Optional[List[int]] = None) -> Dict:
        """
        Access a page using LRU replacement.
        
        Args:
            page_id: Page to access
            future_references: Not used in LRU (ignored)
            
        Returns:
            Dictionary with access result
        """
        result = {
            "page_id": page_id,
            "page_fault": False,
            "replaced_page": None,
            "frame_index": None,
            "algorithm": "LRU"
        }
        
        # Check if page is already loaded
        if self.is_page_loaded(page_id):
            self.page_hits += 1
            result["page_fault"] = False
            # Update access order (move to end)
            if page_id in self.access_order:
                self.access_order.remove(page_id)
            self.access_order.append(page_id)
            # Find frame index
            for i, page in enumerate(self.frames):
                if page == page_id:
                    result["frame_index"] = i
                    break
            return result
        
        # Page fault occurred
        self.page_faults += 1
        result["page_fault"] = True
        
        # Find free frame
        free_index = self.get_free_frame_index()
        
        if free_index is not None:
            # Load page into free frame
            self.frames[free_index] = page_id
            self.access_order.append(page_id)
            result["frame_index"] = free_index
        else:
            # Replace least recently used page (first in access_order)
            if self.access_order:
                lru_page = self.access_order.pop(0)
                # Find and replace the LRU page
                for i, page in enumerate(self.frames):
                    if page == lru_page:
                        self.frames[i] = page_id
                        self.access_order.append(page_id)
                        result["replaced_page"] = lru_page
                        result["frame_index"] = i
                        break
        
        return result
    
    def reset(self) -> None:
        """Reset LRU algorithm state."""
        super().reset()
        self.access_order.clear()


class OptimalReplacement(PageReplacementAlgorithm):
    """
    Optimal Page Replacement Algorithm.
    Replaces the page that will be used furthest in the future (theoretical best).
    """
    
    def __init__(self, num_frames: int):
        """
        Initialize Optimal replacement algorithm.
        
        Args:
            num_frames: Number of frames in physical memory
        """
        super().__init__(num_frames)
    
    def access_page(self, page_id: int, future_references: Optional[List[int]] = None) -> Dict:
        """
        Access a page using Optimal replacement.
        
        Args:
            page_id: Page to access
            future_references: List of future page references (required for Optimal)
            
        Returns:
            Dictionary with access result
        """
        result = {
            "page_id": page_id,
            "page_fault": False,
            "replaced_page": None,
            "frame_index": None,
            "algorithm": "OPTIMAL"
        }
        
        # Check if page is already loaded
        if self.is_page_loaded(page_id):
            self.page_hits += 1
            result["page_fault"] = False
            # Find frame index
            for i, page in enumerate(self.frames):
                if page == page_id:
                    result["frame_index"] = i
                    break
            return result
        
        # Page fault occurred
        self.page_faults += 1
        result["page_fault"] = True
        
        # Find free frame
        free_index = self.get_free_frame_index()
        
        if free_index is not None:
            # Load page into free frame
            self.frames[free_index] = page_id
            result["frame_index"] = free_index
        else:
            # Replace page that will be used furthest in the future
            if future_references is None:
                future_references = []
            
            # Find which loaded page will be used furthest (or never again)
            page_to_replace = None
            max_distance = -1
            
            for loaded_page in self.frames:
                if loaded_page is None:
                    continue
                
                # Find next occurrence of this page in future references
                try:
                    next_occurrence = future_references.index(loaded_page)
                    distance = next_occurrence
                except ValueError:
                    # Page never used again - optimal candidate
                    distance = float('inf')
                    page_to_replace = loaded_page
                    break
                
                if distance > max_distance:
                    max_distance = distance
                    page_to_replace = loaded_page
            
            # If no page found (shouldn't happen), use first page
            if page_to_replace is None:
                page_to_replace = next(p for p in self.frames if p is not None)
            
            # Replace the selected page
            for i, page in enumerate(self.frames):
                if page == page_to_replace:
                    self.frames[i] = page_id
                    result["replaced_page"] = page_to_replace
                    result["frame_index"] = i
                    break
        
        return result
