from application import db, login_manager
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    #id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    tel = db.Column(db.Integer, nullable=False)
    cohort = db.Column(db.String(30), nullable=False)
    pathway = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    topics = db.relationship('Topics', backref='users')

    def __repr__(self):
        return ''.join(['UserID: ', str(self.userid), '\r\n',
        'Email: ', self.email], '\r\n',
        'Name: ', self.first_name, ' ', self.last_name,
        'City: ', self.city, ' ', self.city,
        'Tel: ', self.tel, ' ', self.tel,
        'Cohort: ', self.cohort, ' ', self.cohort,
        'Pathway: ', self.pathway, ' ', self.pathway
        )

@login_manager.user_loader
def load_user(userid):
    return Users.query.get(int(userid))


class Topics(db.Model):
    topic_id = db.Column(db.Integer, primary_key=True)
    userid=db.Column('userid', db.Integer, db.ForeignKey(Users.userid), nullable=False)
    topic_Name = db.Column(db.String(250))
    module = db.relationship('Module', backref='Topics')


class Module(db.Model):
    module_id = db.Column(db.Integer, primary_key=True)
    topic_id= db.Column(db.Integer, db.ForeignKey(Topics.topic_id), nullable=False)
    module_Name = db.Column(db.String(250))
    video = db.relationship('Videos', backref='Module')


class Videos(db.Model):
#id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey(Module.module_id), nullable=False)
    video_link = db.Column(db.String(250))
    #Name = db.Column(db.String(30))
    video_date = db.Column(db.DateTime)
