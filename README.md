# Marcus Swietlicki - Portfolio Website Backend

A production-deployed REST API built with Django and Django REST Framework, serving as the content management backbone for [swietlicki.eu](https://swietlicki.eu). The professional portfolio website of lyric tenor Marcus Swietlicki.

The frontend is a separate React application. This repository contains the backend only.

## Project Background

Marcus needed a professional website he could manage himself so he can updating upcoming performances, his biography, and his media gallery without touching code. The goal was to build a structured, secure API he could interact with through a simple CMS interface, backed by a PostgressSQL database and deployed to a live domain.

This project was planned using **Trello** to track tasks across the design and build, and designed with **wireframes** before any code was written.

> 📎 *[Insert wireframe images here — homepage, events list, media gallery, CMS views]*

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

## Planning & Design

Before writing any code, the project was mapped out using:

- **Trello board**: Cards for each app, endpoint, and deployment task
- **Wireframes**: Sketched rough layouts as a guidline for each page of the frontend to clarify what data the backend needed to serve

> 📎 *[Link to trello board]*

This helped planning the data model decisions before a the models was written.

## Architecture Overview

The backend is structured as a Django project with five dedicated apps, each responsible for a distinct domain of the site:

```
back_end_marcus/
├── marcus_portfolio/     # Project config, settings, root URLs
├── bio/                  # Biography text and CV link
├── events/               # Upcoming performances
├── media/                # Photos and YouTube videos
├── contact/              # Contact form - saves to DB and sends email
├── users/                # Custom auth with JWT
└── utils/                # Cloudinary upload helper, custom permissions
```

## Data Models

### Bio
Stores Marcus's biography text and a link to his CV. A single record, owned by the authenticated user. Publicly readable and only Marcus can update it.

```python
class Bio(models.Model):
    owner       # FK → User
    bio         # TextField
    cv          # URLField (optional)
    updated_at  # DateTimeField (auto)
```

### Event
Represents a single upcoming performance.

```python
class Event(models.Model):
    owner       # FK -> User
    title       # CharField
    image       # CharField (Cloudinary URL)
    datetime    # DateTimeField
    location    # CharField
    event_url   # URLField (ticket / booking / info link)
```

### Production and Media
Media is organised around **Productions**. Each image item belongs to a Production and has a category, or is placed in the personality section.

```python
class Production(models.Model):
    name    # CharField
    slug    # SlugField (auto-generated)
    year    # PositiveIntegerField

class Media(models.Model):
    owner           # FK -> User
    image           # CharField (Cloudinary URL, optional)
    youtube_url     # URLField (optional)
    category        # Choices: 'production' | 'personality'
    production      # FK -> Production (optional)
    created_at      # DateTimeField (auto)
```

The `Media` model includes a helper method that converts a standard YouTube watch URL into an embeddable URL. This is so the frontend never has to handle that transformation.

### Contact Submission
Every contact form submission is saved to the database and simultaneously forwarded to Marcus's inbox.

```python
class ContactSubmission(models.Model):
    first_name  # CharField
    last_name   # CharField
    email       # EmailField
    subject     # CharField
    message     # TextField
    created_at  # DateTimeField (auto)
```

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

## Authentication

The API uses **JWT (JSON Web Tokens)** via `djangorestframework-simplejwt`. Marcus logs in through the frontend, receives a token, and that token is sent with every write request. Public read endpoints (bio, events, media) require no authentication.

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

## Key Problems Solved

### 1. One bio, not many
The bio endpoint needed to enforce that Marcus could only ever have one biography record, not accidentally create duplicates. The `CreateBioView` checks whether a bio already exists for the authenticated user and raises a `PermissionDenied` error if so.

### 2. YouTube URLs -> embed URLs
The frontend needed embeddable YouTube URLs, not standard watch links. Rather than handling this in the frontend, the `Media` model includes a `get_youtube_embed_url()` method that converts `watch?v=` and `youtu.be/` formats automatically. The serializer exposes this as a computed `youtube_embed_url` field.

### 3. Organising media by production
Early in development, all media was a flat list. As the gallery grew, it became clear that grouping by production (e.g. "La Traviata 2024") was important. The `Production` model was introduced mid-project to solve this.

### 4. Contact form - save and send
A contact form that only sends email is fragile, if the SMTP call fails, the message is lost. The `contact` view saves the submission to the database first, then attempts to send the email. If email fails, the submission is still recorded and can be retrieved, there is also error handling included in the front end to convey this to the user.

### 5. Deployment configuration
The Procfile, Whitenoise middleware, and environment variable management via `django-environ` were all required to move from a local SQLite setup to a production PostgreSQL deployment on Heroku, served at a custom domain.

## Future Improvements (look into)

- **Admin dashboard metrics** — add a simple analytics view showing contact form volume, most recent events, and media counts by production
- **Image optimisation pipeline** — currently images are stored as Cloudinary URLs; a future improvement would be to apply Cloudinary transformations (resize, compress, format conversion) at upload time
- **Automated testing** — add a test suite covering the bio one-record constraint, contact form dual save/send behaviour, and JWT permission boundaries
- **Scheduled event archiving** — automatically move past events to an archived state rather than deleting them, preserving historical data
- **Rate limiting on the contact endpoint** — the public contact submission endpoint currently has no rate limiting, which is a production concern worth addressing

## Related

- **Frontend repo:** [https://github.com/rory17swt/front_end_marcus]
- **Live site:** [swietlicki.eu](https://swietlicki.eu)