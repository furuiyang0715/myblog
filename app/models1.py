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

(6) 因为本应用使用SQLite，所以upgrade命令检测到数据库不存在时，会创建它（在这个命令完成之后，你会注意到一个名为app.db的文件，即SQLite数据库）。
在使用类似MySQL和PostgreSQL的数据库服务时，必须在运行upgrade之前在数据库服务器上创建数据库。 
 
 
(7) 通过数据库迁移机制的支持，在你修改应用中的模型之后，将生成一个新的迁移脚本（flask db migrate），
你可能会审查它以确保自动生成的正确性，然后将更改应用到你的开发数据库（flask db upgrade）。 测试无误后，将迁移脚本添加到源代码管理并提交。 
 
当准备将新版本的应用发布到生产服务器时，你只需要获取包含新增迁移脚本的更新版本的应用，然后运行flask db upgrade即可。 
Alembic将检测到生产数据库未更新到最新版本，并运行在上一版本之后创建的所有新增迁移脚本。 
 
正如我前面提到的，flask db downgrade命令可以回滚上次的迁移。 虽然在生产系统上不太可能需要此选项，但在开发过程中可能会发现它非常有用。 
你可能已经生成了一个迁移脚本并将其应用，只是发现所做的更改并不完全是你所需要的。 在这种情况下，可以降级数据库，删除迁移脚本，然后生成一个新的来替换它。 
 
'''