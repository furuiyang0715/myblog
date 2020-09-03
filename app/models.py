from hashlib import md5
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


# 创建关联表
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
)


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
    # 用户的一段自我介绍
    about_me = db.Column(db.String(140))
    # 用户上一次访问该网站的时间
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship(
        'User',
        secondary=followers,     # 指定了用于该关系的关联表
        primaryjoin=(followers.c.follower_id == id),    # 通过关联表关联到左侧实体的条件
        secondaryjoin=(followers.c.followed_id == id),  # 通过关联表关联到右侧实体的条件
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    '''
    建立关系的过程实属不易。 就像我为post一对多关系所做的那样，我使用db.relationship函数来定义模型类中的关系。 
    这种关系将User实例关联到其他User实例，所以按照惯例，对于通过这种关系关联的一对用户来说，左侧用户关注右侧用户。 
    我在左侧的用户中定义了followed的关系，因为当我从左侧查询这个关系时，我将得到已关注的用户列表（即右侧的列表）。 
    
    让我们逐个检查这个db.relationship()所有的参数：'User'是关系当中的右侧实体（将左侧实体看成是上级类）。由于这是自引用关系，所以我不得不在两侧都使用同一个实体。
    secondary 指定了用于该关系的关联表，就是使用我在上面定义的followers。
    primaryjoin 指明了通过关系表关联到左侧实体（关注者）的条件 。关系中的左侧的join条件是关系表中的follower_id字段与这个关注者的用户ID匹配。
    followers.c.follower_id表达式引用了该关系表中的follower_id列。
    secondaryjoin 指明了通过关系表关联到右侧实体（被关注者）的条件 。 这个条件与primaryjoin类似，唯一的区别在于，现在我使用关系表的字段的是followed_id了。
    backref定义了右侧实体如何访问该关系。在左侧，关系被命名为followed，所以在右侧我将使用followers来表示所有左侧用户的列表，即粉丝列表。
    附加的lazy参数表示这个查询的执行模式，设置为动态模式的查询不会立即执行，直到被调用，这也是我设置用户动态一对多的关系的方式。
    lazy和backref中的lazy类似，只不过当前的这个是应用于左侧实体，backref中的是应用于右侧实体。 
    '''

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        """关注用户"""
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        """取消关注"""
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        """
        判断当前用户是否已经关注指定用户
        在当前用户的关注人中筛选 是否已经关注了此人
        :param user:
        :return:
        """
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        """查看当前用户关注者的全部动态"""
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(    # （2） 的全部博客
            followers.c.follower_id == self.id).order_by(     # (1）当前用户的全部关注者
            Post.timestamp.desc())  # (3) 按照时间排序

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

'''关于关联表: 
(1) 我想为每个用户维护一个“粉丝”用户列表和“关注”用户列表。 不幸的是，关系型数据库没有列表类型的字段来保存它们，
那么只能通过表的现有字段和他们之间的关系来实现。 

(2) 数据库已有一个代表用户的表，所以剩下的就是如何正确地组织他们之间的关注与被关注的关系。 

(3) 关于一对多关系: 
用户和用户动态通过这个关系来关联。其中，一个用户拥有多条用户动态，而一条用户动态属于一个用户（作者）。
数据库在多的这方使用了一个外键以表示一对多关系。在上面的一对多关系中，外键是post表的user_id字段，
这个字段将用户的每条动态都与其作者关联了起来。 


(4) 关于多对多关系
多对多关系会更加复杂，举个例子，数据库中有students表和teachers表，一名学生学习多位老师的课程，一位老师教授多名学生。
这就像两个重叠的一对多关系。

对于这种类型的关系，我想要能够查询数据库来获取教授给定学生的教师的列表，以及某个教师课程中的学生的列表。 
想要在关系型数据库中梳理这样的关系并非轻易而举，因为无法通过向现有表添加外键来完成此操作。 

这时我们需要的是一个关联表: 其中存在两个字段：老师 t 以及学生 s. 
存在以下几种关系: 
t1 s1
t1 s2 
t1 s3 
t2 s1 
t3 s1 
.. 
那么查询 t1 的老师即为 s1 s2 s3 
查询 s1 的学生即为 t1, t2, t3 .. 

(5) 关于多对多关系中的自关联: 
在(4) 的多对多关系中，存在着两个实体：即老师和学生。 
但有时在多对多关系中只存在一个实体，称为自关联。 
举例来说, 在微博中一个用户有多个关注，同时有多个粉丝。 关注和粉丝的实体都是用户自身。 
在地区层次关系中，每个地区的上级区域和下属区域仍然是一个地区实例。 


followers 表是关系的关联表。 此表中的外键都指向用户表中的数据行，因为它将用户关联到用户。 
该表中的每个记录代表关注者和被关注者的一个关系。 
即我们可以以关注者为外键，去查询该关注者的关注人，即他对应的所有被关注者。 
也可以以被关注者为外键，去查询该关注者的粉丝，即他对应的所有关注者。 

'''

'''关注以及取消的实现: 
user1.followed.append(user2) 
user1.followed.remove(user2) 

'''


'''关于查看已关注用户的动态: 
最显而易见的方案是先执行一个查询以返回已关注用户的列表，如你所知，可以使用user.followed.all()语句。
然后对每个已关注的用户执行一个查询来返回他们的用户动态。最后将所有用户的动态按照日期时间倒序合并到一个列表中。听起来不错？其实不然。

这种方法有几个问题。 如果一个用户关注了一千人，会发生什么？ 我需要执行一千个数据库查询来收集所有的用户动态。 然后我需要合并和排序内存中的一千个列表。 
作为第二个问题，考虑到应用主页最终将实现分页，所以它不会显示所有可用的用户动态，只能是前几个，并显示一个链接来提供感兴趣的用户查看更多动态。 
如果我要按它们的日期排序来显示动态，我怎么能知道哪些用户动态才是所有用户中最新的呢？除非我首先得到了所有的用户动态并对其进行排序。 
这实际上是一个糟糕的解决方案，不能很好地应对规模化。

用户动态的合并和排序操作是无法避免的，但是在应用中执行会导致效率十分低下， 而这种工作是关系数据库擅长的。 
我可以使用数据库的索引，命令它以更有效的方式执行查询和排序。 所以我真正想要提供的方案是，
定义我想要得到的信息来执行一个数据库查询，然后让数据库找出如何以最有效的方式来提取这些信息。

'''
