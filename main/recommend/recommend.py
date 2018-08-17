from flask import Blueprint,render_template,request,session,make_response,redirect
from models import Userinfo,User,Recommenddata,Bossjob,Lagoujob,Zhilianjob
import json
from main import auth
from main import db
import datetime
import time
from send_email import send_email
import asyncio
import sys
from threading import Thread
recommend = Blueprint('recommend', __name__)

@auth.require_login
@recommend.route('/recommend_perinfo')
def recommend_per():
    return render_template('recommend_perinfo.html')

@auth.require_login
@recommend.route('/recommend_perinfo_all')
def recommend_all():
    return render_template('recommend_perinfo_all.html')

@auth.require_login
@recommend.route('/recommend_all_data')
def recommend_all_data():
    login_ac = session.get('user')
    if login_ac:
        user_l = User.query.filter_by(login_ac=login_ac).first().user_level
    else:
        data = {}
        data['data'] = []
        return json.dumps(data)
    if str(user_l) == '1':
        userinfo_all_data = []
        userinfo_all = Userinfo.query.filter(Userinfo.user_status==0).all()
        for i in userinfo_all:
            userinfo_all_data.append([i.id,i.username,i.sex,i.intersert_hangye,i.hope_money,i.hope_city,i.worktime,i.live_city,i.job_key,
                                      i.hpone_number,i.email,i.stop_time])
        data = {}
        data['data']=userinfo_all_data
    else:
        data = {}
        data['data'] = []
    return json.dumps(data)
@auth.require_login
@recommend.route('/recommend_perinfo_all_p')
def recommend_per_all():
    login_ac = session.get('user')
    if login_ac:
        user_id = User.query.filter_by(login_ac=login_ac).first().id
    else:
        data = {}
        data['data'] = []
        return json.dumps(data)
    userinfo_all_data = []
    userinfo_all = Userinfo.query.filter(Userinfo.user_status==0,Userinfo.user_id==user_id).all()
    for i in userinfo_all:
        userinfo_all_data.append([i.id,i.username,i.sex,i.intersert_hangye,i.hope_money,i.hope_city,i.worktime,i.live_city,i.job_key,
                                  i.hpone_number,i.email,i.stop_time])
    data = {}
    data['data']=userinfo_all_data
    return json.dumps(data)

@auth.require_login
@recommend.route('/recommend_perinfo_addinfo',methods=["GET","POST"])
def recommend_per_addinfo():
    if request.method == 'POST':
        data = request.get_json(force=True)
        try:
            login_ac = session['user']
            user_d = User.query.filter_by(login_ac=login_ac).first().id
            userinfo = Userinfo(username=data['name'],sex=data['sex'],intersert_hangye=data['hangyexingqu'],hope_money=data['hopemoney'],
                                hope_city=data['hope_city'],worktime=data['worktime'],live_city=data['live_city'],per_do=data['per_do'],
                                job_key=data['job_key'],user_id=user_d,hpone_number=data['phone'],email=data['email'],
                                user_level=0,user_type='普通',user_status=0,script_status=0,stop_time='')
            # username, sex, intersert_hangye, hope_money, hope_city, worktime, live_city, per_do, job_key, user_id, hpone_number, email, user_level, user_type, user_status
            db.session.add(userinfo)
            db.session.commit()
            db.create_all()
            return json.dumps({'code':200})
        except:
            return json.dumps({'code':500,'data':'添加失败！'})

@auth.require_login
@recommend.route('/recommend_data')
def recommend_data():
    return render_template('recommend_data.html')
@auth.require_login
@recommend.route('/recommend_xietongdata')
def recommend_xietongdata():
    return render_template('recommend_xietongdata.html')
#启动
@auth.require_login
@recommend.route('/recommend_perinfo_start',methods=["GET","POST"])
def recommend_perinfo_start():
    if request.method == 'POST':
        data = request.get_json(force=True)
        try:
            UserStatus = Userinfo.query.filter_by(id=data['id']).first()
            if int(UserStatus.script_status) == 0:
                UserStatus.script_status = 1
                UserStatus.stop_time = ''
                db.session.commit()
                recommend_script(data['id'])
                recommend_script_xietong(data['id'])
                return json.dumps({'code':200,'data': '已启动此推荐！'})
            else:
                return json.dumps({'code': 500, 'data': '请先停止此推荐！'})
        except:
            return json.dumps({'code':500,'data':'启动此推荐失败！'})
#停止
@auth.require_login
@recommend.route('/recommend_perinfo_stop',methods=["GET","POST"])
def recommend_perinfo_stop():
    if request.method == 'POST':
        data = request.get_json(force=True)
        try:
            UserStatus = Userinfo.query.filter_by(id=data['id']).first()
            if int(UserStatus.script_status) == 1:
                UserStatus.script_status = 0
                newtime = datetime.datetime.strftime((datetime.datetime.now()), '%Y-%m-%d %H:%M:%S')
                UserStatus.stop_time = newtime
                db.session.commit()
                return json.dumps({'code':200,'data': '已停止此推荐！'})
            else:
                return json.dumps({'code': 500, 'data': '此推荐未启动！'})
        except:
            return json.dumps({'code':500,'data':'停止此推荐失败！'})

@auth.require_login
@recommend.route('/recommend_perinfo_changestatus',methods=["GET","POST"])
def recommend_perinfo_change():
    if request.method == 'POST':
        data = request.get_json(force=True)
        try:
            UserStatus = Userinfo.query.filter_by(id=data['id']).first()
            if int(UserStatus.script_status) == 0:
                UserStatus.user_status = 1
                db.session.commit()
                return json.dumps({'code':200,'data': '已成功删除此推荐！'})
            else:
                return json.dumps({'code': 500, 'data': '请先停止此推荐！'})
        except:
            return json.dumps({'code':500,'data':'修改状态失败！'})


@auth.require_login
@recommend.route('/recommend_historyall',methods=["GET","POST"])
def recommend_historyall():
    return render_template('recommend_historyall.html')

#推荐归档data
@auth.require_login
@recommend.route('/recommend_historyall_data', methods=["GET", "POST"])
def recommend_historyall_data():
    login_ac = session.get('user')
    if login_ac:
        user_id = User.query.filter(User.login_ac==login_ac).first().id
    else:
        data = {}
        data['data'] = []
        return json.dumps(data)
    per_recommend_info = Recommenddata.query.filter(Recommenddata.user_id==user_id).all()
    data = []
    for i in  per_recommend_info:
        data.append([i.re_id,i.user_id,i.platom,i.jobname,i.companyname,i.money,i.worktime,i.city,i.youhuo])
    datas = {}
    datas['data'] = data
    return json.dumps(datas)

#查询推荐
@auth.require_login
@recommend.route('/recommend_query_all',methods=["GET","POST"])
def recommend_query_all():
    login_ac = session.get('user')
    if login_ac:
        user_id = User.query.filter_by(login_ac=login_ac).first().id
    else:
        data = {}
        data['data'] = []
        return json.dumps(data)
    newtime = datetime.datetime.strftime((datetime.datetime.now() - datetime.timedelta(days=1)), '%Y-%m-%d %H:%M:%S')
    per_recommend_info = Recommenddata.query.filter(Recommenddata.user_id==user_id,Recommenddata.recommend_type==0,Recommenddata.re_time>=newtime).all()
    data = []
    for i in  per_recommend_info:
        data.append([i.re_id,i.user_id,i.platom,i.jobname,i.companyname,i.money,i.worktime,i.city,i.youhuo])
    datas = {}
    datas['data'] = data
    return json.dumps(datas)
#协同推荐
@auth.require_login
@recommend.route('/recommend_xietong_all', methods=["GET", "POST"])
def recommend_xietong_all():
    login_ac = session.get('user')
    if login_ac:
        user_id = User.query.filter_by(login_ac=login_ac).first().id
    else:
        data = {}
        data['data'] = []
        return json.dumps(data)
    newtime = datetime.datetime.strftime((datetime.datetime.now() - datetime.timedelta(days=1)), '%Y-%m-%d %H:%M:%S')
    per_recommend_info = Recommenddata.query.filter(Recommenddata.user_id==user_id, Recommenddata.recommend_type==1,Recommenddata.re_time>=newtime).all()
    data = []
    for i in per_recommend_info:
        data.append([i.re_id, i.user_id, i.platom, i.jobname, i.companyname, i.money, i.worktime, i.city, i.youhuo])
    datas = {}
    datas['data'] = data
    return json.dumps(datas)

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper
#启动 停止 推荐脚本
@async
def recommend_script(id):
    while 1:
        print('Query!!')
        per_info = Userinfo.query.filter_by(id=id).first()
        db.session.commit()
        if int(per_info.script_status) ==1:
            #启动状态进行查询并保存
            intersert_hangye =per_info.intersert_hangye # 期望薪资
            intersert_hangye = intersert_hangye if intersert_hangye  else '%'
            hope_money =per_info.hope_money # 期望薪资
            hope_money = hope_money if hope_money  else '%'
            hope_city =per_info.hope_city # 期望城市
            hope_city = hope_city if hope_city  else '%'
            worktime =per_info.worktime # 工作经验
            worktime = worktime if worktime  else '%'
            per_do=per_info.per_do  # 个人技能
            per_do = per_do if per_do  else '%'
            job_key=per_info.job_key  # 关键词
            job_key = job_key if job_key  else '%'
            user_id  =per_info.user_id# 用户id
            hpone_number=per_info.hpone_number  # 用户手机号码
            email =per_info.email # 邮箱
            newtime_s = datetime.datetime.strftime((datetime.datetime.now()- datetime.timedelta(minutes=0.5*60)), '%Y-%m-%d %H:%M:%S')
            newtime_end = datetime.datetime.strftime((datetime.datetime.now() - datetime.timedelta(minutes=1*60)),  '%Y-%m-%d %H:%M:%S')

            datas_boss = []
            datas_lagou = []
            datas_zhilian = []
            bossjobs = Bossjob.query.filter(Bossjob.status == '0',
                                            Bossjob.jobname.like('%'+job_key+'%'),
                                            Bossjob.companytype.like('%'+intersert_hangye+'%'),
                                            Bossjob.money.like('%' + hope_money + '%'),
                                            Bossjob.worktime.like('%' + worktime + '%'),
                                            Bossjob.address.like('%' + hope_city + '%'),
                                            Bossjob.releasetime >=newtime_end,
                                            Bossjob.releasetime<=newtime_s
                                            ).all()

            # { title: "序号" }, "推荐用户ID" },: "平台" }, "职位名称" }, "公司名称" },
            # { title: "薪资" },: "工作经验" },: "城市" },位诱惑" }
            for i in bossjobs:
                datas_boss.append(
                    [i.id, user_id,'BOSS', i.jobname, i.companyname, i.money, i.worktime, i.address, i.welfare])

            lagoujobs = Lagoujob.query.filter(Lagoujob.status == '0',
                                              Lagoujob.jobname.like('%' + job_key + '%'),
                                              Lagoujob.companytype.like('%' + intersert_hangye + '%'),
                                              Lagoujob.money.like('%' + hope_money + '%'),
                                              Lagoujob.worktime.like('%' + worktime + '%'),
                                              Lagoujob.address.like('%' + hope_city + '%'),
                                              Lagoujob.releasetime >= newtime_end,
                                              Lagoujob.releasetime <= newtime_s
                                            ).all()
            for i in lagoujobs:
                datas_lagou.append(
                    [i.id, user_id, '拉勾', i.jobname, i.companyname, i.money, i.worktime, i.address, i.welfare])

            zhilianjobs = Zhilianjob.query.filter(Zhilianjob.status == '0',
                                                  Zhilianjob.jobname.like('%' + job_key + '%'),
                                                  Zhilianjob.companytype.like('%' + intersert_hangye + '%'),
                                                  Zhilianjob.money.like('%' + hope_money + '%'),
                                                  Zhilianjob.worktime.like('%' + worktime + '%'),
                                                  Zhilianjob.address.like('%' + hope_city + '%'),
                                                  Zhilianjob.releasetime >= newtime_end,
                                                  Zhilianjob.releasetime <= newtime_s
                                            ).all()
            for i in zhilianjobs:
                datas_zhilian.append(
                    [i.id, user_id, '智联', i.jobname, i.companyname, i.money, i.worktime, i.address, i.welfare])

            datas = datas_boss + datas_lagou + datas_zhilian
            #查询出来后进行入库
            for i in datas:
                # id =   platom  user_id jobname = companyname  money =   worktime   city =
                # youhuo         zhize =        yaoqiu =       recommend_type =     # re_time =
                re_data_in = Recommenddata(i[0],i[2],i[1],i[3],i[4],i[5],i[6],i[7],i[8],'','',0,newtime_s)
                db.session.add(re_data_in)
                db.session.commit()
            print('筛选入库 ok!')
            #邮件通知
            time.sleep(60*30)#每五分钟进行一次查询,推荐。改变状态不能及时的停止
            try:
                send_email(str(email), 'Ocan job 查询推荐提醒！')
            except:
                print('send email fail!')
        else:
            print('stop')
            break
    return

@async
def recommend_script_xietong(id_u):
    while 1:
        print('协同！！',id_u)
        ids_u = id_u
        per_info = Userinfo.query.filter(Userinfo.id==ids_u).first()
        db.session.commit()
        if int(per_info.script_status) ==1:
            #启动状态进行查询并保存
            intersert_hangye =per_info.intersert_hangye # 期望薪资
            intersert_hangye = intersert_hangye if intersert_hangye  else '%'
            hope_money =per_info.hope_money # 期望薪资
            hope_money = hope_money if hope_money  else '%'
            hope_city =per_info.hope_city # 期望城市
            hope_city = hope_city if hope_city  else '%'
            worktime =per_info.worktime # 工作经验
            worktime = worktime if worktime  else '%'
            per_do=per_info.per_do  # 个人技能
            per_do = per_do if per_do  else '%'
            job_key=per_info.job_key  # 关键词
            job_key = job_key if job_key  else '%'
            user_id_d  =per_info.user_id# 用户id

            hpone_number=per_info.hpone_number  # 用户手机号码
            email =per_info.email # 邮箱
            newtime_s = datetime.datetime.strftime((datetime.datetime.now()- datetime.timedelta(minutes=0.5*60)), '%Y-%m-%d %H:%M:%S')
            newtime_end = datetime.datetime.strftime((datetime.datetime.now() - datetime.timedelta(minutes=1*60)),  '%Y-%m-%d %H:%M:%S')

            users_love = Userinfo.query.filter(Userinfo.hope_city.like('%' + hope_city + '%'),
                                               Userinfo.hope_money.like('%' + hope_money + '%'),
                                               Userinfo.intersert_hangye.like('%' + intersert_hangye + '%'),
                                               Userinfo.worktime.like('%' + worktime + '%'),
                                               Userinfo.job_key.like('%' + job_key + '%')).all()
            love_d = []
            for i in users_love:
                user_id = i.user_id
                user_love = User.query.filter(User.id==user_id).first()
                love_list = user_love.love_list
                love_l = [j for j in love_list.split(',')][:-3]
                love_d.append(love_l)
            k = []
            for m in love_d:
                k+=m
            datas_boss = []
            datas_lagou = []
            datas_zhilian = []
            for i in k:
                p = [j for j in i.split('-')]
                pl = p[0]
                id = p[1]
                if pl == 'boss':
                    bossjobs = Bossjob.query.filter(Bossjob.id==id,Bossjob.status=='0').all()
                    # { title: "序号" }, "推荐用户ID" },: "平台" }, "职位名称" }, "公司名称" },
                    # { title: "薪资" },: "工作经验" },: "城市" },位诱惑" }
                    for i in bossjobs:
                        datas_boss.append(
                            [i.id, user_id_d,'BOSS', i.jobname, i.companyname, i.money, i.worktime, i.address, i.welfare])
                elif pl =='拉勾':
                    lagoujobs = Lagoujob.query.filter(Lagoujob.id==id,Lagoujob.status=='0').all()
                    for i in lagoujobs:
                        datas_lagou.append(
                            [i.id, user_id_d, '拉勾', i.jobname, i.companyname, i.money, i.worktime, i.address, i.welfare])
                elif pl =='智联':
                    zhilianjobs = Zhilianjob.query.filter(Zhilianjob.id==id,Zhilianjob.status=='0').all()
                    for i in zhilianjobs:
                        datas_zhilian.append(
                            [i.id, user_id_d, '智联', i.jobname, i.companyname, i.money, i.worktime, i.address, i.welfare])
                else:
                    pass
                datas = datas_boss + datas_lagou + datas_zhilian
                #查询出来后进行入库
                for i in datas:
                    # id =   platom  user_id jobname = companyname  money =   worktime   city =
                    # youhuo         zhize =        yaoqiu =       recommend_type =     # re_time =
                    re_data_in = Recommenddata(i[0],i[2],i[1],i[3],i[4],i[5],i[6],i[7],i[8],'','',1,newtime_s)
                    db.session.add(re_data_in)
                    db.session.commit()
                print('协同入库 ok!')

            try:
                send_email(str(email), 'Ocan job 协同推荐提醒！')
            except:
                print('send email fail!')
            break
        else:
            print('stop')
            break
    return