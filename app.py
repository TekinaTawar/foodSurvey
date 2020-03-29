from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date


import csvdata

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

glob_mail = ''


class Survey(db.Model):
    # from app import db
    # db.create_all()

    # id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)

    beveragesL = db.Column(db.String(5000), nullable=True)
    snacksL = db.Column(db.String(5000), nullable=True)
    main_coursesL = db.Column(db.String(5000), nullable=True)
    othersL = db.Column(db.String(5000), nullable=True)

    beveragesXL = db.Column(db.String(5000), nullable=True)
    snacksXL = db.Column(db.String(5000), nullable=True)
    main_coursesXL = db.Column(db.String(5000), nullable=True)
    othersXL = db.Column(db.String(5000), nullable=True)

    beveragesXXL = db.Column(db.String(5000), nullable=True)
    snacksXXL = db.Column(db.String(5000), nullable=True)
    main_coursesXXL = db.Column(db.String(5000), nullable=True)
    othersXXL = db.Column(db.String(5000), nullable=True)

    form_fill_date = db.Column(db.Date, default=date.today)

    def __repr__(self):
        return '<Task %r>' % self.email


@app.route('/', methods=['POST', 'GET'])
def index():
    global user_name, user_email, user_gender, user_age, user_city, user_state

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        user_name = first_name + " " + last_name

        user_email = request.form['email']
        user_gender = request.form['gender']
        user_age = request.form['age']
        user_city = request.form['city']
        user_state = request.form['state']

        return redirect('/page1')
    else:
        return render_template('index.html')


@app.route('/page1', methods=['POST', 'GET'])
def page1():
    global user_beveragesL, user_snacksL, user_main_coursesL, user_othersL

    if request.method == 'POST':
        user_beveragesL = list(set(csvdata.Beverages) - set(request.form.getlist('beverages')))
        user_snacksL = list(set(csvdata.Snacks) - set(request.form.getlist('snacks')))
        user_main_coursesL = list(set(csvdata.MainCourses) - set(request.form.getlist('main_courses')))
        user_othersL = list(set(csvdata.Others) - set(request.form.getlist('others')))

        return redirect('/page2')
    else:
        return render_template('page1.html', beverages=csvdata.Beverages, snacks=csvdata.Snacks, main_courses=csvdata.MainCourses, others=csvdata.Others)


@app.route('/page2', methods=['POST', 'GET'])
def page2():
    global user_beveragesXL, user_snacksXL, user_main_coursesXL, user_othersXL

    if request.method == 'POST':
        user_beveragesXL = list(set(user_beveragesL) - set(request.form.getlist('beverages')))
        user_snacksXL = list(set(user_snacksL) - set(request.form.getlist('snacks')))
        user_main_coursesXL = list(set(user_main_coursesL) - set(request.form.getlist('main_courses')))
        user_othersXL = list(set(user_othersL) - set(request.form.getlist('others')))

        return redirect('/page3')
    else:
        return render_template('page2.html', beverages=user_beveragesL, snacks=user_snacksL, main_courses=user_main_coursesL, others=user_othersL)


@app.route('/page3', methods=['POST', 'GET'])
def page3():
    # global user_beveragesXXL, user_snacksXXL, user_main_coursesXXL, user_othersXXL
    # global user_name, user_email, user_gender, user_age, user_city, user_state
    # global user_beveragesL, user_snacksL, user_main_coursesL, user_othersL
    # global user_beveragesXL, user_snacksXL, user_main_coursesXL, user_othersXL

    if request.method == 'POST':
        user_beveragesXXL = request.form.getlist('beverages')
        user_snacksXXL = request.form.getlist('snacks')
        user_main_coursesXXL = request.form.getlist('main_courses')
        user_othersXXL = request.form.getlist('others')

        new_user = Survey(email=user_email, name=user_name, gender=user_gender, age=user_age, state=user_state, city=user_city, beveragesL=str(
            user_beveragesL), snacksL=str(user_snacksL), main_coursesL=str(user_main_coursesL), othersL=str(user_othersL), beveragesXL=str(
            user_beveragesXL), snacksXL=str(user_snacksXL), main_coursesXL=str(user_main_coursesXL), othersXL=str(user_othersXL), beveragesXXL=str(
            user_beveragesXXL), snacksXXL=str(user_snacksXXL), main_coursesXXL=str(user_main_coursesXXL), othersXXL=str(user_othersXXL),)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/success')
        except:
            return "There was some error please try again"

    else:
        return render_template('page3.html', beverages=user_beveragesXL, snacks=user_snacksXL, main_courses=user_main_coursesXL, others=user_othersXL)


@app.route('/success')
def success():
    return 'THANKS FOR SUBMITTING DATA'


if __name__ == "__main__":
    app.run(debug=True)
