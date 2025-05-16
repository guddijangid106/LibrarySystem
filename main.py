import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from datetime import datetime
import threading
import time

# Import custom modules
from database import Database
from notifications import NotificationSystem
from forms import UserForm, BookForm, IssueForm
from utils import show_error, format_date, format_datetime

class ModernTheme:
    """Modern UI theme configuration"""
    COLORS = {
        'primary': '#2196F3',      # Blue
        'secondary': '#757575',    # Gray
        'success': '#4CAF50',      # Green
        'warning': '#FFC107',      # Yellow
        'danger': '#F44336',       # Red
        'background': '#FFFFFF',   # White
        'surface': '#F5F5F5',      # Light Gray
        'text': '#212121',         # Dark Gray
        'text_secondary': '#757575' # Medium Gray
    }
    
    FONTS = {
        'title': ('Helvetica', 24, 'bold'),
        'subtitle': ('Helvetica', 18, 'bold'),
        'heading': ('Helvetica', 14, 'bold'),
        'body': ('Helvetica', 12),
        'small': ('Helvetica', 10)
    }
    
    PADDING = {
        'small': 5,
        'medium': 10,
        'large': 20
    }

class ModernButton(ttk.Button):
    """Custom modern button widget"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.style = ttk.Style()
        self.style.configure(
            'Modern.TButton',
            background=ModernTheme.COLORS['primary'],
            foreground='white',
            padding=ModernTheme.PADDING['medium'],
            font=ModernTheme.FONTS['body']
        )
        self.configure(style='Modern.TButton')

class ModernEntry(ttk.Entry):
    """Custom modern entry widget"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            font=ModernTheme.FONTS['body'],
            padding=ModernTheme.PADDING['small']
        )

class ModernLabel(ttk.Label):
    """Custom modern label widget"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            font=ModernTheme.FONTS['body'],
            background=ModernTheme.COLORS['background'],
            foreground=ModernTheme.COLORS['text']
        )

class ModernFrame(ttk.Frame):
    """Custom modern frame widget"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            padding=ModernTheme.PADDING['medium'],
            style='Modern.TFrame'
        )

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Library Management System")
        self.root.geometry("1280x800")
        self.root.minsize(1024, 768)
        
        # Configure theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Initialize database
        try:
            self.db = Database()
            print("Database initialized successfully")
        except Exception as e:
            show_error("Database Error", str(e))
            self.root.destroy()
            sys.exit(1)
        
        # Initialize notification system
        self.notification_system = NotificationSystem(
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            sender_email="your-email@gmail.com",
            sender_password="your-app-password"
        )
        self.notification_system.set_database(self.db)
        
        # Start notification thread
        self.notification_thread = threading.Thread(
            target=self.check_notifications,
            daemon=True
        )
        self.notification_thread.start()
        
        # Initialize UI
        self.setup_ui()
        
        # Show welcome screen
        self.show_welcome_screen()
    
    def configure_styles(self):
        """Configure custom styles for the application"""
        self.style.configure(
            'Modern.TFrame',
            background=ModernTheme.COLORS['background']
        )
        
        self.style.configure(
            'Modern.TLabel',
            background=ModernTheme.COLORS['background'],
            foreground=ModernTheme.COLORS['text'],
            font=ModernTheme.FONTS['body']
        )
        
        self.style.configure(
            'Modern.TButton',
            background=ModernTheme.COLORS['primary'],
            foreground='white',
            padding=ModernTheme.PADDING['medium'],
            font=ModernTheme.FONTS['body']
        )
        
        self.style.map(
            'Modern.TButton',
            background=[('active', ModernTheme.COLORS['secondary'])],
            foreground=[('active', 'white')]
        )
    
    def setup_ui(self):
        """Setup the main UI components"""
        # Main container
        self.main_container = ModernFrame(self.root)
        self.main_container.pack(fill='both', expand=True)
        
        # Header
        self.header = ModernFrame(self.main_container)
        self.header.pack(fill='x', padx=20, pady=10)
        
        # Title
        self.title_label = ModernLabel(
            self.header,
            text="Library Management System",
            font=ModernTheme.FONTS['title']
        )
        self.title_label.pack(side='left')
        
        # Time display
        self.time_label = ModernLabel(
            self.header,
            font=ModernTheme.FONTS['small']
        )
        self.time_label.pack(side='right')
        self.update_time()
        
        # Content area
        self.content = ModernFrame(self.main_container)
        self.content.pack(fill='both', expand=True, padx=20, pady=10)
    
    def show_welcome_screen(self):
        """Show the welcome screen with quick access buttons"""
        # Clear content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Welcome message
        welcome_frame = ModernFrame(self.content)
        welcome_frame.pack(fill='both', expand=True, pady=50)
        
        ModernLabel(
            welcome_frame,
            text="Welcome to the Library Management System",
            font=ModernTheme.FONTS['subtitle']
        ).pack(pady=20)
        
        # Quick access buttons
        buttons_frame = ModernFrame(welcome_frame)
        buttons_frame.pack(pady=30)
        
        buttons = [
            ("Login", self.show_login),
            ("View Available Books", self.show_available_books),
            ("View Overdue Books", self.show_overdue_books),
            ("Exit", self.root.destroy)
        ]
        
        for text, command in buttons:
            ModernButton(
                buttons_frame,
                text=text,
                command=command
            ).pack(pady=10, fill='x')
    
    def show_login(self):
        """Show the login screen"""
        # Clear content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Login form
        login_frame = ModernFrame(self.content)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        ModernLabel(
            login_frame,
            text="Login",
            font=ModernTheme.FONTS['subtitle']
        ).pack(pady=20)
        
        # Username
        username_frame = ModernFrame(login_frame)
        username_frame.pack(fill='x', pady=5)
        
        ModernLabel(
            username_frame,
            text="Username:"
        ).pack(side='left', padx=5)
        
        self.username_var = tk.StringVar()
        ModernEntry(
            username_frame,
            textvariable=self.username_var
        ).pack(side='left', padx=5)
        
        # Password
        password_frame = ModernFrame(login_frame)
        password_frame.pack(fill='x', pady=5)
        
        ModernLabel(
            password_frame,
            text="Password:"
        ).pack(side='left', padx=5)
        
        self.password_var = tk.StringVar()
        ModernEntry(
            password_frame,
            textvariable=self.password_var,
            show='•'
        ).pack(side='left', padx=5)
        
        # Login button
        ModernButton(
            login_frame,
            text="Login",
            command=self.login
        ).pack(pady=20)
    
    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.configure(text=f"Current Time: {current_time}")
        self.root.after(1000, self.update_time)
    
    def check_notifications(self):
        """Check for notifications in the background"""
        while True:
            try:
                self.notification_system.check_and_send_reminders()
            except Exception as e:
                print(f"Notification error: {str(e)}")
            time.sleep(3600)  # Check every hour
    
    def login(self):
        """Handle user login"""
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        result = self.db.verify_user(username, password)
        if result:
            self.current_user = result[0]
            self.current_role = result[1]
            if self.current_role == 'admin':
                self.show_admin_dashboard()
            else:
                self.show_student_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def show_available_books(self):
        """Show available books screen"""
        # Clear content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Create main frame
        main_frame = ModernFrame(self.content)
        main_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ModernFrame(main_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ModernLabel(
            header_frame,
            text="Available Books",
            font=ModernTheme.FONTS['subtitle']
        ).pack(side='left')
        
        # Search frame
        search_frame = ModernFrame(main_frame)
        search_frame.pack(fill='x', pady=(0, 20))
        
        ModernLabel(
            search_frame,
            text="Search:"
        ).pack(side='left', padx=5)
        
        self.search_var = tk.StringVar()
        search_entry = ModernEntry(
            search_frame,
            textvariable=self.search_var,
            width=40
        )
        search_entry.pack(side='left', padx=5)
        
        ModernButton(
            search_frame,
            text="Search",
            command=self.search_books
        ).pack(side='left', padx=5)
        
        # Books list frame
        list_frame = ModernFrame(main_frame)
        list_frame.pack(fill='both', expand=True)
        
        # Create Treeview
        columns = ('Title', 'Author', 'Category', 'ISBN', 'Year')
        self.books_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Configure columns
        for col in columns:
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.books_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load available books
        self.load_available_books()
    
    def load_available_books(self):
        """Load available books into the treeview"""
        try:
            # Clear existing items
            for item in self.books_tree.get_children():
                self.books_tree.delete(item)
            
            # Get available books
            books = self.db.get_available_books()
            
            # Insert books into treeview
            for book in books:
                self.books_tree.insert('', 'end', values=(
                    book['title'],
                    book['author'],
                    book['category'],
                    book['isbn'],
                    book['publication_year']
                ))
        except Exception as e:
            show_error("Error", f"Failed to load books: {str(e)}")
    
    def search_books(self):
        """Search books based on search term"""
        search_term = self.search_var.get().strip().lower()
        if not search_term:
            self.load_available_books()
            return
        
        try:
            # Clear existing items
            for item in self.books_tree.get_children():
                self.books_tree.delete(item)
            
            # Get all books
            books = self.db.get_available_books()
            
            # Filter books based on search term
            filtered_books = [
                book for book in books
                if search_term in book['title'].lower() or
                   search_term in book['author'].lower() or
                   search_term in book['category'].lower() or
                   search_term in book['isbn'].lower()
            ]
            
            # Insert filtered books into treeview
            for book in filtered_books:
                self.books_tree.insert('', 'end', values=(
                    book['title'],
                    book['author'],
                    book['category'],
                    book['isbn'],
                    book['publication_year']
                ))
        except Exception as e:
            show_error("Error", f"Failed to search books: {str(e)}")

def main():
    try:
        # Check for locked database
        if os.path.exists('library.db'):
            try:
                with open('library.db', 'a'):
                    pass
            except IOError:
                print("Database file is locked. Please close any other instances of the application.")
                sys.exit(1)
        
        # Create and run application
        root = tk.Tk()
        app = LibraryApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Application error: {str(e)}")
        if 'root' in locals():
            root.destroy()
        sys.exit(1)

if __name__ == "__main__":
    main() 