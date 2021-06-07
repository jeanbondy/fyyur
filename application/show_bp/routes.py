from flask import Blueprint, render_template, request, flash, redirect, url_for
from application.models.venue import Venue
from application.models.artist import Artist
from application.models.show import Show
from datetime import datetime
from sqlalchemy import func
from forms import *
from application import db
import sys

show_bp = Blueprint('show_bp', __name__)


#  Shows
#  ----------------------------------------------------------------

@show_bp.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    show_query = Show.query.all()
    data = []
    for show in show_query:
        data.append(show.data())
    return render_template('pages/shows.html', shows=data)


@show_bp.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@show_bp.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    form = ShowForm(request.form)
    error = False
    try:
        # create new venue object
        new_show = Show()
        # populate with form values
        form.populate_obj(new_show)
        # write to database
        db.session.add(new_show)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. The show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    else:
        # on successful db insert, flash success
        flash('Show was successfully listed!')

    return render_template('pages/home.html')