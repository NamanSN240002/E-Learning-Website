from project import db, bcrypt,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


class UserModel(db.Model, UserMixin):
        __tablename__ = "user"

        id = db.Column(db.Integer(),primary_key=True)
        username = db.Column(db.String(length=30),nullable=False,unique=True)
        name = db.Column(db.String(length=30),nullable=False,unique=True)
        email_address = db.Column(db.String(length=50),nullable = False, unique=True)
        phone_no = db.Column(db.String(length=50),nullable = False, unique=True)
        password_hash = db.Column(db.String(length=60),nullable=False)
        avatar = db.Column(db.Text(), nullable=True)
        about_me = db.Column(db.String(1000), nullable=True)
        li_link = db.Column(db.Text(), nullable=True)

        @property
        def password(self):
                return self.password
        
        @password.setter
        def password(self,plain_text_password):
                self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

        def check_password_correction(self,attempted_password):
                return bcrypt.check_password_hash(self.password_hash,attempted_password)


class CourseModel(db.Model):
        __tablename__ = "course"

        id = db.Column(db.Integer(),primary_key=True)
        name = db.Column(db.String(length=30),nullable=False,unique=True)
        Author = db.Column(db.String(), nullable=False)
        description = db.Column(db.String(length=1024),nullable=False,unique=False)
        owner = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
        course_image = db.Column(db.Text(), nullable=True)
        what_you_will_learn = db.Column(db.String(length=1024))

        tutorials = db.Column(db.String(length=1024))
        def __repr__(self):
                return f'Course {self.name}'
        


class CommentModel(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer(),primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(length=30),nullable=False)
    course_id = db.Column(db.Integer(), db.ForeignKey('course.id'), nullable=False)
    messageContent = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f"CommentModel(id={self.id}, username={self.username})"
