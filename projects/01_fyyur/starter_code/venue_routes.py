from app import app, db
from flask import render_template, request, jsonify, flash, redirect, url_for
from models import Venue, Show
from datetime import datetime
import sys
from forms import VenueForm

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  areas = Venue.query.with_entities(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()
  for area in areas:
    venues = Venue.query.filter_by(state=area.state).filter_by(city=area.city).all()
    venues_data = []
    for venue in venues:
      shows =Show.query.filter(Show.venue_id==venue.id).filter(Show.start_time>datetime.now()).all()
      venues_data.append({
        "id": venue.id,
        "name": venue.name, 
        "num_upcoming_shows": len(shows) # shows.count() fire an error 
      })
    data.append({"city": area.city, "state": area.state, "venues": venues_data})
 
  return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  data = []
  venues = Venue.query.filter(Venue.name.like('%' + request.form.get('search_term', '') + '%')).all()
  for venue in venues:
    shows = Show.query.filter(Show.venue_id==venue.id).filter(Show.start_time>datetime.now()).all()
    data.append({
      'id': venue.id,
      'name': venue.name,
      'num_upcoming_shows': len(shows) # shows.count() fire an error 
    })
  response = {
    "count": len(venues),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  error = False
  upcoming_shows_data = []
  past_shows_data = []
  try:
    venue = Venue.query.get(venue_id)
    upcoming_shows = Show.query.filter(Show.venue_id==venue.id).filter(Show.start_time>datetime.now()).all()
    past_shows = Show.query.filter(Show.venue_id==venue.id).filter(Show.start_time<datetime.now()).all()
    if upcoming_shows:
      for upcoming_show in upcoming_shows:
        upcoming_shows_data.append({
          "artist_id": upcoming_show.artist_id,
          "artist_name": upcoming_show.artist.name,
          "artist_image_link": upcoming_show.artist.image_link,
          "start_time": upcoming_show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        })
    if past_shows:
      for past_show in past_shows:
        past_shows_data.append({
          "artist_id": past_show.artist_id,
          "artist_name": past_show.artist.name,
          "artist_image_link": past_show.artist.image_link,
          "start_time": past_show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
      })
    data ={
      "id": venue.id,
      "name": venue.name,
      "genres": venue.genres,
      "address": venue.address,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website": venue.website,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.seeking_talent,
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link,
      "past_shows": past_shows_data,
      "upcoming_shows": upcoming_shows_data,
      "past_shows_count": len(past_shows_data),
      "upcoming_shows_count": len(upcoming_shows_data),
    }
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True
  finally:
    db.session.close()
  if error:
    flash('Venue not found!')
    return redirect(url_for('venues'))
  else:
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  data = {}
  form = VenueForm()
  # if form.validate_on_submit():
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    seeking_talent = True if 'seeking_talent' in request.form else False
    # TODO: insert form data as a new Venue record in the db, instead
    venue = Venue(
      name=name, 
      city=city, 
      state=state, 
      address=address, 
      phone=phone, 
      genres=genres, 
      image_link=image_link, 
      seeking_talent=seeking_talent)
    if request.form['facebook_link']:
      venue.facebook_link = request.form['facebook_link']
    if request.form['website']:
      venue.website = request.form['website']
    if request.form['seeking_description']:
      venue.seeking_description = request.form['seeking_description']
    db.session.add(venue)
    db.session.commit()
    # TODO: modify data to be the data object returned from db insertion
    data['name'] = venue.name
    data['state'] = venue.state
    data['city'] = venue.city
    data['address'] = venue.address
    data['phone'] = venue.phone
    data['facebook_link'] = venue.facebook_link
    data['genres'] = venue.genres
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True
  finally:
    db.session.close()
  # on successful db insert, flash success
  if error == False:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')
  # TODO: on unsuccessful db insert, flash an error instead.
  else:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.','error')
    return render_template('forms/new_venue.html', form=form)
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # else:
  #   return render_template('forms/new_venue.html', form=form)

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    venu = Venue.query.get(venue_id)
    if venu.shows:
      error = True
    else:
      db.session.delete(venu)
      db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    return jsonify({ 'success': False })
  else:
    flash('Venue deleted successfully')
    return jsonify({ 'success': True })

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  ####### button added into view ########

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # TODO: populate form with values from venue with ID <venue_id>
  error = False
  try:
    venue = Venue.query.get(venue_id)
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True
  finally:
    db.session.close()
  if error:
    flash('Venue not found!')
    return redirect(url_for('show_venue', venue_id=venue_id))
  else:
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  form = VenueForm()
  data = []
  try:
    venue = Venue.query.get(venue_id)
    data = venue
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone = request.form['phone']
    venue.address = request.form['address']
    venue.genres = request.form.getlist('genres')
    venue.image_link = request.form['image_link']
    venue.seeking_talent= True if 'seeking_talent' in request.form else False
    if request.form['facebook_link']:
      venue.facebook_link = request.form['facebook_link']
    if request.form['website']:
      venue.website = request.form['website']
    if request.form['seeking_description']:
      venue.seeking_description = request.form['seeking_description']
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True
  finally:
    db.session.close()
  if error:
    flash('An error occurred. venue ' + request.form['name'] + ' could not be updated.','error')
    return render_template('forms/edit_venue.html', form=form, venue=data)
  else:
    flash('Venue ' + request.form['name'] + ' updated successfully')
    return redirect(url_for('show_venue', venue_id=venue_id))

