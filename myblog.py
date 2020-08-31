from app import app


if __name__ == '__main__':
    app.run(debug=True)




'''
存在两种启动方式: 
(1) 如上 

(2) # export FLASK_APP=microblog.py 
    # flask run
'''