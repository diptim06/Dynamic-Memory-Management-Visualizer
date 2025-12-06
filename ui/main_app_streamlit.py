"""
Main Streamlit Application
Dynamic Memory Management Visualizer UI
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from module1_paging_engine.paging_engine import PagingSimulator, AllocationStrategy
from module2_segmentation_virtual_memory.segmentation_engine import SegmentationEngine
from module2_segmentation_virtual_memory.virtual_memory import VirtualMemoryManager, ReplacementAlgorithm
from ui.shared_components import header, footer, memory_visualizer, stats_box, info_box, page_table_visualizer

# Load custom CSS
def load_css():
    """Load custom CSS styles."""
    css_path = Path(__file__).parent / "styles.css"
    if css_path.exists():
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if 'paging_sim' not in st.session_state:
    st.session_state.paging_sim = None
    st.session_state.paging_processes = {}

if 'segmentation_sim' not in st.session_state:
    st.session_state.segmentation_sim = None

if 'virtual_memory_sim' not in st.session_state:
    st.session_state.virtual_memory_sim = None

# Page configuration
st.set_page_config(
    page_title="Memory Management Visualizer",
    page_icon="💾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
load_css()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Module",
    ["Paging", "Segmentation", "Virtual Memory", "About Project"],
    index=0
)

# Main header
if page != "About Project":
    header("Dynamic Memory Management Visualizer", "Interactive Memory Management Simulation Tool")

# Paging Page
if page == "Paging":
    st.title("📄 Paging Engine")
    
    # Configuration sidebar
    with st.sidebar.expander("⚙️ Configuration", expanded=True):
        num_frames = st.number_input("Number of Frames", min_value=4, max_value=64, value=16, step=1)
        frame_size = st.number_input("Frame Size (bytes)", min_value=1024, max_value=16384, value=4096, step=1024)
        strategy_str = st.selectbox(
            "Allocation Strategy",
            ["FIRST_FIT", "BEST_FIT", "NEXT_FIT"],
            index=0
        )
        
        if st.button("Initialize Simulator", type="primary"):
            strategy_map = {
                "FIRST_FIT": AllocationStrategy.FIRST_FIT,
                "BEST_FIT": AllocationStrategy.BEST_FIT,
                "NEXT_FIT": AllocationStrategy.NEXT_FIT
            }
            st.session_state.paging_sim = PagingSimulator(
                num_frames=num_frames,
                frame_size=frame_size,
                allocation_strategy=strategy_map[strategy_str]
            )
            st.session_state.paging_processes = {}
            st.success("Simulator initialized!")
    
    if st.session_state.paging_sim is None:
        info_box("Please initialize the simulator in the sidebar first.", "info")
    else:
        sim = st.session_state.paging_sim
        
        # Process management
        st.subheader("Process Management")
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("➕ Create Process", expanded=False):
                process_id = st.number_input("Process ID", min_value=0, value=1, step=1, key="paging_pid")
                num_pages = st.number_input("Initial Pages", min_value=0, value=0, step=1, key="paging_npages")
                if st.button("Create Process"):
                    if sim.create_process(process_id, num_pages):
                        st.session_state.paging_processes[process_id] = {"created": True}
                        st.success(f"Process {process_id} created!")
                    else:
                        st.error("Process already exists!")
        
        with col2:
            with st.expander("🗑️ Remove Process", expanded=False):
                remove_pid = st.selectbox("Select Process", list(st.session_state.paging_processes.keys()), key="paging_remove")
                if st.button("Remove Process"):
                    if sim.remove_process(remove_pid):
                        del st.session_state.paging_processes[remove_pid]
                        st.success(f"Process {remove_pid} removed!")
                    else:
                        st.error("Failed to remove process!")
        
        # Page operations
        st.subheader("Page Operations")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.expander("📥 Allocate Page", expanded=False):
                alloc_pid = st.selectbox("Process ID", list(st.session_state.paging_processes.keys()), key="paging_alloc_pid")
                alloc_page = st.number_input("Page ID", min_value=0, value=0, step=1, key="paging_alloc_page")
                if st.button("Allocate"):
                    frame_id = sim.allocate_page(alloc_pid, alloc_page)
                    if frame_id is not None:
                        st.success(f"Page {alloc_page} allocated to frame {frame_id}!")
                    else:
                        st.error("Allocation failed! Memory might be full.")
        
        with col2:
            with st.expander("📤 Deallocate Page", expanded=False):
                dealloc_pid = st.selectbox("Process ID", list(st.session_state.paging_processes.keys()), key="paging_dealloc_pid")
                dealloc_page = st.number_input("Page ID", min_value=0, value=0, step=1, key="paging_dealloc_page")
                if st.button("Deallocate"):
                    if sim.deallocate_page(dealloc_pid, dealloc_page):
                        st.success(f"Page {dealloc_page} deallocated!")
                    else:
                        st.error("Deallocation failed!")
        
        with col3:
            with st.expander("🔍 Translate Address", expanded=False):
                trans_pid = st.selectbox("Process ID", list(st.session_state.paging_processes.keys()), key="paging_trans_pid")
                logical_addr = st.number_input("Logical Address", min_value=0, value=0, step=1024, key="paging_logical")
                if st.button("Translate"):
                    result = sim.translate_address(trans_pid, logical_addr)
                    if result:
                        phys_addr, offset, page_fault = result
                        if page_fault:
                            st.warning(f"Page Fault! Page not in memory.")
                        else:
                            st.success(f"Physical Address: 0x{phys_addr:X} (offset: {offset})")
        
        # Visualizations
        st.subheader("Visualization")
        
        # Memory layout
        frames_data = sim.physical_memory.visualize_memory()
        memory_visualizer(frames_data, "Physical Memory Layout")
        
        # Page tables
        if st.session_state.paging_processes:
            selected_pid = st.selectbox("Select Process for Page Table", list(st.session_state.paging_processes.keys()))
            if selected_pid in sim.page_tables:
                pt_data = sim.page_tables[selected_pid].visualize_table()
                page_table_visualizer(pt_data, f"Page Table for Process {selected_pid}")
        
        # Statistics
        stats = sim.get_statistics()
        stats_box(stats, "Simulation Statistics")

# Segmentation Page
elif page == "Segmentation":
    st.title("📊 Segmentation Engine")
    
    # Configuration sidebar
    with st.sidebar.expander("⚙️ Configuration", expanded=True):
        if st.button("Initialize Simulator", type="primary"):
            st.session_state.segmentation_sim = SegmentationEngine()
            st.success("Segmentation engine initialized!")
    
    if st.session_state.segmentation_sim is None:
        info_box("Please initialize the simulator in the sidebar first.", "info")
    else:
        sim = st.session_state.segmentation_sim
        
        # Process management
        st.subheader("Process Management")
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("➕ Create Process", expanded=False):
                process_id = st.number_input("Process ID", min_value=0, value=1, step=1, key="seg_pid")
                if st.button("Create Process"):
                    if sim.create_process(process_id):
                        st.success(f"Process {process_id} created!")
                    else:
                        st.error("Process already exists!")
        
        # Segment management
        st.subheader("Segment Management")
        process_ids = list(sim.segment_tables.keys())
        if process_ids:
            selected_pid = st.selectbox("Select Process", process_ids, key="seg_select")
            
            with st.expander("➕ Add Segment", expanded=False):
                segment_id = st.number_input("Segment ID", min_value=0, value=0, step=1, key="seg_id")
                segment_name = st.text_input("Segment Name", value="CODE", key="seg_name")
                segment_size = st.number_input("Segment Size (bytes)", min_value=1024, value=4096, step=1024, key="seg_size")
                segment_base = st.number_input("Base Address (0 for auto)", min_value=0, value=0, step=0x1000, key="seg_base")
                
                if st.button("Add Segment"):
                    base_addr = None if segment_base == 0 else segment_base
                    if sim.add_segment(selected_pid, segment_id, segment_name, segment_size, base_addr):
                        st.success(f"Segment {segment_id} added!")
                    else:
                        st.error("Failed to add segment!")
            
            # Address translation
            st.subheader("Address Translation")
            col1, col2 = st.columns(2)
            
            with col1:
                trans_pid = st.selectbox("Process ID", process_ids, key="seg_trans_pid")
                trans_seg = st.number_input("Segment ID", min_value=0, value=0, step=1, key="seg_trans_seg")
                trans_offset = st.number_input("Offset", min_value=0, value=0, step=0x100, key="seg_trans_offset")
                
                if st.button("Translate Address"):
                    phys_addr, valid, error = sim.translate_address(trans_pid, trans_seg, trans_offset)
                    if valid:
                        st.success(f"Physical Address: 0x{phys_addr:X}")
                    else:
                        st.error(f"Translation failed: {error}")
            
            # Segment table visualization
            if selected_pid in sim.segment_tables:
                st.subheader(f"Segment Table for Process {selected_pid}")
                seg_data = sim.segment_tables[selected_pid].visualize_table()
                if seg_data:
                    st.table(seg_data)
                
                # Fragmentation
                frag_stats = sim.calculate_fragmentation(selected_pid)
                stats_box(frag_stats, "Fragmentation Statistics")
        
        # Statistics
        stats = sim.get_statistics()
        stats_box(stats, "Engine Statistics")

# Virtual Memory Page
elif page == "Virtual Memory":
    st.title("🌐 Virtual Memory Manager")
    
    # Configuration sidebar
    with st.sidebar.expander("⚙️ Configuration", expanded=True):
        num_frames = st.number_input("Number of Frames", min_value=2, max_value=32, value=4, step=1, key="vm_frames")
        frame_size = st.number_input("Frame Size (bytes)", min_value=1024, value=4096, step=1024, key="vm_frame_size")
        algorithm_str = st.selectbox(
            "Replacement Algorithm",
            ["FIFO", "LRU", "OPTIMAL"],
            index=0,
            key="vm_algorithm"
        )
        
        if st.button("Initialize Simulator", type="primary"):
            algorithm_map = {
                "FIFO": ReplacementAlgorithm.FIFO,
                "LRU": ReplacementAlgorithm.LRU,
                "OPTIMAL": ReplacementAlgorithm.OPTIMAL
            }
            st.session_state.virtual_memory_sim = VirtualMemoryManager(
                num_frames=num_frames,
                frame_size=frame_size,
                algorithm=algorithm_map[algorithm_str]
            )
            st.success("Virtual memory manager initialized!")
    
    if st.session_state.virtual_memory_sim is None:
        info_box("Please initialize the simulator in the sidebar first.", "info")
    else:
        sim = st.session_state.virtual_memory_sim
        
        # Process management
        st.subheader("Process Management")
        with st.expander("➕ Load Process", expanded=False):
            process_id = st.number_input("Process ID", min_value=0, value=1, step=1, key="vm_pid")
            pages_input = st.text_input("Page IDs (comma-separated)", value="0,1,2,3,4,5,6,7", key="vm_pages")
            if st.button("Load Process"):
                try:
                    pages = [int(p.strip()) for p in pages_input.split(",")]
                    if sim.load_process(process_id, pages):
                        st.success(f"Process {process_id} loaded with {len(pages)} pages!")
                    else:
                        st.error("Failed to load process!")
                except ValueError:
                    st.error("Invalid page list format!")
        
        # Page access
        st.subheader("Page Access")
        process_ids = list(sim.process_pages.keys())
        if process_ids:
            col1, col2 = st.columns(2)
            
            with col1:
                access_pid = st.selectbox("Process ID", process_ids, key="vm_access_pid")
                access_page = st.number_input("Page ID", min_value=0, value=0, step=1, key="vm_access_page")
                is_write = st.checkbox("Write Access", key="vm_write")
                
                # For Optimal algorithm, provide future references
                future_refs = None
                if sim.algorithm == ReplacementAlgorithm.OPTIMAL:
                    future_input = st.text_input("Future References (comma-separated, optional)", value="", key="vm_future")
                    if future_input:
                        try:
                            future_refs = [int(p.strip()) for p in future_input.split(",")]
                        except ValueError:
                            st.warning("Invalid future references format")
                
                if st.button("Access Page"):
                    result = sim.access_page(access_pid, access_page, is_write, future_refs)
                    if result.get("success"):
                        if result.get("page_fault"):
                            st.warning(f"Page Fault! Page {access_page} not in memory.")
                            if result.get("swap_in"):
                                st.info(f"Page swapped in from backing store.")
                            if result.get("swap_out"):
                                st.info(f"Page {result.get('replaced_page')} swapped out to backing store.")
                        else:
                            st.success(f"Page {access_page} accessed successfully (Hit)!")
                    else:
                        st.error(result.get("error", "Access failed!"))
            
            with col2:
                st.subheader("Address Translation")
                trans_pid = st.selectbox("Process ID", process_ids, key="vm_trans_pid")
                virtual_addr = st.number_input("Virtual Address", min_value=0, value=0, step=0x1000, key="vm_virtual")
                if st.button("Translate"):
                    result = sim.translate_address(trans_pid, virtual_addr)
                    if result:
                        phys_addr, offset, page_fault = result
                        if page_fault:
                            st.warning(f"Page Fault! Page not in memory.")
                        else:
                            st.success(f"Physical Address: 0x{phys_addr:X} (offset: {offset})")
        
        # Visualizations
        st.subheader("Visualization")
        
        # Memory layout
        layout = sim.get_memory_layout()
        memory_visualizer(layout, "Physical Memory Layout")
        
        # Statistics
        stats = sim.get_statistics()
        stats_box(stats, "Virtual Memory Statistics")

# About Page
else:
    st.title("📘 About This Project")
    
    st.markdown("""
    ## Dynamic Memory Management Visualizer
    
    A comprehensive Python-based tool for simulating and visualizing core dynamic memory management 
    techniques used in operating systems.
    
    ### Features
    
    #### Module 1: Paging Engine
    - **Physical Memory Simulation**: Frame-based memory management
    - **Page Tables**: Logical to physical address mapping
    - **Allocation Strategies**: First Fit, Best Fit, Next Fit
    - **Page Fault Handling**: Track and visualize page faults
    - **Address Translation**: Convert logical addresses to physical addresses
    
    #### Module 2: Segmentation & Virtual Memory
    - **Segmentation**: Segment-based memory management with base/limit registers
    - **Virtual Memory**: Demand paging with backing store simulation
    - **Page Replacement Algorithms**:
      - FIFO (First-In-First-Out)
      - LRU (Least Recently Used)
      - Optimal (Theoretical best)
    - **Swap Mechanism**: Simulate page swapping to/from backing store
    - **Fragmentation Analysis**: Internal and external fragmentation tracking
    
    ### How to Use
    
    1. **Paging**: Initialize the simulator, create processes, allocate pages, and visualize memory layout
    2. **Segmentation**: Create processes, add segments, and perform address translation
    3. **Virtual Memory**: Load processes, access pages, and observe page replacement in action
    
    ### Technical Stack
    
    - **Backend**: Python 3.x with object-oriented design
    - **Frontend**: Streamlit for interactive UI
    - **Visualization**: Custom HTML/CSS components
    
    ### Project Structure
    
    ```
    Dynamic-Memory-Management-Visualizer/
    ├── module1_paging_engine/       # Paging simulation
    ├── module2_segmentation_virtual_memory/  # Segmentation & Virtual Memory
    ├── ui/                          # Streamlit UI
    ├── utils/                       # Utilities
    └── requirements.txt             # Dependencies
    ```
    
    ### Installation
    
    1. Install dependencies: `pip install -r requirements.txt`
    2. Run the application: `streamlit run ui/main_app_streamlit.py`
    
    ### Future Improvements
    
    - More page replacement algorithms (Working Set, Clock, Second Chance)
    - TLB (Translation Lookaside Buffer) simulation
    - Real-time animation of memory operations
    - Export simulation results as reports
    - Multi-process simulation with scheduling
    """)
    
    footer()

# Footer for all pages except About
if page != "About Project":
    footer()
