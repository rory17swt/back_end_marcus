# Marcus Swietlicki — Portfolio Website Backend

A production-deployed REST API built with Django and Django REST Framework, serving as the content management backbone for [swietlicki.eu](https://swietlicki.eu) — the professional portfolio website of lyric tenor Marcus Swietlicki (English National Opera, Opera Holland Park, Glyndebourne).

The frontend is a separate React application. This repository contains the backend only.

---

## Project Background

Marcus needed a professional website he could manage himself — updating upcoming performances, his biography, and his media gallery — without touching code. The goal was to build a structured, secure API he could interact with through a simple CMS interface, backed by a real database and deployed to a live domain.

This project was planned using **Trello** to track tasks across design, build, and deployment phases, and designed with **wireframes** before any code was written.

> 📎 *[Insert wireframe images here — homepage, events list, media gallery, CMS views]*

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Language | Python 3 | Strong ecosystem for backend and data work |
| Framework | Django + Django REST Framework | Rapid API development with built-in ORM and admin |
| Database | PostgreSQL | Relational, production-grade, Heroku-native |
| Auth | JWT (SimpleJWT) | Stateless, secure, appropriate for a decoupled frontend |
| Image storage | Cloudinary | Offloads media hosting; returns URLs the frontend consumes directly |
| Email | SMTP (hosted email) | Contact form submissions forwarded to Marcus's custom domain inbox |
| Deployment | Heroku + Whitenoise | Simple, reliable PaaS with static file serving built in |
| Frontend | React (separate repo) | Decoupled architecture — backend is framework-agnostic |

---

## Planning & Design

Before writing any code, the project was mapped out using:

- **Trello board** — cards for each app, endpoint, and deployment task, moved through To Do / In Progress / Done columns
- **Wireframes** — sketched layouts for each page of the frontend to clarify what data the backend needed to serve

> 📎 *[Insert Trello board screenshot here]*

> 📎 *[Insert wireframe sketches here — events page, media gallery, bio page, contact form]*

This upfront planning shaped the data model decisions before a single model was written.

---

## Architecture Overview

The backend is structured as a Django project with five dedicated apps, each responsible for a distinct domain of the site:

```
back_end_marcus/
├── marcus_portfolio/     # Project config, settings, root URLs
├── bio/                  # Biography text and CV link
├── events/               # Upcoming and past performances
├── media/                # Photos and YouTube videos, grouped by Production
├── contact/              # Contact form — saves to DB and sends email
├── users/                # Custom auth with JWT
└── utils/                # Cloudinary upload helper, custom permissions
```

---

## Data Models

### Bio
Stores Marcus's biography text and a link to his CV. A single record, owned by the authenticated user. Publicly readable; only Marcus can update it.

```python
class Bio(models.Model):
    owner       # FK → User
    bio         # TextField
    cv          # URLField (optional)
    updated_at  # DateTimeField (auto)
```

### Event
Represents a single performance — past or upcoming.

```python
class Event(models.Model):
    owner       # FK → User
    title       # CharField
    image       # CharField (Cloudinary URL)
    datetime    # DateTimeField
    location    # CharField
    event_url   # URLField (ticket/booking link)
```

### Production + Media
Media is organised around **Productions** — named operatic productions Marcus has appeared in. Each media item (photo or YouTube video) belongs to a Production and has a category.

```python
class Production(models.Model):
    name    # CharField
    slug    # SlugField (auto-generated)
    year    # PositiveIntegerField

class Media(models.Model):
    owner           # FK → User
    image           # CharField (Cloudinary URL, optional)
    youtube_url     # URLField (optional)
    category        # Choices: 'production' | 'personality'
    production      # FK → Production (optional)
    created_at      # DateTimeField (auto)
```

The `Media` model includes a helper method that converts a standard YouTube watch URL into an embeddable URL — so the frontend never has to handle that transformation.

### ContactSubmission
Every contact form submission is saved to the database and simultaneously forwarded to Marcus's inbox via SMTP.

```python
class ContactSubmission(models.Model):
    first_name  # CharField
    last_name   # CharField
    email       # EmailField
    subject     # CharField
    message     # TextField
    created_at  # DateTimeField (auto)
```

---

## API Endpoints

| Method | Endpoint | Auth required | Description |
|---|---|---|---|
| GET | `/bio/public/` | No | Fetch Marcus's bio (public) |
| POST | `/bio/create/` | Yes | Create bio (one-time only) |
| GET/PUT | `/bio/` | Yes | Read or update the bio |
| GET | `/events/` | No | List all events |
| POST | `/events/` | Yes | Create a new event |
| GET/PUT/DELETE | `/events/<id>/` | Yes | Manage a single event |
| GET | `/media/` | No | List media (filterable by production) |
| POST | `/media/` | Yes | Upload a media item |
| GET/PUT/DELETE | `/media/<id>/` | Yes | Manage a single media item |
| GET | `/productions/` | No | List all productions |
| POST | `/productions/` | Yes | Create a production |
| GET/PUT/DELETE | `/productions/<slug>/` | Yes | Manage a production by slug |
| POST | `/contact/submit/` | No | Submit contact form |
| POST | `/login/` | No | Obtain JWT access token |

---

## Authentication

The API uses **JWT (JSON Web Tokens)** via `djangorestframework-simplejwt`. Marcus logs in through the frontend CMS, receives a token, and that token is sent with every write request. Public read endpoints (bio, events, media) require no authentication.

A custom token serializer returns user data alongside the token on login:

```python
# On successful login, the response includes:
{
  "access": "<token>",
  "refresh": "<token>",
  "user": {
    "id": 3,
    "username": "marcus",
    "email": "..."
  }
}
```

Tokens are valid for **24 hours**, after which Marcus re-authenticates.

---

## Key Problems Solved

### 1. One bio, not many
The bio endpoint needed to enforce that Marcus could only ever have one biography record — not accidentally create duplicates. The `CreateBioView` checks whether a bio already exists for the authenticated user and raises a `PermissionDenied` error if so.

### 2. YouTube URLs → embed URLs
The frontend needed embeddable YouTube URLs, not standard watch links. Rather than handling this in the frontend, the `Media` model includes a `get_youtube_embed_url()` method that converts `watch?v=` and `youtu.be/` formats automatically. The serializer exposes this as a computed `youtube_embed_url` field.

### 3. Organising media by production
Early in development, all media was a flat list. As the gallery grew, it became clear that grouping by production (e.g. "La Traviata 2024") was important. The `Production` model was introduced mid-project — the migration history shows this being added after the initial media model — with a `slug` field auto-generated from the production name for clean frontend URLs.

### 4. Contact form — save and send
A contact form that only sends email is fragile — if the SMTP call fails, the message is lost. The `contact` view saves the submission to the database first, then attempts the email send. If email fails, the submission is still recorded and can be retrieved.

### 5. Deployment configuration
The Procfile, Whitenoise middleware, and environment variable management via `django-environ` were all required to move from a local SQLite setup to a production PostgreSQL deployment on Heroku, served at a custom domain.

---

## Why This Is Relevant to a Data Engineering Role

This project demonstrates several skills that transfer directly into data work:

- **Structured data modelling** — designing relational schemas with appropriate field types, constraints, foreign keys, and ordering
- **API design** — building clean, documented endpoints that serve structured JSON; the same thinking underlies data pipeline interfaces
- **Data integrity** — enforcing business rules at the model and view layer (e.g. one bio per user, media must have an image or a URL)
- **Python backend development** — the primary language of data engineering tooling (Airflow, dbt, Spark, boto3)
- **Deployment and environment management** — production configuration, secrets handling, and cloud hosting
- **Iterative delivery** — the migration history shows the project evolving over time (new fields, new models, constraints being tightened), mirroring how data pipelines are built and maintained in practice

---

## Future Improvements

- **Admin dashboard metrics** — add a simple analytics view showing contact form volume, most recent events, and media counts by production
- **Image optimisation pipeline** — currently images are stored as Cloudinary URLs; a future improvement would be to apply Cloudinary transformations (resize, compress, format conversion) at upload time
- **Automated testing** — add a test suite covering the bio one-record constraint, contact form dual save/send behaviour, and JWT permission boundaries
- **Scheduled event archiving** — automatically move past events to an archived state rather than deleting them, preserving historical data
- **Rate limiting on the contact endpoint** — the public contact submission endpoint currently has no rate limiting, which is a production concern worth addressing

---

## Running Locally

```bash
# Clone the repo
git clone https://github.com/rory17swt/back_end_marcus.git
cd back_end_marcus

# Install dependencies
pipenv install

# Set up environment variables
# Create a .env file with: SECRET_KEY, DATABASE_URL, CLOUDINARY_URL, EMAIL_HOST_PASSWORD

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

---

## Related

- **Frontend repo:** *(link to React repo)*
- **Live site:** [swietlicki.eu](https://swietlicki.eu)