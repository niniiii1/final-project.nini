# Rock Music Hub (Flask)

Rock Music Hub is an integrated resource for rock music history, bands, albums, concerts, and community-driven playlists. The Flask app includes authentication, admin management, and a content-rich UI built with Bootstrap 5.

## Features
- Home, Bands, Albums, and Events pages with curated sample data.
- User registration/login with Flask-Login.
- Favorites, playlists, and commenting for community interaction.
- Admin dashboard to manage bands, albums, events, comments, and user roles.
- Flask-WTF forms with validation and error feedback.
- SQLite by default with PostgreSQL-ready configuration.

## Screenshots
- Homepage: _add screenshot here_
- Bands page: _add screenshot here_
- Admin dashboard: _add screenshot here_

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the app
```bash
flask --app run.py run
```

You can also run:
```bash
python run.py
```

## Admin credentials (seeded)
- Email: `admin@example.com`
- Password: `Admin123!`

You can override these with environment variables:
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`
- `ADMIN_USERNAME`

## Deployment notes
- Set `SECRET_KEY` and `DATABASE_URL` in production.
- Use PostgreSQL by setting `DATABASE_URL=postgresql+psycopg2://...`.

## Hosted app
- _Hosted link placeholder_

## GitHub repository
- _GitHub link placeholder_
