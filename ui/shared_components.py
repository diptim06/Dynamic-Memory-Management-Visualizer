"""
Shared UI Components
Reusable Streamlit components for the memory visualizer.
"""

import streamlit as st
from typing import List, Dict, Optional


def header(title: str = "Dynamic Memory Management Visualizer", subtitle: str = ""):
    """
    Render a styled header.
    
    Args:
        title: Main title
        subtitle: Optional subtitle
    """
    st.markdown(
        f"""
        <div class="main-header">
            <h1>{title}</h1>
            {f'<p>{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True
    )


def footer():
    """Render a styled footer."""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #6c757d; padding: 1rem;'>
            <p>Dynamic Memory Management Visualizer &copy; 2024</p>
            <p>Built with Streamlit | Python</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def memory_visualizer(
    frames: List[Dict],
    title: str = "Physical Memory Layout",
    show_labels: bool = True
) -> None:
    """
    Visualize physical memory frames.
    
    Args:
        frames: List of frame dictionaries with keys: frame_id, status, process_id, page_id
        title: Title for the visualization
        show_labels: Whether to show frame labels
    """
    st.markdown(f"### {title}")
    
    # Group frames in rows (4 per row)
    cols_per_row = 4
    num_rows = (len(frames) + cols_per_row - 1) // cols_per_row
    
    for row in range(num_rows):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            frame_idx = row * cols_per_row + col_idx
            if frame_idx < len(frames):
                frame = frames[frame_idx]
                with cols[col_idx]:
                    render_frame(frame, show_labels)


def render_frame(frame: Dict, show_labels: bool = True) -> None:
    """
    Render a single memory frame.
    
    Args:
        frame: Frame dictionary
        show_labels: Whether to show labels
    """
    status = frame.get("status", "FREE")
    frame_id = frame.get("frame_id", 0)
    process_id = frame.get("process_id")
    page_id = frame.get("page_id")
    
    css_class = "allocated" if status == "ALLOCATED" else "free"
    
    info = f"Frame {frame_id}"
    if status == "ALLOCATED" and process_id is not None:
        info += f"<br>P{process_id}"
        if page_id is not None:
            info += f"|Page {page_id}"
    else:
        info += "<br>FREE"
    
    st.markdown(
        f"""
        <div class="memory-frame {css_class}">
            {info}
        </div>
        """,
        unsafe_allow_html=True
    )


def stats_box(stats: Dict, title: str = "Statistics") -> None:
    """
    Display statistics in a styled box.
    
    Args:
        stats: Dictionary of statistics
        title: Box title
    """
    st.markdown(f"### {title}")
    
    stats_html = "<div class='stats-box'>"
    stats_html += f"<h4>{title}</h4>"
    stats_html += "<table style='width: 100%;'>"
    
    for key, value in stats.items():
        # Format key (convert snake_case to Title Case)
        formatted_key = key.replace("_", " ").title()
        
        # Format value
        if isinstance(value, float):
            formatted_value = f"{value:.2f}"
            if "percent" in key.lower() or "rate" in key.lower():
                formatted_value += "%"
        else:
            formatted_value = str(value)
        
        stats_html += f"<tr><td style='font-weight: bold;'>{formatted_key}:</td>"
        stats_html += f"<td style='text-align: right;'>{formatted_value}</td></tr>"
    
    stats_html += "</table></div>"
    st.markdown(stats_html, unsafe_allow_html=True)


def info_box(message: str, type: str = "info") -> None:
    """
    Display an info/warning/error box.
    
    Args:
        message: Message to display
        type: Type of box ("info", "warning", "error")
    """
    css_class = f"{type}-box"
    st.markdown(
        f"""
        <div class="{css_class}">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )


def page_table_visualizer(page_table: List[Dict], title: str = "Page Table") -> None:
    """
    Visualize a page table.
    
    Args:
        page_table: List of page table entries
        title: Title for the visualization
    """
    st.markdown(f"### {title}")
    
    if not page_table:
        st.info("No pages in table")
        return
    
    # Create table
    table_html = "<table style='width: 100%; border-collapse: collapse;'>"
    table_html += "<thead><tr style='background-color: #667eea; color: white;'>"
    table_html += "<th style='padding: 0.5rem; border: 1px solid #dee2e6;'>Page ID</th>"
    table_html += "<th style='padding: 0.5rem; border: 1px solid #dee2e6;'>Frame ID</th>"
    table_html += "<th style='padding: 0.5rem; border: 1px solid #dee2e6;'>Present</th>"
    table_html += "<th style='padding: 0.5rem; border: 1px solid #dee2e6;'>Modified</th>"
    table_html += "<th style='padding: 0.5rem; border: 1px solid #dee2e6;'>Status</th>"
    table_html += "</tr></thead><tbody>"
    
    for entry in page_table:
        present = "✓" if entry.get("present", False) else "✗"
        modified = "✓" if entry.get("modified", False) else "✗"
        frame_id = entry.get("frame_id", "N/A")
        status = entry.get("status", "UNKNOWN")
        
        row_class = "present" if entry.get("present", False) else "not-present"
        table_html += f"<tr class='page-table-entry {row_class}'>"
        table_html += f"<td style='padding: 0.5rem; border: 1px solid #dee2e6;'>{entry.get('page_id', 'N/A')}</td>"
        table_html += f"<td style='padding: 0.5rem; border: 1px solid #dee2e6;'>{frame_id}</td>"
        table_html += f"<td style='padding: 0.5rem; border: 1px solid #dee2e6; text-align: center;'>{present}</td>"
        table_html += f"<td style='padding: 0.5rem; border: 1px solid #dee2e6; text-align: center;'>{modified}</td>"
        table_html += f"<td style='padding: 0.5rem; border: 1px solid #dee2e6;'>{status}</td>"
        table_html += "</tr>"
    
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)
