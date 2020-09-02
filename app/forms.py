from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length

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


class EditProfileForm(FlaskForm):
    """个人信息编辑表单"""
    username = StringField('用户名', validators=[DataRequired()])
    about_me = TextAreaField('个人简介', validators=[Length(min=0, max=140)])
    submit = SubmitField('提交')
