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


# 这样写是为了解决循环引用的问题
from app import routes, models
