# 🎬 Movie Platform with Ticket Booking System 

A Django-based movie recommendation web application with user authentication, an admin-managed movie catalog, and amenity-based filtering — styled with a dark, cinematic theme.

## 🔗 Live Demo

**[https://movie-recommenation-system.onrender.com/#!](https://movie-recommenation-system.onrender.com/#!)**

> Note: This is hosted on Render's free tier. The app may take 30–60 seconds to load on the first visit after a period of inactivity, as the free instance spins down when idle.

## ✨ Features

- **User Authentication** — Register, log in, and log out securely using Django's built-in auth system.
- **Movie Catalog** — Browse movies with posters, titles, and descriptions.
- **Genre/Amenity Filtering** — Filter movies by category (Action, Comedy, Horror, Thriller, Romance, etc.) using a multi-select dropdown.
- **Admin Panel** — Manage movies and amenities easily via Django's built-in admin interface.
- **Responsive Dark UI** — A Netflix-inspired cinematic dark theme with hover effects on movie cards.

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite (local) / PostgreSQL (production, optional)
- **Frontend**: HTML, CSS, JavaScript, jQuery, Materialize CSS
- **Deployment**: Render
- **Static File Serving**: WhiteNoise
- **WSGI Server**: Gunicorn

## 📁 Project Structure

```
core/
├── book/                   # Main app
│   ├── management/
│   │   └── commands/
│   │       └── create_admin.py   # Auto-creates superuser on deploy
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── login.html
│   │   └── register.html
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── core/                   # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── build.sh                # Render build script
├── manage.py
└── requirements.txt
```

## 🚀 Getting Started Locally

### Prerequisites
- Python 3.10+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SomethingAboutLuv7/Movie-Recommenation-System.git
   cd Movie-Recommenation-System/core
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv env
   # Windows
   env\Scripts\activate
   # macOS/Linux
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Add movies and amenities**
   Visit `http://127.0.0.1:8000/admin/`, log in, and add a few amenities and movies to populate the homepage.

8. **Visit the app**
   Open `http://127.0.0.1:8000/` in your browser.

## 🌐 Deployment

This project is deployed on [Render](https://render.com) using:
- **Build Command**: `bash build.sh`
- **Start Command**: `gunicorn core.wsgi`

Environment variables used in production:
- `DATABASE_URL` — PostgreSQL connection string (optional; falls back to SQLite if unset)
- `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD` — used to auto-create an admin account on deploy

## 📄 License

This project is open source and available for learning purposes.

## 🙏 Acknowledgments

Built as a learning project exploring Django authentication, REST-style API views, and deployment workflows.
