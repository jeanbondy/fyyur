from application import db
from flask import jsonify


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String(120)))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(120))
    shows = db.relationship('Show', backref='guest_artist', lazy=True)

    def data(self):
        genres_list = []
        for genre in self.genres:
            genres_list.append(genre)
        data = {
            "id": self.id,
            "name": self.name,
            "genres": genres_list,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website": self.website,
            "facebook_link": self.facebook_link,
            "seeking_venue": self.seeking_venue,
            "seeking_description": self.seeking_description,
            "image_link": self.image_link
        }
        return data

    # TODO: implement any missing fields, as a database migration using Flask-Migrate