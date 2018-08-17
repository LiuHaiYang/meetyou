from flask import Blueprint,render_template,request,session,make_response,redirect
from models import User
from main import db
import time,datetime
import json
login = Blueprint('login', __name__)

@login.route('/login')
def login_page():
    return render_template('login.html')

@login.route('/api/v1/loginAPI', methods=["POST"])
def login_in():
    if request.method == "POST":
        data = request.get_json(force=True)
        login_ac = data['email']
        passwd = data['password']
        session['user'] = str(login_ac)
        print(session['user'])
        newtime = datetime.datetime.strftime((datetime.datetime.now()),'%Y-%m-%d %H:%M:%S')
        try:
            user = User.query.filter_by(login_ac=login_ac).first()
            if user.user_level == '0':
                if user and str(user.passwd) == str(passwd):
                    if user.status=='0':
                        user.last_time=  newtime
                        db.session.commit()
                        session['leval'] = 0
                        return json.dumps({'code': 200, 'user': login_ac})
                    else:
                        return json.dumps({'code': 500, 'message': u'用户名已过期，请重新注册'})

                else:
                    return json.dumps({'code': 500, 'message': u'用户名或密码不正确'})
            else:
                if user and str(user.passwd) == str(passwd):
                    if user.status=='0':
                        user.last_time = newtime
                        db.session.commit()
                        session['leval'] = 1
                        return json.dumps({'code': 200, 'user': login_ac})
                    else:
                        return json.dumps({'code': 500, 'message': u'用户名已过期，请重新注册'})
                else:
                    return json.dumps({'code': 500, 'message': u'用户名或密码不正确'})

        except Exception as e:
            return json.dumps({'code':500, 'message':u'用户名或密码不正确'})
@login.route('/zhucepage')
def zhucepage():
    return render_template('zhuce.html')
@login.route('/zhuceinfo', methods=["POST"])
def zhuceinfo():
    if request.method == "POST":
        data = request.get_json(force=True)
        login_ac = data['email']
        passwd = data['pwd']
        number = data['number']
        jiaose = data['jiaose']
        try:
            # 判断注册信息
            if  '@' not in str(login_ac) or '.com' not in str(login_ac):
                return json.dumps({'code': 500, 'message': u'邮箱格式不正确！'})
            if len(passwd) < 6:
                return json.dumps({'code': 500, 'message': u'密码不能少于6位！'})
            if len(number) != 11:
                return json.dumps({'code': 500, 'message': u'请填写正确的手机号码！'})
            user = User.query.filter_by(login_ac=login_ac).first()
            if user:
                return json.dumps({'code': 500, 'message': u'此邮箱已经注册！'})
            # 注册入表
            else:
                user_level = str(jiaose)
                create_time = datetime.datetime.strftime((datetime.datetime.now()),'%Y-%m-%d %H:%M:%S')
                last_time = create_time
                userinfodata = User(login_ac, passwd,number,user_level,create_time,last_time,'0','')
                db.session.add(userinfodata)
                db.session.commit()
                db.create_all()
                return json.dumps({'code': 200, 'message': u'注册成功！'})
        except Exception as e:
            return json.dumps({'code':500, 'message':u'请填写正确的个人信息'})