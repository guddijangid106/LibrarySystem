# Modern Library Management System

A modern, user-friendly Library Management System built with Python and Tkinter. This application provides a complete solution for managing library operations, including book management, user management, and automated notifications.

## Features

### User Management
- Secure user authentication with role-based access control
- User registration with email validation
- Password strength requirements
- Admin and student roles with different permissions

### Book Management
- Add, edit, and remove books
- Book search and filtering
- ISBN validation
- Category management
- Publication year validation

### Book Operations
- Issue books to users
- Return books
- Track due dates
- View book history
- Check book availability

### Notifications
- Automated email reminders for due books
- Overdue notices
- Customizable email templates
- Background notification checking

### Modern UI/UX
- Clean and intuitive interface
- Responsive design
- Form validation with error messages
- Tooltips and help text
- Dark mode support

## Technical Details

### Architecture
- Modular design with separate components
- Database abstraction layer
- Form validation system
- Notification system
- Utility functions

### Database
- SQLite database for data storage
- Optimized queries with indexes
- Transaction support
- Connection pooling
- Error handling

### Security
- Password hashing
- Input validation
- SQL injection prevention
- Email verification
- Role-based access control

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/library-management-system.git
cd library-management-system
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure email settings:
   - Open `notifications.py`
   - Update SMTP settings with your email provider details
   - Set sender email and password

4. Run the application:
```bash
python main.py
```

## Default Login

- **Admin**
  - Username: admin
  - Password: admin123

## Project Structure

```
library-management-system/
├── main.py              # Application entry point
├── database.py          # Database operations
├── forms.py            # Form validation
├── notifications.py    # Email notifications
├── utils.py           # Utility functions
├── requirements.txt   # Python dependencies
└── README.md         # Project documentation
```

## Development

### Adding New Features
1. Create a new branch
2. Implement the feature
3. Add tests
4. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings
- Add comments for complex logic

### Testing
- Unit tests for core functionality
- Integration tests for database operations
- UI tests for forms and validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Python Tkinter documentation
- SQLite documentation
- Email template inspiration from various sources

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Roadmap

- [ ] Add book cover images
- [ ] Implement barcode scanning
- [ ] Add fine calculation
- [ ] Create reports and analytics
- [ ] Add multi-language support
- [ ] Implement backup system
- [ ] Add API endpoints
- [ ] Create mobile app 