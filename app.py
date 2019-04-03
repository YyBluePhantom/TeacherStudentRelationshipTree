from flask import Flask,render_template,request, url_for, redirect, flash , session
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm,LoginForm,ShowAccount,AddRelation
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user, UserMixin
from flask_wtf.csrf import CSRFProtect
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


# 配置LoginManager, use login manager to manage session
login_manager=LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'basic'
login_manager.init_app(app)
login_manager.login_message = u"请先登录"

# 这个callback函数用于reload User object，根据session中存储的user_id,我们可以通过对current_user对象调用is_authenticated等属性来判断当前用户的认证状态。
# 如果用户未登录，current_user默认会返回Flask-Login内置的AnonymousUserMixin类对象，它的is_authenticated和is_active属性会返回False，而is_anonymous属性则返回True。


csrf=CSRFProtect()
csrf.init_app(app)


# 既能够充当数据库进行,query查询;    也能够创建当前登录对象;
# 通过is_authenticated(),is_active(),is_anonymous(),get_id()来对函数处理
class CurrentUser(UserMixin,db.Model):
    account = db.Column(db.String(10),primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(40))
    password= db.Column(db.String(16))
    idcard=db.Column(db.String(30))
    sex=db.Column(db.String(10))
    telephone=db.Column(db.String(20))

    def __init__(self,account,name,password,email,idcard,sex,telephone):
        self.account=account
        self.name=name
        self.password=password
        self.email=email
        self.idcard=idcard
        self.sex=sex
        self.telephone=telephone

    def get_id(self):
        return self.account


# 师生关系表
TeachRelation = db.Table('teachrelation',
    db.Column('teacher_account', db.String(10), db.ForeignKey('teacher.account')),
    db.Column('student_account', db.String(10), db.ForeignKey('student.account')),
)


class Teacher(db.Model):
    __tablename__='teacher'
    account=db.Column(db.String(10),primary_key=True)
    start_time=db.Column('date_start', db.String(10)),
    end_time=db.Column('date_end', db.String(10)),
    
    def __init__(self,account,start_time,end_time):
        self.account=account
        self.start_time=start_time
        self.end_time=end_time


class Student(db.Model):
    __tablename__='student'
    account=db.Column(db.String(10),primary_key=True)
    start_time=db.Column('date_start', db.String(10)),
    end_time=db.Column('date_end', db.String(10))

    teachers=db.relationship('Teacher',
            secondary=TeachRelation,
            backref=db.backref('students')
	)

    def __init__(self,account,start_time,end_time):
        self.account=account
        self.start_time=start_time
        self.end_time=end_time



# 调用current_user前,先执行user_loader,传入的数据是session中的id(唯一),将CurrentUser中对应的项作为返回值
@login_manager.user_loader
def load_user(account):
    return CurrentUser.query.get(account)


# 10位数账号生成,首字母不为0;
def generate_account():
    a=str(random.randrange(1,10,1))
    for i in range(9):
        a=a+str(random.randrange(0,10,1))
    return a


# 登录页面,进入登录状态
@app.route('/login.html', methods=['GET','POST'])
def basic():
    # 登录状态,跳转主页
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    
    # 未登录,验证
    loginform=LoginForm()
    if loginform.validate_on_submit():  

        user=CurrentUser.query.filter_by(account=loginform.account.data, password=loginform.password.data).first()        
        # 账号不存在/密码错误
        if user is None:
            flash(u'用户名或者登录密码有误')
            return redirect(url_for('basic'))        
        else:
            login_user(user)
            session['account']=user.account
            return redirect(url_for('homepage'))
    
    #渲染失败信息
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
        while CurrentUser.query.get(account)!=None:
            account=generate_account()
        password=regForm.password.data
        name=regForm.name.data
        phonenumber=regForm.phonenumber.data 
        sex=regForm.sex.data 
        idcard=regForm.idcard.data 
        email=regForm.email.data 

        # 将数据添加入数据库中;
        current_user_message=CurrentUser(account,name,password,email,idcard,sex,phonenumber)
        db.session.add(current_user_message)
        db.session.commit()
        
        return redirect(url_for('back_to_login'))
    
    # 数据不合理/未提交,显示原页面附加错误信息
    return render_template('regist.html',form=regForm,count=CurrentUser.query.count())


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
'''
homepage.html作为主界面;分为两种情况:登录状态,非登陆状态;
登录状态:根据登录信息,获取老师和学生的信息
非登陆状态:显示界面,不显示信息; 在非登陆状态点击功能图标,会跳转入登录界面;
具有Login/Logout两个按钮(选项):(或者根据登录状态变更)
1.对于未登录状态,Login,并跳转入登陆界面
2.对于登陆状态,Logout,并跳转入原界面的非登陆状态
'''
@app.route('/homepage.html',methods=['GET','POST'])
@app.route('/', methods=['GET', 'POST'])
def homepage():
    # 用户登录
    if current_user.is_authenticated:
        #获得账号
        account=session.get('account')

        #返回老师和学生信息的列表,信息只有账号属性;
        teacher_list=db.session.query(Teacher).filter(Teacher.account==account).all()
        student_list=db.session.query(Student).filter(Student.account==account).all()

        # 将信息返回给前端,显示,count=Student.query.all()
        return render_template('homepage.html',students=student_list,teachers=teacher_list,count=Student.query.count())
    
    # 游客状态
    else:
        return render_template('homepage.html')



# 添加关系;    建立表单的form
@app.route('/add.html',methods=['GET','POST'])
@login_required
def add():
    # 获取账号信息
    account=session.get('account')

    # 添加信息
    add_relation=AddRelation()
    if add_relation.validate_on_submit():
        flash(u'成功validate')

        if  CurrentUser.query.get(add_relation.account.data)==None:
            flash(u'该用户不存在,无法建立关系')
            return render_template('add.html',form=add_relation)
        
        else :
            # 对方是你的老师
            if add_relation.T_or_S.data=="teacher" :
                flash('teacher')
                
                t1=Teacher(add_relation.account.data,add_relation.starttime,add_relation.endtime.data)
                s1=Student(account,add_relation.starttime,add_relation.endtime.data)
                t2=[]
                t2.append(t1)
                s1.teachers=t2

                db.session.add(s1)
                db.session.commit()
            
            else:
                flash(u'student')

                t1=Teacher(account,add_relation.starttime,add_relation.endtime.data)
                s1=Student(add_relation.account.data,add_relation.starttime,add_relation.endtime.data)
                t2=[]
                t2.append(t1)
                s1.teachers=t2

                db.session.add(s1)
                db.session.commit()
    
            redirect(url_for('homepage'))
            
    return render_template('add.html',form=add_relation)



#  logout:退出账号
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()
