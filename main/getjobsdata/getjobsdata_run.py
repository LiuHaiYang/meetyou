from flask import Blueprint,render_template,request,session,make_response,redirect
from models import Bossjob,Lagoujob,Zhilianjob,Runhistory
import json
from main import db
import datetime
import os
from threading import Thread
from main import auth
from script.lagou.get_lagou_jobs import get_lagou_data
from script.boss.get_boss_jobs import get_boss_data
from script.zhilian.get_zhilian_jobs import get_zhilian_data
getjobdata = Blueprint('getjobdata', __name__)

@getjobdata.route('/getjobsdata_run', methods=["GET"])
@auth.require_login
def getjobdata_run():
    return render_template('getjobsdata_run.html')

@getjobdata.route('/getjobsdata_run_his', methods=["GET"])
@auth.require_login
def getjobdata_run_his():
    return render_template('getjobsdata_run_his.html')

@getjobdata.route('/getjobsdata_run_hisdata', methods=["GET"])
@auth.require_login
def getjobdata_run_hisdata():
    run_his = []
    run_his_data = Runhistory.query.order_by(Runhistory.id.desc())
    for i in run_his_data:
        run_his.append([i.id,i.data_web, i.data_tianjian,i.every_time,i.start_time,i.operator,i.status,i.stop_time])
    data = {}
    data['data']=run_his
    return json.dumps(data)


@getjobdata.route('/change_hisjobstatus', methods=["POST"])
@auth.require_login
def change_run_status():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id = data['id']
        #更新数据库
        newtime = datetime.datetime.strftime((datetime.datetime.now() ), '%Y-%m-%d %H:%M:%S')
        his_d = Runhistory.query.filter(Runhistory.id == id).first()
        his_d.status = '停止'
        his_d.stop_time = newtime
        db.session.commit()
        return json.dumps({'code': 200, 'message': u'该运行命令已停止！'})

@getjobdata.route('/insert_rundata', methods=["POST"])
@auth.require_login
def insert_run_data():
    if request.method == 'POST':
        data = request.get_json(force=True)
        try:
            webname = data['web_data']
            everytime = data['every_time']
            datafilter = data['data_filter']
            #插入数据库
            newtime = datetime.datetime.strftime((datetime.datetime.now() ), '%Y-%m-%d %H:%M:%S')
            everytimes = str(everytime)+'小时'
            run_insert = Runhistory(status = '运行',data_web = webname,data_tianjian = datafilter,every_time = everytimes,start_time = newtime,operator = session['user'],stop_time = '')
            # 添加person对象，但是仍然没有commit到数据库
            db.session.add(run_insert)
            # commit操作
            db.session.commit()
            # #并执行脚本 添加定时命令 运行，
            getdata_run(webname,everytime,datafilter)
            # os.system("python3 C:\\Users\samsung1\Desktop\meetyou\script\\boss\get_boss_jobs.py 1 2 3")
            return json.dumps({'code': 200, 'message': u'ok！'})
        except:
            return json.dumps({'code': 500, 'message': u'添加运行命令失败！'})

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper
#启动 停止 推荐脚本
@async
def  getdata_run(webname,everytime,datafilter):
    print((webname,everytime,datafilter))
    if webname =='BOSS':
        get_boss_data()
    elif webname=='拉勾':
        get_lagou_data()
    elif webname == '智联':
        get_zhilian_data()
    else:
        pass
    return
