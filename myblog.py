from app import app


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