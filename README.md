
# 💾 Dynamic Memory Management Visualizer

A Python-based tool to simulate, visualize, and analyze core dynamic memory management techniques such as **Paging**, **Segmentation**, **Virtual Memory**, and **Page Replacement Algorithms**, paired with a clean **Streamlit UI**.

This project is divided into two OAS-grade modules and a separate UI layer, making it ideal for academic submission and practical understanding of OS memory systems.

-----

## ⭐ Key Features

### 🔹 Memory Management Techniques

  * **Paging Simulation** – page tables, TLB behaviour, page faults.
  * **Segmentation** – segment tables, logical to physical address translation.
  * **Virtual Memory** – demand paging, swapping, address translation.
  * **Page Replacement Algorithms** – FIFO, LRU, Optimal, LFU, MFU.

### 🔹 Simulation Engine

  * Dynamic process generation.
  * Step-by-step event logging.
  * Memory access trace execution.
  * Statistics and analytics for performance.

### 🔹 Interactive Visualization (UI)

  * **Memory map** view.
  * **Timeline** animations.
  * **Charts** for hit/miss ratio.
  * Process behaviour insights.

-----

## 📁 Folder Structure

```
Dynamic_memory_management_Visualizer/
|
├── Module_1_MemoryTechniques/        # Core OS concepts (OAS Module 1)
│   ├── paging_engine.py
│   ├── segmentation_engine.py
│   ├── virtual_memory.py
│   ├── replacement_algorithms.py
│   ├── allocator.py
│   ├── utils.py
│   └── tests/
│
├── Module_2_Simulation_Analytics/    # Simulation + analytics (OAS Module 2)
│   ├── simulator.py
│   ├── process_generator.py
│   ├── trace_loader.py
│   ├── stats_collector.py
│   ├── event_logger.py
│   ├── analytics.py
│   └── tests/
│
├── UI/                               # Streamlit User Interface
│   ├── main_app_streamlit.py
│   ├── memory_map_view.py
│   ├── charts_view.py
│   ├── timeline_view.py
│   ├── shared_components.py
│   └── assets/
│
├── Demo_Examples/                    # Demo memory traces
└── docs/                             # Project documentation
```

-----

## 🧩 Module 1 – Core Memory Techniques (OAS Module 1)

This module implements the core operating system memory management logic.

### 1\. `paging_engine.py`

  * Frame allocation.
  * Page table translation.
  * Page fault handling.
  * TLB simulation.

### 2\. `segmentation_engine.py`

  * Segment table management.
  * Logical-to-physical address translation.
  * Out-of-bound detection.

### 3\. `virtual_memory.py`

  * Demand paging simulation.
  * Swap-in / Swap-out simulation.
  * Backing store emulation.

### 4\. `replacement_algorithms.py`

Implements standard Page Replacement Algorithms:

| Algorithm | Description |
| :--- | :--- |
| **FIFO** | Evicts the **oldest loaded** page. |
| **LRU** | Evicts the **least-recently used** page. |
| **Optimal** | Evicts the page that **won't be used for the longest time** (theoretical best). |
| **LFU** | Removes the **least-frequently used** page. |
| **MFU** | Removes the **most-frequently used** page. |

### 5\. `allocator.py`

  * Frame/segment allocation strategies.
  * **First-fit** / **Best-fit** / **Worst-fit**.

### 6\. `utils.py`

  * Address conversion helpers, data structures, and common utility functions.

-----

## 🧪 Module 2 – Simulation & Analytics (OAS Module 2)

This module handles the execution of memory traces, collecting statistics, and generating analytics.

### 1\. `simulator.py`

  * Core simulation loop.
  * Handles memory access operations.
  * Interfaces with Module 1 engines.

### 2\. `process_generator.py`

  * Generates fake OS-like processes.
  * Randomized memory access patterns.

### 3\. `trace_loader.py`

  * Loads `.trace` files from `Demo_Examples/`.
  * Parses memory instructions.

### 4\. `stats_collector.py`

Tracks key performance metrics:

  * **Page faults**
  * **Hit ratio** (TLB and Page)
  * Memory utilization
  * Timeline events

### 5\. `event_logger.py`

  * Structured logging of simulation events.
  * JSON/CSV output.

### 6\. `analytics.py`

  * Computes final performance insights.
  * Generates data for UI charts.

-----

## 🎨 UI Overview – Streamlit App

The UI layer provides visual understanding using Streamlit.

| File | Description |
| :--- | :--- |
| `main_app_streamlit.py` | Application entry point and overall layout. |
| `memory_map_view.py` | Interactive visualization of physical memory and frame allocation. |
| `charts_view.py` | Displays Pie/Bar charts for analytics (Hit Ratio, Utilization). |
| `timeline_view.py` | Shows a step-by-step simulation timeline. |
| `shared_components.py` | Reusable UI components (buttons, sliders, inputs). |
| `assets/` | Images, icons, and custom CSS. |

-----

## ⚙️ Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/Dynamic_memory_management_Visualizer.git
    cd Dynamic_memory_management_Visualizer
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux / Mac
    venv\Scripts\activate     # Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

-----

## 🚀 How to Run the Project

1.  **Run the Streamlit UI:**

    ```bash
    streamlit run UI/main_app_streamlit.py
    ```

2.  **Run only the simulator (optional):**

    ```bash
    python Module_2_Simulation_Analytics/simulator.py
    ```

-----

## 📂 Example Inputs / Trace Files

Place your memory access trace files in the **`Demo_Examples/`** folder.

**Sample trace format:**

```
# PID  ADDRESS  OP
1      0x0040   READ
1      0x0500   WRITE
2      0x1200   READ
```

-----

## 🖼️ Screenshots (Coming Soon)

| Feature | Screenshot |
| :--- | :--- |
| **Memory Map** | placeholder |
| **Page Fault Timeline** | placeholder |
| **Analytics Charts** | placeholder |

-----

## 🧰 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Core Logic** | Python |
| **UI** | Streamlit |
| **Charts** | Plotly / Matplotlib |
| **Logging** | JSON / CSV |
| **Documentation** | Markdown |

-----

## 🚧 Future Improvements

  * Add **TLB visualization** with cache hit/miss animations.
  * Include more page replacement algorithms (e.g., Working Set, Second Chance).
  * Add real-time animation for internal and external **fragmentation**.
  * Export simulation results as PDF reports.
  * Allow user-uploaded custom memory traces via the UI.
  * Multi-language support for the UI.

-----
