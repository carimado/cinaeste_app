from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2
import requests
import json
import bcrypt
import os
import cloudinary
import cloudinary.uploader

DB_URL = os.environ.get('DATABASE_URL', 'dbname=cinaeste')

CLOUDINARY_CLOUD = os.environ.get('CLOUDINARY_CLOUD')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

app = Flask(__name__)

# FOR SESSIONS
app.config['SECRET_KEY'] = 'secret key'

cloudinary.config(
    cloud_name = CLOUDINARY_CLOUD,
    api_key = CLOUDINARY_API_KEY,
    api_secret = CLOUDINARY_API_SECRET,
)

# user_id = 1
watch_list = 0

@app.route('/')
def index():

    return render_template('index.html')

# FROM INDEX.HTML > SEARCH_RESULTS.HTML
# THIS SHOWS A LIST OF ALL THE MOVIE RESULTS
@app.route('/search_results', methods=['GET', 'POST'])
def search_results():

    # THIS CONTROL FLOW DOESNT WORK 
    movie = request.form['movie']
    if movie == False:
        return render_template('search_results.html', search_results=search_results)
    else:
        response = requests.get(f'http://www.omdbapi.com/?s={movie}&apikey=4b9f1a76')
        data = response.json()

        search_results = data['Search']

        return render_template('search_results.html', search_results=search_results)

# ADD FAVOURITE BUTTON > DATABASE > DISPLAYED IN PROFILE
@app.route('/add_favourite', methods=['POST'])
def add_favourite_action():

    imdbID = request.form['favourite_movie']
    x = imdbID.replace("'", '"')
    json_data = json.loads(x)

    imdbID_data = json_data['imdbID']
    title = json_data['Title']
    poster = json_data['Poster']

    print(json_data)

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("INSERT INTO fave_movies (user_id, movie_id, movie_title, movie_poster) VALUES (%s, %s, %s, %s)", [session['user_id'], imdbID_data, title, poster])

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/')

@app.route('/delete_from_fave_movies/<movie_id>')
def delete_from_fave_movies(movie_id):

        print(movie_id)
    
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("DELETE FROM fave_movies WHERE movie_id = %s", [movie_id])
    
        conn.commit()
        cur.close()
        conn.close()
    
        return redirect('/profile')

@app.route('/delete_watchlist/<id>')
def delete_watchlist(id):

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('DELETE FROM watch_list_movies WHERE watch_list_id =%s', [id])
    conn.commit()

    cur.execute('DELETE FROM watch_list WHERE watch_list_id =%s', [id])
    conn.commit()

    cur.close()
    conn.close()

    return redirect('/profile')

@app.route('/delete_from_watchlist/<id>')
def delete_from_watchlist(id):

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("DELETE FROM watch_list_movies WHERE movie_id =%s", [id])
    conn.commit()

    cur.close()
    conn.close()

    return redirect('/profile')

# DISPLAYS ALL THE MOVIES IN THE WATCHLIST FROM PROFILE.HTML
# THIS PAGE HAS A SEARCH FUNCTION > WATCH_LIST_SEARCH_RESULT.HTML
@app.route('/watch-list/<id>')
def watch_list_action(id):

    session['list_id'] = id
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM watch_list_movies WHERE watch_list_id=%s", [session['list_id']])
    watch_list = cur.fetchall()

    movie_list_data = []

    for movie in watch_list:
        response = requests.get(f'http://www.omdbapi.com/?i={movie[2]}&apikey=4b9f1a76')
        data = response.json()

        movie_details = {}

        movie_details['imdbID'] = data['imdbID']
        movie_details['Title'] = data['Title']
        movie_details['Year'] = data['Year']
        movie_details['Runtime'] = data['Runtime']
        movie_details['Director'] = data['Director']
        movie_details['Poster'] = data['Poster']
        movie_details['imdbRating'] = data['imdbRating']

        movie_list_data.append(movie_details)

    # print(movie_list_data)
    print(watch_list)
    

    return render_template('watch_list.html', movie_list_data=movie_list_data)

@app.route('/add_to_watch_list/<id>')
def add_to_watch_list_action(id):

    return render_template('add_to_watch_list.html', id=id)

@app.route('/watch_list_search_result/', methods=['POST'])
def watch_list_search_result():

    movie = request.form['movie']
    response = requests.get(f'http://www.omdbapi.com/?s={movie}&apikey=4b9f1a76')
    data = response.json()

    search_results = data['Search']

    return render_template('watch_list_search_result.html', id=id, search_results=search_results)

# THE (HIDDEN) FORM "ADD TO WATCH LIST" > REDIRECTS HOME
# AND ADDS TO WATCH_LIST_ADD.HTML
@app.route('/watch_list_add', methods=['POST'])
def watch_list_add():
    movie = request.form['movie_to_add']
    x = movie.replace("'", '"')
    json_data = json.loads(x)

    movie_id = json_data['imdbID']

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("INSERT INTO watch_list_movies (watch_list_id, movie_id) VALUES (%s, %s)", [session['list_id'], movie_id])

    conn.commit()
    cur.close()
    conn.close()

    print(movie_id)

    return redirect('/')

@app.route('/community_watchlists')
def community_watchlists():

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM watch_list")
    community_watchlists = cur.fetchall()

    return render_template('community_watchlists.html', community_watchlists=community_watchlists)

@app.route('/about')
def about():
    return render_template('about.html')

# SIGN UP > SIGN_UP_ACTION
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/sign_up_action', methods=['POST'])
def sign_up_action():
    # NO SESSION YET AND NO PASSWORD HASH YET
    f_name = request.form['f_name']
    l_name = request.form['l_name']
    email = request.form['email']
    password = request.form['password']

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('INSERT INTO users (f_name, l_name, email, password) VALUES (%s, %s, %s, %s)', [f_name, l_name, email, password])

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/')


# LOGIN.HTML > ACTION
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_form_action', methods=['POST'])
def login_form_action():
    email = request.form['email']
    password = request.form['password']

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, email, password FROM users WHERE email=%s", [email])
    user_record = cur.fetchone()

    cur.close()
    conn.close()

    user_id, user_email, user_password = user_record
    # valid = bcrypt.checkpw(password.encode('utf-8'), user_password.encode('utf-8'))


    if user_record:
        print(f'Logged in as ID: {user_email}, Password: {password}')
        response = redirect('/')
        session['user_id'] = user_id
        return response
    else:
        print(email)
        print('User record not found')
        return redirect('/login')

    return redirect('/')


@app.route('/logout')
def logout():
    response = redirect('/')
    session.pop('user_id', None)
    session.pop('list_id', None)
    session.pop('user_email', None)
    return response


# INDEX.HTML > PROFILE.HTML
# DISPLAYS PROFILE, FAVOURITE MOVIES, WATCHLIST
@app.route('/profile')
def profile():

    # FOR TESTING
    # session['user_id'] = 1

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id =%s", [session['user_id']])
    id, f_name, l_name, email, password, bio, avatar = cur.fetchone()

    cur2 = conn.cursor()
    cur2.execute('SELECT * FROM fave_movies WHERE user_id =%s', [session['user_id']])
    fave_movies = cur2.fetchall()

    cur3 = conn.cursor()
    cur3.execute('SELECT * FROM watch_list WHERE user_id =%s', [session['user_id']])
    watch_list = cur3.fetchall()

    print(fave_movies)
    print(session['user_id'])

    return render_template('profile.html', f_name=f_name, l_name=l_name, bio=bio, avatar=avatar, fave_movies=fave_movies, watch_list=watch_list)

@app.route('/upload_profile_picture', methods=['POST'])
def upload_profile_picture():

    image = request.files['image']

    response = cloudinary.uploader.upload(image, filename=image.filename)

    image_id = response['public_id']

    cloudinary_image = cloudinary.CloudinaryImage(image_id)

    print(cloudinary_image)

    uploaded_image = cloudinary_image.image()

    thumbnail_image = [
        cloudinary_image.image(transformation=["thumbnail"])
    ]

    print(uploaded_image)
    print(session['user_id'])

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('UPDATE users SET avatar=%s WHERE id=%s', [thumbnail_image[0], session['user_id']])

    conn.commit()
    cur.close()
    conn.close()


    return redirect(url_for('profile'))

if __name__ == '__main__':
    from dotenv import load_dotenv
    app.run(debug=True)









