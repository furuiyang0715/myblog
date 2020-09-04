import os
import pprint

from flask import render_template, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from app.models import User, Post

basedir = os.path.abspath(os.path.dirname(__file__))


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
@login_required
def index():
    # posts = current_user.followed_posts()
    # 关于主页用户动态的分类
    # 如果一个用户有成千上万条关注的用户动态时，会发生什么？你可以想象得到，管理这么大的用户动态列表将会变得相当缓慢和低效。
    # 为了解决这个问题，我会将用户动态进行分页。这意味着一开始显示的只是所有用户动态的一部分，并提供链接来访问其余的用户动态。
    # Flask-SQLAlchemy的paginate()方法原生就支持分页。例如，我想要获取用户关注的前20个动态，我可以将all()结束调用替换成如下的查询：
    # 三个参数：从 1 开始的页码；每个展示的个数;
    # 错误处理布尔标记，如果是True，当请求范围超出已知范围时自动引发404错误。如果是False，则会返回一个空列表。

    page = request.args.get('page', 1, type=int)    # 因为分页 要额外获取一个参数 表名当前是第几页
    posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False).items
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    return render_template('index.html', title='Home', form=form, posts=posts)


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
    return render_template('user.html', user=user)


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
    # form = EditProfileForm()
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        # form 通过检验 说明是 post 请求
        username = form.username.data
        about_me = form.about_me.data

        current_user.username = username
        current_user.about_me = about_me
        db.session.add(current_user)
        db.session.commit()
        flash('您已成功修改个人资料')
        # 成功修改 导向用户主页
        return redirect(url_for("user", username=username))

        # # 校验修改的用户名是否已经存在 且 与当前用户名不重复
        # if username != current_user.username and User.query.filter_by(username=username).first():
        #     flash("该用户名已存在")
        #     # post 请求失败时重新导向 get 页面
        #     return render_template('edit_profile.html', title='编辑个人资料', form=form)
        # else:
        #     current_user.username = username
        #     current_user.about_me = about_me
        #     db.session.add(current_user)
        #     db.session.commit()
        #     flash('您已成功修改个人资料')
        #     # 成功修改 导向用户主页
        #     return redirect(url_for("user", username=username))

    elif request.method == "GET":
        # 初次 get 请求时显示默认的用户名和简介
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        return render_template('edit_profile.html',  title='编辑个人资料', form=form)

    return render_template('edit_profile.html', title='编辑个人资料', form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    # 关注的用户不存在 则重定向到首页
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))

    # 不能关注自身
    if user == current_user:
        flash('不能关注自己!')
        return redirect(url_for('user', username=username))

    current_user.follow(user)
    db.session.commit()
    flash('关注 {} 成功!'.format(username))
    # 关注某人成功后进入该用户首页
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))

    if user == current_user:
        flash('不能取关自己!')
        return redirect(url_for('user', username=username))

    current_user.unfollow(user)
    db.session.commit()
    flash('已成功取关 {}.'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/explore')
@login_required
def explore():
    # posts = Post.query.order_by(Post.timestamp.desc()).all()

    page = request.args.get('page', 1, type=int)  # 因为分页 要额外获取一个参数 表名当前是第几页
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False).items

    return render_template('index.html', title='Explore', posts=posts)
