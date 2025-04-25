from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db.init_app(app)
Bootstrap5(app)


class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

# with app.app_context():
#     db.create_all()



# with app.app_context():
#     add_movie = Movie(**movie)
#     db.session.add(add_movie)
#     db.session.commit()

@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.id))
    movies = result.scalars()
    return render_template("index.html", movies=movies)


class RateMovieForm(FlaskForm):
    # Add render_kw{} to set placholders dynamically
    rating = StringField("Your rating out of 10", render_kw={})
    review = StringField("Your rating", render_kw={})
    submit = SubmitField("Done")

class AddMovieForm(FlaskForm):
    add = StringField("Movie Title")
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


@app.route("/add")
def add():
    added_movie = AddMovieForm()

    return render_template('add.html', form=added_movie)

if __name__ == '__main__':
    app.run(debug=True)
