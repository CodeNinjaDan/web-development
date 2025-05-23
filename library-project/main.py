from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
db.init_app(app)


class Books(db.Model):
    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    result = db.session.execute(db.select(Books).order_by(Books.title))
    all_books = result.scalars()
    return render_template('index.html', books=all_books)


@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = {
            "title": request.form["title"],
            "author": request.form["author"],
            "rating": request.form["rating"]
        }
        add_book = Books(**new_book)
        db.session.add(add_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html')


@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    # Fetch book by primary key
    book_to_update = db.get_or_404(Books, id)

    if request.method == "POST":
        new_rating = request.form["rating"]
        book_to_update.rating = new_rating
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('edit_rating.html', book_to_update=book_to_update)


@app.route('/delete')
def delete():
    book_id = request.args.get('id')

    book_to_delete = db.get_or_404(Books, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

