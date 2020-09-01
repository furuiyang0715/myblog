from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


'''
（1） 定义初始数据库结构 即元数据 

（2） 但随着应用的不断增长，很可能会新增、修改或删除数据库结构。 Alembic（Flask-Migrate使用的迁移框架）将以一种不需要重新创建数据库的方式进行数据库结构的变更。 
为了实现它，Alembic维护一个数据库迁移存储库，它是一个存储迁移脚本的目录。 每当对数据库结构进行更改后，都需要向存储库中添加一个包含更改的详细信息的迁移脚本。 当应用这些迁移脚本到数据库时，它们将按照创建的顺序执行。 

（3） 运行flask db init来创建myblog的迁移存储库 



(4)包含映射到User数据库模型的用户表的迁移存储库生成后，是时候创建第一次数据库迁移了。 有两种方法来创建数据库迁移：手动或自动。 
要自动生成迁移，Alembic会将数据库模型定义的数据库模式与数据库中当前使用的实际数据库模式进行比较。 然后，使用必要的更改来填充迁移脚本，以使数据库模式与应用程序模型匹配。 
当前情况是，由于之前没有数据库，自动迁移将把整个User模型添加到迁移脚本中。 flask db migrate子命令生成这些自动迁移：  flask db migrate -m 'User Table.'
 
 
(5) flask db migrate命令不会对数据库进行任何更改，只会生成迁移脚本。 要将更改应用到数据库，必须使用flask db upgrade命令。 
 

'''