from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    '''
    db.relationship的第一个参数表示代表关系“多”的类。 backref参数定义了代表“多”的类的实例反向调用“一”的时候的属性名称。
    这将会为用户动态添加一个属性post.author，调用它将返回给该用户动态的用户实例。 
    lazy参数定义了这种关系调用的数据库查询是如何执行的。
    '''
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # 外键

    def __repr__(self):
        return '<Post {}>'.format(self.body)


'''开启交互测试 
from app import db
from app.models import User, Post
u = User(username='john', email='john@example.com')
u1 = User(username='susan', email='susan@example.com') 

db.session.add(u)
db.session.add(u1)
db.session.commit() 

User.query.all()

u = User.query.get(1) 
p = Post(body='my first post!', author=u) 
u.posts.all() 
db.session.add(p)
db.session.commit() 



'''