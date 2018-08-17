from flask import Blueprint,render_template,request,session,make_response,redirect
from models import Zhilianjob,Bossjob,Lagoujob
import json
import datetime
from main import auth
about = Blueprint('about', __name__)


@about.route('/about/aboutpro',methods=["GET"])
@auth.require_login
def about_pro():
    if request.method == 'GET':
        return render_template('about_pro.html')



@about.route('/about/aboutdata',methods=["GET"])
@auth.require_login
def about_data():
    if request.method == 'GET':
        return render_template('about_data.html')
