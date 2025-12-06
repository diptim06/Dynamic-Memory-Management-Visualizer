"""
Segmentation Engine Module
Implements segmentation with segment tables and address translation.
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum


class SegmentStatus(Enum):
    """Status of a segment."""
    ALLOCATED = "ALLOCATED"
    FREE = "FREE"


class Segment:
    """Represents a memory segment (code, data, stack, heap)."""
    
    def __init__(self, segment_id: int, name: str, base: int, limit: int):
        """
        Initialize a segment.
        
        Args:
            segment_id: Unique segment identifier
            name: Segment name (e.g., "CODE", "DATA", "STACK")
            base: Base address (physical)
            limit: Segment size in bytes
        """
        self.segment_id = segment_id
        self.name = name
        self.base = base
        self.limit = limit
        self.status = SegmentStatus.ALLOCATED
    
    def contains_address(self, offset: int) -> bool:
        """
        Check if offset is within segment bounds.
        
        Args:
            offset: Logical offset within segment
            
        Returns:
            True if offset is valid, False otherwise
        """
        return 0 <= offset < self.limit
    
    def translate(self, offset: int) -> Optional[int]:
        """
        Translate logical offset to physical address.
        
        Args:
            offset: Logical offset within segment
            
        Returns:
            Physical address or None if out of bounds
        """
        if self.contains_address(offset):
            return self.base + offset
        return None
    
    def __repr__(self) -> str:
        return f"Segment(id={self.segment_id}, name={self.name}, " \
               f"base=0x{self.base:X}, limit={self.limit})"


class SegmentTable:
    """Manages segment table for a process."""
    
    def __init__(self, process_id: int):
        """
        Initialize segment table for a process.
        
        Args:
            process_id: Process identifier
        """
        self.process_id = process_id
        self.segments: Dict[int, Segment] = {}
    
    def add_segment(self, segment_id: int, name: str, base: int, limit: int) -> Segment:
        """
        Add a segment to the table.
        
        Args:
            segment_id: Segment identifier
            name: Segment name
            base: Base address
            limit: Segment size
            
        Returns:
            Created Segment object
        """
        segment = Segment(segment_id, name, base, limit)
        self.segments[segment_id] = segment
        return segment
    
    def get_segment(self, segment_id: int) -> Optional[Segment]:
        """
        Get segment by ID.
        
        Args:
            segment_id: Segment identifier
            
        Returns:
            Segment or None if not found
        """
        return self.segments.get(segment_id)
    
    def translate_address(self, segment_id: int, offset: int) -> Tuple[Optional[int], bool, str]:
        """
        Translate logical address (segment, offset) to physical address.
        
        Args:
            segment_id: Segment identifier
            offset: Offset within segment
            
        Returns:
            Tuple of (physical_address, valid, error_message)
        """
        segment = self.get_segment(segment_id)
        
        if segment is None:
            return (None, False, f"Segment {segment_id} does not exist")
        
        if not segment.contains_address(offset):
            return (None, False, f"Offset {offset} out of bounds (limit: {segment.limit})")
        
        physical_addr = segment.translate(offset)
        return (physical_addr, True, "")
    
    def get_stats(self) -> Dict:
        """
        Get segment table statistics.
        
        Returns:
            Dictionary with statistics
        """
        total_size = sum(seg.limit for seg in self.segments.values())
        return {
            "process_id": self.process_id,
            "num_segments": len(self.segments),
            "total_size": total_size,
            "segments": [
                {
                    "id": seg.segment_id,
                    "name": seg.name,
                    "base": seg.base,
                    "limit": seg.limit
                }
                for seg in self.segments.values()
            ]
        }
    
    def visualize_table(self) -> List[Dict]:
        """
        Generate visualization data for segment table.
        
        Returns:
            List of dictionaries with segment information
        """
        return [
            {
                "segment_id": seg.segment_id,
                "name": seg.name,
                "base": seg.base,
                "limit": seg.limit,
                "status": seg.status.value
            }
            for seg in sorted(self.segments.values(), key=lambda s: s.segment_id)
        ]


class SegmentationEngine:
    """
    Main segmentation engine that manages processes and their segment tables.
    
    Usage:
        engine = SegmentationEngine()
        engine.create_process(process_id=1)
        engine.add_segment(process_id=1, segment_id=0, name="CODE", base=0x1000, limit=1024)
        physical_addr, valid, msg = engine.translate_address(process_id=1, segment_id=0, offset=0x100)
    """
    
    def __init__(self):
        """Initialize the segmentation engine."""
        self.segment_tables: Dict[int, SegmentTable] = {}
        self.next_base_address: int = 0x1000
        self.access_attempts: int = 0
        self.access_successes: int = 0
        self.bounds_violations: int = 0
    
    def create_process(self, process_id: int) -> bool:
        """
        Create a new process with an empty segment table.
        
        Args:
            process_id: Unique process identifier
            
        Returns:
            True if process created successfully, False otherwise
        """
        if process_id in self.segment_tables:
            return False  # Process already exists
        
        self.segment_tables[process_id] = SegmentTable(process_id)
        return True
    
    def remove_process(self, process_id: int) -> bool:
        """
        Remove a process and its segment table.
        
        Args:
            process_id: Process identifier
            
        Returns:
            True if process removed successfully, False otherwise
        """
        if process_id not in self.segment_tables:
            return False
        
        del self.segment_tables[process_id]
        return True
    
    def add_segment(
        self,
        process_id: int,
        segment_id: int,
        name: str,
        size: int,
        base: Optional[int] = None
    ) -> bool:
        """
        Add a segment to a process's segment table.
        
        Args:
            process_id: Process identifier
            segment_id: Segment identifier
            name: Segment name
            size: Segment size in bytes
            base: Base address (auto-assigned if None)
            
        Returns:
            True if segment added successfully, False otherwise
        """
        if process_id not in self.segment_tables:
            return False
        
        segment_table = self.segment_tables[process_id]
        
        # Auto-assign base address if not provided
        if base is None:
            base = self.next_base_address
            self.next_base_address += size + 0x100  # Add gap between segments
        
        segment_table.add_segment(segment_id, name, base, size)
        return True
    
    def translate_address(
        self,
        process_id: int,
        segment_id: int,
        offset: int
    ) -> Tuple[Optional[int], bool, str]:
        """
        Translate logical address (segment, offset) to physical address.
        
        Args:
            process_id: Process identifier
            segment_id: Segment identifier
            offset: Offset within segment
            
        Returns:
            Tuple of (physical_address, valid, error_message)
        """
        self.access_attempts += 1
        
        if process_id not in self.segment_tables:
            return (None, False, f"Process {process_id} does not exist")
        
        segment_table = self.segment_tables[process_id]
        physical_addr, valid, error_msg = segment_table.translate_address(segment_id, offset)
        
        if valid:
            self.access_successes += 1
        else:
            self.bounds_violations += 1
        
        return (physical_addr, valid, error_msg)
    
    def calculate_fragmentation(self, process_id: int) -> Dict[str, float]:
        """
        Calculate internal and external fragmentation for a process.
        
        Args:
            process_id: Process identifier
            
        Returns:
            Dictionary with fragmentation metrics
        """
        if process_id not in self.segment_tables:
            return {"internal": 0.0, "external": 0.0}
        
        segment_table = self.segment_tables[process_id]
        segments = list(segment_table.segments.values())
        
        if not segments:
            return {"internal": 0.0, "external": 0.0}
        
        # Sort segments by base address
        sorted_segments = sorted(segments, key=lambda s: s.base)
        
        # Calculate internal fragmentation (sum of unused space within segments)
        # For simplicity, assume segments are fully utilized
        internal_frag = 0.0  # Would need actual usage data
        
        # Calculate external fragmentation (gaps between segments)
        external_frag = 0.0
        for i in range(len(sorted_segments) - 1):
            current_end = sorted_segments[i].base + sorted_segments[i].limit
            next_base = sorted_segments[i + 1].base
            if next_base > current_end:
                external_frag += (next_base - current_end)
        
        total_size = sum(seg.limit for seg in segments)
        internal_pct = (internal_frag / total_size * 100) if total_size > 0 else 0
        external_pct = (external_frag / total_size * 100) if total_size > 0 else 0
        
        return {
            "internal_bytes": internal_frag,
            "external_bytes": external_frag,
            "internal_percent": internal_pct,
            "external_percent": external_pct
        }
    
    def get_statistics(self) -> Dict:
        """
        Get engine statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            "total_processes": len(self.segment_tables),
            "access_attempts": self.access_attempts,
            "access_successes": self.access_successes,
            "bounds_violations": self.bounds_violations,
            "success_rate": (
                self.access_successes / self.access_attempts
                if self.access_attempts > 0 else 0
            )
        }
    
    def reset(self) -> None:
        """Reset the engine to initial state."""
        self.segment_tables.clear()
        self.next_base_address = 0x1000
        self.access_attempts = 0
        self.access_successes = 0
        self.bounds_violations = 0
