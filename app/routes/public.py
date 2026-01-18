from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user

from ..extensions import db
from ..models import Band, Album, Event, Comment, FavoriteBand, FavoriteAlbum
from ..forms import BandSearchForm, AlbumSearchForm, EventSearchForm, CommentForm, AddToPlaylistForm


public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    featured_bands = Band.query.order_by(Band.created_at.desc()).limit(4).all()
    featured_albums = Album.query.order_by(Album.release_year.desc()).limit(6).all()
    events = Event.query.order_by(Event.event_date.asc()).limit(3).all()
    return render_template(
        "pages/home.html",
        featured_bands=featured_bands,
        featured_albums=featured_albums,
        events=events,
    )


@public_bp.route("/bands")
def bands():
    form = BandSearchForm(request.args, meta={"csrf": False})
    query = Band.query
    if form.validate():
        if form.query.data:
            query = query.filter(Band.name.ilike(f"%{form.query.data}%"))
        if form.country.data:
            query = query.filter(Band.country.ilike(f"%{form.country.data}%"))
    bands_list = query.order_by(Band.name.asc()).all()
    return render_template("pages/bands.html", bands=bands_list, form=form)


@public_bp.route("/bands/<int:band_id>", methods=["GET", "POST"])
def band_detail(band_id):
    band = Band.query.get_or_404(band_id)
    comments = (
        Comment.query.filter_by(target_type="band", target_id=band.id, is_hidden=False)
        .order_by(Comment.created_at.desc())
        .all()
    )
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Please log in to comment.", "warning")
            return redirect(url_for("auth.login"))
        comment = Comment(
            user_id=current_user.id,
            target_type="band",
            target_id=band.id,
            body=form.body.data,
        )
        db.session.add(comment)
        db.session.commit()
        flash("Comment posted.", "success")
        return redirect(url_for("public.band_detail", band_id=band.id))
    is_favorite = False
    if current_user.is_authenticated:
        is_favorite = (
            FavoriteBand.query.filter_by(user_id=current_user.id, band_id=band.id).first()
            is not None
        )
    return render_template(
        "pages/band_detail.html",
        band=band,
        comments=comments,
        form=form,
        is_favorite=is_favorite,
    )


@public_bp.route("/albums")
def albums():
    form = AlbumSearchForm(request.args, meta={"csrf": False})
    query = Album.query
    if form.validate():
        if form.query.data:
            query = query.filter(Album.title.ilike(f"%{form.query.data}%"))
        if form.genre.data:
            query = query.filter(Album.genre.ilike(f"%{form.genre.data}%"))
    albums_list = query.order_by(Album.release_year.desc()).all()
    return render_template("pages/albums.html", albums=albums_list, form=form)


@public_bp.route("/albums/<int:album_id>", methods=["GET", "POST"])
def album_detail(album_id):
    album = Album.query.get_or_404(album_id)
    comments = (
        Comment.query.filter_by(target_type="album", target_id=album.id, is_hidden=False)
        .order_by(Comment.created_at.desc())
        .all()
    )
    form = CommentForm()
    playlist_form = AddToPlaylistForm()
    if current_user.is_authenticated:
        playlist_form.playlist_id.choices = [
            (playlist.id, playlist.name) for playlist in current_user.playlists
        ]
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Please log in to comment.", "warning")
            return redirect(url_for("auth.login"))
        comment = Comment(
            user_id=current_user.id,
            target_type="album",
            target_id=album.id,
            body=form.body.data,
        )
        db.session.add(comment)
        db.session.commit()
        flash("Comment posted.", "success")
        return redirect(url_for("public.album_detail", album_id=album.id))
    is_favorite = False
    if current_user.is_authenticated:
        is_favorite = (
            FavoriteAlbum.query.filter_by(user_id=current_user.id, album_id=album.id).first()
            is not None
        )
    return render_template(
        "pages/album_detail.html",
        album=album,
        comments=comments,
        form=form,
        playlist_form=playlist_form,
        is_favorite=is_favorite,
    )


@public_bp.route("/events", methods=["GET"])
def events():
    form = EventSearchForm(request.args, meta={"csrf": False})
    query = Event.query
    if form.validate():
        if form.city.data:
            query = query.filter(Event.city.ilike(f"%{form.city.data}%"))
        if form.after_date.data:
            query = query.filter(Event.event_date >= form.after_date.data)
    events_list = query.order_by(Event.event_date.asc()).all()
    return render_template("pages/events.html", events=events_list, form=form)


@public_bp.route("/events/<int:event_id>", methods=["GET", "POST"])
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    comments = (
        Comment.query.filter_by(target_type="event", target_id=event.id, is_hidden=False)
        .order_by(Comment.created_at.desc())
        .all()
    )
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Please log in to comment.", "warning")
            return redirect(url_for("auth.login"))
        comment = Comment(
            user_id=current_user.id,
            target_type="event",
            target_id=event.id,
            body=form.body.data,
        )
        db.session.add(comment)
        db.session.commit()
        flash("Comment posted.", "success")
        return redirect(url_for("public.event_detail", event_id=event.id))
    return render_template("pages/event_detail.html", event=event, comments=comments, form=form)
