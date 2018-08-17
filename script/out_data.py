from flask import Blueprint,render_template,request,session,make_response,redirect
from models import Bossjob,Lagoujob,Zhilianjob
import datetime
from main import db

def outdata():
    try:
        newtime = datetime.datetime.strftime((datetime.datetime.now() - datetime.timedelta(days=30)), '%Y-%m-%d')
        bossjobs = Bossjob.query.filter(Bossjob.status == '0',Bossjob.date<newtime).all()
        for i in bossjobs:
           i.status ='1'
           db.session.commit()
        lagoujobs = Lagoujob.query.filter(Lagoujob.status == '0',Lagoujob.date<newtime).all()
        for i in lagoujobs:
            i.status = '1'
            db.session.commit()
        zhilianjobs = Zhilianjob.query.filter(Zhilianjob.status == '0',Zhilianjob.date<newtime).all()
        for i in zhilianjobs:
            i.status = '1'
            db.session.commit()
        return
    except Exception:
        return