import os
from flask import Flask, flash, render_template, request, redirect, url_for, session
from extentions import db
from forms import signup_form, signin_form, change_password_form, add_new_user, edit_user_form, add_course_from, edit_course_form, add_episode_form, edit_episode_form
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models import user, course, episode, register

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'ebit1371'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MADIFICATION'] = False
db.init_app(app)



LoginManager = LoginManager(app)
LoginManager.login_view = 'login'

# return user info
@LoginManager.user_loader
def user_loder(user_id):
    return user.query.get(user_id)

@app.route('/')
def Main():
    all_course = course.query.all()
    return render_template('home.html', Courses = all_course)

# Sign UP 
@app.route('/signup', methods=['GET','POST'])
def signup():
    form = signup_form()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            # check user befor is exists
            query = user.query.filter_by(email = email).first()
            if query:
                flash('Error: User is Exists', 'danger')
                return redirect(url_for('signup'))
            # insert info to database
            new_user = user(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Sign up Successfully', 'success')
    return render_template('signup.html', form = form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = signin_form()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form.get('email')
            password = request.form.get('password')
            #next_query_param = request.form.get('next')
            query = user.query.filter_by(email = email).first()
            if query:
                #if check_password_hash(query.password, password):
                if query.password == password:
                    login_user(query)
                    return redirect( url_for('panel'))
                else:
                    flash('password in incorrect', 'danger')
                    return redirect(url_for('login'))
            else:
                flash(' user not found ', 'warning')
                return redirect(url_for('login'))
    return render_template('login.html', form = form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/panel')
#user must login to access this page
@login_required
def panel():
    return render_template('panel.html')

@app.route('/change_password', methods =['GET','POST'])
@login_required
def change_password():
    form = change_password_form()
    if request.method == 'POST':
        if form.validate_on_submit():
            old_password = request.form.get('old_password')
            user_info = db.session.query(user).filter_by(email = current_user.email).one()
            #if not check_password_hash(user_info.password, old_password):
            if user_info.password != old_password:
                flash('Error in old password Field, Password is incurrect', 'danger')
                return redirect(url_for('change_password'))
            #update password
            new_password = request.form.get('new_password')
            #user_info.password = generate_password_hash('new_password')
            user_info.password = new_password
            db.session.add(user_info)
            db.session.commit()
            flash('password Update Successfully', 'success')
            return redirect(url_for('change_password'))
    return render_template('panel_change_password.html', form = form)

@app.route('/edit_profile', methods =['GET','POST'])
@login_required
def edit_profile():
    form = edit_user_form()
    user_info = db.session.query(user).filter_by(email = current_user.email).one()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form.get('name')
            email = request.form.get('email')
            user_info.name = name
            user_info.email = email
            db.session.add(user_info)
            db.session.commit()
            flash('Profile Update Successfully', 'success')
            return redirect(url_for('edit_profile'))
    return render_template('panel_edit_profile.html', form = form, user = user_info)

#admin
@app.route('/admin_panel')
def admin_panel():
    return render_template('admin_panel.html')

@app.route('/user_list', methods = ['GET', 'POST'])
def user_list():
    user_list_info = user.query.all()
    if request.method == 'POST':
        db.session.query(user).filter_by(id = request.args.get('id')).delete()
        db.session.commit()
        return redirect(url_for('user_list'))
    return render_template('admin_list_user.html', users = user_list_info)

@app.route('/add_user', methods = ['GET', 'POST'])
def add_user():
    form = add_new_user()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            # check user befor is exists
            query = user.query.filter_by(email = email).first()
            if query:
                flash('Error: User is Exists', 'danger')
                return redirect(url_for('add_user'))
            # insert info to database
            new_user = user(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Sign up Successfully', 'success')
    return render_template('admin_add_user.html',form = form)

@app.route('/edit_user', methods = ['GET', 'POST'])
def edit_user():
    form = edit_user_form()
    user_info = db.session.query(user).filter_by(id = request.args.get('id')).one()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form.get('name')
            email = request.form.get('email')
            user_info.name = name
            user_info.email = email
            db.session.add(user_info)
            db.session.commit()
            return redirect(url_for('user_list'))
    return render_template('admin_edit_user.html', user = user_info, form = form)

@app.route('/add_course', methods = ['GET', 'POST'])
def add_course():
    form = add_course_from()
    if request.method == 'POST':
        if form.validate_on_submit() and 'pic' in request.files:
            title = request.form.get('title')
            content = request.form.get('content')
            price = request.form.get('price')

            if request.files['pic'].filename != '':
                image = request.files['pic']
                filename = image.filename
                filesecure = secure_filename(filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filesecure))
                image = f'/uploads/{filename}'
            else:
                image = '/uploads/default.jpg'

            new_course = course(title = title, content = content,  price = price, image = image )
            db.session.add(new_course)
            db.session.commit()
            flash('corse created successfully', 'success')
            return redirect(url_for('add_course'))
    return render_template('admin_add_course.html', form = form)

@app.route('/course_list', methods = ['GET', 'POST'])
def course_list():
    course_list_info = course.query.all()
    if request.method == 'POST':
        db.session.query(course).filter_by(id = request.args.get('id')).delete()
        db.session.commit()
        return redirect(url_for('course_list'))
    return render_template('admin_list_course.html', courses = course_list_info)

@app.route('/edit_course', methods = ['GET', 'POST'])
def edit_course():
    form = edit_course_form()
    course_info = db.session.query(course).filter_by(id = request.args.get('id')).one()
    if request.method == 'POST':
        if form.validate_on_submit():
            title = request.form.get('title')
            content = request.form.get('content')
            price = request.form.get('price')
            if request.files['pic'].filename != '':
                image = request.files['pic']
                filename = image.filename
                filesecure = secure_filename(filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filesecure))
                image = f'/uploads/{filename}'
            else:
                image = course_info.image

            course_info.title = title
            course_info.content = content
            course_info.price = price
            course_info.image = image
            db.session.add(course_info)
            db.session.commit()
            return redirect(url_for('course_list'))
    return render_template('admin_edit_course.html', course = course_info, form = form)

@app.route('/single_page')
def single_page():
    course_info = db.session.query(course).filter_by(id = request.args.get('id')).one()
    episodes = episode.query.filter_by(course_id = course_info.id).all()
    return render_template('single_page.html', course = course_info, episodes = episodes)

@app.route('/add_episode', methods=['GET', 'POST'])
def add_episode():
    form = add_episode_form()
    course_list_info = course.query.all()
    if request.method == 'POST':
        if form.validate_on_submit():
            title = request.form.get('title')
            content = request.form.get('content')
            number = request.form.get('number')
            course_id = request.form.get('course_id')

            new_episode = episode(title = title, content = content, number = number, course_id = course_id)
            db.session.add(new_episode)
            db.session.commit()
            flash('Episode created successfully', 'success')
            return redirect(url_for('add_episode'))
    return render_template('admin_add_episode.html', form = form, courses = course_list_info)

@app.route('/episode_list', methods = ['GET', 'POST'])
def episode_list():
    episode_list_info = episode.query.all()
    if request.method == 'POST':
        db.session.query(episode).filter_by(id = request.args.get('id')).delete()
        db.session.commit()
        return redirect(url_for('episode_list'))
    return render_template('admin_list_episode.html', episodes = episode_list_info)

@app.route('/edit_episode', methods = ['GET', 'POST'])
def edit_episode():
    form = edit_episode_form()
    course_list_info = course.query.all()
    episode_info = db.session.query(episode).filter_by(id = request.args.get('id')).one()
    if request.method == 'POST':
        if form.validate_on_submit():
            title = request.form.get('title')
            content = request.form.get('content')
            number = request.form.get('number')
            course_id = request.form.get('course_id')
            episode_info.title = title
            episode_info.content = content
            episode_info.number = number
            episode_info.course_id = course_id
            db.session.add(episode_info)
            db.session.commit()
            return redirect(url_for('episode_list'))
    return render_template('admin_edit_episode.html', episode = episode_info, form = form, courses = course_list_info)

@app.route('/register_add', methods = ['GET', 'POST'])
@login_required
def register_add():
    course_id = request.args.get('id')
    user_id = current_user.id 
    check_user_id = register.query.filter_by(user_id = user_id).first()
    if check_user_id:
        check_course_id = register.query.filter_by(course_id = course_id).first()
        if check_course_id:
            flash('You befor register in this course', 'warning')
            return single_page()
    new_register = register(user_id = user_id, course_id = course_id)
    db.session.add(new_register)
    db.session.commit()
    flash('register in this course is successfully', 'success')
    return single_page()

@app.route('/register_list', methods = ['GET', 'POST'])
def register_list():
    register_list_info = db.session.query(register).filter_by(user_id = current_user.id).all()
    if request.method == 'POST':
        db.session.query(register).filter_by(id = request.args.get('id')).delete()
        db.session.commit()
        return redirect(url_for('register_list'))
    return render_template('panel_register.html', courses = register_list_info)

@app.before_request
def creat_database():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)