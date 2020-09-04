from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length, Email

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    # Email， 这个来自WTForms的另一个验证器将确保用户在此字段中键入的内容与电子邮件地址的结构相匹配。
    # email = StringField('邮箱', validators=[DataRequired(), Email()])
    email = StringField('邮箱', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    # EqualTo 的验证器，它将确保其值与第一个password字段的值相同。
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        # 则通过ValidationError触发验证错误。 异常中作为参数的消息将会在对应字段旁边显示，以供用户查看。
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


# class EditProfileForm(FlaskForm):
#     """个人信息编辑表单"""
#     username = StringField('用户名', validators=[DataRequired()])
#     about_me = TextAreaField('个人简介', validators=[Length(min=0, max=140)])
#     submit = SubmitField('提交')


class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    about_me = TextAreaField('个性签名', validators=[Length(min=0, max=140)])
    submit = SubmitField('提交')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # 用原始的用户名为 form 实例赋予一个新的属性
        self.original_username = original_username

    def validate_username(self, username):
        '''
        大多数情况下，以后在编辑个人资料时出现用户名重复的提交将被友好地阻止。
        而是不是一个完美的解决方案，因为当两个或更多进程同时访问数据库时，这可能不起作用。
        假如存在验证通过的进程A和B都尝试修改用户称为同一个，但稍后进程A尝试重命名时，
        数据库已被进程B更改，无法重命名为该用户名，会再次引发数据库异常。
        '''
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('此用户名已经存在 ~~')


class PostForm(FlaskForm):
    """发送用户动态的表单 """
    post = TextAreaField('说点什么吧 ~~ ', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('发表')


class ResetPasswordRequestForm(FlaskForm):
    """重置密码的表单"""
    # email = StringField('Email', validators=[DataRequired(), Email()])
    email = StringField('邮箱', validators=[DataRequired()])
    submit = SubmitField('请求密码重置')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('请求密码重置')
