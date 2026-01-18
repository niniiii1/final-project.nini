from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from ..extensions import db
from ..forms import BandForm, AlbumForm, EventForm
from ..models import Band, Album, Event, Comment, User


admin_bp = Blueprint("admin", __name__)


def admin_required(func):
    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            flash("Admin access required.", "danger")
            return redirect(url_for("public.home"))
        return func(*args, **kwargs)

    return wrapper


@admin_bp.route("/")
@admin_required
def dashboard():
    return render_template(
        "admin/dashboard.html",
        bands=Band.query.order_by(Band.name.asc()).all(),
        albums=Album.query.order_by(Album.title.asc()).all(),
        events=Event.query.order_by(Event.event_date.asc()).all(),
        comments=Comment.query.order_by(Comment.created_at.desc()).all(),
        users=User.query.order_by(User.created_at.desc()).all(),
    )


@admin_bp.route("/bands/new", methods=["GET", "POST"])
@admin_required
def create_band():
    form = BandForm()
    if form.validate_on_submit():
        band = Band(
            name=form.name.data,
            country=form.country.data,
            formed_year=form.formed_year.data,
            description=form.description.data,
            image_url=form.image_url.data or None,
        )
        db.session.add(band)
        db.session.commit()
        flash("Band created.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/band_form.html", form=form, title="Add Band")


@admin_bp.route("/bands/<int:band_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_band(band_id):
    band = Band.query.get_or_404(band_id)
    form = BandForm(obj=band)
    if form.validate_on_submit():
        form.populate_obj(band)
        band.image_url = form.image_url.data or None
        db.session.commit()
        flash("Band updated.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/band_form.html", form=form, title="Edit Band")


@admin_bp.route("/bands/<int:band_id>/delete", methods=["POST"])
@admin_required
def delete_band(band_id):
    band = Band.query.get_or_404(band_id)
    db.session.delete(band)
    db.session.commit()
    flash("Band deleted.", "info")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/albums/new", methods=["GET", "POST"])
@admin_required
def create_album():
    form = AlbumForm()
    form.band_id.choices = [(band.id, band.name) for band in Band.query.order_by(Band.name.asc())]
    if form.validate_on_submit():
        album = Album(
            band_id=form.band_id.data,
            title=form.title.data,
            release_year=form.release_year.data,
            genre=form.genre.data,
            cover_url=form.cover_url.data or None,
            description=form.description.data,
        )
        db.session.add(album)
        db.session.commit()
        flash("Album created.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/album_form.html", form=form, title="Add Album")


@admin_bp.route("/albums/<int:album_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_album(album_id):
    album = Album.query.get_or_404(album_id)
    form = AlbumForm(obj=album)
    form.band_id.choices = [(band.id, band.name) for band in Band.query.order_by(Band.name.asc())]
    if form.validate_on_submit():
        album.band_id = form.band_id.data
        album.title = form.title.data
        album.release_year = form.release_year.data
        album.genre = form.genre.data
        album.cover_url = form.cover_url.data or None
        album.description = form.description.data
        db.session.commit()
        flash("Album updated.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/album_form.html", form=form, title="Edit Album")


@admin_bp.route("/albums/<int:album_id>/delete", methods=["POST"])
@admin_required
def delete_album(album_id):
    album = Album.query.get_or_404(album_id)
    db.session.delete(album)
    db.session.commit()
    flash("Album deleted.", "info")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/events/new", methods=["GET", "POST"])
@admin_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            venue=form.venue.data,
            city=form.city.data,
            event_date=form.event_date.data,
            description=form.description.data,
            link_url=form.link_url.data or None,
        )
        db.session.add(event)
        db.session.commit()
        flash("Event created.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/event_form.html", form=form, title="Add Event")


@admin_bp.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        event.link_url = form.link_url.data or None
        db.session.commit()
        flash("Event updated.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/event_form.html", form=form, title="Edit Event")


@admin_bp.route("/events/<int:event_id>/delete", methods=["POST"])
@admin_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash("Event deleted.", "info")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/comments/<int:comment_id>/toggle", methods=["POST"])
@admin_required
def toggle_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.is_hidden = not comment.is_hidden
    db.session.commit()
    flash("Comment visibility updated.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/users/<int:user_id>/toggle-admin", methods=["POST"])
@admin_required
def toggle_admin(user_id):
    if current_user.id == user_id:
        flash("You cannot change your own admin status.", "warning")
        return redirect(url_for("admin.dashboard"))
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    flash("User permissions updated.", "success")
    return redirect(url_for("admin.dashboard"))
