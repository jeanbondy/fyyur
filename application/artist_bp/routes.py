from flask import Blueprint, render_template, request
from application.models.artist import Artist
from application.models.show import Show
from datetime import datetime
from forms import *


artist_bp = Blueprint('artist_bp', __name__)


#  Artists
#  ----------------------------------------------------------------
@artist_bp.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@artist_bp.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # search for "A" should return "Guns N Petals", "Matt Quevedo", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '').strip().lower()
    artists_query = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()
    artists_found = []

    for artist in artists_query:
        artist_data = artist.data()
        artist_upcoming_shows = Show.query.filter_by(artist_id=artist.id).filter(Show.start_time > datetime.now()).all()
        artist_data["num_upcoming_shows"] = len(artist_upcoming_shows)
        artists_found.append(artist_data)

    response = {
        "count": len(artists_found),
        "data": artists_found}
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@artist_bp.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    artist_query = Artist.query.get(artist_id)
    artist_data = artist_query.data()
    artist_upcoming_shows = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time > datetime.now()).all()
    artist_shows = Show.query.filter_by(artist_id=artist_id).all()
    upcoming_shows = []
    past_shows = []
    for show in artist_shows:
        if show.start_time > datetime.now():
            upcoming_shows.append(show.data())
        else:
            past_shows.append(show.data())
    artist_data['past_shows'] = past_shows
    artist_data['upcoming_shows'] = upcoming_shows
    artist_data["past_shows_count"] = len(past_shows)
    artist_data["upcoming_shows_count"] = len(upcoming_shows)
    return render_template('pages/show_artist.html', artist=artist_data)


#  Create Artist
#  ----------------------------------------------------------------

@artist_bp.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@artist_bp.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Update
#  ----------------------------------------------------------------
@artist_bp.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist_query = Artist.query.get(artist_id)
    artist_data = artist_query.data()
    artist = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@artist_bp.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))