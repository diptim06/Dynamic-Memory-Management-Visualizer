"""
Page Table Module
Manages page tables for processes, mapping logical pages to physical frames.
"""

from typing import Dict, List, Optional
from enum import Enum


class PageStatus(Enum):
    """Status of a page in the page table."""
    NOT_PRESENT = "NOT_PRESENT"
    PRESENT = "PRESENT"
    MODIFIED = "MODIFIED"
    REFERENCED = "REFERENCED"


class PageTableEntry:
    """Represents a single entry in a page table."""
    
    def __init__(self, page_id: int):
        """
        Initialize a page table entry.
        
        Args:
            page_id: Logical page number
        """
        self.page_id = page_id
        self.frame_id: Optional[int] = None
        self.status = PageStatus.NOT_PRESENT
        self.valid = False
        self.present_bit = False  # P bit: page is in physical memory
        self.modified_bit = False  # M bit: page has been modified
        self.referenced_bit = False  # R bit: page has been referenced
        self.protection_bits: int = 0  # Protection flags (read, write, execute)
    
    def map_to_frame(self, frame_id: int) -> None:
        """
        Map this page to a physical frame.
        
        Args:
            frame_id: Physical frame identifier
        """
        self.frame_id = frame_id
        self.present_bit = True
        self.valid = True
        self.status = PageStatus.PRESENT
    
    def unmap_frame(self) -> None:
        """Remove the mapping to physical frame."""
        self.frame_id = None
        self.present_bit = False
        self.status = PageStatus.NOT_PRESENT
    
    def mark_modified(self) -> None:
        """Mark page as modified."""
        self.modified_bit = True
        self.status = PageStatus.MODIFIED
    
    def mark_referenced(self) -> None:
        """Mark page as referenced."""
        self.referenced_bit = True
        if self.status == PageStatus.PRESENT:
            self.status = PageStatus.REFERENCED
    
    def clear_referenced(self) -> None:
        """Clear referenced bit."""
        self.referenced_bit = False
        if self.status == PageStatus.REFERENCED:
            self.status = PageStatus.PRESENT
    
    def __repr__(self) -> str:
        return f"PTE(page={self.page_id}, frame={self.frame_id}, " \
               f"present={self.present_bit}, valid={self.valid})"


class PageTable:
    """Manages page table for a process."""
    
    def __init__(self, process_id: int, page_size: int = 4096):
        """
        Initialize a page table for a process.
        
        Args:
            process_id: Process identifier
            page_size: Size of each logical page in bytes
        """
        self.process_id = process_id
        self.page_size = page_size
        self.entries: Dict[int, PageTableEntry] = {}
    
    def get_entry(self, page_id: int) -> Optional[PageTableEntry]:
        """
        Get page table entry for a given page.
        
        Args:
            page_id: Logical page number
            
        Returns:
            PageTableEntry or None if page doesn't exist
        """
        return self.entries.get(page_id)
    
    def create_page(self, page_id: int) -> PageTableEntry:
        """
        Create a new page table entry.
        
        Args:
            page_id: Logical page number
            
        Returns:
            Created PageTableEntry
        """
        if page_id not in self.entries:
            self.entries[page_id] = PageTableEntry(page_id)
        return self.entries[page_id]
    
    def map_page_to_frame(self, page_id: int, frame_id: int) -> bool:
        """
        Map a logical page to a physical frame.
        
        Args:
            page_id: Logical page number
            frame_id: Physical frame identifier
            
        Returns:
            True if mapping successful, False otherwise
        """
        entry = self.get_entry(page_id)
        if entry is None:
            entry = self.create_page(page_id)
        
        entry.map_to_frame(frame_id)
        return True
    
    def unmap_page(self, page_id: int) -> bool:
        """
        Unmap a page from its frame.
        
        Args:
            page_id: Logical page number
            
        Returns:
            True if unmapping successful, False otherwise
        """
        entry = self.get_entry(page_id)
        if entry:
            entry.unmap_frame()
            return True
        return False
    
    def get_mapped_pages(self) -> List[int]:
        """
        Get all pages currently mapped to frames.
        
        Returns:
            List of page IDs that are present in memory
        """
        return [
            page_id for page_id, entry in self.entries.items()
            if entry.present_bit
        ]
    
    def translate_address(self, logical_address: int) -> Optional[Tuple[int, int]]:
        """
        Translate logical address to (page_id, offset).
        
        Args:
            logical_address: Logical memory address
            
        Returns:
            Tuple of (page_id, offset) or None if invalid
        """
        page_id = logical_address // self.page_size
        offset = logical_address % self.page_size
        return (page_id, offset)
    
    def get_page_for_address(self, logical_address: int) -> Optional[PageTableEntry]:
        """
        Get page table entry for a logical address.
        
        Args:
            logical_address: Logical memory address
            
        Returns:
            PageTableEntry or None if page not found
        """
        page_id, _ = self.translate_address(logical_address)
        return self.get_entry(page_id)
    
    def get_stats(self) -> Dict:
        """
        Get page table statistics.
        
        Returns:
            Dictionary with statistics
        """
        total_pages = len(self.entries)
        mapped_pages = len(self.get_mapped_pages())
        unmapped_pages = total_pages - mapped_pages
        
        return {
            "process_id": self.process_id,
            "total_pages": total_pages,
            "mapped_pages": mapped_pages,
            "unmapped_pages": unmapped_pages,
            "page_size": self.page_size
        }
    
    def visualize_table(self) -> List[Dict]:
        """
        Generate visualization data for page table.
        
        Returns:
            List of dictionaries with page table entry information
        """
        visualization = []
        for page_id in sorted(self.entries.keys()):
            entry = self.entries[page_id]
            visualization.append({
                "page_id": page_id,
                "frame_id": entry.frame_id,
                "present": entry.present_bit,
                "modified": entry.modified_bit,
                "referenced": entry.referenced_bit,
                "status": entry.status.value
            })
        return visualization
