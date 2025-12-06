"""
Paging Engine Module
Main simulator for paging memory management.
"""

from typing import Dict, List, Optional, Tuple
from module1_paging_engine.physical_memory import PhysicalMemory, Frame
from module1_paging_engine.page_table import PageTable, PageTableEntry
from module1_paging_engine.allocator import MemoryAllocator, AllocationStrategy


class PagingSimulator:
    """
    Main paging simulator that coordinates physical memory, page tables, and allocation.
    
    Usage:
        simulator = PagingSimulator(num_frames=16, frame_size=4096)
        simulator.create_process(process_id=1, num_pages=5)
        simulator.allocate_page(process_id=1, page_id=0)
        physical_addr = simulator.translate_address(process_id=1, logical_address=0x1000)
    """
    
    def __init__(
        self,
        num_frames: int = 16,
        frame_size: int = 4096,
        allocation_strategy: AllocationStrategy = AllocationStrategy.FIRST_FIT
    ):
        """
        Initialize the paging simulator.
        
        Args:
            num_frames: Number of physical frames
            frame_size: Size of each frame in bytes
            allocation_strategy: Strategy for frame allocation
        """
        self.physical_memory = PhysicalMemory(num_frames, frame_size)
        self.page_tables: Dict[int, PageTable] = {}
        self.allocator = MemoryAllocator(allocation_strategy)
        self.page_faults: int = 0
        self.successful_translations: int = 0
        self.processes: Dict[int, Dict] = {}
    
    def create_process(self, process_id: int, num_pages: int = 0) -> bool:
        """
        Create a new process with a page table.
        
        Args:
            process_id: Unique process identifier
            num_pages: Initial number of pages to create (optional)
            
        Returns:
            True if process created successfully, False otherwise
        """
        if process_id in self.page_tables:
            return False  # Process already exists
        
        page_table = PageTable(process_id, self.physical_memory.frame_size)
        self.page_tables[process_id] = page_table
        
        # Pre-create page entries if specified
        for i in range(num_pages):
            page_table.create_page(i)
        
        self.processes[process_id] = {
            "num_pages": num_pages,
            "allocated_pages": 0
        }
        
        return True
    
    def remove_process(self, process_id: int) -> bool:
        """
        Remove a process and free all its allocated frames.
        
        Args:
            process_id: Process identifier
            
        Returns:
            True if process removed successfully, False otherwise
        """
        if process_id not in self.page_tables:
            return False
        
        page_table = self.page_tables[process_id]
        
        # Free all allocated frames
        for page_id in page_table.get_mapped_pages():
            entry = page_table.get_entry(page_id)
            if entry and entry.frame_id is not None:
                frame = self.physical_memory.get_frame(entry.frame_id)
                if frame:
                    frame.deallocate()
        
        # Remove page table
        del self.page_tables[process_id]
        if process_id in self.processes:
            del self.processes[process_id]
        
        return True
    
    def allocate_page(
        self,
        process_id: int,
        page_id: int,
        size: Optional[int] = None
    ) -> Optional[int]:
        """
        Allocate a physical frame for a process page.
        
        Args:
            process_id: Process identifier
            page_id: Logical page number
            size: Size to allocate (defaults to frame_size)
            
        Returns:
            Frame ID if allocation successful, None otherwise
        """
        if process_id not in self.page_tables:
            return None
        
        page_table = self.page_tables[process_id]
        entry = page_table.get_entry(page_id)
        
        # If page doesn't exist, create it
        if entry is None:
            entry = page_table.create_page(page_id)
        
        # If already mapped, return existing frame
        if entry.present_bit and entry.frame_id is not None:
            return entry.frame_id
        
        # Allocate a new frame
        alloc_size = size if size is not None else self.physical_memory.frame_size
        frame_id = self.allocator.allocate(
            self.physical_memory.frames,
            process_id,
            page_id,
            alloc_size
        )
        
        if frame_id is not None:
            entry.map_to_frame(frame_id)
            frame = self.physical_memory.get_frame(frame_id)
            if frame:
                frame.allocate(process_id, page_id, alloc_size)
            if process_id in self.processes:
                self.processes[process_id]["allocated_pages"] += 1
            return frame_id
        
        return None
    
    def deallocate_page(self, process_id: int, page_id: int) -> bool:
        """
        Deallocate a page and free its frame.
        
        Args:
            process_id: Process identifier
            page_id: Logical page number
            
        Returns:
            True if deallocation successful, False otherwise
        """
        if process_id not in self.page_tables:
            return False
        
        page_table = self.page_tables[process_id]
        entry = page_table.get_entry(page_id)
        
        if entry is None or not entry.present_bit or entry.frame_id is None:
            return False
        
        # Free the frame
        frame_id = entry.frame_id
        frame = self.physical_memory.get_frame(frame_id)
        if frame:
            frame.deallocate()
        
        # Unmap the page
        entry.unmap_frame()
        
        if process_id in self.processes:
            self.processes[process_id]["allocated_pages"] = max(0, 
                self.processes[process_id]["allocated_pages"] - 1)
        
        return True
    
    def translate_address(
        self,
        process_id: int,
        logical_address: int
    ) -> Optional[Tuple[int, int, bool]]:
        """
        Translate logical address to physical address.
        
        Args:
            process_id: Process identifier
            logical_address: Logical memory address
            
        Returns:
            Tuple of (physical_address, offset, page_fault) or None if invalid
            page_fault is True if page is not in memory (page fault occurred)
        """
        if process_id not in self.page_tables:
            return None
        
        page_table = self.page_tables[process_id]
        result = page_table.translate_address(logical_address)
        
        if result is None:
            return None
        
        page_id, offset = result
        entry = page_table.get_entry(page_id)
        
        if entry is None:
            # Page doesn't exist - page fault
            self.page_faults += 1
            return (None, offset, True)
        
        if not entry.present_bit or entry.frame_id is None:
            # Page not in memory - page fault
            self.page_faults += 1
            entry.mark_referenced()
            return (None, offset, True)
        
        # Successful translation
        frame = self.physical_memory.get_frame(entry.frame_id)
        if frame is None:
            self.page_faults += 1
            return (None, offset, True)
        
        physical_address = (entry.frame_id * self.physical_memory.frame_size) + offset
        entry.mark_referenced()
        self.successful_translations += 1
        return (physical_address, offset, False)
    
    def access_page(self, process_id: int, page_id: int, write: bool = False) -> bool:
        """
        Access a page (simulates memory access).
        
        Args:
            process_id: Process identifier
            page_id: Logical page number
            write: True for write access, False for read
            
        Returns:
            True if access successful (page in memory), False if page fault
        """
        if process_id not in self.page_tables:
            return False
        
        page_table = self.page_tables[process_id]
        entry = page_table.get_entry(page_id)
        
        if entry is None or not entry.present_bit:
            self.page_faults += 1
            return False
        
        entry.mark_referenced()
        if write:
            entry.mark_modified()
        
        self.successful_translations += 1
        return True
    
    def get_statistics(self) -> Dict:
        """
        Get simulation statistics.
        
        Returns:
            Dictionary with statistics
        """
        memory_stats = self.physical_memory.get_frame_status()
        
        total_processes = len(self.processes)
        total_pages = sum(
            pt.get_stats()["total_pages"]
            for pt in self.page_tables.values()
        )
        
        return {
            "memory": memory_stats,
            "total_processes": total_processes,
            "total_pages": total_pages,
            "page_faults": self.page_faults,
            "successful_translations": self.successful_translations,
            "page_fault_rate": (
                self.page_faults / (self.page_faults + self.successful_translations)
                if (self.page_faults + self.successful_translations) > 0 else 0
            )
        }
    
    def reset(self) -> None:
        """Reset the simulator to initial state."""
        self.physical_memory.reset()
        self.page_tables.clear()
        self.processes.clear()
        self.page_faults = 0
        self.successful_translations = 0
        self.allocator._next_fit_start = 0
    
    def set_allocation_strategy(self, strategy: AllocationStrategy) -> None:
        """
        Change allocation strategy.
        
        Args:
            strategy: New allocation strategy
        """
        self.allocator.set_strategy(strategy)
