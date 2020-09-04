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

'''测试发送加密邮件
import jwt
token = jwt.encode({'a': 'b'}, 'my-secret', algorithm='HS256')
print(token) 
print(jwt.decode(token, 'my-secret', algorithms=['HS256'])) 

'''

'''关于flask中的上下文 
Flask使用上下文来避免必须跨函数传递参数。 我不打算详细讨论这个问题，但是需要知道的是，有两种类型的上下文，即应用上下文和请求上下文。 
在大多数情况下，这些上下文由框架自动管理，但是当应用启动自定义线程时，可能需要手动创建这些线程的上下文。
许多Flask插件需要应用上下文才能工作，因为这使得他们可以在不传递参数的情况下找到Flask应用实例。
这些插件需要知道应用实例的原因是因为它们的配置存储在app.config对象中，这正是Flask-Mail的情况。
mail.send()方法需要访问电子邮件服务器的配置值，而这必须通过访问应用属性的方式来实现。 
使用with app.app_context()调用创建的应用上下文使得应用实例可以通过来自Flask的current_app变量来进行访问。 


'''
