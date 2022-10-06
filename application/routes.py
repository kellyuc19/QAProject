from application import app, db
from application.models import Videos, Users, Topics, Module 
from application.forms import AddVideoForm, UpdateVideoForm, DeleteVideoForm, RegistrationForm, LoginForm
from flask import Flask, request, render_template, url_for, redirect
from flask_login import login_user, current_user, logout_user, login_required
from application import bcrypt

@app.route('/add', methods=['GET', 'POST'])
def add():
    message = ""
    add_video_form = AddVideoForm()
    if request.method == 'POST':
        if add_video_form.validate_on_submit():
            new_video = Videos(video_link=add_video_form.video_link.data.lower())
            new_date = Videos(video_date=add_video_form.video_date.data())
            db.session.add(new_video)
            db.session.add(new_date)
            db.session.commit()
            message = f"{new_video.video_link} has been successfully added to the database"
        else:
            message = "Video link invalid. Please try again"

    return render_template('add_video.html', form=add_video_form, message=message)


@app.route('/')
@app.route('/home')
@app.route('/view_all_videos_as_articles')
def view_all_videos_as_articles():
    all_videos = Videos.query.all()
    # videos_string = ""
    # for video in all_videos:
    #     videos_string += "<br>"+ video.name
    return render_template('view_all_videos_as_articles.html', videos=all_videos)


@app.route('/display_videos_as_table')
def display_videos_as_table():
    all_videos = Videos.query.all()
    # videos_string = ""
    # for video in all_videos:
    #     videos_string += "<br>"+ video.name
    return render_template('display_videos_as_table.html', videos=all_videos)

@app.route('/count')
def count():
    number_of_videos = Videos.query.count()
    message = f"There are currently {number_of_videos} videos in the database"
    return render_template('count.html', message=message)

@app.route('/update', methods=['GET', 'POST'])
def update():
    message = ""
    update_video_form = UpdateVideoForm()
    if request.method == 'POST':
        if update_video_form.validate_on_submit():
            video = Videos.query.filter_by(video_link=update_video_form.oldname.data.lower()).first()
            if not video is None:
                video.video_link = update_video_form.newname.data.lower()
                db.session.commit()
                message = f"{update_video_form.oldname.data.lower()} has been altered to {video.video_link}"
            else:
                message = "Video could not be found. Please enter a valid video."
        else:
            message = "Video link invalid. Please try again"

    return render_template('update_video.html', form=update_video_form, message=message)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    message = ""
    delete_video_form = DeleteVideoForm()
    if request.method == 'POST':
        if delete_video_form.validate_on_submit():
            video = Videos.query.filter_by(video_link=delete_video_form.video_link.data.lower()).first()
            if not video is None:
                db.session.delete(video)
                db.session.commit()
                message = f"{video.video_link} has been successfully removed from the database"
            else:
                message = "Video could not be found. Please enter a valid video."
        else:
            message = "Video name invalid. Please try again"

    return render_template('delete_video.html', form=delete_video_form, message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('view_all_videos_as_articles'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)
        user = Users(
            #userid=form.userid.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            city=form.city.data,
            tel=form.tel.data,
            cohort=form.cohort.data,
            pathway=form.pathway.data,
            email=form.email.data,
            password=hash_pw
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('view_all_videos_as_articles'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('view_all_videos_as_articles'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
        # if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('view_all_videos_as_articles')
    return render_template('login.html', title='Login', form=form)





