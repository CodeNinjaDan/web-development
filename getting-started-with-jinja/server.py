from flask import Flask, render_template
import requests
import random
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def homepage():
    random_number = random.randint(1, 10)
    current_year = datetime.now().year
    return render_template("index.html", num=random_number, year=current_year)


@app.route("/guess/<name>", methods=["GET"])
def name_age(name):
    age_url = f"https://api.agify.io?name={name}"
    gender_url = f"https://api.genderize.io?name={name}"

    age_response = requests.get(age_url)
    gender_response = requests.get(gender_url)

    age_data = age_response.json()
    gender_data = gender_response.json()

    # age = age_data["age"]
    # gender = gender_data["gender"]

    age = age_response.json().get('age')
    gender = gender_response.json().get('gender')

    return render_template('guess.html', name=name, age=age, gender=gender)


@app.route("/blog/<num>")
def get_blog(num):
    print(num)
    blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
    response = requests.get(blog_url)
    all_posts = response.json()

    return render_template("blog.html", posts=all_posts)


if __name__ == "__main__":
    app.run(debug=True)