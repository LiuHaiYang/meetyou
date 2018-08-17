from flask import Blueprint,render_template,request,session,make_response,redirect
from models import Zhilianjob,Bossjob,Lagoujob
import json
import datetime
from main import auth
companys = Blueprint('companys', __name__)

@companys.route('/companys/lagouweb',methods=["GET"])
@auth.require_login
def companys_lagou():
    if request.method == 'GET':
        return render_template('web_lagou.html')

@companys.route('/companys/bossweb',methods=["GET"])
@auth.require_login
def companys_boss():
    if request.method == 'GET':
        return render_template('web_boss.html')

@companys.route('/companys/zhilianweb',methods=["GET"])
@auth.require_login
def companys_zhilian():
    if request.method == 'GET':
        return render_template('web_zhilian.html')

@companys.route('/companys/zhilianweb_datas',methods=["GET"])
@auth.require_login
def companys_zhilian_dats():
    datas_zhilian = []
    zhilianjobs = Zhilianjob.query.filter(Zhilianjob.status=='0').all()
    for i in zhilianjobs:
         datas_zhilian.append([i.jobname,i.companyname,i.companytype,i.degree,i.money,i.worktime,i.address,i.platform,i.releasetime,i.id])
    data = {}
    data['data'] = datas_zhilian
    return json.dumps(data)

@companys.route('/companys/lagouweb_datas',methods=["GET"])
@auth.require_login
def companys_lagou_dats():
    datas_lagou = []
    lagoujobs = Lagoujob.query.filter(Lagoujob.status=='0').all()
    for i in lagoujobs:
        datas_lagou.append([i.jobname,i.companyname,i.companytype,i.degree,i.money,i.worktime,i.address,i.platform,i.releasetime,i.id])
    data = {}
    data['data'] = datas_lagou
    return json.dumps(data)

@companys.route('/companys/bossweb_datas',methods=["GET"])
@auth.require_login
def companys_boss_dats():
    datas_boss = []
    bossjobs = Bossjob.query.filter(Bossjob.status=='0').all()
    for i in bossjobs:
        datas_boss.append([i.jobname,i.companyname,i.companytype,i.degree,i.money,i.worktime,i.address,i.platform,i.releasetime,i.id])
    data = {}
    data['data'] = datas_boss
    return json.dumps(data)