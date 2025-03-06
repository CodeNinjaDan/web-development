from flask import Flask, render_template, request
import requests
from types import SimpleNamespace
import os
import smtplib

app = Flask(__name__)

posts_dicts = requests.get("https://api.npoint.io/5b776c78600bd91b0e9a").json()
my_email = os.getenv("MY_EMAIL")
email_password = os.getenv("EMAIL_PASSWORD")

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
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(my_email, email_password)
        connection.sendmail(my_email, my_email, email_message)

if __name__ == "__main__":
    app.run(debug=True)