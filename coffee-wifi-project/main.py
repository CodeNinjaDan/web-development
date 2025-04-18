from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    location = StringField(label='Cafe Location on Maps (URL)', validators=[DataRequired(), URL(message="invalid URL")])
    open_time = StringField(label='Opening Time eg. 8AM', validators=[DataRequired()])
    close_time = StringField(label='Closing Time eg. 4PM', validators=[DataRequired()])

    coffee_rating = SelectField(label='Coffee Rating',
                                choices=[('✘', '✘'), ('☕️', '☕️'), ('☕️☕️', '☕️☕️'), ('☕️☕️☕️','☕️☕️☕️'), ('☕️☕️☕️☕️','☕️☕️☕️☕️')],
                                validators=[DataRequired()])

    wifi = SelectField(label='Wifi Strength Rating',
                                choices=[('✘', '✘'), ('💪', '💪'), ('💪💪', '💪💪'), ('💪💪💪','💪💪💪'), ('💪💪💪💪','💪💪💪💪')],
                                validators=[DataRequired()])

    power = SelectField(label='Power Socket Availability',
                        choices=[('✘', '✘'), ('🔌', '🔌'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌','🔌🔌🔌'), ('🔌🔌🔌🔌','🔌🔌🔌🔌')],
                        validators=[DataRequired()])

    submit = SubmitField(label='Submit')



@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
