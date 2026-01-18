from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from ..extensions import db
from ..models import FavoriteBand, FavoriteAlbum, Playlist, PlaylistItem, Album, Comment
from ..forms import PlaylistForm, ProfileForm, AddToPlaylistForm


user_bp = Blueprint("user", __name__)


@user_bp.route("/me", methods=["GET", "POST"])
@login_required
def profile():
    playlist_form = PlaylistForm()
    profile_form = ProfileForm(obj=current_user)

    if "update_submit" in request.form and profile_form.validate_on_submit():
        current_user.username = profile_form.username.data
        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("user.profile"))

    if "create_submit" in request.form and playlist_form.validate_on_submit():
        playlist = Playlist(user_id=current_user.id, name=playlist_form.name.data)
        db.session.add(playlist)
        db.session.commit()
        flash("Playlist created.", "success")
        return redirect(url_for("user.profile"))

    favorites_bands = [fav.band for fav in current_user.favorite_bands]
    favorites_albums = [fav.album for fav in current_user.favorite_albums]
    playlists = current_user.playlists
    comments = Comment.query.filter_by(user_id=current_user.id).order_by(Comment.created_at.desc()).all()

    return render_template(
        "user/profile.html",
        playlist_form=playlist_form,
        profile_form=profile_form,
        favorite_bands=favorites_bands,
        favorite_albums=favorites_albums,
        playlists=playlists,
        comments=comments,
    )


@user_bp.route("/favorites/bands/<int:band_id>", methods=["POST"])
@login_required
def toggle_favorite_band(band_id):
    favorite = FavoriteBand.query.filter_by(user_id=current_user.id, band_id=band_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        flash("Band removed from favorites.", "info")
    else:
        db.session.add(FavoriteBand(user_id=current_user.id, band_id=band_id))
        db.session.commit()
        flash("Band added to favorites.", "success")
    return redirect(request.referrer or url_for("public.bands"))


@user_bp.route("/favorites/albums/<int:album_id>", methods=["POST"])
@login_required
def toggle_favorite_album(album_id):
    favorite = FavoriteAlbum.query.filter_by(user_id=current_user.id, album_id=album_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        flash("Album removed from favorites.", "info")
    else:
        db.session.add(FavoriteAlbum(user_id=current_user.id, album_id=album_id))
        db.session.commit()
        flash("Album added to favorites.", "success")
    return redirect(request.referrer or url_for("public.albums"))


@user_bp.route("/playlists/<int:playlist_id>/delete", methods=["POST"])
@login_required
def delete_playlist(playlist_id):
    playlist = Playlist.query.filter_by(id=playlist_id, user_id=current_user.id).first_or_404()
    db.session.delete(playlist)
    db.session.commit()
    flash("Playlist deleted.", "info")
    return redirect(url_for("user.profile"))


@user_bp.route("/playlists/add/<int:album_id>", methods=["POST"])
@login_required
def add_to_playlist(album_id):
    form = AddToPlaylistForm()
    form.playlist_id.choices = [
        (playlist.id, playlist.name) for playlist in current_user.playlists
    ]
    album = Album.query.get_or_404(album_id)
    if not form.validate_on_submit():
        flash("Select a valid playlist.", "warning")
        return redirect(request.referrer or url_for("public.album_detail", album_id=album.id))
    playlist = Playlist.query.filter_by(id=form.playlist_id.data, user_id=current_user.id).first()
    if not playlist:
        flash("Select a valid playlist.", "warning")
        return redirect(request.referrer or url_for("public.album_detail", album_id=album.id))
    position = form.position.data or 1
    item = PlaylistItem(playlist_id=playlist.id, album_id=album.id, position=position)
    db.session.add(item)
    db.session.commit()
    flash("Album added to playlist.", "success")
    return redirect(url_for("user.profile"))


@user_bp.route("/comments/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id and not current_user.is_admin:
        flash("You don't have permission to delete this comment.", "danger")
        return redirect(url_for("user.profile"))
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted.", "info")
    return redirect(request.referrer or url_for("user.profile"))
