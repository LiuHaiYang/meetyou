from flask import Blueprint,render_template,request,session,make_response,redirect
from models import Bossjob,Lagoujob,Zhilianjob,User
import json
import datetime
from main import db
from main import auth
homepage = Blueprint('homepage', __name__)


@homepage.route('/home', methods=["GET"])
@auth.require_login
def home_page():
    if request.method == "GET":
        return render_template('index_base.html')

@homepage.route('/home/alldata', methods=["GET"])
@auth.require_login
def home_alldata():
    if request.method == "GET":
        return render_template('alldata.html')

@homepage.route('/home/newdata', methods=["GET"])
@auth.require_login
def home_newdata():
    if request.method == "GET":
        return render_template('newjobdata.html')

@homepage.route('/home/hotdata', methods=["GET"])
@auth.require_login
def home_hotdata():
    if request.method == "GET":
        return render_template('hotjobdata.html')

@homepage.route('/home/alldatas_tableshow', methods=["GET"])
@auth.require_login
def showdata_table():
    datas_boss = []
    datas_lagou = []
    datas_zhilian = []
    bossjobs = Bossjob.query.filter(Bossjob.status=='0').all()
    for i in bossjobs:
        datas_boss.append([i.jobname,i.companyname,i.companytype,i.degree,i.money,i.worktime,i.address,i.platform,i.releasetime,i.id])
    lagoujobs = Lagoujob.query.filter(Lagoujob.status=='0').all()
    for i in lagoujobs:
        datas_lagou.append([i.jobname,i.companyname,i.companytype,i.degree,i.money,i.worktime,i.address,i.platform,i.releasetime,i.id])
    zhilianjobs = Zhilianjob.query.filter(Zhilianjob.status=='0').all()
    for i in zhilianjobs:
        datas_zhilian.append([i.jobname,i.companyname,i.companytype,i.degree,i.money,i.worktime,i.address,i.platform,i.releasetime,i.id])
    datas = datas_boss+datas_lagou+datas_zhilian
    data = {}
    data['data']=datas
    return json.dumps(data)

@homepage.route('/home/alldatas_tableshow_new', methods=["GET"])
@auth.require_login
def showdata_table_new():
    datas_boss = []
    datas_lagou = []
    datas_zhilian = []
    newtime = datetime.datetime.strftime((datetime.datetime.now()-datetime.timedelta(days=1)),'%Y-%m-%d')

    bossjobs = Bossjob.query.filter(Bossjob.status=='0',Bossjob.releasetime>newtime).all()
    for i in bossjobs:
        datas_boss.append([i.jobname,i.companyname,i.companytype,i.degree,i.money,i.worktime,i.address,i.platform,i.releasetime,i.id])
    lagoujobs = Lagoujob.query.filter(Lagoujob.status=='0',Lagoujob.releasetime>newtime).all()
    for i in lagoujobs:
        datas_lagou.append([i.jobname,i.companyname,i.companytype,i.degree,i.money,i.worktime,i.address,i.platform,i.releasetime,i.id])
    zhilianjobs = Zhilianjob.query.filter(Zhilianjob.status=='0',Zhilianjob.releasetime>newtime).all()
    for i in zhilianjobs:
        datas_zhilian.append([i.jobname,i.companyname,i.companytype,i.degree,i.money,i.worktime,i.address,i.platform,i.releasetime,i.id])
    datas = datas_boss+datas_lagou+datas_zhilian
    data = {}
    data['data']=datas
    return json.dumps(data)

# /getjobinfo
@homepage.route('/getjobinfo', methods=["GET","POST"])
@auth.require_login
def showdata_table_getjobinfo():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id = data['id']
        platform = data['platform']
        if platform == 'boss':
            jobinfo = Bossjob.query.filter(Bossjob.id ==int(id))
        elif platform == '拉勾':
            jobinfo = Lagoujob.query.filter(Lagoujob.id ==int(id))
        elif platform == '智联':
            jobinfo = Zhilianjob.query.filter(Zhilianjob.id == int(id))
        else:
            return json.dumps({'code': 500, 'message': u'获取详情失败！'})
        datainfo_job = []
        for i in jobinfo:
            datainfo_job.append([i.id,i.platform, i.companyname, i.companytype, i.companylevel, i.jobname, i.releasetime, i.date, \
                                i.address, i.requirements, i.worddata, i.welfare, i.degree, i.money, i.worktime, i.jobdesc, i.companydesc])
        data = {}
        data['code']=200
        data['data'] = datainfo_job
        return json.dumps(data)

@homepage.route('/userdata', methods=["GET","POST"])
@auth.require_login
def userdata():
    if request.method == 'GET':
        return render_template('userdata.html')
@homepage.route('/user_data_all', methods=["GET","POST"])
@auth.require_login
def userdata_all():
    datas_user = []
    users = User.query.filter(User.status =='0').all()

    for i in users:
        user_level = i.user_level
        if user_level =='0':
            user_level='普通用户'
        else:
            user_level ='管理员'
        datas_user.append([i.id,i.login_ac,user_level,i.number,i.create_time,i.last_time])
    data = {}
    data['data'] = datas_user
    return json.dumps(data)

# changejobinfo
@homepage.route('/changejobinfo', methods=["GET","POST"])
@auth.require_login
def changejobinfo():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id = data['id']
        platform = data['platform']
        if platform == 'boss':
            jobinfo = Bossjob.query.filter(Bossjob.id == int(id)).first()
        elif platform == '拉勾':
            jobinfo = Lagoujob.query.filter(Lagoujob.id == int(id)).first()
        elif platform == '智联':
            jobinfo = Zhilianjob.query.filter(Zhilianjob.id == int(id)).first()
        else:
            return json.dumps({'code': 500, 'message': u'删除失败！'})
        jobinfo.status = '1'
        db.session.commit()
        return json.dumps({'code': 200, 'message': u'ok！'})

# changeuserstatus
@homepage.route('/changeuserstatus', methods=["GET","POST"])
@auth.require_login
def changeuserstatus():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            id = data['id']
            user_info = User.query.filter(User.id==id).first()
            user_info.status = '1'
            db.session.commit()
            return json.dumps({'code': 200, 'message': u'ok！'})
        except:
            return json.dumps({'code': 500, 'message': u'删除失败！'})

# /edituserinfo
@homepage.route('/edituserinfo', methods=["GET","POST"])
@auth.require_login
def edituserinfo():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            print(data)
            id = data['id']
            user_name = data['user_name']
            user_number = data['user_number']
            user_level = data['user_level']
            user_info = User.query.filter(User.id==id).first()
            user_info.login_ac =user_name
            user_info.number =user_number
            user_info.user_level =user_level
            db.session.commit()
            return json.dumps({'code': 200})
        except:
            return json.dumps({'code': 500, 'message': u'编辑信息失败！'})


# /addlove_list
@homepage.route('/addlove_list', methods=["GET","POST"])
@auth.require_login
def addlove_list():
    if request.method == 'POST':
        data = request.get_json(force=True)
        try:
            id = data['id']
            login_ac = session['user']
            user_d = User.query.filter(User.login_ac==login_ac).first()
            if user_d.love_list:
                love_list = str(user_d.love_list) + ','+id
            else:
                love_list=id
            user_d.love_list =love_list
            db.session.commit()
            return json.dumps({'code': 200})
        except:
            return json.dumps({'code': 500 ,'message': u'添加喜爱失败！'})

@homepage.route('/home/shoucang_list', methods=["GET", "POST"])
@auth.require_login
def shoucang_list():
    if request.method == 'GET':
        return render_template('shoucangdata.html')
# /home/shoucang_list
@homepage.route('/home/shoucang_list_data', methods=["GET","POST"])
@auth.require_login
def shoucang_list_data():
    if request.method == 'GET':
        login_ac = session['user']
        user_d = User.query.filter(User.login_ac==login_ac).first()
        if user_d.love_list:
            love_list = user_d.love_list
            data_b = []
            data_z = []
            data_l = []
            for i in love_list.split(','):
                l = [j for j in i.split('-')]
                pl = l[0]
                id = l[1]
                if pl == 'boss':
                    jobinfo = Bossjob.query.filter(Bossjob.id == int(id),Bossjob.status=='0').all()
                    for i in jobinfo:
                        data_b.append(
                            [i.jobname, i.companyname, i.companytype, i.degree, i.money, i.worktime, i.address,
                             i.platform,
                             i.releasetime, i.id])
                elif pl == '拉勾'or pl =='lagou':
                    jobinfo = Lagoujob.query.filter(Lagoujob.id == int(id),Lagoujob.status=='0').all()
                    for i in jobinfo:
                        data_l.append(
                            [i.jobname, i.companyname, i.companytype, i.degree, i.money, i.worktime, i.address,
                             i.platform,
                             i.releasetime, i.id])
                elif pl == '智联'or pl == 'zhilian':
                    jobinfo = Zhilianjob.query.filter(Zhilianjob.id == int(id),Zhilianjob.status=='0').all()
                    for i in jobinfo:
                        data_z.append(
                            [i.jobname, i.companyname, i.companytype, i.degree, i.money, i.worktime, i.address,
                             i.platform,
                             i.releasetime, i.id])
                else:
                    pass
            datas = data_b + data_l +data_z

        else:
            datas= []
        data = {}
        data['data'] = datas
        return json.dumps(data)
# /changejobinfo_status
@homepage.route('/home/changejobinfo_status', methods=["GET","POST"])
@auth.require_login
def shoucang_changejobinfo_status():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id = data['id']
        pl = data['platform']
        love_l = pl+'-'+id
        login_ac = session['user']
        user_d = User.query.filter(User.login_ac==login_ac).first()
        if user_d.love_list:
            love_list = user_d.love_list
            love_list_data = [i for i in love_list.split(',')]
            love_list_data.remove(love_l)
            love_d = ','.join(love_list_data)
            user_d.love_list=love_d
            db.session.commit()
            return json.dumps({'code': 20, 'message': u'ok！'})
        else:
            return json.dumps({'code': 500, 'message': u'删除收藏信息失败！'})


