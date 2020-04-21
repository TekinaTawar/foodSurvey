# # {% if message %}
# #     <p class ="message">{{message | safe }}</p>
# # {% endif %}


# if db.session.query(FoodSurvey).filter(FoodSurvey.email == user_email).count() == 0:
# you can pass message in render_tmeplate
#     render_template('index', message='You have already submitted feedback')
