from flask import Flask, render_template
import requests
from types import SimpleNamespace

app = Flask(__name__)

posts_dicts = requests.get("https://api.npoint.io/5b776c78600bd91b0e9a").json()

#Convert dictionaries to objects with attribute access to ba able to use dot notation
posts = [SimpleNamespace(**post) for post in posts_dicts]

@app.route("/")
def home():
    return render_template("index.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)