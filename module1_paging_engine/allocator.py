"""
Memory Allocator Module
Implements various memory allocation strategies: First Fit, Best Fit, Next Fit.
"""

from typing import List, Optional
from enum import Enum
from module1_paging_engine.physical_memory import Frame, FrameStatus


class AllocationStrategy(Enum):
    """Types of allocation strategies."""
    FIRST_FIT = "FIRST_FIT"
    BEST_FIT = "BEST_FIT"
    NEXT_FIT = "NEXT_FIT"


class MemoryAllocator:
    """Allocates physical frames using different strategies."""
    
    def __init__(self, strategy: AllocationStrategy = AllocationStrategy.FIRST_FIT):
        """
        Initialize allocator with a strategy.
        
        Args:
            strategy: Allocation strategy to use
        """
        self.strategy = strategy
        self._next_fit_start: int = 0  # For Next Fit strategy
    
    def allocate(
        self,
        frames: List[Frame],
        process_id: int,
        page_id: int,
        size: int
    ) -> Optional[int]:
        """
        Allocate a frame using the configured strategy.
        
        Args:
            frames: List of physical frames
            process_id: Process requesting allocation
            page_id: Page to allocate
            size: Size needed (should be <= frame_size)
            
        Returns:
            Frame ID if allocation successful, None otherwise
        """
        if self.strategy == AllocationStrategy.FIRST_FIT:
            return self._first_fit(frames, process_id, page_id, size)
        elif self.strategy == AllocationStrategy.BEST_FIT:
            return self._best_fit(frames, process_id, page_id, size)
        elif self.strategy == AllocationStrategy.NEXT_FIT:
            return self._next_fit(frames, process_id, page_id, size)
        return None
    
    def _first_fit(
        self,
        frames: List[Frame],
        process_id: int,
        page_id: int,
        size: int
    ) -> Optional[int]:
        """
        First Fit: Allocate the first free frame that can accommodate the request.
        
        Args:
            frames: List of physical frames
            process_id: Process requesting allocation
            page_id: Page to allocate
            size: Size needed
            
        Returns:
            Frame ID if allocation successful, None otherwise
        """
        for frame in frames:
            if frame.status == FrameStatus.FREE and size <= frame.size:
                if frame.allocate(process_id, page_id, size):
                    return frame.frame_id
        return None
    
    def _best_fit(
        self,
        frames: List[Frame],
        process_id: int,
        page_id: int,
        size: int
    ) -> Optional[int]:
        """
        Best Fit: Allocate the smallest free frame that can accommodate the request.
        
        Args:
            frames: List of physical frames
            process_id: Process requesting allocation
            page_id: Page to allocate
            size: Size needed
            
        Returns:
            Frame ID if allocation successful, None otherwise
        """
        best_frame: Optional[Frame] = None
        best_waste = float('inf')
        
        for frame in frames:
            if frame.status == FrameStatus.FREE and size <= frame.size:
                waste = frame.size - size
                if waste < best_waste:
                    best_waste = waste
                    best_frame = frame
        
        if best_frame and best_frame.allocate(process_id, page_id, size):
            return best_frame.frame_id
        return None
    
    def _next_fit(
        self,
        frames: List[Frame],
        process_id: int,
        page_id: int,
        size: int
    ) -> Optional[int]:
        """
        Next Fit: Similar to First Fit, but starts searching from the last allocated position.
        
        Args:
            frames: List of physical frames
            process_id: Process requesting allocation
            page_id: Page to allocate
            size: Size needed
            
        Returns:
            Frame ID if allocation successful, None otherwise
        """
        # Search from last position to end
        for i in range(self._next_fit_start, len(frames)):
            frame = frames[i]
            if frame.status == FrameStatus.FREE and size <= frame.size:
                if frame.allocate(process_id, page_id, size):
                    self._next_fit_start = (i + 1) % len(frames)
                    return frame.frame_id
        
        # Wrap around: search from beginning to last position
        for i in range(self._next_fit_start):
            frame = frames[i]
            if frame.status == FrameStatus.FREE and size <= frame.size:
                if frame.allocate(process_id, page_id, size):
                    self._next_fit_start = (i + 1) % len(frames)
                    return frame.frame_id
        
        return None
    
    def deallocate(self, frames: List[Frame], frame_id: int) -> bool:
        """
        Deallocate a frame.
        
        Args:
            frames: List of physical frames
            frame_id: Frame to deallocate
            
        Returns:
            True if deallocation successful, False otherwise
        """
        if 0 <= frame_id < len(frames):
            return frames[frame_id].deallocate()
        return False
    
    def set_strategy(self, strategy: AllocationStrategy) -> None:
        """
        Change allocation strategy.
        
        Args:
            strategy: New allocation strategy
        """
        self.strategy = strategy
        if strategy == AllocationStrategy.NEXT_FIT:
            self._next_fit_start = 0
