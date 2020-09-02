import logging
from logging.handlers import SMTPHandler

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config


# __name__ 表示当前调用 py 的模块的名字
app = Flask(__name__)

# 为 APP 增加简单的配置项
# app.config['SECRET_KEY'] = 'you-will-never-guess'
# 使用类的方式为 app 增加配置项
app.config.from_object(Config)
# flask 采用插件化的模式
# 数据库的实例
db = SQLAlchemy(app)
# 数据库迁移引擎 将两者结合起来
migrate = Migrate(app, db)

login = LoginManager(app)
# 强制用户登录 跳转页面
login.login_view = 'login'


# 为 Flask 的日志对象 app.logger 添加了一个 SMTPHandler 的实例：
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='我的微博发送信息失败',
            credentials=auth, secure=secure,
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


# 这样写是为了解决循环引用的问题
from app import routes, models, errors
