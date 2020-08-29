from app import app, db
from flask import render_template, request, jsonify, flash, redirect, url_for
from models import Show
from datetime import datetime
import sys
from forms import ShowForm




@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  shows = Show.query.all()
  for show in shows:
    data.append({
      'venue_id': show.venue_id,
      'venue_name': show.venue.name,
      'artist_id': show.artist_id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  error = False
  data = {}
  form = ShowForm()
  # if form.validate_on_submit():
  try:
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']
    # TODO: insert form data as a new Show record in the db, instead
    show = Show(
      artist_id=artist_id, 
      venue_id=venue_id, 
      start_time=start_time)
    db.session.add(show)
    db.session.commit()
    # TODO: modify data to be the data object returned from db insertion
    data['artist_id'] = show.artist_id
    data['venue_id'] = show.venue_id
    data['start_time'] = show.start_time
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True
  finally:
    db.session.close()
  # on successful db insert, flash success
  if error == False:
    flash('Show was successfully listed!')
    return render_template('pages/home.html')
  # TODO: on unsuccessful db insert, flash an error instead.
  else:
    flash('An error occurred. Show could not be listed.','error')
    return render_template('forms/new_show.html', form=form)
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # else:
  #   return render_template('forms/new_show.html', form=form)
