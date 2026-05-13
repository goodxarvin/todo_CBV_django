# Todo CBV Django

A modern, containerized to-do list application built with Django using Class-Based Views (CBV). This project demonstrates best practices for Django development including REST APIs, authentication, caching, and task scheduling.

## 🎯 Overview

This is a comprehensive Django todo application that showcases:
- **Class-Based Views (CBV)** for clean, reusable view logic
- **Django REST Framework** for API endpoints
- **JWT Authentication** with SimplJWT
- **Celery** for asynchronous task processing
- **Redis** for caching and message brokering
- **Docker** containerization for easy deployment
- **pytest** for testing
- **Weather integration** with OpenWeather API

## 🚀 Features

- **User Authentication**: Sign up, login, and logout with django-allauth
- **Todo Management**: Create, read, update, and delete todo items using CBV
- **REST API**: Complete RESTful API with JWT authentication
- **Task Scheduling**: Background tasks with Celery and celery-beat
- **Caching**: Redis-based caching for improved performance
- **Email Support**: Mail templated emails for notifications
- **Weather Integration**: Real-time weather data integration
- **API Documentation**: Auto-generated API docs with drf-yasg (Swagger)
- **Production Ready**: Includes Nginx, Gunicorn, and PostgreSQL setup

## 📋 Tech Stack

### Backend
- **Django** 5.2.11 - Web framework
- **Django REST Framework** 3.17.1 - RESTful API
- **Celery** 5.6.3 - Task queue
- **Redis** - Message broker and cache
- **PostgreSQL** - Database (via psycopg)
- **Gunicorn** - WSGI application server

### Frontend & UI
- **WhiteNoise** 6.12.0 - Static file serving
- **Django Templates** - HTML templating

### Authentication & Authorization
- **django-allauth** 65.14.3 - Authentication and social auth
- **djangorestframework_simplejwt** 5.5.1 - JWT tokens

### Additional Features
- **django-filter** - Query filtering for APIs
- **django-celery-beat** - Periodic task scheduling
- **django-redis** - Redis cache backend
- **drf-yasg** - Swagger/OpenAPI documentation
- **pytest** - Testing framework
- **black** - Code formatting

## 🛠 Setup & Installation

### Prerequisites
- Docker and Docker Compose (recommended)
- Python 3.9+
- PostgreSQL 12+ (if not using Docker)
- Redis (if not using Docker)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/goodxarvin/todo_CBV_django.git
   cd todo_CBV_django
   ```

2. **Copy environment files**
   ```bash
   cp .env.example.dev_todo_web .env
   ```

3. **Start services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Access the application**
   - Web App: http://localhost
   - Admin Panel: http://localhost/admin
   - API: http://localhost/api/
   - Swagger Docs: http://localhost/swagger/

### Local Development Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example.dev_todo_web .env
   # Edit .env with your local settings
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

7. **Start Celery worker** (in another terminal)
   ```bash
   celery -A todo_core worker -l info
   ```

8. **Start Celery beat** (for scheduled tasks, in another terminal)
   ```bash
   celery -A todo_core beat -l info
   ```

## 📁 Project Structure

```
todo_CBV_django/
├── accounts/              # Custom user model and authentication
├── home/                  # Main app with CBV todo views
├── weather/               # Weather integration app
├── todo_core/             # Project settings and configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
├── templates/             # HTML templates
├── static/                # Static files (CSS, JS)
├── media/                 # User uploaded files
├── docker-compose.yml     # Local development compose file
├── docker-compose.prod.yml # Production compose file
├── Dockerfile             # Docker image configuration
├── requirements.txt       # Python dependencies
├── manage.py              # Django CLI
└── pytest.ini            # Pytest configuration
```

## 🔧 Configuration

### Environment Variables

Key environment variables to configure:

```bash
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db

# Redis
REDIS_URL=redis://localhost:6379/3

# OpenWeather API
OPENWEATHER_API_KEY=your-api-key

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Refer to `.env.example.dev_todo_web` and `.env.example.prod_todo_web` for all available options.

## 🧪 Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_views.py

# Docker
docker-compose exec web pytest
```

## 📚 API Documentation

Once running, access interactive API documentation:

- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`
- **OpenAPI Schema**: `/schema/`

### Main API Endpoints

```
GET    /api/todos/              # List all todos
POST   /api/todos/              # Create new todo
GET    /api/todos/<id>/         # Get todo detail
PUT    /api/todos/<id>/         # Update todo
DELETE /api/todos/<id>/         # Delete todo

POST   /api/auth/register/      # User registration
POST   /api/auth/login/         # User login
POST   /api/auth/token/         # Get JWT token
POST   /api/auth/logout/        # User logout
```

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f web

# Run management commands
docker-compose exec todo_web python manage.py <command>

# Production deployment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 🔐 Security

- Environment variables are used for sensitive data (no hardcoding secrets)
- CSRF protection enabled by default
- SQL injection prevention through ORM
- XFrame options protection
- Static files served through WhiteNoise in production
- Database credentials encrypted in environment

## 📝 Development Workflow

1. **Create feature branch**: `git checkout -b feature/new-feature`
2. **Make changes** and test locally
3. **Run black formatter**: `black .`
4. **Run tests**: `pytest`
5. **Commit changes**: `git commit -am "Add new feature"`
6. **Push to GitHub**: `git push origin feature/new-feature`
7. **Create Pull Request**

## 📦 Deployment

### Production Setup with Docker

1. **Use production compose file**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

2. **Collect static files**
   ```bash
   docker-compose -f docker-compose.prod.yml exec todo_web python manage.py collectstatic --noinput
   ```

3. **Run migrations**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec todo_web python manage.py migrate
   ```

4. **Configure Nginx** via `default.conf`

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Ensure code follows Black formatting
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Goodxarvin** - [GitHub Profile](https://github.com/goodxarvin)

## 🆘 Support

For issues and questions:
- Open an [Issue](https://github.com/goodxarvin/todo_CBV_django/issues)
- Check existing documentation and issues
- Review Docker logs: `docker-compose logs web`

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Last Updated**: May 2026

Enjoy building with Django! 🎉
