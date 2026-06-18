# Django Blog

A full-featured blog platform built with Django — designed as a portfolio project demonstrating clean architecture, test coverage, and real-world patterns.

---

## 🌐 Live Demo

**[django-blog-production-93e6.up.railway.app](https://django-blog-production-93e6.up.railway.app/)**

## ✨ Features

- **Custom authentication** — email-based login (no username), custom `User` model with `AbstractBaseUser`
- **Post management** — draft / published / archived workflow with slug auto-generation
- **Comment system** — comment submission with admin approval queue
- **Taxonomy** — category and tag filtering with dedicated URL routes
- **Search** — full-text search across title, excerpt, and body using `Q` objects
- **Reading time** — auto-calculated per post
- **View counter** — atomic increment via Django `F()` expressions (race-condition safe)
- **RSS feed** — available at `/blog/feed/`
- **Sitemap** — auto-generated XML sitemap at `/sitemap.xml`
- **SEO** — per-post Open Graph and Twitter Card meta tags
- **Newsletter** — subscription with duplicate-email protection
- **Contact form** — with CAPTCHA (django-simple-captcha)
- **Related posts** — sidebar widget using category overlap and view count ranking
- **Profile system** — auto-created on user registration via Django signals
- **Admin panel** — customized with filters, search, and date hierarchy

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 6.0.5 |
| Database | PostgreSQL (production), SQLite (development) |
| Image handling | Pillow |
| Media storage | Supabase Storage |
| Static files | WhiteNoise |
| Deployment | Railway |
| CAPTCHA | django-simple-captcha |
| Environment | python-dotenv |
| Code style | Black |

## 📁 Project Structure

```
django-blog/
├── apps/
│   ├── accounts/       # Custom User, Profile, signals, validators
│   ├── blog/           # Post, Category, Tag, Comment models + views
│   └── core/           # Home, Contact, Newsletter, Sitemap
├── config/             # Settings, URLs, WSGI
├── templates/          # HTML templates
├── static/             # CSS, JS, images
├── requirements.txt
└── requirements-dev.txt
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/Paradoxel/django-blog.git
cd django-blog

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your values

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` and configure:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
GOOGLE_MAPS_API_KEY=your-google-maps-key   # optional
```

---

## 🧪 Running Tests

```bash
python manage.py test
```

59+ tests covering models, views, forms, signals, and comment submission.

---

## 🔗 Key URLs

| URL | Description |
|---|---|
| `/` | Home page |
| `/blog/` | Blog post list |
| `/blog/<slug>/` | Post detail |
| `/blog/feed/` | RSS feed |
| `/sitemap.xml` | XML sitemap |
| `/robots.txt` | Robots file |
| `/contact/` | Contact form |
| `/admin/` | Django admin |

---

## 🏗 Architecture Highlights

**Custom User model** — email as the unique identifier, no username field. Built with `AbstractBaseUser` and `PermissionsMixin` for full control.

**QuerySet methods** — `Post.objects.published()`, `Comment.objects.approved()` — business logic lives in the model layer, not views.

**Signals** — `Profile` auto-created on `User` post-save using Django's Observer pattern.

**Atomic view counter** — uses `F("view_count") + 1` to prevent race conditions under concurrent traffic.

**Template tags** — custom inclusion tags for sidebar widgets (categories, tags, authors, related posts) with N+1 query prevention via `annotate()`.

**Context processors** — global template variables (e.g. Google Maps key) injected without repeating in every view.

---

## 📐 Design Principles Applied

- **YAGNI** — no speculative features; every model field earns its place
- **DRY** — shared logic extracted into managers, validators, and template tags
- **SRP** — views handle HTTP, models handle data, forms handle validation
- **Fail Fast** — validate at the earliest point; crash loudly, not silently
- **Clean Code** — self-documenting names, docstrings, conventional commits

---

## 📬 Contact

**Mohammadreza**
- 📧 [a1mmdrez@gmail.com](mailto:a1mmdrez@gmail.com)
- 📍 Karaj, Iran
- 🐙 [github.com/Paradoxel](https://github.com/Paradoxel)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

Thank you for taking the time to explore this project.
This application represents my effort to apply object-oriented design, software architecture principles, and real-world business logic in a practical Django project.
Feedback, suggestions, and contributions are always welcome.

Yours sincerely,  
**Mohammadreza**
