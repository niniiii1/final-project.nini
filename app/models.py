from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    playlists = db.relationship("Playlist", backref="user", lazy=True, cascade="all, delete-orphan")
    comments = db.relationship("Comment", backref="user", lazy=True, cascade="all, delete-orphan")
    favorite_bands = db.relationship(
        "FavoriteBand", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    favorite_albums = db.relationship(
        "FavoriteAlbum", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Band(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    formed_year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    albums = db.relationship("Album", backref="band", lazy=True, cascade="all, delete-orphan")
    favorites = db.relationship(
        "FavoriteBand", backref="band", lazy=True, cascade="all, delete-orphan"
    )


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey("band.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    cover_url = db.Column(db.String(255))
    description = db.Column(db.Text, nullable=False)

    playlist_items = db.relationship(
        "PlaylistItem", backref="album", lazy=True, cascade="all, delete-orphan"
    )
    favorites = db.relationship(
        "FavoriteAlbum", backref="album", lazy=True, cascade="all, delete-orphan"
    )


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    venue = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    link_url = db.Column(db.String(255))


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("PlaylistItem", backref="playlist", lazy=True, cascade="all, delete-orphan")


class PlaylistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlist.id"), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey("album.id"))
    track_name = db.Column(db.String(150))
    position = db.Column(db.Integer, default=1)


class FavoriteBand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    band_id = db.Column(db.Integer, db.ForeignKey("band.id"), nullable=False)

    __table_args__ = (db.UniqueConstraint("user_id", "band_id", name="unique_user_band"),)


class FavoriteAlbum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey("album.id"), nullable=False)

    __table_args__ = (db.UniqueConstraint("user_id", "album_id", name="unique_user_album"),)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    target_type = db.Column(db.String(20), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_hidden = db.Column(db.Boolean, default=False)
