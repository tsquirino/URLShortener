# -----------------------------------------------------------------------
# SQL models module
# Defines the SQL model used for keeping URLs in the database.
#
# (C) Tomás Quirino, August 2020
# -----------------------------------------------------------------------

from datetime import datetime

from db import db


class URL(db.Model):
    """
    Database model for storing URLs.
    """

    __tablename__ = "url"

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    shortened_url = db.Column(db.String(20), unique=True, nullable=False)
    original_url = db.Column(db.String(200), unique=False, nullable=False)
    expiration_date = db.Column(db.String(20), unique=False, nullable=False)


def delete_expired(app):
    """
    Method that deletes expired URLs from the database.
    """

    with app.app_context():
        URL.query.filter(URL.expiration_date < datetime.now().strftime('%Y-%m-%d')).delete()
        db.session.commit()
