from datetime import datetime
from flask_login import current_user

from app import app, db
from app.models import User, Post


@app.shell_context_processor
def make_shell_context():
    """创建 flask shell 的上下文变量"""
    return {'db': db, 'User': User, 'Post': Post}


@app.before_request
def before_request():
    if current_user.is_authenticated:
        # 我之前提到过，应用应该以一致的时间单位工作，标准做法是使用UTC时区，使用系统的本地时间不是一个好主意，
        # 因为如果那么的话，数据库中存储的时间取决于你的时区。
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)


'''
存在两种启动方式: 
(1) 如上 

(2) # export FLASK_APP=microblog.py 
    # flask run
'''


'''
在 flask 中优雅存储环境变量
（1） 安装 python-dotenv
（2） 在项目的根目录下新建一个名为 .flaskenv 的文件
内容: 
FLASK_APP=microblog.py
 (3) 通过此配置, FLASK_APP 就可以自动加载 

'''
