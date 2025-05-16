import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import threading
import time
import logging
from typing import Optional, List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EmailTemplate:
    """Email template manager"""
    
    @staticmethod
    def due_reminder(book_title: str, due_date: str) -> str:
        """Generate due reminder email body"""
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2 style="color: #2196F3;">Library Book Due Reminder</h2>
                <p>Dear Library Member,</p>
                <p>This is a friendly reminder that the following book is due tomorrow:</p>
                <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Book Title:</strong> {book_title}</p>
                    <p><strong>Due Date:</strong> {due_date}</p>
                </div>
                <p>Please return the book on time to avoid any late fees.</p>
                <p>Thank you for your cooperation.</p>
                <hr style="border: 1px solid #eee; margin: 20px 0;">
                <p style="color: #666; font-size: 12px;">
                    This is an automated message. Please do not reply to this email.
                </p>
            </body>
        </html>
        """
    
    @staticmethod
    def overdue_notice(book_title: str, due_date: str, days_overdue: int) -> str:
        """Generate overdue notice email body"""
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2 style="color: #F44336;">Library Book Overdue Notice</h2>
                <p>Dear Library Member,</p>
                <p>The following book is currently overdue:</p>
                <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Book Title:</strong> {book_title}</p>
                    <p><strong>Due Date:</strong> {due_date}</p>
                    <p><strong>Days Overdue:</strong> {days_overdue}</p>
                </div>
                <p>Please return the book as soon as possible to avoid accumulating late fees.</p>
                <p>If you have any questions, please contact the library staff.</p>
                <hr style="border: 1px solid #eee; margin: 20px 0;">
                <p style="color: #666; font-size: 12px;">
                    This is an automated message. Please do not reply to this email.
                </p>
            </body>
        </html>
        """

class NotificationSystem:
    def __init__(self, smtp_server: str, smtp_port: int,
                 sender_email: str, sender_password: str):
        """Initialize notification system with SMTP settings"""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.db = None
        self.running = False
        self.check_interval = 3600  # Check every hour
    
    def set_database(self, db):
        """Set database connection"""
        self.db = db
    
    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """Send email using SMTP"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = recipient
            
            # Attach HTML content
            msg.attach(MIMEText(body, 'html'))
            
            # Connect to SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_due_reminder(self, user_id: int, book_id: int) -> bool:
        """Send due reminder email for a book"""
        try:
            if not self.db:
                raise Exception("Database connection not set")
            
            # Get book and user details
            book = self.db.get_book_details(book_id)
            user = self.db.get_user_details(user_id)
            
            if not book or not user:
                raise Exception("Book or user not found")
            
            # Generate email
            subject = "Library Book Due Reminder"
            body = EmailTemplate.due_reminder(
                book['title'],
                book['due_date']
            )
            
            # Send email
            return self.send_email(user['email'], subject, body)
            
        except Exception as e:
            logger.error(f"Failed to send due reminder: {str(e)}")
            return False
    
    def send_overdue_notice(self, user_id: int, book_id: int) -> bool:
        """Send overdue notice email for a book"""
        try:
            if not self.db:
                raise Exception("Database connection not set")
            
            # Get book and user details
            book = self.db.get_book_details(book_id)
            user = self.db.get_user_details(user_id)
            
            if not book or not user:
                raise Exception("Book or user not found")
            
            # Calculate days overdue
            due_date = datetime.strptime(book['due_date'], "%Y-%m-%d %H:%M:%S")
            days_overdue = (datetime.now() - due_date).days
            
            # Generate email
            subject = "Library Book Overdue Notice"
            body = EmailTemplate.overdue_notice(
                book['title'],
                book['due_date'],
                days_overdue
            )
            
            # Send email
            return self.send_email(user['email'], subject, body)
            
        except Exception as e:
            logger.error(f"Failed to send overdue notice: {str(e)}")
            return False
    
    def check_and_send_reminders(self):
        """Check for books due tomorrow and overdue books"""
        try:
            if not self.db:
                raise Exception("Database connection not set")
            
            # Get books due tomorrow
            tomorrow = datetime.now() + timedelta(days=1)
            tomorrow_str = tomorrow.strftime("%Y-%m-%d")
            
            cursor = self.db.conn.cursor()
            cursor.execute('''
                SELECT ib.book_id, ib.user_id
                FROM issued_books ib
                WHERE ib.return_date IS NULL
                AND date(ib.due_date) = date(?)
            ''', (tomorrow_str,))
            
            due_tomorrow = cursor.fetchall()
            
            # Send due reminders
            for book_id, user_id in due_tomorrow:
                self.send_due_reminder(user_id, book_id)
            
            # Get overdue books
            cursor.execute('''
                SELECT ib.book_id, ib.user_id
                FROM issued_books ib
                WHERE ib.return_date IS NULL
                AND ib.due_date < datetime('now')
            ''')
            
            overdue = cursor.fetchall()
            
            # Send overdue notices
            for book_id, user_id in overdue:
                self.send_overdue_notice(user_id, book_id)
            
            logger.info(f"Sent {len(due_tomorrow)} due reminders and {len(overdue)} overdue notices")
            
        except Exception as e:
            logger.error(f"Failed to check and send reminders: {str(e)}")
    
    def start_notification_thread(self):
        """Start the notification checking thread"""
        if self.running:
            return
        
        self.running = True
        
        def notification_loop():
            while self.running:
                try:
                    self.check_and_send_reminders()
                except Exception as e:
                    logger.error(f"Error in notification loop: {str(e)}")
                time.sleep(self.check_interval)
        
        thread = threading.Thread(target=notification_loop, daemon=True)
        thread.start()
        logger.info("Notification thread started")
    
    def stop_notification_thread(self):
        """Stop the notification checking thread"""
        self.running = False
        logger.info("Notification thread stopped")

# Example usage:
if __name__ == "__main__":
    # Configure email settings
    notification_system = NotificationSystem(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        sender_email="your-email@gmail.com",
        sender_password="your-app-password"
    )
    
    # Set up database connection
    from database import Database
    db = Database()
    notification_system.set_database(db)
    
    # Check and send reminders
    notification_system.check_and_send_reminders() 