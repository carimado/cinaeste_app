from flask import Flask, render_template, request, redirect, session
import psycopg2
import requests
import json
# import bcrypt

app = Flask(__name__)

# FOR SESSIONS
app.config['SECRET_KEY'] = 'secret key'

# user_id = 1
watch_list = 0

@app.route('/')
def index():

    return render_template('index.html')

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

@app.route('/add_favourite', methods=['POST'])
def add_favourite_action():

    imdbID = request.form['favourite_movie']
    x = imdbID.replace("'", '"')
    json_data = json.loads(x)

    imdbID_data = json_data['imdbID']
    title = json_data['Title']
    poster = json_data['Poster']

    print(json_data)

    # for later on - 
    # faveMovie = requests.get(f'http://www.omdbapi.com/?i={imdbID}&apikey=4b9f1a76')
    # data = faveMovie.json()

    # title = data['Title']

    # print(imdbID)

    conn = psycopg2.connect("dbname=cinaeste")
    cur = conn.cursor()
    cur.execute("INSERT INTO fave_movies (user_id, movie_id, movie_title, movie_poster) VALUES (%s, %s, %s, %s)", [session['user_id'], imdbID_data, title, poster])

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/')


@app.route('/watch-list/<id>')
def watch_list_action(id):

    session['list_id'] = id
    conn = psycopg2.connect("dbname=cinaeste")
    cur = conn.cursor()
    cur.execute("SELECT * FROM watch_list_movies WHERE watch_list_id=%s", [session['list_id']])
    watch_list = cur.fetchall()

    return render_template('watch_list.html', watch_list=watch_list)

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

@app.route('/watch_list_add', methods=['POST'])
def watch_list_add():
    movie = request.form['movie_to_add']
    x = movie.replace("'", '"')
    json_data = json.loads(x)

    movie_id = json_data['imdbID']

    conn = psycopg2.connect("dbname=cinaeste")
    cur = conn.cursor()
    cur.execute("INSERT INTO watch_list_movies (watch_list_id, movie_id) VALUES (%s, %s)", [session['list_id'], movie_id])

    conn.commit()
    cur.close()
    conn.close()

    print(movie_id)

    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/sign_up_action', methods=['POST'])
def sign_up_action():


    return 


# LOGIN FORM AND ACTION
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_form_action', methods=['POST'])
def login_form_action():
    email = request.form['email']
    password = request.form['password']

    return redirect('/')




@app.route('/logout')
def logout():
    response = redirect('/')
    session.pop('user_id', None)
    session.pop('list_id', None)
    return response

@app.route('/profile')
def profile():

    # FOR TESTING
    session['user_id'] = 1

    conn = psycopg2.connect("dbname=cinaeste")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    id, f_name, l_name, bio, avatar = cur.fetchone()

    cur2 = conn.cursor()
    cur2.execute('SELECT * FROM fave_movies WHERE user_id =%s', [session['user_id']])
    fave_movies = cur2.fetchall()

    cur3 = conn.cursor()
    cur3.execute('SELECT * FROM watch_list WHERE user_id =%s', [session['user_id']])
    watch_list = cur3.fetchall()

    print(fave_movies)

    return render_template('profile.html', f_name=f_name, l_name=l_name, bio=bio, avatar=avatar, fave_movies=fave_movies, watch_list=watch_list)

app.run(debug=True)









