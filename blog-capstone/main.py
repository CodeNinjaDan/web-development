from flask import Flask, render_template
import requests


app = Flask(__name__)

@app.route('/')
def home():
    blogs_response = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
    all_blogs = blogs_response.json()

    return render_template("index.html", posts=all_blogs)


@app.route('/posts/<num>')
def get_blog(num):
    if num == 1:

    return render_template("post.html", num=num)


if __name__ == "__main__":
    app.run(debug=True)
