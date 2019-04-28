from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db =SQLAlchemy()



class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(10),unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    is_del=db.Column(db.Boolean,default=0)
    create_time =db.Column(db.DateTime,default=datetime.now)

    __tablename__="user"



class ArticleType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_name =db.Column(db.String(10),unique=True,nullable=False)
    # a_name = db.Column(db.String(20),nullable=False)#分类名
    arts = db.relationship('Article',backref='tp')

    __tablename__ = "art_type"


class Article(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(30),unique=True,nullable=False)
    desc = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time =db.Column(db.DateTime,default=datetime.now)
    # len = db.Column(db.Integer,nullable=True)
    type = db.Column(db.Integer,db.ForeignKey('art_type.id'))







#保存
    def save(self):
        db.session.add(self)
        db.session.commit()

#删除
    def __delete__(self):
        db.session.delete(self)
        db.session.commit()