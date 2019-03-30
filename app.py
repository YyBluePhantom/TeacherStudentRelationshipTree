from flask import Flask,render_template,request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm,LoginForm,ShowAccount
import os
import random

app=Flask(__name__)

# sqlalchemy+SQLite的配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'dev'

# 全局变量,为ShowAccount和regist之间传递账号
account=None


# 数据库基础登录信息
class user(db.Model):
    account=db.Column(db.String(10),primary_key=True)
    password=db.Column(db.String(16))

# 数据库用户个人信息
class user_message(db.Model):
    account=db.Column(db.String(10),primary_key=True)
    name=db.Column(db.String(30))
    telephone=db.Column(db.String(20))
    idcard=db.Column(db.String(30))
    email=db.Column(db.String(40))
    sex=db.Column(db.String(10))


# 10位数账号生成,首字母不为0;
def generate_account():
    a=str(random.randrange(1,10,1))
    for i in range(9):
        a=a+str(random.randrange(0,10,1))
    return a


# 登录页面
@app.route('/login.html', methods=['GET','POST'])
#@app.route('/', methods=['GET', 'POST'])
def basic():
    loginform=LoginForm()
    
    #PRG结构:POST redirect GET
    if loginform.validate_on_submit():
        flash(u'I successed')  
        account=loginform.account.data
        password=loginform.password.data
        
        # 账号不存在/密码错误
        if user.query.get(account)==None or password!=user.query.get(account).password:
            flash(u'用户名或者登录密码有误')
            return redirect(url_for('basic'))        
        else:
            #flash(u'进入正确的区域')
            return redirect(url_for('homepage'))
    
    #渲染失败信息
    #flash(u'I failed')
    return render_template('login.html',form=loginform)



# 注册页面
@app.route('/regist.html',methods=['GET','POST'])
def regist():
    regForm=RegisterForm()

    # POST方法, 如果数据合理,那么放入数据库中;否则提示错误;
    if regForm.validate_on_submit():

        # 获取数据
        global account
        account=generate_account()
        while user.query.get(account)!=None:
            account=generate_account()
        password=regForm.password.data
        name=regForm.name.data
        phonenumber=regForm.phonenumber.data 
        sex=regForm.sex.data 
        idcard=regForm.idcard.data 
        email=regForm.email.data 

        # 将数据添加入数据库中;
        user_temp=user(account=account,password=password)
        user_message_temp=user_message(account=account,name=name,telephone=phonenumber,idcard=idcard,sex=sex,email=email)
        db.session.add(user_temp)
        db.session.add(user_message_temp)
        db.session.commit()
        
        return redirect(url_for('back_to_login'))
    
    return render_template('regist.html',form=regForm)


# 注册后显示账号
@app.route('/accountback.html',methods=['GET','POST'])
def back_to_login():
    sa=ShowAccount()
    global account
    
    # 返回登录页面
    if request.method=='POST': 
        return redirect(url_for('basic'))

    return render_template('accountback.html',account=account)


# 主页
@app.route('/homepage.html',methods=['GET','POST'])
def homepage():

    return render_template('homepage.html')


