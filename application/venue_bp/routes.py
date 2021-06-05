from flask import Blueprint, render_template, request, flash
from application.models.venue import Venue
from application.models.artist import Artist
from application.models.show import Show
from datetime import datetime
from sqlalchemy import func
from forms import *
from application import db
import sys



venue_bp = Blueprint('venue_bp', __name__)

#  Venues
#  ----------------------------------------------------------------

@venue_bp.route('/venues')
def venues():

    all_venues = Venue.query.with_entities(func.count(Venue.id), Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()
    all_venues_data = []

    for city in all_venues:
        area_venues = Venue.query.filter_by(state=city.state).filter_by(city=city.city).all()
        venue_data = []
        for venue in area_venues:
            venue_data.append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len(
                    db.session.query(Show).filter(Show.venue_id == venue.id).filter(Show.start_time > datetime.now()).all())
            })
        all_venues_data.append({
            "city": city.city,
            "state": city.state,
            "venues": venue_data
        })


    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    return render_template('pages/venues.html', areas=all_venues_data)


@venue_bp.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '').strip().lower()
    venues_query = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
    venues_found = []

    for venue in venues_query:
        venue_data = venue.data()
        venue_upcoming_shows = Show.query.filter_by(venue_id=venue.id).filter(Show.start_time > datetime.now()).all()
        venue_data["num_upcoming_shows"] = len(venue_upcoming_shows)
        venues_found.append(venue_data)

    response = {
        "count": len(venues_found),
        "data": venues_found}

    sample_response = {
        "count": 1,
        "data": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@venue_bp.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue_query = Venue.query.get(venue_id)
    venue_data = venue_query.data()
    venue_shows = db.session.query(Show).join(Venue).filter(Show.venue_id == venue_id).all()
    upcoming_shows = []
    past_shows = []
    for show in venue_shows:
        show_data = show.data()
        show_data["artist_name"] = show.guest_artist.name
        show_data["artist_image_link"] = show.guest_artist.image_link

        if show.start_time > datetime.now():
            upcoming_shows.append(show_data)
        else:
            past_shows.append(show_data)
    venue_data['past_shows'] = past_shows
    venue_data['upcoming_shows'] = upcoming_shows
    venue_data["past_shows_count"] = len(past_shows)
    venue_data["upcoming_shows_count"] = len(upcoming_shows)


    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
    return render_template('pages/show_venue.html', venue=venue_data)


#  Create Venue
#  ----------------------------------------------------------------

@venue_bp.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@venue_bp.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    form = VenueForm(request.form)

    try:
        # create new venue object and populate with form values
        new_venue = Venue(
            name=form.name.data.strip(),
            address=form.address.data.strip(),
            city=form.city.data.strip(),
            state=form.state.data,
            phone=form.phone.data.strip(),
            genres=form.genres.data,
            seeking_talent=form.seeking_talent.data,
            seeking_description=form.seeking_description.data.strip(),
            image_link=form.image_link.data,
            website=form.website_link.data,
            facebook_link=form.facebook_link.data)
        # write to database
        db.session.add(new_venue)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    else:
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')

    return render_template('pages/home.html')


@venue_bp.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


@venue_bp.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@venue_bp.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))
