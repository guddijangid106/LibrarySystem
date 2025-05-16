import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import tkinter as tk
from tkinter import messagebox

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class FormValidator:
    """Static validation methods"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"
        
        return True, "Password is valid"
    
    @staticmethod
    def validate_isbn(isbn: str) -> bool:
        """Validate ISBN format (10 or 13 digits)"""
        # Remove hyphens and spaces
        isbn = isbn.replace('-', '').replace(' ', '')
        
        # Check length
        if len(isbn) not in [10, 13]:
            return False
        
        # Check if all characters are digits
        if not isbn.isdigit():
            return False
        
        return True
    
    @staticmethod
    def validate_year(year: int) -> bool:
        """Validate publication year"""
        current_year = datetime.now().year
        return 1900 <= year <= current_year

class UserForm:
    """User registration and login form validation"""
    
    def __init__(self):
        self.errors: Dict[str, str] = {}
    
    def validate_registration(self, username: str, password: str,
                            email: str, role: str) -> bool:
        """Validate user registration data"""
        self.errors.clear()
        
        # Validate username
        if not username or len(username) < 3:
            self.errors['username'] = "Username must be at least 3 characters"
        
        # Validate password
        is_valid, message = FormValidator.validate_password(password)
        if not is_valid:
            self.errors['password'] = message
        
        # Validate email
        if not FormValidator.validate_email(email):
            self.errors['email'] = "Invalid email format"
        
        # Validate role
        if role not in ['admin', 'student']:
            self.errors['role'] = "Role must be either 'admin' or 'student'"
        
        return len(self.errors) == 0
    
    def validate_login(self, username: str, password: str) -> bool:
        """Validate login data"""
        self.errors.clear()
        
        if not username:
            self.errors['username'] = "Username is required"
        
        if not password:
            self.errors['password'] = "Password is required"
        
        return len(self.errors) == 0

class BookForm:
    """Book details form validation"""
    
    def __init__(self):
        self.errors: Dict[str, str] = {}
        self.categories = [
            'Fiction', 'Non-Fiction', 'Science', 'Technology',
            'History', 'Biography', 'Self-Help', 'Reference'
        ]
    
    def validate(self, title: str, author: str, category: str,
                isbn: str, year: str, description: str = "") -> bool:
        """Validate book details"""
        self.errors.clear()
        
        # Validate title
        if not title or len(title) < 2:
            self.errors['title'] = "Title must be at least 2 characters"
        
        # Validate author
        if not author or len(author) < 2:
            self.errors['author'] = "Author must be at least 2 characters"
        
        # Validate category
        if not category or category not in self.categories:
            self.errors['category'] = f"Category must be one of: {', '.join(self.categories)}"
        
        # Validate ISBN
        if not isbn or not FormValidator.validate_isbn(isbn):
            self.errors['isbn'] = "Invalid ISBN format"
        
        # Validate year
        try:
            year_int = int(year)
            if not FormValidator.validate_year(year_int):
                self.errors['year'] = "Invalid publication year"
        except ValueError:
            self.errors['year'] = "Year must be a number"
        
        # Validate description (optional)
        if description and len(description) > 1000:
            self.errors['description'] = "Description must be less than 1000 characters"
        
        return len(self.errors) == 0

class IssueForm:
    """Book issue form validation"""
    
    def __init__(self):
        self.errors: Dict[str, str] = {}
    
    def validate(self, book_id: int, user_id: int, days: int = 14) -> bool:
        """Validate book issue data"""
        self.errors.clear()
        
        # Validate book ID
        try:
            book_id = int(book_id)
            if book_id <= 0:
                self.errors['book_id'] = "Invalid book ID"
        except ValueError:
            self.errors['book_id'] = "Book ID must be a number"
        
        # Validate user ID
        try:
            user_id = int(user_id)
            if user_id <= 0:
                self.errors['user_id'] = "Invalid user ID"
        except ValueError:
            self.errors['user_id'] = "User ID must be a number"
        
        # Validate days
        try:
            days = int(days)
            if not 1 <= days <= 30:
                self.errors['days'] = "Days must be between 1 and 30"
        except ValueError:
            self.errors['days'] = "Days must be a number"
        
        return len(self.errors) == 0

def show_validation_errors(errors: Dict[str, str]):
    """Display validation errors in a message box"""
    if not errors:
        return
    
    message = "Please correct the following errors:\n\n"
    for field, error in errors.items():
        message += f"{field}: {error}\n"
    
    messagebox.showerror("Validation Error", message)

def format_date(date_str: str) -> str:
    """Format date string to YYYY-MM-DD"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.strftime("%Y-%m-%d")
    except ValueError:
        return date_str

def format_datetime(dt_str: str) -> str:
    """Format datetime string to YYYY-MM-DD HH:MM:SS"""
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return dt_str

def create_form_field(parent: tk.Frame, label: str, widget_class: type,
                     **widget_kwargs) -> Tuple[tk.Label, Any]:
    """Create a form field with label and widget"""
    # Create label
    label_widget = tk.Label(
        parent,
        text=label,
        font=("Helvetica", 10)
    )
    label_widget.pack(anchor='w', pady=(10, 0))
    
    # Create widget
    widget = widget_class(parent, **widget_kwargs)
    widget.pack(fill='x', pady=(5, 0))
    
    return label_widget, widget

def create_button(parent: tk.Frame, text: str, command: callable,
                 **button_kwargs) -> tk.Button:
    """Create a styled button"""
    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Helvetica", 10),
        bg="#2196F3",
        fg="white",
        padx=20,
        pady=10,
        **button_kwargs
    )
    button.pack(pady=10)
    return button

def create_error_label(parent: tk.Frame) -> tk.Label:
    """Create an error label for form validation"""
    error_label = tk.Label(
        parent,
        text="",
        fg="red",
        font=("Helvetica", 9)
    )
    error_label.pack(pady=5)
    return error_label

def update_error_label(label: tk.Label, error: str):
    """Update error label with validation error"""
    label.config(text=error)
    label.pack(pady=5)

def clear_error_label(label: tk.Label):
    """Clear error label"""
    label.config(text="")
    label.pack_forget() 