import random

from flask import Flask

app = Flask(__name__)


@app.route("/")
def homepage():
    return ('<h1 style="text-align: center">Guess a number between 0 and 9</h1>'
            '<img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdTF6N281cnI2dThkbHZwcGprM2Rka203ZXQ1dGV0OW00bzJzOGp3ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7aCSPqXE5C6T8tBC/giphy.gif">')

random_number = random.randint(0,9)

@app.route("/<int:number>")
def guess_number(number):
    if number == random_number:
        return ('<h2 style="color: green;">You guessed correct!</h2>'
                '<img src="https://media.giphy.com/media/Zw2MBuH3dMCE8/giphy.gif?cid=790b7611l26c6mr4jawzbo5v9i576v5jzn72t7w5hjo42y4n&ep=v1_gifs_search&rid=giphy.gif&ct=g">')

    elif number > random_number:
        return ('<h2 style="color: red;">Too high, guess again.</h2>'
                '<img src="https://media.giphy.com/media/2aIZfQdC2V7bBvU5t2/giphy.gif?cid=790b7611985kpgjpdebpxx3vqmjlzyjdrwua06ixj9mtzv4p&ep=v1_gifs_search&rid=giphy.gif&ct=g">')

    else:
        return ('<h2 style="color: blue;">Too low guess, guess again.</h2>'
                '<img src="https://media.giphy.com/media/ttJpHSwLGXmEEIfa3o/giphy.gif?cid=ecf05e47h7e8tg441pdzxa0y063ood3tq2iz2auw676ntqya&ep=v1_gifs_search&rid=giphy.gif&ct=g">')


if __name__ == "__main__":
    app.run(debug=True)