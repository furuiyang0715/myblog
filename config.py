import os
basedir = os.path.abspath(os.path.dirname(__file__))
# print(basedir)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # sqlite 数据库文件的路径
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 发送邮件的配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '15626046299@163.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', os.environ.get("EMAIL_HOST_PASSWORD"))
    ADMINS = ['15626046299@163.com']

    POSTS_PER_PAGE = 4  # 配置项 表示每页的配置列表长度


# if __name__ == '__main__':
#     print(Config().MAIL_PASSWORD)
#
#     pass
