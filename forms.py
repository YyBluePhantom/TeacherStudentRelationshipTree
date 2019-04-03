# 表单信息

from flask_wtf import FlaskForm
# 表单由若干输入字段组成,每种字段用一种类接收,组成一种类,每种字段作为组合类的一种属性;
from wtforms import StringField, PasswordField, BooleanField, IntegerField, TextAreaField, SubmitField, MultipleFileField ,SelectField,RadioField
from wtforms.validators import DataRequired, Length, ValidationError, Email,InputRequired,NumberRange

# 登录

# 登录界面的登录登录字段组合形成的类
class LoginForm(FlaskForm):
    account=StringField('Account',validators=[Length(10,10,message=u'长度为10位')])   # 文本字段
    password=PasswordField('Password',validators=[Length(6,16,message=u'长度为6~16位')])   # 密码字段
    submit=SubmitField('Log in')   #提交按钮字段

# 登录界面的注册字段
class RegisterForm(FlaskForm):
    password=PasswordField('Password',validators=[Length(6,16,message=u'长度为6~16位')])   # 密码字段
    name=StringField('Username',validators=[DataRequired(message=u'名字不能为空')])
    phonenumber=StringField('Telephone',validators=[Length(11,11,message=u'电话号码长度为11位')])
    sex=SelectField('Sex',
        validators=[DataRequired()],
        choices=[('男','男'),('女','女')]
    )
    idcard=StringField('IDCard',validators=[DataRequired(message=u'身份证号不能为空')])
    email=StringField('Email',validators=[Email(message=u'填写正确的Email格式')])
    regist=SubmitField('Regist')

# 注册返回界面字段
class ShowAccount(FlaskForm):
    BACK=SubmitField('back')

class AddRelation(FlaskForm):
    account=StringField('Account',validators=[Length(10,10,message=u'长度为10位')])
    T_or_S=RadioField('Relations',choices=[('teacher','teacher'),('student','student')],validators=[DataRequired()])
    starttime=StringField('StartTime')
    endtime=StringField('EndTime')
    submit=SubmitField('Submit')
