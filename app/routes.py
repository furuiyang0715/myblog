from flask import render_template, flash, url_for
from werkzeug.utils import redirect

from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        # url_for()的参数是endpoint名称，也就是视图函数的名字。
        return redirect(url_for("index"))

    # 这是因为表单的字段对象的在渲染时会自动转化为HTML元素。
    return render_template('login.html', title='登录', form=form)
