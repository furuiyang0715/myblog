import os
basedir = os.path.abspath(os.path.dirname(__file__))
# print(basedir)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # sqlite 数据库文件的路径
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '15626046299@163.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', os.environ.get("EMAIL_HOST_PASSWORD"))
    ADMINS = [
        '2564493603@qq.com',
        '15626046299@163.com',
    ]

    POSTS_PER_PAGE = 10  # 配置项 表示每页的配置列表长度

    # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    # EMAIL_HOST = 'smtp.163.com'
    # EMAIL_PORT = 25
    # # 发送邮件的邮箱
    # EMAIL_HOST_USER = '15626046299@163.com'
    # # 在邮箱中设置的客户端授权密码
    # EMAIL_HOST_PASSWORD = configs.EMAIL_HOST_PASSWORD
    # # 收件人看到的发件人
    # EMAIL_FROM = 'mydailyfresh<15626046299@163.com>'


# if __name__ == '__main__':
#     print(Config().MAIL_PASSWORD)
#
#     pass
