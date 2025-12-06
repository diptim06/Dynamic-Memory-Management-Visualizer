"""
Virtual Memory Module
Manages virtual memory with backing store, swapping, and page replacement.
"""

from typing import Dict, List, Optional, Tuple
from module2_segmentation_virtual_memory.page_replacement import (
    PageReplacementAlgorithm,
    FIFOReplacement,
    LRUReplacement,
    OptimalReplacement,
    ReplacementAlgorithm
)


class BackingStore:
    """Simulates backing store (disk) for pages not in physical memory."""
    
    def __init__(self):
        """Initialize the backing store."""
        self.pages: Dict[int, bytes] = {}  # page_id -> page_data
    
    def store_page(self, page_id: int, data: bytes) -> None:
        """
        Store a page in backing store.
        
        Args:
            page_id: Page identifier
            data: Page data
        """
        self.pages[page_id] = data
    
    def load_page(self, page_id: int) -> Optional[bytes]:
        """
        Load a page from backing store.
        
        Args:
            page_id: Page identifier
            
        Returns:
            Page data or None if not found
        """
        return self.pages.get(page_id)
    
    def has_page(self, page_id: int) -> bool:
        """
        Check if page exists in backing store.
        
        Args:
            page_id: Page identifier
            
        Returns:
            True if page exists, False otherwise
        """
        return page_id in self.pages
    
    def remove_page(self, page_id: int) -> bool:
        """
        Remove a page from backing store.
        
        Args:
            page_id: Page identifier
            
        Returns:
            True if removed, False if not found
        """
        if page_id in self.pages:
            del self.pages[page_id]
            return True
        return False


class VirtualMemoryManager:
    """
    Virtual Memory Manager with demand paging and page replacement.
    
    Usage:
        manager = VirtualMemoryManager(num_frames=4, algorithm=ReplacementAlgorithm.LRU)
        manager.load_process(process_id=1, pages=[0, 1, 2, 3, 4])
        result = manager.access_page(process_id=1, page_id=0)
        physical_addr = manager.translate_address(process_id=1, virtual_address=0x1000)
    """
    
    def __init__(
        self,
        num_frames: int = 16,
        frame_size: int = 4096,
        algorithm: ReplacementAlgorithm = ReplacementAlgorithm.FIFO
    ):
        """
        Initialize virtual memory manager.
        
        Args:
            num_frames: Number of physical frames
            frame_size: Size of each frame in bytes
            algorithm: Page replacement algorithm to use
        """
        self.num_frames = num_frames
        self.frame_size = frame_size
        self.algorithm = algorithm
        
        # Initialize replacement algorithm
        self.replacement: PageReplacementAlgorithm = self._create_replacement_algorithm(algorithm)
        
        # Backing store for pages not in memory
        self.backing_store = BackingStore()
        
        # Process page mappings: process_id -> [list of page_ids]
        self.process_pages: Dict[int, List[int]] = {}
        
        # Track swaps
        self.swap_ins = 0
        self.swap_outs = 0
        
        # Address translation cache
        self.address_cache: Dict[Tuple[int, int], int] = {}
    
    def _create_replacement_algorithm(
        self,
        algorithm: ReplacementAlgorithm
    ) -> PageReplacementAlgorithm:
        """
        Create a replacement algorithm instance.
        
        Args:
            algorithm: Algorithm type
            
        Returns:
            PageReplacementAlgorithm instance
        """
        if algorithm == ReplacementAlgorithm.FIFO:
            return FIFOReplacement(self.num_frames)
        elif algorithm == ReplacementAlgorithm.LRU:
            return LRUReplacement(self.num_frames)
        elif algorithm == ReplacementAlgorithm.OPTIMAL:
            return OptimalReplacement(self.num_frames)
        else:
            return FIFOReplacement(self.num_frames)  # Default
    
    def load_process(self, process_id: int, pages: List[int]) -> bool:
        """
        Load a process with its virtual pages into backing store.
        
        Args:
            process_id: Process identifier
            pages: List of page IDs for the process
            
        Returns:
            True if process loaded successfully
        """
        self.process_pages[process_id] = pages
        
        # Initialize pages in backing store (simulate they exist on disk)
        for page_id in pages:
            if not self.backing_store.has_page(page_id):
                # Simulate page data
                page_data = bytes(self.frame_size)
                self.backing_store.store_page(page_id, page_data)
        
        return True
    
    def remove_process(self, process_id: int) -> bool:
        """
        Remove a process and free its pages.
        
        Args:
            process_id: Process identifier
            
        Returns:
            True if process removed successfully
        """
        if process_id not in self.process_pages:
            return False
        
        # Free all pages of this process from memory
        pages = self.process_pages[process_id]
        for page_id in pages:
            # Remove from backing store
            self.backing_store.remove_page(page_id)
            
            # If page is in physical memory, free it
            if self.replacement.is_page_loaded(page_id):
                # Find and free the frame
                for i, loaded_page in enumerate(self.replacement.frames):
                    if loaded_page == page_id:
                        self.replacement.frames[i] = None
        
        del self.process_pages[process_id]
        return True
    
    def access_page(
        self,
        process_id: int,
        page_id: int,
        write: bool = False,
        future_references: Optional[List[int]] = None
    ) -> Dict:
        """
        Access a virtual page, handling page faults and replacements.
        
        Args:
            process_id: Process identifier
            page_id: Virtual page number
            write: True for write access, False for read
            future_references: Future page references (for Optimal algorithm)
            
        Returns:
            Dictionary with access result information
        """
        if process_id not in self.process_pages:
            return {
                "success": False,
                "error": f"Process {process_id} not found",
                "page_fault": False
            }
        
        if page_id not in self.process_pages[process_id]:
            return {
                "success": False,
                "error": f"Page {page_id} not in process {process_id}",
                "page_fault": False
            }
        
        # Check if page is in physical memory
        if self.replacement.is_page_loaded(page_id):
            # Page hit
            result = self.replacement.access_page(page_id, future_references)
            result["swap_in"] = False
            result["swap_out"] = False
            result["success"] = True
            return result
        
        # Page fault - page not in memory
        # Check if page exists in backing store
        if not self.backing_store.has_page(page_id):
            return {
                "success": False,
                "error": f"Page {page_id} not in backing store",
                "page_fault": True
            }
        
        # Swap in: Load page from backing store
        page_data = self.backing_store.load_page(page_id)
        
        # Access page through replacement algorithm (will trigger replacement if needed)
        result = self.replacement.access_page(page_id, future_references)
        
        # Handle swap out if a page was replaced
        if result.get("replaced_page") is not None:
            replaced_page = result["replaced_page"]
            # Store replaced page in backing store (if modified)
            self.backing_store.store_page(replaced_page, bytes(self.frame_size))
            self.swap_outs += 1
            result["swap_out"] = True
        else:
            result["swap_out"] = False
        
        self.swap_ins += 1
        result["swap_in"] = True
        result["success"] = True
        
        return result
    
    def translate_address(
        self,
        process_id: int,
        virtual_address: int
    ) -> Optional[Tuple[int, int, bool]]:
        """
        Translate virtual address to physical address.
        
        Args:
            process_id: Process identifier
            virtual_address: Virtual memory address
            
        Returns:
            Tuple of (physical_address, offset, page_fault) or None if invalid
            page_fault is True if page is not in memory
        """
        if process_id not in self.process_pages:
            return None
        
        # Extract page number and offset
        page_id = virtual_address // self.frame_size
        offset = virtual_address % self.frame_size
        
        # Check if page belongs to process
        if page_id not in self.process_pages[process_id]:
            return None
        
        # Check if page is in physical memory
        if not self.replacement.is_page_loaded(page_id):
            # Page fault - page not in memory
            return (None, offset, True)
        
        # Find frame index for this page
        frame_index = None
        for i, loaded_page in enumerate(self.replacement.frames):
            if loaded_page == page_id:
                frame_index = i
                break
        
        if frame_index is None:
            return (None, offset, True)
        
        # Calculate physical address
        physical_address = (frame_index * self.frame_size) + offset
        return (physical_address, offset, False)
    
    def set_replacement_algorithm(self, algorithm: ReplacementAlgorithm) -> None:
        """
        Change the page replacement algorithm.
        
        Args:
            algorithm: New replacement algorithm
        """
        # Save current state if needed
        current_pages = [p for p in self.replacement.frames if p is not None]
        
        # Create new algorithm instance
        self.algorithm = algorithm
        self.replacement = self._create_replacement_algorithm(algorithm)
        
        # Optionally restore pages (simplified - in real scenario would need more state)
    
    def get_statistics(self) -> Dict:
        """
        Get virtual memory statistics.
        
        Returns:
            Dictionary with comprehensive statistics
        """
        replacement_stats = self.replacement.get_statistics()
        
        total_swaps = self.swap_ins + self.swap_outs
        
        return {
            "replacement_algorithm": self.algorithm.value,
            "num_frames": self.num_frames,
            "frame_size": self.frame_size,
            "swap_ins": self.swap_ins,
            "swap_outs": self.swap_outs,
            "total_swaps": total_swaps,
            "processes": len(self.process_pages),
            "backing_store_pages": len(self.backing_store.pages),
            **replacement_stats
        }
    
    def get_memory_layout(self) -> List[Dict]:
        """
        Get current physical memory layout for visualization.
        
        Returns:
            List of dictionaries with frame information
        """
        layout = []
        for i, page_id in enumerate(self.replacement.frames):
            layout.append({
                "frame_id": i,
                "page_id": page_id,
                "status": "ALLOCATED" if page_id is not None else "FREE",
                "base_address": i * self.frame_size,
                "size": self.frame_size
            })
        return layout
    
    def reset(self) -> None:
        """Reset the virtual memory manager."""
        self.replacement.reset()
        self.backing_store = BackingStore()
        self.process_pages.clear()
        self.swap_ins = 0
        self.swap_outs = 0
        self.address_cache.clear()
        # Recreate replacement algorithm
        self.replacement = self._create_replacement_algorithm(self.algorithm)
