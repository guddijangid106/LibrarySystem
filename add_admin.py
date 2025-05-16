import sqlite3
import hashlib
import os

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def add_admin():
    try:
        # Check if database file exists
        if not os.path.exists('library.db'):
            print("Error: library.db file not found!")
            return

        print("Connecting to database...")
        # Connect to database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("Error: users table not found!")
            return
        
        print("Checking for admin user...")
        # Check if admin exists
        cursor.execute('SELECT COUNT(*) as count FROM users WHERE username = ?', ("admin",))
        result = cursor.fetchone()
        print(f"Query result: {result}")
        
        if result["count"] == 0:
            print("Adding admin user...")
            # Add admin user
            hashed_password = hash_password("admin123")
            cursor.execute('''
                INSERT INTO users (username, password, email, role)
                VALUES (?, ?, ?, ?)
            ''', ("admin", hashed_password, "admin@library.com", "admin"))
            conn.commit()
            print("Default admin user created successfully!")
            print("Username: admin")
            print("Password: admin123")
        else:
            print("Admin user already exists!")
        
        conn.close()
        print("Database connection closed.")
        
    except sqlite3.Error as e:
        print(f"SQLite error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    add_admin() 