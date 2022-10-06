from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,email_validator
from application.models import Users
from flask_login import current_user


class AddVideoForm(FlaskForm):
    video_link = StringField('Video Name', validators=[DataRequired(), Length(min=2, max=30)])
    video_date = DateField ('Video Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Video')


class UpdateVideoForm(FlaskForm):
    oldname = StringField('Old Video Name', validators=[DataRequired(), Length(min=2, max=30)])
    newname = StringField('New Video Name', validators=[DataRequired(), Length(min=2, max=30)])
    olddate = DateField('Old Video Date', format='%Y-%m-%d', validators=[DataRequired()])
    newdate = DateField('New Video Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Update Video')

class DeleteVideoForm(FlaskForm):
    video_link = StringField('Video Name', validators=[DataRequired(), Length(min=2, max=30)])
    video_date = DateField ('Video Date', format='%Y-%m-%d', validators=[DataRequired(),])
    submit = SubmitField('Delete Video')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[
                                 DataRequired(),
                                 Length(min=4, max=30)
                             ]
                             )

    last_name = StringField('Last Name',
                            validators=[
                                DataRequired(),
                                Length(min=4, max=30)
                            ]
                            )
    city = StringField('City',
                            validators=[
                                DataRequired(),
                                Length(min=4, max=30)
                            ]
                            )
    tel = StringField('Tel',
                            validators=[
                                DataRequired(),
                                Length(min=4, max=30)
                            ]
                            )
    cohort = StringField('Cohort',
                            validators=[
                                DataRequired(),
                                Length(min=4, max=30)
                            ]
                            ) 
    pathway = StringField('Pathway',
                            validators=[
                                DataRequired(),
                                Length(min=4, max=30)
                            ]
                            )                        
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()
                        ]
                        )
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                             ]
                             )
    confirm_password = PasswordField('Confirm Password',
                                     validators=[
                                         DataRequired(),
                                         EqualTo('password')
                                     ]
                                     )
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email already in use')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                             ])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')