from flask import Flask, render_template, request, redirect
import psycopg2
import requests
import json
# import bcrypt

app = Flask(__name__)

user_id = 1

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/search_results', methods=['GET', 'POST'])
def search_results():

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
    cur.execute("INSERT INTO fave_movies (user_id, movie_id, movie_title, movie_poster) VALUES (%s, %s, %s, %s)", [user_id, imdbID_data, title, poster])



    conn.commit()
    cur.close()
    conn.close()

    # change db movie_name to fave_movie_id 

    # ISSUE - HOW TO PASS AN OBJECT AND NOT A STRING

    return redirect('/')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register-action', methods=['POST'])
def register_action():
    return 

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/profile')
def profile():
    conn = psycopg2.connect("dbname=cinaeste")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    id, f_name, l_name, bio, avatar = cur.fetchone()

    cur2 = conn.cursor()
    cur2.execute('SELECT * FROM fave_movies WHERE user_id =%s', [user_id])
    fave_movies = cur2.fetchall()

    print(fave_movies)

    return render_template('profile.html', f_name=f_name, l_name=l_name, bio=bio, avatar=avatar, fave_movies=fave_movies)

app.run(debug=True)









