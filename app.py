from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import date

# this is a random commen#

# life is eazy
import csvdata

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Survey(db.Model):
    # from app import db
    # db.create_all()
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    beverages_selected = db.Column(db.String(5000), nullable=True)
    snacks_selected = db.Column(db.String(5000), nullable=True)
    main_courses_selected = db.Column(db.String(5000), nullable=True)
    others_selected = db.Column(db.String(5000), nullable=True)
    form_fill_date = db.Column(db.Date, default=date.today)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    global beverages, snacks
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        user_email = request.form['email']
        user_gender = request.form['gender']
        user_age = request.form['age']
        user_city = request.form['city']
        user_state = request.form['state']
        user_beverages = request.form.getlist('beverages')
        user_snacks = request.form.getlist('snacks')
        user_main_courses = request.form.getlist('main_courses')
        user_others = request.form.getlist('others')

        user_name = first_name + " " + last_name

        new_user = Survey(email=user_email, name=user_name, gender=user_gender, age=user_age, state=user_state, city=user_city, beverages_selected=str(
            user_beverages), snacks_selected=str(user_snacks), main_courses_selected=str(user_main_courses), others_selected=str(user_others),)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/page2/')
        except:
            return 'There was an issue adding your task'
    else:
        return render_template('index.html', beverages=csvdata.Beverages, snacks=csvdata.Snacks, main_courses=csvdata.MainCourses, others=csvdata.Others)


@app.route('/page2/', methods=['POST', 'GET'])
def done():
    if request.method == 'POST':
        pass

    else:
        return render_template('page2.html')


if __name__ == "__main__":
    app.run(debug=True)
