from datetime import date

from flask import Flask

from .extensions import db, login_manager, csrf
from .models import User, Band, Album, Event
from .routes.public import public_bp
from .routes.auth import auth_bp
from .routes.user import user_bp
from .routes.admin import admin_bp
from config import Config


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        db.create_all()
        seed_data(app)

    return app


def seed_data(app):
    if User.query.first():
        return

    admin = User(
        username=app.config["ADMIN_USERNAME"],
        email=app.config["ADMIN_EMAIL"],
        is_admin=True,
    )
    admin.set_password(app.config["ADMIN_PASSWORD"])
    db.session.add(admin)

    bands = [
        Band(
            name="The Rolling Stones",
            country="United Kingdom",
            formed_year=1962,
            description="Iconic rock innovators known for blues-infused swagger and legendary tours.",
            image_url="https://images.unsplash.com/photo-1459749411175-04bf5292ceea",
        ),
        Band(
            name="Nirvana",
            country="United States",
            formed_year=1987,
            description="Grunge pioneers who redefined rock with raw emotion and explosive energy.",
            image_url="https://images.unsplash.com/photo-1485579149621-3123dd979885",
        ),
        Band(
            name="Queen",
            country="United Kingdom",
            formed_year=1970,
            description="Theatrical rock legends blending operatic ambition with stadium anthems.",
            image_url="https://images.unsplash.com/photo-1507878866276-a947ef722fee",
        ),
        Band(
            name="Foo Fighters",
            country="United States",
            formed_year=1994,
            description="Arena-ready rock with melodic hooks and massive drum-driven energy.",
            image_url="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
        ),
        Band(
            name="Led Zeppelin",
            country="United Kingdom",
            formed_year=1968,
            description="Hard rock pioneers blending blues, folk, and mythic storytelling.",
            image_url="https://images.unsplash.com/photo-1511379938547-c1f69419868d",
        ),
        Band(
            name="Paramore",
            country="United States",
            formed_year=2004,
            description="Pop-punk to alt-rock shapeshifters with soaring vocals and bold lyrics.",
            image_url="https://images.unsplash.com/photo-1487180144351-b8472da7d491",
        ),
        Band(
            name="Arctic Monkeys",
            country="United Kingdom",
            formed_year=2002,
            description="Indie rock storytellers with sharp riffs and moody crooning.",
            image_url="https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3",
        ),
        Band(
            name="Linkin Park",
            country="United States",
            formed_year=1996,
            description="Genre-blending rock titans merging hip-hop, metal, and emotional catharsis.",
            image_url="https://images.unsplash.com/photo-1506157786151-b8491531f063",
        ),
        Band(
            name="Fleetwood Mac",
            country="United Kingdom",
            formed_year=1967,
            description="Classic rock storytellers known for harmonies and legendary studio drama.",
            image_url="https://images.unsplash.com/photo-1506157786151-b8491531f063",
        ),
    ]
    db.session.add_all(bands)
    db.session.flush()

    albums = [
        Album(
            band_id=bands[0].id,
            title="Let It Bleed",
            release_year=1969,
            genre="Classic Rock",
            cover_url="https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f",
            description="A landmark album filled with swaggering riffs and bluesy grit.",
        ),
        Album(
            band_id=bands[0].id,
            title="Sticky Fingers",
            release_year=1971,
            genre="Classic Rock",
            cover_url="https://images.unsplash.com/photo-1485579149621-3123dd979885",
            description="Soulful grooves and anthemic rock that defined the Stones' peak.",
        ),
        Album(
            band_id=bands[1].id,
            title="Nevermind",
            release_year=1991,
            genre="Grunge",
            cover_url="https://images.unsplash.com/photo-1459749411175-04bf5292ceea",
            description="The record that brought grunge to the mainstream with raw power.",
        ),
        Album(
            band_id=bands[1].id,
            title="In Utero",
            release_year=1993,
            genre="Grunge",
            cover_url="https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3",
            description="A darker, more abrasive follow-up filled with emotional intensity.",
        ),
        Album(
            band_id=bands[2].id,
            title="A Night at the Opera",
            release_year=1975,
            genre="Classic Rock",
            cover_url="https://images.unsplash.com/photo-1511379938547-c1f69419868d",
            description="Operatic ambition and intricate songwriting defined by 'Bohemian Rhapsody'.",
        ),
        Album(
            band_id=bands[2].id,
            title="News of the World",
            release_year=1977,
            genre="Classic Rock",
            cover_url="https://images.unsplash.com/photo-1487180144351-b8472da7d491",
            description="Stadium anthems and heavier riffs fuel Queen's global domination.",
        ),
        Album(
            band_id=bands[3].id,
            title="The Colour and the Shape",
            release_year=1997,
            genre="Alternative Rock",
            cover_url="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
            description="Melodic grit and powerful hooks that propelled Foo Fighters forward.",
        ),
        Album(
            band_id=bands[3].id,
            title="Wasting Light",
            release_year=2011,
            genre="Alternative Rock",
            cover_url="https://images.unsplash.com/photo-1507878866276-a947ef722fee",
            description="A raw, analog-recorded blast of arena-ready rock.",
        ),
        Album(
            band_id=bands[4].id,
            title="Led Zeppelin IV",
            release_year=1971,
            genre="Hard Rock",
            cover_url="https://images.unsplash.com/photo-1506157786151-b8491531f063",
            description="Epic compositions and the immortal 'Stairway to Heaven'.",
        ),
        Album(
            band_id=bands[4].id,
            title="Physical Graffiti",
            release_year=1975,
            genre="Hard Rock",
            cover_url="https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f",
            description="A sprawling double album showcasing Zeppelin's stylistic range.",
        ),
        Album(
            band_id=bands[5].id,
            title="Riot!",
            release_year=2007,
            genre="Pop Punk",
            cover_url="https://images.unsplash.com/photo-1485579149621-3123dd979885",
            description="Explosive hooks and youthful energy made Paramore a global force.",
        ),
        Album(
            band_id=bands[5].id,
            title="After Laughter",
            release_year=2017,
            genre="Alternative Rock",
            cover_url="https://images.unsplash.com/photo-1511379938547-c1f69419868d",
            description="Bright synth textures contrast with introspective lyricism.",
        ),
        Album(
            band_id=bands[6].id,
            title="AM",
            release_year=2013,
            genre="Indie Rock",
            cover_url="https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3",
            description="Dark grooves and confident swagger define Arctic Monkeys' evolution.",
        ),
        Album(
            band_id=bands[6].id,
            title="Whatever People Say I Am, That's What I'm Not",
            release_year=2006,
            genre="Indie Rock",
            cover_url="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
            description="A sharp, witty debut packed with storytelling and kinetic riffs.",
        ),
        Album(
            band_id=bands[7].id,
            title="Hybrid Theory",
            release_year=2000,
            genre="Nu Metal",
            cover_url="https://images.unsplash.com/photo-1507878866276-a947ef722fee",
            description="An era-defining blend of rap, rock, and emotional catharsis.",
        ),
        Album(
            band_id=bands[7].id,
            title="Meteora",
            release_year=2003,
            genre="Nu Metal",
            cover_url="https://images.unsplash.com/photo-1487180144351-b8472da7d491",
            description="Polished intensity and melodic hooks that cemented their legacy.",
        ),
        Album(
            band_id=bands[8].id,
            title="Rumours",
            release_year=1977,
            genre="Soft Rock",
            cover_url="https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f",
            description="Timeless harmonies and emotional storytelling in rock history's classics.",
        ),
        Album(
            band_id=bands[8].id,
            title="Tango in the Night",
            release_year=1987,
            genre="Pop Rock",
            cover_url="https://images.unsplash.com/photo-1459749411175-04bf5292ceea",
            description="Glossy production and melodic pop-rock hooks.",
        ),
    ]
    db.session.add_all(albums)

    events = [
        Event(
            title="Classic Rock Revival Night",
            venue="Apollo Theater",
            city="New York",
            event_date=date(2025, 3, 22),
            description="A multi-band tribute celebrating the legends of classic rock.",
            link_url="https://example.com/rock-revival",
        ),
        Event(
            title="Festival of Sound",
            venue="Echo Park",
            city="Los Angeles",
            event_date=date(2025, 5, 14),
            description="An outdoor festival featuring modern rock and indie headliners.",
            link_url="https://example.com/festival-sound",
        ),
        Event(
            title="Arena Rock Legends",
            venue="United Center",
            city="Chicago",
            event_date=date(2025, 6, 18),
            description="Celebrate the era of guitar heroes and massive choruses.",
            link_url="https://example.com/arena-rock",
        ),
        Event(
            title="Grunge & Grit",
            venue="The Crocodile",
            city="Seattle",
            event_date=date(2025, 4, 2),
            description="A night dedicated to the raw energy of 90s Seattle bands.",
            link_url="https://example.com/grunge-grit",
        ),
        Event(
            title="Vinyl Listening Lounge",
            venue="Soundwave Cafe",
            city="Austin",
            event_date=date(2025, 2, 15),
            description="Community listening party featuring deep cuts and rare pressings.",
            link_url="https://example.com/vinyl-night",
        ),
        Event(
            title="Women in Rock Showcase",
            venue="Red Rocks",
            city="Denver",
            event_date=date(2025, 7, 9),
            description="Spotlighting trailblazing rock performers across generations.",
            link_url="https://example.com/women-in-rock",
        ),
        Event(
            title="Indie Rock Discovery",
            venue="The Anthem",
            city="Washington, DC",
            event_date=date(2025, 8, 12),
            description="Emerging indie acts, album debuts, and collaborative sets.",
            link_url="https://example.com/indie-discovery",
        ),
        Event(
            title="Stadium Singalong",
            venue="Wembley Stadium",
            city="London",
            event_date=date(2025, 9, 5),
            description="A massive singalong celebrating iconic rock anthems.",
            link_url="https://example.com/stadium-singalong",
        ),
    ]
    db.session.add_all(events)

    db.session.commit()
