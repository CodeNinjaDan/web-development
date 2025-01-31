from flask import Flask

app = Flask(__name__)

def make_bold(function):
    def wrapper():
        return "<b>" + function() + "</b>"
    return wrapper

def make_emphasis(function):
    def wrapper():
        return "<em>" + function() + "</em>"
    return wrapper

def make_underlined(function):
    def wrapper():
        return "<u>" + function() + "</u>"
    return wrapper

# Content of the home page:
@app.route("/")
def hello_world():
    return ('<h1 style="text-align: center">Hello, World!</h1>'
            '<p><h2>I like this car</h2></p>'
            '<img src="https://imgs.search.brave.com/QvMgZuOTozi_D3Xx7CP04bXXM6efuoZSlQwu04LvjKI/rs:fit:500:0:0:0/g:ce/aHR0cHM6Ly93d3cu/Z29vZHdvb2QuY29t/L2dsb2JhbGFzc2V0/cy8ucm9hZC0tcmFj/aW5nL2YxLzIwMjQv/LS0tY2FyLWxhdW5j/aGVzLWFuZC1saXZl/cmllcy9mZXJyYXJp/L2ZlcnJhcmktcmV2/ZWFscy1pdHMtMjAy/NC1mMS1jYXItMDIu/anBnP3J4eT0wLjUs/MC41JndpZHRoPTY0/MCZoZWlnaHQ9MzYw">')

@app.route("/bye")
def bye():
    return "Bye!"

# Create a variable
@app.route("/username/<name>/1")
def greet(name):
    return f'<h1 style="text-align: center">Hello there {name}</h1>'

# Variable as a Path
@app.route("/username/<path:test>")
@make_bold
def as_path(test):
    return f"This is the path {test}"

# Multiple Variables
@app.route("/test/<name>/<int:number>")
@make_emphasis
def years(name, number):
    return f"Hello there {name}, you are {number} years old!"



# This tells Flask that you're not running code from an imported module
# It also makes it easier to run flask apps since you don't have to use export FLASK_APP=...
# to run flask apps and ctrl c end the apps

if __name__ == "__main__":
    # Set debug mode to True to allow auto-refresh when you make changes
    app.run(debug=True)
