from flask import Flask

app = Flask(__name__)

# Line 6 defines the content of the home page
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# This tells Flask that you're not running code from an imported module
# It also makes it easier to run flask apps since you don't have to use export FLASK_APP=...
# to run flask apps and ctrl c end the apps

if __name__ == "__main__":
    app.run(debug=True)
