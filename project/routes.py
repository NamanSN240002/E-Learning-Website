from project import app
from flask import render_template, redirect, url_for, flash, request
from project.models import UserModel, CourseModel, CommentModel
from project.forms import  RegisterForm, LoginForm, UpdateProfileForm, AddCourseForm
from project import db, allowed_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os

with app.app_context():
        # db.drop_all()
        db.create_all()

@app.route('/')
@app.route('/home')
def home_page():
        courses = CourseModel.query.all()
        return render_template('home.html',courses=courses)

@app.route('/about')
def about_page():
        return render_template('about.html')

@app.route('/searchResult', methods=['POST'])
def search_result():
        search = request.form['search']
        check = '%'+search+'%'
        courses = CourseModel.query.filter(CourseModel.what_you_will_learn.ilike(check))
        return render_template('search.html',searchRes=search,courses=courses)

@app.route('/profile')
@login_required
def profile_page():
        return render_template('profile.html')

@app.route('/update_profile',methods=['POST','GET'])
@login_required
def update_profile():
        form = UpdateProfileForm(obj=current_user)
        if form.validate_on_submit():
                file = request.files['Picture']
                filename = None
                if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                form.populate_obj(current_user)
                if filename!=None :
                        current_user.avatar = str(filename) 
                db.session.add(current_user)
                db.session.commit()
                return redirect(url_for('profile_page'))
        if form.errors!={}:
                for err_msg in form.errors.values():
                        flash(f'There was an error with updating the user: {err_msg}', category='danger')
        return render_template('updateProfile.html',form=form)

@app.route('/course/<courseid>')
@login_required
def course_page(courseid):
        course = CourseModel.query.filter_by(id=courseid).first()
        comments = CommentModel.query.filter_by(course_id=courseid)        
        return render_template('course.html',course=course,comments=comments)

@app.route('/addComment',methods=['GET','POST'])
@login_required
def addComment():
        messageContent = request.form.get("messageContent")
        courseId = request.form.get("courseId")
        new_comment = CommentModel(
                student_id = current_user.id,
                username = current_user.username,
                course_id =courseId,
                messageContent = messageContent
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect('/course/'+str(courseId))

@app.route('/addCourse',methods=['GET','POST'])
@login_required
def add_course():
        form = AddCourseForm()
        form.what_you_will_learn.choices = [('Python', 'Python'), ('Javascript', 'Javascript'), ('HTML', 'HTML'),('CSS', 'CSS'),('DSA', 'DSA'),('Machine Learning', 'Machine Learning'),('Computer Security', 'Computer Security'),('Compilers', 'Compilers')]
        if form.validate_on_submit():
                file = request.files['Picture']
                filename = None
                if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                strtemp = ''
                for s in form.what_you_will_learn.data:
                        strtemp+=s
                        strtemp+='|'
                course_to_create= CourseModel(
                                        name=form.name.data,
                                        Author=form.Author.data,
                                        owner=current_user.id,
                                        description = form.description.data,
                                        course_image=str(filename),
                                        what_you_will_learn = strtemp,
                                        tutorials=form.tutorials.data
                                        )
                db.session.add(course_to_create)
                db.session.commit()
                flash(f'Course added succesfully!', category='success')      
                return redirect(url_for('home_page'))
        if form.errors != {}:
                for err_msg in form.errors.values():
                        flash(f'There was an error with creating a user: {err_msg}', category='danger')
        return render_template('addcourse.html',form=form)

@app.route('/courseremoval')
@login_required
def remove_course_page():
        courses = CourseModel.query.filter_by(owner=current_user.id)
        return render_template('removecourse.html',courses=courses)

@app.route('/removecourse',methods=['GET','POST'])
@login_required
def remove_course():
        id_ = request.form.get('id_')
        CourseModel.query.filter_by(id=id_).delete()
        db.session.commit()
        return redirect(url_for('remove_course_page'))


@app.route('/register', methods=['GET','POST'])
def register_page():
        form = RegisterForm()
        if form.validate_on_submit():
                user_to_create = UserModel(username=form.username.data,
                                           name=form.name.data,
                                           phone_no=form.phone_no.data,
                                           email_address=form.email_address.data,
                                           password=form.password1.data
                                      )
                db.session.add(user_to_create)
                db.session.commit()
                login_user(user_to_create)
                flash(f'Account created succesfully! You are logged in as: {user_to_create.username}', category='success')      
                return redirect(url_for('home_page'))
        if form.errors != {}:
                for err_msg in form.errors.values():
                        flash(f'There was an error with creating a user: {err_msg}', category='danger')
        return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
        form = LoginForm()
        if form.validate_on_submit():
                attempted_user = UserModel.query.filter_by(username=form.username.data).first()
                if attempted_user and attempted_user.check_password_correction(
                        attempted_password=form.password.data
                ):
                        login_user(attempted_user)
                        flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
                        return redirect(url_for('home_page'))
                else:
                        flash('Username and password are not match! Please try again', category='danger')
        if form.errors != {}:
                for err_msg in form.errors.values():
                        flash(f'There was an error with logging in the user: {err_msg}', category='danger')
        return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():
        logout_user()
        flash("You have been logged out!", category='info')
        return redirect(url_for("home_page"))
