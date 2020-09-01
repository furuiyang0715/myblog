from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
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


@login.user_loader
def load_user(id):
    '''
    用户会话是Flask分配给每个连接到应用的用户的存储空间，Flask-Login通过在用户会话中存储其唯一标识符来跟踪登录用户。
    每当已登录的用户导航到新页面时，Flask-Login将从会话中检索用户的ID，然后将该用户实例加载到内存中.
    因为数据库对Flask-Login透明，所以需要应用来辅助加载用户。 基于此，插件期望应用配置一个用户加载函数，
    可以调用该函数来加载给定ID的用户。 该功能可以添加到app/models.py模块中：
    '''
    return User.query.get(int(id))


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

'''关于用户登录 
(1) 安装： pip install flask-login
(2) 插件化处理 app 对象: 
from flask_login import LoginManager
app = Flask(__name__)
# ...
login = LoginManager(app) 
(3) 为 flask-login 准备用户模型 
Flask-Login插件需要在用户模型上实现某些属性和方法。这种做法很棒，因为只要将这些必需项添加到模型中，Flask-Login就没有其他依赖了，它就可以与基于任何数据库系统的用户模型一起工作。
必须的四项如下：
is_authenticated: 一个用来表示用户是否通过登录认证的属性，用True和False表示。
is_active: 如果用户账户是活跃的，那么这个属性是True，否则就是False（译者注：活跃用户的定义是该用户的登录状态是否通过用户名密码登录，通过“记住我”功能保持登录状态的用户是非活跃的）。
is_anonymous: 常规用户的该属性是False，对特定的匿名用户是True。
get_id(): 返回用户的唯一id的方法，返回值类型是字符串(Python 2下返回unicode字符串). 
我可以很容易地实现这四个属性或方法，但是由于它们是相当通用的，因此Flask-Login提供了一个叫做UserMixin的mixin类来将它们归纳其中。 下面演示了如何将mixin类添加到模型中： 

from flask_login import UserMixin
class User(UserMixin, db.Model):
    # ... 
'''

'''生成用户头像: 
from hashlib import md5
url = 'https://www.gravatar.com/avatar/' + md5(b'ruiyang0715@gmail.com').hexdigest()
print(url) 


'''
