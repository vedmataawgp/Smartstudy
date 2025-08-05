# Smart Study - Django Educational Platform

A comprehensive Django-based educational platform designed to deliver affordable, premium-quality education to students across India. This application serves students from classes 9th-12th across Science, NEET, and JEE streams.

## 🚀 Features

### Core Features
- **User Management**: Role-based access control (Students, Teachers, Administrators)
- **Course System**: Hierarchical content organization (Subjects → Chapters → Lectures)
- **Video Lectures**: Streaming and progress tracking
- **Study Materials**: PDF uploads and downloads
- **Interactive Quizzes**: Timed assessments with automatic scoring
- **Doubt Resolution**: Multi-media doubt submission and teacher assignment
- **Progress Tracking**: Individual and comprehensive analytics
- **Payment Simulation**: Course enrollment with pricing tiers

### User Roles
- **Students**: Access courses, take quizzes, submit doubts, track progress
- **Teachers**: Resolve doubts, monitor student progress, content review
- **Administrators**: Full system management, user administration, content moderation

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 5.2.4
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: Django's built-in authentication system
- **File Handling**: Django's file upload system with Pillow for image processing
- **Forms**: Django Crispy Forms with Bootstrap 5

### Frontend
- **Templates**: Django templates with Jinja2
- **CSS Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.4.0
- **JavaScript**: Vanilla JavaScript for interactivity

### Dependencies
```
Django==5.2.4
django-crispy-forms==2.4
crispy-bootstrap5==2025.6
Pillow==11.1.0
python-decouple==3.8
psycopg2-binary==2.9.10
gunicorn==23.0.0
```

## 📁 Project Structure

```
django_smart_study/
├── smart_study/          # Main project settings
│   ├── settings.py       # Django settings
│   ├── urls.py          # URL configuration
│   └── wsgi.py          # WSGI configuration
├── accounts/            # User management app
│   ├── models.py        # User, Role, Notification models
│   ├── views.py         # Authentication and dashboard views
│   ├── forms.py         # User registration and profile forms
│   └── admin.py         # Admin configuration
├── courses/             # Course management app
│   ├── models.py        # Subject, Chapter, Lecture, Progress models
│   ├── views.py         # Course browsing and enrollment views
│   └── admin.py         # Course admin interface
├── quizzes/             # Quiz system app
│   ├── models.py        # Quiz, Question, Attempt models
│   ├── views.py         # Quiz taking and results views
│   └── admin.py         # Quiz admin interface
├── doubts/              # Doubt resolution app
│   ├── models.py        # Doubt model
│   ├── views.py         # Doubt submission and resolution views
│   ├── forms.py         # Doubt forms
│   └── admin.py         # Doubt admin interface
├── main/                # Main application (home, about, etc.)
│   ├── views.py         # Public pages
│   └── urls.py          # Main URL patterns
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── accounts/        # User-related templates
│   ├── courses/         # Course templates
│   ├── quizzes/         # Quiz templates
│   ├── doubts/          # Doubt templates
│   └── main/            # Main page templates
├── static/              # Static files
│   ├── css/            # Custom stylesheets
│   ├── js/             # JavaScript files
│   └── img/            # Images
├── media/               # User-uploaded files
│   ├── pdfs/           # PDF study materials
│   └── doubts/         # Doubt images
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd django_smart_study
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load Initial Data (Optional)**
   ```bash
   python manage.py loaddata initial_roles.json
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**
   - Web Interface: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

## 🔐 Configuration

### Environment Variables (.env)
```env
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL for production)
DB_NAME=smart_study
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

## 🎯 Usage

### For Students
1. **Registration**: Create account with class and stream selection
2. **Course Access**: Browse and enroll in courses
3. **Learning**: Watch lectures, download PDFs, track progress
4. **Assessment**: Take quizzes and view results
5. **Doubt Resolution**: Submit doubts with images for teacher assistance

### For Teachers
1. **Dashboard**: Access teacher-specific dashboard
2. **Doubt Management**: View, assign, and resolve student doubts
3. **Progress Monitoring**: Track student performance
4. **Content Review**: Provide feedback on course materials

### For Administrators
1. **User Management**: Create and manage user accounts and roles
2. **Content Management**: Add subjects, chapters, lectures, and quizzes
3. **System Monitoring**: View platform analytics and user activity
4. **Data Management**: Bulk operations and data exports

## 🔒 Security Features

- **CSRF Protection**: Built-in Django CSRF protection
- **User Authentication**: Secure login/logout system
- **Role-based Access**: Granular permissions for different user types
- **File Upload Security**: Validated file uploads with size limits
- **SQL Injection Prevention**: Django ORM protection
- **XSS Protection**: Template auto-escaping

## 📱 Mobile Responsiveness

The application is fully responsive and provides an optimal viewing experience across:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes and orientations

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   # Set production environment variables
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com
   DATABASE_URL=postgresql://user:pass@host:port/db
   ```

2. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

3. **Database Migration**
   ```bash
   python manage.py migrate
   ```

4. **Web Server**
   ```bash
   gunicorn smart_study.wsgi:application
   ```

### Docker Deployment (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "smart_study.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🔧 Development

### Adding New Features

1. **Create Django App**
   ```bash
   python manage.py startapp new_feature
   ```

2. **Update Settings**
   Add app to `INSTALLED_APPS` in `settings.py`

3. **Create Models**
   Define models in `models.py`

4. **Create Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Register Admin**
   Add models to `admin.py`

### Testing
```bash
python manage.py test
```

## 🎨 Customization

### Theming
- Modify `static/css/style.css` for custom styling
- Update `templates/base.html` for layout changes
- Customize Bootstrap variables for theme consistency

### Branding
- Update logo and brand colors in CSS variables
- Modify footer and header content in base template
- Customize email templates for notifications

## 📊 Analytics & Monitoring

The platform includes built-in analytics for:
- User registration and activity
- Course completion rates
- Quiz performance metrics
- Doubt resolution times
- Payment and enrollment tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Version History

- **v1.0.0** - Initial Django implementation
  - Complete user management system
  - Course and quiz functionality
  - Doubt resolution system
  - Responsive design
  - Admin interface
  - Payment simulation

---

**Smart Study** - Transforming education through technology