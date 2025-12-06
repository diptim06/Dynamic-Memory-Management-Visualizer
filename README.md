# 💾 Dynamic Memory Management Visualizer

A comprehensive Python-based tool to simulate and visualize core dynamic memory management techniques used in operating systems, including **Paging**, **Segmentation**, and **Virtual Memory** with page replacement algorithms.

This project is structured as two equal OAS (Operating System Architecture) modules with a clean separation between backend simulation logic and the Streamlit-based user interface.

---

## ⭐ Key Features

### 🔹 Module 1: Paging Engine
- **Physical Memory Simulation**: Frame-based memory management
- **Page Tables**: Logical to physical address translation
- **Page Fault Handling**: Track and handle page faults
- **Allocation Strategies**:
  - **First Fit**: Allocates the first free frame that fits
  - **Best Fit**: Allocates the smallest free frame that fits
  - **Next Fit**: Similar to First Fit, but starts from last allocation position
- **Address Translation**: Convert logical addresses to physical addresses
- **Memory Visualization**: Visual representation of frame allocation

### 🔹 Module 2: Segmentation & Virtual Memory
- **Segmentation Engine**:
  - Segment table management
  - Base and limit register checks
  - Logical to physical address translation
  - Bounds violation detection
  - Fragmentation analysis (internal and external)
  
- **Virtual Memory Manager**:
  - Demand paging simulation
  - Backing store (disk) simulation
  - Swap-in and swap-out mechanisms
  
- **Page Replacement Algorithms**:
  - **FIFO** (First-In-First-Out): Replaces the oldest page
  - **LRU** (Least Recently Used): Replaces the least recently accessed page
  - **Optimal**: Replaces the page that will be used furthest in the future (theoretical best)
  
- **Performance Tracking**:
  - Page hits and misses
  - Page fault rate
  - Swap statistics
  - Hit/miss ratios

### 🔹 Interactive UI (Streamlit)
- Clean, modern interface with custom CSS styling
- Sidebar navigation between modules
- Real-time memory layout visualization
- Interactive controls for simulation
- Statistics and analytics display
- Page table and segment table visualization

---

## 📁 Project Structure

```
Dynamic-Memory-Management-Visualizer/
│
├── README.md
├── requirements.txt
│
├── module1_paging_engine/
│   ├── __init__.py
│   ├── paging_engine.py          # Main paging simulator
│   ├── physical_memory.py        # Physical memory frame management
│   ├── page_table.py             # Page table implementation
│   └── allocator.py              # Memory allocation strategies
│
├── module2_segmentation_virtual_memory/
│   ├── __init__.py
│   ├── segmentation_engine.py    # Segmentation implementation
│   ├── virtual_memory.py         # Virtual memory manager
│   ├── page_replacement.py       # Page replacement algorithms
│   └── address_translation.py    # Address translation utilities
│
├── ui/
│   ├── __init__.py
│   ├── main_app_streamlit.py     # Main Streamlit application
│   ├── shared_components.py      # Reusable UI components
│   └── styles.css                # Custom CSS styles
│
└── utils/
    ├── __init__.py
    ├── logger.py                 # Logging utilities
    └── validators.py             # Input validation functions
```

---

## 🧩 Module Details

### Module 1: Paging Engine

#### Components

**1. Physical Memory (`physical_memory.py`)**
- Manages physical memory as a collection of frames
- Tracks frame status (FREE/ALLOCATED)
- Provides memory statistics and visualization data

**2. Page Table (`page_table.py`)**
- Maintains page tables for processes
- Maps logical pages to physical frames
- Tracks page status bits (Present, Modified, Referenced)
- Handles address translation (logical → page/offset)

**3. Allocator (`allocator.py`)**
- Implements three allocation strategies:
  - **First Fit**: Sequential search for first available frame
  - **Best Fit**: Finds the smallest frame that fits the request
  - **Next Fit**: Starts searching from the last allocation position

**4. Paging Engine (`paging_engine.py`)**
- Main coordinator that integrates all components
- Provides high-level API for:
  - Process creation and removal
  - Page allocation and deallocation
  - Address translation
  - Statistics collection

#### Usage Example

```python
from module1_paging_engine.paging_engine import PagingSimulator
from module1_paging_engine.allocator import AllocationStrategy

# Create simulator
simulator = PagingSimulator(
    num_frames=16,
    frame_size=4096,
    allocation_strategy=AllocationStrategy.FIRST_FIT
)

# Create a process
simulator.create_process(process_id=1, num_pages=5)

# Allocate pages
simulator.allocate_page(process_id=1, page_id=0)
simulator.allocate_page(process_id=1, page_id=1)

# Translate logical address to physical
result = simulator.translate_address(process_id=1, logical_address=0x1000)
if result:
    physical_addr, offset, page_fault = result
    if not page_fault:
        print(f"Physical address: 0x{physical_addr:X}")

# Get statistics
stats = simulator.get_statistics()
print(f"Page faults: {stats['page_faults']}")
```

---

### Module 2: Segmentation & Virtual Memory

#### Components

**1. Segmentation Engine (`segmentation_engine.py`)**
- Manages segment tables for processes
- Implements base/limit register checks
- Performs segment-based address translation
- Calculates internal and external fragmentation

**2. Virtual Memory Manager (`virtual_memory.py`)**
- Simulates demand paging
- Manages backing store (disk storage)
- Handles swap-in and swap-out operations
- Integrates with page replacement algorithms

**3. Page Replacement (`page_replacement.py`)**
- **FIFO**: Uses a queue to track page insertion order
- **LRU**: Maintains access order list, replaces least recently used
- **Optimal**: Uses future reference information (requires lookahead)

**4. Address Translation (`address_translation.py`)**
- Utility functions for address translation
- Supports both paging and segmentation schemes

#### Usage Example

```python
from module2_segmentation_virtual_memory.segmentation_engine import SegmentationEngine
from module2_segmentation_virtual_memory.virtual_memory import VirtualMemoryManager, ReplacementAlgorithm

# Segmentation example
seg_engine = SegmentationEngine()
seg_engine.create_process(process_id=1)
seg_engine.add_segment(process_id=1, segment_id=0, name="CODE", size=4096, base=0x1000)
physical_addr, valid, error = seg_engine.translate_address(process_id=1, segment_id=0, offset=0x100)

# Virtual Memory example
vm_manager = VirtualMemoryManager(
    num_frames=4,
    frame_size=4096,
    algorithm=ReplacementAlgorithm.LRU
)

# Load a process with pages
vm_manager.load_process(process_id=1, pages=[0, 1, 2, 3, 4, 5])

# Access pages (triggers page replacement if needed)
result = vm_manager.access_page(process_id=1, page_id=0, write=False)
if result.get("page_fault"):
    print("Page fault occurred!")

# Get statistics
stats = vm_manager.get_statistics()
print(f"Page faults: {stats['page_faults']}, Hit rate: {stats['hit_rate']:.2%}")
```

---

## 🎨 UI Components

### Main Application (`ui/main_app_streamlit.py`)
- **Navigation**: Sidebar menu for switching between modules
- **Paging Interface**: 
  - Process creation and management
  - Page allocation/deallocation
  - Address translation
  - Memory layout visualization
  - Page table display

- **Segmentation Interface**:
  - Process and segment management
  - Address translation with bounds checking
  - Segment table visualization
  - Fragmentation statistics

- **Virtual Memory Interface**:
  - Process loading
  - Page access simulation
  - Algorithm selection (FIFO/LRU/Optimal)
  - Swap operation tracking
  - Performance statistics

### Shared Components (`ui/shared_components.py`)
- `header()`: Styled page header
- `footer()`: Page footer
- `memory_visualizer()`: Visualize physical memory frames
- `stats_box()`: Display statistics in formatted box
- `page_table_visualizer()`: Display page tables
- `info_box()`: Info/warning/error messages

---

## ⚙️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone or download the project**:
   ```bash
   cd Dynamic-Memory-Management-Visualizer
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run ui/main_app_streamlit.py
   ```

   The application will open in your default web browser at `http://localhost:8501`

---

## 🚀 How to Run

### Running the UI

```bash
streamlit run ui/main_app_streamlit.py
```

### Using Modules Programmatically

You can also use the modules directly in Python scripts:

```python
# Example: Paging simulation
from module1_paging_engine.paging_engine import PagingSimulator

sim = PagingSimulator(num_frames=16, frame_size=4096)
sim.create_process(process_id=1, num_pages=10)
sim.allocate_page(process_id=1, page_id=0)
stats = sim.get_statistics()
print(stats)
```

---

## 📊 How Each Algorithm Works

### Allocation Strategies (Paging)

**First Fit**
1. Search frames sequentially from the beginning
2. Allocate the first free frame that is large enough
3. Fast but may lead to external fragmentation

**Best Fit**
1. Search all free frames
2. Allocate the smallest frame that fits the request
3. Minimizes wasted space but slower

**Next Fit**
1. Similar to First Fit, but starts from the last allocation position
2. Wraps around when reaching the end
3. Better distribution of allocations

### Page Replacement Algorithms (Virtual Memory)

**FIFO (First-In-First-Out)**
- Maintains a queue of pages in order of loading
- When replacement is needed, evicts the oldest page
- Simple but may evict frequently used pages

**LRU (Least Recently Used)**
- Tracks the access order of pages
- Evicts the page that hasn't been used for the longest time
- Better performance than FIFO in most cases
- Requires tracking access history

**Optimal**
- Uses knowledge of future page references
- Evicts the page that will be used furthest in the future
- Provides theoretical best performance
- Not practical in real systems (requires future knowledge)

### Address Translation

**Paging**
1. Split logical address into page number and offset
2. Look up page number in page table
3. If page is present, combine frame number with offset to get physical address
4. If page not present, trigger page fault

**Segmentation**
1. Use segment ID to find segment table entry
2. Check if offset is within segment bounds (limit)
3. If valid, add offset to base address to get physical address
4. If out of bounds, trigger segmentation fault

---

## 🖼️ Example Screenshots

### Memory Layout Visualization
The UI displays physical memory frames in a grid layout, color-coded by status:
- **Blue**: Allocated frames
- **Gray**: Free frames
- **Red**: Page fault indicators

### Page Table Display
Interactive tables showing:
- Page ID
- Frame ID mapping
- Present/Modified/Referenced bits
- Status information

### Statistics Dashboard
Real-time display of:
- Total frames and utilization
- Page faults and hits
- Fault rates
- Swap operations

*(Note: Screenshots would be added here in an actual deployment)*

---

## 🧰 Technical Details

### Code Quality
- **Object-Oriented Design**: Clean class hierarchies with proper abstraction
- **Type Hints**: Full type annotations for better code clarity
- **Docstrings**: Comprehensive documentation for all classes and methods
- **Error Handling**: Proper validation and error messages
- **Modular Architecture**: Well-separated concerns with clear APIs

### Design Patterns
- **Strategy Pattern**: For allocation and replacement algorithms
- **State Pattern**: For frame and page status management
- **Factory Pattern**: For creating replacement algorithm instances

### API Design
Both modules expose clean, consistent APIs:
- `create_process()` / `remove_process()` for process management
- `allocate()` / `deallocate()` for memory operations
- `translate_address()` for address translation
- `get_statistics()` for performance metrics
- `reset()` for state reset

---

## 🔧 Configuration

### Paging Simulator Configuration
- Number of frames (default: 16)
- Frame size in bytes (default: 4096)
- Allocation strategy (FIRST_FIT, BEST_FIT, NEXT_FIT)

### Virtual Memory Configuration
- Number of frames (default: 4)
- Frame size (default: 4096)
- Replacement algorithm (FIFO, LRU, OPTIMAL)

### Segmentation Configuration
- Auto-assigned base addresses
- Custom segment sizes
- Segment names (CODE, DATA, STACK, HEAP, etc.)

---

## 📈 Performance Metrics

The simulator tracks various performance metrics:

### Paging Metrics
- Total frames and utilization percentage
- Page faults
- Successful translations
- Page fault rate

### Segmentation Metrics
- Access attempts and successes
- Bounds violations
- Success rate
- Fragmentation (internal and external)

### Virtual Memory Metrics
- Page hits and misses
- Hit rate and fault rate
- Swap-in and swap-out operations
- Backing store statistics

---

## 🚧 Future Improvements

### Planned Features
- **Additional Page Replacement Algorithms**:
  - Working Set algorithm
  - Clock (Second Chance) algorithm
  - LFU/MFU (Least/Most Frequently Used)

- **TLB Simulation**:
  - Translation Lookaside Buffer with cache visualization
  - TLB hit/miss tracking
  - Cache replacement policies

- **Enhanced Visualization**:
  - Real-time animation of memory operations
  - Interactive timeline of memory accesses
  - Graph visualizations for performance trends

- **Extended Features**:
  - Multi-level page tables
  - Process scheduling integration
  - Memory protection bits
  - Export simulation results as PDF/CSV
  - Custom memory trace file support

- **User Experience**:
  - Dark mode support
  - Responsive design improvements
  - Tutorial/guided mode for learning
  - Comparison mode (compare algorithms side-by-side)

---

## 📝 Dependencies

### Core Dependencies
- **streamlit** (>=1.28.0): Web framework for the UI
- **numpy** (>=1.24.0): Numerical operations (for potential future enhancements)

### Python Standard Library
- `typing`: Type hints
- `enum`: Enumeration types
- `collections`: Data structures (deque)
- `pathlib`: File path handling
- `logging`: Logging functionality
- `sys`: System-specific parameters

---

## 🤝 Contributing

This is an educational project designed for learning operating systems concepts. Suggestions and improvements are welcome!

### Code Style
- Follow PEP 8 Python style guide
- Use type hints for all function signatures
- Include docstrings for all classes and functions
- Keep functions focused and modular

---

## 📄 License

This project is provided for educational purposes. Feel free to use and modify for learning.

---

## 👨‍💻 Author

Dynamic Memory Management Visualizer
Built with Python and Streamlit

---

## 🎓 Educational Use

This tool is designed to help students and developers understand:
- How paging and segmentation work in operating systems
- The trade-offs between different allocation strategies
- How page replacement algorithms affect performance
- The relationship between logical and physical addresses
- Virtual memory concepts and demand paging

Perfect for:
- Operating Systems courses
- System programming education
- Interview preparation
- Self-study

---

## 📞 Support

For questions or issues:
1. Check the documentation in this README
2. Review the code comments and docstrings
3. Experiment with the UI to understand functionality

---

**Happy Learning! 💻📚**
