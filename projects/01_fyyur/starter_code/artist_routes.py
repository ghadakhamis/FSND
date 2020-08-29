from app import app, db
from flask import render_template, request, jsonify, flash, redirect, url_for
from models import Artist, Show
from datetime import datetime
import sys
from forms import ArtistForm


@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = []
  artists = Artist.query.all()
  for artist in artists:
    data.append({
        "id": artist.id,
        "name": artist.name, 
      })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  data = []
  artists = Artist.query.filter(Artist.name.like('%' + request.form.get('search_term', '') + '%')).all()
  for artist in artists:
    shows = Show.query.filter(Show.artist_id==artist.id).filter(Show.start_time>datetime.now()).all()
    data.append({
      'id': artist.id,
      'name': artist.name,
      'num_upcoming_shows': len(shows) # shows.count() fire an error 
    })
  response = {
    "count": len(artists),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  error = False
  upcoming_shows_data = []
  past_shows_data = []
  try:
    artist = Artist.query.get(artist_id)
    upcoming_shows = Show.query.filter(Show.venue_id==artist.id).filter(Show.start_time>datetime.now()).all()
    past_shows = Show.query.filter(Show.venue_id==artist.id).filter(Show.start_time<datetime.now()).all()
    if upcoming_shows:
      for upcoming_show in upcoming_shows:
        upcoming_shows_data.append({
          "venue_id": upcoming_show.venue_id,
          "venue_name": upcoming_show.venue.name,
          "venue_image_link": upcoming_show.venue.image_link,
          "start_time": upcoming_show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        })
    if past_shows:
      for past_show in past_shows:
        past_shows_data.append({
          "venue_id": past_show.venue_id,
          "venue_name": past_show.venue.name,
          "venue_image_link": past_show.venue.image_link,
          "start_time": past_show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
      })
    data ={
      "id": artist.id,
      "name": artist.name,
      "genres": artist.genres,
      "city": artist.city,
      "state": artist.state,
      "phone": artist.phone,
      "website": artist.website,
      "facebook_link": artist.facebook_link,
      "seeking_venue": artist.seeking_venue,
      "seeking_description": artist.seeking_description,
      "image_link": artist.image_link,
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
    flash('Artist not found!')
    return redirect(url_for('artists'))
  else:
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # TODO: populate form with fields from artist with ID <artist_id>
  error = False
  try:
    artist = Artist.query.get(artist_id)
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True
  finally:
    db.session.close()
  if error:
    flash('Artist not found!')
    return redirect(url_for('show_artist', artist_id=artist_id))
  else:
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  form = ArtistForm()
  data = []
  try:
    artist = Artist.query.get(artist_id)
    data = artist
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form.getlist('genres')
    artist.image_link = request.form['image_link']
    artist.seeking_venue= True if 'seeking_venue' in request.form else False
    if request.form['facebook_link']:
      artist.facebook_link = request.form['facebook_link']
    if request.form['website']:
      artist.website = request.form['website']
    if request.form['seeking_description']:
      artist.seeking_description = request.form['seeking_description']
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True
  finally:
    db.session.close()
  if error:
    flash('An error occurred. artist ' + request.form['name'] + ' could not be updated.','error')
    return render_template('forms/edit_artist.html', form=form, artist=data)
  else:
    flash('Artist ' + request.form['name'] + ' updated successfully')
    return redirect(url_for('show_artist', artist_id=artist_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  error = False
  data = {}
  form = ArtistForm()
  # if form.validate_on_submit():
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    seeking_venue= True if 'seeking_venue' in request.form else False
    # TODO: insert form data as a new Venue record in the db, instead
    artist = Artist(
      name=name, 
      city=city, 
      state=state, 
      phone=phone, 
      genres=genres, 
      image_link=image_link, 
      seeking_venue=seeking_venue)
    if request.form['facebook_link']:
      artist.facebook_link = request.form['facebook_link']
    if request.form['website']:
      artist.website = request.form['website']
    if request.form['seeking_description']:
      artist.seeking_description = request.form['seeking_description']
    db.session.add(artist)
    db.session.commit()
    # TODO: modify data to be the data object returned from db insertion
    data['name'] = artist.name
    data['state'] = artist.state
    data['city'] = artist.city
    data['phone'] = artist.phone
    data['facebook_link'] = artist.facebook_link
    data['genres'] = artist.genres
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True
  finally:
    db.session.close()
  # on successful db insert, flash success
  if error == False:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')
  # TODO: on unsuccessful db insert, flash an error instead.
  else:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.','error')
    return render_template('forms/new_artist.html', form=form)
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  # else:
  #   return render_template('forms/new_artist.html', form=form)


