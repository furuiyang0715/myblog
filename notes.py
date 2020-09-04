'''flask 发送邮件
（1） 安装依赖：
pip insall flask-mail
pip install pyjwt

（2） mail 插件化
mail = Mail(app)

(3) 进行配置之后 测试邮件的发送
from flask_mail import Message
from app import mail
msg = Message('test subject', sender=app.config['ADMINS'][0], recipients=['2564493603@qq.com'])
msg.body = 'text body'
msg.html = '<h1>HTML body</h1>'
mail.send(msg)

'''