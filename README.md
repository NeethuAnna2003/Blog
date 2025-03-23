# DIY Blog

A beautiful and functional blog application built with Django.

## Features

- User Authentication (Register, Login, Logout)
- Blog Post Management (CRUD Operations)
- Comments System
- Categories/Tags for Posts
- User Profiles with Bio and Profile Pictures
- Search Functionality
- Responsive Design with Bootstrap 5
- Admin Panel for Content Management

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Visit http://127.0.0.1:8000/ in your browser

## Project Structure

- `/blog` - Main application directory
- `/templates` - HTML templates
- `/static` - CSS, JavaScript, and image files
- `/media` - User-uploaded content

## Testing

Run tests with:
```bash
python manage.py test
``` 