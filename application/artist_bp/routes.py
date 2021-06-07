from flask import Blueprint, render_template, request, redirect, url_for, flash
from application.models.artist import Artist
from application.models.show import Show
from forms import *
from application import db
import sys

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

    form = ArtistForm(request.form)
    error = False
    try:
        # create new artist object and populate with form values
        new_artist = Artist()
        # populate with form values
        form.populate_obj(new_artist)
        # write to database
        db.session.add(new_artist)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    else:
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')


#  Update
#  ----------------------------------------------------------------
@artist_bp.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)

    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@artist_bp.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    form = ArtistForm()
    # create the artist object from database
    artist = Artist.query.get(artist_id)
    # create error variable and set to false
    error = False

    try:
        # populate the artist object with form values
        artist.name = form.name.data.strip()
        artist.city = form.city.data.strip()
        artist.state = form.state.data
        artist.phone = form.phone.data.strip()
        artist.genres = form.genres.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data.strip()
        artist.image_link = form.image_link.data
        artist.website = form.website_link.data
        artist.facebook_link = form.facebook_link.data
        # write to database
        db.session.add(artist)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
    else:
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully updated!')

    return redirect(url_for('artist_bp.show_artist', artist_id=artist_id))


@artist_bp.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    artist = Artist.query.get(artist_id)
    error = False
    try:
        db.session.delete(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Artist ' + artist.name + ' could not be deleted.')
        else:
            flash('Successfully deleted Artist ' + artist.name + '.')
        # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
        # clicking that button delete it from the db then redirect the user to the homepage
        return redirect(url_for('index'))