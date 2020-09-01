from flask import render_template, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import redirect

from app import app
from app.forms import LoginForm
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for user {}, remember_me={}'.format(
#             form.username.data, form.remember_me.data))
#         # url_for()的参数是endpoint名称，也就是视图函数的名字。
#         return redirect(url_for("index"))
#
#     # 这是因为表单的字段对象的在渲染时会自动转化为HTML元素。
#     return render_template('login.html', title='登录', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # current_user变量来自Flask-Login，可以在处理过程中的任何时候调用以获取用户对象
    # 这个变量的值可以是数据库中的一个用户对象（Flask-Login通过我上面提供的用户加载函数回调读取），或者如果用户还没有登录，
    # 则是一个特殊的匿名用户对象。 还记得那些Flask-Login必须的用户对象属性？ 其中之一是is_authenticated
    # 它可以方便地检查用户是否登录。 当用户已经登录，我只需要重定向到主页。
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        #  当你只需要一个结果时，通常使用first()方法。
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # flask-login 插件方法 登入用户
        # 该函数会将用户登录状态注册为已登录，这意味着用户导航到任何未来的页面时，应用都会将用户实例赋值给current_user变量。
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='登录', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
