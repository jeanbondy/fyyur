from application import db, format_datetime


class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(timezone=False), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)

    def data(self):
        data = {
            "venue_id": self.show_venue.id,
            "venue_name": self.show_venue.name,
            "venue_image_link": self.show_venue.image_link,
            "start_time": format_datetime(str(self.start_time)),
            "artist_id": self.artist_id,
            "artist_name": self.guest_artist.name,
            "artist_image_link": self.guest_artist.image_link
        }
        return data
