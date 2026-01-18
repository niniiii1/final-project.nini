from datetime import date

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    IntegerField,
    DateField,
    SelectField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    NumberRange,
    Optional,
    URL,
    ValidationError,
)


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=128),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class BandForm(FlaskForm):
    name = StringField("Band Name", validators=[DataRequired(), Length(max=120)])
    country = StringField("Country", validators=[DataRequired(), Length(max=80)])
    formed_year = IntegerField(
        "Formed Year", validators=[DataRequired(), NumberRange(min=1950, max=2100)]
    )
    image_url = StringField("Image URL", validators=[Optional(), URL(), Length(max=255)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=20, max=2000)])
    submit = SubmitField("Save Band")


class AlbumForm(FlaskForm):
    band_id = SelectField("Band", coerce=int, validators=[DataRequired()])
    title = StringField("Album Title", validators=[DataRequired(), Length(max=150)])
    release_year = IntegerField(
        "Release Year", validators=[DataRequired(), NumberRange(min=1950, max=2100)]
    )
    genre = StringField("Genre", validators=[DataRequired(), Length(max=80)])
    cover_url = StringField("Cover URL", validators=[Optional(), URL(), Length(max=255)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=20, max=2000)])
    submit = SubmitField("Save Album")


class CommentForm(FlaskForm):
    body = TextAreaField("Leave a comment", validators=[DataRequired(), Length(min=5, max=500)])
    submit = SubmitField("Post Comment")


class PlaylistForm(FlaskForm):
    name = StringField("Playlist Name", validators=[DataRequired(), Length(max=120)])
    create_submit = SubmitField("Create Playlist")


class AddToPlaylistForm(FlaskForm):
    playlist_id = SelectField("Playlist", coerce=int, validators=[DataRequired()])
    position = IntegerField("Position", validators=[Optional(), NumberRange(min=1, max=500)])
    submit = SubmitField("Add to Playlist")


class ProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    update_submit = SubmitField("Update Profile")


class BandSearchForm(FlaskForm):
    query = StringField("Search", validators=[Optional(), Length(max=120)])
    country = StringField("Country", validators=[Optional(), Length(max=80)])
    submit = SubmitField("Filter")


class AlbumSearchForm(FlaskForm):
    query = StringField("Search", validators=[Optional(), Length(max=150)])
    genre = StringField("Genre", validators=[Optional(), Length(max=80)])
    submit = SubmitField("Filter")


class EventSearchForm(FlaskForm):
    city = StringField("City", validators=[Optional(), Length(max=100)])
    after_date = DateField("After", validators=[Optional()])
    submit = SubmitField("Filter")


def validate_event_date(form, field):
    if field.data and field.data < date(1950, 1, 1):
        raise ValidationError("Date must be after 1950.")


class EventForm(FlaskForm):
    title = StringField("Event Title", validators=[DataRequired(), Length(max=150)])
    venue = StringField("Venue", validators=[DataRequired(), Length(max=150)])
    city = StringField("City", validators=[DataRequired(), Length(max=100)])
    event_date = DateField("Event Date", validators=[DataRequired(), validate_event_date])
    link_url = StringField("Event Link", validators=[Optional(), URL(), Length(max=255)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=20, max=2000)])
    submit = SubmitField("Save Event")
