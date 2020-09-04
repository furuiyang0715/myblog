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

'''搭配前端框架使用: 
(1) 安装: pip install flask-bootstrap 

'''

'''关于页面中的一些时间和日期 
from datetime import datetime
t1 = str(datetime.now())
t2 = str(datetime.utcnow())
print(t1) 
print(t2) 

datetime.now()调用返回我所处位置的本地时间，而datetime.utcnow()调用则返回UTC时区中的时间。 
如果我可以让遍布世界不同地区的多人同时运行上面的代码，那么datetime.now()函数将为他们每个人返回不同的结果，但是无论位置如何，
datetime.utcnow()总是会返回同一时间。 那么你认为哪一个更适合用在一个很可能其用户遍布世界各地的Web应用中呢？ 

很明显，服务器必须管理一致且独立于位置的时间。 如果这个应用增长到在全世界不同地区都需要部署生产服务器的时候，
我不希望每个服务器都在写入不同时区的时间戳到数据库，因为这会导致其无法正常地运行。 
由于UTC是最常用的统一时区，并且在datetime类中也受到支持，因此我将会使用它。 

从服务器的角度来说，将时间戳标准化为UTC，意义重大，但这会为用户带来可用性问题。 
本章的目标就是解决该问题，同时保持服务器中以UTC格式管理的所有时间戳。 

事实证明，Web浏览器可以获取用户的时区，并通过标准的日期和时间JavaScript API暴露它。 实际上有两种方法来利用JavaScript提供的时区信息：

“老派”方法是当用户第一次登录到应用程序时，Web浏览器以某种方式将时区信息发送到服务器。 这可以通过Ajax调用完成，或者更简单地使用meta refresh tag。 
一旦服务器知道了时区，就可以将其保存在用户的会话中，或者将其写入用户在数据库中的条目中，然后在渲染模板时从中调整所有时间戳。
“新派”的做法是不改变服务器中的东西，而在客户端中使用JavaScript来对UTC和本地时区之间进行转换。 


Moment.js是一个小型的JavaScript开源库，它将日期和时间转换成目前可以想象到的所有格式。 
不久前，我创建了Flask-Moment，一个小型Flask插件，它可以使你在应用中轻松使用moment.js。 


(1) 安装： pip install flask-moment 



'''
