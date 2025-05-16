import sqlite3
import os
import hashlib
import time
from datetime import datetime, timedelta
from typing import Optional, Tuple, List, Dict, Any

class Database:
    def __init__(self, db_path: str = "library.db"):
        """Initialize database connection with retry mechanism"""
        self.db_path = db_path
        self.conn = None
        self.max_retries = 3
        self.retry_delay = 1  # seconds
        
        # Ensure database directory exists
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        
        # Try to connect with retries
        for attempt in range(self.max_retries):
            try:
                self.conn = sqlite3.connect(
                    db_path,
                    timeout=20,  # 20 second timeout
                    check_same_thread=False  # Allow multi-threading
                )
                self.conn.row_factory = sqlite3.Row  # Enable row factory
                self.create_tables()
                self.create_default_admin()  # Create default admin if needed
                print(f"Database connected successfully on attempt {attempt + 1}")
                break
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < self.max_retries - 1:
                    print(f"Database locked, retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    raise Exception(f"Failed to connect to database: {str(e)}")
    
    def __del__(self):
        """Cleanup database connection"""
        if self.conn:
            try:
                self.conn.close()
            except Exception as e:
                print(f"Error closing database connection: {str(e)}")
    
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            cursor = self.conn.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    roll_number TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create books table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    category TEXT NOT NULL,
                    isbn TEXT UNIQUE NOT NULL,
                    publication_year INTEGER NOT NULL,
                    description TEXT,
                    available BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create issued_books table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS issued_books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    due_date TIMESTAMP NOT NULL,
                    return_date TIMESTAMP,
                    FOREIGN KEY (book_id) REFERENCES books (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            self.conn.commit()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Error creating tables: {str(e)}")
            raise
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def add_user(self, username: str, email: str, password: str, role: str, roll_number: str = None) -> bool:
        """Add a new user to the database"""
        try:
            cursor = self.conn.cursor()
            hashed_password = self.hash_password(password)
            
            # Validate roll number for students
            if role == "student" and not roll_number:
                raise ValueError("Roll number is required for student users")
            
            cursor.execute('''
                INSERT INTO users (username, email, password, role, roll_number)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, hashed_password, role, roll_number))
            
            self.conn.commit()
            return True
            
        except sqlite3.IntegrityError as e:
            self.conn.rollback()
            if "UNIQUE constraint failed: users.username" in str(e):
                raise ValueError("Username already exists")
            elif "UNIQUE constraint failed: users.email" in str(e):
                raise ValueError("Email already exists")
            elif "UNIQUE constraint failed: users.roll_number" in str(e):
                raise ValueError("Roll number already exists")
            else:
                raise Exception(f"Error adding user: {str(e)}")
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    def verify_user(self, username: str, password: str, role: str) -> Optional[Tuple[Dict[str, Any], str]]:
        """Verify user credentials and return user data and role"""
        try:
            cursor = self.conn.cursor()
            hashed_password = self.hash_password(password)
            
            cursor.execute('''
                SELECT * FROM users
                WHERE username = ? AND password = ? AND role = ?
            ''', (username, hashed_password, role))
            
            result = cursor.fetchone()
            if result:
                return dict(result), result['role']
            return None
            
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def add_book(self, title: str, author: str, category: str, isbn: str,
                 publication_year: int, description: str = "") -> bool:
        """Add a new book to the database"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                INSERT INTO books (title, author, category, isbn, publication_year, description)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, author, category, isbn, publication_year, description))
            
            self.conn.commit()
            return True
            
        except sqlite3.IntegrityError as e:
            self.conn.rollback()
            if "UNIQUE constraint failed: books.isbn" in str(e):
                raise Exception("ISBN already exists")
            else:
                raise Exception(f"Error adding book: {str(e)}")
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    def issue_book(self, book_id: int, user_id: int) -> bool:
        """Issue a book to a user"""
        try:
            cursor = self.conn.cursor()
            
            # Check if book is available
            cursor.execute('SELECT available FROM books WHERE id = ?', (book_id,))
            book = cursor.fetchone()
            if not book or not book['available']:
                return False
            
            # Check if user already has this book
            cursor.execute('''
                SELECT * FROM issued_books 
                WHERE book_id = ? AND user_id = ? AND return_date IS NULL
            ''', (book_id, user_id))
            if cursor.fetchone():
                return False
            
            # Issue the book
            cursor.execute('''
                INSERT INTO issued_books (book_id, user_id, issue_date, due_date)
                VALUES (?, ?, datetime('now'), datetime('now', '+30 days'))
            ''', (book_id, user_id))
            
            # Update book availability
            cursor.execute('''
                UPDATE books 
                SET available = FALSE 
                WHERE id = ?
            ''', (book_id,))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error issuing book: {str(e)}")
            self.conn.rollback()
            return False
    
    def return_book(self, issue_id: int) -> bool:
        """Return a book"""
        try:
            cursor = self.conn.cursor()
            
            # Get book ID
            cursor.execute('SELECT book_id FROM issued_books WHERE id = ?', (issue_id,))
            result = cursor.fetchone()
            if not result:
                return False
            
            book_id = result['book_id']
            
            # Update issued_books
            cursor.execute('''
                UPDATE issued_books 
                SET return_date = datetime('now')
                WHERE id = ?
            ''', (issue_id,))
            
            # Update book availability
            cursor.execute('''
                UPDATE books 
                SET available = TRUE 
                WHERE id = ?
            ''', (book_id,))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error returning book: {str(e)}")
            self.conn.rollback()
            return False
    
    def get_available_books(self) -> List[Dict[str, Any]]:
        """Get all available books"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM books 
                WHERE available = TRUE
                ORDER BY title
            ''')
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting available books: {str(e)}")
            return []
    
    def get_overdue_books(self) -> List[Dict[str, Any]]:
        """Get all overdue books"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT 
                    b.id, b.title, b.author,
                    u.username, u.email,
                    ib.issue_date, ib.due_date,
                    julianday('now') - julianday(ib.due_date) as days_overdue
                FROM issued_books ib
                JOIN books b ON ib.book_id = b.id
                JOIN users u ON ib.user_id = u.id
                WHERE ib.return_date IS NULL
                AND ib.due_date < datetime('now')
                ORDER BY ib.due_date
            ''')
            
            return [dict(row) for row in cursor.fetchall()]
            
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def get_user_books(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all books issued to a user"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT 
                    ib.id as issue_id,
                    b.*,
                    ib.issue_date,
                    ib.return_date
                FROM issued_books ib
                JOIN books b ON ib.book_id = b.id
                WHERE ib.user_id = ?
                ORDER BY ib.issue_date DESC
            ''', (user_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting user books: {str(e)}")
            return []
    
    def search_books(self, query: str) -> List[Dict[str, Any]]:
        """Search books by title, author, or ISBN"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT * FROM books
                WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
                ORDER BY title
            ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
            
            return [dict(row) for row in cursor.fetchall()]
            
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def get_book_details(self, book_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed information about a book"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT 
                    b.*,
                    u.username as current_holder,
                    ib.issue_date,
                    ib.due_date
                FROM books b
                LEFT JOIN issued_books ib ON b.id = ib.book_id AND ib.return_date IS NULL
                LEFT JOIN users u ON ib.user_id = u.id
                WHERE b.id = ?
            ''', (book_id,))
            
            result = cursor.fetchone()
            return dict(result) if result else None
            
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def get_user_details(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed information about a user"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT 
                    u.*,
                    COUNT(DISTINCT ib.id) as total_books_issued,
                    COUNT(DISTINCT CASE WHEN ib.return_date IS NULL THEN ib.id END) as current_books,
                    COUNT(DISTINCT CASE WHEN ib.return_date IS NULL AND ib.due_date < datetime('now') THEN ib.id END) as overdue_books
                FROM users u
                LEFT JOIN issued_books ib ON u.id = ib.user_id
                WHERE u.id = ?
                GROUP BY u.id
            ''', (user_id,))
            
            result = cursor.fetchone()
            return dict(result) if result else None
            
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def filter_books(self, category: Optional[str] = None,
                    available: Optional[bool] = None,
                    year: Optional[int] = None) -> List[Dict[str, Any]]:
        """Filter books by category, availability, and year"""
        try:
            cursor = self.conn.cursor()
            
            query = "SELECT * FROM books WHERE 1=1"
            params = []
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            if available is not None:
                query += " AND available = ?"
                params.append(available)
            
            if year:
                query += " AND publication_year = ?"
                params.append(year)
            
            query += " ORDER BY title"
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
            
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def get_recent_issues(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent book issues"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT 
                    datetime(ib.issue_date) as issue_date,
                    b.title,
                    u.username
                FROM issued_books ib
                JOIN books b ON ib.book_id = b.id
                JOIN users u ON ib.user_id = u.id
                ORDER BY ib.issue_date DESC
                LIMIT ?
            ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
            
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def get_recent_returns(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent book returns"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT 
                    datetime(ib.return_date) as return_date,
                    b.title,
                    u.username
                FROM issued_books ib
                JOIN books b ON ib.book_id = b.id
                JOIN users u ON ib.user_id = u.id
                WHERE ib.return_date IS NOT NULL
                ORDER BY ib.return_date DESC
                LIMIT ?
            ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
            
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def get_all_books(self) -> List[Dict[str, Any]]:
        """Get all books from the database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id, title, author, category, isbn, publication_year, available
                FROM books
                ORDER BY title
            ''')
            books = cursor.fetchall()
            return [dict(book) for book in books]
        except Exception as e:
            print(f"Error getting all books: {str(e)}")
            return []
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users from the database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id, username, email, role, roll_number
                FROM users
                ORDER BY username
            ''')
            users = []
            for row in cursor.fetchall():
                users.append({
                    'id': row['id'],
                    'username': row['username'],
                    'email': row['email'],
                    'role': row['role'],
                    'roll_number': row['roll_number']
                })
            return users
        except Exception as e:
            print(f"Error getting users: {str(e)}")
            raise
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user from the database"""
        try:
            cursor = self.conn.cursor()
            
            # Check if user has any issued books
            cursor.execute('''
                SELECT COUNT(*) as count
                FROM issued_books
                WHERE user_id = ? AND return_date IS NULL
            ''', (user_id,))
            
            if cursor.fetchone()['count'] > 0:
                raise Exception("Cannot delete user: They have issued books that need to be returned first")
            
            # Begin transaction
            cursor.execute('BEGIN TRANSACTION')
            
            try:
                # Delete user's issued books history
                cursor.execute('DELETE FROM issued_books WHERE user_id = ?', (user_id,))
                
                # Delete user
                cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
                
                # Commit transaction
                self.conn.commit()
                return True
                
            except sqlite3.Error as e:
                # Rollback transaction on error
                self.conn.rollback()
                raise Exception(f"Failed to delete user: {str(e)}")
            
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def delete_book(self, book_id: int) -> bool:
        """Delete a book from the database"""
        try:
            cursor = self.conn.cursor()
            
            # Check if book is currently issued
            cursor.execute('''
                SELECT COUNT(*) as count
                FROM issued_books
                WHERE book_id = ? AND return_date IS NULL
            ''', (book_id,))
            
            if cursor.fetchone()['count'] > 0:
                raise Exception("Cannot delete book: It is currently issued to a user")
            
            # Begin transaction
            cursor.execute('BEGIN TRANSACTION')
            
            try:
                # Delete book's issue history
                cursor.execute('DELETE FROM issued_books WHERE book_id = ?', (book_id,))
                
                # Delete book
                cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
                
                # Commit transaction
                self.conn.commit()
                return True
                
            except sqlite3.Error as e:
                # Rollback transaction on error
                self.conn.rollback()
                raise Exception(f"Failed to delete book: {str(e)}")
            
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def delete_transaction(self, transaction_id: int) -> bool:
        """Delete a transaction (issued book record) from the database"""
        try:
            cursor = self.conn.cursor()
            
            # Check if book is still issued
            cursor.execute('''
                SELECT book_id, return_date
                FROM issued_books
                WHERE id = ?
            ''', (transaction_id,))
            
            transaction = cursor.fetchone()
            if not transaction:
                raise Exception("Transaction not found")
            
            if not transaction['return_date']:
                raise Exception("Cannot delete transaction: Book is still issued")
            
            # Delete transaction
            cursor.execute('DELETE FROM issued_books WHERE id = ?', (transaction_id,))
            self.conn.commit()
            return True
            
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    def update_book(self, book_id: int, title: str, author: str, category: str,
                   isbn: str, publication_year: int, description: str = "") -> bool:
        """Update an existing book's details"""
        try:
            cursor = self.conn.cursor()
            
            # Check if book exists
            cursor.execute('SELECT id FROM books WHERE id = ?', (book_id,))
            if not cursor.fetchone():
                raise Exception("Book not found")
            
            # Check if ISBN is already used by another book
            cursor.execute('''
                SELECT id FROM books 
                WHERE isbn = ? AND id != ?
            ''', (isbn, book_id))
            if cursor.fetchone():
                raise Exception("ISBN already exists")
            
            # Begin transaction
            cursor.execute('BEGIN TRANSACTION')
            
            try:
                # Update book details
                cursor.execute('''
                    UPDATE books 
                    SET title = ?,
                        author = ?,
                        category = ?,
                        isbn = ?,
                        publication_year = ?,
                        description = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (title, author, category, isbn, publication_year, description, book_id))
                
                # Commit transaction
                self.conn.commit()
                return True
                
            except sqlite3.Error as e:
                # Rollback transaction on error
                self.conn.rollback()
                raise Exception(f"Failed to update book: {str(e)}")
            
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def get_book_by_id(self, book_id: int) -> Optional[Dict[str, Any]]:
        """Get a book's details by ID"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT * FROM books
                WHERE id = ?
            ''', (book_id,))
            
            result = cursor.fetchone()
            return dict(result) if result else None
            
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def get_user_issued_books(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all books currently issued to a user"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT 
                    b.*,
                    ib.issue_date,
                    ib.due_date,
                    CASE 
                        WHEN ib.due_date < datetime('now') THEN 1
                        ELSE 0
                    END as is_overdue
                FROM issued_books ib
                JOIN books b ON ib.book_id = b.id
                WHERE ib.user_id = ? AND ib.return_date IS NULL
                ORDER BY ib.issue_date DESC
            ''', (user_id,))
            
            return [dict(row) for row in cursor.fetchall()]
            
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def get_user_overdue_books(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all overdue books for a user"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT 
                    b.*,
                    ib.issue_date,
                    ib.due_date,
                    julianday('now') - julianday(ib.due_date) as days_overdue
                FROM issued_books ib
                JOIN books b ON ib.book_id = b.id
                WHERE ib.user_id = ? 
                AND ib.return_date IS NULL
                AND ib.due_date < datetime('now')
                ORDER BY ib.due_date
            ''', (user_id,))
            
            return [dict(row) for row in cursor.fetchall()]
            
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def create_default_admin(self):
        """Create a default admin user if no admin exists"""
        try:
            cursor = self.conn.cursor()
            
            # Check if any admin exists
            cursor.execute('SELECT COUNT(*) as count FROM users WHERE role = "admin"')
            if cursor.fetchone()['count'] == 0:
                # Create default admin user
                default_admin = {
                    'username': 'admin',
                    'password': 'admin123',  # Default password
                    'email': 'admin@library.com',
                    'role': 'admin'
                }
                
                # Hash the password
                hashed_password = self.hash_password(default_admin['password'])
                
                # Insert the admin user
                cursor.execute('''
                    INSERT INTO users (username, email, password, role)
                    VALUES (?, ?, ?, ?)
                ''', (default_admin['username'], default_admin['email'], 
                     hashed_password, default_admin['role']))
                
                self.conn.commit()
                print("Default admin user created successfully")
                print(f"Username: {default_admin['username']}")
                print(f"Password: {default_admin['password']}")
                print("Please change these credentials after first login!")
        except Exception as e:
            print(f"Error creating default admin: {str(e)}")
            raise 