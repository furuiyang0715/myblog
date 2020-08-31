from flask import Flask


# __name__ 表示当前调用 py 的模块的名字
app = Flask(__name__)

# 这样写是为了解决循环引用的问题
from app import routes


# if __name__ == '__main__':
#     app.run(debug=True)
