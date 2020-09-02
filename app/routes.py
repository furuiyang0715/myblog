import os
import pprint

from flask import render_template, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User, Post

basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Home', posts=posts)


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
        # 特别是request.args属性，可用友好的字典格式暴露查询字符串的内容。

        print(pprint.pformat(request.args))

        next_page = request.args.get('next')
        # 因此应用仅在重定向URL是相对路径时才执行重定向，这可确保重定向与应用保持在同一站点中。
        # 为了确定URL是相对的还是绝对的，我使用Werkzeug的url_parse()函数解析，然后检查netloc属性是否被设置。

        # netloc 是域名服务器
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='登录', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username=username, email=email)
        # user.username = username
        # user.email = email
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你 注册成功')
        return redirect(url_for("login"))

    return render_template('register.html', title='注册', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        print("post")
        file = request.files.get('file')
        file_path = os.path.join(basedir, "static/photos/{}".format(file.filename))
        file.save(file_path)
        return "保存成功"
    else:
        return render_template('upload.html')


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        # form 通过检验 说明是 post 请求
        username = form.username.data
        about_me = form.about_me.data

        # 校验修改的用户名是否已经存在 且 与当前用户名不重复
        if username != current_user.username and User.query.filter_by(username=username).first():
            flash("该用户名已存在")
            # post 请求失败时重新导向 get 页面
            return render_template('edit_profile.html', title='编辑个人资料', form=form)
        else:
            current_user.username = username
            current_user.about_me = about_me
            db.session.add(current_user)
            db.session.commit()
            flash('您已成功修改个人资料')
            # 成功修改 导向用户主页
            return redirect(url_for("user", username=username))

    elif request.method == "GET":
        # 初次 get 请求时显示默认的用户名和简介
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        return render_template('edit_profile.html',  title='编辑个人资料', form=form)
