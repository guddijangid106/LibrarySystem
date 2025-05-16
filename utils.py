import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def show_error(title, message):
    """Show error message box"""
    messagebox.showerror(title, message)

def show_info(title, message):
    """Show info message box"""
    messagebox.showinfo(title, message)

def show_warning(title, message):
    """Show warning message box"""
    messagebox.showwarning(title, message)

def format_date(date_str):
    """Format date string to YYYY-MM-DD"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.strftime("%Y-%m-%d")
    except ValueError:
        return date_str

def format_datetime(dt_str):
    """Format datetime string to YYYY-MM-DD HH:MM:SS"""
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return dt_str

def validate_input(value, field_name, min_length=0, max_length=None):
    """Validate input value"""
    if not value:
        return f"{field_name} cannot be empty"
    if len(value) < min_length:
        return f"{field_name} must be at least {min_length} characters"
    if max_length and len(value) > max_length:
        return f"{field_name} must be at most {max_length} characters"
    return None

def create_tooltip(widget, text):
    """Create a tooltip for a widget"""
    def show_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        
        label = tk.Label(
            tooltip,
            text=text,
            justify='left',
            background="#ffffe0",
            relief='solid',
            borderwidth=1,
            font=("Helvetica", "10")
        )
        label.pack()
        
        def hide_tooltip():
            tooltip.destroy()
        
        widget.tooltip = tooltip
        widget.bind('<Leave>', lambda e: hide_tooltip())
    
    widget.bind('<Enter>', show_tooltip)

def center_window(window):
    """Center window on screen"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def create_scrolled_frame(parent):
    """Create a scrolled frame"""
    container = tk.Frame(parent)
    canvas = tk.Canvas(container)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrolled_frame = tk.Frame(canvas)
    
    scrolled_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrolled_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    return scrolled_frame

def create_table(parent, columns, headings):
    """Create a table with headers"""
    # Create frame for table
    table_frame = tk.Frame(parent)
    table_frame.pack(fill='both', expand=True)
    
    # Create headers
    for i, heading in enumerate(headings):
        header = tk.Label(
            table_frame,
            text=heading,
            font=("Helvetica", 12, "bold"),
            relief="solid",
            borderwidth=1,
            padx=5,
            pady=5
        )
        header.grid(row=0, column=i, sticky="nsew")
    
    # Create columns
    for i in range(len(columns)):
        table_frame.grid_columnconfigure(i, weight=1)
    
    return table_frame

def add_table_row(table_frame, values, row):
    """Add a row to the table"""
    for i, value in enumerate(values):
        cell = tk.Label(
            table_frame,
            text=str(value),
            relief="solid",
            borderwidth=1,
            padx=5,
            pady=5
        )
        cell.grid(row=row, column=i, sticky="nsew") 