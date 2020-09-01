from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

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

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

posts = Post.query.all() 
for post in posts: 
    print(post.id) 
    print(post.body) 
    print(post.timestamp) 
    print(post.user_id) 
    
## ??? 
User.query.order_by(User.username.desc()).all() 


## 删除测试数据 
users = User.query.all()
for u in users:
    db.session.delete(u)

posts = Post.query.all()
for p in posts:
    db.session.delete(p)
db.session.commit() 



# *.db-journal 则是为了让数据库能够支持事务而产生的临时日志文件，通常情况下这 个文件的大小都是 0 字节。 
'''

'''关于 flask shell 
flask shell命令是flask命令集中的另一个非常有用的工具。 shell命令是Flask在继run之后的实现第二个“核心”命令。 这个命令的目的是在应用的上下文中启动一个Python解释器。 

'''

'''关于用户hash
from werkzeug.security import generate_password_hash
hash = generate_password_hash('foobar') 

from werkzeug.security import check_password_hash
check_password_hash(hash, 'foobar')
check_password_hash(hash, 'barfoo') 

check_password_hash(hash, generate_password_hash('foobar'))  

'''
