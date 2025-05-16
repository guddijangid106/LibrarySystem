import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import Database
from datetime import datetime, timedelta
from notifications import NotificationSystem
from forms import UserForm, BookForm, IssueForm, show_validation_errors, format_date, format_datetime
import threading
import time
import sys
import traceback
import os

def show_error(title, message):
    """Show error message and print to console"""
    print(f"Error: {title} - {message}")
    messagebox.showerror(title, message)

class MainMenuForm:
    def __init__(self, parent):
        try:
            self.parent = parent
            self.window = parent.root  # Use parent's root window
            self.window.title("Library Management System")
            
            # Get screen dimensions
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            
            # Set window size to 90% of screen size
            window_width = int(screen_width * 0.9)
            window_height = int(screen_height * 0.9)
            
            # Calculate position for center of screen
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            # Set window size and position
            self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            # Configure style
            self.style = ttk.Style()
            self.style.theme_use('clam')
            
            # Configure colors
            self.bg_color = "#f5f5f5"
            self.accent_color = "#2196F3"
            self.text_color = "#333333"
            self.hover_color = "#1976D2"
            
            # Configure styles
            self.style.configure("TFrame", background=self.bg_color)
            self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color)
            self.style.configure("TButton", 
                               background=self.accent_color,
                               foreground="white",
                               padding=15,
                               font=('Helvetica', 12, 'bold'))
            self.style.map("TButton",
                          background=[('active', self.hover_color)],
                          foreground=[('active', 'white')])
            
            self.window.configure(bg=self.bg_color)
            
            # Create main container
            self.main_frame = ttk.Frame(self.window, padding="40")
            self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
            
            # Create widgets
            self.create_widgets()
            print("Main menu form created successfully")
        except Exception as e:
            show_error("Error", f"Failed to create main menu: {str(e)}")
            traceback.print_exc()
            raise
    
    def create_widgets(self):
        # Title with modern styling
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill="x", pady=(0, 40))
        
        ttk.Label(title_frame,
                 text="Library Management System",
                 font=("Helvetica", 36, "bold"),
                 foreground=self.accent_color).pack()
        
        ttk.Label(title_frame,
                 text="Welcome to the Library Management System",
                 font=("Helvetica", 16),
                 foreground=self.text_color).pack(pady=(10, 0))
        
        # Features Section with modern card-like design
        features_frame = ttk.LabelFrame(self.main_frame, 
                                      text="System Features",
                                      padding="30",
                                      style="Card.TLabelframe")
        features_frame.pack(fill="x", pady=(0, 30))
        
        # Configure card style
        self.style.configure("Card.TLabelframe",
                           background="white",
                           foreground=self.text_color,
                           borderwidth=2,
                           relief="solid")
        self.style.configure("Card.TLabelframe.Label",
                           font=("Helvetica", 14, "bold"),
                           foreground=self.accent_color)
        
        # Reduced features list
        features = [
            "User Management: Add and manage users (admin/student)",
            "Book Management: Add, issue, and return books",
            "Search & Filter: Advanced search and filtering options",
            "Due Date Tracking: Automatic due date calculation"
        ]
        
        for feature in features:
            feature_frame = ttk.Frame(features_frame, padding="10")
            feature_frame.pack(fill="x", pady=5)
            
            ttk.Label(feature_frame,
                     text="•",
                     font=("Helvetica", 12, "bold"),
                     foreground=self.accent_color).pack(side="left", padx=(0, 10))
            
            ttk.Label(feature_frame,
                     text=feature,
                     font=("Helvetica", 12),
                     wraplength=800).pack(side="left", fill="x")
        
        # Quick Access Buttons with modern styling
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill="x", pady=(0, 20))
        
        # Main action buttons
        login_button = ttk.Button(buttons_frame,
                                text="Login",
                                command=self.show_login,
                                style="Action.TButton",
                                width=20)
        login_button.pack(side="left", expand=True, padx=5)
        
        exit_button = ttk.Button(buttons_frame,
                               text="Exit",
                               command=self.window.destroy,
                               style="Action.TButton",
                               width=20)
        exit_button.pack(side="right", expand=True, padx=5)
        
        # Configure button styles
        self.style.configure("Action.TButton",
                           background=self.accent_color,
                           foreground="white",
                           padding=15,
                           font=('Helvetica', 14, 'bold'))
        self.style.map("Action.TButton",
                      background=[('active', self.hover_color)],
                      foreground=[('active', 'white')])
    
    def show_login(self):
        self.clear_window()
        self.parent.show_login_frame()
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.window.winfo_children():
            widget.destroy()

class LibraryGUI:
    def __init__(self, root):
        try:
            print("Initializing Library Management System...")
            self.root = root
            self.root.title("Library Management System")
            
            # Get screen dimensions
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Set window size to 90% of screen size
            window_width = int(screen_width * 0.9)
            window_height = int(screen_height * 0.9)
            
            # Calculate position for center of screen
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            # Set window size and position
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            # Configure style
            self.style = ttk.Style()
            self.style.theme_use('clam')
            
            # Configure colors
            self.bg_color = "#f5f5f5"
            self.accent_color = "#2196F3"
            self.text_color = "#333333"
            self.hover_color = "#1976D2"
            
            # Configure styles
            self.style.configure("TFrame", background=self.bg_color)
            self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color)
            self.style.configure("TButton", 
                               background=self.accent_color,
                               foreground="white",
                               padding=15,
                               font=('Helvetica', 12, 'bold'))
            self.style.map("TButton",
                          background=[('active', self.hover_color)],
                          foreground=[('active', 'white')])
            
            self.root.configure(bg=self.bg_color)
            
            # Initialize StringVar variables
            print("Initializing variables...")
            self.username_var = tk.StringVar()
            self.password_var = tk.StringVar()
            self.new_username_var = tk.StringVar()
            self.new_password_var = tk.StringVar()
            self.new_email_var = tk.StringVar()
            self.new_roll_number_var = tk.StringVar()
            self.role_var = tk.StringVar(value="student")
            self.book_title_var = tk.StringVar()
            self.book_author_var = tk.StringVar()
            self.book_category_var = tk.StringVar()
            self.book_isbn_var = tk.StringVar()
            self.book_year_var = tk.StringVar()
            self.book_description_var = tk.StringVar()
            self.search_var = tk.StringVar()
            self.category_var = tk.StringVar()
            self.year_var = tk.StringVar()
            self.status_var = tk.StringVar(value="All")
            
            print("Initializing database...")
            self.db = Database()
            self.current_user = None
            self.current_role = None
            
            print("Initializing notification system...")
            self.notification_system = NotificationSystem(
                smtp_server="smtp.gmail.com",
                smtp_port=587,
                sender_email="your-email@gmail.com",
                sender_password="your-app-password"
            )
            self.notification_system.set_database(self.db)
            
            print("Starting notification thread...")
            self.notification_thread = threading.Thread(target=self.check_notifications, daemon=True)
            self.notification_thread.start()
            
            print("Showing main menu...")
            self.show_main_menu()
            print("Initialization complete!")
        except Exception as e:
            show_error("Initialization Error", f"Failed to initialize application: {str(e)}")
            traceback.print_exc()
            if hasattr(self, 'root'):
                self.root.destroy()
            raise
    
    def show_main_menu(self):
        """Show the main menu"""
        try:
            self.clear_window()
            
            # Create main container with padding
            main_frame = ttk.Frame(self.root, padding="40")
            main_frame.pack(fill="both", expand=True)
            
            # Title with modern styling
            title_frame = ttk.Frame(main_frame)
            title_frame.pack(fill="x", pady=(0, 40))
            
            ttk.Label(
                title_frame,
                text="Library Management System",
                font=("Helvetica", 36, "bold"),
                foreground=self.accent_color
            ).pack()
            
            ttk.Label(
                title_frame,
                text="Welcome to the Library Management System",
                font=("Helvetica", 16),
                foreground=self.text_color
            ).pack(pady=(10, 0))
            
            # Features Section with modern card-like design
            features_frame = ttk.LabelFrame(
                main_frame,
                text="System Features",
                padding="30",
                style="Card.TLabelframe"
            )
            features_frame.pack(fill="x", pady=(0, 30))
            
            # Configure card style
            self.style.configure(
                "Card.TLabelframe",
                background="white",
                foreground=self.text_color,
                borderwidth=2,
                relief="solid"
            )
            self.style.configure(
                "Card.TLabelframe.Label",
                font=("Helvetica", 14, "bold"),
                foreground=self.accent_color
            )
            
            # Features list
            features = [
                "User Management: Add and manage users (admin/student)",
                "Book Management: Add, issue, and return books",
                "Search & Filter: Advanced search and filtering options",
                "Due Date Tracking: Automatic due date calculation"
            ]
            
            for feature in features:
                feature_frame = ttk.Frame(features_frame, padding="10")
                feature_frame.pack(fill="x", pady=5)
                
                ttk.Label(
                    feature_frame,
                    text="•",
                    font=("Helvetica", 12, "bold"),
                    foreground=self.accent_color
                ).pack(side="left", padx=(0, 10))
                
                ttk.Label(
                    feature_frame,
                    text=feature,
                    font=("Helvetica", 12),
                    wraplength=800
                ).pack(side="left", fill="x")
            
            # Quick Access Buttons with modern styling
            buttons_frame = ttk.Frame(main_frame)
            buttons_frame.pack(fill="x", pady=(0, 20))
            
            # Main action buttons
            login_button = ttk.Button(
                buttons_frame,
                text="Login",
                command=self.show_login_frame,
                style="Action.TButton",
                width=20
            )
            login_button.pack(side="left", expand=True, padx=5)
            
            exit_button = ttk.Button(
                buttons_frame,
                text="Exit",
                command=self.root.destroy,
                style="Action.TButton",
                width=20
            )
            exit_button.pack(side="right", expand=True, padx=5)
            
            # Configure button styles
            self.style.configure(
                "Action.TButton",
                background=self.accent_color,
                foreground="white",
                padding=15,
                font=('Helvetica', 14, 'bold')
            )
            self.style.map(
                "Action.TButton",
                background=[('active', self.hover_color)],
                foreground=[('active', 'white')]
            )
            
            print("Main menu displayed successfully")
        except Exception as e:
            print(f"Error showing main menu: {str(e)}")
            traceback.print_exc()
    
    def check_notifications(self):
        while True:
            self.notification_system.check_and_send_reminders()
            time.sleep(3600)  # Check every hour
    
    def show_login_frame(self):
        """Show the login form"""
        self.clear_window()
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="40")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title with modern styling
        title_label = ttk.Label(main_frame, 
                              text="Library Management System",
                              font=("Helvetica", 32, "bold"),
                              foreground=self.accent_color)
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 40))
        
        # Login form with card-like design
        form_frame = ttk.LabelFrame(main_frame, 
                                  text="Login",
                                  padding="30",
                                  style="Card.TLabelframe")
        form_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Role selection first
        ttk.Label(form_frame,
                 text="Login as:",
                 font=("Helvetica", 12)).grid(row=0, column=0, pady=10, padx=5, sticky="e")
        
        role_frame = ttk.Frame(form_frame)
        role_frame.grid(row=0, column=1, sticky="w", pady=10, padx=5)
        
        ttk.Radiobutton(role_frame,
                       text="Admin",
                       variable=self.role_var,
                       value="admin",
                       style="TRadiobutton").pack(side="left", padx=10)
        
        ttk.Radiobutton(role_frame,
                       text="Student",
                       variable=self.role_var,
                       value="student",
                       style="TRadiobutton").pack(side="left", padx=10)
        
        # Username field
        ttk.Label(form_frame,
                 text="Username:",
                 font=("Helvetica", 12)).grid(row=1, column=0, pady=10, padx=5, sticky="e")
        ttk.Entry(form_frame,
                 textvariable=self.username_var,
                 font=("Helvetica", 12),
                 width=30).grid(row=1, column=1, pady=10, padx=5, sticky="w")
        
        # Password field
        ttk.Label(form_frame,
                 text="Password:",
                 font=("Helvetica", 12)).grid(row=2, column=0, pady=10, padx=5, sticky="e")
        
        password_frame = ttk.Frame(form_frame)
        password_frame.grid(row=2, column=1, sticky="w", pady=10, padx=5)
        
        self.password_entry = ttk.Entry(password_frame,
                                      textvariable=self.password_var,
                                      show="•",
                                      font=("Helvetica", 12),
                                      width=30)
        self.password_entry.pack(side="left")
        
        self.show_password_var = tk.BooleanVar(value=False)
        show_password_check = ttk.Checkbutton(password_frame,
                                            text="Show",
                                            variable=self.show_password_var,
                                            command=self.toggle_password_visibility)
        show_password_check.pack(side="left", padx=5)
        
        # Buttons with modern styling
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        login_button = ttk.Button(button_frame,
                                text="Login",
                                command=self.login,
                                style="TButton",
                                width=20)
        login_button.pack(side="left", padx=5)
        
        back_button = ttk.Button(button_frame,
                               text="Back to Main Menu",
                               command=self.show_main_menu,
                               style="TButton",
                               width=20)
        back_button.pack(side="left", padx=5)
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="•")
    
    def login(self):
        """Handle user login from the login form."""
        try:
            username = self.username_var.get().strip()
            password = self.password_var.get()
            role = self.role_var.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Please enter both username and password.")
                return
            
            print(f"Attempting login for user: {username} with role: {role}")
            
            # Get user data from database
            cursor = self.db.conn.cursor()
            hashed_password = self.db.hash_password(password)
            cursor.execute('''
                SELECT id, username, email, role, roll_number
                FROM users
                WHERE username = ? AND password = ? AND role = ?
            ''', (username, hashed_password, role))
            user = cursor.fetchone()
            
            if user:
                print(f"Login successful for user: {username}")
                self.current_user = {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role'],
                    'roll_number': user['roll_number']
                }
                self.current_role = user['role']
                
                # Clear login form
                self.username_var.set("")
                self.password_var.set("")
                
                # Show appropriate dashboard
                if role == "admin":
                    print("Showing admin dashboard")
                    self.show_admin_dashboard()
                else:
                    print("Showing student dashboard")
                    self.show_student_dashboard()
            else:
                print(f"Login failed for user: {username}")
                messagebox.showerror("Login Failed", "Invalid username, password, or role.")
        except Exception as e:
            print(f"Login error: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Login failed: {str(e)}")

    def show_admin_dashboard(self):
        """Show the admin dashboard with sidebar"""
        try:
            print("Initializing admin dashboard...")
            self.clear_window()
            
            # Create main container
            main_container = ttk.Frame(self.root)
            main_container.pack(fill="both", expand=True)
            
            # Create sidebar
            sidebar = ttk.Frame(main_container, style="Sidebar.TFrame")
            sidebar.pack(side="left", fill="y", padx=0, pady=0)
            
            # Configure sidebar style
            self.style.configure("Sidebar.TFrame", background="#2c3e50")
            self.style.configure("Sidebar.TButton",
                               background="#2c3e50",
                               foreground="white",
                               padding=10,
                               font=('Helvetica', 12))
            self.style.map("Sidebar.TButton",
                          background=[('active', '#34495e')],
                          foreground=[('active', 'white')])
            
            # Add logo/title to sidebar
            ttk.Label(sidebar,
                     text="Library Admin",
                     font=('Helvetica', 16, 'bold'),
                     foreground="white",
                     background="#2c3e50",
                     padding=20).pack(fill="x")
            
            # Sidebar buttons
            menu_items = [
                ("Dashboard", self.show_admin_dashboard),
                ("Add Book", self.show_add_book),
                ("View Books", self.show_view_books),
                ("Issue Book", self.show_issue_book),
                ("Return Book", self.show_return_book),
                ("Add User", self.show_add_user),
                ("View Users", self.show_users),
                ("Logout", self.logout)
            ]
            
            for text, command in menu_items:
                btn = ttk.Button(sidebar,
                               text=text,
                               command=command,
                               style="Sidebar.TButton",
                               width=20)
                btn.pack(fill="x", padx=5, pady=2)
            
            # Main content area
            content = ttk.Frame(main_container, padding="20")
            content.pack(side="right", fill="both", expand=True)
            
            # Welcome header
            header = ttk.Frame(content)
            header.pack(fill="x", pady=(0, 20))
            
            ttk.Label(header,
                     text=f"Welcome, {self.current_user['username']}!",
                     font=('Helvetica', 24, 'bold'),
                     foreground=self.accent_color).pack(side="left")
            
            # Quick stats section
            stats_frame = ttk.LabelFrame(content, text="Quick Stats", padding="20")
            stats_frame.pack(fill="x", pady=(0, 20))
            
            try:
                total_books = len(self.db.get_all_books())
                available_books = len(self.db.get_available_books())
                total_users = len(self.db.get_all_users())
                
                stats = [
                    ("Total Books", total_books, "#4CAF50"),
                    ("Available Books", available_books, "#2196F3"),
                    ("Total Users", total_users, "#9C27B0")
                ]
                
                for i, (label, value, color) in enumerate(stats):
                    stat_frame = ttk.Frame(stats_frame)
                    stat_frame.grid(row=0, column=i, padx=20, pady=10, sticky="nsew")
                    
                    ttk.Label(stat_frame,
                             text=str(value),
                             font=('Helvetica', 32, 'bold'),
                             foreground=color).pack()
                    
                    ttk.Label(stat_frame,
                             text=label,
                             font=('Helvetica', 12)).pack()
                
                stats_frame.grid_columnconfigure(0, weight=1)
                stats_frame.grid_columnconfigure(1, weight=1)
                stats_frame.grid_columnconfigure(2, weight=1)
                
            except Exception as e:
                print(f"Error loading stats: {str(e)}")
                messagebox.showerror("Error", f"Failed to load statistics: {str(e)}")
            
            print("Admin dashboard displayed successfully")
        except Exception as e:
            print(f"Error showing admin dashboard: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to show admin dashboard: {str(e)}")

    def logout(self):
        """Handle user logout"""
        try:
            print("Logging out...")
            self.current_user = None
            self.current_role = None
            self.show_main_menu()
            print("Logout successful")
        except Exception as e:
            print(f"Logout error: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Logout failed: {str(e)}")

    def show_student_dashboard(self):
        """Show student dashboard with sidebar"""
        try:
            print("Initializing student dashboard...")
            self.clear_window()
            
            # Create main container
            main_container = ttk.Frame(self.root)
            main_container.pack(fill="both", expand=True)
            
            # Create sidebar
            sidebar = ttk.Frame(main_container, style="Sidebar.TFrame")
            sidebar.pack(side="left", fill="y", padx=0, pady=0)
            
            # Configure sidebar style
            self.style.configure("Sidebar.TFrame", background="#2c3e50")
            self.style.configure("Sidebar.TButton",
                               background="#2c3e50",
                               foreground="white",
                               padding=10,
                               font=('Helvetica', 12))
            self.style.map("Sidebar.TButton",
                          background=[('active', '#34495e')],
                          foreground=[('active', 'white')])
            
            # Add logo/title to sidebar
            ttk.Label(sidebar,
                     text="Student Portal",
                     font=('Helvetica', 16, 'bold'),
                     foreground="white",
                     background="#2c3e50",
                     padding=20).pack(fill="x")
            
            # Sidebar buttons
            menu_items = [
                ("Dashboard", self.show_student_dashboard),
                ("View My Books", self.show_my_books),
                ("Available Books", self.show_available_books),
                ("Logout", self.logout)
            ]
            
            for text, command in menu_items:
                btn = ttk.Button(sidebar,
                               text=text,
                               command=command,
                               style="Sidebar.TButton",
                               width=20)
                btn.pack(fill="x", padx=5, pady=2)
            
            # Main content area
            content = ttk.Frame(main_container, padding="20")
            content.pack(side="right", fill="both", expand=True)
            
            # Welcome header
            header = ttk.Frame(content)
            header.pack(fill="x", pady=(0, 20))
            
            ttk.Label(header,
                     text=f"Welcome, {self.current_user['username']}!",
                     font=('Helvetica', 24, 'bold'),
                     foreground=self.accent_color).pack(side="left")
            
            # Stats section
            stats_frame = ttk.LabelFrame(content, text="My Library Stats", padding="20")
            stats_frame.pack(fill="x", pady=(0, 20))
            
            try:
                issued_books = self.db.get_user_issued_books(self.current_user['id'])
                available_books = self.db.get_available_books()
                
                stats = [
                    ("Books Issued", len(issued_books), "#4CAF50"),
                    ("Available Books", len(available_books), "#2196F3")
                ]
                
                for i, (label, value, color) in enumerate(stats):
                    stat_frame = ttk.Frame(stats_frame)
                    stat_frame.grid(row=0, column=i, padx=20, pady=10, sticky="nsew")
                    
                    ttk.Label(stat_frame,
                             text=str(value),
                             font=('Helvetica', 32, 'bold'),
                             foreground=color).pack()
                    
                    ttk.Label(stat_frame,
                             text=label,
                             font=('Helvetica', 12)).pack()
                
                stats_frame.grid_columnconfigure(0, weight=1)
                stats_frame.grid_columnconfigure(1, weight=1)
                
            except Exception as e:
                print(f"Error loading stats: {str(e)}")
                messagebox.showerror("Error", f"Failed to load statistics: {str(e)}")
            
            # My books section
            books_frame = ttk.LabelFrame(content, text="My Issued Books", padding="20")
            books_frame.pack(fill="both", expand=True)
            
            # Create Treeview
            columns = ('Title', 'Author', 'Issue Date', 'Due Date', 'Status')
            tree = ttk.Treeview(books_frame, columns=columns, show='headings')
            
            # Configure columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(books_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            # Pack tree and scrollbar
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Load issued books
            try:
                for book in issued_books:
                    tree.insert('', 'end', values=(
                        book['title'],
                        book['author'],
                        book['issue_date'],
                        book['due_date'],
                        'Overdue' if book['is_overdue'] else 'Active'
                    ))
            except Exception as e:
                print(f"Error loading issued books: {str(e)}")
                messagebox.showerror("Error", f"Failed to load issued books: {str(e)}")
            
            print("Student dashboard displayed successfully")
        except Exception as e:
            print(f"Error showing student dashboard: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to show student dashboard: {str(e)}")

    def show_my_books(self):
        """Show books issued to the current student"""
        try:
            print("Showing my books...")
            self.clear_window()
            
            # Create main container
            main_container = ttk.Frame(self.root)
            main_container.pack(fill="both", expand=True)
            
            # Create sidebar
            sidebar = ttk.Frame(main_container, style="Sidebar.TFrame")
            sidebar.pack(side="left", fill="y", padx=0, pady=0)
            
            # Configure sidebar style
            self.style.configure("Sidebar.TFrame", background="#2c3e50")
            self.style.configure("Sidebar.TButton",
                               background="#2c3e50",
                               foreground="white",
                               padding=10,
                               font=('Helvetica', 12))
            self.style.map("Sidebar.TButton",
                          background=[('active', '#34495e')],
                          foreground=[('active', 'white')])
            
            # Add logo/title to sidebar
            ttk.Label(sidebar,
                     text="Student Portal",
                     font=('Helvetica', 16, 'bold'),
                     foreground="white",
                     background="#2c3e50",
                     padding=20).pack(fill="x")
            
            # Sidebar buttons
            menu_items = [
                ("Dashboard", self.show_student_dashboard),
                ("View My Books", self.show_my_books),
                ("Available Books", self.show_available_books),
                ("Logout", self.logout)
            ]
            
            for text, command in menu_items:
                btn = ttk.Button(sidebar,
                               text=text,
                               command=command,
                               style="Sidebar.TButton",
                               width=20)
                btn.pack(fill="x", padx=5, pady=2)
            
            # Main content area
            content = ttk.Frame(main_container, padding="20")
            content.pack(side="right", fill="both", expand=True)
            
            # Header
            header = ttk.Frame(content)
            header.pack(fill="x", pady=(0, 20))
            
            ttk.Label(header,
                     text="My Issued Books",
                     font=('Helvetica', 24, 'bold'),
                     foreground=self.accent_color).pack(side="left")
            
            # Books list frame
            list_frame = ttk.LabelFrame(content, text="Issued Books", padding="20")
            list_frame.pack(fill="both", expand=True)
            
            # Create Treeview
            columns = ('Title', 'Author', 'Issue Date', 'Due Date', 'Status')
            tree = ttk.Treeview(list_frame, columns=columns, show='headings')
            
            # Configure columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            # Pack tree and scrollbar
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Load issued books
            try:
                issued_books = self.db.get_user_issued_books(self.current_user['id'])
                for book in issued_books:
                    tree.insert('', 'end', values=(
                        book['title'],
                        book['author'],
                        book['issue_date'],
                        book['due_date'],
                        'Overdue' if book['is_overdue'] else 'Active'
                    ))
            except Exception as e:
                print(f"Error loading issued books: {str(e)}")
                messagebox.showerror("Error", f"Failed to load issued books: {str(e)}")
            
            print("My books screen displayed successfully")
        except Exception as e:
            print(f"Error showing my books: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to show my books: {str(e)}")

    def show_add_user(self):
        """Show the add user form"""
        try:
            print("Showing add user form...")
            self.clear_window()
            
            # Create main container
            main_container = ttk.Frame(self.root)
            main_container.pack(fill="both", expand=True)
            
            # Create sidebar
            sidebar = ttk.Frame(main_container, style="Sidebar.TFrame")
            sidebar.pack(side="left", fill="y", padx=0, pady=0)
            
            # Configure sidebar style
            self.style.configure("Sidebar.TFrame", background="#2c3e50")
            self.style.configure("Sidebar.TButton",
                               background="#2c3e50",
                               foreground="white",
                               padding=10,
                               font=('Helvetica', 12))
            self.style.map("Sidebar.TButton",
                          background=[('active', '#34495e')],
                          foreground=[('active', 'white')])
            
            # Add logo/title to sidebar
            ttk.Label(sidebar,
                     text="Library Admin",
                     font=('Helvetica', 16, 'bold'),
                     foreground="white",
                     background="#2c3e50",
                     padding=20).pack(fill="x")
            
            # Sidebar buttons
            menu_items = [
                ("Dashboard", self.show_admin_dashboard),
                ("Add Book", self.show_add_book),
                ("View Books", self.show_view_books),
                ("Issue Book", self.show_issue_book),
                ("Return Book", self.show_return_book),
                ("Add User", self.show_add_user),
                ("View Users", self.show_users),
                ("Logout", self.logout)
            ]
            
            for text, command in menu_items:
                btn = ttk.Button(sidebar,
                               text=text,
                               command=command,
                               style="Sidebar.TButton",
                               width=20)
                btn.pack(fill="x", padx=5, pady=2)
            
            # Main content area
            content = ttk.Frame(main_container, padding="20")
            content.pack(side="right", fill="both", expand=True)
            
            # Header
            header = ttk.Frame(content)
            header.pack(fill="x", pady=(0, 20))
            
            ttk.Label(header,
                     text="Add New User",
                     font=('Helvetica', 24, 'bold'),
                     foreground=self.accent_color).pack(side="left")
            
            # Form frame
            form_frame = ttk.LabelFrame(content, text="User Details", padding="20")
            form_frame.pack(fill="x", pady=(0, 20))
            
            # Username
            ttk.Label(form_frame,
                     text="Username:",
                     font=('Helvetica', 12)).grid(row=0, column=0, pady=10, padx=5, sticky="e")
            
            username_var = tk.StringVar()
            username_entry = ttk.Entry(form_frame,
                                     textvariable=username_var,
                                     font=('Helvetica', 12),
                                     width=30)
            username_entry.grid(row=0, column=1, pady=10, padx=5, sticky="w")
            
            # Email
            ttk.Label(form_frame,
                     text="Email:",
                     font=('Helvetica', 12)).grid(row=1, column=0, pady=10, padx=5, sticky="e")
            
            email_var = tk.StringVar()
            email_entry = ttk.Entry(form_frame,
                                  textvariable=email_var,
                                  font=('Helvetica', 12),
                                  width=30)
            email_entry.grid(row=1, column=1, pady=10, padx=5, sticky="w")
            
            # Password
            ttk.Label(form_frame,
                     text="Password:",
                     font=('Helvetica', 12)).grid(row=2, column=0, pady=10, padx=5, sticky="e")
            
            password_var = tk.StringVar()
            password_entry = ttk.Entry(form_frame,
                                     textvariable=password_var,
                                     font=('Helvetica', 12),
                                     width=30,
                                     show="*")
            password_entry.grid(row=2, column=1, pady=10, padx=5, sticky="w")
            
            # Role
            ttk.Label(form_frame,
                     text="Role:",
                     font=('Helvetica', 12)).grid(row=3, column=0, pady=10, padx=5, sticky="e")
            
            role_var = tk.StringVar(value="student")
            role_combo = ttk.Combobox(form_frame,
                                    textvariable=role_var,
                                    values=["admin", "student"],
                                    font=('Helvetica', 12),
                                    width=30,
                                    state="readonly")
            role_combo.grid(row=3, column=1, pady=10, padx=5, sticky="w")
            
            # Roll Number (for students)
            roll_number_label = ttk.Label(form_frame,
                                        text="Roll Number:",
                                        font=('Helvetica', 12))
            roll_number_label.grid(row=4, column=0, pady=10, padx=5, sticky="e")
            
            roll_number_var = tk.StringVar()
            roll_number_entry = ttk.Entry(form_frame,
                                        textvariable=roll_number_var,
                                        font=('Helvetica', 12),
                                        width=30)
            roll_number_entry.grid(row=4, column=1, pady=10, padx=5, sticky="w")
            
            def toggle_roll_number(*args):
                if role_var.get() == "student":
                    roll_number_label.grid()
                    roll_number_entry.grid()
                else:
                    roll_number_label.grid_remove()
                    roll_number_entry.grid_remove()
            
            role_var.trace('w', toggle_roll_number)
            toggle_roll_number()  # Initial state
            
            def add_user():
                username = username_var.get().strip()
                email = email_var.get().strip()
                password = password_var.get()
                role = role_var.get()
                roll_number = roll_number_var.get().strip() if role == "student" else None
                
                if not username or not email or not password:
                    messagebox.showwarning("Warning", "Please fill in all required fields")
                    return
                
                if role == "student" and not roll_number:
                    messagebox.showwarning("Warning", "Please enter roll number for student")
                    return
                
                try:
                    if self.db.add_user(username, email, password, role, roll_number):
                        messagebox.showinfo("Success", "User added successfully")
                        self.show_users()  # Refresh the users list
                    else:
                        messagebox.showerror("Error", "Failed to add user")
                except Exception as e:
                    print(f"Error adding user: {str(e)}")
                    messagebox.showerror("Error", f"Failed to add user: {str(e)}")
            
            # Buttons
            button_frame = ttk.Frame(form_frame)
            button_frame.grid(row=5, column=0, columnspan=2, pady=20)
            
            ttk.Button(button_frame,
                      text="Add User",
                      command=add_user,
                      style='Accent.TButton').pack(side="left", padx=5)
            
            ttk.Button(button_frame,
                      text="Back to Users",
                      command=self.show_users,
                      style='Accent.TButton').pack(side="left", padx=5)
            
            print("Add user form displayed successfully")
        except Exception as e:
            print(f"Error showing add user form: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to show add user form: {str(e)}")

    def show_add_book(self):
        self.clear_window()
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="40")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title with modern styling
        ttk.Label(main_frame,
                 text="Add New Book",
                 font=("Helvetica", 32, "bold"),
                 foreground=self.accent_color).grid(row=0, column=0, columnspan=2, pady=(0, 40))
        
        # Form with card-like design
        form_frame = ttk.LabelFrame(main_frame,
                                  text="Book Details",
                                  padding="30",
                                  style="Card.TLabelframe")
        form_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Form fields with modern styling
        fields = [
            ("Title:", "book_title_var"),
            ("Author:", "book_author_var"),
            ("Category:", "book_category_var"),
            ("ISBN:", "book_isbn_var"),
            ("Publication Year:", "book_year_var"),
            ("Description:", "book_description_var")
        ]
        
        for i, field in enumerate(fields, 1):
            ttk.Label(form_frame,
                     text=field[0],
                     font=("Helvetica", 12)).grid(row=i, column=0, pady=10, padx=5, sticky="e")
            
            if field[0] == "Category:":  # Category dropdown
                categories = ["Fiction", "Non-Fiction", "Science", "History", "Technology"]
                ttk.Combobox(form_frame,
                           textvariable=getattr(self, field[1]),
                           values=categories,
                           state="readonly",
                           font=("Helvetica", 12),
                           width=28).grid(row=i, column=1, pady=10, padx=5)
            elif field[0] == "Publication Year:":  # Year dropdown
                years = [str(year) for year in range(2024, 1900, -1)]
                ttk.Combobox(form_frame,
                           textvariable=getattr(self, field[1]),
                           values=years,
                           state="readonly",
                           font=("Helvetica", 12),
                           width=28).grid(row=i, column=1, pady=10, padx=5)
            else:  # Regular field
                ttk.Entry(form_frame,
                         textvariable=getattr(self, field[1]),
                         font=("Helvetica", 12),
                         width=30).grid(row=i, column=1, pady=10, padx=5)
        
        # Buttons with modern styling
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        
        add_button = ttk.Button(button_frame,
                              text="Add Book",
                              command=self.add_book,
                              style="TButton",
                              width=20)
        add_button.pack(side="left", padx=5)
        
        back_button = ttk.Button(button_frame,
                               text="Back",
                               command=self.show_admin_dashboard,
                               style="TButton",
                               width=20)
        back_button.pack(side="left", padx=5)
    
    def show_issue_book(self):
        """Show the issue book form"""
        try:
            print("Showing issue book form...")
            self.clear_window()
            
            # Create main container
            main_container = ttk.Frame(self.root)
            main_container.pack(fill="both", expand=True)
            
            # Create sidebar
            sidebar = ttk.Frame(main_container, style="Sidebar.TFrame")
            sidebar.pack(side="left", fill="y", padx=0, pady=0)
            
            # Configure sidebar style
            self.style.configure("Sidebar.TFrame", background="#2c3e50")
            self.style.configure("Sidebar.TButton",
                               background="#2c3e50",
                               foreground="white",
                               padding=10,
                               font=('Helvetica', 12))
            self.style.map("Sidebar.TButton",
                          background=[('active', '#34495e')],
                          foreground=[('active', 'white')])
            
            # Add logo/title to sidebar
            ttk.Label(sidebar,
                     text="Library Admin",
                     font=('Helvetica', 16, 'bold'),
                     foreground="white",
                     background="#2c3e50",
                     padding=20).pack(fill="x")
            
            # Sidebar buttons
            menu_items = [
                ("Dashboard", self.show_admin_dashboard),
                ("Add Book", self.show_add_book),
                ("View Books", self.show_view_books),
                ("Issue Book", self.show_issue_book),
                ("Return Book", self.show_return_book),
                ("Add User", self.show_add_user),
                ("View Users", self.show_users),
                ("Logout", self.logout)
            ]
            
            for text, command in menu_items:
                btn = ttk.Button(sidebar,
                               text=text,
                               command=command,
                               style="Sidebar.TButton",
                               width=20)
                btn.pack(fill="x", padx=5, pady=2)
            
            # Main content area
            content = ttk.Frame(main_container, padding="20")
            content.pack(side="right", fill="both", expand=True)
            
            # Header
            header = ttk.Frame(content)
            header.pack(fill="x", pady=(0, 20))
            
            ttk.Label(header,
                     text="Issue Book",
                     font=('Helvetica', 24, 'bold'),
                     foreground=self.accent_color).pack(side="left")
            
            # Form frame
            form_frame = ttk.LabelFrame(content, text="Issue Book Details", padding="20")
            form_frame.pack(fill="x", pady=(0, 20))
            
            # Student selection
            ttk.Label(form_frame,
                     text="Student Roll Number:",
                     font=('Helvetica', 12)).grid(row=0, column=0, pady=10, padx=5, sticky="e")
            
            roll_number_var = tk.StringVar()
            roll_number_entry = ttk.Entry(form_frame,
                                        textvariable=roll_number_var,
                                        font=('Helvetica', 12),
                                        width=30)
            roll_number_entry.grid(row=0, column=1, pady=10, padx=5, sticky="w")
            
            # Book selection
            ttk.Label(form_frame,
                     text="Book:",
                     font=('Helvetica', 12)).grid(row=1, column=0, pady=10, padx=5, sticky="e")
            
            book_var = tk.StringVar()
            book_combo = ttk.Combobox(form_frame,
                                    textvariable=book_var,
                                    font=('Helvetica', 12),
                                    width=30,
                                    state="readonly")
            book_combo.grid(row=1, column=1, pady=10, padx=5, sticky="w")
            
            # Load available books
            try:
                books = self.db.get_available_books()
                book_combo['values'] = [f"{book['title']} by {book['author']}" for book in books]
            except Exception as e:
                print(f"Error loading books: {str(e)}")
                messagebox.showerror("Error", f"Failed to load books: {str(e)}")
            
            def issue_book():
                roll_number = roll_number_var.get().strip()
                book_title = book_var.get()
                
                if not roll_number or not book_title:
                    messagebox.showwarning("Warning", "Please fill in all fields")
                    return
                
                try:
                    # Get student ID from roll number
                    cursor = self.db.conn.cursor()
                    cursor.execute('SELECT id FROM users WHERE roll_number = ? AND role = "student"',
                                 (roll_number,))
                    student = cursor.fetchone()
                    
                    if not student:
                        messagebox.showerror("Error", "Student not found")
                        return
                    
                    # Get book ID from title
                    book_title = book_title.split(" by ")[0]
                    cursor.execute('SELECT id FROM books WHERE title = ? AND available = TRUE',
                                 (book_title,))
                    book = cursor.fetchone()
                    
                    if not book:
                        messagebox.showerror("Error", "Book not available")
                        return
                    
                    # Issue the book
                    if self.db.issue_book(book['id'], student['id']):
                        messagebox.showinfo("Success", "Book issued successfully")
                        self.show_issue_book()  # Refresh the form
                    else:
                        messagebox.showerror("Error", "Failed to issue book")
                except Exception as e:
                    print(f"Error issuing book: {str(e)}")
                    messagebox.showerror("Error", f"Failed to issue book: {str(e)}")
            
            # Buttons
            button_frame = ttk.Frame(form_frame)
            button_frame.grid(row=2, column=0, columnspan=2, pady=20)
            
            ttk.Button(button_frame,
                      text="Issue Book",
                      command=issue_book,
                      style='Accent.TButton').pack(side="left", padx=5)
            
            ttk.Button(button_frame,
                      text="Back to Dashboard",
                      command=self.show_admin_dashboard,
                      style='Accent.TButton').pack(side="left", padx=5)
            
            print("Issue book form displayed successfully")
        except Exception as e:
            print(f"Error showing issue book form: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to show issue book form: {str(e)}")

    def show_view_books(self):
        """Show the view books screen"""
        try:
            print("Showing view books screen...")
            self.clear_window()
            
            # Create main container
            main_container = ttk.Frame(self.root)
            main_container.pack(fill="both", expand=True)
            
            # Create sidebar
            sidebar = ttk.Frame(main_container, style="Sidebar.TFrame")
            sidebar.pack(side="left", fill="y", padx=0, pady=0)
            
            # Configure sidebar style
            self.style.configure("Sidebar.TFrame", background="#2c3e50")
            self.style.configure("Sidebar.TButton",
                               background="#2c3e50",
                               foreground="white",
                               padding=10,
                               font=('Helvetica', 12))
            self.style.map("Sidebar.TButton",
                          background=[('active', '#34495e')],
                          foreground=[('active', 'white')])
            
            # Add logo/title to sidebar
            ttk.Label(sidebar,
                     text="Library Admin",
                     font=('Helvetica', 16, 'bold'),
                     foreground="white",
                     background="#2c3e50",
                     padding=20).pack(fill="x")
            
            # Sidebar buttons
            menu_items = [
                ("Dashboard", self.show_admin_dashboard),
                ("Add Book", self.show_add_book),
                ("View Books", self.show_view_books),
                ("Issue Book", self.show_issue_book),
                ("Return Book", self.show_return_book),
                ("Add User", self.show_add_user),
                ("View Users", self.show_users),
                ("Logout", self.logout)
            ]
            
            for text, command in menu_items:
                btn = ttk.Button(sidebar,
                               text=text,
                               command=command,
                               style="Sidebar.TButton",
                               width=20)
                btn.pack(fill="x", padx=5, pady=2)
            
            # Main content area
            content = ttk.Frame(main_container, padding="20")
            content.pack(side="right", fill="both", expand=True)
            
            # Header
            header = ttk.Frame(content)
            header.pack(fill="x", pady=(0, 20))
            
            ttk.Label(header,
                     text="Book Management",
                     font=('Helvetica', 24, 'bold'),
                     foreground=self.accent_color).pack(side="left")
            
            # Search frame
            search_frame = ttk.Frame(content)
            search_frame.pack(fill="x", pady=(0, 20))
            
            ttk.Label(search_frame,
                     text="Search:",
                     font=('Helvetica', 12)).pack(side="left", padx=(0, 10))
            
            search_var = tk.StringVar()
            search_entry = ttk.Entry(search_frame,
                                   textvariable=search_var,
                                   font=('Helvetica', 12),
                                   width=30)
            search_entry.pack(side="left", padx=(0, 10))
            
            def search_books():
                search_term = search_var.get().strip().lower()
                for item in tree.get_children():
                    tree.delete(item)
                
                try:
                    books = self.db.get_all_books()
                    for book in books:
                        if (search_term in book['title'].lower() or
                            search_term in book['author'].lower() or
                            search_term in book['category'].lower() or
                            search_term in str(book['isbn'])):
                            tree.insert("", "end", values=(
                                book['id'],
                                book['title'],
                                book['author'],
                                book['category'],
                                book['isbn'],
                                book['publication_year'],
                                "Yes" if book['available'] else "No"
                            ))
                except Exception as e:
                    print(f"Error searching books: {str(e)}")
                    messagebox.showerror("Error", f"Failed to search books: {str(e)}")
            
            ttk.Button(search_frame,
                      text="Search",
                      command=search_books,
                      style='Accent.TButton').pack(side="left")
            
            # Treeview for books
            tree_frame = ttk.Frame(content)
            tree_frame.pack(fill="both", expand=True)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(tree_frame)
            scrollbar.pack(side="right", fill="y")
            
            # Treeview
            tree = ttk.Treeview(tree_frame,
                               columns=("ID", "Title", "Author", "Category", "ISBN", "Year", "Available"),
                               show="headings",
                               yscrollcommand=scrollbar.set)
            
            # Configure columns
            tree.heading("ID", text="ID")
            tree.heading("Title", text="Title")
            tree.heading("Author", text="Author")
            tree.heading("Category", text="Category")
            tree.heading("ISBN", text="ISBN")
            tree.heading("Year", text="Year")
            tree.heading("Available", text="Available")
            
            tree.column("ID", width=50)
            tree.column("Title", width=200)
            tree.column("Author", width=150)
            tree.column("Category", width=100)
            tree.column("ISBN", width=100)
            tree.column("Year", width=70)
            tree.column("Available", width=80)
            
            tree.pack(fill="both", expand=True)
            scrollbar.config(command=tree.yview)
            
            # Load books
            try:
                books = self.db.get_all_books()
                for book in books:
                    tree.insert("", "end", values=(
                        book['id'],
                        book['title'],
                        book['author'],
                        book['category'],
                        book['isbn'],
                        book['publication_year'],
                        "Yes" if book['available'] else "No"
                    ))
            except Exception as e:
                print(f"Error loading books: {str(e)}")
                messagebox.showerror("Error", f"Failed to load books: {str(e)}")
            
            # Delete button
            def delete_book():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Warning", "Please select a book to delete")
                    return
                
                if messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
                    try:
                        book_id = tree.item(selected[0])['values'][0]
                        if self.db.delete_book(book_id):
                            tree.delete(selected[0])
                            messagebox.showinfo("Success", "Book deleted successfully")
                        else:
                            messagebox.showerror("Error", "Failed to delete book")
                    except Exception as e:
                        print(f"Error deleting book: {str(e)}")
                        messagebox.showerror("Error", f"Failed to delete book: {str(e)}")
            
            button_frame = ttk.Frame(content)
            button_frame.pack(fill="x", pady=20)
            
            ttk.Button(button_frame,
                      text="Delete Selected",
                      command=delete_book,
                      style='Accent.TButton').pack(side="left", padx=5)
            
            ttk.Button(button_frame,
                      text="Back to Dashboard",
                      command=self.show_admin_dashboard,
                      style='Accent.TButton').pack(side="left", padx=5)
            
            print("View books screen displayed successfully")
        except Exception as e:
            print(f"Error showing view books screen: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to show view books screen: {str(e)}")

    def show_return_book(self):
        """Show the return book form"""
        try:
            print("Showing return book form...")
            self.clear_window()
            
            # Main container with padding
            main_frame = ttk.Frame(self.root, padding="20")
            main_frame.pack(fill="both", expand=True)
            
            # Header with back button
            header_frame = ttk.Frame(main_frame)
            header_frame.pack(fill="x", pady=(0, 20))
            
            ttk.Label(
                header_frame,
                text="Return Book",
                font=('Helvetica', 24, 'bold'),
                foreground=self.accent_color
            ).pack(side="left")
            
            ttk.Button(
                header_frame,
                text="Back to Dashboard",
                command=self.show_admin_dashboard,
                style='Accent.TButton'
            ).pack(side="right")
            
            # Books list frame
            list_frame = ttk.LabelFrame(main_frame, text="Issued Books", padding="20")
            list_frame.pack(fill="both", expand=True)
            
            # Create Treeview
            columns = ('Issue ID', 'Book ID', 'Title', 'Author', 'Issued To', 'Issue Date', 'Due Date')
            tree = ttk.Treeview(list_frame, columns=columns, show='headings')
            
            # Configure columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            # Pack tree and scrollbar
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Load issued books
            try:
                cursor = self.db.conn.cursor()
                cursor.execute('''
                    SELECT 
                        ib.id as issue_id,
                        b.id as book_id,
                        b.title,
                        b.author,
                        u.username as issued_to,
                        ib.issue_date,
                        ib.due_date
                    FROM books b
                    JOIN issued_books ib ON b.id = ib.book_id
                    JOIN users u ON ib.user_id = u.id
                    WHERE ib.return_date IS NULL
                    ORDER BY ib.issue_date DESC
                ''')
                
                for row in cursor.fetchall():
                    tree.insert('', 'end', values=(
                        row['issue_id'],
                        row['book_id'],
                        row['title'],
                        row['author'],
                        row['issued_to'],
                        row['issue_date'],
                        row['due_date']
                    ))
            except Exception as e:
                print(f"Error loading issued books: {str(e)}")
                messagebox.showerror("Error", f"Failed to load issued books: {str(e)}")
            
            # Return button
            ttk.Button(
                main_frame,
                text="Return Selected Book",
                command=lambda: self.return_selected_book(tree),
                style='Accent.TButton'
            ).pack(pady=20)
            
            print("Return book screen displayed successfully")
        except Exception as e:
            print(f"Error showing return book form: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to show return book form: {str(e)}")

    def return_selected_book(self, tree):
        """Handle returning a selected book"""
        try:
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a book to return")
                return
            
            # Get issue ID from the selected item
            issue_id = tree.item(selected_item[0])['values'][0]
            
            # Return the book
            if self.db.return_book(issue_id):
                messagebox.showinfo("Success", "Book returned successfully")
                # Remove the returned book from the tree
                tree.delete(selected_item[0])
            else:
                messagebox.showerror("Error", "Failed to return book")
        except Exception as e:
            print(f"Error returning book: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to return book: {str(e)}")

    def show_users(self):
        """Show all users in the system"""
        try:
            print("Showing users list...")
            self.clear_window()
            
            # Create main container
            main_container = ttk.Frame(self.root)
            main_container.pack(fill="both", expand=True)
            
            # Create sidebar
            sidebar = ttk.Frame(main_container, style="Sidebar.TFrame")
            sidebar.pack(side="left", fill="y", padx=0, pady=0)
            
            # Configure sidebar style
            self.style.configure("Sidebar.TFrame", background="#2c3e50")
            self.style.configure("Sidebar.TButton",
                               background="#2c3e50",
                               foreground="white",
                               padding=10,
                               font=('Helvetica', 12))
            self.style.map("Sidebar.TButton",
                          background=[('active', '#34495e')],
                          foreground=[('active', 'white')])
            
            # Add logo/title to sidebar
            ttk.Label(sidebar,
                     text="Library Admin",
                     font=('Helvetica', 16, 'bold'),
                     foreground="white",
                     background="#2c3e50",
                     padding=20).pack(fill="x")
            
            # Sidebar buttons
            menu_items = [
                ("Dashboard", self.show_admin_dashboard),
                ("Add Book", self.show_add_book),
                ("View Books", self.show_view_books),
                ("Issue Book", self.show_issue_book),
                ("Return Book", self.show_return_book),
                ("Add User", self.show_add_user),
                ("View Users", self.show_users),
                ("Logout", self.logout)
            ]
            
            for text, command in menu_items:
                btn = ttk.Button(sidebar,
                               text=text,
                               command=command,
                               style="Sidebar.TButton",
                               width=20)
                btn.pack(fill="x", padx=5, pady=2)
            
            # Main content area
            content = ttk.Frame(main_container, padding="20")
            content.pack(side="right", fill="both", expand=True)
            
            # Header
            header = ttk.Frame(content)
            header.pack(fill="x", pady=(0, 20))
            
            ttk.Label(header,
                     text="User Management",
                     font=('Helvetica', 24, 'bold'),
                     foreground=self.accent_color).pack(side="left")
            
            # Search frame
            search_frame = ttk.Frame(content)
            search_frame.pack(fill="x", pady=(0, 20))
            
            ttk.Label(search_frame,
                     text="Search:",
                     font=('Helvetica', 12)).pack(side="left", padx=5)
            
            search_var = tk.StringVar()
            search_entry = ttk.Entry(search_frame,
                                   textvariable=search_var,
                                   font=('Helvetica', 12),
                                   width=40)
            search_entry.pack(side="left", padx=5)
            
            def search_users():
                search_term = search_var.get().strip().lower()
                for item in tree.get_children():
                    tree.delete(item)
                
                try:
                    users = self.db.get_all_users()
                    for user in users:
                        if (search_term in user['username'].lower() or
                            search_term in user['email'].lower() or
                            search_term in user['role'].lower() or
                            (user['roll_number'] and search_term in user['roll_number'].lower())):
                            tree.insert('', 'end', values=(
                                user['id'],
                                user['username'],
                                user['email'],
                                user['role'],
                                user['roll_number'] or 'N/A'
                            ))
                except Exception as e:
                    print(f"Error searching users: {str(e)}")
                    messagebox.showerror("Error", f"Failed to search users: {str(e)}")
            
            ttk.Button(search_frame,
                      text="Search",
                      command=search_users,
                      style='Accent.TButton').pack(side="left", padx=5)
            
            # Users list frame
            list_frame = ttk.LabelFrame(content, text="All Users", padding="20")
            list_frame.pack(fill="both", expand=True)
            
            # Create Treeview
            columns = ('ID', 'Username', 'Email', 'Role', 'Roll Number')
            tree = ttk.Treeview(list_frame, columns=columns, show='headings')
            
            # Configure columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            # Pack tree and scrollbar
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Load users
            try:
                users = self.db.get_all_users()
                for user in users:
                    tree.insert('', 'end', values=(
                        user['id'],
                        user['username'],
                        user['email'],
                        user['role'],
                        user['roll_number'] or 'N/A'
                    ))
            except Exception as e:
                print(f"Error loading users: {str(e)}")
                messagebox.showerror("Error", f"Failed to load users: {str(e)}")
            
            # Action buttons
            button_frame = ttk.Frame(content)
            button_frame.pack(fill="x", pady=20)
            
            def delete_selected_user():
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showwarning("Warning", "Please select a user to delete")
                    return
                
                user_id = tree.item(selected_item[0])['values'][0]
                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?"):
                    try:
                        if self.db.delete_user(user_id):
                            tree.delete(selected_item[0])
                            messagebox.showinfo("Success", "User deleted successfully")
                        else:
                            messagebox.showerror("Error", "Failed to delete user")
                    except Exception as e:
                        print(f"Error deleting user: {str(e)}")
                        messagebox.showerror("Error", f"Failed to delete user: {str(e)}")
            
            ttk.Button(button_frame,
                      text="Add New User",
                      command=self.show_add_user,
                      style='Accent.TButton').pack(side="left", padx=5)
            
            ttk.Button(button_frame,
                      text="Delete Selected",
                      command=delete_selected_user,
                      style='Accent.TButton').pack(side="left", padx=5)
            
            ttk.Button(button_frame,
                      text="Back to Dashboard",
                      command=self.show_admin_dashboard,
                      style='Accent.TButton').pack(side="right", padx=5)
            
            print("Users list displayed successfully")
        except Exception as e:
            print(f"Error showing users list: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to show users list: {str(e)}")

    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_book(self):
        """Add a new book to the database"""
        try:
            title = self.book_title_var.get().strip()
            author = self.book_author_var.get().strip()
            category = self.book_category_var.get()
            isbn = self.book_isbn_var.get().strip()
            year = self.book_year_var.get()
            description = self.book_description_var.get().strip()
            
            if not all([title, author, category, isbn, year]):
                messagebox.showwarning("Warning", "Please fill in all required fields")
                return
            
            try:
                year = int(year)
            except ValueError:
                messagebox.showerror("Error", "Publication year must be a number")
                return
            
            if self.db.add_book(title, author, category, isbn, year, description):
                messagebox.showinfo("Success", "Book added successfully")
                # Clear form
                self.book_title_var.set("")
                self.book_author_var.set("")
                self.book_category_var.set("")
                self.book_isbn_var.set("")
                self.book_year_var.set("")
                self.book_description_var.set("")
                # Show books list
                self.show_view_books()
            else:
                messagebox.showerror("Error", "Failed to add book")
        except Exception as e:
            print(f"Error adding book: {str(e)}")
            messagebox.showerror("Error", f"Failed to add book: {str(e)}")

    def show_available_books(self):
        """Show available books for students"""
        try:
            print("Showing available books...")
            self.clear_window()
            
            # Create main container
            main_container = ttk.Frame(self.root)
            main_container.pack(fill="both", expand=True)
            
            # Create sidebar
            sidebar = ttk.Frame(main_container, style="Sidebar.TFrame")
            sidebar.pack(side="left", fill="y", padx=0, pady=0)
            
            # Configure sidebar style
            self.style.configure("Sidebar.TFrame", background="#2c3e50")
            self.style.configure("Sidebar.TButton",
                               background="#2c3e50",
                               foreground="white",
                               padding=10,
                               font=('Helvetica', 12))
            self.style.map("Sidebar.TButton",
                          background=[('active', '#34495e')],
                          foreground=[('active', 'white')])
            
            # Add logo/title to sidebar
            ttk.Label(sidebar,
                     text="Student Portal",
                     font=('Helvetica', 16, 'bold'),
                     foreground="white",
                     background="#2c3e50",
                     padding=20).pack(fill="x")
            
            # Sidebar buttons
            menu_items = [
                ("Dashboard", self.show_student_dashboard),
                ("View My Books", self.show_my_books),
                ("Available Books", self.show_available_books),
                ("Logout", self.logout)
            ]
            
            for text, command in menu_items:
                btn = ttk.Button(sidebar,
                               text=text,
                               command=command,
                               style="Sidebar.TButton",
                               width=20)
                btn.pack(fill="x", padx=5, pady=2)
            
            # Main content area
            content = ttk.Frame(main_container, padding="20")
            content.pack(side="right", fill="both", expand=True)
            
            # Header
            header = ttk.Frame(content)
            header.pack(fill="x", pady=(0, 20))
            
            ttk.Label(header,
                     text="Available Books",
                     font=('Helvetica', 24, 'bold'),
                     foreground=self.accent_color).pack(side="left")
            
            # Search frame
            search_frame = ttk.Frame(content)
            search_frame.pack(fill="x", pady=(0, 20))
            
            ttk.Label(search_frame,
                     text="Search:",
                     font=('Helvetica', 12)).pack(side="left", padx=5)
            
            search_var = tk.StringVar()
            search_entry = ttk.Entry(search_frame,
                                   textvariable=search_var,
                                   font=('Helvetica', 12),
                                   width=40)
            search_entry.pack(side="left", padx=5)
            
            def search_books():
                search_term = search_var.get().strip()
                for item in tree.get_children():
                    tree.delete(item)
                
                try:
                    books = self.db.search_books(search_term)
                    for book in books:
                        if book['available']:
                            tree.insert('', 'end', values=(
                                book['id'],
                                book['title'],
                                book['author'],
                                book['category'],
                                book['isbn'],
                                book['publication_year']
                            ))
                except Exception as e:
                    print(f"Error searching books: {str(e)}")
                    messagebox.showerror("Error", f"Failed to search books: {str(e)}")
            
            ttk.Button(search_frame,
                      text="Search",
                      command=search_books,
                      style='Accent.TButton').pack(side="left", padx=5)
            
            # Books list frame
            list_frame = ttk.LabelFrame(content, text="Available Books", padding="20")
            list_frame.pack(fill="both", expand=True)
            
            # Create Treeview
            columns = ('ID', 'Title', 'Author', 'Category', 'ISBN', 'Year')
            tree = ttk.Treeview(list_frame, columns=columns, show='headings')
            
            # Configure columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            # Pack tree and scrollbar
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Load available books
            try:
                books = self.db.get_available_books()
                for book in books:
                    tree.insert('', 'end', values=(
                        book['id'],
                        book['title'],
                        book['author'],
                        book['category'],
                        book['isbn'],
                        book['publication_year']
                    ))
            except Exception as e:
                print(f"Error loading books: {str(e)}")
                messagebox.showerror("Error", f"Failed to load books: {str(e)}")
            
            print("Available books screen displayed successfully")
        except Exception as e:
            print(f"Error showing available books: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to show available books: {str(e)}")

if __name__ == "__main__":
    try:
        # Create the root window
        root = tk.Tk()
        
        # Set window title
        root.title("Library Management System")
        
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Set window size to 90% of screen size
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        
        # Calculate position for center of screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set window size and position
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create the application
        app = LibraryGUI(root)
        
        # Start the main event loop
        root.mainloop()
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        traceback.print_exc()