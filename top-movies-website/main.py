from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db.init_app(app)
Bootstrap5(app)

MOVIE_API_KEY = os.getenv("TMDB_API_KEY")
MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_API_URL = "https://api.themoviedb.org/3/movie/{movie_id}"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

headers = {
    "accept": "application/json",
    "Authorization": MOVIE_API_KEY
}

class Movie(db.Model):
    # nullable=True is redundant because default behaviour is True but is included because of debugging issues
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    description: Mapped[str] = mapped_column(String(250), nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=True)

# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating.desc()))
    movies = result.scalars().all() #Convert to a list

    # Set the rank according to rating - highest rating first
    for i in range(len(movies)):
        movies[i].ranking = i + 1
    db.session.commit()

    return render_template("index.html", movies=movies)


class RateMovieForm(FlaskForm):
    # Add render_kw{} to set placholders dynamically
    rating = StringField("Your rating out of 10", render_kw={})
    review = StringField("Your review", render_kw={})
    submit = SubmitField("Done")

class AddMovieForm(FlaskForm):
    add = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add movie")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    movie_to_update = db.get_or_404(Movie, id)
    # Instantiate without pre-populating
    edit_form = RateMovieForm()

    # Pre-populate the form
    # edit_form = RateMovieForm(obj=movie_to_update)

    if edit_form.validate_on_submit():
        movie_to_update.rating = float(edit_form.rating.data)
        movie_to_update.review = edit_form.review.data
        db.session.commit()
        return redirect(url_for('home'))

    elif request.method == "GET":
        # Set placeholders for GET requests
        edit_form.rating.render_kw["placeholder"] = movie_to_update.rating
        edit_form.review.render_kw["placeholder"] = movie_to_update.review

    return render_template('edit.html', movie=movie_to_update, form=edit_form)

@app.route("/delete")
def delete():
    movie_id = request.args.get('id')

    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()

    return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
def add():
    added_movie = AddMovieForm()

    if added_movie.validate_on_submit():
        movie_title = added_movie.add.data
        response = requests.get(MOVIE_DB_SEARCH_URL, headers=headers, params={"query": movie_title})
        data = response.json()['results']
        return render_template('select.html', options=data)

    return render_template('add.html', form=added_movie)


@app.route("/find")
def get_movie():
    movie_api_id = request.args.get('id')

    if movie_api_id:
        movie_api_url = f"https://api.themoviedb.org/3/movie/{movie_api_id}"
        response = requests.get(movie_api_url, headers=headers)
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"]
        )
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for('edit', id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
