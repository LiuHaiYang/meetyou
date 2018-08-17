from flask import Blueprint,render_template,request,session,make_response,redirect
from models import Zhilianjob,Bossjob,Lagoujob
import json
import datetime
from main import auth
analysis = Blueprint('analysis', __name__)

@analysis.route('/analysis/analysis_statistics',methods=["GET"])
@auth.require_login
def analysis_statistics():
    if request.method == 'GET':
        newtime_w = datetime.datetime.strftime((datetime.datetime.now() - datetime.timedelta(days=7)), '%Y-%m-%d')
        newtime_m = datetime.datetime.strftime((datetime.datetime.now() - datetime.timedelta(days=30)), '%Y-%m-%d')
        newtime = datetime.datetime.strftime((datetime.datetime.now()), '%Y-%m-%d %H:%M:%S')

        bossjobs_w = Bossjob.query.filter(Bossjob.status == '0',Bossjob.releasetime>=newtime_w).count()
        bossjobs_m = Bossjob.query.filter(Bossjob.status == '0',Bossjob.releasetime>=newtime_m).count()
        bossjobs_all = Bossjob.query.filter(Bossjob.status == '0').count()
        bossjobs_out = Bossjob.query.filter(Bossjob.status != '0').count()

        lagoujobs_w = Lagoujob.query.filter(Lagoujob.status == '0',Lagoujob.releasetime>=newtime_w).count()
        lagoujobs_m = Lagoujob.query.filter(Lagoujob.status == '0',Lagoujob.releasetime>=newtime_m).count()
        lagoujobs_all = Lagoujob.query.filter(Lagoujob.status == '0',).count()
        lagoujobs_out = Lagoujob.query.filter(Lagoujob.status != '0',).count()

        zhilianjobs_w = Zhilianjob.query.filter(Zhilianjob.status == '0',Zhilianjob.releasetime>=newtime_w).count()
        zhilianjobs_m = Zhilianjob.query.filter(Zhilianjob.status == '0',Zhilianjob.releasetime>=newtime_m).count()
        zhilianjobs_all = Zhilianjob.query.filter(Zhilianjob.status == '0').count()
        zhilianjobs_out = Zhilianjob.query.filter(Zhilianjob.status != '0').count()
        data = [['BOSS网',bossjobs_w,bossjobs_m,bossjobs_all,bossjobs_out,newtime],['拉勾网',lagoujobs_w,lagoujobs_m,lagoujobs_all,lagoujobs_out,newtime],
                ['智联网',zhilianjobs_w,zhilianjobs_m,zhilianjobs_all,zhilianjobs_out,newtime]]

        return render_template('analysis_statistics.html',datas = data)



@analysis.route('/analysis/analysis_area',methods=["GET"])
@auth.require_login
def analysis_area():
    if request.method == 'GET':
        return render_template('analysis_area.html')

@analysis.route('/analysis/analysis_association',methods=["GET"])
@auth.require_login
def analysis_association():
    if request.method == 'GET':
        return render_template('analysis_association.html')
