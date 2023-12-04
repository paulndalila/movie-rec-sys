from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/your_database_name'
db = SQLAlchemy(app)


#routes
#index route
@app.route('/', methods=['GET'])
def index():
    movies = get_random_movies()
    return render_template('index.html', movies=movies)

#movie list route
@app.route('/genre')
def movie_list():
    return render_template('movie_genre.html')

#specific movie route
@app.route('/search')
def searched_movie():
    query = request.args.get('query')
    print(query)
    movies = search_movie(query)
    return render_template('movie_searched.html', movies=movies, query=query)

#popular movies route
@app.route('/popularmovies', methods=['GET'])
def popular():
    movies = get_popular_movies()
    return render_template('popular.html', movies=movies)

# user login route
@app.route('/login')
def user_login():
    return render_template('login.html')

# user registration route
@app.route('/register')
def user_register():
    return render_template('register.html')

# user recommendation form route
@app.route('/recommend')
def user_recommend():
    return render_template('recommend.html')

# Route for logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


#postgreSQL database tables
#users table
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


#Movies table
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100))
    release_year = db.Column(db.Integer)
    director = db.Column(db.String(150))
    description = db.Column(db.Text)

#Ratings table
# class Rating(db.Model):
#     __tablename__ = 'ratings'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
#     rating = db.Column(db.Float, nullable=False)
#     timestamp = db.Column(db.DateTime, nullable=False)

# # Define relationships
#     user = db.relationship('User', backref=db.backref('ratings', lazy=True))
#     movie = db.relationship('Movie', backref=db.backref('ratings', lazy=True))


#processing user form inputs
#user registration
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        # Create a new User instance
        new_user = User(username=username, email=email)

        # Add the new user to the database session
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('user_added'))

    return render_template('register.html')

@app.route('/user_added')
def user_added():
    return 'User added successfully!'

#user login
@app.route('/user_login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        session['user_id'] = user.username
        # Query the database for the user
        user = User.query.filter_by(username=username).first()

        if user and user.password_hash == password:
            # Successful login, redirect to a dashboard or profile page
            return redirect(url_for('add_movie'))
        else:
            # Authentication failed, redirect back to login page with a message
            return redirect(url_for('login_failed'))

    return render_template('login.html')

@app.route('/login_failed')
def login_failed():
    return 'Login failed. Please try again.'

#movie recommended add
@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        director = request.form['director']

        # Create a new Movie instance
        new_movie = Movie(title=title, genre=genre, director=director)
        # Add the new movie to the database session
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for('movie_added'))

    return render_template('recommend.html')

@app.route('/movie_added')
def movie_added():
    return 'Movie added successfully!'



#api fetching
#fetch popular movies
def get_popular_movies():
    url = 'https://moviesdatabase.p.rapidapi.com/titles?year=2023&page=2'

    headers = {
        "X-RapidAPI-Key": "ad6e9940ddmsh7cf7e0b2fe866d1p1f42bdjsn44776da3eb3d",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    # data = response.json()
    # print(data)
    
    if response.status_code == 200:

        movies_data = response.json().get('results', [])
        return movies_data
    else:
        return []

def search_movie(title):
    url = 'https://moviesdatabase.p.rapidapi.com/titles/search/title/'+title+'?exact=false&titleType=movie'

    headers = {
        "X-RapidAPI-Key": "ad6e9940ddmsh7cf7e0b2fe866d1p1f42bdjsn44776da3eb3d",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    # data = response.json()
    # print(data)
    
    if response.status_code == 200:

        movies_data = response.json().get('results', [])
        return movies_data
    else:
        return []

#fetch random movies
def get_random_movies():
    url = 'https://moviesdatabase.p.rapidapi.com/titles?startYear=2010&page=2'

    headers = {
        "X-RapidAPI-Key": "ad6e9940ddmsh7cf7e0b2fe866d1p1f42bdjsn44776da3eb3d",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    # data = response.json()
    # print(data)
    
    if response.status_code == 200:

        movies_data = response.json().get('results', [])
        return movies_data
    else:
        return []


if __name__ == '__main__':
    app.run(debug=True)