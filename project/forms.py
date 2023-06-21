from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, widgets, SelectMultipleField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from project.models import UserModel

class RegisterForm(FlaskForm):
    def validate_username(self,username_to_check):
        user = UserModel.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')
    
    def validate_email_address(self,email_address_to_check):
        email_address = UserModel.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different Email Address')

    username = StringField(label='User Name:',validators=[Length(min=2,max=30),DataRequired()])
    name = StringField(label='Name:',validators=[Length(min=2,max=50),DataRequired()])
    phone_no = StringField(label='Phone Number:',validators=[Length(min=10,max=12),DataRequired()])
    email_address = StringField(label='Email Address:',validators=[Email(),DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:',validators=[DataRequired()])
    password = PasswordField(label='Password:',validators=[DataRequired()])
    submit = SubmitField(label='Sign In')
    

class UpdateProfileForm(FlaskForm):
    name = StringField(label='Name:',validators=[Length(min=2,max=50)])
    avatar = StringField(label='avatar:')
    about_me = StringField(label='About me:',validators=[Length(max=500)])
    li_link = StringField(label='LinkedIn Link:',validators=[Length(min=0,max=50)])
    submit = SubmitField(label='Update Profile')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AddCourseForm(FlaskForm):
    name = StringField(label='Course Name:',validators=[Length(min=2,max=50),DataRequired()])
    Author = StringField(label='Author Name:', validators=[Length(min=2,max=50),DataRequired()])
    description = StringField(label='Course Description:', validators=[Length(min=2,max=1024),DataRequired()])
    what_you_will_learn = MultiCheckboxField(label='What you will learn:')

    # comments = db.relationship("CommentModel", secondary="comment")
    tutorials = StringField(label='Tutorial ID:',validators=[Length(min=2,max=50),DataRequired()])
    submit = SubmitField(label='Add Course')



class RegisterCourseForm(FlaskForm):
    pass


class UnRegisterCourseForm(FlaskForm):
    pass