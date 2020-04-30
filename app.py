from flask import Flask, request, render_template
from flask import redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from jsondata import getdishes as gd


app = Flask(__name__)

# change this to dev if you are using these files locally.
ENV = 'prod'
app.config['SECRET_KEY'] = '04a3a646d40f8fc28899016312007807'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:toor@localhost/foodSurvey'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gfwqeznjqizuki:745f9be7c8779add122a2ffc9bde86565fbf809359f3fb33f382843b02403a83@ec2-18-235-20-228.compute-1.amazonaws.com:5432/d541dctpgsmsse'

# This line remove the warning of overhead during creating database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class UserData(db.Model):
    # from app import db
    # db.create_all()
    # db.drop_all()
    __tablename__ = 'user_data'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
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
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.email}, {self.name})'


@app.route('/')
def index():
    session['start_time'] = datetime.utcnow()
    return render_template('index.html')


@app.route('/form', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        if db.session.query(UserData).filter(UserData.email == request.form['email']).count() == 0:
            session['user_email'] = request.form['email']
            session['user_name'] = request.form['first_name'] + " " + request.form['last_name']
            session['user_gender'] = request.form['gender']
            session['user_age'] = request.form['age']
            session['user_city'] = request.form['city']
            session['user_state'] = request.form['state']
            session['user_food_pref'] = request.form['dietary_restriction']
            return redirect('/page1')
        else:
            return render_template('form.html', message='Survey have been already filled with this email.')
    else:
        return render_template('form.html')


@app.route('/page1', methods=['POST', 'GET'])
def page1():
    user_food_pref = session['user_food_pref']
    if request.method == 'POST':
        session['user_beveragesK'] = request.form.getlist('beverages')
        session['user_snacksK'] = request.form.getlist('snacks')
        session['user_main_coursesK'] = request.form.getlist('main_courses')
        session['user_othersK'] = request.form.getlist('others')
        return redirect('/page2')
    else:
        return render_template(
            'page1.html',
            beverages=gd("BEVERAGE", user_food_pref),
            snacks=gd("SNACK", user_food_pref),
            main_courses=gd("MAIN_COURSE", user_food_pref),
            others=gd("OTHER", user_food_pref))


@app.route('/page2', methods=['POST', 'GET'])
def page2():
    if request.method == 'POST':
        session['user_beveragesNL'] = request.form.getlist('beverages')
        session['user_snacksNL'] = request.form.getlist('snacks')
        session['user_main_coursesNL'] = request.form.getlist('main_courses')
        session['user_othersNL'] = request.form.getlist('others')

        return redirect('/page3')
    else:
        return render_template(
            'page2.html',
            beverages=session['user_beveragesK'],
            snacks=session['user_snacksK'],
            main_courses=session['user_main_coursesK'],
            others=session['user_othersK'])


@app.route('/page3', methods=['POST', 'GET'])
def page3():
    if request.method == 'POST':
        session['user_beveragesXL'] = request.form.getlist('beverages')
        session['user_snacksXL'] = request.form.getlist('snacks')
        session['user_main_coursesXL'] = request.form.getlist('main_courses')
        session['user_othersXL'] = request.form.getlist('others')
        return redirect('/suggestion')

    else:
        return render_template(
            'page3.html',
            beverages=list(set(session['user_beveragesK']) - set(session['user_beveragesNL'])),
            snacks=list(set(session['user_snacksK']) - set(session['user_snacksNL'])),
            main_courses=list(set(session['user_main_coursesK']) - set(session['user_main_coursesNL'])),
            others=list(set(session['user_othersK']) - set(session['user_othersNL'])))


@app.route('/suggestion', methods=['POST', 'GET'])
def suggestion():
    if request.method == 'POST':
        user_suggestion = request.form['suggestion']
        end_time = datetime.utcnow()

        time_taken = int((end_time - session['start_time']).seconds)

        new_user = UserData(
            email=session['user_email'],
            name=session['user_name'],
            gender=session['user_gender'],
            age=session['user_age'],
            state=session['user_state'],
            city=session['user_city'],
            food_pref=session['user_food_pref'],

            beveragesNK=list(set(gd("BEVERAGE", session['user_food_pref'])) - set(session['user_beveragesK'])),
            snacksNK=list(set(gd("SNACK", session['user_food_pref'])) - set(session['user_snacksK'])),
            main_coursesNK=list(set(gd("MAIN_COURSE", session['user_food_pref'])) - set(session['user_main_coursesK'])),
            othersNK=list(set(gd("OTHER", session['user_food_pref'])) - set(session['user_othersK'])),

            beveragesNL=str(session['user_beveragesNL']),
            snacksNL=str(session['user_snacksNL']),
            main_coursesNL=str(session['user_main_coursesNL']),
            othersNL=str(session['user_othersNL']),
            beveragesXL=str(session['user_beveragesXL']),
            snacksXL=str(session['user_snacksXL']),
            main_coursesXL=str(session['user_main_coursesXL']),
            othersXL=str(session['user_othersXL']),
            suggestion=user_suggestion,
            time_taken=time_taken)

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
# random commment.
# life is crazy.