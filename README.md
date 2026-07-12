# MyDream

Flask web app for Georgian writers and their short stories. Visitors get a random story on the homepage; an admin can add writers and stories from the UI.

## Stack

- Flask + Jinja2 templates
- Flask-SQLAlchemy (SQLite)
- Flask-Login (session auth)
- Flask-WTF / WTForms (forms + CSRF)

## Features

- Register / login / logout
- The **first registered user automatically becomes admin**
- Admin-only: add writer, add story
- Writers listing page
- Random story on the homepage

## Run locally

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

# set a real secret key
# Windows (PowerShell):  $env:SECRET_KEY="your-random-secret"
# macOS / Linux:         export SECRET_KEY="your-random-secret"

python app.py
```

App runs at http://127.0.0.1:5000 — the SQLite database is created automatically at `instance/mydream.db` on first run.

## Configuration

| Env var | Default | Purpose |
| --- | --- | --- |
| `SECRET_KEY` | `dev-only-change-me` | Flask session / CSRF signing key. **Set this in production.** |
| `DATABASE_URL` | `sqlite:///mydream.db` | SQLAlchemy connection string |
| `FLASK_DEBUG` | `1` | Set to `0` in production |

## Project structure

```
app.py              # models, forms, routes
templates/          # Jinja2 templates (base, index, about, writers, auth, admin forms)
static/             # style.css, script.js, logo
instance/           # SQLite DB (generated, not committed)
```

## Notes

The database file is intentionally not committed — it contains user accounts. Register a fresh account after cloning to become the admin.
