# from flask import render_template, redirect, url_for, flash, request
# from flask_login import login_user, logout_user, current_user, login_required
# from app import app, db
# from app.models import User, Survey, Response
# from app.forms import RegistrationForm, LoginForm, SurveyForm, ResponseForm
# from uuid import uuid4

# @app.before_request
# def before_request():
#     db.connect()

# @app.after_request
# def after_request(response):
#     db.close()
#     return response

# @app.route("/")
# @app.route("/home")
# def home():
#     return render_template('home.html')

# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         if User.select().where(User.username == form.username.data).exists():
#             flash('Username already exists.', 'danger')
#         else:
#             User.create(
#                 username=form.username.data,
#                 email=form.email.data,
#                 password=form.password.data
#             )
#             flash('Your account has been created!', 'success')
#             return redirect(url_for('login'))
#     return render_template('register.html', form=form)

# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.get_or_none(User.email == form.email.data)
#         if user and user.password == form.password.data:
#             login_user(user)
#             flash('Login successful!', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Invalid credentials.', 'danger')
#     return render_template('login.html', form=form)

# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     flash('You have been logged out.', 'info')
#     return redirect(url_for('home'))

# @app.route("/survey/new", methods=['GET', 'POST'])
# @login_required
# def new_survey():
#     form = SurveyForm()
#     if form.validate_on_submit():
#         Survey.create(
#             title=form.title.data,
#             description=form.description.data,
#             link=str(uuid4()),  # Generate a unique link
#             user=current_user
#         )
#         flash('Survey created successfully!', 'success')
#         return redirect(url_for('surveys'))
#     return render_template('create_survey.html', form=form)

# @app.route("/surveys")
# @login_required
# def surveys():
#     user_surveys = Survey.select().where(Survey.user == current_user)
#     return render_template('surveys.html', surveys=user_surveys)

# @app.route("/survey/<link>")
# @login_required
# def survey_detail(link):
#     survey = Survey.get_or_none(Survey.link == link)
#     if survey is None:
#         flash("Survey not found.", "danger")
#         return redirect(url_for('surveys'))

#     responses = Response.select().where(Response.survey == survey)
#     return render_template("view_survey.html", survey=survey, responses=responses)

# @app.route("/survey/<link>/respond", methods=['GET', 'POST'])
# def survey_respond(link):
#     survey = Survey.get_or_none(Survey.link == link)
#     if survey is None:
#         flash("Survey not found.", "danger")
#         return redirect(url_for('home'))

#     form = ResponseForm()
#     if form.validate_on_submit():
#         Response.create(
#             content=form.response.data,
#             survey=survey
#         )
#         flash("Thank you for your response!", "success")
#         return redirect(url_for('home'))
#     return render_template("public_survey.html", survey=survey, form=form)


from flask import abort, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User, Survey, Response
from app.forms import RegistrationForm, LoginForm, SurveyForm
from uuid import uuid4
from flask import request

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.select().where(User.username == form.username.data).exists():
            flash("Username already exists.", "danger")
        else:
            User.create(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
            flash("Your account has been created!", "success")
            return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_or_none(User.email == form.email.data)
        if user and user.password == form.password.data:
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials.", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

@app.route("/survey/new", methods=["GET", "POST"])
@login_required
def new_survey():
    form = SurveyForm()
    if form.validate_on_submit():
        Survey.create(
            title=form.title.data,
            description=form.description.data,
            link=str(uuid4()),
            user=current_user,
        )
        flash("Survey created successfully!", "success")
        return redirect(url_for("surveys"))
    return render_template("create_survey.html", form=form)

@app.route("/surveys")
@login_required
def surveys():
    user_surveys = Survey.select().where(Survey.user == current_user)
    return render_template("surveys.html", surveys=user_surveys)

from app.forms import ResponseForm

@app.route("/survey/<link>", methods=["GET", "POST"])
@login_required
def survey_detail(link):
    survey = Survey.get(Survey.link == link)
    responses = Response.select().where(Response.survey == survey)
    form = ResponseForm()

    if form.validate_on_submit():
        Response.create(
            survey=survey,
            content=form.response.data,
            user=current_user
        )
        flash("Response added successfully!", "success")
        return redirect(url_for("survey_detail", link=link))

    return render_template("view_survey.html", survey=survey, responses=responses, form=form)


@app.route("/survey/<int:survey_id>")
@login_required
def view_survey(survey_id):
    survey = Survey.get_or_none(Survey.id == survey_id)
    if not survey:
        flash("Survey not found.", "danger")
        return redirect(url_for("surveys"))
    
    responses = Response.select().where(Response.survey == survey)
    return render_template("view_survey.html", survey=survey, responses=responses)



@app.route("/survey/<link>/add_response", methods=["POST"])
@login_required
def add_response(link):
    survey = Survey.get_or_none(Survey.link == link)
    if not survey:
        flash("Survey not found.", "danger")
        return redirect(url_for("surveys"))
    
    content = request.form.get("response")
    if content:
        Response.create(content=content, timestamp=datetime.now(), survey=survey)
        flash("Response added successfully!", "success")
    else:
        flash("Response cannot be empty.", "danger")
    
    return redirect(url_for("survey_detail", link=survey.link))    



