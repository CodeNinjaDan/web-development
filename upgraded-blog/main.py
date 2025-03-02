from flask import Flask, render_template, request
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

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        form_data = request.form
        for field in ["name", "email", "phone", "message"]:
            if field not in form_data or not form_data[field]:
                return render_template("contact.html", error="All fields are required.")
        return receive_data()

    return render_template("contact.html")

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

app.route("/form-entry", methods=["POST"])
def receive_data():
    return f"<h1>Successfully sent your message</h1>"



if __name__ == "__main__":
    app.run(debug=True)