import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

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
# 如您所见，仅当应用未以调试模式运行，并配置中存在邮件服务器时，我才会启用电子邮件日志记录器。
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

    if not os.path.exists('logs'):
        os.mkdir('logs')
    # 日志文件
    file_handler = RotatingFileHandler('logs/myblog.log', maxBytes=10240, backupCount=10)
    # 日志的时间格式
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    # 日志等级
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Myblog startup')


# 这样写是为了解决循环引用的问题
from app import routes, models, errors


'''使用Python的SMTP调试服务器。
这是一个模拟的电子邮件服务器，它接受电子邮件，然后打印到控制台。要运行此服务器，请打开第二个终端会话并在其上运行以下命令：

(venv) $ python -m smtpd -n -c DebuggingServer localhost:8025 

如果使用的是 python 自建的电子邮件服务器（如上）, 那么相应的配置应该是: 
MAIL_SERVER=localhost 和  
MAIL_PORT=8025 

'''


'''关于 flask 中的日志: 
日志文件的存储路径位于顶级目录下，相对路径为logs/microblog.log，如果其不存在，则复制它。
RotatingFileHandler类非常棒，因为它可以切割和清理日志文件，以确保日志文件在应用程序运行很连续时不会变得太大。
本处，我将日志文件的大小限制为10KB，并只保留最后的十个日志文件作为备份。
由于这些消息正在写入到一个文件，我希望它们可以存储多重的信息。所以我使用的格式包括替换，日志记录级别，消息和日志来源的源代码文件和行号。
为了使日志记录更有用，我还将应用状语从句：文件日志记录器的日志记录级别降低到INFO级别。如果你不熟悉日志记录类别，
则按照严重程度递增的顺序来认识它们就行了，分别是DEBUG，INFO，WARNING，ERROR和CRITICAL。
当此应用程序在生产服务器上运行时，这些日志数据将告诉您服务器何时重新启动过。 

'''