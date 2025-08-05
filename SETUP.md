# Smart Study - Setup Instructions

## Quick Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Sample Data**
   ```bash
   python manage.py create_sample_data
   ```

4. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

5. **Access the Application**
   - Web Interface: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

## Login Credentials

### Admin User
- Username: `admin`
- Password: `admin123`
- Access: Full system administration

### Teacher User
- Username: `teacher1`
- Password: `teacher123`
- Access: Doubt resolution, student progress monitoring

### Student User
- Username: `student1`
- Password: `student123`
- Access: Course access, quiz taking, doubt submission

## Features Available

### For Students
- Browse and access courses
- Watch video lectures
- Download study materials (PDFs)
- Take interactive quizzes
- Submit doubts with images
- Track learning progress
- Enroll in courses (payment simulation)

### For Teachers
- View and resolve student doubts
- Monitor student progress
- Access teacher dashboard
- Assign doubts to themselves

### For Administrators
- Full system management
- User administration
- Content management
- View system analytics

## Application Structure

- **Main App**: Home page, search, about, contact
- **Accounts App**: User management, authentication, profiles
- **Courses App**: Subjects, chapters, lectures, enrollment
- **Quizzes App**: Interactive quizzes with timer and results
- **Doubts App**: Doubt submission and resolution system

## Color Scheme & Design

The application uses a modern, accessible color scheme:
- Primary: Blue (#3b82f6)
- Success: Green (#10b981)
- Warning: Amber (#f59e0b)
- Danger: Red (#ef4444)
- Text: Dark gray (#111827)
- Background: White with light gray accents

All pages are fully responsive and work on desktop, tablet, and mobile devices.

## Next Steps

1. Add real video content to lectures
2. Implement actual payment gateway
3. Add email notifications
4. Enhance analytics and reporting
5. Add more interactive features

## Troubleshooting

If you encounter any issues:
1. Make sure all dependencies are installed
2. Run migrations if database errors occur
3. Check that the development server is running on port 8000
4. Clear browser cache if styling issues persist