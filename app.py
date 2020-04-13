from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from jsondata import getdishes as gd


app = Flask(__name__)

ENV = 'prod'


if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:toor@localhost/test'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:foodforu@survey.cugkgprl9fae.us-east-1.rds.amazonaws.com:5432/survey'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Survey(db.Model):
    # from app import db
    # db.create_all()

    email = db.Column(db.String(200), nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    food_pref = db.Column(db.String(20), nullable=False)

    beveragesNK = db.Column(db.String(5000), nullable=True)
    snacksNK = db.Column(db.String(5000), nullable=True)
    main_coursesNK = db.Column(db.String(5000), nullable=True)
    othersNK = db.Column(db.String(5000), nullable=True)

    beveragesNL = db.Column(db.String(5000), nullable=True)
    snacksNL = db.Column(db.String(5000), nullable=True)
    main_coursesNL = db.Column(db.String(5000), nullable=True)
    othersNL = db.Column(db.String(5000), nullable=True)

    beveragesXL = db.Column(db.String(5000), nullable=True)
    snacksXL = db.Column(db.String(5000), nullable=True)
    main_coursesXL = db.Column(db.String(5000), nullable=True)
    othersXL = db.Column(db.String(5000), nullable=True)

    suggestion = db.Column(db.String(10000), nullable=True)

    time_taken = db.Column(db.Integer, nullable=False)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.email


@app.route('/')
def index():
    global start_time
    start_time = datetime.utcnow()
    return render_template('index.html')


@app.route('/form', methods=['POST', 'GET'])
def form():
    global user_name, user_email, user_gender, user_age, user_city, user_state, user_food_pref

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        user_name = first_name + " " + last_name

        user_email = request.form['email']
        user_gender = request.form['gender']
        user_age = request.form['age']
        user_city = request.form['city']
        user_state = request.form['state']
        user_food_pref = request.form['dietary_restriction']

        return redirect('/page1')
    else:
        return render_template('form.html')


@app.route('/page1', methods=['POST', 'GET'])
def page1():
    global user_beveragesNK, user_snacksNK, user_main_coursesNK, user_othersNK
    global user_beveragesK, user_snacksK, user_main_coursesK, user_othersK

    user_beveragesK = request.form.getlist('beverages')
    user_snacksK = request.form.getlist('snacks')
    user_main_coursesK = request.form.getlist('main_courses')
    user_othersK = request.form.getlist('others')

    if request.method == 'POST':
        user_beveragesNK = list(set(gd("BEVERAGE", user_food_pref)) - set(user_beveragesK))
        user_snacksNK = list(set(gd("SNACK", user_food_pref)) - set(user_snacksK))
        user_main_coursesNK = list(set(gd("MAIN_COURSE", user_food_pref)) - set(user_main_coursesK))
        user_othersNK = list(set(gd("OTHER", user_food_pref)) - set(user_othersK))

        return redirect('/page2')
    else:
        return render_template('page1.html', beverages=gd("BEVERAGE", user_food_pref),
                               snacks=gd("SNACK", user_food_pref),
                               main_courses=gd("MAIN_COURSE", user_food_pref),
                               others=gd("OTHER", user_food_pref))


@app.route('/page2', methods=['POST', 'GET'])
def page2():
    global user_beveragesNL, user_snacksNL, user_main_coursesNL, user_othersNL

    if request.method == 'POST':
        user_beveragesNL = request.form.getlist('beverages')
        user_snacksNL = request.form.getlist('snacks')
        user_main_coursesNL = request.form.getlist('main_courses')
        user_othersNL = request.form.getlist('others')

        return redirect('/page3')
    else:
        return render_template('page2.html', beverages=user_beveragesK, snacks=user_snacksK, main_courses=user_main_coursesK, others=user_othersK)


@app.route('/page3', methods=['POST', 'GET'])
def page3():
    global user_beveragesXL, user_snacksXL, user_main_coursesXL, user_othersXL

    if request.method == 'POST':
        user_beveragesXL = request.form.getlist('beverages')
        user_snacksXL = request.form.getlist('snacks')
        user_main_coursesXL = request.form.getlist('main_courses')
        user_othersXL = request.form.getlist('others')
        return redirect('/suggestion')

    else:
        user_beveragesM = list(set(user_beveragesK) - set(user_beveragesNL))
        user_snacksM = list(set(user_snacksK) - set(user_snacksNL))
        user_main_coursesM = list(set(user_main_coursesK) - set(user_main_coursesNL))
        user_othersM = list(set(user_othersK) - set(user_othersNL))
        return render_template('page3.html', beverages=user_beveragesM, snacks=user_snacksM, main_courses=user_main_coursesM, others=user_othersM)


@app.route('/suggestion', methods=['POST', 'GET'])
def suggestion():
    if request.method == 'POST':
        user_suggestion = request.form['suggestion']
        end_time = datetime.utcnow()

        time_taken = int((end_time - start_time).seconds)

        new_user = Survey(email=user_email, name=user_name, gender=user_gender, age=user_age, state=user_state, city=user_city, food_pref=user_food_pref, beveragesNK=str(
            user_beveragesNK), snacksNK=str(user_snacksNK), main_coursesNK=str(user_main_coursesNK), othersNK=str(user_othersNK), beveragesNL=str(
            user_beveragesNL), snacksNL=str(user_snacksNL), main_coursesNL=str(user_main_coursesNL), othersNL=str(user_othersNL), beveragesXL=str(
            user_beveragesXL), snacksXL=str(user_snacksXL), main_coursesXL=str(user_main_coursesXL), othersXL=str(user_othersXL), suggestion=user_suggestion, time_taken=time_taken)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/success')
        except:
            return render_template('error.html')

    else:
        return render_template('suggestion.html')


@app.route('/success')
def success():
    return render_template('thank.html')


if __name__ == "__main__":
    app.run(debug=True)
