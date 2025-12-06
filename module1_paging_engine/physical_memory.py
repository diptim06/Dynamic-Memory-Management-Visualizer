"""
Physical Memory Module
Simulates physical memory as a collection of frames.
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum


class FrameStatus(Enum):
    """Status of a physical memory frame."""
    FREE = "FREE"
    ALLOCATED = "ALLOCATED"


class Frame:
    """Represents a single physical memory frame."""
    
    def __init__(self, frame_id: int, size: int = 4096):
        """
        Initialize a frame.
        
        Args:
            frame_id: Unique identifier for the frame
            size: Size of the frame in bytes (default: 4KB)
        """
        self.frame_id = frame_id
        self.size = size
        self.status = FrameStatus.FREE
        self.process_id: Optional[int] = None
        self.page_id: Optional[int] = None
        self.allocated_size: int = 0
    
    def allocate(self, process_id: int, page_id: int, size: int) -> bool:
        """
        Allocate this frame to a process page.
        
        Args:
            process_id: ID of the process
            page_id: ID of the page
            size: Size to allocate
            
        Returns:
            True if allocation successful, False otherwise
        """
        if self.status == FrameStatus.FREE and size <= self.size:
            self.status = FrameStatus.ALLOCATED
            self.process_id = process_id
            self.page_id = page_id
            self.allocated_size = min(size, self.size)
            return True
        return False
    
    def deallocate(self) -> bool:
        """
        Free this frame.
        
        Returns:
            True if deallocation successful, False otherwise
        """
        if self.status == FrameStatus.ALLOCATED:
            self.status = FrameStatus.FREE
            self.process_id = None
            self.page_id = None
            self.allocated_size = 0
            return True
        return False
    
    def __repr__(self) -> str:
        return f"Frame(id={self.frame_id}, status={self.status.value}, " \
               f"process={self.process_id}, page={self.page_id})"


class PhysicalMemory:
    """Manages physical memory as a collection of frames."""
    
    def __init__(self, num_frames: int = 16, frame_size: int = 4096):
        """
        Initialize physical memory.
        
        Args:
            num_frames: Number of physical frames
            frame_size: Size of each frame in bytes
        """
        self.num_frames = num_frames
        self.frame_size = frame_size
        self.frames: List[Frame] = [
            Frame(i, frame_size) for i in range(num_frames)
        ]
        self._next_frame_id = num_frames
    
    def get_frame(self, frame_id: int) -> Optional[Frame]:
        """
        Get a frame by ID.
        
        Args:
            frame_id: Frame identifier
            
        Returns:
            Frame object or None if not found
        """
        if 0 <= frame_id < len(self.frames):
            return self.frames[frame_id]
        return None
    
    def get_free_frames(self) -> List[Frame]:
        """
        Get all free frames.
        
        Returns:
            List of free frames
        """
        return [frame for frame in self.frames if frame.status == FrameStatus.FREE]
    
    def get_allocated_frames(self) -> List[Frame]:
        """
        Get all allocated frames.
        
        Returns:
            List of allocated frames
        """
        return [frame for frame in self.frames if frame.status == FrameStatus.ALLOCATED]
    
    def get_frame_status(self) -> Dict[str, int]:
        """
        Get memory statistics.
        
        Returns:
            Dictionary with memory statistics
        """
        free_count = len(self.get_free_frames())
        allocated_count = len(self.get_allocated_frames())
        total_size = self.num_frames * self.frame_size
        used_size = allocated_count * self.frame_size
        
        return {
            "total_frames": self.num_frames,
            "free_frames": free_count,
            "allocated_frames": allocated_count,
            "total_size": total_size,
            "used_size": used_size,
            "free_size": total_size - used_size,
            "utilization_percent": (used_size / total_size * 100) if total_size > 0 else 0
        }
    
    def visualize_memory(self) -> List[Dict]:
        """
        Generate visualization data for memory layout.
        
        Returns:
            List of dictionaries with frame information for visualization
        """
        visualization = []
        for frame in self.frames:
            visualization.append({
                "frame_id": frame.frame_id,
                "status": frame.status.value,
                "process_id": frame.process_id,
                "page_id": frame.page_id,
                "size": frame.size,
                "allocated_size": frame.allocated_size
            })
        return visualization
    
    def reset(self) -> None:
        """Reset all frames to free state."""
        for frame in self.frames:
            frame.deallocate()
